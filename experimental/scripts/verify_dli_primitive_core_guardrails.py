#!/usr/bin/env python3
"""Replay lightweight checks for the DLI primitive-core guardrail packet."""

from __future__ import annotations

import cmath
import itertools
import math
from fractions import Fraction

import sympy as sp


def primitive_root_of_order(p: int, n: int) -> int:
    assert (p - 1) % n == 0
    g = int(sp.primitive_root(p))
    z = pow(g, (p - 1) // n, p)
    assert pow(z, n, p) == 1
    assert pow(z, n // 2, p) != 1
    return z


def powersum(indices: set[int], n: int, p: int, zeta: int, r: int) -> int:
    return sum(pow(zeta, (r * i) % n, p) for i in indices) % p


def rank_mod(matrix: list[list[int]], p: int) -> int:
    rows = [row[:] for row in matrix if any(x % p for x in row)]
    if not rows:
        return 0
    m, n = len(rows), len(rows[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        pivot = None
        for i in range(rank, m):
            if rows[i][col] % p:
                pivot = i
                break
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % p, -1, p)
        rows[rank] = [(x * inv) % p for x in rows[rank]]
        for i in range(m):
            if i == rank:
                continue
            factor = rows[i][col] % p
            if factor:
                rows[i] = [
                    (x - factor * y) % p for x, y in zip(rows[i], rows[rank])
                ]
        rank += 1
        col += 1
    return rank


def check_complement_duality() -> None:
    p, n = 97, 32
    zeta = primitive_root_of_order(p, n)
    universe = set(range(n))
    for r in range(1, n):
        assert powersum(universe, n, p, zeta, r) == 0
    subset = {0, 2, 5, 9, 17, 24}
    comp = universe - subset
    for r in range(1, 9):
        assert (powersum(subset, n, p, zeta, r) + powersum(comp, n, p, zeta, r)) % p == 0


def check_dyadic_pushforward_and_skew() -> None:
    p, n = 97, 32
    zeta = primitive_root_of_order(p, n)
    subset = {0, 3, 6, 11, 17, 18, 23, 29}

    for j in (1, 2):
        quotient_n = n // (1 << j)
        zeta_q = pow(zeta, 1 << j, p)
        multiplicities = [0] * quotient_n
        for i in subset:
            multiplicities[i % quotient_n] += 1
        assert all(0 <= m <= (1 << j) for m in multiplicities)
        for s in range(1, 5):
            lhs = sum(m * pow(zeta_q, (s * i) % quotient_n, p) for i, m in enumerate(multiplicities)) % p
            rhs = powersum(subset, n, p, zeta, (1 << j) * s)
            assert lhs == rhs

    half = n // 2
    skew = []
    for i in range(half):
        skew.append((1 if i in subset else 0) - (1 if i + half in subset else 0))
    for s in range(0, 6):
        r = 2 * s + 1
        lhs = sum(d * pow(zeta, (r * i) % n, p) for i, d in enumerate(skew)) % p
        rhs = powersum(subset, n, p, zeta, r)
        assert lhs == rhs


def check_near_tail_arithmetic() -> None:
    n = 2**41
    t = 2**33 + 1
    total = Fraction(0, 1)
    for k in range(1, 16):
        bound = Fraction(math.comb(n, k), math.comb(t + k, k))
        assert bound < 2 ** (8 * k)
        total += Fraction(2 ** (8 * k), 1)
    assert 2 * total < 2**122


def check_vandermonde_threshold() -> None:
    p, n, L = 97, 32, 4
    zeta = primitive_root_of_order(p, n)
    section = [pow(zeta, i, p) for i in range(n // 2)]
    for size in range(1, L + 1):
        for support in itertools.combinations(range(n // 2), size):
            matrix = [
                [pow(section[i], 2 * ell - 1, p) for i in support]
                for ell in range(1, L + 1)
            ]
            assert rank_mod(matrix, p) == size


def check_resultant_gate_example() -> None:
    p, m = 97, 16
    omega = primitive_root_of_order(p, m)
    x = sp.symbols("x")
    q_poly = -(x**5) - 2 * x - 2
    assert sum(
        int(coeff) * pow(omega, int(exp[0]), p)
        for exp, coeff in sp.Poly(q_poly, x).terms()
    ) % p == 0
    resultant = int(sp.resultant(x ** (m // 2) + 1, q_poly, x))
    assert resultant == 1649
    assert resultant % p == 0
    assert resultant != 0


def check_d3_identity() -> None:
    p, n, levels = 17, 8, 2
    omega = 3  # order 16 modulo 17
    roots = [pow(omega, 2 * a + 1, p) for a in range(n)]

    def phi(vec: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(
            sum(di * pow(r, 2 * ell - 1, p) for di, r in zip(vec, roots)) % p
            for ell in range(1, levels + 1)
        )

    def fourier_term(lam: tuple[int, ...], domains: list[list[int]]) -> complex:
        product = 1 + 0j
        for domain, root in zip(domains, roots):
            a = sum(lam[ell - 1] * pow(root, 2 * ell - 1, p) for ell in range(1, levels + 1)) % p
            product *= sum(cmath.exp(2j * math.pi * ((a * u) % p) / p) for u in domain) / len(domain)
        return product

    for domains in ([[-1, 1]] * n, [[-2, 0, 2]] * n):
        universe = list(itertools.product(*domains))
        zero_count = sum(1 for vec in universe if phi(vec) == (0,) * levels)
        rho = (p**levels) * zero_count / math.prod(len(domain) for domain in domains)
        fourier = sum(
            fourier_term(lam, domains)
            for lam in itertools.product(range(p), repeat=levels)
        )
        assert abs(fourier.real - rho) < 1e-8
        assert abs(fourier.imag) < 1e-8


def main() -> int:
    checks = [
        ("complement_duality", check_complement_duality),
        ("dyadic_pushforward_and_skew", check_dyadic_pushforward_and_skew),
        ("near_tail_arithmetic", check_near_tail_arithmetic),
        ("vandermonde_threshold", check_vandermonde_threshold),
        ("resultant_gate_example", check_resultant_gate_example),
        ("d3_weighted_identity", check_d3_identity),
    ]
    for name, check in checks:
        check()
        print(f"{name}: PASS")
    print("DLI_PRIMITIVE_CORE_GUARDRAILS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
