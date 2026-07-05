#!/usr/bin/env python3
"""Replay the DLI odd-phase polar-obstruction soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_odd_phase_polar_obstruction_soundness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-odd-phase-polar-obstruction-soundness"
    / "dli_odd_phase_polar_obstruction_soundness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_odd_phase_polar_obstruction_soundness",
    "criterion_dependency": "dli_artin_schreier_conductor_criterion",
    "reduced_pole_predicate": "positive order not divisible by `p`",
    "non_claim": "does not construct the reduced-phase manifest",
}


def verifies_polar_obstruction(p: int, reduced_pole_order: int) -> bool:
    return p > 1 and reduced_pole_order > 0 and reduced_pole_order % p != 0


def toy_check() -> dict[str, Any]:
    p = 5
    cases = [
        {"order": 3, "expected": True},
        {"order": 1, "expected": True},
        {"order": 10, "expected": False},
        {"order": 0, "expected": False},
        {"order": -2, "expected": False},
    ]
    results = [
        {
            "p": p,
            "order": case["order"],
            "accepted": verifies_polar_obstruction(p, case["order"]),
            "expected": case["expected"],
        }
        for case in cases
    ]
    return {
        "field_characteristic": p,
        "cases": results,
        "all_expected": all(row["accepted"] == row["expected"] for row in results),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-odd-phase-polar-obstruction-soundness-v1",
        "status": "PROVED_POLAR_OBSTRUCTION_REPLAY",
        "source_dag_node": "dli_odd_phase_polar_obstruction_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not construct the reduced-phase manifest",
            "does not enumerate the DLI tuple universe",
            "does not prove the harmonic conductor budget",
        ],
        "note": "experimental/notes/dli/dli_odd_phase_polar_obstruction_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-odd-phase-polar-obstruction-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["toy_check"]["all_expected"]:
        raise AssertionError(f"failed toy check: {cert['toy_check']}")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
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
        print(f"{cert['status']}: {cert['toy_check']}")


if __name__ == "__main__":
    main()
