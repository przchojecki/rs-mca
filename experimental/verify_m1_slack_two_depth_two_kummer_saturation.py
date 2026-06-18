#!/usr/bin/env python3
"""Audit the slack-two depth-two Kummer-Weil saturation certificate."""

from __future__ import annotations

import math
from itertools import product
from typing import Sequence, Tuple

from m1_support_occupancy_scan import (
    all_residual_packets_lift_active,
    ceil_sqrt,
    kummer_quadratic_uniform_prime_threshold,
    quotient_limited_pair_parameter_bound,
    quotient_window_label_nonprincipal_bound,
    quotient_window_label_l1_data,
    quotient_window_label_triple_count,
    scan_supports,
    slack_two_second_fixed_window_data,
    slack_two_second_fixed_window_kummer_saturation_data,
    slack_two_second_quotient_window_union_kummer_saturation_data,
    slack_two_second_quotient_window_reduction_data,
    slack_two_second_kummer_saturation_data,
    slack_two_second_superboundary_shape_ledger,
    slack_two_second_two_fiber_kummer_saturation_data,
    slack_two_second_two_fiber_union_reduction_data,
    slack_two_second_two_fiber_window_data,
)
from mca_slope_scan import make_domain


CASES = (
    # Index-two proper subgroups where the certificate is positive.
    (383, 191, True),
    (769, 384, True),
    # A high-index sample from the non-field-filling side of the existing PR.
    (193, 6, False),
)

LIFT_CASES = (
    # The only quotient fiber is left unused, so every packet is active.
    (17, 16, 1, 16, 4, True),
    # Six quotient fibers, two whole fibers selected, four left for any packet.
    (97, 48, 6, 8, 20, True),
    # Only three quotient fibers remain, so four-fiber packets are not certified.
    (97, 48, 6, 8, 28, False),
)

LIFT_BOUND_CASES = (
    # Only one quotient fiber remains, giving a nontrivial exact-slope bound.
    (97, 48, 6, 8, 44, True),
    # Three quotient fibers remain; the bound is true but field-trivial here.
    (97, 48, 6, 8, 28, False),
)

KERNEL_REDUCTION_CASES = (
    # R=1: active normalized shapes are exactly the quotient-kernel catalog.
    (97, 48, 6, 8, 44),
)

TWO_FIBER_KUMMER_CASES = (
    # Small lift-limited sample: a fixed two-fiber window is not saturated.
    (97, 48, 6, False),
    # Full-domain N=3 sample where the two-fiber certificate is positive.
    (919, 918, 3, True),
    # Proper index-two N=3 sample above the uniform two-fiber threshold.
    (7351, 3675, 3, True),
)

TWO_FIBER_UNION_CASES = (
    # R=2: no fixed two-fiber certificate, but the union saturates.
    (97, 48, 6, 8, 36),
)

R_WINDOW_CASES = (
    # R=1: the general window reduction specializes to the kernel reduction.
    (97, 48, 6, 8, 44, False),
    # R=2: the general reduction agrees with the two-fiber union.
    (97, 48, 6, 8, 36, True),
    # R=3: exact-support saturation below the all-shapes R=4 gate.
    (97, 48, 6, 8, 28, True),
)

FIXED_WINDOW_KUMMER_CASES = (
    # Small R=3 sample below the conservative fixed-window threshold.
    (97, 48, 6, 3, False),
    # Positive fixed R=3 certificate for a full-domain N=4 window.
    (2213, 2212, 4, 3, True),
)

R_WINDOW_UNION_KUMMER_CASES = (
    # Exact R=2 union saturation, but below the union Kummer threshold.
    (97, 48, 6, 2, False, False),
    # Both union L1 and complement-window L1 certify this R=2 case.
    (181, 180, 3, 2, True, True),
    # Both union L1 and complement-window L1 certify this R=3 case.
    (113, 112, 4, 3, True, True),
)

EQUAL_LINE_SPLIT_CASES = (
    (3, 3),
    (4, 4),
    (6, 6),
    (12, 12),
    (5, 10),
    (6, 12),
    (9, 18),
    (12, 24),
    (32, 64),
)

SCAN_LABEL_CASES = (
    # Public scanner regression for the R=2 union-saturated label.
    (19, 18, 8, 2, 3, "r2_union_saturated"),
)


def divisor_power_failure_count(character_order: int, square_kernel_index: int) -> int:
    square_coset_index = character_order * square_kernel_index
    failures = 0
    for a in range(character_order):
        for b in range(character_order):
            for c in range(character_order):
                for d in range(square_coset_index):
                    if (a, b, c, d) == (0, 0, 0, 0):
                        continue
                    divisor_exponents = (
                        square_kernel_index * a,
                        square_kernel_index * b,
                        square_kernel_index * c,
                        d,
                    )
                    if all(
                        exponent % square_coset_index == 0
                        for exponent in divisor_exponents
                    ):
                        failures += 1
    return failures


def two_fiber_divisor_power_failure_count(
    kernel_character_order: int,
    square_coset_index: int,
) -> int:
    failures = 0
    for a in range(kernel_character_order):
        for b in range(kernel_character_order):
            for c in range(kernel_character_order):
                for d in range(square_coset_index):
                    if (a, b, c, d) == (0, 0, 0, 0):
                        continue
                    divisor_exponents = (a, b, c, d)
                    if all(exponent == 0 for exponent in divisor_exponents):
                        failures += 1
    return failures


def raw_two_coordinate_projective_l1_split(
    character_order: int,
    square_coset_index: int,
) -> dict[str, int]:
    if square_coset_index % character_order:
        raise AssertionError((character_order, square_coset_index))
    lift = square_coset_index // character_order
    infinity_unramified = 0
    projective_reciprocal = 0
    ramified_nonreciprocal = 0
    coordinate_diagonal = 0
    coordinate_diagonal_alpha_square_trivial = 0
    coordinate_diagonal_2f1_cancellation = 0
    projective_equal_pair = 0
    equal_line_diagonal = 0
    projective_asymmetric_line_conic_resonant = 0
    for first_exponent in range(1, character_order):
        for second_exponent in range(1, character_order):
            for conic_exponent in range(1, square_coset_index):
                first = lift * first_exponent
                second = lift * second_exponent
                infinity = (-(first + second + 2 * conic_exponent)) % (
                    square_coset_index
                )
                if infinity == 0:
                    infinity_unramified += 1
                elif (
                    (first + second) % square_coset_index == 0
                    or (first + infinity) % square_coset_index == 0
                    or (second + infinity) % square_coset_index == 0
                ):
                    projective_reciprocal += 1
                else:
                    ramified_nonreciprocal += 1
                    has_projective_equal_pair = (
                        first == second
                        or first == infinity
                        or second == infinity
                    )
                    if first == second:
                        coordinate_diagonal += 1
                        alpha = (first + conic_exponent) % square_coset_index
                        if (2 * alpha) % square_coset_index == 0:
                            coordinate_diagonal_alpha_square_trivial += 1
                        if alpha == first or (
                            square_coset_index % 2 == 0
                            and alpha == square_coset_index // 2
                        ):
                            coordinate_diagonal_2f1_cancellation += 1
                    if has_projective_equal_pair:
                        projective_equal_pair += 1
                    else:
                        has_line_conic_resonance = (
                            (first + conic_exponent) % square_coset_index == 0
                            or (second + conic_exponent)
                            % square_coset_index
                            == 0
                            or (infinity + conic_exponent)
                            % square_coset_index
                            == 0
                        )
                        if has_line_conic_resonance:
                            projective_asymmetric_line_conic_resonant += 1
                    if first == second == infinity:
                        equal_line_diagonal += 1
    active_pair_count = 3
    projective_asymmetric = ramified_nonreciprocal - projective_equal_pair
    if projective_asymmetric < 0 or projective_asymmetric % 2:
        raise AssertionError(
            (character_order, square_coset_index, projective_asymmetric)
        )
    projective_asymmetric_line_conic_nonresonant = (
        projective_asymmetric - projective_asymmetric_line_conic_resonant
    )
    if projective_asymmetric_line_conic_nonresonant < 0:
        raise AssertionError(
            (
                character_order,
                square_coset_index,
                projective_asymmetric_line_conic_resonant,
            )
        )
    return {
        "infinity_unramified": active_pair_count * infinity_unramified,
        "projective_reciprocal": active_pair_count * projective_reciprocal,
        "ramified_nonreciprocal": active_pair_count * ramified_nonreciprocal,
        "coordinate_diagonal": active_pair_count * coordinate_diagonal,
        "coordinate_diagonal_non_equal": (
            active_pair_count * (coordinate_diagonal - equal_line_diagonal)
        ),
        "coordinate_diagonal_alpha_square_trivial_count": (
            active_pair_count * coordinate_diagonal_alpha_square_trivial
        ),
        "coordinate_diagonal_2f1_cancellation_count": (
            active_pair_count * coordinate_diagonal_2f1_cancellation
        ),
        "projective_equal_pair": active_pair_count * projective_equal_pair,
        "projective_equal_pair_non_coordinate": (
            active_pair_count * (projective_equal_pair - coordinate_diagonal)
        ),
        "projective_asymmetric": active_pair_count * projective_asymmetric,
        "projective_asymmetric_orbit_count": (
            active_pair_count * projective_asymmetric // 6
        ),
        "projective_asymmetric_line_conic_resonant": (
            active_pair_count * projective_asymmetric_line_conic_resonant
        ),
        "projective_asymmetric_line_conic_nonresonant": (
            active_pair_count * projective_asymmetric_line_conic_nonresonant
        ),
        "projective_asymmetric_line_conic_resonant_orbit_count": (
            active_pair_count * projective_asymmetric_line_conic_resonant // 6
        ),
        "projective_asymmetric_line_conic_nonresonant_orbit_count": (
            active_pair_count
            * projective_asymmetric_line_conic_nonresonant
            // 6
        ),
        "equal_line_diagonal": active_pair_count * equal_line_diagonal,
    }


def equal_line_diagonal_pair_count_formula(
    character_order: int,
    square_coset_index: int,
) -> int:
    if square_coset_index % character_order:
        raise AssertionError((character_order, square_coset_index))
    e = character_order
    q = square_coset_index
    lift = q // e
    if lift == 1:
        if e % 2:
            return e - math.gcd(e, 3)
        half = e // 2
        even_allowed = half - 1 - (1 if e % 4 == 0 else 0)
        zero_solutions = math.gcd(half, 3) - 1
        return 2 * even_allowed - zero_solutions
    if lift == 2:
        allowed = e - 1 - (1 if e % 2 == 0 else 0)
        zero_solutions = math.gcd(e, 3) - 1
        return 2 * allowed - zero_solutions
    raise AssertionError((character_order, square_coset_index, lift))


def coordinate_diagonal_pair_count_formula(
    character_order: int,
    square_coset_index: int,
) -> int:
    if square_coset_index % character_order:
        raise AssertionError((character_order, square_coset_index))
    e = character_order
    q = square_coset_index
    lift = q // e
    if lift == 1:
        if e % 2:
            return (e - 1) * (e - 3)
        even_allowed = e // 2 - 1 - (1 if e % 4 == 0 else 0)
        return (e - 2) * (e - 3) - 2 * even_allowed
    if lift == 2:
        allowed = e - 1 - (1 if e % 2 == 0 else 0)
        return allowed * (2 * e - 5)
    raise AssertionError((character_order, square_coset_index, lift))


def projective_equal_pair_count_formula(
    character_order: int,
    square_coset_index: int,
) -> int:
    coordinate = coordinate_diagonal_pair_count_formula(
        character_order,
        square_coset_index,
    )
    equal_line = equal_line_diagonal_pair_count_formula(
        character_order,
        square_coset_index,
    )
    return 3 * coordinate - 2 * equal_line


def asymmetric_line_conic_resonant_pair_count_formula(
    character_order: int,
    square_coset_index: int,
) -> int:
    if square_coset_index % character_order:
        raise AssertionError((character_order, square_coset_index))
    e = character_order
    lift = square_coset_index // e
    if lift not in (1, 2):
        raise AssertionError((character_order, square_coset_index, lift))
    single_line_count = (e - 1) * (e - 5)
    if e % 2 == 0:
        single_line_count += 3
    single_line_count += 2 * (math.gcd(e, 3) - 1)
    return 3 * single_line_count


def coordinate_diagonal_parameter_failure_counts(
    character_order: int,
    square_coset_index: int,
) -> dict[str, int]:
    if square_coset_index % character_order:
        raise AssertionError((character_order, square_coset_index))
    e = character_order
    q = square_coset_index
    lift = q // e
    alpha_square_trivial = 0
    twof1_cancellation = 0
    for exponent in range(1, e):
        first = lift * exponent % q
        for conic_exponent in range(1, q):
            infinity = (-(2 * first + 2 * conic_exponent)) % q
            if infinity == 0:
                continue
            if (2 * first) % q == 0:
                continue
            if (first + infinity) % q == 0:
                continue
            alpha = (first + conic_exponent) % q
            if (2 * alpha) % q == 0:
                alpha_square_trivial += 1
            if alpha == first or (q % 2 == 0 and alpha == q // 2):
                twof1_cancellation += 1
    return {
        "alpha_square_trivial": alpha_square_trivial,
        "twof1_cancellation": twof1_cancellation,
    }


def raw_two_coordinate_projective_l1_split_formula(
    character_order: int,
    square_coset_index: int,
) -> dict[str, int]:
    if square_coset_index % character_order:
        raise AssertionError((character_order, square_coset_index))
    e = character_order
    q = square_coset_index
    lift = q // e
    if lift == 1:
        if e % 2:
            infinity_unramified = (e - 1) * (e - 2)
            projective_reciprocal = 3 * (e - 1) * (e - 2)
        else:
            infinity_unramified = (e - 1) * (e - 2) + 1
            projective_reciprocal = 3 * (e - 2) * (e - 2)
            if e % 4 == 0:
                projective_reciprocal += 2
    elif lift == 2:
        infinity_unramified = (e - 1) * (2 * e - 3)
        projective_reciprocal = 6 * (e - 1) * (e - 2)
        if e % 2 == 0:
            projective_reciprocal += 2
    else:
        raise AssertionError((character_order, square_coset_index, lift))
    total = (e - 1) * (e - 1) * (q - 1)
    diagonal_failures = coordinate_diagonal_parameter_failure_counts(
        character_order,
        square_coset_index,
    )
    if any(diagonal_failures.values()):
        raise AssertionError(
            (character_order, square_coset_index, diagonal_failures)
        )
    projective_equal_pair = projective_equal_pair_count_formula(
        character_order,
        square_coset_index,
    )
    projective_asymmetric = (
        total - infinity_unramified - projective_reciprocal - projective_equal_pair
    )
    line_conic_resonant = asymmetric_line_conic_resonant_pair_count_formula(
        character_order,
        square_coset_index,
    )
    line_conic_nonresonant = projective_asymmetric - line_conic_resonant
    if line_conic_nonresonant < 0:
        raise AssertionError(
            (character_order, square_coset_index, line_conic_resonant)
        )
    return {
        "infinity_unramified": 3 * infinity_unramified,
        "projective_reciprocal": 3 * projective_reciprocal,
        "ramified_nonreciprocal": (
            3 * (total - infinity_unramified - projective_reciprocal)
        ),
        "coordinate_diagonal": (
            3
            * coordinate_diagonal_pair_count_formula(
                character_order,
                square_coset_index,
            )
        ),
        "coordinate_diagonal_non_equal": (
            3
            * (
                coordinate_diagonal_pair_count_formula(
                    character_order,
                    square_coset_index,
                )
                - equal_line_diagonal_pair_count_formula(
                    character_order,
                    square_coset_index,
                )
            )
        ),
        "coordinate_diagonal_alpha_square_trivial_count": 0,
        "coordinate_diagonal_2f1_cancellation_count": 0,
        "projective_equal_pair": (
            3
            * projective_equal_pair
        ),
        "projective_equal_pair_non_coordinate": (
            3
            * (
                projective_equal_pair
                - coordinate_diagonal_pair_count_formula(
                    character_order,
                    square_coset_index,
                )
            )
        ),
        "projective_asymmetric": 3 * projective_asymmetric,
        "projective_asymmetric_orbit_count": projective_asymmetric // 2,
        "projective_asymmetric_line_conic_resonant": 3 * line_conic_resonant,
        "projective_asymmetric_line_conic_nonresonant": (
            3 * line_conic_nonresonant
        ),
        "projective_asymmetric_line_conic_resonant_orbit_count": (
            line_conic_resonant // 2
        ),
        "projective_asymmetric_line_conic_nonresonant_orbit_count": (
            line_conic_nonresonant // 2
        ),
        "equal_line_diagonal": (
            3
            * equal_line_diagonal_pair_count_formula(
                character_order,
                square_coset_index,
            )
        ),
    }


def principal_open_count(p: int) -> int:
    count = 0
    for u in range(p):
        for v in range(p):
            w = (-1 - u - v) % p
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if u and v and w and shape_slope:
                count += 1
    return count


def degeneracy_line_union_count(p: int) -> int:
    count = 0
    for u in range(p):
        for v in range(p):
            w = (-1 - u - v) % p
            if u == 1 or v == 1 or w == 1 or u == v or u == w or v == w:
                count += 1
    return count


def square_coset_counts(p: int, domain: Sequence[int]) -> Tuple[int, int]:
    domain_set = set(domain)
    square_image = {x * x % p for x in domain}
    nonzero_cosets = set()
    for u in domain:
        for v in domain:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in domain_set or len(set(values)) != 4:
                continue
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                continue
            nonzero_cosets.add(
                min((shape_slope * square) % p for square in square_image)
            )
    return len(nonzero_cosets), (p - 1) // len(square_image)


def lift_limited_bound_formula(
    quotient_order: int,
    fiber_size: int,
    remaining_fibers: int,
) -> int:
    max_touched = min(remaining_fibers, 4, quotient_order)
    return sum(
        math.comb(quotient_order - 1, touched - 1)
        * (touched * fiber_size) ** 2
        for touched in range(1, max_touched + 1)
    )


def direct_quotient_window_label_triple_count(
    quotient_order: int,
    window_size: int,
) -> int:
    return sum(
        1
        for labels in product(range(quotient_order), repeat=3)
        if len({0, *labels}) <= window_size
    )


def quotient_label_sum(value: int, quotient_order: int) -> int:
    return quotient_order - 1 if value % quotient_order == 0 else -1


def quotient_window_label_coefficient(
    quotient_order: int,
    window_size: int,
    triple: Tuple[int, int, int],
) -> int:
    r, s, t = triple
    if window_size == 1:
        return 1
    if window_size == 2:
        zero_subset_count = 0
        frequencies = (r, s, t)
        for mask in range(1, 8):
            subset_sum = sum(
                frequencies[index]
                for index in range(3)
                if mask & (1 << index)
            )
            if subset_sum % quotient_order == 0:
                zero_subset_count += 1
        return zero_subset_count * quotient_order - 6
    if window_size == 3:
        full_cube = quotient_order ** 3 if (r, s, t) == (0, 0, 0) else 0
        distinct_nonzero = (
            quotient_label_sum(r, quotient_order)
            * quotient_label_sum(s, quotient_order)
            * quotient_label_sum(t, quotient_order)
            - quotient_label_sum(r + s, quotient_order)
            * quotient_label_sum(t, quotient_order)
            - quotient_label_sum(r + t, quotient_order)
            * quotient_label_sum(s, quotient_order)
            - quotient_label_sum(s + t, quotient_order)
            * quotient_label_sum(r, quotient_order)
            + 2 * quotient_label_sum(r + s + t, quotient_order)
        )
        return full_cube - distinct_nonzero
    return 0


def direct_quotient_window_label_nonprincipal_bound(
    quotient_order: int,
    window_size: int,
) -> int:
    return max(
        abs(
            quotient_window_label_coefficient(
                quotient_order,
                window_size,
                (r, s, t),
            )
        )
        for r in range(quotient_order)
        for s in range(quotient_order)
        for t in range(quotient_order)
        if (r, s, t) != (0, 0, 0)
    )


def direct_quotient_window_label_l1_data(
    quotient_order: int,
    window_size: int,
) -> Tuple[
    int,
    Tuple[Tuple[int, int], ...],
    Tuple[Tuple[int, int], ...],
]:
    total = 0
    zero_subset_histogram = {}
    coefficient_histogram = {}
    for r in range(quotient_order):
        for s in range(quotient_order):
            for t in range(quotient_order):
                coefficient = quotient_window_label_coefficient(
                    quotient_order,
                    window_size,
                    (r, s, t),
                )
                total += abs(coefficient)
                coefficient_histogram[coefficient] = (
                    coefficient_histogram.get(coefficient, 0) + 1
                )
                if window_size == 2:
                    zero_subset_count = sum(
                        (
                            (sum(
                                (r, s, t)[index]
                                for index in range(3)
                                if mask & (1 << index)
                            )
                            % quotient_order)
                            == 0
                        )
                        for mask in range(1, 8)
                    )
                    zero_subset_histogram[zero_subset_count] = (
                        zero_subset_histogram.get(zero_subset_count, 0) + 1
                    )
    return (
        total,
        tuple(sorted(zero_subset_histogram.items())),
        tuple(sorted(coefficient_histogram.items())),
    )


def direct_ambient_window_label_l1_bound(
    ambient_character_order: int,
    quotient_order: int,
    window_size: int,
    square_coset_index: int,
) -> int:
    label_triples = direct_quotient_window_label_triple_count(
        quotient_order,
        window_size,
    )
    quotient_l1_bound = sum(
        abs(
            quotient_window_label_coefficient(
                quotient_order,
                window_size,
                (
                    r % quotient_order,
                    s % quotient_order,
                    t % quotient_order,
                ),
            )
        )
        for r in range(ambient_character_order)
        for s in range(ambient_character_order)
        for t in range(ambient_character_order)
    )
    return square_coset_index * quotient_l1_bound - label_triples


def direct_ambient_window_label_one_coordinate_l1_bound(
    ambient_character_order: int,
    quotient_order: int,
    window_size: int,
) -> int:
    total = 0
    for coordinate in range(3):
        for frequency in range(1, ambient_character_order):
            triple = [0, 0, 0]
            triple[coordinate] = frequency
            total += abs(
                quotient_window_label_coefficient(
                    quotient_order,
                    window_size,
                    (
                        triple[0] % quotient_order,
                        triple[1] % quotient_order,
                        triple[2] % quotient_order,
                    ),
                )
            )
    return total


def direct_ambient_window_label_coordinate_active_l1_bounds(
    ambient_character_order: int,
    quotient_order: int,
    window_size: int,
) -> Tuple[int, int, int]:
    totals = [0, 0, 0, 0]
    for r in range(ambient_character_order):
        for s in range(ambient_character_order):
            for t in range(ambient_character_order):
                active_count = int(r != 0) + int(s != 0) + int(t != 0)
                if active_count == 0:
                    continue
                totals[active_count] += abs(
                    quotient_window_label_coefficient(
                        quotient_order,
                        window_size,
                        (
                            r % quotient_order,
                            s % quotient_order,
                            t % quotient_order,
                        ),
                    )
                )
    return (totals[1], totals[2], totals[3])


def fixed_window_parseval_active_l1_bound(
    quotient_order: int,
    window_size: int,
    ambient_restriction_kernel_count: int,
) -> int:
    radicand = (quotient_order - 1) * window_size * (
        quotient_order - window_size
    )
    root = math.isqrt(radicand)
    if root * root < radicand:
        root += 1
    return (
        (ambient_restriction_kernel_count - 1) * window_size
        + ambient_restriction_kernel_count * root
    )


def kernel_fiber_reduction_counts(
    p: int,
    domain: Sequence[int],
    quotient_order: int,
) -> Tuple[int, int, int, int, int]:
    kernel = tuple(domain[index] for index in range(0, len(domain), quotient_order))
    kernel_set = set(kernel)
    square_image = {x * x % p for x in domain}
    nonzero_cosets = set()
    parameter_count = 0
    zero_parameter_count = 0
    for u in kernel:
        for v in kernel:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in kernel_set or len(set(values)) != 4:
                continue
            parameter_count += 1
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                zero_parameter_count += 1
                continue
            nonzero_cosets.add(
                min((shape_slope * square) % p for square in square_image)
            )
    slope_count = (1 if zero_parameter_count else 0) + (
        len(nonzero_cosets) * len(square_image)
    )
    return (
        len(kernel),
        parameter_count,
        zero_parameter_count,
        len(nonzero_cosets),
        min(p, slope_count),
    )


def main() -> None:
    checked = []
    for p, n, expected_certificate in CASES:
        _, domain = make_domain(p, n, None)
        certificate = slack_two_second_kummer_saturation_data(p, n)
        failures = divisor_power_failure_count(
            int(certificate["character_order"]),
            int(certificate["square_kernel_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        deligne_constant = (radical_total - 1) ** 2
        if deligne_constant != int(certificate["deligne_constant"]):
            raise AssertionError((p, n, deligne_constant, certificate))
        if not bool(certificate["deligne_constant_check"]):
            raise AssertionError((p, n, certificate))
        principal_count = principal_open_count(p)
        if principal_count != int(certificate["principal_exact_count"]):
            raise AssertionError((p, n, principal_count, certificate))
        degeneracy_count = degeneracy_line_union_count(p)
        if degeneracy_count != int(certificate["degeneracy_line_union_count"]):
            raise AssertionError((p, n, degeneracy_count, certificate))
        coefficient_l1_bound = int(certificate["denominator"]) - 1
        if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        character_triple_count = int(certificate["character_order"]) ** 3
        square_coset_index = int(certificate["square_coset_index"])
        jacobi_l1_bound = character_triple_count - 1
        conic_l1_bound = square_coset_index - 1
        quadratic_conic_character_count = (
            1 if square_coset_index > 1 and square_coset_index % 2 == 0 else 0
        )
        coordinate_one_l1_bound = (
            3 * (int(certificate["character_order"]) - 1)
        )
        coordinate_two_l1_bound = (
            3 * (int(certificate["character_order"]) - 1) ** 2
        )
        coordinate_three_l1_bound = (
            (int(certificate["character_order"]) - 1) ** 3
        )
        quadratic_one_coordinate_l1_bound = (
            coordinate_one_l1_bound * quadratic_conic_character_count
        )
        one_coordinate_kummer_l1_bound = coordinate_one_l1_bound * (
            square_coset_index - 1 - quadratic_conic_character_count
        )
        two_coordinate_kummer_l1_bound = (
            coordinate_two_l1_bound * (square_coset_index - 1)
        )
        two_coordinate_projective_split = raw_two_coordinate_projective_l1_split(
            int(certificate["character_order"]),
            square_coset_index,
        )
        two_coordinate_projective_formula = (
            raw_two_coordinate_projective_l1_split_formula(
                int(certificate["character_order"]),
                square_coset_index,
            )
        )
        if two_coordinate_projective_split != two_coordinate_projective_formula:
            raise AssertionError(
                (
                    p,
                    n,
                    two_coordinate_projective_split,
                    two_coordinate_projective_formula,
                )
            )
        two_coordinate_infinity_unramified_l1_bound = int(
            two_coordinate_projective_split["infinity_unramified"]
        )
        two_coordinate_projective_reciprocal_l1_bound = int(
            two_coordinate_projective_split["projective_reciprocal"]
        )
        two_coordinate_ramified_nonreciprocal_l1_bound = int(
            two_coordinate_projective_split["ramified_nonreciprocal"]
        )
        two_coordinate_equal_line_l1_bound = int(
            two_coordinate_projective_split["equal_line_diagonal"]
        )
        two_coordinate_coordinate_diagonal_l1_bound = int(
            two_coordinate_projective_split["coordinate_diagonal"]
        )
        two_coordinate_projective_equal_pair_l1_bound = int(
            two_coordinate_projective_split["projective_equal_pair"]
        )
        two_coordinate_projective_asymmetric_nonresonant_l1_bound = int(
            two_coordinate_projective_split[
                "projective_asymmetric_line_conic_nonresonant"
            ]
        )
        two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound = int(
            two_coordinate_projective_split[
                "projective_asymmetric_line_conic_resonant"
            ]
        )
        two_coordinate_ramified_l1_bound = (
            two_coordinate_kummer_l1_bound
            - two_coordinate_infinity_unramified_l1_bound
        )
        three_coordinate_kummer_l1_bound = (
            coordinate_three_l1_bound * (square_coset_index - 1)
        )
        kummer_l1_bound = (
            one_coordinate_kummer_l1_bound
            + two_coordinate_kummer_l1_bound
            + three_coordinate_kummer_l1_bound
        )
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["quadratic_one_coordinate_error_constant"])
            * quadratic_one_coordinate_l1_bound
            + int(certificate["one_coordinate_kummer_error_constant"])
            * one_coordinate_kummer_l1_bound
            + int(
                certificate[
                    "two_coordinate_infinity_unramified_error_constant"
                ]
            )
            * two_coordinate_infinity_unramified_l1_bound
            + int(
                certificate[
                    "two_coordinate_projective_reciprocal_error_constant"
                ]
            )
            * two_coordinate_projective_reciprocal_l1_bound
            + int(certificate["two_coordinate_kummer_error_constant"])
            * two_coordinate_ramified_nonreciprocal_l1_bound
            + int(certificate["three_coordinate_kummer_error_constant"])
            * three_coordinate_kummer_l1_bound
        )
        if (
            jacobi_l1_bound
            + conic_l1_bound
            + quadratic_one_coordinate_l1_bound
            + kummer_l1_bound
            != coefficient_l1_bound
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if quadratic_one_coordinate_l1_bound != int(
            certificate["quadratic_one_coordinate_l1_bound"]
        ):
            raise AssertionError(
                (p, n, quadratic_one_coordinate_l1_bound, certificate)
            )
        if one_coordinate_kummer_l1_bound != int(
            certificate["one_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, one_coordinate_kummer_l1_bound))
        if two_coordinate_kummer_l1_bound != int(
            certificate["two_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, two_coordinate_kummer_l1_bound))
        if two_coordinate_infinity_unramified_l1_bound != int(
            certificate["two_coordinate_infinity_unramified_l1_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    two_coordinate_infinity_unramified_l1_bound,
                    certificate,
                )
            )
        if two_coordinate_ramified_l1_bound != int(
            certificate["two_coordinate_ramified_l1_bound"]
        ):
            raise AssertionError(
                (p, n, two_coordinate_ramified_l1_bound, certificate)
            )
        if two_coordinate_projective_reciprocal_l1_bound != int(
            certificate["two_coordinate_projective_reciprocal_l1_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    two_coordinate_projective_reciprocal_l1_bound,
                    certificate,
                )
            )
        if two_coordinate_ramified_nonreciprocal_l1_bound != int(
            certificate["two_coordinate_ramified_nonreciprocal_l1_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    two_coordinate_ramified_nonreciprocal_l1_bound,
                    certificate,
                )
            )
        if two_coordinate_equal_line_l1_bound != int(
            certificate["two_coordinate_equal_line_l1_bound"]
        ):
            raise AssertionError(
                (p, n, two_coordinate_equal_line_l1_bound, certificate)
            )
        if int(two_coordinate_projective_split["coordinate_diagonal"]) != int(
            certificate["two_coordinate_coordinate_diagonal_l1_bound"]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split["coordinate_diagonal_non_equal"]
        ) != int(
            certificate[
                "two_coordinate_coordinate_diagonal_non_equal_l1_bound"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "coordinate_diagonal_alpha_square_trivial_count"
            ]
        ) != int(
            certificate[
                "two_coordinate_coordinate_diagonal_alpha_square_trivial_count"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "coordinate_diagonal_2f1_cancellation_count"
            ]
        ) != int(
            certificate[
                "two_coordinate_coordinate_diagonal_2f1_cancellation_count"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(two_coordinate_projective_split["projective_equal_pair"]) != int(
            certificate["two_coordinate_projective_equal_pair_l1_bound"]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "projective_equal_pair_non_coordinate"
            ]
        ) != int(
            certificate[
                "two_coordinate_projective_equal_pair_non_coordinate_l1_bound"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(two_coordinate_projective_split["projective_asymmetric"]) != int(
            certificate["two_coordinate_projective_asymmetric_l1_bound"]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "projective_asymmetric_orbit_count"
            ]
        ) != int(
            certificate["two_coordinate_projective_asymmetric_orbit_count"]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "projective_asymmetric_line_conic_resonant"
            ]
        ) != int(
            certificate[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_l1_bound"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "projective_asymmetric_line_conic_nonresonant"
            ]
        ) != int(
            certificate[
                "two_coordinate_projective_asymmetric_line_conic_"
                "nonresonant_l1_bound"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "projective_asymmetric_line_conic_resonant_orbit_count"
            ]
        ) != int(
            certificate[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_orbit_count"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(
            two_coordinate_projective_split[
                "projective_asymmetric_line_conic_nonresonant_orbit_count"
            ]
        ) != int(
            certificate[
                "two_coordinate_projective_asymmetric_line_conic_"
                "nonresonant_orbit_count"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if int(certificate["two_coordinate_projective_asymmetric_l1_bound"]) % 6:
            raise AssertionError((p, n, certificate))
        if two_coordinate_projective_asymmetric_nonresonant_l1_bound != int(
            certificate[
                "two_coordinate_projective_asymmetric_nonresonant_l1_bound"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound != int(
            certificate[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_l1_bound"
            ]
        ):
            raise AssertionError((p, n, two_coordinate_projective_split, certificate))
        if three_coordinate_kummer_l1_bound != int(
            certificate["three_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, three_coordinate_kummer_l1_bound))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if int(certificate["quadratic_one_coordinate_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["one_coordinate_kummer_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if (
            int(certificate["two_coordinate_infinity_unramified_error_constant"])
            != 2
        ):
            raise AssertionError((p, n, certificate))
        if (
            int(certificate["two_coordinate_infinity_unramified_sqrt_constant"])
            != 5
        ):
            raise AssertionError((p, n, certificate))
        if (
            int(certificate["two_coordinate_projective_reciprocal_error_constant"])
            != 4
        ):
            raise AssertionError((p, n, certificate))
        if (
            int(certificate["two_coordinate_projective_reciprocal_sqrt_constant"])
            != 3
        ):
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_equal_line_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_equal_line_sqrt_constant"]) != 3:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_coordinate_diagonal_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_coordinate_diagonal_sqrt_constant"]) != 3:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_projective_equal_pair_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_projective_equal_pair_sqrt_constant"]) != 3:
            raise AssertionError((p, n, certificate))
        if (
            int(
                certificate[
                    "two_coordinate_projective_asymmetric_nonresonant_"
                    "error_constant"
                ]
            )
            != 4
        ):
            raise AssertionError((p, n, certificate))
        if (
            int(
                certificate[
                    "two_coordinate_projective_asymmetric_nonresonant_"
                    "sqrt_constant"
                ]
            )
            != 3
        ):
            raise AssertionError((p, n, certificate))
        if (
            int(
                certificate[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "resonant_error_constant"
                ]
            )
            != 4
        ):
            raise AssertionError((p, n, certificate))
        if (
            int(
                certificate[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "resonant_sqrt_constant"
                ]
            )
            != 3
        ):
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_kummer_error_constant"]) != 9:
            raise AssertionError((p, n, certificate))
        if int(certificate["three_coordinate_kummer_error_constant"]) != int(
            certificate["nonprincipal_constant"]
        ):
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        equal_line_leading_l1_drop = 5 * two_coordinate_equal_line_l1_bound
        equal_line_conditional_weighted_error_l1_bound = (
            weighted_error_l1_bound - equal_line_leading_l1_drop
        )
        coordinate_diagonal_leading_l1_drop = (
            5 * two_coordinate_coordinate_diagonal_l1_bound
        )
        coordinate_diagonal_conditional_weighted_error_l1_bound = (
            weighted_error_l1_bound - coordinate_diagonal_leading_l1_drop
        )
        projective_equal_pair_leading_l1_drop = (
            5 * two_coordinate_projective_equal_pair_l1_bound
        )
        projective_equal_pair_conditional_weighted_error_l1_bound = (
            weighted_error_l1_bound - projective_equal_pair_leading_l1_drop
        )
        projective_asymmetric_nonresonant_leading_l1_drop = (
            5 * two_coordinate_projective_asymmetric_nonresonant_l1_bound
        )
        projective_equal_pair_nonresonant_weighted_error_l1_bound = (
            weighted_error_l1_bound
            - projective_equal_pair_leading_l1_drop
            - projective_asymmetric_nonresonant_leading_l1_drop
        )
        projective_asymmetric_line_conic_resonant_leading_l1_drop = (
            5 * two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound
        )
        projective_equal_pair_all_asymmetric_weighted_error_l1_bound = (
            weighted_error_l1_bound
            - projective_equal_pair_leading_l1_drop
            - projective_asymmetric_nonresonant_leading_l1_drop
            - projective_asymmetric_line_conic_resonant_leading_l1_drop
        )
        if equal_line_leading_l1_drop != int(
            certificate["two_coordinate_equal_line_leading_l1_drop"]
        ):
            raise AssertionError(
                (p, n, equal_line_leading_l1_drop, certificate)
            )
        if equal_line_conditional_weighted_error_l1_bound != int(
            certificate["equal_line_conditional_weighted_error_l1_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    equal_line_conditional_weighted_error_l1_bound,
                    certificate,
                )
            )
        if coordinate_diagonal_leading_l1_drop != int(
            certificate["two_coordinate_coordinate_diagonal_leading_l1_drop"]
        ):
            raise AssertionError(
                (p, n, coordinate_diagonal_leading_l1_drop, certificate)
            )
        if coordinate_diagonal_conditional_weighted_error_l1_bound != int(
            certificate["coordinate_diagonal_conditional_weighted_error_l1_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    coordinate_diagonal_conditional_weighted_error_l1_bound,
                    certificate,
                )
            )
        if projective_equal_pair_leading_l1_drop != int(
            certificate["two_coordinate_projective_equal_pair_leading_l1_drop"]
        ):
            raise AssertionError(
                (p, n, projective_equal_pair_leading_l1_drop, certificate)
            )
        if projective_equal_pair_conditional_weighted_error_l1_bound != int(
            certificate["projective_equal_pair_conditional_weighted_error_l1_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_conditional_weighted_error_l1_bound,
                    certificate,
                )
            )
        if projective_asymmetric_nonresonant_leading_l1_drop != int(
            certificate[
                "two_coordinate_projective_asymmetric_nonresonant_"
                "leading_l1_drop"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_asymmetric_nonresonant_leading_l1_drop,
                    certificate,
                )
            )
        if projective_asymmetric_line_conic_resonant_leading_l1_drop != int(
            certificate[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_leading_l1_drop"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_asymmetric_line_conic_resonant_leading_l1_drop,
                    certificate,
                )
            )
        if projective_equal_pair_nonresonant_weighted_error_l1_bound != int(
            certificate[
                "projective_equal_pair_nonresonant_conditional_"
                "weighted_error_l1_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_nonresonant_weighted_error_l1_bound,
                    certificate,
                )
            )
        if projective_equal_pair_all_asymmetric_weighted_error_l1_bound != int(
            certificate[
                "projective_equal_pair_all_asymmetric_conditional_"
                "weighted_error_l1_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_all_asymmetric_weighted_error_l1_bound,
                    certificate,
                )
            )
        elementary_open_sqrt_error_bound = (
            6 * ceil_sqrt(p) * (jacobi_l1_bound + conic_l1_bound)
        )
        infinity_unramified_sqrt_error_bound = (
            5
            * ceil_sqrt(p)
            * two_coordinate_infinity_unramified_l1_bound
        )
        projective_reciprocal_sqrt_error_bound = (
            3
            * ceil_sqrt(p)
            * two_coordinate_projective_reciprocal_l1_bound
        )
        if elementary_open_sqrt_error_bound != int(
            certificate["elementary_open_sqrt_error_bound"]
        ):
            raise AssertionError(
                (p, n, elementary_open_sqrt_error_bound, certificate)
            )
        if infinity_unramified_sqrt_error_bound != (
            ceil_sqrt(p)
            * int(
                certificate[
                    "two_coordinate_infinity_unramified_sqrt_l1_bound"
                ]
            )
        ):
            raise AssertionError(
                (p, n, infinity_unramified_sqrt_error_bound, certificate)
            )
        if projective_reciprocal_sqrt_error_bound != (
            ceil_sqrt(p)
            * int(
                certificate[
                    "two_coordinate_projective_reciprocal_sqrt_l1_bound"
                ]
            )
        ):
            raise AssertionError(
                (p, n, projective_reciprocal_sqrt_error_bound, certificate)
            )
        sqrt_error_bound = (
            elementary_open_sqrt_error_bound
            + infinity_unramified_sqrt_error_bound
            + projective_reciprocal_sqrt_error_bound
        )
        equal_line_sqrt_error_bound = (
            3 * ceil_sqrt(p) * two_coordinate_equal_line_l1_bound
        )
        equal_line_conditional_sqrt_error_bound = (
            sqrt_error_bound + equal_line_sqrt_error_bound
        )
        coordinate_diagonal_sqrt_error_bound = (
            3 * ceil_sqrt(p) * two_coordinate_coordinate_diagonal_l1_bound
        )
        coordinate_diagonal_conditional_sqrt_error_bound = (
            sqrt_error_bound + coordinate_diagonal_sqrt_error_bound
        )
        projective_equal_pair_sqrt_error_bound = (
            3 * ceil_sqrt(p) * two_coordinate_projective_equal_pair_l1_bound
        )
        projective_equal_pair_conditional_sqrt_error_bound = (
            sqrt_error_bound + projective_equal_pair_sqrt_error_bound
        )
        projective_asymmetric_nonresonant_sqrt_error_bound = (
            3
            * ceil_sqrt(p)
            * two_coordinate_projective_asymmetric_nonresonant_l1_bound
        )
        projective_equal_pair_nonresonant_conditional_sqrt_error_bound = (
            sqrt_error_bound
            + projective_equal_pair_sqrt_error_bound
            + projective_asymmetric_nonresonant_sqrt_error_bound
        )
        projective_asymmetric_line_conic_resonant_sqrt_error_bound = (
            3
            * ceil_sqrt(p)
            * two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound
        )
        projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound = (
            projective_equal_pair_nonresonant_conditional_sqrt_error_bound
            + projective_asymmetric_line_conic_resonant_sqrt_error_bound
        )
        if sqrt_error_bound != int(certificate["sqrt_error_bound"]):
            raise AssertionError((p, n, sqrt_error_bound, certificate))
        if equal_line_sqrt_error_bound != (
            ceil_sqrt(p)
            * int(certificate["two_coordinate_equal_line_sqrt_l1_bound"])
        ):
            raise AssertionError((p, n, equal_line_sqrt_error_bound, certificate))
        if coordinate_diagonal_sqrt_error_bound != (
            ceil_sqrt(p)
            * int(
                certificate[
                    "two_coordinate_coordinate_diagonal_sqrt_l1_bound"
                ]
            )
        ):
            raise AssertionError(
                (p, n, coordinate_diagonal_sqrt_error_bound, certificate)
            )
        if projective_equal_pair_sqrt_error_bound != (
            ceil_sqrt(p)
            * int(
                certificate[
                    "two_coordinate_projective_equal_pair_sqrt_l1_bound"
                ]
            )
        ):
            raise AssertionError(
                (p, n, projective_equal_pair_sqrt_error_bound, certificate)
            )
        if projective_asymmetric_nonresonant_sqrt_error_bound != (
            ceil_sqrt(p)
            * int(
                certificate[
                    "two_coordinate_projective_asymmetric_nonresonant_"
                    "sqrt_l1_bound"
                ]
            )
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_asymmetric_nonresonant_sqrt_error_bound,
                    certificate,
                )
            )
        if projective_asymmetric_line_conic_resonant_sqrt_error_bound != (
            ceil_sqrt(p)
            * int(
                certificate[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "resonant_sqrt_l1_bound"
                ]
            )
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_asymmetric_line_conic_resonant_sqrt_error_bound,
                    certificate,
                )
            )
        if equal_line_conditional_sqrt_error_bound != int(
            certificate["equal_line_conditional_sqrt_error_bound"]
        ):
            raise AssertionError(
                (p, n, equal_line_conditional_sqrt_error_bound, certificate)
            )
        if coordinate_diagonal_conditional_sqrt_error_bound != int(
            certificate["coordinate_diagonal_conditional_sqrt_error_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    coordinate_diagonal_conditional_sqrt_error_bound,
                    certificate,
                )
            )
        if projective_equal_pair_conditional_sqrt_error_bound != int(
            certificate["projective_equal_pair_conditional_sqrt_error_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_conditional_sqrt_error_bound,
                    certificate,
                )
            )
        if projective_equal_pair_nonresonant_conditional_sqrt_error_bound != int(
            certificate[
                "projective_equal_pair_nonresonant_conditional_"
                "sqrt_error_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_nonresonant_conditional_sqrt_error_bound,
                    certificate,
                )
            )
        if projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound != int(
            certificate[
                "projective_equal_pair_all_asymmetric_conditional_"
                "sqrt_error_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound,
                    certificate,
                )
            )
        weighted_error_total_bound = (
            p * weighted_error_l1_bound + sqrt_error_bound
        )
        equal_line_conditional_weighted_error_total_bound = (
            p * equal_line_conditional_weighted_error_l1_bound
            + equal_line_conditional_sqrt_error_bound
        )
        coordinate_diagonal_conditional_weighted_error_total_bound = (
            p * coordinate_diagonal_conditional_weighted_error_l1_bound
            + coordinate_diagonal_conditional_sqrt_error_bound
        )
        projective_equal_pair_conditional_weighted_error_total_bound = (
            p * projective_equal_pair_conditional_weighted_error_l1_bound
            + projective_equal_pair_conditional_sqrt_error_bound
        )
        projective_equal_pair_nonresonant_weighted_error_total_bound = (
            p * projective_equal_pair_nonresonant_weighted_error_l1_bound
            + projective_equal_pair_nonresonant_conditional_sqrt_error_bound
        )
        projective_equal_pair_all_asymmetric_weighted_error_total_bound = (
            p * projective_equal_pair_all_asymmetric_weighted_error_l1_bound
            + projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound
        )
        if weighted_error_total_bound != int(
            certificate["weighted_error_total_bound"]
        ):
            raise AssertionError(
                (p, n, weighted_error_total_bound, certificate)
            )
        if equal_line_conditional_weighted_error_total_bound != int(
            certificate["equal_line_conditional_weighted_error_total_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    equal_line_conditional_weighted_error_total_bound,
                    certificate,
                )
            )
        if coordinate_diagonal_conditional_weighted_error_total_bound != int(
            certificate[
                "coordinate_diagonal_conditional_weighted_error_total_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    coordinate_diagonal_conditional_weighted_error_total_bound,
                    certificate,
                )
            )
        if projective_equal_pair_conditional_weighted_error_total_bound != int(
            certificate[
                "projective_equal_pair_conditional_weighted_error_total_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_conditional_weighted_error_total_bound,
                    certificate,
                )
            )
        if projective_equal_pair_nonresonant_weighted_error_total_bound != int(
            certificate[
                "projective_equal_pair_nonresonant_conditional_"
                "weighted_error_total_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_nonresonant_weighted_error_total_bound,
                    certificate,
                )
            )
        if projective_equal_pair_all_asymmetric_weighted_error_total_bound != int(
            certificate[
                "projective_equal_pair_all_asymmetric_conditional_"
                "weighted_error_total_bound"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_all_asymmetric_weighted_error_total_bound,
                    certificate,
                )
            )
        lower_numerator = principal_count - (
            p * weighted_error_l1_bound
            + sqrt_error_bound
            + degeneracy_count * int(certificate["denominator"])
        )
        equal_line_conditional_lower_numerator = principal_count - (
            p * equal_line_conditional_weighted_error_l1_bound
            + equal_line_conditional_sqrt_error_bound
            + degeneracy_count * int(certificate["denominator"])
        )
        coordinate_diagonal_conditional_lower_numerator = principal_count - (
            p * coordinate_diagonal_conditional_weighted_error_l1_bound
            + coordinate_diagonal_conditional_sqrt_error_bound
            + degeneracy_count * int(certificate["denominator"])
        )
        projective_equal_pair_conditional_lower_numerator = principal_count - (
            p * projective_equal_pair_conditional_weighted_error_l1_bound
            + projective_equal_pair_conditional_sqrt_error_bound
            + degeneracy_count * int(certificate["denominator"])
        )
        projective_equal_pair_nonresonant_lower_numerator = principal_count - (
            p * projective_equal_pair_nonresonant_weighted_error_l1_bound
            + projective_equal_pair_nonresonant_conditional_sqrt_error_bound
            + degeneracy_count * int(certificate["denominator"])
        )
        projective_equal_pair_all_asymmetric_lower_numerator = principal_count - (
            p * projective_equal_pair_all_asymmetric_weighted_error_l1_bound
            + projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound
            + degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        if equal_line_conditional_lower_numerator != int(
            certificate["equal_line_conditional_lower_numerator"]
        ):
            raise AssertionError(
                (p, n, equal_line_conditional_lower_numerator, certificate)
            )
        if coordinate_diagonal_conditional_lower_numerator != int(
            certificate["coordinate_diagonal_conditional_lower_numerator"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    coordinate_diagonal_conditional_lower_numerator,
                    certificate,
                )
            )
        if projective_equal_pair_conditional_lower_numerator != int(
            certificate["projective_equal_pair_conditional_lower_numerator"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_conditional_lower_numerator,
                    certificate,
                )
            )
        if projective_equal_pair_nonresonant_lower_numerator != int(
            certificate[
                "projective_equal_pair_nonresonant_conditional_"
                "lower_numerator"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_nonresonant_lower_numerator,
                    certificate,
                )
            )
        if projective_equal_pair_all_asymmetric_lower_numerator != int(
            certificate[
                "projective_equal_pair_all_asymmetric_conditional_"
                "lower_numerator"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_all_asymmetric_lower_numerator,
                    certificate,
                )
            )
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            1,
            (
                weighted_error_l1_bound
                + int(certificate["degeneracy_line_count"])
                * int(certificate["denominator"])
            ),
            sqrt_error_weight=int(certificate["sqrt_error_weight"]),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        equal_line_conditional_expected_threshold = (
            kummer_quadratic_uniform_prime_threshold(
                1,
                (
                    equal_line_conditional_weighted_error_l1_bound
                    + int(certificate["degeneracy_line_count"])
                    * int(certificate["denominator"])
                ),
                sqrt_error_weight=int(
                    certificate["equal_line_conditional_sqrt_error_weight"]
                ),
            )
        )
        if equal_line_conditional_expected_threshold != int(
            certificate["equal_line_conditional_uniform_prime_threshold"]
        ):
            raise AssertionError(
                (p, n, equal_line_conditional_expected_threshold, certificate)
            )
        coordinate_diagonal_conditional_expected_threshold = (
            kummer_quadratic_uniform_prime_threshold(
                1,
                (
                    coordinate_diagonal_conditional_weighted_error_l1_bound
                    + int(certificate["degeneracy_line_count"])
                    * int(certificate["denominator"])
                ),
                sqrt_error_weight=int(
                    certificate[
                        "coordinate_diagonal_conditional_sqrt_error_weight"
                    ]
                ),
            )
        )
        if coordinate_diagonal_conditional_expected_threshold != int(
            certificate[
                "coordinate_diagonal_conditional_uniform_prime_threshold"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    coordinate_diagonal_conditional_expected_threshold,
                    certificate,
                )
            )
        projective_equal_pair_conditional_expected_threshold = (
            kummer_quadratic_uniform_prime_threshold(
                1,
                (
                    projective_equal_pair_conditional_weighted_error_l1_bound
                    + int(certificate["degeneracy_line_count"])
                    * int(certificate["denominator"])
                ),
                sqrt_error_weight=int(
                    certificate[
                        "projective_equal_pair_conditional_sqrt_error_weight"
                    ]
                ),
            )
        )
        if projective_equal_pair_conditional_expected_threshold != int(
            certificate[
                "projective_equal_pair_conditional_uniform_prime_threshold"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_conditional_expected_threshold,
                    certificate,
                )
            )
        projective_equal_pair_nonresonant_expected_threshold = (
            kummer_quadratic_uniform_prime_threshold(
                1,
                (
                    projective_equal_pair_nonresonant_weighted_error_l1_bound
                    + int(certificate["degeneracy_line_count"])
                    * int(certificate["denominator"])
                ),
                sqrt_error_weight=int(
                    certificate[
                        "projective_equal_pair_nonresonant_conditional_"
                        "sqrt_error_weight"
                    ]
                ),
            )
        )
        if projective_equal_pair_nonresonant_expected_threshold != int(
            certificate[
                "projective_equal_pair_nonresonant_conditional_"
                "uniform_prime_threshold"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_nonresonant_expected_threshold,
                    certificate,
                )
            )
        projective_equal_pair_all_asymmetric_expected_threshold = (
            kummer_quadratic_uniform_prime_threshold(
                1,
                (
                    projective_equal_pair_all_asymmetric_weighted_error_l1_bound
                    + int(certificate["degeneracy_line_count"])
                    * int(certificate["denominator"])
                ),
                sqrt_error_weight=int(
                    certificate[
                        "projective_equal_pair_all_asymmetric_conditional_"
                        "sqrt_error_weight"
                    ]
                ),
            )
        )
        if projective_equal_pair_all_asymmetric_expected_threshold != int(
            certificate[
                "projective_equal_pair_all_asymmetric_conditional_"
                "uniform_prime_threshold"
            ]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    projective_equal_pair_all_asymmetric_expected_threshold,
                    certificate,
                )
            )
        nonzero_coset_count, total_coset_count = square_coset_counts(p, domain)
        saturates = nonzero_coset_count == total_coset_count
        certificate_positive = bool(certificate["saturation_certificate"])
        equal_line_conditional_certificate_positive = bool(
            certificate["equal_line_conditional_saturation_certificate"]
        )
        coordinate_diagonal_conditional_certificate_positive = bool(
            certificate["coordinate_diagonal_conditional_saturation_certificate"]
        )
        projective_equal_pair_conditional_certificate_positive = bool(
            certificate["projective_equal_pair_conditional_saturation_certificate"]
        )
        projective_equal_pair_nonresonant_certificate_positive = bool(
            certificate[
                "projective_equal_pair_nonresonant_conditional_"
                "saturation_certificate"
            ]
        )
        projective_equal_pair_all_asymmetric_certificate_positive = bool(
            certificate[
                "projective_equal_pair_all_asymmetric_conditional_"
                "saturation_certificate"
            ]
        )
        if certificate_positive != expected_certificate:
            raise AssertionError((p, n, certificate))
        if bool(certificate["uniform_threshold_applies"]) != certificate_positive:
            raise AssertionError((p, n, certificate))
        if bool(
            certificate["equal_line_conditional_uniform_threshold_applies"]
        ) != equal_line_conditional_certificate_positive:
            raise AssertionError((p, n, certificate))
        if bool(
            certificate[
                "coordinate_diagonal_conditional_uniform_threshold_applies"
            ]
        ) != coordinate_diagonal_conditional_certificate_positive:
            raise AssertionError((p, n, certificate))
        if bool(
            certificate[
                "projective_equal_pair_conditional_uniform_threshold_applies"
            ]
        ) != projective_equal_pair_conditional_certificate_positive:
            raise AssertionError((p, n, certificate))
        if bool(
            certificate[
                "projective_equal_pair_nonresonant_conditional_"
                "uniform_threshold_applies"
            ]
        ) != projective_equal_pair_nonresonant_certificate_positive:
            raise AssertionError((p, n, certificate))
        if bool(
            certificate[
                "projective_equal_pair_all_asymmetric_conditional_"
                "uniform_threshold_applies"
            ]
        ) != projective_equal_pair_all_asymmetric_certificate_positive:
            raise AssertionError((p, n, certificate))
        if certificate_positive and not equal_line_conditional_certificate_positive:
            raise AssertionError((p, n, certificate))
        if (
            equal_line_conditional_certificate_positive
            and not coordinate_diagonal_conditional_certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        if (
            coordinate_diagonal_conditional_certificate_positive
            and not projective_equal_pair_conditional_certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        if (
            projective_equal_pair_conditional_certificate_positive
            and not projective_equal_pair_nonresonant_certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        if (
            projective_equal_pair_nonresonant_certificate_positive
            and not projective_equal_pair_all_asymmetric_certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        if certificate_positive and not saturates:
            raise AssertionError((p, n, nonzero_coset_count, total_coset_count))
        checked.append(
            (
                p,
                n,
                certificate_positive,
                certificate["uniform_prime_threshold"],
                failures,
                radical_total,
                deligne_constant,
                principal_count,
                degeneracy_count,
                nonzero_coset_count,
                total_coset_count,
            )
        )
    equal_line_checked = []
    for character_order, square_coset_index in EQUAL_LINE_SPLIT_CASES:
        direct_split = raw_two_coordinate_projective_l1_split(
            character_order,
            square_coset_index,
        )
        formula_split = raw_two_coordinate_projective_l1_split_formula(
            character_order,
            square_coset_index,
        )
        if direct_split != formula_split:
            raise AssertionError((character_order, square_coset_index, direct_split))
        equal_line_l1 = int(direct_split["equal_line_diagonal"])
        coordinate_diagonal_l1 = int(direct_split["coordinate_diagonal"])
        coordinate_diagonal_non_equal_l1 = int(
            direct_split["coordinate_diagonal_non_equal"]
        )
        projective_equal_pair_l1 = int(direct_split["projective_equal_pair"])
        projective_equal_pair_non_coordinate_l1 = int(
            direct_split["projective_equal_pair_non_coordinate"]
        )
        projective_asymmetric_l1 = int(direct_split["projective_asymmetric"])
        projective_asymmetric_orbit_count = int(
            direct_split["projective_asymmetric_orbit_count"]
        )
        line_conic_resonant_l1 = int(
            direct_split["projective_asymmetric_line_conic_resonant"]
        )
        line_conic_nonresonant_l1 = int(
            direct_split["projective_asymmetric_line_conic_nonresonant"]
        )
        line_conic_resonant_orbit_count = int(
            direct_split[
                "projective_asymmetric_line_conic_resonant_orbit_count"
            ]
        )
        line_conic_nonresonant_orbit_count = int(
            direct_split[
                "projective_asymmetric_line_conic_nonresonant_orbit_count"
            ]
        )
        ramified_l1 = int(direct_split["ramified_nonreciprocal"])
        if equal_line_l1 > ramified_l1:
            raise AssertionError((character_order, square_coset_index, direct_split))
        if not equal_line_l1 <= coordinate_diagonal_l1 <= ramified_l1:
            raise AssertionError((character_order, square_coset_index, direct_split))
        if coordinate_diagonal_non_equal_l1 != (
            coordinate_diagonal_l1 - equal_line_l1
        ):
            raise AssertionError((character_order, square_coset_index, direct_split))
        if not coordinate_diagonal_l1 <= projective_equal_pair_l1 <= ramified_l1:
            raise AssertionError((character_order, square_coset_index, direct_split))
        if projective_equal_pair_non_coordinate_l1 != (
            projective_equal_pair_l1 - coordinate_diagonal_l1
        ):
            raise AssertionError((character_order, square_coset_index, direct_split))
        if projective_asymmetric_l1 != ramified_l1 - projective_equal_pair_l1:
            raise AssertionError((character_order, square_coset_index, direct_split))
        if projective_asymmetric_l1 != 6 * projective_asymmetric_orbit_count:
            raise AssertionError((character_order, square_coset_index, direct_split))
        if projective_asymmetric_l1 != (
            line_conic_resonant_l1 + line_conic_nonresonant_l1
        ):
            raise AssertionError((character_order, square_coset_index, direct_split))
        if line_conic_resonant_l1 != 6 * line_conic_resonant_orbit_count:
            raise AssertionError((character_order, square_coset_index, direct_split))
        if line_conic_nonresonant_l1 != 6 * line_conic_nonresonant_orbit_count:
            raise AssertionError((character_order, square_coset_index, direct_split))
        equal_line_checked.append(
            (
                character_order,
                square_coset_index,
                coordinate_diagonal_l1,
                coordinate_diagonal_non_equal_l1,
                projective_equal_pair_l1,
                projective_equal_pair_non_coordinate_l1,
                projective_asymmetric_l1,
                projective_asymmetric_orbit_count,
                line_conic_resonant_l1,
                line_conic_nonresonant_l1,
                line_conic_resonant_orbit_count,
                line_conic_nonresonant_orbit_count,
                equal_line_l1,
                ramified_l1,
                5 * equal_line_l1,
                3 * equal_line_l1,
                5 * coordinate_diagonal_l1,
                3 * coordinate_diagonal_l1,
                5 * projective_equal_pair_l1,
                3 * projective_equal_pair_l1,
            )
        )
    lift_checked = []
    for p, n, quotient_order, fiber_size, support_size, expected_gate in LIFT_CASES:
        _, domain = make_domain(p, n, None)
        gate, remaining_fibers, required_fibers = all_residual_packets_lift_active(
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            residual_size=4,
        )
        if gate != expected_gate:
            raise AssertionError(
                (p, n, quotient_order, fiber_size, support_size, gate)
            )
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if gate:
            if int(ledger["active_parameter_count"]) != int(
                ledger["parameter_count"]
            ):
                raise AssertionError((p, n, support_size, ledger))
            if int(ledger["active_nonzero_square_coset_count"]) != int(
                ledger["nonzero_square_coset_count"]
            ):
                raise AssertionError((p, n, support_size, ledger))
        lift_checked.append(
            (
                p,
                n,
                quotient_order,
                fiber_size,
                support_size,
                gate,
                remaining_fibers,
                required_fibers,
            )
        )
    lift_bound_checked = []
    for (
        p,
        n,
        quotient_order,
        fiber_size,
        support_size,
        expected_nontrivial,
    ) in LIFT_BOUND_CASES:
        _, domain = make_domain(p, n, None)
        whole_fibers = (support_size - 4) // fiber_size
        remaining_fibers = quotient_order - whole_fibers
        direct_bound = lift_limited_bound_formula(
            quotient_order,
            fiber_size,
            remaining_fibers,
        )
        helper_bound = quotient_limited_pair_parameter_bound(
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            remaining_fibers=remaining_fibers,
            residual_size=4,
        )
        if direct_bound != helper_bound:
            raise AssertionError((p, n, support_size, direct_bound, helper_bound))
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if int(ledger["lift_limited_parameter_bound"]) != direct_bound:
            raise AssertionError((p, n, support_size, ledger))
        slope_count = len(ledger["support_slope_histogram"])
        slope_bound = int(ledger["lift_limited_slope_bound"])
        if slope_count > slope_bound:
            raise AssertionError((p, n, support_size, slope_count, ledger))
        if bool(ledger["lift_limited_slope_bound_nontrivial"]) != (
            expected_nontrivial
        ):
            raise AssertionError((p, n, support_size, ledger))
        lift_bound_checked.append(
            (
                p,
                n,
                quotient_order,
                fiber_size,
                support_size,
                remaining_fibers,
                direct_bound,
                slope_count,
                slope_bound,
            )
        )
    kernel_checked = []
    for p, n, quotient_order, fiber_size, support_size in KERNEL_REDUCTION_CASES:
        _, domain = make_domain(p, n, None)
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        reduction = ledger["kernel_fiber_reduction"]
        if reduction is None:
            raise AssertionError((p, n, support_size, ledger))
        expected = kernel_fiber_reduction_counts(p, domain, quotient_order)
        observed = (
            int(reduction["kernel_order"]),
            int(reduction["parameter_count"]),
            int(reduction["zero_parameter_count"]),
            int(reduction["nonzero_square_coset_count"]),
            int(reduction["slope_count"]),
        )
        if observed != expected:
            raise AssertionError((p, n, support_size, observed, expected))
        if int(reduction["parameter_count"]) != int(
            ledger["active_parameter_count"]
        ):
            raise AssertionError((p, n, support_size, ledger))
        if int(reduction["zero_parameter_count"]) != int(
            ledger["active_zero_parameter_count"]
        ):
            raise AssertionError((p, n, support_size, ledger))
        if int(reduction["nonzero_square_coset_count"]) != int(
            ledger["active_nonzero_square_coset_count"]
        ):
            raise AssertionError((p, n, support_size, ledger))
        if int(reduction["slope_count"]) != len(ledger["support_slope_histogram"]):
            raise AssertionError((p, n, support_size, ledger))
        kernel_checked.append(
            (p, n, quotient_order, fiber_size, support_size, *observed)
        )
    two_fiber_checked = []
    for p, n, quotient_order, expected_certificate in TWO_FIBER_KUMMER_CASES:
        _, domain = make_domain(p, n, None)
        certificate = slack_two_second_two_fiber_kummer_saturation_data(
            p,
            n,
            quotient_order,
        )
        if certificate is None:
            raise AssertionError((p, n, quotient_order))
        failures = two_fiber_divisor_power_failure_count(
            int(certificate["kernel_character_order"]),
            int(certificate["square_coset_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        deligne_constant = (radical_total - 1) ** 2
        if deligne_constant != int(certificate["deligne_constant"]):
            raise AssertionError((p, n, deligne_constant, certificate))
        principal_count = principal_open_count(p)
        degeneracy_count = degeneracy_line_union_count(p)
        square_coset_index = int(certificate["square_coset_index"])
        window_size = 2
        active_character_l1_bound = fixed_window_parseval_active_l1_bound(
            quotient_order,
            window_size,
            int(certificate["ambient_restriction_kernel_count"]),
        )
        if active_character_l1_bound != int(
            certificate["window_one_dimensional_l1_bound"]
        ):
            raise AssertionError((p, n, active_character_l1_bound, certificate))
        coordinate_nonprincipal_l1_bound = (
            (window_size + active_character_l1_bound) ** 3
            - int(certificate["principal_weight"])
        )
        coefficient_l1_bound = (
            square_coset_index
            * (
                int(certificate["principal_weight"])
                + coordinate_nonprincipal_l1_bound
            )
            - int(certificate["principal_weight"])
        )
        if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        jacobi_l1_bound = coordinate_nonprincipal_l1_bound
        conic_l1_bound = int(certificate["principal_weight"]) * (
            square_coset_index - 1
        )
        quadratic_conic_character_count = (
            1 if square_coset_index > 1 and square_coset_index % 2 == 0 else 0
        )
        coordinate_one_l1_bound = (
            3 * window_size * window_size * active_character_l1_bound
        )
        coordinate_two_l1_bound = (
            3 * window_size * active_character_l1_bound ** 2
        )
        coordinate_three_l1_bound = active_character_l1_bound ** 3
        quadratic_one_coordinate_l1_bound = (
            coordinate_one_l1_bound * quadratic_conic_character_count
        )
        one_coordinate_kummer_l1_bound = coordinate_one_l1_bound * (
            square_coset_index - 1 - quadratic_conic_character_count
        )
        two_coordinate_kummer_l1_bound = (
            coordinate_two_l1_bound * (square_coset_index - 1)
        )
        three_coordinate_kummer_l1_bound = (
            coordinate_three_l1_bound * (square_coset_index - 1)
        )
        kummer_l1_bound = (
            one_coordinate_kummer_l1_bound
            + two_coordinate_kummer_l1_bound
            + three_coordinate_kummer_l1_bound
        )
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["quadratic_one_coordinate_error_constant"])
            * quadratic_one_coordinate_l1_bound
            + int(certificate["one_coordinate_kummer_error_constant"])
            * one_coordinate_kummer_l1_bound
            + int(certificate["two_coordinate_kummer_error_constant"])
            * two_coordinate_kummer_l1_bound
            + int(certificate["three_coordinate_kummer_error_constant"])
            * three_coordinate_kummer_l1_bound
        )
        if (
            jacobi_l1_bound
            + conic_l1_bound
            + quadratic_one_coordinate_l1_bound
            + kummer_l1_bound
            != coefficient_l1_bound
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if quadratic_one_coordinate_l1_bound != int(
            certificate["quadratic_one_coordinate_l1_bound"]
        ):
            raise AssertionError(
                (p, n, quadratic_one_coordinate_l1_bound, certificate)
            )
        if one_coordinate_kummer_l1_bound != int(
            certificate["one_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, one_coordinate_kummer_l1_bound))
        if two_coordinate_kummer_l1_bound != int(
            certificate["two_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, two_coordinate_kummer_l1_bound))
        if three_coordinate_kummer_l1_bound != int(
            certificate["three_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, three_coordinate_kummer_l1_bound))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if int(certificate["quadratic_one_coordinate_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["one_coordinate_kummer_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_kummer_error_constant"]) != 9:
            raise AssertionError((p, n, certificate))
        if int(certificate["three_coordinate_kummer_error_constant"]) != int(
            certificate["nonprincipal_constant"]
        ):
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        elementary_open_sqrt_error_bound = (
            6 * ceil_sqrt(p) * (jacobi_l1_bound + conic_l1_bound)
        )
        if elementary_open_sqrt_error_bound != int(
            certificate["elementary_open_sqrt_error_bound"]
        ):
            raise AssertionError(
                (p, n, elementary_open_sqrt_error_bound, certificate)
            )
        weighted_error_total_bound = (
            p * weighted_error_l1_bound + elementary_open_sqrt_error_bound
        )
        if weighted_error_total_bound != int(
            certificate["weighted_error_total_bound"]
        ):
            raise AssertionError(
                (p, n, weighted_error_total_bound, certificate)
            )
        lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * weighted_error_l1_bound
            - elementary_open_sqrt_error_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            int(certificate["principal_weight"]),
            (
                weighted_error_l1_bound
                + int(certificate["degeneracy_line_count"])
                * int(certificate["denominator"])
            ),
            sqrt_error_weight=6 * (jacobi_l1_bound + conic_l1_bound),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        certificate_positive = bool(certificate["saturation_certificate"])
        if certificate_positive != expected_certificate:
            raise AssertionError((p, n, certificate))
        if (
            bool(certificate["uniform_threshold_applies"])
            and not certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        window = slack_two_second_two_fiber_window_data(
            p,
            domain,
            quotient_order,
        )
        if window is None:
            raise AssertionError((p, n, quotient_order))
        window_saturates = int(window["nonzero_square_coset_count"]) == int(
            window["total_nonzero_square_coset_count"]
        )
        if certificate_positive and not window_saturates:
            raise AssertionError((p, n, certificate, window))
        two_fiber_checked.append(
            (
                p,
                n,
                quotient_order,
                certificate_positive,
                certificate["kernel_character_order"],
                certificate["square_coset_index"],
                certificate["denominator"],
                certificate["uniform_prime_threshold"],
                window["parameter_count"],
                window["zero_parameter_count"],
                window["nonzero_square_coset_count"],
                window["total_nonzero_square_coset_count"],
            )
        )
    two_fiber_union_checked = []
    for p, n, quotient_order, fiber_size, support_size in TWO_FIBER_UNION_CASES:
        _, domain = make_domain(p, n, None)
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        reduction = slack_two_second_two_fiber_union_reduction_data(
            p,
            domain,
            quotient_order,
        )
        if reduction is None:
            raise AssertionError((p, n, quotient_order))
        remaining_fibers = int(ledger["lift_limited_remaining_fibers"])
        if remaining_fibers != 2:
            raise AssertionError((p, n, support_size, ledger))
        observed = (
            int(reduction["parameter_count"]),
            int(reduction["zero_parameter_count"]),
            int(reduction["nonzero_square_coset_count"]),
            int(reduction["slope_count"]),
        )
        expected = (
            int(ledger["active_parameter_count"]),
            int(ledger["active_zero_parameter_count"]),
            int(ledger["active_nonzero_square_coset_count"]),
            len(ledger["support_slope_histogram"]),
        )
        if observed != expected:
            raise AssertionError((p, n, support_size, observed, expected))
        if not bool(reduction["saturates_nonzero_square_cosets"]):
            raise AssertionError((p, n, support_size, reduction))
        per_window_cosets = tuple(
            int(profile["nonzero_square_coset_count"])
            for profile in reduction["per_window_profiles"]
        )
        if max(per_window_cosets) >= int(
            reduction["total_nonzero_square_coset_count"]
        ):
            raise AssertionError((p, n, support_size, reduction))
        two_fiber_union_checked.append(
            (
                p,
                n,
                quotient_order,
                support_size,
                remaining_fibers,
                *observed,
                per_window_cosets,
            )
        )
    r_window_checked = []
    for (
        p,
        n,
        quotient_order,
        fiber_size,
        support_size,
        expected_saturation,
    ) in R_WINDOW_CASES:
        _, domain = make_domain(p, n, None)
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        reduction = slack_two_second_quotient_window_reduction_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
            remaining_fibers=int(ledger["lift_limited_remaining_fibers"]),
        )
        if reduction is None:
            raise AssertionError((p, n, support_size))
        observed = (
            int(reduction["parameter_count"]),
            int(reduction["zero_parameter_count"]),
            int(reduction["nonzero_square_coset_count"]),
            int(reduction["slope_count"]),
        )
        expected = (
            int(ledger["active_parameter_count"]),
            int(ledger["active_zero_parameter_count"]),
            int(ledger["active_nonzero_square_coset_count"]),
            len(ledger["support_slope_histogram"]),
        )
        if observed != expected:
            raise AssertionError((p, n, support_size, observed, expected))
        saturates = bool(reduction["saturates_nonzero_square_cosets"])
        if saturates != expected_saturation:
            raise AssertionError((p, n, support_size, reduction))
        r_window_checked.append(
            (
                p,
                n,
                quotient_order,
                support_size,
                reduction["remaining_fibers"],
                reduction["effective_window_size"],
                *observed,
                tuple(reduction["touched_fiber_histogram"]),
            )
        )
    fixed_window_kummer_checked = []
    for (
        p,
        n,
        quotient_order,
        window_size,
        expected_certificate,
    ) in FIXED_WINDOW_KUMMER_CASES:
        _, domain = make_domain(p, n, None)
        certificate = slack_two_second_fixed_window_kummer_saturation_data(
            p=p,
            domain_order=n,
            quotient_order=quotient_order,
            window_size=window_size,
        )
        if certificate is None:
            raise AssertionError((p, n, quotient_order, window_size))
        failures = two_fiber_divisor_power_failure_count(
            int(certificate["kernel_character_order"]),
            int(certificate["square_coset_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        principal_count = principal_open_count(p)
        degeneracy_count = degeneracy_line_union_count(p)
        square_coset_index = int(certificate["square_coset_index"])
        active_character_l1_bound = fixed_window_parseval_active_l1_bound(
            quotient_order,
            window_size,
            int(certificate["ambient_restriction_kernel_count"]),
        )
        if active_character_l1_bound != int(
            certificate["window_one_dimensional_l1_bound"]
        ):
            raise AssertionError((p, n, active_character_l1_bound, certificate))
        coordinate_nonprincipal_l1_bound = (
            (window_size + active_character_l1_bound) ** 3
            - int(certificate["principal_weight"])
        )
        coefficient_l1_bound = (
            square_coset_index
            * (
                int(certificate["principal_weight"])
                + coordinate_nonprincipal_l1_bound
            )
            - int(certificate["principal_weight"])
        )
        if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        jacobi_l1_bound = coordinate_nonprincipal_l1_bound
        conic_l1_bound = int(certificate["principal_weight"]) * (
            square_coset_index - 1
        )
        quadratic_conic_character_count = (
            1 if square_coset_index > 1 and square_coset_index % 2 == 0 else 0
        )
        coordinate_one_l1_bound = (
            3 * window_size * window_size * active_character_l1_bound
        )
        coordinate_two_l1_bound = (
            3 * window_size * active_character_l1_bound ** 2
        )
        coordinate_three_l1_bound = active_character_l1_bound ** 3
        quadratic_one_coordinate_l1_bound = (
            coordinate_one_l1_bound * quadratic_conic_character_count
        )
        one_coordinate_kummer_l1_bound = coordinate_one_l1_bound * (
            square_coset_index - 1 - quadratic_conic_character_count
        )
        two_coordinate_kummer_l1_bound = (
            coordinate_two_l1_bound * (square_coset_index - 1)
        )
        three_coordinate_kummer_l1_bound = (
            coordinate_three_l1_bound * (square_coset_index - 1)
        )
        kummer_l1_bound = (
            one_coordinate_kummer_l1_bound
            + two_coordinate_kummer_l1_bound
            + three_coordinate_kummer_l1_bound
        )
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["quadratic_one_coordinate_error_constant"])
            * quadratic_one_coordinate_l1_bound
            + int(certificate["one_coordinate_kummer_error_constant"])
            * one_coordinate_kummer_l1_bound
            + int(certificate["two_coordinate_kummer_error_constant"])
            * two_coordinate_kummer_l1_bound
            + int(certificate["three_coordinate_kummer_error_constant"])
            * three_coordinate_kummer_l1_bound
        )
        if (
            jacobi_l1_bound
            + conic_l1_bound
            + quadratic_one_coordinate_l1_bound
            + kummer_l1_bound
            != coefficient_l1_bound
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if quadratic_one_coordinate_l1_bound != int(
            certificate["quadratic_one_coordinate_l1_bound"]
        ):
            raise AssertionError(
                (p, n, quadratic_one_coordinate_l1_bound, certificate)
            )
        if one_coordinate_kummer_l1_bound != int(
            certificate["one_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, one_coordinate_kummer_l1_bound))
        if two_coordinate_kummer_l1_bound != int(
            certificate["two_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, two_coordinate_kummer_l1_bound))
        if three_coordinate_kummer_l1_bound != int(
            certificate["three_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, three_coordinate_kummer_l1_bound))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if int(certificate["quadratic_one_coordinate_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["one_coordinate_kummer_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_kummer_error_constant"]) != 9:
            raise AssertionError((p, n, certificate))
        if int(certificate["three_coordinate_kummer_error_constant"]) != int(
            certificate["nonprincipal_constant"]
        ):
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        elementary_open_sqrt_error_bound = (
            6 * ceil_sqrt(p) * (jacobi_l1_bound + conic_l1_bound)
        )
        if elementary_open_sqrt_error_bound != int(
            certificate["elementary_open_sqrt_error_bound"]
        ):
            raise AssertionError(
                (p, n, elementary_open_sqrt_error_bound, certificate)
            )
        weighted_error_total_bound = (
            p * weighted_error_l1_bound + elementary_open_sqrt_error_bound
        )
        if weighted_error_total_bound != int(
            certificate["weighted_error_total_bound"]
        ):
            raise AssertionError(
                (p, n, weighted_error_total_bound, certificate)
            )
        lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * weighted_error_l1_bound
            - elementary_open_sqrt_error_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            int(certificate["principal_weight"]),
            (
                weighted_error_l1_bound
                + 6 * int(certificate["denominator"])
            ),
            sqrt_error_weight=6 * (jacobi_l1_bound + conic_l1_bound),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        certificate_positive = bool(certificate["saturation_certificate"])
        if certificate_positive != expected_certificate:
            raise AssertionError((p, n, certificate))
        if (
            bool(certificate["uniform_threshold_applies"])
            and not certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        window = slack_two_second_fixed_window_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
            window_fibers=tuple(range(window_size)),
        )
        if window is None:
            raise AssertionError((p, n, quotient_order, window_size))
        window_saturates = int(window["nonzero_square_coset_count"]) == int(
            window["total_nonzero_square_coset_count"]
        )
        if certificate_positive and not window_saturates:
            raise AssertionError((p, n, certificate, window))
        fixed_window_kummer_checked.append(
            (
                p,
                n,
                quotient_order,
                window_size,
                certificate_positive,
                certificate["kernel_character_order"],
                certificate["square_coset_index"],
                certificate["denominator"],
                certificate["uniform_prime_threshold"],
                window["parameter_count"],
                window["zero_parameter_count"],
                window["nonzero_square_coset_count"],
                window["total_nonzero_square_coset_count"],
            )
        )
    r_window_union_kummer_checked = []
    for (
        p,
        n,
        quotient_order,
        remaining_fibers,
        expected_union_certificate,
        expected_fixed_certificate,
    ) in R_WINDOW_UNION_KUMMER_CASES:
        _, domain = make_domain(p, n, None)
        label_triples = quotient_window_label_triple_count(
            quotient_order,
            remaining_fibers,
        )
        direct_label_triples = direct_quotient_window_label_triple_count(
            quotient_order,
            remaining_fibers,
        )
        if label_triples != direct_label_triples:
            raise AssertionError(
                (p, n, quotient_order, label_triples, direct_label_triples)
            )
        coefficient_bound = quotient_window_label_nonprincipal_bound(
            quotient_order,
            remaining_fibers,
        )
        direct_coefficient_bound = (
            direct_quotient_window_label_nonprincipal_bound(
                quotient_order,
                remaining_fibers,
            )
        )
        if coefficient_bound != direct_coefficient_bound:
            raise AssertionError(
                (
                    p,
                    n,
                    quotient_order,
                    coefficient_bound,
                    direct_coefficient_bound,
                )
            )
        quotient_l1 = quotient_window_label_l1_data(
            quotient_order,
            remaining_fibers,
        )
        (
            direct_quotient_l1,
            direct_zero_subset_histogram,
            direct_coefficient_histogram,
        ) = (
            direct_quotient_window_label_l1_data(
                quotient_order,
                remaining_fibers,
            )
        )
        if bool(quotient_l1["exact"]):
            if int(quotient_l1["l1_bound"]) != direct_quotient_l1:
                raise AssertionError((p, n, quotient_l1, direct_quotient_l1))
            if quotient_l1.get("zero_subset_count_histogram") is not None:
                expected_histogram = tuple(
                    (count, multiplicity)
                    for count, multiplicity in quotient_l1[
                        "zero_subset_count_histogram"
                    ]
                    if multiplicity
                )
                if (
                    expected_histogram
                    != direct_zero_subset_histogram
                ):
                    raise AssertionError(
                        (p, n, quotient_l1, direct_zero_subset_histogram)
                    )
            if quotient_l1.get("coefficient_value_histogram") is not None:
                if (
                    tuple(quotient_l1["coefficient_value_histogram"])
                    != direct_coefficient_histogram
                ):
                    raise AssertionError(
                        (p, n, quotient_l1, direct_coefficient_histogram)
                    )
        elif int(quotient_l1["l1_bound"]) < direct_quotient_l1:
            raise AssertionError((p, n, quotient_l1, direct_quotient_l1))
        certificate = (
            slack_two_second_quotient_window_union_kummer_saturation_data(
                p=p,
                domain_order=n,
                quotient_order=quotient_order,
                remaining_fibers=remaining_fibers,
            )
        )
        if certificate is None:
            raise AssertionError((p, n, quotient_order, remaining_fibers))
        if label_triples != int(certificate["label_triple_count"]):
            raise AssertionError((p, n, label_triples, certificate))
        if coefficient_bound != int(certificate["coefficient_abs_bound"]):
            raise AssertionError((p, n, coefficient_bound, certificate))
        ambient_kernel_count = (p - 1) // n
        if bool(quotient_l1["exact"]):
            quotient_l1_bound = (
                ambient_kernel_count ** 3 * int(quotient_l1["l1_bound"])
            )
        else:
            quotient_l1_bound = (
                ambient_kernel_count ** 3 * label_triples
                + (
                    int(certificate["kernel_character_order"]) ** 3
                    - ambient_kernel_count ** 3
                )
                * coefficient_bound
            )
        if quotient_l1_bound != int(
            certificate["quotient_coefficient_l1_bound"]
        ):
            raise AssertionError((p, n, quotient_l1_bound, certificate))
        quotient_one_coordinate_l1_bound = (
            direct_ambient_window_label_one_coordinate_l1_bound(
                int(certificate["kernel_character_order"]),
                quotient_order,
                remaining_fibers,
            )
        )
        (
            quotient_active_one_l1_bound,
            quotient_active_two_l1_bound,
            quotient_active_three_l1_bound,
        ) = direct_ambient_window_label_coordinate_active_l1_bounds(
            int(certificate["kernel_character_order"]),
            quotient_order,
            remaining_fibers,
        )
        if quotient_active_one_l1_bound != quotient_one_coordinate_l1_bound:
            raise AssertionError(
                (p, n, quotient_active_one_l1_bound, certificate)
            )
        if quotient_one_coordinate_l1_bound != int(
            certificate["quotient_one_coordinate_l1_bound"]
        ):
            raise AssertionError(
                (p, n, quotient_one_coordinate_l1_bound, certificate)
            )
        if quotient_active_two_l1_bound != int(
            certificate["quotient_two_coordinate_l1_bound"]
        ):
            raise AssertionError((p, n, quotient_active_two_l1_bound))
        if quotient_active_three_l1_bound != int(
            certificate["quotient_three_coordinate_l1_bound"]
        ):
            raise AssertionError((p, n, quotient_active_three_l1_bound))
        if bool(certificate["quotient_l1_exact"]) != bool(quotient_l1["exact"]):
            raise AssertionError((p, n, quotient_l1, certificate))
        coefficient_l1_bound = direct_ambient_window_label_l1_bound(
            int(certificate["kernel_character_order"]),
            quotient_order,
            remaining_fibers,
            int(certificate["square_coset_index"]),
        )
        if bool(certificate["quotient_l1_exact"]):
            if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
                raise AssertionError((p, n, coefficient_l1_bound, certificate))
        elif coefficient_l1_bound > int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        crude_coefficient_l1_bound = (
            int(certificate["crude_coefficient_abs_bound"])
            * int(certificate["denominator"])
            - int(certificate["principal_weight"])
        )
        if crude_coefficient_l1_bound != int(
            certificate["crude_coefficient_l1_bound"]
        ):
            raise AssertionError((p, n, crude_coefficient_l1_bound, certificate))
        jacobi_l1_bound = (
            int(certificate["quotient_coefficient_l1_bound"])
            - int(certificate["principal_weight"])
        )
        conic_l1_bound = int(certificate["principal_weight"]) * (
            int(certificate["square_coset_index"]) - 1
        )
        quadratic_conic_character_count = (
            1
            if int(certificate["square_coset_index"]) > 1
            and int(certificate["square_coset_index"]) % 2 == 0
            else 0
        )
        quadratic_one_coordinate_l1_bound = (
            quotient_one_coordinate_l1_bound * quadratic_conic_character_count
        )
        one_coordinate_kummer_l1_bound = quotient_active_one_l1_bound * (
            int(certificate["square_coset_index"])
            - 1
            - quadratic_conic_character_count
        )
        two_coordinate_kummer_l1_bound = quotient_active_two_l1_bound * (
            int(certificate["square_coset_index"]) - 1
        )
        three_coordinate_kummer_l1_bound = quotient_active_three_l1_bound * (
            int(certificate["square_coset_index"]) - 1
        )
        kummer_l1_bound = (
            one_coordinate_kummer_l1_bound
            + two_coordinate_kummer_l1_bound
            + three_coordinate_kummer_l1_bound
        )
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["quadratic_one_coordinate_error_constant"])
            * quadratic_one_coordinate_l1_bound
            + int(certificate["one_coordinate_kummer_error_constant"])
            * one_coordinate_kummer_l1_bound
            + int(certificate["two_coordinate_kummer_error_constant"])
            * two_coordinate_kummer_l1_bound
            + int(certificate["three_coordinate_kummer_error_constant"])
            * three_coordinate_kummer_l1_bound
        )
        if (
            jacobi_l1_bound
            + conic_l1_bound
            + quadratic_one_coordinate_l1_bound
            + kummer_l1_bound
            != int(certificate["coefficient_l1_bound"])
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if quadratic_one_coordinate_l1_bound != int(
            certificate["quadratic_one_coordinate_l1_bound"]
        ):
            raise AssertionError(
                (p, n, quadratic_one_coordinate_l1_bound, certificate)
            )
        if one_coordinate_kummer_l1_bound != int(
            certificate["one_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, one_coordinate_kummer_l1_bound))
        if two_coordinate_kummer_l1_bound != int(
            certificate["two_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, two_coordinate_kummer_l1_bound))
        if three_coordinate_kummer_l1_bound != int(
            certificate["three_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, three_coordinate_kummer_l1_bound))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if int(certificate["quadratic_one_coordinate_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["one_coordinate_kummer_error_constant"]) != 4:
            raise AssertionError((p, n, certificate))
        if int(certificate["two_coordinate_kummer_error_constant"]) != 9:
            raise AssertionError((p, n, certificate))
        if int(certificate["three_coordinate_kummer_error_constant"]) != int(
            certificate["nonprincipal_constant"]
        ):
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        elementary_open_sqrt_error_bound = (
            6 * ceil_sqrt(p) * (jacobi_l1_bound + conic_l1_bound)
        )
        if elementary_open_sqrt_error_bound != int(
            certificate["elementary_open_sqrt_error_bound"]
        ):
            raise AssertionError(
                (p, n, elementary_open_sqrt_error_bound, certificate)
            )
        weighted_error_total_bound = (
            p * weighted_error_l1_bound + elementary_open_sqrt_error_bound
        )
        if weighted_error_total_bound != int(
            certificate["weighted_error_total_bound"]
        ):
            raise AssertionError(
                (p, n, weighted_error_total_bound, certificate)
            )
        crude_jacobi_l1_bound = int(
            certificate["crude_coefficient_abs_bound"]
        ) * (int(certificate["kernel_character_order"]) ** 3 - 1)
        crude_conic_l1_bound = int(certificate["principal_weight"]) * (
            int(certificate["square_coset_index"]) - 1
        )
        crude_quadratic_one_coordinate_l1_bound = (
            int(certificate["crude_coefficient_abs_bound"])
            * 3
            * (int(certificate["kernel_character_order"]) - 1)
            * quadratic_conic_character_count
        )
        crude_one_coordinate_kummer_l1_bound = (
            int(certificate["crude_coefficient_abs_bound"])
            * 3
            * (int(certificate["kernel_character_order"]) - 1)
            * (
                int(certificate["square_coset_index"])
                - 1
                - quadratic_conic_character_count
            )
        )
        crude_two_coordinate_kummer_l1_bound = (
            int(certificate["crude_coefficient_abs_bound"])
            * 3
            * (int(certificate["kernel_character_order"]) - 1) ** 2
            * (int(certificate["square_coset_index"]) - 1)
        )
        crude_three_coordinate_kummer_l1_bound = (
            int(certificate["crude_coefficient_abs_bound"])
            * (int(certificate["kernel_character_order"]) - 1) ** 3
            * (int(certificate["square_coset_index"]) - 1)
        )
        crude_kummer_l1_bound = (
            crude_one_coordinate_kummer_l1_bound
            + crude_two_coordinate_kummer_l1_bound
            + crude_three_coordinate_kummer_l1_bound
        )
        crude_weighted_error_l1_bound = (
            crude_jacobi_l1_bound
            + crude_conic_l1_bound
            + int(certificate["quadratic_one_coordinate_error_constant"])
            * crude_quadratic_one_coordinate_l1_bound
            + int(certificate["one_coordinate_kummer_error_constant"])
            * crude_one_coordinate_kummer_l1_bound
            + int(certificate["two_coordinate_kummer_error_constant"])
            * crude_two_coordinate_kummer_l1_bound
            + int(certificate["three_coordinate_kummer_error_constant"])
            * crude_three_coordinate_kummer_l1_bound
        )
        if crude_jacobi_l1_bound != int(certificate["crude_jacobi_l1_bound"]):
            raise AssertionError((p, n, crude_jacobi_l1_bound, certificate))
        if crude_conic_l1_bound != int(certificate["crude_conic_l1_bound"]):
            raise AssertionError((p, n, crude_conic_l1_bound, certificate))
        if crude_quadratic_one_coordinate_l1_bound != int(
            certificate["crude_quadratic_one_coordinate_l1_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    crude_quadratic_one_coordinate_l1_bound,
                    certificate,
                )
            )
        if crude_one_coordinate_kummer_l1_bound != int(
            certificate["crude_one_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, crude_one_coordinate_kummer_l1_bound))
        if crude_two_coordinate_kummer_l1_bound != int(
            certificate["crude_two_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, crude_two_coordinate_kummer_l1_bound))
        if crude_three_coordinate_kummer_l1_bound != int(
            certificate["crude_three_coordinate_kummer_l1_bound"]
        ):
            raise AssertionError((p, n, crude_three_coordinate_kummer_l1_bound))
        if crude_kummer_l1_bound != int(certificate["crude_kummer_l1_bound"]):
            raise AssertionError((p, n, crude_kummer_l1_bound, certificate))
        if crude_weighted_error_l1_bound != int(
            certificate["crude_weighted_error_l1_bound"]
        ):
            raise AssertionError(
                (p, n, crude_weighted_error_l1_bound, certificate)
            )
        crude_elementary_open_sqrt_error_bound = (
            6 * ceil_sqrt(p) * (crude_jacobi_l1_bound + crude_conic_l1_bound)
        )
        if crude_elementary_open_sqrt_error_bound != int(
            certificate["crude_elementary_open_sqrt_error_bound"]
        ):
            raise AssertionError(
                (
                    p,
                    n,
                    crude_elementary_open_sqrt_error_bound,
                    certificate,
                )
            )
        crude_weighted_error_total_bound = (
            p * crude_weighted_error_l1_bound
            + crude_elementary_open_sqrt_error_bound
        )
        if crude_weighted_error_total_bound != int(
            certificate["crude_weighted_error_total_bound"]
        ):
            raise AssertionError(
                (p, n, crude_weighted_error_total_bound, certificate)
            )
        failures = two_fiber_divisor_power_failure_count(
            int(certificate["kernel_character_order"]),
            int(certificate["square_coset_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        principal_count = principal_open_count(p)
        degeneracy_count = degeneracy_line_union_count(p)
        lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * weighted_error_l1_bound
            - elementary_open_sqrt_error_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            int(certificate["principal_weight"]),
            weighted_error_l1_bound + 6 * int(certificate["denominator"]),
            sqrt_error_weight=6 * (jacobi_l1_bound + conic_l1_bound),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        direct_quotient_l1_bound_numerator = (
            coefficient_l1_bound + int(certificate["principal_weight"])
        )
        if (
            direct_quotient_l1_bound_numerator
            % int(certificate["square_coset_index"])
        ):
            raise AssertionError(
                (p, n, direct_quotient_l1_bound_numerator, certificate)
            )
        direct_quotient_l1_bound = (
            direct_quotient_l1_bound_numerator
            // int(certificate["square_coset_index"])
        )
        direct_jacobi_l1_bound = (
            direct_quotient_l1_bound - int(certificate["principal_weight"])
        )
        direct_weighted_error_l1_bound = (
            direct_jacobi_l1_bound
            + int(certificate["principal_weight"])
            * (int(certificate["square_coset_index"]) - 1)
            + int(certificate["quadratic_one_coordinate_error_constant"])
            * quadratic_one_coordinate_l1_bound
            + int(certificate["one_coordinate_kummer_error_constant"])
            * one_coordinate_kummer_l1_bound
            + int(certificate["two_coordinate_kummer_error_constant"])
            * two_coordinate_kummer_l1_bound
            + int(certificate["three_coordinate_kummer_error_constant"])
            * three_coordinate_kummer_l1_bound
        )
        direct_lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * direct_weighted_error_l1_bound
            - elementary_open_sqrt_error_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if direct_lower_numerator < lower_numerator:
            raise AssertionError((p, n, direct_lower_numerator, certificate))
        crude_lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * crude_weighted_error_l1_bound
            - crude_elementary_open_sqrt_error_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if crude_lower_numerator != int(certificate["crude_lower_numerator"]):
            raise AssertionError((p, n, crude_lower_numerator, certificate))
        if crude_lower_numerator > 0:
            raise AssertionError((p, n, crude_lower_numerator, certificate))
        union_certificate_positive = bool(certificate["saturation_certificate"])
        if union_certificate_positive != expected_union_certificate:
            raise AssertionError((p, n, certificate))
        fixed_certificate = slack_two_second_fixed_window_kummer_saturation_data(
            p=p,
            domain_order=n,
            quotient_order=quotient_order,
            window_size=remaining_fibers,
        )
        if fixed_certificate is None:
            raise AssertionError((p, n, quotient_order, remaining_fibers))
        if (
            bool(fixed_certificate["saturation_certificate"])
            != expected_fixed_certificate
        ):
            raise AssertionError((p, n, fixed_certificate))
        reduction = slack_two_second_quotient_window_reduction_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
            remaining_fibers=remaining_fibers,
        )
        if reduction is None:
            raise AssertionError((p, n, quotient_order, remaining_fibers))
        if union_certificate_positive and not bool(
            reduction["saturates_nonzero_square_cosets"]
        ):
            raise AssertionError((p, n, certificate, reduction))
        r_window_union_kummer_checked.append(
            (
                p,
                n,
                quotient_order,
                remaining_fibers,
                label_triples,
                coefficient_bound,
                certificate["denominator"],
                certificate["coefficient_l1_bound"],
                certificate["crude_lower_numerator"],
                certificate["lower_numerator"],
                union_certificate_positive,
                bool(fixed_certificate["saturation_certificate"]),
                reduction["nonzero_square_coset_count"],
                reduction["total_nonzero_square_coset_count"],
            )
        )
    scan_label_checked = []
    for p, n, k, slack, quotient_order, expected_label in SCAN_LABEL_CASES:
        result = scan_supports(
            p=p,
            n=n,
            k=k,
            slack=slack,
            quotient_order=quotient_order,
            primitive=None,
            anchor_exp=None,
            direction_exp=None,
            max_supports=50_000,
            top_histograms=3,
        )
        label = result["canonical_slack_two_second_index_window_label"]
        if label != expected_label:
            raise AssertionError((p, n, k, quotient_order, label, result))
        if not bool(
            result["canonical_slack_two_second_r2_union_exact_support_certificate"]
        ):
            raise AssertionError((p, n, k, quotient_order, result))
        if not bool(result["canonical_slack_two_second_r2_union_reduction_check"]):
            raise AssertionError((p, n, k, quotient_order, result))
        scan_label_checked.append((p, n, k, quotient_order, label))
    print(
        "verify_m1_slack_two_depth_two_kummer_saturation: "
        f"PASS checked={checked} equal_line_checked={equal_line_checked} "
        f"lift_checked={lift_checked} "
        f"lift_bound_checked={lift_bound_checked} "
        f"kernel_checked={kernel_checked} "
        f"two_fiber_checked={two_fiber_checked} "
        f"two_fiber_union_checked={two_fiber_union_checked} "
        f"r_window_checked={r_window_checked} "
        f"fixed_window_kummer_checked={fixed_window_kummer_checked} "
        f"r_window_union_kummer_checked={r_window_union_kummer_checked} "
        f"scan_label_checked={scan_label_checked}"
    )


if __name__ == "__main__":
    main()
