#!/usr/bin/env python3
"""Replay the XR minor-specialization certificate-semantics packet."""

from __future__ import annotations

import argparse
import json
from itertools import permutations
from pathlib import Path
from typing import Any


P = 101
NVAR = 2
REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "xr-minor-specialization-certificate-semantics"
    / "xr_minor_specialization_certificate_semantics.json"
)
NOTE = REPO / "experimental" / "notes" / "m1" / "xr_minor_specialization_certificate_semantics.md"

Monomial = tuple[int, ...]
Poly = dict[Monomial, int]

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "xr_minor_specialization_certificate_semantics",
    "evaluation_map": "ev_a : R -> K",
    "nonzero_minor": "zero polynomial on the chart",
    "non_claim": "profile-by-profile minor certificates",
}


def norm(poly: Poly) -> Poly:
    return {m: c % P for m, c in poly.items() if c % P}


def const(c: int) -> Poly:
    return norm({(0,) * NVAR: c})


def var(i: int) -> Poly:
    monomial = [0] * NVAR
    monomial[i] = 1
    return {tuple(monomial): 1}


def add(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for monomial, coeff in b.items():
        out[monomial] = out.get(monomial, 0) + coeff
    return norm(out)


def mul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            monomial = tuple(x + y for x, y in zip(ma, mb))
            out[monomial] = out.get(monomial, 0) + ca * cb
    return norm(out)


def eval_poly(poly: Poly, point: tuple[int, ...]) -> int:
    total = 0
    for monomial, coeff in poly.items():
        term = coeff
        for x, power in zip(point, monomial):
            term = term * pow(x, power, P)
        total += term
    return total % P


def parity(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inversions += perm[i] > perm[j]
    return -1 if inversions % 2 else 1


def det_poly(matrix: list[list[Poly]]) -> Poly:
    n = len(matrix)
    total: Poly = {}
    for perm in permutations(range(n)):
        term = const(parity(perm))
        for row, col in enumerate(perm):
            term = mul(term, matrix[row][col])
        total = add(total, term)
    return total


def det_mod(matrix: list[list[int]]) -> int:
    n = len(matrix)
    total = 0
    for perm in permutations(range(n)):
        term = parity(perm)
        for row, col in enumerate(perm):
            term *= matrix[row][col]
        total += term
    return total % P


def toy_check() -> dict[str, Any]:
    zero = const(0)
    one = const(1)
    x = var(0)
    y = var(1)
    minor = [
        [x, one, zero],
        [y, one, one],
        [one, zero, y],
    ]
    determinant = det_poly(minor)
    point = (3, 5)
    specialized = [[eval_poly(entry, point) for entry in row] for row in minor]
    value_from_polynomial = eval_poly(determinant, point)
    value_from_matrix = det_mod(specialized)
    return {
        "field": f"F_{P}",
        "point": list(point),
        "det_from_polynomial": value_from_polynomial,
        "det_from_matrix": value_from_matrix,
        "polynomial_nonzero": bool(determinant),
        "specialized_nonzero": value_from_polynomial != 0,
        "evaluation_agrees": value_from_polynomial == value_from_matrix,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    check = toy_check()
    cert = {
        "schema": "xr-minor-specialization-certificate-semantics-v1",
        "status": "PROVED_SPECIALIZATION_SEMANTICS_REPLAY",
        "source_dag_node": "xr_minor_specialization_certificate_semantics",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": check,
        "non_claims": [
            "does not produce profile-by-profile minor certificates",
            "does not count hypersurface points",
        ],
        "note": "experimental/notes/m1/xr_minor_specialization_certificate_semantics.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "xr-minor-specialization-certificate-semantics-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    if not (check["polynomial_nonzero"] and check["specialized_nonzero"] and check["evaluation_agrees"]):
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
        print(f"{cert['status']}: det={cert['toy_check']['det_from_matrix']}")


if __name__ == "__main__":
    main()
