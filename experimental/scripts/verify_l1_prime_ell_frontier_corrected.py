#!/usr/bin/env python3
"""verify_l1_prime_ell_frontier_corrected.py

Zero-arg, stdlib-only, deterministic verifier for the CORRECTED prime-`ell` listing
frontier at the onset `m = t+1`:

      m*(ell) = (ell+3)/2      (REFUTES the conjectured  m0 = ceil(2ell/3)  of
      experimental/notes/l1/l1_prime_ell_pv_refutation.md sec 4, L164-165).

Seven gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)   witness spectra recomputed from stored gamma by TWO independent spectrum
        implementations (generator-coset power-sum vs x^ell-grouping Horner), matched
        to the claimed top-m >= 2ell.
  (ii)  the PROVED elementary bound  top-m <= 2m + E_3  (and the sharper
        top-m <= m + min(m,a) + E_3), tight-saturated by the ell=11 witness.
  (iii) the PROVED rank formula  rank = (P-K) - delta,  realizable iff rank <= ell-2
        (dim Z = (P-ell)_+ full-Vandermonde convention; see note sec).  Configs include
        rank==ell-2 (boundary-realizable), rank==ell-1 (boundary-non-realizable) and
        delta>0 cases so BOTH the (P-K)-delta identity AND the `ell-2` threshold constant
        are load-bearing (a wrong threshold, e.g. ell-3, fails the rank==ell-2 configs).
  (iv)  the KEY LEMMA (NUMERIC)  E_3 <= ell-2,  solve-based bounded seeded sweep
        + saturation by the shipped p=331/p=313 witnesses (E_3 = ell-2 exactly),
        saturated by the concentrated Gamma.
  (v)   the geometric / concentrated Gamma is a NON-LISTER: spectrum [ell-1,1,..,1],
        top-m = ell+m-2 < 2ell for every m<=ell-1.
  (vi)  LAMBDA-FREENESS + full-codeword chain (ported from the #260 V1 machinery
        d1_v1_witness_check.py) for each frontier witness: the modal level targets are
        hit by DISTINCT NONZERO petal scalars (Lemma LF, surjective rank m), an explicit
        P (deg <= m*ell) retains R = top-m >= 2ell on the core, agrees on all t*ell petal
        points, and its missed core is a MINIMAL, PRIMITIVE (mixed) kernel set.
  (vii) NEGATIVE CONTROL guarding the refutation: the conjecture predicts vacancy at
        m = (ell+3)/2 (since (ell+3)/2 < ceil(2ell/3) for ell in {11,13}); the witness
        LISTS there, contradicting it.

Hidden self-test:  python3 verify_...py --tamper-selftest
    flips one datum per gate class and asserts each gate then FAILS (proves every gate
    has teeth); gate (iii) flips the rank-identity offset AND the realizability threshold
    INDEPENDENTLY, requiring BOTH to be caught.  The shipped default is zero-arg.

All arithmetic is exact over F_p, stdlib only.  No network, no files, no args.
"""
import sys
import time

# =====================================================================================
# exact F_p arithmetic  (self-contained)
# =====================================================================================
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def inv(a, p):
    return pow(a % p, p - 2, p)

def pmul(a, b, p):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] = (out[i + j] + ai * bj) % p
    while out and out[-1] == 0:
        out.pop()
    return out

def padd(a, b, p):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(len(a)):
        out[i] = a[i] % p
    for i in range(len(b)):
        out[i] = (out[i] + b[i]) % p
    while out and out[-1] == 0:
        out.pop()
    return out

def peval(c, x, p):
    v = 0
    for co in reversed(c):
        v = (v * x + co) % p
    return v

def poly_from_roots(rs, p):
    out = [1]
    for r in rs:
        out = pmul(out, [(-r) % p, 1], p)
    return out

def substitute_xk(c, k):
    if not c:
        return []
    out = [0] * ((len(c) - 1) * k + 1)
    for i, co in enumerate(c):
        out[i * k] = co
    return out

def lagrange_interp(xs, ys, p):
    res = []
    n = len(xs)
    for j in range(n):
        num = [1]
        den = 1
        for k in range(n):
            if k == j:
                continue
            num = pmul(num, [(-xs[k]) % p, 1], p)
            den = den * (xs[j] - xs[k]) % p
        s = ys[j] * inv(den, p) % p
        res = padd(res, [(co * s) % p for co in num], p)
    return res

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

# deterministic, version-independent PRNG (never used for extremal EXISTENCE, only to
# pick test coset positions / random gammas for the identity spot-suites)
class LCG:
    def __init__(self, seed):
        self.s = seed & ((1 << 64) - 1)

    def nxt(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return self.s >> 17

    def randint(self, lo, hi):  # inclusive
        return lo + self.nxt() % (hi - lo + 1)

# =====================================================================================
# TWO independent spectrum implementations
# =====================================================================================
def spectrum_A(gamma, p, ell):
    """generator-power cosets g^i H, direct ascending power-sum evaluation."""
    g = find_gen(p)
    n = (p - 1) // ell
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    out = []
    for i in range(n):
        b = pow(g, i, p)
        cnt = {}
        for h in H:
            x = b * h % p
            v = 0
            xr = 1
            for r in range(1, ell):
                xr = xr * x % p
                if gamma[r - 1]:
                    v = (v + gamma[r - 1] * xr) % p
            cnt[v] = cnt.get(v, 0) + 1
        out.append(max(cnt.values()))
    out.sort(reverse=True)
    return out

def spectrum_B(gamma, p, ell):
    """independent: label cosets by x^ell mod p (no generator), Horner evaluation."""
    groups = {}
    for x in range(1, p):
        a = pow(x, ell, p)
        v = 0
        for c in reversed(gamma):
            v = (v * x + c) % p
        v = v * x % p  # Gamma has no constant term: sum_{r>=1} gamma_r x^r
        d = groups.setdefault(a, {})
        d[v] = d.get(v, 0) + 1
    out = [max(d.values()) for d in groups.values()]
    out.sort(reverse=True)
    return out

def topk(spec, k):
    return sum(spec[:k])

def E3(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)

def spread(spec):
    return sum(1 for mu in spec if mu >= 2)

# =====================================================================================
# rank-formula machinery (gate iii) — exact F_p linear algebra
# =====================================================================================
def rref(rows, ncols, p):
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
    return r, A, piv

def rank_Fp(rows, ncols, p):
    if not rows:
        return 0
    return rref(rows, ncols, p)[0]

def nulldim(rows, ncols, p):
    return ncols - rank_Fp(rows, ncols, p)

def vpow(x, ell, p):
    return [pow(x, r, p) for r in range(1, ell)]

def vfull(x, ell, p):
    return [pow(x, r, p) for r in range(ell)]

def fiber_rows(points, ell, p):
    if len(points) < 2:
        return []
    v0 = vpow(points[0], ell, p)
    rows = []
    for x in points[1:]:
        vx = vpow(x, ell, p)
        rows.append([(v0[r] - vx[r]) % p for r in range(ell - 1)])
    return rows

def pattern_rows(fibers, ell, p):
    rows = []
    for F in fibers:
        rows.extend(fiber_rows(F, ell, p))
    return rows

def delta_dim(fibers, ell, p):
    """delta = dim(D cap Z) in F_p^P: nullspace of stacked K fiber-indicator rows and
    ell full-Vandermonde rows (r=0..ell-1)."""
    pts = [x for F in fibers for x in F]
    P = len(pts)
    rows = []
    idx = 0
    for F in fibers:
        row = [0] * P
        for _ in F:
            row[idx] = 1
            idx += 1
        rows.append(row)
    for rr in range(ell):
        rows.append([pow(x, rr, p) for x in pts])
    return nulldim(rows, P, p)

# =====================================================================================
# lambda-freeness + full-codeword chain (gate vi) — port of #260 d1_v1_witness_check.py
# =====================================================================================
def solve_aug(M, rhs, p):
    ncols = len(M[0])
    A = [M[i][:] + [rhs[i] % p] for i in range(len(M))]
    nr = len(A)
    piv = {}
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, nr):
            if A[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = inv(A[r][c], p)
        A[r] = [(v * iv) % p for v in A[r]]
        for i in range(nr):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(ncols + 1)]
        piv[c] = r
        r += 1
        if r == nr:
            break
    for i in range(r, nr):
        if A[i][ncols] % p:
            return None, None, len(piv)
    part = [0] * ncols
    for c, ri in piv.items():
        part[c] = A[ri][ncols] % p
    nb = []
    for free in range(ncols):
        if free in piv:
            continue
        v = [0] * ncols
        v[free] = 1
        for c, ri in piv.items():
            v[c] = (-A[ri][free]) % p
        nb.append(v)
    return part, nb, len(piv)

def gamma_eval(gamma, x, p, ell):
    v = 0
    xr = 1
    for r in range(1, ell):
        xr = xr * x % p
        v = (v + gamma[r - 1] * xr) % p
    return v

def spectrum_detail(gamma, p, ell, g, zeta):
    n = (p - 1) // ell
    H = [pow(zeta, j, p) for j in range(ell)]
    per = []
    for i in range(n):
        b = pow(g, i, p)
        vals = {}
        for h in H:
            v = gamma_eval(gamma, b * h % p, p, ell)
            vals[v] = vals.get(v, 0) + 1
        mf = max(vals.values())
        modal = min(v for v, c in vals.items() if c == mf)
        per.append({"rep": b, "idx": i, "maxfiber": mf, "modal": modal})
    fibers = sorted((d["maxfiber"] for d in per), reverse=True)
    return fibers, per

def crt_poly(pts, cprime, Eset, p):
    LE = poly_from_roots(list(Eset), p)
    xs, ys = [], []
    for (x, c) in zip(pts, cprime):
        xs.append(x)
        ys.append(c * peval(LE, x, p) % p)
    return lagrange_interp(xs, ys, p)

def is_kernel_set(pts, cprime, Eset, p):
    return len(crt_poly(pts, cprime, Eset, p)) - 1 <= len(Eset)

def run_witness_chain(gamma, p, ell, m, check_minimal=True):
    """Returns dict of gate booleans + (lam_free, full)."""
    t = m - 1
    g = find_gen(p)
    zeta = pow(g, (p - 1) // ell, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    fibers, per = spectrum_detail(gamma, p, ell, g, zeta)
    G = {}
    top_m = sum(fibers[:m])
    G["L1_topm>=2ell"] = top_m >= 2 * ell
    per_sorted = sorted(per, key=lambda d: (-d["maxfiber"], d["idx"]))
    core = per_sorted[:m]
    core_idx = {d["idx"] for d in core}
    petals = [d for d in per if d["idx"] not in core_idx][:t]
    b = [d["rep"] for d in core]
    beta = [pow(bj, ell, p) for bj in b]
    lam_target = [d["modal"] for d in core]
    a = [d["rep"] for d in petals]
    alpha = [pow(ai, ell, p) for ai in a]
    labels = alpha + beta
    G["cosets_distinct"] = (len(set(labels)) == t + m and 0 not in labels)
    phi = poly_from_roots(alpha, p)

    def lam_of(c, u, v):
        w = lagrange_interp(alpha, list(c), p)
        out = []
        for j in range(m):
            wbj = peval(w, beta[j], p)
            phibj = peval(phi, beta[j], p)
            g0bj = (u + v * beta[j]) % p
            out.append((-(wbj + phibj * g0bj) * inv(phibj, p)) % p)
        return out

    zero = lam_of([0] * t, 0, 0)
    cols = []
    for i in range(t):
        e = [0] * t
        e[i] = 1
        cols.append(lam_of(e, 0, 0))
    cols.append(lam_of([0] * t, 1, 0))
    cols.append(lam_of([0] * t, 0, 1))
    Mmat = [[cols[k][j] for k in range(t + 2)] for j in range(m)]
    _, _, rank = solve_aug(Mmat, [0] * m, p)
    G["LF_map_zeroconst"] = all(z == 0 for z in zero)
    G["LF_rank_m_surjective"] = (rank == m)
    part, nb, _ = solve_aug(Mmat, [(lam_target[j] - zero[j]) % p for j in range(m)], p)
    good = None
    if part is not None and nb:
        kk = nb[0]
        for s in range(p):
            x = [(part[i] + s * kk[i]) % p for i in range(t + 2)]
            c = x[:t]
            if 0 not in c and len(set(c)) == t:
                good = x
                break
    elif part is not None:
        if 0 not in part[:t] and len(set(part[:t])) == t:
            good = part
    G["LF_c_distinct_nonzero"] = good is not None
    lam_free = G["LF_rank_m_surjective"] and G["LF_c_distinct_nonzero"]
    if good is None:
        return G, lam_free, False, top_m
    c = good[:t]
    u, v = good[t], good[t + 1]
    w = lagrange_interp(alpha, list(c), p)
    gpoly = [0] * (ell + 1)
    gpoly[0] = u % p
    gpoly[ell] = v % p
    for r in range(1, ell):
        gpoly[r] = (gpoly[r] + gamma[r - 1]) % p
    while gpoly and gpoly[-1] == 0:
        gpoly.pop()
    P = padd(substitute_xk(w, ell), pmul(substitute_xk(phi, ell), gpoly, p), p)
    G["L3_degP<=m*ell"] = (len(P) - 1 <= m * ell)
    G["L3_mixed"] = any(x % p for x in gamma)
    petal_pts, petal_c = [], []
    petal_ok = True
    for i in range(t):
        for h in H:
            x = a[i] * h % p
            petal_pts.append(x)
            petal_c.append(c[i])
            if peval(P, x, p) != c[i] % p:
                petal_ok = False
    G["L3_petal_full"] = petal_ok
    core_pts, retained, missed, per_ret = [], [], [], []
    for j in range(m):
        rj = 0
        for h in H:
            x = b[j] * h % p
            core_pts.append(x)
            if peval(P, x, p) % p == 0:
                retained.append(x)
                rj += 1
            else:
                missed.append(x)
        per_ret.append(rj)
    R = len(retained)
    G["L4_R>=2ell"] = (R >= 2 * ell)
    G["L4_agreements>=s"] = (t * ell + R >= (m + 1) * ell)
    G["L4_retained==maxfiber"] = (per_ret == [d["maxfiber"] for d in core])
    G["dom_distinct_pts"] = (len(set(petal_pts + core_pts)) == (t + m) * ell)
    Mset = set(missed)
    Lambda = poly_from_roots(beta, p)
    cprime = [c[i] * inv(peval(Lambda, alpha[i], p), p) % p for i in range(t)]
    petal_cprime = [cprime[i] for i in range(t) for _ in H]
    WM = crt_poly(petal_pts, petal_cprime, Mset, p)
    degWM = len(WM) - 1
    Lret = poly_from_roots(retained, p)
    id_ok = (pmul(WM, Lret, p) == P) and (degWM == len(P) - 1 - len(retained))
    G["L5_M_kernel"] = (degWM <= len(Mset))
    G["L5_identity"] = id_ok
    if check_minimal:
        minimal = True
        for x in list(Mset):
            if is_kernel_set(petal_pts, petal_cprime, Mset - {x}, p):
                minimal = False
                break
        G["L5_minimal"] = minimal
    proper = []
    for j in range(m):
        cj = set(b[j] * h % p for h in H)
        proper.append(len(Mset & cj))
    G["L6_primitive_mixed"] = all(0 < x < ell for x in proper)
    full = all(G.values())
    return G, lam_free, full, top_m

# =====================================================================================
# recorded witness data  (spectra + verdicts fixed by explore_lf.py run — see .out)
# =====================================================================================
WITNESSES = [
    {"label": "ell=11 m=7 p=199", "p": 199, "ell": 11, "m": 7,
     "gamma": [1, 172, 129, 7, 90, 84, 119, 194, 176, 1],
     "spectrum_head": [4, 4, 3, 3, 3, 3, 2, 2, 1], "top_m": 22,
     "lam_free": True, "full": True},
    {"label": "ell=11 m=7 p=331", "p": 331, "ell": 11, "m": 7,
     "gamma": [97, 29, 97, 239, 171, 92, 143, 155, 270, 1],
     "spectrum_head": [5, 5, 4, 3, 2, 2, 2, 1, 1], "top_m": 23,
     "lam_free": True, "full": True},
    {"label": "ell=13 m=8 p=313", "p": 313, "ell": 13, "m": 8,
     "gamma": [254, 289, 29, 276, 242, 219, 201, 261, 79, 232, 133, 1],
     "spectrum_head": [5, 4, 4, 3, 3, 3, 3, 2, 2, 2], "top_m": 27,
     "lam_free": True, "full": True},
    {"label": "ell=17 m=10 p=409", "p": 409, "ell": 17, "m": 10,
     "gamma": [165, 169, 244, 263, 276, 149, 333, 170, 86, 260, 80, 398, 377, 77, 324, 1],
     "spectrum_head": [6, 5, 4, 4, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2], "top_m": 34,
     "lam_free": True, "full": True},
]

SPECTRUM_EVIDENCE_17 = [
    # spectrum-side ell=17 evidence (lambda-freeness not checkable: n < t+m = 19)
    {"label": "ell=17 m=10 p=307 (spectrum-side)", "p": 307, "ell": 17, "m": 10,
     "gamma": [228, 204, 58, 38, 264, 64, 141, 107, 259, 208, 216, 48, 69, 281, 201, 1], "top_m": 34, "E3": 14},
    {"label": "ell=17 m=10 p=239 (spectrum-side)", "p": 239, "ell": 17, "m": 10,
     "gamma": [191, 180, 118, 44, 62, 65, 196, 62, 156, 90, 217, 77, 169, 126, 183, 1], "top_m": 34, "E3": 14},
    # tight E_3 ceiling anchor at ell=17: E_3 = 15 = ell-2 exactly
    {"label": "ell=17 p=103 E3-anchor", "p": 103, "ell": 17, "m": None,
     "gamma": [30, 82, 52, 3, 7, 90, 70, 30, 27, 71, 85, 33, 12, 85, 66, 0], "top_m": None, "E3": 15},
]

def ceil2ell3(ell):
    return -(-2 * ell // 3)  # ceil(2ell/3)

def corrected_frontier(ell):
    return (ell + 3) // 2

# =====================================================================================
# GATES  (each returns (ok: bool, summary: str); tamper flips ONE guarded datum)
# =====================================================================================
def gate_i_spectra(tamper=False):
    ok = True
    lines = []
    for wi, W in enumerate(WITNESSES):
        gamma = list(W["gamma"])
        if tamper and wi == 0:
            gamma[0] = (gamma[0] + 1) % W["p"]  # flip one coefficient of first witness
        sA = spectrum_A(gamma, W["p"], W["ell"])
        sB = spectrum_B(gamma, W["p"], W["ell"])
        head = W["spectrum_head"]
        tm = topk(sA, W["m"])
        good = (sA == sB) and (sA[:len(head)] == head) and (tm == W["top_m"]) and (tm >= 2 * W["ell"])
        ok = ok and good
        lines.append("%s: A==B=%s top-%d=%d(>=2ell=%d) head_ok=%s"
                     % (W["label"], sA == sB, W["m"], tm, 2 * W["ell"], sA[:len(head)] == head))
    return ok, " | ".join(lines)

def gate_ii_topm_bound(tamper=False):
    slack = 1 if tamper else 0  # tamper shrinks the PROVED budget by 1
    rng = LCG(20260704)
    bad = 0
    ntot = 0
    for ell, p in [(7, 211), (11, 199), (13, 313)]:
        for _ in range(40):
            gamma = [rng.randint(0, p - 1) for _ in range(ell - 1)]
            if not any(gamma):
                continue
            spec = spectrum_A(gamma, p, ell)
            a = spread(spec)
            e = E3(spec)
            for m in range(1, min(len(spec), ell) + 1):
                tm = topk(spec, m)
                if tm > 2 * m + e - slack:
                    bad += 1
                if tm > m + min(m, a) + e - slack:
                    bad += 1
                ntot += 2
    # tightness anchor: the ell=11 p=199 witness saturates top-7 = 2*7 + E_3
    Wsat = WITNESSES[0]
    spec = spectrum_A(Wsat["gamma"], Wsat["p"], Wsat["ell"])
    sat = (topk(spec, 7) == 2 * 7 + E3(spec) - slack)
    ok = (bad == 0) and sat
    return ok, "%d (gamma,m) tests, viol=%d; ell=11 saturation top-7==2m+E_3 (slack=%d): %s" % (ntot, bad, slack, sat)

def gate_iii_rank_formula(tamper=False):
    # cfgs deliberately EXERCISE the realizability boundary (rank == ell-2 and rank == ell-1)
    # and the delta>0 regime, so BOTH the (P-K)-delta identity AND the `rank<=ell-2` threshold
    # constant are load-bearing (a wrong threshold, e.g. ell-3, fails the rank==ell-2 configs).
    cfgs = [(7, 211, (3, 3)), (7, 211, (4, 4)), (7, 211, (5, 3)), (7, 337, (3, 3, 3)),
            (7, 211, (2, 2, 2, 2)), (11, 199, (4, 4)), (11, 199, (3, 3, 3)),
            (11, 67, (4, 3)), (13, 79, (5, 3)), (13, 313, (3, 3, 3)),
            # single fiber of size ell-1: generic (delta=0), rank = (ell-1)-1 = ell-2 EXACTLY
            #   -> boundary-REALIZABLE (pins the threshold constant from below)
            (7, 211, (6,)), (11, 199, (10,)), (13, 313, (12,)),
            # full-coset fiber of size ell: delta=0, rank = ell-1 EXACTLY -> boundary-NON-realizable
            #   (a nonzero constant-free deg<=ell-1 Gamma cannot be constant on a whole coset)
            (7, 211, (7,)),
            # delta>0 configs: exercise rank=(P-K)-delta OUTSIDE the trivial generic regime
            #   ((4,4,4): delta=3; the note's ell=7 extremal spread [3,3,3,3,2,2,2]: delta=5)
            (7, 211, (4, 4, 4)), (7, 211, (3, 3, 3, 3, 2, 2, 2))]

    def run(off, thr):
        # off: perturb the rank IDENTITY by +1 ; thr: tighten the realizability THRESHOLD by 1
        ok = True
        ntot = 0
        nlo = 0   # #configs at rank == ell-2 (boundary-realizable)
        nhi = 0   # #configs at rank == ell-1 (boundary-non-realizable)
        maxdelta = 0
        rng = LCG(777)
        for ell, p, sizes in cfgs:
            if not (is_prime(p) and (p - 1) % ell == 0):
                continue
            n = (p - 1) // ell
            g = find_gen(p)
            zeta = pow(g, n, p)
            H = [pow(zeta, j, p) for j in range(ell)]
            K = len(sizes)
            if K + 1 > n or max(sizes) > ell:   # allow the full-coset (size ell) boundary config
                continue
            # place fibers on K distinct random cosets, first `nu` H-exponents each
            cos = []
            while len(cos) < K:
                c = rng.randint(0, n - 1)
                if c not in cos:
                    cos.append(c)
            fibers = [[pow(g, cos[s], p) * H[e] % p for e in range(sizes[s])] for s in range(K)]
            pts = [x for F in fibers for x in F]
            if len(set(pts)) != len(pts):
                continue
            P = len(pts)
            rows = pattern_rows(fibers, ell, p)
            rank = rank_Fp(rows, ell - 1, p)
            delta = delta_dim(fibers, ell, p)
            maxdelta = max(maxdelta, delta)
            if rank == ell - 2:
                nlo += 1
            if rank == ell - 1:
                nhi += 1
            rel = (rank == (P - K) - delta + off)
            real = (rank <= ell - 2 - thr)
            ns_nonzero = (nulldim(rows, ell - 1, p) > 0)
            ok = ok and rel and (ns_nonzero == real)
            ntot += 1
        return ok, ntot, nlo, nhi, maxdelta

    if not tamper:
        ok, ntot, nlo, nhi, md = run(0, 0)
        # coverage: the shipped run MUST hit the ell-2 boundary, the ell-1 boundary, and a delta>0 case,
        # else the threshold constant / identity would not be load-bearing.
        cover = (nlo >= 1 and nhi >= 1 and md >= 1)
        return (ok and cover), ("%d configs (rank==(P-K)-delta and realizable<=>rank<=ell-2); "
                                "coverage rank==ell-2:%d rank==ell-1:%d maxdelta=%d" % (ntot, nlo, nhi, md))
    # tamper: prove BOTH sub-claims have teeth INDEPENDENTLY -- the rank-identity offset flip must
    # break some config AND the realizability-threshold flip must (separately) break some config;
    # report CAUGHT only if both do (a missed sub-claim -> gate reports 'MISSED', flagging the gap).
    ident_caught = not run(1, 0)[0]
    thresh_caught = not run(0, 1)[0]
    caught = ident_caught and thresh_caught
    return (not caught), ("identity-flip caught=%s threshold-flip caught=%s" % (ident_caught, thresh_caught))

def gate_iv_e3_bound(tamper=False):
    off = 1 if tamper else 0  # tamper tightens KEY LEMMA to E_3<=ell-3; the saturating
    # witnesses (p=331 E_3=9=ell-2, p=313 E_3=11=ell-2) catch it
    ok = True
    viol = 0
    maxE = {}
    seen_total = 0
    # bounded, seeded, solve-based sweep: K three-fiber patterns on distinct cosets
    import itertools
    for ell, p in [(7, 211), (11, 199)]:
        n = (p - 1) // ell
        g = find_gen(p)
        zeta = pow(g, n, p)
        H = [pow(zeta, j, p) for j in range(ell)]
        shapes = [c for c in itertools.combinations(range(ell), 3) if c[0] == 0]
        if ell > 7:
            shapes = shapes[:6]
        rng = LCG(31 + ell)
        mE = 0
        for _ in range(120):  # bounded number of random planted configs (documented cap)
            K = rng.randint(2, 3)
            cos = []
            while len(cos) < K:
                cc = rng.randint(0, n - 1)
                if cc not in cos:
                    cos.append(cc)
            combo = [shapes[rng.randint(0, len(shapes) - 1)] for _ in range(K)]
            fibers = [[pow(g, cos[s], p) * H[e] % p for e in combo[s]] for s in range(K)]
            pts = [x for F in fibers for x in F]
            if len(set(pts)) != 3 * K:
                continue
            rows = pattern_rows(fibers, ell, p)
            if rank_Fp(rows, ell - 1, p) > ell - 2:
                continue
            # solve nullspace, test each basis gamma (exact solve, never sampled)
            _, A, piv = rref(rows, ell - 1, p)
            pivset = set(piv)
            basis = []
            for free in range(ell - 1):
                if free in pivset:
                    continue
                vv = [0] * (ell - 1)
                vv[free] = 1
                for i, cc in enumerate(piv):
                    vv[cc] = (-A[i][free]) % p
                basis.append(vv)
            for gm in basis:
                if not any(gm):
                    continue
                spec = spectrum_A(gm, p, ell)
                e = E3(spec)
                mE = max(mE, e)
                seen_total += 1
                if e > ell - 2 - off:
                    viol += 1
        maxE[ell] = mE
    # saturation anchors: two of the shipped witnesses attain E_3 = ell-2 EXACTLY
    # (p=331: 9, p=313: 11), so a tightened cap (off=1 -> ell-3) must fail here.
    sat_ok = True
    sat_seen = []
    for W in (WITNESSES[1], WITNESSES[2]):
        spec = spectrum_A(W["gamma"], W["p"], W["ell"])
        e = E3(spec)
        sat_seen.append(e)
        if not (e == W["ell"] - 2 and e <= W["ell"] - 2 - off):
            sat_ok = False
    # structural identity (not a saturator): concentrated Gamma has E_3 = ell-3 exactly
    conc_ok = True
    for ell, p in [(7, 211), (11, 199), (13, 313)]:
        spec = spectrum_A([1] * (ell - 1), p, ell)
        if E3(spec) != ell - 3:
            conc_ok = False
    ok = (viol == 0) and sat_ok and conc_ok
    return ok, "solve-based sweep %d gammas maxE_3=%s (cap ell-2); witness saturation E_3=%s(off=%d):%s concentrated-identity:%s viol=%d" % (
        seen_total, maxE, sat_seen, off, sat_ok, conc_ok, viol)

def gate_viii_ell17_evidence(tamper=False):
    ok = True
    lines = []
    for wi, W in enumerate(SPECTRUM_EVIDENCE_17):
        gamma = list(W["gamma"])
        if tamper and wi == 0:
            gamma[0] = (gamma[0] + 1) % W["p"]  # corrupt -> recomputed top-10/E3 must mismatch
        sA = spectrum_A(gamma, W["p"], W["ell"])
        sB = spectrum_B(gamma, W["p"], W["ell"])
        good = (sA == sB) and (E3(sA) == W["E3"])
        if W["m"] is not None:
            good = good and (topk(sA, W["m"]) == W["top_m"] == 2 * W["ell"])
            good = good and (topk(sA, W["m"] - 1) < 2 * W["ell"])  # (ell+1)/2 stays vacant here
        else:
            good = good and (E3(sA) == W["ell"] - 2)  # tight ceiling anchor
        ok = ok and good
        lines.append("%s: %s" % (W["label"], "ok" if good else "MISMATCH"))
    return ok, " | ".join(lines)

def gate_v_geometric_nonlister(tamper=False):
    ok = True
    lines = []
    for ell, p in [(7, 211), (11, 199), (13, 313)]:
        # (a) concentrated Gamma = X+...+X^{ell-1}; (b) genuine geometric gamma_r = 2^r
        fams = {"concentrated": [1] * (ell - 1), "geometric(2^r)": [pow(2, r, p) for r in range(1, ell)]}
        for fam, gamma in fams.items():
            gm = list(gamma)
            if tamper and fam == "concentrated" and ell == 7:
                gm[0] = (gm[0] + 1) % p  # break the concentrated structure
            sA = spectrum_A(gm, p, ell)
            sB = spectrum_B(gm, p, ell)
            struct = (sA == sB and sA[0] == ell - 1 and set(sA[1:]) == {1}
                      and E3(sA) == ell - 3 and spread(sA) == 1)
            nonlist = all(topk(sA, m) == ell + m - 2 and topk(sA, m) < 2 * ell for m in range(1, ell))
            ok = ok and struct and nonlist
        lines.append("ell=%d ok" % ell)
    return ok, "concentrated & geometric: spectrum [ell-1,1,..], top-m=ell+m-2<2ell; " + " ".join(lines)

def gate_vi_lambda_freeness(tamper=False):
    ok = True
    lines = []
    for wi, W in enumerate(WITNESSES):
        gamma = list(W["gamma"])
        if tamper and wi == 0:
            gamma[0] = (gamma[0] + 1) % W["p"]  # corrupt the witness -> chain must fail
        G, lam_free, full, top_m = run_witness_chain(gamma, W["p"], W["ell"], W["m"])
        match = (lam_free == W["lam_free"]) and (full == W["full"])
        ok = ok and match and (full if not tamper else True)
        lines.append("%s: lam_free=%s full=%s (recorded %s/%s) match=%s"
                     % (W["label"], lam_free, full, W["lam_free"], W["full"], match))
    return ok, " | ".join(lines)

def gate_vii_negative_control(tamper=False):
    # guards the refutation: conjecture predicts vacancy at m=(ell+3)/2 (< ceil(2ell/3)),
    # but the witness LISTS there. tamper corrupts the witness so it no longer lists.
    ok = True
    lines = []
    for W in WITNESSES:
        if W["label"] == "ell=11 m=7 p=331":
            continue  # one witness per ell suffices for the control
        ell = W["ell"]
        m = W["m"]
        gamma = list(W["gamma"])
        if tamper and ell == 11:
            gamma[0] = (gamma[0] + 1) % W["p"]
        if m != corrected_frontier(ell):   # clean per-gate FAIL (not a bare-assert traceback)
            return False, "witness m=%d != corrected_frontier(%d)=%d" % (m, ell, corrected_frontier(ell))
        conjecture_predicts_vacant = (m < ceil2ell3(ell))  # old law: listing iff m>=ceil(2ell/3)
        actually_lists = (topk(spectrum_A(gamma, W["p"], ell), m) >= 2 * ell)
        refuted = conjecture_predicts_vacant and actually_lists
        ok = ok and refuted
        lines.append("ell=%d: corrected m*=%d < ceil(2ell/3)=%d, lists=%s -> conj REFUTED=%s"
                     % (ell, m, ceil2ell3(ell), actually_lists, refuted))
    return ok, " | ".join(lines)

GATES = [
    ("(i)   witness spectra (2 impls)          ", gate_i_spectra),
    ("(ii)  top-m <= 2m+E_3 (tight)            ", gate_ii_topm_bound),
    ("(iii) rank formula rank=(P-K)-delta      ", gate_iii_rank_formula),
    ("(iv)  KEY LEMMA E_3<=ell-2 (solve sweep) ", gate_iv_e3_bound),
    ("(v)   geometric Gamma non-lister         ", gate_v_geometric_nonlister),
    ("(vi)  lambda-freeness + full codeword    ", gate_vi_lambda_freeness),
    ("(vii) negative control (refutation)      ", gate_vii_negative_control),
    ("(viii) ell=17 evidence (spectrum-side)    ", gate_viii_ell17_evidence),
]

def main():
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 90)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is flipped")
    else:
        print(" verify_l1_prime_ell_frontier_corrected  (zero-arg)   m*(ell)=(ell+3)/2 refutes ceil(2ell/3)")
    print("=" * 90)
    all_good = True
    for name, fn in GATES:
        if selftest:
            ok, summ = fn(tamper=True)
            caught = not ok
            all_good = all_good and caught
            print("  %s  TAMPER %s" % (name, "CAUGHT " if caught else "MISSED!"))
        else:
            ok, summ = fn(tamper=False)
            all_good = all_good and ok
            print("  %s  %s" % (name, "PASS" if ok else "FAIL"))
            print("        %s" % summ)
    print("=" * 90)
    if selftest:
        print(" SELF-TEST RESULT: %s   (%.1fs)" % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)" % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)

if __name__ == "__main__":
    main()
