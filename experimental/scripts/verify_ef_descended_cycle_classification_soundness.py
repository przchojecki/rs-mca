#!/usr/bin/env python3
"""Replay the EF descended-cycle classification soundness certificate."""

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
    / "ef-descended-cycle-classification-soundness"
    / "ef_descended_cycle_classification_soundness.json"
)
NOTE = REPO / "experimental" / "notes" / "ef" / "ef_descended_cycle_classification_soundness.md"

ALLOWED = {"base_descended", "tower_confined", "noncontainment_degenerate"}

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "ef_descended_cycle_classification_soundness",
    "descent_dependency": "By `ef_full_orbit_cycle_descent`",
    "base_case": "base-descended, it is paid by the base component",
    "tower_case": "proper-subfield or tower-confined",
    "noncontainment_case": "excluded by the noncontainment gate",
    "exclusion": "ef_pole_free_cycle_exclusion",
    "non_claim": "does not produce the classification certificate",
}


def leakage(cycles: list[str], classification: dict[str, str]) -> list[str]:
    return [
        cycle
        for cycle in cycles
        if cycle not in classification or classification[cycle] not in ALLOWED
    ]


def classification_sample() -> dict[str, Any]:
    cycles = ["C0", "C1", "C2"]
    classification = {
        "C0": "base_descended",
        "C1": "tower_confined",
        "C2": "noncontainment_degenerate",
    }
    complete_leakage = leakage(cycles, classification)
    incomplete_leakage = leakage(cycles + ["C3"], classification)
    checks = {
        "complete_classification_has_no_leakage": complete_leakage == [],
        "missing_cycle_is_detected": incomplete_leakage == ["C3"],
        "labels_allowed": all(label in ALLOWED for label in classification.values()),
    }
    return {
        "cycles": cycles,
        "classification": classification,
        "allowed_labels": sorted(ALLOWED),
        "complete_leakage": complete_leakage,
        "incomplete_leakage": incomplete_leakage,
        "checks": checks,
        "passes": all(checks.values()),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "ef-descended-cycle-classification-soundness-v1",
        "status": "PROVED_CLASSIFICATION_EXCLUSION_SEMANTICS",
        "source_dag_node": "ef_descended_cycle_classification_soundness",
        "statement": (
            "a complete base/tower/noncontainment classification of descended "
            "pole-free cycles proves ef_pole_free_cycle_exclusion"
        ),
        "anchor_checks": checks,
        "sample_classification": classification_sample(),
        "dependencies": [
            "ef_full_orbit_cycle_descent",
            "base/tower/noncontainment removal semantics",
        ],
        "non_claims": [
            "does not construct the descended-cycle classification certificate",
            "does not certify a proposed classification payload",
            "does not close ef_ru by itself",
        ],
        "note": "experimental/notes/ef/ef_descended_cycle_classification_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "ef-descended-cycle-classification-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["sample_classification"]["passes"]:
        raise AssertionError(f"sample classification failed: {cert['sample_classification']}")
    if "ef_pole_free_cycle_exclusion" not in cert["statement"]:
        raise AssertionError("statement must name the exclusion node")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("ef-descended-cycle-classification-soundness certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    for name, ok in cert["anchor_checks"].items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    for name, ok in cert["sample_classification"]["checks"].items():
        print(f"  sample {name}: {'PASS' if ok else 'FAIL'}")


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
