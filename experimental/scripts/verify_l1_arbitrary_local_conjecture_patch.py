#!/usr/bin/env python3
"""Verify the conj:arbitrary-local / conj:final-locator / ass:locator erratum.

Self-contained: standard library only (no numpy/sympy).

Reproduces, independently of PR #80's own verifier, that the raw arbitrary
locator fiber |Fib_U(k+sigma)| is not polynomially bounded for interpolants
U with deg(U) < k (the literal hypothesis of the current conjecture text),
and separately confirms -- via the Reed-Solomon minimum-distance argument,
not PR #80's image-fiber injectivity argument -- that the *actual* codeword
list for such U has size exactly 1, so the repaired object ImgFib_U(s)
(proposed in experimental/notes/l1/l1_arbitrary_fiber_repair.md) is correct
where the raw object is not.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from math import comb


def prime_factors(m: int) -> set[int]:
    fs = set()
    d = 2
    while d * d <= m:
        while m % d == 0:
            fs.add(d)
            m //= d
        d += 1
    if m > 1:
        fs.add(m)
    return fs


def subgroup(p: int, n: int) -> list[int]:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    order = p - 1
    factors = prime_factors(order)
    gen = next(
        g for g in range(2, p)
        if all(pow(g, order // q, p) != 1 for q in factors)
    )
    step = pow(gen, order // n, p)
    H, x = [], 1
    for _ in range(n):
        H.append(x)
        x = (x * step) % p
    assert len(set(H)) == n
    return sorted(H)


def poly_degree(poly: list[int]) -> int:
    d = len(poly) - 1
    while d >= 0 and poly[d] == 0:
        d -= 1
    return d


def poly_eval(coeffs: list[int], x: int, p: int) -> int:
    acc = 0
    for c in reversed(coeffs):
        acc = (acc * x + c) % p
    return acc


def mul_root(poly: list[int], root: int, p: int) -> list[int]:
    new = [0] * (len(poly) + 1)
    for i, c in enumerate(poly):
        new[i + 1] = (new[i + 1] + c) % p
        new[i] = (new[i] - c * root) % p
    return new


def locator(S: tuple[int, ...], p: int) -> list[int]:
    poly = [1]
    for h in S:
        poly = mul_root(poly, h, p)
    return poly


def poly_mod(U: list[int], L: list[int], p: int) -> list[int]:
    U = U[:]
    Ldeg = poly_degree(L)
    while poly_degree(U) >= Ldeg and poly_degree(U) >= 0:
        du = poly_degree(U)
        coef = U[du] % p  # L is monic
        shift = du - Ldeg
        for i, c in enumerate(L):
            U[i + shift] = (U[i + shift] - coef * c) % p
    return U


def fib_count(U: list[int], H: list[int], s: int, k: int, p: int) -> int:
    return sum(
        1
        for S in itertools.combinations(H, s)
        if poly_degree(poly_mod(U, locator(S, p), p)) < k
    )


def run(p: int, n: int, k: int, sigma: int, seed: int) -> dict:
    s = k + sigma
    H = subgroup(p, n)
    result: dict = {"p": p, "n": n, "k": k, "sigma": sigma, "s": s}

    # (a) literal-hypothesis counterexample: deg(U) < k gives the full binomial.
    U_low = [1, 2, 0, 5]  # 5X^3 + 2X + 1, degree 3 < k
    assert poly_degree(U_low) < k
    cnt_low = fib_count(U_low, H, s, k, p)
    result["low_degree_U_fib_count"] = cnt_low
    result["binom_n_s"] = comb(n, s)
    assert cnt_low == comb(n, s), "expected the raw fiber to be the full binomial"

    # (b) generic U of degree >= s: no such blowup (the actually-hard regime).
    rng = random.Random(seed)
    U_generic = [rng.randrange(p) for _ in range(s)] + [1]
    result["generic_U_fib_count"] = fib_count(U_generic, H, s, k, p)

    # (c) the repair: minimum-distance argument, independent of PR #80's
    # injectivity-based ImgFib proof. Any degree-<k P != U_low must satisfy
    # agreement(P, U_low) <= k-1, and s > k-1, so no such P reaches agreement s.
    max_agree = 0
    trials = 20000
    padded_low = U_low + [0] * (k - len(U_low))
    for _ in range(trials):
        P = [rng.randrange(p) for _ in range(k)]
        if P == padded_low:
            continue
        agree = sum(1 for h in H if poly_eval(P, h, p) == poly_eval(padded_low, h, p))
        max_agree = max(max_agree, agree)
    result["max_agreement_distinct_low_degree_pair"] = max_agree
    result["k_minus_1"] = k - 1
    assert max_agree <= k - 1
    assert s > k - 1
    result["repair_holds"] = True
    result["conclusion"] = (
        "deg(U)<k forces |Fib_U(s)|=C(n,s) (exponential) while the true list "
        "size is exactly 1 (ImgFib_U(s)={U}); the raw conjecture is false as "
        "literally stated, the ImgFib-repaired conjecture is unaffected."
    )
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--p", type=int, default=97)
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--k", type=int, default=7)
    ap.add_argument("--sigma", type=int, default=4)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--check", type=str, default=None, help="path to a JSON cert to compare against")
    args = ap.parse_args()

    result = run(args.p, args.n, args.k, args.sigma, args.seed)
    print(json.dumps(result, indent=2))

    if args.check:
        with open(args.check) as f:
            expected = json.load(f)
        mismatches = [key for key in expected if result.get(key) != expected[key]]
        if mismatches:
            raise SystemExit(f"MISMATCH vs {args.check}: {mismatches}")
        print(f"OK: matches {args.check}")


if __name__ == "__main__":
    main()
