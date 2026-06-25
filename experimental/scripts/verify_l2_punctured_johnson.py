#!/usr/bin/env python3
r"""
L2 codegree theorem, step 2: bound the inner punctured-RS list D(n,k,a).

The codegree decomposition (verify_l2_codegree_decomposition.py, in main) gives
    |Lambda_2(U,a)| = sum_{c1 in Fib_1} |punctured-RS list of U_2 on A_1(c1)|,
so the saving reduces to bounding the inner list
    L(A, U2) = #{ P in F[X]_{<k} : |{x in A : P(x) = U2(x)}| >= a },
the RS[F, A, k] list at agreement a on the punctured domain A = A_1(c1) (size N').
This script MEASURES the worst-case L over adversarial (A, U2) and checks it
against the predicted bound (verify-first, before any claim).

PREDICTED BOUND (Johnson / Fisher second moment). Distinct deg-<k codewords agree
on <= k-1 points, so the list's agreement sets are >= a, pairwise <= k-1. Double
counting deg(x) = #{listed P : x in A, P(x)=U2(x)}:
    (L a)^2 <= (sum_x deg x)^2 <= N' sum_x deg(x)^2
            <= N'[ L(L-1)(k-1) + L N' ],
hence, when a^2 > N'(k-1),
    L <= N'(N'-k+1) / (a^2 - N'(k-1))   =: Johnson(N',k,a),
and L = 1 (unique decoding) when a > (N'+k)/2.  D(n,k,a) := max_{a<=N'<=n} of
the worst-case L; the bound is monotone-ish in N', so the binding N' is checked.

CHECK: for each (N', a), the measured worst-case L (over random + planted
adversarial U2 that glues/overlaps many codewords) must satisfy L <= Johnson.
If it does across the sweep, the qualitative bound D <= Johnson is supported.

Status: AUDIT / VERIFY-FIRST scan for the L2 codegree theorem (step 2).

Run:
    python3 experimental/scripts/verify_l2_punctured_johnson.py
    python3 experimental/scripts/verify_l2_punctured_johnson.py --json
"""

from __future__ import annotations

import argparse
import json
import random
from itertools import product, combinations


def johnson_bound(Np, k, a):
    """N'(N'-k+1)/(a^2 - N'(k-1)) when a^2 > N'(k-1); unique (1) when a>(N'+k)/2."""
    if a > (Np + k) / 2:
        return 1
    denom = a * a - Np * (k - 1)
    if denom <= 0:
        return None  # bound vacuous in this regime
    return Np * (Np - k + 1) / denom


def list_size(p, A, U2, k):
    """#{deg-<k poly P over F_p : |{i : P(A[i]) = U2[i]}| >= a-implicit}; returns
    the agreement multiset; caller thresholds. Enumerate all q^k polys."""
    best = {}
    polys = product(range(p), repeat=k)
    counts = []
    for co in polys:
        agree = sum(1 for i, x in enumerate(A) if
                    sum(co[j] * pow(x, j, p) for j in range(k)) % p == U2[i])
        counts.append(agree)
    return counts


def worst_case_L(p, H, k, Np, a, trials, rng):
    """Max list size over adversarial U2 on a size-N' subset A of H."""
    A = H[:Np]
    best = 0
    best_desc = ""
    # codeword evaluations on A, precomputed
    cw = []
    for co in product(range(p), repeat=k):
        cw.append(tuple(sum(co[j] * pow(x, j, p) for j in range(k)) % p for x in A))
    # candidate U2 families:
    def count(U2):
        return sum(1 for c in cw if sum(1 for i in range(Np) if c[i] == U2[i]) >= a)
    # (1) random words
    for _ in range(trials):
        U2 = [rng.randrange(p) for _ in range(Np)]
        L = count(U2)
        if L > best:
            best, best_desc = L, "random"
    # (2) planted: glue t codewords on disjoint chunks (each chunk >= a)
    t_max = Np // a
    for t in range(2, max(2, t_max) + 1):
        for _ in range(min(trials, 200)):
            chosen = rng.sample(cw, min(t, len(cw)))
            U2 = [0] * Np
            # assign chunks
            idx = 0
            for ci, c in enumerate(chosen):
                end = min(Np, idx + max(a, Np // len(chosen)))
                for i in range(idx, end):
                    U2[i] = c[i]
                idx = end
            for i in range(idx, Np):
                U2[i] = chosen[-1][i]
            L = count(U2)
            if L > best:
                best, best_desc = L, f"planted t={t}"
    # (3) planted: common-core overlap (codewords sharing a (k-1)-core, U2 = on union)
    for _ in range(min(trials, 200)):
        core = rng.sample(range(Np), min(k - 1, Np))
        chosen = rng.sample(cw, min(Np // (a - (k - 1) if a > k - 1 else 1) + 2, len(cw)))
        U2 = [0] * Np
        # core: set to one codeword's values (all that agree on core counted)
        base = chosen[0]
        for i in core:
            U2[i] = base[i]
        rest = [i for i in range(Np) if i not in core]
        # spread chosen codewords over rest in blocks of size a-(k-1)
        blk = max(1, a - (k - 1))
        idx = 0
        for c in chosen:
            for i in rest[idx:idx + blk]:
                U2[i] = c[i]
            idx += blk
            if idx >= len(rest):
                break
        for i in rest[idx:]:
            U2[i] = chosen[-1][i]
        L = count(U2)
        if L > best:
            best, best_desc = L, "core-overlap"
    return best, best_desc


def run():
    p = 17
    H = [pow(3, i, p) for i in range(p - 1)]  # F_17^* (n=16)
    rng = random.Random(20260625)
    rows = []
    all_ok = True
    for k in (2, 3):
        for Np in range(6, len(H) + 1, 2):
            for a in range(k + 1, Np + 1):
                jb = johnson_bound(Np, k, a)
                if jb is None:
                    continue  # bound vacuous (a^2 <= N'(k-1)); skip
                Lmax, desc = worst_case_L(p, H, k, Np, a, trials=400, rng=rng)
                ok = Lmax <= jb + 1e-9
                all_ok = all_ok and ok
                rows.append({"k": k, "Np": Np, "a": a, "L_measured": Lmax,
                             "johnson": round(jb, 2), "unique": jb == 1,
                             "ok": ok, "witness": desc})
    # only keep informative rows (L_measured >= 2 or violations) for the table
    interesting = [r for r in rows if r["L_measured"] >= 2 or not r["ok"]]
    return {"all_ok": all_ok, "num_checks": len(rows),
            "num_violations": sum(1 for r in rows if not r["ok"]),
            "rows": interesting[:40]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("L2 punctured-RS list (step 2): measured worst-case L vs Johnson bound (F_17).")
    print(f"  {out['num_checks']} (N',a,k) checks; {out['num_violations']} violations.")
    print(f"  {'k':>2} {'Np':>4} {'a':>3} {'L_meas':>6} {'johnson':>8} {'uniq':>5}  ok  witness")
    for r in out["rows"]:
        print(f"  {r['k']:>2} {r['Np']:>4} {r['a']:>3} {r['L_measured']:>6} {r['johnson']:>8} "
              f"{str(r['unique']):>5}  {'OK ' if r['ok'] else 'FAIL'} {r['witness']}")
    print()
    print("RESULT:", "PASS (measured punctured list <= Johnson bound across the sweep "
          "-- supports D <= Johnson(N',k,a))" if out["all_ok"]
          else "VIOLATION -- the Johnson bound form needs correction (verify-first caught it)")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
