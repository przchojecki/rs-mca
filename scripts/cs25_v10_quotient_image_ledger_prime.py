#!/usr/bin/env python3
"""Exact quotient-branch line-image ledger for small prime-field rows.

This is a scanner prototype for the v10 milestone-3 gcd/lcm quotient-image
ledger.  It is intentionally small and transparent: it enumerates the quotient
support union, computes each co-support locator, applies the syndrome-locator
image map, and coalesces duplicate finite/projective line parameters.

The script is for sanity checks and certificate prototyping over prime fields.
It is not intended for cryptographic-size rows.

Example:
    python quotient_image_ledger_prime.py --p 97 --n 12 --k 6 --a 8 --divisors 2 3 4 --f-exp 9 --g-exp 7
"""
from __future__ import annotations

import argparse
import itertools
import math
import random
from collections import defaultdict
from typing import Iterable


def inv_mod(a: int, p: int) -> int:
    a %= p
    if a == 0:
        raise ZeroDivisionError("inverse of zero")
    return pow(a, p - 2, p)


def is_prime_trial(p: int) -> bool:
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    d = 3
    while d * d <= p:
        if p % d == 0:
            return False
        d += 2
    return True


def factor(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    if p == 2:
        return 1
    primes = factor(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // ell, p) != 1 for ell in primes):
            return g
    raise RuntimeError("no primitive root found")


def subgroup_domain(p: int, n: int, alpha: int = 1) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1 for the default multiplicative subgroup domain")
    g = primitive_root(p)
    omega = pow(g, (p - 1) // n, p)
    D = [(alpha * pow(omega, i, p)) % p for i in range(n)]
    if len(set(D)) != n:
        raise RuntimeError("domain generation failed")
    return D


def fibers_by_power(D: list[int], c: int, p: int) -> list[tuple[int, ...]]:
    buckets: dict[int, list[int]] = defaultdict(list)
    for i, x in enumerate(D):
        buckets[pow(x, c, p)].append(i)
    fibers = [tuple(sorted(v)) for v in buckets.values()]
    fibers.sort()
    if any(len(v) != c for v in fibers):
        raise ValueError(f"x -> x^{c} does not have fibers of size {c}; check c|n and domain")
    return fibers


def quotient_supports(D: list[int], p: int, a: int, divisors: list[int]) -> set[frozenset[int]]:
    n = len(D)
    all_idx = set(range(n))
    supports: set[frozenset[int]] = set()
    fiber_cache = {c: fibers_by_power(D, c, p) for c in divisors}
    for A in range(a, n + 1):
        for c in divisors:
            m, s = divmod(A, c)
            fibers = fiber_cache[c]
            if m > len(fibers):
                continue
            for chosen in itertools.combinations(range(len(fibers)), m):
                full = set()
                for idx in chosen:
                    full.update(fibers[idx])
                rest = sorted(all_idx - full)
                if s > len(rest):
                    continue
                for residual in itertools.combinations(rest, s):
                    S = frozenset(full | set(residual))
                    if len(S) == A:
                        supports.add(S)
    return supports


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def locator_coeffs(points: Iterable[int], p: int) -> tuple[int, ...]:
    coeff = [1]
    for x in points:
        coeff = poly_mul(coeff, [(-x) % p, 1], p)
    return tuple(coeff)


def lagrange_lambdas(D: list[int], p: int) -> list[int]:
    lambdas = []
    for i, x in enumerate(D):
        prod = 1
        for j, y in enumerate(D):
            if i != j:
                prod = (prod * (x - y)) % p
        lambdas.append(inv_mod(prod, p))
    return lambdas


def syndrome(values: list[int], D: list[int], lambdas: list[int], r: int, p: int) -> list[int]:
    syn = []
    for m in range(r):
        total = 0
        for lam, x, y in zip(lambdas, D, values):
            total = (total + lam * pow(x, m, p) * y) % p
        syn.append(total)
    return syn


def hankel_contract(syn: list[int], coeff: tuple[int, ...], t: int, p: int) -> tuple[int, ...]:
    j = len(coeff) - 1
    return tuple(sum(coeff[b] * syn[h + b] for b in range(j + 1)) % p for h in range(t))


def finite_slope(Avec: tuple[int, ...], Bvec: tuple[int, ...], p: int) -> int | None:
    pivot = next((i for i, b in enumerate(Bvec) if b % p != 0), None)
    if pivot is None:
        return None
    z = (-Avec[pivot] * inv_mod(Bvec[pivot], p)) % p
    if all((a + z * b) % p == 0 for a, b in zip(Avec, Bvec)):
        return z
    return None


def norm_projective(alpha: int, beta: int, p: int) -> tuple[int, int]:
    alpha %= p
    beta %= p
    if alpha == 0 and beta == 0:
        raise ValueError("zero projective pair")
    if alpha != 0:
        inv = inv_mod(alpha, p)
        return (1, beta * inv % p)
    inv = inv_mod(beta, p)
    return (0, 1)


def projective_param(Avec: tuple[int, ...], Bvec: tuple[int, ...], p: int) -> tuple[int, int] | None:
    if all(a == 0 for a in Avec) and all(b == 0 for b in Bvec):
        return None
    if all(b == 0 for b in Bvec):
        return (0, 1)
    z = finite_slope(Avec, Bvec, p)
    if z is not None:
        return (1, z)
    # remaining possibility: B nonzero, but projectively dependent with alpha=0 impossible
    return None


def line_values(args: argparse.Namespace, D: list[int], p: int) -> tuple[list[int], list[int]]:
    if args.random_line:
        rng = random.Random(args.seed)
        return ([rng.randrange(p) for _ in D], [rng.randrange(p) for _ in D])
    f_exp = args.f_exp
    g_exp = args.g_exp
    return ([pow(x, f_exp, p) for x in D], [pow(x, g_exp, p) for x in D])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--p", type=int, required=True, help="prime field size")
    ap.add_argument("--n", type=int, required=True, help="multiplicative subgroup size")
    ap.add_argument("--k", type=int, required=True, help="RS dimension")
    ap.add_argument("--a", type=int, required=True, help="agreement threshold")
    ap.add_argument("--divisors", type=int, nargs="+", required=True, help="quotient divisors c|n")
    ap.add_argument("--alpha", type=int, default=1, help="multiplicative coset shift")
    ap.add_argument("--f-exp", type=int, default=9, help="monomial exponent for f")
    ap.add_argument("--g-exp", type=int, default=7, help="monomial exponent for g")
    ap.add_argument("--random-line", action="store_true", help="use random f,g values instead of monomials")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--max-supports", type=int, default=2_000_000, help="safety cap")
    args = ap.parse_args()

    p, n, k, a = args.p, args.n, args.k, args.a
    if not is_prime_trial(p):
        raise SystemExit("--p must be prime for this prototype")
    if not (0 < k <= a <= n):
        raise SystemExit("need 0 < k <= a <= n")
    if any(n % c != 0 or c <= 0 for c in args.divisors):
        raise SystemExit("each divisor must be positive and divide n")

    D = subgroup_domain(p, n, args.alpha % p)
    supports = quotient_supports(D, p, a, sorted(set(args.divisors)))
    if len(supports) > args.max_supports:
        raise SystemExit(f"support family has {len(supports)} supports, above --max-supports")

    fvals, gvals = line_values(args, D, p)
    lambdas = lagrange_lambdas(D, p)
    r = n - k
    usyn = syndrome(fvals, D, lambdas, r, p)
    vsyn = syndrome(gvals, D, lambdas, r, p)

    finite: set[int] = set()
    projective: set[tuple[int, int]] = set()
    contributing_locators: set[tuple[int, ...]] = set()
    all_idx = set(range(n))

    for S in supports:
        A = len(S)
        T_idx = sorted(all_idx - set(S))
        T_points = [D[i] for i in T_idx]
        coeff = locator_coeffs(T_points, p)
        j = len(coeff) - 1
        t = A - k
        if j != n - A or t != r - j or t < 0:
            raise RuntimeError("inconsistent support/co-support dimensions")
        Avec = hankel_contract(usyn, coeff, t, p)
        Bvec = hankel_contract(vsyn, coeff, t, p)
        z = finite_slope(Avec, Bvec, p)
        if z is not None:
            finite.add(z)
            contributing_locators.add(coeff)
        pp = projective_param(Avec, Bvec, p)
        if pp is not None:
            projective.add(pp)

    safe_sum = 0
    for A in range(a, n + 1):
        for c in sorted(set(args.divisors)):
            m, s = divmod(A, c)
            safe_sum += math.comb(n // c, m) * math.comb(n - c * m, s)

    print(f"p={p} n={n} k={k} a={a} divisors={sorted(set(args.divisors))}")
    print(f"support_union={len(supports)}")
    print(f"safe_support_sum={safe_sum}")
    print(f"finite_quotient_slopes={len(finite)}")
    print(f"projective_quotient_params={len(projective)}")
    print(f"contributing_locators={len(contributing_locators)}")
    if len(finite) <= 30:
        print("finite_slopes=", sorted(finite))
    if len(projective) <= 30:
        print("projective_params=", sorted(projective))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
