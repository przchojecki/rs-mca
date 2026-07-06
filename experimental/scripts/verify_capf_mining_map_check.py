#!/usr/bin/env python3
"""Independent checks for the CAP25 raw finite-testability map.

Proof status: AUDIT.  This checker re-reads the TeX source and certificate,
recomputes the exact toy gates by a separate route, and verifies the triage
anchors.  It does not prove any frontier input and does not resolve prob:band.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


THEOREM_PROBLEM_ID = "cap25-raw finite-testability map independent check"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source and JSON certificate check"

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_REL = "experimental/cap25_cap_v13_raw.tex"
CERT_REL = "experimental/data/certificates/capf-mining-map/capf_mining_map.json"

REQUIRED_HIGH = {
    "cor:capfr1-Q-R1-closing",
    "prob:capg-split-pencil-B",
    "cor:capg-adjacent-pairs",
    "prob:capg-shiftpairs",
}
REQUIRED_ORACLE = {
    "thm:capf-first-moment",
    "thm:capf-fixeddim",
    "prob:capg-active-BC",
    "prob:capg-active-shiftpairs",
}


def read_source() -> tuple[str, list[str]]:
    source = (REPO_ROOT / SOURCE_REL).read_text(encoding="utf-8")
    return source, source.splitlines()


def read_cert(path: Path | None = None) -> dict[str, Any]:
    cert_path = path or (REPO_ROOT / CERT_REL)
    return json.loads(cert_path.read_text(encoding="utf-8"))


def line_has_label(lines: list[str], line: int, label: str) -> bool:
    if not 1 <= line <= len(lines):
        return False
    return f"\\label{{{label}}}" in lines[line - 1]


def find_environment(source: str, label: str) -> dict[str, Any]:
    marker = f"\\label{{{label}}}"
    pos = source.find(marker)
    if pos < 0:
        raise ValueError(f"missing label {label}")
    begin_pos = source.rfind("\\begin{", 0, pos)
    end_pos = source.find("\\end{", pos)
    if begin_pos < 0 or end_pos < 0:
        raise ValueError(f"could not bound environment for {label}")
    begin_match = re.match(r"\\begin\{([^}]+)\}(?:\[([^\]]*)\])?", source[begin_pos:])
    if not begin_match:
        raise ValueError(f"could not parse environment for {label}")
    kind = begin_match.group(1)
    title = begin_match.group(2) or ""
    env_end_marker = f"\\end{{{kind}}}"
    env_end = source.find(env_end_marker, pos)
    if env_end < 0:
        raise ValueError(f"missing end marker for {label}")
    body = source[begin_pos : env_end + len(env_end_marker)]
    next_begin = source.find("\\begin{", env_end + len(env_end_marker))
    trailer = source[env_end + len(env_end_marker) : next_begin if next_begin >= 0 else env_end + len(env_end_marker) + 500]
    line = source.count("\n", 0, pos) + 1
    return {
        "kind": kind,
        "title": re.sub(r"\s+", " ", title).strip(),
        "line": line,
        "body": body,
        "has_following_proof": "\\begin{proof}" in trailer,
    }


def exact_first_moment_check() -> dict[str, Any]:
    q = 5
    domain = [1, 2, 3, 4]
    support_roots = list(itertools.combinations(domain, 2))
    words = list(itertools.product(range(q), repeat=len(domain)))

    def locator_value(roots: tuple[int, int], x: int) -> int:
        return ((x - roots[0]) * (x - roots[1])) % q

    nonzero_syndrome_counts = []
    for roots in support_roots:
        count = 0
        for word in words:
            syndrome = sum(word[i] * locator_value(roots, domain[i]) for i in range(len(domain))) % q
            if syndrome:
                count += 1
        nonzero_syndrome_counts.append(count)
    # For t=1, every v with nonzero syndrome aligns with every u.
    aligned_pairs = sum(count * len(words) for count in nonzero_syndrome_counts)
    observed = Fraction(aligned_pairs, len(words) * len(words))
    expected = Fraction(math.comb(4, 2) * (1 - Fraction(1, q)) * 1, 1)
    return {
        "label": "thm:capf-first-moment",
        "observed_average": {"numerator": observed.numerator, "denominator": observed.denominator},
        "theorem_average": {"numerator": expected.numerator, "denominator": expected.denominator},
        "passes": observed == expected,
    }


def exact_fixed_dim_check() -> dict[str, Any]:
    q = 5
    domain = [1, 2, 3, 4]
    j = 2
    seen = set()
    for roots in itertools.combinations(domain, j):
        coeffs = (1, (-(roots[0] + roots[1])) % q, (roots[0] * roots[1]) % q)
        seen.add(coeffs)
    incidence = len(seen)
    bound = math.comb(len(domain), 2)
    return {
        "label": "thm:capf-fixeddim",
        "incidence": incidence,
        "bound": bound,
        "passes": incidence <= bound and incidence == bound,
    }


def check_certificate(cert: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source, lines = read_source()
    source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if cert.get("source", {}).get("sha256") != source_hash:
        errors.append("source hash mismatch")

    rows = cert.get("rows", [])
    if not rows:
        errors.append("certificate has no rows")
    by_label = {row.get("label"): row for row in rows}

    high = {row.get("label") for row in cert.get("high_priority_rows", [])}
    if high != REQUIRED_HIGH:
        errors.append(f"high priority rows mismatch: {sorted(high)}")

    for row in rows:
        label = row.get("label", "")
        line = int(row.get("line", 0))
        if not line_has_label(lines, line, label):
            errors.append(f"line anchor mismatch for {label}")
            continue
        env = find_environment(source, label)
        if env["kind"] != row.get("kind"):
            errors.append(f"kind mismatch for {label}")
        if row.get("quote"):
            compact = re.sub(r"\s+", " ", env["body"]).strip()
            if row["quote"][:80] not in compact:
                errors.append(f"quote mismatch for {label}")

    for label in REQUIRED_HIGH:
        row = by_label.get(label)
        if not row:
            errors.append(f"missing high row {label}")
            continue
        if row.get("reachability_layer") != "GENUINE-TEST":
            errors.append(f"high row is not GENUINE-TEST: {label}")
        if row.get("mining_priority") != "HIGH":
            errors.append(f"high row priority mismatch: {label}")

    gates = {gate.get("label"): gate for gate in cert.get("oracle_gates", [])}
    if set(gates) != REQUIRED_ORACLE:
        errors.append(f"oracle labels mismatch: {sorted(gates)}")
    gate_one = exact_first_moment_check()
    if gates.get("thm:capf-first-moment", {}).get("observed_average") != gate_one["observed_average"]:
        errors.append("first-moment observed average mismatch")
    if gates.get("thm:capf-first-moment", {}).get("theorem_average") != gate_one["theorem_average"]:
        errors.append("first-moment theorem average mismatch")
    if not gate_one["passes"]:
        errors.append("first-moment independent check failed")
    gate_two = exact_fixed_dim_check()
    if gates.get("thm:capf-fixeddim", {}).get("incidence") != gate_two["incidence"]:
        errors.append("fixed-dim incidence mismatch")
    if gates.get("thm:capf-fixeddim", {}).get("bound") != gate_two["bound"]:
        errors.append("fixed-dim bound mismatch")
    if not gate_two["passes"]:
        errors.append("fixed-dim independent check failed")
    for label in ("prob:capg-active-BC", "prob:capg-active-shiftpairs"):
        env = find_environment(source, label)
        if env["has_following_proof"]:
            errors.append(f"{label} unexpectedly has a following proof")
        if "prove" not in env["body"].lower() and "bound" not in env["body"].lower():
            errors.append(f"{label} does not expose an input body")
    cb = cert.get("claim_boundaries", {})
    for field in ("resolves_or_advances_prob_band", "proves_prob_band_undecidable", "claims_no_method_can_reach", "is_counterexample"):
        if cb.get(field) is not False:
            errors.append(f"claim boundary {field} must be false")
    if cb.get("is_novel_not_confirming_a_proven_theorem") is not True:
        errors.append("scope-map novelty boundary must be true")
    if cert.get("evidence_type") != "FULL_FINITE_CENSUS":
        errors.append("unexpected evidence_type")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check the default certificate")
    parser.add_argument("--cert", type=Path, help="optional certificate path")
    parser.add_argument("--json", action="store_true", help="print check JSON")
    args = parser.parse_args()

    cert = read_cert(args.cert)
    errors = check_certificate(cert)
    result = {
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "proof_status": PROOF_STATUS,
        "determinism": DETERMINISM,
        "certificate": str(args.cert or (REPO_ROOT / CERT_REL)),
        "result": "PASS" if not errors else "FAIL",
        "review_reasons": errors,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"theorem_problem_id: {THEOREM_PROBLEM_ID}")
        print(f"proof_status: {PROOF_STATUS}")
        print(f"result: {result['result']}")
        print("review_reasons:", "<none>" if not errors else "; ".join(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
