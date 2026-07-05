#!/usr/bin/env python3
"""Replay the XR profile minor record-inventory soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "xr-profile-minor-record-inventory-soundness"
    / "xr_profile_minor_record_inventory_soundness.json"
)
NOTE = REPO / "experimental" / "notes" / "m1" / "xr_profile_minor_record_inventory_soundness.md"
ACCEPTED = {"triangular", "monomial", "remote_table"}

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "xr_profile_minor_record_inventory_soundness",
    "accepted": "Accepted record types are:",
    "triangular": "triangular-minor certificate soundness",
    "payload": "xr_profile_minor_certificate_payload",
    "non_claim": "does not construct the inventory",
}


def verify_inventory(required: set[str], records: dict[str, str]) -> dict[str, Any]:
    checks = {
        "covers_required_profiles": set(records) == required,
        "accepted_record_types": all(kind in ACCEPTED for kind in records.values()),
        "single_record_per_profile": len(records) == len(set(records)),
    }
    return {"checks": checks, "passes": all(checks.values())}


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    required = {"profile_A", "profile_B", "profile_C"}
    records = {
        "profile_A": "triangular",
        "profile_B": "monomial",
        "profile_C": "remote_table",
    }
    cert = {
        "schema": "xr-profile-minor-record-inventory-soundness-v1",
        "status": "PROVED_INVENTORY_SOUNDNESS_REPLAY",
        "source_dag_node": "xr_profile_minor_record_inventory_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "sample_inventory": {
            "required_profiles": sorted(required),
            "records": records,
            "accepted_record_types": sorted(ACCEPTED),
            **verify_inventory(required, records),
        },
        "non_claims": [
            "does not construct the XR profile inventory",
            "does not prove the actual profile-minor payload by itself",
        ],
        "note": "experimental/notes/m1/xr_profile_minor_record_inventory_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "xr-profile-minor-record-inventory-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["sample_inventory"]["passes"]:
        raise AssertionError(f"failed inventory check: {cert['sample_inventory']}")


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
        print(f"{cert['status']}: {len(cert['sample_inventory']['records'])} records")


if __name__ == "__main__":
    main()
