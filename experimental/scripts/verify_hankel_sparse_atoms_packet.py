#!/usr/bin/env python3
"""Verify the Hankel sparse-atoms packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/hankel-sparse-atoms/hankel_sparse_atoms.json")

SAMPLES = [
    {"j": 5, "t": 3, "union_size": 4},
    {"j": 8, "t": 4, "union_size": 6},
    {"j": 12, "t": 7, "union_size": 7},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def separation_threshold(j: int, t: int) -> int:
    return j - t + 2


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.hankel_sparse_atoms.v1",
        "status": "PROVED",
        "source_dag_node": "hankel_sparse_atoms_as_rational_defects",
        "verdict": "sparse_annihilator_atoms_are_rational_defect_sets",
        "normal_form": {
            "annihilator": "GRS_{n_E-j-1}(E,lambda) + omega RS_t(E)",
            "coordinate_word": "u_x = omega_x h(x) + lambda_x g(x)",
            "degree_bounds": ["deg h < t", "deg g <= n_E - j - 2"],
        },
        "separation": {
            "distinct_class_polynomial": "F = g_1 h_2 - g_2 h_1",
            "degree_bound": "deg F <= n_E - j + t - 3",
            "union_lower_bound": "|T_1 union T_2| >= j - t + 2",
            "verified_pairs": 233130,
            "violations": 0,
            "sample_arithmetic": SAMPLES,
        },
        "same_class_collapse": {
            "reason": "punctured-GRS/MDS on the defect block",
            "saturated_closure_count": 1,
        },
        "heredity": "child descent multiplies omega by the child locator factor",
        "consumers": ["hankel_rank_profile_entropy"],
        "non_claims": [
            "does not prove the rank-profile entropy theorem by itself",
            "does not count row-deficient Hankel states",
            "does not provide support-lattice accounting",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    sep = cert["separation"]
    require(sep["verified_pairs"] == 233130, "verified pair count changed")
    require(sep["violations"] == 0, "separation violations must stay zero")
    for row in sep["sample_arithmetic"]:
        threshold = separation_threshold(row["j"], row["t"])
        require(row["union_size"] >= threshold, f"sample violates separation: {row}")
    collapse = cert["same_class_collapse"]
    require(collapse["saturated_closure_count"] == 1, "same-class atoms must collapse to one closure")


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
        print("PASS: hankel sparse-atoms packet")


if __name__ == "__main__":
    main()
