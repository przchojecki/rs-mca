#!/usr/bin/env python3
"""Replay the M720 complete-certificate semantics packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m720" / "m720_certificate_semantics.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m720-certificate-semantics"
    / "m720_certificate_semantics.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "m720_certificate_semantics",
    "complete_rule": "complete = (W == n) and not aborted",
    "slice_local": "slice-local evidence",
    "non_claim": "does not run the MITM scan",
}


def complete_flag(n: int, w: int, aborted: bool) -> bool:
    return w == n and not aborted


def accepts_global_zero(record: dict[str, Any]) -> bool:
    return (
        record.get("complete") is True
        and record.get("unpaid_non_toral_active_cores") == 0
    )


def toy_check() -> dict[str, Any]:
    cases = [
        {"n": 32, "W": 32, "aborted": False, "zero": 0, "expected_complete": True, "expected_global": True},
        {"n": 32, "W": 16, "aborted": False, "zero": 0, "expected_complete": False, "expected_global": False},
        {"n": 32, "W": 32, "aborted": True, "zero": 0, "expected_complete": False, "expected_global": False},
        {"n": 32, "W": 32, "aborted": False, "zero": 1, "expected_complete": True, "expected_global": False},
    ]
    rows = []
    for case in cases:
        complete = complete_flag(case["n"], case["W"], case["aborted"])
        record = {
            "complete": complete,
            "unpaid_non_toral_active_cores": case["zero"],
        }
        rows.append(
            {
                **case,
                "computed_complete": complete,
                "accepted_global_zero": accepts_global_zero(record),
            }
        )
    return {
        "rows": rows,
        "all_expected": all(
            row["computed_complete"] == row["expected_complete"]
            and row["accepted_global_zero"] == row["expected_global"]
            for row in rows
        ),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "m720-certificate-semantics-v1",
        "status": "PROVED_CERTIFICATE_SEMANTICS_REPLAY",
        "source_dag_node": "m720_certificate_semantics",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not run the MITM scan",
            "does not construct zero certificates",
            "does not prove an official norm-gate payload",
        ],
        "note": "experimental/notes/m720/m720_certificate_semantics.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "m720-certificate-semantics-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["toy_check"]["all_expected"]:
        raise AssertionError(f"failed toy check: {cert['toy_check']}")


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
