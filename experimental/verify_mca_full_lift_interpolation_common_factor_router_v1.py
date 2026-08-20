#!/usr/bin/env python3
"""Verify the M31 interpolation common-factor router constants."""

from __future__ import annotations

import copy
from fractions import Fraction


N, M, C, BUDGET = 1048582, 67454, 5, 16777215


class Reject(ValueError):
    pass


def monomial_count(degree: int, weight: int) -> int:
    return sum((level + 1) * (degree - weight * level + 1)
               for level in range(degree // weight + 1))


def compute() -> dict[str, int]:
    e, cutoff, layer, size = 130237, 65521, 65522, 2
    lower = size * layer - e
    cap, lines = e + 9 - 65450, 2704
    core_budget = min(lines * cap, e + lines * (lines + 1) * C // 2)
    lower_sum = lines * lower
    full, remainder = divmod(core_budget - lower_sum, cap - lower)
    value = full * Fraction(N - cap, M - cap)
    value += Fraction(N - lower - remainder, M - lower - remainder)
    value += (lines - full - 1) * Fraction(N - lower, M - lower)
    charge = value.numerator // value.denominator
    target = BUDGET - charge
    base, groups = 13961576, 1933560
    threshold = (target - base + groups) // groups
    degree, weight = 264, 5
    monomials = monomial_count(degree, weight)
    value_degree = degree // weight
    return {
        "e": e, "cutoff": cutoff, "minimum_layer": layer,
        "minimum_line_size": size, "inside_core_lower": lower,
        "actual_core_cap": cap, "removed_before_forcing": lines,
        "forced_distinct_lines": lines + 1, "core_budget": core_budget,
        "lower_sum": lower_sum, "full_caps": full,
        "remainder": remainder, "charge": charge, "target": target,
        "base": base, "groups": groups, "next_threshold": threshold,
        "weighted_degree": degree, "monomials": monomials,
        "kernel_dimension_lower": monomials - e,
        "value_total_degree": value_degree,
        "bezout_cap": value_degree**2, "root_count": lower,
    }


EXPECTED = {
    "e": 130237, "cutoff": 65521, "minimum_layer": 65522,
    "minimum_line_size": 2, "inside_core_lower": 807,
    "actual_core_cap": 64796, "removed_before_forcing": 2704,
    "forced_distinct_lines": 2705, "core_budget": 18416037,
    "lower_sum": 2182128, "full_caps": 253, "remainder": 44692,
    "charge": 132203, "target": 16645012, "base": 13961576,
    "groups": 1933560, "next_threshold": 2, "weighted_degree": 264,
    "monomials": 131175, "kernel_dimension_lower": 938,
    "value_total_degree": 52, "bezout_cap": 2704, "root_count": 807,
}


def validate(expected: dict[str, int]) -> int:
    actual = compute()
    if actual != expected:
        wrong = sorted(key for key in actual if actual[key] != expected.get(key))
        raise Reject(f"constants {wrong}")
    if actual["root_count"] <= actual["weighted_degree"]:
        raise Reject("root-degree gap")
    if actual["forced_distinct_lines"] <= actual["bezout_cap"]:
        raise Reject("Bezout contradiction")
    if actual["next_threshold"] < 2:
        raise Reject("line forcing")
    return len(actual) + 7


def main() -> None:
    checks = validate(EXPECTED)
    mutations = []
    for key, delta in (
            ("inside_core_lower", -1), ("charge", 1),
            ("monomials", -1), ("bezout_cap", 1)):
        mutant = copy.deepcopy(EXPECTED)
        mutant[key] += delta
        try:
            validate(mutant)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise Reject("mutations")
    print("MCA_FULL_LIFT_INTERPOLATION_COMMON_FACTOR_ROUTER_V1_PASS "
          f"checks={checks} mutations={sum(mutations)}/{len(mutations)} "
          "kernel>=938 coprime_cap=2704 forced=2705")


if __name__ == "__main__":
    main()
