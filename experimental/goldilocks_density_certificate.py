#!/usr/bin/env python3
"""Exact Goldilocks extension-density certificate for Paper A.

This checks the finite arithmetic in `tex/RS_disproof_v3.tex`
`ex:goldilocks-density`, using the box-density lower bound from
`prop:ext-density`.

For `p = 2^64 - 2^32 + 1` and `m = 2^32`, it verifies the tower prerequisites,
computes

    theta = rho*(1-rho)*m^2 / p

for the prize rates, confirms that full DSH coverage fails, and finds the
largest integer `d` with `theta^d > 2^-128`.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


STATUS = "PROVED"
THEOREM_ID = (
    "tex/RS_disproof_v3.tex:prop:ext-density, ex:goldilocks-density"
)
OBJECT = "Goldilocks extension-density arithmetic certificate"
SECURITY_BITS = 128
PRIZE_RATES = (
    Fraction(1, 2),
    Fraction(1, 4),
    Fraction(1, 8),
    Fraction(1, 16),
)


@dataclass(frozen=True)
class GoldilocksParams:
    p: int = 2**64 - 2**32 + 1
    m: int = 2**32


PARAMS = GoldilocksParams()


def v2(value: int) -> int:
    """Return the 2-adic valuation of a positive integer."""
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def decimal_lower(value: Fraction, digits: int = 18) -> str:
    scale = 10**digits
    scaled = (value.numerator * scale) // value.denominator
    whole, frac = divmod(scaled, scale)
    return f"{whole}.{frac:0{digits}d}"


def above_security_bound(value: Fraction, d_value: int) -> bool:
    return value.numerator**d_value * 2**SECURITY_BITS > value.denominator**d_value


def max_d_above_bound(value: Fraction) -> int:
    d_value = 0
    while above_security_bound(value, d_value + 1):
        d_value += 1
    return d_value


def row_for_rate(rho: Fraction) -> dict[str, object]:
    p = PARAMS.p
    m = PARAMS.m
    numerator = rho * (1 - rho) * m * m
    if numerator.denominator != 1:
        raise ValueError(f"rho*(1-rho)*m^2 is not integral for rho={rho}")
    theta_raw = Fraction(numerator.numerator, p)
    theta = min(Fraction(1, 1), theta_raw)
    max_d = max_d_above_bound(theta)
    r_value = rho * m
    if r_value.denominator != 1:
        raise ValueError(f"rho*m is not integral for rho={rho}")
    return {
        "rho": fraction_text(rho),
        "r": int(r_value),
        "theta": fraction_text(theta),
        "theta_decimal_floor": decimal_lower(theta),
        "theta_gt_rho_one_minus_rho": theta > rho * (1 - rho),
        "full_coverage_condition": numerator.numerator >= p,
        "max_integer_d_with_theta_d_gt_2^-128": max_d,
        "d_equals_max_still_above": above_security_bound(theta, max_d),
        "d_after_max_above": above_security_bound(theta, max_d + 1),
    }


def certificate_rows() -> list[dict[str, object]]:
    return [row_for_rate(rate) for rate in PRIZE_RATES]


def payload(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    result_rows = list(rows)
    p = PARAMS.p
    m = PARAMS.m
    prerequisites = {
        "p": p,
        "m": m,
        "p_formula": "2^64-2^32+1",
        "m_formula": "2^32",
        "p_mod_4": p % 4,
        "p_congruent_1_mod_4": p % 4 == 1,
        "m_divides_p_minus_1": (p - 1) % m == 0,
        "v2_p_minus_1": v2(p - 1),
        "v2_m": v2(m),
        "v2_match": v2(p - 1) == v2(m),
    }
    all_rows_ok = all(
        bool(row["d_equals_max_still_above"])
        and not bool(row["d_after_max_above"])
        and not bool(row["full_coverage_condition"])
        for row in result_rows
    )
    claimed_rows_ok = (
        result_rows[0]["max_integer_d_with_theta_d_gt_2^-128"] == 64
        and result_rows[3]["max_integer_d_with_theta_d_gt_2^-128"] == 31
        and bool(result_rows[0]["theta_gt_rho_one_minus_rho"])
        and bool(result_rows[3]["theta_gt_rho_one_minus_rho"])
    )
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "security_bits": SECURITY_BITS,
            "prize_rates": [fraction_text(rate) for rate in PRIZE_RATES],
            "params": prerequisites,
        },
        "result": {
            "all_rows_ok": all_rows_ok,
            "claimed_goldilocks_bounds_ok": claimed_rows_ok,
            "rows": result_rows,
        },
    }


def print_text(rows: list[dict[str, object]], cert: dict[str, object]) -> None:
    params = cert["inputs"]["params"]
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: Goldilocks tower prerequisites and theta^d bounds.")
    print()
    print(
        "p={p} ({p_formula}), m={m} ({m_formula}), "
        "v2(p-1)={v2_p_minus_1}, v2(m)={v2_m}".format(**params)
    )
    print(
        "Prerequisites: p == 1 mod 4: {p_congruent_1_mod_4}; "
        "m | p-1: {m_divides_p_minus_1}; v2 match: {v2_match}".format(
            **params
        )
    )
    print()
    print(
        "{:<6} {:>11} {:>28} {:>20} {:>9} {:>9} {:>9}".format(
            "rho",
            "r",
            "theta",
            "theta floor",
            "full",
            "max d",
            "next ok",
        )
    )
    for row in rows:
        print(
            "{rho:<6} {r:>11} {theta:>28} {theta_decimal_floor:>20} "
            "{full:>9} {maxd:>9} {next_ok:>9}".format(
                **row,
                full="yes" if row["full_coverage_condition"] else "no",
                maxd=row["max_integer_d_with_theta_d_gt_2^-128"],
                next_ok="yes" if row["d_after_max_above"] else "no",
            )
        )
    print()
    result = cert["result"]
    print(f"All rows internally checked: {result['all_rows_ok']}")
    print(
        "Paper's stated rate 1/2 and 1/16 bounds checked: "
        f"{result['claimed_goldilocks_bounds_ok']}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. JSON is machine-readable and text is for review.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = certificate_rows()
    cert = payload(rows)
    if args.format == "json":
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print_text(rows, cert)
    result = cert["result"]
    return 0 if result["all_rows_ok"] and result["claimed_goldilocks_bounds_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
