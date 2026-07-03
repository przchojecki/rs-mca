#!/usr/bin/env python3
"""Verify the exact arithmetic in census_dodge_selection.md."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


TARGET_EXP = 128
OFFICIAL_RATES = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)]
OUTPUT = Path(
    "experimental/data/certificates/census-dodge-selection/"
    "census_dodge_selection.json"
)


@dataclass(frozen=True)
class Crossing:
    mode: str
    budget_bits: int
    rate: Fraction
    last_safe_scale: int
    first_unsafe_scale: int
    last_safe_count: int
    first_unsafe_count: int
    safe_margin: int
    unsafe_missing_tolerance: int


def a2_count(N: int, ell: int) -> int:
    if N <= 0 or N % 2:
        raise ValueError("N must be positive and even")
    if not 0 <= ell <= N:
        raise ValueError("ell must lie in [0,N]")
    half = N // 2
    total = 0
    u = 0
    while ell - 2 * u >= 0:
        t = ell - 2 * u
        if t <= half and u <= half - t:
            total += comb(half, t) * (2**t)
        u += 1
    return total


def ell_for_rate(N: int, rho: Fraction) -> int | None:
    value = rho * N + 1
    if value.denominator != 1:
        return None
    ell = value.numerator
    if not 0 <= ell <= N:
        return None
    return ell


def exact_count_for_rate(N: int, rho: Fraction) -> int | None:
    ell = ell_for_rate(N, rho)
    if ell is None:
        return None
    return a2_count(N, ell)


def first_relaxed_crossing(rho: Fraction, budget: int, limit: int = 1024) -> tuple[int, int]:
    last_safe: int | None = None
    for N in range(2, limit + 1, 2):
        count = exact_count_for_rate(N, rho)
        if count is None:
            continue
        if count <= budget:
            last_safe = N
            continue
        if last_safe is None:
            raise AssertionError("crossing before any safe scale")
        return last_safe, N
    raise AssertionError("no relaxed crossing found")


def first_dyadic_crossing(rho: Fraction, budget: int, max_exp: int = 12) -> tuple[int, int]:
    last_safe: int | None = None
    for exp in range(1, max_exp + 1):
        N = 2**exp
        count = exact_count_for_rate(N, rho)
        if count is None:
            continue
        if count <= budget:
            last_safe = N
            continue
        if last_safe is None:
            raise AssertionError("crossing before any safe dyadic scale")
        return last_safe, N
    raise AssertionError("no dyadic crossing found")


def classify_budget(budget: int, lower: int, exact_upper: int) -> str:
    if not 0 <= lower <= exact_upper:
        raise ValueError("need 0 <= lower <= exact_upper")
    if budget < lower:
        return "CERTIFIED_UNSAFE_BY_LOWER"
    if budget >= exact_upper:
        return "CERTIFIED_SAFE_BY_EXACT_UPPER"
    return "UNRESOLVED_WINDOW"


def crossing_row(mode: str, budget_bits: int, rho: Fraction) -> Crossing:
    budget = 2**budget_bits - 1
    if mode == "relaxed":
        last_safe, first_unsafe = first_relaxed_crossing(rho, budget)
    elif mode == "dyadic":
        last_safe, first_unsafe = first_dyadic_crossing(rho, budget)
    else:
        raise ValueError(mode)

    last_count = exact_count_for_rate(last_safe, rho)
    first_count = exact_count_for_rate(first_unsafe, rho)
    if last_count is None or first_count is None:
        raise AssertionError("integrality failure at crossing")
    if not (last_count <= budget < first_count):
        raise AssertionError((mode, budget_bits, rho, last_safe, first_unsafe))
    safe_margin = budget - last_count
    unsafe_tolerance = first_count - budget - 1
    if classify_budget(budget, first_count, first_count) != "CERTIFIED_UNSAFE_BY_LOWER":
        raise AssertionError("exact lower should certify unsafe at first unsafe scale")
    if classify_budget(budget, last_count, last_count) != "CERTIFIED_SAFE_BY_EXACT_UPPER":
        raise AssertionError("exact upper should certify safe at last safe scale")
    if unsafe_tolerance < 0:
        raise AssertionError("negative unsafe tolerance")
    return Crossing(
        mode=mode,
        budget_bits=budget_bits,
        rate=rho,
        last_safe_scale=last_safe,
        first_unsafe_scale=first_unsafe,
        last_safe_count=last_count,
        first_unsafe_count=first_count,
        safe_margin=safe_margin,
        unsafe_missing_tolerance=unsafe_tolerance,
    )


def build_certificate() -> dict[str, Any]:
    rows = [
        crossing_row(mode, bits, rho)
        for bits in (64, 96, 128)
        for rho in OFFICIAL_RATES
        for mode in ("relaxed", "dyadic")
    ]
    min_safe = min(row.safe_margin for row in rows)
    min_unsafe = min(row.unsafe_missing_tolerance for row in rows)
    if min_unsafe <= 0:
        raise AssertionError("expected positive unsafe tolerance in replay")
    expected = {
        (128, Fraction(1, 2), "relaxed"): (162, 164),
        (128, Fraction(1, 16), "dyadic"): (256, 512),
        (64, Fraction(1, 8), "relaxed"): (120, 128),
    }
    by_key = {
        (row.budget_bits, row.rate, row.mode): (row.last_safe_scale, row.first_unsafe_scale)
        for row in rows
    }
    for key, value in expected.items():
        if by_key[key] != value:
            raise AssertionError((key, by_key[key], value))
    return {
        "schema": "census-dodge-selection-v1",
        "status": "PROVED_COMPILER_ARITHMETIC",
        "dag_node": "census_dodge_selection",
        "theorem": {
            "budget": "B(q)=floor(q/2^128)",
            "window": "L <= B(q) < K is the only unresolved census window",
            "unsafe_dodge": "K>B and L=K-g certify unsafe whenever g <= K-B-1",
            "safe_dodge": "K<=B certifies safe by exact upper count",
        },
        "rows": [
            {
                "mode": row.mode,
                "budget_bits": row.budget_bits,
                "rate": f"{row.rate.numerator}/{row.rate.denominator}",
                "last_safe_scale": row.last_safe_scale,
                "first_unsafe_scale": row.first_unsafe_scale,
                "last_safe_count_bits": row.last_safe_count.bit_length(),
                "first_unsafe_count_bits": row.first_unsafe_count.bit_length(),
                "safe_margin_bits": row.safe_margin.bit_length(),
                "unsafe_missing_tolerance_bits": row.unsafe_missing_tolerance.bit_length(),
                "safe_margin": row.safe_margin,
                "unsafe_missing_tolerance": row.unsafe_missing_tolerance,
            }
            for row in rows
        ],
        "summary": {
            "row_count": len(rows),
            "minimum_safe_margin_bits": min_safe.bit_length(),
            "minimum_unsafe_missing_tolerance_bits": min_unsafe.bit_length(),
            "minimum_unsafe_missing_tolerance": min_unsafe,
        },
        "non_claims": [
            "does not prove quotient-collision lower bounds",
            "does not count primes in q congruence classes",
            "does not prove mixed-radix quotient counts",
            "does not resolve global quotient-periodic branch exhaustion",
        ],
    }


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("census dodge selection")
    print(f"  rows: {cert['summary']['row_count']}")
    print(
        "  min unsafe missing tolerance bits: "
        f"{cert['summary']['minimum_unsafe_missing_tolerance_bits']}"
    )
    for row in cert["rows"][:4]:
        print(
            f"  {row['mode']} bits={row['budget_bits']} rho={row['rate']}: "
            f"{row['last_safe_scale']}->{row['first_unsafe_scale']}, "
            f"tol_bits={row['unsafe_missing_tolerance_bits']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if args.check:
        assert_same(cert, json.loads(args.check.read_text()))
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
