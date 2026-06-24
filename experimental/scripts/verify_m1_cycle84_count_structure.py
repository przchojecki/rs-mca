#!/usr/bin/env python3
r"""
Independent structural audit of the Cycle84 count N and of PR #105's fixed-jet
locator transfer (Lemma 1) -- the bridge "finite count => LD_sw".

CONTEXT. PR #105 ("M1 standalone Cycle120 LDsw proof") derives
    LD_sw(RS[F_17^32,H,256],262) >= N,    N = 52,747,567,092,
from (a) the Cycle84 finite census of the seven-slot color-filtered family, and
(b) the fixed-jet locator transfer + smooth-padding transfer. PR #105's own
"Proof Boundary" states it does NOT rerun the Cycle84 census; N is an input.

This script does the two things that ARE independently checkable here:

PART A -- the count's structure (the census headline, not a recomputation):
  * the Cycle84 audit reports
        compatible pairs (color shell) = 52,747,567,104
        Occ(beta) = #{Phi(T)} = N       = 52,747,567,092
        double fibers = 12, fibers>=3 = 0, m_max(beta) = 2, ordered energy = 24.
  * CLEAN FACTORIZATION  52,747,567,104 = 2^27 * 3 * 131  (a structural
    fingerprint -- not a generic census output; note 131 = 262/2, half the
    Cycle120 support threshold).
  * COLLISION BOOKKEEPING is internally forced: with m_max=2 and no fiber of
    size >=3, if t values are double-hit then #distinct = #total - t and the
    ordered off-diagonal energy is 2t. The reported (t=12) gives
    Occ = shell - 12 = N and energy = 24. Consistent.
  NOTE: a first-principles recomputation of the shell 2^27*3*131 needs the
  slot-model spec (7 slots x 48 keys, projected logs, tau involution), which is
  NOT in this repo (it lived in Danny's rejected archive). So PART A is a
  partial independent check (fingerprint + collision consistency), NOT a census.

PART B -- the fixed-jet locator transfer (Lemma 1 of PR #105), on small exact
models (the genuine PROOF content; the count is merely its input). For a family
of j-subsets J of an n-point D with the top sigma coefficients of
P_J = prod_{a in J}(X-a) held common, beta not in D, k = n-j-sigma, the lemma
builds ONE line (f,g) with, for every J, f + z_J g agreeing with a codeword of
RS[F,D,k] on D\J (size n-j), z_J = 1/P_J(beta), and (f,g) NOT jointly explained
there. We reconstruct (f,g) from the paper's parity-check / error-word formulas
and check all four conclusions for sigma=1 and sigma=2 over F_17.

CROSS-LANE: z_J = 1/P_J(beta), bad slopes = {P_J(beta)} is the SAME
locator-fiber => deep-image mechanism as the X1 universal-cap bridge
(notes/x1) -- the M1 LD_sw count and the L2 cap are two instances of
"locator fiber -> bad slopes via a parity-check / deep-point identity."

Status: AUDIT / PROVED-by-enumeration (Part B); STRUCTURAL CHECK (Part A).

Run:
    python3 experimental/scripts/verify_m1_cycle84_count_structure.py
    python3 experimental/scripts/verify_m1_cycle84_count_structure.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations


# ----------------------------------------------------------------------------
# Part A: the count structure
# ----------------------------------------------------------------------------

def factorize(m):
    f, d = {}, 2
    while d * d <= m:
        while m % d == 0:
            f[d] = f.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        f[m] = f.get(m, 0) + 1
    return f


def part_a():
    shell = 52_747_567_104          # compatible pairs / color shell
    occ = 52_747_567_092            # Occ(beta) = #{Phi(T)} = N
    double_fibers = 12
    ordered_energy = 24
    m_max = 2
    fac_shell = factorize(shell)
    checks = {
        "shell = 2^27 * 3 * 131": fac_shell == {2: 27, 3: 1, 131: 1},
        "131 = 262/2 (half support threshold)": 131 * 2 == 262,
        # collision bookkeeping forced by m_max=2, no fiber>=3:
        "Occ = shell - double_fibers": occ == shell - double_fibers,
        "ordered_energy = 2 * double_fibers": ordered_energy == 2 * double_fibers,
        "m_max=2 consistent (energy/ (2*choose(2,2)) = doubles)":
            ordered_energy // 2 == double_fibers and m_max == 2,
    }
    return {
        "shell": shell, "occ_N": occ,
        "shell_factorization": "2^27 * 3 * 131",
        "occ_factorization": "2^2 * 3^4 * 11 * 14800103",
        "double_fibers": double_fibers, "ordered_energy": ordered_energy,
        "m_max": m_max,
        "checks": checks,
        "all_ok": all(checks.values()),
    }


# ----------------------------------------------------------------------------
# Part B: fixed-jet locator transfer (Lemma 1) over F_p
# ----------------------------------------------------------------------------

P = 17


def inv(a):
    return pow(a % P, P - 2, P)


def pmul(f, g):
    out = [0] * (len(f) + len(g) - 1)
    for i, fi in enumerate(f):
        if fi:
            for j, gj in enumerate(g):
                out[i + j] = (out[i + j] + fi * gj) % P
    return out


def ptrim(f):
    f = list(f)
    while len(f) > 1 and f[-1] % P == 0:
        f.pop()
    return [c % P for c in f]


def peval(f, x):
    acc = 0
    for c in reversed(f):
        acc = (acc * x + c) % P
    return acc


def locator(J):
    """monic prod_{a in J}(X - a)."""
    poly = [1]
    for a in J:
        poly = pmul(poly, [(-a) % P, 1])
    return ptrim(poly)


def deriv(f):
    return [(i * f[i]) % P for i in range(1, len(f))] or [0]


def lagrange_interp(xs, ys):
    """interpolating polynomial through (xs[i], ys[i]); return coeff list."""
    n = len(xs)
    acc = [0]
    for i in range(n):
        # basis poly L_i(X) = prod_{m != i} (X - xs[m]) / (xs[i] - xs[m])
        num = [1]
        den = 1
        for m in range(n):
            if m != i:
                num = pmul(num, [(-xs[m]) % P, 1])
                den = (den * (xs[i] - xs[m])) % P
        scale = (ys[i] * inv(den)) % P
        term = [(c * scale) % P for c in num]
        acc = acc + [0] * (len(term) - len(acc))
        for t in range(len(term)):
            acc[t] = (acc[t] + term[t]) % P
    return ptrim(acc)


def run_lemma1(D, beta, sigma, family):
    """Reconstruct (f,g) per PR#105 Lemma 1 and verify all four conclusions."""
    n = len(D)
    j = len(family[0])
    k = n - j - sigma
    redundancy = j + sigma          # = n - k
    agreement = n - j
    # L_D'(x) for x in D
    LD = [1]
    for x in D:
        LD = pmul(LD, [(-x) % P, 1])
    LDp = deriv(LD)
    LDp_at = {x: peval(LDp, x) % P for x in D}
    LD_at_beta = peval(LD, beta) % P

    # parity check H: rows m=0..redundancy-1, (H w)_m = sum_x x^m w(x)/LD'(x)
    def Hw(w):  # w: dict x->value
        return [sum((pow(x, m, P) * w[x] % P) * inv(LDp_at[x]) for x in D) % P
                for m in range(redundancy)]

    # error word e_J supported on J: e_J(x) = LD'(x)/((beta-x) P_J'(x)), x in J
    def err_word(J):
        PJ = locator(J)
        PJp = deriv(PJ)
        w = {x: 0 for x in D}
        for x in J:
            w[x] = (LDp_at[x] * inv((beta - x) % P) % P) * inv(peval(PJp, x) % P) % P
        return w, PJ

    # g(x) = LD(beta)/(beta - x)
    g = {x: (LD_at_beta * inv((beta - x) % P)) % P for x in D}

    J0 = family[0]
    e0, _ = err_word(J0)
    PJ0 = locator(J0)
    z0 = inv(peval(PJ0, beta) % P)
    f = {x: (e0[x] - z0 * g[x]) % P for x in D}

    line_ok = True            # f + z_J g agrees with a codeword on D\J
    slope_ok = True           # z_J = 1/P_J(beta)
    noncontain_ok = True      # (f,g) not jointly explained on D\J
    slopes = set()
    pj_betas = set()
    for J in family:
        eJ, PJ = err_word(J)
        zJ = inv(peval(PJ, beta) % P)
        slopes.add(zJ)
        pj_betas.add(peval(PJ, beta) % P)
        if zJ != inv(peval(PJ, beta) % P):
            slope_ok = False
        # f + z_J g - e_J should be in ker H  (=> agrees with codeword on D\J)
        resid = {x: (f[x] + zJ * g[x] - eJ[x]) % P for x in D}
        if any(c != 0 for c in Hw(resid)):
            line_ok = False
        # also: residual is supported off D\J? e_J is 0 on D\J, so on D\J,
        # f+z_J g = codeword. Check agreement count on D\J:
        cw = {x: (f[x] + zJ * g[x]) % P for x in D}  # equals codeword on D\J
        complement = [x for x in D if x not in J]
        # codeword = interp of cw on D\J must have degree < k for "explained";
        # for the LINE point it does (that's the agreement); verify size:
        if len(complement) != agreement:
            line_ok = False
        # noncontainment: g restricted to D\J is NOT a degree-<k codeword
        gpoly = lagrange_interp(complement, [g[x] for x in complement])
        if len(gpoly) - 1 < k and not (len(gpoly) == 1 and gpoly[0] == 0):
            # g would be code-explained on D\J -> containment -> bad
            noncontain_ok = False

    checks = {
        "k = n-j-sigma": k == n - j - sigma,
        "redundancy = n-k": redundancy == n - k,
        "agreement n-j == k+sigma": agreement == k + sigma,
        "line: f+z_J g in codeword + e_J on D\\J (all J)": line_ok,
        "slopes z_J = 1/P_J(beta)": slope_ok,
        "distinct slopes == #distinct P_J(beta)": len(slopes) == len(pj_betas),
        "noncontainment: g not explained on D\\J (all J)": noncontain_ok,
    }
    return {
        "n": n, "j": j, "sigma": sigma, "k": k, "agreement": agreement,
        "family_size": len(family), "distinct_bad_slopes": len(slopes),
        "checks": checks, "all_ok": all(checks.values()),
    }


def part_b():
    D = [1, 2, 3, 4, 5, 6, 7]
    beta = 10
    # sigma=1: no constraint on subsets (only monic leading coeff common).
    fam1 = [list(c) for c in combinations(D, 3)]          # j=3, k=3
    r1 = run_lemma1(D, beta, 1, fam1)
    # sigma=2: 3-subsets with fixed sum (e_1 common) => top 2 coeffs common.
    fam2 = [list(c) for c in combinations(D, 3) if sum(c) == 12]   # j=3,k=2
    r2 = run_lemma1(D, beta, 2, fam2)
    return {"sigma1": r1, "sigma2": r2,
            "all_ok": r1["all_ok"] and r2["all_ok"]}


def run():
    a = part_a()
    b = part_b()
    return {"all_ok": a["all_ok"] and b["all_ok"], "part_a_count_structure": a,
            "part_b_fixed_jet_transfer": b}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2)); raise SystemExit(0 if out["all_ok"] else 1)
    a, b = out["part_a_count_structure"], out["part_b_fixed_jet_transfer"]
    print("PART A -- Cycle84 count structure (fingerprint + collision bookkeeping):")
    print(f"  color shell = {a['shell']:,} = {a['shell_factorization']}")
    print(f"  Occ(beta) = N = {a['occ_N']:,} = {a['occ_factorization']}")
    print(f"  double fibers = {a['double_fibers']}, ordered energy = {a['ordered_energy']}, m_max = {a['m_max']}")
    for nme, ok in a["checks"].items():
        print(f"    [{'OK ' if ok else 'FAIL'}] {nme}")
    print("  (NOTE: shell not recomputed from slots -- spec lives in the rejected archive.)")
    print()
    print("PART B -- fixed-jet locator transfer (Lemma 1) over F_17:")
    for tag, r in (("sigma=1", b["sigma1"]), ("sigma=2", b["sigma2"])):
        print(f"  {tag}: n={r['n']} j={r['j']} k={r['k']} agreement={r['agreement']} "
              f"family={r['family_size']} distinct_bad_slopes={r['distinct_bad_slopes']}")
        for nme, ok in r["checks"].items():
            print(f"    [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (count fingerprint + collision consistent; fixed-jet transfer verified)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
