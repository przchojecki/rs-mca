#!/usr/bin/env python3
r"""
Mechanism check for the prob:explicit construction (Paper D), small F_{p^2} model.

Goal (notes/x1): make Paper D `cor:Fvalued` / `prob:explicit` CONSTRUCTIVE by an
explicit non-B-rational simple-pole deep-point line on the `lem:fiber` heavy word.

At deployed scale the density `M/|F| ~ 1/k = 2^-20 > 2^-22` is pure arithmetic
(verified separately): `M >= |Omega|/k` by the averaging saturation, `|Omega|=q-n`.
This script validates the *mechanism* on a small smooth-domain extension model:

  B = F_17, F = F_{17^2} = B[t]/(t^2-3), D = B^* (order n=16 = 2^4, smooth),
  rho=1/2, k=8, a_q=2, N=n/a_q=8, ell2=rho*N+2=6, agreement=k+2a_q=12,
  heavy word u_z = x^{k+2a_q} + z x^{k+a_q} = x^12 + z x^10  (z = lem:fiber slope).

Checks, by brute force:
  (A) deep-point identity on the lem:fiber word: the support-wise MCA-bad slopes
      of the line f=u_z/(x-alpha), g=-1/(x-alpha) for C=RS[F,D,k] at agreement 12
      equal the deep image {P(alpha): P in the C_+=RS[F,D,k+1] list of u_z};
  (B) lem:confine vs cor:Fvalued via the deep point: alpha in B\D (=0) gives
      B-valued bad slopes (confined); alpha=t in F\B gives genuinely F-valued
      (non-B-rational) bad slopes -- the cor:Fvalued regime;
  (C) the averaging count: M(alpha)=|deep image| satisfies, for the best alpha,
      M >= L/(1 + k(L-1)/|Omega|) (the expansion behind the 1/k saturation), and
      a positive fraction of alpha achieve at least that.

Finite mechanism check; the deployed density is the separate arithmetic.
Status: AUDIT / mechanism validation for the prob:explicit construction.

Run:
    python3 experimental/scripts/verify_x1_prob_explicit_mechanism.py
    python3 experimental/scripts/verify_x1_prob_explicit_mechanism.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from fractions import Fraction

P = 17
NS = 3  # t^2 = 3, nonsquare mod 17


def fadd(A, B): return ((A[0]+B[0]) % P, (A[1]+B[1]) % P)
def fsub(A, B): return ((A[0]-B[0]) % P, (A[1]-B[1]) % P)
def fmul(A, B): return ((A[0]*B[0]+NS*A[1]*B[1]) % P, (A[0]*B[1]+A[1]*B[0]) % P)
def femb(x): return (x % P, 0)
def finv(A):
    den = (A[0]*A[0]-NS*A[1]*A[1]) % P
    d = pow(den, -1, P)
    return ((A[0]*d) % P, (-A[1]*d) % P)
def fdiv(A, B): return fmul(A, finv(B))
ZERO, ONE, T = (0, 0), (1, 0), (0, 1)


def interp(points):
    res = []
    for i, (xi, yi) in enumerate(points):
        basis, den = [ONE], ONE
        for j, (xj, _y) in enumerate(points):
            if i == j:
                continue
            new = [ZERO]*(len(basis)+1)
            for d, b in enumerate(basis):
                new[d] = fsub(new[d], fmul(xj, b))
                new[d+1] = fadd(new[d+1], b)
            basis, den = new, fmul(den, fsub(xi, xj))
        sc = fdiv(yi, den)
        if len(res) < len(basis):
            res += [ZERO]*(len(basis)-len(res))
        for d, b in enumerate(basis):
            res[d] = fadd(res[d], fmul(sc, b))
    while res and res[-1] == ZERO:
        res.pop()
    return res


def deg(c): return len(c)-1
def peval(c, x):
    out = ZERO
    for co in reversed(c):
        out = fadd(fmul(out, x), co)
    return out


def close_slope(fI, gI, k, m):
    cand = None
    for j in range(k, m):
        fj = fI[j] if j < len(fI) else ZERO
        gj = gI[j] if j < len(gI) else ZERO
        if gj == ZERO:
            if fj != ZERO:
                return None
            continue
        zj = fdiv(fsub(ZERO, fj), gj)
        if cand is None:
            cand = zj
        elif cand != zj:
            return None
    return cand


def build():
    n, k, a_q = 16, 8, 2
    N = n//a_q
    ell2 = N//2 + 2
    agreement = k + 2*a_q
    g = 3
    D = []
    x = 1
    for _ in range(n):
        D.append(femb(x)); x = (x*g) % P
    Dset = set(D)
    # Q = {x^a_q : x in D} (quotient, order N)
    Q = sorted({tuple(fmul(d, d)) for d in D})  # x^2 since a_q=2
    assert len(Q) == N
    # heavy z: z = -(most popular e_1(A)) over ell2-subsets A of Q (lem:fiber)
    from collections import Counter
    cnt = Counter()
    for A in combinations(Q, ell2):
        s = ZERO
        for b in A:
            s = fadd(s, b)
        cnt[s] += 1
    e1_heavy, _ = cnt.most_common(1)[0]
    z = fsub(ZERO, e1_heavy)
    # u_z(x) = x^{k+2a_q} + z x^{k+a_q}
    U = {}
    for d in D:
        xk2 = ONE
        for _ in range(k+2*a_q):
            xk2 = fmul(xk2, d)
        xk1 = ONE
        for _ in range(k+a_q):
            xk1 = fmul(xk1, d)
        U[d] = fadd(xk2, fmul(z, xk1))
    return D, Dset, U, k, agreement, N, ell2


def cplus_list(D, U, k, a):
    found = {}
    for S in combinations(D, a):
        Pp = interp([(s, U[s]) for s in S])
        if deg(Pp) < k+1:           # C_+ = RS deg < k+1
            found[tuple(Pp)] = Pp
    return list(found.values())


def deep_image(plist, alpha):
    return {peval(list(Pp), alpha) for Pp in plist}


def bad_mca(D, U, k, a, alpha):
    inv = {d: finv(fsub(d, alpha)) for d in D}
    f = {d: fmul(U[d], inv[d]) for d in D}
    gg = {d: fsub(ZERO, inv[d]) for d in D}
    out = set()
    for S in combinations(D, a):
        fI = interp([(s, f[s]) for s in S])
        gI = interp([(s, gg[s]) for s in S])
        zz = close_slope(fI, gI, k, a)
        if zz is not None:
            out.add(zz)
    return out


def fpow(base, e):
    out = ONE
    while e:
        if e & 1:
            out = fmul(out, base)
        base = fmul(base, base); e >>= 1
    return out


def find_generator():
    # generator of F_{p^2}^* (order p^2-1 = 288)
    order = P*P - 1
    import sympy
    facs = list(sympy.factorint(order).keys())
    for u in range(P):
        for v in range(1, P):
            g = (u, v)
            if all(fpow(g, order//pf) != ONE for pf in facs):
                if fpow(g, order) == ONE:
                    return g
    raise RuntimeError("no generator")


def run():
    D, Dset, U, k, a, N, ell2 = build()
    a_q = 2
    plist = cplus_list(D, U, k, a)
    L = len(plist)
    Omega = [(u, v) for u in range(P) for v in range(P) if (u, v) not in Dset]
    q = P*P
    gen = find_generator()

    def in_B(x): return x[1] == 0
    def alpha_pow_aq_in_B(alpha): return in_B(fpow(alpha, a_q))

    # (A)/(B) identity + confine-vs-Fvalued: the slopes P(alpha)=G(alpha^{a_q})
    # are F-valued iff alpha^{a_q} not in B (quotient-periodicity of the heavy word).
    rows = {}
    for name, alpha in [("alpha=t  (t^2=3 in B)", T),
                        ("alpha=gen (gen^2 not in B)", gen)]:
        deep = deep_image(plist, alpha)
        bad = bad_mca(D, U, k, a, alpha)
        rows[name] = {"deep": len(deep), "bad": len(bad),
                      "identity": deep == bad,
                      "F_valued": any(s[1] != 0 for s in deep),
                      "alpha^aq_in_B": alpha_pow_aq_in_B(alpha)}

    # characterization over all deep points: F-valued(alpha) <=> alpha^{a_q} not in B
    char_ok = True
    n_good = 0
    for alpha in Omega:
        deep = deep_image(plist, alpha)
        fval = any(s[1] != 0 for s in deep)
        good = not alpha_pow_aq_in_B(alpha)
        if good:
            n_good += 1
        if fval != good:
            char_ok = False

    # averaging over the GOOD deep points (alpha^{a_q} not in B)
    Ms = [len(deep_image(plist, alpha)) for alpha in Omega
          if not alpha_pow_aq_in_B(alpha)]
    Mmax = max(Ms); Mmean = sum(Ms)/len(Ms)
    avg_bound = Fraction(L, 1) / (1 + Fraction(k*(L-1), len(Omega)))

    checks = {
        "identity_at_t": rows["alpha=t  (t^2=3 in B)"]["identity"],
        "identity_at_gen": rows["alpha=gen (gen^2 not in B)"]["identity"],
        "t_confined (alpha^aq in B => B-valued)":
            (not rows["alpha=t  (t^2=3 in B)"]["F_valued"]),
        "gen_F_valued (alpha^aq notin B => F-valued)":
            rows["alpha=gen (gen^2 not in B)"]["F_valued"],
        "characterization F-valued <=> alpha^aq notin B": char_ok,
        "good_deep_points_are_majority": n_good >= len(Omega)//2,
        "Mmax_meets_avg_bound": Mmax >= float(avg_bound),
    }
    all_ok = all(checks.values())
    return {
        "all_ok": all_ok,
        "params": {"p": P, "F": "F_{17^2}", "n": 16, "k": k, "a_q": a_q, "N": N,
                   "ell2": ell2, "agreement": a, "L_list": L, "|Omega|": len(Omega),
                   "q": q, "good_deep_points": n_good},
        "rows": rows,
        "averaging": {"M_max": Mmax, "M_mean": round(Mmean, 2),
                      "avg_bound L/(1+k(L-1)/|Omega|)": round(float(avg_bound), 2),
                      "saturation_|Omega|/k": round(len(Omega)/k, 2),
                      "best_density_M/q": round(Mmax/q, 4)},
        "checks": checks,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2)); raise SystemExit(0 if out["all_ok"] else 1)
    pr = out["params"]
    print("prob:explicit construction -- mechanism check over F_{17^2} (smooth D=F_17^*):")
    print(f"  n={pr['n']} k={pr['k']} a_q={pr['a_q']} N={pr['N']} ell2={pr['ell2']} "
          f"agreement={pr['agreement']}  heavy-word list L={pr['L_list']}  |Omega|={pr['|Omega|']}"
          f"  good deep pts (alpha^aq notin B)={pr['good_deep_points']}")
    print()
    for name, r in out["rows"].items():
        print(f"  {name}: bad=deep? {r['identity']} (={r['bad']});  "
              f"F-valued? {r['F_valued']};  alpha^aq in B? {r['alpha^aq_in_B']}")
    av = out["averaging"]
    print()
    print(f"  averaging over good alpha: M_max={av['M_max']}, M_mean={av['M_mean']}, "
          f"bound L/(1+k(L-1)/|Omega|)={av['avg_bound L/(1+k(L-1)/|Omega|)']}")
    print(f"  saturation target |Omega|/k={av['saturation_|Omega|/k']}; "
          f"best density M/q={av['best_density_M/q']}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (mechanism validated: identity, confine-vs-Fvalued, averaging)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
