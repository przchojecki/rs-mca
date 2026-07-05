#!/usr/bin/env python3
"""Verify the FM1 exact first-moment packet certificate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/fm1/fm1.json")
VTDV_CERT_PATH = Path("experimental/data/certificates/vtdv/vtdv.json")

SAMPLES = [
    {"q": 3, "t": 1, "n": 5, "j": 2},
    {"q": 5, "t": 2, "n": 8, "j": 3},
    {"q": 7, "t": 3, "n": 10, "j": 4},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def finite_slope_count(q: int, t: int) -> int:
    return q * (q**t - 1)


def total_syndrome_pairs(q: int, t: int) -> int:
    return q ** (2 * t)


def enumerate_finite_slope_count(q: int, t: int) -> int:
    count = 0
    vectors = range(q**t)
    decoded = {value: tuple((value // (q**i)) % q for i in range(t)) for value in vectors}
    for u_value in vectors:
        u = decoded[u_value]
        for v_value in vectors:
            v = decoded[v_value]
            if all(x == 0 for x in v):
                continue
            aligned = False
            for z in range(q):
                if all((u_i + z * v_i) % q == 0 for u_i, v_i in zip(u, v)):
                    aligned = True
                    break
            if aligned:
                count += 1
    return count


def probability_fraction(q: int, t: int) -> Fraction:
    return Fraction(finite_slope_count(q, t), total_syndrome_pairs(q, t))


def expected_aligned_fraction(q: int, t: int, n: int, j: int) -> Fraction:
    return comb(n, j) * probability_fraction(q, t)


def sample_record(row: dict[str, int]) -> dict[str, Any]:
    q, t, n, j = row["q"], row["t"], row["n"], row["j"]
    probability = probability_fraction(q, t)
    expected = expected_aligned_fraction(q, t, n, j)
    return {
        "q": q,
        "t": t,
        "n": n,
        "j": j,
        "finite_slope_pairs": finite_slope_count(q, t),
        "total_pairs": total_syndrome_pairs(q, t),
        "enumerated_finite_slope_pairs": enumerate_finite_slope_count(q, t),
        "probability": [probability.numerator, probability.denominator],
        "support_count": comb(n, j),
        "expected_aligned": [expected.numerator, expected.denominator],
    }


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.fm1.v1",
        "status": "PROVED",
        "source_dag_node": "fm1",
        "source_dag_dependencies": ["vtdv"],
        "verdict": "exact_first_moment_for_finite_slope_aligned_supports",
        "claim": {
            "fixed_support_probability": "(1 - q^(-t)) q^(1-t)",
            "finite_slope_pair_count": "q(q^t - 1)",
            "total_syndrome_pair_count": "q^(2t)",
            "expectation": "binom(n,j) (1 - q^(-t)) q^(1-t)",
            "excluded_degeneracy": "V = 0 all-slope/paid-fiber case",
        },
        "sample_arithmetic": [sample_record(row) for row in SAMPLES],
        "consumers": [
            "mca_safe",
            "spread_regime_bound",
            "averaged_slope_conversion",
            "aperiodic_zero_at_crossing",
        ],
        "non_claims": [
            "does not count the all-slope degeneracy V=0",
            "does not classify aligned supports as paid or unpaid",
            "does not prove a higher-moment or concentration bound",
            "does not edit Papers A-D",
        ],
    }


def validate_vtdv_certificate() -> None:
    require(VTDV_CERT_PATH.exists(), f"missing dependency certificate: {VTDV_CERT_PATH}")
    cert = json.loads(VTDV_CERT_PATH.read_text())
    require(cert.get("source_dag_node") == "vtdv", "dependency node mismatch")
    require(cert.get("status") == "PROVED", "vtdv dependency must be PROVED")


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    for row in cert["sample_arithmetic"]:
        q, t, n, j = row["q"], row["t"], row["n"], row["j"]
        require(row["finite_slope_pairs"] == q * (q**t - 1), f"finite-slope pair count mismatch: {row}")
        require(row["total_pairs"] == q ** (2 * t), f"total pair count mismatch: {row}")
        require(row["enumerated_finite_slope_pairs"] == row["finite_slope_pairs"], f"enumeration mismatch: {row}")
        probability = Fraction(*row["probability"])
        require(probability == probability_fraction(q, t), f"probability mismatch: {row}")
        expected = Fraction(*row["expected_aligned"])
        require(expected == expected_aligned_fraction(q, t, n, j), f"expectation mismatch: {row}")


def emit_certificate(path: Path, cert: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", nargs="?", const=CERT_PATH, type=Path)
    parser.add_argument("--check", nargs="?", const=CERT_PATH, type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit is not None:
        emit_certificate(args.emit, cert)
        print(f"WROTE: {args.emit}")
    if args.check is not None:
        loaded = json.loads(args.check.read_text())
        validate_certificate(loaded)
        validate_vtdv_certificate()
        print(f"PASS: certificate matches {args.check}")
    if args.emit is None and args.check is None:
        validate_certificate(cert)
        print("PASS: fm1 packet")


if __name__ == "__main__":
    main()
