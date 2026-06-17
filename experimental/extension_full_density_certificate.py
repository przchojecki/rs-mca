#!/usr/bin/env python3
"""Exact extension full-density certificate for Paper A.

This checks the integer arithmetic behind `tex/RS_disproof_v3.tex`
`thm:ext-smooth-towers` and `cor:fermat-proth-towers`.

For each listed base prime, set `m = 2^v2(p-1)`.  The script verifies:

* `p == 1 mod 4` and `m` is the full 2-part of `p-1`;
* `m^2 >= 18*p`, the simultaneous all-prize-rate condition;
* `rho*m` is integral for every prize rate;
* the two exact DSH quantities used in the extension proof are at least `p`.

The tower-order conclusion for every power-of-two extension degree `d` is then
the symbolic input `lem:ext-tower-criterion`; this script certifies the finite
arithmetic side of the corollary.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


STATUS = "PROVED"
THEOREM_ID = (
    "tex/RS_disproof_v3.tex:thm:ext-smooth-towers, cor:fermat-proth-towers"
)
OBJECT = "Fermat/Proth extension full-density arithmetic certificate"
PRIZE_RATES = (
    Fraction(1, 2),
    Fraction(1, 4),
    Fraction(1, 8),
    Fraction(1, 16),
)


@dataclass(frozen=True)
class BaseField:
    name: str
    p: int
    family: str
    formula: str


FIELDS = (
    BaseField("Fermat 257", 257, "Fermat", "2^8+1"),
    BaseField("Fermat 65537", 65537, "Fermat", "2^16+1"),
    BaseField("BabyBear", 15 * 2**27 + 1, "Proth/deployed", "15*2^27+1"),
    BaseField(
        "KoalaBear",
        2**31 - 2**24 + 1,
        "Proth/deployed",
        "2^31-2^24+1",
    ),
    BaseField("3*2^30+1", 3 * 2**30 + 1, "Proth/deployed", "3*2^30+1"),
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


def base_row(field: BaseField) -> dict[str, object]:
    two_adic = v2(field.p - 1)
    m_value = 2**two_adic
    full_two_part = (field.p - 1) % m_value == 0
    full_two_part = full_two_part and ((field.p - 1) // m_value) % 2 == 1
    return {
        "field": field.name,
        "family": field.family,
        "p": field.p,
        "p_formula": field.formula,
        "p_mod_4": field.p % 4,
        "v2_p_minus_1": two_adic,
        "m": m_value,
        "m_is_full_two_part": full_two_part,
        "m2_minus_18p": m_value * m_value - 18 * field.p,
        "m2_ge_18p": m_value * m_value >= 18 * field.p,
        "sixteen_divides_m": m_value % 16 == 0,
        "base_ok": field.p % 4 == 1
        and full_two_part
        and m_value * m_value >= 18 * field.p
        and m_value % 16 == 0,
    }


def rate_row(field: BaseField, rho: Fraction) -> dict[str, object]:
    two_adic = v2(field.p - 1)
    m_value = 2**two_adic
    r_value = rho * m_value
    if r_value.denominator != 1:
        raise ValueError(f"rho*m is not integral: field={field.name}, rho={rho}")
    r_int = r_value.numerator
    rho_term = rho * (1 - rho) * m_value * m_value
    if rho_term.denominator != 1:
        raise ValueError(
            f"rho*(1-rho)*m^2 is not integral: field={field.name}, rho={rho}"
        )
    dsh_r = r_int * (m_value - r_int) + 1
    dsh_r_plus = (r_int + 1) * (m_value - r_int - 1) + 1
    return {
        "field": field.name,
        "rho": fraction_text(rho),
        "m": m_value,
        "r": r_int,
        "rho_m_integral": True,
        "rho_one_minus_rho_m2_minus_p": rho_term.numerator - field.p,
        "dsh_r_bound": dsh_r,
        "dsh_r_margin": dsh_r - field.p,
        "dsh_r_plus_bound": dsh_r_plus,
        "dsh_r_plus_margin": dsh_r_plus - field.p,
        "rate_ok": dsh_r >= field.p and dsh_r_plus >= field.p,
    }


def certificate_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    bases = [base_row(field) for field in FIELDS]
    rates = [rate_row(field, rho) for field in FIELDS for rho in PRIZE_RATES]
    return bases, rates


def payload(
    bases: Iterable[dict[str, object]],
    rates: Iterable[dict[str, object]],
) -> dict[str, object]:
    base_rows = list(bases)
    rate_rows = list(rates)
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "base_fields": [
                {
                    "name": field.name,
                    "p": field.p,
                    "family": field.family,
                    "formula": field.formula,
                }
                for field in FIELDS
            ],
            "prize_rates": [fraction_text(rate) for rate in PRIZE_RATES],
            "symbolic_tower_input": "lem:ext-tower-criterion",
        },
        "result": {
            "all_bases_ok": all(bool(row["base_ok"]) for row in base_rows),
            "all_rates_ok": all(bool(row["rate_ok"]) for row in rate_rows),
            "base_rows": base_rows,
            "rate_rows": rate_rows,
        },
    }


def print_text(
    bases: list[dict[str, object]],
    rates: list[dict[str, object]],
    cert: dict[str, object],
) -> None:
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: base prerequisites and coordinate-wise DSH bounds.")
    print()
    print("{:<15} {:<15} {:>12} {:>5} {:>5} {:>12} {:>16} {:>3}".format(
        "field",
        "family",
        "p",
        "v2",
        "p%4",
        "m",
        "m^2-18p",
        "ok",
    ))
    for row in bases:
        print("{field:<15} {family:<15} {p:>12} {v2_p_minus_1:>5} "
              "{p_mod_4:>5} {m:>12} {m2_minus_18p:>16} {ok:>3}".format(
                  **row,
                  ok="yes" if row["base_ok"] else "no",
              ))
    print()
    print("{:<15} {:>5} {:>12} {:>12} {:>14} {:>14} {:>3}".format(
        "field",
        "rho",
        "r",
        "rho-term",
        "r margin",
        "r+1 margin",
        "ok",
    ))
    for row in rates:
        print("{field:<15} {rho:>5} {r:>12} "
              "{rho_one_minus_rho_m2_minus_p:>12} {dsh_r_margin:>14} "
              "{dsh_r_plus_margin:>14} {ok:>3}".format(
                  **row,
                  ok="yes" if row["rate_ok"] else "no",
              ))
    print()
    result = cert["result"]
    print(f"All base rows qualify: {result['all_bases_ok']}")
    print(f"All prize-rate DSH rows qualify: {result['all_rates_ok']}")


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
    bases, rates = certificate_rows()
    cert = payload(bases, rates)
    if args.format == "json":
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print_text(bases, rates, cert)
    result = cert["result"]
    return 0 if result["all_bases_ok"] and result["all_rates_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
