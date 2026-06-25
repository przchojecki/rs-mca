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


def multiply_bivariate(
    left: Counter[tuple[int, int]],
    right: Counter[tuple[int, int]],
) -> Counter[tuple[int, int]]:
    product: Counter[tuple[int, int]] = Counter()
    for (left_balance, left_distance), left_coeff in left.items():
        for (right_balance, right_distance), right_coeff in right.items():
            product[
                (
                    left_balance + right_balance,
                    left_distance + right_distance,
                )
            ] += left_coeff * right_coeff
    return product


def multiply_trivariate(
    left: Counter[tuple[int, int, int]],
    right: Counter[tuple[int, int, int]],
) -> Counter[tuple[int, int, int]]:
    product: Counter[tuple[int, int, int]] = Counter()
    for (left_balance, left_distance, left_exchange), left_coeff in left.items():
        for (right_balance, right_distance, right_exchange), right_coeff in right.items():
            product[
                (
                    left_balance + right_balance,
                    left_distance + right_distance,
                    left_exchange + right_exchange,
                )
            ] += left_coeff * right_coeff
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


def occupancy_exchange_distance(
    source_occupancy: tuple[int, ...],
    target_occupancy: tuple[int, ...],
) -> int:
    return sum(
        max(0, source - target)
        for source, target in zip(source_occupancy, target_occupancy)
    )


def leading_min_exchange_coefficient(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
    target_occupancy: tuple[int, ...],
) -> int:
    coefficient = 1
    for source, target in zip(source_occupancy, target_occupancy):
        if source >= target:
            coefficient *= comb(source, target)
        else:
            coefficient *= comb(fiber_size - source, target - source)
    return coefficient


def check_minimum_exchange_case(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
    target_occupancy: tuple[int, ...],
    slack: int,
) -> None:
    formula = exchange_kernel_formula(fiber_size, source_occupancy, target_occupancy)
    brute = brute_exchange_kernel(fiber_size, source_occupancy, target_occupancy)
    if formula != brute:
        raise AssertionError((fiber_size, source_occupancy, target_occupancy, formula, brute))

    expected_minimum = occupancy_exchange_distance(source_occupancy, target_occupancy)
    actual_minimum = min(formula)
    if actual_minimum != expected_minimum:
        raise AssertionError(
            (fiber_size, source_occupancy, target_occupancy, actual_minimum, expected_minimum)
        )

    expected_leading = leading_min_exchange_coefficient(
        fiber_size,
        source_occupancy,
        target_occupancy,
    )
    if formula[expected_minimum] != expected_leading:
        raise AssertionError(
            (
                fiber_size,
                source_occupancy,
                target_occupancy,
                formula[expected_minimum],
                expected_leading,
            )
        )

    if source_occupancy != target_occupancy and expected_minimum >= slack:
        strict_mass = sum(
            coefficient
            for exchange, coefficient in formula.items()
            if 0 < exchange < slack
        )
        if strict_mass:
            raise AssertionError(
                (fiber_size, source_occupancy, target_occupancy, slack, strict_mass)
            )


def check_minimum_exchange_all_case(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> None:
    vectors = occupancy_vectors(fiber_count, fiber_size, support_size)
    for source_occupancy in vectors:
        for target_occupancy in vectors:
            check_minimum_exchange_case(
                fiber_size,
                source_occupancy,
                target_occupancy,
                slack,
            )


def profile_neighbor_counts_formula(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
) -> Counter[int]:
    kernel: Counter[tuple[int, int]] = Counter({(0, 0): 1})
    for source in source_occupancy:
        fiber_kernel: Counter[tuple[int, int]] = Counter()
        for target in range(fiber_size + 1):
            if target <= source:
                deficit = source - target
                fiber_kernel[(-deficit, deficit)] += 1
            else:
                surplus = target - source
                fiber_kernel[(surplus, 0)] += 1
        kernel = multiply_bivariate(kernel, fiber_kernel)
    return +Counter(
        {
            distance: coefficient
            for (balance, distance), coefficient in kernel.items()
            if balance == 0
        }
    )


def profile_neighbor_counts_brute(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
    source_occupancy: tuple[int, ...],
) -> Counter[int]:
    counts: Counter[int] = Counter()
    for target_occupancy in occupancy_vectors(fiber_count, fiber_size, support_size):
        counts[occupancy_exchange_distance(source_occupancy, target_occupancy)] += 1
    return counts


def profile_neighborhood_bound(fiber_count: int, distance: int) -> int:
    return comb(fiber_count + distance - 1, distance) ** 2


def check_profile_neighborhood_case(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> None:
    vectors = occupancy_vectors(fiber_count, fiber_size, support_size)
    degree_bound = sum(
        profile_neighborhood_bound(fiber_count, distance)
        for distance in range(1, slack)
    )
    for source_occupancy in vectors:
        formula = profile_neighbor_counts_formula(fiber_size, source_occupancy)
        brute = profile_neighbor_counts_brute(
            fiber_count,
            fiber_size,
            support_size,
            source_occupancy,
        )
        if formula != brute:
            raise AssertionError(
                (fiber_count, fiber_size, support_size, source_occupancy, formula, brute)
            )
        if formula.get(0, 0) != 1:
            raise AssertionError((fiber_count, fiber_size, support_size, source_occupancy))
        for distance, count in formula.items():
            bound = profile_neighborhood_bound(fiber_count, distance)
            if count > bound:
                raise AssertionError(
                    (
                        fiber_count,
                        fiber_size,
                        support_size,
                        source_occupancy,
                        distance,
                        count,
                        bound,
                    )
                )
        strict_neighbors = sum(
            count
            for distance, count in formula.items()
            if 0 < distance < slack
        )
        if strict_neighbors > degree_bound:
            raise AssertionError(
                (
                    fiber_count,
                    fiber_size,
                    support_size,
                    source_occupancy,
                    strict_neighbors,
                    degree_bound,
                )
            )


def mixed_profile_exchange_kernel_formula(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
) -> Counter[tuple[int, int]]:
    kernel: Counter[tuple[int, int, int]] = Counter({(0, 0, 0): 1})
    for source in source_occupancy:
        fiber_kernel: Counter[tuple[int, int, int]] = Counter()
        for target in range(fiber_size + 1):
            lower = max(0, source + target - fiber_size)
            upper = min(source, target)
            for intersection in range(lower, upper + 1):
                balance = target - source
                profile_distance = max(0, source - target)
                exchange = source - intersection
                fiber_kernel[(balance, profile_distance, exchange)] += comb(
                    source,
                    intersection,
                ) * comb(fiber_size - source, target - intersection)
        kernel = multiply_trivariate(kernel, fiber_kernel)

    out: Counter[tuple[int, int]] = Counter()
    for (balance, profile_distance, exchange), coefficient in kernel.items():
        if balance == 0:
            out[(profile_distance, exchange)] += coefficient
    return +out


def occupancy_vector_from_support(
    fiber_count: int,
    fiber_size: int,
    support: frozenset[int],
) -> tuple[int, ...]:
    occupancy = [0] * fiber_count
    for point in support:
        occupancy[point // fiber_size] += 1
    return tuple(occupancy)


def brute_mixed_profile_exchange_kernel(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
    source_occupancy: tuple[int, ...],
) -> Counter[tuple[int, int]]:
    points = range(fiber_count * fiber_size)
    source = canonical_support(fiber_size, source_occupancy)
    counts: Counter[tuple[int, int]] = Counter()
    for target_tuple in itertools.combinations(points, support_size):
        target = frozenset(target_tuple)
        target_occupancy = occupancy_vector_from_support(
            fiber_count,
            fiber_size,
            target,
        )
        profile_distance = occupancy_exchange_distance(source_occupancy, target_occupancy)
        exchange = len(source - target)
        counts[(profile_distance, exchange)] += 1
    return counts


def check_mixed_profile_exchange_case(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
    slack: int,
) -> None:
    vectors = occupancy_vectors(fiber_count, fiber_size, support_size)
    domain_size = fiber_count * fiber_size
    for source_occupancy in vectors:
        formula = mixed_profile_exchange_kernel_formula(fiber_size, source_occupancy)
        brute = brute_mixed_profile_exchange_kernel(
            fiber_count,
            fiber_size,
            support_size,
            source_occupancy,
        )
        if formula != brute:
            raise AssertionError(
                (fiber_count, fiber_size, support_size, source_occupancy, formula, brute)
            )
        by_exchange: Counter[int] = Counter()
        for (profile_distance, exchange), count in formula.items():
            if profile_distance > exchange:
                raise AssertionError(
                    (
                        fiber_count,
                        fiber_size,
                        support_size,
                        source_occupancy,
                        profile_distance,
                        exchange,
                    )
                )
            if profile_distance >= slack and 0 < exchange < slack:
                raise AssertionError(
                    (
                        fiber_count,
                        fiber_size,
                        support_size,
                        source_occupancy,
                        profile_distance,
                        exchange,
                    )
                )
            by_exchange[exchange] += count

        for exchange in range(min(support_size, domain_size - support_size) + 1):
            expected = comb(support_size, exchange) * comb(
                domain_size - support_size,
                exchange,
            )
            if by_exchange.get(exchange, 0) != expected:
                raise AssertionError(
                    (
                        fiber_count,
                        fiber_size,
                        support_size,
                        source_occupancy,
                        exchange,
                        by_exchange.get(exchange, 0),
                        expected,
                    )
                )


def one_fiber_internal_kernel(fiber_size: int, source: int) -> Counter[int]:
    return Counter(
        {
            exchange: comb(source, exchange) * comb(fiber_size - source, exchange)
            for exchange in range(min(source, fiber_size - source) + 1)
        }
    )


def one_fiber_deficit_one_kernel(fiber_size: int, source: int) -> Counter[int]:
    if source == 0:
        return Counter()
    return Counter(
        {
            exchange: comb(source, exchange) * comb(fiber_size - source, exchange - 1)
            for exchange in range(1, min(source, fiber_size - source + 1) + 1)
        }
    )


def one_fiber_surplus_one_kernel(fiber_size: int, source: int) -> Counter[int]:
    if source == fiber_size:
        return Counter()
    return Counter(
        {
            exchange: comb(source, exchange) * comb(fiber_size - source, exchange + 1)
            for exchange in range(min(source, fiber_size - source - 1) + 1)
        }
    )


def first_mixed_shell_formula(
    fiber_size: int,
    source_occupancy: tuple[int, ...],
) -> Counter[int]:
    total: Counter[int] = Counter()
    internal_kernels = [
        one_fiber_internal_kernel(fiber_size, source)
        for source in source_occupancy
    ]
    deficit_kernels = [
        one_fiber_deficit_one_kernel(fiber_size, source)
        for source in source_occupancy
    ]
    surplus_kernels = [
        one_fiber_surplus_one_kernel(fiber_size, source)
        for source in source_occupancy
    ]

    for deficit_index, deficit_kernel in enumerate(deficit_kernels):
        if not deficit_kernel:
            continue
        for surplus_index, surplus_kernel in enumerate(surplus_kernels):
            if deficit_index == surplus_index or not surplus_kernel:
                continue
            product = multiply_polynomials(deficit_kernel, surplus_kernel)
            for fiber_index, internal_kernel in enumerate(internal_kernels):
                if fiber_index in (deficit_index, surplus_index):
                    continue
                product = multiply_polynomials(product, internal_kernel)
            total.update(product)
    return +total


def check_first_mixed_shell_case(
    fiber_count: int,
    fiber_size: int,
    support_size: int,
) -> None:
    domain_size = fiber_count * fiber_size
    for source_occupancy in occupancy_vectors(fiber_count, fiber_size, support_size):
        first_shell = first_mixed_shell_formula(fiber_size, source_occupancy)
        general_kernel = mixed_profile_exchange_kernel_formula(fiber_size, source_occupancy)
        from_general = Counter(
            {
                exchange: count
                for (profile_distance, exchange), count in general_kernel.items()
                if profile_distance == 1
            }
        )
        if first_shell != from_general:
            raise AssertionError(
                (fiber_count, fiber_size, support_size, source_occupancy, first_shell, from_general)
            )

        internal_exchange = internal_exchange_one(source_occupancy, fiber_size)
        expected_exchange_one = support_size * (domain_size - support_size) - internal_exchange
        if first_shell.get(1, 0) != expected_exchange_one:
            raise AssertionError(
                (
                    fiber_count,
                    fiber_size,
                    support_size,
                    source_occupancy,
                    first_shell.get(1, 0),
                    expected_exchange_one,
                )
            )

        total_exchange_one = internal_exchange + first_shell.get(1, 0)
        if total_exchange_one != support_size * (domain_size - support_size):
            raise AssertionError(
                (
                    fiber_count,
                    fiber_size,
                    support_size,
                    source_occupancy,
                    total_exchange_one,
                )
            )


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


def one_remainder_family_size(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    remainder_size: int,
) -> int:
    return (
        comb(fiber_count, whole_fibers)
        * (fiber_count - whole_fibers)
        * comb(fiber_size, remainder_size)
    )


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
    family_size = one_remainder_family_size(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
    )
    brute_size = len(
        one_remainder_supports(
            fiber_count,
            fiber_size,
            whole_fibers,
            remainder_size,
        )
    )
    if brute_size != family_size:
        raise AssertionError(
            (fiber_count, fiber_size, whole_fibers, remainder_size, brute_size, family_size)
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


def one_remainder_variance_terms(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    remainder_size: int,
    slack: int,
    field_size: int,
) -> tuple[int, int]:
    family_size = one_remainder_family_size(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
    )
    correction = weighted_profile(
        one_remainder_strict_formula(
            fiber_count,
            fiber_size,
            whole_fibers,
            remainder_size,
            slack,
        ),
        slack,
        field_size,
    )
    return family_size, correction


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
    family_size, correction = one_remainder_variance_terms(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
        slack,
        field_size,
    )
    if correction != weighted:
        raise AssertionError((correction, weighted))
    expected_family_size = one_remainder_family_size(
        fiber_count,
        fiber_size,
        whole_fibers,
        remainder_size,
    )
    if family_size != expected_family_size:
        raise AssertionError((family_size, expected_family_size))


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


def maximal_dither_all_scale_formula(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    slack: int,
) -> Counter[int]:
    empty_after_remainder = fiber_count - whole_fibers - 1
    profile: Counter[int] = Counter()

    for exchange_fibers in range(0, whole_fibers + 1):
        exchange = exchange_fibers * fiber_size + 1
        if exchange < slack:
            coefficient = (
                comb(whole_fibers, exchange_fibers)
                * comb(empty_after_remainder, exchange_fibers)
                * (fiber_size * (empty_after_remainder - exchange_fibers + 1) - 1)
            )
            profile[exchange] += coefficient

    for exchange_fibers in range(1, whole_fibers + 1):
        exchange = exchange_fibers * fiber_size
        if exchange < slack:
            coefficient = (
                comb(whole_fibers, exchange_fibers)
                * comb(empty_after_remainder, exchange_fibers)
                * (1 + 2 * fiber_size * exchange_fibers)
            )
            profile[exchange] += coefficient

        exchange = exchange_fibers * fiber_size - 1
        if exchange < slack:
            coefficient = (
                fiber_size
                * exchange_fibers
                * comb(whole_fibers, exchange_fibers)
                * comb(empty_after_remainder, exchange_fibers - 1)
            )
            profile[exchange] += coefficient

    return +profile


def co_maximal_dither_all_scale_formula(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    slack: int,
) -> Counter[int]:
    return maximal_dither_all_scale_formula(
        fiber_count,
        fiber_size,
        fiber_count - whole_fibers - 1,
        slack,
    )


def check_maximal_all_scale_case(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    slack: int,
    field_size: int,
) -> None:
    formula = maximal_dither_all_scale_formula(
        fiber_count,
        fiber_size,
        whole_fibers,
        slack,
    )
    brute = brute_one_remainder_strict_profile(
        fiber_count,
        fiber_size,
        whole_fibers,
        1,
        slack,
    )
    if formula != brute:
        raise AssertionError((fiber_count, fiber_size, whole_fibers, slack, formula, brute))

    domain_size = fiber_count * fiber_size
    exact_dimension = whole_fibers * fiber_size
    correction = weighted_profile(formula, slack, field_size)
    if fiber_size > slack:
        expected = (domain_size - exact_dimension - 1) * field_size ** (slack - 1)
        if correction != expected:
            raise AssertionError((domain_size, exact_dimension, slack, fiber_size, correction, expected))
    if fiber_size == slack:
        expected = (
            (domain_size - exact_dimension - 1) * field_size ** (slack - 1)
            + exact_dimension * field_size
        )
        if correction != expected:
            raise AssertionError((domain_size, exact_dimension, slack, fiber_size, correction, expected))


def check_co_maximal_all_scale_case(
    fiber_count: int,
    fiber_size: int,
    whole_fibers: int,
    slack: int,
    field_size: int,
) -> None:
    formula = co_maximal_dither_all_scale_formula(
        fiber_count,
        fiber_size,
        whole_fibers,
        slack,
    )
    brute = brute_one_remainder_strict_profile(
        fiber_count,
        fiber_size,
        whole_fibers,
        fiber_size - 1,
        slack,
    )
    if formula != brute:
        raise AssertionError((fiber_count, fiber_size, whole_fibers, slack, formula, brute))

    exact_dimension = (whole_fibers + 1) * fiber_size
    domain_size = fiber_count * fiber_size
    correction = weighted_profile(formula, slack, field_size)
    if fiber_size > slack:
        expected = (exact_dimension - 1) * field_size ** (slack - 1)
        if correction != expected:
            raise AssertionError((domain_size, exact_dimension, slack, fiber_size, correction, expected))
    if fiber_size == slack:
        expected = (
            (exact_dimension - 1) * field_size ** (slack - 1)
            + (domain_size - exact_dimension) * field_size
        )
        if correction != expected:
            raise AssertionError((domain_size, exact_dimension, slack, fiber_size, correction, expected))


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
        (3, 3, 4, 2),
        (4, 2, 4, 2),
        (4, 3, 5, 3),
        (5, 2, 5, 3),
    ]:
        check_minimum_exchange_all_case(*case)
    for case in [
        (3, 3, 4, 2),
        (4, 2, 4, 3),
        (4, 3, 5, 3),
        (5, 2, 5, 4),
    ]:
        check_profile_neighborhood_case(*case)
    for case in [
        (3, 3, 4, 2),
        (4, 2, 4, 3),
        (4, 3, 5, 3),
        (5, 2, 5, 4),
    ]:
        check_mixed_profile_exchange_case(*case)
    for case in [
        (3, 3, 4),
        (4, 2, 4),
        (4, 3, 5),
        (5, 2, 5),
    ]:
        check_first_mixed_shell_case(*case)
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
    for case in [
        (5, 3, 2, 5, 7),
        (6, 4, 2, 4, 7),
        (6, 5, 2, 4, 11),
        (5, 6, 2, 4, 11),
    ]:
        check_maximal_all_scale_case(*case)
    for case in [
        (5, 3, 1, 5, 7),
        (6, 4, 2, 4, 7),
        (6, 5, 2, 4, 11),
        (5, 6, 1, 4, 11),
    ]:
        check_co_maximal_all_scale_case(*case)
    print("M1 quotient occupancy theorem verifier passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
