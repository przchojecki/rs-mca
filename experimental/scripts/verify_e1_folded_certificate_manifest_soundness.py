#!/usr/bin/env python3
"""Replay the E1 folded-certificate manifest soundness packet."""

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
    / "e1-folded-certificate-manifest-soundness"
    / "e1_folded_certificate_manifest_soundness.json"
)
NOTE = REPO / "experimental" / "notes" / "e1" / "e1_folded_certificate_manifest_soundness.md"
OPEN_CELLS = {128, 256}

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e1_folded_certificate_manifest_soundness",
    "open_cells": "N' in {128,256}",
    "control_payload": "e1_open_cell_control_payload",
    "folded_route": "folded-certificate route",
    "non_claim": "does not provide the actual",
}


def verify_manifest(manifest: dict[int, dict[str, object]]) -> dict[str, Any]:
    checks = {
        "covers_open_cells": set(manifest) == OPEN_CELLS,
        "fields_named": all(bool(record.get("field")) for record in manifest.values()),
        "searches_complete": all(record.get("complete") is True for record in manifest.values()),
        "zero_noncyclotomic": all(
            record.get("nonzero_folded_vectors") == 0 for record in manifest.values()
        ),
    }
    return {"checks": checks, "passes": all(checks.values())}


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    manifest = {
        128: {"field": "named-exhibit-128", "complete": True, "nonzero_folded_vectors": 0},
        256: {"field": "named-exhibit-256", "complete": True, "nonzero_folded_vectors": 0},
    }
    cert = {
        "schema": "e1-folded-certificate-manifest-soundness-v1",
        "status": "PROVED_MANIFEST_ROUTE_SOUNDNESS",
        "source_dag_node": "e1_folded_certificate_manifest_soundness",
        "statement": (
            "a manifest covering N'=128 and N'=256 with named complete zero "
            "folded certificates satisfies the E1 open-cell folded route"
        ),
        "anchor_checks": checks,
        "sample_manifest": {
            "cells": sorted(manifest),
            **verify_manifest(manifest),
        },
        "dependencies": ["definition of e1_open_cell_control_payload folded-certificate route"],
        "non_claims": [
            "does not provide the actual two-cell certificate transcripts",
            "does not certify either no-vector payload",
        ],
        "note": "experimental/notes/e1/e1_folded_certificate_manifest_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "e1-folded-certificate-manifest-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["sample_manifest"]["passes"]:
        raise AssertionError(f"sample manifest failed: {cert['sample_manifest']}")


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
        print(f"{cert['status']}: manifest cells {cert['sample_manifest']['cells']}")


if __name__ == "__main__":
    main()
