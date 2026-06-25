#!/usr/bin/env python3
"""Finite checks for the M1 quotient occupancy theorem."""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict
from math import comb, factorial


def occupancy_profiles(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
) -> list[tuple[int, ...]]:
    profiles: list[tuple[int, ...]] = []

    def rec(level: int, remaining_fibers: int, remaining_points: int, values: list[int]) -> None:
        if level == fiber_size:
            if remaining_points == level * remaining_fibers:
                profiles.append(tuple(values + [remaining_fibers]))
            return
        for count in range(remaining_fibers + 1):
            used = level * count
            if used > remaining_points:
                break
            max_future = fiber_size * (remaining_fibers - count)
            if remaining_points - used > max_future:
                continue
            rec(
                level + 1,
                remaining_fibers - count,
                remaining_points - used,
                values + [count],
            )

    rec(0, fiber_count, support_size, [])
    return profiles


def occupancy_count_formula(profile: tuple[int, ...], fiber_size: int) -> int:
    fiber_count = sum(profile)
    out = factorial(fiber_count)
    for occupancy, count in enumerate(profile):
        out //= factorial(count)
        out *= comb(fiber_size, occupancy) ** count
    return out


def brute_occupancy_counts(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
) -> Counter[tuple[int, ...]]:
    points = [(fiber, point) for fiber in range(fiber_count) for point in range(fiber_size)]
    counts: Counter[tuple[int, ...]] = Counter()
    for support in itertools.combinations(points, support_size):
        fiber_hits = [0] * fiber_count
        for fiber, _ in support:
            fiber_hits[fiber] += 1
        profile = [0] * (fiber_size + 1)
        for hit in fiber_hits:
            profile[hit] += 1
        counts[tuple(profile)] += 1
    return counts


def check_occupancy_case(fiber_count: int, fiber_size: int, support_size: int) -> None:
    brute = brute_occupancy_counts(fiber_count, fiber_size, support_size)
    formulas = {
        profile: occupancy_count_formula(profile, fiber_size)
        for profile in occupancy_profiles(fiber_count, fiber_size, support_size)
    }
    if brute != formulas:
        raise AssertionError((fiber_count, fiber_size, support_size, brute, formulas))
    if sum(formulas.values()) != comb(fiber_count * fiber_size, support_size):
        raise AssertionError((fiber_count, fiber_size, support_size, sum(formulas.values())))


def whole_fiber_supports(fiber_count: int, whole_fibers: int, fiber_size: int) -> list[frozenset[int]]:
    supports: list[frozenset[int]] = []
    for chosen in itertools.combinations(range(fiber_count), whole_fibers):
        points = {
            fiber * fiber_size + point
            for fiber in chosen
            for point in range(fiber_size)
        }
        supports.append(frozenset(points))
    return supports


def brute_exchange_profile(
    fiber_count: int,
    whole_fibers: int,
    fiber_size: int,
) -> tuple[Counter[int], dict[int, int]]:
    supports = whole_fiber_supports(fiber_count, whole_fibers, fiber_size)
    delta: Counter[int] = Counter()
    codegrees: dict[int, Counter[frozenset[int]]] = defaultdict(Counter)
    for left in supports:
        for right in supports:
            if left == right:
                continue
            exchange = len(left - right)
            delta[exchange] += 1
            codegrees[exchange][left] += 1
    gamma = {
        exchange: max(per_support.values(), default=0)
        for exchange, per_support in codegrees.items()
    }
    return delta, gamma


def exchange_formula(
    fiber_count: int,
    whole_fibers: int,
    fiber_size: int,
) -> tuple[Counter[int], dict[int, int]]:
    delta: Counter[int] = Counter()
    gamma: dict[int, int] = {}
    support_count = comb(fiber_count, whole_fibers)
    for quotient_exchange in range(1, min(whole_fibers, fiber_count - whole_fibers) + 1):
        exchange = quotient_exchange * fiber_size
        codegree = comb(whole_fibers, quotient_exchange) * comb(
            fiber_count - whole_fibers,
            quotient_exchange,
        )
        delta[exchange] = support_count * codegree
        gamma[exchange] = codegree
    return delta, gamma


def strict_budget_formula(
    fiber_count: int,
    whole_fibers: int,
    fiber_size: int,
    slack: int,
    field_size: int,
) -> int:
    return sum(
        comb(whole_fibers, h)
        * comb(fiber_count - whole_fibers, h)
        * (field_size ** (slack - h * fiber_size))
        for h in range(1, min(whole_fibers, fiber_count - whole_fibers) + 1)
        if h * fiber_size <= slack - 1
    )


def strict_budget_from_gamma(
    gamma: dict[int, int],
    slack: int,
    field_size: int,
) -> int:
    return sum(
        codegree * (field_size ** (slack - exchange))
        for exchange, codegree in gamma.items()
        if exchange <= slack - 1
    )


def check_exchange_case(
    fiber_count: int,
    whole_fibers: int,
    fiber_size: int,
    slack: int,
    field_size: int,
) -> None:
    brute_delta, brute_gamma = brute_exchange_profile(fiber_count, whole_fibers, fiber_size)
    formula_delta, formula_gamma = exchange_formula(fiber_count, whole_fibers, fiber_size)
    if brute_delta != formula_delta:
        raise AssertionError((fiber_count, whole_fibers, fiber_size, brute_delta, formula_delta))
    if brute_gamma != formula_gamma:
        raise AssertionError((fiber_count, whole_fibers, fiber_size, brute_gamma, formula_gamma))
    direct_budget = strict_budget_from_gamma(brute_gamma, slack, field_size)
    formula_budget = strict_budget_formula(
        fiber_count,
        whole_fibers,
        fiber_size,
        slack,
        field_size,
    )
    if direct_budget != formula_budget:
        raise AssertionError((fiber_count, whole_fibers, fiber_size, direct_budget, formula_budget))


def multiply_polynomials(left: Counter[int], right: Counter[int]) -> Counter[int]:
    product: Counter[int] = Counter()
    for left_degree, left_coeff in left.items():
        for right_degree, right_coeff in right.items():
            product[left_degree + right_degree] += left_coeff * right_coeff
    return product


def exchange_kernel_formula(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
    target_occupancy: tuple[int, ...],
) -> Counter[int]:
    kernel: Counter[int] = Counter({0: 1})
    for source, target in zip(source_occupancy, target_occupancy):
        fiber_kernel: Counter[int] = Counter()
        lower = max(0, source + target - fiber_size)
        upper = min(source, target)
        for intersection in range(lower, upper + 1):
            exchange = source - intersection
            fiber_kernel[exchange] += comb(source, intersection) * comb(
                fiber_size - source,
                target - intersection,
            )
        kernel = multiply_polynomials(kernel, fiber_kernel)
    return +kernel


def canonical_support(
    fiber_size: int,
    occupancy: tuple[int, ...],
) -> frozenset[int]:
    points: set[int] = set()
    for fiber, count in enumerate(occupancy):
        for point in range(count):
            points.add(fiber * fiber_size + point)
    return frozenset(points)


def supports_with_occupancy(
    fiber_size: int,
    occupancy: tuple[int, ...],
) -> list[frozenset[int]]:
    per_fiber_choices: list[list[tuple[int, ...]]] = []
    for count in occupancy:
        per_fiber_choices.append(list(itertools.combinations(range(fiber_size), count)))
    supports: list[frozenset[int]] = []
    for choices in itertools.product(*per_fiber_choices):
        points: set[int] = set()
        for fiber, fiber_points in enumerate(choices):
            for point in fiber_points:
                points.add(fiber * fiber_size + point)
        supports.append(frozenset(points))
    return supports


def brute_exchange_kernel(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
    target_occupancy: tuple[int, ...],
) -> Counter[int]:
    source = canonical_support(fiber_size, source_occupancy)
    counts: Counter[int] = Counter()
    for target in supports_with_occupancy(fiber_size, target_occupancy):
        counts[len(source - target)] += 1
    return counts


def check_exchange_kernel_case(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
    target_occupancy: tuple[int, ...],
) -> None:
    if sum(source_occupancy) != sum(target_occupancy):
        raise AssertionError((source_occupancy, target_occupancy, "unequal support sizes"))
    formula = exchange_kernel_formula(fiber_size, source_occupancy, target_occupancy)
    brute = brute_exchange_kernel(fiber_size, source_occupancy, target_occupancy)
    if formula != brute:
        raise AssertionError((fiber_size, source_occupancy, target_occupancy, formula, brute))
    if source_occupancy == target_occupancy:
        exchange_one = formula.get(1, 0)
        expected = sum(source * (fiber_size - source) for source in source_occupancy)
        if exchange_one != expected:
            raise AssertionError((fiber_size, source_occupancy, exchange_one, expected))


def occupancy_vectors(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
) -> list[tuple[int, ...]]:
    vectors: list[tuple[int, ...]] = []

    def rec(index: int, remaining: int, prefix: list[int]) -> None:
        if index == fiber_count:
            if remaining == 0:
                vectors.append(tuple(prefix))
            return
        remaining_slots = fiber_count - index - 1
        for occupancy in range(min(fiber_size, remaining) + 1):
            if remaining - occupancy > remaining_slots * fiber_size:
                continue
            prefix.append(occupancy)
            rec(index + 1, remaining - occupancy, prefix)
            prefix.pop()

    rec(0, support_size, [])
    return vectors


def internal_exchange_one(occupancy: tuple[int, ...], fiber_size: int) -> int:
    return sum(value * (fiber_size - value) for value in occupancy)


def is_whole_fiber_vector(occupancy: tuple[int, ...], fiber_size: int) -> bool:
    return all(value in (0, fiber_size) for value in occupancy)


def check_exchange_one_floor_case(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
) -> None:
    residue = support_size % fiber_size
    vectors = occupancy_vectors(fiber_count, fiber_size, support_size)
    values = [
        (internal_exchange_one(vector, fiber_size), vector)
        for vector in vectors
    ]
    minimum = min(value for value, _ in values)
    if residue:
        expected = residue * (fiber_size - residue)
        if minimum != expected:
            raise AssertionError((fiber_count, fiber_size, support_size, minimum, expected))
        for value, vector in values:
            partial = [entry for entry in vector if 0 < entry < fiber_size]
            if value == expected:
                if partial != [residue]:
                    raise AssertionError((fiber_count, fiber_size, support_size, vector))
            elif partial != [residue] and value < expected + 2:
                raise AssertionError(
                    (
                        fiber_count,
                        fiber_size,
                        support_size,
                        vector,
                        value,
                        expected + 2,
                    )
                )
    else:
        if minimum != 0:
            raise AssertionError((fiber_count, fiber_size, support_size, minimum))
        for value, vector in values:
            if value == 0 and not is_whole_fiber_vector(vector, fiber_size):
                raise AssertionError((fiber_count, fiber_size, support_size, vector))
        nonwhole_values = [
            (value, vector)
            for value, vector in values
            if not is_whole_fiber_vector(vector, fiber_size)
        ]
        if 0 < support_size < fiber_count * fiber_size and nonwhole_values:
            expected = 2 * (fiber_size - 1)
            nonwhole_minimum = min(value for value, _ in nonwhole_values)
            if nonwhole_minimum != expected:
                raise AssertionError(
                    (fiber_count, fiber_size, support_size, nonwhole_minimum, expected)
                )
            for value, vector in nonwhole_values:
                if value == expected:
                    partial = sorted(entry for entry in vector if 0 < entry < fiber_size)
                    if partial != [1, fiber_size - 1]:
                        raise AssertionError((fiber_count, fiber_size, support_size, vector))


def one_remainder_supports(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    remainder_size: int,
) -> list[frozenset[int]]:
    supports: list[frozenset[int]] = []
    for whole_indices in itertools.combinations(range(fiber_count), whole_fibers):
        whole_set = set(whole_indices)
        for partial_index in range(fiber_count):
            if partial_index in whole_set:
                continue
            for partial_points in itertools.combinations(range(fiber_size), remainder_size):
                points: set[int] = set()
                for fiber in whole_set:
                    for point in range(fiber_size):
                        points.add(fiber * fiber_size + point)
                for point in partial_points:
                    points.add(partial_index * fiber_size + point)
                supports.append(frozenset(points))
    return supports


def brute_one_remainder_strict_profile(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    remainder_size: int,
    slack: int,
) -> Counter[int]:
    supports = one_remainder_supports(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
    )
    fixed = supports[0]
    return Counter(
        exchange
        for support in supports
        for exchange in [len(fixed - support)]
        if 0 < exchange < slack
    )


def one_remainder_strict_formula(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    remainder_size: int,
    slack: int,
) -> Counter[int]:
    if slack > fiber_size:
        raise AssertionError((fiber_size, slack, "formula assumes slack <= fiber size"))
    profile: Counter[int] = Counter()
    for exchange in range(1, min(remainder_size, fiber_size - remainder_size, slack - 1) + 1):
        profile[exchange] += comb(remainder_size, exchange) * comb(
            fiber_size - remainder_size,
            exchange,
        )
    if remainder_size < slack:
        profile[remainder_size] += (fiber_count - whole_fibers - 1) * comb(
            fiber_size,
            remainder_size,
        )
    complement_size = fiber_size - remainder_size
    if complement_size < slack:
        profile[complement_size] += whole_fibers * comb(
            fiber_size,
            remainder_size,
        )
    return +profile


def check_one_remainder_case(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    remainder_size: int,
    slack: int,
) -> None:
    brute = brute_one_remainder_strict_profile(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
        slack,
    )
    formula = one_remainder_strict_formula(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
        slack,
    )
    if brute != formula:
        raise AssertionError(
            (fiber_count, fiber_size, whole_fibers, remainder_size, slack, brute, formula)
        )
    if 1 <= remainder_size < slack and fiber_size >= slack + remainder_size:
        expected_mass = (
            (fiber_count - whole_fibers) * comb(fiber_size, remainder_size)
            - 1
        )
        if sum(formula.values()) != expected_mass:
            raise AssertionError(
                (
                    fiber_count,
                    fiber_size,
                    whole_fibers,
                    remainder_size,
                    slack,
                    sum(formula.values()),
                    expected_mass,
                )
            )
    complement_size = fiber_size - remainder_size
    if 1 <= complement_size < slack and fiber_size >= slack + complement_size:
        expected_mass = (
            (whole_fibers + 1) * comb(fiber_size, complement_size)
            - 1
        )
        if sum(formula.values()) != expected_mass:
            raise AssertionError(
                (
                    fiber_count,
                    fiber_size,
                    whole_fibers,
                    remainder_size,
                    slack,
                    sum(formula.values()),
                    expected_mass,
                )
            )


def weighted_profile(profile: Counter[int], slack: int, field_size: int) -> int:
    return sum(
        coefficient * (field_size ** (slack - exchange))
        for exchange, coefficient in profile.items()
    )


def stable_tail_formula(
    domain_size: int,
    exact_dimension: int,
    dither: int,
    slack: int,
    fiber_size: int,
    field_size: int,
) -> tuple[Counter[int], int]:
    gap = abs(slack - dither)
    if not (1 <= gap < slack):
        raise AssertionError((domain_size, exact_dimension, dither, slack, gap))
    if exact_dimension % fiber_size or domain_size % fiber_size:
        raise AssertionError((domain_size, exact_dimension, fiber_size))
    if fiber_size < slack + gap:
        raise AssertionError((fiber_size, slack, gap, "unstable scale"))

    if slack > dither:
        coefficient_blocks = (domain_size - exact_dimension) // fiber_size - 1
    else:
        coefficient_blocks = exact_dimension // fiber_size - 1

    profile: Counter[int] = Counter()
    for exchange in range(1, gap + 1):
        profile[exchange] += comb(gap, exchange) * comb(
            fiber_size - gap,
            exchange,
        )
    profile[gap] += coefficient_blocks * comb(fiber_size, gap)
    return +profile, weighted_profile(profile, slack, field_size)


def dyadic_divisors(value: int) -> list[int]:
    divisors: list[int] = []
    scale = 2
    while scale <= value and value % scale == 0:
        divisors.append(scale)
        scale *= 2
    return divisors


def v2(value: int) -> int:
    exponent = 0
    while value and value % 2 == 0:
        exponent += 1
        value //= 2
    return exponent


def floor_log2(value: int) -> int:
    if value <= 0:
        raise AssertionError(value)
    return value.bit_length() - 1


def check_stable_tail_case(
    domain_size: int,
    exact_dimension: int,
    dither: int,
    slack: int,
    fiber_size: int,
    field_size: int,
) -> None:
    profile, weighted = stable_tail_formula(
        domain_size,
        exact_dimension,
        dither,
        slack,
        fiber_size,
        field_size,
    )
    if slack > dither:
        remainder_size = slack - dither
        whole_fibers = exact_dimension // fiber_size
    else:
        remainder_size = fiber_size - (dither - slack)
        whole_fibers = exact_dimension // fiber_size - 1
    fiber_count = domain_size // fiber_size
    brute = brute_one_remainder_strict_profile(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
        slack,
    )
    if profile != brute:
        raise AssertionError(
            (domain_size, exact_dimension, dither, slack, fiber_size, profile, brute)
        )
    if weighted != weighted_profile(brute, slack, field_size):
        raise AssertionError((profile, weighted, weighted_profile(brute, slack, field_size)))


def check_dyadic_prefix_case(
    exact_dimension: int,
    slack: int,
    gap: int,
) -> None:
    prefix = [
        scale
        for scale in dyadic_divisors(exact_dimension)
        if scale < slack + gap
    ]
    expected_count = min(v2(exact_dimension), floor_log2(slack + gap - 1))
    if len(prefix) != expected_count:
        raise AssertionError((exact_dimension, slack, gap, prefix, expected_count))


def main() -> int:
    for case in [
        (4, 2, 3),
        (4, 2, 4),
        (5, 3, 5),
        (6, 2, 5),
    ]:
        check_occupancy_case(*case)
    for case in [
        (5, 2, 2, 3, 7),
        (5, 2, 2, 5, 7),
        (6, 3, 2, 4, 5),
        (6, 2, 3, 5, 11),
    ]:
        check_exchange_case(*case)
    for case in [
        (3, (1, 2, 0), (2, 1, 0)),
        (3, (1, 1, 2), (2, 0, 2)),
        (2, (1, 0, 2, 1), (0, 1, 2, 1)),
        (4, (0, 2, 3), (1, 1, 3)),
        (4, (1, 2, 0), (1, 2, 0)),
    ]:
        check_exchange_kernel_case(*case)
    for case in [
        (4, 3, 4),
        (4, 3, 6),
        (5, 4, 6),
        (5, 4, 8),
        (6, 2, 5),
    ]:
        check_exchange_one_floor_case(*case)
    for case in [
        (5, 4, 2, 1, 3),
        (6, 5, 2, 2, 3),
        (6, 5, 2, 2, 4),
        (5, 3, 1, 1, 3),
        (6, 5, 2, 4, 3),
        (7, 6, 3, 4, 4),
        (7, 6, 2, 5, 3),
    ]:
        check_one_remainder_case(*case)
    for case in [
        (64, 32, 4, 5, 8, 7),
        (64, 32, 6, 5, 8, 7),
        (96, 48, 5, 7, 12, 11),
        (128, 32, 6, 8, 16, 13),
        (128, 64, 10, 7, 16, 13),
    ]:
        check_stable_tail_case(*case)
    for case in [
        (32, 5, 1),
        (32, 5, 2),
        (64, 8, 3),
        (128, 13, 4),
        (256, 17, 1),
    ]:
        check_dyadic_prefix_case(*case)
    print("M1 quotient occupancy theorem verifier passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
