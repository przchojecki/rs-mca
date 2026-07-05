#!/usr/bin/env python3
"""Replay the M720 official norm-gate payload soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m720" / "m720_official_norm_gate_certificate_soundness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m720-official-norm-gate-certificate-soundness"
    / "m720_official_norm_gate_certificate_soundness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "m720_official_norm_gate_certificate_soundness",
    "alignment_dependency": "m720_official_paid_branch_alignment",
    "semantics_dependency": "m720_certificate_semantics",
    "non_claim": "does not provide the actual official",
}


def accepts_payload(expected_cases: list[tuple[int, int]], records: list[dict[str, Any]]) -> bool:
    by_case = {tuple(record.get("case", [])): record for record in records}
    if set(by_case) != set(expected_cases):
        return False
    for case in expected_cases:
        record = by_case[case]
        if record.get("branch") != "primitive_norm_gate":
            return False
        if record.get("complete") is not True:
            return False
        if record.get("unpaid_non_toral_survivors") != 0:
            return False
    return True


def toy_check() -> dict[str, Any]:
    expected = [(128, 7), (128, 8), (256, 20)]
    good = [
        {"case": [128, 7], "branch": "primitive_norm_gate", "complete": True, "unpaid_non_toral_survivors": 0},
        {"case": [128, 8], "branch": "primitive_norm_gate", "complete": True, "unpaid_non_toral_survivors": 0},
        {"case": [256, 20], "branch": "primitive_norm_gate", "complete": True, "unpaid_non_toral_survivors": 0},
    ]
    missing = good[:-1]
    bad_branch = [dict(record) for record in good]
    bad_branch[0]["branch"] = "slice_evidence"
    incomplete = [dict(record) for record in good]
    incomplete[1]["complete"] = False
    nonzero = [dict(record) for record in good]
    nonzero[2]["unpaid_non_toral_survivors"] = 1

    return {
        "good_payload_accepted": accepts_payload(expected, good),
        "missing_case_rejected": not accepts_payload(expected, missing),
        "bad_branch_rejected": not accepts_payload(expected, bad_branch),
        "incomplete_record_rejected": not accepts_payload(expected, incomplete),
        "nonzero_survivor_rejected": not accepts_payload(expected, nonzero),
        "expected_case_count": len(expected),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "m720-official-norm-gate-certificate-soundness-v1",
        "status": "PROVED_NORM_GATE_PAYLOAD_SOUNDNESS_REPLAY",
        "source_dag_node": "m720_official_norm_gate_certificate_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "dependencies": ["m720_official_paid_branch_alignment", "m720_certificate_semantics"],
        "non_claims": [
            "does not provide the actual official h=7..20 payload",
            "does not run M720 MITM certificates",
            "does not prove branch alignment in this packet",
        ],
        "note": "experimental/notes/m720/m720_official_norm_gate_certificate_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "m720-official-norm-gate-certificate-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_payload_accepted",
        "missing_case_rejected",
        "bad_branch_rejected",
        "incomplete_record_rejected",
        "nonzero_survivor_rejected",
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
