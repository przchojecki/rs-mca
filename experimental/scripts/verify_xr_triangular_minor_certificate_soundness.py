#!/usr/bin/env python3
"""Replay the XR triangular-minor certificate-soundness packet."""

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
    / "xr-triangular-minor-certificate-soundness"
    / "xr_triangular_minor_certificate_soundness.json"
)
NOTE = REPO / "experimental" / "notes" / "m1" / "xr_triangular_minor_certificate_soundness.md"

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "xr_triangular_minor_certificate_soundness",
    "det_formula": "det(A) = prod_i A_{ii}",
    "nonzero_diag": "every diagonal entry is nonzero",
    "non_claim": "profile inventory",
}


def det(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 0:
        return 1
    total = 0
    for col, value in enumerate(matrix[0]):
        sub = [row[:col] + row[col + 1 :] for row in matrix[1:]]
        total += ((-1) ** col) * value * det(sub)
    return total


def diag_product(matrix: list[list[int]]) -> int:
    out = 1
    for i, row in enumerate(matrix):
        out *= row[i]
    return out


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    upper = [[2, 7, -1], [0, -3, 5], [0, 0, 11]]
    lower = [[5, 0, 0, 0], [1, -2, 0, 0], [9, 3, 7, 0], [4, 6, 8, -1]]
    zero_diag = [[2, 1, 4], [0, 0, 3], [0, 0, 5]]
    matrix_checks = []
    for name, matrix in (("upper", upper), ("lower", lower)):
        determinant = det(matrix)
        product = diag_product(matrix)
        matrix_checks.append(
            {
                "name": name,
                "determinant": determinant,
                "diagonal_product": product,
                "matches": determinant == product,
                "nonzero": determinant != 0,
            }
        )
    zero_det = det(zero_diag)
    cert = {
        "schema": "xr-triangular-minor-certificate-soundness-v1",
        "status": "PROVED_TRIANGULAR_MINOR_SOUNDNESS_REPLAY",
        "source_dag_node": "xr_triangular_minor_certificate_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "matrix_checks": matrix_checks,
        "zero_diagonal_control": {"determinant": zero_det, "passes": zero_det == 0},
        "non_claims": [
            "does not construct the profile inventory",
            "does not claim every profile has a triangular certificate",
        ],
        "note": "experimental/notes/m1/xr_triangular_minor_certificate_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "xr-triangular-minor-certificate-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if any(not (row["matches"] and row["nonzero"]) for row in cert["matrix_checks"]):
        raise AssertionError(f"failed triangular matrix checks: {cert['matrix_checks']}")
    if not cert["zero_diagonal_control"]["passes"]:
        raise AssertionError("zero diagonal control failed")


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
        print(f"{cert['status']}: {len(cert['matrix_checks'])} triangular samples")


if __name__ == "__main__":
    main()
