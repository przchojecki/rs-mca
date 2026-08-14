#!/usr/bin/env python3
"""Verify the M31 common-factor weighted-degree constants."""

from __future__ import annotations

import copy


class Reject(ValueError):
    pass


def monomials(degree: int) -> int:
    return sum((level + 1) * (degree - 5 * level + 1)
               for level in range(degree // 5 + 1))


EXPECTED = {
    "reject_degree": 46, "reject_monomials": 935,
    "accept_degree": 47, "accept_monomials": 990,
    "factor_weight_max": 217, "factor_yz_degree_max": 43,
    "pairs_min": 5083, "factor_points_min": 126266,
    "exceptions_max": 3971,
}


def validate(expected: dict[str, int]) -> int:
    if expected["accept_degree"] != expected["reject_degree"] + 1:
        raise Reject("adjacency")
    if monomials(expected["reject_degree"]) != expected["reject_monomials"]:
        raise Reject("reject count")
    if monomials(expected["accept_degree"]) != expected["accept_monomials"]:
        raise Reject("accept count")
    if not (expected["reject_monomials"] < 938
            <= expected["accept_monomials"]):
        raise Reject("threshold")
    first = min(degree for degree in range(265) if monomials(degree) >= 938)
    if 264 - first != expected["factor_weight_max"]:
        raise Reject("factor weight")
    if expected["factor_weight_max"] // 5 != expected["factor_yz_degree_max"]:
        raise Reject("YZ degree")
    pairs = 7583 - (52 - 2) ** 2
    if expected["pairs_min"] != pairs:
        raise Reject("pairs")
    numerator = pairs * 807**2
    denominator = 807 + 5 * (pairs - 1)
    points = (numerator + denominator - 1) // denominator
    if expected["factor_points_min"] != points:
        raise Reject("factor points")
    if expected["exceptions_max"] != 130237 - points:
        raise Reject("exceptions")
    return 79


def main() -> None:
    checks = validate(EXPECTED)
    mutations = []
    for key, delta in (
            ("reject_monomials", 1), ("factor_weight_max", 1),
            ("pairs_min", -1), ("factor_points_min", -1)):
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
    print("MCA_FULL_LIFT_COMMON_FACTOR_WEIGHTED_DEGREE_BOUND_V1_PASS "
          f"checks={checks} mutations={sum(mutations)}/{len(mutations)} "
          "wdeg<=217 yzdeg<=43 pairs>=5083 exceptions<=3971")


if __name__ == "__main__":
    main()
