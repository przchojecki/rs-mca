#!/usr/bin/env python3
r"""
Forward interleaved-MCA count: list bound -> interleaved-MCA bad-slope vectors.

Increment 3 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.
Combines the interleaved deep-point identity (Section 2, verified in
`verify_x1_interleaved_deep_point.py`) with the L2 interleaved-list saving
(`notes/l2/l2_interleaved_dilation_constants.md`) to print the explicit forward
count chain, for shared-pole curves from structured (quotient-locator) words:

    ceil( L / (1 + k(L-1)/|Omega|) )                 (averaging lower bound, Lemma 2.1)
      <=  BadVec_max  =  max_alpha |Deep_alpha^mu(U,a)|   (forward interleaved-MCA count)
      <=  L           =  |interleaved C_+ list at delta_a|
      <=  prod_i L_row_i  =  Cartesian per-row product.

Two facts make this useful for Paper C:
  * L is mu-INDEPENDENT for the structured words (does not raise the numerator to
    the mu-th power), the L2 no-Cartesian-exponent saving -- so the
    interleaved-MCA bad-slope-vector count inherits it;
  * the protocol soundness contribution is |BadVec|/q^mu <= L/q^mu, NOT the naive
    (L_row/q)^mu.

Finite toy evidence + an exact-count chain; no cap / deployed / protocol-safety
claim. Status: PROVED-by-check.  Supports X1 (forward) and L2.

Run:
    python3 experimental/scripts/verify_x1_forward_interleaved_count.py
    python3 experimental/scripts/verify_x1_forward_interleaved_count.py --json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_x1_interleaved_deep_point import (   # noqa: E402
    multiplicative_subgroup, poly_eval, quotient_locator_word, dilate,
    interleaved_list_and_deep, bad_slope_vectors, global_far_condition,
)


def single_row_list_size(U_row, D, k, a, alpha, p) -> int:
    tuples, _ = interleaved_list_and_deep([U_row], D, k, a, alpha, p)
    return len(tuples)


def deep_image_from_tuples(tuples, alpha, p) -> set:
    return {tuple(poly_eval(list(P), alpha, p) for P in tup) for tup in tuples}


# structured configs (p, n, k, a, mu); a = k + 2*a0 with a0 = n//N, N = n//2
CONFIGS = [
    (97, 16, 8, 12, 2),
    (97, 16, 8, 12, 3),
    (193, 16, 8, 12, 2),
    (193, 16, 8, 12, 3),
]


def run() -> dict:
    rows_out = []
    all_ok = True
    for (p, n, k, a, mu) in CONFIGS:
        D = multiplicative_subgroup(p, n)
        Dset = set(D)
        Omega = [al for al in range(p) if al not in Dset]
        alpha0 = Omega[0]
        assert global_far_condition(D, k, alpha0, p)
        a0 = 2
        N = n // a0
        U0 = quotient_locator_word(D, k, n, N, p)
        h = next(x for x in D if x != 1)
        # genuinely non-diagonal interleaving: row0 = U0, others = dilates
        U = [dict(U0)] + [dilate(U0, h, D, p) for _ in range(mu - 1)]

        L_row = [single_row_list_size(U[i], D, k, a, alpha0, p) for i in range(mu)]
        cart = 1
        for lr in L_row:
            cart *= lr

        tuples, _ = interleaved_list_and_deep(U, D, k, a, alpha0, p)
        L = len(tuples)
        # forward interleaved-MCA count = max over deep points of |Deep_alpha^mu|
        bad_max, argmax = 0, alpha0
        for al in Omega:
            m = len(deep_image_from_tuples(tuples, al, p))
            if m > bad_max:
                bad_max, argmax = m, al
        # cross-check the identity at the argmax deep point
        badvec_at_argmax = len(bad_slope_vectors(U, D, k, a, argmax, p))
        deep_at_argmax = len(deep_image_from_tuples(tuples, argmax, p))
        identity_ok = (badvec_at_argmax == deep_at_argmax == bad_max)

        avg_lb = math.ceil(L / (1 + k * (L - 1) / len(Omega))) if L else 0
        chain_ok = (avg_lb <= bad_max <= L <= cart)
        ok = identity_ok and chain_ok
        rows_out.append({
            "p": p, "n": n, "k": k, "a": a, "mu": mu, "omega": len(Omega),
            "L_row": L_row, "cartesian": cart, "L_interleaved": L,
            "badvec_max": bad_max, "avg_lower_bound": avg_lb,
            "saving_L_over_cart": (L / cart if cart else None),
            "density_badvec_over_qmu": bad_max / (p ** mu),
            "density_cart_over_qmu": cart / (p ** mu),
            "identity_ok": identity_ok, "chain_ok": chain_ok, "ok": ok,
        })
        if not ok:
            all_ok = False
    return {"all_ok": all_ok, "rows": rows_out}


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
    print("Forward interleaved-MCA count chain (X1 / L2), structured words:")
    print("  avg_lb <= BadVec_max = max_a |Deep_a^mu| <= L(interleaved) <= Cartesian")
    print()
    # group by (p,n,k) to show mu-independence of L
    for r in out["rows"]:
        print(f"  p={r['p']} n={r['n']} k={r['k']} a={r['a']} mu={r['mu']}"
              f"  |Omega|={r['omega']}")
        print(f"      per-row lists L_row={r['L_row']}  Cartesian prod={r['cartesian']}")
        print(f"      L(interleaved)={r['L_interleaved']}   "
              f"BadVec_max={r['badvec_max']}   avg_lb={r['avg_lower_bound']}")
        print(f"      saving L/Cartesian={r['saving_L_over_cart']:.4f}   "
              f"chain_ok={r['chain_ok']}  identity_ok={r['identity_ok']}")
    print()
    # explicit mu-independence callout
    by_pk = {}
    for r in out["rows"]:
        by_pk.setdefault((r["p"], r["n"], r["k"]), {})[r["mu"]] = r["L_interleaved"]
    for (p, n, k), d in by_pk.items():
        mus = sorted(d)
        same = len(set(d[m] for m in mus)) == 1
        print(f"  mu-independence  p={p},n={n},k={k}: "
              f"L={[d[m] for m in mus]} for mu={mus}  "
              f"-> {'CONSTANT in mu (no Cartesian exponent)' if same else 'VARIES'}")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
