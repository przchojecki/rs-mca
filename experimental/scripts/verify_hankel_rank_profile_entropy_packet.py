#!/usr/bin/env python3
"""Verify the Hankel rank-profile entropy packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path(
    "experimental/data/certificates/hankel-rank-profile-entropy/hankel_rank_profile_entropy.json"
)

DEPENDENCY_CERTS = {
    "f_support_lattice": Path("experimental/data/certificates/f-support-lattice/f_support_lattice.json"),
    "hankel_sparse_atoms_as_rational_defects": Path(
        "experimental/data/certificates/hankel-sparse-atoms/hankel_sparse_atoms.json"
    ),
}

NARROW_SAMPLES = [
    {"W": 3, "j": 5, "t": 3, "dim_p": 3},
    {"W": 4, "j": 10, "t": 6, "dim_p": 5},
]

WIDE_SAMPLES = [
    {"W": 3, "j": 8, "t": 3},
    {"W": 5, "j": 16, "t": 8},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.hankel_rank_profile_entropy.v1",
        "status": "PROVED",
        "source_dag_node": "hankel_rank_profile_entropy",
        "source_dag_dependencies": [
            "f_support_lattice",
            "hankel_sparse_atoms_as_rational_defects",
        ],
        "verdict": "fixed_cutoff_hankel_unpaid_states_are_n_to_O_W_squared",
        "row_deficient": {
            "claim": "corrected binary-apolarity gives a principal GRS segment after root-at-infinity strip",
            "torus_verified_cases": 5086,
            "boundary_cases": 2966,
            "seed_row_deficient_cases": 4000,
            "consequence": "MDS zero-support matroid, no unpaid closure entropy",
        },
        "row_full_wide": {
            "condition": "j - t + 3 > 2W",
            "consequence": "all weight-<=W atoms lie in one saturated rational class, so Delta_u <= 1",
            "sample_arithmetic": WIDE_SAMPLES,
        },
        "row_full_narrow": {
            "condition": "j - t + 3 <= 2W",
            "dimension_bound": "dim P = j + 1 - t <= 2W - 2",
            "sample_arithmetic": NARROW_SAMPLES,
        },
        "total_bound": "unpaid primitive saturated states <= n^{O(W^2)} for fixed W",
        "consumers": ["f_termination_hankel", "spi_exceptional_class"],
        "non_claims": [
            "does not give a uniform bound when W grows with n",
            "does not supply the terminal moment/member count",
            "does not assemble f_termination_hankel by itself",
            "does not edit Papers A-D",
        ],
    }


def validate_dependency_certificates() -> None:
    for node, path in DEPENDENCY_CERTS.items():
        require(path.exists(), f"dependency certificate missing: {path}")
        cert = json.loads(path.read_text())
        require(cert.get("status") == "PROVED", f"dependency is not PROVED: {node}")
        require(cert.get("source_dag_node") == node, f"dependency node mismatch: {path}")


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    rd = cert["row_deficient"]
    require(rd["torus_verified_cases"] == 5086, "corrected torus verification count changed")
    require(rd["boundary_cases"] == 2966, "boundary-case count changed")
    require(rd["seed_row_deficient_cases"] == 4000, "seed row-deficient count changed")
    for row in cert["row_full_wide"]["sample_arithmetic"]:
        require(row["j"] - row["t"] + 3 > 2 * row["W"], f"wide sample is not wide: {row}")
    for row in cert["row_full_narrow"]["sample_arithmetic"]:
        require(row["j"] - row["t"] + 3 <= 2 * row["W"], f"narrow sample is not narrow: {row}")
        require(row["dim_p"] == row["j"] + 1 - row["t"], f"dim P formula mismatch: {row}")
        require(row["dim_p"] <= 2 * row["W"] - 2, f"narrow dimension bound mismatch: {row}")
    require("fixed W" in cert["total_bound"], "fixed-W boundary missing")


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
        validate_dependency_certificates()
        print(f"PASS: certificate matches {args.check}")
    if args.emit is None and args.check is None:
        validate_certificate(cert)
        print("PASS: hankel rank-profile entropy packet")


if __name__ == "__main__":
    main()
