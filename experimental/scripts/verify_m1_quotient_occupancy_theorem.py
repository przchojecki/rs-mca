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
    print("M1 quotient occupancy theorem verifier passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
