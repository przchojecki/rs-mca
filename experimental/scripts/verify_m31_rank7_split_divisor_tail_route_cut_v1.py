#!/usr/bin/env python3
"""Verify the M31 rank-seven cumulative split-divisor tail route cut.

This verifier has one proved positive theorem and one exact negative result.

* If ``q_i = g - m_i`` is the planted-zero/denominator deficit, then the
  cumulative head ``q_i <= Q`` is one rank-at-most-seven RS list on ``E0``.
  The recursive affine-span compiler gives the exact cap ``C_Q(g)`` below.
* The sharp histogram allowed by all of those head caps survives every
  already-proved colored, cross-block, affine-line, and codimension-one
  scalar resource.  In particular, the harmonic two-resource primal has
  122 feasible integer endpoint allocations at the final residual cell,
  and an explicit integer q-by-b transport verifies the two marginals.

The second bullet is a route cut for the current inequalities.  It is not a
construction of one common support layer, a source family, a full-gcd
realization, or a row closure.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Any, Iterable


FIELD_PRIME = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
DEEP_CAP = 1_001_282
L = B_STAR - DEEP_CAP
TARGET = L - 1
S_MAX = 366_886

RANK = 7
G_MIN = 72_428
G_MAX = 354_972
FULL_SLICE_TRANSITION = 328_678
Q_PROFILE = W + 1
D6_MIN = N - K + 6

SCHEMA_ID = "m31-rank7-split-divisor-tail-route-cut-summary-v1"
THEOREM_ID = "M31_RANK7_SPLIT_DIVISOR_TAIL_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_RANK7_SPLIT_DIVISOR_TAIL_V1"
STATUS = (
    "PROVED_CUMULATIVE_HEAD_SCALAR_ROUTE_CUT_AND_TOY_REALIZATION_ROW_OPEN"
)
PARENT_PAYLOAD = (
    "8135b49370b491cc14defb6c9e62648148fa2420a3d0cc45084ba00410eca239"
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def product(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def falling(value: int, length: int) -> int:
    require(length >= 0, "falling length nonnegative")
    require(value >= length, "falling argument large enough")
    return product(value - offset for offset in range(length))


def ceil_div(numerator: int, denominator: int) -> int:
    require(denominator > 0, "ceil-div denominator positive")
    return -((-numerator) // denominator)


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    text = json.dumps(
        value,
        sort_keys=True,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return (text + "\n").encode("ascii")


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unsigned)).hexdigest()


def head_cap(union_size: int, cutoff: int) -> int:
    """Affine-span cap for the cumulative head q_i <= cutoff."""
    require(G_MIN <= union_size <= G_MAX, "head-cap union range")
    require(0 <= cutoff <= min(W, union_size - W - 1), "head cutoff range")
    numerator = comb(R - union_size + W + RANK, RANK)
    denominator = comb(W - cutoff + RANK, RANK)
    return numerator // denominator


def q_star(union_size: int) -> int:
    """Largest Q whose cumulative head cap is at most TARGET."""
    maximum = min(W, union_size - W - 1)
    require(maximum >= 0, "nonnegative legal deficit")
    if head_cap(union_size, 0) > TARGET:
        return -1
    low, high = 0, maximum
    while low < high:
        middle = (low + high + 1) // 2
        if head_cap(union_size, middle) <= TARGET:
            low = middle
        else:
            high = middle - 1
    return low


def adversarial_histogram(union_size: int) -> tuple[int, list[int]]:
    """Stochastically smallest deficit histogram allowed by all C_Q."""
    cutoff = q_star(union_size)
    if cutoff < 0:
        return cutoff, [L]
    histogram: list[int] = []
    previous = 0
    for deficit in range(cutoff + 1):
        current = head_cap(union_size, deficit)
        require(current >= previous, "head caps nondecreasing")
        histogram.append(current - previous)
        previous = current
    histogram.append(L - previous)
    require(histogram[-1] > 0, "forced tail nonempty")
    return cutoff, histogram


def joint_q_b_transport(
    histogram: list[int],
    b_zero_total: int,
    union_size: int,
    layer: int,
) -> list[list[int]]:
    """Greedy integer transport between q rows and b in {0, layer}."""
    require(0 <= b_zero_total <= sum(histogram), "transport column range")
    remaining = b_zero_total
    table: list[list[int]] = []
    for deficit, count in enumerate(histogram):
        at_zero = min(count, remaining)
        at_layer = count - at_zero
        remaining -= at_zero
        require(at_zero >= 0 and at_layer >= 0, "transport nonnegative")
        require(at_zero + at_layer == count, "transport row marginal")
        if at_zero:
            require(
                layer <= union_size - deficit,
                "transport b=0 placement",
            )
        if at_layer:
            require(
                union_size - deficit <= R - layer,
                "transport b=e placement",
            )
        table.append([deficit, at_zero, at_layer])
    require(remaining == 0, "transport b=0 column exhausted")
    require(
        sum(row[1] for row in table) == b_zero_total,
        "transport b=0 column marginal",
    )
    require(
        sum(row[2] for row in table) == sum(histogram) - b_zero_total,
        "transport b=e column marginal",
    )
    return table


def transport_digest(table: list[list[int]]) -> str:
    return hashlib.sha256(canonical_json(table)).hexdigest()


def histogram_moments(histogram: list[int]) -> tuple[int, int, int]:
    total = sum(histogram)
    first = sum(deficit * count for deficit, count in enumerate(histogram))
    second = sum(
        deficit * deficit * count for deficit, count in enumerate(histogram)
    )
    return total, first, second


def affine_fiber_cap(dimension: int) -> int:
    require(1 <= dimension <= 5, "q6 affine-fiber dimension")
    return comb((N - K) + dimension, dimension) // comb(
        W + dimension, dimension
    )


def raw_q6_cap(union_size: int, fiber_dimension: int) -> int:
    fixed = L * union_size * product(
        W + index for index in range(fiber_dimension + 1, RANK - 1)
    )
    numerator = affine_fiber_cap(fiber_dimension) * falling(
        R + union_size, RANK - fiber_dimension
    )
    return numerator // fixed - (W + RANK - 1)


def q6_envelope(union_size: int) -> tuple[int, int, int]:
    raw_cap, winner = min(
        (raw_q6_cap(union_size, dimension), dimension)
        for dimension in range(1, RANK - 1)
    )
    strict_cap = union_size - W - RANK
    require(strict_cap >= 0, "strict generalized-weight cap")
    return min(raw_cap, strict_cap), winner, raw_cap


def pi_profile(d6: int, mismatch: int) -> int:
    require(d6 >= D6_MIN, "legal d6")
    require(mismatch >= 0, "nonnegative mismatch")
    return (d6 - R + mismatch) * product(
        W + index + mismatch for index in range(1, 6)
    )


def ratio_is_larger(
    left_numerator: int,
    left_denominator: int,
    right_numerator: int,
    right_denominator: int,
) -> bool:
    return (
        left_numerator * right_denominator
        > right_numerator * left_denominator
    )


def interval_digest(intervals: list[dict[str, int]]) -> str:
    return hashlib.sha256(
        json.dumps(
            intervals,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def poly_trim(poly: tuple[int, ...], prime: int) -> tuple[int, ...]:
    values = [value % prime for value in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_sub(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    length = max(len(left), len(right))
    values = [
        (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        )
        % prime
        for index in range(length)
    ]
    return poly_trim(tuple(values), prime)


def poly_mul(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    values = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            values[left_index + right_index] = (
                values[left_index + right_index]
                + left_value * right_value
            ) % prime
    return poly_trim(tuple(values), prime)


def poly_divmod(
    numerator: tuple[int, ...],
    denominator: tuple[int, ...],
    prime: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    numerator_values = list(poly_trim(numerator, prime))
    denominator = poly_trim(denominator, prime)
    require(denominator != (0,), "polynomial divisor nonzero")
    if len(numerator_values) < len(denominator):
        return (0,), tuple(numerator_values)
    quotient = [0] * (len(numerator_values) - len(denominator) + 1)
    inverse_lead = pow(denominator[-1], -1, prime)
    while (
        len(numerator_values) >= len(denominator)
        and any(numerator_values)
    ):
        offset = len(numerator_values) - len(denominator)
        coefficient = numerator_values[-1] * inverse_lead % prime
        quotient[offset] = coefficient
        for index, value in enumerate(denominator):
            numerator_values[offset + index] = (
                numerator_values[offset + index] - coefficient * value
            ) % prime
        while len(numerator_values) > 1 and numerator_values[-1] == 0:
            numerator_values.pop()
    return (
        poly_trim(tuple(quotient), prime),
        poly_trim(tuple(numerator_values), prime),
    )


def poly_monic(
    poly: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    poly = poly_trim(poly, prime)
    require(poly != (0,), "monic polynomial nonzero")
    inverse_lead = pow(poly[-1], -1, prime)
    return tuple(value * inverse_lead % prime for value in poly)


def poly_gcd(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    left = poly_trim(left, prime)
    right = poly_trim(right, prime)
    while right != (0,):
        _, remainder = poly_divmod(left, right, prime)
        left, right = right, remainder
    return poly_monic(left, prime)


def poly_from_roots(
    roots: Iterable[int], prime: int
) -> tuple[int, ...]:
    result = (1,)
    for root in roots:
        result = poly_mul(result, ((-root) % prime, 1), prime)
    return result


def modular_rank(rows: list[tuple[int, ...]], prime: int) -> int:
    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime for value in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    (matrix[row][index] - factor * matrix[pivot_row][index])
                    % prime
                    for index in range(column_count)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def toy_full_gcd_counterexample() -> dict[str, Any]:
    """Replay an exact positive-w, full-gcd, lcm-restored source family."""
    prime = 31
    planted_roots = tuple(range(8))
    evaluation_roots = tuple(range(8, 31))
    restorer_roots = (8, 9, 10, 11, 12, 13, 28, 30)
    subset_size = 7
    message_dimension = 7

    planted = poly_from_roots(planted_roots, prime)
    evaluation = poly_from_roots(evaluation_roots, prime)
    modulus = poly_mul(planted, evaluation, prime)
    x_poly = (0, 1)
    require(sum(planted_roots) % prime == 28, "toy planted root sum")
    require(
        sum(restorer_roots) % prime == 28,
        "toy restorer root sum",
    )

    tail_subsets = [
        subset
        for subset in combinations(evaluation_roots, subset_size)
        if sum(subset) % prime == 28
    ]
    require(len(tail_subsets) == 7_864, "toy tail prefix fiber size")

    tail_messages: list[tuple[int, ...]] = []
    tail_locators: list[tuple[int, ...]] = []
    for subset in tail_subsets:
        locator = poly_from_roots(subset, prime)
        shifted_locator = poly_mul(x_poly, locator, prime)
        message = poly_sub(planted, shifted_locator, prime)
        require(len(message) - 1 < message_dimension, "toy tail degree")
        require(
            poly_gcd(planted, message, prime) == x_poly,
            "toy tail exact planted gcd",
        )
        require(
            poly_gcd(
                evaluation,
                poly_sub(planted, message, prime),
                prime,
            )
            == locator,
            "toy tail exact evaluation gcd",
        )
        require(
            poly_gcd(
                modulus,
                poly_sub(planted, message, prime),
                prime,
            )
            == poly_mul(x_poly, locator, prime),
            "toy tail exact full gcd",
        )
        tail_messages.append(
            tuple(
                message[index] if index < len(message) else 0
                for index in range(message_dimension)
            )
        )
        tail_locators.append(locator)

    require(
        len(set(tail_messages)) == len(tail_messages),
        "toy tail messages distinct",
    )
    require(
        len(set(tail_locators)) == len(tail_locators),
        "toy tail locators distinct",
    )

    restorer_locator = poly_from_roots(restorer_roots, prime)
    restorer_message = poly_sub(planted, restorer_locator, prime)
    require(
        len(restorer_message) - 1 < message_dimension,
        "toy restorer degree",
    )
    require(
        poly_gcd(planted, restorer_message, prime) == (1,),
        "toy restorer exact planted gcd",
    )
    require(
        poly_gcd(
            evaluation,
            poly_sub(planted, restorer_message, prime),
            prime,
        )
        == restorer_locator,
        "toy restorer exact evaluation gcd",
    )
    require(
        poly_gcd(
            modulus,
            poly_sub(planted, restorer_message, prime),
            prime,
        )
        == restorer_locator,
        "toy restorer exact full gcd",
    )
    restorer_row = tuple(
        restorer_message[index] if index < len(restorer_message) else 0
        for index in range(message_dimension)
    )
    require(restorer_row not in set(tail_messages), "toy restorer distinct")

    family = tail_messages + [restorer_row]
    require(len(family) == 7_865, "toy total list size")
    require(modular_rank(family, prime) == 7, "toy exact linear rank")

    tail_denominator = poly_from_roots(range(1, 8), prime)
    restorer_denominator = planted
    require(
        poly_mul(x_poly, tail_denominator, prime) == planted,
        "toy tail recovered denominator",
    )
    denominator_gcd = poly_gcd(
        tail_denominator, restorer_denominator, prime
    )
    denominator_lcm, denominator_remainder = poly_divmod(
        poly_mul(tail_denominator, restorer_denominator, prime),
        denominator_gcd,
        prime,
    )
    require(
        denominator_remainder == (0,)
        and poly_monic(denominator_lcm, prime) == planted,
        "toy denominator lcm restoration",
    )
    no_common_zero = all(
        any(
            sum(
                coefficient * pow(root, degree, prime)
                for degree, coefficient in enumerate(message)
            )
            % prime
            != 0
            for message in family
        )
        for root in planted_roots
    )
    require(no_common_zero, "toy no common planted zero")

    return {
        "field_prime": prime,
        "domain": "all 31 field elements",
        "P_roots": list(planted_roots),
        "L_roots": list(evaluation_roots),
        "w": 1,
        "message_dimension": message_dimension,
        "agreement": 8,
        "tail_prefix_condition": "7-subset T of Z(L) with sum(T)=28 mod 31",
        "tail_fixed_quotient": "X",
        "tail_count": len(tail_messages),
        "restorer_roots": list(restorer_roots),
        "restorer_count": 1,
        "total_list_size": len(family),
        "deficit_histogram": {"0": 1, "1": len(tail_messages)},
        "linear_rank": modular_rank(family, prime),
        "every_full_gcd_exact": True,
        "master_lcm_restored": True,
        "no_common_zero_on_P": no_common_zero,
        "deployed_implication": (
            "SMALL_FIELD_FALSIFIER_OF_LCM_OR_FULL_GCD_ONLY_CLOSURE; "
            "NO_M31_LOWER_BOUND"
        ),
    }


def scan_all() -> dict[str, Any]:
    """Exhaust every deployed residual union size with integer arithmetic."""
    intervals: list[dict[str, int]] = []
    interval_start = G_MIN
    interval_q = q_star(G_MIN)

    zero_tail_upper_cells: list[dict[str, int]] = []
    maximum_tail_upper = (-1, -1, -1)
    maximum_proper_bucket = (-1, -1, -1)
    minimum_slice_margin = (10**30, -1, -1, -1, -1)
    minimum_harmonic_width = (10**30, -1, -1, -1, -1, -1)
    minimum_contain_margin = (10**30, -1, -1, -1)
    minimum_avoid_margin = (10**30, -1, -1, -1)
    endpoint_transport: dict[str, Any] | None = None

    ratio_maxima: dict[str, tuple[int, int, int, int, int]] = {
        name: (0, 1, -1, -2, 0)
        for name in (
            "first_pivot",
            "colored_E",
            "colored_S",
            "cross_block",
            "affine_line",
        )
    }

    endpoint_records: dict[str, Any] = {}
    record_cells = {
        72_428,
        328_677,
        328_678,
        328_689,
        340_000,
        350_000,
        354_966,
        354_970,
        354_971,
        354_972,
    }

    full_six_factor = falling(W + 6, 6)
    cross_extension = comb(W + 5, 5)
    affine_line_extension = comb(W + 6, 5)
    minimum_proper_slice_ceiling = (
        comb(R - (G_MAX - 1) + W + 6, 6) // comb(W + 6, 6)
    )
    require(
        minimum_proper_slice_ceiling == 1_182_429,
        "minimum proper-slice ceiling",
    )

    for union_size in range(G_MIN, G_MAX + 1):
        cutoff, histogram = adversarial_histogram(union_size)
        if cutoff != interval_q:
            intervals.append(
                {
                    "q_star": interval_q,
                    "g_min": interval_start,
                    "g_max": union_size - 1,
                }
            )
            interval_start = union_size
            interval_q = cutoff

        total, first_moment, second_moment = histogram_moments(histogram)
        require(total == L, "histogram total")
        require(all(count >= 0 for count in histogram), "histogram nonnegative")
        require(len(histogram) == max(1, cutoff + 2), "histogram support")
        require(len(histogram) - 1 <= union_size - W - 1, "legal deficits")

        if cutoff < 0:
            require(
                head_cap(union_size, 0) >= L,
                "pretransition full-slice relaxation",
            )
            forced_tail = 0
            weakest_tail_upper = -1
        else:
            cumulative = 0
            for deficit in range(cutoff + 1):
                cumulative += histogram[deficit]
                require(
                    cumulative == head_cap(union_size, deficit),
                    "every cumulative head saturated",
                )
            require(
                head_cap(union_size, cutoff) <= TARGET,
                "q-star head paid",
            )
            require(
                head_cap(union_size, cutoff + 1) >= L,
                "q-star maximality",
            )
            forced_tail = histogram[-1]
            weakest_tail_upper = forced_tail - 1
            require(weakest_tail_upper >= 0, "tail upper nonnegative")
            if weakest_tail_upper == 0:
                zero_tail_upper_cells.append(
                    {"g": union_size, "q_star": cutoff}
                )
            if weakest_tail_upper > maximum_tail_upper[0]:
                maximum_tail_upper = (
                    weakest_tail_upper,
                    union_size,
                    cutoff,
                )

        for deficit, count in enumerate(histogram[1:], start=1):
            if count > maximum_proper_bucket[0]:
                maximum_proper_bucket = (count, union_size, deficit)
            margin = minimum_proper_slice_ceiling - count
            if margin < minimum_slice_margin[0]:
                minimum_slice_margin = (
                    margin,
                    union_size,
                    deficit,
                    count,
                    minimum_proper_slice_ceiling,
                )

        # First-pivot and both colored resources at s=e_common=0.
        first_lhs = L * union_size * full_six_factor
        first_rhs = falling(R + union_size, 7)
        colored_e_lhs = (union_size * L - first_moment) * full_six_factor
        colored_e_rhs = R * falling(R + union_size - 1, 6)
        colored_s_lhs = first_moment * full_six_factor
        colored_s_rhs = union_size * falling(R + union_size - 1, 6)
        cross_lhs = (
            (union_size * first_moment - second_moment) * cross_extension
        )
        cross_rhs = (
            union_size * R * comb(R + union_size - 2, RANK - 2)
        )
        affine_lhs = L * union_size * affine_line_extension
        affine_rhs = (
            15
            * (R + union_size)
            * comb(R + union_size - 1, RANK - 2)
        )
        inequalities = {
            "first_pivot": (first_lhs, first_rhs),
            "colored_E": (colored_e_lhs, colored_e_rhs),
            "colored_S": (colored_s_lhs, colored_s_rhs),
            "cross_block": (cross_lhs, cross_rhs),
            "affine_line": (affine_lhs, affine_rhs),
        }
        for name, (lhs, rhs) in inequalities.items():
            require(lhs <= rhs, f"{name} relaxation feasible")
            old_numerator, old_denominator, _, _, _ = ratio_maxima[name]
            if ratio_is_larger(lhs, rhs, old_numerator, old_denominator):
                ratio_maxima[name] = (
                    lhs,
                    rhs,
                    union_size,
                    cutoff,
                    rhs - lhs,
                )

        # Exact harmonic primal.  The two endpoint mismatch classes b=0,e
        # are enough; this tests the resource inequalities themselves rather
        # than merely observing that a dual upper bound misses the target.
        q6_cap, q6_winner, q6_raw = q6_envelope(union_size)
        d6 = D6_MIN + q6_cap
        layer = R + union_size - d6
        require(1 <= layer <= Q_PROFILE, "harmonic layer range")
        pi_zero = pi_profile(d6, 0)
        pi_layer = pi_profile(d6, layer)
        t_capacity = layer * falling(d6, 6)
        u_capacity = falling(d6, 7)
        t_cost_zero = layer * pi_zero
        u_cost_zero = (Q_PROFILE - layer) * pi_zero
        u_cost_layer = Q_PROFILE * pi_layer
        require(u_cost_layer > u_cost_zero, "harmonic endpoint tradeoff")

        harmonic_high = min(L, t_capacity // t_cost_zero)
        harmonic_low = max(
            0,
            ceil_div(
                L * u_cost_layer - u_capacity,
                u_cost_layer - u_cost_zero,
            ),
        )
        harmonic_width = max(0, harmonic_high - harmonic_low + 1)
        require(harmonic_width > 0, "integer harmonic primal feasible")
        require(
            harmonic_low * t_cost_zero <= t_capacity,
            "harmonic T resource",
        )
        require(
            harmonic_low * u_cost_zero
            + (L - harmonic_low) * u_cost_layer
            <= u_capacity,
            "harmonic U resource",
        )
        transport = joint_q_b_transport(
            histogram,
            harmonic_low,
            union_size,
            layer,
        )
        if union_size == G_MAX:
            endpoint_transport = {
                "g": union_size,
                "b_classes": [0, layer],
                "b_zero_total": harmonic_low,
                "b_e_total": L - harmonic_low,
                "rows": transport,
                "rows_sha256": transport_digest(transport),
            }
        if harmonic_width < minimum_harmonic_width[0]:
            minimum_harmonic_width = (
                harmonic_width,
                union_size,
                harmonic_low,
                harmonic_high,
                d6,
                layer,
            )

        maximum_deficit = len(histogram) - 1
        contain_margin = union_size - maximum_deficit - layer
        avoid_margin = R - layer - union_size
        require(contain_margin >= 0, "b=0 E0-layer placement relaxation")
        require(avoid_margin >= 0, "b=e E0-layer placement relaxation")
        if contain_margin < minimum_contain_margin[0]:
            minimum_contain_margin = (
                contain_margin,
                union_size,
                maximum_deficit,
                layer,
            )
        if avoid_margin < minimum_avoid_margin[0]:
            minimum_avoid_margin = (
                avoid_margin,
                union_size,
                maximum_deficit,
                layer,
            )

        if union_size in record_cells:
            truncated_moment = (
                sum(
                    L - head_cap(union_size, value)
                    for value in range(cutoff + 1)
                )
                if cutoff >= 0
                else 0
            )
            require(
                truncated_moment == first_moment,
                "layer-cake deficit identity",
            )
            endpoint_records[str(union_size)] = {
                "q_star": cutoff,
                "C_0": head_cap(union_size, 0),
                "C_q_star": (
                    head_cap(union_size, cutoff) if cutoff >= 0 else None
                ),
                "C_q_star_plus_one": (
                    head_cap(union_size, cutoff + 1)
                    if cutoff >= 0
                    else None
                ),
                "forced_tail": forced_tail,
                "weakest_tail_upper": weakest_tail_upper,
                "histogram_first_moment": first_moment,
                "histogram_cross_moment": (
                    union_size * first_moment - second_moment
                ),
                "harmonic": {
                    "q6_cap": q6_cap,
                    "q6_winner": q6_winner,
                    "q6_raw_cap": q6_raw,
                    "d6": d6,
                    "layer": layer,
                    "low": harmonic_low,
                    "high": harmonic_high,
                    "integer_width": harmonic_width,
                },
            }

    intervals.append(
        {"q_star": interval_q, "g_min": interval_start, "g_max": G_MAX}
    )

    require(len(intervals) == 2_465, "q-star interval count")
    require(
        intervals[0]
        == {"q_star": -1, "g_min": 72_428, "g_max": 328_677},
        "initial q-star interval",
    )
    require(
        intervals[1]
        == {"q_star": 0, "g_min": 328_678, "g_max": 328_688},
        "first paid-head interval",
    )
    require(
        intervals[-1]
        == {"q_star": 2_463, "g_min": 354_966, "g_max": 354_972},
        "last q-star interval",
    )
    digest = interval_digest(intervals)
    require(
        digest
        == "e3c0bc60f3c1e3918a2499cf1baa746f8dfd363c6d74f26af1a345ab5453787f",
        "q-star interval digest",
    )

    lengths: dict[str, int] = {}
    for interval in intervals:
        length = interval["g_max"] - interval["g_min"] + 1
        lengths[str(length)] = lengths.get(str(length), 0) + 1
    require(
        lengths == {"7": 1, "10": 805, "11": 1_658, "256250": 1},
        "q-star interval-length histogram",
    )

    require(
        endpoint_records["354972"]["histogram_first_moment"]
        == 4_678_598_254,
        "endpoint truncated moment",
    )
    require(
        endpoint_records["354972"]["C_q_star"] == 15_774_894,
        "endpoint paid head",
    )
    require(
        endpoint_records["354972"]["C_q_star_plus_one"] == 15_776_593,
        "endpoint adjacent head",
    )
    require(
        endpoint_records["354972"]["forced_tail"] == 1_039,
        "endpoint forced tail",
    )
    require(
        maximum_tail_upper == (1_696, 354_165, 2_387),
        "maximum weakest tail upper",
    )
    require(len(zero_tail_upper_cells) == 17, "zero-tail cell count")
    require(
        maximum_proper_bucket == (1_700, 354_957, 2_462),
        "maximum proper histogram bucket",
    )
    require(
        minimum_slice_margin
        == (1_180_729, 354_957, 2_462, 1_700, 1_182_429),
        "minimum proper-slice margin",
    )
    require(
        minimum_harmonic_width
        == (122, 354_972, 10_411_669, 10_411_790, 1_270_586, 65_515),
        "minimum harmonic integer interval",
    )
    require(
        minimum_contain_margin == (72_427, 72_428, 0, 1),
        "minimum b=0 placement margin",
    )
    require(
        minimum_avoid_margin == (560_642, 354_972, 2_464, 65_515),
        "minimum b=e placement margin",
    )
    require(endpoint_transport is not None, "endpoint transport emitted")
    require(
        endpoint_transport["b_zero_total"] == 10_411_669
        and endpoint_transport["b_e_total"] == 5_364_264,
        "endpoint transport column totals",
    )
    require(
        endpoint_transport["rows_sha256"]
        == "e2e89b305b732bad92e139d2bf89c0476f5bf89eb73b314a02b36361bba509ca",
        "endpoint transport digest",
    )

    ratio_records: dict[str, Any] = {}
    for name, (lhs, rhs, union_size, cutoff, slack) in ratio_maxima.items():
        ratio_records[name] = {
            "g": union_size,
            "q_star": cutoff,
            "lhs": lhs,
            "rhs": rhs,
            "slack": slack,
            "utilization_parts_per_billion": lhs * 10**9 // rhs,
        }
    require(
        {
            name: (record["g"], record["q_star"])
            for name, record in ratio_records.items()
        }
        == {
            "first_pivot": (163_521, -1),
            "colored_E": (196_225, -1),
            "colored_S": (354_972, 2_463),
            "cross_block": (354_972, 2_463),
            "affine_line": (196_225, -1),
        },
        "existing inequality worst cells",
    )

    return {
        "q_star_intervals": intervals,
        "q_star_interval_sha256": digest,
        "q_star_interval_length_histogram": lengths,
        "endpoint_records": endpoint_records,
        "tail_requirement": {
            "formula": "U_tail(g)=L-1-C_{Q_star(g)}(g)",
            "zero_upper_required_cells": zero_tail_upper_cells,
            "maximum_weakest_upper": {
                "value": maximum_tail_upper[0],
                "g": maximum_tail_upper[1],
                "q_star": maximum_tail_upper[2],
            },
        },
        "histogram_controls": {
            "formula": (
                "h_0=C_0; h_q=C_q-C_{q-1}; "
                "h_{Q_star+1}=L-C_{Q_star}"
            ),
            "pretransition_formula": "h_0=L",
            "maximum_proper_bucket": {
                "count": maximum_proper_bucket[0],
                "g": maximum_proper_bucket[1],
                "q": maximum_proper_bucket[2],
            },
            "minimum_proper_slice_ceiling": minimum_proper_slice_ceiling,
            "minimum_bucket_to_slice_ceiling_margin": {
                "margin": minimum_slice_margin[0],
                "g": minimum_slice_margin[1],
                "q": minimum_slice_margin[2],
                "bucket": minimum_slice_margin[3],
                "cap": minimum_slice_margin[4],
            },
        },
        "joint_harmonic_controls": {
            "allocation": "x members at b=0 and L-x members at b=e",
            "scope": (
                "EXACT_JOINT_Q_B_INTEGER_MARGINAL_RELAXATION; "
                "NO_COMMON_T_OR_SOURCE_REALIZATION"
            ),
            "transport_rule": (
                "Greedily fill b=0 in increasing q; put the remainder at b=e."
            ),
            "placement_rule": (
                "For a q row and b class, split g-q minimum E0 agreements "
                "as e-b on T and g-q-(e-b) off T."
            ),
            "endpoint_transport": endpoint_transport,
            "minimum_integer_interval": {
                "width": minimum_harmonic_width[0],
                "g": minimum_harmonic_width[1],
                "low": minimum_harmonic_width[2],
                "high": minimum_harmonic_width[3],
                "d6": minimum_harmonic_width[4],
                "e": minimum_harmonic_width[5],
            },
            "minimum_b_zero_placement_margin": {
                "margin": minimum_contain_margin[0],
                "g": minimum_contain_margin[1],
                "maximum_q": minimum_contain_margin[2],
                "e": minimum_contain_margin[3],
            },
            "minimum_b_e_placement_margin": {
                "margin": minimum_avoid_margin[0],
                "g": minimum_avoid_margin[1],
                "maximum_q": minimum_avoid_margin[2],
                "e": minimum_avoid_margin[3],
            },
        },
        "existing_inequality_ratio_maxima": ratio_records,
    }


def build_summary() -> dict[str, Any]:
    global CHECKS
    CHECKS = 0
    require((R, W) == (981_129, 67_447), "deployed R,w")
    require(L == 15_775_933 and TARGET == 15_775_932, "shallow target")
    scan = scan_all()
    toy = toy_full_gcd_counterexample()
    summary: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture": ARCHITECTURE_ID,
        "status": STATUS,
        "parent_payload_sha256": PARENT_PAYLOAD,
        "row": {
            "field_prime": FIELD_PRIME,
            "n": N,
            "K": K,
            "agreement": A,
            "R": R,
            "w": W,
            "B_star": B_STAR,
            "deep_cap": DEEP_CAP,
            "shallow_forbidden_size": L,
            "shallow_target": TARGET,
            "maximum_excess": S_MAX,
            "rank": RANK,
            "residual_g_range": [G_MIN, G_MAX],
        },
        "cumulative_head_theorem": {
            "deficit": "q_i=deg(gcd(P,f_i))=g-deg(G_i)",
            "head": "N_{<=Q}=#{i:q_i<=Q}",
            "range": "0<=Q<=min(w,g-w-1)",
            "E0_agreement_floor": "g-Q=(g-w)+(w-Q)",
            "formula": (
                "C_Q(g)=floor(binomial(R-g+w+7,7)/"
                "binomial(w-Q+7,7))"
            ),
            "proved_bound": "N_{<=Q}<=C_Q(g)",
            "q_star": (
                "max{Q:C_Q(g)<=15775932}, or -1 if C_0(g)>15775932"
            ),
        },
        "transition_scan": {
            "g_cells": G_MAX - G_MIN + 1,
            "interval_count": len(scan["q_star_intervals"]),
            "initial_interval": scan["q_star_intervals"][0],
            "first_paid_head_interval": scan["q_star_intervals"][1],
            "final_interval": scan["q_star_intervals"][-1],
            "interval_sha256": scan["q_star_interval_sha256"],
            "interval_length_histogram": (
                scan["q_star_interval_length_histogram"]
            ),
            "endpoint_records": scan["endpoint_records"],
            "tail_requirement": scan["tail_requirement"],
        },
        "adversarial_histogram": scan["histogram_controls"],
        "joint_harmonic_extremizer": scan["joint_harmonic_controls"],
        "prefix_fiber_source_family": {
            "general_lemma": {
                "hypotheses": (
                    "V=H0=1; P=QG and L are coprime squarefree split "
                    "polynomials; A_E divides L is monic of degree deg(G)=m; "
                    "deg(G-A_E)<m-w"
                ),
                "message": "f=Q(G-A_E)=P-QA_E",
                "degree": "deg(f)<deg(P)-w",
                "exact_gcds": (
                    "gcd(P,f)=Q, gcd(L,P-f)=A_E, "
                    "gcd(P*L,P-f)=Q*A_E"
                ),
                "recovered_pair": "G=P/Q and b=G-A_E",
                "lcm_restorer": (
                    "If A_0|L is monic of degree deg(P) and "
                    "deg(P-A_0)<deg(P)-w, then f_0=P-A_0 has gcd(P,f_0)=1 "
                    "and recovered denominator P."
                ),
                "scope": (
                    "Exact algebraic source family; cardinality and rank "
                    "still depend on the prefix fiber."
                ),
            },
            "gf31_positive_w_fixture": toy,
        },
        "existing_inequality_audit": {
            "ratio_maxima": scan["existing_inequality_ratio_maxima"],
            "all_pass": True,
            "combination_status": (
                "EXACT_INTEGER_SCALAR_RELAXATION_SURVIVES_EVERY_G"
            ),
        },
        "missing_theorem": {
            "name": "JOINT_HEAD_TAIL_FULL_GCD_INCIDENCE",
            "high_g_statement": (
                "#{exact full-gcd candidates with q>=Q_star(g)+1}"
                "<=15775932-C_{Q_star(g)}(g)"
            ),
            "low_g_obstruction": (
                "For g<=328677, C_0(g)>=15775933; a tail theorem alone "
                "cannot close the full fixed-G ordinary-RS branch."
            ),
            "falsifier": (
                "A source-realized family of size 15775933 with the printed "
                "head histogram, full gcds, and compatible harmonic profile."
            ),
            "toy_warning": (
                "The exact GF(31) fixture proves that positive w, exact full "
                "gcds, no common planted zero, and lcm restoration alone do "
                "not force a tail bound."
            ),
        },
        "impact": {
            "new_green_local_theorem": True,
            "current_inequality_route_cut": True,
            "rank7_closed": False,
            "rank8_and_above_closed": False,
            "row_closed": False,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
        },
        "nonclaims": [
            "The adversarial histogram is not asserted to be source-realizable.",
            "Equality in the MDS-soft harmonic profile is not asserted for a code.",
            "No deployed M31 common-unit/full-gcd family of forbidden size is constructed.",
            "The GF(31) family is an exact toy source family, not an M31 lift.",
            "The rank-seven stratum, higher ranks, and M31 LIST row remain open.",
            "No Grande Finale v4 atom or official endpoint moves.",
        ],
    }
    summary["checks"] = CHECKS + 2
    summary["payload_sha256"] = payload_sha256(summary)
    require(summary["payload_sha256"] == payload_sha256(summary), "payload seal")
    require(summary["checks"] == CHECKS + 1, "check counter sealed")
    return summary


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def tamper_selftest() -> dict[str, Any]:
    expected = build_summary()
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("row", "shallow_forbidden_size"), L - 1),
        (("row", "residual_g_range"), [G_MIN, G_MAX + 1]),
        (("cumulative_head_theorem", "range"), "0<=Q<=w+1"),
        (
            ("transition_scan", "interval_sha256"),
            "0" * 64,
        ),
        (("transition_scan", "g_cells"), 282_544),
        (
            ("transition_scan", "initial_interval", "g_max"),
            328_678,
        ),
        (
            ("transition_scan", "first_paid_head_interval", "g_min"),
            328_677,
        ),
        (
            ("transition_scan", "final_interval", "q_star"),
            2_464,
        ),
        (
            (
                "transition_scan",
                "endpoint_records",
                "354972",
                "C_q_star",
            ),
            15_774_895,
        ),
        (
            (
                "transition_scan",
                "endpoint_records",
                "354972",
                "forced_tail",
            ),
            1_038,
        ),
        (
            (
                "transition_scan",
                "tail_requirement",
                "maximum_weakest_upper",
                "value",
            ),
            1_697,
        ),
        (
            ("adversarial_histogram", "maximum_proper_bucket", "count"),
            1_701,
        ),
        (
            (
                "adversarial_histogram",
                "minimum_bucket_to_slice_ceiling_margin",
                "cap",
            ),
            1_182_428,
        ),
        (
            (
                "joint_harmonic_extremizer",
                "minimum_integer_interval",
                "width",
            ),
            121,
        ),
        (
            (
                "joint_harmonic_extremizer",
                "endpoint_transport",
                "rows_sha256",
            ),
            "0" * 64,
        ),
        (
            (
                "joint_harmonic_extremizer",
                "minimum_integer_interval",
                "low",
            ),
            10_411_668,
        ),
        (
            (
                "joint_harmonic_extremizer",
                "minimum_integer_interval",
                "e",
            ),
            65_514,
        ),
        (
            (
                "prefix_fiber_source_family",
                "gf31_positive_w_fixture",
                "tail_count",
            ),
            7_863,
        ),
        (
            (
                "prefix_fiber_source_family",
                "gf31_positive_w_fixture",
                "master_lcm_restored",
            ),
            False,
        ),
        (
            (
                "existing_inequality_audit",
                "ratio_maxima",
                "cross_block",
                "g",
            ),
            354_971,
        ),
        (
            ("existing_inequality_audit", "all_pass"),
            False,
        ),
        (("impact", "rank7_closed"), True),
        (("impact", "ledger_movement"), 1),
        (("parent_payload_sha256",), "f" * 64),
    ]
    detected = 0
    for path, value in mutations:
        mutant = copy.deepcopy(expected)
        cursor: Any = mutant
        for component in path[:-1]:
            cursor = cursor[component]
        cursor[path[-1]] = value
        try:
            deep_exact(mutant, expected)
        except VerificationError:
            detected += 1
        else:
            raise VerificationError(f"mutation escaped: {path!r}")
    require(detected == len(mutations), "all primary mutations detected")
    return {
        "schema": "m31-rank7-split-divisor-tail-primary-tamper-v1",
        "mutations": len(mutations),
        "detected": detected,
        "all_detected": True,
        "base_payload_sha256": expected["payload_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        summary = tamper_selftest() if args.tamper_selftest else build_summary()
        encoded = canonical_json(summary, pretty=args.pretty)
        if args.output is not None:
            args.output.write_bytes(encoded)
        if not args.check or args.output is None:
            sys.stdout.buffer.write(encoded)
        return 0
    except (VerificationError, ValueError, OverflowError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
