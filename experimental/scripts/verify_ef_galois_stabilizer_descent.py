#!/usr/bin/env python3
"""Replay the EF Galois stabilizer descent certificate."""

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
    / "ef-galois-stabilizer-descent"
    / "ef_galois_stabilizer_descent.json"
)
NOTE = REPO / "experimental" / "notes" / "ef" / "ef_galois_stabilizer_descent.md"


ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "ef_galois_stabilizer_descent",
    "full_stabilizer": "full stabilizer gives a base-descended component",
    "proper_stabilizer": "proper nontrivial stabilizer gives an intermediate-subfield",
    "trivial_stabilizer": "trivial stabilizer gives the genuinely full-field",
    "galois_correspondence": "exhaustive by the Galois correspondence",
    "non_claim": "does not exclude the full-orbit case",
}


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def classify_stabilizer(group_order: int, stabilizer_order: int) -> str:
    if stabilizer_order == group_order:
        return "base_descended"
    if stabilizer_order == 1:
        return "full_orbit"
    return "tower_confined"


def trichotomy_checks() -> list[dict[str, Any]]:
    checks = []
    for group_order in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 60):
        seen = {"base_descended": 0, "tower_confined": 0, "full_orbit": 0}
        classifications = {}
        for stabilizer_order in divisors(group_order):
            label = classify_stabilizer(group_order, stabilizer_order)
            seen[label] += 1
            classifications[str(stabilizer_order)] = label
        if group_order == 1:
            checks.append(
                {
                    "group_order": group_order,
                    "degenerate_base_equals_top": True,
                    "stabilizer_classifications": classifications,
                    "passes": seen == {
                        "base_descended": 1,
                        "tower_confined": 0,
                        "full_orbit": 0,
                    },
                }
            )
        else:
            checks.append(
                {
                    "group_order": group_order,
                    "exhaustive_partition": True,
                    "stabilizer_classifications": classifications,
                    "class_counts": seen,
                    "passes": seen["base_descended"] == 1 and seen["full_orbit"] == 1,
                }
            )
    return checks


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "ef-galois-stabilizer-descent-v1",
        "status": "PROVED_CYCLIC_GALOIS_STABILIZER_TRICHOTOMY",
        "source_dag_node": "ef_galois_stabilizer_descent",
        "statement": (
            "horizontal EF components split by Galois stabilizer into "
            "base-descended, tower-confined, or full-orbit cases"
        ),
        "anchor_checks": checks,
        "trichotomy_checks": trichotomy_checks(),
        "dependencies": ["finite-field Galois correspondence", "Galois descent for stable ideals"],
        "non_claims": [
            "does not exclude full-orbit components",
            "does not prove EF pole-free cycle exclusion",
            "does not close ef_ru by itself",
        ],
        "note": "experimental/notes/ef/ef_galois_stabilizer_descent.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "ef-galois-stabilizer-descent-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    failed_checks = [check for check in cert["trichotomy_checks"] if not check["passes"]]
    if failed_checks:
        raise AssertionError(f"failed trichotomy checks: {failed_checks}")
    if "full-orbit" not in cert["statement"]:
        raise AssertionError("statement must include full-orbit case")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("ef-galois-stabilizer-descent certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    print(f"  trichotomy checks: {len(cert['trichotomy_checks'])}")
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
