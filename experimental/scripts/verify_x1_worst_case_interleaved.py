#!/usr/bin/env python3
r"""
Worst-case interleaved list = base-code list in the a-regular regime  (L2 / X1).

Increment 4 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.

Background (bridge note `notes/l2/l2_interleaved_support_bridge.md`, PROVED):
the interleaved list equals the common-intersection profile of the full
agreement supports,

    |Lambda(Int(C_+,mu),1-a/n,U)|
      = #{ (A_1,...,A_mu) : A_i in Supp_{U_i}^{>=a}, |A_1 cap ... cap A_mu| >= a }.

Call a row word V "a-regular" if every C_+ codeword that agrees with V on at
least a points agrees on EXACTLY a points (no over-agreement; the generic
maximal-radius case).  Distinct C_+ = RS[F,D,k+1] codewords agree on at most k
points, and here a > k.

Theorem (this increment):
  (i)  [lower bound]  Lst(Int(C_+,mu),1-a/n) >= Lst(C_+,1-a/n) for every mu,
       achieved by the diagonal word U=(V,...,V), whose interleaved list equals
       the base list of V exactly.
  (ii) [a-regular upper bound]  if every row U_i is a-regular then

         |Lambda(Int(C_+,mu),1-a/n,U)| = | intersect_i Supp_{U_i}^{=a} |
                                       <= min_i |Lambda(C_+,1-a/n,U_i)|,

       so interleaving carries NO Cartesian exponent and cannot exceed the base
       list.  Combined with (i): in the a-regular regime the worst-case
       interleaved list equals the base list, for every mu -- the interleaving
       exponent is exactly 1.

Proof of (ii): if |A_i|=a for all i and |intersect A_i|>=a then each A_i equals
the common a-set T, so the tuple is (T,...,T) with T a full agreement support of
every row, i.e. T in intersect_i Supp_{U_i}^{=a}; the map tuple<->T is a
bijection.

Via the deep-point bridge (Sections 1-2), the interleaved-MCA bad-slope-vector
count is therefore governed by the BASE-code list, mu-independently.  The base
list is exactly the L1 locator-fiber object, so the L2 worst-case constant in
this regime coincides with the L1 constant.

Finite toy evidence + exact-count check; no cap / deployed claim.
Status: PROVED (i),(ii) / PROVED-by-check.  Supports L2 and X1.

Run:
    python3 experimental/scripts/verify_x1_worst_case_interleaved.py
    python3 experimental/scripts/verify_x1_worst_case_interleaved.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_x1_interleaved_deep_point import (   # noqa: E402
    multiplicative_subgroup, interpolate, poly_eval, degree,
    quotient_locator_word, dilate, interleaved_list_and_deep,
)


def full_agreement_supports(V, D, k, a, p):
    """Return (tight_supports, is_a_regular):
    tight_supports = set of frozenset full-agreement supports of size exactly a;
    is_a_regular = True iff no listed codeword agrees with V on > a points."""
    tight = set()
    regular = True
    seen_codewords = {}
    for S in combinations(D, a):
        P = interpolate([(x, V[x]) for x in S], p)
        if degree(P, p) >= k + 1:
            continue
        A = frozenset(x for x in D if poly_eval(P, x, p) == V[x])
        seen_codewords[tuple(P)] = len(A)
        if len(A) == a:
            tight.add(A)
        elif len(A) > a:
            regular = False
    return tight, regular, len(seen_codewords)


CONFIGS = [
    # (p, n, k, a)
    (97, 16, 8, 12),
    (193, 16, 8, 12),
]
MUS = [1, 2, 3]


def run() -> dict:
    out_cfgs = []
    all_ok = True
    for (p, n, k, a) in CONFIGS:
        D = multiplicative_subgroup(p, n)
        a0 = 2
        N = n // a0
        V = quotient_locator_word(D, k, n, N, p)        # a-regular row word
        h = next(x for x in D if x != 1)
        tightV, regV, baseV = full_agreement_supports(V, D, k, a, p)
        cfg = {"p": p, "n": n, "k": k, "a": a,
               "base_list": baseV, "a_regular": regV,
               "tight_supports": len(tightV), "rows": []}
        for mu in MUS:
            # diagonal word (lower bound / equality)
            Udiag = [dict(V) for _ in range(mu)]
            diag_tuples, _ = interleaved_list_and_deep(Udiag, D, k, a,
                                                       [x for x in range(p) if x not in set(D)][0], p)
            diag_ok = (len(diag_tuples) == baseV)        # (i) equality

            # non-diagonal a-regular word: row0 = V, others = dilates of V
            U = [dict(V)] + [dilate(V, h, D, p) for _ in range(mu - 1)]
            tights = [full_agreement_supports(U[i], D, k, a, p) for i in range(mu)]
            regs = all(t[1] for t in tights)
            common = set.intersection(*[t[0] for t in tights]) if mu >= 1 else set()
            min_base = min(t[2] for t in tights)
            inter_tuples, _ = interleaved_list_and_deep(
                U, D, k, a, [x for x in range(p) if x not in set(D)][0], p)
            # (ii): a-regular formula  |interleaved| = |common| <= min base
            formula_ok = (len(inter_tuples) == len(common)) if regs else None
            bound_ok = (len(inter_tuples) <= min_base)
            row_ok = diag_ok and bound_ok and (formula_ok is not False)
            cfg["rows"].append({
                "mu": mu, "diag_interleaved": len(diag_tuples), "base": baseV,
                "diag_eq_base": diag_ok,
                "nondiag_interleaved": len(inter_tuples),
                "common_supports": len(common), "min_base": min_base,
                "a_regular": regs, "formula_ok": formula_ok,
                "bound_ok": bound_ok, "ok": row_ok})
            if not row_ok:
                cfg["ok_all"] = False
                all_ok = False
        out_cfgs.append(cfg)
    return {"all_ok": all_ok, "configs": out_cfgs}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
        if not out["all_ok"]:
            raise SystemExit(1)
        return
    print("Worst-case interleaved list vs base list (a-regular regime):")
    print("  (i) diagonal interleaved == base list;  (ii) interleaved == |common supports| <= min base")
    print()
    for c in out["configs"]:
        print(f"  p={c['p']} n={c['n']} k={c['k']} a={c['a']}  "
              f"base_list={c['base_list']}  a_regular={c['a_regular']}  "
              f"tight_supports={c['tight_supports']}")
        for r in c["rows"]:
            print(f"      mu={r['mu']}: diag_interleaved={r['diag_interleaved']}"
                  f"(=base {r['base']}? {r['diag_eq_base']})   "
                  f"nondiag_interleaved={r['nondiag_interleaved']}"
                  f"  common={r['common_supports']}  min_base={r['min_base']}"
                  f"  formula_ok={r['formula_ok']}  bound_ok={r['bound_ok']}")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
