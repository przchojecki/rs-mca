#!/usr/bin/env python3
"""Independent verifier for the M31 depth-32 selector-spectrum generator.

Standard library only; runs in well under a minute.  It recomputes, from the
generating-function definition alone, the central binomial law E(t), the four
atlas-sourced coefficient laws X_sigma(t), their pointwise maximum, and checks
these against the hardcoded selector spectrum, the cross-pattern envelope, the
four exceptional odd-shell values, the single-/few-term reductions at those
points, and the irredundancy (deletion-loss) values.

X_sigma is computed two independent ways and cross-checked:

  A) full bivariate polynomial expansion of (q+z)^a (q^2+z)^b (1+z)^c, then
     extraction of the coefficient of z^d q^(t-f);
  B) the closed triple-sum implemented by the Lean `crossSignatureCount`.

Modes:
  --check           run every check against the shipped constants; exit 0 iff
                    all pass.
  --tamper-selftest apply a battery of single-value mutations and confirm each
                    is caught (some check fails); exit 0 iff every mutation is
                    caught.  Guards against a vacuous verifier.

With no argument, --check is assumed.
"""

import sys
from math import comb
from copy import deepcopy

# --------------------------------------------------------------------------
# Shipped constants (the object under verification).
# --------------------------------------------------------------------------

# Signature order: (a, b, c, f, d) = (anchorOne, anchorBoth, zeroZero,
# fixedRemoved, partnerDoubled).
SIGNATURES = {
    "sigma7":  (5, 0, 6, 4, 3),
    "sigma9":  (8, 0, 3, 5, 5),
    "sigma11": (5, 3, 3, 3, 5),
    "sigma13": (3, 2, 3, 7, 4),
}

# selectorRootedMaximum(t), t = 1..14  (the printed selector spectrum).
CLAIMED_SPECTRUM = [0, 49, 0, 441, 0, 1225, 60, 1225, 210, 441, 45, 49, 3, 1]

# centralPatternCount(t) row, t = 1..14.
CLAIMED_CENTRAL = [0, 49, 0, 441, 0, 1225, 0, 1225, 0, 441, 0, 49, 0, 1]

# max_i X_i(t) cross-pattern envelope, t = 1..14.
CLAIMED_ENVELOPE = [0, 0, 0, 0, 0, 10, 60, 108, 210, 168, 45, 11, 3, 0]

# Exceptional odd-shell values: signature name -> (t, value).
CLAIMED_EXCEPTIONAL = {
    "sigma7":  (7, 60),
    "sigma9":  (9, 210),
    "sigma11": (11, 45),
    "sigma13": (13, 3),
}

# Number of contributing binomial terms and their multiset at each exceptional
# point (single-/few-term reductions, paper Section 3).
CLAIMED_TERMS = {
    "sigma7":  (7, [60]),
    "sigma9":  (9, [210]),
    "sigma11": (11, [15, 30]),
    "sigma13": (13, [3]),
}

# Irredundancy: removing the signature responsible for t lowers K(t) to this.
CLAIMED_DELETION_LOSS = {7: 45, 9: 136, 11: 28, 13: 0}


# --------------------------------------------------------------------------
# Independent recomputation.
# --------------------------------------------------------------------------

def E(t):
    """Central binomial law C(7, t/2)^2 on even t, else 0."""
    if t % 2 == 1:
        return 0
    return comb(7, t // 2) ** 2


def _poly_mul(p, q):
    r = {}
    for (i, j), c in p.items():
        for (k, l), d in q.items():
            key = (i + k, j + l)
            r[key] = r.get(key, 0) + c * d
    return r


def _poly_pow(base, n):
    r = {(0, 0): 1}
    for _ in range(n):
        r = _poly_mul(r, base)
    return r


def X_polyexpand(sig, t):
    """[z^d q^(t-f)] (q+z)^a (q^2+z)^b (1+z)^c by full expansion."""
    a, b, c, f, d = sig
    P = _poly_pow({(1, 0): 1, (0, 1): 1}, a)      # (q + z)^a
    P = _poly_mul(P, _poly_pow({(2, 0): 1, (0, 1): 1}, b))  # (q^2 + z)^b
    P = _poly_mul(P, _poly_pow({(0, 0): 1, (0, 1): 1}, c))  # (1 + z)^c
    tq = t - f
    if tq < 0:
        return 0
    return P.get((tq, d), 0)


def X_sum(sig, t):
    """Closed triple-sum, mirroring the Lean crossSignatureCount."""
    a, b, c, f, d = sig
    total = 0
    for x in range(a + 1):
        for y in range(b + 1):
            if x + y <= d:
                z = d - x - y
                if z <= c and f + (a - x) + 2 * (b - y) == t:
                    total += comb(a, x) * comb(b, y) * comb(c, z)
    return total


def X_terms(sig, t):
    """Contributing binomial terms at (sig, t)."""
    a, b, c, f, d = sig
    terms = []
    for x in range(a + 1):
        for y in range(b + 1):
            if x + y <= d:
                z = d - x - y
                if z <= c and f + (a - x) + 2 * (b - y) == t:
                    terms.append(comb(a, x) * comb(b, y) * comb(c, z))
    return terms


# --------------------------------------------------------------------------
# Check battery.  Returns a list of (name, ok) pairs; never raises on a
# mathematical mismatch, so it can be reused for the tamper self-test.
# --------------------------------------------------------------------------

def run_checks(C):
    results = []

    def add(name, ok):
        results.append((name, bool(ok)))

    sigs = C["signatures"]

    # Method A vs Method B agreement on every signature and t = 1..14.
    methods_agree = all(
        X_polyexpand(sigs[n], t) == X_sum(sigs[n], t)
        for n in sigs for t in range(1, 15)
    )
    add("methodA_equals_methodB", methods_agree)

    # Recomputed tables (Method B, which equals A when the above holds).
    Xtab = {n: [X_sum(sigs[n], t) for t in range(1, 15)] for n in sigs}
    Etab = [E(t) for t in range(1, 15)]
    maxXtab = [max(Xtab[n][i] for n in sigs) for i in range(14)]
    Ktab = [max(Etab[i], maxXtab[i]) for i in range(14)]

    add("central_row_matches", Etab == C["central"])
    add("envelope_row_matches", maxXtab == C["envelope"])
    add("spectrum_max_equality", Ktab == C["spectrum"])

    # Exceptional values.
    for n, (t, val) in C["exceptional"].items():
        add(f"exceptional_{n}", X_sum(sigs[n], t) == val)

    # Single-/few-term reductions.
    for n, (t, expected_terms) in C["terms"].items():
        add(f"terms_{n}", sorted(X_terms(sigs[n], t)) == sorted(expected_terms))

    # Irredundancy / deletion losses: remove the signature named for t.
    for t, expected in C["deletion_loss"].items():
        resp = f"sigma{t}"
        remaining = [n for n in sigs if n != resp]
        got = max([E(t)] + [X_sum(sigs[n], t) for n in remaining])
        add(f"deletion_loss_t{t}", got == expected)

    # Point-deficiency form: kappa_hat_32(e), e = 34..479.
    def khat(e):
        t = e // 32
        if e % 32 == 0 and 1 <= t <= 14:
            return Ktab[t - 1]
        return 0

    add("offlattice_zero",
        all(khat(e) == 0 for e in range(34, 480) if e % 32 != 0))
    add("point_exceptional",
        (khat(224), khat(288), khat(352), khat(416)) == (60, 210, 45, 3))
    add("point_explicit_zeros", khat(96) == 0 and khat(160) == 0)

    return results


def base_claims():
    return {
        "signatures": deepcopy(SIGNATURES),
        "spectrum": list(CLAIMED_SPECTRUM),
        "central": list(CLAIMED_CENTRAL),
        "envelope": list(CLAIMED_ENVELOPE),
        "exceptional": deepcopy(CLAIMED_EXCEPTIONAL),
        "terms": deepcopy(CLAIMED_TERMS),
        "deletion_loss": dict(CLAIMED_DELETION_LOSS),
    }


def do_check(verbose=True):
    results = run_checks(base_claims())
    failed = [n for n, ok in results if not ok]
    if verbose:
        for n, ok in results:
            print(f"  [{'ok' if ok else 'FAIL'}] {n}")
    if failed:
        print(f"CHECK FAILED: {len(failed)} check(s) failed: {failed}")
        return 1
    print(f"CHECK PASSED: all {len(results)} checks pass "
          f"(two independent methods agree; all shipped values reproduced).")
    return 0


def do_tamper_selftest(verbose=True):
    """Each mutation must be caught by at least one failing check."""
    mutations = []

    def mut(name, fn):
        mutations.append((name, fn))

    def spectrum_bump(C): C["spectrum"][6] = 61            # 60 -> 61
    def central_bump(C):  C["central"][1] = 48            # 49 -> 48
    def envelope_bump(C): C["envelope"][8] = 209          # 210 -> 209
    def exc_bump(C):      C["exceptional"]["sigma9"] = (9, 211)
    def terms_bump(C):    C["terms"]["sigma11"] = (11, [45])   # split -> single
    def terms_count(C):   C["terms"]["sigma13"] = (13, [3, 3])  # 1 -> 2 terms
    def delloss_bump(C):  C["deletion_loss"][9] = 135     # 136 -> 135
    def sig_perturb(C):   C["signatures"]["sigma7"] = (5, 0, 6, 4, 2)  # d 3->2
    def sig_perturb2(C):  C["signatures"]["sigma9"] = (8, 0, 3, 4, 5)  # f 5->4

    mut("spectrum[t7]=61", spectrum_bump)
    mut("central[t2]=48", central_bump)
    mut("envelope[t9]=209", envelope_bump)
    mut("exceptional_sigma9=211", exc_bump)
    mut("terms_sigma11=[45]", terms_bump)
    mut("terms_sigma13_count", terms_count)
    mut("deletion_loss_t9=135", delloss_bump)
    mut("signature_sigma7_d", sig_perturb)
    mut("signature_sigma9_f", sig_perturb2)

    all_caught = True
    for name, fn in mutations:
        C = base_claims()
        fn(C)
        results = run_checks(C)
        caught = any(not ok for _, ok in results)
        if verbose:
            print(f"  [{'caught' if caught else 'MISSED'}] mutation {name}")
        if not caught:
            all_caught = False

    # Sanity: the untampered battery must fully pass.
    clean = run_checks(base_claims())
    clean_ok = all(ok for _, ok in clean)
    if verbose:
        print(f"  [{'ok' if clean_ok else 'FAIL'}] untampered battery passes")
    if not clean_ok:
        all_caught = False

    if all_caught:
        print(f"TAMPER SELF-TEST PASSED: all {len(mutations)} mutations caught, "
              f"clean battery passes.")
        return 0
    print("TAMPER SELF-TEST FAILED: a mutation went undetected.")
    return 1


def main(argv):
    mode = argv[1] if len(argv) > 1 else "--check"
    if mode in ("--check", "check"):
        return do_check()
    if mode in ("--tamper-selftest", "tamper-selftest"):
        return do_tamper_selftest()
    print(__doc__)
    print(f"unknown mode: {mode!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
