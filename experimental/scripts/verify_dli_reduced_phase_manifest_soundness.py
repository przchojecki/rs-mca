#!/usr/bin/env python3
"""Replay the DLI reduced-phase manifest soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_reduced_phase_manifest_soundness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-reduced-phase-manifest-soundness"
    / "dli_reduced_phase_manifest_soundness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_reduced_phase_manifest_soundness",
    "polar_payload": "dli_odd_phase_polar_obstruction_payload",
    "majorant_payload": "dli_reduced_pole_majorant_table_payload",
    "polar_soundness": "dli_odd_phase_polar_obstruction_soundness",
    "majorant_soundness": "dli_reduced_pole_majorant_table_soundness",
    "non_claim": "does not construct the actual",
}


def verifies_polar_obstruction(p: int, reduced_pole_order: int) -> bool:
    return p > 1 and reduced_pole_order > 0 and reduced_pole_order % p != 0


def verify_manifest(universe: set[str], manifest: dict[str, dict[str, Any]], budget: int, p: int) -> bool:
    if set(manifest) != universe:
        return False
    total = 0
    for key, row in manifest.items():
        if row.get("tuple_id") != key:
            return False
        if not row.get("local_expansion"):
            return False
        if not verifies_polar_obstruction(p, row.get("reduced_pole_order", 0)):
            return False
        true_degree = row.get("true_reduced_polar_degree")
        majorant = row.get("majorant")
        if not isinstance(true_degree, int) or not isinstance(majorant, int):
            return False
        if true_degree < 0 or majorant < true_degree:
            return False
        total += majorant
    return total < budget


def toy_check() -> dict[str, Any]:
    p = 5
    budget = 8
    universe = {"tau0", "tau1", "tau2"}
    manifest: dict[str, dict[str, Any]] = {
        "tau0": {
            "tuple_id": "tau0",
            "local_expansion": "u^-3 + O(1)",
            "reduced_pole_order": 3,
            "true_reduced_polar_degree": 3,
            "majorant": 3,
        },
        "tau1": {
            "tuple_id": "tau1",
            "local_expansion": "u^-2 + O(1)",
            "reduced_pole_order": 2,
            "true_reduced_polar_degree": 2,
            "majorant": 3,
        },
        "tau2": {
            "tuple_id": "tau2",
            "local_expansion": "u^-1 + O(1)",
            "reduced_pole_order": 1,
            "true_reduced_polar_degree": 1,
            "majorant": 1,
        },
    }

    missing = dict(manifest)
    missing.pop("tau2")
    bad_pole = {key: dict(row) for key, row in manifest.items()}
    bad_pole["tau1"]["reduced_pole_order"] = 10
    underbound = {key: dict(row) for key, row in manifest.items()}
    underbound["tau0"]["majorant"] = 2
    over_budget = {key: dict(row) for key, row in manifest.items()}
    over_budget["tau2"]["majorant"] = 5

    return {
        "field_characteristic": p,
        "universe_size": len(universe),
        "good_manifest_accepted": verify_manifest(universe, manifest, budget, p),
        "missing_tuple_rejected": not verify_manifest(universe, missing, budget, p),
        "bad_reduced_pole_rejected": not verify_manifest(universe, bad_pole, budget, p),
        "underbound_rejected": not verify_manifest(universe, underbound, budget, p),
        "over_budget_rejected": not verify_manifest(universe, over_budget, budget, p),
        "majorant_total": sum(row["majorant"] for row in manifest.values()),
        "budget": budget,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-reduced-phase-manifest-soundness-v1",
        "status": "PROVED_MANIFEST_SOUNDNESS_REPLAY",
        "source_dag_node": "dli_reduced_phase_manifest_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "payloads_supplied": [
            "dli_odd_phase_polar_obstruction_payload",
            "dli_reduced_pole_majorant_table_payload",
        ],
        "non_claims": [
            "does not construct the actual manifest",
            "does not prove the harmonic o(t) estimate independently",
            "does not close the remaining DLI analytic gap",
        ],
        "note": "experimental/notes/dli/dli_reduced_phase_manifest_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-reduced-phase-manifest-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_manifest_accepted",
        "missing_tuple_rejected",
        "bad_reduced_pole_rejected",
        "underbound_rejected",
        "over_budget_rejected",
    ]
    if not all(check[name] for name in required):
        raise AssertionError(f"failed toy check: {check}")
    if not check["majorant_total"] < check["budget"]:
        raise AssertionError(f"bad toy budget: {check}")


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
