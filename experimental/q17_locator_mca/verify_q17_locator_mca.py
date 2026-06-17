#!/usr/bin/env python3
"""Exhaust q=17 locator fibers and canonical-line MCA slopes.

The script verifies the q=17, n=16 toy case requested in agents.md.  It uses
linear algebra over F_17 to test whether a word restricted to a support is the
evaluation of a degree-<d polynomial, avoiding enumeration of all RS codewords.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Iterable


P = 17
N = 16
GENERATOR = 3
RATES = ((1, 2), (1, 4))
SLACKS = (1, 2)


def inv(value: int, p: int = P) -> int:
    return pow(value % p, p - 2, p)


def field_domain() -> tuple[int, ...]:
    values = []
    x = 1
    for _ in range(P - 1):
        values.append(x)
        x = (x * GENERATOR) % P
    if len(set(values)) != P - 1 or x != 1:
        raise ValueError(f"{GENERATOR} is not primitive in F_{P}")
    return tuple(values)


DOMAIN = field_domain()


def nullspace_mod(matrix: list[list[int]], p: int = P) -> list[list[int]]:
    """Return a basis for the right nullspace of matrix over F_p."""
    if not matrix:
        return []

    rows = [[entry % p for entry in row] for row in matrix]
    row_count = len(rows)
    col_count = len(rows[0])
    pivot_cols: list[int] = []
    pivot_row = 0

    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue

        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = inv(rows[pivot_row][col], p)
        rows[pivot_row] = [(entry * scale) % p for entry in rows[pivot_row]]

        for row in range(row_count):
            if row == pivot_row or rows[row][col] % p == 0:
                continue
            factor = rows[row][col] % p
            rows[row] = [
                (rows[row][idx] - factor * rows[pivot_row][idx]) % p
                for idx in range(col_count)
            ]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free_cols = [col for col in range(col_count) if col not in pivot_cols]
    basis: list[list[int]] = []
    for free_col in free_cols:
        vector = [0] * col_count
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = (-rows[row][free_col]) % p
        basis.append(vector)
    return basis


@lru_cache(maxsize=None)
def support_constraints(indices: tuple[int, ...], dimension: int) -> tuple[tuple[int, ...], ...]:
    """Parity checks for degree-<dimension words on the selected support."""
    if len(indices) <= dimension:
        return ()
    xs = [DOMAIN[index] for index in indices]
    vandermonde_t = [[pow(x, degree, P) for x in xs] for degree in range(dimension)]
    return tuple(tuple(row) for row in nullspace_mod(vandermonde_t))


def fits_degree(values: tuple[int, ...], indices: tuple[int, ...], dimension: int) -> bool:
    checks = support_constraints(indices, dimension)
    for check in checks:
        total = sum(check[pos] * values[index] for pos, index in enumerate(indices))
        if total % P:
            return False
    return True


def word_for_exponent(exponent: int) -> tuple[int, ...]:
    return tuple(pow(x, exponent, P) for x in DOMAIN)


def line_word(anchor_exp: int, direction_exp: int, slope: int) -> tuple[int, ...]:
    return tuple(
        (pow(x, anchor_exp, P) + slope * pow(x, direction_exp, P)) % P
        for x in DOMAIN
    )


def quotient_values(a: int) -> tuple[int, ...]:
    return tuple(sorted({pow(x, a, P) for x in DOMAIN}))


def locator_counts(q_values: Iterable[int], ell: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for subset in combinations(q_values, ell):
        counts[(-sum(subset)) % P] += 1
    return counts


def close_slopes(
    anchor_exp: int,
    direction_exp: int,
    support_size: int,
    code_dimension: int,
) -> set[int]:
    supports = list(combinations(range(N), support_size))
    slopes: set[int] = set()
    for slope in range(P):
        word = line_word(anchor_exp, direction_exp, slope)
        if any(fits_degree(word, support, code_dimension) for support in supports):
            slopes.add(slope)
    return slopes


def mca_bad_slopes(
    anchor_exp: int,
    direction_exp: int,
    min_support_size: int,
    code_dimension: int,
) -> tuple[set[int], int, int]:
    anchor = word_for_exponent(anchor_exp)
    direction = word_for_exponent(direction_exp)
    slopes: set[int] = set()
    support_count = 0
    noncontained_support_count = 0

    supports_by_size = [
        support
        for size in range(min_support_size, N + 1)
        for support in combinations(range(N), size)
    ]

    for support in supports_by_size:
        support_count += 1
        anchor_fit = fits_degree(anchor, support, code_dimension)
        direction_fit = fits_degree(direction, support, code_dimension)
        noncontained = not (anchor_fit and direction_fit)
        if noncontained:
            noncontained_support_count += 1

        for slope in range(P):
            if slope in slopes and noncontained:
                continue
            word = line_word(anchor_exp, direction_exp, slope)
            if noncontained and fits_degree(word, support, code_dimension):
                slopes.add(slope)

    return slopes, support_count, noncontained_support_count


def histogram(values: Iterable[int]) -> dict[str, int]:
    return {str(key): value for key, value in sorted(Counter(values).items())}


def fraction_string(numerator: int, denominator: int) -> str:
    gcd = math.gcd(numerator, denominator)
    numerator //= gcd
    denominator //= gcd
    if denominator == 1:
        return str(numerator)
    return f"{numerator}/{denominator}"


def valid_scales(k: int) -> list[tuple[int, int]]:
    scales = []
    for quotient_order in range(1, N + 1):
        if N % quotient_order != 0:
            continue
        a = N // quotient_order
        if k % a == 0:
            scales.append((quotient_order, a))
    return scales


def build_case(rate_num: int, rate_den: int, quotient_order: int, a: int, slack: int) -> dict:
    k = N * rate_num // rate_den
    ell = k // a + slack
    support_size = k + slack * a
    anchor_exp = k + slack * a
    direction_exp = k + (slack - 1) * a
    list_dimension = k + slack - 1
    q_values = quotient_values(a)
    counts = locator_counts(q_values, ell)
    locator_slopes = set(counts)
    list_slopes = close_slopes(anchor_exp, direction_exp, support_size, list_dimension)
    mca_slopes, mca_supports, noncontained_supports = mca_bad_slopes(
        anchor_exp,
        direction_exp,
        support_size,
        k,
    )

    if not locator_slopes <= list_slopes:
        raise AssertionError("locator slopes must be close to the locator-list code")
    if slack == 1 and not locator_slopes <= mca_slopes:
        raise AssertionError("slack-one locator slopes must be MCA-bad")

    radius_num = N - k - slack * a
    radius_den = N
    locator_by_slope = [[slope, counts[slope]] for slope in sorted(counts)]

    return {
        "N": quotient_order,
        "a": a,
        "slack_t": slack,
        "ell": ell,
        "support_size": support_size,
        "radius": fraction_string(radius_num, radius_den),
        "anchor_exponent": anchor_exp,
        "direction_exponent": direction_exp,
        "locator_list_code_dimension": list_dimension,
        "locator_subset_count": math.comb(quotient_order, ell),
        "quotient_values": list(q_values),
        "locator_slope_count": len(locator_slopes),
        "locator_slope_count_histogram": histogram(counts.values()),
        "locator_counts_by_slope": locator_by_slope,
        "list_supports_examined": math.comb(N, support_size),
        "exhaustive_list_slope_count": len(list_slopes),
        "exhaustive_list_slopes": sorted(list_slopes),
        "locator_slopes_subset_exhaustive_list": locator_slopes <= list_slopes,
        "locator_slopes_equal_exhaustive_list": locator_slopes == list_slopes,
        "mca_code_dimension": k,
        "mca_supports_examined": mca_supports,
        "mca_noncontained_supports": noncontained_supports,
        "exhaustive_mca_slope_count": len(mca_slopes),
        "exhaustive_mca_slopes": sorted(mca_slopes),
        "locator_slopes_subset_exhaustive_mca": locator_slopes <= mca_slopes,
        "locator_slopes_equal_exhaustive_mca": locator_slopes == mca_slopes,
        "extra_list_slopes_beyond_locator": sorted(list_slopes - locator_slopes),
        "extra_mca_slopes_beyond_locator": sorted(mca_slopes - locator_slopes),
    }


def build_certificate() -> dict:
    rates = []
    for rate_num, rate_den in RATES:
        k = N * rate_num // rate_den
        cases = []
        for quotient_order, a in valid_scales(k):
            for slack in SLACKS:
                ell = k // a + slack
                support_size = k + slack * a
                if ell <= quotient_order and support_size <= N:
                    cases.append(build_case(rate_num, rate_den, quotient_order, a, slack))
        rates.append(
            {
                "rho": f"{rate_num}/{rate_den}",
                "k": k,
                "cases": cases,
            }
        )

    return {
        "status": "PROVED",
        "field": {
            "p": P,
            "domain_order": N,
            "primitive_generator": GENERATOR,
            "domain": list(DOMAIN),
        },
        "method": {
            "rs_code": "RS[F_17,D,k] uses degree < k polynomials.",
            "list_check": "Parity checks test degree-<d agreement on each support.",
            "mca_check": "All target-or-larger supports and all 17 slopes are exhausted.",
            "slack_one": "Slack-one locator slopes are direct support-wise MCA witnesses.",
            "slack_two": "Slack-two locator slopes are C+ list-fiber inputs.",
        },
        "rates": rates,
    }


def dump_certificate(certificate: dict) -> str:
    return json.dumps(certificate, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the generated certificate to this path")
    parser.add_argument("--check", type=Path, help="compare a certificate file with a fresh run")
    args = parser.parse_args()

    certificate = build_certificate()
    rendered = dump_certificate(certificate)

    if args.check:
        existing = args.check.read_text(encoding="utf-8")
        if existing != rendered:
            raise SystemExit(f"certificate mismatch: {args.check}")
        print(f"certificate matches: {args.check}")

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    elif not args.check:
        print(rendered, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
