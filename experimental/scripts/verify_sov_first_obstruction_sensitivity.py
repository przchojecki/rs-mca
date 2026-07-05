#!/usr/bin/env python3
"""Replay the SOV first-obstruction sensitivity packet."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from verify_sov_forced_root_recursion_algebra import (
    forced_obstructions,
    locator_from_roots,
    poly_mul,
)


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "sov" / "sov_first_obstruction_sensitivity.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "sov-first-obstruction-sensitivity"
    / "sov_first_obstruction_sensitivity.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "sov_first_obstruction_sensitivity",
    "recursion_dependency": "sov_forced_root_recursion_algebra",
    "first_obstruction": "O_{h-1} = [X^{h-1}](S^2 - L)",
    "negative_shift": "O_{h-1} -> O_{h-1} - delta",
    "non_claim": "small value sets or",
}


def sensitivity_check() -> dict[str, Any]:
    h = 10
    p = 65537
    roots = random.Random(99).sample(range(2, p - 1), h)
    a_poly = locator_from_roots(roots, p)
    b_poly = list(a_poly)
    b_poly[0] = (b_poly[0] + 17) % p
    locator = poly_mul(a_poly, b_poly, p)
    root0, obs0, constant0 = forced_obstructions(locator, p, h)

    rows = []
    for delta in (1, 7, p - 3):
        perturbed = list(locator)
        perturbed[h - 1] = (perturbed[h - 1] + delta) % p
        root1, obs1, constant1 = forced_obstructions(perturbed, p, h)
        rows.append(
            {
                "delta": delta,
                "root_unchanged": root1 == root0,
                "lower_obstructions_unchanged": obs1[:-1] == obs0[:-1],
                "first_obstruction_shift": (obs1[-1] - obs0[-1]) % p,
                "expected_shift": (-delta) % p,
                "constant_unchanged": constant1 == constant0,
            }
        )

    return {
        "h": h,
        "p": p,
        "cases": rows,
        "all_passed": all(
            row["root_unchanged"]
            and row["lower_obstructions_unchanged"]
            and row["first_obstruction_shift"] == row["expected_shift"]
            and row["constant_unchanged"]
            for row in rows
        ),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "sov-first-obstruction-sensitivity-v1",
        "status": "PROVED_SENSITIVITY_REPLAY",
        "source_dag_node": "sov_first_obstruction_sensitivity",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "sensitivity_check": sensitivity_check(),
        "non_claims": [
            "does not prove small value sets",
            "does not prove the SOV character-sum bound",
        ],
        "note": "experimental/notes/sov/sov_first_obstruction_sensitivity.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "sov-first-obstruction-sensitivity-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["sensitivity_check"]["all_passed"]:
        raise AssertionError(f"failed sensitivity check: {cert['sensitivity_check']}")


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
        print(f"{cert['status']}: {cert['sensitivity_check']}")


if __name__ == "__main__":
    main()
