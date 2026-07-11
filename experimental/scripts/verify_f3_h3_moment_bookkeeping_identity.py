#!/usr/bin/env python3
"""Verify the h=3 ordered-triple moment bookkeeping identity."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, combinations_with_replacement
from math import comb


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(p: int) -> int:
    factors = factor_distinct(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise AssertionError(("no primitive root", p))


def subgroup(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n != 0:
        raise AssertionError((p, n, "n must divide p-1"))
    zeta = pow(primitive_root(p), (p - 1) // n, p)
    values: list[int] = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = x * zeta % p
    if x != 1 or len(set(values)) != n:
        raise AssertionError((p, n, "bad subgroup"))
    return tuple(values)


def signature(values: tuple[int, int, int], p: int) -> tuple[int, int]:
    return sum(values) % p, sum((x * x) % p for x in values) % p


def perm_count(multiset: tuple[int, int, int]) -> int:
    distinct = len(set(multiset))
    if distinct == 3:
        return 6
    if distinct == 2:
        return 3
    return 1


def trivial_term(n: int) -> int:
    return 36 * comb(n, 3) + 9 * n * (n - 1) + n


def verify_row(p: int, n: int) -> dict[str, int]:
    vals = subgroup(p, n)

    multiset_buckets: dict[
        tuple[int, int], list[tuple[tuple[int, int, int], int]]
    ] = defaultdict(list)
    for idxs in combinations_with_replacement(range(n), 3):
        key = signature(tuple(vals[i] for i in idxs), p)
        multiset_buckets[key].append((idxs, perm_count(idxs)))

    moment = 0
    trivial = 0
    t3 = 0
    repeat_residue = 0
    overlapping_distinct = 0

    for entries in multiset_buckets.values():
        bucket_ordered = sum(weight for _, weight in entries)
        moment += bucket_ordered * bucket_ordered
        for idxs, weight in entries:
            trivial += weight * weight
        for i, (left, left_weight) in enumerate(entries):
            left_distinct = len(set(left)) == 3
            for j, (right, right_weight) in enumerate(entries):
                if i == j:
                    continue
                right_distinct = len(set(right)) == 3
                if left_distinct and right_distinct:
                    if set(left).isdisjoint(right):
                        if i < j:
                            t3 += 1
                        continue
                    overlapping_distinct += 1
                    continue
                repeat_residue += left_weight * right_weight

    if trivial != trivial_term(n):
        raise AssertionError((p, n, trivial, trivial_term(n)))
    if overlapping_distinct:
        raise AssertionError((p, n, "overlapping distinct same-signature triples"))
    if moment != trivial + 72 * t3 + repeat_residue:
        raise AssertionError((p, n, moment, trivial, 72 * t3, repeat_residue))

    subset_buckets: dict[tuple[int, int], list[tuple[int, int, int]]] = defaultdict(list)
    for idxs in combinations(range(n), 3):
        key = signature(tuple(vals[i] for i in idxs), p)
        subset_buckets[key].append(idxs)
    direct_t3 = 0
    for subsets in subset_buckets.values():
        for i, left in enumerate(subsets):
            for right in subsets[i + 1 :]:
                if set(left).isdisjoint(right):
                    direct_t3 += 1
    if direct_t3 != t3:
        raise AssertionError((p, n, direct_t3, t3))

    return {
        "moment": moment,
        "trivial": trivial,
        "t3": t3,
        "seventy_two_t3": 72 * t3,
        "repeat_residue": repeat_residue,
        "signature_buckets": len(multiset_buckets),
    }


def main() -> None:
    rows = (
        (97, 16),
        (97, 32),
        (193, 64),
    )
    print("h=3 moment bookkeeping identity")
    for p, n in rows:
        row = verify_row(p, n)
        print(
            f"p={p} n={n} buckets={row['signature_buckets']} "
            f"M={row['moment']} trivial={row['trivial']} "
            f"72T3={row['seventy_two_t3']} repeat_residue={row['repeat_residue']}"
        )
    print("M = trivial + 72*T3 + repeat_residue")
    print("H3_MOMENT_BOOKKEEPING_IDENTITY_PASS")


if __name__ == "__main__":
    main()
