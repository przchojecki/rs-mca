#!/usr/bin/env python3
"""Verify the qcore packet certificate."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/qcore/qcore.json")

SAMPLES = [
    {"n": 16, "k": 8, "M": 2, "sigma": 1, "count": 35},
    {"n": 32, "k": 16, "M": 4, "sigma": 3, "count": 35},
    {"n": 64, "k": 16, "M": 8, "sigma": 7, "count": 21},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def qcore_count(n: int, k: int, M: int) -> int:
    require(k % M == 0, "M must divide k")
    require(n % M == 0, "M must divide n in the quotient-row samples")
    return comb(n // M - 1, k // M)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.qcore.v1",
        "status": "PROVED",
        "source_dag_node": "qcore",
        "verdict": "quotient_core_count_is_q_independent",
        "claim": {
            "conditions": ["M divides k", "0 <= sigma < M"],
            "agreement": "k + sigma",
            "lower_bound": "binom(n/M - 1, k/M)",
            "field_dependence": "none",
        },
        "sample_arithmetic": SAMPLES,
        "upstream_evidence": [
            "experimental/notes/roadmaps/proof_sketch/s7_list_side.md",
        ],
        "consumers": ["list_unsafe"],
        "non_claims": [
            "does not close list_unsafe",
            "does not decide endpoint conventions",
            "does not provide the S0 object/rules audit",
            "does not prove the list-safe upper bound",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    claim = cert["claim"]
    require(claim["lower_bound"] == "binom(n/M - 1, k/M)", "lower-bound formula mismatch")
    require(claim["field_dependence"] == "none", "q-independence boundary mismatch")
    for row in cert["sample_arithmetic"]:
        got = qcore_count(row["n"], row["k"], row["M"])
        require(row["count"] == got, f"sample count mismatch: {row} != {got}")
        require(0 <= row["sigma"] < row["M"], f"sigma outside qcore range: {row}")
    require(cert["consumers"] == ["list_unsafe"], "consumer list mismatch")


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
        print(f"PASS: certificate matches {args.check}")
    if args.emit is None and args.check is None:
        validate_certificate(cert)
        print("PASS: qcore packet")


if __name__ == "__main__":
    main()
