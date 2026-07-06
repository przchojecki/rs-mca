#!/usr/bin/env python3
"""verify_l1_ell19_attainment.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_ell19_attainment.md`, which resolves the
`ell = 19` row of `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`
(there marked "`m=10` listing OPEN") POSITIVELY: an explicit full witness at
`p = 647` lists at `m = 10 = (ell+1)/2`, so `ell = 19` joins the attainment
half of `m*(ell) = (ell+1)/2` unconditionally (`ell in {11,13,17,19,23}`).

Ground rule: this verifier is SELF-CONTAINED. It does not import
`experimental/scripts/verify_l1_prime_ell_frontier_corrected.py` or any other
sibling verifier at runtime -- every piece of arithmetic below (the spectrum
computation, in TWO independent implementations, and the full 16-gate
`run_witness_chain` lambda-freeness + codeword chain) is a fresh, from-scratch
reimplementation, faithfully matching the gate names and semantics of the
integrated convention (`experimental/scripts/verify_l1_key_lemma_refuted.py`
sec-header + the shipped note's sec 1 gate list), so that a bug shared with
the original module could not silently launder a false witness.

Six gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)   witness-1 spectrum (`m=10, p=647`): recompute the FULL spectrum from
        the raw `gamma` alone via two independent implementations (coset-key
        `x^ell mod p` + Horner; and generator-power-coset walk + ascending
        power-sum), require they AGREE, and check `E_3 = 18`, `top-9 = 36`,
        `top-10 = 38`, `top-11 = 40` exactly.
  (ii)  witness-2 spectrum (`m=11, p=647`): same, `E_3 = 17`, `top-10 = 37`,
        `top-11 = 38`.
  (iii) FULL 16-gate `run_witness_chain` (fresh port, not imported) on both
        witnesses at their listing `m` (10 for witness-1, 11 for witness-2):
        all 16 gates True, `lambda`-free True (this is the expensive gate --
        it runs the `L5_minimal` missed-core-minimality search LIVE for both
        witnesses, no deferral).
  (iv)  concentrated `K=1` floor (note sec 4a): construct `gamma_r == 1` for
        `r=1..ell-1` at `p in {191, 419, 647, 1103}`; check spectrum
        `[ell-1, 1, ..., 1]` (`n-1` ones) and `E_3 = ell-3 = 16` at each.
  (v)   two-fiber plant identity (note sec 4b): for EVERY integer split
        `s_1 + s_2 = ell = 19` with `s_1, s_2 >= 2`, check the identity
        `(s_1-2) + (s_2-2) = ell-4 = 15` -- a closed-form arithmetic check,
        no `F_p` machinery needed.
  (vi)  coverage-consistency: load the companion certificate JSON
        (`experimental/data/certificates/l1-ell19/l1_ell19_witnesses.json`)
        and, for every one of its `coverage_rows` (36 primes; every row here
        carries a stored `gamma`), independently recompute `E_3` from the
        stored `gamma` and require it match the row's `claimed_max_E3`
        exactly.

Hidden self-test: `python3 verify_l1_ell19_attainment.py --tamper-selftest`
    flips one datum per gate class (a `gamma` coefficient, a spectrum entry,
    or a claimed count, spread across the six gates) and asserts each gate
    then FAILS -- proving every gate has teeth. The shipped default is
    zero-arg.

All arithmetic is exact over F_p, stdlib only. No network, no CLI args
required for the default run (only the companion JSON under this repo is
read, resolved relative to this file so invocation cwd does not matter).
"""
import sys
import os
import json
import time

ELL = 19

# =====================================================================================
# exact F_p arithmetic -- fresh, self-contained (no import of any sibling verifier)
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
    raise RuntimeError("no generator found for p=%d" % p)

# =====================================================================================
# TWO independent spectrum implementations (gate i/ii cross-check)
# =====================================================================================
def spectrum_coset_key(gamma, p, ell):
    """Implementation A: label F_p^* by coset key x^ell mod p (no generator
    needed), Horner-evaluate Gamma(x) = sum_{r=1}^{ell-1} gamma_r x^r (NOTE:
    gamma has no constant term, so after the length-(ell-1) Horner pass over
    gamma treated as coefficients of x^0..x^(ell-2), one extra factor of x is
    required); per-coset max multiplicity ("max fiber"), sorted descending."""
    groups = {}
    for x in range(1, p):
        lab = pow(x, ell, p)
        v = 0
        for c in reversed(gamma):
            v = (v * x + c) % p
        v = v * x % p  # shift: Gamma has no x^0 term
        d = groups.setdefault(lab, {})
        d[v] = d.get(v, 0) + 1
    return sorted((max(d.values()) for d in groups.values()), reverse=True)

def spectrum_gen_walk(gamma, p, ell):
    """Implementation B: independent -- walk generator-power cosets g^i * H
    (H = the order-ell subgroup), ascending power-sum evaluation of Gamma at
    each point (no x^ell grouping, no Horner)."""
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

def E3(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)

def topk(spec, k):
    return sum(spec[:k])

# =====================================================================================
# polynomial + linear-algebra machinery over F_p (fresh port, needed by
# run_witness_chain below)
# =====================================================================================
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

def solve_aug(M, rhs, p):
    """Gaussian elimination of an augmented system; returns (particular
    solution, nullspace basis, rank), or (None, None, rank) if inconsistent."""
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
    """Per-coset detail record: representative, index, max-fiber size, and
    the MODAL value achieved by that max fiber (needed by the lambda-free
    machinery below)."""
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

# =====================================================================================
# FULL 16-gate run_witness_chain -- faithful fresh port of the integrated
# convention (gate names/semantics match experimental/scripts/
# verify_l1_prime_ell_frontier_corrected.py and the laneA/6af63e14 replay
# scripts that call it); this copy is independent at runtime (no import).
# =====================================================================================
def run_witness_chain(gamma, p, ell, m, check_minimal=True):
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
    else:
        G["L5_minimal"] = None
    proper = []
    for j in range(m):
        cj = set(b[j] * h % p for h in H)
        proper.append(len(Mset & cj))
    G["L6_primitive_mixed"] = all(0 < x < ell for x in proper)
    full = all(v for v in G.values() if v is not None) and (G["L5_minimal"] is not False)
    return G, lam_free, full, top_m

# =====================================================================================
# the two shipped witnesses (verbatim from the note / companion JSON)
# =====================================================================================
WITNESS_M10 = {
    "label": "m=10 p=647 (headline)", "ell": 19, "m": 10, "p": 647,
    "gamma": [298, 638, 143, 294, 14, 111, 237, 78, 464, 166, 355, 385, 207, 68, 465, 369, 316, 1],
    "E3": 18, "top9": 36, "top10": 38, "top11": 40,
}
WITNESS_M11 = {
    "label": "m=11 p=647 (companion)", "ell": 19, "m": 11, "p": 647,
    "gamma": [318, 474, 374, 319, 297, 217, 24, 346, 0, 609, 514, 362, 499, 309, 174, 383, 93, 1],
    "E3": 17, "top10": 37, "top11": 38,
}

# repo-relative path to the companion certificate JSON, resolved relative to
# THIS file so it works regardless of invocation cwd.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
CERT_PATH = os.path.join(_REPO_ROOT, "experimental", "data", "certificates", "l1-ell19", "l1_ell19_witnesses.json")

def load_cert():
    with open(CERT_PATH) as f:
        return json.load(f)

# =====================================================================================
# GATES (each returns (ok: bool, summary: str); tamper flips ONE guarded datum)
# =====================================================================================
def gate_i_witness1_spectrum(tamper=False):
    gamma = list(WITNESS_M10["gamma"])
    p, ell = WITNESS_M10["p"], WITNESS_M10["ell"]
    if tamper:
        gamma[0] = (gamma[0] + 1) % p  # flip a gamma coefficient
    sA = spectrum_coset_key(gamma, p, ell)
    sB = spectrum_gen_walk(gamma, p, ell)
    agree = (sA == sB)
    e3 = E3(sA)
    t9, t10, t11 = topk(sA, 9), topk(sA, 10), topk(sA, 11)
    ok = (agree and e3 == WITNESS_M10["E3"] and t9 == WITNESS_M10["top9"]
          and t10 == WITNESS_M10["top10"] and t11 == WITNESS_M10["top11"])
    return ok, ("A==B=%s E3=%d(exp %d) top9=%d(exp %d) top10=%d(exp %d) top11=%d(exp %d)"
                % (agree, e3, WITNESS_M10["E3"], t9, WITNESS_M10["top9"],
                   t10, WITNESS_M10["top10"], t11, WITNESS_M10["top11"]))

def gate_ii_witness2_spectrum(tamper=False):
    gamma = list(WITNESS_M11["gamma"])
    p, ell = WITNESS_M11["p"], WITNESS_M11["ell"]
    sA = spectrum_coset_key(gamma, p, ell)
    sB = spectrum_gen_walk(gamma, p, ell)
    agree = (sA == sB)
    e3 = E3(sA)
    t10, t11 = topk(sA, 10), topk(sA, 11)
    exp_top10, exp_top11 = WITNESS_M11["top10"], WITNESS_M11["top11"]
    if tamper:
        exp_top11 = exp_top11 + 1  # flip a claimed count (target, not the object)
    ok = (agree and e3 == WITNESS_M11["E3"] and t10 == WITNESS_M11["top10"] and t11 == exp_top11)
    return ok, ("A==B=%s E3=%d(exp %d) top10=%d(exp %d) top11=%d(exp %d%s)"
                % (agree, e3, WITNESS_M11["E3"], t10, WITNESS_M11["top10"],
                   t11, exp_top11, " TAMPERED" if tamper else ""))

def gate_iii_full_chain(tamper=False):
    g1 = list(WITNESS_M10["gamma"])
    g2 = list(WITNESS_M11["gamma"])
    if tamper:
        g1[0] = (g1[0] + 1) % WITNESS_M10["p"]  # flip a gamma coefficient
    G1, lf1, full1, tm1 = run_witness_chain(g1, WITNESS_M10["p"], WITNESS_M10["ell"], WITNESS_M10["m"], check_minimal=True)
    G2, lf2, full2, tm2 = run_witness_chain(g2, WITNESS_M11["p"], WITNESS_M11["ell"], WITNESS_M11["m"], check_minimal=True)
    all16_1 = (len(G1) == 16) and all(G1.values())
    all16_2 = (len(G2) == 16) and all(G2.values())
    ok = all16_1 and full1 and lf1 and all16_2 and full2 and lf2
    return ok, ("w1(m=10): all16=%s full=%s lam_free=%s top_m=%d | "
                "w2(m=11): all16=%s full=%s lam_free=%s top_m=%d"
                % (all16_1, full1, lf1, tm1, all16_2, full2, lf2, tm2))

def gate_iv_concentrated_floor(tamper=False):
    ok = True
    lines = []
    for wi, p in enumerate([191, 419, 647, 1103]):
        n = (p - 1) // ELL
        gamma = [1] * (ELL - 1)
        if tamper and wi == 0:
            gamma[0] = 2  # flip a gamma coefficient (breaks the concentrated design)
        sA = spectrum_coset_key(gamma, p, ELL)
        sB = spectrum_gen_walk(gamma, p, ELL)
        expect = sorted([ELL - 1] + [1] * (n - 1), reverse=True)
        e3 = E3(sA)
        good = (sA == sB == expect) and (e3 == 16)
        ok = ok and good
        lines.append("p=%d n=%d shape_ok=%s E3=%d(exp16)" % (p, n, sA == expect, e3))
    return ok, " | ".join(lines)

def gate_v_twofiber_identity(tamper=False):
    target = 14 if tamper else 15  # tamper flips the claimed count (identity constant)
    ok = True
    n_checked = 0
    for s1 in range(2, ELL - 1):
        s2 = ELL - s1
        if s2 < 2:
            continue
        n_checked += 1
        val = (s1 - 2) + (s2 - 2)
        if val != target:
            ok = False
    return ok, "%d splits s1+s2=19 (s_i>=2), all (s1-2)+(s2-2)==%d: %s" % (n_checked, target, ok)

def gate_vi_coverage_consistency(tamper=False):
    cert = load_cert()
    rows = cert["coverage_rows"]
    ok = True
    n_rows = 0
    n_mismatch = 0
    for i, row in enumerate(rows):
        p = row["p"]
        gamma = list(row["gamma_X1_to_Xell_minus_1"])
        claimed = row["claimed_max_E3"]
        if tamper and i == 0:
            gamma[0] = (gamma[0] + 1) % p  # flip a gamma coefficient of one row
        sA = spectrum_coset_key(gamma, p, ELL)
        e3 = E3(sA)
        n_rows += 1
        if e3 != claimed:
            n_mismatch += 1
            ok = False
    return ok, "%d coverage rows, recomputed E3 mismatches claimed_max_E3: %d (expect 0)" % (n_rows, n_mismatch)

GATES = [
    ("(i)   witness-1 (m=10,p=647) spectrum   ", gate_i_witness1_spectrum),
    ("(ii)  witness-2 (m=11,p=647) spectrum   ", gate_ii_witness2_spectrum),
    ("(iii) full 16-gate run_witness_chain    ", gate_iii_full_chain),
    ("(iv)  concentrated K=1 floor            ", gate_iv_concentrated_floor),
    ("(v)   two-fiber plant identity          ", gate_v_twofiber_identity),
    ("(vi)  coverage-consistency (36 primes)  ", gate_vi_coverage_consistency),
]

def main():
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 92)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is flipped")
    else:
        print(" verify_l1_ell19_attainment  (zero-arg)   m*(19) <= 10 = (ell+1)/2 ATTAINED at p=647")
        print(" (experimental/notes/l1/l1_ell19_attainment.md)")
    print("=" * 92)
    all_good = True
    for name, fn in GATES:
        gt0 = time.time()
        if selftest:
            ok, summ = fn(tamper=True)
            caught = not ok
            all_good = all_good and caught
            print("  %s  TAMPER %s  [%.1fs]" % (name, "CAUGHT " if caught else "MISSED!", time.time() - gt0))
        else:
            ok, summ = fn(tamper=False)
            all_good = all_good and ok
            print("  %s  %s  [%.1fs]" % (name, "PASS" if ok else "FAIL", time.time() - gt0))
        print("        %s" % summ)
    print("=" * 92)
    if selftest:
        print(" SELF-TEST RESULT: %s   (%.1fs)" % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)" % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)

if __name__ == "__main__":
    main()
