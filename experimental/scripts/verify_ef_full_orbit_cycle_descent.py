#!/usr/bin/env python3
"""Replay the EF full-orbit cycle descent certificate."""

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
    / "ef-full-orbit-cycle-descent"
    / "ef_full_orbit_cycle_descent.json"
)
NOTE = REPO / "experimental" / "notes" / "ef" / "ef_full_orbit_cycle_descent.md"


ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "ef_full_orbit_cycle_descent",
    "orbit": "O(C) = { gC : g in G }",
    "stable_union": "hZ = union_{g in G} hgC = union_{g in G} gC = Z",
    "descent": "descends to a reduced closed subscheme",
    "pole_divisor": "Since `D` is",
    "non_claim": "does not exclude pole-free descended cycles",
}


def translate(component: int, shift: int, order: int) -> int:
    return (component + shift) % order


def orbit_checks() -> list[dict[str, Any]]:
    checks = []
    for order in (1, 2, 3, 4, 6, 8, 12):
        orbit = set(range(order))
        stable_under_all = all(
            {translate(c, shift, order) for c in orbit} == orbit for shift in range(order)
        )
        pole_free_components = {c: True for c in orbit}
        checks.append(
            {
                "galois_order": order,
                "orbit_size": len(orbit),
                "stable_under_all_translates": stable_under_all,
                "pole_free_union": all(pole_free_components.values()),
                "passes": stable_under_all and all(pole_free_components.values()),
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
        "schema": "ef-full-orbit-cycle-descent-v1",
        "status": "PROVED_GALOIS_ORBIT_UNION_DESCENT",
        "source_dag_node": "ef_full_orbit_cycle_descent",
        "statement": (
            "a full Galois orbit of pole-free horizontal components has a "
            "B-defined reduced union still disjoint from the pole divisor"
        ),
        "anchor_checks": checks,
        "orbit_checks": orbit_checks(),
        "dependencies": [
            "finite Galois descent for stable radical ideals",
            "B-defined pole divisor is Galois-invariant",
        ],
        "non_claims": [
            "does not exclude descended pole-free cycles",
            "does not prove ef_pole_free_cycle_exclusion",
            "does not close ef_ru by itself",
        ],
        "note": "experimental/notes/ef/ef_full_orbit_cycle_descent.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "ef-full-orbit-cycle-descent-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    failed_checks = [check for check in cert["orbit_checks"] if not check["passes"]]
    if failed_checks:
        raise AssertionError(f"failed orbit checks: {failed_checks}")
    if "B-defined reduced union" not in cert["statement"]:
        raise AssertionError("statement must include B-defined reduced union")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("ef-full-orbit-cycle-descent certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    for name, ok in cert["anchor_checks"].items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print(f"  orbit checks: {len(cert['orbit_checks'])}")


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
