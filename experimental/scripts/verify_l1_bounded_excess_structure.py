#!/usr/bin/env python3
"""verify_l1_bounded_excess_structure.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_bounded_excess_structure.md`, which packages three
exact structural results toward the post-refutation open target
`E_3 <= ell + C'` (currently observed `C' = 2`, NOT proved extremal):

  (i)   the excess identity  excess = E_3-ell = T-4-capslack
        (capslack = ell-(mu_1+mu_2)), verified on the six
        `l1_e3_law_refuted.md` residual-chart witnesses;
  (ii)  the Lemma-R sub-ceiling for the canonical fat-tail shape
        `[ell-3, 3^k]`:  excess <= floor((2*ell-20)/3)  -- PROVES excess<=2
        at ell<=13, but only <=4 at ell=17 (W3 attains +2, a gap of 2);
  (iii) a concrete q-plane concurrency spot-check on the record witness W3:
        the 7 tail 3-fibers, solved INDEPENDENTLY from each other (no use of
        the global Gamma), all recover the identical point of the
        degree-<=2 "q-plane" P^2(F_p);
  (iv)  a bounded-time re-run of the (ell=19,p=229,n=12) toy sweep: the full
        130-dropset sweep took 661.8s offline (embedded here as a
        certificate), so this gate reproduces the reported best dropset live
        plus a small deterministic subsample, stating explicitly that this
        is a subsample, not a full reproduction.

Ground rule: self-contained. This script does NOT import from, edit, or
depend on any other script's claims being true, the source hunt's scratch
files, or the two concurrent (unmerged) sibling PRs it cites by path only
(`l1_ell19_band_refuted.md` / PR #364, `l1_e3_dim_syz_crux_refuted.md` /
PR #365). Every witness is reconstructed here from its raw `gamma` alone.

Four gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)   excess identity, all six `l1_e3_law_refuted.md` witnesses, plus
        pairwise-cap-holds-on-every-pair and top-pair-is-the-maximum checks
  (ii)  Lemma-R sub-ceiling table (ell in {11,13,17,19,23,29}), the
        ell<=13=>excess<=2 consequence, Lemma R's raw inequality on all six
        witnesses, and the W3-specific mu_1=ell-3 => mu_2<=3 instance
  (iii) q-plane spot-check on W3 (recover q from the big fiber, recover it
        again independently from each of the 7 tail 3-fibers, check they
        all coincide)
  (iv)  bounded-time re-run at (ell=19,p=229,n=12): live reproduction of the
        reported global-best dropset + a 4-triple deterministic subsample,
        with the full 130-plant sweep embedded as certificate data

Hidden self-test: python3 verify_l1_bounded_excess_structure.py
--tamper-selftest flips one datum per gate class and asserts each gate then
FAILS. The shipped default is zero-arg.

All arithmetic is exact over F_p, stdlib only. No network, no files, no CLI
args required. Runtime target < 60s for gates i-iii; gate iv adds ~20s for
its 5 live dropset sweeps (total < 90s).
"""
import sys
import time
import itertools

# =====================================================================================
# exact F_p polynomial + linear-algebra arithmetic (self-contained; a fresh port of
# the conventions used throughout the integrated L1 verifiers -- NOT an import)
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

def trim(c):
    out = list(c)
    while out and out[-1] == 0:
        out.pop()
    return out

def pmul(a, b, p):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        ai %= p
        if ai:
            for j, bj in enumerate(b):
                out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out)

def padd(a, b, p):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(len(a)):
        out[i] = a[i] % p
    for i in range(len(b)):
        out[i] = (out[i] + b[i]) % p
    return trim(out)

def poly_from_roots(rs, p):
    out = [1]
    for r in rs:
        out = pmul(out, [(-r) % p, 1], p)
    return out

def poly_div_exact(num, den, p):
    """Exact polynomial division num/den over F_p; raises if remainder != 0."""
    num = trim(list(num))
    den = trim(list(den))
    if not den:
        raise ZeroDivisionError
    if len(num) < len(den):
        if not num:
            return []
        raise ValueError("does not divide (deg num < deg den)")
    rem = num[:]
    dlead_inv = inv(den[-1], p)
    q = [0] * (len(rem) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        coeff = rem[i + len(den) - 1] * dlead_inv % p
        q[i] = coeff
        if coeff:
            for j, dj in enumerate(den):
                rem[i + j] = (rem[i + j] - coeff * dj) % p
    rem = trim(rem)
    if rem:
        raise ValueError("does not divide exactly, nonzero remainder %r" % (rem,))
    return q

def peval(poly, x, p):
    v = 0
    for c in reversed(poly):
        v = (v * x + c) % p
    return v

def nullspace_basis(rows, ncols, p):
    """RREF-based nullspace basis of the row space of `rows` (each length
    ncols) over F_p. Returns a list of basis vectors (each length ncols)."""
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

def gamma_eval(gamma, x, p):
    """Gamma(x) = sum_{r=1}^{ell-1} gamma[r-1] x^r  (constant-free)."""
    v = 0
    for c in reversed(gamma):
        v = (v * x + c) % p
    return v * x % p

def build_spectrum(gamma, p, ell):
    """Group F_p^* by x^ell; per coset take the modal Gamma-value class.
    Return the list of (coset_label, points) with fiber size >= 2, sorted
    largest-first."""
    groups = {}
    for x in range(1, p):
        w = pow(x, ell, p)
        groups.setdefault(w, []).append(x)
    fibers = []
    for w, xs in groups.items():
        byval = {}
        for x in xs:
            v = gamma_eval(gamma, x, p)
            byval.setdefault(v, []).append(x)
        best_v = max(byval, key=lambda v: len(byval[v]))
        fibers.append((w, sorted(byval[best_v])))
    fibers = [(w, xs) for w, xs in fibers if len(xs) >= 2]
    fibers.sort(key=lambda t: -len(t[1]))
    return fibers

def E3_of(mus):
    return sum(m - 2 for m in mus if m >= 3)

def T_of(mus):
    """T = sum_{k>=3}(mu_k-2)_+ from the THIRD-largest fiber onward
    (mus assumed already sorted descending)."""
    return sum(m - 2 for m in mus[2:] if m >= 3)

def normalize_proj(v, p):
    for c in v:
        if c % p:
            iv = inv(c, p)
            return tuple((cc * iv) % p for cc in v)
    return tuple(v)

# =====================================================================================
# the six E_3<=ell law-refutation witnesses (verbatim raw gammas from
# experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json /
# experimental/notes/l1/l1_e3_law_refuted.md Sec 1; "expect" values were
# independently cross-checked against that JSON and against
# verify_l1_e3_law_refuted.py's own WITNESSES table before shipping -- this
# verifier recomputes every one of them here from scratch, from the raw
# gamma alone, via a fresh spectrum implementation)
# =====================================================================================
WITNESSES = [
    {"id": "W3", "ell": 17, "p": 137,
     "gamma": [95, 83, 94, 43, 16, 101, 72, 52, 93, 129, 47, 76, 80, 45, 64, 1],
     "expect_spectrum": [14, 3, 3, 3, 3, 3, 3, 3], "expect_E3": 19, "expect_T": 6},
    {"id": "W1", "ell": 29, "p": 233,
     "gamma": [126, 24, 50, 214, 172, 207, 131, 212, 64, 48, 179, 143, 189, 59,
               86, 107, 196, 67, 125, 47, 63, 162, 110, 189, 69, 218, 156, 1],
     "expect_spectrum": [15, 14, 4, 3, 3, 3, 2, 2], "expect_E3": 30, "expect_T": 5},
    {"id": "W2", "ell": 23, "p": 139,
     "gamma": [91, 120, 12, 78, 12, 136, 48, 11, 118, 111, 69, 66, 43, 110, 6,
               14, 54, 38, 104, 2, 76, 1],
     "expect_spectrum": [14, 9, 4, 4, 3, 2], "expect_E3": 24, "expect_T": 5},
    {"id": "EXTRA1_ell29_p233_a", "ell": 29, "p": 233,
     "gamma": [17, 195, 160, 138, 183, 48, 208, 127, 215, 127, 165, 216, 5, 154,
               15, 168, 221, 41, 15, 96, 205, 78, 67, 200, 8, 208, 182, 1],
     "expect_spectrum": [20, 9, 4, 3, 3, 3, 2, 2], "expect_E3": 30, "expect_T": 5},
    {"id": "EXTRA2_ell29_p233_b", "ell": 29, "p": 233,
     "gamma": [83, 0, 6, 232, 143, 192, 212, 48, 86, 182, 127, 17, 104, 134,
               194, 213, 17, 205, 118, 19, 45, 203, 39, 182, 145, 212, 102, 1],
     "expect_spectrum": [16, 13, 4, 3, 3, 3, 2, 2], "expect_E3": 30, "expect_T": 5},
    {"id": "EXTRA3_ell17_p103", "ell": 17, "p": 103,
     "gamma": [1, 30, 67, 2, 86, 41, 28, 85, 62, 87, 80, 84, 36, 89, 76, 1],
     "expect_spectrum": [11, 5, 5, 4, 3, 2], "expect_E3": 18, "expect_T": 6},
]

EXPECTED_SUBCEILING = {11: 0, 13: 2, 17: 4, 19: 6, 23: 8, 29: 12}

# W3's known size-(ell-3) planted fiber (the same 14 points used to validate
# the source hunt's toolkit; re-derived here independently of that use)
W3_ELL, W3_P = 17, 137
W3_GAMMA = [95, 83, 94, 43, 16, 101, 72, 52, 93, 129, 47, 76, 80, 45, 64, 1]
W3_F0 = sorted([10, 12, 35, 42, 45, 52, 55, 58, 66, 89, 94, 97, 106, 134])

# the (ell=19,p=229,n=12) toy-sweep certificate (matches laneG_results.json /
# the shipped ledger JSON exactly): full 130-of-969-possible-dropset sweep,
# 661.8s offline. max_excess is 0 here (E_3=19=ell exactly) -- NOT +1; see
# note Sec 5 correction #2.
TOY_ELL, TOY_P = 19, 229
TOY_BIG_EXCL = (0, 2, 15)
TOY_BIG_EXPECT_SPEC = [16, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2]
TOY_BIG_EXPECT_E3 = 19
TOY_FULL_SWEEP_CERT = {
    "plants_done": 130, "plants_requested": 130, "of_possible_dropsets": 969,
    "max_E3": 19, "max_excess": 0, "secs": 661.8,
    "best_spec": TOY_BIG_EXPECT_SPEC, "best_excl": list(TOY_BIG_EXCL),
}

# =====================================================================================
# GATE (i): the excess identity, all six witnesses
# =====================================================================================
def gate_i_excess_identity(tamper=False):
    ok = True
    lines = []
    for wi, w in enumerate(WITNESSES):
        gamma = list(w["gamma"])
        if tamper and wi == 0:
            gamma[0] = (gamma[0] + 1) % w["p"]
        ell = w["ell"]
        fibers = build_spectrum(gamma, w["p"], ell)
        mus = [len(xs) for _, xs in fibers]
        spec_ok = (mus == w["expect_spectrum"])
        e3 = E3_of(mus)
        T = T_of(mus)
        e3_ok = (e3 == w["expect_E3"])
        t_ok = (T == w["expect_T"])
        capslack = ell - (mus[0] + mus[1])
        excess = e3 - ell
        identity_ok = (excess == T - 4 - capslack)
        allpairs = [mus[i] + mus[j] for i in range(len(mus)) for j in range(i + 1, len(mus))]
        cap_ok = all(s <= ell for s in allpairs)
        top_is_max = (max(allpairs) == mus[0] + mus[1]) if allpairs else True
        good = spec_ok and e3_ok and t_ok and identity_ok and cap_ok and top_is_max
        ok = ok and good
        lines.append(
            "%s: spec==expect:%s E3=%d(exp %d) T=%d(exp %d) capslack=%d excess=%+d "
            "identity(excess==T-4-capslack):%s cap_all_pairs<=ell:%s top_pair_is_max_pair:%s"
            % (w["id"], spec_ok, e3, w["expect_E3"], T, w["expect_T"], capslack, excess,
               identity_ok, cap_ok, top_is_max))
    return ok, " | ".join(lines)

# =====================================================================================
# GATE (ii): Lemma-R sub-ceiling table + consequence + raw Lemma R on witnesses
# =====================================================================================
def gate_ii_lemma_r_subceiling(tamper=False):
    ok = True
    lines = []
    expected = dict(EXPECTED_SUBCEILING)
    if tamper:
        expected[17] = expected[17] + 1  # corrupt one table entry
    for ell in sorted(expected):
        kmax = (2 * ell - 5) // 3
        ceiling = kmax - 5
        alt = (2 * ell - 20) // 3
        row_ok = (ceiling == alt) and (ceiling == expected[ell])
        ok = ok and row_ok
        lines.append("ell=%2d: kmax=floor((2ell-5)/3)=%2d ceiling=k_max-5=%+d altform floor((2ell-20)/3)=%+d expect=%+d :%s"
                     % (ell, kmax, ceiling, alt, expected[ell], row_ok))
    consequence_ok = (expected[11] <= 2) and (expected[13] <= 2) and (expected[17] > 2)
    ok = ok and consequence_ok
    lines.append("consequence ell<=13=>excess<=2 (11:%+d<=2, 13:%+d<=2), ell=17 EXCEEDS 2 (%+d>2): %s"
                 % (EXPECTED_SUBCEILING[11], EXPECTED_SUBCEILING[13], EXPECTED_SUBCEILING[17], consequence_ok))
    # raw Lemma R inequality (sum mu(mu-1) <= (ell-1)(ell-2)) + W3 shape check, on real data
    for w in WITNESSES:
        gamma = list(w["gamma"])
        ell = w["ell"]
        fibers = build_spectrum(gamma, w["p"], ell)
        mus = [len(xs) for _, xs in fibers]
        lemma_r_val = sum(m * (m - 1) for m in mus)
        bound = (ell - 1) * (ell - 2)
        lemma_r_ok = (lemma_r_val <= bound)
        ok = ok and lemma_r_ok
        lines.append("%s: Lemma R sum mu(mu-1)=%d <= (ell-1)(ell-2)=%d : %s"
                     % (w["id"], lemma_r_val, bound, lemma_r_ok))
        if w["id"] == "W3":
            mu1, mu2 = mus[0], mus[1]
            w3_ok = (mu1 == ell - 3) and (mu2 <= ell - mu1) and (mu2 == 3)
            ok = ok and w3_ok
            lines.append("W3 shape: mu1=%d(==ell-3:%s) => cap forces mu2<=%d, actual mu2=%d(==3:%s) : %s"
                         % (mu1, mu1 == ell - 3, ell - mu1, mu2, mu2 == 3, w3_ok))
    return ok, " | ".join(lines)

# =====================================================================================
# GATE (iii): q-plane spot-check on W3
# =====================================================================================
def solve_q_from_triple(g0, x, y, z, p):
    """The 2 linear homogeneous equations in q=(q0,q1,q2) forcing
    g0(x)q(x)=g0(y)q(y)=g0(z)q(z); return the nullspace basis (expect dim 1)."""
    def g0_eval(a):
        return peval(g0, a, p)

    def row(a, b):
        ga, gb = g0_eval(a), g0_eval(b)
        return [(ga - gb) % p, (ga * a - gb * b) % p, (ga * a * a - gb * b * b) % p]

    M = [row(x, y), row(y, z)]
    return nullspace_basis(M, 3, p)

def gate_iii_qplane(tamper=False):
    p, ell = W3_P, W3_ELL
    gamma = list(W3_GAMMA)
    F0 = list(W3_F0)

    def Gamma_eval(x):
        return gamma_eval(gamma, x, p)

    vals0 = set(Gamma_eval(x) for x in F0)
    f0_const_ok = (len(vals0) == 1)
    lambda0 = next(iter(vals0)) if f0_const_ok else 0

    g0 = poly_from_roots(F0, p)
    deg_g0_ok = (len(g0) - 1 == ell - 3)

    Gamma_poly = [0] + gamma
    Gamma_minus = padd(Gamma_poly, [(-lambda0) % p], p)
    q = poly_div_exact(Gamma_minus, g0, p)
    deg_q_ok = (len(q) - 1 == 2)

    recon = padd(pmul(g0, q, p), [lambda0], p)
    recon = (recon + [0] * ell)[:ell]
    gamma_padded = (Gamma_poly + [0] * ell)[:ell]
    recon_ok = (recon == gamma_padded)

    if tamper:
        q = list(q)
        q[0] = (q[0] + 1) % p  # corrupt q AFTER the honest reconstruction check above

    # find all cosets, then the 7 tail 3-fibers (every coset not containing F0)
    g = find_gen(p)
    n = (p - 1) // ell
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    cosets = [sorted([pow(g, i, p) * h % p for h in H]) for i in range(n)]
    F0_set = set(F0)
    tail_fibers = []
    for cs in cosets:
        if F0_set <= set(cs):
            continue
        byval = {}
        for x in cs:
            v = Gamma_eval(x)
            byval.setdefault(v, []).append(x)
        best = max(byval.values(), key=len)
        tail_fibers.append(sorted(best))
    tail_ok = (len(tail_fibers) == 7) and all(len(tf) == 3 for tf in tail_fibers)

    qglobal_norm = normalize_proj(q, p)
    recovered = []
    for tf in tail_fibers:
        x, y, z = tf
        basis = solve_q_from_triple(g0, x, y, z, p)
        onepoint_ok = (len(basis) == 1)
        qn = normalize_proj(basis[0], p) if onepoint_ok else None
        recovered.append((tf, qn, onepoint_ok))

    all_onepoint = all(onepoint_ok for _, _, onepoint_ok in recovered)
    all_match = all(qn == qglobal_norm for _, qn, _ in recovered)

    ok = f0_const_ok and deg_g0_ok and deg_q_ok and recon_ok and tail_ok and all_onepoint and all_match
    lines = [
        "F0(size %d) constant under Gamma:%s (lambda0=%d) deg(g0)==ell-3:%s deg(q)==2:%s "
        "Gamma==g0*q+lambda0 (reconstruction):%s" % (len(F0), f0_const_ok, lambda0, deg_g0_ok, deg_q_ok, recon_ok),
        "7 tail cosets each carry one size-3 fiber:%s ; global q(normalized)=%s" % (tail_ok, qglobal_norm),
    ]
    for tf, qn, onepoint_ok in recovered:
        lines.append("  fiber %s -> independently-solved q=%s (unique point:%s, matches global:%s)"
                     % (tf, qn, onepoint_ok, qn == qglobal_norm))
    return ok, " | ".join(lines)

# =====================================================================================
# GATE (iv): bounded-time toy re-run at (ell=19,p=229,n=12)
# =====================================================================================
def cosets_of(p, ell):
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    return [[pow(g, i, p) * h % p for h in H] for i in range(n)]

def fiber_rows(points, ell, p):
    if len(points) < 2:
        return []
    v0 = [pow(points[0], r, p) for r in range(1, ell)]
    rows = []
    for x in points[1:]:
        vx = [pow(x, r, p) for r in range(1, ell)]
        rows.append([(v0[r] - vx[r]) % p for r in range(ell - 1)])
    return rows

def build_coord_map(basis, cosets, ell, p):
    Mx = {}
    for pts in cosets:
        for x in pts:
            xr = [pow(x, r, p) for r in range(1, ell)]
            Mx[x] = tuple(sum(B[r] * xr[r] for r in range(ell - 1)) % p for B in basis)
    return Mx

def family_spectrum(coeffs, Mx, cosets, p):
    spec = []
    for pts in cosets:
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

def proj_points_d3(p):
    """Every point of P^2(F_p), leading-1 normal form: p^2+p+1 points total."""
    for a in range(p):
        for b in range(p):
            yield (1, a, b)
    for b in range(p):
        yield (0, 1, b)
    yield (0, 0, 1)

def E3_spec(spec):
    return sum(m - 2 for m in spec if m >= 3)

def sweep_one_dropset(ell, p, excl, cosets, c0):
    bigf = [c0[i] for i in range(ell) if i not in set(excl)]
    rows = fiber_rows(sorted(bigf), ell, p)
    basis = nullspace_basis(rows, ell - 1, p)
    d = len(basis)
    if d != 3:
        raise AssertionError("expected nullspace dim 3, got %d for excl=%s" % (d, excl))
    Mx = build_coord_map(basis, cosets, ell, p)
    best_e3 = -1
    best_spec = None
    for coeffs in proj_points_d3(p):
        fs = family_spectrum(coeffs, Mx, cosets, p)
        e3 = E3_spec(fs)
        if e3 > best_e3:
            best_e3, best_spec = e3, fs
    return best_e3, best_spec

def gate_iv_toy_rerun(tamper=False):
    ell, p = TOY_ELL, TOY_P
    cosets = cosets_of(p, ell)
    c0 = cosets[0]
    ok = True
    lines = []

    # (a) live reproduction of the specific reported global-best dropset
    best_e3, best_spec = sweep_one_dropset(ell, p, TOY_BIG_EXCL, cosets, c0)
    claimed_spec = list(TOY_BIG_EXPECT_SPEC)
    if tamper:
        claimed_spec[0] += 1  # corrupt the certificate's claimed spectrum
    reproduce_ok = (best_spec == claimed_spec) and (best_e3 == TOY_BIG_EXPECT_E3) and (best_e3 - ell == 0)
    ok = ok and reproduce_ok
    lines.append("live resweep of the reported best dropset excl=%s: E3=%d excess=%+d spec=%s == claimed %s : %s"
                 % (TOY_BIG_EXCL, best_e3, best_e3 - ell, best_spec, claimed_spec, reproduce_ok))

    # (b) a small DETERMINISTIC subsample (first 4 lex triples of C(19,3)=969)
    #     -- explicitly not a reproduction of the full 130-plant/661.8s sweep
    subsample = list(itertools.combinations(range(ell), 3))[:4]
    no_win = True
    for excl in subsample:
        e3, spec = sweep_one_dropset(ell, p, excl, cosets, c0)
        excess = e3 - ell
        win = (excess >= 3)
        no_win = no_win and (not win)
        lines.append("deterministic-subsample excl=%s: E3=%d excess=%+d spec=%s win(excess>=3):%s"
                     % (excl, e3, excess, spec, win))
    ok = ok and no_win

    # (c) the embedded full-130-plant certificate (computed offline, 661.8s;
    #     stated here, not reproduced live) is at least internally consistent
    cert = TOY_FULL_SWEEP_CERT
    cert_ok = (cert["max_excess"] == cert["max_E3"] - ell == 0) and (cert["best_spec"] == TOY_BIG_EXPECT_SPEC) \
        and (cert["plants_done"] == cert["plants_requested"] == 130) and (cert["of_possible_dropsets"] == 969)
    ok = ok and cert_ok
    lines.append("embedded full-sweep certificate (130/969 dropsets, 661.8s OFFLINE, not reproduced live here): "
                 "max_E3=%d excess=%+d spec=%s internally consistent:%s"
                 % (cert["max_E3"], cert["max_excess"], cert["best_spec"], cert_ok))
    return ok, " | ".join(lines)

GATES = [
    ("(i)   excess identity (six witnesses)      ", gate_i_excess_identity),
    ("(ii)  Lemma-R sub-ceiling table + raw check", gate_ii_lemma_r_subceiling),
    ("(iii) q-plane spot-check on W3             ", gate_iii_qplane),
    ("(iv)  bounded toy re-run (19,229,n=12)      ", gate_iv_toy_rerun),
]

def main():
    assert len(WITNESSES) == 6, "expected 6 witnesses"
    assert len(EXPECTED_SUBCEILING) == 6, "expected 6 ell rows in the sub-ceiling table"
    assert len(W3_F0) == 14, "expected W3's planted fiber to have 14 points"
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 96)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum/claim is corrupted")
    else:
        print(" verify_l1_bounded_excess_structure  (zero-arg)")
        print(" experimental/notes/l1/l1_bounded_excess_structure.md -- C' localized to +2, NOT proved")
    print("=" * 96)
    all_good = True
    for name, fn in GATES:
        if selftest:
            ok, summ = fn(tamper=True)
            caught = not ok
            all_good = all_good and caught
            print("  %s  TAMPER %s" % (name, "CAUGHT " if caught else "MISSED!"))
            print("        %s" % summ)
        else:
            ok, summ = fn(tamper=False)
            all_good = all_good and ok
            print("  %s  %s" % (name, "PASS" if ok else "FAIL"))
            print("        %s" % summ)
    print("=" * 96)
    if selftest:
        print(" SELF-TEST RESULT: %s   (%.1fs)"
              % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)" % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)

if __name__ == "__main__":
    main()
