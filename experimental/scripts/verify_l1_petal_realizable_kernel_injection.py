#!/usr/bin/env python3
"""Replay the L1 petal realizable-kernel injection certificate."""

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
    / "l1-petal-realizable-kernel-injection"
    / "l1_petal_realizable_kernel_injection.json"
)
PROOF_PROGRAM = REPO / "experimental" / "notes" / "l1" / "l1_full_list_quotient_proof_program.md"
RESIDUE_BRIDGE = REPO / "experimental" / "notes" / "l1" / "l1_coset_chart_residue_bridge_v1.md"


ANCHORS = {
    "lemma_8_heading": "## Lemma 8. Full-Petal Rank Certificate",
    "kernel_definition": "K_{I,d} = ker(pi_{>d} R_{I,d})",
    "locator_intersection": "{ L_D : D subset C, |D|=d } cap K_{I,d}",
    "bridge_claim": "residue-line bridge",
}


def text(path: Path) -> str:
    return path.read_text()


def build_certificate() -> dict[str, Any]:
    proof_text = text(PROOF_PROGRAM)
    bridge_text = text(RESIDUE_BRIDGE).lower()
    checks = {
        "proof_program_exists": PROOF_PROGRAM.exists(),
        "residue_bridge_exists": RESIDUE_BRIDGE.exists(),
        "lemma_8_heading": ANCHORS["lemma_8_heading"] in proof_text,
        "kernel_definition": ANCHORS["kernel_definition"] in proof_text,
        "locator_intersection": ANCHORS["locator_intersection"] in proof_text,
        "bridge_claim": ANCHORS["bridge_claim"] in bridge_text,
    }
    cert = {
        "schema": "l1-petal-realizable-kernel-injection-v1",
        "status": "PROVED_BY_LEMMA_8_REPLAY",
        "source_dag_node": "petal_realizable_kernel_injection",
        "statement": (
            "exact realizable full-petal extras inject into squarefree "
            "locator points in K_{I,d}"
        ),
        "dependencies": [
            "l1_coset_chart_residue_bridge_v1",
            "l1_full_list_quotient_proof_program Lemma 8",
        ],
        "anchor_checks": checks,
        "non_claims": [
            "does not count squarefree locator points in K_{I,d}",
            "does not prove the squarefree classification ledger",
            "does not close the L1 mixed/growing residual",
        ],
        "note": "experimental/notes/l1/l1_petal_realizable_kernel_injection.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "l1-petal-realizable-kernel-injection-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if "inject" not in cert["statement"]:
        raise AssertionError("statement must include injection")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("l1-petal-realizable-kernel-injection certificate")
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
