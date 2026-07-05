#!/usr/bin/env python3
"""Replay the L1 petal residue-kernel linear-bound certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "l1-petal-residue-kernel-linear-bound"
    / "l1_petal_residue_kernel_linear_bound.json"
)
PROOF_PROGRAM = REPO / "experimental" / "notes" / "l1" / "l1_full_list_quotient_proof_program.md"
RESIDUE_BRIDGE = REPO / "experimental" / "notes" / "l1" / "l1_coset_chart_residue_bridge_v1.md"


ANCHORS = {
    "lemma_13_heading": "## Lemma 13. Full-Petal High Rank Below Top Defect",
    "lemma_13_bound": "dim K_{I,d} <= d-ell+1",
    "kernel_definition": "K_{I,d} = ker(pi_{>d} R_{I,d})",
    "bridge_claim": "residue-line bridge",
}


def check_anchor(path: Path, needle: str) -> bool:
    return needle in path.read_text()


def build_certificate() -> dict[str, Any]:
    checks = {
        "proof_program_exists": PROOF_PROGRAM.exists(),
        "residue_bridge_exists": RESIDUE_BRIDGE.exists(),
        "lemma_13_heading": check_anchor(PROOF_PROGRAM, ANCHORS["lemma_13_heading"]),
        "lemma_13_bound": check_anchor(PROOF_PROGRAM, ANCHORS["lemma_13_bound"]),
        "kernel_definition": check_anchor(PROOF_PROGRAM, ANCHORS["kernel_definition"]),
        "bridge_claim": ANCHORS["bridge_claim"] in RESIDUE_BRIDGE.read_text().lower(),
    }
    cert = {
        "schema": "l1-petal-residue-kernel-linear-bound-v1",
        "status": "PROVED_BY_LEMMA_13_REPLAY",
        "source_dag_node": "petal_residue_kernel_linear_bound",
        "statement": "dim K_{I,d} <= c + 1, where c = d - ell",
        "dependencies": [
            "l1_coset_chart_residue_bridge_v1",
            "l1_full_list_quotient_proof_program Lemma 13",
        ],
        "anchor_checks": checks,
        "non_claims": [
            "does not prove ambient-kernel flatness",
            "does not count squarefree realizable locator points",
            "does not close the L1 mixed/growing residual",
        ],
        "note": "experimental/notes/l1/l1_petal_residue_kernel_linear_bound.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "l1-petal-residue-kernel-linear-bound-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if "c + 1" not in cert["statement"]:
        raise AssertionError("statement must include c + 1 bound")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("l1-petal-residue-kernel-linear-bound certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    for name, ok in cert["anchor_checks"].items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text())
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
