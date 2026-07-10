#!/usr/bin/env python3
"""Exact coset-level replay for the Terminal B h=2 energy upgrade."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass


def is_prime(m: int) -> bool:
    if m < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for a in small:
        if m % a == 0:
            return m == a
    d, r = m - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in small:
        if a >= m:
            continue
        x = pow(a, d, m)
        if x in (1, m - 1):
            continue
        for _ in range(r - 1):
            x = x * x % m
            if x == m - 1:
                break
        else:
            return False
    return True


def next_prime_1mod(n: int, lo: int) -> int:
    q = (lo // n) * n + 1
    while q <= lo or not is_prime(q):
        q += n
    return q


def primitive_root_of_order(q: int, n: int) -> int:
    assert (q - 1) % n == 0
    for cand in range(2, q):
        x = pow(cand, (q - 1) // n, q)
        if x == 1:
            continue
        y, order = x, 1
        while y != 1:
            y = y * x % q
            order += 1
            if order > n:
                break
        if order == n:
            return x
    raise RuntimeError(f"no primitive {n}-th root modulo {q}")


@dataclass(frozen=True)
class LevelRow:
    n: int
    q: int
    regime: int
    positive_cosets: int
    max_r: int
    sum_r: int
    coset_l2: int
    energy: int
    coset_l2_ratio: float
    energy_ratio: float
    levels: tuple[tuple[int, int], ...]


def level_row(n: int, regime: int) -> LevelRow:
    q = next_prime_1mod(n, n**regime)
    zeta = primitive_root_of_order(q, n)
    domain = [pow(zeta, i, q) for i in range(n)]

    diff_counts: dict[int, int] = {}
    for x in domain:
        for y in domain:
            if x == y:
                continue
            s = (x - y) % q
            diff_counts[s] = diff_counts.get(s, 0) + 1

    visited: set[int] = set()
    coset_counts = []
    for s in sorted(diff_counts):
        if s in visited:
            continue
        coset = {(s * h) % q for h in domain}
        if len(coset) != n:
            raise AssertionError((n, q, s, len(coset)))
        values = {diff_counts.get(t, 0) for t in coset}
        if len(values) != 1:
            raise AssertionError((n, q, s, sorted(values)))
        r = values.pop()
        if r <= 0:
            raise AssertionError((n, q, s, r))
        visited.update(coset)
        coset_counts.append(r)

    if visited != set(diff_counts):
        raise AssertionError((n, q, len(visited), len(diff_counts)))
    sum_r = sum(coset_counts)
    if sum_r != n - 1:
        raise AssertionError((n, q, sum_r, n - 1))

    coset_l2 = sum(r * r for r in coset_counts)
    energy = n * n + n * coset_l2

    # Direct ordered difference-energy check.
    direct_energy = n * n + sum(v * v for v in diff_counts.values())
    if direct_energy != energy:
        raise AssertionError((n, q, direct_energy, energy))

    levels = Counter((r.bit_length() - 1) for r in coset_counts)
    return LevelRow(
        n=n,
        q=q,
        regime=regime,
        positive_cosets=len(coset_counts),
        max_r=max(coset_counts),
        sum_r=sum_r,
        coset_l2=coset_l2,
        energy=energy,
        coset_l2_ratio=coset_l2 / (n**1.5),
        energy_ratio=energy / (n**2.5),
        levels=tuple(sorted(levels.items())),
    )


def main() -> None:
    ns = (16, 32, 64, 128, 256, 512, 1024, 2048)
    rows = [level_row(n, regime) for n in ns for regime in (2, 3)]
    print("h=2 coset-level energy rows:")
    print(
        "   n regime        q cosets max_r sum_r   coset_l2"
        "  l2/n^1.5  E/n^2.5  levels"
    )
    for row in rows:
        level_text = ",".join(f"2^{j}:{count}" for j, count in row.levels)
        print(
            f"{row.n:4d}   n^{row.regime:<1d} {row.q:8d}"
            f" {row.positive_cosets:6d} {row.max_r:5d} {row.sum_r:5d}"
            f" {row.coset_l2:10d} {row.coset_l2_ratio:9.4f}"
            f" {row.energy_ratio:9.4f}  {level_text}"
        )
    max_l2 = max(row.coset_l2_ratio for row in rows)
    max_energy = max(row.energy_ratio for row in rows)
    if max_l2 > 1 or max_energy > 1:
        raise AssertionError((max_l2, max_energy))
    print(f"max coset_l2 / n^1.5 = {max_l2:.4f}")
    print(f"max E(H) / n^2.5 = {max_energy:.4f}")
    print("H2_LEVEL_SET_REPLAY_PASS")


if __name__ == "__main__":
    main()
