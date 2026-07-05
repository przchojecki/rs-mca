#!/usr/bin/env python3
"""Verify the noncontainment-degeneracy packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/noncontain-degeneracy/noncontain_degeneracy.json")

SAMPLES = [
    {"q": 5, "A": [0, 0], "B": [0, 0], "all_slopes": True, "degenerate": True},
    {"q": 5, "A": [1, 2], "B": [2, 4], "all_slopes": False, "degenerate": False},
    {"q": 7, "A": [3, 0, 1], "B": [0, 0, 0], "all_slopes": False, "degenerate": False},
    {"q": 7, "A": [0, 0, 0], "B": [0, 1, 0], "all_slopes": False, "degenerate": False},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def is_zero(q: int, vec: list[int]) -> bool:
    return all(x % q == 0 for x in vec)


def all_slopes(q: int, a_vec: list[int], b_vec: list[int]) -> bool:
    for z in range(q):
        if any((a + z * b) % q != 0 for a, b in zip(a_vec, b_vec)):
            return False
    return True


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.noncontain_degeneracy.v1",
        "status": "PROVED",
        "source_dag_node": "noncontain_degeneracy",
        "verdict": "all_slope_containment_is_exactly_the_zero_endpoint_pencil",
        "claim": {
            "fixed_locator_equation": "A + z B = 0",
            "all_slope_condition": "A = 0 and B = 0",
            "interpretation": "containment / degenerate pencil / def:residue degeneracy",
            "counting_boundary": "remove before finite-slope counting",
        },
        "sample_arithmetic": SAMPLES,
        "consumers": ["counting_frame", "ef_full_orbit_pole_forcing"],
        "non_claims": [
            "does not count noncontained finite slopes",
            "does not classify paid quotient, tangent, or extension strata",
            "does not prove the Paper B normal form",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    for row in cert["sample_arithmetic"]:
        degenerate = is_zero(row["q"], row["A"]) and is_zero(row["q"], row["B"])
        require(degenerate == row["degenerate"], f"degeneracy mismatch: {row}")
        require(all_slopes(row["q"], row["A"], row["B"]) == row["all_slopes"], f"all-slope mismatch: {row}")
        require(row["all_slopes"] == row["degenerate"], f"all slopes must equal degeneracy: {row}")


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
        print("PASS: noncontain_degeneracy packet")


if __name__ == "__main__":
    main()
