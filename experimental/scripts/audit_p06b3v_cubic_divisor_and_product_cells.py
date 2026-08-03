#!/usr/bin/env python3
"""Independent audit of the P06b3v exact incidence reductions."""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path


OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data/certificates/paper-d-cubic-product-line/"
    "p06b3v_cubic_divisor_and_product_cells.json"
)


def root_of_order(p: int, n: int) -> int:
    for candidate in range(2, p):
        zeta = pow(candidate, (p - 1) // n, p)
        if pow(zeta, n, p) == 1 and pow(zeta, n // 2, p) != 1:
            return zeta
    raise AssertionError((p, n))


def elementary(values: tuple[int, ...], p: int) -> tuple[int, int, int]:
    e1 = sum(values) % p
    e2 = sum(values[i] * values[j] for i in range(4) for j in range(i + 1, 4)) % p
    e3 = sum(
        values[i] * values[j] * values[k]
        for i in range(4)
        for j in range(i + 1, 4)
        for k in range(j + 1, 4)
    ) % p
    return e1, e2, e3


def smooth(key: tuple[int, int, int], p: int) -> bool:
    e1, e2, e3 = key
    m = e1 * pow(4, -1, p) % p
    sigma = (6 * m * m - e2) * pow(2, -1, p) % p
    rho = (e3 - 4 * m**3 + 4 * m * sigma) * pow(8, -1, p) % p
    return rho != 0 and (sigma**3 - 27 * rho**2) % p != 0


def canonical_trade(
    left: tuple[int, ...], right: tuple[int, ...], n: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    images = []
    for shift in range(n):
        a = tuple(sorted((x + shift) % n for x in left))
        b = tuple(sorted((x + shift) % n for x in right))
        images.append(tuple(sorted((a, b))))
    return min(images)


def locator(roots: tuple[int, ...], p: int) -> tuple[int, ...]:
    coefficients = [1]
    for root in roots:
        out = [0] * (len(coefficients) + 1)
        for index, value in enumerate(coefficients):
            out[index] = (out[index] + value) % p
            out[index + 1] = (out[index + 1] - root * value) % p
        coefficients = out
    return tuple(coefficients)


def audit_row(n: int, p: int) -> dict[str, int]:
    zeta = root_of_order(p, n)
    roots = [pow(zeta, exponent, p) for exponent in range(n)]
    buckets: dict[tuple[int, int, int], list[tuple[int, ...]]] = defaultdict(list)
    orbit_set: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()

    for support in itertools.combinations(range(n), 4):
        key = elementary(tuple(roots[x] for x in support), p)
        if not smooth(key, p):
            continue
        for other in buckets[key]:
            if set(support) & set(other):
                raise AssertionError("equal-top distinct quartets intersect")
            orbit_set.add(canonical_trade(other, support, n))
        buckets[key].append(support)

    cross_ratio = Counter()
    product_cells = Counter()
    cubic_records = 0
    decorated_product_line_records = 0
    product_line_left_degenerate = 0
    product_line_right_degenerate = 0
    for unordered_left, unordered_right in orbit_set:
        for left, right in (
            (unordered_left, unordered_right),
            (unordered_right, unordered_left),
        ):
            alpha = sum(left) % n
            beta = sum(right) % n
            for y in right:
                product_cells[((alpha - 4 * y) % n, (beta - 4 * y) % n)] += 1
            for x in left:
                for y in right:
                    normalized_left = tuple(sorted((a - y) % n for a in left))
                    normalized_right = tuple(sorted((b - y) % n for b in right))
                    r_exponent = (x - y) % n
                    r = roots[r_exponent]
                    left_remainder = tuple(
                        roots[a] for a in normalized_left if a != r_exponent
                    )
                    right_remainder = tuple(
                        roots[b] for b in normalized_right if b != 0
                    )
                    if len(left_remainder) != 3 or len(right_remainder) != 3:
                        raise AssertionError("distinguished root multiplicity drift")
                    cubic_left = locator(left_remainder, p)
                    cubic_right = locator(right_remainder, p)
                    p_at_one = sum(cubic_left) % p

                    # Coefficients are stored from highest to lowest degree.
                    x_minus_r_times_p = [0] * 5
                    for index, value in enumerate(cubic_left):
                        x_minus_r_times_p[index] = (
                            x_minus_r_times_p[index] + value
                        ) % p
                        x_minus_r_times_p[index + 1] = (
                            x_minus_r_times_p[index + 1] - r * value
                        ) % p
                    x_minus_r_times_p[-1] = (
                        x_minus_r_times_p[-1] - (1 - r) * p_at_one
                    ) % p

                    x_minus_one_times_q = [0] * 5
                    for index, value in enumerate(cubic_right):
                        x_minus_one_times_q[index] = (
                            x_minus_one_times_q[index] + value
                        ) % p
                        x_minus_one_times_q[index + 1] = (
                            x_minus_one_times_q[index + 1] - value
                        ) % p
                    if tuple(x_minus_r_times_p) != tuple(x_minus_one_times_q):
                        raise AssertionError("cubic divided-difference identity failed")

                    left_product = 1
                    for value in left_remainder:
                        left_product = left_product * value % p
                    right_product = 1
                    for value in right_remainder:
                        right_product = right_product * value % p
                    for av in left_remainder:
                        for tv in right_remainder:
                            left_factor = (
                                -av * r
                                + av * tv
                                + av
                                + r * tv
                                + r
                                - tv * tv
                                - tv
                                - 1
                            ) % p
                            right_factor = (
                                av * av
                                + av * r
                                - av * tv
                                - av
                                + r * r
                                - r * tv
                                - r
                                + tv
                            ) % p
                            constant = (
                                av
                                * tv
                                * (tv - av)
                                * (av - 1)
                                * (r - 1)
                                * (r - tv)
                            ) % p
                            line_value = (
                                -av * left_factor * right_product
                                + tv * right_factor * left_product
                                + constant
                            ) % p
                            if constant == 0:
                                raise AssertionError("valid product line has zero constant")
                            if left_factor == 0 and right_factor == 0:
                                raise AssertionError("both product-line factors vanish")
                            if line_value != 0:
                                raise AssertionError("decorated product-line identity failed")
                            decorated_product_line_records += 1
                            product_line_left_degenerate += left_factor == 0
                            product_line_right_degenerate += right_factor == 0

                    if set(normalized_left) & set(normalized_right):
                        raise AssertionError("normalized trade lost disjointness")
                    cross_ratio[r_exponent] += 1
                    cubic_records += 1

    trade_orbits = len(orbit_set)
    if cubic_records != 32 * trade_orbits:
        raise AssertionError("32T cubic-record identity failed")
    if sum(product_cells.values()) != 8 * trade_orbits:
        raise AssertionError("8T normalized-product identity failed")
    if decorated_product_line_records != 288 * trade_orbits:
        raise AssertionError("288T decorated product-line identity failed")

    return {
        "n": n,
        "p": p,
        "smooth_trade_orbits": trade_orbits,
        "cubic_records": cubic_records,
        "expected_cubic_records": 32 * trade_orbits,
        "normalized_product_cell_records": sum(product_cells.values()),
        "expected_normalized_product_cell_records": 8 * trade_orbits,
        "occupied_product_cells": len(product_cells),
        "maximum_product_cell_multiplicity": max(product_cells.values(), default=0),
        "maximum_cross_ratio_multiplicity": max(cross_ratio.values(), default=0),
        "decorated_product_line_records": decorated_product_line_records,
        "expected_decorated_product_line_records": 288 * trade_orbits,
        "product_line_left_degenerate": product_line_left_degenerate,
        "product_line_right_degenerate": product_line_right_degenerate,
    }


def main() -> None:
    rows = [audit_row(16, 17), audit_row(32, 97), audit_row(32, 193)]
    expected = [
        (0, 0, 0, 0, 0, 0, 0),
        (9, 288, 72, 2, 2592, 112, 112),
        (1, 32, 8, 2, 288, 8, 8),
    ]
    for row, target in zip(rows, expected, strict=True):
        observed = (
            row["smooth_trade_orbits"],
            row["cubic_records"],
            row["normalized_product_cell_records"],
            row["maximum_product_cell_multiplicity"],
            row["decorated_product_line_records"],
            row["product_line_left_degenerate"],
            row["product_line_right_degenerate"],
        )
        if observed != target:
            raise AssertionError((observed, target))

    payload = {
        "schema": "p06b3v-cubic-divisor-and-product-cell-audit/v1",
        "claim_id": "P06B3V_EXACT_CROSS_PAIR_CUBIC_DIVISOR_REDUCTION",
        "status": "PASS_INDEPENDENT_EXHAUSTIVE_SMALL_ROW_AUDIT",
        "rows": rows,
        "scope_guard": (
            "The 32T and 8T identities are exact. The finite rows do not prove "
            "the global T_sm<=n^2/2 inequality."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print("PASS independent P06b3v cubic-divisor/product-cell audit")
    for row in rows:
        print(
            f"n={row['n']} p={row['p']} T={row['smooth_trade_orbits']} "
            f"cubic={row['cubic_records']} cells={row['normalized_product_cell_records']} "
            f"max_cell={row['maximum_product_cell_multiplicity']} "
            f"decorated={row['decorated_product_line_records']} "
            f"degenerate=({row['product_line_left_degenerate']},"
            f"{row['product_line_right_degenerate']})"
        )


if __name__ == "__main__":
    main()
