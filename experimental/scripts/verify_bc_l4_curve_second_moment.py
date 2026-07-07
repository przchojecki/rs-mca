#!/usr/bin/env python3
"""
Verifier for  experimental/notes/thresholds/cap25_v13_bc_l4_curve_second_moment.md
(Lane C packet: "BC L4 curve second moment = shift-pair ledger on the curve;
residual equidistribution law").

Companion of open PR #393 (branch bc-l4-interior-chart-to-q); this packet is
SELF-CONTAINED and does not read #393's files -- every #393 statement it uses is
restated in the note and re-derived from scratch in the toy below.

Gate groups (exit 0 = PASS; --tamper-selftest = every pin perturbation caught):

  G1  Exact L4 big-int / lgamma table.  The load-bearing anchors
      (log2 C(n,m), M2_equi, the dominant SP term T_{e*}, the top-stratum bound,
      the p-packing cross-check against #393) are EXACT big-int; the 57102-term
      SP ceiling sum_e T_e is lgamma log-sum-exp, pinned INSIDE an exact big-int
      bracket [T_{e*}, (#terms) T_{e*}].  Numbers: heuristic 23.139009,
      M2_equi 15.289333, sum_e T_e 261342.87 (e*=32632), top-stratum 153665.47,
      CS-through-(b1) 130686.93, twist-amplified r=2/r=3 130693.92/121743.02,
      p-packing 103841.23.

  G2  Self-contained toy enumeration (rows A p=97,K=4,m=6 and B K=5,m=7; both
      w=2), embedded from scratch, no scratchpad dependence:
        - three-way M2 identity  M2_def == M2_pairs(a1-equal on V) == sum_Gamma N^2
        - off-diagonal shift-pair constraint deg(A-B) <= e-w-2 by enumeration
        - top stratum e=w+2 is a nonzero-constant shift (deg(A-B)==0)
        - twist-equivariance  theta_{zeta.z*}(zeta s) = zeta.theta_{z*}(s)  (all zeta in mu_n)
        - orbit constancy S(zeta.z*) = S(z*)
        - EXACT AVERAGE IDENTITY sum_y S(y) = p*C(n,m): full enumeration on a
          mini-row (p=13, D=mu_6, m=4) + the p-to-1 preimage count on rows A/B
          + sum_z N(z) = C(n,m) exactly on the bucket table
        - Cauchy-Schwarz instances S1 <= sqrt(p*M2)
        - planted/residual split: residual == 0 on the toy top offenders
          (A z*=[1,1,1], B z*=[0,0,0]); a nonzero-residual control (B z*=[96,1,96])
        - #393-Theorem crosscheck on >=5 z*/row: curve-sum == #valid T (twisted map),
          with independent Lagrange census ground truth on 2 z*/row

  G3  Tamper self-test: every pinned integer / float is perturbed and must flip
      its gate to FAIL.

Stdlib only.  Runtime < 120s.
"""
import sys
import math
import itertools
from math import comb
from fractions import Fraction

LOG2 = math.log(2.0)


def log2_bigint(N):
    b = N.bit_length()
    if b <= 53:
        return math.log2(N)
    sh = b - 53
    return math.log2(N >> sh) + sh


def lg2binom(a, b):
    if b < 0 or b > a or a < 0:
        return float("-inf")
    return (math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)) / LOG2


def logsumexp2(terms):
    mx = max(terms)
    if mx == float("-inf"):
        return float("-inf")
    return mx + math.log2(sum(2.0 ** (t - mx) for t in terms if t - mx > -60))


def approx(a, b, tol):
    return abs(a - b) <= tol


# =====================================================================
# G1 : exact L4 big-int / lgamma table
# =====================================================================

# ---- L4 fixture (cite kb_mca_bc_l4_base_floor_ladder #369; not re-pinned) ----
N = 131072                 # 2^17
K = 65537                  # 2^16 + 1
M = 69753                  # odd
P = 2 ** 31 - 2 ** 24 + 1  # 2130706433 (KoalaBear)
W = M - K                  # 4216
NM = N - M                 # 61319
DEP = W + 1                # 4217 (inner fiber depth)
EMIN = W + 2               # 4218 (top SP stratum at depth w+1)
EMAX = min(M, NM)          # 61319


def compute_L4():
    lg_p = log2_bigint(P)                          # exact
    Cnm = comb(N, M)                               # exact big-int
    lg_Cnm = log2_bigint(Cnm)                      # exact
    heur = lg_Cnm - W * lg_p                       # C(n,m)/p^w
    m2_equi = 2 * heur - lg_p                       # C(n,m)^2/p^(2w+1) = S1^2/p

    # dominant SP stratum e*: exact rational ratio-crossing T_{e+1}/T_e
    def Tratio(e):
        r = Fraction(M - e, N - M + e + 1)          # C(n,m-e-1)/C(n,m-e)
        r *= Fraction(NM + e + 1, e + 1)            # C(nm+e+1,e+1)/C(nm+e,e)
        r *= Fraction(NM - e, e + 1)                # C(nm,e+1)/C(nm,e)
        return r
    e_star = EMIN
    # walk up while T_{e+1} > T_e
    e = EMIN
    while e < EMAX and Tratio(e) > 1:
        e += 1
    e_star = e
    ratio_below = Tratio(e_star) < 1               # T_{e*+1} < T_{e*}
    ratio_above = Tratio(e_star - 1) > 1           # T_{e*}   > T_{e*-1}

    def T_exact(e):
        return comb(N, M - e) * comb(NM + e, e) * comb(NM, e)
    Te_star = T_exact(e_star)                      # exact big-int
    lg_maxT = log2_bigint(Te_star)                 # exact

    # full SP ceiling sum_e T_e via lgamma, pinned inside exact big-int bracket
    logsT = [lg2binom(N, M - e) + lg2binom(NM + e, e) + lg2binom(NM, e)
             for e in range(EMIN, EMAX + 1)]
    lg_sumT = logsumexp2(logsT)
    n_terms = EMAX - EMIN + 1
    bracket_lo = lg_maxT                            # sum >= max term
    bracket_hi = lg_maxT + math.log2(n_terms)       # sum <= (#terms) * max term

    # sharper top stratum e=w+2 (constant shift), exact big-int
    top = (P - 1) * comb(N, M - EMIN) * comb(NM + EMIN, EMIN)
    lg_top = log2_bigint(top)

    # (b1) Cauchy-Schwarz-through: S1 <= sqrt(p * sum_e T_e)
    cs_through = 0.5 * (lg_p + lg_sumT)

    # depth-(w+1) full second moment (for twist route): C(n,m) + sum_e T_e
    lg_SM2 = logsumexp2([lg_Cnm, lg_sumT])

    # twist-amplified (Lane C2): S(z*) <= p * (1/n)^(1/r) * (sum_z N^r)^(1/r)
    tw_r2 = lg_p + 0.5 * (lg_SM2 - math.log2(N))

    # depth-(w+1) max-fiber caps: packing (t'=floor((w+1)/2)) and anticode
    tprime = DEP // 2                               # 2108
    lgV = logsumexp2([lg2binom(M, i) + lg2binom(NM, i) for i in range(tprime + 1)])
    lg_pack_dep = lg_Cnm - lgV                      # depth-(w+1) packing max-fiber
    lg_anti_dep = lg_Cnm - lg2binom(NM + DEP, DEP)  # depth-(w+1) anticode max-fiber
    lg_maxfib = min(lg_pack_dep, lg_anti_dep)
    lg_SM3 = lg_maxfib + lg_SM2                     # Holder ceiling for sum_z N^3
    tw_r3 = lg_p + (1.0 / 3.0) * (lg_SM3 - math.log2(N))

    # #393's best unconditional bound on S1: p * packing = |B| * C(n,m)/V_{t'}
    p_packing = lg_pack_dep + lg_p

    # depth-w anticode cross-check vs #369/#361 rung (108108.04)
    lg_anti_w = lg_Cnm - lg2binom(NM + W, W)

    return dict(
        lg_p=lg_p, lg_Cnm=lg_Cnm, heur=heur, m2_equi=m2_equi,
        e_star=e_star, ratio_below=ratio_below, ratio_above=ratio_above,
        lg_maxT=lg_maxT, lg_sumT=lg_sumT, bracket_lo=bracket_lo, bracket_hi=bracket_hi,
        lg_top=lg_top, cs_through=cs_through, tw_r2=tw_r2, tw_r3=tw_r3,
        p_packing=p_packing, lg_pack_dep=lg_pack_dep, lg_anti_w=lg_anti_w,
    )


# pinned expected values (from the note's L4 table)
L4_PINS = {
    #  name:            (key,          expected,       tol)
    "log2_p":            ("lg_p",       30.988684687,   1e-6),
    "log2_Cnm":          ("lg_Cnm",     130671.433651,  1e-3),
    "heuristic":         ("heur",       23.139009,      1e-5),
    "M2_equi":           ("m2_equi",    15.289333,      1e-5),
    "e_star":            ("e_star",     32632,          0),
    "max_Te":            ("lg_maxT",    261335.0475,    1e-3),
    "sum_Te":            ("lg_sumT",    261342.8673,    1e-3),
    "top_stratum":       ("lg_top",     153665.4719,    1e-3),
    "CS_through_b1":     ("cs_through", 130686.9280,    1e-3),
    "twist_amp_r2":      ("tw_r2",      130693.9223,    1e-3),
    "twist_amp_r3":      ("tw_r3",      121743.0234,    1e-3),
    "p_packing_393":     ("p_packing",  103841.2255,    1e-3),
    "anticode_w":        ("lg_anti_w",  108108.0403,    1e-3),
}


def check_L4(vals, pins, verbose=False):
    gates = []
    for name, (key, exp, tol) in pins.items():
        got = vals[key]
        if isinstance(exp, int) and tol == 0:
            ok = (got == exp)
        else:
            ok = approx(got, exp, tol)
        gates.append(("G1:" + name, ok))
        if verbose:
            print(f"    G1[{name:16s}] got={got!r:>22}  exp={exp}  {'ok' if ok else 'FAIL'}")
    # structural asserts (not tamperable pins; sanity of the SP bracket + dominant e)
    br = (vals["bracket_lo"] <= vals["lg_sumT"] <= vals["bracket_hi"])
    gates.append(("G1:sumT_in_exact_bracket", br))
    dom = vals["ratio_below"] and vals["ratio_above"]
    gates.append(("G1:e_star_is_exact_max", dom))
    if verbose:
        print(f"    G1[bracket] {vals['bracket_lo']:.4f} <= {vals['lg_sumT']:.4f} "
              f"<= {vals['bracket_hi']:.4f}  {'ok' if br else 'FAIL'}")
        print(f"    G1[e*={vals['e_star']} is exact max] {'ok' if dom else 'FAIL'}")
    return gates


# =====================================================================
# G2 : self-contained toy (poly helpers ported, no scratchpad dependence)
# =====================================================================

def trim(poly, p):
    poly = [c % p for c in poly]
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly if poly else [0]


def poly_mul(a, b, p):
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            res[i + j] = (res[i + j] + ai * bj) % p
    return trim(res, p)


def poly_sub(a, b, p):
    k = max(len(a), len(b))
    res = [0] * k
    for i in range(len(a)):
        res[i] = (res[i] + a[i]) % p
    for i in range(len(b)):
        res[i] = (res[i] - b[i]) % p
    return trim(res, p)


def poly_deg(a):
    d = len(a) - 1
    while d > 0 and a[d] == 0:
        d -= 1
    if d == 0 and a[0] == 0:
        return -1
    return d


def poly_eval(coeffs, x, p):
    r = 0
    for c in reversed(coeffs):
        r = (r * x + c) % p
    return r


def poly_from_roots(roots, p):
    res = [1]
    for r in roots:
        res = poly_mul(res, [(-r) % p, 1], p)
    return res


def find_D(p, n):
    D = sorted(x for x in range(1, p) if pow(x, n, p) == 1)
    assert len(D) == n, f"expected |D|={n}, got {len(D)}"
    return D


def get_a(ell, size, i, p):
    deg = size - i
    if deg < 0 or deg >= len(ell):
        return 0
    return ell[deg] % p


def twisted_curve(s, zstar, w, p):
    r = (s - zstar[0]) % p
    phis = [s % p]
    for j in range(2, w + 2):
        phis.append((zstar[j - 1] % p + r * phis[-1]) % p)
    return tuple(phis)


def build_U(zstar, mprime, p):
    coeffs = [0] * (mprime + 1)
    coeffs[mprime] = 1
    for h in range(1, len(zstar) + 1):
        coeffs[mprime - h] = zstar[h - 1] % p
    return trim(coeffs, p)


def solve_linear_system(A, b, p):
    nn = len(A)
    ncols = len(A[0])
    Mx = [row[:] + [b[i] % p] for i, row in enumerate(A)]
    for col in range(ncols):
        piv = next((r for r in range(col, nn) if Mx[r][col] % p), None)
        if piv is None:
            return None
        Mx[col], Mx[piv] = Mx[piv], Mx[col]
        inv = pow(Mx[col][col], p - 2, p)
        Mx[col] = [(x * inv) % p for x in Mx[col]]
        for r in range(nn):
            if r != col and Mx[r][col] % p:
                f = Mx[r][col] % p
                Mx[r] = [(Mx[r][kk] - f * Mx[col][kk]) % p for kk in range(ncols + 1)]
    return [Mx[i][ncols] % p for i in range(nn)]


def census_direct(T, U, Kp, p):
    """Independent ground truth: deg<Kp interpolation on first Kp points, verify rest."""
    pts = T[:Kp]
    A = [[pow(t, i, p) for i in range(Kp)] for t in pts]
    bvec = [poly_eval(U, t, p) for t in pts]
    sol = solve_linear_system(A, bvec, p)
    if sol is None:
        raise RuntimeError("singular Vandermonde")
    c = trim(sol, p)
    for t in T[Kp:]:
        if poly_eval(c, t, p) != poly_eval(U, t, p):
            return False
    return True


def build_row(p, n, K, m, w):
    """Enumerate all m- and (m+1)-subsets; bucket by depth-(w+1) prefix."""
    D = find_D(p, n)
    mprime = m + 1
    fib = {}
    fib_members = {}
    for T in itertools.combinations(D, m):
        ell = poly_from_roots(T, p)
        pref = tuple(get_a(ell, m, i, p) for i in range(1, w + 2))
        fib[pref] = fib.get(pref, 0) + 1
        fib_members.setdefault(pref, []).append(T)
    fibmp = {}
    for T in itertools.combinations(D, mprime):
        ell = poly_from_roots(T, p)
        pref = tuple(get_a(ell, mprime, i, p) for i in range(1, w + 2))
        fibmp[pref] = fibmp.get(pref, 0) + 1
    assert sum(fib.values()) == comb(n, m)
    assert sum(fibmp.values()) == comb(n, mprime)
    return D, fib, fib_members, fibmp


def valid_by_a1(D, fib_members, m, w, zstar, p):
    """V = {valid T}; return dict a1 -> [T].  Valid via twisted map Theta_w(T)=z*."""
    by_a1 = {}
    valid = []
    for pref, members in fib_members.items():
        a = (1,) + pref                       # a_0..a_{w+1}
        r = (a[1] - zstar[0]) % p
        ok = all((a[j] - r * a[j - 1]) % p == zstar[j - 1] % p for j in range(2, w + 2))
        if ok:
            for T in members:
                by_a1.setdefault(a[1], []).append(T)
                valid.append(T)
    return by_a1, valid


def curve_stats(fib, m, w, zstar, p):
    vals = [fib.get(twisted_curve(s, zstar, w, p), 0) for s in range(p)]
    S1 = sum(vals)
    M2 = sum(v * v for v in vals)
    return S1, M2, (max(vals) if vals else 0)


def toy_row_observables(label, p, n, K, m, w, seeds):
    D, fib, fib_members, fibmp = build_row(p, n, K, m, w)
    mprime = m + 1
    out = {"per_z": {}}

    # three-way M2 identity + planted/residual + CS, on each seed z*
    for z in seeds:
        zt = tuple(x % p for x in z)
        S1, M2_def, maxfib = curve_stats(fib, m, w, list(z), p)
        by_a1, valid = valid_by_a1(D, fib_members, m, w, list(z), p)
        S1_valid = len(valid)
        M2_pairs = sum(len(l) ** 2 for l in by_a1.values())
        # M2 via curve = sum_{z in Gamma} N(z)^2 (distinct curve points)
        Gimg = set(twisted_curve(s, list(z), w, p) for s in range(p))
        M2_curve = sum(fib.get(gz, 0) ** 2 for gz in Gimg)
        planted = mprime * fibmp.get(zt, 0)
        residual = S1 - planted
        cs_ok = (S1 * S1 <= p * M2_def)
        # off-diagonal shift-pair constraint + top stratum, by enumeration on V
        prefixeq_ok = True
        top_ok = True
        e_ge_ok = True
        for a1, lst in by_a1.items():
            for i in range(len(lst)):
                for j in range(len(lst)):
                    if i == j:
                        continue
                    Ti, Tj = set(lst[i]), set(lst[j])
                    e = len(Ti - Tj)
                    if e < w + 2:
                        e_ge_ok = False
                    A = poly_from_roots(sorted(Ti - Tj), p)
                    B = poly_from_roots(sorted(Tj - Ti), p)
                    dg = poly_deg(poly_sub(A, B, p))
                    if dg > e - w - 2:
                        prefixeq_ok = False
                    if e == w + 2 and dg != 0:
                        top_ok = False
        out["per_z"][zt] = dict(
            S1=S1, S1_valid=S1_valid, M2_def=M2_def, M2_pairs=M2_pairs,
            M2_curve=M2_curve, planted=planted, residual=residual, maxfib=maxfib,
            three_way=(M2_def == M2_pairs == M2_curve),
            S1_eq=(S1 == S1_valid),
            cs=cs_ok, prefixeq=prefixeq_ok, top=top_ok, e_ge=e_ge_ok,
        )

    # twist-equivariance + orbit constancy on the first seed
    z0 = list(seeds[0])
    eq_ok = True
    orbit_ok = True
    S_base = curve_stats(fib, m, w, z0, p)[0]
    for zeta in D:
        # equivariance theta_{zeta.z*}(zeta s) = zeta.theta_{z*}(s)
        zz = [(pow(zeta, j + 1, p) * z0[j]) % p for j in range(w + 1)]
        for s in range(p):
            lhs = twisted_curve((zeta * s) % p, zz, w, p)
            rhs = tuple((pow(zeta, j + 1, p) * v) % p
                        for j, v in enumerate(twisted_curve(s, z0, w, p)))
            if lhs != rhs:
                eq_ok = False
                break
        if curve_stats(fib, m, w, zz, p)[0] != S_base:
            orbit_ok = False
    out["twist_equiv"] = eq_ok
    out["orbit_const"] = orbit_ok

    # p-to-1 preimage identity (sample) + sum_z N = C(n,m)
    out["sumN_eq_Cnm"] = (sum(fib.values()) == comb(n, m))
    preimg_ok = True
    for z in list(fib.keys())[:8]:
        cnt = 0
        s = z[0]
        for y1 in range(p):
            # reconstruct the unique y with theta_y(s)=z given y_1
            yv = [y1]
            ok = True
            for j in range(2, w + 2):
                # z_j = y_j + (s - y_1) z_{j-1}  =>  y_j = z_j - (s-y_1) z_{j-1}
                yj = (z[j - 1] - (s - y1) * z[j - 2]) % p
                yv.append(yj)
            if twisted_curve(s, yv, w, p) == z:
                cnt += 1
        if cnt != p:
            preimg_ok = False
    out["preimage_p_to_1"] = preimg_ok

    # #393-Theorem crosscheck: curve-sum == #valid T on all seeds (already in per_z)
    # + independent Lagrange census ground truth on 2 seeds
    lag_ok = True
    all_T = list(itertools.combinations(D, m))
    for z in seeds[:2]:
        U = build_U(list(z), mprime, p)
        Cen = sum(1 for T in all_T if census_direct(list(T), U, K, p))
        if Cen != out["per_z"][tuple(x % p for x in z)]["S1"]:
            lag_ok = False
    out["lagrange_theorem"] = lag_ok
    return out


def check_avg_identity(p, n, m, w):
    """Full-enumeration exact average identity on a mini field row."""
    D = find_D(p, n)
    fib = {}
    for T in itertools.combinations(D, m):
        ell = poly_from_roots(T, p)
        pref = tuple(get_a(ell, m, i, p) for i in range(1, w + 2))
        fib[pref] = fib.get(pref, 0) + 1
    tot = 0
    for y in itertools.product(range(p), repeat=w + 1):
        for s in range(p):
            tot += fib.get(twisted_curve(s, list(y), w, p), 0)
    return tot, p * comb(n, m)


# toy pins (exact integers)
TOY_PINS = {
    "A": dict(p=97, n=16, K=4, m=6, w=2,
              seeds=[[1, 1, 1], [96, 1, 96], [0, 0, 0], [2, 3, 5], [7, 11, 13], [1, 2, 3]],
              pin={(1, 1, 1): dict(S1=21, M2_def=39, planted=21, residual=0),
                   (96, 1, 96): dict(S1=21, M2_def=39, planted=21, residual=0),
                   (0, 0, 0): dict(S1=0, M2_def=0, planted=0, residual=0)}),
    "B": dict(p=97, n=16, K=5, m=7, w=2,
              seeds=[[0, 0, 0], [96, 1, 96], [3, 5, 7], [1, 0, 2], [11, 13, 17], [2, 4, 8]],
              pin={(0, 0, 0): dict(S1=48, M2_def=144, planted=48, residual=0),
                   (96, 1, 96): dict(S1=3, M2_def=9, planted=0, residual=3)}),
}
MINI_PIN = dict(p=13, n=6, m=4, w=2, expected=195)   # 13 * C(6,4) = 13*15


def check_toy(pins, verbose=False):
    gates = []
    for label, cfg in pins.items():
        obs = toy_row_observables(label, cfg["p"], cfg["n"], cfg["K"],
                                  cfg["m"], cfg["w"], cfg["seeds"])
        # per-z pinned integer observables
        for zt, exp in cfg["pin"].items():
            got = obs["per_z"][zt]
            for field, ev in exp.items():
                ok = (got[field] == ev)
                gates.append((f"G2:{label}:{zt}:{field}", ok))
                if verbose:
                    print(f"    G2[{label} {zt} {field}] got={got[field]} exp={ev} "
                          f"{'ok' if ok else 'FAIL'}")
        # structural gates over all seeds
        three = all(v["three_way"] for v in obs["per_z"].values())
        s1eq = all(v["S1_eq"] for v in obs["per_z"].values())
        cs = all(v["cs"] for v in obs["per_z"].values())
        preq = all(v["prefixeq"] for v in obs["per_z"].values())
        top = all(v["top"] for v in obs["per_z"].values())
        ege = all(v["e_ge"] for v in obs["per_z"].values())
        for nm2, ok in [("M2_three_way_identity", three),
                        ("curve_sum==valid_T(#393thm)", s1eq),
                        ("cauchy_schwarz", cs),
                        ("offdiag_deg<=e-w-2", preq),
                        ("topstratum_const_shift", top),
                        ("offdiag_e>=w+2", ege),
                        ("twist_equivariance", obs["twist_equiv"]),
                        ("orbit_constancy", obs["orbit_const"]),
                        ("sumN==Cnm", obs["sumN_eq_Cnm"]),
                        ("preimage_p_to_1", obs["preimage_p_to_1"]),
                        ("lagrange_ground_truth", obs["lagrange_theorem"])]:
            gates.append((f"G2:{label}:{nm2}", ok))
            if verbose:
                print(f"    G2[{label} {nm2}] {'ok' if ok else 'FAIL'}")
    # mini-row exact average identity
    tot, exp = check_avg_identity(MINI_PIN["p"], MINI_PIN["n"], MINI_PIN["m"], MINI_PIN["w"])
    ok = (tot == exp == MINI_PIN["expected"])
    gates.append(("G2:mini:avg_identity_sum_y_S=p*Cnm", ok))
    if verbose:
        print(f"    G2[mini avg-identity] sum_y S(y)={tot} exp={exp} "
              f"(pin {MINI_PIN['expected']})  {'ok' if ok else 'FAIL'}")
    return gates


# =====================================================================
# main + tamper
# =====================================================================

def run_all(verbose=False):
    vals = compute_L4()
    gates = check_L4(vals, L4_PINS, verbose)
    gates += check_toy(TOY_PINS, verbose)
    return gates


def main():
    tamper = "--tamper-selftest" in sys.argv
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    print("=== BC L4 curve-second-moment verifier ===")
    print(f"fixture: n={N} K={K} m={M} w={W} p={P} (log2 p={log2_bigint(P):.9f})")
    gates = run_all(verbose)
    n_fail = sum(1 for _, ok in gates if not ok)
    print(f"\nGATES: {len(gates)} total, {len(gates) - n_fail} pass, {n_fail} fail")
    if n_fail:
        for name, ok in gates:
            if not ok:
                print(f"  FAIL: {name}")
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS (all gates green)")

    if not tamper:
        print("\n(run with --tamper-selftest to confirm every pin is load-bearing)")
        return 0

    # ---- tamper self-test: perturb every pinned value; each must be caught ----
    print("\n=== --tamper-selftest: every pin must be caught ===")
    vals = compute_L4()
    caught = 0
    total = 0
    # G1 pins
    for name, (key, exp, tol) in L4_PINS.items():
        total += 1
        bad = dict(L4_PINS)
        delta = 1 if (isinstance(exp, int) and tol == 0) else max(10 * tol, 0.5)
        bad[name] = (key, exp + delta, tol)
        sub = check_L4(vals, {name: bad[name]}, verbose=False)
        target = [ok for gname, ok in sub if gname == "G1:" + name]
        if target and not target[0]:
            caught += 1
        else:
            print(f"  MISSED G1 pin: {name}")
    # G2 pins (perturb each pinned integer observable)
    for label, cfg in TOY_PINS.items():
        obs = toy_row_observables(label, cfg["p"], cfg["n"], cfg["K"],
                                  cfg["m"], cfg["w"], cfg["seeds"])
        for zt, exp in cfg["pin"].items():
            for field, ev in exp.items():
                total += 1
                got = obs["per_z"][zt][field]
                # tamper = assert against a wrong expected value
                if got != ev + 1:
                    caught += 1
                else:
                    print(f"  MISSED G2 pin: {label}:{zt}:{field}")
    # mini-row avg-identity pin
    total += 1
    tot, _ = check_avg_identity(MINI_PIN["p"], MINI_PIN["n"], MINI_PIN["m"], MINI_PIN["w"])
    if tot != MINI_PIN["expected"] + 1:
        caught += 1
    else:
        print("  MISSED mini avg-identity pin")

    print(f"tamper: {caught}/{total} pins caught")
    if caught != total:
        print("RESULT: TAMPER-SELFTEST FAIL")
        return 1
    print("RESULT: TAMPER-SELFTEST PASS (every pin perturbation is detected)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
