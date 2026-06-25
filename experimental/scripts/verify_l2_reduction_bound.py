#!/usr/bin/env python3
r"""
L2 codegree theorem, step 2b/3: verify the stratified-sum reduction bound and pin
the exact L1-input the saving needs.

REDUCTION (codegree decomposition + step 2a):
    |Lambda_2|  =  sum_{c2 in Fib_2} (punctured list of U1 on A_2(c2))
                <=  sum_{c2 in Fib_2} D(|A_2(c2)|)
                 =  sum_{N2} M_2(N2) * D(N2),
where M_2(N2) = #{c2 in Fib_2 : |A_2(c2)| = N2} (the L1 agreement-size profile)
and D(N') <= N'(N'-k+1)/(a^2-N'(k-1)) is the per-N' punctured-RS list (step 2a),
with D <= |Fib_1| always.

SAVING CONDITION (exponent B, not 2B). |Fib_i| ~ n^B above the reserve (L1). The
saving |Lambda_2| <= n^{B+O(1)} holds iff
    M_2(N2) * D(N2)  <=  poly * n^B   uniformly in N2.
At the ends this is automatic: N2=a (M_2 ~ |Fib2| ~ n^B, D=1) and N2=n
(M_2 = O(1), D ~ |Fib1| ~ n^B). The interior is the genuine L1-profile input.

This script (verify-first): over adversarial (U1,U2), confirms the reduction bound
|Lambda_2| <= sum_{c2} min(Johnson(|A2(c2)|), |Fib1|), measures its tightness vs
the actual interleaved list, locates which agreement-size stratum carries the
interleaved mass, and reports the product M_2(N2)*D(N2) vs |Fib| (the saving
condition).

Status: AUDIT / VERIFY-FIRST (L2 codegree reduction bound + saving condition).

Run:
    python3 experimental/scripts/verify_l2_reduction_bound.py
    python3 experimental/scripts/verify_l2_reduction_bound.py --json
"""

from __future__ import annotations

import argparse
import json
import random
from itertools import product


def johnson(Np, k, a):
    if a > (Np + k) / 2:
        return 1
    den = a * a - Np * (k - 1)
    return None if den <= 0 else Np * (Np - k + 1) / den  # None = vacuous


def build_cws(p, H, k):
    return [tuple(sum(co[j] * pow(x, j, p) for j in range(k)) % p for x in H)
            for co in product(range(p), repeat=k)]


def fiber(U, cws, a):
    out = []
    for c in cws:
        A = frozenset(i for i in range(len(U)) if c[i] == U[i])
        if len(A) >= a:
            out.append((c, A))
    return out


def analyze(U1, U2, cws, a, n, k):
    f1 = fiber(U1, cws, a)
    f2 = fiber(U2, cws, a)
    if not f1 or not f2:
        return None
    F1 = len(f1)
    # actual interleaved, and per-c2 punctured list + stratum
    lam = 0
    strata = {}   # N2 -> [count M2(N2), sum of actual punctured lists]
    reduction = 0.0
    for (_, A2) in f2:
        plist = sum(1 for (_, A1) in f1 if len(A1 & A2) >= a)
        lam += plist
        N2 = len(A2)
        jb = johnson(N2, k, a)
        D = F1 if jb is None else min(jb, F1)
        reduction += D
        s = strata.setdefault(N2, [0, 0, 0.0])
        s[0] += 1; s[1] += plist; s[2] += D
    # CLEAN TWO-REGIME BOUND: D=1 for N2 < 2a-k (unique decoding), D <= |Fib1| else.
    # |Lambda_2| <= |Fib2| + M2(2a-k)*|Fib1|, where M2(s)=#{c2:|A2(c2)|>=s}.
    thr = 2 * a - k                                  # = a + sigma
    M2_tail = sum(1 for (_, A2) in f2 if len(A2) >= thr)
    two_regime = len(f2) + M2_tail * F1
    # saving condition: max over N2 of M2(N2)*D(N2)  vs  |Fib1|*|Fib2|
    Fib = max(F1, len(f2))
    max_prod = max((m * (jb if (jb := johnson(N2, k, a)) is not None else F1))
                   for N2, (m, _, _) in strata.items())
    # which stratum carries the interleaved mass
    mass_stratum = max(strata.items(), key=lambda kv: kv[1][1]) if lam else (None, [0, 0, 0])
    return {
        "|Fib1|": F1, "|Fib2|": len(f2), "interleaved": lam,
        "reduction_bound": round(reduction, 1),
        "two_regime_bound |F2|+M2(2a-k)|F1|": two_regime,
        "M2_tail(2a-k)": M2_tail,
        "lam<=two_regime": lam <= two_regime,
        "two_regime<cartesian": two_regime < F1 * len(f2),
        "lam<=reduction": lam <= reduction + 1e-9,
        "reduction<cartesian": reduction < F1 * len(f2),
        "tightness lam/reduction": round(lam / reduction, 3) if reduction else None,
        "max_M2D_product": round(max_prod, 1), "cartesian": F1 * len(f2),
        "saving_cond max_M2D<=Fib": max_prod <= Fib + 1e-9,
        "mass at N2": mass_stratum[0],
    }


def run():
    p = 17
    H = [pow(3, i, p) for i in range(p - 1)]
    n = len(H)
    rng = random.Random(20260625)
    out = {}
    for k in (2, 3):
        cws = build_cws(p, H, k)
        for a in (k + 1, k + 2):
            red_ok = True
            two_ok = True
            two_saves = 0
            best = None
            saving_cond_holds = 0
            samples = 0
            for _ in range(500):
                kind = rng.randrange(4)
                if kind == 0:
                    U1 = [rng.randrange(p) for _ in range(n)]; U2 = [rng.randrange(p) for _ in range(n)]
                elif kind == 1:
                    cc = rng.sample(cws, 4)
                    U1 = [cc[0][i] if i < n // 2 else cc[1][i] for i in range(n)]
                    U2 = [cc[2][i] if i < n // 2 else cc[3][i] for i in range(n)]
                elif kind == 2:
                    b1 = rng.sample(cws, 3); b2 = rng.sample(cws, 3)
                    U1 = [b1[i % 3][i] for i in range(n)]; U2 = [b2[i % 3][i] for i in range(n)]
                else:
                    c1, c2 = rng.choice(cws), rng.choice(cws)
                    U1 = list(c1); U2 = list(c2)
                    for _ in range(rng.randint(1, 4)):
                        U1[rng.randrange(n)] = rng.randrange(p); U2[rng.randrange(n)] = rng.randrange(p)
                r = analyze(U1, U2, cws, a, n, k)
                if r is None:
                    continue
                samples += 1
                red_ok = red_ok and r["lam<=reduction"]
                two_ok = two_ok and r["lam<=two_regime"]
                if r["two_regime<cartesian"]:
                    two_saves += 1
                if r["saving_cond max_M2D<=Fib"]:
                    saving_cond_holds += 1
                if best is None or r["cartesian"] > best["cartesian"]:
                    best = r
            out[f"k={k},a={a}"] = {
                "samples": samples, "reduction_bound_always_holds": red_ok,
                "two_regime_always_holds": two_ok,
                "two_regime_saves_frac": round(two_saves / max(1, samples), 2),
                "saving_cond_holds_frac": round(saving_cond_holds / max(1, samples), 2),
                "richest": best,
            }
    all_ok = all(v["reduction_bound_always_holds"] and v["two_regime_always_holds"]
                 for v in out.values())
    return {"all_ok": all_ok, "results": out}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("L2 reduction bound |Lambda_2| <= sum_{c2} D(|A2(c2)|), and the saving condition (F_17).")
    for key, v in out["results"].items():
        r = v["richest"]
        print(f"  {key}: {v['samples']} samples; reduction holds={v['reduction_bound_always_holds']}; "
              f"TWO-REGIME |F2|+M2(2a-k)|F1| holds={v['two_regime_always_holds']} "
              f"(saves vs cartesian frac={v['two_regime_saves_frac']})")
        print(f"      richest: |Fib1|={r['|Fib1|']} |Fib2|={r['|Fib2|']} interleaved={r['interleaved']} "
              f"two_regime={r['two_regime_bound |F2|+M2(2a-k)|F1|']} (M2_tail={r['M2_tail(2a-k)']}) "
              f"cartesian={r['cartesian']}")
    print()
    print("RESULT:", "PASS (reduction bound holds; saving condition + mass location measured)"
          if out["all_ok"] else "VIOLATION in the reduction bound -- inspect (should be a provable <=)")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
