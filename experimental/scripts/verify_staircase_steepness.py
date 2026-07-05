#!/usr/bin/env python3
"""Replay the staircase steepness packet."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "staircase_steepness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "staircase-steepness"
    / "staircase_steepness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "staircase_steepness",
    "ratio_identity": "M(j + 1,t - 1) / M(j,t)",
    "lower_bound": "F(q,t) - q/(q+1)",
    "upper_bound": "1 - F(q,t)",
    "non_claim": "does not decide any particular deployed `v13` frontier row",
}


def aligned_stratum(n: int, j: int, t: int, q: int) -> Fraction:
    if not (0 <= j <= n and t >= 1 and q >= 2):
        raise ValueError("invalid aligned-stratum parameters")
    return Fraction(math.comb(n, j) * (q**t - 1), q ** (2 * t - 1))


def last_factor(q: int, t: int) -> Fraction:
    if not (q >= 2 and t > 1):
        raise ValueError("last-factor bound requires q >= 2 and t > 1")
    return Fraction(q**t - q, q**t - 1)


def ratio_formula(n: int, j: int, t: int, q: int) -> Fraction:
    return Fraction(n - j, j + 1) * q * last_factor(q, t)


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def ratio_checks() -> dict[str, object]:
    q_values = [2, 3, 5, 17, 257]
    n_values = [8, 16, 64]
    checked = 0
    min_factor: Fraction | None = None
    max_factor: Fraction | None = None

    for q in q_values:
        for n in n_values:
            for t in range(2, min(10, n) + 1):
                for j in range(0, min(12, n)):
                    actual = aligned_stratum(n, j + 1, t - 1, q) / aligned_stratum(
                        n, j, t, q
                    )
                    expected = ratio_formula(n, j, t, q)
                    if actual != expected:
                        raise AssertionError((q, n, j, t, actual, expected))

                    factor = last_factor(q, t)
                    if not (Fraction(q, q + 1) <= factor < 1):
                        raise AssertionError((q, t, factor))

                    normalized = actual / Fraction(n - j, j + 1)
                    if normalized != q * factor:
                        raise AssertionError((q, n, j, t, normalized, q * factor))
                    if not (Fraction(2 * q, 3) <= normalized < q):
                        raise AssertionError((q, n, j, t, normalized))

                    min_factor = factor if min_factor is None else min(min_factor, factor)
                    max_factor = factor if max_factor is None else max(max_factor, factor)
                    checked += 1

    return {
        "q_values": q_values,
        "n_values": n_values,
        "t_range": "2..10, truncated by n",
        "j_range": "0..11, truncated by n-1",
        "checked_adjacent_cells": checked,
        "min_last_factor_seen": fraction_text(min_factor or Fraction(0, 1)),
        "max_last_factor_seen": fraction_text(max_factor or Fraction(0, 1)),
        "uniform_lower_bound": "q/(q+1)",
        "uniform_upper_bound": "1",
        "normalized_jump_bounds": "[2q/3, q)",
        "all_checks_pass": checked > 0,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "staircase-steepness-v1",
        "status": "PROVED",
        "source_dag_node": "staircase_steepness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "ratio_checks": ratio_checks(),
        "non_claims": [
            "does not decide any deployed v13 frontier row",
            "does not supply the knife-edge census",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/staircase_steepness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert.get("schema") != "staircase-steepness-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "staircase_steepness":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    checks = cert.get("ratio_checks")
    if not isinstance(checks, dict) or not checks.get("all_checks_pass"):
        raise AssertionError("ratio checks failed")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
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
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
