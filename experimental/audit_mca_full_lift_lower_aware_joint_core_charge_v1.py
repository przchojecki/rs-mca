#!/usr/bin/env python3
"""Independent ledger audit for the M31 lower-aware line charge."""

from __future__ import annotations

from fractions import Fraction


N, M, C, BUDGET = 1048582, 67454, 5, 16777215


def charge(e: int, lower: list[int]) -> tuple[int, list[int], int]:
    count = len(lower)
    budget = min(count * (M - 1), e + count * (count + 1) * C // 2)
    values = sorted(lower, reverse=True)
    excess = budget - sum(values)
    assert excess >= 0
    for index, value in enumerate(values):
        addition = min(excess, M - 1 - value)
        values[index] += addition
        excess -= addition
        if excess == 0:
            break
    assert excess == 0
    total = sum((Fraction(N - value, M - value) for value in values),
                Fraction())
    return total.numerator // total.denominator, values, budget


def core(threshold: int) -> tuple[int, int]:
    numerator = threshold * M - N
    total = (0 if numerator <= 0 else
             (numerator + threshold - 2) // (threshold - 1))
    return total, max(total - C, 0)


def audit_paid(e: int, prefix: int, groups: int, allocation_head: int) -> int:
    base = prefix + M - 65515 - groups
    thresholds = [20] + [16] * 33 + [20] * 4
    cores: list[int] = []
    insides: list[int] = []
    for threshold in thresholds:
        old_charge = 0 if not cores else charge(e, cores)[0]
        target = BUDGET - old_charge
        forced = (target - base + 1 + groups - 1) // groups
        assert forced == threshold
        total, inside = core(threshold)
        cores.append(total)
        insides.append(inside)
    packing = sum(insides) - len(insides) * (len(insides) - 1) * C // 2
    assert packing == 142893 > e
    final_charge, allocation, budget = charge(e, cores[:-1])
    assert final_charge == 609
    assert allocation == [allocation_head] + [15816] * 3 + [2046] * 33
    assert budget == e + 37 * 38 * C // 2
    return len(thresholds) * 4 + 8


def main() -> None:
    checks = audit_paid(130220, 11904256, 260559, 18769)
    checks += audit_paid(130221, 11903751, 269440, 18770)

    wall_thresholds = [18] + [14] * 42 + [11] * 127 + [7] * 66 + [3] * 52
    wall_cores = [core(value)[0] for value in wall_thresholds]
    wall_insides = [core(value)[1] for value in wall_thresholds]
    assert wall_cores == [9741] + [0] * 287
    assert wall_insides == [9736] + [0] * 287
    wall_charge, allocation, budget = charge(130222, wall_cores)
    assert allocation == [67453] * 5 + [1037] + [0] * 282
    assert budget == 338302 and wall_charge == 4910044
    assert BUDGET - wall_charge == 11867171 < 12148280

    first_q = sum((Fraction(N - x, M - x)
                   for x in [18769] + [15816] * 3 + [2046] * 33),
                  Fraction())
    last_q = sum((Fraction(N - x, M - x)
                  for x in [18770] + [15816] * 3 + [2046] * 33),
                 Fraction())
    wall_q = sum((Fraction(N - x, M - x) for x in allocation), Fraction())
    assert (first_q.numerator, first_q.denominator) == (
        894348212835561, 1468173681520)
    assert (last_q.numerator, last_q.denominator) == (
        1565078288323625, 2569251168624)
    assert (wall_q.numerator, wall_q.denominator) == (
        379266425096056, 77242971)
    print("MCA_FULL_LIFT_LOWER_AWARE_JOINT_CORE_CHARGE_V1_AUDIT_PASS "
          f"checks={checks + 13} exact_rational_replay=1")


if __name__ == "__main__":
    main()
