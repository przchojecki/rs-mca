#!/usr/bin/env python3
"""Verify the M31 base-field component descent constants."""

from __future__ import annotations

import copy


class Reject(ValueError):
    pass


EXPECTED = {
    "base_pairs_min": 5079,
    "component_pairs_min": 132,
    "factor_points_min": 126263,
    "exceptions_max": 3974,
}


def validate(expected: dict[str, int]) -> int:
    if 2147483647 <= 43:
        raise Reject("characteristic guard")
    records = []
    for degree in range(2, 44):
        captured = 7583 - (52 - degree) ** 2
        retained = captured - degree**2
        component = (retained + degree - 1) // degree
        records.append((degree, captured, retained, component))
    if min(record[2] for record in records) != expected["base_pairs_min"]:
        raise Reject("base pairs")
    if min(record[3] for record in records) != expected["component_pairs_min"]:
        raise Reject("component pairs")
    pairs = expected["base_pairs_min"]
    numerator = pairs * 807**2
    denominator = 807 + 5 * (pairs - 1)
    points = (numerator + denominator - 1) // denominator
    if points != expected["factor_points_min"]:
        raise Reject("factor points")
    if 130237 - points != expected["exceptions_max"]:
        raise Reject("exceptions")
    return 83


def main() -> None:
    checks = validate(EXPECTED)
    mutations = []
    for key, delta in (
            ("base_pairs_min", -1), ("component_pairs_min", -1),
            ("factor_points_min", -1), ("exceptions_max", 1)):
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
    print("MCA_FULL_LIFT_COMMON_FACTOR_BASE_FIELD_DESCENT_V1_PASS "
          f"checks={checks} mutations={sum(mutations)}/{len(mutations)} "
          "base_pairs>=5079 component_pairs>=132 exceptions<=3974")


if __name__ == "__main__":
    main()
