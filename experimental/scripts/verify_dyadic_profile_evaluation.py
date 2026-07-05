#!/usr/bin/env python3
"""Replay the dyadic profile evaluation packet."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "dyadic_profile_evaluation.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dyadic-profile-evaluation"
    / "dyadic_profile_evaluation.json"
)

TOL = 5e-4

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dyadic_profile_evaluation",
    "profile": "Q_H = sum_{M | n, M > t} binom(n/M - 1, floor(A/M)).",
    "first_scale": "first admissible scale dominates the sum",
    "uniformity": "uniform between Row-C scale `n = 2^10` and prize scale `n = 2^41`",
    "non_claim": "does not alter Papers A-D",
}

ROWS = [
    {"name": "pinned 1/2", "n": 512, "k": 256, "A": 507},
    {"name": "RowC 1/4", "n": 2**10, "k": 2**8, "A": 261},
    {"name": "RowC 1/8", "n": 2**10, "k": 2**7, "A": 133},
    {"name": "RowC 1/16", "n": 2**10, "k": 2**6, "A": 67},
    {"name": "prize 1/4", "n": 2**41, "k": 2**39, "A": 558_345_748_481},
    {"name": "prize 1/8", "n": 2**41, "k": 2**38, "A": 283_467_841_537},
    {"name": "prize 1/16", "n": 2**41, "k": 2**37, "A": 141_733_920_769},
]

QA22_Q = {"1/4": 99.8063, "1/8": 66.1465, "1/16": 82.9664}
QA22_D = {"1/4": 48.3804, "1/8": 31.8508, "1/16": 40.2857}


def pow2_divisors(n: int) -> list[int]:
    divisors = []
    modulus = 1
    while modulus <= n:
        if n % modulus == 0:
            divisors.append(modulus)
        modulus *= 2
    return divisors


def profile_terms(n: int, k: int, A: int) -> list[tuple[int, int, int, int]]:
    t = A - k
    terms = []
    for modulus in pow2_divisors(n):
        if modulus > t:
            quotient_len = n // modulus
            h = A // modulus
            if 0 <= h <= quotient_len - 1:
                terms.append((modulus, quotient_len, h, math.comb(quotient_len - 1, h)))
    return terms


def dihedral_companion(quotient_len: int, h: int, tail_size: int) -> int:
    pairs = (quotient_len - 2) // 2
    fixed = 2 if tail_size == 0 else 1
    total = 0
    for fixed_count in range(fixed + 1):
        rem = h - fixed_count
        if rem >= 0 and rem % 2 == 0:
            pair_count = rem // 2
            if 0 <= pair_count <= pairs:
                total += math.comb(fixed, fixed_count) * math.comb(pairs, pair_count)
    return total


def row_rate(name: str) -> str:
    return name.split()[-1]


def evaluate_row(row: dict[str, int | str]) -> dict[str, object]:
    name = str(row["name"])
    n = int(row["n"])
    k = int(row["k"])
    A = int(row["A"])
    t = A - k
    terms = profile_terms(n, k, A)
    if not terms or terms[0][3] <= 1:
        return {
            "row": name,
            "rate": row_rate(name),
            "n": n,
            "k": k,
            "A": A,
            "t": t,
            "profile": "trivial",
            "reason": "parity-killed dyadic quotient mass",
        }

    modulus, quotient_len, h, q_top = terms[0]
    q_sum = sum(term[3] for term in terms)
    tail_size = A - h * modulus
    d_top = dihedral_companion(quotient_len, h, tail_size)
    log2_q_top = math.log2(q_top)
    log2_q_sum = math.log2(q_sum)
    log2_d_top = math.log2(d_top) if d_top else float("nan")
    return {
        "row": name,
        "rate": row_rate(name),
        "n": n,
        "k": k,
        "A": A,
        "t": t,
        "M_star": modulus,
        "N_star": quotient_len,
        "h": h,
        "tail_size": tail_size,
        "Q_top": q_top,
        "Q_sum": q_sum,
        "D_top": d_top,
        "log2_Q_top": round(log2_q_top, 6),
        "log2_Q_sum": round(log2_q_sum, 6),
        "log2_D_top": round(log2_d_top, 6),
        "qa22_Q_target": QA22_Q.get(row_rate(name)),
        "qa22_D_target": QA22_D.get(row_rate(name)),
        "qa22_Q_check": abs(log2_q_top - QA22_Q[row_rate(name)]) <= TOL,
        "qa22_D_check": abs(log2_d_top - QA22_D[row_rate(name)]) <= TOL,
        "first_scale_dominance": abs(log2_q_sum - log2_q_top) <= 1e-6,
    }


def n_uniformity_checks(rows: list[dict[str, object]]) -> dict[str, object]:
    by_name = {row["row"]: row for row in rows}
    checks = {}
    for rate in ("1/4", "1/8", "1/16"):
        rowc = by_name[f"RowC {rate}"]
        prize = by_name[f"prize {rate}"]
        signature_keys = ("N_star", "h", "log2_Q_top", "log2_D_top")
        checks[rate] = {
            "rowc": {key: rowc[key] for key in signature_keys},
            "prize": {key: prize[key] for key in signature_keys},
            "accepted": all(rowc[key] == prize[key] for key in signature_keys),
        }
    return checks


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    rows = [evaluate_row(row) for row in ROWS]
    cert = {
        "schema": "dyadic-profile-evaluation-v1",
        "status": "PROVED",
        "source_dag_node": "dyadic_profile_evaluation",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "profile_formula": "Q_H = sum_{M | n, M > t} binom(n/M - 1, floor(A/M))",
        "rows": rows,
        "n_uniformity_checks": n_uniformity_checks(rows),
        "non_claims": [
            "does not close a deployed adjacent row theorem by itself",
            "does not prove non-dyadic profile statements",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/dyadic_profile_evaluation.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "dyadic-profile-evaluation-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "dyadic_profile_evaluation":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    rows = cert.get("rows")
    if not isinstance(rows, list) or len(rows) != len(ROWS):
        raise AssertionError("unexpected row count")
    by_name = {row["row"]: row for row in rows}
    if by_name["pinned 1/2"].get("profile") != "trivial":
        raise AssertionError("rate-1/2 row should be trivial")
    for row in rows:
        if row["row"] == "pinned 1/2":
            continue
        if not row.get("qa22_Q_check") or not row.get("qa22_D_check"):
            raise AssertionError(f"{row['row']}: QA.22 check failed")
        if not row.get("first_scale_dominance"):
            raise AssertionError(f"{row['row']}: first-scale dominance failed")
    uniformity = cert.get("n_uniformity_checks")
    if not isinstance(uniformity, dict):
        raise AssertionError("missing n-uniformity checks")
    for rate, check in uniformity.items():
        if not check.get("accepted"):
            raise AssertionError(f"{rate}: n-uniformity failed")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
