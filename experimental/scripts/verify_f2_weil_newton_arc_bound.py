#!/usr/bin/env python3
"""Replay checks for the F2 Weil-Newton arc bound.

The script verifies the bound on small dyadic root-domain cells. It is a replay
and sanity check, not a proof of the external Weil theorem.
"""

from __future__ import annotations

import cmath
from collections import Counter
from itertools import combinations
from math import comb, sqrt


def prime_factors(n: int) -> set[int]:
    out: set[int] = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def primitive_root(q: int) -> int:
    factors = prime_factors(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // r, q) != 1 for r in factors):
            return g
    raise ValueError(f"no primitive root found for {q}")


def root_domain(q: int, n: int) -> list[int]:
    assert (q - 1) % n == 0
    g = primitive_root(q)
    h = pow(g, (q - 1) // n, q)
    return sorted(pow(h, i, q) for i in range(n))


def value_counts(domain: list[int], q: int, b: int) -> Counter[tuple[int, int]]:
    counts: Counter[tuple[int, int]] = Counter()
    squares = {x: (x * x) % q for x in domain}
    for subset in combinations(domain, b):
        p1 = sum(subset) % q
        p2 = sum(squares[x] for x in subset) % q
        counts[(p1, p2)] += 1
    return counts


def W_bound(q: int, b: int) -> float:
    m = 2.0 * sqrt(q)
    out = 1.0
    for a in range(b):
        out *= (m + a) / (a + 1)
    return out


def check_cell(q: int, n: int, b: int) -> dict[str, object]:
    domain = root_domain(q, n)
    counts = value_counts(domain, q, b)
    roots = [cmath.exp(2j * cmath.pi * r / q) for r in range(q)]
    M = 2.0 * sqrt(q)
    W = W_bound(q, b)

    max_first_moment = 0.0
    for r in range(1, b + 1):
        for l1 in range(q):
            for l2 in range(q):
                if l1 == 0 and l2 == 0:
                    continue
                rl1 = (r * l1) % q
                rl2 = (r * l2) % q
                total = 0j
                for x in domain:
                    total += roots[(rl1 * x + rl2 * x * x) % q]
                max_first_moment = max(max_first_moment, abs(total))
                assert abs(total) <= M + 1e-9, (q, n, b, r, l1, l2, abs(total), M)

    max_arc = 0.0
    for l1 in range(q):
        for l2 in range(q):
            if l1 == 0 and l2 == 0:
                continue
            total = 0j
            for (p1, p2), count in counts.items():
                total += count * roots[(l1 * p1 + l2 * p2) % q]
            max_arc = max(max_arc, abs(total))
            assert abs(total) <= W + 1e-7, (q, n, b, l1, l2, abs(total), W)

    zero_count = counts[(0, 0)]
    inversion_bound = comb(n, b) / (q * q) + W
    assert zero_count <= inversion_bound + 1e-7

    return {
        "q": q,
        "n": n,
        "b": b,
        "states": len(counts),
        "zero_count": zero_count,
        "max_first_moment": max_first_moment,
        "M": M,
        "max_arc": max_arc,
        "W": W,
        "inversion_bound": inversion_bound,
    }


def main() -> None:
    cells = [
        (17, 16, 4),
        (17, 16, 8),
        (97, 16, 3),
        (97, 32, 3),
        (193, 32, 2),
    ]
    for q, n, b in cells:
        row = check_cell(q, n, b)
        print(
            f"q={q} n={n} b={b}: states={row['states']} zero={row['zero_count']} "
            f"max_p_r={row['max_first_moment']:.6g} <= {row['M']:.6g}; "
            f"max_arc={row['max_arc']:.6g} <= W={row['W']:.6g}; "
            f"inversion_bound={row['inversion_bound']:.6g}"
        )
    print("F2_WEIL_NEWTON_ARC_BOUND_PASS")


if __name__ == "__main__":
    main()
