#!/usr/bin/env python3
"""Verify the V8 one-support-one-slope packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/v8-ledger/v8_ledger.json")

SAMPLES = [
    {"q": 5, "A": [1, 2], "B": [2, 4], "finite_slopes": [2], "case": "one"},
    {"q": 5, "A": [1, 0], "B": [0, 1], "finite_slopes": [], "case": "none"},
    {"q": 7, "A": [0, 0, 0], "B": [0, 0, 0], "finite_slopes": list(range(7)), "case": "all"},
    {"q": 7, "A": [3, 1, 4], "B": [0, 0, 0], "finite_slopes": [], "case": "none"},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def slopes(q: int, a_vec: list[int], b_vec: list[int]) -> list[int]:
    out = []
    for z in range(q):
        if all((a + z * b) % q == 0 for a, b in zip(a_vec, b_vec)):
            out.append(z)
    return out


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.v8_ledger.v1",
        "status": "PROVED",
        "source_dag_node": "v8_ledger",
        "verdict": "fixed_noncontained_locator_has_at_most_one_finite_slope",
        "claim": {
            "fixed_locator_equation": "A + z B = 0",
            "nondegenerate_case": "B != 0 gives at most one finite slope",
            "degenerate_case": "A = B = 0 gives all slopes and is handled by noncontainment",
            "zero_direction_case": "B = 0, A != 0 gives no finite slopes",
        },
        "sample_arithmetic": SAMPLES,
        "consumers": ["counting_frame", "xr_expansion", "xr_junta_to_paid", "xr_globalness_from_ledger"],
        "non_claims": [
            "does not count how many locators occur",
            "does not remove the all-slope degeneracy",
            "does not classify the locator as paid or unpaid",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    for row in cert["sample_arithmetic"]:
        got = slopes(row["q"], row["A"], row["B"])
        require(got == row["finite_slopes"], f"slope set mismatch: {row} != {got}")
        if any(b % row["q"] for b in row["B"]):
            require(len(got) <= 1, f"nonzero direction has more than one slope: {row}")


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
        print("PASS: v8_ledger packet")


if __name__ == "__main__":
    main()
