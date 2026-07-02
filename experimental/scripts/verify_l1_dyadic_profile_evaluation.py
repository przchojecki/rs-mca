#!/usr/bin/env python3
"""Verify the exact dyadic quotient-profile evaluation.

This is the finite divisor-count node called ``dyadic_profile_evaluation`` in
the prize DAG.  It specializes the existing exact-divisibility quotient profile
to dyadic domains n=2^nu and official rates rho=1/R.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "l1-dyadic-profile-evaluation-v1"
CERTIFICATE_PATH = Path(
    "experimental/data/certificates/l1-dyadic-profile-evaluation/"
    "l1_dyadic_profile_evaluation.json"
)
RATES = (2, 4, 8, 16)
ETA_EXPONENTS = tuple(range(1, 13))
VALIDATION_NU = (12, 20, 40)
BUDGET_BITS = 128


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def log2_floor(value: int) -> int:
    require(value > 0, "log2_floor expects a positive integer")
    return value.bit_length() - 1


def log2_approx(value: int) -> float:
    """Return a stable double approximation to log2(value)."""
    if value <= 0:
        raise ValueError("log2_approx expects a positive integer")
    bits = value.bit_length()
    if bits <= 53:
        return math.log2(value)
    shift = bits - 53
    mantissa = value >> shift
    return math.log2(mantissa) + shift


def eta_record(exponent: int) -> dict[str, Any]:
    return {
        "fraction": f"1/{1 << exponent}",
        "exponent": exponent,
    }


def active_quotient_orders(rate_denominator: int, eta: Fraction) -> list[int]:
    """Dyadic quotient orders N=n/M active at exact rate k=n/R."""
    require(is_power_of_two(rate_denominator), "rate denominator must be dyadic")
    orders: list[int] = []
    order = rate_denominator
    while eta * order < 1:
        orders.append(order)
        order *= 2
    return orders


def quotient_count(quotient_order: int, rate_denominator: int) -> int:
    require(quotient_order % rate_denominator == 0, "rate must divide quotient")
    return math.comb(quotient_order - 1, quotient_order // rate_denominator)


def profile_entry(rate_denominator: int, eta_exponent: int) -> dict[str, Any]:
    eta = Fraction(1, 1 << eta_exponent)
    orders = active_quotient_orders(rate_denominator, eta)
    max_count = 0
    max_order = None
    for order in orders:
        count = quotient_count(order, rate_denominator)
        if count > max_count:
            max_count = count
            max_order = order
    return {
        "rate": f"1/{rate_denominator}",
        "rate_denominator": rate_denominator,
        "eta": eta_record(eta_exponent),
        "active_quotient_orders": orders,
        "active_count": len(orders),
        "max_attaining_quotient_order": max_order,
        "max_count_decimal": str(max_count) if max_count else "0",
        "max_count_bit_length": max_count.bit_length() if max_count else 0,
        "max_log2_floor": log2_floor(max_count) if max_count else None,
        "max_log2_approx": round(log2_approx(max_count), 12)
        if max_count
        else None,
        "max_exceeds_2_128": max_count > (1 << BUDGET_BITS),
        "all_binomial_counts_recomputed_by_verifier": True,
    }


def minimal_crossing_order(rate_denominator: int, budget_bits: int) -> int:
    threshold = 1 << budget_bits
    order = rate_denominator
    while True:
        if quotient_count(order, rate_denominator) > threshold:
            return order
        order *= 2


def exact_rate_direct_orders(
    nu: int, rate_denominator: int, eta_exponent: int
) -> list[int]:
    n = 1 << nu
    k = n // rate_denominator
    sigma = n >> eta_exponent
    orders: list[int] = []
    gcd_n_k = math.gcd(n, k)
    scale = 2
    while scale <= gcd_n_k:
        if gcd_n_k % scale == 0:
            quotient_order = n // scale
            quotient_dimension = k // scale
            if sigma < scale and quotient_dimension <= quotient_order - 1:
                orders.append(quotient_order)
        scale *= 2
    return sorted(orders)


def dither_direct_orders(
    nu: int, rate_denominator: int, eta_exponent: int
) -> list[int]:
    n = 1 << nu
    k0 = n // rate_denominator
    k = k0 - 1
    sigma = n >> eta_exponent
    orders: list[int] = []
    gcd_n_k = math.gcd(n, k)
    scale = 2
    while scale <= gcd_n_k:
        if gcd_n_k % scale == 0:
            quotient_order = n // scale
            quotient_dimension = k // scale
            if sigma < scale and quotient_dimension <= quotient_order - 1:
                orders.append(quotient_order)
        scale *= 2
    return sorted(orders)


def validation_records() -> list[dict[str, Any]]:
    records = []
    for nu in VALIDATION_NU:
        n = 1 << nu
        for rate_denominator in RATES:
            if nu <= int(math.log2(rate_denominator)):
                continue
            for eta_exponent in ETA_EXPONENTS:
                if eta_exponent > nu:
                    continue
                eta = Fraction(1, 1 << eta_exponent)
                direct = exact_rate_direct_orders(
                    nu, rate_denominator, eta_exponent
                )
                formula = active_quotient_orders(rate_denominator, eta)
                require(
                    direct == formula,
                    "direct exact-rate profile disagrees with dyadic formula",
                )
                dithered = dither_direct_orders(nu, rate_denominator, eta_exponent)
                require(
                    dithered == [],
                    "one-step dither should empty exact dyadic profile",
                )
            records.append(
                {
                    "n": n,
                    "nu": nu,
                    "rate": f"1/{rate_denominator}",
                    "eta_exponents_checked": list(
                        range(1, min(max(ETA_EXPONENTS), nu) + 1)
                    ),
                    "exact_rate_formula_matches_direct_divisor_scan": True,
                    "one_step_dither_profile_empty": True,
                }
            )
    return records


def build_certificate() -> dict[str, Any]:
    table = []
    for rate_denominator in RATES:
        for eta_exponent in ETA_EXPONENTS:
            table.append(profile_entry(rate_denominator, eta_exponent))

    crossing_rows = []
    for rate_denominator in RATES:
        order = minimal_crossing_order(rate_denominator, BUDGET_BITS)
        count = quotient_count(order, rate_denominator)
        previous = order // 2
        previous_count = quotient_count(previous, rate_denominator)
        require(previous_count <= (1 << BUDGET_BITS), "minimality failed")
        crossing_rows.append(
            {
                "rate": f"1/{rate_denominator}",
                "rate_denominator": rate_denominator,
                "minimal_dyadic_quotient_order_N_with_count_gt_2_128": order,
                "strict_unsafe_reserve_condition": f"eta < 1/{order}",
                "safe_from_exact_quotient_core_at_or_above": f"eta >= 1/{order}",
                "count_at_crossing_decimal": str(count),
                "count_at_crossing_log2_floor": log2_floor(count),
                "count_at_crossing_log2_approx": round(log2_approx(count), 12),
                "previous_order": previous,
                "previous_count_decimal": str(previous_count),
                "previous_count_log2_floor": log2_floor(previous_count),
                "previous_count_log2_approx": round(
                    log2_approx(previous_count), 12
                ),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / EXACT-ARITHMETIC",
        "object": "exact-divisibility quotient profile Q_H(a,k)",
        "domain_family": "dyadic H, n=2^nu",
        "rates": [f"1/{rate}" for rate in RATES],
        "eta_grid": [eta_record(exponent) for exponent in ETA_EXPONENTS],
        "budget_bits": BUDGET_BITS,
        "theorem": {
            "exact_rate_active_orders": (
                "For n=2^nu, k=n/R, sigma=eta*n, active exact quotient "
                "orders are N=2^v with R <= N and eta*N < 1."
            ),
            "profile_value": (
                "Q_H(a,k)=max_N log2 binom(N-1,N/R), with the empty max "
                "when no active N exists."
            ),
            "one_step_dither": (
                "For k=n/R-1, gcd(n,k)=1; hence the exact-divisibility "
                "profile is empty for every nontrivial dyadic scale."
            ),
        },
        "profile_table": table,
        "budget_crossings": crossing_rows,
        "direct_validation": validation_records(),
    }


def check_certificate(path: Path) -> None:
    expected = build_certificate()
    actual = json.loads(path.read_text())
    require(actual == expected, f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("Dyadic quotient-profile evaluation")
    print(f"schema: {certificate['schema_version']}")
    print("128-bit exact quotient-core crossings:")
    for row in certificate["budget_crossings"]:
        print(
            "  rate {rate}: N={N}, unsafe iff {cond}, log2 count={bits}".format(
                rate=row["rate"],
                N=row[
                    "minimal_dyadic_quotient_order_N_with_count_gt_2_128"
                ],
                cond=row["strict_unsafe_reserve_condition"],
                bits=row["count_at_crossing_log2_approx"],
            )
        )
    print("direct finite dyadic validations:", len(certificate["direct_validation"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the dyadic exact quotient-profile formula."
    )
    parser.add_argument("--emit", action="store_true", help="write certificate JSON")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    if args.emit:
        certificate = build_certificate()
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True))
        print(f"wrote {CERTIFICATE_PATH}")
        print_summary(certificate)
        return

    if args.check:
        check_certificate(args.check)
        print(f"checked {args.check}")
        print_summary(build_certificate())
        return

    print_summary(build_certificate())


if __name__ == "__main__":
    main()
