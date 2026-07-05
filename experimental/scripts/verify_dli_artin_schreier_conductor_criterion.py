#!/usr/bin/env python3
"""Replay the DLI Artin-Schreier conductor-criterion packet."""

from __future__ import annotations

import argparse
import cmath
import json
import math
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_artin_schreier_conductor_criterion.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-artin-schreier-conductor-criterion"
    / "dli_artin_schreier_conductor_criterion.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_artin_schreier_conductor_criterion",
    "coboundary_form": "f = g^p - g + c",
    "conductor_control": "global conductor is controlled",
    "non_claim": "does not verify a deployed row",
}


def additive_character(p: int, x: int) -> complex:
    return cmath.exp(2j * math.pi * (x % p) / p)


def toy_coboundary_check() -> dict[str, Any]:
    p = 5
    c = 3

    def g(x: int) -> int:
        return (x * x + 2 * x + 1) % p

    values = []
    for x in range(p):
        f = (pow(g(x), p, p) - g(x) + c) % p
        values.append(additive_character(p, f))

    constant_trace = all(abs(v - values[0]) < 1e-12 for v in values)
    equals_constant = abs(values[0] - additive_character(p, c)) < 1e-12
    return {
        "field": f"F_{p}",
        "constant": c,
        "points_checked": p,
        "constant_trace": constant_trace,
        "equals_constant_phase": equals_constant,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-artin-schreier-conductor-criterion-v1",
        "status": "PROVED_CRITERION_REPLAY",
        "source_dag_node": "dli_artin_schreier_conductor_criterion",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_coboundary_check(),
        "non_claims": [
            "does not construct a DLI reduced-phase manifest",
            "does not verify a deployed row",
            "does not prove the remaining harmonic conductor ledger",
        ],
        "note": "experimental/notes/dli/dli_artin_schreier_conductor_criterion.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-artin-schreier-conductor-criterion-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    if not (check["constant_trace"] and check["equals_constant_phase"]):
        raise AssertionError(f"failed toy check: {check}")


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
