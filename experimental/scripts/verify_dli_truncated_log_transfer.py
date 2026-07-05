#!/usr/bin/env python3
"""Replay the DLI truncated-log transfer packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_truncated_log_transfer.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-truncated-log-transfer"
    / "dli_truncated_log_transfer.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_truncated_log_transfer",
    "constant_dependency": "dli_circle_log_integral_constant",
    "error_hypothesis": "sum_j eps_j=o(t)",
    "non_claim": "finite-frequency Weyl bounds",
}


def accepts_truncation_transfer(records: list[dict[str, Any]], total_error_budget: float) -> bool:
    total_error = 0.0
    for record in records:
        full_loss = record.get("full_loss")
        truncated_loss = record.get("truncated_loss")
        discrepancy_error = record.get("discrepancy_error")
        peak_tail_error = record.get("peak_tail_error")
        for value in (full_loss, truncated_loss, discrepancy_error, peak_tail_error):
            if not isinstance(value, (int, float)):
                return False
        if full_loss < truncated_loss:
            return False
        if discrepancy_error < 0 or peak_tail_error < 0:
            return False
        total_error += discrepancy_error + peak_tail_error
    return total_error <= total_error_budget


def toy_check() -> dict[str, Any]:
    records = [
        {"profile": "j0", "full_loss": 11.0, "truncated_loss": 9.5, "discrepancy_error": 0.1, "peak_tail_error": 0.2},
        {"profile": "j1", "full_loss": 7.0, "truncated_loss": 7.0, "discrepancy_error": 0.05, "peak_tail_error": 0.05},
    ]
    bad_truncation = [dict(record) for record in records]
    bad_truncation[0]["truncated_loss"] = 12.0
    bad_error = [dict(record) for record in records]
    bad_error[1]["peak_tail_error"] = -0.1
    over_budget = [dict(record) for record in records]
    over_budget[0]["discrepancy_error"] = 10.0

    return {
        "good_records_accepted": accepts_truncation_transfer(records, total_error_budget=0.5),
        "bad_truncation_rejected": not accepts_truncation_transfer(bad_truncation, total_error_budget=0.5),
        "bad_error_rejected": not accepts_truncation_transfer(bad_error, total_error_budget=0.5),
        "over_budget_rejected": not accepts_truncation_transfer(over_budget, total_error_budget=0.5),
        "record_count": len(records),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-truncated-log-transfer-v1",
        "status": "PROVED_TRUNCATED_LOG_TRANSFER_REPLAY",
        "source_dag_node": "dli_truncated_log_transfer",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove truncated-log discrepancy",
            "does not prove peak-mass tails",
            "does not prove finite-frequency Weyl bounds",
        ],
        "note": "experimental/notes/dli/dli_truncated_log_transfer.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-truncated-log-transfer-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_records_accepted",
        "bad_truncation_rejected",
        "bad_error_rejected",
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
