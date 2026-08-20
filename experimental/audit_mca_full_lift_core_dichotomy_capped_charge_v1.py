#!/usr/bin/env python3
"""Independent exact audit of the M31 core-dichotomy endpoints."""

from __future__ import annotations

from fractions import Fraction


N, M, C, BUDGET = 1048582, 67454, 5, 16777215
LINE = N - M + 1


def charge(e: int, lower: list[int], cap: int) -> int:
    count = len(lower)
    if count == 0:
        return 0
    budget = min(count * cap, e + count * (count + 1) * C // 2)
    values = sorted(lower, reverse=True)
    excess = budget - sum(values)
    for index, value in enumerate(values):
        addition = min(excess, cap - value)
        values[index] += addition
        excess -= addition
        if excess == 0:
            break
    assert excess == 0
    value = sum((Fraction(N - x, M - x) for x in values), Fraction())
    return value.numerator // value.denominator


def core(threshold: int) -> tuple[int, int]:
    numerator = threshold * M - N
    total = (0 if numerator <= 0 else
             (numerator + threshold - 2) // (threshold - 1))
    return total, max(total - C, 0)


def paid(e: int, cap: int, base: int, groups: int,
         threshold: int, lines: int, expected_packing: int,
         absorption_prefix: int) -> int:
    assert absorption_prefix + LINE < BUDGET
    cores: list[int] = []
    insides: list[int] = []
    for _ in range(lines):
        target = BUDGET - charge(e, cores, cap)
        assert (target - base + 1 + groups - 1) // groups == threshold
        total, inside = core(threshold)
        cores.append(total)
        insides.append(inside)
    packing = sum(insides) - len(insides) * (len(insides) - 1) * C // 2
    assert packing == expected_packing > e
    return 7 + 4 * lines


def main() -> None:
    checks = paid(130222, 64781, 12148280, 260580, 18, 14, 135849, 4180178)
    checks += paid(130223, 64782, 12138824, 269480, 18, 14, 135849, 4180156)
    checks += paid(130224, 64783, 12702685, 260602, 16, 70, 130795, 4180145)
    checks += paid(130225, 64784, 12693152, 269520, 16, 70, 130795, 4180124)

    e, cap, lines = 130226, 64785, 14763
    budget = min(lines * cap, e + lines * (lines + 1) * C // 2)
    full, remainder = divmod(budget, cap)
    value = full * Fraction(N - cap, M - cap)
    value += Fraction(N - remainder, M - remainder)
    value += (lines - full - 1) * Fraction(N, M)
    wall_charge = value.numerator // value.denominator
    assert (budget, full, remainder) == (545032556, 8412, 61136)
    assert wall_charge == 3199542
    target = BUDGET - wall_charge
    assert target == 13577673
    assert (target - 13317279 + 1 + 260627 - 1) // 260627 == 1
    assert core(14) == (0, 0)
    assert 4180114 + LINE == 5161243 < BUDGET
    print("MCA_FULL_LIFT_CORE_DICHOTOMY_CAPPED_CHARGE_V1_AUDIT_PASS "
          f"checks={checks + 15} exact_rational_replay=1")


if __name__ == "__main__":
    main()
