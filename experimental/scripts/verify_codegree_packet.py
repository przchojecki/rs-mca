#!/usr/bin/env python3
"""Verify the codegree packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/codegree/codegree.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.codegree.v1",
        "status": "PROVED",
        "source_dag_node": "codegree",
        "source_dag_dependencies": ["deep_point"],
        "verdict": "l2_interleaved_list_reduces_to_base_and_higher_agreement_lists",
        "proved_reductions": {
            "theorem_a_decomposition": (
                "Lambda_2^{(a)} equals a sum over row-1 fibers of punctured-RS "
                "lists on A_{U_1}(c_1)."
            ),
            "theorem_b_two_regime_mu2": (
                "Lambda_2^{(a)} <= |Fib_2| + M_2(2a-k) |Fib_1|, symmetrically."
            ),
            "theorem_c_mu_recursion": (
                "Lambda_mu^{(a)} <= Lambda_{mu-1}^{(a)} + "
                "Lambda_{mu-1}^{(2a-k)} |Fib_1|."
            ),
        },
        "conditional_boundary": {
            "saving_corollary": "CONDITIONAL",
            "needed_input": (
                "polynomial L1-family tail/profile control at agreement 2a-k "
                "after quotient-periodic mass is budgeted"
            ),
            "not_claimed": "unconditional exponent saving",
        },
        "upstream_evidence": [
            "experimental/notes/l2/l2_codegree_reduction_theorem.md",
            "experimental/scripts/verify_l2_codegree_decomposition.py",
            "experimental/scripts/verify_l2_reduction_bound.py",
            "experimental/scripts/verify_l2_mu_recursion.py",
        ],
        "consumers": ["list_safe"],
        "non_claims": [
            "does not prove the L1 image-fiber theorem",
            "does not prove the exponent-saving corollary unconditionally",
            "does not close list_safe",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    reductions = cert["proved_reductions"]
    require("punctured-RS" in reductions["theorem_a_decomposition"], "Theorem A boundary missing")
    require("M_2(2a-k)" in reductions["theorem_b_two_regime_mu2"], "Theorem B formula missing")
    require("Lambda_{mu-1}^{(2a-k)}" in reductions["theorem_c_mu_recursion"], "Theorem C formula missing")
    require(cert["conditional_boundary"]["saving_corollary"] == "CONDITIONAL", "saving must remain conditional")
    require(cert["consumers"] == ["list_safe"], "consumer list mismatch")


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
        print("PASS: codegree packet")


if __name__ == "__main__":
    main()
