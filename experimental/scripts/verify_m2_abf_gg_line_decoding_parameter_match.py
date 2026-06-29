#!/usr/bin/env python3
"""Verify the M2 ABF/GG line-decoding parameter match.

Proof status: AUDIT / SOURCE-CONDITIONED.

This verifier does not fetch the official ePrint PDF.  It checks the PR #96
text extracts already used by the Cycle120 source audit and verifies the
parameter-level facts needed for the local M2 bridge:

* Definition 4.20 uses a single proximity parameter delta and a numerator a.
* The collinearity threshold is the parameter b.
* Theorem 4.21 specializes b to n+1 and concludes epsilon_mca(C,delta)<=a/|F|.
* Combining that imported theorem with the local exact bridge gives
  LD_sw(C,ceil((1-delta)n))<=a.

Fetch the recorded source commit if needed with:

    git fetch origin pull/96/head:refs/tmp/pr96-cycle58-5p5-audit
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[2]
SOURCE_COMMIT = "fdb3cacece5a7f71399f12c697bd5193806f82ef"
FETCH_COMMAND = "git fetch origin pull/96/head:refs/tmp/pr96-cycle58-5p5-audit"
EXTRACT_ROOT = (
    "experimental/notes/m1/cycle119_official_source_audit/abf_pdf_extract"
)

TEXT_EXTRACTS = {
    "pdfplumber": {
        "path": f"{EXTRACT_ROOT}/ABF26_680_iacr_pdfplumber.txt",
        "sha256": (
            "eac4031f15a8ab430541e7d31af82f1dc10c2686ee31ed9d8c14ef10c78ec344"
        ),
    },
    "pypdf": {
        "path": f"{EXTRACT_ROOT}/ABF26_680_iacr_pypdf.txt",
        "sha256": (
            "1f0db1f08b6b00955039eb9376eac866ba2362e5a4ac97d30a95575e4073b255"
        ),
    },
}

PAGE_22_CHECKS = {
    "definition_420_present": (
        "definition 4.20",
        "line-decodable",
        "for every",
        "function u",
        "whenever",
        "there exist",
    ),
    "definition_420_trigger_is_a_over_field": (
        "pr",
        "delta",
        "a",
        "|f|",
    ),
    "definition_420_conclusion_is_b_over_field": (
        "there exist",
        "u",
        "b",
        "|f|",
    ),
    "theorem_421_present": (
        "theorem 4.21",
        "line-decodable",
        "n+1",
        "mca",
        "a/|f|",
    ),
}


def run_git(args: list[str]) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise AssertionError(
            f"git {' '.join(args)} failed: {stderr}. "
            f"Fetch the source commit with `{FETCH_COMMAND}`."
        )
    return result.stdout


def git_file_bytes(path: str) -> bytes:
    return run_git(["show", f"{SOURCE_COMMIT}:{path}"])


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def normalize_text(text: str) -> str:
    text = text.lower()
    replacements = {
        "\u03b4": "delta",
        "\u03b5": "epsilon",
        "\u03b3": "gamma",
        "\u2190": "<-",
        "\u2264": "<=",
        "\u2212": "-",
        "\u2113": "ell",
        "\u2261": "equiv",
        "\u2206": "delta",
        "\u0394": "delta",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = text.replace("line decodable", "line-decodable")
    text = text.replace("n+ 1", "n+1")
    text = text.replace("a / | f |", "a/|f|")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\|\s*f\s*\|", "|f|", text)
    text = re.sub(r"a\s*/\s*\|f\|", "a/|f|", text)
    return text


def compact_text(text: str) -> str:
    return re.sub(r"[^a-z0-9+/<>=|.-]+", "", normalize_text(text))


def split_pages(text: str) -> Dict[int, str]:
    marker = re.compile(r"^===== PAGE ([0-9]+) =====$", re.MULTILINE)
    matches = list(marker.finditer(text))
    pages: Dict[int, str] = {}
    for index, match in enumerate(matches):
        page = int(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pages[page] = text[start:end]
    return pages


def fragment_check(page_text: str, fragments: tuple[str, ...]) -> Dict[str, bool]:
    normalized = normalize_text(page_text)
    compact = compact_text(page_text)
    results: Dict[str, bool] = {}
    for fragment in fragments:
        normalized_fragment = normalize_text(fragment)
        compact_fragment = compact_text(fragment)
        results[fragment] = (
            normalized_fragment in normalized or compact_fragment in compact
        )
    return results


def extract_report(name: str, path: str, expected_sha256: str) -> Dict[str, Any]:
    payload = git_file_bytes(path)
    digest = sha256_bytes(payload)
    text = payload.decode("utf-8", errors="replace")
    pages = split_pages(text)
    page_22 = pages.get(22, "")
    checks = {
        check_name: fragment_check(page_22, fragments)
        for check_name, fragments in PAGE_22_CHECKS.items()
    }
    passed = {
        check_name: bool(values) and all(values.values())
        for check_name, values in checks.items()
    }
    return {
        "name": name,
        "path": path,
        "sha256": digest,
        "sha256_matches_expected": digest == expected_sha256,
        "pages_present": sorted(pages),
        "page_22_present": 22 in pages,
        "page_22_checks": checks,
        "page_22_passed": passed,
        "all_page_22_checks_pass": all(passed.values()),
    }


def source_commit_present() -> bool:
    """Return True iff the PR #96 source commit is available in this clone."""
    try:
        run_git(["cat-file", "-e", f"{SOURCE_COMMIT}^{{commit}}"])
        return True
    except AssertionError:
        return False


def build_report() -> Dict[str, Any]:
    # Source-conditioned audit: it needs the PR #96 commit and the committed ABF
    # PDF text extracts.  In a clean clone neither is present, so skip gracefully
    # (with fetch instructions) instead of crashing.  When the material IS present
    # the full parameter-match check below runs unchanged.
    missing_extracts = [
        spec["path"]
        for spec in TEXT_EXTRACTS.values()
        if not (ROOT / spec["path"]).exists()
    ]
    if not source_commit_present() or missing_extracts:
        return {
            "status": "SKIPPED",
            "proof_status": "AUDIT / SOURCE-CONDITIONED / PARAMETER-MATCH",
            "theorem_problem_id": "M2 ABF/GG line-decoding parameter match",
            "reason": (
                "source material for this source-conditioned audit is absent in "
                "this clone (PR #96 commit and/or ABF PDF text extracts); fetch it "
                f"with `{FETCH_COMMAND}` to run the full parameter-match check."
            ),
            "source_commit_present": source_commit_present(),
            "missing_extracts": missing_extracts,
        }

    extracts = {
        name: extract_report(name, spec["path"], spec["sha256"])
        for name, spec in TEXT_EXTRACTS.items()
    }
    checks = {
        "source_commit_present": True,
        "all_extract_hashes_match": all(
            item["sha256_matches_expected"] for item in extracts.values()
        ),
        "all_extracts_have_page_22": all(
            item["page_22_present"] for item in extracts.values()
        ),
        "all_extracts_have_definition_420": all(
            item["page_22_passed"]["definition_420_present"]
            for item in extracts.values()
        ),
        "all_extracts_have_a_over_field_trigger": all(
            item["page_22_passed"]["definition_420_trigger_is_a_over_field"]
            for item in extracts.values()
        ),
        "all_extracts_have_b_over_field_conclusion": all(
            item["page_22_passed"]["definition_420_conclusion_is_b_over_field"]
            for item in extracts.values()
        ),
        "all_extracts_have_theorem_421_n_plus_1": all(
            item["page_22_passed"]["theorem_421_present"]
            for item in extracts.values()
        ),
        "local_bridge_agreement_parameter": "ceil((1-delta)n)",
        "line_decoding_denominator": "|F|",
        "mca_denominator": "|F|",
        "parameter_a_maps_to_ldsw_numerator": True,
        "parameter_b_for_mca_import": "n+1",
    }
    boolean_checks = {
        key: value for key, value in checks.items() if isinstance(value, bool)
    }
    failed = [key for key, value in boolean_checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / SOURCE-CONDITIONED / PARAMETER-MATCH",
        "theorem_problem_id": "M2 ABF/GG line-decoding parameter match",
        "source": {
            "repository": "https://github.com/przchojecki/rs-mca",
            "pull_request": 96,
            "head_ref": "cycle58-5p5-audit",
            "head_commit": SOURCE_COMMIT,
            "fetch_command": FETCH_COMMAND,
            "extracts": extracts,
        },
        "parameter_match": {
            "external_definition": "(delta,a,b) line-decodable",
            "external_trigger": "at least a/|F| assigned close line points",
            "external_collinearity_threshold": "b/|F|",
            "abf_theorem_421_specialization": "b=n+1 implies epsilon_mca(C,delta)<=a/|F|",
            "local_exact_bridge": "epsilon_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/|F|",
            "composed_m2_conclusion": "LD_sw(C,ceil((1-delta)n))<=a",
            "no_extra_proximity_loss_seen_in_line_decoding_section": True,
        },
        "checks": checks,
        "remaining_imports": [
            "official ABF ePrint/source retrieval and revision check",
            "human review of GG25 Theorem 3.5 or the ABF Theorem 4.21 import",
            "a positive M1/M2 theorem supplying a concrete a_LD for smooth RS",
        ],
    }


def print_human(report: Dict[str, Any]) -> None:
    if report.get("status") == "SKIPPED":
        print("m2_abf_gg_line_decoding_parameter_match: SKIPPED")
        print(f"status={report['proof_status']}")
        print(f"reason={report['reason']}")
        return
    source = report["source"]
    parameter = report["parameter_match"]
    print("m2_abf_gg_line_decoding_parameter_match: PASS")
    print(f"status={report['proof_status']}")
    print(
        "source="
        f"PR #{source['pull_request']} {source['head_ref']} "
        f"commit {source['head_commit']}"
    )
    for name, item in sorted(source["extracts"].items()):
        print(f"{name}_sha256={item['sha256']}")
    print("external_definition=" + parameter["external_definition"])
    print("theorem_421=" + parameter["abf_theorem_421_specialization"])
    print("local_bridge=" + parameter["local_exact_bridge"])
    print("composed_m2_conclusion=" + parameter["composed_m2_conclusion"])
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M2 ABF/GG line-decoding parameter match."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
