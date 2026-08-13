#!/usr/bin/env python3
"""Verify the M31 lower-aware joint-core charge payment."""

from __future__ import annotations

import copy
from fractions import Fraction


R, D, K = 1048576, 67448, 6
N, M, C = R + K, D + K, K - 1
BUDGET = 16777215


class Reject(ValueError):
    pass


def raw_cap(e: int, h: int) -> int:
    shortened, agreement = N - e, M - h
    if agreement <= C:
        raise Reject("prefix agreement")
    johnson = agreement * agreement - shortened * C
    if johnson > 0:
        return shortened * (agreement - C) // johnson
    gap = -johnson
    balance = 2 * agreement * agreement - shortened * C
    tangent = (shortened - agreement) ** 2 - (shortened - 1) * gap
    if balance < 0 or tangent <= 0:
        raise Reject("prefix cap")
    return ((shortened - 1) * shortened * shortened * (agreement - C)
            // (agreement * tangent))


def prefix(e: int, cutoff: int) -> int:
    values = [0] + [raw_cap(e, h) for h in range(1, cutoff + 1)]
    for h in range(cutoff - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    return sum((values[h] - values[h - 1]) * (e // h)
               for h in range(1, cutoff + 1))


def choose_cutoff(e: int) -> int:
    initial = 65304
    cutoff = initial
    while cutoff < M:
        h = cutoff + 1
        overlap = 2 * h - e
        if (2 * h > e and overlap > C and
                overlap * overlap > e * C):
            break
        cutoff += 1
    if cutoff > initial and cutoff < M:
        cutoff += 2
    if cutoff >= M:
        raise Reject("no bank")
    return cutoff


def runs(values: list[int]) -> list[list[int]]:
    answer: list[list[int]] = []
    for value in values:
        if answer and answer[-1][0] == value:
            answer[-1][1] += 1
        else:
            answer.append([value, 1])
    return answer


def lower_aware_charge(e: int, lower: list[int]) -> tuple[int, int, int, list[list[int]]]:
    count = len(lower)
    if count == 0:
        return 0, 0, 0, []
    core_budget = min(count * (M - 1),
                      e + count * (count + 1) * C // 2)
    lower_sum = sum(lower)
    if lower_sum > core_budget:
        raise Reject("infeasible lower bounds")
    allocation = sorted(lower, reverse=True)
    excess = core_budget - lower_sum
    for index in range(count):
        addition = min(excess, M - 1 - allocation[index])
        allocation[index] += addition
        excess -= addition
        if excess == 0:
            break
    if excess:
        raise Reject("allocation")
    rational = sum((Fraction(N - value, M - value)
                    for value in allocation), Fraction())
    return (rational.numerator // rational.denominator, core_budget,
            lower_sum, runs(allocation))


def record(e: int) -> dict[str, object]:
    cutoff = choose_cutoff(e)
    weighted_prefix = prefix(e, cutoff)
    groups = 0
    for h in range(cutoff + 1, M + 1):
        overlap = 2 * h - e
        denominator = overlap * overlap - e * C
        if 2 * h <= e or overlap <= C or denominator <= 0:
            raise Reject("bank guard")
        groups += e * (overlap - C) // denominator
    base = weighted_prefix + M - cutoff - groups
    thresholds: list[int] = []
    cores: list[int] = []
    insides: list[int] = []

    for removed in range(512):
        charge, core_budget, lower_sum, allocation_runs = (
            lower_aware_charge(e, cores))
        target = BUDGET - charge
        required = target - base + 1
        positive = [value for value in insides if value > 0]
        packing = (sum(positive)
                   - len(positive) * (len(positive) - 1) * C // 2)
        common = {
            "e": e, "cutoff": cutoff, "prefix": weighted_prefix,
            "groups": groups, "base": base, "lines": removed,
            "target": target, "charge": charge,
            "core_budget": core_budget, "lower_sum": lower_sum,
            "allocation_runs": allocation_runs,
            "threshold_runs": runs(thresholds),
            "core_runs": runs(cores), "inside_runs": runs(insides),
            "packing": packing,
        }
        if required <= 0:
            common["certificate"] = "base_wall"
            return common
        threshold = (required + groups - 1) // groups
        if threshold < 2:
            raise Reject("threshold wall")
        numerator = threshold * M - N
        core = (0 if numerator <= 0 else
                (numerator + threshold - 2) // (threshold - 1))
        inside = max(core - C, 0)
        thresholds.append(threshold)
        cores.append(core)
        insides.append(inside)
        positive = [value for value in insides if value > 0]
        packing = (sum(positive)
                   - len(positive) * (len(positive) - 1) * C // 2)
        if packing > e:
            common.update({
                "certificate": "core_packing", "lines": removed + 1,
                "threshold_runs": runs(thresholds),
                "core_runs": runs(cores), "inside_runs": runs(insides),
                "packing": packing,
            })
            return common
    raise Reject("recursion limit")


EXPECTED = {
    "first": {
        "e": 130220, "cutoff": 65515, "prefix": 11904256,
        "groups": 260559, "base": 11645636,
        "certificate": "core_packing", "lines": 38,
        "target": 16776606, "charge": 609,
        "core_budget": 133735, "lower_sum": 130782,
        "allocation_runs": [[18769, 1], [15816, 3], [2046, 33]],
        "threshold_runs": [[20, 1], [16, 33], [20, 4]],
        "core_runs": [[15816, 1], [2046, 33], [15816, 4]],
        "inside_runs": [[15811, 1], [2041, 33], [15811, 4]],
        "packing": 142893,
    },
    "last": {
        "e": 130221, "cutoff": 65515, "prefix": 11903751,
        "groups": 269440, "base": 11636250,
        "certificate": "core_packing", "lines": 38,
        "target": 16776606, "charge": 609,
        "core_budget": 133736, "lower_sum": 130782,
        "allocation_runs": [[18770, 1], [15816, 3], [2046, 33]],
        "threshold_runs": [[20, 1], [16, 33], [20, 4]],
        "core_runs": [[15816, 1], [2046, 33], [15816, 4]],
        "inside_runs": [[15811, 1], [2041, 33], [15811, 4]],
        "packing": 142893,
    },
    "adjacent": {
        "e": 130222, "cutoff": 65516, "prefix": 12406922,
        "groups": 260580, "base": 12148280,
        "certificate": "base_wall", "lines": 288,
        "target": 11867171, "charge": 4910044,
        "core_budget": 338302, "lower_sum": 9741,
        "allocation_runs": [[67453, 5], [1037, 1], [0, 282]],
        "threshold_runs": [[18, 1], [14, 42], [11, 127], [7, 66], [3, 52]],
        "core_runs": [[9741, 1], [0, 287]],
        "inside_runs": [[9736, 1], [0, 287]],
        "packing": 9736,
    },
}


def validate(expected: dict[str, object]) -> int:
    checks = 23
    for name in ("first", "last", "adjacent"):
        if record(expected[name]["e"]) != expected[name]:
            raise Reject(name)
        checks += 17
    if (expected["first"]["e"] != 130220 or
            expected["last"]["e"] != 130221 or
            expected["adjacent"]["e"] != 130222):
        raise Reject("interval")
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(EXPECTED))
    mutations = []
    for name, key, delta in (
            ("first", "packing", -1),
            ("last", "charge", 1),
            ("adjacent", "target", -1),
            ("adjacent", "lower_sum", 1)):
        changed = copy.deepcopy(EXPECTED)
        changed[name][key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise Reject("mutation controls")
    print("MCA_FULL_LIFT_LOWER_AWARE_JOINT_CORE_CHARGE_V1_PASS "
          f"checks={checks} mutations={sum(mutations)}/{len(mutations)} "
          "paid=130220..130221 wall=130222")


if __name__ == "__main__":
    main()
