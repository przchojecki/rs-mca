#!/usr/bin/env python3
"""Replay checks for the F2 arc-class recursion note."""

from __future__ import annotations

import cmath
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb, log2


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


def value_counts(q: int, n: int, b: int) -> Counter[tuple[int, int]]:
    domain = root_domain(q, n)
    counts: Counter[tuple[int, int]] = Counter()
    for subset in combinations(domain, b):
        p1 = sum(subset) % q
        p2 = sum((x * x) % q for x in subset) % q
        counts[(p1, p2)] += 1
    return counts


def arc_sum(
    counts: Counter[tuple[int, int]],
    roots: list[complex],
    q: int,
    lambdas: list[tuple[int, int]],
) -> complex:
    zeta = cmath.exp(2j * cmath.pi / q)
    assert abs(roots[1] - zeta) < 1e-14
    total = 0j
    for lam1, lam2 in lambdas:
        for (p1, p2), count in counts.items():
            total += count * roots[(lam1 * p1 + lam2 * p2) % q]
    return total


def check_cell(q: int, n: int, b: int) -> dict[str, object]:
    counts = value_counts(q, n, b)
    total = comb(n, b)
    n1 = sum(count for (p1, _), count in counts.items() if p1 == 0)
    n2 = sum(count for (_, p2), count in counts.items() if p2 == 0)
    n12 = counts[(0, 0)]
    sp = sum(count * count for count in counts.values())

    roots = [cmath.exp(2j * cmath.pi * r / q) for r in range(q)]
    linear = arc_sum(counts, roots, q, [(l1, 0) for l1 in range(q)])
    quadratic = arc_sum(counts, roots, q, [(0, l2) for l2 in range(q)])
    all_arcs = arc_sum(counts, roots, q, [(l1, l2) for l1 in range(q) for l2 in range(q)])
    generic = arc_sum(counts, roots, q, [(l1, l2) for l1 in range(1, q) for l2 in range(1, q)])

    tol = 1e-6
    assert abs(linear.real - q * n1) < tol and abs(linear.imag) < tol
    assert abs(quadratic.real - q * n2) < tol and abs(quadratic.imag) < tol
    assert abs(all_arcs.real - q * q * n12) < tol and abs(all_arcs.imag) < tol

    generic_expected = (
        Fraction(n12, 1)
        - Fraction(n1, q)
        - Fraction(n2, q)
        + Fraction(total, q * q)
    )
    generic_normalized = generic / (q * q)
    assert abs(generic_normalized.real - float(generic_expected)) < tol
    assert abs(generic_normalized.imag) < tol

    if q <= 31:
        # Parseval identity in value-fiber form. Keep this numerical check only
        # on cheap cells so the verifier remains a lightweight replay.
        parseval_lhs = 0.0
        for l1 in range(q):
            for l2 in range(q):
                eb = 0j
                for (p1, p2), count in counts.items():
                    eb += count * roots[(l1 * p1 + l2 * p2) % q]
                parseval_lhs += abs(eb) ** 2
        assert abs(parseval_lhs - q * q * sp) < 1e-5, (parseval_lhs, q * q * sp)

    assert sp >= total

    return {
        "q": q,
        "n": n,
        "b": b,
        "states": len(counts),
        "total": total,
        "N1": n1,
        "N2": n2,
        "N12": n12,
        "SP": sp,
        "generic_normalized": f"{generic_expected.numerator}/{generic_expected.denominator}",
        "sqrt_total_bits": log2(total) / 2.0,
    }


def main() -> None:
    cells = [
        (17, 16, 4),
        (17, 16, 8),
        (31, 30, 4),
        (97, 16, 3),
    ]
    for q, n, b in cells:
        row = check_cell(q, n, b)
        print(
            f"q={q} n={n} b={b}: states={row['states']} total={row['total']} "
            f"N1={row['N1']} N2={row['N2']} N12={row['N12']} "
            f"generic/q^2={row['generic_normalized']} "
            f"sqrt(total)_bits={row['sqrt_total_bits']:.4f}"
        )

    print("F2_ARCCLASS_RECURSION_PASS")


if __name__ == "__main__":
    main()
