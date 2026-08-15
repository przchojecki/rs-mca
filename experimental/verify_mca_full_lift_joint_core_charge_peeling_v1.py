#!/usr/bin/env python3
"""Verify endpoints of the M31 joint-core charge peeling payment."""

from __future__ import annotations

import copy
from fractions import Fraction


R, D, K = 1048576, 67448, 6
N, M, C = R + K, D + K, K - 1
BUDGET, LINE = 16777215, N - M + 1


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
    if not 1 <= cutoff <= M:
        raise Reject("cutoff")
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


def joint_charge(e: int, lines: int) -> tuple[int, int, int, int]:
    if lines == 0:
        return 0, 0, 0, 0
    core_budget = min(
        lines * (M - 1), e + lines * (lines + 1) * C // 2)
    full, remainder = divmod(core_budget, M - 1)
    full = min(full, lines)
    if full == lines:
        charge = lines * LINE
    else:
        left = lines - full
        rational = Fraction(full * LINE, 1)
        rational += Fraction(N - remainder, M - remainder)
        rational += (left - 1) * Fraction(N, M)
        charge = rational.numerator // rational.denominator
    return charge, core_budget, full, remainder


def runs(values: list[int]) -> list[list[int]]:
    answer: list[list[int]] = []
    for value in values:
        if answer and answer[-1][0] == value:
            answer[-1][1] += 1
        else:
            answer.append([value, 1])
    return answer


def record(e: int) -> dict[str, object]:
    cutoff = choose_cutoff(e)
    p = prefix(e, cutoff)
    groups = 0
    for h in range(cutoff + 1, M + 1):
        overlap = 2 * h - e
        denominator = overlap * overlap - e * C
        if 2 * h <= e or overlap <= C or denominator <= 0:
            raise Reject("bank guard")
        groups += e * (overlap - C) // denominator
    base = p + M - cutoff - groups
    thresholds: list[int] = []
    insides: list[int] = []

    for removed in range(256):
        charge, core_budget, full, remainder = joint_charge(e, removed)
        target = BUDGET - charge
        required = target - base + 1
        if required <= 0:
            return {
                "e": e, "cutoff": cutoff, "prefix": p,
                "groups": groups, "base": base,
                "certificate": "base_wall", "lines": removed,
                "target": target, "charge": charge,
                "core_budget": core_budget, "full": full,
                "remainder": remainder,
                "threshold_runs": runs(thresholds),
                "inside_runs": runs(insides),
            }
        threshold = (required + groups - 1) // groups
        if threshold < 2:
            raise Reject("threshold")
        numerator = threshold * M - N
        core = 0 if numerator <= 0 else (
            numerator + threshold - 2) // (threshold - 1)
        inside = max(core - C, 0)
        thresholds.append(threshold)
        insides.append(inside)
        positive = [value for value in insides if value > 0]
        packing = (sum(positive)
                   - len(positive) * (len(positive) - 1) * C // 2)
        if packing > e:
            return {
                "e": e, "cutoff": cutoff, "prefix": p,
                "groups": groups, "base": base,
                "certificate": "core_packing", "lines": removed + 1,
                "target": target, "charge": charge,
                "core_budget": core_budget, "full": full,
                "remainder": remainder, "packing": packing,
                "threshold_runs": runs(thresholds),
                "inside_runs": runs(insides),
            }
        if inside == 0:
            return {
                "e": e, "cutoff": cutoff, "prefix": p,
                "groups": groups, "base": base,
                "certificate": "zero_core_wall", "lines": removed + 1,
                "target": target, "charge": charge,
                "core_budget": core_budget, "full": full,
                "remainder": remainder, "packing": packing,
                "threshold_runs": runs(thresholds),
                "inside_runs": runs(insides),
            }
    raise Reject("recursion")



EXPECTED = {
    "first": {
        "e": 130199, "cutoff": 65504, "prefix": 8421151,
        "groups": 269019, "base": 8154082, "certificate": "core_packing",
        "lines": 4, "target": 15795860, "charge": 981355,
        "core_budget": 130229, "full": 1, "remainder": 62776,
        "packing": 133986, "threshold_runs": [[33, 1], [29, 3]],
        "inside_runs": [[36789, 1], [32409, 3]],
    },
    "last": {
        "e": 130219, "cutoff": 65514, "prefix": 11445963,
        "groups": 269400, "base": 11178503, "certificate": "core_packing",
        "lines": 13, "target": 15795702, "charge": 981513,
        "core_budget": 130609, "full": 1, "remainder": 63156,
        "packing": 134835, "threshold_runs": [[21, 1], [18, 12]],
        "inside_runs": [[18393, 1], [9736, 12]],
    },
    "adjacent": {
        "e": 130220, "cutoff": 65515, "prefix": 11904256,
        "groups": 260559, "base": 11645636,
        "certificate": "zero_core_wall", "lines": 44,
        "target": 14814320, "charge": 1962895,
        "core_budget": 134950, "full": 2, "remainder": 44,
        "packing": 97018,
        "threshold_runs": [[20, 1], [16, 42], [13, 1]],
        "inside_runs": [[15811, 1], [2041, 42], [0, 1]],
    },
    "line_counts": {4: 2, 5: 10, 6: 3, 7: 2, 8: 1, 10: 1, 13: 2},
    "paid": 21,
}


def validate(expected):
    checks = 31
    for name in ("first", "last", "adjacent"):
        if record(expected[name]["e"]) != expected[name]:
            raise Reject(name)
        checks += 14
    line_counts = {}
    paid = 0
    for e in range(expected["first"]["e"], expected["adjacent"]["e"]):
        got = record(e)
        if got["certificate"] != "core_packing":
            raise Reject("interval")
        line_counts[got["lines"]] = line_counts.get(got["lines"], 0) + 1
        paid += 1
        checks += 1
    if (paid != expected["paid"] or line_counts != expected["line_counts"] or
            expected["last"]["e"] - expected["first"]["e"] + 1 != paid or
            expected["adjacent"]["e"] != expected["last"]["e"] + 1):
        raise Reject("census")
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(EXPECTED))
    mutations = []
    for name, key, delta in (
            ("first", "packing", -1), ("last", "charge", 1),
            ("adjacent", "packing", 1), ("adjacent", "target", -1)):
        changed = copy.deepcopy(EXPECTED)
        changed[name][key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    changed = copy.deepcopy(EXPECTED)
    changed["paid"] += 1
    try:
        validate(changed)
    except Reject:
        mutations.append(True)
    else:
        mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_FULL_LIFT_JOINT_CORE_CHARGE_PEELING_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
