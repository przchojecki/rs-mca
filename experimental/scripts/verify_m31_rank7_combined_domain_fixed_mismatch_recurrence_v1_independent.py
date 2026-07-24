#!/usr/bin/env python3
"""Independent heap replay for the M31 fixed-mismatch recurrence packet."""

from __future__ import annotations

import hashlib
import heapq
import json
from math import comb


K = 1_048_576
W = 67_447
R = 981_129
G = 354_972
D = 287_525
TARGET = 15_775_932


def digest(values: list[int]) -> str:
    raw = (
        json.dumps(values, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def direct_cap(rank: int, dimension: int) -> int:
    inner = (
        comb(K + rank - 1, rank - 1)
        // comb(W + rank - 1, rank - 1)
    )
    cap = (K + dimension) * inner // (W + dimension)
    denominator = (
        (W + dimension) ** 2
        - (K + dimension) * (dimension - 1)
    )
    if denominator > 0:
        cap = min(
            cap,
            (K + dimension) * (W + 1) // denominator,
        )
    return cap


def independent_recurrence() -> dict[int, list[int]]:
    """Use a lazy max heap rather than the primary monotone deque."""

    result: dict[int, list[int]] = {}
    rank_one = [0]
    rank_one.extend(
        (K + dimension) // (W + dimension)
        for dimension in range(1, D + 1)
    )
    result[1] = rank_one

    for rank in range(2, 7):
        child = result[rank - 1]
        current = child.copy()
        prefix_max = -1
        window: list[tuple[int, int]] = []
        for dimension in range(rank, D + 1):
            added = dimension - 1
            prefix_max = max(prefix_max, child[added])
            heapq.heappush(window, (-child[added], added))
            lower = dimension - (dimension - 1) // (rank - 1)
            while window[0][1] < lower:
                heapq.heappop(window)
            window_max = -window[0][0]
            recurrence = (
                (dimension - 1) * prefix_max
                + (K + 1) * window_max
            ) // (W + dimension)
            current[dimension] = max(
                child[dimension],
                min(recurrence, direct_cap(rank, dimension)),
            )
        result[rank] = current
    return result


def prefix(class_caps: list[int]) -> tuple[list[int], list[int]]:
    values = [0] * len(class_caps)
    args = [0] * len(class_caps)
    best = 0
    arg = 0
    for index in range(1, len(class_caps)):
        if class_caps[index] > best:
            best = class_caps[index]
            arg = index
        values[index] = best
        args[index] = arg
    return values, args


def classes(rank_six: list[int], reduction: int = 0) -> list[int]:
    output = [0] * (D - 6 + 1)
    for size in range(1, len(output)):
        dimension = D - size
        output[size] = rank_six[dimension]
        if dimension == 4_981:
            output[size] -= reduction
    return output


def coarse(cutoff: int, class_caps: list[int]) -> tuple[int, int, int, int]:
    maxima, _args = prefix(class_caps)
    denominator = G - cutoff
    best = -1
    survivors = 0
    for size in range(1, len(class_caps)):
        rest = D - 1 - size
        upper = min(size, rest - 4)
        tail = min(size, rest // 5)
        if upper < 1 or tail < 1:
            continue
        value = (
            size * class_caps[size]
            + rest * maxima[upper]
            + (R - (D - 1)) * maxima[tail]
        )
        if value // denominator > TARGET:
            survivors += 1
        best = max(best, value)
    return best, best // denominator, best % denominator, survivors


def residue_shortest_path(
    tail_mass: int,
    maximum_part: int,
    class_caps: list[int],
) -> tuple[int, int, int, list[int]]:
    """Independent residue Dijkstra; maximum parts are free filler."""

    baseline = class_caps[maximum_part]
    loss = [
        size * (baseline - class_caps[size])
        for size in range(maximum_part)
    ]
    infinity = 10**100
    distance = [infinity] * maximum_part
    mass = [infinity] * maximum_part
    parent: list[tuple[int, int] | None] = [None] * maximum_part
    distance[0] = 0
    mass[0] = 0
    queue: list[tuple[int, int, int]] = [(0, 0, 0)]
    while queue:
        cost, used, residue = heapq.heappop(queue)
        if (cost, used) != (distance[residue], mass[residue]):
            continue
        for part in range(1, maximum_part):
            target = (residue + part) % maximum_part
            candidate = (cost + loss[part], used + part)
            if candidate < (distance[target], mass[target]):
                distance[target], mass[target] = candidate
                parent[target] = (residue, part)
                heapq.heappush(
                    queue,
                    (candidate[0], candidate[1], target),
                )
    residue = tail_mass % maximum_part
    parts: list[int] = []
    cursor = residue
    while cursor:
        step = parent[cursor]
        assert step is not None
        cursor, part = step
        parts.append(part)
    assert mass[residue] <= tail_mass
    fillers = (tail_mass - mass[residue]) // maximum_part
    objective = tail_mass * baseline - distance[residue]
    return objective, distance[residue], fillers, sorted(parts)


def refined(
    cutoff: int,
    rank_six: list[int],
    reduction: int = 0,
) -> tuple[int, int, int, int, int]:
    class_caps = classes(rank_six, reduction)
    maxima, _args = prefix(class_caps)
    largest = 282_544
    budget = D - 1 - largest
    candidates: list[tuple[int, int]] = []
    for sixth in range(1, budget // 5 + 1):
        high = budget - 4 * sixth
        value = (
            (R - largest) * maxima[sixth]
            + budget * (maxima[high] - maxima[sixth])
        )
        candidates.append((value, sixth))
    ordered = sorted(candidates, reverse=True)
    assert ordered[0] == (500_828_161_030, 996)
    assert ordered[1][0] == 500_826_095_155

    tail_mass = R - largest - budget
    tail, loss, fillers, parts = residue_shortest_path(
        tail_mass,
        996,
        class_caps,
    )
    assert (tail, loss, fillers, parts) == (
        497_257_822_254,
        87_136,
        696,
        [389],
    )
    nonlargest = budget * class_caps[996] + tail
    assert nonlargest == 500_828_073_894
    assert nonlargest > ordered[1][0]
    numerator = largest * class_caps[largest] + nonlargest
    denominator = G - cutoff
    return (
        numerator,
        numerator // denominator,
        numerator % denominator,
        TARGET - numerator // denominator,
        coarse(cutoff, class_caps)[3],
    )


def main() -> None:
    arrays = independent_recurrence()
    rank_six = arrays[6]
    assert [rank_six[k] for k in range(4_981, 4_987)] == [
        9_806_438,
        9_806_312,
        9_806_186,
        9_806_060,
        9_805_934,
        9_805_807,
    ]
    assert arrays[5][4_980] == 674_155
    assert rank_six[D - 389] == 716_694
    assert rank_six[D - 996] == 716_918
    assert digest(rank_six) == (
        "3cafd8d5d4a9d00b6bd90c13050476bab4bfac9ccb43125ba90a2844dbab70b6"
    )

    class_caps = classes(rank_six)
    maxima, args = prefix(class_caps)
    assert digest(class_caps) == (
        "acbf2c1ca7de99a5b206a0ff4285fd8dff176fc5ac9730b0d1a6b26dfd6ffb26"
    )
    assert digest(maxima) == (
        "5aece4aaf582faf028e60fca243cd434513cee976c72c19c843314ac05cccc1b"
    )
    assert digest(args) == (
        "f2d1a3e7f8e34c259c655ff8bd41fdf174638dc22ad6f1e6b61e9a230ac5dc7d"
    )

    assert coarse(147_593, class_caps) == (
        3_271_586_860_242,
        15_775_883,
        19_585,
        0,
    )
    assert refined(147_594, rank_six) == (
        3_271_578_292_166,
        15_775_917,
        176_540,
        15,
        1,
    )
    assert refined(147_595, rank_six) == (
        3_271_578_292_166,
        15_775_993,
        191_805,
        -61,
        1,
    )
    assert refined(147_595, rank_six, 44)[:4] == (
        3_271_565_860_230,
        15_775_933,
        202_489,
        -1,
    )
    assert refined(147_595, rank_six, 45)[:4] == (
        3_271_565_577_686,
        15_775_932,
        127_322,
        0,
    )
    print("M31 rank7 fixed-mismatch independent replay: PASS")


if __name__ == "__main__":
    main()
