#!/usr/bin/env python3
"""Compute E14 integrality-margin tables for the adjacency endgames.

The table evaluates FM/entropy upper proxies at the candidate crossing scales
already used by the quotient-census and planted-list arithmetic packets.  It is
the computational half of the claim that an n^3 polynomial factor is absorbed
by integrality at those candidates.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "integrality-margin-tables-v1"
CERTIFICATE = Path(
    "experimental/data/certificates/integrality-margin-tables/"
    "integrality_margin_tables.json"
)
TARGET_BITS = (64, 96, 128)
Q_OFFSET_BITS = 128
K_MAX = 1 << 40
RATES = (2, 4, 8, 16)
POLY_EXPONENT = 3
MIN_MARGIN_BITS = 1000.0


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def binary_entropy(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def a2_count(order: int, ell: int) -> int:
    """Paper B 2-power antipodal count A_2(order, ell)."""
    require(order > 0 and order % 2 == 0, "order must be positive and even")
    require(0 <= ell <= order, "ell must lie in [0,order]")
    half = order // 2
    total = 0
    u = 0
    while ell - 2 * u >= 0:
        singles = ell - 2 * u
        if singles <= half and u <= half - singles:
            total += math.comb(half, singles) * (2**singles)
        u += 1
    return total


def ell_for_rate(order: int, rate_denominator: int) -> int | None:
    value = Fraction(order, rate_denominator) + 1
    if value.denominator != 1:
        return None
    ell = value.numerator
    if not (0 <= ell <= order):
        return None
    return ell


def first_relaxed_a2_crossing(rate_denominator: int, budget_bits: int) -> int:
    budget = (1 << budget_bits) - 1
    for order in range(2, 2049, 2):
        ell = ell_for_rate(order, rate_denominator)
        if ell is None:
            continue
        if a2_count(order, ell) > budget:
            return order
    raise AssertionError("no relaxed crossing found")


def first_dyadic_a2_crossing(rate_denominator: int, budget_bits: int) -> int:
    budget = (1 << budget_bits) - 1
    order = 2
    while order <= 4096:
        ell = ell_for_rate(order, rate_denominator)
        if ell is not None and a2_count(order, ell) > budget:
            return order
        order *= 2
    raise AssertionError("no dyadic crossing found")


def first_list_planted_crossing(rate_denominator: int, budget_bits: int) -> int:
    budget = (1 << budget_bits) - 1
    order = rate_denominator
    while order <= 4096:
        count = math.comb(order - 1, order // rate_denominator)
        if count > budget:
            return order
        order *= 2
    raise AssertionError("no planted crossing found")


def mca_fm_log2_upper(n: int, k: int, sigma: int, q_bits: int) -> float:
    """Upper bound log2 C(n,j)(1-q^-sigma)q^(1-sigma)."""
    j = n - k - sigma
    require(0 <= j <= n, "invalid MCA complement size")
    return n * binary_entropy(j / n) + q_bits * (1 - sigma)


def list_entropy_log2_upper(n: int, k: int, sigma: int, q_bits: int) -> float:
    """Upper bound for the list-side extras proxy C(n,k+sigma)q^-sigma."""
    a = k + sigma
    require(0 <= a <= n, "invalid list agreement size")
    return n * binary_entropy(a / n) - q_bits * sigma


def margin_record(
    *,
    side: str,
    candidate_family: str,
    rate_denominator: int,
    budget_bits: int,
    quotient_order: int,
) -> dict[str, Any]:
    q_bits = budget_bits + Q_OFFSET_BITS
    k = K_MAX
    n = rate_denominator * k
    sigma = (n + quotient_order - 1) // quotient_order
    if side == "MCA":
        log2_upper = mca_fm_log2_upper(n, k, sigma, q_bits)
    elif side == "LIST":
        log2_upper = list_entropy_log2_upper(n, k, sigma, q_bits)
    else:
        raise ValueError(f"unknown side: {side}")
    margin = -log2_upper - POLY_EXPONENT * math.log2(n)
    require(
        margin > MIN_MARGIN_BITS,
        f"{side} {candidate_family} margin too small: {margin}",
    )
    return {
        "side": side,
        "candidate_family": candidate_family,
        "rate": f"1/{rate_denominator}",
        "rate_denominator": rate_denominator,
        "budget_bits": budget_bits,
        "q_bits": q_bits,
        "k": str(k),
        "n": str(n),
        "quotient_order_N": quotient_order,
        "sigma": str(sigma),
        "sigma_over_n_upper": f"ceil(n/{quotient_order})/n",
        "log2_proxy_upper": round(log2_upper, 6),
        "poly_exponent": POLY_EXPONENT,
        "minus_log2_n_pow_B_times_proxy": round(margin, 6),
        "passes_n3_integrality_margin": True,
    }


def build_certificate() -> dict[str, Any]:
    rows = []
    candidate_scales = []
    for budget_bits in TARGET_BITS:
        for rate_denominator in RATES:
            relaxed = first_relaxed_a2_crossing(rate_denominator, budget_bits)
            dyadic = first_dyadic_a2_crossing(rate_denominator, budget_bits)
            planted = first_list_planted_crossing(rate_denominator, budget_bits)
            candidate_scales.append(
                {
                    "rate": f"1/{rate_denominator}",
                    "budget_bits": budget_bits,
                    "mca_relaxed_a2_crossing_N": relaxed,
                    "mca_dyadic_a2_crossing_N": dyadic,
                    "list_planted_crossing_N": planted,
                }
            )
            rows.append(
                margin_record(
                    side="MCA",
                    candidate_family="relaxed_A2_crossing",
                    rate_denominator=rate_denominator,
                    budget_bits=budget_bits,
                    quotient_order=relaxed,
                )
            )
            rows.append(
                margin_record(
                    side="MCA",
                    candidate_family="dyadic_A2_crossing",
                    rate_denominator=rate_denominator,
                    budget_bits=budget_bits,
                    quotient_order=dyadic,
                )
            )
            rows.append(
                margin_record(
                    side="LIST",
                    candidate_family="planted_dyadic_crossing",
                    rate_denominator=rate_denominator,
                    budget_bits=budget_bits,
                    quotient_order=planted,
                )
            )
    min_margin = min(row["minus_log2_n_pow_B_times_proxy"] for row in rows)
    return {
        "schema": SCHEMA,
        "status": "EXPERIMENTAL / ENTROPY-UPPER-MARGIN TABLE",
        "task": "E14 integrality margin tables / QA.3 + QL.4",
        "scope": {
            "official_rates": [f"1/{rate}" for rate in RATES],
            "budget_bits": list(TARGET_BITS),
            "q_bits": [bits + Q_OFFSET_BITS for bits in TARGET_BITS],
            "row_choice": "max official dimension k=2^40, n=R*k",
            "polynomial_factor_tested": f"n^{POLY_EXPONENT}",
            "mca_proxy": "C(n,j)(1-q^-sigma)q^(1-sigma) <= C(n,j)q^(1-sigma)",
            "list_proxy": "C(n,k+sigma)q^-sigma",
            "entropy_bound": "log2 binom(n,m) <= n H2(m/n)",
        },
        "candidate_scales": candidate_scales,
        "rows": rows,
        "minimum_margin_bits": min_margin,
        "all_rows_pass_n3_integrality_margin": all(
            row["passes_n3_integrality_margin"] for row in rows
        ),
        "non_claims": [
            "does not prove R2 rigidity",
            "does not prove the list ImgFib safe-side theorem",
            "does not count exact binomial coefficients at k=2^40",
            "does not settle rows away from the recorded candidate families",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = build_certificate()
    actual = json.loads(path.read_text())
    require(actual == expected, f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("Integrality margin tables")
    print(f"schema: {certificate['schema']}")
    print(f"rows: {len(certificate['rows'])}")
    print(f"minimum margin bits: {certificate['minimum_margin_bits']}")
    for row in certificate["rows"]:
        if row["minus_log2_n_pow_B_times_proxy"] == certificate["minimum_margin_bits"]:
            print(
                "worst row: {side} {family} rate {rate} budget_bits {bits} "
                "N={N}".format(
                    side=row["side"],
                    family=row["candidate_family"],
                    rate=row["rate"],
                    bits=row["budget_bits"],
                    N=row["quotient_order_N"],
                )
            )
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify E14 integrality margins.")
    parser.add_argument("--emit", action="store_true", help="write certificate JSON")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    if args.emit:
        certificate = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True))
        print(f"wrote {CERTIFICATE}")
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
