#!/usr/bin/env python3
"""Replay the E1 two-cell folded manifest assembly certificate."""

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
    / "e1-two-cell-folded-manifest-assembly-soundness"
    / "e1_two_cell_folded_manifest_assembly_soundness.json"
)
NOTE = (
    REPO
    / "experimental"
    / "notes"
    / "e1"
    / "e1_two_cell_folded_manifest_assembly_soundness.md"
)
OPEN_CELLS = {128, 256}

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e1_two_cell_folded_manifest_assembly_soundness",
    "cell_128": "e1_folded_certificate_cell_128_payload",
    "cell_256": "e1_folded_certificate_cell_256_payload",
    "manifest_payload": "e1_folded_certificate_manifest_payload",
    "non_claim": "does not prove either cell payload",
}


def valid_cell(cell: int, record: dict[str, object]) -> bool:
    return (
        cell in OPEN_CELLS
        and bool(record.get("field"))
        and record.get("complete") is True
        and record.get("nonzero_folded_vectors") == 0
    )


def assemble(cells: dict[int, dict[str, object]]) -> dict[int, dict[str, object]]:
    if set(cells) != OPEN_CELLS:
        raise AssertionError("manifest must cover exactly the two open cells")
    for cell, record in cells.items():
        if not valid_cell(cell, record):
            raise AssertionError(f"invalid cell record: {cell} {record}")
    return cells


def assembly_samples() -> list[dict[str, Any]]:
    good = {
        128: {"field": "named-exhibit-128", "complete": True, "nonzero_folded_vectors": 0},
        256: {"field": "named-exhibit-256", "complete": True, "nonzero_folded_vectors": 0},
    }
    missing = {
        128: {"field": "named-exhibit-128", "complete": True, "nonzero_folded_vectors": 0}
    }
    samples = []
    for name, cells, should_accept in (
        ("good_two_cell_manifest", good, True),
        ("missing_256_cell", missing, False),
    ):
        try:
            assemble(cells)
            accepted = True
        except AssertionError:
            accepted = False
        samples.append(
            {
                "name": name,
                "cells": sorted(cells),
                "accepted": accepted,
                "should_accept": should_accept,
                "passes": accepted == should_accept,
            }
        )
    return samples


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "e1-two-cell-folded-manifest-assembly-soundness-v1",
        "status": "PROVED_TWO_CELL_MANIFEST_ASSEMBLY",
        "source_dag_node": "e1_two_cell_folded_manifest_assembly_soundness",
        "statement": (
            "valid folded cell payload records for N'=128 and N'=256 assemble "
            "to the E1 folded-certificate manifest payload"
        ),
        "anchor_checks": checks,
        "assembly_samples": assembly_samples(),
        "dependencies": [
            "e1_folded_certificate_cell_128_payload",
            "e1_folded_certificate_cell_256_payload",
        ],
        "non_claims": [
            "does not prove either folded cell payload",
            "does not supply no-vector certificates",
        ],
        "note": "experimental/notes/e1/e1_two_cell_folded_manifest_assembly_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "e1-two-cell-folded-manifest-assembly-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    failed_samples = [sample for sample in cert["assembly_samples"] if not sample["passes"]]
    if failed_samples:
        raise AssertionError(f"failed assembly samples: {failed_samples}")


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
        print(f"{cert['status']}: {len(cert['assembly_samples'])} samples")


if __name__ == "__main__":
    main()
