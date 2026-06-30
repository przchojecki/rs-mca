#!/usr/bin/env python3
"""Verify the M1 t=2 one-exchange residual-degree identities.

This is a focused checker for
experimental/notes/m1/m1_t2_one_exchange_residual_degree.md.  It checks local
finite-field algebra and small Johnson-graph combinatorics.  It does not scan
MCA bad slopes and does not prove the global M1 local limit.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import comb
from random import Random


PRIMES = (3, 5, 7, 11)


def det2(left: tuple[int, int], right: tuple[int, int], p: int) -> int:
    return (left[0] * right[1] - left[1] * right[0]) % p


def vec_add(left: tuple[int, int], right: tuple[int, int], p: int) -> tuple[int, int]:
    return ((left[0] + right[0]) % p, (left[1] + right[1]) % p)


def vec_scale(a: int, vector: tuple[int, int], p: int) -> tuple[int, int]:
    return ((a * vector[0]) % p, (a * vector[1]) % p)


def affine_vec(
    constant: tuple[int, int], direction: tuple[int, int], y: int, p: int
) -> tuple[int, int]:
    return ((constant[0] - y * direction[0]) % p, (constant[1] - y * direction[1]) % p)


def determinant_coefficients(
    a_x: tuple[int, int],
    a_0: tuple[int, int],
    b_x: tuple[int, int],
    b_0: tuple[int, int],
    p: int,
) -> tuple[int, int, int]:
    constant = det2(a_x, b_x, p)
    linear = (-(det2(a_0, b_x, p) + det2(a_x, b_0, p))) % p
    quadratic = det2(a_0, b_0, p)
    return constant, linear, quadratic


def poly_eval(coeffs: tuple[int, int, int], y: int, p: int) -> int:
    return (coeffs[0] + coeffs[1] * y + coeffs[2] * y * y) % p


def check_determinant_gate() -> int:
    checked = 0
    rng = Random(20260630)
    for p in PRIMES:
        vectors = list(product(range(p), repeat=2))
        exhaustive = p <= 5
        if exhaustive:
            samples = product(vectors, vectors, vectors, vectors)
        else:
            samples = (
                (
                    tuple(rng.randrange(p) for _ in range(2)),
                    tuple(rng.randrange(p) for _ in range(2)),
                    tuple(rng.randrange(p) for _ in range(2)),
                    tuple(rng.randrange(p) for _ in range(2)),
                )
                for _ in range(2000)
            )

        for a_x, a_0, b_x, b_0 in samples:
            coeffs = determinant_coefficients(a_x, a_0, b_x, b_0, p)
            roots: list[int] = []
            for y in range(p):
                a_y = affine_vec(a_x, a_0, y, p)
                b_y = affine_vec(b_x, b_0, y, p)
                direct = det2(a_y, b_y, p)
                expanded = poly_eval(coeffs, y, p)
                assert direct == expanded, (p, a_x, a_0, b_x, b_0, y, direct, expanded)
                if direct == 0:
                    roots.append(y)

            if coeffs != (0, 0, 0):
                assert len(roots) <= 2, (p, coeffs, roots)
            else:
                assert len(roots) == p, (p, coeffs, roots)
            checked += 1
    return checked


def hankel_pair(triple: tuple[int, int, int], y: int, p: int) -> tuple[int, int]:
    c0, c1, c2 = triple
    return ((c1 - y * c0) % p, (c2 - y * c1) % p)


def ruled_coefficients(
    a: tuple[int, int, int], b: tuple[int, int, int], p: int
) -> tuple[int, int, int]:
    a0, a1, a2 = a
    b0, b1, b2 = b
    return (
        (a1 * b2 - a2 * b1) % p,
        (a2 * b0 - a0 * b2) % p,
        (a0 * b1 - a1 * b0) % p,
    )


def fixed_slope_or_inactive(
    a: tuple[int, int, int], b: tuple[int, int, int], p: int
) -> tuple[str, int | None]:
    if all(entry % p == 0 for entry in b):
        return "inactive", None
    pivot = next(idx for idx, entry in enumerate(b) if entry % p)
    z = (-a[pivot] * pow(b[pivot], -1, p)) % p
    assert all((ai + z * bi) % p == 0 for ai, bi in zip(a, b)), (p, a, b, z)
    return "fixed", z


def check_hankel_ruled_collapse() -> int:
    checked = 0
    rng = Random(20260630)
    for p in PRIMES:
        triples = list(product(range(p), repeat=3))
        if p <= 7:
            samples = product(triples, triples)
        else:
            samples = (
                (
                    tuple(rng.randrange(p) for _ in range(3)),
                    tuple(rng.randrange(p) for _ in range(3)),
                )
                for _ in range(12000)
            )
        for a, b in samples:
            coeffs = ruled_coefficients(a, b, p)
            roots = [
                y
                for y in range(p)
                if det2(hankel_pair(a, y, p), hankel_pair(b, y, p), p) == 0
            ]
            assert all(poly_eval(coeffs, y, p) == 0 for y in roots)
            if coeffs != (0, 0, 0):
                assert len(roots) <= 2, (p, a, b, coeffs, roots)
                checked += 1
                continue

            assert len(roots) == p, (p, a, b, roots)
            status, z = fixed_slope_or_inactive(a, b, p)
            if status == "inactive":
                assert all(hankel_pair(b, y, p) == (0, 0) for y in range(p))
            else:
                assert z is not None
                for y in range(p):
                    collapsed = vec_add(
                        hankel_pair(a, y, p),
                        vec_scale(z, hankel_pair(b, y, p), p),
                        p,
                    )
                    assert collapsed == (0, 0), (p, a, b, z, y, collapsed)
            checked += 1
    return checked


def check_residual_degree_bound() -> int:
    checked = 0
    for n in range(3, 10):
        points = tuple(range(n))
        for j in range(1, n):
            supports = [frozenset(c) for c in combinations(points, j)]
            support_index = {support: idx for idx, support in enumerate(supports)}
            edges: set[tuple[int, int]] = set()
            core_count = 0
            for core in combinations(points, j - 1):
                core_set = frozenset(core)
                anchors = [point for point in points if point not in core_set]
                # Worst residual case after the local theorem: each core can
                # carry at most two anchors, hence at most one edge.
                if len(anchors) >= 2:
                    left = support_index[core_set | {anchors[0]}]
                    right = support_index[core_set | {anchors[1]}]
                    edges.add(tuple(sorted((left, right))))
                core_count += 1

            degrees = [0] * len(supports)
            for left, right in edges:
                degrees[left] += 1
                degrees[right] += 1

            assert max(degrees, default=0) <= j, (n, j, max(degrees))
            assert 2 * len(edges) <= j * len(supports), (n, j, len(edges))
            assert len(edges) <= core_count, (n, j, len(edges), core_count)
            checked += 1
    return checked


def check_average_collinearity_substitution() -> int:
    checked = 0
    for q in (5, 7, 17, 31):
        p_z = Fraction(q * q - 1, q**4)
        for locator_degree in range(1, 10):
            for family_size in (1, 2, 5, 25, 100, 1000):
                for delta_g1 in range(locator_degree + 1):
                    ledger = (
                        Fraction(1, 1) - p_z
                    ) / (family_size * p_z) + Fraction(4 * delta_g1 * q, family_size)
                    bound = (
                        Fraction(1, 1) - p_z
                    ) / (family_size * p_z) + Fraction(
                        4 * locator_degree * q, family_size
                    )
                    assert ledger <= bound, (
                        q,
                        locator_degree,
                        family_size,
                        delta_g1,
                        ledger,
                        bound,
                    )
                    checked += 1
    return checked


def main() -> None:
    det_checks = check_determinant_gate()
    ruled_checks = check_hankel_ruled_collapse()
    degree_checks = check_residual_degree_bound()
    average_checks = check_average_collinearity_substitution()

    print("M1 t=2 one-exchange residual-degree verifier passed")
    print(f"  determinant-gate checks: {det_checks}")
    print(f"  Hankel ruled-core checks: {ruled_checks}")
    print(f"  residual degree checks: {degree_checks}")
    print(f"  average-ledger substitution checks: {average_checks}")


if __name__ == "__main__":
    main()
