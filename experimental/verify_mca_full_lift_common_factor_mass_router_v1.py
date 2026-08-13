#!/usr/bin/env python3
"""Verify the M31 common-factor mass router constants."""

from __future__ import annotations

import copy
from fractions import Fraction


N, M, C, BUDGET = 1048582, 67454, 5, 16777215


class Reject(ValueError):
    pass


def compute() -> dict[str, int]:
    e, lines, lower, cap = 130237, 7582, 807, 64796
    core_budget = min(lines * cap, e + lines * (lines + 1) * C // 2)
    lower_sum = lines * lower
    full, remainder = divmod(core_budget - lower_sum, cap - lower)
    value = full * Fraction(N - cap, M - cap)
    value += Fraction(N - lower - remainder, M - lower - remainder)
    value += (lines - full - 1) * Fraction(N - lower, M - lower)
    charge = value.numerator // value.denominator
    target = BUDGET - charge
    threshold = (target - 13961576 + 1933560) // 1933560
    degree, factor_degree = 52, 1
    off = (degree - factor_degree) ** 2
    on = lines + 1 - off
    points = (on * lower * lower + lower + C * (on - 1) - 1) // (
        lower + C * (on - 1))
    return {
        "e": e, "removed_before_forcing": lines,
        "forced_distinct_lines": lines + 1, "inside_core_lower": lower,
        "actual_core_cap": cap, "core_budget": core_budget,
        "lower_sum": lower_sum, "full_caps": full,
        "remainder": remainder, "charge": charge, "target": target,
        "next_threshold": threshold, "ambient_value_degree": degree,
        "minimum_factor_degree": factor_degree,
        "maximum_off_factor_pairs": off,
        "minimum_on_factor_pairs": on,
        "minimum_factor_points": points,
        "maximum_exception_points": e - points,
    }


EXPECTED = {
    "e": 130237, "removed_before_forcing": 7582,
    "forced_distinct_lines": 7583, "inside_core_lower": 807,
    "actual_core_cap": 64796, "core_budget": 143866002,
    "lower_sum": 6118674, "full_caps": 2152, "remainder": 43000,
    "charge": 881897, "target": 15895318, "next_threshold": 2,
    "ambient_value_degree": 52, "minimum_factor_degree": 1,
    "maximum_off_factor_pairs": 2601, "minimum_on_factor_pairs": 4982,
    "minimum_factor_points": 126188, "maximum_exception_points": 4049,
}


def validate(expected: dict[str, int]) -> int:
    actual = compute()
    if actual != expected:
        wrong = sorted(key for key in actual if actual[key] != expected.get(key))
        raise Reject(f"constants {wrong}")
    if actual["next_threshold"] != 2:
        raise Reject("line forcing")
    if actual["minimum_factor_points"] + actual["maximum_exception_points"] != actual["e"]:
        raise Reject("support partition")
    return len(actual) + 9


def main() -> None:
    checks = validate(EXPECTED)
    mutations = []
    for key, delta in (
            ("charge", 1), ("maximum_off_factor_pairs", 1),
            ("minimum_on_factor_pairs", -1),
            ("minimum_factor_points", -1)):
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
    print("MCA_FULL_LIFT_COMMON_FACTOR_MASS_ROUTER_V1_PASS "
          f"checks={checks} mutations={sum(mutations)}/{len(mutations)} "
          "pairs>=4982 factor_points>=126188 exceptions<=4049")


if __name__ == "__main__":
    main()
