#!/usr/bin/env python3
"""Replay the M720 official norm-gate case-manifest soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m720" / "m720_official_norm_gate_case_manifest_soundness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m720-official-norm-gate-case-manifest-soundness"
    / "m720_official_norm_gate_case_manifest_soundness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "m720_official_norm_gate_case_manifest_soundness",
    "target": "m720_official_h7_20_norm_gate_payload",
    "semantics_dependency": "m720_certificate_semantics",
    "non_claim": "does not construct the official",
}


def accepts_manifest(cases: set[str], entries: dict[str, dict[str, Any]]) -> bool:
    if set(entries) != cases:
        return False
    for entry in entries.values():
        kind = entry.get("kind")
        if kind == "uniform_theorem":
            if not entry.get("citation"):
                return False
        elif kind == "certificate":
            if entry.get("complete") is not True:
                return False
            if entry.get("unpaid_non_toral_survivors") != 0:
                return False
        else:
            return False
    return True


def toy_check() -> dict[str, Any]:
    cases = {"h7-row-a", "h8-row-a", "h16-row-b"}
    good = {
        "h7-row-a": {"kind": "certificate", "complete": True, "unpaid_non_toral_survivors": 0},
        "h8-row-a": {"kind": "certificate", "complete": True, "unpaid_non_toral_survivors": 0},
        "h16-row-b": {"kind": "uniform_theorem", "citation": "uniform-norm-gate"},
    }
    missing = dict(good)
    missing.pop("h16-row-b")
    no_citation = {key: dict(value) for key, value in good.items()}
    no_citation["h16-row-b"]["citation"] = ""
    incomplete = {key: dict(value) for key, value in good.items()}
    incomplete["h7-row-a"]["complete"] = False
    nonzero = {key: dict(value) for key, value in good.items()}
    nonzero["h8-row-a"]["unpaid_non_toral_survivors"] = 1
    bad_kind = {key: dict(value) for key, value in good.items()}
    bad_kind["h7-row-a"]["kind"] = "slice_evidence"

    return {
        "good_manifest_accepted": accepts_manifest(cases, good),
        "missing_case_rejected": not accepts_manifest(cases, missing),
        "missing_citation_rejected": not accepts_manifest(cases, no_citation),
        "incomplete_certificate_rejected": not accepts_manifest(cases, incomplete),
        "nonzero_survivor_rejected": not accepts_manifest(cases, nonzero),
        "bad_kind_rejected": not accepts_manifest(cases, bad_kind),
        "case_count": len(cases),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "m720-official-norm-gate-case-manifest-soundness-v1",
        "status": "PROVED_CASE_MANIFEST_SOUNDNESS_REPLAY",
        "source_dag_node": "m720_official_norm_gate_case_manifest_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not construct the official case manifest",
            "does not prove a uniform nonvanishing theorem",
            "does not run an M720 MITM payload scan",
        ],
        "note": "experimental/notes/m720/m720_official_norm_gate_case_manifest_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "m720-official-norm-gate-case-manifest-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_manifest_accepted",
        "missing_case_rejected",
        "missing_citation_rejected",
        "incomplete_certificate_rejected",
        "nonzero_survivor_rejected",
        "bad_kind_rejected",
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
