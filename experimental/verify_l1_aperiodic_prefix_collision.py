#!/usr/bin/env python3
"""Verify the F_17 aperiodic monomial-prefix collision certificate.

The certificate is a finite L1 route cut: after generated-field entropy clears
and the Paper B quotient-core profile is empty, the monomial-prefix map
Phi_4 on 10-subsets of F_17^* still has aperiodic finite-field collisions.
The maximum fiber size in this toy instance is only 2, so this does not refute
the prefix local-limit target; it refutes an aperiodic-injectivity route.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from math import comb, gcd, log2
from typing import Any, Iterable


STATUS = "PROVED finite certificate; COUNTEREXAMPLE to injectivity route"
P = 17
N = 16
K = 6
SIGMA = 4
AGREEMENT = K + SIGMA
GENERATOR = 3
EXAMPLE_PREFIX = (8, 12, 13, 7)
EXAMPLE_S = (1, 2, 3, 4, 5, 6, 7, 9, 10, 12)
EXAMPLE_T = (1, 2, 3, 8, 10, 11, 13, 14, 15, 16)
EXPECTED_HISTOGRAM = {1: 7928, 2: 40}
EXPECTED_ORBIT_SIZES = (8, 16, 16)
EXPECTED_ORBIT_REPRESENTATIVES = (
    {
        "orbit_size": 16,
        "complements": (
            (1, 2, 3, 4, 6, 9),
            (5, 8, 10, 11, 12, 13),
        ),
        "linear_gap": {"alpha": 3, "beta": 13},
    },
    {
        "orbit_size": 16,
        "complements": (
            (1, 2, 4, 11, 14, 15),
            (6, 8, 9, 12, 13, 16),
        ),
        "linear_gap": {"alpha": 16, "beta": 5},
    },
    {
        "orbit_size": 8,
        "complements": (
            (1, 2, 5, 6, 7, 13),
            (4, 10, 11, 12, 15, 16),
        ),
        "linear_gap": {"alpha": 13, "beta": 0},
    },
)


def positive_divisors(value: int) -> list[int]:
    small: list[int] = []
    large: list[int] = []
    divisor = 1
    while divisor * divisor <= value:
        if value % divisor == 0:
            small.append(divisor)
            if divisor != value // divisor:
                large.append(value // divisor)
        divisor += 1
    return small + large[::-1]


def domain() -> list[int]:
    values = list(range(1, P))
    generated = {pow(GENERATOR, exponent, P) for exponent in range(N)}
    if generated != set(values):
        raise ValueError("GENERATOR is not primitive in F_17^*")
    return values


def elementary_prefix(support: Iterable[int]) -> tuple[int, ...]:
    coeffs = [0] * (SIGMA + 1)
    coeffs[0] = 1
    for value in support:
        for index in range(SIGMA, 0, -1):
            coeffs[index] = (
                coeffs[index] + coeffs[index - 1] * value
            ) % P
    return tuple(coeffs[1:])


def trim_poly(poly: list[int]) -> list[int]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def poly_degree(poly: list[int]) -> int:
    return len(trim_poly(poly[:])) - 1


def poly_sub(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        left_coeff = left[index] if index < len(left) else 0
        right_coeff = right[index] if index < len(right) else 0
        out[index] = (left_coeff - right_coeff) % P
    return trim_poly(out)


def poly_add(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        left_coeff = left[index] if index < len(left) else 0
        right_coeff = right[index] if index < len(right) else 0
        out[index] = (left_coeff + right_coeff) % P
    return trim_poly(out)


def poly_remainder(poly: list[int], divisor: list[int]) -> list[int]:
    rem = trim_poly(poly[:])
    div = trim_poly(divisor[:])
    if not div:
        raise ValueError("divisor must be nonzero")
    inverse_lead = pow(div[-1], -1, P)
    while rem and len(rem) >= len(div):
        shift = len(rem) - len(div)
        scale = (rem[-1] * inverse_lead) % P
        for index, coeff in enumerate(div):
            rem[index + shift] = (rem[index + shift] - scale * coeff) % P
        trim_poly(rem)
    return rem


def divides_xn_minus_one(poly: list[int]) -> bool:
    xn_minus_one = [P - 1] + [0] * (N - 1) + [1]
    return not poly_remainder(xn_minus_one, poly)


def poly_eval(poly: list[int], value: int) -> int:
    total = 0
    for coeff in reversed(poly):
        total = (total * value + coeff) % P
    return total


def multiply_by_linear(poly: list[int], root: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for index, coeff in enumerate(poly):
        out[index] = (out[index] - root * coeff) % P
        out[index + 1] = (out[index + 1] + coeff) % P
    return trim_poly(out)


def locator_polynomial(support: Iterable[int]) -> list[int]:
    poly = [1]
    for value in support:
        poly = multiply_by_linear(poly, value)
    return poly


def monomial_prefix_polynomial(prefix: tuple[int, ...]) -> list[int]:
    poly = [0] * (AGREEMENT + 1)
    poly[AGREEMENT] = 1
    for index, coeff in enumerate(prefix, start=1):
        sign = -1 if index % 2 else 1
        poly[AGREEMENT - index] = (sign * coeff) % P
    return poly


def codeword_from_support(prefix: tuple[int, ...], support: Iterable[int]) -> list[int]:
    return poly_sub(
        monomial_prefix_polynomial(prefix),
        locator_polynomial(support),
    )


def subgroup(order: int) -> set[int]:
    if N % order != 0:
        raise ValueError("order must divide N")
    step = N // order
    return {pow(GENERATOR, step * exponent, P) for exponent in range(order)}


def cosets_of_subgroup(order: int) -> list[set[int]]:
    kernel = subgroup(order)
    remaining = set(domain())
    cosets: list[set[int]] = []
    while remaining:
        representative = next(iter(remaining))
        coset = {(representative * value) % P for value in kernel}
        cosets.append(coset)
        remaining -= coset
    return cosets


def is_union_of_cosets(values: set[int], order: int) -> bool:
    return all(
        not (values & coset) or coset <= values
        for coset in cosets_of_subgroup(order)
    )


def support_complement(support: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(set(domain()) - set(support)))


def scale_support(support: Iterable[int], scalar: int) -> tuple[int, ...]:
    return tuple(sorted((scalar * value) % P for value in support))


def normalize_pair(
    first: Iterable[int],
    second: Iterable[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    first_tuple = tuple(sorted(first))
    second_tuple = tuple(sorted(second))
    ordered = sorted((first_tuple, second_tuple))
    return ordered[0], ordered[1]


def orbit_key(
    first: Iterable[int],
    second: Iterable[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return min(
        normalize_pair(
            scale_support(first, scalar),
            scale_support(second, scalar),
        )
        for scalar in domain()
    )


def linear_locator_gap(
    first: Iterable[int],
    second: Iterable[int],
) -> dict[str, int]:
    first_locator = locator_polynomial(first)
    second_locator = locator_polynomial(second)
    size = max(len(first_locator), len(second_locator))
    difference = []
    for index in range(size):
        first_coeff = first_locator[index] if index < len(first_locator) else 0
        second_coeff = second_locator[index] if index < len(second_locator) else 0
        difference.append((first_coeff - second_coeff) % P)
    if any(difference[index] for index in range(2, len(difference))):
        raise AssertionError("locator gap is not linear")
    return {
        "alpha": difference[1] if len(difference) > 1 else 0,
        "beta": difference[0] if difference else 0,
    }


def pair_stabilizer(
    first: Iterable[int],
    second: Iterable[int],
) -> list[int]:
    normalized = normalize_pair(first, second)
    return [
        scalar
        for scalar in domain()
        if normalize_pair(
            scale_support(first, scalar),
            scale_support(second, scalar),
        )
        == normalized
    ]


def active_quotient_cores() -> list[int]:
    out: list[int] = []
    for order in positive_divisors(gcd(N, K)):
        if order > 1 and SIGMA < order and K // order <= N // order - 1:
            out.append(order)
    return out


def prefix_fibers() -> dict[tuple[int, ...], list[tuple[int, ...]]]:
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for support in itertools.combinations(domain(), AGREEMENT):
        fibers[elementary_prefix(support)].append(support)
    return fibers


def verify_example(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    example_fiber = fibers[EXAMPLE_PREFIX]
    if sorted(example_fiber) != sorted([EXAMPLE_S, EXAMPLE_T]):
        raise AssertionError("example fiber mismatch")

    word = monomial_prefix_polynomial(EXAMPLE_PREFIX)
    codewords = []
    for support in (EXAMPLE_S, EXAMPLE_T):
        codeword = codeword_from_support(EXAMPLE_PREFIX, support)
        if poly_degree(codeword) >= K:
            raise AssertionError("example codeword has degree >= k")
        for value in support:
            if poly_eval(codeword, value) != poly_eval(word, value):
                raise AssertionError("example codeword does not agree on support")
        codewords.append(codeword)

    return {
        "prefix": EXAMPLE_PREFIX,
        "supports": [list(EXAMPLE_S), list(EXAMPLE_T)],
        "word_coefficients_low_to_high": word,
        "codeword_coefficients_low_to_high": codewords,
        "codeword_degrees": [poly_degree(codeword) for codeword in codewords],
    }


def collision_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    quotient_exception_orders = [
        order for order in positive_divisors(N) if order > SIGMA
    ]
    collisions = []
    all_aperiodic = True
    for prefix, supports in sorted(fibers.items()):
        if len(supports) == 1:
            continue
        if len(supports) != 2:
            raise AssertionError("unexpected fiber size above two")
        first = set(supports[0])
        second = set(supports[1])
        difference = first ^ second
        union_flags = {
            str(order): is_union_of_cosets(difference, order)
            for order in quotient_exception_orders
        }
        if any(union_flags.values()):
            all_aperiodic = False
        collisions.append(
            {
                "prefix": prefix,
                "symmetric_difference_size": len(difference),
                "quotient_union_flags": union_flags,
            }
        )

    return {
        "quotient_exception_orders_checked": quotient_exception_orders,
        "collision_fibers": len(collisions),
        "all_collision_fibers_aperiodic": all_aperiodic,
        "symmetric_difference_histogram": dict(
            sorted(
                Counter(
                    row["symmetric_difference_size"] for row in collisions
                ).items()
            )
        ),
    }


def complement_prefix_partition_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    support_to_complement: dict[tuple[int, ...], set[tuple[int, ...]]] = (
        defaultdict(set)
    )
    complement_to_support: dict[tuple[int, ...], set[tuple[int, ...]]] = (
        defaultdict(set)
    )
    for support_prefix, supports in fibers.items():
        for support in supports:
            complement_prefix = elementary_prefix(support_complement(support))
            support_to_complement[support_prefix].add(complement_prefix)
            complement_to_support[complement_prefix].add(support_prefix)

    support_partition_ok = all(
        len(values) == 1 for values in support_to_complement.values()
    )
    complement_partition_ok = all(
        len(values) == 1 for values in complement_to_support.values()
    )
    if not support_partition_ok or not complement_partition_ok:
        raise AssertionError("support/complement prefix partitions differ")

    return {
        "checked": True,
        "support_prefix_values": len(support_to_complement),
        "complement_prefix_values": len(complement_to_support),
        "partitions_agree": True,
        "complement_size": N - AGREEMENT,
        "locator_gap_degree_bound": N - AGREEMENT - SIGMA - 1,
    }


def johnson_packing_bound(n: int, m: int, r: int) -> int:
    if r <= 0:
        return 1
    if r > m:
        return comb(n, m)
    bound = 1
    for offset in range(r - 1, -1, -1):
        bound = ((n - offset) * bound) // (m - offset)
    return bound


def johnson_packing_bound_case(n: int, k: int, sigma: int) -> dict[str, Any]:
    complement_size = n - k - sigma
    gap_dimension = max(n - k - 2 * sigma, 0)
    if gap_dimension == 0:
        packing_bound_floor = 1
    else:
        packing_bound_floor = (
            comb(n, gap_dimension) // comb(complement_size, gap_dimension)
        )
    johnson_bound_floor = johnson_packing_bound(
        n,
        complement_size,
        gap_dimension,
    )
    if johnson_bound_floor > packing_bound_floor:
        raise AssertionError("Johnson recursion exceeded packing ratio")
    return {
        "n": n,
        "k": k,
        "sigma": sigma,
        "complement_size": complement_size,
        "gap_dimension": gap_dimension,
        "packing_bound_floor": packing_bound_floor,
        "johnson_bound_floor": johnson_bound_floor,
        "improves_ratio_floor": johnson_bound_floor < packing_bound_floor,
    }


def co_large_bound_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    complement_size = N - AGREEMENT
    gap_dimension = max(complement_size - SIGMA, 0)
    field_bound = P**gap_dimension
    if gap_dimension == 0:
        packing_numerator = 1
        packing_denominator = 1
    else:
        packing_numerator = comb(N, gap_dimension)
        packing_denominator = comb(complement_size, gap_dimension)
    maximum_fiber_size = max(len(values) for values in fibers.values())
    if maximum_fiber_size > field_bound:
        raise AssertionError("co-large field-size bound failed")
    if maximum_fiber_size * packing_denominator > packing_numerator:
        raise AssertionError("co-large packing bound failed")
    johnson_instance = johnson_packing_bound_case(N, K, SIGMA)
    if maximum_fiber_size > johnson_instance["johnson_bound_floor"]:
        raise AssertionError("co-large Johnson bound failed")
    return {
        "checked": True,
        "complement_size": complement_size,
        "gap_dimension": gap_dimension,
        "field_bound": field_bound,
        "packing_bound_numerator": packing_numerator,
        "packing_bound_denominator": packing_denominator,
        "packing_bound_floor": packing_numerator // packing_denominator,
        "johnson_bound_floor": johnson_instance["johnson_bound_floor"],
        "maximum_fiber_size": maximum_fiber_size,
        "fixed_width_instance": {
            "r": gap_dimension,
            "finite_ratio": (
                packing_numerator / packing_denominator
                if packing_denominator
                else 1.0
            ),
            "asymptotic_base_at_rate": 2 / (1 - (K / N)),
        },
        "holds": True,
    }


def johnson_packing_report() -> dict[str, Any]:
    cases = [
        (N, K, SIGMA),
        (64, 28, 15),
        (128, 56, 31),
        (256, 96, 76),
        (512, 192, 150),
        (1024, 384, 304),
    ]
    checked_cases = [johnson_packing_bound_case(*case) for case in cases]
    return {
        "checked": True,
        "cases": checked_cases,
        "improved_cases": sum(
            1 for case in checked_cases if case["improves_ratio_floor"]
        ),
    }


def plotkin_bound_case(n: int, k: int, sigma: int) -> dict[str, Any]:
    complement_size = n - k - sigma
    gap_dimension = n - k - 2 * sigma
    if gap_dimension <= 0:
        return {
            "n": n,
            "k": k,
            "sigma": sigma,
            "complement_size": complement_size,
            "gap_dimension": gap_dimension,
            "available": True,
            "singleton_range": True,
            "numerator": 1,
            "denominator": 1,
            "upper_bound_floor": 1,
        }

    numerator = n * (complement_size - gap_dimension + 1)
    denominator = (
        complement_size * complement_size
        - n * (gap_dimension - 1)
    )
    available = denominator > 0
    return {
        "n": n,
        "k": k,
        "sigma": sigma,
        "complement_size": complement_size,
        "gap_dimension": gap_dimension,
        "available": available,
        "singleton_range": False,
        "numerator": numerator,
        "denominator": denominator,
        "upper_bound_floor": numerator // denominator if available else None,
    }


def support_johnson_threshold_case(
    n: int,
    k: int,
    sigma: int,
) -> dict[str, Any]:
    agreement = k + sigma
    complement_size = n - agreement
    gap_dimension = n - k - 2 * sigma
    if gap_dimension <= 0:
        return {
            "n": n,
            "k": k,
            "sigma": sigma,
            "agreement": agreement,
            "johnson_margin": agreement * agreement - n * (k - 1),
            "available": True,
            "singleton_range": True,
            "support_numerator": 1,
            "support_denominator": 1,
            "support_bound_floor": 1,
        }

    plotkin_case = plotkin_bound_case(n, k, sigma)
    support_numerator = n * (agreement - k + 1)
    support_denominator = agreement * agreement - n * (k - 1)
    complement_denominator = (
        complement_size * complement_size
        - n * (gap_dimension - 1)
    )
    if support_numerator != plotkin_case["numerator"]:
        raise AssertionError("support numerator does not match Plotkin numerator")
    if support_denominator != complement_denominator:
        raise AssertionError("support denominator does not match complement form")
    if support_denominator != plotkin_case["denominator"]:
        raise AssertionError("support denominator does not match Plotkin case")

    available = support_denominator > 0
    return {
        "n": n,
        "k": k,
        "sigma": sigma,
        "agreement": agreement,
        "johnson_margin": support_denominator,
        "available": available,
        "singleton_range": False,
        "support_numerator": support_numerator,
        "support_denominator": support_denominator,
        "support_bound_floor": (
            support_numerator // support_denominator
            if available
            else None
        ),
        "agreement_square": agreement * agreement,
        "threshold_square": n * (k - 1),
    }


def minimum_square_sum(total: int, boxes: int) -> int:
    quotient, remainder = divmod(total, boxes)
    return (
        (boxes - remainder) * quotient * quotient
        + remainder * (quotient + 1) * (quotient + 1)
    )


def integer_plotkin_bound_case(n: int, k: int, sigma: int) -> dict[str, Any]:
    complement_size = n - k - sigma
    gap_dimension = n - k - 2 * sigma
    rational_case = plotkin_bound_case(n, k, sigma)
    if gap_dimension <= 0:
        return {
            "n": n,
            "k": k,
            "sigma": sigma,
            "complement_size": complement_size,
            "gap_dimension": gap_dimension,
            "available": True,
            "rational_floor": rational_case["upper_bound_floor"],
            "integer_upper_bound": 1,
            "first_excluded_size": 2,
            "first_excluded_witness": None,
        }
    if not rational_case["available"]:
        return {
            "n": n,
            "k": k,
            "sigma": sigma,
            "complement_size": complement_size,
            "gap_dimension": gap_dimension,
            "available": False,
            "rational_floor": None,
            "integer_upper_bound": None,
            "first_excluded_size": None,
            "first_excluded_witness": None,
        }

    integer_upper_bound = 1
    first_excluded_size = None
    first_excluded_witness = None
    rational_floor = rational_case["upper_bound_floor"]
    for list_size in range(1, rational_floor + 1):
        total_incidence = list_size * complement_size
        min_squares = minimum_square_sum(total_incidence, n)
        max_squares = (
            total_incidence
            + list_size * (list_size - 1) * (gap_dimension - 1)
        )
        if min_squares <= max_squares:
            integer_upper_bound = list_size
            continue
        first_excluded_size = list_size
        first_excluded_witness = {
            "total_incidence": total_incidence,
            "minimum_square_sum": min_squares,
            "maximum_allowed_square_sum": max_squares,
        }
        break

    return {
        "n": n,
        "k": k,
        "sigma": sigma,
        "complement_size": complement_size,
        "gap_dimension": gap_dimension,
        "available": True,
        "rational_floor": rational_floor,
        "integer_upper_bound": integer_upper_bound,
        "first_excluded_size": first_excluded_size,
        "first_excluded_witness": first_excluded_witness,
    }


def co_large_plotkin_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    maximum_fiber_size = max(len(values) for values in fibers.values())
    finite_instance = plotkin_bound_case(N, K, SIGMA)
    if not finite_instance["available"]:
        raise AssertionError("F_17 Plotkin bound should be available")
    if maximum_fiber_size > finite_instance["upper_bound_floor"]:
        raise AssertionError("co-large Plotkin bound failed")

    grid_cases = [
        (N, K, SIGMA),
        (64, 28, 15),
        (128, 56, 31),
        (256, 96, 76),
        (512, 192, 150),
        (1024, 384, 304),
    ]
    cases = [plotkin_bound_case(*case) for case in grid_cases]
    if not all(case["available"] for case in cases):
        raise AssertionError("deterministic Plotkin grid left the safe range")

    support_johnson_cases = [
        support_johnson_threshold_case(*case)
        for case in grid_cases
    ]
    for plotkin_case, support_case in zip(cases, support_johnson_cases):
        if plotkin_case["available"] != support_case["available"]:
            raise AssertionError("support Johnson availability mismatch")
        if (
            plotkin_case["upper_bound_floor"]
            != support_case["support_bound_floor"]
        ):
            raise AssertionError("support Johnson bound mismatch")

    integer_cases = [integer_plotkin_bound_case(*case) for case in grid_cases]
    if not all(case["available"] for case in integer_cases):
        raise AssertionError("integer Plotkin grid left the safe range")
    finite_integer = integer_cases[0]
    if maximum_fiber_size > finite_integer["integer_upper_bound"]:
        raise AssertionError("integer Plotkin bound failed")

    return {
        "checked": True,
        "finite_instance": finite_instance,
        "finite_integer_instance": finite_integer,
        "finite_support_johnson_instance": support_johnson_cases[0],
        "deterministic_cases": cases,
        "support_johnson_cases": support_johnson_cases,
        "integer_deterministic_cases": integer_cases,
        "maximum_fiber_size": maximum_fiber_size,
        "holds": True,
    }


def plotkin_defect_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    complement_size = N - AGREEMENT
    gap_dimension = N - K - 2 * SIGMA
    degree_variance_histogram: Counter[int] = Counter()
    pair_slack_histogram: Counter[int] = Counter()
    total_defect_histogram: Counter[int] = Counter()
    checked_fibers = 0

    for supports in fibers.values():
        list_size = len(supports)
        if list_size < 2:
            continue
        checked_fibers += 1
        degrees: Counter[int] = Counter()
        for support in supports:
            for value in support_complement(support):
                degrees[value] += 1

        incidence_total = list_size * complement_size
        square_sum = sum(count * count for count in degrees.values())
        ordered_intersections = sum(
            count * (count - 1)
            for count in degrees.values()
        )
        max_ordered_intersections = (
            list_size * (list_size - 1) * (gap_dimension - 1)
        )
        degree_variance = N * square_sum - incidence_total * incidence_total
        pair_slack = max_ordered_intersections - ordered_intersections
        total_defect = (
            N * (incidence_total + max_ordered_intersections)
            - incidence_total * incidence_total
        )
        if pair_slack < 0:
            raise AssertionError("negative Plotkin pair slack")
        if total_defect != degree_variance + N * pair_slack:
            raise AssertionError("Plotkin defect identity failed")

        degree_variance_histogram[degree_variance] += 1
        pair_slack_histogram[pair_slack] += 1
        total_defect_histogram[total_defect] += 1

    return {
        "checked": True,
        "checked_nonsingleton_fibers": checked_fibers,
        "degree_variance_histogram": dict(
            sorted(degree_variance_histogram.items())
        ),
        "pair_slack_histogram": dict(sorted(pair_slack_histogram.items())),
        "total_defect_histogram": dict(sorted(total_defect_histogram.items())),
        "equality_requires_regular_max_intersecting": True,
    }


def affine_rs_list_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    complement_size = N - AGREEMENT
    rs_dimension = max(complement_size - SIGMA, 0)
    if rs_dimension == 0:
        low_degree_polys = [[]]
    else:
        low_degree_polys = [
            list(coeffs)
            for coeffs in itertools.product(range(P), repeat=rs_dimension)
        ]

    list_size_histogram: Counter[int] = Counter()
    maximum_affine_list_size = 0
    domain_values = domain()

    for supports in fibers.values():
        base_locator = locator_polynomial(support_complement(supports[0]))
        observed_gaps: set[tuple[int, ...]] = set()
        for support in supports:
            locator = locator_polynomial(support_complement(support))
            gap = tuple(poly_sub(locator, base_locator))
            if poly_degree(list(gap)) >= rs_dimension:
                raise AssertionError("observed gap is outside RS_r")
            observed_gaps.add(gap)

        affine_gaps: set[tuple[int, ...]] = set()
        for gap_poly in low_degree_polys:
            candidate = poly_add(base_locator, gap_poly)
            zeros = tuple(
                value for value in domain_values
                if poly_eval(candidate, value) == 0
            )
            if len(zeros) != complement_size:
                continue
            if locator_polynomial(zeros) != candidate:
                raise AssertionError("affine-list element is not a locator")
            affine_gaps.add(tuple(trim_poly(gap_poly[:])))

        if affine_gaps != observed_gaps:
            raise AssertionError("affine RS list does not match prefix fiber")
        list_size = len(affine_gaps)
        list_size_histogram[list_size] += 1
        maximum_affine_list_size = max(maximum_affine_list_size, list_size)

    johnson_case = plotkin_bound_case(N, K, SIGMA)
    return {
        "checked": True,
        "checked_fibers": len(fibers),
        "rs_dimension": rs_dimension,
        "agreement": complement_size,
        "search_space_size": len(low_degree_polys),
        "list_size_histogram": dict(sorted(list_size_histogram.items())),
        "maximum_affine_list_size": maximum_affine_list_size,
        "matches_prefix_fibers": True,
        "rs_minimum_distance": N - rs_dimension + 1,
        "johnson_region": {
            "m_squared": complement_size * complement_size,
            "n_times_r_minus_one": N * (rs_dimension - 1),
            "inside": johnson_case["available"],
            "plotkin_bound_floor": johnson_case["upper_bound_floor"],
        },
    }


def co_large_separation_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    exchange_histogram: Counter[int] = Counter()
    overlap_histogram: Counter[int] = Counter()
    fixed_support_exchange_counts: dict[tuple[int, ...], Counter[int]] = {}
    strict_high_overlap_pairs = 0
    pair_count = 0

    for supports in fibers.values():
        if len(supports) < 2:
            continue
        for support in supports:
            fixed_support_exchange_counts[support] = Counter()
        for first, second in itertools.combinations(supports, 2):
            first_set = set(first)
            second_set = set(second)
            exchange = len(first_set - second_set)
            overlap = len(first_set & second_set)
            pair_count += 1
            exchange_histogram[exchange] += 1
            overlap_histogram[overlap] += 1
            fixed_support_exchange_counts[first][exchange] += 1
            fixed_support_exchange_counts[second][exchange] += 1
            if exchange < SIGMA:
                strict_high_overlap_pairs += 1

    if pair_count:
        min_exchange = min(exchange_histogram)
        max_overlap = max(overlap_histogram)
        if min_exchange < SIGMA + 1:
            raise AssertionError("co-large exchange separation failed")
        if max_overlap > K - 1:
            raise AssertionError("co-large overlap separation failed")
    else:
        min_exchange = None
        max_overlap = None

    if strict_high_overlap_pairs:
        raise AssertionError("found strict high-overlap pair inside a prefix fiber")

    ordered_exchange_profile = {
        exchange: 2 * count
        for exchange, count in sorted(exchange_histogram.items())
    }
    max_exchange_codegree: Counter[int] = Counter()
    for counts in fixed_support_exchange_counts.values():
        for exchange, count in counts.items():
            max_exchange_codegree[exchange] = max(
                max_exchange_codegree[exchange],
                count,
            )
    for exchange in range(1, SIGMA + 1):
        if ordered_exchange_profile.get(exchange, 0):
            raise AssertionError("unexpected ordered mass at small exchange")
        if max_exchange_codegree.get(exchange, 0):
            raise AssertionError("unexpected codegree at small exchange")

    return {
        "checked": True,
        "unordered_pair_count": pair_count,
        "minimum_exchange": min_exchange,
        "maximum_overlap": max_overlap,
        "exchange_histogram": dict(sorted(exchange_histogram.items())),
        "overlap_histogram": dict(sorted(overlap_histogram.items())),
        "ordered_exchange_profile": ordered_exchange_profile,
        "max_exchange_codegree": dict(sorted(max_exchange_codegree.items())),
        "zero_exchange_profile_through": SIGMA,
        "strict_high_overlap_pairs_at_slack_sigma": strict_high_overlap_pairs,
        "internal_m1_correction_vanishes": True,
    }


def verify_growing_width_envelope(
    n: int,
    k: int,
    sigma: int,
    rho_num: int,
    rho_den: int,
) -> dict[str, Any]:
    if k * rho_den > rho_num * n:
        raise AssertionError("k/n exceeds rho")
    r = n - k - 2 * sigma
    if r < 0:
        raise AssertionError("not in the co-large strip")
    denominator = (rho_den - rho_num) * n - rho_den * r
    if denominator <= 0:
        raise AssertionError("growth envelope denominator is not positive")

    m = n - k - sigma
    packing_numerator = comb(n, r)
    packing_denominator = comb(m, r)
    envelope_numerator = 2 * rho_den * n
    envelope_denominator = denominator

    if (
        packing_numerator * envelope_denominator**r
        > packing_denominator * envelope_numerator**r
    ):
        raise AssertionError("growing-width envelope failed")

    return {
        "n": n,
        "k": k,
        "sigma": sigma,
        "rho": f"{rho_num}/{rho_den}",
        "r": r,
        "packing_bound_numerator": packing_numerator,
        "packing_bound_denominator": packing_denominator,
        "envelope_base_numerator": envelope_numerator,
        "envelope_base_denominator": envelope_denominator,
        "holds": True,
    }


def growing_width_report() -> dict[str, Any]:
    cases = [
        (N, K, SIGMA, 3, 8),
        (64, 28, 15, 1, 2),
        (128, 56, 31, 1, 2),
        (256, 96, 76, 1, 2),
        (512, 192, 150, 1, 2),
        (1024, 384, 304, 1, 2),
    ]
    return {
        "checked": True,
        "cases": [
            verify_growing_width_envelope(*case)
            for case in cases
        ],
    }


def divisor_gap_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    gap_degree_bound = N - AGREEMENT - SIGMA - 1
    gap_degrees: Counter[int] = Counter()
    nonzero_gaps: set[tuple[int, ...]] = set()
    total_parameters = 0

    for supports in fibers.values():
        base_locator = locator_polynomial(support_complement(supports[0]))
        seen_gaps: set[tuple[int, ...]] = set()
        for support in supports:
            locator = locator_polynomial(support_complement(support))
            if not divides_xn_minus_one(locator):
                raise AssertionError("complement locator does not divide X^n-1")
            gap = tuple(poly_sub(locator, base_locator))
            if gap in seen_gaps:
                raise AssertionError("divisor-gap parametrization is not injective")
            seen_gaps.add(gap)
            degree = poly_degree(list(gap))
            if degree > gap_degree_bound:
                raise AssertionError("divisor gap exceeds degree bound")
            gap_degrees[degree] += 1
            if gap:
                nonzero_gaps.add(gap)
            total_parameters += 1
        if len(seen_gaps) != len(supports):
            raise AssertionError("divisor-gap count mismatch")

    return {
        "checked": True,
        "gap_degree_bound": gap_degree_bound,
        "parameterized_supports": total_parameters,
        "zero_gap_count": gap_degrees[-1],
        "nonzero_gap_count": total_parameters - gap_degrees[-1],
        "distinct_nonzero_gaps": len(nonzero_gaps),
        "gap_degree_histogram": dict(sorted(gap_degrees.items())),
    }


def divisor_gap_graph_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    component_sizes = Counter(len(supports) for supports in fibers.values())
    vertices = sum(size * count for size, count in component_sizes.items())
    edge_count = sum(
        count * size * (size - 1) // 2
        for size, count in component_sizes.items()
    )
    nontrivial_components = sum(
        count for size, count in component_sizes.items() if size > 1
    )
    max_component = max(component_sizes)
    if vertices != comb(N, AGREEMENT):
        raise AssertionError("divisor-gap graph vertex count mismatch")
    if max_component != max(EXPECTED_HISTOGRAM):
        raise AssertionError("unexpected divisor-gap graph maximum component")
    return {
        "checked": True,
        "vertices": vertices,
        "components": len(fibers),
        "component_size_histogram": dict(sorted(component_sizes.items())),
        "nontrivial_components": nontrivial_components,
        "edge_count": edge_count,
        "max_component_size": max_component,
        "components_are_cliques": True,
    }


def complement_orbit_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    orbit_members: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[dict[str, Any]],
    ] = defaultdict(list)
    all_gaps_linear = True

    for prefix, supports in sorted(fibers.items()):
        if len(supports) == 1:
            continue
        first_support, second_support = supports
        first_complement = support_complement(first_support)
        second_complement = support_complement(second_support)
        if elementary_prefix(first_complement) != elementary_prefix(
            second_complement
        ):
            raise AssertionError("complement prefixes do not match")
        try:
            gap = linear_locator_gap(first_complement, second_complement)
        except AssertionError:
            all_gaps_linear = False
            raise
        orbit_members[orbit_key(first_complement, second_complement)].append(
            {
                "prefix": prefix,
                "linear_gap": gap,
            }
        )

    representatives = []
    for key in sorted(orbit_members):
        first, second = key
        representatives.append(
            {
                "orbit_size": len(orbit_members[key]),
                "complements": [list(first), list(second)],
                "linear_gap": linear_locator_gap(first, second),
                "stabilizer": pair_stabilizer(first, second),
            }
        )

    orbit_sizes = tuple(sorted(row["orbit_size"] for row in representatives))
    expected_representatives = [
        {
            "orbit_size": row["orbit_size"],
            "complements": [list(part) for part in row["complements"]],
            "linear_gap": row["linear_gap"],
        }
        for row in EXPECTED_ORBIT_REPRESENTATIVES
    ]
    observed_representatives = [
        {
            "orbit_size": row["orbit_size"],
            "complements": row["complements"],
            "linear_gap": row["linear_gap"],
        }
        for row in representatives
    ]
    if orbit_sizes != EXPECTED_ORBIT_SIZES:
        raise AssertionError("unexpected complement orbit sizes")
    if observed_representatives != expected_representatives:
        raise AssertionError("unexpected complement orbit representatives")

    return {
        "complement_prefix_equivalence_checked": True,
        "all_locator_gaps_linear": all_gaps_linear,
        "dilation_orbits": len(representatives),
        "orbit_size_histogram": dict(
            sorted(Counter(row["orbit_size"] for row in representatives).items())
        ),
        "representatives": representatives,
    }


def build_certificate() -> dict[str, Any]:
    fibers = prefix_fibers()
    histogram = Counter(len(values) for values in fibers.values())
    entropy_margin = SIGMA * log2(P) - log2(comb(N, AGREEMENT))

    if dict(histogram) != EXPECTED_HISTOGRAM:
        raise AssertionError("unexpected prefix fiber histogram")
    if entropy_margin <= 0:
        raise AssertionError("entropy margin should be positive")
    if active_quotient_cores():
        raise AssertionError("quotient-core profile should be empty")

    collisions = collision_report(fibers)
    if not collisions["all_collision_fibers_aperiodic"]:
        raise AssertionError("found quotient-periodic collision")
    complement_partition = complement_prefix_partition_report(fibers)
    divisor_gaps = divisor_gap_report(fibers)
    divisor_graph = divisor_gap_graph_report(fibers)
    co_large_bound = co_large_bound_report(fibers)
    johnson_packing = johnson_packing_report()
    co_large_plotkin = co_large_plotkin_report(fibers)
    plotkin_defects = plotkin_defect_report(fibers)
    affine_rs_list = affine_rs_list_report(fibers)
    co_large_separation = co_large_separation_report(fibers)
    growing_width = growing_width_report()
    complement_orbits = complement_orbit_report(fibers)

    return {
        "status": STATUS,
        "inputs": {
            "field": "F_17",
            "p": P,
            "domain": "F_17^*",
            "n": N,
            "k": K,
            "sigma": SIGMA,
            "agreement": AGREEMENT,
            "generator": GENERATOR,
        },
        "entropy_ledger": {
            "margin_bits": entropy_margin,
            "clears": entropy_margin > 0,
        },
        "quotient_core_ledger": {
            "gcd_n_k": gcd(N, K),
            "active_quotient_cores": active_quotient_cores(),
            "empty": not active_quotient_cores(),
        },
        "prefix_distribution": {
            "total_supports": comb(N, AGREEMENT),
            "distinct_prefix_values": len(fibers),
            "fiber_size_histogram": dict(sorted(histogram.items())),
            "maximum_fiber_size": max(histogram),
        },
        "collision_report": collisions,
        "complement_prefix_lemma_report": complement_partition,
        "divisor_gap_report": divisor_gaps,
        "divisor_gap_graph_report": divisor_graph,
        "co_large_bound_report": co_large_bound,
        "johnson_packing_report": johnson_packing,
        "co_large_plotkin_report": co_large_plotkin,
        "plotkin_defect_report": plotkin_defects,
        "affine_rs_list_report": affine_rs_list,
        "co_large_separation_report": co_large_separation,
        "growing_width_report": growing_width,
        "complement_orbit_report": complement_orbits,
        "example": verify_example(fibers),
        "passed": True,
    }


def print_text(cert: dict[str, Any]) -> None:
    inputs = cert["inputs"]
    distribution = cert["prefix_distribution"]
    collisions = cert["collision_report"]
    complement_partition = cert["complement_prefix_lemma_report"]
    divisor_gaps = cert["divisor_gap_report"]
    divisor_graph = cert["divisor_gap_graph_report"]
    co_large_bound = cert["co_large_bound_report"]
    johnson_packing = cert["johnson_packing_report"]
    co_large_plotkin = cert["co_large_plotkin_report"]
    plotkin_defects = cert["plotkin_defect_report"]
    affine_rs_list = cert["affine_rs_list_report"]
    co_large_separation = cert["co_large_separation_report"]
    growing_width = cert["growing_width_report"]
    complement_orbits = cert["complement_orbit_report"]
    print("L1 aperiodic prefix-collision certificate")
    print(f"Status: {cert['status']}")
    print(
        "p={p}, n={n}, k={k}, sigma={sigma}, agreement={agreement}".format(
            **inputs
        )
    )
    print(
        "entropy margin bits: "
        f"{cert['entropy_ledger']['margin_bits']:.6f}"
    )
    print(
        "active quotient cores: "
        f"{cert['quotient_core_ledger']['active_quotient_cores']}"
    )
    print(f"total supports: {distribution['total_supports']}")
    print(f"distinct prefix values: {distribution['distinct_prefix_values']}")
    print(f"fiber histogram: {distribution['fiber_size_histogram']}")
    print(f"maximum fiber size: {distribution['maximum_fiber_size']}")
    print(f"collision fibers: {collisions['collision_fibers']}")
    print(
        "all collision fibers aperiodic for orders "
        f"{collisions['quotient_exception_orders_checked']}: "
        f"{collisions['all_collision_fibers_aperiodic']}"
    )
    print(
        "symmetric-difference histogram: "
        f"{collisions['symmetric_difference_histogram']}"
    )
    print(
        "support/complement prefix partitions agree: "
        f"{complement_partition['partitions_agree']} "
        f"({complement_partition['support_prefix_values']} values)"
    )
    print(
        "divisor-gap parametrization: "
        f"{divisor_gaps['parameterized_supports']} supports, "
        f"{divisor_gaps['nonzero_gap_count']} nonzero gaps, "
        f"degree bound {divisor_gaps['gap_degree_bound']}"
    )
    print(
        "divisor-gap graph: "
        f"{divisor_graph['components']} components, "
        f"{divisor_graph['nontrivial_components']} nontrivial, "
        f"{divisor_graph['edge_count']} edges"
    )
    print(
        "co-large packing bound: "
        f"max fiber {co_large_bound['maximum_fiber_size']} <= "
        f"{co_large_bound['packing_bound_numerator']}/"
        f"{co_large_bound['packing_bound_denominator']} "
        f"= {co_large_bound['packing_bound_floor']}"
    )
    print(
        "co-large Johnson bound: "
        f"max fiber {co_large_bound['maximum_fiber_size']} <= "
        f"{co_large_bound['johnson_bound_floor']}"
    )
    print(
        "fixed-width instance: "
        f"r={co_large_bound['fixed_width_instance']['r']}, "
        f"finite ratio={co_large_bound['fixed_width_instance']['finite_ratio']:.3f}"
    )
    print(
        "co-large field-size bound: "
        f"max fiber {co_large_bound['maximum_fiber_size']} <= "
        f"{co_large_bound['field_bound']}"
    )
    plotkin_instance = co_large_plotkin["finite_instance"]
    print(
        "co-large Plotkin bound: "
        f"max fiber {co_large_plotkin['maximum_fiber_size']} <= "
        f"{plotkin_instance['numerator']}/"
        f"{plotkin_instance['denominator']} "
        f"= {plotkin_instance['upper_bound_floor']}"
    )
    integer_plotkin = co_large_plotkin["finite_integer_instance"]
    print(
        "integer Plotkin bound: "
        f"max fiber {co_large_plotkin['maximum_fiber_size']} <= "
        f"{integer_plotkin['integer_upper_bound']} "
        f"(first excluded {integer_plotkin['first_excluded_size']})"
    )
    support_johnson = co_large_plotkin["finite_support_johnson_instance"]
    print(
        "support Johnson margin: "
        f"{support_johnson['agreement_square']} > "
        f"{support_johnson['threshold_square']}, "
        f"bound {support_johnson['support_bound_floor']}"
    )
    print(
        "Plotkin defects: "
        f"D2={plotkin_defects['degree_variance_histogram']}, "
        f"P2={plotkin_defects['pair_slack_histogram']}, "
        f"total={plotkin_defects['total_defect_histogram']}"
    )
    print(
        "affine RS list reduction: "
        f"dimension {affine_rs_list['rs_dimension']}, "
        f"search {affine_rs_list['search_space_size']}, "
        f"histogram {affine_rs_list['list_size_histogram']}"
    )
    print(
        "co-large separation: "
        f"min exchange {co_large_separation['minimum_exchange']}, "
        f"max overlap {co_large_separation['maximum_overlap']}, "
        "strict high-overlap pairs "
        f"{co_large_separation['strict_high_overlap_pairs_at_slack_sigma']}"
    )
    print(
        "internal exchange profile: "
        f"Delta={co_large_separation['ordered_exchange_profile']}, "
        f"Gamma={co_large_separation['max_exchange_codegree']}"
    )
    print(
        "growing-width envelope cases checked: "
        f"{len(growing_width['cases'])}"
    )
    print(
        "Plotkin grid cases checked: "
        f"{len(co_large_plotkin['deterministic_cases'])}"
    )
    print(
        "Johnson grid cases checked: "
        f"{len(johnson_packing['cases'])}, "
        f"improved {johnson_packing['improved_cases']}"
    )
    print(
        "complement dilation orbits: "
        f"{complement_orbits['dilation_orbits']} with size histogram "
        f"{complement_orbits['orbit_size_histogram']}"
    )
    print(
        "all complement locator gaps linear: "
        f"{complement_orbits['all_locator_gaps_linear']}"
    )
    print(f"example prefix: {cert['example']['prefix']}")
    print("passed: True")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cert = build_certificate()
    if args.format == "json":
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print_text(cert)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
