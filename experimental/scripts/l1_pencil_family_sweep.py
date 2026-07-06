#!/usr/bin/env python3
"""l1_pencil_family_sweep.py

Under-plant-then-EXHAUSTIVELY-sweep-the-nullspace-family CONSTRUCTOR for the
`E_3 <= ell` law refutation of `experimental/notes/l1/l1_e3_law_refuted.md`
(verified by the companion `experimental/scripts/verify_l1_e3_law_refuted.py`).

Stdlib only. No imports from any other script in this repo (independent,
from-scratch reimplementation; the `F_p`/nullspace machinery necessarily
resembles the sibling scripts' because it is the same underlying
mathematics, but no code is shared or imported).

--------------------------------------------------------------------------
METHOD (see the note Sec 0 item 3, the AUDIT)
--------------------------------------------------------------------------
The refuted law's "0 violations" evidence came from constructors that plant
a FEW fibers and read off a SINGLE nullspace vector (`basis[0]`) as the
answer. That systematically misses the extremal members of the family: once
you under-plant a big-fiber pair (leaving `mu_1 + mu_2` one or two below the
pairwise-cap ceiling `ell`), the remaining nullspace is not a point but a
whole projective FAMILY (dimension `d = 2` for a `pairgap = 1` plant, a
"pencil"; `d = 3` for `pairgap = 2`), and the true extremal spectrum can sit
at any member of it, discovered only by reading every member's EMERGENT
spectrum (not the planted one -- solving typically grows/reshapes the
tail).  This script demonstrates that mechanism concretely and
reproducibly, in the two sizes the note's witnesses actually used:

  DEFAULT MODE (`d = 2`, a pencil, exhaustive, no seed):
    Re-derives the `ell = 17, p = 137` violation (witness "W3", the
    strongest of the six: `E_3 = ell + 2`). The plant is the ACTUAL size-14
    fiber of the known W3 `Gamma` (a fact about that realizable object, not
    a free parameter) paired with an "under-planted" 2-point SUBSET of its
    second fiber (which is size 3 in the achieved solution) -- i.e.
    `mu_1 + mu_2 = 14 + 2 = 16 = ell - 1`, one below the pairwise-cap
    ceiling. This is a DETERMINISTIC recipe (the two point-sets are fixed
    data, extracted once from the known witness; no RNG anywhere in this
    mode) whose resulting 2-dimensional nullspace is then swept COMPLETELY:
    all `p + 1 = 138` members of the pencil (`[1,t]` for `t = 0..p-1`, plus
    the point at infinity `[0,1]`), each independently re-solved for its
    `Gamma` and re-evaluated for its TRUE spectrum by brute force (no
    shortcuts, no reuse of any cached answer). The script does not
    special-case or look up the target `Gamma` anywhere: it only encodes
    the two fiber point-sets as the deterministic plant, then performs the
    linear algebra and the exhaustive search for real. Asserted outcome:
    the swept family contains a member with spectrum
    `[14,3,3,3,3,3,3,3]`, `E_3 = 19 = ell + 2` (it does, at `t = 15`; the
    reconstructed `Gamma` there is byte-for-byte the shipped W3 witness).

  `--d3-search` (`d = 3`, a full projective plane, exhaustive, no seed):
    Re-derives the `ell = 29, p = 233` violation (witness "W1",
    `E_3 = ell + 1`), by the OTHER method the note documents: seed the
    plant on an already-known, pre-existing object's top-2 fibers -- here
    the `(29, 233)` residual-tight witness of
    `experimental/notes/l1/l1_sigma_calculus.md` Sec 2A.2 (`spectrum
    [14,13,5,5,2,2,2,2]`, an "integrated" object, not discovered fresh in
    this search) -- giving a `pairgap = 2` plant (`mu_1+mu_2 = 27 = ell-2`)
    and a 3-dimensional nullspace. `P^2(F_p)` has exactly `p^2+p+1` points;
    this flag enumerates ALL of them (`[1,a,b]` for `a,b = 0..p-1`, plus
    `[0,1,b]` for `b = 0..p-1`, plus `[0,0,1]`) -- `54523` members for
    `p = 233`, matching the note's own accounting exactly. Asserted outcome:
    the swept family contains a member with spectrum
    `[15,14,4,3,3,3,2,2]`, `E_3 = 30 = ell + 1` (the shipped W1 witness).

Both modes are exhaustive (no sampling, no probabilistic miss risk) and
deterministic (no seed argument needed or accepted for either).
"""
import argparse
import sys
import time

# =====================================================================================
# exact F_p arithmetic (self-contained; no imports from sibling scripts)
# =====================================================================================
def inv(a, p):
    return pow(a % p, p - 2, p)

def factorize(n):
    f = set()
    d, m = 2, n
    while d * d <= m:
        while m % d == 0:
            f.add(d)
            m //= d
        d += 1
    if m > 1:
        f.add(m)
    return f

def find_gen(p):
    fac = factorize(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no generator")

def vpow(x, ell, p):
    return [pow(x, r, p) for r in range(1, ell)]

def fiber_rows(points, ell, p):
    """Coincidence rows for one fiber: v(x)-v(anchor) for x in points[1:]."""
    if len(points) < 2:
        return []
    v0 = vpow(points[0], ell, p)
    return [[(v0[r] - vpow(x, ell, p)[r]) % p for r in range(ell - 1)] for x in points[1:]]

def nullspace_basis(rows, ncols, p):
    """Exact nullspace basis (RREF-based) of the given rows over F_p^ncols."""
    if not rows:
        return [[1 if i == j else 0 for i in range(ncols)] for j in range(ncols)]
    A = [[v % p for v in r] for r in rows]
    m = len(A)
    piv = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, m):
            if A[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = inv(A[r][c], p)
        A[r] = [(v * iv) % p for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(ncols)]
        piv.append(c)
        r += 1
        if r == m:
            break
    pivset = set(piv)
    basis = []
    for free in range(ncols):
        if free in pivset:
            continue
        v = [0] * ncols
        v[free] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][free]) % p
        basis.append(v)
    return basis

def recon_gamma(basis, coeffs, p):
    """Gamma = sum_j coeffs[j] * basis[j], normalized so its top nonzero
    coefficient is 1 (fibers are scale-invariant). None if all-zero."""
    gm = [0] * len(basis[0])
    for j, c in enumerate(coeffs):
        if not c:
            continue
        for r in range(len(gm)):
            gm[r] = (gm[r] + c * basis[j][r]) % p
    nz = [i for i, cc in enumerate(gm) if cc]
    if not nz:
        return None
    s = inv(gm[max(nz)], p)
    return [(cc * s) % p for cc in gm]

def brute_spectrum(gamma, p, ell):
    """TRUE spectrum from scratch: group F_p^* by x^ell, per-coset max fiber."""
    groups = {}
    for x in range(1, p):
        lab = pow(x, ell, p)
        v = 0
        for r in range(1, ell):
            v = (v + gamma[r - 1] * pow(x, r, p)) % p
        groups.setdefault(lab, {}).setdefault(v, []).append(x)
    return sorted((max(len(v) for v in byval.values()) for byval in groups.values()), reverse=True)

def E3(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)

def Tval(spec):
    s = sorted(spec, reverse=True)
    return sum(mu - 2 for mu in s[2:] if mu >= 3)

def cosets_of(p, ell):
    """The n=(p-1)/ell cosets of the order-ell subgroup H of F_p^*."""
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    return [[pow(g, i, p) * h % p for h in H] for i in range(n)]

def build_eval_matrix(basis, cs, p, ell):
    """Precompute M[x] = [basis_j evaluated at x] for every point x in every
    coset, so each family member costs only len(basis) multiplications per
    point (fast exhaustive sweep)."""
    Mx = {}
    for pts in cs:
        for x in pts:
            xr = [pow(x, r, p) for r in range(1, ell)]
            Mx[x] = [sum(B[r] * xr[r] for r in range(ell - 1)) % p for B in basis]
    return Mx

def family_spectrum(coeffs, Mx, cs, p):
    """Spectrum of Gamma = sum coeffs[j]*basis[j], via the precomputed Mx."""
    spec = []
    for pts in cs:
        byval = {}
        for x in pts:
            vals = Mx[x]
            v = 0
            for j, c in enumerate(coeffs):
                if c:
                    v += c * vals[j]
            v %= p
            byval[v] = byval.get(v, 0) + 1
        m = max(byval.values())
        if m >= 2:
            spec.append(m)
    spec.sort(reverse=True)
    return spec

# =====================================================================================
# DEFAULT MODE: deterministic d=2 pencil sweep, re-derives W3 (ell=17, p=137)
# =====================================================================================
# The two fiber point-sets below are DATA extracted once (at authoring time)
# from the true spectrum of the shipped W3 witness
# (`experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json`,
# id "W3"): F1 is its actual size-14 fiber (unchanged); F2 is an
# UNDER-PLANTED 2-point subset of its actual size-3 second fiber (one point
# dropped), so mu_1+mu_2 = 16 = ell-1, one below the pairwise-cap ceiling.
# Nothing else about W3 is used: the script does not see its gamma, its
# spectrum, or its E_3 anywhere below except as the ASSERTED target.
W3_ELL, W3_P = 17, 137
W3_F1 = [10, 12, 35, 42, 45, 52, 55, 58, 66, 89, 94, 97, 106, 134]   # size 14 (unmodified)
W3_F2_UNDERPLANT = [38, 72]                                          # 2 of the 3 points of the second fiber
W3_TARGET_SPECTRUM = [14, 3, 3, 3, 3, 3, 3, 3]
W3_TARGET_E3 = 19

def run_default_pencil_sweep(verbose=True):
    ell, p = W3_ELL, W3_P
    t0 = time.time()
    if verbose:
        print("DEFAULT MODE: deterministic d=2 pencil sweep, ell=%d p=%d" % (ell, p))
        print("  plant: F1 (size %d, the actual big fiber) + F2 (size %d, under-planted subset)"
              % (len(W3_F1), len(W3_F2_UNDERPLANT)))
        print("  mu1+mu2 = %d (ell-1 = %d)" % (len(W3_F1) + len(W3_F2_UNDERPLANT), ell - 1))
    rows = fiber_rows(sorted(W3_F1), ell, p) + fiber_rows(sorted(W3_F2_UNDERPLANT), ell, p)
    basis = nullspace_basis(rows, ell - 1, p)
    d = len(basis)
    if verbose:
        print("  nullspace dim d = %d (expect 2, a pencil)" % d)
    if d != 2:
        raise AssertionError("expected a 2-dimensional pencil, got d=%d" % d)

    members = [(t, [1, t]) for t in range(p)] + [("inf", [0, 1])]
    if verbose:
        print("  sweeping ALL p+1 = %d members exhaustively (no early stop, no sampling)..." % (p + 1))
    best_e3, best_spec, best_t = -1, None, None
    found_target = None
    n_reconstructed = 0
    for t, coeffs in members:
        gamma = recon_gamma(basis, coeffs, p)
        if gamma is None:
            continue
        n_reconstructed += 1
        spec = brute_spectrum(gamma, p, ell)
        e3 = E3(spec)
        if e3 > best_e3:
            best_e3, best_spec, best_t = e3, spec, t
        if spec == W3_TARGET_SPECTRUM and found_target is None:
            found_target = (t, gamma, spec, e3)
    elapsed = time.time() - t0
    if verbose:
        print("  members reconstructed: %d/%d  (elapsed %.3fs)" % (n_reconstructed, p + 1, elapsed))
        print("  best E_3 found in the family: %d  (spectrum %s, at t=%s)" % (best_e3, best_spec, best_t))
    ok = (found_target is not None) and (found_target[3] == W3_TARGET_E3)
    if found_target:
        t, gamma, spec, e3 = found_target
        if verbose:
            print("  TARGET FOUND at pencil member t=%s: spectrum=%s E_3=%d (=ell+2=%d)"
                  % (t, spec, e3, ell + 2))
            print("  reconstructed gamma = %s" % gamma)
    else:
        if verbose:
            print("  TARGET NOT FOUND in this pencil (unexpected)")
    return {"ok": ok, "elapsed": elapsed, "members": n_reconstructed,
            "best_E3": best_e3, "best_spectrum": best_spec, "found": found_target}

# =====================================================================================
# --d3-search: deterministic d=3 full-plane sweep, re-derives W1 (ell=29, p=233)
# =====================================================================================
# SAT2: the (ell=29, p=233) residual-tight witness of
# experimental/notes/l1/l1_sigma_calculus.md Sec 2A.2 (spectrum
# [14,13,5,5,2,2,2,2]) -- an ALREADY-KNOWN, pre-existing object (not
# discovered in this search) whose top-2 fibers [14,13] seed the plant.
SAT2_ELL, SAT2_P = 29, 233
SAT2_GAMMA = [203, 187, 107, 98, 59, 120, 193, 102, 190, 101, 206, 153, 193, 196,
              119, 185, 120, 153, 188, 140, 192, 218, 113, 205, 228, 206, 224, 1]
W1_TARGET_SPECTRUM = [15, 14, 4, 3, 3, 3, 2, 2]
W1_TARGET_E3 = 30

def run_d3_seeded_search(verbose=True):
    ell, p = SAT2_ELL, SAT2_P
    t0 = time.time()
    if verbose:
        print("--d3-search MODE: deterministic d=3 full-projective-plane sweep, ell=%d p=%d" % (ell, p))
        print("  seed: top-2 fibers of the pre-existing SAT2 residual-tight witness")
    spec = brute_spectrum(SAT2_GAMMA, p, ell)
    fibers = []
    # recover point-lists for the top-2 fibers of SAT2 (needed for the plant)
    groups = {}
    for x in range(1, p):
        lab = pow(x, ell, p)
        v = 0
        for r in range(1, ell):
            v = (v + SAT2_GAMMA[r - 1] * pow(x, r, p)) % p
        groups.setdefault(lab, {}).setdefault(v, []).append(x)
    all_fibers = []
    for lab, byval in groups.items():
        bv = max(byval, key=lambda vv: len(byval[vv]))
        all_fibers.append(byval[bv])
    all_fibers.sort(key=lambda F: -len(F))
    planted = [sorted(all_fibers[0]), sorted(all_fibers[1])]
    if verbose:
        print("  SAT2 spectrum=%s ; planted top-2 sizes=%s (mu1+mu2=%d, ell-2=%d)"
              % (spec, [len(F) for F in planted], sum(len(F) for F in planted), ell - 2))
    rows = fiber_rows(planted[0], ell, p) + fiber_rows(planted[1], ell, p)
    basis = nullspace_basis(rows, ell - 1, p)
    d = len(basis)
    if verbose:
        print("  nullspace dim d = %d (expect 3)" % d)
    if d != 3:
        raise AssertionError("expected a 3-dimensional family, got d=%d" % d)

    cs = cosets_of(p, ell)
    Mx = build_eval_matrix(basis, cs, p, ell)
    total_expected = p * p + p + 1
    if verbose:
        print("  sweeping ALL p^2+p+1 = %d members of P^2(F_%d) exhaustively..." % (total_expected, p))
    best_e3, best_spec = -1, None
    found_target = None
    count = 0
    checkpoint = max(1, p // 4)
    for a in range(p):
        for b in range(p):
            coeffs = [1, a, b]
            fs = family_spectrum(coeffs, Mx, cs, p)
            e3 = E3(fs)
            count += 1
            if e3 > best_e3:
                best_e3, best_spec = e3, fs
            if fs == W1_TARGET_SPECTRUM and found_target is None:
                found_target = (tuple(coeffs), fs, e3)
        if verbose and (a % checkpoint == 0):
            print("    a=%d/%d  elapsed=%.1fs  best_E3_so_far=%d" % (a, p, time.time() - t0, best_e3), flush=True)
    for b in range(p):
        coeffs = [0, 1, b]
        fs = family_spectrum(coeffs, Mx, cs, p)
        e3 = E3(fs)
        count += 1
        if e3 > best_e3:
            best_e3, best_spec = e3, fs
        if fs == W1_TARGET_SPECTRUM and found_target is None:
            found_target = (tuple(coeffs), fs, e3)
    coeffs = [0, 0, 1]
    fs = family_spectrum(coeffs, Mx, cs, p)
    e3 = E3(fs)
    count += 1
    if e3 > best_e3:
        best_e3, best_spec = e3, fs
    if fs == W1_TARGET_SPECTRUM and found_target is None:
        found_target = (tuple(coeffs), fs, e3)

    elapsed = time.time() - t0
    if verbose:
        print("  members enumerated: %d (expect p^2+p+1=%d)  (elapsed %.1fs)" % (count, total_expected, elapsed))
        print("  best E_3 found in the family: %d  (spectrum %s)" % (best_e3, best_spec))
    ok = (count == total_expected) and (found_target is not None) and (found_target[2] == W1_TARGET_E3)
    if found_target:
        coeffs, fs, e3 = found_target
        gamma = recon_gamma(basis, list(coeffs), p)
        if verbose:
            print("  TARGET FOUND at coeffs=%s: spectrum=%s E_3=%d (=ell+1=%d)" % (coeffs, fs, e3, ell + 1))
            print("  reconstructed gamma = %s" % gamma)
    return {"ok": ok, "elapsed": elapsed, "members": count,
            "best_E3": best_e3, "best_spectrum": best_spec, "found": found_target}

# =====================================================================================
# CLI
# =====================================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--d3-search", action="store_true",
                     help="also run the deterministic d=3 seeded full-plane sweep (re-derives W1, ell=29 p=233)")
    ap.add_argument("-q", "--quiet", action="store_true", help="suppress progress printing")
    args = ap.parse_args()

    t0 = time.time()
    print("=" * 90)
    print(" l1_pencil_family_sweep: under-plant-then-exhaustively-sweep CONSTRUCTOR")
    print(" (companion to experimental/notes/l1/l1_e3_law_refuted.md)")
    print("=" * 90)

    res1 = run_default_pencil_sweep(verbose=not args.quiet)
    all_ok = res1["ok"]
    print("-" * 90)
    print(" DEFAULT MODE RESULT: %s  (spectrum=%s E_3=%d, %d members, %.3fs)"
          % ("FOUND (matches W3)" if res1["ok"] else "NOT FOUND",
             res1["found"][2] if res1["found"] else None,
             res1["found"][3] if res1["found"] else -1,
             res1["members"], res1["elapsed"]))

    if args.d3_search:
        print("-" * 90)
        res2 = run_d3_seeded_search(verbose=not args.quiet)
        all_ok = all_ok and res2["ok"]
        print("-" * 90)
        print(" --d3-search RESULT: %s  (spectrum=%s E_3=%d, %d members, %.1fs)"
              % ("FOUND (matches W1)" if res2["ok"] else "NOT FOUND",
                 res2["found"][1] if res2["found"] else None,
                 res2["found"][2] if res2["found"] else -1,
                 res2["members"], res2["elapsed"]))

    print("=" * 90)
    print(" RESULT: %s   (total %.1fs)"
          % ("ALL TARGETS RE-DERIVED" if all_ok else "FAILURE", time.time() - t0))
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
