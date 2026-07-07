#!/usr/bin/env python3
"""Verifier for cap25_v13_bc_l4_interior_chart_to_q.md.

Packet: "BC L4 interior excess-1 chart discharges to depth-(w+1) row-sharp Q."

Two gate groups, all values recomputed exactly (stdlib only, no numpy/sympy):

  G1  Exact L4 big-int table: the heuristic/floor/ceiling logs, M_B(4218),
      packing (Johnson ball recomputed with big-int binomials), anticode,
      K-1, distinct-slope threshold, and the cross-consistency checks against
      the integrated #369 boundary row and the #361 rung-audit value a_4.

  G2  Self-contained toy enumeration at two rows (embedded from scratch, no
      dependence on the Lane B scratchpad): direct deg<K Lagrange/Vandermonde
      census == twisted-equation count; planted<->m'-fiber bijection;
      saturation identity Cen == sum C(rt_D,m); Theorem [interior chart
      decomposition] sum_s |Fib_{w+1}(theta(s))| == Cen; Corollary [discharge]
      inequality Cen <= |B|*max fiber (exact max over all B^{w+1} prefixes);
      collision degree bound == K-1 attained; rigidity min|T\\T'| == w+1
      attained; d1(U)=w+2 by brute module search; line-for-RS[k] == word
      census at a base-field pole; word census subset line-for-RS[K].

Usage:
  verify_bc_l4_interior_chart_to_q.py                 # exit 0 = PASS
  verify_bc_l4_interior_chart_to_q.py --tamper-selftest  # every pin caught

Runtime < 5s.

Cross-referenced integrated files (constants embedded below with their paths):
  #369 fixture: experimental/notes/thresholds/cap25_v13_bc_l4_base_floor_ladder.md
                (boundary row d1=4217: log2 prefix average / base-field floor = 23.139009)
  #361 rung audit: experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md
                (line 216: row_4 = (131072, 69753, 4216), a_4 = 23.139009074)
"""
import sys
import math
import itertools
from math import comb


# --------------------------------------------------------------------------
# exact-ish log2 of an arbitrary positive integer (stdlib only, no overflow)
# --------------------------------------------------------------------------
def log2_bigint(N):
    if N <= 0:
        raise ValueError("log2 of non-positive")
    b = N.bit_length()
    if b <= 53:
        return math.log2(N)
    shift = b - 53
    return math.log2(N >> shift) + shift


def approx(a, b, tol=5e-6):
    return abs(a - b) <= tol


# ==========================================================================
# G1 : exact L4 big-int table
# ==========================================================================
# L4 fixture (scale-16 KoalaBear-MCA quotient row; #369).
N_L4  = 131072            # n = 2^17
K_L4  = 65537             # = 2^16 + 1  (MCA threshold = k+1)
M_L4  = 69753             # agreement (odd)
W_L4  = M_L4 - K_L4       # 4216
P_L4  = 2**31 - 2**24 + 1 # KoalaBear prime = |B|
D1_L4 = W_L4 + 2          # 4218  (first interior profile)
MP_L4 = K_L4 - 1 + D1_L4  # m' = 69754 = m+1
Q_L4  = P_L4**6           # |F|

# Pinned expectations (rounded values as they appear in the note / sources).
PINS_L4 = {
    "log2_p":              30.988684687,
    "log2_Cnm":            130671.433651,
    "heuristic":           23.139009,      # C(n,m)/p^w
    "planted_density":     -8.035617,      # C(n,m')/p^(d1-1)
    "M_B_4218":            69754,          # exact int
    "Km1":                 65536,          # exact int
    "packing_fullball":    103810.24,      # C(n,m)/V_t, t=floor(w/2)
    "packing_oneterm":     103810.24,      # C(n,m)/[C(m,t)C(n-m,t)]
    "anticode":            108108.04,      # C(n,m)/C(n-m+w,w)
    "reduce_pack":         103841.23,      # |B|*C(n,m)/V_t' (depth w+1 route)
    "distinct_slope_thr":  169.93,         # (q-p)/(K-1)+1
    "ray_floor":           7.05,           # heuristic - log2(m+1)
    "slope_floor":         6.05,           # ray_floor - 1
    "gap_pack":            103787.10,      # packing - heuristic
    "collisions_at_N":     -124.65,        # C(N,2)(K-1)/(q-p) at N=heuristic
    # cross-consistency embeds (do NOT re-pin; assert equal to heuristic):
    "rung_a4_361":         23.139009074,   # #361 rung audit, row_4, line 216
    "boundary_369":        23.139009,      # #369 boundary row d1=4217
}


def compute_L4(pins):
    """Recompute the whole L4 table from scratch with big-int binomials."""
    n, K, m, w, p, d1, mp = N_L4, K_L4, M_L4, W_L4, P_L4, D1_L4, MP_L4
    nm = n - m
    lp = log2_bigint(p)
    Cnm = comb(n, m)
    Cnmp = comb(n, mp)
    l2_Cnm = log2_bigint(Cnm)

    heuristic = l2_Cnm - w * lp
    planted_density = log2_bigint(Cnmp) - (d1 - 1) * lp
    M_B = comb(mp, m) * 1                     # C(m',m)*ceil(density<1)=m+1
    Km1 = K - 1

    # Johnson ball V_t recomputed EXACTLY with big-int binomials, incrementally.
    t = w // 2
    cm = 1     # C(m,i)
    cnm = 1    # C(nm,i)
    Vt = 1     # sum_{i=0}^{t} C(m,i)C(nm,i)
    top = 1    # last term C(m,t)C(nm,t)
    for i in range(1, t + 1):
        cm = cm * (m - i + 1) // i
        cnm = cnm * (nm - i + 1) // i
        top = cm * cnm
        Vt += top
    packing_fullball = l2_Cnm - log2_bigint(Vt)
    packing_oneterm = l2_Cnm - log2_bigint(top)
    anticode = l2_Cnm - log2_bigint(comb(nm + w, w))

    # depth-(w+1) reduction + packing at t' = floor((w+1)/2) (= t since w even)
    tp = (w + 1) // 2
    cm2 = 1
    cnm2 = 1
    Vtp = 1
    for i in range(1, tp + 1):
        cm2 = cm2 * (m - i + 1) // i
        cnm2 = cnm2 * (nm - i + 1) // i
        Vtp += cm2 * cnm2
    reduce_pack = lp + l2_Cnm - log2_bigint(Vtp)

    distinct_slope_thr = log2_bigint((Q_L4 - p) // Km1 + 1)
    ray_floor = heuristic - log2_bigint(m + 1)
    slope_floor = ray_floor - 1.0
    gap_pack = packing_oneterm - heuristic
    # E[colliding pairs] at N = 2^heuristic: log2( 0.5 * N^2 * (K-1) / (q-p) )
    collisions_at_N = math.log2(0.5) + 2 * heuristic + math.log2(Km1) - log2_bigint(Q_L4 - p)

    return {
        "log2_p": lp,
        "log2_Cnm": l2_Cnm,
        "heuristic": heuristic,
        "planted_density": planted_density,
        "M_B_4218": M_B,
        "Km1": Km1,
        "packing_fullball": packing_fullball,
        "packing_oneterm": packing_oneterm,
        "anticode": anticode,
        "reduce_pack": reduce_pack,
        "distinct_slope_thr": distinct_slope_thr,
        "ray_floor": ray_floor,
        "slope_floor": slope_floor,
        "gap_pack": gap_pack,
        "collisions_at_N": collisions_at_N,
        # raw big ints for structural asserts
        "_Vt": Vt, "_top": top, "_t": t,
    }


def check_L4(pins, verbose=False):
    """Return list of (gate_name, ok) for the L4 table under `pins`."""
    V = compute_L4(pins)
    gates = []

    def g(name, ok):
        gates.append((name, bool(ok)))
        if verbose:
            print(f"    G1[{name}]: {'ok' if ok else 'FAIL'}")

    # exact integers
    g("M_B_4218 == pin",        V["M_B_4218"] == pins["M_B_4218"])
    g("M_B_4218 == m+1",        V["M_B_4218"] == M_L4 + 1)
    g("Km1 == pin",             V["Km1"] == pins["Km1"])
    g("Km1 == K-1",             V["Km1"] == K_L4 - 1)
    # float logs vs pins
    for key, tol in [("log2_p", 1e-6), ("log2_Cnm", 1e-4), ("heuristic", 5e-6),
                     ("planted_density", 5e-6), ("packing_fullball", 5e-3),
                     ("packing_oneterm", 5e-3), ("anticode", 5e-3),
                     ("reduce_pack", 5e-3), ("distinct_slope_thr", 5e-3),
                     ("ray_floor", 5e-3), ("slope_floor", 5e-3),
                     ("gap_pack", 5e-2), ("collisions_at_N", 5e-2)]:
        g(f"{key} == pin", approx(V[key], pins[key], tol))
    # structural: full-ball and one-term packing coincide (V_t top-term dominated)
    g("packing full==one-term (<0.01)", abs(V["packing_fullball"] - V["packing_oneterm"]) < 0.01)
    # structural: reduction route is ~log2 p worse than direct packing
    g("reduce - direct ~ log2 p", approx(V["reduce_pack"] - V["packing_oneterm"], V["log2_p"], 1e-2))
    # structural: direct packing beats anticode
    g("packing < anticode", V["packing_oneterm"] < V["anticode"])
    # structural: gap = packing - heuristic
    g("gap == packing - heuristic", approx(V["gap_pack"], V["packing_oneterm"] - V["heuristic"], 1e-2))
    # CROSS-CONSISTENCY: heuristic == a_4 (#361) == boundary (#369)
    g("heuristic == rung a_4 (#361)", approx(V["heuristic"], pins["rung_a4_361"], 1e-6))
    g("heuristic == boundary (#369)", approx(V["heuristic"], pins["boundary_369"], 5e-6))
    g("rung_a4 pin == boundary pin (self)", approx(pins["rung_a4_361"], pins["boundary_369"], 1e-6))
    # planted density < 0 (so ceil floor = 1)
    g("planted density < 0", V["planted_density"] < 0)
    return gates


# ==========================================================================
# G2 : self-contained toy enumeration (embedded; no scratchpad dependence)
# ==========================================================================
def modinv(a, p):
    return pow(a % p, p - 2, p)


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
    n = max(len(a), len(b))
    res = [0] * n
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


def poly_divmod(a, b, p):
    a = [c % p for c in a]
    b = [c % p for c in b]
    dega, degb = poly_deg(a), poly_deg(b)
    if dega < degb:
        return [0], trim(a, p)
    inv = modinv(b[degb], p)
    a = a[:]
    quot = [0] * (dega - degb + 1)
    for i in range(dega - degb, -1, -1):
        coef = (a[i + degb] * inv) % p
        quot[i] = coef
        if coef:
            for j in range(degb + 1):
                a[i + j] = (a[i + j] - coef * b[j]) % p
    rem = trim(a[:degb] if degb > 0 else [a[0] if a else 0], p)
    return trim(quot, p), rem


def solve_linear_system(A, b, p):
    n = len(A)
    ncols = len(A[0])
    M = [row[:] + [b[i] % p] for i, row in enumerate(A)]
    for col in range(ncols):
        piv = next((r for r in range(col, n) if M[r][col] % p), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        inv = modinv(M[col][col], p)
        M[col] = [(x * inv) % p for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] % p:
                f = M[r][col] % p
                M[r] = [(M[r][k] - f * M[col][k]) % p for k in range(ncols + 1)]
    return [M[i][ncols] % p for i in range(n)]


def matrix_has_kernel(rows, ncols, p):
    """True iff the linear map with these rows has a nonzero kernel vector."""
    M = [row[:] for row in rows]
    nrows = len(M)
    r = 0
    for col in range(ncols):
        piv = next((i for i in range(r, nrows) if M[i][col] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = modinv(M[r][col], p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(nrows):
            if i != r and M[i][col] % p:
                f = M[i][col] % p
                M[i] = [(M[i][k] - f * M[r][k]) % p for k in range(ncols)]
        r += 1
        if r == nrows:
            break
    return r < ncols   # rank deficient => nonzero kernel


def find_D(p, n):
    D = sorted(x for x in range(1, p) if pow(x, n, p) == 1)
    assert len(D) == n, f"expected |D|={n}, got {len(D)}"
    return D


def build_U(zstar, mprime, p):
    coeffs = [0] * (mprime + 1)
    coeffs[mprime] = 1
    for h in range(1, len(zstar) + 1):
        coeffs[mprime - h] = zstar[h - 1] % p
    return trim(coeffs, p)


def census_direct(T, U, K, p):
    """Ground-truth deg<K interpolation on first K points, verify the rest."""
    pts = T[:K]
    A = [[pow(t, i, p) for i in range(K)] for t in pts]
    bvec = [poly_eval(U, t, p) for t in pts]
    sol = solve_linear_system(A, bvec, p)
    if sol is None:
        raise RuntimeError("singular Vandermonde (should not happen)")
    c = trim(sol, p)
    for t in T[K:]:
        if poly_eval(c, t, p) != poly_eval(U, t, p):
            return None
    return c


def pole_line_support(T, U, Kp, alpha, p):
    """Exists (zeta, P) deg P < Kp with U(t)-zeta = (t-alpha)P(t) on T?"""
    Kp1 = Kp + 1
    pts = T[:Kp1]
    A, bvec = [], []
    for t in pts:
        tma = (t - alpha) % p
        A.append([1] + [(tma * pow(t, i, p)) % p for i in range(Kp)])
        bvec.append(poly_eval(U, t, p))
    sol = solve_linear_system(A, bvec, p)
    if sol is None:
        raise RuntimeError("singular pole system (should not happen)")
    zeta = sol[0] % p
    P = trim(sol[1:], p)
    for t in T[Kp1:]:
        if (zeta + (t - alpha) * poly_eval(P, t, p)) % p != poly_eval(U, t, p):
            return None
    return zeta, P


def get_a(ell, m, i, p):
    deg = m - i
    if deg < 0 or deg >= len(ell):
        return 0
    return ell[deg] % p


def twisted_valid_and_r(ell, m, w, zstar, p):
    a = [get_a(ell, m, i, p) for i in range(w + 2)]
    r = (a[1] - zstar[0]) % p
    ok = all((a[j] - r * a[j - 1]) % p == zstar[j - 1] % p for j in range(2, w + 2))
    return ok, r, a


def twisted_curve(s, zstar, w, p):
    """theta(s) = (phi_1,...,phi_{w+1}); phi_1=s, phi_j=z*_j+(s-z*_1)phi_{j-1}."""
    r = (s - zstar[0]) % p
    phis = [s % p]
    for j in range(2, w + 2):
        phis.append((zstar[j - 1] % p + r * phis[-1]) % p)
    return tuple(phis)


def module_d1(U, K, n, beta, p, dmax):
    """Smallest d with nonzero (W,N): deg W<=d, deg N<=d+K-1, W*U=N on D
    (i.e. (W*U mod X^n-beta) - N == 0). Brute kernel search."""
    for d in range(dmax + 1):
        ncols = (d + 1) + (d + K)
        columns = []
        for i in range(d + 1):
            prod = poly_mul([0] * i + [1], U, p)
            red = [c % p for c in prod]
            while len(red) > n:
                topc = red.pop()
                if topc:
                    shift = len(red) - n
                    while len(red) <= shift:
                        red.append(0)
                    red[shift] = (red[shift] + topc * beta) % p
            vec = [0] * n
            for idx in range(min(len(red), n)):
                vec[idx] = red[idx] % p
            columns.append(vec)
        for j in range(d + K):
            vec = [0] * n
            vec[j] = (-1) % p
            columns.append(vec)
        rows = [[columns[c][r] for c in range(ncols)] for r in range(n)]
        if matrix_has_kernel(rows, ncols, p):
            return d
    return None


def toy_run(p, n, K, m, w, d1, mprime, zstar, alpha=5):
    """Full self-contained toy pass. Returns the gate observables."""
    D = find_D(p, n)
    Dset = set(D)
    U = build_U(zstar, mprime, p)

    valid_T = []
    rays = {}                # S_Psi -> {'Psi':.., 'members':[T,...]}
    m_fiber = {}             # (a_1..a_{w+1}) -> [T,...]   (ALL m-subsets)
    stratum = {"planted": 0, "primitive": 0, "degenerate": 0}
    census_vs_twisted_mismatch = 0
    factor_mismatch = 0

    for T in itertools.combinations(D, m):
        T = list(T)
        ell = poly_from_roots(T, p)
        ok_tw, r, a = twisted_valid_and_r(ell, m, w, zstar, p)
        m_fiber.setdefault(tuple(a[1:w + 2]), []).append(tuple(T))

        c = census_direct(T, U, K, p)
        ok_dir = c is not None
        if ok_tw != ok_dir:
            census_vs_twisted_mismatch += 1
            continue
        if not ok_tw:
            continue

        # derive Psi from the independent interpolant c, factor to get r, compare
        Psi = poly_sub(U, c, p)
        quo, rem = poly_divmod(Psi, ell, p)
        rem_zero = (poly_deg(rem) == -1) or (rem == [0])
        r_from_c = (-quo[0]) % p if (rem_zero and poly_deg(quo) == 1 and quo[1] % p == 1) else None
        if r_from_c is None or r_from_c != r % p:
            factor_mismatch += 1
        Psi_closed = poly_mul(ell, [(-r) % p, 1], p)
        if Psi_closed != Psi:
            factor_mismatch += 1

        S_Psi = tuple(sorted(x for x in D if poly_eval(Psi, x, p) == 0))
        if r in Dset and r not in set(T):
            stratum["planted"] += 1
        elif r not in Dset:
            stratum["primitive"] += 1
        else:
            stratum["degenerate"] += 1

        valid_T.append({"T": tuple(T), "a1": a[1], "S_Psi": S_Psi})
        rays.setdefault(S_Psi, {"Psi": Psi, "members": []})["members"].append(tuple(T))

    Cen = len(valid_T)
    keys = list(rays.keys())

    # Theorem: sum_s |Fib_{w+1}(theta(s))| == Cen
    sum_fib = sum(len(m_fiber.get(twisted_curve(s, zstar, w, p), [])) for s in range(p))

    # Corollary: exact max fiber over ALL depth-(w+1) prefixes
    max_fiber = max(len(v) for v in m_fiber.values())

    # saturation: Cen == sum_ray C(|S_Psi|, m)
    sat_sum = sum(comb(len(k), m) for k in keys)
    per_ray_membership_ok = True
    for k in keys:
        want = set(tuple(sorted(c)) for c in itertools.combinations(k, m))
        got = set(rays[k]["members"])
        if want != got:
            per_ray_membership_ok = False

    # rigidity: min |T\T'| over ray-representative pairs
    min_sep = None
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            sep = len(set(rays[keys[i]]["members"][0]) - set(rays[keys[j]]["members"][0]))
            if min_sep is None or sep < min_sep:
                min_sep = sep

    # collision: max deg(Psi-Psi') and max base-field-pole collision count
    max_deg = -1
    max_coll = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            diff = poly_sub(rays[keys[i]]["Psi"], rays[keys[j]]["Psi"], p)
            max_deg = max(max_deg, poly_deg(diff))
            cnt = sum(1 for x in range(p) if x not in Dset and poly_eval(diff, x, p) == 0)
            max_coll = max(max_coll, cnt)

    # module d1(U) by brute search
    d1_found = module_d1(U, K, n, 1, p, dmax=w + 4)

    # planted bijection: rays of size m+1 == m'-fiber at prefix z*
    mp_fiber = {}
    for Mp in itertools.combinations(D, mprime):
        ellmp = poly_from_roots(Mp, p)
        key = tuple(ellmp[mprime - h] % p for h in range(1, d1))
        mp_fiber.setdefault(key, []).append(tuple(sorted(Mp)))
    raw_fib = set(mp_fiber.get(tuple(zstar), []))
    planted_rays = set(k for k in keys if len(k) == mprime)

    # convention: line-for-RS[k] (deg quotient < K-1) == word census at pole alpha
    census_T = set(e["T"] for e in valid_T)
    line_k = set(tuple(T) for T in itertools.combinations(D, m)
                 if pole_line_support(list(T), U, K - 1, alpha, p) is not None)
    # convention pin: word census subset of line-for-RS[K] (deg quotient < K)
    line_K = set(tuple(T) for T in itertools.combinations(D, m)
                 if pole_line_support(list(T), U, K, alpha, p) is not None)

    return {
        "Cen": Cen,
        "rays": len(keys),
        "census_vs_twisted_mismatch": census_vs_twisted_mismatch,
        "factor_mismatch": factor_mismatch,
        "sum_fib": sum_fib,
        "max_fiber": max_fiber,
        "sat_sum": sat_sum,
        "per_ray_membership_ok": per_ray_membership_ok,
        "min_sep": min_sep,
        "max_deg": max_deg,
        "max_coll": max_coll,
        "d1_found": d1_found,
        "planted_rays": len(planted_rays),
        "raw_fib": len(raw_fib),
        "planted_bijection": (planted_rays == raw_fib),
        "stratum": stratum,
        "line_k_size": len(line_k),
        "census_size": len(census_T),
        "line_k_eq_census": (line_k == census_T),
        "line_K_size": len(line_K),
        "census_subset_line_K": census_T.issubset(line_K),
    }


# toy rows and their pinned expectations (from toy2 results.json, ALL-GREEN 60/60)
TOY_ROWS = {
    "A": dict(p=97, n=16, K=4, m=6, w=2, d1=4, mprime=7, zstar=[96, 1, 96]),
    "B": dict(p=97, n=16, K=5, m=7, w=2, d1=4, mprime=8, zstar=[0, 0, 0]),
}
PINS_TOY = {
    "A": dict(Cen=21, rays=3, sum_fib=21, max_fiber=3, min_sep=3, max_deg=3,
              max_coll=0, d1_found=4, planted_rays=3, raw_fib=3, line_k_size=21,
              census_size=21, line_K_size=105, stratum_planted=21),
    "B": dict(Cen=48, rays=6, sum_fib=48, max_fiber=3, min_sep=3, max_deg=4,
              max_coll=1, d1_found=4, planted_rays=6, raw_fib=6, line_k_size=48,
              census_size=48, line_K_size=144, stratum_planted=48),
}


_TOY_CACHE = {}


def toy_observables(row_label):
    """toy_run() depends only on the row config (not on pinned expectations),
    so cache it; the tamper self-test perturbs pins, not the enumeration."""
    if row_label not in _TOY_CACHE:
        _TOY_CACHE[row_label] = toy_run(**TOY_ROWS[row_label])
    return _TOY_CACHE[row_label]


def check_toy(row_label, pins, verbose=False):
    """Return list of (gate_name, ok) for a toy row under pinned expectations."""
    cfg = TOY_ROWS[row_label]
    V = toy_observables(row_label)
    K, w = cfg["K"], cfg["w"]
    gates = []

    def g(name, ok):
        gates.append((f"{row_label}:{name}", bool(ok)))
        if verbose:
            print(f"    G2[{row_label}:{name}]: {'ok' if ok else 'FAIL'}")

    # census correctness (direct Lagrange == twisted equation count)
    g("census twisted==direct (0 mismatch)", V["census_vs_twisted_mismatch"] == 0)
    g("Psi factor r==a1-z*1 (0 mismatch)", V["factor_mismatch"] == 0)
    g("Cen == pin", V["Cen"] == pins["Cen"])
    g("rays == pin", V["rays"] == pins["rays"])
    # Theorem [interior chart decomposition]
    g("sum_fib == pin", V["sum_fib"] == pins["sum_fib"])
    g("Theorem: sum_fib == Cen", V["sum_fib"] == V["Cen"])
    # Corollary [discharge]  Cen <= |B|*max_fiber, exact max over all prefixes
    g("max_fiber == pin", V["max_fiber"] == pins["max_fiber"])
    g("Corollary: rays<=Cen<=p*maxfiber",
      V["rays"] <= V["Cen"] <= cfg["p"] * V["max_fiber"])
    # saturation identity
    g("sat_sum == pin", V["sat_sum"] == pins["Cen"])
    g("saturation: Cen == sum C(rt,m)", V["Cen"] == V["sat_sum"])
    g("per-ray membership exact", V["per_ray_membership_ok"])
    # rigidity  min|T\T'| == w+1
    g("min_sep == pin", V["min_sep"] == pins["min_sep"])
    g("rigidity: min_sep == w+1", V["min_sep"] == w + 1)
    # collision degree bound == K-1 attained
    g("max_deg == pin", V["max_deg"] == pins["max_deg"])
    g("collision: max_deg == K-1", V["max_deg"] == K - 1)
    g("max_coll == pin", V["max_coll"] == pins["max_coll"])
    g("collision count <= K-1", V["max_coll"] <= K - 1)
    # module d1(U) == w+2
    g("d1_found == pin", V["d1_found"] == pins["d1_found"])
    g("module: d1(U) == w+2", V["d1_found"] == w + 2)
    # planted bijection
    g("planted_rays == pin", V["planted_rays"] == pins["planted_rays"])
    g("raw_fib == pin", V["raw_fib"] == pins["raw_fib"])
    g("planted <-> m'-fiber bijection", V["planted_bijection"])
    g("all rays planted (stratum)", V["stratum"]["planted"] == pins["stratum_planted"])
    # convention: line-for-RS[k] == word census
    g("line_k_size == pin", V["line_k_size"] == pins["line_k_size"])
    g("census_size == pin", V["census_size"] == pins["census_size"])
    g("line-for-RS[k] == word census", V["line_k_eq_census"])
    # convention pin: word census subset line-for-RS[K]
    g("line_K_size == pin", V["line_K_size"] == pins["line_K_size"])
    g("census subset line-for-RS[K]", V["census_subset_line_K"])
    g("line-for-RS[K] strictly larger", V["line_K_size"] > V["census_size"])
    return gates


# ==========================================================================
# driver
# ==========================================================================
def run_all(pins_L4, pins_toy, verbose=False):
    all_gates = []
    all_gates += [("G1:" + n, ok) for (n, ok) in check_L4(pins_L4, verbose)]
    for row in ("A", "B"):
        all_gates += [("G2:" + n, ok) for (n, ok) in check_toy(row, pins_toy[row], verbose)]
    return all_gates


def main():
    tamper = "--tamper-selftest" in sys.argv
    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    print("=== BC L4 interior-chart-to-Q verifier ===")
    print(f"fixture: n={N_L4} K={K_L4} m={M_L4} w={W_L4} d1={D1_L4} m'={MP_L4} "
          f"p=2^31-2^24+1  (excess e=1)")

    gates = run_all(PINS_L4, PINS_TOY, verbose=verbose)
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
        return 0

    # ---- tamper self-test: perturb every pinned integer + toy expectation ----
    print("\n=== --tamper-selftest: every pin must be caught ===")
    caught = 0
    missed = []

    def perturb(v):
        if isinstance(v, bool):
            return (not v)
        if isinstance(v, int):
            return v + 1
        return v + 1.0        # push floats well outside tolerance

    # L4 pins
    for key in PINS_L4:
        bad = dict(PINS_L4)
        bad[key] = perturb(bad[key])
        g = check_L4(bad)
        if any(not ok for _, ok in g):
            caught += 1
        else:
            missed.append(f"L4:{key}")

    # toy pins
    for row in ("A", "B"):
        for key in PINS_TOY[row]:
            bad = {r: dict(PINS_TOY[r]) for r in PINS_TOY}
            bad[row][key] = perturb(bad[row][key])
            g = check_toy(row, bad[row])
            if any(not ok for _, ok in g):
                caught += 1
            else:
                missed.append(f"toy[{row}]:{key}")

    total = len(PINS_L4) + sum(len(PINS_TOY[r]) for r in PINS_TOY)
    print(f"tamper: {caught}/{total} pins caught")
    if missed:
        print("  MISSED (perturbation not detected):")
        for mm in missed:
            print(f"    {mm}")
        print("RESULT: TAMPER-SELFTEST FAIL")
        return 1
    print("RESULT: TAMPER-SELFTEST PASS (every pin perturbation is detected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
