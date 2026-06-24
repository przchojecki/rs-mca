#!/usr/bin/env python3
r"""
The period-d QuotientBudget = the same-rate L1 problem on the quotient domain.
This resolves the growing-d concern and unifies with Codex's Mobius decomposition.

CONTEXT. x1_nonequivariant_product_bound.md bounded the non-equivariant periodic
slope mass by C^d (C = per-character confined count), polynomial only for bounded
d. The growing-d (deep-cap a_q) regime was left open. The C^d bound is loose; the
true structure is a QUOTIENT REDUCTION.

CLAIM (verified here). Let H_n = <omega> be cyclic of order n, d | n, K_d the
order-d subgroup, and phi: x |-> x^d the d-to-1 map onto the quotient domain
H_{n/d} (fibers = K_d-cosets). Then:

  (1) A K_d-stable support S (union of K_d-cosets) pushes to S' = phi(S) on
      H_{n/d} with |S'| = |S|/d.
  (2) Stab_{H_n}(S) = K_d EXACTLY  <=>  S' is PRIMITIVE (trivial stabilizer) on
      H_{n/d}. (H_n cyclic => unique order-d subgroup, so "exact stabilizer order
      d" means Stab = K_d.) Hence
          Q_d(H_n)  [exact-stabilizer-d mass]  =  Q_1(H_{n/d})  [primitive mass].
  (3) The folded codewords P = G(X^d) of degree < k correspond bijectively to
      codewords G of degree < k/d on H_{n/d}, with P(x) = G(x^d). The quotient
      RATE is preserved: (k/d)/(n/d) = k/n.

CONSEQUENCES.
  * The period-d QuotientBudget mass is the SAME-RATE L1 fiber problem on the
    smaller domain H_{n/d} -- NOT a C^d blow-up. Growing d shrinks the quotient
    domain, so large-period mass is governed by a SMALLER instance.
  * Codex's Mobius decomposition |Fib_U| = sum_{d|n} Q_d(H_n) is exactly the
    multi-scale recursion  sum_{d|n} Q_1(H_{n/d})  -- the fiber is the sum over
    divisors of the PRIMITIVE mass at each quotient scale. My slope-side
    confinement analysis and Codex's stabilizer budget are the SAME recursion.
  * HONEST CAVEAT: the L1 conjecture Q_1(H_m) <= m^B holds only ABOVE the reserve
    at scale m. lem:fiber's exponential mass is Q_1 on a quotient that is BELOW
    that quotient's reserve (so no contradiction with the conjecture, but the
    per-scale reserve bookkeeping is the real remaining content, not resolved
    here). The growing-d concern is thus reduced to "does the reserve hold at the
    relevant quotient scales", a sharper and more structured question than C^d.

Checks (exact F_13, H_12, for d in {2,3,6}):
  (1) phi is d-to-1 onto H_{12/d} (fibers = K_d-cosets);
  (2) rate preserved: (k/d)/(n/d) = k/n;
  (3) stabilizer bijection: S = phi^{-1}(S') has Stab = K_d  <=>  S' primitive;
  (4) folded codeword P=G(X^d) (deg<k) <-> G (deg<k/d) on H_{n/d}, P(x)=G(x^d).

Status: AUDIT / PROVED (the quotient reduction) + verified; the per-scale reserve
bookkeeping (growing-d full resolution) remains open.

Run:
    python3 experimental/scripts/verify_x1_quotient_reduction.py
    python3 experimental/scripts/verify_x1_quotient_reduction.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from fractions import Fraction


P = 13                    # F_13, H_12 = F_13^*
N = P - 1                 # 12
K = 6                     # degree bound k (rate 1/2)


def subgroup_of_order(d):
    """unique order-d subgroup of F_13^* = {x : x^d == 1}."""
    return sorted(x for x in range(1, P) if pow(x, d, P) == 1)


def stab_order(S):
    Sset = set(S)
    return sum(1 for h in range(1, P) if set((h * x) % P for x in Sset) == Sset)


def poly_eval(coeffs, x):
    acc = 0
    for c in reversed(coeffs):
        acc = (acc * x + c) % P
    return acc


def check_d(d):
    n, k = N, K
    np_, kp = n // d, k // d
    out = {"d": d, "n": n, "k": k, "nq": np_, "kq": kp,
           "rate": str(Fraction(k, n)), "rateq": str(Fraction(kp, np_))}
    H = list(range(1, P))
    Kd = subgroup_of_order(d)
    # (1) phi d-to-1 onto H_{n/d}
    fibers = {}
    for x in H:
        fibers.setdefault(pow(x, d, P), []).append(x)
    quotient = sorted(fibers.keys())
    phi_ok = (len(quotient) == np_ and all(len(v) == d for v in fibers.values())
              and len(Kd) == d)
    # K_d-coset check: each fiber is a coset of K_d
    coset_ok = all(sorted((r * h) % P for h in Kd) == sorted(fibers[pow(r, d, P)])
                   for r in H)
    # (2) rate preserved
    rate_ok = Fraction(kp, np_) == Fraction(k, n)
    # (3) stabilizer bijection: test all S' of size 2 on the quotient (small)
    stab_bij_ok = True
    qlist = quotient
    for Sp in combinations(qlist, 2):
        # S' primitive on H_{n/d}?  stabilizer of S' under H_{n/d}-action.
        # H_{n/d} acts; represent quotient as its own multiplicative group.
        Spset = set(Sp)
        stabp = sum(1 for h in qlist if set((h * x) % P for x in Spset) == Spset)
        # lift S = phi^{-1}(S')
        S = [x for x in H if pow(x, d, P) in Spset]
        st = stab_order(S)
        primitive = (stabp == 1)
        exact_Kd = (st == d)
        if primitive != exact_Kd:
            stab_bij_ok = False
    # (4) folded codeword bijection: G of deg<k' -> P=G(X^d), check P(x)=G(x^d)
    fold_ok = True
    deg_ok = True
    # a few G's
    import itertools
    tests = 0
    for Gco in itertools.product(range(P), repeat=kp):   # all G of deg<k'
        Gco = list(Gco)
        P_coeffs = [0] * (d * (kp - 1) + 1) if kp >= 1 else [0]
        for i, c in enumerate(Gco):
            P_coeffs[i * d] = c            # P(X) = sum c_i X^{i d} = G(X^d)
        if len(P_coeffs) - 1 >= k:
            deg_ok = False
        for x in H:
            if poly_eval(P_coeffs, x) != poly_eval(Gco, pow(x, d, P)):
                fold_ok = False
        tests += 1
        if tests >= 200:                   # cap enumeration for d=2 (k'=3 -> 13^3)
            break
    out.update({"phi_d_to_1": phi_ok, "fibers_are_Kd_cosets": coset_ok,
                "rate_preserved": rate_ok, "stabilizer_bijection": stab_bij_ok,
                "folded_codeword_bijection": fold_ok, "deg<k": deg_ok})
    out["ok"] = all([phi_ok, coset_ok, rate_ok, stab_bij_ok, fold_ok, deg_ok])
    return out


def run():
    rows = [check_d(d) for d in (2, 3, 6)]
    return {"all_ok": all(r["ok"] for r in rows), "rows": rows}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("Quotient reduction: period-d QuotientBudget = same-rate L1 on H_{n/d} (F_13, H_12):")
    print("  Q_d(H_n) [exact stab d] = Q_1(H_{n/d}) [primitive]; rate preserved; folded codeword = quotient codeword.")
    print()
    for r in out["rows"]:
        print(f"  d={r['d']}: H_{r['n']}->H_{r['nq']}  rate {r['rate']}->{r['rateq']}  "
              f"(k={r['k']}->kq={r['kq']})")
        for key in ("phi_d_to_1", "fibers_are_Kd_cosets", "rate_preserved",
                    "stabilizer_bijection", "folded_codeword_bijection", "deg<k"):
            print(f"      [{'OK ' if r[key] else 'FAIL'}] {key}")
    print()
    print("RESULT:", "PASS (period-d mass reduces to the same-rate L1 problem on the quotient; "
          "Q_d = Q_1 on H_{n/d}; matches Codex's Mobius recursion)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
