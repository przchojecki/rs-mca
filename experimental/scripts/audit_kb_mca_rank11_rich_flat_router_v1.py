#!/usr/bin/env python3
"""Independent arithmetic and combinatorial audit for the rich-flat router.

This implementation intentionally does not import the primary verifier.  It
uses multiplicative recurrences for binomial ratios and a direct cutoff scan.
"""

from __future__ import annotations

import itertools
from math import comb

N = 2_097_152
K = 1_048_576
M = 1_116_048
W = 67_472
BUDGET = 274_980_728_111_395_087
NEAR = 134_944
RESOURCE = 106_618_568_137_036_225_644
RAY = 8_147_918
TAU = 1_547
H = 42_452


def falling_loop(x: int, t: int) -> int:
    value = 1
    for j in range(t):
        value *= x - j
    return value


FALL_M = {t: falling_loop(M, t) for t in (8, 9)}


def m2_loop(tau: int) -> int:
    d = W - tau
    numerator = (N - K + 2) * (N - K + 1)
    denominator = (d + 2) * (d + 1)
    return numerator // denominator


def cap_spaces(tau: int, h: int, t: int) -> int:
    c = 2 * (M - tau) - N
    return FALL_M[t] // pow(c - h, t)


def direct_total(tau: int, h: int) -> int:
    a = M - tau
    c = 2 * a - N
    if not (1 <= tau < W and 0 <= h < c):
        raise ValueError("illegal cell")
    outside = N - a
    rank_two = m2_loop(tau) * outside
    return (
        NEAR
        + RESOURCE // (tau + 1)
        + outside
        + cap_spaces(tau, h, 9) * RAY
        + cap_spaces(tau, h, 8) * rank_two
    )


def scan() -> tuple[int, list[int], tuple[int, int], tuple[int, int]]:
    global_h = -1
    maximizers: list[int] = []
    first: tuple[int, int] | None = None
    last: tuple[int, int] | None = None
    for tau in range(1, W):
        c = 2 * (M - tau) - N
        if direct_total(tau, 0) > BUDGET:
            continue
        lo, hi, best = 0, c - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if direct_total(tau, mid) <= BUDGET:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        if first is None:
            first = (tau, best)
        last = (tau, best)
        if best > global_h:
            global_h = best
            maximizers = [tau]
        elif best == global_h:
            maximizers.append(tau)
    assert first is not None and last is not None
    return global_h, maximizers, first, last


def rank2(vectors: list[tuple[int, int]], p: int) -> int:
    if not vectors:
        return 0
    if any(x or y for x, y in vectors):
        first = next((v for v in vectors if v != (0, 0)), None)
        assert first is not None
        if any((first[0] * v[1] - first[1] * v[0]) % p for v in vectors):
            return 2
        return 1
    return 0


def tiny_matroid_audit() -> int:
    """Independent exhaustive rank-two test over multisets in F_3^2."""

    types = list(itertools.product(range(3), repeat=2))
    checked = 0
    # Enumerate sorted 5-tuples of vector-type indices.
    for indices in itertools.combinations_with_replacement(range(len(types)), 5):
        vectors = [types[i] for i in indices]
        r = rank2(vectors, 3)
        if r == 0:
            continue
        # Proper flats are zero for rank one and projective lines for rank two.
        if r == 1:
            h = vectors.count((0, 0))
        else:
            h = vectors.count((0, 0))
            for normal in types[1:]:
                count = sum((normal[0] * x + normal[1] * y) % 3 == 0 for x, y in vectors)
                if count < len(vectors):
                    h = max(h, count)
        ordered = 0
        for positions in itertools.permutations(range(5), r):
            chosen = [vectors[i] for i in positions]
            if rank2(chosen, 3) == r:
                ordered += 1
        assert ordered >= (5 - h) ** r
        checked += 1
    return checked


def main() -> None:
    a = M - TAU
    c = 2 * a - N
    outside = N - a
    m2 = m2_loop(TAU)
    n1 = cap_spaces(TAU, H, 9)
    n2 = cap_spaces(TAU, H, 8)
    total = direct_total(TAU, H)
    assert (a, c, outside, m2, n1, n2) == (
        1_114_501,
        131_850,
        982_651,
        252,
        7_365_150_514,
        589_969_647,
    )
    assert total == 274_978_720_888_758_363
    assert BUDGET - total == 2_007_222_636_724
    assert direct_total(TAU, H + 1) - BUDGET == 17_108_854_816_460
    assert m2 == comb(N - K + 2, 2) // comb(W - TAU + 2, 2)
    assert scan() == (42_452, [1547, 1548, 1549], (397, 101), (21132, 4))
    checked = tiny_matroid_audit()
    assert checked == 1_286
    print(
        "KB_MCA_RANK11_RICH_FLAT_AUDIT_PASS "
        f"total={total} slack={BUDGET-total} scan_max=42452 "
        f"tiny_matroids={checked}"
    )


if __name__ == "__main__":
    main()
