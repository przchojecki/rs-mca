#!/usr/bin/env python3
"""L1 Fourier reduction: prefix count -> subgroup exponential sums.

EXPERIMENTAL / AUDIT verifier for §10 of `l1_prefix_divisor_count.md`. List
/locator side only; does not edit Papers A-D; does not duplicate the M1
residue-line Weil-sum work (different object: this is the base-code LIST count).

Identity under test (power-sum coordinates, valid for p > sigma so Newton's
identities are invertible).  For H = mu_n <= F_p, write p_j(A) = sum_{a in A} a^j
and parametrize the prefix fiber by (p_1,...,p_sigma).  With the additive
character e_p(x) = exp(2 pi i x / p) and g_r(w) = sum_{j=1}^sigma r_j w^j,

    S(r) := sum_{|A|=m} e_p(<r, p(A)>)
          = sum_{|A|=m} prod_{a in A} e_p(g_r(a))           [additive over A]
          = e_m( { e_p(g_r(a)) : a in mu_n } )               [elementary symm.]

and the level-set count satisfies the exact Fourier inversion

    |{ A : |A|=m, p(A) = c }| = (1/p^sigma) sum_{r in F_p^sigma} e_p(-<r,c>) S(r),

with main term S(0) = binom(n,m).  The power sums of the values e_p(g_r(a)) are
the subgroup exponential (Weil) sums

    P_l(r) = sum_{a in mu_n} e_p(l g_r(a)) = T(l r),

so S(r) is a fixed polynomial (Newton) in the Weil sums {T(l r)}.

Conditional bound under test.  If |T(l r)| <= tau for 1 <= l <= m, then by the
Newton recurrence |S(r)| <= prod_{j=1}^m (1 + tau/j).

The script verifies (over F_17, n=16): (1) S(r) by subset enumeration equals the
elementary-symmetric product formula; (2) the exact Fourier inversion
reconstructs the brute-force fiber histogram; (3) the conditional Newton bound
holds for every r.  Standard library only (uses cmath).
"""

import argparse
import cmath
import itertools
import json
import sys
from collections import defaultdict
from math import comb, pi


def factorize(num):
    f, d = set(), 2
    while d * d <= num:
        while num % d == 0:
            f.add(d); num //= d
        d += 1
    if num > 1:
        f.add(num)
    return f


def primitive_root(p):
    phi = p - 1
    primes = factorize(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in primes):
            return g
    raise ValueError("no primitive root")


def subgroup(p, n):
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p-1}")
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    out, cur = [], 1
    for _ in range(n):
        out.append(cur); cur = (cur * h) % p
    return out


def ep(x, p):
    return cmath.exp(2j * pi * (x % p) / p)


def g_eval(r, a, p):
    """g_r(a) = sum_j r_j a^j  (j = 1..sigma) mod p."""
    s, ap = 0, 1
    for rj in r:
        ap = (ap * a) % p
        s = (s + rj * ap) % p
    return s


def elem_sym_m(weights, m):
    """e_m of a list of complex weights via the generating product."""
    poly = [0j] * (m + 1)
    poly[0] = 1 + 0j
    for w in weights:
        for i in range(min(m, len(poly) - 1), 0, -1):
            poly[i] = poly[i] + w * poly[i - 1]
    return poly[m]


def S_product(r, H, m, p):
    return elem_sym_m([ep(g_eval(r, a, p), p) for a in H], m)


def weil_sum(lr_vec, H, p):
    return sum(ep(g_eval(lr_vec, a, p), p) for a in H)


def run(p=17, n=16, k=8, sigma=2, tol=1e-6):
    H = subgroup(p, n)
    m = n - (k + sigma)
    idx = list(range(n))

    # Brute power-sum fiber histogram.
    brute = defaultdict(int)
    for A in itertools.combinations(idx, m):
        key = tuple(sum(pow(H[i], j, p) for i in A) % p for j in range(1, sigma + 1))
        brute[key] += 1
    total = comb(n, m)

    rvecs = list(itertools.product(range(p), repeat=sigma))

    # (1) S(r): subset enumeration vs product formula, on a sample of r.
    s_consistent = True
    for r in rvecs[1:6]:
        s_enum = sum(ep(sum(rj * sum(pow(H[i], j + 1, p) for i in A) for j, rj in
                            enumerate(r)), p)
                     for A in itertools.combinations(idx, m))
        if abs(s_enum - S_product(r, H, m, p)) > tol:
            s_consistent = False
    # Precompute S(r) for all r by the product formula.
    Svals = {r: S_product(r, H, m, p) for r in rvecs}

    # (2) Exact Fourier inversion reconstructs the brute histogram.
    inv_ok = True
    max_err = 0.0
    for c, cnt in brute.items():
        rec = sum(ep(-sum(rj * cj for rj, cj in zip(r, c)), p) * Svals[r]
                  for r in rvecs) / (p ** sigma)
        max_err = max(max_err, abs(rec.real - cnt), abs(rec.imag))
        if abs(rec.real - cnt) > tol or abs(rec.imag) > tol:
            inv_ok = False

    # (3) Conditional Newton bound |S(r)| <= prod_{j=1}^m (1 + tau_r/j).
    newton_ok = True
    worst_ratio = 0.0
    for r in rvecs[1:]:
        tau = max(abs(weil_sum(tuple((l * rj) % p for rj in r), H, p))
                  for l in range(1, m + 1))
        bound = 1.0
        for j in range(1, m + 1):
            bound *= (1 + tau / j)
        sval = abs(Svals[r])
        if sval > bound + tol:
            newton_ok = False
        worst_ratio = max(worst_ratio, sval / bound if bound > 0 else 0.0)

    # (4) Structured / generic split (§11).  r is STRUCTURED iff g_r is a
    # polynomial in w^e with e = gcd{j : r_j != 0} > 1 (then it folds to mu_{n/e}
    # and carries large Weil sums); GENERIC iff e = 1.
    from math import gcd as _gcd, sqrt
    def support_gcd(r):
        e = 0
        for j in range(sigma):
            if r[j] % p != 0:
                e = (j + 1) if e == 0 else _gcd(e, j + 1)
        return e
    struct_sum = gen_sum = 0.0
    struct_cnt = gen_cnt = 0
    max_gen_S = max_gen_T = max_struct_S = 0.0
    for r in rvecs:
        if not any(r):
            continue
        aS = abs(Svals[r])
        if support_gcd(r) > 1:
            struct_sum += aS; struct_cnt += 1
            max_struct_S = max(max_struct_S, aS)
        else:
            gen_sum += aS; gen_cnt += 1
            max_gen_S = max(max_gen_S, aS)
            max_gen_T = max(max_gen_T, abs(weil_sum(r, H, p)))
    main = total / (p ** sigma)
    max_dev = max(abs(cnt - main) for cnt in brute.values())

    return {
        "status": "EXPERIMENTAL/AUDIT",
        "params": {"p": p, "n": n, "k": k, "sigma": sigma, "m": m},
        "total_divisors": total,
        "main_term_binom_over_psigma": total / (p ** sigma),
        "distinct_fibers": len(brute),
        "max_fiber": max(brute.values()),
        "S_enum_eq_product": s_consistent,
        "fourier_inversion_ok": inv_ok,
        "fourier_max_abs_err": max_err,
        "newton_bound_ok": newton_ok,
        "newton_worst_ratio": round(worst_ratio, 4),
        "split": {
            "structured_count": struct_cnt,
            "generic_count": gen_cnt,
            "structured_frac": round(struct_cnt / (p ** sigma - 1), 4),
            "err_bound_structured": round(struct_sum / p ** sigma, 4),
            "err_bound_generic": round(gen_sum / p ** sigma, 4),
            "max_struct_S": round(max_struct_S, 3),
            "max_generic_S": round(max_gen_S, 3),
            "max_generic_T": round(max_gen_T, 3),
            "weil_pred_sigma_sqrt_p": round(sigma * (p ** 0.5), 3),
            "actual_max_fiber_deviation": round(max_dev, 3),
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--p", type=int, default=17)
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--sigma", type=int, default=2)
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)
    r = run(args.p, args.n, args.k, args.sigma)
    if args.format == "json":
        print(json.dumps(r, indent=2))
    else:
        pp = r["params"]
        print(f"L1 Fourier reduction verifier  (status {r['status']})")
        print(f"  F_{pp['p']}, n={pp['n']}, k={pp['k']}, sigma={pp['sigma']}, m={pp['m']}")
        print(f"  total divisors / main term : {r['total_divisors']} / "
              f"{r['main_term_binom_over_psigma']:.4f}")
        print(f"  distinct fibers / max      : {r['distinct_fibers']} / {r['max_fiber']}")
        print(f"  [{'OK ' if r['S_enum_eq_product'] else 'FAIL'}] S(r): subset enum == "
              f"elementary-symmetric product formula")
        print(f"  [{'OK ' if r['fourier_inversion_ok'] else 'FAIL'}] exact Fourier "
              f"inversion reconstructs brute histogram (max err {r['fourier_max_abs_err']:.2e})")
        print(f"  [{'OK ' if r['newton_bound_ok'] else 'FAIL'}] conditional Newton bound "
              f"|S(r)| <= prod(1+tau/j)  (worst ratio {r['newton_worst_ratio']})")
        sp = r["split"]
        print(f"  -- structured/generic split (§11) --")
        print(f"     structured r: {sp['structured_count']} ({sp['structured_frac']} frac), "
              f"generic r: {sp['generic_count']}")
        print(f"     error-bound mass: structured {sp['err_bound_structured']}, "
              f"generic {sp['err_bound_generic']}  (actual max dev {sp['actual_max_fiber_deviation']})")
        print(f"     max |S|: struct {sp['max_struct_S']}, generic {sp['max_generic_S']}; "
              f"max generic |T|={sp['max_generic_T']} vs Weil sigma*sqrt(p)={sp['weil_pred_sigma_sqrt_p']}")
        ok = (r["S_enum_eq_product"] and r["fourier_inversion_ok"] and r["newton_bound_ok"])
        print(f"RESULT: {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
