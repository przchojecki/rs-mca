#!/usr/bin/env python3
r"""
L2 codegree theorem, step 2b: the agreement-size-stratified sum / the saving.

The codegree decomposition gives |Lambda_2| = sum_{c1 in Fib_1} D(|A1(c1)|), the
interleaved list = #{(c1,c2): |A1(c1) cap A2(c2)| >= a}. Step 2a bounded the
per-N' inner list D; here we measure the actual SAVING and test the bound forms,
to see where the saving comes from (verify-first before claiming a bound).

CANDIDATE BOUNDS (all from Markov + Cauchy-Schwarz on cov_i(x) = #{c in Fib_i :
c(x)=U_i(x)}):
  |Lambda_2| <= (1/a) sum_x cov1(x) cov2(x)                         (Markov)
             <= (1/a) sqrt( S1 * S2 ),   S_i = sum_x cov_i(x)^2     (Cauchy-Schwarz)
  S_i = (linear) sum_x cov_i = sum_c |A_i(c)|   +   (quadratic excess)
        sum_{c!=c'} |A_i(c) cap A_i(c')|  <=  |Fib_i| n + |Fib_i|^2 (k-1).
If S_i is dominated by the LINEAR term (|Fib_i| n, sparse coverage), the bound is
~ (n/a) sqrt(|Fib1| |Fib2|) -- a sqrt-saving (removes a full base-list factor).
If dominated by the QUADRATIC term, only a constant (k-1)/a saving.

This scanner measures, over adversarial (U1,U2): |Lambda_2|, |Fib_i|, S_i and its
linear/quadratic split, the Markov and CS bounds, and the saving ratio
|Lambda_2| / (|Fib1||Fib2|). Goal: find the worst-case saving and which term of
S_i dominates -> which bound form is the truth.

Status: AUDIT / VERIFY-FIRST scan (L2 codegree step 2b).

Run:
    python3 experimental/scripts/verify_l2_stratified_sum.py
    python3 experimental/scripts/verify_l2_stratified_sum.py --json
"""

from __future__ import annotations

import argparse
import json
import math
import random
from itertools import product


def build_cws(p, H, k):
    return [tuple(sum(co[j] * pow(x, j, p) for j in range(k)) % p for x in H)
            for co in product(range(p), repeat=k)]


def fiber(U, cws, a):
    out = []
    for c in cws:
        A = [i for i in range(len(U)) if c[i] == U[i]]
        if len(A) >= a:
            out.append((c, frozenset(A)))
    return out


def analyze(U1, U2, cws, a, n):
    f1 = fiber(U1, cws, a)
    f2 = fiber(U2, cws, a)
    if not f1 or not f2:
        return None
    # interleaved list (stratified sum)
    lam = sum(1 for (_, A1) in f1 for (_, A2) in f2 if len(A1 & A2) >= a)
    # coverage and S_i
    def cov_stats(f):
        cov = [0] * n
        for (_, A) in f:
            for x in A:
                cov[x] += 1
        S = sum(c * c for c in cov)
        lin = sum(cov)                      # = sum_c |A(c)|
        quad = S - lin                      # sum cov(cov-1) = pairwise-overlap mass
        return S, lin, quad
    S1, lin1, quad1 = cov_stats(f1)
    S2, lin2, quad2 = cov_stats(f2)
    markov = (1 / a) * sum(
        (sum(1 for (_, A1) in f1 if x in A1)) * (sum(1 for (_, A2) in f2 if x in A2))
        for x in range(n))
    cs = (1 / a) * math.sqrt(S1 * S2)
    cart = len(f1) * len(f2)
    return {
        "|Fib1|": len(f1), "|Fib2|": len(f2), "interleaved": lam, "cartesian": cart,
        "saving_ratio": round(lam / cart, 4) if cart else None,
        "markov_bound": round(markov, 2), "cs_bound": round(cs, 2),
        "S1": S1, "S1_linear": lin1, "S1_quad": quad1,
        "S1_quad_dominates": quad1 > lin1,
        "lam<=markov": lam <= markov + 1e-9, "lam<=cs": lam <= cs + 1e-9,
    }


def run():
    p = 17
    H = [pow(3, i, p) for i in range(p - 1)]
    n = len(H)
    rng = random.Random(20260625)
    results = {}
    for k in (2, 3):
        cws = build_cws(p, H, k)
        for a in (k + 1, k + 2, k + 3):
            best = None  # worst-case (max saving ratio) with valid fibers
            markov_ok = cs_ok = True
            quad_dom_count = 0
            samples = 0
            for _ in range(600):
                # adversarial families
                kind = rng.randrange(4)
                if kind == 0:
                    U1 = [rng.randrange(p) for _ in range(n)]
                    U2 = [rng.randrange(p) for _ in range(n)]
                elif kind == 1:  # glued codewords
                    cs_sel = rng.sample(cws, 4)
                    U1 = [cs_sel[0][i] if i < n // 2 else cs_sel[1][i] for i in range(n)]
                    U2 = [cs_sel[2][i] if i < n // 2 else cs_sel[3][i] for i in range(n)]
                elif kind == 2:  # core-overlap (rich fibers)
                    base1 = rng.sample(cws, 3); base2 = rng.sample(cws, 3)
                    U1 = [base1[i % 3][i] for i in range(n)]
                    U2 = [base2[i % 3][i] for i in range(n)]
                else:            # codeword + noise
                    c1, c2 = rng.choice(cws), rng.choice(cws)
                    U1 = list(c1); U2 = list(c2)
                    for _ in range(rng.randint(1, 4)):
                        U1[rng.randrange(n)] = rng.randrange(p)
                        U2[rng.randrange(n)] = rng.randrange(p)
                r = analyze(U1, U2, cws, a, n)
                if r is None:
                    continue
                samples += 1
                markov_ok = markov_ok and r["lam<=markov"]
                cs_ok = cs_ok and r["lam<=cs"]
                if r["S1_quad_dominates"]:
                    quad_dom_count += 1
                # track the RICHEST-fiber case (max cartesian) -- where the saving is informative
                if best is None or r["cartesian"] > best["cartesian"]:
                    best = r
            if best:
                results[f"k={k},a={a}"] = {
                    "samples": samples, "markov_always_holds": markov_ok,
                    "cs_always_holds": cs_ok,
                    "quad_dominates_frac": round(quad_dom_count / max(1, samples), 2),
                    "worst_case": best,
                }
    all_ok = all(v["markov_always_holds"] and v["cs_always_holds"] for v in results.values())
    return {"all_ok": all_ok, "results": results}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("L2 stratified sum / saving (step 2b), F_17. Markov & Cauchy-Schwarz bounds + saving.")
    for key, v in out["results"].items():
        w = v["worst_case"]
        print(f"  {key}: {v['samples']} samples; markov holds={v['markov_always_holds']} "
              f"cs holds={v['cs_always_holds']}; quad-dominates frac={v['quad_dominates_frac']}")
        print(f"      worst saving: interleaved={w['interleaved']} cartesian={w['cartesian']} "
              f"ratio={w['saving_ratio']}  |Fib1|={w['|Fib1|']} |Fib2|={w['|Fib2|']}")
        print(f"        S1={w['S1']} (lin={w['S1_linear']}, quad={w['S1_quad']}, "
              f"quad>lin? {w['S1_quad_dominates']})  cs_bound={w['cs_bound']}")
    print()
    print("RESULT:", "PASS (Markov & CS bounds hold everywhere; saving + dominant-term measured)"
          if out["all_ok"] else "VIOLATION -- a proven inequality failed; inspect (likely a bug)")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
