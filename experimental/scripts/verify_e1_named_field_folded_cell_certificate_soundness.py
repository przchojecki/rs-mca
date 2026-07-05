#!/usr/bin/env python3
"""Replay the E1 named-field folded-cell schema certificate."""

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
    / "e1-named-field-folded-cell-certificate-soundness"
    / "e1_named_field_folded_cell_certificate_soundness.json"
)
NOTE = (
    REPO
    / "experimental"
    / "notes"
    / "e1"
    / "e1_named_field_folded_cell_certificate_soundness.md"
)

P = 904625697166646869347790708689937759412227977745095982970820953353127723009
RHO = {
    128: 440266185830122294862552098878717819794821358702875176198798016633729926114,
    256: 368095729527972287347366462180303065908636718991804826343652948937354262881,
}

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e1_named_field_folded_cell_certificate_soundness",
    "field_dependency": "e1_pocklington_250bit_exhibit_field",
    "zero_certificate": "zero nonzero non-cyclotomic folded vectors",
    "cell_schema": "cell schema",
    "non_claim": "does not supply either no-vector payload",
}


def verify_cell(cell: int, record: dict[str, object]) -> dict[str, Any]:
    return {
        "cell": cell,
        "field_matches": record["field"] == P,
        "root_matches": record["root"] == RHO[cell],
        "p_congruent_1_mod_cell": P % cell == 1,
        "root_order": pow(RHO[cell], cell, P) == 1,
        "root_half_order_not_one": pow(RHO[cell], cell // 2, P) != 1,
        "complete": record["complete"] is True,
        "zero_noncyclotomic": record["nonzero_folded_vectors"] == 0,
    }


def sample_cells() -> list[dict[str, Any]]:
    out = []
    for cell in (128, 256):
        record = {
            "field": P,
            "root": RHO[cell],
            "complete": True,
            "nonzero_folded_vectors": 0,
        }
        check = verify_cell(cell, record)
        check["passes"] = all(value for key, value in check.items() if key != "cell")
        out.append(check)
    return out


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "e1-named-field-folded-cell-certificate-soundness-v1",
        "status": "PROVED_NAMED_FIELD_CELL_SCHEMA",
        "source_dag_node": "e1_named_field_folded_cell_certificate_soundness",
        "statement": (
            "a named prime field/root plus a complete zero folded no-vector "
            "record satisfies the E1 folded cell payload schema"
        ),
        "anchor_checks": checks,
        "sample_cells": sample_cells(),
        "dependencies": [
            "e1_pocklington_250bit_exhibit_field",
            "cell-specific folded no-vector payload",
        ],
        "non_claims": [
            "does not supply either no-vector payload",
            "does not certify the two-cell manifest by itself",
        ],
        "note": "experimental/notes/e1/e1_named_field_folded_cell_certificate_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "e1-named-field-folded-cell-certificate-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    failed_cells = [cell for cell in cert["sample_cells"] if not cell["passes"]]
    if failed_cells:
        raise AssertionError(f"failed cell checks: {failed_cells}")


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
        print(f"{cert['status']}: {len(cert['sample_cells'])} sample cells checked")


if __name__ == "__main__":
    main()
