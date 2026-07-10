#!/usr/bin/env python3
"""Exact checks for the row-sharp Q / Myerson bridge.

The script verifies two algebraic joints used by
rowsharp_q_myerson_summit_bridge.md:

1. Habegger/Myerson subgroup-census identity in Z[zeta_p], computed exactly
   as Z[X]/Phi_p(X), not numerically.
2. The zero-prefix Newton/divisor dictionary for small mu_n rows, with two
   independent dynamic programs.
"""

from __future__ import annotations

from collections import defaultdict
from math import comb


def prime_factors(x: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= x:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    if x > 1:
        out.append(x)
    return out


def primitive_root(p: int) -> int:
    factors = set(prime_factors(p - 1))
    for cand in range(2, p):
        if all(pow(cand, (p - 1) // r, p) != 1 for r in factors):
            return cand
    raise AssertionError(f"no primitive root found for p={p}")


def subgroup_of_order(p: int, order: int) -> list[int]:
    assert (p - 1) % order == 0
    g = primitive_root(p)
    h = pow(g, (p - 1) // order, p)
    return sorted(pow(h, i, p) for i in range(order))


def coset_representatives(p: int, group: list[int]) -> list[int]:
    used: set[int] = set()
    reps: list[int] = []
    for a in range(1, p):
        if a in used:
            continue
        reps.append(a)
        used.update((a * g) % p for g in group)
    assert len(used) == p - 1
    return reps


def linear_zero_count(p: int, group: list[int], reps: list[int]) -> int:
    """Count sum_i A_i x_i = 0 with x_i in group by exact DP."""
    dp: dict[int, int] = {0: 1}
    for a in reps:
        new: defaultdict[int, int] = defaultdict(int)
        for s, count in dp.items():
            for x in group:
                new[(s + a * x) % p] += count
        dp = dict(new)
    return dp.get(0, 0)


def circular_mul_mod_xp_minus_1(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * p
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj:
                out[(i + j) % p] += ai * bj
    return out


def gaussian_period_product_basis(
    p: int, group: list[int], reps: list[int]
) -> list[int]:
    """Return Delta_G in the basis 1,zeta,...,zeta^{p-2}.

    First multiply in Z[X]/(X^p - 1), then reduce by
    Phi_p(X)=1+X+...+X^{p-1}.  If the product is rational, every
    nonconstant basis coordinate is zero.
    """
    poly = [1] + [0] * (p - 1)
    for t in reps:
        period = [0] * p
        for g in group:
            period[(t * g) % p] += 1
        poly = circular_mul_mod_xp_minus_1(poly, period, p)

    top = poly[p - 1]
    return [poly[i] - top for i in range(p - 1)]


def verify_myerson_identity() -> None:
    rows = [(7, 3), (13, 3), (17, 4), (17, 8), (19, 3), (31, 5)]
    for p, order in rows:
        group = subgroup_of_order(p, order)
        reps = coset_representatives(p, group)
        index = len(reps)
        count = linear_zero_count(p, group, reps)
        basis = gaussian_period_product_basis(p, group, reps)
        delta = basis[0]
        assert all(c == 0 for c in basis[1:]), (p, order, basis)
        assert p * count - order**index == (p - 1) * delta, (
            p,
            order,
            count,
            delta,
        )
        print(
            "myerson",
            f"p={p}",
            f"|G|={order}",
            f"index={index}",
            f"N={count}",
            f"Delta={delta}",
        )


def mu_n(p: int, n: int) -> list[int]:
    assert (p - 1) % n == 0
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    return sorted(pow(h, i, p) for i in range(n))


def power_sum_zero_count(p: int, domain: list[int], b: int, depth: int) -> int:
    dp: dict[tuple[int, ...], list[int]] = {(0,) * depth: [1] + [0] * b}
    for x in domain:
        powers = [pow(x, e, p) for e in range(1, depth + 1)]
        new: dict[tuple[int, ...], list[int]] = {}
        for state, sizes in dp.items():
            keep = new.setdefault(state, [0] * (b + 1))
            for size, count in enumerate(sizes):
                keep[size] += count
            state2 = tuple((state[i] + powers[i]) % p for i in range(depth))
            take = new.setdefault(state2, [0] * (b + 1))
            for size in range(b):
                if sizes[size]:
                    take[size + 1] += sizes[size]
        dp = new
    assert sum(v[b] for v in dp.values()) == comb(len(domain), b)
    return dp.get((0,) * depth, [0] * (b + 1))[b]


def locator_zero_count(p: int, domain: list[int], b: int, depth: int) -> int:
    """Track top locator coefficients of prod_{x in S}(X-x)."""
    dp: dict[tuple[int, ...], list[int]] = {(0,) * depth: [1] + [0] * b}
    for x in domain:
        new: dict[tuple[int, ...], list[int]] = {}
        for state, sizes in dp.items():
            keep = new.setdefault(state, [0] * (b + 1))
            for size, count in enumerate(sizes):
                keep[size] += count

            state2 = []
            prev = 1
            for i in range(depth):
                state2.append((state[i] - x * prev) % p)
                prev = state[i]
            state2_tuple = tuple(state2)
            take = new.setdefault(state2_tuple, [0] * (b + 1))
            for size in range(b):
                if sizes[size]:
                    take[size + 1] += sizes[size]
        dp = new
    assert sum(v[b] for v in dp.values()) == comb(len(domain), b)
    return dp.get((0,) * depth, [0] * (b + 1))[b]


def verify_zero_prefix_dictionary() -> None:
    rows = [(17, 16, 8, 4), (31, 30, 15, 3), (97, 32, 16, 2)]
    for p, n, b, max_depth in rows:
        domain = mu_n(p, n)
        counts: dict[int, int] = {}
        for depth in range(1, max_depth + 1):
            left = power_sum_zero_count(p, domain, b, depth)
            right = locator_zero_count(p, domain, b, depth)
            assert left == right, (p, n, b, depth, left, right)
            counts[depth] = left
        print("zero-prefix", f"p={p}", f"n={n}", f"b={b}", counts)


def main() -> None:
    verify_myerson_identity()
    verify_zero_prefix_dictionary()
    print("ROWSHARP_Q_MYERSON_BRIDGE_PASS")


if __name__ == "__main__":
    main()
