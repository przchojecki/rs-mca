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
