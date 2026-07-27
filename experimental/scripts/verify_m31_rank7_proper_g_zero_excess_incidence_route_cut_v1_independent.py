#!/usr/bin/env python3
"""Independent exact-integer replay of the M31 proper-G route cut."""

from __future__ import annotations

import heapq
from itertools import combinations
from math import ceil, comb


K = 1_048_576
RADIUS = 981_129
W = 67_447
G = 354_972
D = 287_525
SIGMA = 282_544
RESIDUAL_K = 4_981


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def affine_cap(rank: int, ambient_gap: int, excess: int) -> int:
    return comb(ambient_gap + rank, rank) // comb(excess + rank, rank)


def direct_cap(rank: int, dimension: int, excess: int) -> int:
    child = (
        comb(K + rank - 1, rank - 1)
        // comb(excess + rank - 1, rank - 1)
    )
    value = (K + dimension) * child // (excess + dimension)
    denominator = (
        (excess + dimension) ** 2
        - (K + dimension) * (dimension - 1)
    )
    if denominator > 0:
        value = min(
            value,
            (K + dimension) * (excess + 1) // denominator,
        )
    return value


def recurrence(maximum_dimension: int, excess: int) -> dict[int, list[int]]:
    """Independent heap implementation of the projective recurrence."""

    output: dict[int, list[int]] = {
        1: [
            0,
            *[
                (K + dimension) // (excess + dimension)
                for dimension in range(1, maximum_dimension + 1)
            ],
        ]
    }
    for rank in range(2, 7):
        child = output[rank - 1]
        current = child.copy()
        prefix = -1
        heap: list[tuple[int, int]] = []
        for dimension in range(rank, maximum_dimension + 1):
            index = dimension - 1
            prefix = max(prefix, child[index])
            heapq.heappush(heap, (-child[index], index))
            lower = dimension - (dimension - 1) // (rank - 1)
            while heap and heap[0][1] < lower:
                heapq.heappop(heap)
            require(bool(heap), "recurrence window")
            window_maximum = -heap[0][0]
            candidate = (
                (dimension - 1) * prefix
                + (K + 1) * window_maximum
            ) // (excess + dimension)
            current[dimension] = max(
                child[dimension],
                min(candidate, direct_cap(rank, dimension, excess)),
            )
        output[rank] = current
    return output


def deployed_arithmetic() -> None:
    require(D - SIGMA == RESIDUAL_K, "residual link")
    require(affine_cap(5, K, W) == 908_021, "rank-five cap")
    require(affine_cap(5, K, W + 1) == 907_953, "rank-five fallback")

    arrays = recurrence(RESIDUAL_K, W + 1)
    child = arrays[5][RESIDUAL_K - 1]
    numerator = (K + RESIDUAL_K) * child
    denominator = W + 1 + RESIDUAL_K
    require(child == 444_522, "excess-one child")
    require(
        divmod(numerator, denominator) == (6_466_046, 19_020),
        "excess-one parent",
    )

    full = divmod(comb(693_610, 6), comb(67_453, 6))
    proper = divmod(comb(698_589, 5), comb(67_452, 5))
    require(
        full
        == (
            1_182_419,
            86_919_124_762_661_448_764_444_630,
        ),
        "full-P division",
    )
    require(
        proper
        == (119_177, 892_372_184_216_353_689_387),
        "proper fixed-G division",
    )

    proper_minimum = 9_806_394 - 6_466_046 - 1_182_419
    require(proper_minimum == 2_157_929, "proper minimum")
    require(
        6_466_046 + 1_182_419 + 2_157_928 == 9_806_393,
        "closing add-back",
    )
    require(ceil(proper_minimum / 119_177) == 19, "slice minimum")
    require(18 * 119_177 + 12_743 == proper_minimum, "scalar obstruction")


def incidence_replay() -> None:
    pair_count = comb(7, 2)
    intersection_budget = pair_count * (RESIDUAL_K - 1)
    require(pair_count == 21, "pair count")
    require(intersection_budget == 104_580, "intersection budget")

    # Check the pointwise inequalities used to pass from complement
    # incidence to locator overlap.
    for missing in range(7):
        require(
            missing <= 1 + comb(missing, 2),
            f"missing-incidence inequality {missing}",
        )
        present = 7 - missing
        require(
            comb(present, 2) + 5 * comb(missing, 2) >= 15,
            f"pointwise overlap inequality {missing}",
        )

    union_sum = 6 * G + 5 * intersection_budget
    require(union_sum == 2_652_732, "union-sum envelope")
    require(divmod(union_sum, pair_count) == (126_320, 12), "union average")
    require(G - union_sum // pair_count == 228_652, "forced overlap")

    total_overlap = 15 * G - 5 * intersection_budget
    require(total_overlap == 4_801_680, "total overlap")
    require(ceil(total_overlap / pair_count) == 228_652, "overlap ceiling")
    require(
        228_652 + SIGMA + W + 1 == 578_644,
        "determinant degree sum",
    )
    require(2 * G - 578_644 == 131_300, "cofactor sum")


def sharp_support_fixture() -> None:
    """Build the exact abstract seven-set extremizer independently."""

    missing_patterns: list[tuple[int, ...]] = []
    for pair in combinations(range(7), 2):
        missing_patterns.extend([pair] * 4_980)
    singleton_counts = [35_771, 35_771, 35_770, 35_770, 35_770, 35_770, 35_770]
    for index, count in enumerate(singleton_counts):
        missing_patterns.extend([(index,)] * count)
    require(len(missing_patterns) == G, "sharp universe")

    complement_intersections: list[int] = []
    locator_overlaps: list[int] = []
    complement_sizes = [
        sum(index in pattern for pattern in missing_patterns)
        for index in range(7)
    ]
    for left, right in combinations(range(7), 2):
        complement_intersections.append(
            sum(
                left in pattern and right in pattern
                for pattern in missing_patterns
            )
        )
        locator_overlaps.append(
            sum(
                left not in pattern and right not in pattern
                for pattern in missing_patterns
            )
        )

    require(set(complement_intersections) == {4_980}, "sharp C_ij")
    require(max(locator_overlaps) == 228_652, "sharp overlap")
    require(
        sorted(complement_sizes) == [65_650] * 5 + [65_651] * 2,
        "sharp cofactor sizes",
    )


def main() -> None:
    deployed_arithmetic()
    incidence_replay()
    sharp_support_fixture()
    print(
        "independent M31 rank7 proper-G zero-excess route cut: PASS"
    )


if __name__ == "__main__":
    main()
