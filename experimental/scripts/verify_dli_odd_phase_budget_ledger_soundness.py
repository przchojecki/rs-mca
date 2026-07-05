#!/usr/bin/env python3
"""Replay the DLI odd-phase budget-ledger soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_odd_phase_budget_ledger_soundness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-odd-phase-budget-ledger-soundness"
    / "dli_odd_phase_budget_ledger_soundness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_odd_phase_budget_ledger_soundness",
    "target": "dli_odd_phase_reduced_pole_budget",
    "tuple_universe": "(central profile, nonzero frequency, harmonic, square-root component)",
    "non_claim": "does not construct the ledger",
}

Key = tuple[str, str, int, str]


def accepts(required: list[Key], records: list[dict[str, Any]], budget: int) -> bool:
    by_key = {tuple(record.get("key", [])): record for record in records}
    if set(by_key) != set(required):
        return False
    total = 0
    for key in required:
        record = by_key[key]
        if record.get("artin_schreier_trivial") is not False:
            return False
        bound = record.get("reduced_pole_bound")
        if not isinstance(bound, int) or bound < 0:
            return False
        total += bound
    return total <= budget


def toy_check() -> dict[str, Any]:
    required: list[Key] = [
        ("profile-a", "lambda-1", 1, "component-0"),
        ("profile-a", "lambda-1", 2, "component-0"),
        ("profile-b", "lambda-2", 1, "component-1"),
    ]
    good = [
        {"key": list(key), "artin_schreier_trivial": False, "reduced_pole_bound": i}
        for i, key in enumerate(required, start=1)
    ]
    missing = good[:-1]
    trivial = [dict(record) for record in good]
    trivial[0]["artin_schreier_trivial"] = True
    malformed = [dict(record) for record in good]
    malformed[1]["reduced_pole_bound"] = -1
    too_large = [dict(record) for record in good]
    too_large[1]["reduced_pole_bound"] = 10

    budget = 6
    return {
        "required_rows": len(required),
        "good_ledger_accepted": accepts(required, good, budget),
        "missing_row_rejected": not accepts(required, missing, budget),
        "trivial_phase_rejected": not accepts(required, trivial, budget),
        "malformed_bound_rejected": not accepts(required, malformed, budget),
        "over_budget_rejected": not accepts(required, too_large, budget),
        "budget": budget,
        "good_total": sum(record["reduced_pole_bound"] for record in good),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-odd-phase-budget-ledger-soundness-v1",
        "status": "PROVED_BUDGET_LEDGER_REPLAY",
        "source_dag_node": "dli_odd_phase_budget_ledger_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not construct the odd-phase ledger",
            "does not prove the individual nontriviality certificates",
            "does not prove the remaining DLI equidistribution theorem",
        ],
        "note": "experimental/notes/dli/dli_odd_phase_budget_ledger_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-odd-phase-budget-ledger-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_ledger_accepted",
        "missing_row_rejected",
        "trivial_phase_rejected",
        "malformed_bound_rejected",
        "over_budget_rejected",
    ]
    if not all(check[name] for name in required):
        raise AssertionError(f"failed toy check: {check}")
    if check["good_total"] != check["budget"]:
        raise AssertionError(f"unexpected toy total: {check}")


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
