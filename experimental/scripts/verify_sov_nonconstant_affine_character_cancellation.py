#!/usr/bin/env python3
"""Replay the SOV nonconstant affine character-cancellation packet."""

from __future__ import annotations

import argparse
import cmath
import json
import math
from pathlib import Path
from typing import Any, Iterator


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "sov" / "sov_nonconstant_affine_character_cancellation.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "sov-nonconstant-affine-character-cancellation"
    / "sov_nonconstant_affine_character_cancellation.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "sov_nonconstant_affine_character_cancellation",
    "affine_map": "c(v) = ell(v) + b",
    "zero_sum": "sum_{v in V} psi(xi c(v)) = 0",
    "exceptional_bound": "at most `|E|`",
    "non_claim": "budget-small exceptional sets",
}


def additive_character(p: int, x: int) -> complex:
    return cmath.exp(2j * math.pi * (x % p) / p)


def dot(coeffs: tuple[int, ...], x: tuple[int, ...], p: int) -> int:
    return sum(a * b for a, b in zip(coeffs, x)) % p


def points(p: int, dim: int) -> Iterator[tuple[int, ...]]:
    if dim == 0:
        yield ()
        return
    for tail in points(p, dim - 1):
        for x in range(p):
            yield tail + (x,)


def cancellation_check() -> dict[str, Any]:
    checks = 0
    max_abs = 0.0
    rows = []
    for p in (3, 5, 7):
        for dim in range(1, 4):
            local_checks = 0
            for coeffs in points(p, dim):
                if all(c == 0 for c in coeffs):
                    continue
                for offset in range(p):
                    for xi in range(1, p):
                        total = sum(
                            additive_character(p, xi * (dot(coeffs, x, p) + offset))
                            for x in points(p, dim)
                        )
                        max_abs = max(max_abs, abs(total))
                        if abs(total) >= 1e-8:
                            raise AssertionError((p, dim, coeffs, offset, xi, total))
                        checks += 1
                        local_checks += 1
            rows.append({"p": p, "dim": dim, "checks": local_checks})
    return {"rows": rows, "total_checks": checks, "max_abs_rounded": round(max_abs, 12)}


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "sov-nonconstant-affine-character-cancellation-v1",
        "status": "PROVED_AFFINE_CANCELLATION_REPLAY",
        "source_dag_node": "sov_nonconstant_affine_character_cancellation",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "cancellation_check": cancellation_check(),
        "non_claims": [
            "does not construct affine-piece partitions for actual anchored-core cells",
            "does not prove the SOV h-minus-1 character-sum bound",
        ],
        "note": "experimental/notes/sov/sov_nonconstant_affine_character_cancellation.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "sov-nonconstant-affine-character-cancellation-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["cancellation_check"]
    if check["total_checks"] <= 0 or check["max_abs_rounded"] >= 1e-8:
        raise AssertionError(f"failed cancellation check: {check}")


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
        print(f"{cert['status']}: {cert['cancellation_check']}")


if __name__ == "__main__":
    main()
