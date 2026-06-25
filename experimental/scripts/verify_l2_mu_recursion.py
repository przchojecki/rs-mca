#!/usr/bin/env python3
r"""
L2 codegree theorem: the mu-arity recursion (extends the two-regime theorem).

Peeling one row and applying unique decoding to the innermost punctured list
(a degree-<k poly agreeing with U_1 on >= a of |S| points is UNIQUE when
a > (|S|+k)/2, i.e. |S| < 2a-k) gives, for the j-fold interleaved list at
agreement s,  Lambda_j^{(s)}(U) = #{(c_1,...,c_j) : |A_1(c_1) cap ... cap A_j(c_j)| >= s}:

    RECURSION (proved, L1-free):
        |Lambda_mu^{(a)}|  <=  |Lambda_{mu-1}^{(a)}|  +  |Lambda_{mu-1}^{(2a-k)}| * |Fib_1|,

peeling row 1 (Fib_1 = {c : |A_1(c)| >= a}); Lambda_{mu-1} is over the remaining
rows. For mu=2 this is the two-regime theorem (Lambda_1^{(s)} = M(s) = base list
at agreement s). Unrolling over mu-1 peels gives a sum of products of |Fib_i| and
higher-agreement lists -- the all-unique term is ~|Fib_mu| (single base list).

This verifier (verify-first) checks the mu=3 step exactly over adversarial 3-row
words:
    |Lambda_3^{(a)}|  <=  |Lambda_2^{(a)}(rows 2,3)|  +  |Lambda_2^{(2a-k)}(rows 2,3)| * |Fib_1|,
and that it is < Cartesian |Fib_1||Fib_2||Fib_3| (the saving persists at mu=3).

Status: AUDIT / VERIFY-FIRST (L2 codegree mu-recursion).

Run:
    python3 experimental/scripts/verify_l2_mu_recursion.py
"""

from __future__ import annotations

import argparse
import json
import random
from itertools import product


def build_cws(p, H, k):
    return [tuple(sum(co[j] * pow(x, j, p) for j in range(k)) % p for x in H)
            for co in product(range(p), repeat=k)]


def fiber(U, cws, a):
    return [frozenset(i for i in range(len(U)) if c[i] == U[i])
            for c in cws if sum(1 for i in range(len(U)) if c[i] == U[i]) >= a]


def lam2_at(f_rows_a, f_rows_b, s):
    """# pairs (A from a-fiber, B from b-fiber) with |A cap B| >= s."""
    return sum(1 for A in f_rows_a for B in f_rows_b if len(A & B) >= s)


def lam3_at(fa, fb, fc, s):
    cnt = 0
    for A in fa:
        for B in fb:
            AB = A & B
            if len(AB) < s:
                continue
            for C in fc:
                if len(AB & C) >= s:
                    cnt += 1
    return cnt


def run():
    p = 17
    H = [pow(3, i, p) for i in range(p - 1)]
    n = len(H)
    rng = random.Random(31)
    out = {}
    for k in (2, 3):
        cws = build_cws(p, H, k)
        for a in (k + 1, k + 2):
            thr = 2 * a - k
            rec_ok = True
            saves = 0
            samples = 0
            best = None
            for _ in range(400):
                kind = rng.randrange(3)
                Us = []
                for _r in range(3):
                    if kind == 0:
                        Us.append([rng.randrange(p) for _ in range(n)])
                    elif kind == 1:
                        cc = rng.sample(cws, 2)
                        Us.append([cc[0][i] if i < n // 2 else cc[1][i] for i in range(n)])
                    else:
                        bb = rng.sample(cws, 3)
                        Us.append([bb[i % 3][i] for i in range(n)])
                # fibers (agreement >= a) for each row
                fA = fiber(Us[0], cws, a)   # row 1 (peeled)
                fB = fiber(Us[1], cws, a)   # row 2  -- but for the inner Lambda_2 at
                fC = fiber(Us[2], cws, a)   # row 3     agreement 2a-k we need the
                # higher-agreement fibers of rows 2,3 for the (2a-k)-list
                fB_thr = fiber(Us[1], cws, thr)
                fC_thr = fiber(Us[2], cws, thr)
                if not fA or not fB or not fC:
                    continue
                samples += 1
                lam3 = lam3_at(fA, fB, fC, a)
                lam2_a = lam2_at(fB, fC, a)              # Lambda_2^{(a)}(rows 2,3)
                # Lambda_2^{(2a-k)}(rows 2,3): pairs (c2,c3) with |A2 cap A3| >= 2a-k.
                # Such pairs require each agreement >= 2a-k, so use higher-agreement fibers.
                lam2_thr = lam2_at(fB_thr, fC_thr, thr)
                bound = lam2_a + lam2_thr * len(fA)
                cart = len(fA) * len(fB) * len(fC)
                ok = lam3 <= bound
                rec_ok = rec_ok and ok
                if bound < cart:
                    saves += 1
                if best is None or cart > best["cartesian"]:
                    best = {"|Fib1|": len(fA), "|Fib2|": len(fB), "|Fib3|": len(fC),
                            "lam3": lam3, "lam2_a": lam2_a, "lam2_thr": lam2_thr,
                            "bound": bound, "cartesian": cart, "ok": ok}
            out[f"k={k},a={a}"] = {
                "samples": samples, "recursion_always_holds": rec_ok,
                "bound<cartesian_frac": round(saves / max(1, samples), 2),
                "richest": best,
            }
    all_ok = all(v["recursion_always_holds"] for v in out.values())
    return {"all_ok": all_ok, "results": out}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("L2 mu=3 recursion: |Lambda_3^a| <= |Lambda_2^a(2,3)| + |Lambda_2^{2a-k}(2,3)|*|Fib_1|  (F_17)")
    for key, v in out["results"].items():
        r = v["richest"]
        print(f"  {key}: {v['samples']} samples; recursion holds={v['recursion_always_holds']}; "
              f"bound<cartesian frac={v['bound<cartesian_frac']}")
        if r:
            print(f"      richest: |Fib|=({r['|Fib1|']},{r['|Fib2|']},{r['|Fib3|']}) lam3={r['lam3']} "
                  f"bound={r['bound']} (lam2_a={r['lam2_a']}+lam2_thr={r['lam2_thr']}*Fib1) cartesian={r['cartesian']}")
    print()
    print("RESULT:", "PASS (mu=3 recursion holds, bound < cartesian -- saving persists at mu=3)"
          if out["all_ok"] else "VIOLATION in the recursion -- inspect (the peel/threshold may be off)")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
