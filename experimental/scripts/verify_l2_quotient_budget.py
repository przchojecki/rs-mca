#!/usr/bin/env python3
r"""
L2 sharp-constant falsification, iteration 5: the EXACT quotient budget Quot_rem_mu
and a direct test of the full V0 bound on quotient-periodic words.

The L2-Sharp V0 conjecture (l2_sharp_target_conjecture.md sec 3) is

    Lst_mu(H,k,a;q)  <=  binom(n,a) q^{-mu(a-k)}  +  Quot_rem_mu(n,k,a)  +  n^B.

Prior iterations (l2_falsification_log.md) tested the SAVING (random term vs the
Cartesian binom(n,a)^mu) under gluing/grid attacks and found it robust, and the
codegree decomposition reduced the saving to punctured-RS list decoding. The
scanner so far computes only the random term, NOT the explicit quotient budget
Quot_rem_mu. This script implements Quot_rem_mu EXACTLY (sec 2 of the note) and
brute-force-verifies its combinatorial core, then evaluates the FULL V0 right-hand
side and tests quotient-periodic words U_i = g_i(x^M) -- the stress case the
quotient packets are meant to budget -- hunting for a reserve-cleared excess.

Quot_rem_mu (note sec 2). sigma = a-k. For each M | n with M > sigma, M >= 2:
    N = n/M,  Q = N-1,  ell_M = floor(a/M),  u_M = a - M*ell_M  (0 <= u_M < M),
    h_M(a,tau) = max(0, ceil((a-tau)/M)),
    E_empty(R,b,mu) = sum_{j=0}^b (-1)^j C(R,j) C(R-j,b-j)^mu   [# ordered mu-tuples
        of b-subsets of an R-set with EMPTY common intersection],
    L_{M,mu}(a,tau) = sum_{c=h_M(a,tau)}^{ell_M} C(Q,c) E_empty(Q-c, ell_M-c, mu)
        (0 if h_M(a,tau) > ell_M),
    Quot_rem_mu = sum_{M|n, M>sigma, M>=2, 1<=ell_M<=Q} max_{0<=tau<=u_M} L_{M,mu}(a,tau).

Rigorous self-checks (independent of the conjecture):
  (1) E_empty(R,b,mu) matches a brute-force count of ordered mu-tuples of b-subsets
      of [R] with empty intersection (small R,b,mu);
  (2) E_empty(R,b,1) = [b==0] (one subset has empty intersection iff it is empty);
  (3) aligned endpoint: L_{M,mu}(a,u_M) = C(Q, ell_M) (note sec 2);
  (4) active-scale criterion: a scale M contributes iff M|n and sigma < M <= a.

Falsification probe (honest about reserve): build quotient-periodic words on a small
RS code, compute the exact interleaved list, and compare to
binom(n,a)q^{-mu(a-k)} + Quot_rem_mu. A small-model excess absorbed by a fixed n^B
is NOT a falsification (n^B dominates for small n); only a SUPER-POLYNOMIAL-SCALING
excess over (random + Quot_rem_mu) would be. We report the raw excess and flag it.

Run:
    python3 experimental/scripts/verify_l2_quotient_budget.py
    python3 experimental/scripts/verify_l2_quotient_budget.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from itertools import combinations, product
from math import comb, ceil


# ---- exact quotient-budget arithmetic ----

def E_empty(R, b, mu):
    """# ordered mu-tuples of b-subsets of an R-set with empty common intersection."""
    if b < 0 or b > R:
        return 0
    s = 0
    for j in range(b + 1):
        s += (-1) ** j * comb(R, j) * comb(R - j, b - j) ** mu
    return s


def E_empty_bruteforce(R, b, mu):
    """direct enumeration (small R,b,mu) for verification."""
    subs = list(combinations(range(R), b))
    cnt = 0
    for tup in product(subs, repeat=mu):
        inter = set(tup[0])
        for t in tup[1:]:
            inter &= set(t)
        if not inter:
            cnt += 1
    return cnt


def quot_rem_mu(n, k, a, mu, return_scales=False):
    """exact Quot_rem_mu(n,k,a) per l2_sharp_target_conjecture.md sec 2."""
    sigma = a - k
    total = 0
    scales = []
    for M in range(2, n + 1):
        if n % M != 0 or M <= sigma:
            continue
        N = n // M
        Q = N - 1
        ell_M = a // M
        u_M = a - M * ell_M
        if ell_M == 0 or ell_M > Q:
            continue
        best = 0
        for tau in range(0, u_M + 1):
            h = max(0, ceil((a - tau) / M))
            if h > ell_M:
                L = 0
            else:
                L = sum(comb(Q, c) * E_empty(Q - c, ell_M - c, mu)
                        for c in range(h, ell_M + 1))
            best = max(best, L)
        total += best
        scales.append({"M": M, "ell_M": ell_M, "u_M": u_M, "Q": Q, "L_max": best})
    return (total, scales) if return_scales else total


# ---- small RS machinery (reuse the existing scanner if importable) ----

def _load_scanner():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import importlib
    return importlib.import_module("verify_l2_falsify_interleaved")


def grid_scaling_vs_budget(S):
    """Run the worst cross-mass family (grid gluing, k=2,a=4) across scale and test
    the FULL V0 bound with the exact Quot_rem_mu: confirm
    interleaved - binom(n,a)q^{-mu(a-k)} - Quot_rem_mu  stays POLYNOMIAL (<= n)."""
    points = [(13, 12, 2), (17, 16, 2), (41, 20, 2), (73, 24, 2), (97, 48, 2)]
    mu = 2
    rows = []
    bound_holds = True
    residual_poly = True
    for (p, n, k) in points:
        a = k + 2
        H, cws, _ = S.build(p, n, k)
        g = S.grid_witness(p, n, k, a, H, cws)
        if g is None:
            continue
        inter = g["interleaved"]
        rand_term = comb(n, a) * (p ** (-mu * (a - k)))
        Qrem = quot_rem_mu(n, k, a, mu)
        residual = inter - rand_term - Qrem               # the part charged to n^B
        rows.append({"p": p, "n": n, "a": a, "interleaved": inter,
                     "max_base": g["max_base"], "rand_term": round(rand_term, 4),
                     "Quot_rem_mu": Qrem, "residual_to_nB": round(residual, 3),
                     "n_over_a": n // a})
        # V0 holds with n^B (B=1 proxy): interleaved <= rand + Quot_rem + n
        if inter > rand_term + Qrem + n:
            bound_holds = False
        if residual > n:                                  # residual must be poly (<= n)
            residual_poly = False
    return {"rows": rows, "bound_holds": bound_holds, "residual_poly": residual_poly}


def run():
    checks = {}

    # (1)(2) E_empty correctness
    ee_ok = True
    for R in range(0, 6):
        for b in range(0, R + 1):
            for mu in (1, 2, 3):
                if E_empty(R, b, mu) != E_empty_bruteforce(R, b, mu):
                    ee_ok = False
    ee_mu1_ok = all(E_empty(R, b, 1) == (1 if b == 0 else 0)
                    for R in range(0, 6) for b in range(0, R + 1))
    checks["E_empty matches brute force (R<=5, b, mu in {1,2,3})"] = ee_ok
    checks["E_empty(R,b,1) = [b==0]"] = ee_mu1_ok

    # (3) aligned endpoint L_{M,mu}(a,u_M) = C(Q, ell_M)
    aligned_ok = True
    aligned_examples = []
    for (n, k, a, mu) in [(16, 3, 5, 2), (24, 4, 8, 2), (16, 3, 5, 3), (30, 5, 12, 2)]:
        sigma = a - k
        for M in range(2, n + 1):
            if n % M != 0 or M <= sigma:
                continue
            N = n // M; Q = N - 1; ell_M = a // M; u_M = a - M * ell_M
            if ell_M == 0 or ell_M > Q:
                continue
            h = max(0, ceil((a - u_M) / M))
            L = 0 if h > ell_M else sum(comb(Q, c) * E_empty(Q - c, ell_M - c, mu)
                                        for c in range(h, ell_M + 1))
            if L != comb(Q, ell_M):
                aligned_ok = False
            aligned_examples.append({"n": n, "M": M, "L_aligned": L, "C(Q,ell_M)": comb(Q, ell_M)})
    checks["aligned endpoint L_{M,mu}(a,u_M) = C(Q,ell_M)"] = aligned_ok

    # (4) active-scale criterion: contributes iff M|n and sigma < M <= a
    crit_ok = True
    for (n, k, a) in [(16, 3, 5), (24, 4, 8), (30, 5, 12), (48, 2, 4)]:
        sigma = a - k
        _, scales = quot_rem_mu(n, k, a, 2, return_scales=True)
        contributing = {s["M"] for s in scales}
        expected = {M for M in range(2, n + 1) if n % M == 0 and sigma < M <= a}
        if contributing != expected:
            crit_ok = False
    checks["active-scale criterion: M|n and sigma<M<=a"] = crit_ok

    # ---- falsification probe: quotient-periodic words + grid attack vs full V0 RHS ----
    probe = {"available": False}
    grid = {"available": False}
    try:
        S = _load_scanner()
        probe = quotient_periodic_probe(S)
        grid = grid_scaling_vs_budget(S)
        grid["available"] = True
        checks["grid attack: full V0 bound holds at scale (interleaved <= rand+Quot_rem+n)"] = \
            grid["bound_holds"]
        checks["grid attack: residual charged to n^B stays polynomial (<= n)"] = \
            grid["residual_poly"]
    except Exception as e:  # honest: don't fail the rigorous checks if the probe can't run
        probe = {"available": False, "error": repr(e)}
        grid = {"available": False, "error": repr(e)}

    all_ok = all(checks.values())
    return {"checks": checks, "all_ok": all_ok,
            "aligned_examples": aligned_examples[:6], "probe": probe, "grid": grid}


def quotient_periodic_probe(S):
    """Build quotient-periodic words U_i = g_i(x^M) on a small RS code, compute the
    exact interleaved list, and compare to binom(n,a)q^{-mu(a-k)} + Quot_rem_mu."""
    import random
    p, n, k, a, mu = 17, 16, 3, 5, 2
    H, cws, _ = S.build(p, n, k)           # H = F_17^* (size n), all degree-<k codewords
    sigma = a - k
    Qrem = quot_rem_mu(n, k, a, mu)
    rand_term = comb(n, a) * (p ** (-mu * (a - k)))   # float, tiny here
    scales = [M for M in range(2, n + 1) if n % M == 0 and sigma < M <= a]
    rng = random.Random(20260626)

    worst = {"interleaved": 0, "M": None, "max_base": 0}
    worst_cross = {"cross_excess": 0, "interleaved": 0, "max_base": 0, "M": None}
    per_scale = []
    for M in scales:
        # cosets of the order-M subgroup {x: x^M=1}; U is constant on each coset
        cosets = {}
        for idx, x in enumerate(H):
            cosets.setdefault(pow(x, M, p), []).append(idx)
        reps = list(cosets.keys())
        # candidate quotient-periodic words: (a) linear g(y)=g0+g1*y in quotient var
        # y=x^M; (b) random full coset-value assignments. Precompute each fiber once.
        words = []
        for g0 in range(p):
            for g1 in range(p):
                U = [0] * n
                for r in reps:
                    val = (g0 + g1 * r) % p
                    for idx in cosets[r]:
                        U[idx] = val
                words.append(tuple(U))
        for _ in range(300):                          # random full quotient-periodic
            assign = {r: rng.randrange(p) for r in reps}
            U = [0] * n
            for r in reps:
                for idx in cosets[r]:
                    U[idx] = assign[r]
            words.append(tuple(U))
        words = list(dict.fromkeys(words))            # dedup
        fibs = [S.fiber(list(U), cws, a) for U in words]
        nonempty = [f for f in fibs if f]
        for i in range(len(nonempty)):
            fi = nonempty[i]
            for j in range(len(nonempty)):
                inter = S.interleaved_count([fi, nonempty[j]], a, n)
                mb = max(len(fi), len(nonempty[j]))
                if inter > worst["interleaved"]:
                    worst = {"interleaved": inter, "M": M, "max_base": mb}
                # genuine mu-fold cross-mass = interleaved beyond the single-row (L1) list
                if inter - mb > worst_cross["cross_excess"]:
                    worst_cross = {"cross_excess": inter - mb, "interleaved": inter,
                                   "max_base": mb, "M": M}
        per_scale.append({"M": M, "num_words": len(words), "num_nonempty_fibers": len(nonempty)})

    budget = rand_term + Qrem
    return {"available": True, "params": {"p": p, "n": n, "k": k, "a": a, "mu": mu},
            "Quot_rem_mu": Qrem, "rand_term": round(rand_term, 6),
            "V0_budget_excl_nB": round(budget, 4),
            "worst_quotient_periodic_interleaved": worst,
            "worst_genuine_cross_mass": worst_cross,
            "cross_mass_within_Quot_rem_mu": worst_cross["cross_excess"] <= Qrem,
            "interleaved_is_L1_dominated (interleaved <= max_base, i.e. cross_excess<=0)":
                worst_cross["cross_excess"] <= 0,
            "scales_active": scales, "per_scale": per_scale, "note":
            "interleaved up to max_base is single-row (L1) mass charged to n^B, NOT a V0 "
            "violation; the mu-fold quotient cross-mass (interleaved-max_base) is what "
            "Quot_rem_mu must budget. Small-model/below-reserve caveat applies."}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("L2 sharp-constant iteration 5: exact Quot_rem_mu + full V0 bound probe")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    pr = out["probe"]
    if pr.get("available"):
        print(f"  quotient-periodic probe (n={pr['params']['n']},k={pr['params']['k']},"
              f"a={pr['params']['a']},mu={pr['params']['mu']}):")
        print(f"    Quot_rem_mu = {pr['Quot_rem_mu']}   random term = {pr['rand_term']}   "
              f"active scales M = {pr['scales_active']}")
        print(f"    worst interleaved = {pr['worst_quotient_periodic_interleaved']}")
        print(f"    worst GENUINE mu-fold cross-mass (interleaved-max_base) = "
              f"{pr['worst_genuine_cross_mass']}")
        print(f"    cross-mass within Quot_rem_mu: {pr['cross_mass_within_Quot_rem_mu']}   "
              f"interleaved L1-dominated (<=max_base): "
              f"{pr['interleaved_is_L1_dominated (interleaved <= max_base, i.e. cross_excess<=0)']}")
        print(f"    [{pr['note']}]")
    else:
        print(f"  quotient-periodic probe unavailable: {pr.get('error')}")
    print()
    gr = out.get("grid", {})
    if gr.get("available"):
        print("  grid gluing attack (worst cross-mass, k=2,a=4) vs FULL V0 bound at scale:")
        print(f"    {'n':>4}{'a':>3}{'interlvd':>9}{'rand':>7}{'Quot_rem':>9}{'resid->n^B':>11}{'n/a':>5}")
        for r in gr["rows"]:
            print(f"    {r['n']:>4}{r['a']:>3}{r['interleaved']:>9}{r['rand_term']:>7}"
                  f"{r['Quot_rem_mu']:>9}{r['residual_to_nB']:>11}{r['n_over_a']:>5}")
    print()
    print("RESULT:", "PASS (Quot_rem_mu implementation verified; probe recorded)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
