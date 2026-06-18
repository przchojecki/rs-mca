#!/usr/bin/env python3
"""Scan M1 support-coefficient incidences by quotient-fiber occupancy.

Proof status: AUDIT / EXPERIMENTAL.

This is a tiny-field scanner for the support-coefficient criterion in
experimental/m1_support_coefficient_test.md. It enumerates exact supports of
size k+t, computes Pi_S(f), Pi_S(g), records the bad slope contributed by each
collinear noncontained support, and labels the support by its quotient-fiber
occupancy histogram.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from itertools import combinations, product
from typing import Dict, List, Optional, Sequence, Tuple

from mca_slope_scan import fraction_string, inv, make_domain
from verify_m1_quotient_remainder_profile import occupancy_family_size


def monomial_word(domain: Sequence[int], exponent: int, p: int) -> Tuple[int, ...]:
    return tuple(pow(x, exponent, p) for x in domain)


def solve_coefficients(xs: Sequence[int], ys: Sequence[int], p: int) -> List[int]:
    size = len(xs)
    matrix = [
        [pow(xs[row], col, p) for col in range(size)] + [ys[row] % p]
        for row in range(size)
    ]

    pivot_row = 0
    for col in range(size):
        pivot = None
        for row in range(pivot_row, size):
            if matrix[row][col] % p:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular interpolation matrix")

        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inv(matrix[pivot_row][col], p)
        matrix[pivot_row] = [(entry * scale) % p for entry in matrix[pivot_row]]

        for row in range(size):
            if row == pivot_row or matrix[row][col] % p == 0:
                continue
            factor = matrix[row][col] % p
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[pivot_row][idx]) % p
                for idx in range(size + 1)
            ]
        pivot_row += 1

    return [matrix[row][size] % p for row in range(size)]


def top_coefficients(
    values: Sequence[int],
    domain: Sequence[int],
    support: Sequence[int],
    k: int,
    slack: int,
    p: int,
) -> Tuple[int, ...]:
    xs = [domain[index] for index in support]
    ys = [values[index] for index in support]
    coeffs = solve_coefficients(xs, ys, p)
    return tuple(coeffs[k : k + slack])


def slope_from_top_coefficients(
    anchor_top: Sequence[int],
    direction_top: Sequence[int],
    p: int,
) -> Optional[int]:
    if all(entry % p == 0 for entry in anchor_top):
        if all(entry % p == 0 for entry in direction_top):
            return None
    if all(entry % p == 0 for entry in direction_top):
        return None

    pivot = next(index for index, entry in enumerate(direction_top) if entry % p)
    scalar = anchor_top[pivot] * inv(direction_top[pivot], p)
    scalar %= p
    for left, right in zip(anchor_top, direction_top):
        if (left - scalar * right) % p:
            return None
    return (-scalar) % p


def elementary_symmetric_prefix(
    values: Sequence[int],
    max_degree: int,
    p: int,
) -> Tuple[int, ...]:
    """Return e_0,...,e_max_degree for the supplied field values."""

    coeffs = [0] * (max_degree + 1)
    coeffs[0] = 1
    for value in values:
        for degree in range(max_degree, 0, -1):
            coeffs[degree] += value * coeffs[degree - 1]
            coeffs[degree] %= p
    return tuple(coeffs)


def residual_support_indices(
    support: Sequence[int],
    quotient_order: int,
    fiber_size: int,
) -> Tuple[int, ...]:
    support_set = set(support)
    residual = []
    for fiber in range(quotient_order):
        fiber_indices = [
            fiber + quotient_order * offset
            for offset in range(fiber_size)
        ]
        occupied = [index for index in fiber_indices if index in support_set]
        if len(occupied) == fiber_size:
            continue
        residual.extend(occupied)
    return tuple(residual)


def residual_touched_fiber_count(
    residual: Sequence[int],
    quotient_order: int,
) -> int:
    return len({index % quotient_order for index in residual})


def quotient_core_value_sum(
    support: Sequence[int],
    quotient_order: int,
    fiber_size: int,
    domain: Sequence[int],
    p: int,
) -> int:
    support_set = set(support)
    total = 0
    for fiber in range(quotient_order):
        fiber_indices = [
            fiber + quotient_order * offset
            for offset in range(fiber_size)
        ]
        if all(index in support_set for index in fiber_indices):
            total += pow(domain[fiber], fiber_size, p)
            total %= p
    return total


def canonical_slope_from_symmetric_prefix(
    values: Sequence[int],
    slack: int,
    p: int,
) -> Optional[int]:
    sym = elementary_symmetric_prefix(values, slack, p)
    if any(sym[degree] % p for degree in range(1, slack)):
        return None
    sign = -1 if slack % 2 else 1
    return (sign * sym[slack]) % p


def first_nonzero_frontier(
    values: Sequence[int],
    slack: int,
    p: int,
) -> Tuple[Optional[int], int]:
    sym = elementary_symmetric_prefix(values, len(values), p)
    for degree in range(slack, len(values)):
        if sym[degree] % p:
            sign = -1 if degree % 2 else 1
            return degree, (sign * sym[degree]) % p
    return None, 0


def is_power_coset(values: Sequence[int], exponent: int, p: int) -> bool:
    if not values:
        return False
    target = pow(values[0], exponent, p)
    return all(pow(value, exponent, p) == target for value in values)


def multiplicative_coset_representative_map(
    p: int,
    subgroup: Sequence[int],
) -> Dict[int, int]:
    representative_by_value: Dict[int, int] = {}
    subgroup_values = tuple(subgroup)
    for value in range(1, p):
        if value in representative_by_value:
            continue
        coset = [(value * element) % p for element in subgroup_values]
        representative = min(coset)
        for element in coset:
            representative_by_value[element] = representative
    return representative_by_value


def quadratic_character(value: int, p: int) -> int:
    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def full_domain_slack_two_alpha_class_data(p: int) -> Optional[Dict[str, object]]:
    if p <= 5:
        return None

    chi_minus_one = quadratic_character(-1, p)
    chi_minus_three = quadratic_character(-3, p)
    admissible_count = p - 5
    zero_count = 1 + chi_minus_three
    signed_nonzero_sum = -3 * (chi_minus_one + chi_minus_three)
    nonzero_count = admissible_count - zero_count
    square_count = (nonzero_count + signed_nonzero_sum) // 2
    nonsquare_count = (nonzero_count - signed_nonzero_sum) // 2
    nonzero_slope_classes = (1 if square_count else 0) + (
        1 if nonsquare_count else 0
    )
    slope_count = (1 if zero_count else 0) + nonzero_slope_classes * (
        (p - 1) // 2
    )

    if square_count and nonsquare_count:
        slope_image = "full_field" if zero_count else "nonzero_field"
    elif zero_count and square_count:
        slope_image = "zero_plus_squares"
    elif zero_count and nonsquare_count:
        slope_image = "zero_plus_nonsquares"
    elif square_count:
        slope_image = "squares"
    elif nonsquare_count:
        slope_image = "nonsquares"
    elif zero_count:
        slope_image = "zero_only"
    else:
        slope_image = "empty"

    return {
        "alpha_square_count": square_count,
        "alpha_nonsquare_count": nonsquare_count,
        "alpha_zero_count": zero_count,
        "alpha_character_sum": signed_nonzero_sum,
        "slope_count": slope_count,
        "slope_image": slope_image,
    }


def full_domain_slack_two_depth_two_A_class_data(
    p: int,
) -> Optional[Dict[str, object]]:
    if p <= 3:
        return None

    square_count = 0
    nonsquare_count = 0
    zero_count = 0
    for u in range(1, p):
        for v in range(1, p):
            w = (-1 - u - v) % p
            if w == 0 or len({1, u, v, w}) != 4:
                continue
            value = (-(u * u + v * v + u * v + u + v + 1)) % p
            character = quadratic_character(value, p)
            if character > 0:
                square_count += 1
            elif character < 0:
                nonsquare_count += 1
            else:
                zero_count += 1

    nonzero_square_coset_count = (1 if square_count else 0) + (
        1 if nonsquare_count else 0
    )
    nonzero_slope_count = nonzero_square_coset_count * ((p - 1) // 2)
    if square_count and nonsquare_count:
        nonzero_slope_image = "nonzero_field"
    elif square_count:
        nonzero_slope_image = "squares"
    elif nonsquare_count:
        nonzero_slope_image = "nonsquares"
    else:
        nonzero_slope_image = "empty"

    large_prime_class_lower_bound = (p * p - 2 * p - 1) // 2
    excluded_line_bound = 9 * p
    return {
        "A_square_count": square_count,
        "A_nonsquare_count": nonsquare_count,
        "A_zero_count": zero_count,
        "A_character_sum_all_plane": p * quadratic_character(2, p),
        "A_zero_conic_bound": p + 1,
        "excluded_line_bound": excluded_line_bound,
        "large_prime_class_lower_bound": large_prime_class_lower_bound,
        "large_prime_certificate": (
            p >= 23 and large_prime_class_lower_bound > excluded_line_bound
        ),
        "finite_low_prime_certificate": p in {11, 13, 17, 19},
        "saturates_nonzero_square_cosets": (
            square_count > 0 and nonsquare_count > 0
        ),
        "nonzero_square_coset_count": nonzero_square_coset_count,
        "total_nonzero_square_coset_count": 2,
        "nonzero_slope_count": nonzero_slope_count,
        "nonzero_slope_image": nonzero_slope_image,
    }


def full_domain_slack_three_beta_class_data(p: int) -> Optional[Dict[str, object]]:
    if p <= 3:
        return None

    chi_minus_one = quadratic_character(-1, p)
    chi_minus_two = quadratic_character(-2, p)
    chi_minus_three = quadratic_character(-3, p)
    ordered_shape_count = p - 9 - 4 * chi_minus_three - 6 * chi_minus_two
    beta_count = ordered_shape_count // 6
    zero_beta_count = 1 if chi_minus_one == 1 else 0
    nonzero_beta_count = beta_count - zero_beta_count
    nonzero_ordered_shape_count = 6 * nonzero_beta_count
    cube_surjective = math.gcd(3, p - 1) == 1
    cube_coset_lower_numerator = (
        nonzero_ordered_shape_count - 12 * ceil_sqrt(p) - 36
    )
    cube_coset_beta_lower_bound = (
        (cube_coset_lower_numerator + 17) // 18
        if cube_coset_lower_numerator > 0
        else 0
    )
    cube_coset_saturation_certificate = cube_coset_beta_lower_bound > 0

    if cube_surjective and nonzero_beta_count > 0:
        slope_count = (p - 1) + zero_beta_count
        slope_image = "full_field" if zero_beta_count else "nonzero_field"
    elif cube_surjective and zero_beta_count:
        slope_count = 1
        slope_image = "zero_only"
    elif cube_surjective:
        slope_count = 0
        slope_image = "empty"
    elif cube_coset_saturation_certificate:
        slope_count = (p - 1) + zero_beta_count
        slope_image = "full_field" if zero_beta_count else "nonzero_field"
    else:
        slope_count = None
        slope_image = "cube_coset_dependent"

    return {
        "ordered_shape_count": ordered_shape_count,
        "beta_count": beta_count,
        "zero_beta_count": zero_beta_count,
        "nonzero_beta_count": nonzero_beta_count,
        "cube_surjective": cube_surjective,
        "cube_coset_beta_lower_bound": cube_coset_beta_lower_bound,
        "cube_coset_saturation_certificate": cube_coset_saturation_certificate,
        "slope_count": slope_count,
        "slope_image": slope_image,
    }


def signed_symmetric_coefficient(
    values: Sequence[int],
    degree: int,
    p: int,
) -> int:
    sym = elementary_symmetric_prefix(values, degree, p)
    sign = -1 if degree % 2 else 1
    return (sign * sym[degree]) % p


def expected_boundary_residual_coset_count(
    domain_order: int,
    quotient_order: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> int:
    if slack >= fiber_size:
        return 0
    if domain_order % slack:
        return 0
    if (support_size - slack) % fiber_size:
        return 0
    whole_fibers = (support_size - slack) // fiber_size
    touched_fibers = slack // math.gcd(slack, fiber_size)
    remaining_fibers = quotient_order - touched_fibers
    if whole_fibers < 0 or whole_fibers > remaining_fibers:
        return 0
    return (domain_order // slack) * math.comb(remaining_fibers, whole_fibers)


def expected_boundary_slope_data(
    domain_order: int,
    quotient_order: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> Tuple[int, int]:
    if slack >= fiber_size:
        return (0, 0)
    if domain_order % slack:
        return (0, 0)
    if (support_size - slack) % fiber_size:
        return (0, 0)
    whole_fibers = (support_size - slack) // fiber_size
    touched_fibers = slack // math.gcd(slack, fiber_size)
    remaining_fibers = quotient_order - touched_fibers
    if whole_fibers < 0 or whole_fibers > remaining_fibers:
        return (0, 0)
    multiplicity = math.comb(remaining_fibers, whole_fibers)
    if multiplicity == 0:
        return (0, 0)
    return (domain_order // slack, multiplicity)


def subboundary_residual_floor(
    support_size: int,
    fiber_size: int,
    slack: int,
) -> Optional[int]:
    residue = support_size % fiber_size
    if 0 < residue < slack < fiber_size:
        return fiber_size + residue
    return None


def expected_small_residual_ledger(
    domain_order: int,
    quotient_order: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> Tuple[str, Optional[int], Optional[int], Optional[int]]:
    if slack >= fiber_size:
        return ("not_large_fiber", None, None, None)

    residue = support_size % fiber_size
    if residue == 0:
        whole_fibers = support_size // fiber_size
        if 0 <= whole_fibers <= quotient_order:
            support_count = math.comb(quotient_order, whole_fibers)
        else:
            support_count = 0
        slope_count = 1 if support_count else 0
        return ("whole_fiber_zero_slope", support_count, slope_count, support_count)

    if residue < slack:
        return ("subboundary_absent", 0, 0, 0)

    if residue == slack:
        support_count = expected_boundary_residual_coset_count(
            domain_order=domain_order,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            support_size=support_size,
            slack=slack,
        )
        slope_count, multiplicity = expected_boundary_slope_data(
            domain_order=domain_order,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            support_size=support_size,
            slack=slack,
        )
        regime = "boundary_power_cosets" if support_count else "boundary_absent"
        return (regime, support_count, slope_count, multiplicity)

    return ("superboundary_unclassified", None, None, None)


def expected_residual_packet_lift_count(
    support_size: int,
    quotient_order: int,
    fiber_size: int,
    residual_size: int,
    touched_fibers: int,
) -> int:
    if residual_size > support_size:
        return 0
    if (support_size - residual_size) % fiber_size:
        return 0
    whole_fibers = (support_size - residual_size) // fiber_size
    available_fibers = quotient_order - touched_fibers
    if whole_fibers < 0 or whole_fibers > available_fibers:
        return 0
    return math.comb(available_fibers, whole_fibers)


def all_residual_packets_lift_active(
    support_size: int,
    quotient_order: int,
    fiber_size: int,
    residual_size: int,
) -> Tuple[bool, Optional[int], int]:
    required_fibers = min(residual_size, quotient_order)
    if residual_size > support_size:
        return (False, None, required_fibers)
    if (support_size - residual_size) % fiber_size:
        return (False, None, required_fibers)

    whole_fibers = (support_size - residual_size) // fiber_size
    remaining_fibers = quotient_order - whole_fibers
    return (remaining_fibers >= required_fibers, remaining_fibers, required_fibers)


def quotient_limited_pair_parameter_bound(
    quotient_order: int,
    fiber_size: int,
    remaining_fibers: Optional[int],
    residual_size: int,
) -> int:
    if remaining_fibers is None or remaining_fibers <= 0:
        return 0

    max_touched = min(remaining_fibers, residual_size, quotient_order)
    total = 0
    for touched in range(1, max_touched + 1):
        total += (
            math.comb(quotient_order - 1, touched - 1)
            * (touched * fiber_size) ** 2
        )
    return total


def slack_two_second_kernel_fiber_reduction_data(
    p: int,
    domain: Sequence[int],
    quotient_order: int,
) -> Dict[str, object]:
    kernel = tuple(domain[index] for index in range(0, len(domain), quotient_order))
    kernel_set = set(kernel)
    square_image = {x * x % p for x in domain}
    nonzero_square_cosets = set()
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
            nonzero_square_cosets.add(
                min((shape_slope * square) % p for square in square_image)
            )

    slope_count = (1 if zero_parameter_count else 0) + (
        len(nonzero_square_cosets) * len(square_image)
    )
    return {
        "kernel_order": len(kernel),
        "parameter_count": parameter_count,
        "zero_parameter_count": zero_parameter_count,
        "nonzero_parameter_count": parameter_count - zero_parameter_count,
        "nonzero_square_coset_count": len(nonzero_square_cosets),
        "slope_count": min(p, slope_count),
    }


def slack_two_second_two_fiber_window_data(
    p: int,
    domain: Sequence[int],
    quotient_order: int,
    second_fiber: int = 1,
) -> Optional[Dict[str, object]]:
    if quotient_order < 2 or len(domain) % quotient_order:
        return None

    second_fiber %= quotient_order
    if second_fiber == 0:
        return None

    fiber_size = len(domain) // quotient_order
    window = tuple(
        domain[fiber + quotient_order * offset]
        for fiber in (0, second_fiber)
        for offset in range(fiber_size)
    )
    window_set = set(window)
    square_image = {x * x % p for x in domain}
    square_coset_rep = multiplicative_coset_representative_map(
        p,
        tuple(square_image),
    )

    nonzero_square_cosets = set()
    parameter_count = 0
    zero_parameter_count = 0
    for u in window:
        for v in window:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in window_set or len(set(values)) != 4:
                continue
            parameter_count += 1
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                zero_parameter_count += 1
                continue
            nonzero_square_cosets.add(square_coset_rep[shape_slope])

    slope_count = (1 if zero_parameter_count else 0) + (
        len(nonzero_square_cosets) * len(square_image)
    )
    return {
        "second_fiber": second_fiber,
        "fiber_size": fiber_size,
        "window_size": len(window),
        "parameter_count": parameter_count,
        "zero_parameter_count": zero_parameter_count,
        "nonzero_parameter_count": parameter_count - zero_parameter_count,
        "nonzero_square_coset_count": len(nonzero_square_cosets),
        "total_nonzero_square_coset_count": (p - 1) // len(square_image),
        "square_image_size": len(square_image),
        "slope_count": min(p, slope_count),
    }


def slack_two_second_fixed_window_data(
    p: int,
    domain: Sequence[int],
    quotient_order: int,
    window_fibers: Sequence[int],
) -> Optional[Dict[str, object]]:
    if quotient_order < 1 or len(domain) % quotient_order:
        return None

    normalized_fibers = tuple(
        sorted({fiber % quotient_order for fiber in window_fibers})
    )
    if not normalized_fibers or 0 not in normalized_fibers:
        return None

    fiber_size = len(domain) // quotient_order
    window = tuple(
        domain[fiber + quotient_order * offset]
        for fiber in normalized_fibers
        for offset in range(fiber_size)
    )
    window_set = set(window)
    square_image = {x * x % p for x in domain}
    square_coset_rep = multiplicative_coset_representative_map(
        p,
        tuple(square_image),
    )

    nonzero_square_cosets = set()
    parameter_count = 0
    zero_parameter_count = 0
    for u in window:
        u_square = u * u
        for v in window:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in window_set or len(set(values)) != 4:
                continue
            parameter_count += 1
            shape_slope = (-(u_square + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                zero_parameter_count += 1
                continue
            nonzero_square_cosets.add(square_coset_rep[shape_slope])

    slope_count = (1 if zero_parameter_count else 0) + (
        len(nonzero_square_cosets) * len(square_image)
    )
    return {
        "window_fibers": normalized_fibers,
        "window_size": len(normalized_fibers),
        "fiber_size": fiber_size,
        "window_point_count": len(window),
        "parameter_count": parameter_count,
        "zero_parameter_count": zero_parameter_count,
        "nonzero_parameter_count": parameter_count - zero_parameter_count,
        "nonzero_square_coset_count": len(nonzero_square_cosets),
        "total_nonzero_square_coset_count": (p - 1) // len(square_image),
        "square_image_size": len(square_image),
        "slope_count": min(p, slope_count),
    }


def slack_two_second_two_fiber_union_reduction_data(
    p: int,
    domain: Sequence[int],
    quotient_order: int,
) -> Optional[Dict[str, object]]:
    if quotient_order < 2 or len(domain) % quotient_order:
        return None

    domain_set = set(domain)
    value_to_fiber = {
        value: index % quotient_order for index, value in enumerate(domain)
    }
    square_image = {x * x % p for x in domain}
    square_coset_rep = multiplicative_coset_representative_map(
        p,
        tuple(square_image),
    )

    parameter_count = 0
    zero_parameter_count = 0
    nonzero_square_cosets = set()
    for u in domain:
        u_square = u * u
        u_fiber = value_to_fiber[u]
        for v in domain:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in domain_set or len(set(values)) != 4:
                continue
            touched_fibers = {
                0,
                u_fiber,
                value_to_fiber[v],
                value_to_fiber[w],
            }
            if len(touched_fibers) > 2:
                continue
            parameter_count += 1
            shape_slope = (-(u_square + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                zero_parameter_count += 1
                continue
            nonzero_square_cosets.add(square_coset_rep[shape_slope])

    per_window_profiles = []
    for second_fiber in range(1, quotient_order):
        window = slack_two_second_two_fiber_window_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
            second_fiber=second_fiber,
        )
        if window is None:
            continue
        per_window_profiles.append(
            {
                "second_fiber": int(window["second_fiber"]),
                "parameter_count": int(window["parameter_count"]),
                "zero_parameter_count": int(window["zero_parameter_count"]),
                "nonzero_square_coset_count": int(
                    window["nonzero_square_coset_count"]
                ),
                "slope_count": int(window["slope_count"]),
            }
        )

    slope_count = (1 if zero_parameter_count else 0) + (
        len(nonzero_square_cosets) * len(square_image)
    )
    total_nonzero_square_cosets = (p - 1) // len(square_image)
    return {
        "quotient_order": quotient_order,
        "fiber_size": len(domain) // quotient_order,
        "window_count": len(per_window_profiles),
        "parameter_count": parameter_count,
        "zero_parameter_count": zero_parameter_count,
        "nonzero_parameter_count": parameter_count - zero_parameter_count,
        "nonzero_square_coset_count": len(nonzero_square_cosets),
        "total_nonzero_square_coset_count": total_nonzero_square_cosets,
        "square_image_size": len(square_image),
        "slope_count": min(p, slope_count),
        "saturates_nonzero_square_cosets": (
            len(nonzero_square_cosets) == total_nonzero_square_cosets
        ),
        "per_window_profiles": tuple(per_window_profiles),
    }


def slack_two_second_quotient_window_reduction_data(
    p: int,
    domain: Sequence[int],
    quotient_order: int,
    remaining_fibers: Optional[int],
) -> Optional[Dict[str, object]]:
    if (
        remaining_fibers is None
        or remaining_fibers <= 0
        or len(domain) % quotient_order
    ):
        return None

    effective_window_size = min(remaining_fibers, 4, quotient_order)
    domain_set = set(domain)
    value_to_fiber = {
        value: index % quotient_order for index, value in enumerate(domain)
    }
    square_image = {x * x % p for x in domain}
    square_coset_rep = multiplicative_coset_representative_map(
        p,
        tuple(square_image),
    )

    parameter_count = 0
    zero_parameter_count = 0
    nonzero_square_cosets = set()
    touched_fiber_histogram: Counter[int] = Counter()
    for u in domain:
        u_square = u * u
        u_fiber = value_to_fiber[u]
        for v in domain:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in domain_set or len(set(values)) != 4:
                continue
            touched_fibers = {
                0,
                u_fiber,
                value_to_fiber[v],
                value_to_fiber[w],
            }
            touched_count = len(touched_fibers)
            if touched_count > effective_window_size:
                continue
            parameter_count += 1
            touched_fiber_histogram[touched_count] += 1
            shape_slope = (-(u_square + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                zero_parameter_count += 1
                continue
            nonzero_square_cosets.add(square_coset_rep[shape_slope])

    slope_count = (1 if zero_parameter_count else 0) + (
        len(nonzero_square_cosets) * len(square_image)
    )
    total_nonzero_square_cosets = (p - 1) // len(square_image)
    window_count = math.comb(quotient_order - 1, effective_window_size - 1)
    return {
        "remaining_fibers": remaining_fibers,
        "effective_window_size": effective_window_size,
        "quotient_order": quotient_order,
        "fiber_size": len(domain) // quotient_order,
        "window_count": window_count,
        "parameter_count": parameter_count,
        "zero_parameter_count": zero_parameter_count,
        "nonzero_parameter_count": parameter_count - zero_parameter_count,
        "nonzero_square_coset_count": len(nonzero_square_cosets),
        "total_nonzero_square_coset_count": total_nonzero_square_cosets,
        "square_image_size": len(square_image),
        "slope_count": min(p, slope_count),
        "saturates_nonzero_square_cosets": (
            len(nonzero_square_cosets) == total_nonzero_square_cosets
        ),
        "touched_fiber_histogram": tuple(
            sorted(touched_fiber_histogram.items())
        ),
    }


def expected_first_superboundary_zero_slope_data(
    domain_order: int,
    quotient_order: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> Tuple[int, int, int, Optional[int]]:
    residual_size = slack + 1
    if residual_size >= fiber_size:
        return (0, 0, 0, None)
    if support_size % fiber_size != residual_size:
        return (0, 0, 0, None)
    if domain_order % residual_size:
        return (0, 0, 0, None)

    whole_fibers = (support_size - residual_size) // fiber_size
    touched_fibers = residual_size // math.gcd(residual_size, fiber_size)
    remaining_fibers = quotient_order - touched_fibers
    if whole_fibers < 0 or whole_fibers > remaining_fibers:
        return (0, 0, 0, touched_fibers)

    packet_count = domain_order // residual_size
    lift_multiplicity = math.comb(remaining_fibers, whole_fibers)
    return (
        packet_count,
        packet_count * lift_multiplicity,
        lift_multiplicity,
        touched_fibers,
    )


def expected_terminal_pure_zero_chain_data(
    domain_order: int,
    quotient_order: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> Dict[int, Dict[str, Optional[int]]]:
    data: Dict[int, Dict[str, Optional[int]]] = {}
    largest_residual_size = min(fiber_size, support_size + 1)
    for residual_size in range(slack + 1, largest_residual_size):
        depth = residual_size - slack
        lift_dividend = support_size - residual_size
        lift_gate_active = (
            lift_dividend >= 0 and lift_dividend % fiber_size == 0
        )
        whole_fibers = lift_dividend // fiber_size if lift_gate_active else None
        touched_fibers = residual_size // math.gcd(residual_size, fiber_size)
        abstract_packet_count = (
            domain_order // residual_size
            if domain_order % residual_size == 0
            else 0
        )
        lift_multiplicity = 0
        support_count = 0
        if abstract_packet_count and whole_fibers is not None:
            remaining_fibers = quotient_order - touched_fibers
            if 0 <= whole_fibers <= remaining_fibers:
                lift_multiplicity = math.comb(remaining_fibers, whole_fibers)
                support_count = abstract_packet_count * lift_multiplicity
        data[residual_size] = {
            "depth": depth,
            "lift_gate_active": int(lift_gate_active),
            "whole_fibers": whole_fibers,
            "touched_fibers": touched_fibers if abstract_packet_count else None,
            "packet_count": abstract_packet_count if lift_multiplicity else 0,
            "abstract_packet_count": abstract_packet_count,
            "lift_multiplicity": lift_multiplicity,
            "support_count": support_count,
        }
    return data


def first_superboundary_shape_coset_ledger(
    p: int,
    domain: Sequence[int],
    slack: int,
    support_size: int,
    quotient_order: int,
    fiber_size: int,
) -> Dict[str, object]:
    """Enumerate the normalized first-superboundary shape theorem."""

    value_to_index = {value: index for index, value in enumerate(domain)}
    residual_size = slack + 1
    orbit_factor = math.factorial(residual_size)
    parameter_count = 0
    active_parameter_count = 0
    active_zero_parameter_count = 0
    packet_count_numerator = 0
    support_count_numerator = 0
    packet_slope_histogram_numerator: Counter[int] = Counter()
    support_slope_histogram_numerator: Counter[int] = Counter()
    zero_slope = False
    active_zero_slope = False
    power_image = {pow(x, slack, p) for x in domain}
    nonzero_power_cosets = set()
    active_nonzero_power_cosets = set()
    total_nonzero_power_cosets = (p - 1) // len(power_image)
    whole_fibers = (
        (support_size - residual_size) // fiber_size
        if (
            support_size >= residual_size
            and (support_size - residual_size) % fiber_size == 0
        )
        else None
    )

    for tail in product(domain, repeat=slack):
        values = (1, *tail)
        if len(set(values)) != residual_size:
            continue
        sym = elementary_symmetric_prefix(values, slack, p)
        if any(sym[degree] % p for degree in range(1, slack)):
            continue
        parameter_count += 1
        shape_slope = signed_symmetric_coefficient(values, slack, p)
        if shape_slope == 0:
            zero_slope = True
            coset_representative = None
        else:
            coset_representative = min(
                (shape_slope * power) % p for power in power_image
            )
            nonzero_power_cosets.add(coset_representative)

        if whole_fibers is None:
            continue

        touched_fibers = len(
            {value_to_index[value] % quotient_order for value in values}
        )
        lift_count = expected_residual_packet_lift_count(
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            residual_size=residual_size,
            touched_fibers=touched_fibers,
        )
        if lift_count == 0:
            continue
        active_parameter_count += 1
        if shape_slope == 0:
            active_zero_parameter_count += 1
            active_zero_slope = True
        else:
            assert coset_representative is not None
            active_nonzero_power_cosets.add(coset_representative)

        for x in domain:
            slope = (pow(x, slack, p) * shape_slope) % p
            packet_count_numerator += 1
            support_count_numerator += lift_count
            packet_slope_histogram_numerator[slope] += 1
            support_slope_histogram_numerator[slope] += lift_count

    numerators = [
        packet_count_numerator,
        support_count_numerator,
        *packet_slope_histogram_numerator.values(),
        *support_slope_histogram_numerator.values(),
    ]
    orbit_check = all(numerator % orbit_factor == 0 for numerator in numerators)
    packet_slope_histogram = Counter(
        {
            slope: count // orbit_factor
            for slope, count in packet_slope_histogram_numerator.items()
        }
    )
    support_slope_histogram = Counter(
        {
            slope: count // orbit_factor
            for slope, count in support_slope_histogram_numerator.items()
        }
    )
    power_coset_slope_count = (
        (1 if active_zero_slope else 0)
        + len(active_nonzero_power_cosets) * len(power_image)
    )
    abstract_power_coset_slope_count = (
        (1 if zero_slope else 0) + len(nonzero_power_cosets) * len(power_image)
    )
    active_nonzero_parameter_count = (
        active_parameter_count - active_zero_parameter_count
    )
    active_nonzero_parameter_orbit_check = (
        active_nonzero_parameter_count % orbit_factor == 0
    )
    active_nonzero_orbit_bound = (
        active_nonzero_parameter_count // orbit_factor
        if active_nonzero_parameter_orbit_check
        else active_parameter_count
    )
    power_coset_slope_bound = (
        (1 if active_zero_slope else 0)
        + active_nonzero_orbit_bound * len(power_image)
    )
    return {
        "residual_size": residual_size,
        "orbit_factor": orbit_factor,
        "parameter_count": parameter_count,
        "active_parameter_count": active_parameter_count,
        "active_zero_parameter_count": active_zero_parameter_count,
        "active_nonzero_parameter_orbit_check": (
            active_nonzero_parameter_orbit_check
        ),
        "nonzero_power_coset_count": len(nonzero_power_cosets),
        "active_nonzero_power_coset_count": len(active_nonzero_power_cosets),
        "total_nonzero_power_coset_count": total_nonzero_power_cosets,
        "power_image_size": len(power_image),
        "abstract_power_coset_slope_count": abstract_power_coset_slope_count,
        "power_coset_slope_count": power_coset_slope_count,
        "power_coset_slope_bound": min(p, power_coset_slope_bound),
        "orbit_quotient_check": orbit_check,
        "packet_count": packet_count_numerator // orbit_factor,
        "weighted_support_count": support_count_numerator // orbit_factor,
        "packet_slope_histogram": packet_slope_histogram,
        "support_slope_histogram": support_slope_histogram,
    }


def slack_two_first_superboundary_shape_ledger(
    p: int,
    domain: Sequence[int],
    support_size: int,
    quotient_order: int,
    fiber_size: int,
) -> Dict[str, object]:
    domain_set = set(domain)
    value_to_index = {value: index for index, value in enumerate(domain)}
    parameter_count = 0
    active_parameter_count = 0
    active_zero_parameter_count = 0
    packet_count_numerator = 0
    support_count_numerator = 0
    packet_slope_histogram_numerator: Counter[int] = Counter()
    support_slope_histogram_numerator: Counter[int] = Counter()
    zero_slope = False
    nonzero_square_cosets = set()
    active_zero_slope = False
    square_image = {x * x % p for x in domain}
    active_nonzero_square_cosets = set()
    total_nonzero_square_cosets = (p - 1) // len(square_image)
    whole_fibers = (
        (support_size - 3) // fiber_size
        if support_size >= 3 and (support_size - 3) % fiber_size == 0
        else None
    )

    for u in domain:
        v = (-1 - u) % p
        if v not in domain_set:
            continue
        if u == 1 or v == 1 or v == u:
            continue
        parameter_count += 1
        shape_slope = (-1 - u - u * u) % p
        if shape_slope == 0:
            zero_slope = True
        else:
            coset_representative = min(
                (shape_slope * square) % p for square in square_image
            )
            nonzero_square_cosets.add(coset_representative)

        if whole_fibers is None:
            continue

        touched_fibers = len(
            {
                0,
                value_to_index[u] % quotient_order,
                value_to_index[v] % quotient_order,
            }
        )
        if whole_fibers > quotient_order - touched_fibers:
            lift_count = 0
        else:
            lift_count = math.comb(quotient_order - touched_fibers, whole_fibers)
        if lift_count == 0:
            continue
        active_parameter_count += 1
        if shape_slope == 0:
            active_zero_parameter_count += 1
            active_zero_slope = True
        else:
            active_nonzero_square_cosets.add(coset_representative)

        for x in domain:
            slope = (x * x * shape_slope) % p
            packet_count_numerator += 1
            support_count_numerator += lift_count
            packet_slope_histogram_numerator[slope] += 1
            support_slope_histogram_numerator[slope] += lift_count

    numerators = [
        packet_count_numerator,
        support_count_numerator,
        *packet_slope_histogram_numerator.values(),
        *support_slope_histogram_numerator.values(),
    ]
    quotient_check = all(numerator % 6 == 0 for numerator in numerators)
    packet_slope_histogram = Counter(
        {
            slope: count // 6
            for slope, count in packet_slope_histogram_numerator.items()
        }
    )
    support_slope_histogram = Counter(
        {
            slope: count // 6
            for slope, count in support_slope_histogram_numerator.items()
        }
    )
    nonzero_shape_orbit_count = (
        (active_parameter_count - active_zero_parameter_count) // 6
    )
    square_coset_slope_bound = (
        (1 if active_zero_slope else 0)
        + nonzero_shape_orbit_count * (len(domain) // math.gcd(2, len(domain)))
    )
    square_coset_slope_count = (
        (1 if active_zero_slope else 0)
        + len(active_nonzero_square_cosets) * len(square_image)
    )
    abstract_square_coset_slope_count = (
        (1 if zero_slope else 0) + len(nonzero_square_cosets) * len(square_image)
    )
    return {
        "parameter_count": parameter_count,
        "active_parameter_count": active_parameter_count,
        "active_zero_parameter_count": active_zero_parameter_count,
        "nonzero_square_coset_count": len(nonzero_square_cosets),
        "active_nonzero_square_coset_count": len(active_nonzero_square_cosets),
        "total_nonzero_square_coset_count": total_nonzero_square_cosets,
        "square_image_size": len(square_image),
        "abstract_square_coset_slope_count": abstract_square_coset_slope_count,
        "square_coset_slope_count": square_coset_slope_count,
        "sixfold_quotient_check": quotient_check,
        "packet_count": packet_count_numerator // 6,
        "weighted_support_count": support_count_numerator // 6,
        "square_coset_slope_bound": min(p, square_coset_slope_bound),
        "packet_slope_histogram": packet_slope_histogram,
        "support_slope_histogram": support_slope_histogram,
    }


def second_superboundary_shape_coset_ledger(
    p: int,
    domain: Sequence[int],
    slack: int,
    support_size: int,
    quotient_order: int,
    fiber_size: int,
) -> Dict[str, object]:
    """Enumerate the normalized second-superboundary shape theorem."""

    value_to_index = {value: index for index, value in enumerate(domain)}
    residual_size = slack + 2
    orbit_factor = math.factorial(residual_size)
    parameter_count = 0
    active_parameter_count = 0
    zero_parameter_count = 0
    active_zero_parameter_count = 0
    packet_count_numerator = 0
    active_nonzero_packet_count_numerator = 0
    zero_packet_count_numerator = 0
    support_count_numerator = 0
    zero_support_count_numerator = 0
    packet_slope_histogram_numerator: Counter[int] = Counter()
    support_slope_histogram_numerator: Counter[int] = Counter()
    zero_slope = False
    active_zero_slope = False
    power_image = {pow(x, slack, p) for x in domain}
    nonzero_power_cosets = set()
    active_nonzero_power_cosets = set()
    total_nonzero_power_cosets = (p - 1) // len(power_image)
    whole_fibers = (
        (support_size - residual_size) // fiber_size
        if (
            support_size >= residual_size
            and (support_size - residual_size) % fiber_size == 0
        )
        else None
    )

    for tail in product(domain, repeat=slack + 1):
        values = (1, *tail)
        if len(set(values)) != residual_size:
            continue
        sym = elementary_symmetric_prefix(values, slack, p)
        if any(sym[degree] % p for degree in range(1, slack)):
            continue
        parameter_count += 1
        shape_slope = signed_symmetric_coefficient(values, slack, p)
        if shape_slope == 0:
            zero_parameter_count += 1
            zero_slope = True
            coset_representative = None
        else:
            coset_representative = min(
                (shape_slope * power) % p for power in power_image
            )
            nonzero_power_cosets.add(coset_representative)

        if whole_fibers is None:
            continue

        touched_fibers = len(
            {value_to_index[value] % quotient_order for value in values}
        )
        lift_count = expected_residual_packet_lift_count(
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            residual_size=residual_size,
            touched_fibers=touched_fibers,
        )
        if lift_count == 0:
            continue
        active_parameter_count += 1
        if shape_slope == 0:
            active_zero_parameter_count += 1
            active_zero_slope = True
        else:
            assert coset_representative is not None
            active_nonzero_power_cosets.add(coset_representative)

        for x in domain:
            slope = (pow(x, slack, p) * shape_slope) % p
            packet_count_numerator += 1
            if shape_slope != 0:
                active_nonzero_packet_count_numerator += 1
            else:
                zero_packet_count_numerator += 1
                zero_support_count_numerator += lift_count
            support_count_numerator += lift_count
            packet_slope_histogram_numerator[slope] += 1
            support_slope_histogram_numerator[slope] += lift_count

    numerators = [
        packet_count_numerator,
        support_count_numerator,
        *packet_slope_histogram_numerator.values(),
        *support_slope_histogram_numerator.values(),
    ]
    orbit_check = all(numerator % orbit_factor == 0 for numerator in numerators)
    packet_slope_histogram = Counter(
        {
            slope: count // orbit_factor
            for slope, count in packet_slope_histogram_numerator.items()
        }
    )
    support_slope_histogram = Counter(
        {
            slope: count // orbit_factor
            for slope, count in support_slope_histogram_numerator.items()
        }
    )
    active_nonzero_parameter_count = (
        active_parameter_count - active_zero_parameter_count
    )
    active_nonzero_packet_orbit_check = (
        active_nonzero_packet_count_numerator % orbit_factor == 0
    )
    active_nonzero_packet_orbit_count = (
        active_nonzero_packet_count_numerator // orbit_factor
        if active_nonzero_packet_orbit_check
        else active_nonzero_parameter_count
    )
    power_coset_slope_count = (
        (1 if active_zero_slope else 0)
        + len(active_nonzero_power_cosets) * len(power_image)
    )
    abstract_power_coset_slope_count = (
        (1 if zero_slope else 0) + len(nonzero_power_cosets) * len(power_image)
    )
    power_coset_slope_bound = (
        (1 if active_zero_slope else 0)
        + active_nonzero_packet_orbit_count * len(power_image)
    )
    next_slack_first_ledger = first_superboundary_shape_coset_ledger(
        p=p,
        domain=domain,
        slack=slack + 1,
        support_size=support_size,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
    )
    zero_packet_count = zero_packet_count_numerator // orbit_factor
    zero_weighted_support_count = zero_support_count_numerator // orbit_factor
    return {
        "residual_size": residual_size,
        "orbit_factor": orbit_factor,
        "parameter_count": parameter_count,
        "active_parameter_count": active_parameter_count,
        "zero_parameter_count": zero_parameter_count,
        "active_zero_parameter_count": active_zero_parameter_count,
        "active_nonzero_packet_orbit_check": active_nonzero_packet_orbit_check,
        "active_nonzero_packet_orbit_count": active_nonzero_packet_orbit_count,
        "nonzero_power_coset_count": len(nonzero_power_cosets),
        "active_nonzero_power_coset_count": len(active_nonzero_power_cosets),
        "total_nonzero_power_coset_count": total_nonzero_power_cosets,
        "power_image_size": len(power_image),
        "abstract_power_coset_slope_count": abstract_power_coset_slope_count,
        "power_coset_slope_count": power_coset_slope_count,
        "power_coset_slope_bound": min(p, power_coset_slope_bound),
        "orbit_quotient_check": orbit_check,
        "packet_count": packet_count_numerator // orbit_factor,
        "zero_packet_count": zero_packet_count,
        "weighted_support_count": support_count_numerator // orbit_factor,
        "zero_weighted_support_count": zero_weighted_support_count,
        "packet_slope_histogram": packet_slope_histogram,
        "support_slope_histogram": support_slope_histogram,
        "next_slack_first_parameter_count": int(
            next_slack_first_ledger["parameter_count"]
        ),
        "next_slack_first_active_parameter_count": int(
            next_slack_first_ledger["active_parameter_count"]
        ),
        "next_slack_first_packet_count": int(
            next_slack_first_ledger["packet_count"]
        ),
        "next_slack_first_weighted_support_count": int(
            next_slack_first_ledger["weighted_support_count"]
        ),
        "next_slack_transition_parameter_check": (
            zero_parameter_count == int(next_slack_first_ledger["parameter_count"])
        ),
        "next_slack_transition_active_parameter_check": (
            active_zero_parameter_count
            == int(next_slack_first_ledger["active_parameter_count"])
        ),
        "next_slack_transition_packet_count_check": (
            zero_packet_count == int(next_slack_first_ledger["packet_count"])
        ),
        "next_slack_transition_support_count_check": (
            zero_weighted_support_count
            == int(next_slack_first_ledger["weighted_support_count"])
        ),
    }


def slack_two_second_superboundary_shape_ledger(
    p: int,
    domain: Sequence[int],
    support_size: int,
    quotient_order: int,
    fiber_size: int,
) -> Dict[str, object]:
    domain_set = set(domain)
    value_to_index = {value: index for index, value in enumerate(domain)}
    parameter_count = 0
    active_parameter_count = 0
    zero_parameter_count = 0
    active_zero_parameter_count = 0
    packet_count_numerator = 0
    active_nonzero_packet_count_numerator = 0
    support_count_numerator = 0
    packet_slope_histogram_numerator: Counter[int] = Counter()
    support_slope_histogram_numerator: Counter[int] = Counter()
    zero_slope = False
    active_zero_slope = False
    nonzero_square_cosets = set()
    active_nonzero_square_cosets = set()
    square_image = {x * x % p for x in domain}
    total_nonzero_square_cosets = (p - 1) // len(square_image)
    residual_size = 4
    orbit_factor = math.factorial(residual_size)
    whole_fibers = (
        (support_size - residual_size) // fiber_size
        if (
            support_size >= residual_size
            and (support_size - residual_size) % fiber_size == 0
        )
        else None
    )
    remaining_fibers = (
        quotient_order - whole_fibers if whole_fibers is not None else None
    )
    lift_limited_parameter_bound = quotient_limited_pair_parameter_bound(
        quotient_order=quotient_order,
        fiber_size=fiber_size,
        remaining_fibers=remaining_fibers,
        residual_size=residual_size,
    )
    lift_limited_nonzero_packet_orbit_bound = (
        lift_limited_parameter_bound // orbit_factor
    )
    lift_limited_slope_bound = min(
        p,
        (1 if lift_limited_parameter_bound else 0)
        + lift_limited_nonzero_packet_orbit_bound * len(square_image),
    )
    kernel_fiber_reduction = (
        slack_two_second_kernel_fiber_reduction_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
        )
        if remaining_fibers == 1
        else None
    )

    for u in domain:
        for v in domain:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in domain_set or len(set(values)) != residual_size:
                continue
            parameter_count += 1
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                zero_parameter_count += 1
                zero_slope = True
                coset_representative = None
            else:
                coset_representative = min(
                    (shape_slope * square) % p for square in square_image
                )
                nonzero_square_cosets.add(coset_representative)

            if whole_fibers is None:
                continue

            touched_fibers = len(
                {value_to_index[value] % quotient_order for value in values}
            )
            lift_count = expected_residual_packet_lift_count(
                support_size=support_size,
                quotient_order=quotient_order,
                fiber_size=fiber_size,
                residual_size=residual_size,
                touched_fibers=touched_fibers,
            )
            if lift_count == 0:
                continue
            active_parameter_count += 1
            if shape_slope == 0:
                active_zero_parameter_count += 1
                active_zero_slope = True
            else:
                assert coset_representative is not None
                active_nonzero_square_cosets.add(coset_representative)

            for x in domain:
                slope = (x * x * shape_slope) % p
                packet_count_numerator += 1
                if shape_slope != 0:
                    active_nonzero_packet_count_numerator += 1
                support_count_numerator += lift_count
                packet_slope_histogram_numerator[slope] += 1
                support_slope_histogram_numerator[slope] += lift_count

    numerators = [
        packet_count_numerator,
        support_count_numerator,
        *packet_slope_histogram_numerator.values(),
        *support_slope_histogram_numerator.values(),
    ]
    quotient_check = all(numerator % orbit_factor == 0 for numerator in numerators)
    packet_slope_histogram = Counter(
        {
            slope: count // orbit_factor
            for slope, count in packet_slope_histogram_numerator.items()
        }
    )
    support_slope_histogram = Counter(
        {
            slope: count // orbit_factor
            for slope, count in support_slope_histogram_numerator.items()
        }
    )
    active_nonzero_parameter_count = (
        active_parameter_count - active_zero_parameter_count
    )
    active_nonzero_packet_orbit_check = (
        active_nonzero_packet_count_numerator % orbit_factor == 0
    )
    active_nonzero_packet_orbit_count = (
        active_nonzero_packet_count_numerator // orbit_factor
        if active_nonzero_packet_orbit_check
        else active_nonzero_parameter_count
    )
    square_coset_slope_count = (
        (1 if active_zero_slope else 0)
        + len(active_nonzero_square_cosets) * len(square_image)
    )
    abstract_square_coset_slope_count = (
        (1 if zero_slope else 0) + len(nonzero_square_cosets) * len(square_image)
    )
    square_coset_slope_bound = (
        (1 if active_zero_slope else 0)
        + active_nonzero_packet_orbit_count * len(square_image)
    )
    high_index_slope_bound = min(
        p,
        1 + len(domain) * len(domain) * len(square_image),
    )
    return {
        "residual_size": residual_size,
        "orbit_factor": orbit_factor,
        "parameter_count": parameter_count,
        "active_parameter_count": active_parameter_count,
        "zero_parameter_count": zero_parameter_count,
        "active_zero_parameter_count": active_zero_parameter_count,
        "active_nonzero_packet_orbit_check": active_nonzero_packet_orbit_check,
        "active_nonzero_packet_orbit_count": active_nonzero_packet_orbit_count,
        "nonzero_square_coset_count": len(nonzero_square_cosets),
        "active_nonzero_square_coset_count": len(active_nonzero_square_cosets),
        "total_nonzero_square_coset_count": total_nonzero_square_cosets,
        "square_image_size": len(square_image),
        "abstract_square_coset_slope_count": abstract_square_coset_slope_count,
        "square_coset_slope_count": square_coset_slope_count,
        "square_coset_slope_bound": min(p, square_coset_slope_bound),
        "high_index_slope_bound": high_index_slope_bound,
        "high_index_slope_bound_nontrivial": high_index_slope_bound < p,
        "lift_limited_remaining_fibers": remaining_fibers,
        "lift_limited_parameter_bound": lift_limited_parameter_bound,
        "lift_limited_nonzero_packet_orbit_bound": (
            lift_limited_nonzero_packet_orbit_bound
        ),
        "lift_limited_slope_bound": lift_limited_slope_bound,
        "lift_limited_slope_bound_nontrivial": lift_limited_slope_bound < p,
        "kernel_fiber_reduction_active": kernel_fiber_reduction is not None,
        "kernel_fiber_reduction": kernel_fiber_reduction,
        "twentyfourfold_quotient_check": quotient_check,
        "packet_count": packet_count_numerator // orbit_factor,
        "weighted_support_count": support_count_numerator // orbit_factor,
        "packet_slope_histogram": packet_slope_histogram,
        "support_slope_histogram": support_slope_histogram,
    }


def slack_three_split_cubic_beta_ledger(
    p: int,
    domain: Sequence[int],
) -> Dict[str, object]:
    beta_roots: Dict[int, set[int]] = {}
    for y in domain:
        if y == 1:
            continue
        beta = (-(pow(y, 3, p) + pow(y, 2, p) + y + 1)) % p
        beta_roots.setdefault(beta, set()).add(y)

    root_count_histogram: Counter[int] = Counter(
        len(roots) for roots in beta_roots.values()
    )
    admissible_beta_values = {
        beta
        for beta, roots in beta_roots.items()
        if len(roots) == 3
    }
    cube_image = {pow(x, 3, p) for x in domain}
    cube_coset_representative = multiplicative_coset_representative_map(
        p,
        tuple(cube_image),
    )
    nonzero_cube_coset_beta_values: Dict[int, set[int]] = {}
    for beta in admissible_beta_values:
        if beta == 0:
            continue
        representative = cube_coset_representative[beta]
        nonzero_cube_coset_beta_values.setdefault(
            representative,
            set(),
        ).add(beta)

    return {
        "candidate_beta_count": len(beta_roots),
        "beta_count": len(admissible_beta_values),
        "zero_beta_count": 1 if 0 in admissible_beta_values else 0,
        "parameter_count": 6 * len(admissible_beta_values),
        "root_count_histogram": {
            str(count): frequency
            for count, frequency in sorted(root_count_histogram.items())
        },
        "nonzero_cube_coset_count": len(nonzero_cube_coset_beta_values),
        "nonzero_cube_coset_beta_counts": sorted(
            len(values)
            for values in nonzero_cube_coset_beta_values.values()
        ),
        "total_nonzero_cube_coset_count": (p - 1) // len(cube_image),
        "cube_image_size": len(cube_image),
    }


def slack_three_first_superboundary_shape_ledger(
    p: int,
    domain: Sequence[int],
    support_size: int,
    quotient_order: int,
    fiber_size: int,
) -> Dict[str, object]:
    domain_set = set(domain)
    value_to_index = {value: index for index, value in enumerate(domain)}
    split_cubic_ledger = slack_three_split_cubic_beta_ledger(p, domain)
    parameter_count = 0
    active_parameter_count = 0
    active_zero_parameter_count = 0
    packet_count_numerator = 0
    support_count_numerator = 0
    packet_slope_histogram_numerator: Counter[int] = Counter()
    support_slope_histogram_numerator: Counter[int] = Counter()
    zero_slope = False
    beta_values = set()
    active_beta_values = set()
    nonzero_cube_cosets = set()
    nonzero_cube_coset_beta_values: Dict[int, set[int]] = {}
    active_zero_slope = False
    cube_image = {pow(x, 3, p) for x in domain}
    active_nonzero_cube_cosets = set()
    active_nonzero_cube_coset_beta_values: Dict[int, set[int]] = {}
    total_nonzero_cube_cosets = (p - 1) // len(cube_image)
    whole_fibers = (
        (support_size - 4) // fiber_size
        if support_size >= 4 and (support_size - 4) % fiber_size == 0
        else None
    )

    for u in domain:
        for v in domain:
            w = (-1 - u - v) % p
            if w not in domain_set:
                continue
            if len({1, u, v, w}) != 4:
                continue
            if (u * u + v * v + u * v + u + v + 1) % p:
                continue
            parameter_count += 1
            shape_slope = (-(1 + u * v * w)) % p
            beta_values.add(shape_slope)
            if shape_slope == 0:
                zero_slope = True
            else:
                coset_representative = min(
                    (shape_slope * cube) % p for cube in cube_image
                )
                nonzero_cube_cosets.add(coset_representative)
                nonzero_cube_coset_beta_values.setdefault(
                    coset_representative,
                    set(),
                ).add(shape_slope)

            if whole_fibers is None:
                continue

            touched_fibers = len(
                {
                    0,
                    value_to_index[u] % quotient_order,
                    value_to_index[v] % quotient_order,
                    value_to_index[w] % quotient_order,
                }
            )
            if whole_fibers > quotient_order - touched_fibers:
                lift_count = 0
            else:
                lift_count = math.comb(
                    quotient_order - touched_fibers,
                    whole_fibers,
                )
            if lift_count == 0:
                continue
            active_parameter_count += 1
            active_beta_values.add(shape_slope)
            if shape_slope == 0:
                active_zero_parameter_count += 1
                active_zero_slope = True
            else:
                active_nonzero_cube_cosets.add(coset_representative)
                active_nonzero_cube_coset_beta_values.setdefault(
                    coset_representative,
                    set(),
                ).add(shape_slope)

            for x in domain:
                slope = (pow(x, 3, p) * shape_slope) % p
                packet_count_numerator += 1
                support_count_numerator += lift_count
                packet_slope_histogram_numerator[slope] += 1
                support_slope_histogram_numerator[slope] += lift_count

    numerators = [
        packet_count_numerator,
        support_count_numerator,
        *packet_slope_histogram_numerator.values(),
        *support_slope_histogram_numerator.values(),
    ]
    quotient_check = all(numerator % 24 == 0 for numerator in numerators)
    packet_slope_histogram = Counter(
        {
            slope: count // 24
            for slope, count in packet_slope_histogram_numerator.items()
        }
    )
    support_slope_histogram = Counter(
        {
            slope: count // 24
            for slope, count in support_slope_histogram_numerator.items()
        }
    )
    cube_coset_slope_count = (
        (1 if active_zero_slope else 0)
        + len(active_nonzero_cube_cosets) * len(cube_image)
    )
    abstract_cube_coset_slope_count = (
        (1 if zero_slope else 0) + len(nonzero_cube_cosets) * len(cube_image)
    )
    nonzero_cube_coset_beta_counts = sorted(
        len(values) for values in nonzero_cube_coset_beta_values.values()
    )
    active_nonzero_cube_coset_beta_counts = sorted(
        len(values) for values in active_nonzero_cube_coset_beta_values.values()
    )
    return {
        "parameter_count": parameter_count,
        "active_parameter_count": active_parameter_count,
        "active_zero_parameter_count": active_zero_parameter_count,
        "beta_count": len(beta_values),
        "active_beta_count": len(active_beta_values),
        "beta_parameter_count_check": parameter_count == 6 * len(beta_values),
        "active_beta_parameter_count_check": (
            active_parameter_count == 6 * len(active_beta_values)
        ),
        "nonzero_cube_coset_count": len(nonzero_cube_cosets),
        "active_nonzero_cube_coset_count": len(active_nonzero_cube_cosets),
        "nonzero_cube_coset_beta_counts": nonzero_cube_coset_beta_counts,
        "active_nonzero_cube_coset_beta_counts": (
            active_nonzero_cube_coset_beta_counts
        ),
        "split_cubic_candidate_beta_count": int(
            split_cubic_ledger["candidate_beta_count"]
        ),
        "split_cubic_beta_count": int(split_cubic_ledger["beta_count"]),
        "split_cubic_zero_beta_count": int(
            split_cubic_ledger["zero_beta_count"]
        ),
        "split_cubic_parameter_count": int(
            split_cubic_ledger["parameter_count"]
        ),
        "split_cubic_root_count_histogram": (
            split_cubic_ledger["root_count_histogram"]
        ),
        "split_cubic_nonzero_cube_coset_count": int(
            split_cubic_ledger["nonzero_cube_coset_count"]
        ),
        "split_cubic_nonzero_cube_coset_beta_counts": (
            split_cubic_ledger["nonzero_cube_coset_beta_counts"]
        ),
        "split_cubic_parameter_count_check": (
            parameter_count == int(split_cubic_ledger["parameter_count"])
        ),
        "split_cubic_beta_count_check": (
            len(beta_values) == int(split_cubic_ledger["beta_count"])
        ),
        "split_cubic_zero_beta_count_check": (
            (1 if zero_slope else 0)
            == int(split_cubic_ledger["zero_beta_count"])
        ),
        "split_cubic_cube_coset_count_check": (
            len(nonzero_cube_cosets)
            == int(split_cubic_ledger["nonzero_cube_coset_count"])
        ),
        "split_cubic_cube_coset_beta_counts_check": (
            nonzero_cube_coset_beta_counts
            == split_cubic_ledger["nonzero_cube_coset_beta_counts"]
        ),
        "total_nonzero_cube_coset_count": total_nonzero_cube_cosets,
        "cube_image_size": len(cube_image),
        "abstract_cube_coset_slope_count": abstract_cube_coset_slope_count,
        "cube_coset_slope_count": cube_coset_slope_count,
        "twentyfourfold_quotient_check": quotient_check,
        "packet_count": packet_count_numerator // 24,
        "weighted_support_count": support_count_numerator // 24,
        "packet_slope_histogram": packet_slope_histogram,
        "support_slope_histogram": support_slope_histogram,
    }


def ceil_sqrt(value: int) -> int:
    root = math.isqrt(value)
    if root * root < value:
        root += 1
    return root


def slack_two_cyclotomic_shape_bound(p: int, domain_order: int) -> int:
    character_order = (p - 1) // domain_order
    ceil_sqrt_p = ceil_sqrt(p)
    numerator = p - 2 + (character_order * character_order - 1) * ceil_sqrt_p
    return (numerator + character_order * character_order - 1) // (
        character_order * character_order
    )


def fixed_window_active_character_l1_bound(
    quotient_order: int,
    window_size: int,
    ambient_restriction_kernel_count: int,
) -> int:
    """Bound one-dimensional nonprincipal L1 for a fixed quotient window."""

    if (
        quotient_order < 1
        or window_size < 1
        or ambient_restriction_kernel_count < 1
    ):
        return 0
    quotient_nonprincipal_l1_bound = ceil_sqrt(
        (quotient_order - 1) * window_size * (quotient_order - window_size)
    )
    return (
        (ambient_restriction_kernel_count - 1) * window_size
        + ambient_restriction_kernel_count * quotient_nonprincipal_l1_bound
    )


def fixed_window_active_coordinate_l1_bounds(
    window_size: int,
    active_character_l1_bound: int,
) -> Tuple[int, int, int]:
    """Split a fixed-window tensor L1 bound by active coordinate count."""

    return (
        3 * window_size * window_size * active_character_l1_bound,
        3 * window_size * active_character_l1_bound * active_character_l1_bound,
        active_character_l1_bound ** 3,
    )


def depth_two_kummer_error_l1_split(
    coordinate_principal_weight: int,
    coordinate_nonprincipal_l1_bound: int,
    square_coset_index: int,
    nonprincipal_constant: int,
    coordinate_one_nonprincipal_l1_bound: int = 0,
    coordinate_two_nonprincipal_l1_bound: int = 0,
    coordinate_three_nonprincipal_l1_bound: int = 0,
    quadratic_one_coordinate_constant: int = 4,
    one_coordinate_kummer_constant: int = 4,
    two_coordinate_kummer_constant: int = 9,
    two_coordinate_infinity_unramified_l1_bound: int = 0,
    two_coordinate_infinity_unramified_constant: int = 2,
    two_coordinate_infinity_unramified_sqrt_constant: int = 5,
    two_coordinate_projective_reciprocal_l1_bound: int = 0,
    two_coordinate_projective_reciprocal_constant: int = 4,
    two_coordinate_projective_reciprocal_sqrt_constant: int = 3,
    two_coordinate_equal_line_l1_bound: int = 0,
    two_coordinate_equal_line_constant: int = 4,
    two_coordinate_equal_line_sqrt_constant: int = 3,
    two_coordinate_coordinate_diagonal_l1_bound: int = 0,
    two_coordinate_coordinate_diagonal_constant: int = 4,
    two_coordinate_coordinate_diagonal_sqrt_constant: int = 3,
    two_coordinate_projective_equal_pair_l1_bound: int = 0,
    two_coordinate_projective_equal_pair_constant: int = 4,
    two_coordinate_projective_equal_pair_sqrt_constant: int = 3,
    two_coordinate_projective_asymmetric_nonresonant_l1_bound: int = 0,
    two_coordinate_projective_asymmetric_nonresonant_constant: int = 4,
    two_coordinate_projective_asymmetric_nonresonant_sqrt_constant: int = 3,
    two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound: int = 0,
    two_coordinate_projective_asymmetric_line_conic_resonant_constant: int = 4,
    two_coordinate_projective_asymmetric_line_conic_resonant_sqrt_constant: int = 3,
) -> Dict[str, int]:
    """Split depth-two character error into proved and imported masses."""

    jacobi_l1_bound = coordinate_nonprincipal_l1_bound
    conic_l1_bound = coordinate_principal_weight * (square_coset_index - 1)
    quadratic_conic_character_count = (
        1 if square_coset_index > 1 and square_coset_index % 2 == 0 else 0
    )
    quadratic_one_coordinate_l1_bound = (
        coordinate_one_nonprincipal_l1_bound
        * quadratic_conic_character_count
    )
    active_coordinate_l1_bound = (
        coordinate_one_nonprincipal_l1_bound
        + coordinate_two_nonprincipal_l1_bound
        + coordinate_three_nonprincipal_l1_bound
    )
    if active_coordinate_l1_bound != coordinate_nonprincipal_l1_bound:
        raise ValueError(
            "active-coordinate L1 masses must sum to the nonprincipal L1"
        )
    one_coordinate_kummer_l1_bound = (
        coordinate_one_nonprincipal_l1_bound
        * (square_coset_index - 1 - quadratic_conic_character_count)
    )
    two_coordinate_kummer_l1_bound = (
        coordinate_two_nonprincipal_l1_bound * (square_coset_index - 1)
    )
    if not 0 <= two_coordinate_infinity_unramified_l1_bound <= (
        two_coordinate_kummer_l1_bound
    ):
        raise ValueError("invalid infinity-unramified two-coordinate L1 split")
    two_coordinate_ramified_l1_bound = (
        two_coordinate_kummer_l1_bound
        - two_coordinate_infinity_unramified_l1_bound
    )
    if not 0 <= two_coordinate_projective_reciprocal_l1_bound <= (
        two_coordinate_ramified_l1_bound
    ):
        raise ValueError("invalid projective-reciprocal two-coordinate L1 split")
    two_coordinate_ramified_nonreciprocal_l1_bound = (
        two_coordinate_ramified_l1_bound
        - two_coordinate_projective_reciprocal_l1_bound
    )
    if not 0 <= two_coordinate_equal_line_l1_bound <= (
        two_coordinate_ramified_nonreciprocal_l1_bound
    ):
        raise ValueError("invalid equal-line two-coordinate L1 split")
    if not 0 <= two_coordinate_coordinate_diagonal_l1_bound <= (
        two_coordinate_ramified_nonreciprocal_l1_bound
    ):
        raise ValueError("invalid coordinate-diagonal two-coordinate L1 split")
    if two_coordinate_projective_equal_pair_l1_bound == 0:
        two_coordinate_projective_equal_pair_l1_bound = (
            two_coordinate_coordinate_diagonal_l1_bound
        )
    if not 0 <= two_coordinate_projective_equal_pair_l1_bound <= (
        two_coordinate_ramified_nonreciprocal_l1_bound
    ):
        raise ValueError("invalid projective-equal two-coordinate L1 split")
    if two_coordinate_equal_line_l1_bound > (
        two_coordinate_coordinate_diagonal_l1_bound
    ):
        raise ValueError("equal-line L1 mass cannot exceed coordinate diagonal")
    if two_coordinate_coordinate_diagonal_l1_bound > (
        two_coordinate_projective_equal_pair_l1_bound
    ):
        raise ValueError("coordinate diagonal cannot exceed projective-equal")
    two_coordinate_projective_asymmetric_l1_bound = (
        two_coordinate_ramified_nonreciprocal_l1_bound
        - two_coordinate_projective_equal_pair_l1_bound
    )
    if not 0 <= two_coordinate_projective_asymmetric_nonresonant_l1_bound <= (
        two_coordinate_projective_asymmetric_l1_bound
    ):
        raise ValueError("invalid asymmetric-nonresonant two-coordinate L1 split")
    if not 0 <= (
        two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound
    ) <= two_coordinate_projective_asymmetric_l1_bound:
        raise ValueError("invalid asymmetric line-conic resonant L1 split")
    if (
        two_coordinate_projective_asymmetric_nonresonant_l1_bound
        + two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound
        > two_coordinate_projective_asymmetric_l1_bound
    ):
        raise ValueError("asymmetric line-conic split exceeds total mass")
    three_coordinate_kummer_l1_bound = (
        coordinate_three_nonprincipal_l1_bound * (square_coset_index - 1)
    )
    kummer_l1_bound = (
        one_coordinate_kummer_l1_bound
        + two_coordinate_kummer_l1_bound
        + three_coordinate_kummer_l1_bound
    )
    weighted_error_l1_bound = (
        jacobi_l1_bound
        + conic_l1_bound
        + quadratic_one_coordinate_constant * quadratic_one_coordinate_l1_bound
        + one_coordinate_kummer_constant * one_coordinate_kummer_l1_bound
        + two_coordinate_infinity_unramified_constant
        * two_coordinate_infinity_unramified_l1_bound
        + two_coordinate_projective_reciprocal_constant
        * two_coordinate_projective_reciprocal_l1_bound
        + two_coordinate_kummer_constant
        * two_coordinate_ramified_nonreciprocal_l1_bound
        + nonprincipal_constant * three_coordinate_kummer_l1_bound
    )
    equal_line_leading_l1_drop = (
        (two_coordinate_kummer_constant - two_coordinate_equal_line_constant)
        * two_coordinate_equal_line_l1_bound
    )
    equal_line_conditional_weighted_error_l1_bound = (
        weighted_error_l1_bound - equal_line_leading_l1_drop
    )
    coordinate_diagonal_leading_l1_drop = (
        (
            two_coordinate_kummer_constant
            - two_coordinate_coordinate_diagonal_constant
        )
        * two_coordinate_coordinate_diagonal_l1_bound
    )
    coordinate_diagonal_conditional_weighted_error_l1_bound = (
        weighted_error_l1_bound - coordinate_diagonal_leading_l1_drop
    )
    projective_equal_pair_leading_l1_drop = (
        (two_coordinate_kummer_constant - two_coordinate_projective_equal_pair_constant)
        * two_coordinate_projective_equal_pair_l1_bound
    )
    projective_equal_pair_conditional_weighted_error_l1_bound = (
        weighted_error_l1_bound - projective_equal_pair_leading_l1_drop
    )
    projective_asymmetric_nonresonant_leading_l1_drop = (
        (
            two_coordinate_kummer_constant
            - two_coordinate_projective_asymmetric_nonresonant_constant
        )
        * two_coordinate_projective_asymmetric_nonresonant_l1_bound
    )
    projective_equal_pair_nonresonant_conditional_weighted_error_l1_bound = (
        weighted_error_l1_bound
        - projective_equal_pair_leading_l1_drop
        - projective_asymmetric_nonresonant_leading_l1_drop
    )
    projective_asymmetric_line_conic_resonant_leading_l1_drop = (
        (
            two_coordinate_kummer_constant
            - two_coordinate_projective_asymmetric_line_conic_resonant_constant
        )
        * two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound
    )
    projective_equal_pair_all_asymmetric_conditional_weighted_error_l1_bound = (
        weighted_error_l1_bound
        - projective_equal_pair_leading_l1_drop
        - projective_asymmetric_nonresonant_leading_l1_drop
        - projective_asymmetric_line_conic_resonant_leading_l1_drop
    )
    two_coordinate_infinity_unramified_sqrt_l1_bound = (
        two_coordinate_infinity_unramified_sqrt_constant
        * two_coordinate_infinity_unramified_l1_bound
    )
    two_coordinate_projective_reciprocal_sqrt_l1_bound = (
        two_coordinate_projective_reciprocal_sqrt_constant
        * two_coordinate_projective_reciprocal_l1_bound
    )
    two_coordinate_equal_line_sqrt_l1_bound = (
        two_coordinate_equal_line_sqrt_constant
        * two_coordinate_equal_line_l1_bound
    )
    two_coordinate_coordinate_diagonal_sqrt_l1_bound = (
        two_coordinate_coordinate_diagonal_sqrt_constant
        * two_coordinate_coordinate_diagonal_l1_bound
    )
    two_coordinate_projective_equal_pair_sqrt_l1_bound = (
        two_coordinate_projective_equal_pair_sqrt_constant
        * two_coordinate_projective_equal_pair_l1_bound
    )
    two_coordinate_projective_asymmetric_nonresonant_sqrt_l1_bound = (
        two_coordinate_projective_asymmetric_nonresonant_sqrt_constant
        * two_coordinate_projective_asymmetric_nonresonant_l1_bound
    )
    two_coordinate_projective_asymmetric_line_conic_resonant_sqrt_l1_bound = (
        two_coordinate_projective_asymmetric_line_conic_resonant_sqrt_constant
        * two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound
    )
    return {
        "jacobi_l1_bound": jacobi_l1_bound,
        "conic_l1_bound": conic_l1_bound,
        "quadratic_one_coordinate_l1_bound": (
            quadratic_one_coordinate_l1_bound
        ),
        "quadratic_one_coordinate_error_constant": (
            quadratic_one_coordinate_constant
        ),
        "one_coordinate_kummer_l1_bound": one_coordinate_kummer_l1_bound,
        "one_coordinate_kummer_error_constant": (
            one_coordinate_kummer_constant
        ),
        "two_coordinate_kummer_l1_bound": two_coordinate_kummer_l1_bound,
        "two_coordinate_kummer_error_constant": (
            two_coordinate_kummer_constant
        ),
        "two_coordinate_infinity_unramified_l1_bound": (
            two_coordinate_infinity_unramified_l1_bound
        ),
        "two_coordinate_infinity_unramified_error_constant": (
            two_coordinate_infinity_unramified_constant
        ),
        "two_coordinate_infinity_unramified_sqrt_constant": (
            two_coordinate_infinity_unramified_sqrt_constant
        ),
        "two_coordinate_infinity_unramified_sqrt_l1_bound": (
            two_coordinate_infinity_unramified_sqrt_l1_bound
        ),
        "two_coordinate_ramified_l1_bound": two_coordinate_ramified_l1_bound,
        "two_coordinate_projective_reciprocal_l1_bound": (
            two_coordinate_projective_reciprocal_l1_bound
        ),
        "two_coordinate_projective_reciprocal_error_constant": (
            two_coordinate_projective_reciprocal_constant
        ),
        "two_coordinate_projective_reciprocal_sqrt_constant": (
            two_coordinate_projective_reciprocal_sqrt_constant
        ),
        "two_coordinate_projective_reciprocal_sqrt_l1_bound": (
            two_coordinate_projective_reciprocal_sqrt_l1_bound
        ),
        "two_coordinate_ramified_nonreciprocal_l1_bound": (
            two_coordinate_ramified_nonreciprocal_l1_bound
        ),
        "two_coordinate_equal_line_l1_bound": (
            two_coordinate_equal_line_l1_bound
        ),
        "two_coordinate_equal_line_error_constant": (
            two_coordinate_equal_line_constant
        ),
        "two_coordinate_equal_line_sqrt_constant": (
            two_coordinate_equal_line_sqrt_constant
        ),
        "two_coordinate_equal_line_leading_l1_drop": (
            equal_line_leading_l1_drop
        ),
        "two_coordinate_equal_line_sqrt_l1_bound": (
            two_coordinate_equal_line_sqrt_l1_bound
        ),
        "two_coordinate_coordinate_diagonal_l1_bound": (
            two_coordinate_coordinate_diagonal_l1_bound
        ),
        "two_coordinate_coordinate_diagonal_error_constant": (
            two_coordinate_coordinate_diagonal_constant
        ),
        "two_coordinate_coordinate_diagonal_sqrt_constant": (
            two_coordinate_coordinate_diagonal_sqrt_constant
        ),
        "two_coordinate_coordinate_diagonal_leading_l1_drop": (
            coordinate_diagonal_leading_l1_drop
        ),
        "two_coordinate_coordinate_diagonal_sqrt_l1_bound": (
            two_coordinate_coordinate_diagonal_sqrt_l1_bound
        ),
        "two_coordinate_projective_equal_pair_l1_bound": (
            two_coordinate_projective_equal_pair_l1_bound
        ),
        "two_coordinate_projective_equal_pair_error_constant": (
            two_coordinate_projective_equal_pair_constant
        ),
        "two_coordinate_projective_equal_pair_sqrt_constant": (
            two_coordinate_projective_equal_pair_sqrt_constant
        ),
        "two_coordinate_projective_equal_pair_leading_l1_drop": (
            projective_equal_pair_leading_l1_drop
        ),
        "two_coordinate_projective_equal_pair_sqrt_l1_bound": (
            two_coordinate_projective_equal_pair_sqrt_l1_bound
        ),
        "two_coordinate_projective_asymmetric_nonresonant_l1_bound": (
            two_coordinate_projective_asymmetric_nonresonant_l1_bound
        ),
        "two_coordinate_projective_asymmetric_nonresonant_error_constant": (
            two_coordinate_projective_asymmetric_nonresonant_constant
        ),
        "two_coordinate_projective_asymmetric_nonresonant_sqrt_constant": (
            two_coordinate_projective_asymmetric_nonresonant_sqrt_constant
        ),
        (
            "two_coordinate_projective_asymmetric_nonresonant_"
            "leading_l1_drop"
        ): projective_asymmetric_nonresonant_leading_l1_drop,
        (
            "two_coordinate_projective_asymmetric_nonresonant_"
            "sqrt_l1_bound"
        ): two_coordinate_projective_asymmetric_nonresonant_sqrt_l1_bound,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_l1_bound"
        ): two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_error_constant"
        ): two_coordinate_projective_asymmetric_line_conic_resonant_constant,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_sqrt_constant"
        ): two_coordinate_projective_asymmetric_line_conic_resonant_sqrt_constant,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_leading_l1_drop"
        ): projective_asymmetric_line_conic_resonant_leading_l1_drop,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_sqrt_l1_bound"
        ): two_coordinate_projective_asymmetric_line_conic_resonant_sqrt_l1_bound,
        "three_coordinate_kummer_l1_bound": three_coordinate_kummer_l1_bound,
        "three_coordinate_kummer_error_constant": nonprincipal_constant,
        "kummer_l1_bound": kummer_l1_bound,
        "weighted_error_l1_bound": weighted_error_l1_bound,
        "equal_line_conditional_weighted_error_l1_bound": (
            equal_line_conditional_weighted_error_l1_bound
        ),
        "coordinate_diagonal_conditional_weighted_error_l1_bound": (
            coordinate_diagonal_conditional_weighted_error_l1_bound
        ),
        "projective_equal_pair_conditional_weighted_error_l1_bound": (
            projective_equal_pair_conditional_weighted_error_l1_bound
        ),
        (
            "projective_equal_pair_nonresonant_conditional_"
            "weighted_error_l1_bound"
        ): projective_equal_pair_nonresonant_conditional_weighted_error_l1_bound,
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "weighted_error_l1_bound"
        ): projective_equal_pair_all_asymmetric_conditional_weighted_error_l1_bound,
    }


def depth_two_open_sqrt_error_bound(
    p: int,
    error_split: Dict[str, int],
) -> int:
    """Return the extra open-set removal term for elementary depth-two masses."""

    elementary_open_l1_bound = (
        int(error_split["jacobi_l1_bound"])
        + int(error_split["conic_l1_bound"])
    )
    infinity_unramified_sqrt_l1_bound = int(
        error_split.get("two_coordinate_infinity_unramified_sqrt_l1_bound", 0)
    )
    projective_reciprocal_sqrt_l1_bound = int(
        error_split.get("two_coordinate_projective_reciprocal_sqrt_l1_bound", 0)
    )
    return ceil_sqrt(p) * (
        6 * elementary_open_l1_bound
        + infinity_unramified_sqrt_l1_bound
        + projective_reciprocal_sqrt_l1_bound
    )


def raw_two_coordinate_projective_l1_split_formula(
    character_order: int,
    square_coset_index: int,
) -> Dict[str, int]:
    """Closed-form raw two-coordinate projective line-monodromy split."""

    if character_order < 1 or square_coset_index % character_order:
        raise ValueError((character_order, square_coset_index))
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
        raise ValueError((character_order, square_coset_index, lift))
    total = (e - 1) * (e - 1) * (q - 1)
    ramified_nonreciprocal = (
        total - infinity_unramified - projective_reciprocal
    )
    equal_line_diagonal = equal_line_diagonal_pair_count_formula(
        character_order,
        square_coset_index,
    )
    coordinate_diagonal = coordinate_diagonal_pair_count(
        character_order,
        square_coset_index,
    )
    projective_equal_pair = projective_equal_pair_count(
        character_order,
        square_coset_index,
    )
    line_conic_resonant = asymmetric_line_conic_resonant_pair_count_formula(
        character_order,
        square_coset_index,
    )
    diagonal_failures = coordinate_diagonal_parameter_failure_counts(
        character_order,
        square_coset_index,
    )
    if equal_line_diagonal > coordinate_diagonal:
        raise ValueError(
            (character_order, square_coset_index, equal_line_diagonal)
        )
    if coordinate_diagonal > projective_equal_pair:
        raise ValueError(
            (character_order, square_coset_index, projective_equal_pair)
        )
    if any(diagonal_failures.values()):
        raise ValueError(
            (character_order, square_coset_index, diagonal_failures)
        )
    active_pair_count = 3
    projective_asymmetric = ramified_nonreciprocal - projective_equal_pair
    if projective_asymmetric < 0 or projective_asymmetric % 2:
        raise ValueError(
            (character_order, square_coset_index, projective_asymmetric)
        )
    if line_conic_resonant > projective_asymmetric:
        raise ValueError(
            (character_order, square_coset_index, line_conic_resonant)
        )
    line_conic_nonresonant = projective_asymmetric - line_conic_resonant
    return {
        "two_coordinate_infinity_unramified_l1_bound": (
            active_pair_count * infinity_unramified
        ),
        "two_coordinate_projective_reciprocal_l1_bound": (
            active_pair_count * projective_reciprocal
        ),
        "two_coordinate_ramified_nonreciprocal_l1_bound": (
            active_pair_count * ramified_nonreciprocal
        ),
        "two_coordinate_equal_line_l1_bound": (
            active_pair_count * equal_line_diagonal
        ),
        "two_coordinate_coordinate_diagonal_l1_bound": (
            active_pair_count * coordinate_diagonal
        ),
        "two_coordinate_coordinate_diagonal_non_equal_l1_bound": (
            active_pair_count * (coordinate_diagonal - equal_line_diagonal)
        ),
        "two_coordinate_projective_equal_pair_l1_bound": (
            active_pair_count * projective_equal_pair
        ),
        "two_coordinate_projective_equal_pair_non_coordinate_l1_bound": (
            active_pair_count * (projective_equal_pair - coordinate_diagonal)
        ),
        "two_coordinate_projective_asymmetric_l1_bound": (
            active_pair_count * projective_asymmetric
        ),
        "two_coordinate_projective_asymmetric_orbit_count": (
            active_pair_count * projective_asymmetric // 6
        ),
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_l1_bound"
        ): active_pair_count * line_conic_resonant,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "nonresonant_l1_bound"
        ): active_pair_count * line_conic_nonresonant,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_orbit_count"
        ): active_pair_count * line_conic_resonant // 6,
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "nonresonant_orbit_count"
        ): active_pair_count * line_conic_nonresonant // 6,
        "two_coordinate_coordinate_diagonal_alpha_square_trivial_count": 0,
        "two_coordinate_coordinate_diagonal_2f1_cancellation_count": 0,
    }


def coordinate_diagonal_parameter_failure_counts(
    character_order: int,
    square_coset_index: int,
) -> Dict[str, int]:
    """Return forbidden parameter counts in the diagonal ramified slice."""

    if character_order < 1 or square_coset_index % character_order:
        raise ValueError((character_order, square_coset_index))
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


def coordinate_diagonal_pair_count(
    character_order: int,
    square_coset_index: int,
) -> int:
    """Count ramified nonreciprocal diagonal terms for one active pair."""

    if character_order < 1 or square_coset_index % character_order:
        raise ValueError((character_order, square_coset_index))
    e = character_order
    q = square_coset_index
    lift = q // e
    count = 0
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
            count += 1
    return count


def coordinate_diagonal_pair_count_formula(
    character_order: int,
    square_coset_index: int,
) -> int:
    """Closed form for coordinate_diagonal_pair_count."""

    if character_order < 1 or square_coset_index % character_order:
        raise ValueError((character_order, square_coset_index))
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
    raise ValueError((character_order, square_coset_index, lift))


def projective_equal_pair_count(
    character_order: int,
    square_coset_index: int,
) -> int:
    """Count ramified terms with some equal projective line pair."""

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
    """Count asymmetric line-conic resonances for one active pair."""

    if character_order < 1 or square_coset_index % character_order:
        raise ValueError((character_order, square_coset_index))
    e = character_order
    lift = square_coset_index // e
    if lift not in (1, 2):
        raise ValueError((character_order, square_coset_index, lift))
    single_line_count = (e - 1) * (e - 5)
    if e % 2 == 0:
        single_line_count += 3
    single_line_count += 2 * (math.gcd(e, 3) - 1)
    return 3 * single_line_count


def equal_line_diagonal_pair_count_formula(
    character_order: int,
    square_coset_index: int,
) -> int:
    """Count equal-line diagonal terms for one active coordinate pair."""

    if character_order < 1 or square_coset_index % character_order:
        raise ValueError((character_order, square_coset_index))
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
    raise ValueError((character_order, square_coset_index, lift))


def raw_two_coordinate_projective_l1_split(
    character_order: int,
    square_coset_index: int,
) -> Dict[str, int]:
    """Split raw two-coordinate terms by projective line monodromy."""

    return raw_two_coordinate_projective_l1_split_formula(
        character_order,
        square_coset_index,
    )


def raw_two_coordinate_infinity_unramified_l1_bound(
    character_order: int,
    square_coset_index: int,
) -> int:
    """Count raw two-coordinate terms with trivial infinity monodromy."""

    return raw_two_coordinate_projective_l1_split(
        character_order,
        square_coset_index,
    )["two_coordinate_infinity_unramified_l1_bound"]


def slack_two_second_kummer_saturation_data(
    p: int,
    domain_order: int,
    nonprincipal_constant: int = 16,
) -> Dict[str, object]:
    """Return the depth-two low-index square-coset saturation certificate."""

    character_order = (p - 1) // domain_order
    square_kernel_index = math.gcd(2, domain_order)
    square_coset_index = character_order * square_kernel_index
    denominator = (
        character_order
        * character_order
        * character_order
        * square_coset_index
    )
    nonprincipal_tuple_count = denominator - 1
    radical_component_degrees = (1, 1, 1, 2)
    radical_total_degree = sum(radical_component_degrees)
    deligne_constant = (radical_total_degree - 1) ** 2
    coefficient_l1_bound = nonprincipal_tuple_count
    two_coordinate_projective_split = raw_two_coordinate_projective_l1_split(
        character_order,
        square_coset_index,
    )
    error_split = depth_two_kummer_error_l1_split(
        coordinate_principal_weight=1,
        coordinate_nonprincipal_l1_bound=character_order ** 3 - 1,
        square_coset_index=square_coset_index,
        nonprincipal_constant=nonprincipal_constant,
        coordinate_one_nonprincipal_l1_bound=3 * (character_order - 1),
        coordinate_two_nonprincipal_l1_bound=(
            3 * (character_order - 1) ** 2
        ),
        coordinate_three_nonprincipal_l1_bound=(
            (character_order - 1) ** 3
        ),
        two_coordinate_infinity_unramified_l1_bound=int(
            two_coordinate_projective_split[
                "two_coordinate_infinity_unramified_l1_bound"
            ]
        ),
        two_coordinate_projective_reciprocal_l1_bound=int(
            two_coordinate_projective_split[
                "two_coordinate_projective_reciprocal_l1_bound"
            ]
        ),
        two_coordinate_equal_line_l1_bound=int(
            two_coordinate_projective_split[
                "two_coordinate_equal_line_l1_bound"
            ]
        ),
        two_coordinate_coordinate_diagonal_l1_bound=int(
            two_coordinate_projective_split[
                "two_coordinate_coordinate_diagonal_l1_bound"
            ]
        ),
        two_coordinate_projective_equal_pair_l1_bound=int(
            two_coordinate_projective_split[
                "two_coordinate_projective_equal_pair_l1_bound"
            ]
        ),
        two_coordinate_projective_asymmetric_nonresonant_l1_bound=int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_line_conic_"
                "nonresonant_l1_bound"
            ]
        ),
        two_coordinate_projective_asymmetric_line_conic_resonant_l1_bound=int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_l1_bound"
            ]
        ),
    )
    open_sqrt_error_bound = depth_two_open_sqrt_error_bound(
        p,
        error_split,
    )
    elementary_open_sqrt_weight = 6 * (
        int(error_split["jacobi_l1_bound"])
        + int(error_split["conic_l1_bound"])
    )
    total_sqrt_weight = (
        elementary_open_sqrt_weight
        + int(error_split["two_coordinate_infinity_unramified_sqrt_l1_bound"])
        + int(error_split["two_coordinate_projective_reciprocal_sqrt_l1_bound"])
    )
    equal_line_conditional_sqrt_weight = (
        total_sqrt_weight
        + int(error_split["two_coordinate_equal_line_sqrt_l1_bound"])
    )
    equal_line_conditional_sqrt_error_bound = (
        ceil_sqrt(p) * equal_line_conditional_sqrt_weight
    )
    coordinate_diagonal_conditional_sqrt_weight = (
        total_sqrt_weight
        + int(
            error_split[
                "two_coordinate_coordinate_diagonal_sqrt_l1_bound"
            ]
        )
    )
    coordinate_diagonal_conditional_sqrt_error_bound = (
        ceil_sqrt(p) * coordinate_diagonal_conditional_sqrt_weight
    )
    projective_equal_pair_conditional_sqrt_weight = (
        total_sqrt_weight
        + int(
            error_split[
                "two_coordinate_projective_equal_pair_sqrt_l1_bound"
            ]
        )
    )
    projective_equal_pair_conditional_sqrt_error_bound = (
        ceil_sqrt(p) * projective_equal_pair_conditional_sqrt_weight
    )
    projective_equal_pair_nonresonant_conditional_sqrt_weight = (
        total_sqrt_weight
        + int(
            error_split[
                "two_coordinate_projective_equal_pair_sqrt_l1_bound"
            ]
        )
        + int(
            error_split[
                "two_coordinate_projective_asymmetric_nonresonant_"
                "sqrt_l1_bound"
            ]
        )
    )
    projective_equal_pair_nonresonant_conditional_sqrt_error_bound = (
        ceil_sqrt(p)
        * projective_equal_pair_nonresonant_conditional_sqrt_weight
    )
    projective_equal_pair_all_asymmetric_conditional_sqrt_weight = (
        projective_equal_pair_nonresonant_conditional_sqrt_weight
        + int(
            error_split[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_sqrt_l1_bound"
            ]
        )
    )
    projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound = (
        ceil_sqrt(p)
        * projective_equal_pair_all_asymmetric_conditional_sqrt_weight
    )
    uniform_prime_threshold = kummer_quadratic_uniform_prime_threshold(
        principal_weight=1,
        linear_error_weight=(
            int(error_split["weighted_error_l1_bound"]) + 6 * denominator
        ),
        sqrt_error_weight=total_sqrt_weight,
    )
    equal_line_conditional_uniform_prime_threshold = (
        kummer_quadratic_uniform_prime_threshold(
            principal_weight=1,
            linear_error_weight=(
                int(error_split["equal_line_conditional_weighted_error_l1_bound"])
                + 6 * denominator
            ),
            sqrt_error_weight=equal_line_conditional_sqrt_weight,
        )
    )
    coordinate_diagonal_conditional_uniform_prime_threshold = (
        kummer_quadratic_uniform_prime_threshold(
            principal_weight=1,
            linear_error_weight=(
                int(
                    error_split[
                        "coordinate_diagonal_conditional_weighted_error_l1_bound"
                    ]
                )
                + 6 * denominator
            ),
            sqrt_error_weight=coordinate_diagonal_conditional_sqrt_weight,
        )
    )
    projective_equal_pair_conditional_uniform_prime_threshold = (
        kummer_quadratic_uniform_prime_threshold(
            principal_weight=1,
            linear_error_weight=(
                int(
                    error_split[
                        "projective_equal_pair_conditional_weighted_error_l1_bound"
                    ]
                )
                + 6 * denominator
            ),
            sqrt_error_weight=projective_equal_pair_conditional_sqrt_weight,
        )
    )
    projective_equal_pair_nonresonant_conditional_uniform_prime_threshold = (
        kummer_quadratic_uniform_prime_threshold(
            principal_weight=1,
            linear_error_weight=(
                int(
                    error_split[
                        "projective_equal_pair_nonresonant_conditional_"
                        "weighted_error_l1_bound"
                    ]
                )
                + 6 * denominator
            ),
            sqrt_error_weight=(
                projective_equal_pair_nonresonant_conditional_sqrt_weight
            ),
        )
    )
    projective_equal_pair_all_asymmetric_conditional_uniform_prime_threshold = (
        kummer_quadratic_uniform_prime_threshold(
            principal_weight=1,
            linear_error_weight=(
                int(
                    error_split[
                        "projective_equal_pair_all_asymmetric_conditional_"
                        "weighted_error_l1_bound"
                    ]
                )
                + 6 * denominator
            ),
            sqrt_error_weight=(
                projective_equal_pair_all_asymmetric_conditional_sqrt_weight
            ),
        )
    )
    chi_minus_three = quadratic_character(-3, p)
    principal_exact_count = p * p - 4 * p + 6 + 4 * chi_minus_three
    degeneracy_line_count = 6
    degeneracy_line_union_count = 6 * p - 11
    lower_numerator = principal_exact_count - (
        p * int(error_split["weighted_error_l1_bound"])
        + open_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    equal_line_conditional_lower_numerator = principal_exact_count - (
        p * int(error_split["equal_line_conditional_weighted_error_l1_bound"])
        + equal_line_conditional_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    coordinate_diagonal_conditional_lower_numerator = principal_exact_count - (
        p
        * int(
            error_split[
                "coordinate_diagonal_conditional_weighted_error_l1_bound"
            ]
        )
        + coordinate_diagonal_conditional_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    projective_equal_pair_conditional_lower_numerator = principal_exact_count - (
        p
        * int(
            error_split[
                "projective_equal_pair_conditional_weighted_error_l1_bound"
            ]
        )
        + projective_equal_pair_conditional_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    projective_equal_pair_nonresonant_conditional_lower_numerator = (
        principal_exact_count
        - (
            p
            * int(
                error_split[
                    "projective_equal_pair_nonresonant_conditional_"
                    "weighted_error_l1_bound"
                ]
            )
            + projective_equal_pair_nonresonant_conditional_sqrt_error_bound
            + degeneracy_line_union_count * denominator
        )
    )
    projective_equal_pair_all_asymmetric_conditional_lower_numerator = (
        principal_exact_count
        - (
            p
            * int(
                error_split[
                    "projective_equal_pair_all_asymmetric_conditional_"
                    "weighted_error_l1_bound"
                ]
            )
            + projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound
            + degeneracy_line_union_count * denominator
        )
    )
    admissible_per_coset_lower_bound = (
        (lower_numerator + denominator - 1) // denominator
        if lower_numerator > 0
        else 0
    )
    equal_line_conditional_admissible_per_coset_lower_bound = (
        (
            equal_line_conditional_lower_numerator
            + denominator
            - 1
        )
        // denominator
        if equal_line_conditional_lower_numerator > 0
        else 0
    )
    coordinate_diagonal_conditional_admissible_per_coset_lower_bound = (
        (
            coordinate_diagonal_conditional_lower_numerator
            + denominator
            - 1
        )
        // denominator
        if coordinate_diagonal_conditional_lower_numerator > 0
        else 0
    )
    projective_equal_pair_conditional_admissible_per_coset_lower_bound = (
        (
            projective_equal_pair_conditional_lower_numerator
            + denominator
            - 1
        )
        // denominator
        if projective_equal_pair_conditional_lower_numerator > 0
        else 0
    )
    projective_equal_pair_nonresonant_admissible_per_coset_lower_bound = (
        (
            projective_equal_pair_nonresonant_conditional_lower_numerator
            + denominator
            - 1
        )
        // denominator
        if projective_equal_pair_nonresonant_conditional_lower_numerator > 0
        else 0
    )
    projective_equal_pair_all_asymmetric_admissible_per_coset_lower_bound = (
        (
            projective_equal_pair_all_asymmetric_conditional_lower_numerator
            + denominator
            - 1
        )
        // denominator
        if projective_equal_pair_all_asymmetric_conditional_lower_numerator > 0
        else 0
    )
    return {
        "character_order": character_order,
        "square_kernel_index": square_kernel_index,
        "square_coset_index": square_coset_index,
        "denominator": denominator,
        "nonprincipal_tuple_count": nonprincipal_tuple_count,
        "coefficient_l1_bound": coefficient_l1_bound,
        **error_split,
        "jacobi_error_constant": 1,
        "elementary_open_sqrt_constant": 6,
        "elementary_open_sqrt_error_bound": (
            ceil_sqrt(p) * elementary_open_sqrt_weight
        ),
        "sqrt_error_weight": total_sqrt_weight,
        "sqrt_error_bound": open_sqrt_error_bound,
        "weighted_error_total_bound": (
            p * int(error_split["weighted_error_l1_bound"])
            + open_sqrt_error_bound
        ),
        "equal_line_conditional_import_status": (
            "CONDITIONAL / not consumed by saturation_certificate"
        ),
        "coordinate_diagonal_conditional_import_status": (
            "CONDITIONAL / not consumed by saturation_certificate"
        ),
        "projective_equal_pair_conditional_import_status": (
            "CONDITIONAL / not consumed by saturation_certificate"
        ),
        "projective_equal_pair_nonresonant_conditional_import_status": (
            "CONDITIONAL / not consumed by saturation_certificate"
        ),
        "projective_equal_pair_all_asymmetric_conditional_import_status": (
            "CONDITIONAL / not consumed by saturation_certificate"
        ),
        "equal_line_conditional_sqrt_error_weight": (
            equal_line_conditional_sqrt_weight
        ),
        "equal_line_conditional_sqrt_error_bound": (
            equal_line_conditional_sqrt_error_bound
        ),
        "equal_line_conditional_weighted_error_total_bound": (
            p * int(error_split["equal_line_conditional_weighted_error_l1_bound"])
            + equal_line_conditional_sqrt_error_bound
        ),
        "coordinate_diagonal_conditional_sqrt_error_weight": (
            coordinate_diagonal_conditional_sqrt_weight
        ),
        "coordinate_diagonal_conditional_sqrt_error_bound": (
            coordinate_diagonal_conditional_sqrt_error_bound
        ),
        "coordinate_diagonal_conditional_weighted_error_total_bound": (
            p
            * int(
                error_split[
                    "coordinate_diagonal_conditional_weighted_error_l1_bound"
                ]
            )
            + coordinate_diagonal_conditional_sqrt_error_bound
        ),
        "projective_equal_pair_conditional_sqrt_error_weight": (
            projective_equal_pair_conditional_sqrt_weight
        ),
        "projective_equal_pair_conditional_sqrt_error_bound": (
            projective_equal_pair_conditional_sqrt_error_bound
        ),
        "projective_equal_pair_conditional_weighted_error_total_bound": (
            p
            * int(
                error_split[
                    "projective_equal_pair_conditional_weighted_error_l1_bound"
                ]
            )
            + projective_equal_pair_conditional_sqrt_error_bound
        ),
        (
            "projective_equal_pair_nonresonant_conditional_"
            "sqrt_error_weight"
        ): projective_equal_pair_nonresonant_conditional_sqrt_weight,
        (
            "projective_equal_pair_nonresonant_conditional_"
            "sqrt_error_bound"
        ): projective_equal_pair_nonresonant_conditional_sqrt_error_bound,
        (
            "projective_equal_pair_nonresonant_conditional_"
            "weighted_error_total_bound"
        ): (
            p
            * int(
                error_split[
                    "projective_equal_pair_nonresonant_conditional_"
                    "weighted_error_l1_bound"
                ]
            )
            + projective_equal_pair_nonresonant_conditional_sqrt_error_bound
        ),
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "sqrt_error_weight"
        ): projective_equal_pair_all_asymmetric_conditional_sqrt_weight,
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "sqrt_error_bound"
        ): projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound,
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "weighted_error_total_bound"
        ): (
            p
            * int(
                error_split[
                    "projective_equal_pair_all_asymmetric_conditional_"
                    "weighted_error_l1_bound"
                ]
            )
            + projective_equal_pair_all_asymmetric_conditional_sqrt_error_bound
        ),
        "conic_error_constant": 1,
        "two_coordinate_coordinate_diagonal_l1_bound": int(
            two_coordinate_projective_split[
                "two_coordinate_coordinate_diagonal_l1_bound"
            ]
        ),
        "two_coordinate_coordinate_diagonal_non_equal_l1_bound": int(
            two_coordinate_projective_split[
                "two_coordinate_coordinate_diagonal_non_equal_l1_bound"
            ]
        ),
        "two_coordinate_coordinate_diagonal_alpha_square_trivial_count": int(
            two_coordinate_projective_split[
                "two_coordinate_coordinate_diagonal_alpha_square_trivial_count"
            ]
        ),
        "two_coordinate_coordinate_diagonal_2f1_cancellation_count": int(
            two_coordinate_projective_split[
                "two_coordinate_coordinate_diagonal_2f1_cancellation_count"
            ]
        ),
        "two_coordinate_projective_equal_pair_l1_bound": int(
            two_coordinate_projective_split[
                "two_coordinate_projective_equal_pair_l1_bound"
            ]
        ),
        "two_coordinate_projective_equal_pair_non_coordinate_l1_bound": int(
            two_coordinate_projective_split[
                "two_coordinate_projective_equal_pair_non_coordinate_l1_bound"
            ]
        ),
        "two_coordinate_projective_asymmetric_l1_bound": int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_l1_bound"
            ]
        ),
        "two_coordinate_projective_asymmetric_orbit_count": int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_orbit_count"
            ]
        ),
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_l1_bound"
        ): int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_l1_bound"
            ]
        ),
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "nonresonant_l1_bound"
        ): int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_line_conic_"
                "nonresonant_l1_bound"
            ]
        ),
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "resonant_orbit_count"
        ): int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_line_conic_"
                "resonant_orbit_count"
            ]
        ),
        (
            "two_coordinate_projective_asymmetric_line_conic_"
            "nonresonant_orbit_count"
        ): int(
            two_coordinate_projective_split[
                "two_coordinate_projective_asymmetric_line_conic_"
                "nonresonant_orbit_count"
            ]
        ),
        "divisor_power_failure_count": 0,
        "divisor_nontriviality_check": True,
        "radical_component_degrees": radical_component_degrees,
        "radical_total_degree": radical_total_degree,
        "deligne_constant_formula": "(radical_total_degree - 1)^2",
        "deligne_constant": deligne_constant,
        "deligne_constant_check": nonprincipal_constant == deligne_constant,
        "uniform_prime_threshold": uniform_prime_threshold,
        "uniform_threshold_applies": p >= uniform_prime_threshold,
        "equal_line_conditional_uniform_prime_threshold": (
            equal_line_conditional_uniform_prime_threshold
        ),
        "equal_line_conditional_uniform_threshold_applies": (
            p >= equal_line_conditional_uniform_prime_threshold
        ),
        "coordinate_diagonal_conditional_uniform_prime_threshold": (
            coordinate_diagonal_conditional_uniform_prime_threshold
        ),
        "coordinate_diagonal_conditional_uniform_threshold_applies": (
            p >= coordinate_diagonal_conditional_uniform_prime_threshold
        ),
        "projective_equal_pair_conditional_uniform_prime_threshold": (
            projective_equal_pair_conditional_uniform_prime_threshold
        ),
        "projective_equal_pair_conditional_uniform_threshold_applies": (
            p >= projective_equal_pair_conditional_uniform_prime_threshold
        ),
        (
            "projective_equal_pair_nonresonant_conditional_"
            "uniform_prime_threshold"
        ): projective_equal_pair_nonresonant_conditional_uniform_prime_threshold,
        (
            "projective_equal_pair_nonresonant_conditional_"
            "uniform_threshold_applies"
        ): (
            p
            >= projective_equal_pair_nonresonant_conditional_uniform_prime_threshold
        ),
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "uniform_prime_threshold"
        ): (
            projective_equal_pair_all_asymmetric_conditional_uniform_prime_threshold
        ),
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "uniform_threshold_applies"
        ): (
            p
            >= projective_equal_pair_all_asymmetric_conditional_uniform_prime_threshold
        ),
        "nonprincipal_constant": nonprincipal_constant,
        "principal_chi_minus_three": chi_minus_three,
        "principal_exact_count": principal_exact_count,
        "principal_lower_bound": principal_exact_count,
        "degeneracy_line_count": degeneracy_line_count,
        "degeneracy_line_union_count": degeneracy_line_union_count,
        "lower_numerator": lower_numerator,
        "equal_line_conditional_lower_numerator": (
            equal_line_conditional_lower_numerator
        ),
        "coordinate_diagonal_conditional_lower_numerator": (
            coordinate_diagonal_conditional_lower_numerator
        ),
        "projective_equal_pair_conditional_lower_numerator": (
            projective_equal_pair_conditional_lower_numerator
        ),
        (
            "projective_equal_pair_nonresonant_conditional_"
            "lower_numerator"
        ): projective_equal_pair_nonresonant_conditional_lower_numerator,
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "lower_numerator"
        ): projective_equal_pair_all_asymmetric_conditional_lower_numerator,
        "admissible_per_coset_lower_bound": (
            admissible_per_coset_lower_bound
        ),
        "equal_line_conditional_admissible_per_coset_lower_bound": (
            equal_line_conditional_admissible_per_coset_lower_bound
        ),
        "coordinate_diagonal_conditional_admissible_per_coset_lower_bound": (
            coordinate_diagonal_conditional_admissible_per_coset_lower_bound
        ),
        "projective_equal_pair_conditional_admissible_per_coset_lower_bound": (
            projective_equal_pair_conditional_admissible_per_coset_lower_bound
        ),
        (
            "projective_equal_pair_nonresonant_conditional_"
            "admissible_per_coset_lower_bound"
        ): projective_equal_pair_nonresonant_admissible_per_coset_lower_bound,
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "admissible_per_coset_lower_bound"
        ): projective_equal_pair_all_asymmetric_admissible_per_coset_lower_bound,
        "saturation_certificate": admissible_per_coset_lower_bound > 0,
        "equal_line_conditional_saturation_certificate": (
            equal_line_conditional_admissible_per_coset_lower_bound > 0
        ),
        "coordinate_diagonal_conditional_saturation_certificate": (
            coordinate_diagonal_conditional_admissible_per_coset_lower_bound > 0
        ),
        "projective_equal_pair_conditional_saturation_certificate": (
            projective_equal_pair_conditional_admissible_per_coset_lower_bound > 0
        ),
        (
            "projective_equal_pair_nonresonant_conditional_"
            "saturation_certificate"
        ): (
            projective_equal_pair_nonresonant_admissible_per_coset_lower_bound
            > 0
        ),
        (
            "projective_equal_pair_all_asymmetric_conditional_"
            "saturation_certificate"
        ): (
            projective_equal_pair_all_asymmetric_admissible_per_coset_lower_bound
            > 0
        ),
    }


def kummer_quadratic_uniform_prime_threshold(
    principal_weight: int,
    linear_error_weight: int,
    sqrt_error_weight: int = 0,
) -> int:
    """Return a uniform positive threshold for a quadratic Kummer numerator."""

    total_weight = linear_error_weight + sqrt_error_weight
    return (total_weight + principal_weight - 1) // principal_weight + 4


def slack_two_second_two_fiber_kummer_saturation_data(
    p: int,
    domain_order: int,
    quotient_order: int,
    nonprincipal_constant: int = 16,
) -> Optional[Dict[str, object]]:
    """Return a two-quotient-fiber depth-two saturation certificate."""

    if quotient_order < 2 or domain_order % quotient_order:
        return None

    fiber_size = domain_order // quotient_order
    kernel_character_order = (p - 1) // fiber_size
    square_kernel_index = math.gcd(2, domain_order)
    square_coset_index = ((p - 1) // domain_order) * square_kernel_index
    denominator = (
        kernel_character_order
        * kernel_character_order
        * kernel_character_order
        * square_coset_index
    )
    principal_weight = 8
    window_size = 2
    coefficient_abs_bound = 8
    ambient_restriction_kernel_count = kernel_character_order // quotient_order
    active_character_l1_bound = fixed_window_active_character_l1_bound(
        quotient_order,
        window_size,
        ambient_restriction_kernel_count,
    )
    (
        coordinate_one_nonprincipal_l1_bound,
        coordinate_two_nonprincipal_l1_bound,
        coordinate_three_nonprincipal_l1_bound,
    ) = fixed_window_active_coordinate_l1_bounds(
        window_size,
        active_character_l1_bound,
    )
    coordinate_nonprincipal_l1_bound = (
        (window_size + active_character_l1_bound) ** 3
        - principal_weight
    )
    radical_component_degrees = (1, 1, 1, 2)
    radical_total_degree = sum(radical_component_degrees)
    deligne_constant = (radical_total_degree - 1) ** 2
    chi_minus_three = quadratic_character(-3, p)
    principal_exact_count = p * p - 4 * p + 6 + 4 * chi_minus_three
    degeneracy_line_count = 6
    degeneracy_line_union_count = 6 * p - 11
    coefficient_l1_bound = (
        square_coset_index
        * (principal_weight + coordinate_nonprincipal_l1_bound)
        - principal_weight
    )
    error_split = depth_two_kummer_error_l1_split(
        coordinate_principal_weight=principal_weight,
        coordinate_nonprincipal_l1_bound=coordinate_nonprincipal_l1_bound,
        square_coset_index=square_coset_index,
        nonprincipal_constant=nonprincipal_constant,
        coordinate_one_nonprincipal_l1_bound=coordinate_one_nonprincipal_l1_bound,
        coordinate_two_nonprincipal_l1_bound=coordinate_two_nonprincipal_l1_bound,
        coordinate_three_nonprincipal_l1_bound=(
            coordinate_three_nonprincipal_l1_bound
        ),
    )
    open_sqrt_error_bound = depth_two_open_sqrt_error_bound(
        p,
        error_split,
    )
    uniform_prime_threshold = kummer_quadratic_uniform_prime_threshold(
        principal_weight,
        int(error_split["weighted_error_l1_bound"]) + 6 * denominator,
        sqrt_error_weight=6
        * (
            int(error_split["jacobi_l1_bound"])
            + int(error_split["conic_l1_bound"])
        ),
    )
    lower_numerator = principal_weight * principal_exact_count - (
        p * int(error_split["weighted_error_l1_bound"])
        + open_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    admissible_per_coset_lower_bound = (
        (lower_numerator + denominator - 1) // denominator
        if lower_numerator > 0
        else 0
    )
    return {
        "quotient_order": quotient_order,
        "fiber_size": fiber_size,
        "kernel_character_order": kernel_character_order,
        "square_kernel_index": square_kernel_index,
        "square_coset_index": square_coset_index,
        "denominator": denominator,
        "nonprincipal_tuple_count_bound": denominator - 1,
        "divisor_power_failure_count": 0,
        "divisor_nontriviality_check": True,
        "radical_component_degrees": radical_component_degrees,
        "radical_total_degree": radical_total_degree,
        "deligne_constant_formula": "(radical_total_degree - 1)^2",
        "deligne_constant": deligne_constant,
        "deligne_constant_check": nonprincipal_constant == deligne_constant,
        "principal_weight": principal_weight,
        "coefficient_abs_bound": coefficient_abs_bound,
        "ambient_restriction_kernel_count": ambient_restriction_kernel_count,
        "window_one_dimensional_l1_bound": active_character_l1_bound,
        "coefficient_l1_bound": coefficient_l1_bound,
        **error_split,
        "jacobi_error_constant": 1,
        "elementary_open_sqrt_constant": 6,
        "elementary_open_sqrt_error_bound": open_sqrt_error_bound,
        "weighted_error_total_bound": (
            p * int(error_split["weighted_error_l1_bound"])
            + open_sqrt_error_bound
        ),
        "conic_error_constant": 1,
        "uniform_prime_threshold": uniform_prime_threshold,
        "uniform_threshold_applies": p >= uniform_prime_threshold,
        "nonprincipal_constant": nonprincipal_constant,
        "principal_chi_minus_three": chi_minus_three,
        "principal_exact_count": principal_exact_count,
        "degeneracy_line_count": degeneracy_line_count,
        "degeneracy_line_union_count": degeneracy_line_union_count,
        "lower_numerator": lower_numerator,
        "admissible_per_coset_lower_bound": (
            admissible_per_coset_lower_bound
        ),
        "saturation_certificate": admissible_per_coset_lower_bound > 0,
    }


def slack_two_second_fixed_window_kummer_saturation_data(
    p: int,
    domain_order: int,
    quotient_order: int,
    window_size: int,
    nonprincipal_constant: int = 16,
) -> Optional[Dict[str, object]]:
    """Return a fixed quotient-window depth-two saturation certificate."""

    if (
        quotient_order < 1
        or window_size < 1
        or window_size > quotient_order
        or domain_order % quotient_order
    ):
        return None

    fiber_size = domain_order // quotient_order
    kernel_character_order = (p - 1) // fiber_size
    square_kernel_index = math.gcd(2, domain_order)
    square_coset_index = ((p - 1) // domain_order) * square_kernel_index
    denominator = (
        kernel_character_order
        * kernel_character_order
        * kernel_character_order
        * square_coset_index
    )
    principal_weight = window_size ** 3
    coefficient_abs_bound = window_size ** 3
    ambient_restriction_kernel_count = kernel_character_order // quotient_order
    active_character_l1_bound = fixed_window_active_character_l1_bound(
        quotient_order,
        window_size,
        ambient_restriction_kernel_count,
    )
    (
        coordinate_one_nonprincipal_l1_bound,
        coordinate_two_nonprincipal_l1_bound,
        coordinate_three_nonprincipal_l1_bound,
    ) = fixed_window_active_coordinate_l1_bounds(
        window_size,
        active_character_l1_bound,
    )
    coordinate_nonprincipal_l1_bound = (
        (window_size + active_character_l1_bound) ** 3
        - principal_weight
    )
    radical_component_degrees = (1, 1, 1, 2)
    radical_total_degree = sum(radical_component_degrees)
    deligne_constant = (radical_total_degree - 1) ** 2
    chi_minus_three = quadratic_character(-3, p)
    principal_exact_count = p * p - 4 * p + 6 + 4 * chi_minus_three
    degeneracy_line_union_count = 6 * p - 11
    coefficient_l1_bound = (
        square_coset_index
        * (principal_weight + coordinate_nonprincipal_l1_bound)
        - principal_weight
    )
    error_split = depth_two_kummer_error_l1_split(
        coordinate_principal_weight=principal_weight,
        coordinate_nonprincipal_l1_bound=coordinate_nonprincipal_l1_bound,
        square_coset_index=square_coset_index,
        nonprincipal_constant=nonprincipal_constant,
        coordinate_one_nonprincipal_l1_bound=coordinate_one_nonprincipal_l1_bound,
        coordinate_two_nonprincipal_l1_bound=coordinate_two_nonprincipal_l1_bound,
        coordinate_three_nonprincipal_l1_bound=(
            coordinate_three_nonprincipal_l1_bound
        ),
    )
    open_sqrt_error_bound = depth_two_open_sqrt_error_bound(
        p,
        error_split,
    )
    uniform_prime_threshold = kummer_quadratic_uniform_prime_threshold(
        principal_weight,
        int(error_split["weighted_error_l1_bound"]) + 6 * denominator,
        sqrt_error_weight=6
        * (
            int(error_split["jacobi_l1_bound"])
            + int(error_split["conic_l1_bound"])
        ),
    )
    lower_numerator = principal_weight * principal_exact_count - (
        p * int(error_split["weighted_error_l1_bound"])
        + open_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    admissible_per_coset_lower_bound = (
        (lower_numerator + denominator - 1) // denominator
        if lower_numerator > 0
        else 0
    )
    return {
        "quotient_order": quotient_order,
        "window_size": window_size,
        "fiber_size": fiber_size,
        "kernel_character_order": kernel_character_order,
        "square_kernel_index": square_kernel_index,
        "square_coset_index": square_coset_index,
        "denominator": denominator,
        "nonprincipal_tuple_count_bound": denominator - 1,
        "divisor_power_failure_count": 0,
        "divisor_nontriviality_check": True,
        "radical_component_degrees": radical_component_degrees,
        "radical_total_degree": radical_total_degree,
        "deligne_constant_formula": "(radical_total_degree - 1)^2",
        "deligne_constant": deligne_constant,
        "deligne_constant_check": nonprincipal_constant == deligne_constant,
        "principal_weight": principal_weight,
        "coefficient_abs_bound": coefficient_abs_bound,
        "ambient_restriction_kernel_count": ambient_restriction_kernel_count,
        "window_one_dimensional_l1_bound": active_character_l1_bound,
        "coefficient_l1_bound": coefficient_l1_bound,
        **error_split,
        "jacobi_error_constant": 1,
        "elementary_open_sqrt_constant": 6,
        "elementary_open_sqrt_error_bound": open_sqrt_error_bound,
        "weighted_error_total_bound": (
            p * int(error_split["weighted_error_l1_bound"])
            + open_sqrt_error_bound
        ),
        "conic_error_constant": 1,
        "uniform_prime_threshold": uniform_prime_threshold,
        "uniform_threshold_applies": p >= uniform_prime_threshold,
        "nonprincipal_constant": nonprincipal_constant,
        "principal_chi_minus_three": chi_minus_three,
        "principal_exact_count": principal_exact_count,
        "degeneracy_line_union_count": degeneracy_line_union_count,
        "lower_numerator": lower_numerator,
        "admissible_per_coset_lower_bound": (
            admissible_per_coset_lower_bound
        ),
        "saturation_certificate": admissible_per_coset_lower_bound > 0,
    }


def quotient_window_label_triple_count(
    quotient_order: int,
    window_size: int,
) -> int:
    """Count quotient-label triples touching at most ``window_size`` fibers."""

    if quotient_order < 1 or window_size < 1:
        return 0

    max_new_labels = min(window_size - 1, 3, quotient_order - 1)
    total = 0
    for new_labels in range(max_new_labels + 1):
        onto_count = 0
        for missing in range(new_labels + 1):
            onto_count += (
                (-1) ** missing
                * math.comb(new_labels, missing)
                * (new_labels + 1 - missing) ** 3
            )
        total += math.comb(quotient_order - 1, new_labels) * onto_count
    return total


def quotient_window_label_nonprincipal_bound(
    quotient_order: int,
    window_size: int,
) -> int:
    """Bound nonprincipal quotient-label Fourier coefficients."""

    if quotient_order < 1 or window_size < 1:
        return 0
    if window_size == 1:
        return 1
    if window_size == 2:
        return max(1, 3 * quotient_order - 6)
    if window_size == 3:
        return max(6, (quotient_order - 2) * (quotient_order - 3))
    return 0


def quotient_label_sum(value: int, quotient_order: int) -> int:
    return quotient_order - 1 if value % quotient_order == 0 else -1


def quotient_window_label_coefficient(
    quotient_order: int,
    window_size: int,
    triple: Tuple[int, int, int],
) -> int:
    """Return the quotient-label Fourier coefficient for an R-window union."""

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


def quotient_window_label_l1_data(
    quotient_order: int,
    window_size: int,
) -> Dict[str, object]:
    """Return an exact or certified quotient-label Fourier L1 bound."""

    if quotient_order < 1 or window_size < 1:
        return {"l1_bound": 0, "exact": False}
    if window_size == 1:
        return {"l1_bound": quotient_order ** 3, "exact": True}
    if window_size == 2:
        n = quotient_order
        if n % 2:
            zero_count = (n - 1) * (n - 3) * (n - 3)
            one_count = (n - 1) * (7 * n - 17)
            two_count = 3 * n - 3
            three_count = 6 * n - 6
        else:
            zero_count = n ** 3 - 7 * n ** 2 + 15 * n - 10
            one_count = (n - 2) * (7 * n - 10)
            two_count = 3 * n - 6
            three_count = 6 * n - 5
        seven_count = 1
        l1_bound = (
            6 * zero_count
            + abs(n - 6) * one_count
            + abs(2 * n - 6) * two_count
            + abs(3 * n - 6) * three_count
            + (7 * n - 6) * seven_count
        )
        return {
            "l1_bound": l1_bound,
            "exact": True,
            "zero_subset_count_histogram": (
                (0, zero_count),
                (1, one_count),
                (2, two_count),
                (3, three_count),
                (7, seven_count),
            ),
        }
    if window_size == 3:
        n = quotient_order
        principal_value = quotient_window_label_triple_count(n, 3)
        if n % 2:
            entries = (
                (principal_value, 1),
                (-(2 * n - 6), (n - 1) * (4 * n - 5)),
                (-(n - 6), 3 * (n - 1) * (n - 3)),
                (6, n ** 3 - 7 * n ** 2 + 15 * n - 9),
                ((n - 2) * (n - 3), 6 * n - 6),
            )
        else:
            entries = (
                (principal_value, 1),
                (-(3 * n - 6), 1),
                (-(2 * n - 6), (n - 2) * (4 * n - 1)),
                (-(n - 6), 3 * (n - 2) ** 2),
                (6, n ** 3 - 7 * n ** 2 + 15 * n - 10),
                ((n - 2) * (n - 3), 6 * n - 6),
            )
        coefficient_histogram: Dict[int, int] = {}
        for value, count in entries:
            if count:
                coefficient_histogram[value] = (
                    coefficient_histogram.get(value, 0) + count
                )
        coefficient_value_histogram = tuple(sorted(coefficient_histogram.items()))
        l1_bound = sum(
            abs(value) * count for value, count in coefficient_value_histogram
        )
        return {
            "l1_bound": l1_bound,
            "exact": True,
            "coefficient_value_histogram": coefficient_value_histogram,
        }

    label_triple_count = quotient_window_label_triple_count(
        quotient_order,
        window_size,
    )
    coefficient_abs_bound = quotient_window_label_nonprincipal_bound(
        quotient_order,
        window_size,
    )
    quotient_l1_bound = label_triple_count + (
        quotient_order ** 3 - 1
    ) * coefficient_abs_bound
    return {"l1_bound": quotient_l1_bound, "exact": False}


def quotient_window_one_coordinate_l1_bound(
    quotient_order: int,
    window_size: int,
    ambient_restriction_kernel_count: int,
) -> int:
    """Return the ambient L1 mass with exactly one active coordinate."""

    if (
        quotient_order < 1
        or window_size < 1
        or ambient_restriction_kernel_count < 1
    ):
        return 0

    label_triple_count = quotient_window_label_triple_count(
        quotient_order,
        window_size,
    )
    if window_size == 1:
        nonzero_quotient_coefficient_abs = 1
    elif window_size == 2:
        nonzero_quotient_coefficient_abs = abs(3 * quotient_order - 6)
    elif window_size == 3:
        nonzero_quotient_coefficient_abs = abs(
            (quotient_order - 2) * (quotient_order - 3)
        )
    else:
        nonzero_quotient_coefficient_abs = (
            quotient_window_label_nonprincipal_bound(
                quotient_order,
                window_size,
            )
        )

    quotient_principal_lift = (
        ambient_restriction_kernel_count - 1
    ) * label_triple_count
    quotient_nonprincipal_lift = (
        ambient_restriction_kernel_count
        * (quotient_order - 1)
        * nonzero_quotient_coefficient_abs
    )
    return 3 * (quotient_principal_lift + quotient_nonprincipal_lift)


def quotient_window_coordinate_active_l1_bounds(
    quotient_order: int,
    window_size: int,
    ambient_restriction_kernel_count: int,
) -> Tuple[int, int, int]:
    """Return exact ambient L1 masses by active coordinate count."""

    if (
        quotient_order < 1
        or window_size < 1
        or ambient_restriction_kernel_count < 1
    ):
        return (0, 0, 0)

    totals = [0, 0, 0, 0]
    for r, s, t in product(range(quotient_order), repeat=3):
        coefficient_abs = abs(
            quotient_window_label_coefficient(
                quotient_order,
                window_size,
                (r, s, t),
            )
        )
        if coefficient_abs == 0:
            continue
        active_count_weights = [1, 0, 0, 0]
        for residue in (r, s, t):
            if residue == 0:
                zero_choices = 1
                nonzero_choices = ambient_restriction_kernel_count - 1
            else:
                zero_choices = 0
                nonzero_choices = ambient_restriction_kernel_count
            next_weights = [0, 0, 0, 0]
            for active_count, weight in enumerate(active_count_weights):
                if weight == 0:
                    continue
                next_weights[active_count] += weight * zero_choices
                if active_count < 3:
                    next_weights[active_count + 1] += (
                        weight * nonzero_choices
                    )
            active_count_weights = next_weights
        for active_count in range(1, 4):
            totals[active_count] += (
                coefficient_abs * active_count_weights[active_count]
            )
    return (totals[1], totals[2], totals[3])


def slack_two_second_quotient_window_union_kummer_saturation_data(
    p: int,
    domain_order: int,
    quotient_order: int,
    remaining_fibers: int,
    nonprincipal_constant: int = 16,
) -> Optional[Dict[str, object]]:
    """Return a Kummer certificate for the full quotient-window union."""

    if (
        quotient_order < 1
        or remaining_fibers < 1
        or domain_order % quotient_order
    ):
        return None

    effective_window_size = min(remaining_fibers, 4, quotient_order)
    if effective_window_size >= min(4, quotient_order):
        return None

    fiber_size = domain_order // quotient_order
    kernel_character_order = (p - 1) // fiber_size
    square_kernel_index = math.gcd(2, domain_order)
    square_coset_index = ((p - 1) // domain_order) * square_kernel_index
    denominator = (
        kernel_character_order
        * kernel_character_order
        * kernel_character_order
        * square_coset_index
    )
    label_triple_count = quotient_window_label_triple_count(
        quotient_order,
        effective_window_size,
    )
    principal_weight = label_triple_count
    coefficient_abs_bound = quotient_window_label_nonprincipal_bound(
        quotient_order,
        effective_window_size,
    )
    ambient_restriction_kernel_count = kernel_character_order // quotient_order
    quotient_l1_data = quotient_window_label_l1_data(
        quotient_order,
        effective_window_size,
    )
    if bool(quotient_l1_data["exact"]):
        quotient_coefficient_l1_bound = (
            ambient_restriction_kernel_count ** 3
            * int(quotient_l1_data["l1_bound"])
        )
    else:
        quotient_coefficient_l1_bound = (
            ambient_restriction_kernel_count ** 3 * label_triple_count
            + (
                kernel_character_order ** 3
                - ambient_restriction_kernel_count ** 3
            )
            * coefficient_abs_bound
        )
    coefficient_l1_bound = (
        square_coset_index * quotient_coefficient_l1_bound
        - label_triple_count
    )
    coordinate_nonprincipal_l1_bound = (
        quotient_coefficient_l1_bound - label_triple_count
    )
    quotient_one_coordinate_l1_bound = quotient_window_one_coordinate_l1_bound(
        quotient_order,
        effective_window_size,
        ambient_restriction_kernel_count,
    )
    (
        quotient_active_one_l1_bound,
        quotient_active_two_l1_bound,
        quotient_active_three_l1_bound,
    ) = quotient_window_coordinate_active_l1_bounds(
        quotient_order,
        effective_window_size,
        ambient_restriction_kernel_count,
    )
    if quotient_active_one_l1_bound != quotient_one_coordinate_l1_bound:
        raise ValueError("quotient one-coordinate L1 formulas disagree")
    error_split = depth_two_kummer_error_l1_split(
        coordinate_principal_weight=label_triple_count,
        coordinate_nonprincipal_l1_bound=coordinate_nonprincipal_l1_bound,
        square_coset_index=square_coset_index,
        nonprincipal_constant=nonprincipal_constant,
        coordinate_one_nonprincipal_l1_bound=(
            quotient_active_one_l1_bound
        ),
        coordinate_two_nonprincipal_l1_bound=(
            quotient_active_two_l1_bound
        ),
        coordinate_three_nonprincipal_l1_bound=(
            quotient_active_three_l1_bound
        ),
    )
    crude_coefficient_l1_bound = (
        label_triple_count * denominator - label_triple_count
    )
    crude_error_split = depth_two_kummer_error_l1_split(
        coordinate_principal_weight=label_triple_count,
        coordinate_nonprincipal_l1_bound=(
            label_triple_count * (kernel_character_order ** 3 - 1)
        ),
        square_coset_index=square_coset_index,
        nonprincipal_constant=nonprincipal_constant,
        coordinate_one_nonprincipal_l1_bound=(
            3 * label_triple_count * (kernel_character_order - 1)
        ),
        coordinate_two_nonprincipal_l1_bound=(
            3 * label_triple_count * (kernel_character_order - 1) ** 2
        ),
        coordinate_three_nonprincipal_l1_bound=(
            label_triple_count * (kernel_character_order - 1) ** 3
        ),
    )
    radical_component_degrees = (1, 1, 1, 2)
    radical_total_degree = sum(radical_component_degrees)
    deligne_constant = (radical_total_degree - 1) ** 2
    chi_minus_three = quadratic_character(-3, p)
    principal_exact_count = p * p - 4 * p + 6 + 4 * chi_minus_three
    degeneracy_line_union_count = 6 * p - 11
    open_sqrt_error_bound = depth_two_open_sqrt_error_bound(
        p,
        error_split,
    )
    crude_open_sqrt_error_bound = (
        depth_two_open_sqrt_error_bound(p, crude_error_split)
    )
    uniform_prime_threshold = kummer_quadratic_uniform_prime_threshold(
        principal_weight,
        int(error_split["weighted_error_l1_bound"]) + 6 * denominator,
        sqrt_error_weight=6
        * (
            int(error_split["jacobi_l1_bound"])
            + int(error_split["conic_l1_bound"])
        ),
    )
    crude_lower_numerator = principal_weight * principal_exact_count - (
        p * int(crude_error_split["weighted_error_l1_bound"])
        + crude_open_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    lower_numerator = principal_weight * principal_exact_count - (
        p * int(error_split["weighted_error_l1_bound"])
        + open_sqrt_error_bound
        + degeneracy_line_union_count * denominator
    )
    admissible_per_coset_lower_bound = (
        (lower_numerator + denominator - 1) // denominator
        if lower_numerator > 0
        else 0
    )
    return {
        "quotient_order": quotient_order,
        "effective_window_size": effective_window_size,
        "window_count": math.comb(
            quotient_order - 1,
            effective_window_size - 1,
        ),
        "label_triple_count": label_triple_count,
        "fiber_size": fiber_size,
        "kernel_character_order": kernel_character_order,
        "square_kernel_index": square_kernel_index,
        "square_coset_index": square_coset_index,
        "denominator": denominator,
        "nonprincipal_tuple_count_bound": denominator - 1,
        "divisor_power_failure_count": 0,
        "divisor_nontriviality_check": True,
        "radical_component_degrees": radical_component_degrees,
        "radical_total_degree": radical_total_degree,
        "deligne_constant_formula": "(radical_total_degree - 1)^2",
        "deligne_constant": deligne_constant,
        "deligne_constant_check": nonprincipal_constant == deligne_constant,
        "principal_weight": principal_weight,
        "coefficient_abs_bound": coefficient_abs_bound,
        "crude_coefficient_abs_bound": label_triple_count,
        "ambient_restriction_kernel_count": ambient_restriction_kernel_count,
        "quotient_l1_exact": bool(quotient_l1_data["exact"]),
        "quotient_l1_zero_subset_histogram": quotient_l1_data.get(
            "zero_subset_count_histogram"
        ),
        "quotient_l1_coefficient_histogram": quotient_l1_data.get(
            "coefficient_value_histogram"
        ),
        "quotient_one_coordinate_l1_bound": quotient_one_coordinate_l1_bound,
        "quotient_two_coordinate_l1_bound": quotient_active_two_l1_bound,
        "quotient_three_coordinate_l1_bound": quotient_active_three_l1_bound,
        "quotient_coefficient_l1_bound": quotient_coefficient_l1_bound,
        "coefficient_l1_bound": coefficient_l1_bound,
        **error_split,
        "jacobi_error_constant": 1,
        "elementary_open_sqrt_constant": 6,
        "elementary_open_sqrt_error_bound": open_sqrt_error_bound,
        "weighted_error_total_bound": (
            p * int(error_split["weighted_error_l1_bound"])
            + open_sqrt_error_bound
        ),
        "conic_error_constant": 1,
        "crude_coefficient_l1_bound": crude_coefficient_l1_bound,
        "crude_jacobi_l1_bound": crude_error_split["jacobi_l1_bound"],
        "crude_conic_l1_bound": crude_error_split["conic_l1_bound"],
        "crude_quadratic_one_coordinate_l1_bound": (
            crude_error_split["quadratic_one_coordinate_l1_bound"]
        ),
        "crude_one_coordinate_kummer_l1_bound": (
            crude_error_split["one_coordinate_kummer_l1_bound"]
        ),
        "crude_two_coordinate_kummer_l1_bound": (
            crude_error_split["two_coordinate_kummer_l1_bound"]
        ),
        "crude_three_coordinate_kummer_l1_bound": (
            crude_error_split["three_coordinate_kummer_l1_bound"]
        ),
        "crude_kummer_l1_bound": crude_error_split["kummer_l1_bound"],
        "crude_weighted_error_l1_bound": (
            crude_error_split["weighted_error_l1_bound"]
        ),
        "crude_elementary_open_sqrt_error_bound": (
            crude_open_sqrt_error_bound
        ),
        "crude_weighted_error_total_bound": (
            p * int(crude_error_split["weighted_error_l1_bound"])
            + crude_open_sqrt_error_bound
        ),
        "uniform_prime_threshold": uniform_prime_threshold,
        "uniform_threshold_applies": p >= uniform_prime_threshold,
        "nonprincipal_constant": nonprincipal_constant,
        "principal_chi_minus_three": chi_minus_three,
        "principal_exact_count": principal_exact_count,
        "degeneracy_line_union_count": degeneracy_line_union_count,
        "crude_lower_numerator": crude_lower_numerator,
        "lower_numerator": lower_numerator,
        "admissible_per_coset_lower_bound": (
            admissible_per_coset_lower_bound
        ),
        "saturation_certificate": admissible_per_coset_lower_bound > 0,
    }


def slack_three_conic_shape_bound(p: int, domain_order: int) -> int:
    character_order = (p - 1) // domain_order
    character_cube = character_order * character_order * character_order
    conic_weil_constant = 6
    numerator = (
        p
        + 1
        + (character_cube - 1) * conic_weil_constant * ceil_sqrt(p)
    )
    return (numerator + character_cube - 1) // character_cube


def slack_three_cube_coset_uniform_prime_threshold(
    denominator: int,
) -> int:
    """Return a prime-independent threshold for the cube-coset certificate."""

    def bucket_min_positive(root_bucket: int) -> bool:
        bucket_start = (root_bucket - 1) * (root_bucket - 1) + 1
        return bucket_start - 13 > (12 * root_bucket + 12) * denominator

    high = 1
    while not bucket_min_positive(high):
        high *= 2
    low = high // 2
    while low + 1 < high:
        middle = (low + high) // 2
        if bucket_min_positive(middle):
            high = middle
        else:
            low = middle
    return (high - 1) * (high - 1) + 1


def slack_three_cube_coset_coverage_data(
    p: int,
    domain_order: int,
) -> Dict[str, object]:
    character_order = (p - 1) // domain_order
    cube_kernel_index = math.gcd(3, domain_order)
    cube_coset_index = character_order * cube_kernel_index
    denominator = (
        character_order
        * character_order
        * character_order
        * cube_coset_index
    )
    uniform_prime_threshold = (
        slack_three_cube_coset_uniform_prime_threshold(denominator)
    )
    conic_weil_constant = 12
    degeneracy_cost = 12
    principal_lower = p - 9 - 4 * quadratic_character(-3, p)
    numerator = principal_lower - (
        conic_weil_constant * ceil_sqrt(p) + degeneracy_cost
    ) * denominator
    admissible_parameter_lower_bound = (
        (numerator + denominator - 1) // denominator
        if numerator > 0
        else 0
    )
    return {
        "character_order": character_order,
        "cube_kernel_index": cube_kernel_index,
        "cube_coset_index": cube_coset_index,
        "denominator": denominator,
        "uniform_prime_threshold": uniform_prime_threshold,
        "uniform_threshold_applies": p >= uniform_prime_threshold,
        "principal_lower": principal_lower,
        "conic_weil_constant": conic_weil_constant,
        "degeneracy_cost": degeneracy_cost,
        "lower_numerator": numerator,
        "admissible_parameter_lower_bound": (
            admissible_parameter_lower_bound
        ),
        "saturation_certificate": admissible_parameter_lower_bound > 0,
    }


def occupancy_histogram(
    support: Sequence[int],
    quotient_order: int,
    fiber_size: int,
) -> Tuple[int, ...]:
    occupancies = [0] * quotient_order
    for index in support:
        occupancies[index % quotient_order] += 1
    histogram = [0] * (fiber_size + 1)
    for occupancy in occupancies:
        histogram[occupancy] += 1
    return tuple(histogram)


def histogram_text(histogram: Sequence[int]) -> str:
    return ",".join(
        f"{occupancy}:{count}"
        for occupancy, count in enumerate(histogram)
        if count
    )


def classify_histogram(histogram: Sequence[int]) -> str:
    fiber_size = len(histogram) - 1
    partial = [
        (occupancy, count)
        for occupancy, count in enumerate(histogram)
        if 0 < occupancy < fiber_size and count
    ]
    if not partial:
        return "whole_fiber"
    if len(partial) == 1 and partial[0][1] == 1:
        return "one_remainder"
    if len(partial) == 1:
        return "single_partial_occupancy"
    return "mixed_partial_occupancy"


def empty_histogram_record(histogram: Sequence[int]) -> Dict[str, object]:
    return {
        "histogram": list(histogram),
        "histogram_text": histogram_text(histogram),
        "class": classify_histogram(histogram),
        "support_count": 0,
        "predicted_support_count": 0,
        "contained_support_count": 0,
        "no_slope_support_count": 0,
        "incidence_count": 0,
        "canonical_zero_prefix_support_count": 0,
        "canonical_residual_zero_prefix_support_count": 0,
        "canonical_low_residual_zero_prefix_count": 0,
        "canonical_boundary_residual_coset_count": 0,
        "canonical_boundary_residual_coset_mismatch_count": 0,
        "canonical_boundary_touched_fiber_mismatch_count": 0,
        "canonical_residual_slope_mismatch_count": 0,
        "canonical_boundary_slope_mismatch_count": 0,
        "residual_size_histogram": Counter(),
        "bad_slopes": set(),
        "slope_histogram": Counter(),
    }


def retained_histograms(
    records: Sequence[Dict[str, object]],
    top_histograms: int,
) -> List[Dict[str, object]]:
    retained = records if top_histograms < 0 else records[:top_histograms]
    output = []
    for record in retained:
        slope_histogram = record["slope_histogram"]
        assert isinstance(slope_histogram, Counter)
        bad_slopes = record["bad_slopes"]
        assert isinstance(bad_slopes, set)
        residual_size_histogram = record["residual_size_histogram"]
        assert isinstance(residual_size_histogram, Counter)
        item = {
            key: value
            for key, value in record.items()
            if key not in {
                "bad_slopes",
                "slope_histogram",
                "residual_size_histogram",
            }
        }
        item["bad_slope_count"] = len(bad_slopes)
        item["bad_slopes"] = sorted(bad_slopes)
        item["slope_histogram"] = {
            str(slope): count for slope, count in sorted(slope_histogram.items())
        }
        item["residual_size_histogram"] = {
            str(size): count
            for size, count in sorted(residual_size_histogram.items())
        }
        output.append(item)
    return output


def scan_supports(
    p: int,
    n: int,
    k: int,
    slack: int,
    quotient_order: int,
    primitive: Optional[int],
    anchor_exp: Optional[int],
    direction_exp: Optional[int],
    max_supports: int,
    top_histograms: int,
) -> Dict[str, object]:
    support_size = k + slack
    if support_size > n:
        raise ValueError("require k + slack <= n")
    if n % quotient_order:
        raise ValueError("--quotient-order must divide --n")
    fiber_size = n // quotient_order

    total_supports = math.comb(n, support_size)
    if total_supports > max_supports:
        raise ValueError(
            f"scan needs {total_supports} supports; raise --max-supports to run it"
        )

    primitive, domain = make_domain(p, n, primitive)
    anchor_exp = k + slack if anchor_exp is None else anchor_exp
    direction_exp = k if direction_exp is None else direction_exp
    anchor = monomial_word(domain, anchor_exp, p)
    direction = monomial_word(domain, direction_exp, p)
    canonical_line = anchor_exp == k + slack and direction_exp == k
    low_deficit_limit = min(slack - 1, fiber_size - 1)
    canonical_formula_mismatches = 0
    low_deficit_mismatches = 0
    residual_zero_prefix_mismatches = 0
    canonical_zero_prefix_count = 0
    canonical_residual_zero_prefix_count = 0
    canonical_low_residual_zero_prefix_count = 0
    canonical_boundary_residual_coset_count = 0
    canonical_boundary_residual_coset_mismatches = 0
    canonical_boundary_touched_fiber_mismatches = 0
    canonical_subboundary_floor_violations = 0
    canonical_residual_slope_mismatches = 0
    canonical_boundary_slope_mismatches = 0
    canonical_small_residual_depth_gate_mismatches = 0
    residual_size_histogram: Counter[int] = Counter()
    support_residue = support_size % fiber_size
    superboundary_active_depth = (
        support_residue - slack
        if 0 < slack < support_residue < fiber_size
        else None
    )
    positive_dither_clearance_applies = 0 < support_residue < slack < fiber_size
    positive_dither_inferred_r = (
        slack - support_residue if positive_dither_clearance_applies else None
    )
    positive_dither_exact_dimension = (
        k + positive_dither_inferred_r
        if positive_dither_inferred_r is not None
        else None
    )
    positive_dither_dyadic_prefix_scale_count = (
        slack.bit_length() - 1 if positive_dither_clearance_applies else None
    )
    (
        small_residual_regime,
        expected_small_residual_support_count,
        expected_small_residual_slope_count,
        expected_small_residual_slope_multiplicity,
    ) = expected_small_residual_ledger(
        domain_order=n,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
        support_size=support_size,
        slack=slack,
    )
    subboundary_floor = subboundary_residual_floor(
        support_size=support_size,
        fiber_size=fiber_size,
        slack=slack,
    )
    expected_boundary_count = expected_boundary_residual_coset_count(
        domain_order=n,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
        support_size=support_size,
        slack=slack,
    )
    (
        expected_boundary_slope_count,
        expected_boundary_slope_multiplicity,
    ) = expected_boundary_slope_data(
        domain_order=n,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
        support_size=support_size,
        slack=slack,
    )
    expected_boundary_touched_fibers = (
        slack // math.gcd(slack, fiber_size)
        if slack < fiber_size and n % slack == 0
        else None
    )
    (
        expected_first_superboundary_zero_packet_count,
        expected_first_superboundary_zero_support_count,
        expected_first_superboundary_zero_lift_multiplicity,
        expected_first_superboundary_zero_touched_fibers,
    ) = expected_first_superboundary_zero_slope_data(
        domain_order=n,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
        support_size=support_size,
        slack=slack,
    )
    expected_terminal_pure_zero_data = expected_terminal_pure_zero_chain_data(
        domain_order=n,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
        support_size=support_size,
        slack=slack,
    )

    records: Dict[Tuple[int, ...], Dict[str, object]] = {}
    bad_slopes = set()
    boundary_slope_histogram: Counter[int] = Counter()
    small_residual_slope_histogram: Counter[int] = Counter()
    canonical_slope_histogram: Counter[int] = Counter()
    residual_packet_records: Dict[Tuple[int, ...], Dict[str, object]] = {}
    canonical_small_residual_support_count = 0
    incidence_count = 0
    contained_count = 0
    no_slope_count = 0

    for support in combinations(range(n), support_size):
        histogram = occupancy_histogram(support, quotient_order, fiber_size)
        if histogram not in records:
            records[histogram] = empty_histogram_record(histogram)
        record = records[histogram]
        record["support_count"] = int(record["support_count"]) + 1

        support_values = [domain[index] for index in support]
        residual = residual_support_indices(
            support,
            quotient_order,
            fiber_size,
        )
        residual_values = [domain[index] for index in residual]
        quotient_core_sum = quotient_core_value_sum(
            support,
            quotient_order,
            fiber_size,
            domain,
            p,
        )
        residual_size = len(residual)
        residual_size_histogram[residual_size] += 1
        record_residual_sizes = record["residual_size_histogram"]
        assert isinstance(record_residual_sizes, Counter)
        record_residual_sizes[residual_size] += 1
        support_sym = elementary_symmetric_prefix(support_values, slack, p)
        residual_sym = elementary_symmetric_prefix(residual_values, slack, p)
        for degree in range(1, low_deficit_limit + 1):
            if support_sym[degree] != residual_sym[degree]:
                low_deficit_mismatches += 1
        residual_zero_prefix = all(
            residual_sym[degree] % p == 0 for degree in range(1, slack)
        )
        if residual_zero_prefix:
            canonical_residual_zero_prefix_count += 1
            record["canonical_residual_zero_prefix_support_count"] = (
                int(record["canonical_residual_zero_prefix_support_count"]) + 1
            )

        anchor_top = top_coefficients(anchor, domain, support, k, slack, p)
        direction_top = top_coefficients(direction, domain, support, k, slack, p)
        slope = slope_from_top_coefficients(anchor_top, direction_top, p)

        if canonical_line:
            canonical_slope = canonical_slope_from_symmetric_prefix(
                support_values,
                slack,
                p,
            )
            if canonical_slope is not None:
                canonical_zero_prefix_count += 1
                canonical_slope_histogram[canonical_slope] += 1
                record["canonical_zero_prefix_support_count"] = (
                    int(record["canonical_zero_prefix_support_count"]) + 1
                )
                if residual_size < fiber_size and residual_size != support_residue:
                    canonical_small_residual_depth_gate_mismatches += 1
                if slack < fiber_size:
                    packet = residual_packet_records.setdefault(
                        residual,
                        {
                            "residual_size": residual_size,
                            "touched_fibers": residual_touched_fiber_count(
                                residual,
                                quotient_order,
                            ),
                            "observed_support_count": 0,
                            "slope_histogram": Counter(),
                        },
                    )
                    packet["observed_support_count"] = (
                        int(packet["observed_support_count"]) + 1
                    )
                    packet_slope_histogram = packet["slope_histogram"]
                    assert isinstance(packet_slope_histogram, Counter)
                    packet_slope_histogram[canonical_slope] += 1
                if residual_size < fiber_size:
                    canonical_small_residual_support_count += 1
                    small_residual_slope_histogram[canonical_slope] += 1
            if slack <= fiber_size and (canonical_slope is not None) != (
                residual_zero_prefix
            ):
                residual_zero_prefix_mismatches += 1
            if slope != canonical_slope:
                canonical_formula_mismatches += 1
            if (
                subboundary_floor is not None
                and canonical_slope is not None
                and residual_size < subboundary_floor
            ):
                canonical_subboundary_floor_violations += 1
            if canonical_slope is not None and slack < fiber_size:
                residual_slope = canonical_slope_from_symmetric_prefix(
                    residual_values,
                    slack,
                    p,
                )
                if residual_slope != canonical_slope:
                    canonical_residual_slope_mismatches += 1
                    record["canonical_residual_slope_mismatch_count"] = (
                        int(record["canonical_residual_slope_mismatch_count"])
                        + 1
                    )
            if slack == fiber_size:
                support_slope_value = signed_symmetric_coefficient(
                    support_values,
                    slack,
                    p,
                )
                residual_slope_value = signed_symmetric_coefficient(
                    residual_values,
                    slack,
                    p,
                )
                boundary_value = (residual_slope_value - quotient_core_sum) % p
                if support_slope_value != boundary_value:
                    canonical_boundary_slope_mismatches += 1
                    record["canonical_boundary_slope_mismatch_count"] = (
                        int(record["canonical_boundary_slope_mismatch_count"])
                        + 1
                    )
            if (
                slack <= fiber_size
                and canonical_slope is not None
                and 0 < residual_size < slack
            ):
                canonical_low_residual_zero_prefix_count += 1
                record["canonical_low_residual_zero_prefix_count"] = (
                    int(record["canonical_low_residual_zero_prefix_count"]) + 1
                )
            if (
                slack <= fiber_size
                and canonical_slope is not None
                and residual_size == slack
            ):
                canonical_boundary_residual_coset_count += 1
                record["canonical_boundary_residual_coset_count"] = (
                    int(record["canonical_boundary_residual_coset_count"]) + 1
                )
                boundary_slope_histogram[canonical_slope] += 1
                if not is_power_coset(residual_values, slack, p):
                    canonical_boundary_residual_coset_mismatches += 1
                    record[
                        "canonical_boundary_residual_coset_mismatch_count"
                    ] = (
                        int(
                            record[
                                "canonical_boundary_residual_coset_mismatch_count"
                            ]
                        )
                        + 1
                    )
                touched_fibers = residual_touched_fiber_count(
                    residual,
                    quotient_order,
                )
                if (
                    expected_boundary_touched_fibers is not None
                    and touched_fibers != expected_boundary_touched_fibers
                ):
                    canonical_boundary_touched_fiber_mismatches += 1
                    record[
                        "canonical_boundary_touched_fiber_mismatch_count"
                    ] = (
                        int(
                            record[
                                "canonical_boundary_touched_fiber_mismatch_count"
                            ]
                        )
                        + 1
                    )

        contained = all(entry == 0 for entry in anchor_top) and all(
            entry == 0 for entry in direction_top
        )
        if contained:
            contained_count += 1
            record["contained_support_count"] = (
                int(record["contained_support_count"]) + 1
            )
            continue

        if slope is None:
            no_slope_count += 1
            record["no_slope_support_count"] = (
                int(record["no_slope_support_count"]) + 1
            )
            continue

        incidence_count += 1
        bad_slopes.add(slope)
        record["incidence_count"] = int(record["incidence_count"]) + 1
        record_bad_slopes = record["bad_slopes"]
        assert isinstance(record_bad_slopes, set)
        record_bad_slopes.add(slope)
        slope_histogram = record["slope_histogram"]
        assert isinstance(slope_histogram, Counter)
        slope_histogram[slope] += 1

    for histogram, record in records.items():
        predicted = occupancy_family_size(quotient_order, fiber_size, histogram)
        record["predicted_support_count"] = predicted
        record["support_count_matches_prediction"] = (
            int(record["support_count"]) == predicted
        )
        record_outcomes = (
            int(record["contained_support_count"])
            + int(record["no_slope_support_count"])
            + int(record["incidence_count"])
        )
        record["support_outcome_partition"] = (
            record_outcomes == int(record["support_count"])
        )

    ordered_records = sorted(
        records.values(),
        key=lambda item: (
            -int(item["incidence_count"]),
            -len(item["bad_slopes"]),
            -int(item["support_count"]),
            str(item["histogram_text"]),
        ),
    )
    support_count_sum = sum(int(item["support_count"]) for item in ordered_records)
    predictions_match = all(
        bool(item["support_count_matches_prediction"]) for item in ordered_records
    )
    record_outcomes_match = all(
        bool(item["support_outcome_partition"]) for item in ordered_records
    )
    outcome_count_sum = contained_count + no_slope_count + incidence_count
    outcome_partition = outcome_count_sum == total_supports and record_outcomes_match
    residual_packet_lift_mismatches = 0
    residual_packet_slope_mismatches = 0
    residual_packet_weighted_support_count = 0
    residual_packet_size_histogram: Counter[int] = Counter()
    residual_packet_touched_fiber_histogram: Counter[int] = Counter()
    residual_packet_slope_histogram: Counter[int] = Counter()
    first_superboundary_packet_count = 0
    first_superboundary_zero_slope_packet_count = 0
    first_superboundary_zero_slope_support_count = 0
    first_superboundary_zero_slope_coset_mismatches = 0
    first_superboundary_packet_slope_histogram: Counter[int] = Counter()
    first_superboundary_slope_histogram: Counter[int] = Counter()
    second_superboundary_packet_count = 0
    second_superboundary_packet_slope_histogram: Counter[int] = Counter()
    second_superboundary_slope_histogram: Counter[int] = Counter()
    slack_two_second_superboundary_packet_count = 0
    slack_two_second_superboundary_packet_slope_histogram: Counter[int] = Counter()
    slack_two_second_superboundary_slope_histogram: Counter[int] = Counter()
    terminal_pure_zero_packet_counts: Counter[int] = Counter()
    terminal_pure_zero_support_counts: Counter[int] = Counter()
    terminal_pure_zero_slope_mismatches = 0
    terminal_pure_zero_touched_fiber_mismatches = 0
    first_nonzero_frontier_packet_counts: Counter[str] = Counter()
    first_nonzero_frontier_support_counts: Counter[str] = Counter()
    first_nonzero_frontier_slope_histograms: Dict[str, Counter[int]] = {}
    first_nonzero_frontier_packet_count = 0
    first_nonzero_frontier_support_count = 0
    first_nonzero_frontier_original_slope_mismatches = 0

    for residual, packet in residual_packet_records.items():
        residual_size = int(packet["residual_size"])
        touched_fibers = int(packet["touched_fibers"])
        expected_lift_count = expected_residual_packet_lift_count(
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            residual_size=residual_size,
            touched_fibers=touched_fibers,
        )
        packet["expected_lift_count"] = expected_lift_count
        residual_packet_weighted_support_count += expected_lift_count
        residual_packet_size_histogram[residual_size] += 1
        residual_packet_touched_fiber_histogram[touched_fibers] += 1
        if int(packet["observed_support_count"]) != expected_lift_count:
            residual_packet_lift_mismatches += 1
        slope_histogram = packet["slope_histogram"]
        assert isinstance(slope_histogram, Counter)
        if len(slope_histogram) != 1:
            residual_packet_slope_mismatches += 1
            continue
        slope = next(iter(slope_histogram))
        residual_packet_slope_histogram[slope] += expected_lift_count
        residual_values = [domain[index] for index in residual]
        if slack < residual_size < fiber_size:
            first_nonzero_frontier_packet_count += 1
            first_nonzero_frontier_support_count += expected_lift_count
            frontier_degree, frontier_slope = first_nonzero_frontier(
                residual_values,
                slack,
                p,
            )
            frontier_key = (
                "terminal" if frontier_degree is None else str(frontier_degree)
            )
            first_nonzero_frontier_packet_counts[frontier_key] += 1
            first_nonzero_frontier_support_counts[frontier_key] += (
                expected_lift_count
            )
            first_nonzero_frontier_slope_histograms.setdefault(
                frontier_key,
                Counter(),
            )[frontier_slope] += expected_lift_count
            expected_original_slope = (
                frontier_slope if frontier_degree == slack else 0
            )
            if slope != expected_original_slope:
                first_nonzero_frontier_original_slope_mismatches += 1
        if residual_size in expected_terminal_pure_zero_data:
            if is_power_coset(residual_values, residual_size, p):
                terminal_pure_zero_packet_counts[residual_size] += 1
                terminal_pure_zero_support_counts[residual_size] += (
                    expected_lift_count
                )
                if slope != 0:
                    terminal_pure_zero_slope_mismatches += 1
                expected_touched = expected_terminal_pure_zero_data[
                    residual_size
                ]["touched_fibers"]
                if (
                    expected_touched is not None
                    and touched_fibers != expected_touched
                ):
                    terminal_pure_zero_touched_fiber_mismatches += 1
        if residual_size == slack + 1:
            first_superboundary_packet_count += 1
            first_superboundary_packet_slope_histogram[slope] += 1
            first_superboundary_slope_histogram[slope] += expected_lift_count
            if slope == 0:
                first_superboundary_zero_slope_packet_count += 1
                first_superboundary_zero_slope_support_count += (
                    expected_lift_count
                )
                residual_values = [domain[index] for index in residual]
                if not is_power_coset(residual_values, slack + 1, p):
                    first_superboundary_zero_slope_coset_mismatches += 1
        if residual_size == slack + 2:
            second_superboundary_packet_count += 1
            second_superboundary_packet_slope_histogram[slope] += 1
            second_superboundary_slope_histogram[slope] += expected_lift_count
        if slack == 2 and residual_size == 4:
            slack_two_second_superboundary_packet_count += 1
            slack_two_second_superboundary_packet_slope_histogram[slope] += 1
            slack_two_second_superboundary_slope_histogram[
                slope
            ] += expected_lift_count
    first_superboundary_support_count = sum(
        first_superboundary_slope_histogram.values()
    )
    slack_two_second_superboundary_support_count = sum(
        slack_two_second_superboundary_slope_histogram.values()
    )
    second_superboundary_support_count = sum(
        second_superboundary_slope_histogram.values()
    )
    terminal_pure_zero_expected_packet_counts = {
        size: int(item["packet_count"] or 0)
        for size, item in expected_terminal_pure_zero_data.items()
    }
    terminal_pure_zero_expected_support_counts = {
        size: int(item["support_count"] or 0)
        for size, item in expected_terminal_pure_zero_data.items()
    }
    terminal_pure_zero_packet_count_check = all(
        terminal_pure_zero_packet_counts[size]
        == terminal_pure_zero_expected_packet_counts[size]
        for size in expected_terminal_pure_zero_data
    )
    terminal_pure_zero_support_count_check = all(
        terminal_pure_zero_support_counts[size]
        == terminal_pure_zero_expected_support_counts[size]
        for size in expected_terminal_pure_zero_data
    )
    terminal_pure_zero_chain_check = (
        terminal_pure_zero_packet_count_check
        and terminal_pure_zero_support_count_check
        and terminal_pure_zero_slope_mismatches == 0
        and terminal_pure_zero_touched_fiber_mismatches == 0
    )
    first_nonzero_frontier_partition_check = (
        sum(first_nonzero_frontier_packet_counts.values())
        == first_nonzero_frontier_packet_count
        and sum(first_nonzero_frontier_support_counts.values())
        == first_nonzero_frontier_support_count
    )
    first_nonzero_frontier_original_slope_check = (
        first_nonzero_frontier_original_slope_mismatches == 0
    )
    first_nonzero_frontier_check = (
        first_nonzero_frontier_partition_check
        and first_nonzero_frontier_original_slope_check
    )
    first_superboundary_residual_size = slack + 1
    first_superboundary_lift_dividend = support_size - first_superboundary_residual_size
    first_superboundary_lift_remainder = (
        first_superboundary_lift_dividend % fiber_size
        if first_superboundary_lift_dividend >= 0
        else None
    )
    first_superboundary_lift_gate_active = (
        first_superboundary_lift_remainder == 0
        if first_superboundary_lift_remainder is not None
        else False
    )
    first_superboundary_lift_whole_fibers = (
        first_superboundary_lift_dividend // fiber_size
        if first_superboundary_lift_gate_active
        else None
    )
    first_superboundary_lift_gate_check = (
        first_superboundary_lift_gate_active
        or (
            first_superboundary_packet_count == 0
            and first_superboundary_support_count == 0
        )
    )
    second_superboundary_residual_size = slack + 2
    second_superboundary_lift_dividend = (
        support_size - second_superboundary_residual_size
    )
    second_superboundary_lift_remainder = (
        second_superboundary_lift_dividend % fiber_size
        if second_superboundary_lift_dividend >= 0
        else None
    )
    second_superboundary_lift_gate_active = (
        second_superboundary_lift_remainder == 0
        if second_superboundary_lift_remainder is not None
        else False
    )
    second_superboundary_lift_whole_fibers = (
        second_superboundary_lift_dividend // fiber_size
        if second_superboundary_lift_gate_active
        else None
    )
    second_superboundary_lift_gate_check = (
        second_superboundary_lift_gate_active
        or (
            second_superboundary_packet_count == 0
            and second_superboundary_support_count == 0
        )
    )
    slack_two_second_superboundary_residual_size = 4
    slack_two_second_superboundary_lift_dividend = (
        support_size - slack_two_second_superboundary_residual_size
    )
    slack_two_second_superboundary_lift_remainder = (
        slack_two_second_superboundary_lift_dividend % fiber_size
        if slack_two_second_superboundary_lift_dividend >= 0
        else None
    )
    slack_two_second_superboundary_lift_gate_active = (
        slack_two_second_superboundary_lift_remainder == 0
        if slack_two_second_superboundary_lift_remainder is not None
        else False
    )
    slack_two_second_superboundary_lift_whole_fibers = (
        slack_two_second_superboundary_lift_dividend // fiber_size
        if slack_two_second_superboundary_lift_gate_active
        else None
    )
    (
        slack_two_second_all_shapes_lift_active_gate,
        slack_two_second_lift_safety_remaining_fibers,
        slack_two_second_lift_safety_required_fibers,
    ) = all_residual_packets_lift_active(
        support_size=support_size,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
        residual_size=slack_two_second_superboundary_residual_size,
    )
    slack_two_second_superboundary_lift_gate_check = (
        slack_two_second_superboundary_lift_gate_active
        or (
            slack_two_second_superboundary_packet_count == 0
            and slack_two_second_superboundary_support_count == 0
        )
    )
    first_superboundary_shape_ledger = (
        first_superboundary_shape_coset_ledger(
            p=p,
            domain=domain,
            slack=slack,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if canonical_line and slack + 1 < fiber_size and slack <= 4
        else None
    )
    second_superboundary_shape_ledger = (
        second_superboundary_shape_coset_ledger(
            p=p,
            domain=domain,
            slack=slack,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if canonical_line and slack + 2 < fiber_size and slack <= 3
        else None
    )
    slack_two_shape_ledger = (
        slack_two_first_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if canonical_line and slack == 2 and slack + 1 < fiber_size
        else None
    )
    slack_two_second_shape_ledger = (
        slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if canonical_line and slack == 2 and slack + 2 < fiber_size
        else None
    )
    slack_three_shape_ledger = (
        slack_three_first_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if canonical_line and slack == 3 and slack + 1 < fiber_size
        else None
    )
    slack_two_full_domain_alpha_data = (
        full_domain_slack_two_alpha_class_data(p)
        if slack_two_shape_ledger is not None and n == p - 1
        else None
    )
    slack_two_depth_two_full_domain_A_data = (
        full_domain_slack_two_depth_two_A_class_data(p)
        if slack_two_second_shape_ledger is not None and n == p - 1
        else None
    )
    slack_two_second_kummer_saturation = (
        slack_two_second_kummer_saturation_data(p, n)
        if slack_two_second_shape_ledger is not None
        else None
    )
    slack_two_second_two_fiber_kummer_saturation = (
        slack_two_second_two_fiber_kummer_saturation_data(
            p,
            n,
            quotient_order,
        )
        if slack_two_second_shape_ledger is not None
        else None
    )
    slack_three_full_domain_beta_data = (
        full_domain_slack_three_beta_class_data(p)
        if slack_three_shape_ledger is not None and n == p - 1
        else None
    )
    slack_two_cyclotomic_bound = (
        slack_two_cyclotomic_shape_bound(p, n)
        if slack_two_shape_ledger is not None
        else None
    )
    slack_two_cyclotomic_slope_bound = (
        min(
            p,
            1
            + (
                (slack_two_cyclotomic_bound + 5) // 6
            )
            * (n // math.gcd(2, n)),
        )
        if slack_two_cyclotomic_bound is not None
        else None
    )
    slack_three_cyclotomic_bound = (
        slack_three_conic_shape_bound(p, n)
        if slack_three_shape_ledger is not None
        else None
    )
    slack_three_cyclotomic_slope_bound = (
        min(
            p,
            1
            + (
                (slack_three_cyclotomic_bound + 23) // 24
            )
            * (n // math.gcd(3, n)),
        )
        if slack_three_cyclotomic_bound is not None
        else None
    )
    slack_three_cube_coset_coverage = (
        slack_three_cube_coset_coverage_data(p, n)
        if slack_three_shape_ledger is not None
        else None
    )
    slack_three_cube_coset_parameter_lower_bound = (
        int(
            slack_three_cube_coset_coverage[
                "admissible_parameter_lower_bound"
            ]
        )
        if slack_three_cube_coset_coverage is not None
        else None
    )
    slack_three_exact_min_cube_coset_parameter_count = None
    if slack_three_shape_ledger is not None:
        exact_beta_counts = list(
            slack_three_shape_ledger["nonzero_cube_coset_beta_counts"]
        )
        if int(slack_three_shape_ledger["nonzero_cube_coset_count"]) < int(
            slack_three_shape_ledger["total_nonzero_cube_coset_count"]
        ):
            slack_three_exact_min_cube_coset_parameter_count = 0
        elif exact_beta_counts:
            slack_three_exact_min_cube_coset_parameter_count = (
                6 * min(exact_beta_counts)
            )
        else:
            slack_three_exact_min_cube_coset_parameter_count = 0

    slack_two_second_two_fiber_union_reduction = (
        slack_two_second_two_fiber_union_reduction_data(
            p,
            domain,
            quotient_order,
        )
        if (
            slack_two_second_shape_ledger is not None
            and slack_two_second_shape_ledger["lift_limited_remaining_fibers"]
            == 2
        )
        else None
    )
    slack_two_second_r_window_reduction = (
        slack_two_second_quotient_window_reduction_data(
            p,
            domain,
            quotient_order,
            slack_two_second_shape_ledger["lift_limited_remaining_fibers"],
        )
        if (
            slack_two_second_shape_ledger is not None
            and slack_two_second_shape_ledger["lift_limited_remaining_fibers"]
            is not None
            and int(slack_two_second_shape_ledger["lift_limited_remaining_fibers"])
            < min(4, quotient_order)
        )
        else None
    )
    slack_two_second_r_window_kummer_saturation = (
        slack_two_second_fixed_window_kummer_saturation_data(
            p,
            n,
            quotient_order,
            int(slack_two_second_shape_ledger["lift_limited_remaining_fibers"]),
        )
        if (
            slack_two_second_shape_ledger is not None
            and slack_two_second_shape_ledger["lift_limited_remaining_fibers"]
            is not None
            and 0
            < int(slack_two_second_shape_ledger["lift_limited_remaining_fibers"])
            < min(4, quotient_order)
        )
        else None
    )
    slack_two_second_r_window_union_kummer_saturation = (
        slack_two_second_quotient_window_union_kummer_saturation_data(
            p,
            n,
            quotient_order,
            int(slack_two_second_shape_ledger["lift_limited_remaining_fibers"]),
        )
        if (
            slack_two_second_shape_ledger is not None
            and slack_two_second_shape_ledger["lift_limited_remaining_fibers"]
            is not None
            and 0
            < int(slack_two_second_shape_ledger["lift_limited_remaining_fibers"])
            < min(4, quotient_order)
        )
        else None
    )
    slack_two_second_index_window_label = None
    slack_two_second_kummer_exact_support_saturation = False
    slack_two_second_two_fiber_exact_support_saturation = False
    slack_two_second_r2_union_exact_support_saturation = False
    slack_two_second_r_window_kummer_exact_support_saturation = False
    slack_two_second_r_window_union_kummer_exact_support_saturation = False
    slack_two_second_r_window_exact_support_saturation = False
    if slack_two_second_kummer_saturation is not None:
        slack_two_second_kummer_exact_support_saturation = (
            bool(slack_two_second_kummer_saturation["saturation_certificate"])
            and slack_two_second_all_shapes_lift_active_gate
        )
    if (
        slack_two_second_two_fiber_kummer_saturation is not None
        and slack_two_second_shape_ledger is not None
    ):
        remaining_fibers = slack_two_second_shape_ledger[
            "lift_limited_remaining_fibers"
        ]
        slack_two_second_two_fiber_exact_support_saturation = (
            bool(
                slack_two_second_two_fiber_kummer_saturation[
                    "saturation_certificate"
                ]
            )
            and remaining_fibers is not None
            and int(remaining_fibers) >= 2
        )
    if slack_two_second_two_fiber_union_reduction is not None:
        slack_two_second_r2_union_exact_support_saturation = bool(
            slack_two_second_two_fiber_union_reduction[
                "saturates_nonzero_square_cosets"
            ]
        )
    if slack_two_second_r_window_reduction is not None:
        slack_two_second_r_window_exact_support_saturation = bool(
            slack_two_second_r_window_reduction[
                "saturates_nonzero_square_cosets"
            ]
        )
    if slack_two_second_r_window_kummer_saturation is not None:
        slack_two_second_r_window_kummer_exact_support_saturation = bool(
            slack_two_second_r_window_kummer_saturation[
                "saturation_certificate"
            ]
        )
    if slack_two_second_r_window_union_kummer_saturation is not None:
        slack_two_second_r_window_union_kummer_exact_support_saturation = bool(
            slack_two_second_r_window_union_kummer_saturation[
                "saturation_certificate"
            ]
        )
    if (
        slack_two_second_shape_ledger is not None
        and slack_two_second_kummer_saturation is not None
    ):
        full_domain_raw_saturation = (
            slack_two_depth_two_full_domain_A_data is not None
            and bool(
                slack_two_depth_two_full_domain_A_data[
                    "saturates_nonzero_square_cosets"
                ]
            )
        )
        if not slack_two_second_superboundary_lift_gate_active:
            slack_two_second_index_window_label = "inactive_lift_gate"
        elif (
            full_domain_raw_saturation
            and slack_two_second_all_shapes_lift_active_gate
        ):
            slack_two_second_index_window_label = "full_domain_saturated"
        elif slack_two_second_kummer_exact_support_saturation:
            slack_two_second_index_window_label = "low_index_saturated"
        elif slack_two_second_two_fiber_exact_support_saturation:
            slack_two_second_index_window_label = "two_fiber_saturated"
        elif slack_two_second_r_window_kummer_exact_support_saturation:
            slack_two_second_index_window_label = "r_window_kummer_saturated"
        elif slack_two_second_r_window_union_kummer_exact_support_saturation:
            slack_two_second_index_window_label = (
                "r_window_union_kummer_saturated"
            )
        elif slack_two_second_r2_union_exact_support_saturation:
            slack_two_second_index_window_label = "r2_union_saturated"
        elif slack_two_second_r_window_exact_support_saturation:
            slack_two_second_index_window_label = "r_window_saturated"
        elif bool(
            slack_two_second_shape_ledger[
                "lift_limited_slope_bound_nontrivial"
            ]
        ):
            slack_two_second_index_window_label = "lift_limited_sparse"
        elif (
            full_domain_raw_saturation
            or bool(slack_two_second_kummer_saturation["saturation_certificate"])
        ):
            slack_two_second_index_window_label = "raw_saturated_lift_limited"
        elif bool(
            slack_two_second_shape_ledger["high_index_slope_bound_nontrivial"]
        ):
            slack_two_second_index_window_label = "high_index_sparse"
        else:
            slack_two_second_index_window_label = "intermediate_index_window"

    slack_two_second_kernel_reduction = (
        slack_two_second_shape_ledger["kernel_fiber_reduction"]
        if (
            slack_two_second_shape_ledger is not None
            and bool(slack_two_second_shape_ledger["kernel_fiber_reduction_active"])
        )
        else None
    )

    return {
        "proof_status": "AUDIT / EXPERIMENTAL",
        "theorem_problem_id": "M1-support-coefficient-occupancy-scan",
        "determinism": "deterministic exact support enumeration; no random seed",
        "parameters": {
            "prime": p,
            "domain_order": n,
            "primitive_generator": primitive,
            "k": k,
            "rho": fraction_string(k, n),
            "slack": slack,
            "support_size": support_size,
            "quotient_order": quotient_order,
            "fiber_size": fiber_size,
            "anchor_exponent": anchor_exp,
            "direction_exponent": direction_exp,
        },
        "domain": list(domain),
        "support_count": total_supports,
        "scanned_support_count": support_count_sum,
        "histogram_count": len(ordered_records),
        "histogram_counts_match_binomial": support_count_sum == total_supports,
        "histogram_counts_match_formula": predictions_match,
        "support_outcome_partition": outcome_partition,
        "canonical_line": canonical_line,
        "canonical_symmetric_formula_check": (
            canonical_formula_mismatches == 0 if canonical_line else None
        ),
        "canonical_symmetric_formula_mismatch_count": (
            canonical_formula_mismatches if canonical_line else None
        ),
        "canonical_zero_prefix_support_count": (
            canonical_zero_prefix_count if canonical_line else None
        ),
        "canonical_zero_prefix_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(canonical_slope_histogram.items())
            }
            if canonical_line
            else None
        ),
        "canonical_residual_zero_prefix_support_count": (
            canonical_residual_zero_prefix_count if canonical_line else None
        ),
        "canonical_residual_zero_prefix_match": (
            residual_zero_prefix_mismatches == 0
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_residual_zero_prefix_mismatch_count": (
            residual_zero_prefix_mismatches
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_low_residual_exclusion_check": (
            canonical_low_residual_zero_prefix_count == 0
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_low_residual_zero_prefix_count": (
            canonical_low_residual_zero_prefix_count
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_residual_coset_check": (
            canonical_boundary_residual_coset_mismatches == 0
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_residual_coset_count": (
            canonical_boundary_residual_coset_count
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_residual_coset_mismatch_count": (
            canonical_boundary_residual_coset_mismatches
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_residual_expected_count": (
            expected_boundary_count
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_residual_count_check": (
            canonical_boundary_residual_coset_count == expected_boundary_count
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_slope_expected_count": (
            expected_boundary_slope_count
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_slope_count": (
            len(boundary_slope_histogram)
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_slope_count_check": (
            len(boundary_slope_histogram) == expected_boundary_slope_count
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_slope_expected_multiplicity": (
            expected_boundary_slope_multiplicity
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_slope_multiplicity_check": (
            all(
                count == expected_boundary_slope_multiplicity
                for count in boundary_slope_histogram.values()
            )
            and len(boundary_slope_histogram) == expected_boundary_slope_count
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_boundary_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(boundary_slope_histogram.items())
            }
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_support_residue_mod_fiber": (
            support_residue if canonical_line and slack < fiber_size else None
        ),
        "canonical_small_residual_active_size": (
            support_residue if canonical_line and slack < fiber_size else None
        ),
        "canonical_superboundary_active_depth": (
            superboundary_active_depth
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_superboundary_active_depth_remainder_check": (
            (k - superboundary_active_depth) % fiber_size == 0
            if (
                canonical_line
                and slack < fiber_size
                and superboundary_active_depth is not None
            )
            else None
        ),
        "canonical_small_residual_depth_gate_check": (
            canonical_small_residual_depth_gate_mismatches == 0
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_small_residual_depth_gate_mismatch_count": (
            canonical_small_residual_depth_gate_mismatches
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_positive_dither_clearance_applies": (
            positive_dither_clearance_applies
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_positive_dither_inferred_r": (
            positive_dither_inferred_r
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_positive_dither_exact_dimension": (
            positive_dither_exact_dimension
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_positive_dither_prefix_max_fiber_size": (
            slack
            if (
                canonical_line
                and slack < fiber_size
                and positive_dither_clearance_applies
            )
            else None
        ),
        "canonical_positive_dither_dyadic_prefix_scale_count": (
            positive_dither_dyadic_prefix_scale_count
            if (
                canonical_line
                and slack < fiber_size
                and positive_dither_clearance_applies
            )
            else None
        ),
        "canonical_positive_dither_finite_prefix_check": (
            positive_dither_exact_dimension % fiber_size == 0
            and slack < fiber_size
            if (
                canonical_line
                and slack < fiber_size
                and positive_dither_clearance_applies
            )
            else None
        ),
        "canonical_positive_dither_residual_floor": (
            subboundary_floor
            if (
                canonical_line
                and slack < fiber_size
                and positive_dither_clearance_applies
            )
            else None
        ),
        "canonical_positive_dither_clearance_check": (
            canonical_small_residual_support_count == 0
            and subboundary_floor == fiber_size + support_residue
            and canonical_subboundary_floor_violations == 0
            if (
                canonical_line
                and slack < fiber_size
                and positive_dither_clearance_applies
            )
            else None
        ),
        "canonical_small_residual_regime": (
            small_residual_regime
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_small_residual_support_count": (
            canonical_small_residual_support_count
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_small_residual_expected_support_count": (
            expected_small_residual_support_count
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_small_residual_support_count_check": (
            canonical_small_residual_support_count
            == expected_small_residual_support_count
            if (
                canonical_line
                and slack < fiber_size
                and expected_small_residual_support_count is not None
            )
            else None
        ),
        "canonical_small_residual_slope_count": (
            len(small_residual_slope_histogram)
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_small_residual_expected_slope_count": (
            expected_small_residual_slope_count
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_small_residual_slope_count_check": (
            len(small_residual_slope_histogram)
            == expected_small_residual_slope_count
            if (
                canonical_line
                and slack < fiber_size
                and expected_small_residual_slope_count is not None
            )
            else None
        ),
        "canonical_small_residual_expected_slope_multiplicity": (
            expected_small_residual_slope_multiplicity
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_small_residual_slope_multiplicity_check": (
            all(
                count == expected_small_residual_slope_multiplicity
                for count in small_residual_slope_histogram.values()
            )
            and len(small_residual_slope_histogram)
            == expected_small_residual_slope_count
            if (
                canonical_line
                and slack < fiber_size
                and expected_small_residual_slope_multiplicity is not None
                and expected_small_residual_slope_count is not None
            )
            else None
        ),
        "canonical_small_residual_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(small_residual_slope_histogram.items())
            }
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_count": (
            len(residual_packet_records)
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_weighted_support_count": (
            residual_packet_weighted_support_count
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_lift_count_check": (
            residual_packet_lift_mismatches == 0
            and residual_packet_weighted_support_count == canonical_zero_prefix_count
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_lift_mismatch_count": (
            residual_packet_lift_mismatches
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_slope_consistency_check": (
            residual_packet_slope_mismatches == 0
            and residual_packet_slope_histogram == canonical_slope_histogram
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_slope_mismatch_count": (
            residual_packet_slope_mismatches
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_slope_count": (
            len(residual_packet_slope_histogram)
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(residual_packet_slope_histogram.items())
            }
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_size_histogram": (
            {
                str(size): count
                for size, count in sorted(residual_packet_size_histogram.items())
            }
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_packet_touched_fiber_histogram": (
            {
                str(size): count
                for size, count in sorted(
                    residual_packet_touched_fiber_histogram.items()
                )
            }
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_chain_check": (
            terminal_pure_zero_chain_check
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_packet_count_check": (
            terminal_pure_zero_packet_count_check
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_support_count_check": (
            terminal_pure_zero_support_count_check
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_slope_mismatch_count": (
            terminal_pure_zero_slope_mismatches
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_touched_fiber_mismatch_count": (
            terminal_pure_zero_touched_fiber_mismatches
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_observed_packet_counts": (
            {
                str(size): terminal_pure_zero_packet_counts[size]
                for size in sorted(expected_terminal_pure_zero_data)
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_expected_packet_counts": (
            {
                str(size): terminal_pure_zero_expected_packet_counts[size]
                for size in sorted(expected_terminal_pure_zero_data)
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_observed_support_counts": (
            {
                str(size): terminal_pure_zero_support_counts[size]
                for size in sorted(expected_terminal_pure_zero_data)
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_expected_support_counts": (
            {
                str(size): terminal_pure_zero_expected_support_counts[size]
                for size in sorted(expected_terminal_pure_zero_data)
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_terminal_pure_zero_expected_data": (
            {
                str(size): values
                for size, values in sorted(expected_terminal_pure_zero_data.items())
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_check": (
            first_nonzero_frontier_check
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_partition_check": (
            first_nonzero_frontier_partition_check
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_original_slope_check": (
            first_nonzero_frontier_original_slope_check
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_original_slope_mismatch_count": (
            first_nonzero_frontier_original_slope_mismatches
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_packet_count": (
            first_nonzero_frontier_packet_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_support_count": (
            first_nonzero_frontier_support_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_packet_counts": (
            {
                key: first_nonzero_frontier_packet_counts[key]
                for key in sorted(first_nonzero_frontier_packet_counts)
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_support_counts": (
            {
                key: first_nonzero_frontier_support_counts[key]
                for key in sorted(first_nonzero_frontier_support_counts)
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_nonzero_frontier_slope_histograms": (
            {
                key: {
                    str(slope): count
                    for slope, count in sorted(
                        first_nonzero_frontier_slope_histograms[key].items()
                    )
                }
                for key in sorted(first_nonzero_frontier_slope_histograms)
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_residual_size": (
            slack + 1 if canonical_line and slack + 1 < fiber_size else None
        ),
        "canonical_first_superboundary_lift_gate_remainder": (
            first_superboundary_lift_remainder
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_lift_gate_active": (
            first_superboundary_lift_gate_active
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_lift_gate_whole_fibers": (
            first_superboundary_lift_whole_fibers
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_lift_gate_check": (
            first_superboundary_lift_gate_check
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_packet_count": (
            first_superboundary_packet_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_support_count": (
            first_superboundary_support_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_slope_count": (
            len(first_superboundary_slope_histogram)
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_packet_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    first_superboundary_packet_slope_histogram.items()
                )
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    first_superboundary_slope_histogram.items()
                )
            }
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_packet_count": (
            first_superboundary_zero_slope_packet_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_expected_zero_slope_packet_count": (
            expected_first_superboundary_zero_packet_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_packet_count_check": (
            first_superboundary_zero_slope_packet_count
            == expected_first_superboundary_zero_packet_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_support_count": (
            first_superboundary_zero_slope_support_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_expected_zero_slope_support_count": (
            expected_first_superboundary_zero_support_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_support_count_check": (
            first_superboundary_zero_slope_support_count
            == expected_first_superboundary_zero_support_count
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_lift_multiplicity": (
            expected_first_superboundary_zero_lift_multiplicity
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_touched_fiber_count": (
            expected_first_superboundary_zero_touched_fibers
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_coset_check": (
            first_superboundary_zero_slope_coset_mismatches == 0
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_first_superboundary_zero_slope_coset_mismatch_count": (
            first_superboundary_zero_slope_coset_mismatches
            if canonical_line and slack + 1 < fiber_size
            else None
        ),
        "canonical_second_superboundary_residual_size": (
            second_superboundary_residual_size
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_lift_gate_remainder": (
            second_superboundary_lift_remainder
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_lift_gate_active": (
            second_superboundary_lift_gate_active
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_lift_gate_whole_fibers": (
            second_superboundary_lift_whole_fibers
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_lift_gate_check": (
            second_superboundary_lift_gate_check
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_packet_count": (
            second_superboundary_packet_count
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_support_count": (
            second_superboundary_support_count
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_slope_count": (
            len(second_superboundary_slope_histogram)
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_packet_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    second_superboundary_packet_slope_histogram.items()
                )
            }
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    second_superboundary_slope_histogram.items()
                )
            }
            if canonical_line and slack + 2 < fiber_size
            else None
        ),
        "canonical_second_superboundary_shape_orbit_factor": (
            int(second_superboundary_shape_ledger["orbit_factor"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_parameter_count": (
            int(second_superboundary_shape_ledger["parameter_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_active_parameter_count": (
            int(second_superboundary_shape_ledger["active_parameter_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_zero_next_slack_parameter_count": (
            int(second_superboundary_shape_ledger["zero_parameter_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_active_zero_parameter_count": (
            int(second_superboundary_shape_ledger["active_zero_parameter_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_zero_packet_count": (
            int(second_superboundary_shape_ledger["zero_packet_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_zero_support_count": (
            int(second_superboundary_shape_ledger["zero_weighted_support_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_first_parameter_count": (
            int(second_superboundary_shape_ledger["next_slack_first_parameter_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_first_active_parameter_count": (
            int(
                second_superboundary_shape_ledger[
                    "next_slack_first_active_parameter_count"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_first_packet_count": (
            int(second_superboundary_shape_ledger["next_slack_first_packet_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_first_support_count": (
            int(
                second_superboundary_shape_ledger[
                    "next_slack_first_weighted_support_count"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_parameter_check": (
            bool(
                second_superboundary_shape_ledger[
                    "next_slack_transition_parameter_check"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_active_parameter_check": (
            bool(
                second_superboundary_shape_ledger[
                    "next_slack_transition_active_parameter_check"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_packet_count_check": (
            bool(
                second_superboundary_shape_ledger[
                    "next_slack_transition_packet_count_check"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_next_slack_support_count_check": (
            bool(
                second_superboundary_shape_ledger[
                    "next_slack_transition_support_count_check"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_active_nonzero_orbit_check": (
            bool(
                second_superboundary_shape_ledger[
                    "active_nonzero_packet_orbit_check"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_active_nonzero_orbit_count": (
            int(
                second_superboundary_shape_ledger[
                    "active_nonzero_packet_orbit_count"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_orbit_quotient_check": (
            bool(second_superboundary_shape_ledger["orbit_quotient_check"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_expected_packet_count": (
            int(second_superboundary_shape_ledger["packet_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_packet_count_check": (
            int(second_superboundary_shape_ledger["packet_count"])
            == second_superboundary_packet_count
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_expected_support_count": (
            int(second_superboundary_shape_ledger["weighted_support_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_support_count_check": (
            int(second_superboundary_shape_ledger["weighted_support_count"])
            == second_superboundary_support_count
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_packet_slope_histogram_check": (
            second_superboundary_shape_ledger["packet_slope_histogram"]
            == second_superboundary_packet_slope_histogram
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_support_slope_histogram_check": (
            second_superboundary_shape_ledger["support_slope_histogram"]
            == second_superboundary_slope_histogram
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_nonzero_power_coset_count": (
            int(second_superboundary_shape_ledger["nonzero_power_coset_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_active_nonzero_power_coset_count": (
            int(
                second_superboundary_shape_ledger[
                    "active_nonzero_power_coset_count"
                ]
            )
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_power_image_size": (
            int(second_superboundary_shape_ledger["power_image_size"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_power_coset_slope_count": (
            int(second_superboundary_shape_ledger["power_coset_slope_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_power_coset_slope_count_check": (
            len(second_superboundary_slope_histogram)
            == int(second_superboundary_shape_ledger["power_coset_slope_count"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_power_coset_slope_bound": (
            int(second_superboundary_shape_ledger["power_coset_slope_bound"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_second_superboundary_shape_power_coset_slope_bound_check": (
            len(second_superboundary_slope_histogram)
            <= int(second_superboundary_shape_ledger["power_coset_slope_bound"])
            if second_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_superboundary_residual_size": (
            slack_two_second_superboundary_residual_size
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_lift_gate_remainder": (
            slack_two_second_superboundary_lift_remainder
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_lift_gate_active": (
            slack_two_second_superboundary_lift_gate_active
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_lift_gate_whole_fibers": (
            slack_two_second_superboundary_lift_whole_fibers
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_lift_safety_remaining_fibers": (
            slack_two_second_lift_safety_remaining_fibers
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_lift_safety_required_fibers": (
            slack_two_second_lift_safety_required_fibers
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_all_shapes_lift_active_gate": (
            slack_two_second_all_shapes_lift_active_gate
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_lift_gate_check": (
            slack_two_second_superboundary_lift_gate_check
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_packet_count": (
            slack_two_second_superboundary_packet_count
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_support_count": (
            slack_two_second_superboundary_support_count
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_slope_count": (
            len(slack_two_second_superboundary_slope_histogram)
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_packet_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_two_second_superboundary_packet_slope_histogram.items()
                )
            }
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_slack_two_second_superboundary_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_two_second_superboundary_slope_histogram.items()
                )
            }
            if canonical_line and slack == 2 and slack + 2 < fiber_size
            else None
        ),
        "canonical_first_superboundary_shape_orbit_factor": (
            int(first_superboundary_shape_ledger["orbit_factor"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_parameter_count": (
            int(first_superboundary_shape_ledger["parameter_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_active_parameter_count": (
            int(first_superboundary_shape_ledger["active_parameter_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_active_zero_parameter_count": (
            int(first_superboundary_shape_ledger["active_zero_parameter_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_active_nonzero_orbit_check": (
            bool(
                first_superboundary_shape_ledger[
                    "active_nonzero_parameter_orbit_check"
                ]
            )
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_nonzero_power_coset_count": (
            int(first_superboundary_shape_ledger["nonzero_power_coset_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_active_nonzero_power_coset_count": (
            int(
                first_superboundary_shape_ledger[
                    "active_nonzero_power_coset_count"
                ]
            )
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_total_nonzero_power_coset_count": (
            int(first_superboundary_shape_ledger["total_nonzero_power_coset_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_power_image_size": (
            int(first_superboundary_shape_ledger["power_image_size"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_orbit_quotient_check": (
            bool(first_superboundary_shape_ledger["orbit_quotient_check"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_expected_packet_count": (
            int(first_superboundary_shape_ledger["packet_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_packet_count_check": (
            int(first_superboundary_shape_ledger["packet_count"])
            == first_superboundary_packet_count
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_expected_support_count": (
            int(first_superboundary_shape_ledger["weighted_support_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_support_count_check": (
            int(first_superboundary_shape_ledger["weighted_support_count"])
            == first_superboundary_support_count
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_packet_slope_histogram_check": (
            first_superboundary_shape_ledger["packet_slope_histogram"]
            == first_superboundary_packet_slope_histogram
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_support_slope_histogram_check": (
            first_superboundary_shape_ledger["support_slope_histogram"]
            == first_superboundary_slope_histogram
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_abstract_power_coset_slope_count": (
            int(first_superboundary_shape_ledger["abstract_power_coset_slope_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_power_coset_slope_count": (
            int(first_superboundary_shape_ledger["power_coset_slope_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_power_coset_slope_count_check": (
            len(first_superboundary_slope_histogram)
            == int(first_superboundary_shape_ledger["power_coset_slope_count"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_power_coset_slope_bound": (
            int(first_superboundary_shape_ledger["power_coset_slope_bound"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_first_superboundary_shape_power_coset_slope_bound_check": (
            len(first_superboundary_slope_histogram)
            <= int(first_superboundary_shape_ledger["power_coset_slope_bound"])
            if first_superboundary_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_parameter_count": (
            int(slack_two_shape_ledger["parameter_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_active_parameter_count": (
            int(slack_two_shape_ledger["active_parameter_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_active_zero_parameter_count": (
            int(slack_two_shape_ledger["active_zero_parameter_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_nonzero_square_coset_count": (
            int(slack_two_shape_ledger["nonzero_square_coset_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_active_nonzero_square_coset_count": (
            int(slack_two_shape_ledger["active_nonzero_square_coset_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_total_nonzero_square_coset_count": (
            int(slack_two_shape_ledger["total_nonzero_square_coset_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_nonzero_square_coset_coverage_density": (
            fraction_string(
                int(slack_two_shape_ledger["nonzero_square_coset_count"]),
                int(slack_two_shape_ledger["total_nonzero_square_coset_count"]),
            )
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_active_nonzero_square_coset_coverage_density": (
            fraction_string(
                int(slack_two_shape_ledger["active_nonzero_square_coset_count"]),
                int(slack_two_shape_ledger["total_nonzero_square_coset_count"]),
            )
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_saturates_nonzero_square_cosets": (
            int(slack_two_shape_ledger["nonzero_square_coset_count"])
            == int(slack_two_shape_ledger["total_nonzero_square_coset_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_active_saturates_nonzero_square_cosets": (
            int(slack_two_shape_ledger["active_nonzero_square_coset_count"])
            == int(slack_two_shape_ledger["total_nonzero_square_coset_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_square_image_size": (
            int(slack_two_shape_ledger["square_image_size"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_sixfold_quotient_check": (
            bool(slack_two_shape_ledger["sixfold_quotient_check"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_expected_packet_count": (
            int(slack_two_shape_ledger["packet_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_packet_count_check": (
            int(slack_two_shape_ledger["packet_count"])
            == first_superboundary_packet_count
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_expected_support_count": (
            int(slack_two_shape_ledger["weighted_support_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_support_count_check": (
            int(slack_two_shape_ledger["weighted_support_count"])
            == first_superboundary_support_count
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_packet_slope_histogram_check": (
            slack_two_shape_ledger["packet_slope_histogram"]
            == first_superboundary_packet_slope_histogram
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_support_slope_histogram_check": (
            slack_two_shape_ledger["support_slope_histogram"]
            == first_superboundary_slope_histogram
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_abstract_square_coset_slope_count": (
            int(slack_two_shape_ledger["abstract_square_coset_slope_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_square_coset_slope_count": (
            int(slack_two_shape_ledger["square_coset_slope_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_square_coset_slope_count_check": (
            len(first_superboundary_slope_histogram)
            == int(slack_two_shape_ledger["square_coset_slope_count"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_square_coset_slope_bound": (
            int(slack_two_shape_ledger["square_coset_slope_bound"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_square_coset_slope_bound_check": (
            len(first_superboundary_slope_histogram)
            <= int(slack_two_shape_ledger["square_coset_slope_bound"])
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_full_domain_alpha_square_count": (
            int(slack_two_full_domain_alpha_data["alpha_square_count"])
            if slack_two_full_domain_alpha_data is not None
            else None
        ),
        "canonical_slack_two_full_domain_alpha_nonsquare_count": (
            int(slack_two_full_domain_alpha_data["alpha_nonsquare_count"])
            if slack_two_full_domain_alpha_data is not None
            else None
        ),
        "canonical_slack_two_full_domain_alpha_zero_count": (
            int(slack_two_full_domain_alpha_data["alpha_zero_count"])
            if slack_two_full_domain_alpha_data is not None
            else None
        ),
        "canonical_slack_two_full_domain_alpha_character_sum": (
            int(slack_two_full_domain_alpha_data["alpha_character_sum"])
            if slack_two_full_domain_alpha_data is not None
            else None
        ),
        "canonical_slack_two_full_domain_slope_image": (
            str(slack_two_full_domain_alpha_data["slope_image"])
            if slack_two_full_domain_alpha_data is not None
            else None
        ),
        "canonical_slack_two_full_domain_slope_count": (
            int(slack_two_full_domain_alpha_data["slope_count"])
            if slack_two_full_domain_alpha_data is not None
            else None
        ),
        "canonical_slack_two_full_domain_slope_count_check": (
            len(first_superboundary_slope_histogram)
            == int(slack_two_full_domain_alpha_data["slope_count"])
            if (
                slack_two_full_domain_alpha_data is not None
                and int(slack_two_shape_ledger["active_parameter_count"])
                == int(slack_two_shape_ledger["parameter_count"])
            )
            else None
        ),
        "canonical_slack_two_second_shape_orbit_factor": (
            int(slack_two_second_shape_ledger["orbit_factor"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_parameter_count": (
            int(slack_two_second_shape_ledger["parameter_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_active_parameter_count": (
            int(slack_two_second_shape_ledger["active_parameter_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_zero_conic_parameter_count": (
            int(slack_two_second_shape_ledger["zero_parameter_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_active_zero_parameter_count": (
            int(slack_two_second_shape_ledger["active_zero_parameter_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_active_nonzero_orbit_check": (
            bool(
                slack_two_second_shape_ledger[
                    "active_nonzero_packet_orbit_check"
                ]
            )
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_active_nonzero_packet_orbit_count": (
            int(slack_two_second_shape_ledger["active_nonzero_packet_orbit_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_nonzero_square_coset_count": (
            int(slack_two_second_shape_ledger["nonzero_square_coset_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_active_nonzero_square_coset_count": (
            int(
                slack_two_second_shape_ledger[
                    "active_nonzero_square_coset_count"
                ]
            )
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_total_nonzero_square_coset_count": (
            int(slack_two_second_shape_ledger["total_nonzero_square_coset_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_saturates_nonzero_square_cosets": (
            int(slack_two_second_shape_ledger["nonzero_square_coset_count"])
            == int(slack_two_second_shape_ledger["total_nonzero_square_coset_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_active_saturates_nonzero_square_cosets": (
            int(
                slack_two_second_shape_ledger[
                    "active_nonzero_square_coset_count"
                ]
            )
            == int(slack_two_second_shape_ledger["total_nonzero_square_coset_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_square_image_size": (
            int(slack_two_second_shape_ledger["square_image_size"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_twentyfourfold_quotient_check": (
            bool(slack_two_second_shape_ledger["twentyfourfold_quotient_check"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_expected_packet_count": (
            int(slack_two_second_shape_ledger["packet_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_packet_count_check": (
            int(slack_two_second_shape_ledger["packet_count"])
            == slack_two_second_superboundary_packet_count
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_expected_support_count": (
            int(slack_two_second_shape_ledger["weighted_support_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_support_count_check": (
            int(slack_two_second_shape_ledger["weighted_support_count"])
            == slack_two_second_superboundary_support_count
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_packet_slope_histogram_check": (
            slack_two_second_shape_ledger["packet_slope_histogram"]
            == slack_two_second_superboundary_packet_slope_histogram
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_support_slope_histogram_check": (
            slack_two_second_shape_ledger["support_slope_histogram"]
            == slack_two_second_superboundary_slope_histogram
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_abstract_square_coset_slope_count": (
            int(slack_two_second_shape_ledger["abstract_square_coset_slope_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_square_coset_slope_count": (
            int(slack_two_second_shape_ledger["square_coset_slope_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_square_coset_slope_count_check": (
            len(slack_two_second_superboundary_slope_histogram)
            == int(slack_two_second_shape_ledger["square_coset_slope_count"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_square_coset_slope_bound": (
            int(slack_two_second_shape_ledger["square_coset_slope_bound"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_square_coset_slope_bound_check": (
            len(slack_two_second_superboundary_slope_histogram)
            <= int(slack_two_second_shape_ledger["square_coset_slope_bound"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_high_index_slope_bound": (
            int(slack_two_second_shape_ledger["high_index_slope_bound"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_high_index_nontrivial": (
            bool(slack_two_second_shape_ledger["high_index_slope_bound_nontrivial"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_high_index_bound_check": (
            len(slack_two_second_superboundary_slope_histogram)
            <= int(slack_two_second_shape_ledger["high_index_slope_bound"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_lift_limited_remaining_fibers": (
            slack_two_second_shape_ledger["lift_limited_remaining_fibers"]
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_lift_limited_parameter_bound": (
            int(slack_two_second_shape_ledger["lift_limited_parameter_bound"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_lift_limited_nonzero_orbit_bound": (
            int(
                slack_two_second_shape_ledger[
                    "lift_limited_nonzero_packet_orbit_bound"
                ]
            )
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_lift_limited_slope_bound": (
            int(slack_two_second_shape_ledger["lift_limited_slope_bound"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_lift_limited_nontrivial": (
            bool(
                slack_two_second_shape_ledger[
                    "lift_limited_slope_bound_nontrivial"
                ]
            )
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_lift_limited_bound_check": (
            len(slack_two_second_superboundary_slope_histogram)
            <= int(slack_two_second_shape_ledger["lift_limited_slope_bound"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_kernel_fiber_reduction_active": (
            bool(slack_two_second_shape_ledger["kernel_fiber_reduction_active"])
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_kernel_fiber_order": (
            int(slack_two_second_kernel_reduction["kernel_order"])
            if slack_two_second_kernel_reduction is not None
            else None
        ),
        "canonical_slack_two_second_kernel_fiber_parameter_count": (
            int(slack_two_second_kernel_reduction["parameter_count"])
            if slack_two_second_kernel_reduction is not None
            else None
        ),
        "canonical_slack_two_second_kernel_fiber_zero_parameter_count": (
            int(slack_two_second_kernel_reduction["zero_parameter_count"])
            if slack_two_second_kernel_reduction is not None
            else None
        ),
        "canonical_slack_two_second_kernel_fiber_nonzero_square_coset_count": (
            int(slack_two_second_kernel_reduction["nonzero_square_coset_count"])
            if slack_two_second_kernel_reduction is not None
            else None
        ),
        "canonical_slack_two_second_kernel_fiber_slope_count": (
            int(slack_two_second_kernel_reduction["slope_count"])
            if slack_two_second_kernel_reduction is not None
            else None
        ),
        "canonical_slack_two_second_kernel_fiber_reduction_check": (
            (
                int(slack_two_second_kernel_reduction["parameter_count"])
                == int(slack_two_second_shape_ledger["active_parameter_count"])
            )
            and (
                int(slack_two_second_kernel_reduction["zero_parameter_count"])
                == int(slack_two_second_shape_ledger["active_zero_parameter_count"])
            )
            and (
                int(
                    slack_two_second_kernel_reduction[
                        "nonzero_square_coset_count"
                    ]
                )
                == int(
                    slack_two_second_shape_ledger[
                        "active_nonzero_square_coset_count"
                    ]
                )
            )
            and (
                int(slack_two_second_kernel_reduction["slope_count"])
                == len(slack_two_second_superboundary_slope_histogram)
            )
            if (
                slack_two_second_kernel_reduction is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_r2_union_reduction_active": (
            slack_two_second_two_fiber_union_reduction is not None
        ),
        "canonical_slack_two_second_r2_union_window_count": (
            int(slack_two_second_two_fiber_union_reduction["window_count"])
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_parameter_count": (
            int(slack_two_second_two_fiber_union_reduction["parameter_count"])
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_zero_parameter_count": (
            int(
                slack_two_second_two_fiber_union_reduction[
                    "zero_parameter_count"
                ]
            )
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_nonzero_square_coset_count": (
            int(
                slack_two_second_two_fiber_union_reduction[
                    "nonzero_square_coset_count"
                ]
            )
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_saturates": (
            bool(
                slack_two_second_two_fiber_union_reduction[
                    "saturates_nonzero_square_cosets"
                ]
            )
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_exact_support_certificate": (
            slack_two_second_r2_union_exact_support_saturation
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_slope_count": (
            int(slack_two_second_two_fiber_union_reduction["slope_count"])
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_per_window_profiles": (
            list(
                slack_two_second_two_fiber_union_reduction[
                    "per_window_profiles"
                ]
            )
            if slack_two_second_two_fiber_union_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r2_union_reduction_check": (
            (
                int(
                    slack_two_second_two_fiber_union_reduction[
                        "parameter_count"
                    ]
                )
                == int(slack_two_second_shape_ledger["active_parameter_count"])
            )
            and (
                int(
                    slack_two_second_two_fiber_union_reduction[
                        "zero_parameter_count"
                    ]
                )
                == int(slack_two_second_shape_ledger["active_zero_parameter_count"])
            )
            and (
                int(
                    slack_two_second_two_fiber_union_reduction[
                        "nonzero_square_coset_count"
                    ]
                )
                == int(
                    slack_two_second_shape_ledger[
                        "active_nonzero_square_coset_count"
                    ]
                )
            )
            and (
                int(slack_two_second_two_fiber_union_reduction["slope_count"])
                == len(slack_two_second_superboundary_slope_histogram)
            )
            if (
                slack_two_second_two_fiber_union_reduction is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_r_window_reduction_active": (
            slack_two_second_r_window_reduction is not None
        ),
        "canonical_slack_two_second_r_window_effective_size": (
            int(slack_two_second_r_window_reduction["effective_window_size"])
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_window_count": (
            int(slack_two_second_r_window_reduction["window_count"])
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_parameter_count": (
            int(slack_two_second_r_window_reduction["parameter_count"])
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_zero_parameter_count": (
            int(slack_two_second_r_window_reduction["zero_parameter_count"])
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_nonzero_square_coset_count": (
            int(
                slack_two_second_r_window_reduction[
                    "nonzero_square_coset_count"
                ]
            )
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_touched_fiber_histogram": (
            {
                str(touched): count
                for touched, count in slack_two_second_r_window_reduction[
                    "touched_fiber_histogram"
                ]
            }
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_saturates": (
            bool(
                slack_two_second_r_window_reduction[
                    "saturates_nonzero_square_cosets"
                ]
            )
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_exact_support_certificate": (
            slack_two_second_r_window_exact_support_saturation
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_slope_count": (
            int(slack_two_second_r_window_reduction["slope_count"])
            if slack_two_second_r_window_reduction is not None
            else None
        ),
        "canonical_slack_two_second_r_window_reduction_check": (
            (
                int(slack_two_second_r_window_reduction["parameter_count"])
                == int(slack_two_second_shape_ledger["active_parameter_count"])
            )
            and (
                int(slack_two_second_r_window_reduction["zero_parameter_count"])
                == int(slack_two_second_shape_ledger["active_zero_parameter_count"])
            )
            and (
                int(
                    slack_two_second_r_window_reduction[
                        "nonzero_square_coset_count"
                    ]
                )
                == int(
                    slack_two_second_shape_ledger[
                        "active_nonzero_square_coset_count"
                    ]
                )
            )
            and (
                int(slack_two_second_r_window_reduction["slope_count"])
                == len(slack_two_second_superboundary_slope_histogram)
            )
            if (
                slack_two_second_r_window_reduction is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_window_size": (
            int(slack_two_second_r_window_kummer_saturation["window_size"])
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_character_order": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "kernel_character_order"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_square_coset_index": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "square_coset_index"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_denominator": (
            int(slack_two_second_r_window_kummer_saturation["denominator"])
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_principal_weight": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "principal_weight"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_coefficient_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "coefficient_abs_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_ambient_kernel_count": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "ambient_restriction_kernel_count"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_window_l1_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "window_one_dimensional_l1_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_coefficient_l1_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "coefficient_l1_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_jacobi_l1_bound": (
            int(slack_two_second_r_window_kummer_saturation["jacobi_l1_bound"])
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_conic_l1_bound": (
            int(slack_two_second_r_window_kummer_saturation["conic_l1_bound"])
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_quadratic_one_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "quadratic_one_coordinate_l1_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_one_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "one_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_two_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "two_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_three_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "three_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_kummer_l1_bound": (
            int(slack_two_second_r_window_kummer_saturation["kummer_l1_bound"])
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_weighted_error_l1_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "weighted_error_l1_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_prime_threshold": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "uniform_prime_threshold"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_threshold_applies": (
            bool(
                slack_two_second_r_window_kummer_saturation[
                    "uniform_threshold_applies"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_lower_numerator": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "lower_numerator"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_lower_bound": (
            int(
                slack_two_second_r_window_kummer_saturation[
                    "admissible_per_coset_lower_bound"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_certificate": (
            bool(
                slack_two_second_r_window_kummer_saturation[
                    "saturation_certificate"
                ]
            )
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_kummer_exact_support_certificate": (
            slack_two_second_r_window_kummer_exact_support_saturation
            if slack_two_second_r_window_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_effective_size": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "effective_window_size"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_window_count": (
            int(slack_two_second_r_window_union_kummer_saturation["window_count"])
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_label_triples": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "label_triple_count"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_character_order": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "kernel_character_order"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_square_coset_index": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "square_coset_index"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_denominator": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "denominator"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_principal_weight": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "principal_weight"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_coefficient_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "coefficient_abs_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_coefficient_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_coefficient_abs_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_ambient_kernel_count": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "ambient_restriction_kernel_count"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_quotient_l1_exact": (
            bool(slack_two_second_r_window_union_kummer_saturation[
                "quotient_l1_exact"
            ])
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_zero_subset_histogram": (
            dict(
                slack_two_second_r_window_union_kummer_saturation[
                    "quotient_l1_zero_subset_histogram"
                ]
            )
            if (
                slack_two_second_r_window_union_kummer_saturation is not None
                and slack_two_second_r_window_union_kummer_saturation[
                    "quotient_l1_zero_subset_histogram"
                ]
                is not None
            )
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_coefficient_histogram": (
            dict(
                slack_two_second_r_window_union_kummer_saturation[
                    "quotient_l1_coefficient_histogram"
                ]
            )
            if (
                slack_two_second_r_window_union_kummer_saturation is not None
                and slack_two_second_r_window_union_kummer_saturation[
                    "quotient_l1_coefficient_histogram"
                ]
                is not None
            )
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_quotient_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "quotient_coefficient_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_quotient_one_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "quotient_one_coordinate_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_quotient_two_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "quotient_two_coordinate_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_quotient_three_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "quotient_three_coordinate_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_coefficient_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "coefficient_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_jacobi_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "jacobi_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_conic_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "conic_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_quadratic_one_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "quadratic_one_coordinate_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_one_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "one_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_two_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "two_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_three_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "three_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_kummer_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_weighted_error_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "weighted_error_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_coefficient_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_conic_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_conic_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_r_window_union_kummer_crude_"
            "quadratic_one_coordinate_l1_bound"
        ): (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_quadratic_one_coordinate_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_one_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_one_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_two_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_two_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_three_coordinate_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_three_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_weighted_error_l1_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_weighted_error_l1_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_prime_threshold": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "uniform_prime_threshold"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_threshold_applies": (
            bool(
                slack_two_second_r_window_union_kummer_saturation[
                    "uniform_threshold_applies"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_lower_numerator": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "lower_numerator"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_crude_lower_numerator": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "crude_lower_numerator"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_lower_bound": (
            int(
                slack_two_second_r_window_union_kummer_saturation[
                    "admissible_per_coset_lower_bound"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_certificate": (
            bool(
                slack_two_second_r_window_union_kummer_saturation[
                    "saturation_certificate"
                ]
            )
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_r_window_union_kummer_exact_support_certificate": (
            slack_two_second_r_window_union_kummer_exact_support_saturation
            if slack_two_second_r_window_union_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_character_order": (
            int(slack_two_second_kummer_saturation["character_order"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_square_kernel_index": (
            int(slack_two_second_kummer_saturation["square_kernel_index"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_square_coset_index": (
            int(slack_two_second_kummer_saturation["square_coset_index"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_denominator": (
            int(slack_two_second_kummer_saturation["denominator"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_nonprincipal_tuple_count": (
            int(slack_two_second_kummer_saturation["nonprincipal_tuple_count"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_coefficient_l1_bound": (
            int(slack_two_second_kummer_saturation["coefficient_l1_bound"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_jacobi_l1_bound": (
            int(slack_two_second_kummer_saturation["jacobi_l1_bound"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_conic_l1_bound": (
            int(slack_two_second_kummer_saturation["conic_l1_bound"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_quadratic_one_coordinate_l1_bound": (
            int(
                slack_two_second_kummer_saturation[
                    "quadratic_one_coordinate_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_one_coordinate_l1_bound": (
            int(
                slack_two_second_kummer_saturation[
                    "one_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_two_coordinate_l1_bound": (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_two_coordinate_"
            "infinity_unramified_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_infinity_unramified_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_two_coordinate_ramified_l1_bound": (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_ramified_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_two_coordinate_"
            "projective_reciprocal_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_reciprocal_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_two_coordinate_"
            "ramified_nonreciprocal_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_ramified_nonreciprocal_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_three_coordinate_l1_bound": (
            int(
                slack_two_second_kummer_saturation[
                    "three_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_kummer_l1_bound": (
            int(slack_two_second_kummer_saturation["kummer_l1_bound"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_weighted_error_l1_bound": (
            int(slack_two_second_kummer_saturation["weighted_error_l1_bound"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_equal_line_l1_bound": (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_equal_line_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "coordinate_diagonal_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_coordinate_diagonal_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "coordinate_diagonal_non_equal_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_coordinate_diagonal_non_equal_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_equal_pair_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_equal_pair_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_equal_pair_non_coordinate_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_equal_pair_non_coordinate_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_asymmetric_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_asymmetric_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_asymmetric_orbit_count"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_asymmetric_orbit_count"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_asymmetric_line_conic_resonant_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "resonant_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_asymmetric_line_conic_nonresonant_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "nonresonant_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_asymmetric_line_conic_resonant_orbit_count"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "resonant_orbit_count"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_asymmetric_line_conic_nonresonant_orbit_count"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "nonresonant_orbit_count"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "coordinate_diagonal_alpha_square_trivial_count"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_coordinate_diagonal_"
                    "alpha_square_trivial_count"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "coordinate_diagonal_2f1_cancellation_count"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_coordinate_diagonal_"
                    "2f1_cancellation_count"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_equal_line_leading_l1_drop": (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_equal_line_leading_l1_drop"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "coordinate_diagonal_leading_l1_drop"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_coordinate_diagonal_leading_l1_drop"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "projective_equal_pair_leading_l1_drop"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_equal_pair_leading_l1_drop"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_"
            "line_conic_resonant_leading_l1_drop"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "two_coordinate_projective_asymmetric_line_conic_"
                    "resonant_leading_l1_drop"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_equal_line_"
            "conditional_weighted_error_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "equal_line_conditional_weighted_error_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_coordinate_diagonal_"
            "conditional_weighted_error_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "coordinate_diagonal_conditional_weighted_error_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "conditional_weighted_error_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_conditional_weighted_error_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "nonresonant_conditional_weighted_error_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_nonresonant_conditional_"
                    "weighted_error_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "all_asymmetric_conditional_weighted_error_l1_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_all_asymmetric_conditional_"
                    "weighted_error_l1_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_sqrt_error_bound": (
            int(slack_two_second_kummer_saturation["sqrt_error_bound"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_equal_line_"
            "conditional_sqrt_error_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "equal_line_conditional_sqrt_error_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_coordinate_diagonal_"
            "conditional_sqrt_error_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "coordinate_diagonal_conditional_sqrt_error_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "conditional_sqrt_error_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_conditional_sqrt_error_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "nonresonant_conditional_sqrt_error_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_nonresonant_conditional_"
                    "sqrt_error_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "all_asymmetric_conditional_sqrt_error_bound"
        ): (
            int(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_all_asymmetric_conditional_"
                    "sqrt_error_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_coordinate_diagonal_"
            "conditional_saturation_certificate"
        ): (
            bool(
                slack_two_second_kummer_saturation[
                    "coordinate_diagonal_conditional_saturation_certificate"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "conditional_saturation_certificate"
        ): (
            bool(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_conditional_saturation_certificate"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "nonresonant_conditional_saturation_certificate"
        ): (
            bool(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_nonresonant_conditional_"
                    "saturation_certificate"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        (
            "canonical_slack_two_second_kummer_projective_equal_pair_"
            "all_asymmetric_conditional_saturation_certificate"
        ): (
            bool(
                slack_two_second_kummer_saturation[
                    "projective_equal_pair_all_asymmetric_conditional_"
                    "saturation_certificate"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_divisor_power_failure_count": (
            int(
                slack_two_second_kummer_saturation[
                    "divisor_power_failure_count"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_divisor_nontriviality_check": (
            bool(
                slack_two_second_kummer_saturation[
                    "divisor_nontriviality_check"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_radical_component_degrees": (
            list(
                slack_two_second_kummer_saturation[
                    "radical_component_degrees"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_radical_total_degree": (
            int(slack_two_second_kummer_saturation["radical_total_degree"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_deligne_constant_formula": (
            str(slack_two_second_kummer_saturation["deligne_constant_formula"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_deligne_constant": (
            int(slack_two_second_kummer_saturation["deligne_constant"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_deligne_constant_check": (
            bool(slack_two_second_kummer_saturation["deligne_constant_check"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_uniform_prime_threshold": (
            int(slack_two_second_kummer_saturation["uniform_prime_threshold"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_uniform_threshold_applies": (
            bool(slack_two_second_kummer_saturation["uniform_threshold_applies"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_nonprincipal_constant": (
            int(slack_two_second_kummer_saturation["nonprincipal_constant"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_principal_chi_minus_three": (
            int(slack_two_second_kummer_saturation["principal_chi_minus_three"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_principal_exact_count": (
            int(slack_two_second_kummer_saturation["principal_exact_count"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_principal_lower_bound": (
            int(slack_two_second_kummer_saturation["principal_lower_bound"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_degeneracy_line_count": (
            int(slack_two_second_kummer_saturation["degeneracy_line_count"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_degeneracy_line_union_count": (
            int(
                slack_two_second_kummer_saturation[
                    "degeneracy_line_union_count"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_lower_numerator": (
            int(slack_two_second_kummer_saturation["lower_numerator"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_admissible_per_coset_lower_bound": (
            int(
                slack_two_second_kummer_saturation[
                    "admissible_per_coset_lower_bound"
                ]
            )
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_saturation_certificate": (
            bool(slack_two_second_kummer_saturation["saturation_certificate"])
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_exact_support_saturation_certificate": (
            slack_two_second_kummer_exact_support_saturation
            if slack_two_second_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_kummer_saturation_certificate_check": (
            (
                not bool(
                    slack_two_second_kummer_saturation[
                        "saturation_certificate"
                    ]
                )
            )
            or (
                int(slack_two_second_shape_ledger["nonzero_square_coset_count"])
                == int(
                    slack_two_second_shape_ledger[
                        "total_nonzero_square_coset_count"
                    ]
                )
            )
            if (
                slack_two_second_kummer_saturation is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_kummer_exact_support_certificate_check": (
            (
                not slack_two_second_kummer_exact_support_saturation
            )
            or (
                int(
                    slack_two_second_shape_ledger[
                        "active_nonzero_square_coset_count"
                    ]
                )
                == int(
                    slack_two_second_shape_ledger[
                        "total_nonzero_square_coset_count"
                    ]
                )
            )
            if (
                slack_two_second_kummer_saturation is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_character_order": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "kernel_character_order"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_square_coset_index": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "square_coset_index"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_denominator": (
            int(slack_two_second_two_fiber_kummer_saturation["denominator"])
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_principal_weight": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "principal_weight"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_coefficient_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "coefficient_abs_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_ambient_kernel_count": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "ambient_restriction_kernel_count"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_window_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "window_one_dimensional_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_coefficient_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "coefficient_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_jacobi_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "jacobi_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_conic_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "conic_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_quadratic_one_coordinate_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "quadratic_one_coordinate_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_one_coordinate_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "one_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_two_coordinate_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "two_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_three_coordinate_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "three_coordinate_kummer_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_kummer_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "kummer_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_weighted_error_l1_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "weighted_error_l1_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_uniform_prime_threshold": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "uniform_prime_threshold"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_threshold_applies": (
            bool(
                slack_two_second_two_fiber_kummer_saturation[
                    "uniform_threshold_applies"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_lower_numerator": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "lower_numerator"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_lower_bound": (
            int(
                slack_two_second_two_fiber_kummer_saturation[
                    "admissible_per_coset_lower_bound"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_saturation_certificate": (
            bool(
                slack_two_second_two_fiber_kummer_saturation[
                    "saturation_certificate"
                ]
            )
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_exact_support_certificate": (
            slack_two_second_two_fiber_exact_support_saturation
            if slack_two_second_two_fiber_kummer_saturation is not None
            else None
        ),
        "canonical_slack_two_second_two_fiber_kummer_certificate_check": (
            (
                not bool(
                    slack_two_second_two_fiber_kummer_saturation[
                        "saturation_certificate"
                    ]
                )
            )
            or (
                int(slack_two_second_shape_ledger["nonzero_square_coset_count"])
                == int(
                    slack_two_second_shape_ledger[
                        "total_nonzero_square_coset_count"
                    ]
                )
            )
            if (
                slack_two_second_two_fiber_kummer_saturation is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_two_fiber_exact_support_check": (
            (
                not slack_two_second_two_fiber_exact_support_saturation
            )
            or (
                int(
                    slack_two_second_shape_ledger[
                        "active_nonzero_square_coset_count"
                    ]
                )
                == int(
                    slack_two_second_shape_ledger[
                        "total_nonzero_square_coset_count"
                    ]
                )
            )
            if (
                slack_two_second_two_fiber_kummer_saturation is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_index_window_label": (
            slack_two_second_index_window_label
        ),
        "canonical_slack_two_second_intermediate_index_window_candidate": (
            slack_two_second_index_window_label == "intermediate_index_window"
            if slack_two_second_index_window_label is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_A_square_count": (
            int(slack_two_depth_two_full_domain_A_data["A_square_count"])
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_A_nonsquare_count": (
            int(slack_two_depth_two_full_domain_A_data["A_nonsquare_count"])
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_A_zero_count": (
            int(slack_two_depth_two_full_domain_A_data["A_zero_count"])
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_A_character_sum_all_plane": (
            int(
                slack_two_depth_two_full_domain_A_data[
                    "A_character_sum_all_plane"
                ]
            )
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_large_prime_certificate": (
            bool(
                slack_two_depth_two_full_domain_A_data[
                    "large_prime_certificate"
                ]
            )
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_finite_low_prime_certificate": (
            bool(
                slack_two_depth_two_full_domain_A_data[
                    "finite_low_prime_certificate"
                ]
            )
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_saturates_nonzero_slopes": (
            bool(
                slack_two_depth_two_full_domain_A_data[
                    "saturates_nonzero_square_cosets"
                ]
            )
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_nonzero_slope_image": (
            str(slack_two_depth_two_full_domain_A_data["nonzero_slope_image"])
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_nonzero_slope_count": (
            int(slack_two_depth_two_full_domain_A_data["nonzero_slope_count"])
            if slack_two_depth_two_full_domain_A_data is not None
            else None
        ),
        "canonical_slack_two_second_full_domain_coset_count_check": (
            int(
                slack_two_depth_two_full_domain_A_data[
                    "nonzero_square_coset_count"
                ]
            )
            == int(slack_two_second_shape_ledger["nonzero_square_coset_count"])
            if (
                slack_two_depth_two_full_domain_A_data is not None
                and slack_two_second_shape_ledger is not None
            )
            else None
        ),
        "canonical_slack_two_second_shape_expected_packet_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_two_second_shape_ledger[
                        "packet_slope_histogram"
                    ].items()
                )
            }
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_second_shape_expected_support_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_two_second_shape_ledger[
                        "support_slope_histogram"
                    ].items()
                )
            }
            if slack_two_second_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_parameter_count": (
            int(slack_three_shape_ledger["parameter_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_parameter_count": (
            int(slack_three_shape_ledger["active_parameter_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_zero_parameter_count": (
            int(slack_three_shape_ledger["active_zero_parameter_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_beta_count": (
            int(slack_three_shape_ledger["beta_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_beta_count": (
            int(slack_three_shape_ledger["active_beta_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_beta_parameter_count_check": (
            bool(slack_three_shape_ledger["beta_parameter_count_check"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_candidate_beta_count": (
            int(slack_three_shape_ledger["split_cubic_candidate_beta_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_beta_count": (
            int(slack_three_shape_ledger["split_cubic_beta_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_zero_beta_count": (
            int(slack_three_shape_ledger["split_cubic_zero_beta_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_parameter_count": (
            int(slack_three_shape_ledger["split_cubic_parameter_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_root_count_histogram": (
            slack_three_shape_ledger["split_cubic_root_count_histogram"]
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_nonzero_cube_coset_count": (
            int(
                slack_three_shape_ledger[
                    "split_cubic_nonzero_cube_coset_count"
                ]
            )
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_nonzero_cube_coset_beta_counts": (
            list(
                slack_three_shape_ledger[
                    "split_cubic_nonzero_cube_coset_beta_counts"
                ]
            )
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_parameter_count_check": (
            bool(slack_three_shape_ledger["split_cubic_parameter_count_check"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_beta_count_check": (
            bool(slack_three_shape_ledger["split_cubic_beta_count_check"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_zero_beta_count_check": (
            bool(slack_three_shape_ledger["split_cubic_zero_beta_count_check"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_cube_coset_count_check": (
            bool(
                slack_three_shape_ledger[
                    "split_cubic_cube_coset_count_check"
                ]
            )
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_split_cubic_cube_coset_beta_counts_check": (
            bool(
                slack_three_shape_ledger[
                    "split_cubic_cube_coset_beta_counts_check"
                ]
            )
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_beta_parameter_count_check": (
            bool(slack_three_shape_ledger["active_beta_parameter_count_check"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_nonzero_cube_coset_count": (
            int(slack_three_shape_ledger["nonzero_cube_coset_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_nonzero_cube_coset_count": (
            int(slack_three_shape_ledger["active_nonzero_cube_coset_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_nonzero_cube_coset_beta_counts": (
            list(slack_three_shape_ledger["nonzero_cube_coset_beta_counts"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_nonzero_cube_coset_beta_counts": (
            list(
                slack_three_shape_ledger[
                    "active_nonzero_cube_coset_beta_counts"
                ]
            )
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_total_nonzero_cube_coset_count": (
            int(slack_three_shape_ledger["total_nonzero_cube_coset_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_nonzero_cube_coset_coverage_density": (
            fraction_string(
                int(slack_three_shape_ledger["nonzero_cube_coset_count"]),
                int(slack_three_shape_ledger["total_nonzero_cube_coset_count"]),
            )
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_nonzero_cube_coset_coverage_density": (
            fraction_string(
                int(slack_three_shape_ledger["active_nonzero_cube_coset_count"]),
                int(slack_three_shape_ledger["total_nonzero_cube_coset_count"]),
            )
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_saturates_nonzero_cube_cosets": (
            int(slack_three_shape_ledger["nonzero_cube_coset_count"])
            == int(slack_three_shape_ledger["total_nonzero_cube_coset_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_active_saturates_nonzero_cube_cosets": (
            int(slack_three_shape_ledger["active_nonzero_cube_coset_count"])
            == int(slack_three_shape_ledger["total_nonzero_cube_coset_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_cube_image_size": (
            int(slack_three_shape_ledger["cube_image_size"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_twentyfourfold_quotient_check": (
            bool(slack_three_shape_ledger["twentyfourfold_quotient_check"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_expected_packet_count": (
            int(slack_three_shape_ledger["packet_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_packet_count_check": (
            int(slack_three_shape_ledger["packet_count"])
            == first_superboundary_packet_count
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_expected_support_count": (
            int(slack_three_shape_ledger["weighted_support_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_support_count_check": (
            int(slack_three_shape_ledger["weighted_support_count"])
            == first_superboundary_support_count
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_packet_slope_histogram_check": (
            slack_three_shape_ledger["packet_slope_histogram"]
            == first_superboundary_packet_slope_histogram
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_support_slope_histogram_check": (
            slack_three_shape_ledger["support_slope_histogram"]
            == first_superboundary_slope_histogram
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_abstract_cube_coset_slope_count": (
            int(slack_three_shape_ledger["abstract_cube_coset_slope_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_cube_coset_slope_count": (
            int(slack_three_shape_ledger["cube_coset_slope_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_cube_coset_slope_count_check": (
            len(first_superboundary_slope_histogram)
            == int(slack_three_shape_ledger["cube_coset_slope_count"])
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_full_domain_ordered_shape_count": (
            int(slack_three_full_domain_beta_data["ordered_shape_count"])
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_ordered_shape_count_check": (
            int(slack_three_shape_ledger["parameter_count"])
            == int(slack_three_full_domain_beta_data["ordered_shape_count"])
            if (
                slack_three_shape_ledger is not None
                and slack_three_full_domain_beta_data is not None
            )
            else None
        ),
        "canonical_slack_three_full_domain_beta_count": (
            int(slack_three_full_domain_beta_data["beta_count"])
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_beta_count_check": (
            int(slack_three_shape_ledger["beta_count"])
            == int(slack_three_full_domain_beta_data["beta_count"])
            if (
                slack_three_shape_ledger is not None
                and slack_three_full_domain_beta_data is not None
            )
            else None
        ),
        "canonical_slack_three_full_domain_zero_beta_count": (
            int(slack_three_full_domain_beta_data["zero_beta_count"])
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_nonzero_beta_count": (
            int(slack_three_full_domain_beta_data["nonzero_beta_count"])
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_cube_surjective": (
            bool(slack_three_full_domain_beta_data["cube_surjective"])
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_cube_coset_beta_lower_bound": (
            int(slack_three_full_domain_beta_data["cube_coset_beta_lower_bound"])
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_cube_coset_saturation_certificate": (
            bool(
                slack_three_full_domain_beta_data[
                    "cube_coset_saturation_certificate"
                ]
            )
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_exact_cube_coset_beta_counts": (
            list(slack_three_shape_ledger["nonzero_cube_coset_beta_counts"])
            if (
                slack_three_shape_ledger is not None
                and slack_three_full_domain_beta_data is not None
            )
            else None
        ),
        "canonical_slack_three_full_domain_exact_cube_coset_saturates": (
            int(slack_three_shape_ledger["nonzero_cube_coset_count"])
            == int(slack_three_shape_ledger["total_nonzero_cube_coset_count"])
            if (
                slack_three_shape_ledger is not None
                and slack_three_full_domain_beta_data is not None
            )
            else None
        ),
        "canonical_slack_three_full_domain_slope_image": (
            str(slack_three_full_domain_beta_data["slope_image"])
            if slack_three_full_domain_beta_data is not None
            else None
        ),
        "canonical_slack_three_full_domain_slope_count": (
            int(slack_three_full_domain_beta_data["slope_count"])
            if (
                slack_three_full_domain_beta_data is not None
                and slack_three_full_domain_beta_data["slope_count"] is not None
            )
            else None
        ),
        "canonical_slack_three_full_domain_slope_count_check": (
            len(first_superboundary_slope_histogram)
            == int(slack_three_full_domain_beta_data["slope_count"])
            if (
                slack_three_shape_ledger is not None
                and slack_three_full_domain_beta_data is not None
                and slack_three_full_domain_beta_data["slope_count"] is not None
                and int(slack_three_shape_ledger["active_parameter_count"])
                == int(slack_three_shape_ledger["parameter_count"])
            )
            else None
        ),
        "canonical_slack_two_cyclotomic_shape_count_bound": (
            slack_two_cyclotomic_bound
            if slack_two_cyclotomic_bound is not None
            else None
        ),
        "canonical_slack_two_cyclotomic_character_order": (
            (p - 1) // n if slack_two_cyclotomic_bound is not None else None
        ),
        "canonical_slack_two_cyclotomic_shape_count_bound_check": (
            int(slack_two_shape_ledger["parameter_count"])
            <= slack_two_cyclotomic_bound
            if (
                slack_two_shape_ledger is not None
                and slack_two_cyclotomic_bound is not None
            )
            else None
        ),
        "canonical_slack_two_cyclotomic_slope_bound": (
            slack_two_cyclotomic_slope_bound
            if slack_two_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_two_cyclotomic_slope_bound_density": (
            fraction_string(slack_two_cyclotomic_slope_bound, p)
            if slack_two_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_two_cyclotomic_slope_bound_nontrivial": (
            slack_two_cyclotomic_slope_bound < p
            if slack_two_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_two_cyclotomic_slope_bound_check": (
            len(first_superboundary_slope_histogram)
            <= slack_two_cyclotomic_slope_bound
            if slack_two_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_three_cyclotomic_shape_count_bound": (
            slack_three_cyclotomic_bound
            if slack_three_cyclotomic_bound is not None
            else None
        ),
        "canonical_slack_three_cyclotomic_character_order": (
            (p - 1) // n if slack_three_cyclotomic_bound is not None else None
        ),
        "canonical_slack_three_cyclotomic_conic_weil_constant": (
            6 if slack_three_cyclotomic_bound is not None else None
        ),
        "canonical_slack_three_cyclotomic_shape_count_bound_check": (
            int(slack_three_shape_ledger["parameter_count"])
            <= slack_three_cyclotomic_bound
            if (
                slack_three_shape_ledger is not None
                and slack_three_cyclotomic_bound is not None
            )
            else None
        ),
        "canonical_slack_three_cyclotomic_slope_bound": (
            slack_three_cyclotomic_slope_bound
            if slack_three_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_three_cyclotomic_slope_bound_density": (
            fraction_string(slack_three_cyclotomic_slope_bound, p)
            if slack_three_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_three_cyclotomic_slope_bound_nontrivial": (
            slack_three_cyclotomic_slope_bound < p
            if slack_three_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_three_cyclotomic_slope_bound_check": (
            len(first_superboundary_slope_histogram)
            <= slack_three_cyclotomic_slope_bound
            if slack_three_cyclotomic_slope_bound is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_character_order": (
            int(slack_three_cube_coset_coverage["character_order"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_cube_kernel_index": (
            int(slack_three_cube_coset_coverage["cube_kernel_index"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_cube_coset_index": (
            int(slack_three_cube_coset_coverage["cube_coset_index"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_denominator": (
            int(slack_three_cube_coset_coverage["denominator"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_uniform_prime_threshold": (
            int(slack_three_cube_coset_coverage["uniform_prime_threshold"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_uniform_threshold_applies": (
            bool(slack_three_cube_coset_coverage["uniform_threshold_applies"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_uniform_threshold_check": (
            bool(slack_three_cube_coset_coverage["saturation_certificate"])
            if (
                slack_three_cube_coset_coverage is not None
                and bool(
                    slack_three_cube_coset_coverage[
                        "uniform_threshold_applies"
                    ]
                )
            )
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_principal_lower": (
            int(slack_three_cube_coset_coverage["principal_lower"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_weil_constant": (
            int(slack_three_cube_coset_coverage["conic_weil_constant"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_degeneracy_cost": (
            int(slack_three_cube_coset_coverage["degeneracy_cost"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_lower_numerator": (
            int(slack_three_cube_coset_coverage["lower_numerator"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_parameter_lower_bound": (
            slack_three_cube_coset_parameter_lower_bound
        ),
        "canonical_slack_three_cube_coset_coverage_certificate": (
            bool(slack_three_cube_coset_coverage["saturation_certificate"])
            if slack_three_cube_coset_coverage is not None
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_certificate_check": (
            int(slack_three_shape_ledger["nonzero_cube_coset_count"])
            == int(slack_three_shape_ledger["total_nonzero_cube_coset_count"])
            if (
                slack_three_shape_ledger is not None
                and slack_three_cube_coset_coverage is not None
                and bool(
                    slack_three_cube_coset_coverage[
                        "saturation_certificate"
                    ]
                )
            )
            else None
        ),
        "canonical_slack_three_cube_coset_coverage_exact_min_parameter_count": (
            slack_three_exact_min_cube_coset_parameter_count
        ),
        "canonical_slack_three_cube_coset_coverage_lower_bound_check": (
            slack_three_exact_min_cube_coset_parameter_count
            >= slack_three_cube_coset_parameter_lower_bound
            if (
                slack_three_exact_min_cube_coset_parameter_count is not None
                and slack_three_cube_coset_parameter_lower_bound is not None
            )
            else None
        ),
        "canonical_slack_two_shape_expected_packet_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_two_shape_ledger["packet_slope_histogram"].items()
                )
            }
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_two_shape_expected_support_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_two_shape_ledger["support_slope_histogram"].items()
                )
            }
            if slack_two_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_expected_packet_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_three_shape_ledger["packet_slope_histogram"].items()
                )
            }
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_slack_three_shape_expected_support_slope_histogram": (
            {
                str(slope): count
                for slope, count in sorted(
                    slack_three_shape_ledger["support_slope_histogram"].items()
                )
            }
            if slack_three_shape_ledger is not None
            else None
        ),
        "canonical_subboundary_residual_floor": (
            subboundary_floor if canonical_line and slack < fiber_size else None
        ),
        "canonical_subboundary_residual_floor_check": (
            canonical_subboundary_floor_violations == 0
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_subboundary_residual_floor_violation_count": (
            canonical_subboundary_floor_violations
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_boundary_touched_fiber_count": (
            expected_boundary_touched_fibers
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_boundary_touched_fiber_check": (
            canonical_boundary_touched_fiber_mismatches == 0
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_boundary_touched_fiber_mismatch_count": (
            canonical_boundary_touched_fiber_mismatches
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_slope_check": (
            canonical_residual_slope_mismatches == 0
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_residual_slope_mismatch_count": (
            canonical_residual_slope_mismatches
            if canonical_line and slack < fiber_size
            else None
        ),
        "canonical_boundary_slope_decomposition_check": (
            canonical_boundary_slope_mismatches == 0
            if canonical_line and slack == fiber_size
            else None
        ),
        "canonical_boundary_slope_mismatch_count": (
            canonical_boundary_slope_mismatches
            if canonical_line and slack == fiber_size
            else None
        ),
        "low_deficit_whole_fiber_invisibility": low_deficit_mismatches == 0,
        "low_deficit_checked_degrees": list(range(1, low_deficit_limit + 1)),
        "low_deficit_mismatch_count": low_deficit_mismatches,
        "residual_size_histogram": {
            str(size): count for size, count in sorted(residual_size_histogram.items())
        },
        "contained_support_count": contained_count,
        "no_slope_support_count": no_slope_count,
        "incidence_count": incidence_count,
        "bad_slope_count": len(bad_slopes),
        "bad_slopes": sorted(bad_slopes),
        "bad_slope_density": fraction_string(len(bad_slopes), p),
        "top_histograms": retained_histograms(ordered_records, top_histograms),
    }


def print_text(result: Dict[str, object]) -> None:
    params = result["parameters"]
    assert isinstance(params, dict)
    print("M1 support-coefficient occupancy scan")
    print("proof_status: AUDIT / EXPERIMENTAL")
    print(
        "p={p} n={n} k={k} slack={t} support={s} quotient_order={N}".format(
            p=params["prime"],
            n=params["domain_order"],
            k=params["k"],
            t=params["slack"],
            s=params["support_size"],
            N=params["quotient_order"],
        )
    )
    print(
        "supports={supports} histograms={histograms} incidences={inc} "
        "bad_slopes={slopes} density={density}".format(
            supports=result["support_count"],
            histograms=result["histogram_count"],
            inc=result["incidence_count"],
            slopes=result["bad_slope_count"],
            density=result["bad_slope_density"],
        )
    )
    print(
        "histogram_counts_match_binomial={binom} "
        "histogram_counts_match_formula={formula} "
        "support_outcome_partition={partition}".format(
            binom=result["histogram_counts_match_binomial"],
            formula=result["histogram_counts_match_formula"],
            partition=result["support_outcome_partition"],
        )
    )
    print(
        "low_deficit_whole_fiber_invisibility={ok} degrees={degrees}".format(
            ok=result["low_deficit_whole_fiber_invisibility"],
            degrees=result["low_deficit_checked_degrees"],
        )
    )
    if result["canonical_line"]:
        print(
            "canonical_symmetric_formula_check={formula} "
            "zero_prefix_supports={zero} "
            "residual_zero_prefix_match={residual} "
            "low_residual_exclusion={low} "
            "boundary_coset_check={coset} "
            "boundary_count_check={count} "
            "boundary_slope_count_check={slope_count} "
            "small_residual_regime={small} "
            "small_residual_depth_gate={depth_gate} "
            "active_superboundary_depth={active_depth} "
            "positive_dither_clearance={positive_clearance} "
            "positive_dither_finite_prefix={positive_prefix} "
            "residual_packet_lift_check={packet} "
            "terminal_pure_zero_check={terminal} "
            "first_nonzero_frontier_check={frontier} "
            "first_superboundary_lift_gate={gate} "
            "first_superboundary_lift_gate_check={gate_check} "
            "first_superboundary_zero_check={first} "
            "first_superboundary_shape_check={first_shape} "
            "first_superboundary_shape_bound={first_shape_bound} "
            "second_superboundary_shape_check={second_shape} "
            "second_superboundary_transition={second_transition} "
            "slack_two_shape_check={shape} "
            "slack_two_second_shape_check={shape2} "
            "slack_three_shape_check={shape3} "
            "subboundary_floor_check={floor} "
            "residual_slope_check={slope} "
            "boundary_slope_check={boundary}".format(
                formula=result["canonical_symmetric_formula_check"],
                zero=result["canonical_zero_prefix_support_count"],
                residual=result["canonical_residual_zero_prefix_match"],
                low=result["canonical_low_residual_exclusion_check"],
                coset=result["canonical_boundary_residual_coset_check"],
                count=result["canonical_boundary_residual_count_check"],
                slope_count=result["canonical_boundary_slope_count_check"],
                small=result["canonical_small_residual_regime"],
                depth_gate=result["canonical_small_residual_depth_gate_check"],
                active_depth=result["canonical_superboundary_active_depth"],
                positive_clearance=result[
                    "canonical_positive_dither_clearance_check"
                ],
                positive_prefix=result[
                    "canonical_positive_dither_finite_prefix_check"
                ],
                packet=result["canonical_residual_packet_lift_count_check"],
                terminal=result["canonical_terminal_pure_zero_chain_check"],
                frontier=result["canonical_first_nonzero_frontier_check"],
                gate=result["canonical_first_superboundary_lift_gate_active"],
                gate_check=result["canonical_first_superboundary_lift_gate_check"],
                first=result[
                    "canonical_first_superboundary_zero_slope_packet_count_check"
                ],
                first_shape=result[
                    "canonical_first_superboundary_shape_support_count_check"
                ],
                first_shape_bound=result[
                    "canonical_first_superboundary_shape_power_coset_slope_bound_check"
                ],
                second_shape=result[
                    "canonical_second_superboundary_shape_support_count_check"
                ],
                second_transition=result[
                    "canonical_second_superboundary_next_slack_support_count_check"
                ],
                shape=result["canonical_slack_two_shape_support_count_check"],
                shape2=result[
                    "canonical_slack_two_second_shape_support_count_check"
                ],
                shape3=result["canonical_slack_three_shape_support_count_check"],
                floor=result["canonical_subboundary_residual_floor_check"],
                slope=result["canonical_residual_slope_check"],
                boundary=result["canonical_boundary_slope_decomposition_check"],
            )
        )
    print()

    for record in result["top_histograms"]:
        assert isinstance(record, dict)
        print(
            "class={kind} h={hist} supports={supports} "
            "incidences={inc} slopes={slopes}".format(
                kind=record["class"],
                hist=record["histogram_text"],
                supports=record["support_count"],
                inc=record["incidence_count"],
                slopes=record["bad_slope_count"],
            )
        )
        if record["slope_histogram"]:
            slopes = ", ".join(
                f"{slope}:{count}"
                for slope, count in record["slope_histogram"].items()
            )
            print(f"  slope histogram: {slopes}")


def positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan exact-support Pi_S incidences by quotient occupancy."
    )
    parser.add_argument("--prime", type=positive_int, required=True)
    parser.add_argument("--n", type=positive_int, required=True)
    parser.add_argument("--k", type=positive_int, required=True)
    parser.add_argument("--slack", type=positive_int, required=True)
    parser.add_argument("--quotient-order", type=positive_int, required=True)
    parser.add_argument("--primitive", type=positive_int, default=None)
    parser.add_argument("--anchor-exp", type=int, default=None)
    parser.add_argument("--direction-exp", type=int, default=None)
    parser.add_argument("--max-supports", type=positive_int, default=200_000)
    parser.add_argument(
        "--top-histograms",
        type=int,
        default=10,
        help="number of histogram records to retain; negative retains all",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = scan_supports(
        p=args.prime,
        n=args.n,
        k=args.k,
        slack=args.slack,
        quotient_order=args.quotient_order,
        primitive=args.primitive,
        anchor_exp=args.anchor_exp,
        direction_exp=args.direction_exp,
        max_supports=args.max_supports,
        top_histograms=args.top_histograms,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
