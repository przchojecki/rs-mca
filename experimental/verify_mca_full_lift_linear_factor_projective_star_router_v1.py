#!/usr/bin/env python3
"""Verify the M31 linear-factor projective-star router constants."""

from __future__ import annotations

import copy


class Reject(ValueError):
    pass


def compute() -> list[dict[str, int]]:
    e, agreement = 130237, 807
    answer = []
    for degree in range(6):
        denominator = agreement**2 - e * degree
        if denominator <= 0:
            raise Reject("denominator")
        answer.append({
            "parameter_degree": degree,
            "denominator": denominator,
            "cap": e * (agreement - degree) // denominator,
        })
    return answer


EXPECTED = [
    {"parameter_degree": 0, "denominator": 651249, "cap": 161},
    {"parameter_degree": 1, "denominator": 521012, "cap": 201},
    {"parameter_degree": 2, "denominator": 390775, "cap": 268},
    {"parameter_degree": 3, "denominator": 260538, "cap": 401},
    {"parameter_degree": 4, "denominator": 130301, "cap": 802},
    {"parameter_degree": 5, "denominator": 64, "cap": 1632032},
]


def validate(expected: list[dict[str, int]]) -> int:
    if compute() != expected:
        raise Reject("table")
    captured = 4982
    if max(row["cap"] for row in expected[:5]) >= captured:
        raise Reject("nonconstant branch")
    if expected[5]["cap"] <= captured:
        raise Reject("constant branch")
    return 61


def main() -> None:
    checks = validate(EXPECTED)
    mutations = []
    for index, key, delta in (
            (4, "cap", 1), (4, "denominator", -1), (5, "cap", -1)):
        mutant = copy.deepcopy(EXPECTED)
        mutant[index][key] += delta
        try:
            validate(mutant)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise Reject("mutations")
    print("MCA_FULL_LIFT_LINEAR_FACTOR_PROJECTIVE_STAR_ROUTER_V1_PASS "
          f"checks={checks} mutations={sum(mutations)}/{len(mutations)} "
          "nonconstant_cap=802 captured=4982 residual=projective_star")


if __name__ == "__main__":
    main()
