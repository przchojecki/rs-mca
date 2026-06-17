#!/usr/bin/env python3
"""Exact DSH certificate for Paper A deployed-field claims.

This checks the finite arithmetic behind `tex/RS_disproof_v3.tex`
`thm:main(a)`: for each deployed prime, prize rate, and quoted divisor N,
verify

    (rho*N + 1) * ((1 - rho)*N - 1) + 1 >= p

and the divisibility prerequisites `N | p-1` and `rho*N in Z`.
It is a certificate for the Dias da Silva--Hamidoune inequality input, not an
enumeration of restricted sums.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


STATUS = "PROVED"
THEOREM_ID = "tex/RS_disproof_v3.tex:thm:main(a), lem:dsh, ex:babybear"
OBJECT = "Deployed-field DSH divisor certificate"

PRIZE_RATES = (
    Fraction(1, 2),
    Fraction(1, 4),
    Fraction(1, 8),
    Fraction(1, 16),
)


@dataclass(frozen=True)
class FieldSpec:
    name: str
    p: int
    formula: str


FIELDS = (
    FieldSpec("BabyBear", 15 * 2**27 + 1, "15*2^27+1"),
    FieldSpec("KoalaBear", 2**31 - 2**24 + 1, "2^31-2^24+1"),
    FieldSpec("3*2^30+1", 3 * 2**30 + 1, "3*2^30+1"),
)

DIVISOR_CASES = (
    (2**18, PRIZE_RATES),
    (2**17, (Fraction(1, 2), Fraction(1, 4))),
)


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


def dsh_bound(n_divisor: int, rho: Fraction) -> int:
    rho_n = rho * n_divisor
    if rho_n.denominator != 1:
        raise ValueError(f"rho*N is not integral: rho={rho}, N={n_divisor}")
    r = rho_n.numerator
    return (r + 1) * (n_divisor - r - 1) + 1


def certificate_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for field in FIELDS:
        two_adic = v2(field.p - 1)
        for n_divisor, rates in DIVISOR_CASES:
            divides = (field.p - 1) % n_divisor == 0
            for rho in rates:
                rho_n = rho * n_divisor
                rho_integral = rho_n.denominator == 1
                bound = dsh_bound(n_divisor, rho)
                margin = bound - field.p
                radius_floor = Fraction(1, 1) - rho - Fraction(1, n_divisor)
                rows.append(
                    {
                        "field": field.name,
                        "p": field.p,
                        "p_formula": field.formula,
                        "v2_p_minus_1": two_adic,
                        "N": n_divisor,
                        "rho": fraction_text(rho),
                        "rho_N": int(rho_n),
                        "ell": int(rho_n) + 1,
                        "radius_floor": fraction_text(radius_floor),
                        "dsh_bound": bound,
                        "dsh_margin": margin,
                        "N_divides_p_minus_1": divides,
                        "rho_N_integral": rho_integral,
                        "qualifies": divides and rho_integral and margin >= 0,
                    }
                )
    return rows


def payload(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    result_rows = list(rows)
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "fields": [
                {"name": field.name, "p": field.p, "formula": field.formula}
                for field in FIELDS
            ],
            "divisor_cases": [
                {
                    "N": n_divisor,
                    "rates": [fraction_text(rate) for rate in rates],
                }
                for n_divisor, rates in DIVISOR_CASES
            ],
        },
        "result": {
            "all_qualify": all(bool(row["qualifies"]) for row in result_rows),
            "rows": result_rows,
        },
    }


def print_text(rows: list[dict[str, object]]) -> None:
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: N | p-1, rho*N in Z, and the exact DSH bound.")
    print()
    headers = (
        "field",
        "N",
        "rho",
        "ell",
        "v2(p-1)",
        "dsh_bound",
        "p",
        "margin",
        "radius_floor",
        "ok",
    )
    print(
        "{:<22} {:>8} {:>5} {:>7} {:>8} {:>12} {:>12} {:>12} {:>18} {:>3}"
        .format(*headers)
    )
    for row in rows:
        print(
            "{field:<22} {N:>8} {rho:>5} {ell:>7} {v2_p_minus_1:>8} "
            "{dsh_bound:>12} {p:>12} {dsh_margin:>12} "
            "{radius_floor:>18} {ok:>3}".format(
                **row,
                ok="yes" if row["qualifies"] else "no",
            )
        )
    print()
    print(f"All rows qualify: {all(bool(row['qualifies']) for row in rows)}")


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
        print_text(rows)
    return 0 if cert["result"]["all_qualify"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
