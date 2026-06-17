#!/usr/bin/env python3
"""Verify the one-remainder-fiber M1 quotient exchange profile.

This checks the closed fixed-support enumerator in
experimental/m1_quotient_periodic_overlap_profile.md against brute-force
enumeration for small quotient partitions.
"""

from collections import Counter
from itertools import combinations
from math import comb


def choose(n, k):
    if k < 0 or k > n:
        return 0
    return comb(n, k)


def add_term(poly, coeff, exponent):
    if coeff:
        poly[exponent] += coeff


def formula_enumerator(N, m, L, r):
    poly = Counter()

    for h in range(0, L + 1):
        for ell in range(0, r + 1):
            coeff = choose(L, h) * choose(N - L - 1, h)
            coeff *= choose(r, ell) * choose(m - r, ell)
            add_term(poly, coeff, h * m + ell)

    for h in range(0, L):
        coeff = L * choose(m, r) * choose(L - 1, h) * choose(N - L - 1, h)
        add_term(poly, coeff, h * m + m - r)

    for h in range(0, L):
        coeff = L * choose(m, r) * choose(L - 1, h)
        coeff *= choose(N - L - 1, h + 1)
        add_term(poly, coeff, (h + 1) * m)

    for h in range(1, L + 1):
        coeff = (N - L - 1) * choose(m, r) * choose(L, h)
        coeff *= choose(N - L - 2, h - 1)
        add_term(poly, coeff, h * m)

    for h in range(0, L + 1):
        coeff = (N - L - 1) * choose(m, r) * choose(L, h)
        coeff *= choose(N - L - 2, h)
        add_term(poly, coeff, h * m + r)

    return +poly


def support(fibers, whole_indices, partial_index, partial_points):
    out = set()
    for index in whole_indices:
        out.update(fibers[index])
    out.update(partial_points)
    return frozenset(out)


def remainder_family(N, m, L, r):
    fibers = [
        tuple((fiber_index, point_index) for point_index in range(m))
        for fiber_index in range(N)
    ]
    family = []
    for whole_indices in combinations(range(N), L):
        whole_set = set(whole_indices)
        for partial_index in range(N):
            if partial_index in whole_set:
                continue
            for partial_points in combinations(fibers[partial_index], r):
                family.append(
                    support(fibers, whole_indices, partial_index, partial_points)
                )
    return family


def brute_enumerator(N, m, L, r):
    family = remainder_family(N, m, L, r)
    fixed = family[0]
    return Counter(len(fixed - other) for other in family)


def verify_case(N, m, L, r):
    brute = brute_enumerator(N, m, L, r)
    formula = formula_enumerator(N, m, L, r)
    assert brute == formula, (N, m, L, r, brute, formula)
    family_size = choose(N, L) * (N - L) * choose(m, r)
    assert sum(formula.values()) == family_size
    return family_size, formula


def main():
    cases = [
        (5, 4, 1, 1),
        (5, 4, 2, 1),
        (6, 3, 2, 1),
        (6, 5, 2, 2),
        (7, 4, 3, 2),
    ]
    for case in cases:
        family_size, enumerator = verify_case(*case)
        print(f"N,m,L,r={case}: |A_REM|={family_size}, H={dict(sorted(enumerator.items()))}")
    print("M1 quotient remainder profile verifier passed")


if __name__ == "__main__":
    main()
