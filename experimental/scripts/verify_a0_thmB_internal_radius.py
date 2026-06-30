#!/usr/bin/env python3
"""
Resolves the strict-vs-non-strict 1/n internal-radius question flagged for
Paper D v7 thm:B / prop:slacked (the BCHKS/ABF slacked fallback).

THE FLAG (a0-thmA-audit workflow): BCHKS Thm 1.9 states the internal bound
NON-STRICTLY, Delta([f,g],C^2) >= delta - 1/n.  v7's eca bad event (def:ca)
requires the STRICT Delta > delta_int with delta_int = 1-rho-1/n.  Worry: the
boundary case Delta = 1-rho-1/n would fail the strict event -> possible off-by-one.

THE RESOLUTION (convention tracking): the worry assumes BCHKS's delta = 1-rho.
It is not, once the degree convention is matched:
  * BCHKS RS[F_q,D,k_B]  = polynomials of degree <= k_B   (dim k_B+1; bchks.txt L3071, Def 1.8)
    with k_B = (1-delta)n, so BCHKS delta = (n - k_B)/n.
  * cs25  RS[F,D,k]      = polynomials of degree <  k      (dim k;   cs25_cap_v7.tex L83)
To make the SAME code C, set k_B = k-1.  Then BCHKS delta = 1-(k-1)/n = 1-rho+1/n,
and BCHKS's conclusion Delta([f,g],C^2) >= delta - 1/n becomes
            Delta([f,g],C^2) >= 1 - rho        (NOT 1-rho-1/n).
Equivalently, BCHKS's own far-argument (bchks.txt L3116-3124): g=-1/(x-alpha)
agrees with a degree-<k poly P only where P(X)(X-alpha)+1 = 0; that polynomial has
degree <= (k-1)+1 = k, hence <= k roots, so g agrees with any C-codeword on <= k
points => Delta(g,C) >= 1 - k/n = 1 - rho.  (This is literally thm:A's S2 lemma.)

CONCLUSION: Delta([f,g],C^2) >= Delta(g,C) >= 1-rho > 1-rho-1/n.  The strict eca
event Delta > 1-rho-1/n holds with a full 1/n margin; v7 thm:B's internal radius
1-rho-1/n is CORRECT and in fact CONSERVATIVE.  No off-by-one.

This script constructs the BCHKS witness g over small fields, brute-forces its best
agreement with every degree-<k codeword, and certifies maxagree(g) <= k, i.e.
Delta(g,C) >= 1-rho, strictly above the 1-rho-1/n threshold.  Pure stdlib.
"""

from fractions import Fraction
from itertools import product


def best_agreement_with_C(vals, D, q, k):
    """max over P of degree < k of |{x in D : P(x) == vals[x]}|, brute force."""
    best = 0
    best_poly = None
    for coeffs in product(range(q), repeat=k):          # P = sum coeffs[i] X^i, deg < k
        agree = 0
        for x in D:
            px = 0
            for c in reversed(coeffs):
                px = (px * x + c) % q
            if px == vals[x]:
                agree += 1
        if agree > best:
            best, best_poly = agree, coeffs
    return best, best_poly


def run_case(q, D, k, alpha):
    """Build BCHKS g(x) = -1/(x-alpha) on D and certify Delta(g,C) >= 1-rho."""
    n = len(D)
    rho = Fraction(k, n)
    inv = {a: pow(a, q - 2, q) for a in range(1, q)}     # F_q inverses (q prime)
    g = {x: (-inv[(x - alpha) % q]) % q for x in D}       # -1/(x-alpha)
    maxagree, wit = best_agreement_with_C(g, D, q, k)
    dist_gC = Fraction(n - maxagree, n)                   # Delta(g,C) = 1 - maxagree/n
    # bounds
    far_paper = 1 - rho - Fraction(1, n)                  # v7 thm:B internal radius (strict threshold)
    far_bchks = 1 - rho                                   # BCHKS far bound, correct convention
    return dict(q=q, n=n, k=k, rho=rho, alpha=alpha, maxagree=maxagree,
                dist_gC=dist_gC, far_paper=far_paper, far_bchks=far_bchks,
                le_k=(maxagree <= k),
                ge_bchks=(dist_gC >= far_bchks),
                strict_ok=(dist_gC > far_paper))


def main():
    # small prime fields; D = a multiplicative coset (here F_q^* or a subgroup)
    cases = []
    # q=7, D=F_7^* (n=6), k=2,3 ; alpha=0 (in Omega=F\D)
    for k in (2, 3):
        cases.append((7, list(range(1, 7)), k, 0))
    # q=11, D = subgroup of order 5 {1,3,9,5,4}, k=2 ; alpha=0
    sub5 = [pow(3, i, 11) for i in range(5)]              # <3> has order 5 in F_11^*
    cases.append((11, sorted(set(sub5)), 2, 0))
    # q=13, D=F_13^* (n=12), k=3 ; alpha=0
    cases.append((13, list(range(1, 13)), 3, 0))

    print("=" * 96)
    print("Paper D v7 thm:B internal-radius certificate  (BCHKS witness g = -1/(x-alpha))")
    print("convention: cs25 RS[F,D,k] = deg<k ;  certify maxagree(g) <= k  =>  Delta(g,C) >= 1-rho")
    print("=" * 96)
    hdr = ("q", "n", "k", "rho", "maxagree", "<=k?", "Delta(g,C)", ">=1-rho?", ">1-rho-1/n?")
    print("%-4s %-4s %-3s %-6s %-9s %-5s %-12s %-9s %-12s" % hdr)
    print("-" * 96)
    all_ok = True
    for (q, D, k, alpha) in cases:
        r = run_case(q, D, k, alpha)
        ok = r["le_k"] and r["ge_bchks"] and r["strict_ok"]
        all_ok = all_ok and ok
        print("%-4d %-4d %-3d %-6s %-9d %-5s %-12s %-9s %-12s" % (
            r["q"], r["n"], r["k"], "%d/%d" % (r["rho"].numerator, r["rho"].denominator),
            r["maxagree"], "Y" if r["le_k"] else "N",
            "%d/%d" % (r["dist_gC"].numerator, r["dist_gC"].denominator),
            "Y" if r["ge_bchks"] else "N",
            "Y" if r["strict_ok"] else "N"))
    print("-" * 96)
    print("Interpretation: maxagree(g) <= k in every case (often = k, so Delta(g,C) = 1-rho EXACTLY,")
    print("confirming BCHKS's bound is genuinely non-strict at 1-rho) -- yet 1-rho > 1-rho-1/n always,")
    print("so the strict eca event Delta > 1-rho-1/n holds with a full 1/n margin.")
    print()
    print("ALL CHECKS PASS:", all_ok)
    print("=> v7 thm:B internal radius 1-rho-1/n is CORRECT and conservative; the flagged")
    print("   strict/non-strict 1/n off-by-one is a NON-ISSUE (artifact of BCHKS deg<=k vs cs25 deg<k).")


if __name__ == "__main__":
    main()
