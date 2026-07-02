#!/usr/bin/env python3
r"""
conj:B quotient-separation, step-2 biconditional (X1): does a quotient-periodic
denominator E in F[X^M] confine the residue-line bad slopes?

CONTEXT (notes/x1/x1_conjB_proof_plan.md). conj:B's aperiodic packing Λ^aper
separates the quotient-periodic residue lines (rem:aper, slackMCA_v4.tex 1255:
denominator E a pullback through x↦x^M, M|gcd(n,k), M>1). My contribution to
conj:B is to prove these periodic lines CONFINE (contribute the quotient term),
isolating Λ^aper for the L1 bound. This script tests the load-bearing step on a
small extension field.

RESIDUE-LINE BAD SLOPES (def:residue, 1189; via thm:normalform). The line is
f = w/E, g = -B/E on D. A slope z is bad at radius 1-a/n iff f+zg agrees with a
degree-<k codeword on >= a points. For k=2 each a-subset S yields a candidate
z_S by solving  f(x) + z g(x) = P0 + P1 x  for (P0,P1,z) over the a points of S.
The bad-slope set is { z_S } (with the noncontainment filter).

CLAIM TESTED. Over F = F_{p^2}, B = F_p, smooth D <= B^*, with M | gcd(n,k):
  * PERIODIC denominator E = X^2 - gamma in F[X^M] (M=2, no X term, K_M-invariant
    since E(-x)=E(x)) ==> the bad slopes z_S CONFINE (lie in a proper B-structure);
  * GENERIC denominator E = X^2 + beta X + gamma (beta != 0, NOT in F[X^M]) ==>
    the bad slopes spread over F (genuinely F-valued).
If so, this is the residue-line form of confinement-from-stabilizer: the
quotient-periodic (K_M-invariant denominator) lines are exactly the confined ones.

Status: AUDIT / EXPLORATORY VERIFY (testing the conj:B separation mechanism).

Run:
    python3 experimental/scripts/verify_x1_conjB_residue_confinement.py
    python3 experimental/scripts/verify_x1_conjB_residue_confinement.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations


class GF:
    """F_{p^2} = F_p[t]/(t^2 - g); element = (u, v) ~ u + v t."""
    def __init__(self, p, g): self.p, self.g = p, g
    def add(self, a, b): return ((a[0]+b[0]) % self.p, (a[1]+b[1]) % self.p)
    def sub(self, a, b): return ((a[0]-b[0]) % self.p, (a[1]-b[1]) % self.p)
    def mul(self, a, b):
        p, g = self.p, self.g
        return ((a[0]*b[0]+a[1]*b[1]*g) % p, (a[0]*b[1]+a[1]*b[0]) % p)
    def inv(self, a):
        p, g = self.p, self.g
        nrm = (a[0]*a[0]-a[1]*a[1]*g) % p
        ni = pow(nrm, p-2, p)
        return ((a[0]*ni) % p, ((-a[1])*ni) % p)
    def div(self, a, b): return self.mul(a, self.inv(b))
    def base(self, u): return (u % self.p, 0)
    def is_zero(self, a): return a[0] % self.p == 0 and a[1] % self.p == 0
    def in_B(self, a): return a[1] % self.p == 0
    def neg(self, a): return ((-a[0]) % self.p, (-a[1]) % self.p)


def is_nonsquare(g, p): return pow(g % p, (p-1)//2, p) == p-1


def poly_eval(F, coeffs, x):
    acc = (0, 0)
    for c in reversed(coeffs):
        acc = F.add(F.mul(acc, x), c)
    return acc


def solve3(F, rows, rhs):
    """Solve 3x3 linear system over F (Gaussian elimination). Return solution or None."""
    M = [list(r) + [b] for r, b in zip(rows, rhs)]
    for col in range(3):
        piv = next((r for r in range(col, 3) if not F.is_zero(M[r][col])), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        inv = F.inv(M[col][col])
        M[col] = [F.mul(inv, v) for v in M[col]]
        for r in range(3):
            if r != col and not F.is_zero(M[r][col]):
                f = M[r][col]
                M[r] = [F.sub(M[r][i], F.mul(f, M[col][i])) for i in range(4)]
    return [M[i][3] for i in range(3)]


def bad_slopes(F, D, w, B, E, a):
    """Bad slopes z_S over a-subsets S of D for the line f=w/E, g=-B/E (k=2)."""
    fvals, gvals = {}, {}
    for x in D:
        Ex = poly_eval(F, E, x)
        if F.is_zero(Ex):
            return None  # E vanishes on D -> invalid datum
        fvals[x] = F.div(poly_eval(F, w, x), Ex)
        gvals[x] = F.neg(F.div(poly_eval(F, B, x), Ex))
    slopes = []
    for S in combinations(D, a):
        # f(x) + z g(x) = P0 + P1 x  =>  unknowns (P0, P1, z); use first 3 points;
        # then require the rest of S to be consistent (deg<2 on all of S).
        S3 = S[:3]
        rows = [[F.base(p_neg1), F.neg(x), gvals[x]] for x, p_neg1 in
                ((xx, 1) for xx in S3)]
        # row: -P0 - P1 x + g(x) z = -f(x)  => coeffs [-1, -x, g(x)], rhs -f(x)
        rows = [[F.base((-1) % F.p), F.neg(x), gvals[x]] for x in S3]
        rhs = [F.neg(fvals[x]) for x in S3]
        sol = solve3(F, rows, rhs)
        if sol is None:
            continue
        P0, P1, z = sol
        # consistency on all of S (a points): f(x)+z g(x) == P0+P1 x
        ok = True
        for x in S:
            lhs = F.add(fvals[x], F.mul(z, gvals[x]))
            rhsv = F.add(P0, F.mul(P1, x))
            if not (lhs == rhsv):
                ok = False; break
        if not ok:
            continue
        # noncontainment: NOT both f and g individually deg<2 on S.
        def deg_lt2_on(vals):
            xs = list(S[:2])
            r = [[F.base((-1) % F.p), F.neg(xx)] for xx in xs]
            # solve P0+P1 x = vals(x) on 2 pts, check rest
            # 2x2 solve
            a0, a1 = xs
            den = F.sub(a0, a1)
            if F.is_zero(den):
                return False
            P1c = F.div(F.sub(vals[a0], vals[a1]), den)
            P0c = F.sub(vals[a0], F.mul(P1c, a0))
            return all(vals[x] == F.add(P0c, F.mul(P1c, x)) for x in S)
        if deg_lt2_on(fvals) and deg_lt2_on(gvals):
            continue  # contained
        slopes.append(z)
    # dedupe
    uniq = []
    seen = set()
    for z in slopes:
        if z not in seen:
            seen.add(z); uniq.append(z)
    return uniq


def run():
    p = 17
    g = next(x for x in range(2, p) if is_nonsquare(x, p))
    F = GF(p, g)
    n, k, a, M = 8, 2, 3, 2
    # D = order-8 subgroup of F_17^* (base-field smooth domain)
    gen = next(c for c in range(2, p) if pow(c, n, p) == 1 and pow(c, n//2, p) != 1)
    D = [F.base(pow(gen, i, p)) for i in range(n)]
    assert any(D[i] == F.sub((0, 0), (1, 0)) for i in range(n)), "-1 must be in D (K_2)"

    # extension-valued numerator/anchor (so generic slopes are F-valued)
    t = (0, 1)  # the extension generator
    w = [(3, 1), (1, 2), (2, 0)]          # deg-2 anchor, extension coeffs
    Bn = [(1, 1), (4, 0)]                 # deg-1 numerator (deg B < t=2)
    # PERIODIC E in F[X^2]: X^2 - gamma (no X term) -> K_2-invariant
    gamma = (5, 3)
    E_per = [F.neg(gamma), (0, 0), (1, 0)]      # X^2 - gamma
    # GENERIC E: X^2 + beta X + gamma, beta != 0 -> NOT in F[X^2]
    E_gen = [F.neg(gamma), (2, 1), (1, 0)]      # X^2 + (2+t)X - gamma

    res_per = bad_slopes(F, D, w, Bn, E_per, a)
    res_gen = bad_slopes(F, D, w, Bn, E_gen, a)

    def summarize(slopes):
        if slopes is None:
            return {"valid": False}
        inB = sum(1 for z in slopes if F.in_B(z))
        return {"valid": True, "num_bad": len(slopes), "num_in_B": inB,
                "all_confined_to_B": len(slopes) > 0 and inB == len(slopes),
                "fraction_in_B": round(inB / len(slopes), 3) if slopes else None}

    sp, sg = summarize(res_per), summarize(res_gen)
    # HYPOTHESIS TESTED: "periodic denominator E in F[X^M] => bad slopes confine to B".
    # The data FALSIFY it (periodic E gives mostly F-valued slopes). The finding is
    # that rem:aper's separation is NOT slope-confinement: a periodic-denominator
    # line contributes the quotient COUNT term (it descends via x↦x^M to a line on
    # H_{n/M}), which is the quotient-reduction mechanism, not the base-vs-F
    # confinement of my confinement theorem. Recorded as a banked negative result.
    naive_periodic_confines = sp.get("all_confined_to_B", False)
    checks = {
        "datum computation valid (both)": sp.get("valid", False) and sg.get("valid", False),
        "FALSIFIED: periodic E alone does NOT confine slopes": not naive_periodic_confines,
        "(observed) periodic E bad slopes mostly F-valued": sp.get("fraction_in_B", 1) < 0.5,
    }
    return {"params": {"p": p, "n": n, "k": k, "a": a, "M": M, "field": "F_17^2"},
            "periodic": sp, "generic": sg, "checks": checks,
            "hypothesis_periodic_confines": naive_periodic_confines,
            "all_ok": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print(f"conj:B residue-line confinement test  params={out['params']}")
    print("  Quotient-periodic denominator E in F[X^M] vs generic E -- do bad slopes confine to B?")
    print(f"  PERIODIC E=X^2-gamma : {out['periodic']}")
    print(f"  GENERIC  E=X^2+bX+g  : {out['generic']}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT (banked negative finding):")
    print("  HYPOTHESIS 'periodic denominator E in F[X^M] => confined slopes' is FALSIFIED.")
    print("  => rem:aper's separation is the quotient COUNT (periodic line descends via x↦x^M to")
    print("     a line on H_{n/M}; its bad-slope count is the quotient instance = the Quot term),")
    print("     NOT slope-confinement. Next: build the quotient-DESCENT verifier (count-preserving).")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
