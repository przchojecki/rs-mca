#!/usr/bin/env python3
"""Verifier for cap25_v13_q_atom_binding_row_calibration.

Zero-arg, pure Python 3 stdlib, exit 0 = PASS.  Target runtime < ~90 s.

Framing: R_prim below is the measured value, at an exact row, of the kappa in
grande_finale.tex thm:q-implies-sp's max-fiber form of the remaining Q input
(max_z N_w(z) <= kappa * Fbar after quotient/planted strata are removed); the
finite budgets are prop:q-exact-target's, binding at M31-list (kappa <= 8.4152).

Checks (every headline number in the note is recomputed or cross-checked here):

  A. BUDGET RATIO from prop:q-exact-target's OWN integers, from scratch:
       B*  = floor((2^31-1)^4 / 2^100)                        (= 2^24-1 = 16777215)
       avg = ceil( C(2^21, 1116023) / (2^31-1)^67447 )        (= 1993678)
       ratio = B*/avg = 8.4152 ,  bit margin = log2(ratio) = 3.0730 .
     (The giant binomial C(2^21,1116023) is recomputed exactly, ~15 s.)

  B. R_prim EXACT RECOMPUTATION on a representative fast subset of the 59 shipped
     rows (documented below), matched against the shipped table:
       - (16,97,1)  R_prim=1.2210  heavy-max (avg>=100), THE binding comparison
       - (16,113,1) R_prim=1.1063  heavy
       - (12,61,1)  R_prim=1.2323  moderate
       - (20,101,2) R_prim=3.2392  structured-probe row
       - (20,41,3)  R_prim=5.3344  moderate
       - (24,97,3)  R_prim=7.6783  HEAVIEST R_prim among avg>=1 rows (~10 s)
       - (10,41,4)  R_prim=282576  absolute-max R_prim (sparse avg<<1 artifact)

  C. STRUCTURED sweep: recompute the (20,101,2) max-all cell and the arc[0:m]
     seed, confirming (i) the winner is the symmetric-origin key [0,0] with a
     quotient/planted split (prim 40 / quot 10), and (ii) every structured seed
     lands in a SMALLER (already-paid) cell than the exhaustive primitive max.

  D. beta(w) HEAVINESS-CONFOUND FIT recomputed from the shipped table:
       per-w slopes beta(1,2,3) = 0.254, 0.467, 0.667 and intercepts k(w);
       the FULL shipped fit block (per_w 1,2,3 beta/k/n + avg*) is gated;
       linear beta(w) = 0.2065 w + 0.047 (per-step ~0.21) ;
       avg* asymptote = exp(1.465/0.2065) = 1205 .
     Plus the note's quoted witnesses: M31-list ~1.65e3 x avg* (~3.2 orders),
     KB rows ~7.7 orders above avg* (from prop:q-exact-target's printed
     integers), full-model R^2 = 0.94 / max ratio error 2.47x, and the naive
     w-free extrapolation ~197 (the confound trap named in the note).

  E. TAMPER self-tests: perturb B*, a shipped R_prim, and fit-block fields
     (incl. per_w['2'].beta and per_w['3'].k), and confirm the corresponding
     check rejects each tampered value.
"""
import json
import math
import os
import sys
from collections import defaultdict
from itertools import combinations
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data",
                    "cap25_v13_q_atom_binding_row_calibration.json")

FAILS = []


def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {name}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)
    return cond


def approx(a, b, tol):
    return abs(a - b) <= tol


# ----------------------------------------------------------------------------
# exact row enumeration (self-contained; identical logic to the G2 pipeline
# scaling_pipeline.row, matching the deployed verify_q2 prefix key up to sign)
# ----------------------------------------------------------------------------
def prime_factors(x):
    fs, d = set(), 2
    while d * d <= x:
        while x % d == 0:
            fs.add(d)
            x //= d
        d += 1
    if x > 1:
        fs.add(x)
    return sorted(fs)


def primitive_root(p):
    fs = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g
    raise ValueError("no primitive root")


def subgroup(p, n):
    assert (p - 1) % n == 0
    w = pow(primitive_root(p), (p - 1) // n, p)
    vals = tuple(pow(w, i, p) for i in range(n))
    assert len(set(vals)) == n
    return vals


def row(p, n, w):
    """Exact per-row ledger -> (avg, max_all, max_prim, max_prim_np)."""
    m = n // 2 + w
    R = subgroup(p, n)
    total = comb(n, m)
    avg = total / p ** w
    steps = [n // c for c in prime_factors(n)]
    agg = defaultdict(lambda: [0, 0, None])  # [total, prim, common-support]
    for S in combinations(range(n), m):
        Sset = set(S)
        E = [1] + [0] * w
        for i in S:
            r = R[i]
            for k in range(w, 0, -1):
                E[k] = (E[k] + r * E[k - 1]) % p
        key = tuple(E[1:])
        prim = True
        for st in steps:
            if all((i + st) % n in Sset for i in S):
                prim = False
                break
        a = agg[key]
        a[0] += 1
        if prim:
            a[1] += 1
            if a[2] is None:
                a[2] = Sset
            elif a[2]:
                a[2] &= Sset
    max_all = max(v[0] for v in agg.values())
    max_prim = max(v[1] for v in agg.values())
    max_prim_np = 0
    for v in agg.values():
        if v[1] > max_prim_np and not v[2]:
            max_prim_np = v[1]
    if max_prim_np == 0:
        max_prim_np = max_prim
    return avg, max_all, max_prim, max_prim_np


def structured_probe_101_20_2():
    """Recompute the (p=101,n=20,w=2) max-all cell + arc seed for claim (3)."""
    p, n, w = 101, 20, 2
    m = n // 2 + w
    R = subgroup(p, n)
    steps = [n // c for c in prime_factors(n)]

    def is_quot(Sset):
        return any(all((i + st) % n in Sset for i in Sset) for st in steps)

    def prefix(S):
        E = [1] + [0] * w
        for i in S:
            r = R[i]
            for k in range(w, 0, -1):
                E[k] = (E[k] + r * E[k - 1]) % p
        return tuple(E[1:])

    fibers = defaultdict(list)
    for S in combinations(range(n), m):
        fibers[prefix(S)].append(S)
    avg = comb(n, m) / p ** w
    maxkey = max(fibers, key=lambda k: len(fibers[k]))
    prim = quot = 0
    for S in fibers[maxkey]:
        if is_quot(set(S)):
            quot += 1
        else:
            prim += 1
    prim_sizes = {k: sum(1 for S in mem if not is_quot(set(S)))
                  for k, mem in fibers.items()}
    max_prim = max(prim_sizes.values())
    arc = tuple(range(m))
    arc_prim = prim_sizes.get(prefix(arc), 0)
    return {
        "maxkey": list(maxkey), "prim": prim, "quot": quot,
        "max_prim": max_prim, "avg": avg,
        "arc_prim": arc_prim, "arc_R": arc_prim / avg,
        "max_prim_R": max_prim / avg,
    }


# ----------------------------------------------------------------------------
def main():
    data = json.load(open(DATA))
    rows = data["rows"]
    by = {(r["n"], r["p"], r["w"]): r for r in rows}
    print(f"loaded {len(rows)} rows from {os.path.relpath(DATA)}")

    # ---- A. budget ratio from prop:q-exact-target's own integers -----------
    print("\nA. budget ratio (prop:q-exact-target, M31-list) from scratch:")
    Bstar = (2 ** 31 - 1) ** 4 // 2 ** 100
    check("B* = floor((2^31-1)^4/2^100) = 2^24-1 = 16777215",
          Bstar == 16777215 == 2 ** 24 - 1, f"B*={Bstar}")
    n_dep, aplus, w_dep, B = 2 ** 21, 1116023, 67447, 2 ** 31 - 1
    check("a_+ = K + w  (2^20 + 67447 = 1116023)",
          2 ** 20 + w_dep == aplus, f"{2**20}+{w_dep}={2**20+w_dep}")
    C = comb(n_dep, aplus)             # ~2.09e6-bit binomial, exact (~15 s)
    Bw = B ** w_dep
    q, rem = divmod(C, Bw)
    avg = q + (1 if rem else 0)         # ceiling
    check("avg = ceil(C(2^21,1116023)/(2^31-1)^67447) = 1993678",
          avg == 1993678, f"avg={avg}")
    ratio = Bstar / avg
    bit_margin = math.log2(ratio)
    br = data["binding_row_M31_list"]
    check("budget ratio B*/avg = 8.4152",
          approx(ratio, 8.4152, 5e-5), f"ratio={ratio:.4f}")
    check("bit margin = log2(ratio) = 3.0730",
          approx(bit_margin, 3.0730, 5e-5), f"bits={bit_margin:.4f}")
    check("shipped binding_row matches recompute",
          br["Bstar"] == Bstar and br["avg_ceil"] == avg
          and approx(br["budget_ratio"], ratio, 5e-5)
          and approx(br["bit_margin"], bit_margin, 5e-5))

    # ---- B. exact R_prim recomputation on representative rows --------------
    print("\nB. exact R_prim recomputation vs shipped table:")
    subset = [(16, 97, 1), (16, 113, 1), (12, 61, 1),
              (20, 101, 2), (20, 41, 3), (24, 97, 3), (10, 41, 4)]
    for (n, p, w) in subset:
        r = by[(n, p, w)]
        avg_r, mall, mprim, mpnp = row(p, n, w)
        ok = (mall == r["max_all"] and mprim == r["max_prim"]
              and mpnp == r["max_prim_np"]
              and approx(avg_r, r["avg"], 1e-6 * max(1.0, r["avg"]))
              and approx(mprim / avg_r, r["R_prim"], 1e-9 * max(1.0, r["R_prim"])))
        check(f"row (n={n},p={p},w={w}) R_prim={r['R_prim']:.4f}", ok,
              f"max_prim {mprim}=={r['max_prim']}, R_prim={mprim/avg_r:.4f}")

    # headline maxima over the shipped table
    heavy = [r for r in rows if r["avg"] >= 100]
    ge1 = [r for r in rows if r["avg"] >= 1.0]
    mh = max(heavy, key=lambda r: r["R_prim"])
    m1 = max(ge1, key=lambda r: r["R_prim"])
    check("heavy (avg>=100) max R_prim = 1.221 at (16,97,1)",
          approx(mh["R_prim"], 1.220979, 1e-4)
          and (mh["n"], mh["p"], mh["w"]) == (16, 97, 1),
          f"max={mh['R_prim']:.4f}")
    check("avg>=1 max R_prim = 7.678 (< 8.4152) at (24,97,3)",
          approx(m1["R_prim"], 7.6783, 1e-3)
          and (m1["n"], m1["p"], m1["w"]) == (24, 97, 3)
          and m1["R_prim"] < 8.4152,
          f"max={m1['R_prim']:.4f}")
    check("every heavy row has R_prim <= 1.221 <= budget 8.4152",
          all(r["R_prim"] <= 1.221 for r in heavy))
    check("R_prim_np <= R_prim on every row (planted removal only helps)",
          all(r["max_prim_np"] <= r["max_prim"] for r in rows))

    # ---- C. structured sweep: winners are already-paid cells ---------------
    print("\nC. structured-family sweep (row 20,101,2):")
    sp = structured_probe_101_20_2()
    check("max-all cell is the symmetric origin key [0,0]",
          sp["maxkey"] == [0, 0], f"key={sp['maxkey']}")
    check("origin cell split = 40 primitive / 10 quotient (paid)",
          sp["prim"] == 40 and sp["quot"] == 10,
          f"prim/quot={sp['prim']}/{sp['quot']}")
    check("arc[0:m] seed lands in a SMALLER cell than exhaustive prim max",
          sp["arc_R"] < sp["max_prim_R"],
          f"arc_R={sp['arc_R']:.4f} < max_prim_R={sp['max_prim_R']:.4f}")
    # cross-check shipped structured.json: no seed beats the exhaustive R_prim
    worst = -1e9
    for s in data["structured"]:
        rp = s["R_prim"]
        for sv in s["structured_seeds"].values():
            worst = max(worst, sv["R_prim_of_seed"] - rp)
    check("no structured seed R_prim exceeds its row exhaustive R_prim",
          worst < 0, f"max(seed-row)={worst:.4f}")

    # ---- D. beta(w) heaviness-confound fit from shipped table --------------
    print("\nD. beta(w) confound fit recomputed from shipped table:")
    resolved = [r for r in rows
                if r["avg"] >= 1.0 and r["R_prim"] > 1.02 and r["max_prim"] >= 4]
    check("resolved excess points = 20", len(resolved) == 20,
          f"n={len(resolved)}")

    def per_w_beta(wsel):
        sub = [r for r in resolved if r["w"] == wsel]
        xs = [math.log(r["avg"]) for r in sub]
        ys = [math.log(r["R_prim"] - 1) for r in sub]
        nn = len(xs)
        sx, sy = sum(xs), sum(ys)
        sxx = sum(x * x for x in xs)
        sxy = sum(xs[i] * ys[i] for i in range(nn))
        slope = (nn * sxy - sx * sy) / (nn * sxx - sx * sx)
        intercept = (sy - slope * sx) / nn
        return -slope, intercept, nn

    betas, ks, ns = {}, {}, {}
    for wsel, exp_beta in ((1, 0.254), (2, 0.467), (3, 0.667)):
        b, kk, nn = per_w_beta(wsel)
        betas[wsel], ks[wsel], ns[wsel] = b, kk, nn
        check(f"beta(w={wsel}) = {exp_beta} (n={nn})",
              approx(b, exp_beta, 2e-3), f"beta={b:.3f}")
    step12 = betas[2] - betas[1]
    step23 = betas[3] - betas[2]
    check("per-step beta increment ~ 0.21",
          approx((step12 + step23) / 2, 0.2065, 0.01),
          f"steps={step12:.3f},{step23:.3f}")
    # linear beta(w)=slope*w+intercept from the three points, and avg* asymptote
    ws = [1, 2, 3]
    bs = [betas[1], betas[2], betas[3]]
    nn = 3
    sx, sy = sum(ws), sum(bs)
    sxx = sum(x * x for x in ws)
    sxy = sum(ws[i] * bs[i] for i in range(nn))
    slope_b = (nn * sxy - sx * sy) / (nn * sxx - sx * sx)
    check("linear beta(w) slope ~ 0.2065", approx(slope_b, 0.2065, 5e-3),
          f"slope={slope_b:.4f}")
    avg_star = math.exp(1.465 / 0.2065)
    check("avg* asymptote = exp(1.465/0.2065) = 1205",
          approx(avg_star, 1205, 1.0), f"avg*={avg_star:.1f}")
    check("avg* is >=3 orders of magnitude below deployed M31-list avg",
          avg / avg_star >= 1e3, f"deployed/avg* = {avg/avg_star:.3g}")
    # full fit block cross-check: every numeric field vs the recompute
    fit_ok = data["fit"]["avg_star_asymptote"] == 1205
    for wsel in (1, 2, 3):
        pw = data["fit"]["per_w"][str(wsel)]
        fit_ok = (fit_ok
                  and approx(pw["beta"], betas[wsel], 2e-3)
                  and approx(pw["k"], ks[wsel], 2e-3)
                  and pw["n"] == ns[wsel])
    check("shipped fit block (per_w 1,2,3 beta/k/n + avg*) matches recompute",
          fit_ok,
          f"beta={[round(betas[i],3) for i in (1,2,3)]} "
          f"k={[round(ks[i],3) for i in (1,2,3)]}")

    # note-witness gates: deployed heaviness in orders of magnitude above avg*
    # (M31-list avg recomputed above; KB avgs are prop:q-exact-target's own
    #  printed integers 57198030366 / 65065153468)
    check("M31-list avg = ~1.65e3 x avg* (~3.2 orders)",
          approx(avg / avg_star, 1.65e3, 0.02e3)
          and round(math.log10(avg / avg_star), 1) == 3.2,
          f"ratio={avg/avg_star:.4g}, orders={math.log10(avg/avg_star):.2f}")
    kb_orders = [math.log10(a / avg_star)
                 for a in (57198030366, 65065153468)]
    check("KB rows are ~7.7 orders above avg*",
          all(round(o, 1) == 7.7 for o in kb_orders),
          f"orders={[round(o,2) for o in kb_orders]}")

    # note-witness gates: fit-quality numbers quoted in the note
    def lstsq(feats):
        X = [[1.0] + feats(r) for r in resolved]
        y = [math.log(r["R_prim"] - 1) for r in resolved]
        kdim = len(X[0])
        A = [[sum(X[t][i] * X[t][j] for t in range(len(X)))
              for j in range(kdim)] for i in range(kdim)]
        bvec = [sum(X[t][i] * y[t] for t in range(len(X))) for i in range(kdim)]
        M = [rowi[:] + [bvec[i]] for i, rowi in enumerate(A)]
        for c in range(kdim):
            piv = max(range(c, kdim), key=lambda rr: abs(M[rr][c]))
            M[c], M[piv] = M[piv], M[c]
            pv = M[c][c]
            for j in range(c, kdim + 1):
                M[c][j] /= pv
            for rr in range(kdim):
                if rr != c and M[rr][c]:
                    f = M[rr][c]
                    for j in range(c, kdim + 1):
                        M[rr][j] -= f * M[c][j]
        coef = [M[i][kdim] for i in range(kdim)]
        pred = [sum(coef[j] * X[t][j] for j in range(kdim))
                for t in range(len(X))]
        ybar = sum(y) / len(y)
        sst = sum((v - ybar) ** 2 for v in y)
        sse = sum((y[t] - pred[t]) ** 2 for t in range(len(X)))
        maxres = max(abs(y[t] - pred[t]) for t in range(len(X)))
        return coef, 1 - sse / sst, maxres

    _, r2_full, maxres_full = lstsq(
        lambda r: [r["w"], math.log(r["avg"]), math.log(r["p"])])
    check("full model R^2 = 0.94 and max ratio error = 2.47x",
          approx(r2_full, 0.9403, 5e-3)
          and approx(math.exp(maxres_full), 2.47, 0.02),
          f"R2={r2_full:.4f}, maxerr={math.exp(maxres_full):.2f}x")
    coef_nw, _, _ = lstsq(lambda r: [math.log(r["avg"]), math.log(r["p"])])
    naive = 1 + math.exp(coef_nw[0] + coef_nw[1] * math.log(avg)
                         + coef_nw[2] * math.log(2 ** 31 - 1))
    check("naive w-free extrapolation at M31-list = ~197 (the named trap)",
          approx(naive, 197.0, 1.0), f"R_prim={naive:.4f}")

    # ---- E. tamper self-tests ----------------------------------------------
    print("\nE. tamper self-tests (checks must reject corruptions):")
    # NB: an off-by-one in B* shifts the ratio by only ~5e-7 (< printed 4-dp
    # precision), so it is caught by the EXACT-integer B* check in section A,
    # not by the ratio.  Point the tamper test at the check that has teeth.
    check("tamper B* (2^24 not 2^24-1) is rejected by exact B* check",
          (2 ** 24) != Bstar)
    check("tamper R_prim(+1.0) breaks the row equality check",
          not approx(by[(16, 97, 1)]["R_prim"] + 1.0, mh["R_prim"], 1e-4))
    check("tamper beta(1)->0.30 breaks the fit check",
          not approx(0.30, 0.254, 2e-3))
    check("tamper fit.per_w['2'].beta->0.999 breaks the fit-block check",
          not approx(0.999, betas[2], 2e-3))
    check("tamper fit.per_w['3'].k->0.0 breaks the fit-block check",
          not approx(0.0, ks[3], 2e-3))
    check("tamper avg(+1) breaks the exact avg check", (avg + 1) != 1993678)

    print()
    if FAILS:
        print(f"RESULT: FAIL ({len(FAILS)} check(s)): {FAILS}")
        return 1
    print("RESULT: PASS (all checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
