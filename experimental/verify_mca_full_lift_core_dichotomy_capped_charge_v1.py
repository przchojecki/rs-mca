#!/usr/bin/env python3
"""Verify the M31 high-core/low-core capped-charge dichotomy."""

from __future__ import annotations

import copy
from fractions import Fraction


R, D, K = 1048576, 67448, 6
N, M, C = R + K, D + K, K - 1
BUDGET, LINE, ABS_CUTOFF = 16777215, N - M + 1, 65450


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


def bank(e: int) -> tuple[int, int, int, int]:
    cutoff = choose_cutoff(e)
    weighted_prefix = prefix(e, cutoff)
    groups = 0
    for h in range(cutoff + 1, M + 1):
        overlap = 2 * h - e
        denominator = overlap * overlap - e * C
        if 2 * h <= e or overlap <= C or denominator <= 0:
            raise Reject("bank guard")
        groups += e * (overlap - C) // denominator
    return cutoff, weighted_prefix, groups, weighted_prefix + M - cutoff - groups


def runs(values: list[int]) -> list[list[int]]:
    answer: list[list[int]] = []
    for value in values:
        if answer and answer[-1][0] == value:
            answer[-1][1] += 1
        else:
            answer.append([value, 1])
    return answer


def capped_charge(e: int, lower: list[int], cap: int) -> tuple[int, int, list[list[int]]]:
    count = len(lower)
    if count == 0:
        return 0, 0, []
    budget = min(count * cap, e + count * (count + 1) * C // 2)
    allocation = sorted(lower, reverse=True)
    excess = budget - sum(allocation)
    if excess < 0:
        raise Reject("lower bounds")
    for index, value in enumerate(allocation):
        addition = min(excess, cap - value)
        allocation[index] += addition
        excess -= addition
        if excess == 0:
            break
    if excess:
        raise Reject("allocation")
    rational = sum((Fraction(N - value, M - value)
                    for value in allocation), Fraction())
    return rational.numerator // rational.denominator, budget, runs(allocation)


def zero_charge(e: int, lines: int, cap: int) -> tuple[int, int, int, int]:
    if lines == 0:
        return 0, 0, 0, 0
    budget = min(lines * cap, e + lines * (lines + 1) * C // 2)
    full, remainder = divmod(budget, cap)
    if full == lines:
        rational = lines * Fraction(N - cap, M - cap)
    else:
        rational = full * Fraction(N - cap, M - cap)
        rational += Fraction(N - remainder, M - remainder)
        rational += (lines - full - 1) * Fraction(N, M)
    return rational.numerator // rational.denominator, budget, full, remainder


def paid(e: int) -> dict[str, object]:
    cap = e + 9 - ABS_CUTOFF
    absorb = prefix(e, ABS_CUTOFF)
    cutoff, weighted, groups, base = bank(e)
    thresholds: list[int] = []
    cores: list[int] = []
    insides: list[int] = []
    for removed in range(256):
        charge, budget, allocation = capped_charge(e, cores, cap)
        target = BUDGET - charge
        threshold = (target - base + 1 + groups - 1) // groups
        if threshold < 2:
            raise Reject("wall")
        numerator = threshold * M - N
        core = (0 if numerator <= 0 else
                (numerator + threshold - 2) // (threshold - 1))
        inside = max(core - C, 0)
        thresholds.append(threshold)
        cores.append(core)
        insides.append(inside)
        packing = sum(insides) - len(insides) * (len(insides) - 1) * C // 2
        if packing > e:
            return {
                "e": e, "core_cap": cap, "absorption_prefix": absorb,
                "absorption_bound": absorb + LINE, "cutoff": cutoff,
                "prefix": weighted, "groups": groups, "base": base,
                "certificate": "core_packing", "lines": removed + 1,
                "target": target, "charge": charge, "core_budget": budget,
                "allocation_runs": allocation,
                "threshold_runs": runs(thresholds),
                "core_runs": runs(cores), "inside_runs": runs(insides),
                "packing": packing,
            }
    raise Reject("limit")


def wall(e: int) -> dict[str, object]:
    cap = e + 9 - ABS_CUTOFF
    absorb = prefix(e, ABS_CUTOFF)
    cutoff, weighted, groups, base = bank(e)
    first = (BUDGET - base + 1 + groups - 1) // groups
    if first * M - N > 0:
        raise Reject("positive first core")
    for lines in range(20000):
        charge, budget, full, remainder = zero_charge(e, lines, cap)
        target = BUDGET - charge
        threshold = (target - base + 1 + groups - 1) // groups
        if threshold < 2:
            return {
                "e": e, "core_cap": cap, "absorption_prefix": absorb,
                "absorption_bound": absorb + LINE, "cutoff": cutoff,
                "prefix": weighted, "groups": groups, "base": base,
                "certificate": "threshold_one_wall", "lines": lines,
                "target": target, "charge": charge, "core_budget": budget,
                "full_caps": full, "remainder": remainder,
                "first_threshold": first, "next_threshold": threshold,
                "packing": 0,
            }
        if threshold > first:
            raise Reject("monotonicity")
    raise Reject("limit")


EXPECTED = {
    "e130222": {"e": 130222, "core_cap": 64781, "absorption_prefix": 4180178, "absorption_bound": 5161307, "cutoff": 65516, "prefix": 12406922, "groups": 260580, "base": 12148280, "certificate": "core_packing", "lines": 14, "target": 16776980, "charge": 235, "core_budget": 130677, "allocation_runs": [[13785, 1], [9741, 12]], "threshold_runs": [[18, 14]], "core_runs": [[9741, 14]], "inside_runs": [[9736, 14]], "packing": 135849},
    "e130223": {"e": 130223, "core_cap": 64782, "absorption_prefix": 4180156, "absorption_bound": 5161285, "cutoff": 65516, "prefix": 12406366, "groups": 269480, "base": 12138824, "certificate": "core_packing", "lines": 14, "target": 16776980, "charge": 235, "core_budget": 130678, "allocation_runs": [[13786, 1], [9741, 12]], "threshold_runs": [[18, 14]], "core_runs": [[9741, 14]], "inside_runs": [[9736, 14]], "packing": 135849},
    "e130224": {"e": 130224, "core_cap": 64783, "absorption_prefix": 4180145, "absorption_bound": 5161274, "cutoff": 65517, "prefix": 12961350, "groups": 260602, "base": 12702685, "certificate": "core_packing", "lines": 70, "target": 16776111, "charge": 1104, "core_budget": 142299, "allocation_runs": [[3171, 1], [2046, 68]], "threshold_runs": [[16, 70]], "core_runs": [[2046, 70]], "inside_runs": [[2041, 70]], "packing": 130795},
    "e130225": {"e": 130225, "core_cap": 64784, "absorption_prefix": 4180124, "absorption_bound": 5161253, "cutoff": 65517, "prefix": 12960735, "groups": 269520, "base": 12693152, "certificate": "core_packing", "lines": 70, "target": 16776111, "charge": 1104, "core_budget": 142300, "allocation_runs": [[3172, 1], [2046, 68]], "threshold_runs": [[16, 70]], "core_runs": [[2046, 70]], "inside_runs": [[2041, 70]], "packing": 130795},
    "adjacent": {"e": 130226, "core_cap": 64785, "absorption_prefix": 4180114, "absorption_bound": 5161243, "cutoff": 65518, "prefix": 13575970, "groups": 260627, "base": 13317279, "certificate": "threshold_one_wall", "lines": 14763, "target": 13577673, "charge": 3199542, "core_budget": 545032556, "full_caps": 8412, "remainder": 61136, "first_threshold": 14, "next_threshold": 1, "packing": 0},
}


def validate(expected: dict[str, object]) -> int:
    checks = 29
    for e in range(130222, 130226):
        if paid(e) != expected[f"e{e}"]:
            raise Reject(str(e))
        checks += 21
    if wall(130226) != expected["adjacent"]:
        raise Reject("adjacent")
    return checks + 21


def main() -> None:
    checks = validate(copy.deepcopy(EXPECTED))
    mutations = []
    for name, key, delta in (
            ("e130222", "packing", -1),
            ("e130225", "charge", 1),
            ("adjacent", "target", -1),
            ("adjacent", "full_caps", 1)):
        changed = copy.deepcopy(EXPECTED)
        changed[name][key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise Reject("mutations")
    print("MCA_FULL_LIFT_CORE_DICHOTOMY_CAPPED_CHARGE_V1_PASS "
          f"checks={checks} mutations={sum(mutations)}/{len(mutations)} "
          "paid=130222..130225 wall=130226")


if __name__ == "__main__":
    main()
