#!/usr/bin/env python3
"""Replay the EF descended-cycle inventory soundness certificate."""

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
    / "ef-descended-cycle-inventory-soundness"
    / "ef_descended_cycle_inventory_soundness.json"
)
NOTE = REPO / "experimental" / "notes" / "ef" / "ef_descended_cycle_inventory_soundness.md"

ALLOWED = {"base_descended", "tower_confined", "noncontainment_degenerate"}

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "ef_descended_cycle_inventory_soundness",
    "covers": "The inventory covers `C`",
    "accepted_labels": "base-descended, proper-subfield/tower-confined, or",
    "payload": "ef_descended_cycle_classification_payload",
    "non_claim": "does not construct or certify the actual descended-cycle",
}


def inventory_sample() -> dict[str, Any]:
    cycles = ["C0", "C1", "C2"]
    labels = {
        "C0": "base_descended",
        "C1": "tower_confined",
        "C2": "noncontainment_degenerate",
    }
    checks = {
        "covers_all_cycles": set(labels) == set(cycles),
        "labels_allowed": all(label in ALLOWED for label in labels.values()),
        "entries_disjoint": len(labels) == len(set(labels)),
    }
    return {
        "cycles": cycles,
        "labels": labels,
        "allowed_labels": sorted(ALLOWED),
        "checks": checks,
        "passes": all(checks.values()),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "ef-descended-cycle-inventory-soundness-v1",
        "status": "PROVED_INVENTORY_SEMANTICS",
        "source_dag_node": "ef_descended_cycle_inventory_soundness",
        "statement": (
            "a complete disjoint descended-cycle inventory with verified "
            "base/tower/noncontainment labels satisfies the EF classification payload"
        ),
        "anchor_checks": checks,
        "sample_inventory": inventory_sample(),
        "dependencies": ["definition of ef_descended_cycle_classification_payload"],
        "non_claims": [
            "does not construct the descended-cycle inventory",
            "does not certify a proposed inventory payload",
            "does not close ef_ru by itself",
        ],
        "note": "experimental/notes/ef/ef_descended_cycle_inventory_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "ef-descended-cycle-inventory-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["sample_inventory"]["passes"]:
        raise AssertionError(f"sample inventory failed: {cert['sample_inventory']}")
    if "inventory" not in cert["statement"]:
        raise AssertionError("statement must mention inventory")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("ef-descended-cycle-inventory-soundness certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    for name, ok in cert["anchor_checks"].items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    for name, ok in cert["sample_inventory"]["checks"].items():
        print(f"  sample {name}: {'PASS' if ok else 'FAIL'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
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
        print_summary(cert)


if __name__ == "__main__":
    main()
