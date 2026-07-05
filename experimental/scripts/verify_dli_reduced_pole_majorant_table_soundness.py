#!/usr/bin/env python3
"""Replay the DLI reduced-pole majorant-table soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_reduced_pole_majorant_table_soundness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-reduced-pole-majorant-table-soundness"
    / "dli_reduced_pole_majorant_table_soundness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_reduced_pole_majorant_table_soundness",
    "tuple_universe": "(central profile, nonzero frequency, harmonic, square-root component)",
    "domination": "D_tau <= M_tau",
    "non_claim": "remaining analytic DLI estimate",
}


def accepts_majorant_table(
    universe: set[str],
    true_degrees: dict[str, int],
    majorants: dict[str, int],
    budget: int,
) -> bool:
    if set(true_degrees) != universe or set(majorants) != universe:
        return False
    if budget < 0:
        return False
    for key in universe:
        if true_degrees[key] < 0 or majorants[key] < true_degrees[key]:
            return False
    return sum(majorants.values()) < budget


def toy_check() -> dict[str, Any]:
    universe = {"tau0", "tau1", "tau2"}
    true_degrees = {"tau0": 2, "tau1": 0, "tau2": 3}
    majorants = {"tau0": 2, "tau1": 1, "tau2": 4}
    budget = 8

    missing = dict(majorants)
    missing.pop("tau2")
    underbound = dict(majorants)
    underbound["tau2"] = 2
    too_large = dict(majorants)
    too_large["tau1"] = 5

    return {
        "universe_size": len(universe),
        "good_table_accepted": accepts_majorant_table(universe, true_degrees, majorants, budget),
        "missing_table_rejected": not accepts_majorant_table(universe, true_degrees, missing, budget),
        "underbound_rejected": not accepts_majorant_table(universe, true_degrees, underbound, budget),
        "over_budget_rejected": not accepts_majorant_table(universe, true_degrees, too_large, budget),
        "true_total": sum(true_degrees.values()),
        "majorant_total": sum(majorants.values()),
        "budget": budget,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-reduced-pole-majorant-table-soundness-v1",
        "status": "PROVED_MAJORANT_TABLE_REPLAY",
        "source_dag_node": "dli_reduced_pole_majorant_table_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not construct the majorant table",
            "does not prove Artin-Schreier nontriviality",
            "does not close the remaining analytic DLI estimate",
        ],
        "note": "experimental/notes/dli/dli_reduced_pole_majorant_table_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-reduced-pole-majorant-table-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_table_accepted",
        "missing_table_rejected",
        "underbound_rejected",
        "over_budget_rejected",
    ]
    if not all(check[name] for name in required):
        raise AssertionError(f"failed toy check: {check}")
    if not check["true_total"] <= check["majorant_total"] < check["budget"]:
        raise AssertionError(f"bad toy totals: {check}")


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
