#!/usr/bin/env python3
"""Verify the M31 exact-layer slot-core packing payment."""

from __future__ import annotations

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


def bank(e: int, cutoff: int) -> tuple[int, int, int]:
    weighted = prefix(e, cutoff)
    groups = 0
    for h in range(cutoff + 1, M + 1):
        overlap = 2 * h - e
        denominator = overlap * overlap - e * C
        if 2 * h <= e or overlap <= C or denominator <= 0:
            raise Reject("bank guard")
        groups += e * (overlap - C) // denominator
    return weighted, groups, weighted + M - cutoff - groups


def capped_charge(e: int, lower: list[int], cap: int) -> tuple[int, int]:
    if not lower:
        return 0, 0
    count = len(lower)
    budget = min(count * cap, e + count * (count + 1) * C // 2)
    values = sorted(lower, reverse=True)
    excess = budget - sum(values)
    if excess < 0:
        raise Reject("packing before charge")
    for index, value in enumerate(values):
        addition = min(excess, cap - value)
        values[index] += addition
        excess -= addition
        if excess == 0:
            break
    if excess:
        raise Reject("allocation")
    value = sum((Fraction(N - core, M - core) for core in values),
                Fraction())
    return value.numerator // value.denominator, budget


def paid_row(e: int, cutoff: int) -> tuple[int, ...]:
    weighted, groups, base = bank(e, cutoff)
    cap = e + 9 - ABS_CUTOFF
    absorption_bound = prefix(e, ABS_CUTOFF) + LINE
    lower: list[int] = []
    threshold = inside = charge = target = core_budget = 0
    for _ in range(3):
        charge, core_budget = capped_charge(e, lower, cap)
        target = BUDGET - charge
        threshold = (target - base + groups) // groups
        if threshold < 2:
            raise Reject("paid threshold")
        numerator = threshold * (cutoff + 1) - e
        inside = max(0, (numerator + threshold - 2) // (threshold - 1))
        lower.append(inside)
    packing = sum(lower) - len(lower) * (len(lower) - 1) * C // 2
    if packing <= e or absorption_bound >= BUDGET:
        raise Reject("payment")
    return (e, cutoff, weighted, groups, base, cap, absorption_bound,
            threshold, inside, charge, target, core_budget, packing)


EXPECTED = (
    (130226, 65516, 12404722, 342025, 12064635, 64785, 5161243, 14, 60540, 737, 16776478, 129570, 181605),
    (130227, 65516, 12404167, 1217008, 11189097, 64786, 5161221, 5, 49340, 737, 16776478, 129572, 148005),
    (130228, 65517, 12958915, 342446, 12618406, 64787, 5161211, 13, 60126, 737, 16776478, 129574, 180363),
    (130229, 65517, 12958300, 1305245, 11654992, 64788, 5161190, 4, 43948, 738, 16776477, 129576, 131829),
    (130230, 65518, 13573258, 342865, 13232329, 64789, 5161180, 11, 59048, 738, 16776477, 129578, 177129),
    (130231, 65518, 13572575, 1412234, 12162277, 64790, 5161158, 4, 43949, 738, 16776477, 129580, 131832),
    (130232, 65519, 14258109, 343295, 13916749, 64791, 5161148, 9, 57431, 738, 16776477, 129582, 172278),
    (130233, 65520, 15027192, 301252, 14727874, 64792, 5161126, 7, 54736, 739, 16776476, 129584, 164193),
    (130234, 65520, 15026344, 343725, 14684553, 64793, 5161117, 7, 54736, 739, 16776476, 129586, 164193),
    (130235, 65521, 15895144, 301391, 15595686, 64794, 5161095, 4, 43951, 739, 16776476, 129588, 131838),
    (130236, 65521, 15894179, 344160, 15551952, 64795, 5161085, 4, 43951, 739, 16776476, 129590, 131838),
)


def uniform_charge(e: int, lines: int, lower: int,
                   cap: int) -> tuple[int, int, int, int, int]:
    budget = min(lines * cap, e + lines * (lines + 1) * C // 2)
    lower_sum = lines * lower
    full, remainder = divmod(budget - lower_sum, cap - lower)
    full = min(full, lines)
    value = full * Fraction(N - cap, M - cap)
    if full < lines:
        if remainder:
            value += Fraction(N - lower - remainder, M - lower - remainder)
            residual = lines - full - 1
        else:
            residual = lines - full
        value += residual * Fraction(N - lower, M - lower)
    return (value.numerator // value.denominator, budget, lower_sum,
            full, remainder)


def adjacent_row() -> tuple[int, ...]:
    e, cutoff = 130237, 65521
    weighted, groups, base = bank(e, cutoff)
    cap = e + 9 - ABS_CUTOFF
    absorption_bound = prefix(e, ABS_CUTOFF) + LINE
    first = (BUDGET - base + groups) // groups
    inside = (first * (cutoff + 1) - e + first - 2) // (first - 1)
    maximum = max(s * inside - s * (s - 1) * C // 2
                  for s in range(1, 1000))
    for lines in range(1, 10000):
        charge, budget, lower_sum, full, remainder = uniform_charge(
            e, lines, inside, cap)
        target = BUDGET - charge
        threshold = (target - base + groups) // groups
        if threshold < 2:
            return (e, cutoff, weighted, groups, base, cap,
                    absorption_bound, first, inside, maximum, lines,
                    budget, lower_sum, full, remainder, charge, target,
                    threshold)
    raise Reject("adjacent limit")


ADJACENT = (
    130237, 65521, 15893203, 1933560, 13961576, 64796, 5161064,
    2, 807, 65529, 7583, 143903917, 6119481, 2153, 16119,
    882245, 15894970, 1,
)


def main() -> None:
    checks = 0
    for expected in EXPECTED:
        actual = paid_row(expected[0], expected[1])
        if actual != expected:
            raise Reject(f"row {expected[0]}")
        checks += len(expected)
    if adjacent_row() != ADJACENT:
        raise Reject("adjacent")
    checks += len(ADJACENT)
    print("MCA_FULL_LIFT_EXACT_LAYER_SLOT_CORE_PACKING_V1_PASS "
          f"checks={checks} paid=130226..130236 wall=130237")


if __name__ == "__main__":
    main()
