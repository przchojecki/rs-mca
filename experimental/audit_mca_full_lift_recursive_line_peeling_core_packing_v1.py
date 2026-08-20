#!/usr/bin/env python3
"""Independent endpoint audit for recursive M31 line peeling."""

from __future__ import annotations


R, D, K = 1048576, 67448, 6
N, M, C = R + K, D + K, K - 1
BUDGET, LINE = 16777215, N - M + 1


def gram_cap(e: int, h: int) -> int:
    shortened = N - e
    agreement = M - h
    assert agreement > C
    delta = agreement * agreement - shortened * C
    if delta > 0:
        return shortened * (agreement - C) // delta
    gap = -delta
    assert 2 * agreement * agreement >= shortened * C
    tangent = ((shortened - agreement) ** 2
               - (shortened - 1) * gap)
    assert tangent > 0
    return ((shortened - 1) * shortened * shortened * (agreement - C)
            // (agreement * tangent))


def weighted_prefix(e: int, cutoff: int) -> int:
    suffix = [0] + [gram_cap(e, h) for h in range(1, cutoff + 1)]
    running = suffix[cutoff]
    for h in range(cutoff - 1, 0, -1):
        running = min(running, suffix[h])
        suffix[h] = running
    return sum((suffix[h] - suffix[h - 1]) * (e // h)
               for h in range(1, cutoff + 1))


def bank(e: int, cutoff: int, upper: int) -> tuple[int, int]:
    groups = 0
    for h in range(cutoff + 1, upper + 1):
        overlap = 2 * h - e
        denominator = overlap * overlap - e * C
        assert 2 * h > e and overlap > C and denominator > 0
        groups += e * (overlap - C) // denominator
    base = weighted_prefix(e, cutoff) + upper - cutoff - groups
    return groups, base


def forced_inside(threshold: int) -> int:
    numerator = threshold * M - N
    core = 0 if numerator <= 0 else (
        numerator + threshold - 2) // (threshold - 1)
    return max(core - C, 0)


def thresholds(groups: int, base: int, count: int) -> list[int]:
    answer = []
    for r in range(count):
        required = BUDGET - r * LINE - base + 1
        assert required > 0
        answer.append((required + groups - 1) // groups)
    return answer


def main() -> None:
    groups, base = bank(124806, 65304, M)
    threshold = thresholds(groups, base, 1)[0]
    inside = forced_inside(threshold)
    sync = 124806 - inside + K
    low = weighted_prefix(124806, sync - 1)
    assert (groups, base, threshold, inside, sync, low + LINE) == (
        33873, 2138482, 433, 65178, 59634, 2603990)

    groups, base = bank(128340, 65304, M)
    threshold1 = thresholds(groups, base, 1)[0]
    inside1 = forced_inside(threshold1)
    sync1 = 128340 - inside1 + K
    groups2, base2 = bank(128340, 65304, sync1 - 1)
    threshold2 = thresholds(groups2, base2, 2)[1]
    inside2 = forced_inside(threshold2)
    assert (threshold1, inside1, sync1, groups2, base2,
            threshold2, inside2) == (
        213, 62822, 65524, 12523, 1749442, 1122, 66574)
    assert inside1 + inside2 - C == 129391 > 128340

    groups, base = bank(130198, 65504, M)
    last_thresholds = thresholds(groups, base, 5)
    last_inside = [forced_inside(value) for value in last_thresholds]
    last_lhs = sum(last_inside) - 10 * C
    assert (groups, base, last_thresholds, last_inside, last_lhs) == (
        260297, 8163020, [34, 30, 26, 22, 19],
        [37718, 33617, 28204, 20729, 12942], 133160)
    assert last_lhs > 130198

    groups, base = bank(130199, 65504, M)
    wall_thresholds = thresholds(groups, base, 9)
    wall_inside = [forced_inside(value) for value in wall_thresholds]
    wall_lhs = sum(wall_inside) - 36 * C
    next_target = BUDGET - 9 * LINE
    assert (groups, base, wall_thresholds, wall_inside,
            wall_lhs, next_target) == (
        269019, 8154082, [33, 29, 25, 22, 18, 14, 11, 7, 3],
        [36789, 32409, 26569, 20729, 9736, 0, 0, 0, 0],
        126052, 7947054)
    assert wall_lhs <= 130199 and next_target - base + 1 <= 0

    print(
        "MCA_FULL_LIFT_RECURSIVE_LINE_PEELING_CORE_PACKING_V1_AUDIT_PASS "
        "first=124806 packing=128340 last=130198 wall=130199"
    )


if __name__ == "__main__":
    main()
