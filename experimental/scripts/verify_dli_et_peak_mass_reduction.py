#!/usr/bin/env python3
"""Replay the DLI Erdos-Turan peak-mass reduction packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_et_peak_mass_reduction.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-et-peak-mass-reduction"
    / "dli_et_peak_mass_reduction.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_et_peak_mass_reduction",
    "erdos_turan": "|#{y : theta_y in I}/Y - |I||",
    "layer_cake": "min(F,T) = int_0^T 1_{F >= u} du",
    "target": "dli_truncated_log_transfer",
    "non_claim": "does not prove the finite-frequency",
}


def accepts_annulus_budget(records: list[dict[str, Any]], budget: float) -> bool:
    total = 0.0
    for record in records:
        if record.get("annulus_interval_count", 0) > 2:
            return False
        discrepancy = record.get("interval_discrepancy")
        layer_weight = record.get("layer_weight")
        if not isinstance(discrepancy, (int, float)) or not isinstance(layer_weight, (int, float)):
            return False
        if discrepancy < 0 or layer_weight < 0:
            return False
        total += discrepancy * layer_weight
    return total <= budget


def toy_check() -> dict[str, Any]:
    records = [
        {"annulus": "peak0-r0", "annulus_interval_count": 2, "interval_discrepancy": 0.01, "layer_weight": 3.0},
        {"annulus": "peak0-r1", "annulus_interval_count": 2, "interval_discrepancy": 0.02, "layer_weight": 2.0},
        {"annulus": "peak1-r0", "annulus_interval_count": 1, "interval_discrepancy": 0.01, "layer_weight": 1.0},
    ]
    bad_interval_count = [dict(record) for record in records]
    bad_interval_count[0]["annulus_interval_count"] = 3
    bad_discrepancy = [dict(record) for record in records]
    bad_discrepancy[1]["interval_discrepancy"] = -0.1
    over_budget = [dict(record) for record in records]
    over_budget[2]["layer_weight"] = 100.0

    return {
        "good_budget_accepted": accepts_annulus_budget(records, budget=0.09),
        "bad_interval_count_rejected": not accepts_annulus_budget(bad_interval_count, budget=0.09),
        "bad_discrepancy_rejected": not accepts_annulus_budget(bad_discrepancy, budget=0.09),
        "over_budget_rejected": not accepts_annulus_budget(over_budget, budget=0.09),
        "record_count": len(records),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-et-peak-mass-reduction-v1",
        "status": "PROVED_ET_PEAK_TRANSFER_REPLAY",
        "source_dag_node": "dli_et_peak_mass_reduction",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": ["does not prove finite-frequency Weyl-sum bounds"],
        "note": "experimental/notes/dli/dli_et_peak_mass_reduction.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-et-peak-mass-reduction-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_budget_accepted",
        "bad_interval_count_rejected",
        "bad_discrepancy_rejected",
        "over_budget_rejected",
    ]
    if not all(check[name] for name in required):
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
