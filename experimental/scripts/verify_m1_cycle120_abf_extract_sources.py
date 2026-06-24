#!/usr/bin/env python3
"""Verify the PR #96 ABF PDF-extract objects used by the Cycle120 gate audit.

The Cycle120 ABF-facing notes still require a human or maintainer to fetch and
review the official ePrint source directly.  This verifier checks a narrower
intermediate fact: the copied PDF, text extracts, rendered source pages, and
counterexample packet that were used in PR #96 are pinned to the recorded PR
head, and the two text extracts contain the source anchors cited by the local
Cycle120 gate audit.

The verifier is nonmutating but it requires the recorded PR #96 commit to be
present in the local Git object database.  Fetch it with:

    git fetch origin pull/96/head:refs/remotes/origin/pr-96
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_external_packet_contract as packet_contract


ROOT = packet_contract.ROOT
SOURCE_COMMIT = packet_contract.EXPECTED_HEAD_COMMIT
FETCH_COMMAND = "git fetch origin pull/96/head:refs/remotes/origin/pr-96"
EXTRACT_ROOT = (
    "experimental/notes/m1/cycle119_official_source_audit/abf_pdf_extract"
)

EXPECTED_GIT_OBJECTS = {
    "abf_pdf": {
        "path": f"{EXTRACT_ROOT}/ABF26_680_iacr.pdf",
        "mode": "100644",
        "blob": "928d294a9475cf67d0c30b16b478a6eaa228afb0",
        "size": 810836,
        "sha256": (
            "e543ec6a4f3312b4383000e72e5aa23862e79cc9770ce21db2c48db679581de3"
        ),
    },
    "pdfplumber_text": {
        "path": f"{EXTRACT_ROOT}/ABF26_680_iacr_pdfplumber.txt",
        "mode": "100644",
        "blob": "ce0f305a36968d5bc59da347b16a7b57ff75274b",
        "size": 120492,
        "sha256": (
            "eac4031f15a8ab430541e7d31af82f1dc10c2686ee31ed9d8c14ef10c78ec344"
        ),
    },
    "pypdf_text": {
        "path": f"{EXTRACT_ROOT}/ABF26_680_iacr_pypdf.txt",
        "mode": "100644",
        "blob": "1ae7fe12d0524aada94027d8a0d062cdc2ed4783",
        "size": 113185,
        "sha256": (
            "1f0db1f08b6b00955039eb9376eac866ba2362e5a4ac97d30a95575e4073b255"
        ),
    },
    "rendered_page_1": {
        "path": f"{EXTRACT_ROOT}/rendered/page-01.png",
        "mode": "100644",
        "blob": "5c57ab48c31857059dff4b68627974c1c49cd325",
        "size": 107437,
        "sha256": (
            "75465c0de094bce32b792ed24866e889abea859dd84666768973c4e9a054454c"
        ),
    },
    "rendered_page_2": {
        "path": f"{EXTRACT_ROOT}/rendered/page-02.png",
        "mode": "100644",
        "blob": "a504a18b52f69b5f08209341809b8ffe56e11fff",
        "size": 140174,
        "sha256": (
            "532e187a03b466e2aeaa6bd4faab749dc646162ff2952ea8da8bf73845af3b33"
        ),
    },
    "rendered_page_3": {
        "path": f"{EXTRACT_ROOT}/rendered/page-03.png",
        "mode": "100644",
        "blob": "bbaf45aae56468b0732a262140ee6c6d4ce060a7",
        "size": 382543,
        "sha256": (
            "79f083516c8ce2ab0dfd0048c1c2955824772e085d183dc098fa2787990422a7"
        ),
    },
    "rendered_page_5": {
        "path": f"{EXTRACT_ROOT}/rendered/page5-05.png",
        "mode": "100644",
        "blob": "727479a87e1d05809432782a5470bae2c7a7551b",
        "size": 437375,
        "sha256": (
            "5ebcf4cfd6f73ed871bb5f066e42048f55a827c3401b7b8ea2820cb745454245"
        ),
    },
    "rendered_page_9": {
        "path": f"{EXTRACT_ROOT}/rendered/page9-09.png",
        "mode": "100644",
        "blob": "2813569e6ec537ee12eb78515c055d1dbee55446",
        "size": 398818,
        "sha256": (
            "736feb90503e1bee835d5b98134b570261e6c78f2c3e2096a60e3834e8ea872f"
        ),
    },
    "rendered_page_10": {
        "path": f"{EXTRACT_ROOT}/rendered/page10-10.png",
        "mode": "100644",
        "blob": "86b336aa8f01491532b2988e18cfae56e474fc42",
        "size": 346956,
        "sha256": (
            "b5d5df0c5ea7131d2580f657ee0ab4a97b5737a9905dd1afbc9f6886b2624472"
        ),
    },
    "rendered_page_17": {
        "path": f"{EXTRACT_ROOT}/rendered/page17-17.png",
        "mode": "100644",
        "blob": "524634a3317f162468ec122516ad029f681c156d",
        "size": 431957,
        "sha256": (
            "661b1fc0e600e6cf076ae6b19a0aff9de85eaf391df227006b87d175ae730af3"
        ),
    },
    "cycle120_abf_packet_zip": {
        "path": "experimental/notes/m1/cycle120_abf_counterexample_packet.zip",
        "mode": "100644",
        "blob": "43e7d42ebabfe3c4cb1e2090938e9340625b81c4",
        "size": 21116,
        "sha256": (
            "da580c57f0cb9c6c56e3bab8106b4275ced3e8b4f876a410bf34f0b17ca538b2"
        ),
    },
    "cycle120_abf_packet_zip_sha256": {
        "path": "experimental/notes/m1/cycle120_abf_counterexample_packet.zip.sha256",
        "mode": "100644",
        "blob": "360ace35d5239c97628b8b330d9fc87684ec70d1",
        "size": 127,
        "sha256": (
            "698a207e53f291d436035bc6ece095972b10f54a641cfd6a96565a153b868319"
        ),
    },
}

RENDERED_SOURCE_PAGES = {
    5: "rendered_page_5",
    9: "rendered_page_9",
    17: "rendered_page_17",
}

TEXT_EXTRACTS = {
    "pdfplumber": "pdfplumber_text",
    "pypdf": "pypdf_text",
}

PAGE_FRAGMENT_CHECKS = {
    "page5_grand_mca_challenge": {
        "page": 5,
        "fragments": [
            "The grand MCA challenge",
            "Reed",
            "Solomon",
            "smooth",
            "rate",
            "128",
        ],
    },
    "page9_rs_and_smooth_definitions": {
        "page": 9,
        "fragments": [
            "Definition 2.11",
            "Definition 2.12",
            "finite field",
            "Reed",
            "Solomon",
            "power of two",
        ],
    },
    "page17_mca_definition": {
        "page": 17,
        "fragments": [
            "Definition 4.3",
            "mutual correlated agreement",
            "max",
            "Pr",
            "same",
            "size at least",
        ],
    },
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


def check_commit_present() -> None:
    run_git(["cat-file", "-e", f"{SOURCE_COMMIT}^{{commit}}"])


def git_object_info(path: str) -> Dict[str, Any]:
    raw = run_git(["ls-tree", "-l", SOURCE_COMMIT, "--", path])
    text = raw.decode("utf-8").strip()
    if not text:
        raise AssertionError(f"missing source path at {SOURCE_COMMIT}: {path}")
    fields = text.split(None, 4)
    if len(fields) != 5 or fields[1] != "blob":
        raise AssertionError(f"unexpected git ls-tree output: {text}")
    return {
        "mode": fields[0],
        "type": fields[1],
        "blob": fields[2],
        "size": int(fields[3]),
        "path": fields[4],
    }


def git_file_bytes(path: str) -> bytes:
    return run_git(["show", f"{SOURCE_COMMIT}:{path}"])


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def normalize_fragment_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


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


def fragment_report(text: str) -> Dict[str, Any]:
    pages = split_pages(text)
    checks: Dict[str, Dict[str, Any]] = {}
    for check_name, spec in PAGE_FRAGMENT_CHECKS.items():
        page = int(spec["page"])
        page_text = pages.get(page, "")
        normalized_page_text = normalize_fragment_text(page_text)
        fragments = {
            fragment: normalize_fragment_text(fragment) in normalized_page_text
            for fragment in spec["fragments"]
        }
        checks[check_name] = {
            "page": page,
            "page_present": page in pages,
            "fragments": fragments,
            "passed": page in pages and all(fragments.values()),
        }
    return {
        "pages_present": sorted(pages),
        "checks": checks,
    }


def build_report() -> Dict[str, Any]:
    check_commit_present()

    source_reports = {}
    payloads = {}
    checks = {
        "source_commit_present": True,
        "source_commit_matches_cycle116_external_packet_commit": (
            SOURCE_COMMIT == packet_contract.EXPECTED_HEAD_COMMIT
        ),
    }

    for name, expected in EXPECTED_GIT_OBJECTS.items():
        path = expected["path"]
        info = git_object_info(path)
        payload = git_file_bytes(path)
        digest = sha256_bytes(payload)
        payloads[name] = payload
        source_reports[name] = {
            "path": path,
            "mode": info["mode"],
            "blob": info["blob"],
            "size": info["size"],
            "sha256": digest,
        }
        checks[f"{name}_git_object_matches_expected"] = (
            info["mode"] == expected["mode"]
            and info["blob"] == expected["blob"]
            and info["size"] == expected["size"]
        )
        checks[f"{name}_sha256_matches_expected"] = digest == expected["sha256"]
        checks[f"{name}_payload_size_matches_git"] = len(payload) == info["size"]

    zip_digest_line = payloads["cycle120_abf_packet_zip_sha256"].decode("utf-8").strip()
    checks["packet_zip_sha256_file_matches_zip_payload"] = (
        zip_digest_line.split()[0]
        == source_reports["cycle120_abf_packet_zip"]["sha256"]
    )

    extract_reports = {}
    for extract_name, object_name in TEXT_EXTRACTS.items():
        text = payloads[object_name].decode("utf-8", errors="replace")
        report = fragment_report(text)
        extract_reports[extract_name] = report
        for check_name, check_report in report["checks"].items():
            checks[f"{extract_name}_{check_name}_passed"] = bool(
                check_report["passed"]
            )

    checks["critical_rendered_source_pages_present"] = all(
        name in source_reports for name in RENDERED_SOURCE_PAGES.values()
    )

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / ABF-PDF-EXTRACT-SOURCES-VERIFIED",
        "theorem_problem_id": "M1 Cycle120 ABF PDF extract source audit",
        "source": {
            "repository": "https://github.com/przchojecki/rs-mca",
            "pull_request": 96,
            "head_ref": "cycle58-5p5-audit",
            "head_commit": SOURCE_COMMIT,
            "fetch_command": FETCH_COMMAND,
            "files": source_reports,
        },
        "text_extract_fragment_audit": extract_reports,
        "rendered_source_pages": {
            page: {
                "object": object_name,
                "path": source_reports[object_name]["path"],
                "sha256": source_reports[object_name]["sha256"],
            }
            for page, object_name in RENDERED_SOURCE_PAGES.items()
        },
        "checks": checks,
        "remaining_imports": [
            "independent official ePrint PDF/source fetch and revision check",
            "human review that the copied PR #96 PDF is the intended official ABF "
            "source",
            "human review of the ABF wording beyond the anchor fragments checked "
            "here",
            "reviewer acceptance of the finite Cycle84/Cycle116 chain",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    source = report["source"]
    files = source["files"]
    rendered = report["rendered_source_pages"]

    print("m1_cycle120_abf_extract_sources: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "source="
        f"PR #{source['pull_request']} {source['head_ref']} "
        f"commit {source['head_commit']}"
    )
    print(f"abf_pdf_sha256={files['abf_pdf']['sha256']}")
    print(
        "text_extracts="
        + ", ".join(
            f"{name}:{files[object_name]['sha256'][:12]}"
            for name, object_name in sorted(TEXT_EXTRACTS.items())
        )
    )
    print(
        "rendered_pages="
        + ", ".join(
            f"p{page}:{payload['sha256'][:12]}"
            for page, payload in sorted(rendered.items())
        )
    )
    print(
        "packet_zip="
        f"{files['cycle120_abf_packet_zip']['sha256']} "
        f"({files['cycle120_abf_packet_zip']['size']}B)"
    )
    print("fetch_command=" + source["fetch_command"])
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify PR #96 ABF PDF-extract source objects for Cycle120."
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
