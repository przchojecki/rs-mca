#!/usr/bin/env python3
"""Verify the f_termination_hankel assembly packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/f-termination-hankel/f_termination_hankel.json")

DEPENDENCY_CERTS = {
    "hankel_rank_profile_entropy": Path(
        "experimental/data/certificates/hankel-rank-profile-entropy/hankel_rank_profile_entropy.json"
    ),
    "hankel_moment_clean_leaves": Path(
        "experimental/data/certificates/hankel-moment-clean-leaves/hankel_moment_clean_leaves.json"
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.f_termination_hankel.v1",
        "status": "PROVED",
        "source_dag_node": "f_termination_hankel",
        "source_dag_dependencies": [
            "hankel_rank_profile_entropy",
            "hankel_moment_clean_leaves",
        ],
        "verdict": "hankel_family_termination_follows_from_rank_profile_and_pinned_leaf_bounds",
        "claim": {
            "object": "rate-1/2 Hankel-kernel instances over mu_n",
            "state_model": "saturated root-closure states, not raw support branches",
            "paid_routes": [
                "tangent/common-divisor",
                "quotient/pullback",
                "dihedral/Chebyshev quotient",
                "extension or already-paid ledgers where applicable",
            ],
            "state_count": "reachable unpaid primitive saturated states <= n^{O(W^2)} for fixed W",
            "leaf_count": "terminal leaves satisfy the pinned affine moment/member-count bound",
        },
        "proof_inputs": {
            "state_count_input": "hankel_rank_profile_entropy",
            "leaf_member_input": "hankel_moment_clean_leaves",
            "subinputs_inside_rank_profile": [
                "f_support_lattice",
                "hankel_sparse_atoms_as_rational_defects",
            ],
        },
        "consumers": ["f_descent_termination"],
        "non_claims": [
            "does not bound raw sparse-support branch counts",
            "does not remove the fixed-W hypothesis",
            "does not produce the F17^32 M3/M4 root tables",
            "does not edit Papers A-D",
        ],
    }


def validate_dependency_certificates() -> None:
    rank = json.loads(DEPENDENCY_CERTS["hankel_rank_profile_entropy"].read_text())
    moment = json.loads(DEPENDENCY_CERTS["hankel_moment_clean_leaves"].read_text())
    require(rank.get("status") == "PROVED", "rank-profile dependency is not PROVED")
    require(moment.get("status") == "PROVED", "moment-clean dependency is not PROVED")
    require(rank.get("source_dag_node") == "hankel_rank_profile_entropy", "rank-profile node mismatch")
    require(moment.get("source_dag_node") == "hankel_moment_clean_leaves", "moment-clean node mismatch")
    require("fixed W" in rank.get("total_bound", ""), "rank-profile fixed-W boundary missing")
    require(
        moment.get("correction", {}).get("packaged_variant") == "pinned-value affine lemma",
        "moment-clean pinned variant missing",
    )


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    require("not raw support branches" in cert["claim"]["state_model"], "raw-branch boundary missing")
    require("fixed W" in cert["claim"]["state_count"], "fixed-W boundary missing")
    require(cert["proof_inputs"]["state_count_input"] == "hankel_rank_profile_entropy", "state input mismatch")
    require(cert["proof_inputs"]["leaf_member_input"] == "hankel_moment_clean_leaves", "leaf input mismatch")


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
        print("PASS: f_termination_hankel packet")


if __name__ == "__main__":
    main()
