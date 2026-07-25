#!/usr/bin/env python3
"""Independent replay of the M31 rank-seven source-basis dichotomy."""

from __future__ import annotations

import heapq
import json
from math import ceil, comb
from pathlib import Path


K = 1_048_576
W = 67_447
G = 354_972
J = 4_981
RANK = 6
REQUIRED_DEFICIT = 3_214_704
MANIFEST = (
    Path(__file__).resolve().parents[2]
    / "experimental/data/certificates/"
    "m31-rank7-source-basis-private-root-overlap-dichotomy-v1/manifest.json"
)


def direct_cap(rank: int, dimension: int, excess: int) -> int:
    quotient = (
        comb(K + rank - 1, rank - 1)
        // comb(excess + rank - 1, rank - 1)
    )
    output = (K + dimension) * quotient // (excess + dimension)
    denominator = (
        (excess + dimension) ** 2
        - (K + dimension) * (dimension - 1)
    )
    if denominator > 0:
        output = min(
            output,
            (K + dimension) * (excess + 1) // denominator,
        )
    return output


def heap_recurrence(maximum: int, excess: int) -> dict[int, list[int]]:
    """Use a lazy maximum heap, independent of the primary monotone deque."""

    arrays = {
        1: [0]
        + [(K + dimension) // (excess + dimension)
           for dimension in range(1, maximum + 1)]
    }
    for rank in range(2, RANK + 1):
        child = arrays[rank - 1]
        current = child.copy()
        prefix = -1
        heap: list[tuple[int, int]] = []
        for dimension in range(rank, maximum + 1):
            added = dimension - 1
            prefix = max(prefix, child[added])
            heapq.heappush(heap, (-child[added], added))
            lower = dimension - (dimension - 1) // (rank - 1)
            while heap[0][1] < lower:
                heapq.heappop(heap)
            recurrence = (
                (dimension - 1) * prefix
                + (K + 1) * (-heap[0][0])
            ) // (excess + dimension)
            current[dimension] = max(
                child[dimension],
                min(recurrence, direct_cap(rank, dimension, excess)),
            )
        arrays[rank] = current
    return arrays


zero = heap_recurrence(J, W)
one = heap_recurrence(J - 1, W + 1)

assert zero[5][J - 1] == 674_155
assert zero[6][J] == 9_806_438
assert one[6][J - 1] == 444_522
positive_zero_direct_caps = [
    (direct_cap(6, J - zero_count, W + zero_count), zero_count)
    for zero_count in range(1, J - 6 + 1)
]
assert max(positive_zero_direct_caps) == (444_522, 1)

baseline = zero[5][J - 1]
loss = {
    size: size * (baseline - zero[5][J - size])
    for size in range(1, 12)
}
assert loss == {
    1: 0,
    2: 1_195_278,
    3: 1_906_755,
    4: 2_593_488,
    5: 3_273_960,
    6: 3_951_912,
    7: 4_628_603,
    8: 5_304_568,
    9: 5_980_086,
    10: 6_655_300,
    11: 7_330_301,
}
all_large_line_losses = [
    (
        size * (baseline - zero[5][J - size]),
        size,
    )
    for size in range(5, J - 5 + 1)
]
assert min(all_large_line_losses) == (3_273_960, 5)

histograms: list[tuple[int, tuple[int, ...]]] = []
for h2 in range(REQUIRED_DEFICIT // loss[2] + 1):
    for h3 in range(REQUIRED_DEFICIT // loss[3] + 1):
        for h4 in range(REQUIRED_DEFICIT // loss[4] + 1):
            deficit = h2 * loss[2] + h3 * loss[3] + h4 * loss[4]
            if deficit < REQUIRED_DEFICIT:
                parts = tuple(sorted(
                    (2,) * h2 + (3,) * h3 + (4,) * h4,
                    reverse=True,
                ))
                histograms.append((deficit, parts))
assert sorted(histograms) == [
    (0, ()),
    (1_195_278, (2,)),
    (1_906_755, (3,)),
    (2_390_556, (2, 2)),
    (2_593_488, (4,)),
    (3_102_033, (3, 2)),
]

# Pointwise multiplicity inequalities underlying the source-basis proof.
for multiplicity in range(1, 8):
    assert comb(multiplicity, 2) >= multiplicity - 1
assert ceil(29 / 7) == 5
assert 2 * G - 28 == 709_916
assert 709_916 - G == 354_944
assert ceil(354_944 / comb(7, 2)) == 16_903

manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
assert manifest["fixed_mismatch_branch"]["z1_cap"] == 444_522
assert (
    manifest["projective_deficit_branch"]["line_deficits"][4]
    ["numerator_deficit"]
    == 3_273_960
)
assert (
    manifest["source_basis_dichotomy"]["forced_pairwise_gcd_degree"]
    == 16_903
)
assert manifest["remaining_terminal"]["paid_owner"] is None
assert manifest["remaining_terminal"]["Q147595_closed"] is False

print(
    "M31 rank7 source-basis overlap independent replay: PASS "
    "(heap recurrence, histogram exhaustion, multiplicity inequalities)"
)
