#!/usr/bin/env python3
"""verify_l1_ell19_band_refuted.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_ell19_band_refuted.md`, which supersedes:

  - the `m*(19) = 10` / "vacancy half stands" framing of the INTEGRATED
    `experimental/notes/l1/l1_ell19_attainment.md` (its `m = 10`, `m = 11`
    witnesses SURVIVE unchanged as earlier attainment-ladder rungs), and
  - the named falsifier of the INTEGRATED
    `experimental/notes/l1/l1_e3_law_refuted.md` sec 4 (attained here, and
    refined: `top-m >= 2 ell` is the true requirement, `E_3 = ell + 1`
    suffices, `E_3 = ell + 2` is not necessary),

via one explicit, listing-eligible, full 16-gate witness at `ell = 19,
p = 571, m = 9 = (ell-1)/2` (one below the `(ell+1)/2` onset).

Ground rule: this verifier is SELF-CONTAINED. It does NOT import
`verify_l1_ell19_attainment.py`, `verify_l1_e3_law_refuted.py`, or any
other sibling verifier at runtime -- every piece of arithmetic below (the
spectrum computation, in TWO independent implementations, the full
16-gate `run_witness_chain` lambda-freeness + codeword chain, and the
reduction-formula recomputation) is a fresh, from-scratch reimplementation
matching the gate names/semantics of the integrated convention
(`experimental/scripts/verify_l1_key_lemma_refuted.py` sec-header + the
two integrated notes this one supersedes), so that a bug shared with an
existing module could not silently launder a false witness. Ground-rule
compliance (neither integrated note nor its verifier is edited, both
still exit 0 unmodified) was confirmed by manually re-running both at
packaging time -- see the note's sec 5 and the shipping commit message;
that check is NOT wired into this file as a gate, to keep this verifier
from invoking any sibling file at all, not even as a subprocess.

Four gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)   witness spectrum (`m=9, p=571`): recompute the FULL spectrum from
        the raw `gamma` alone via two independent implementations (coset-
        key `x^ell mod p` + Horner; generator-power-coset walk + ascending
        power-sum), require they AGREE, and check `E_3 = 20`, the sigma-
        calculus residual quantity `T = 5` (third-largest fiber onward),
        `top-8 = 36`, `top-9 = 38`, `top-10 = 40` exactly.
  (ii)  FULL 16-gate `run_witness_chain` (fresh port, not imported) on the
        witness at `m = 9`: all 16 gates True, `lambda`-free True,
        `top_m = 38` -- this is the expensive gate (it runs the
        `L5_minimal` missed-core-minimality search live, no deferral).
  (iii) reduction-formula check: recompute `a` (the number of cosets,
        OTHER than the single planted big-fiber coset, whose per-coset
        max fiber is `>= 3`) directly from the witness's own spectrum,
        and check `a = 6` and the closed-form identity
        `top-9 == 2*ell - 6 + a`.
  (iv)  structural/eligibility checks: `n = 30 >= 2*m-1 = 17`; `Gamma` is
        genuinely MIXED (more than one nonzero coefficient, a stricter
        check than the 16-gate chain's own `L3_mixed`); the PROVED
        pairwise cap `mu_1 + mu_2 <= ell` holds and is tight
        (`= 19 = ell`).

Hidden self-test: `python3 verify_l1_ell19_band_refuted.py
--tamper-selftest` flips one datum per gate (the witness `gamma`'s
leading coefficient, independently for each gate's own from-scratch
recomputation) and asserts each gate then FAILS -- proving every gate has
teeth. The shipped default is zero-arg.

All arithmetic is exact over F_p, stdlib only. No network, no CLI args
required for the default run, no filesystem reads outside this file.
"""
import sys
import time

ELL = 19
P = 571
M = 9                      # (ELL - 1) // 2 -- one below the (ELL+1)//2 onset
TARGET_2ELL = 2 * ELL      # 38

WITNESS = {
    "label": "m=9 p=571 (vacancy-band-refutation witness)",
    "ell": ELL, "m": M, "p": P, "n_cosets": (P - 1) // ELL,
    "gamma": [545, 15, 163, 341, 470, 274, 474, 224, 174, 556,
              179, 28, 321, 233, 543, 54, 203, 1],
    "E3": 20, "T": 5, "top8": 36, "top9": 38, "top10": 40,
}

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
# TWO independent spectrum implementations (gate i cross-check)
# =====================================================================================
def spectrum_coset_key(gamma, p, ell):
    """Implementation A: label F_p^* by coset key x^ell mod p (no generator
    needed), Horner-evaluate Gamma(x) = sum_{r=1}^{ell-1} gamma_r x^r
    (gamma has no constant term, so after a length-(ell-1) Horner pass
    over gamma as coefficients of x^0..x^(ell-2), one extra factor of x is
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

def T_third_onward(spec):
    """sigma-calculus residual quantity: sum_{k>=3}(mu_k-2)_+ computed on
    the descending spectrum FROM THE THIRD-LARGEST entry onward (excludes
    only the top two)."""
    s = sorted(spec, reverse=True)
    return sum(max(mu - 2, 0) for mu in s[2:])

def topk(spec, k):
    return sum(sorted(spec, reverse=True)[:k])

# =====================================================================================
# polynomial + linear-algebra machinery over F_p (fresh port, needed by
# run_witness_chain below -- same conventions as the integrated notes'
# own verifiers, reimplemented independently)
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
    the MODAL value achieved by that max fiber (needed by the
    lambda-free machinery below, and by gate iii/iv's per-coset counts)."""
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
# convention (gate names/semantics match
# experimental/scripts/verify_l1_ell19_attainment.py's own fresh port,
# itself independent of experimental/scripts/verify_l1_prime_ell_frontier_corrected.py);
# this copy is independent at runtime (no import of either).
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
# GATES (each returns (ok: bool, summary: str); tamper flips ONE guarded datum)
# =====================================================================================
def gate_i_spectrum(tamper=False):
    gamma = list(WITNESS["gamma"])
    p, ell = WITNESS["p"], WITNESS["ell"]
    if tamper:
        gamma[0] = (gamma[0] + 1) % p
    sA = spectrum_coset_key(gamma, p, ell)
    sB = spectrum_gen_walk(gamma, p, ell)
    agree = (sA == sB)
    e3 = E3(sA)
    tt = T_third_onward(sA)
    t8, t9, t10 = topk(sA, 8), topk(sA, 9), topk(sA, 10)
    ok = (agree and e3 == WITNESS["E3"] and tt == WITNESS["T"]
          and t8 == WITNESS["top8"] and t9 == WITNESS["top9"] and t10 == WITNESS["top10"])
    return ok, ("A==B=%s E3=%d(exp %d) T=%d(exp %d) top8=%d(exp %d) top9=%d(exp %d) top10=%d(exp %d)"
                % (agree, e3, WITNESS["E3"], tt, WITNESS["T"],
                   t8, WITNESS["top8"], t9, WITNESS["top9"], t10, WITNESS["top10"]))

def gate_ii_full_chain(tamper=False):
    gamma = list(WITNESS["gamma"])
    p, ell, m = WITNESS["p"], WITNESS["ell"], WITNESS["m"]
    if tamper:
        gamma[0] = (gamma[0] + 1) % p
    G, lam_free, full, top_m = run_witness_chain(gamma, p, ell, m, check_minimal=True)
    all16 = (len(G) == 16) and all(G.values())
    ok = all16 and full and lam_free and (top_m == WITNESS["top9"])
    return ok, ("all16=%s full=%s lam_free=%s top_m=%d(exp %d)"
                % (all16, full, lam_free, top_m, WITNESS["top9"]))

def gate_iii_reduction_formula(tamper=False):
    """Recompute a = #{cosets, OTHER than the single big-fiber coset, whose
    per-coset max fiber is >= 3}, directly from the witness's own spectrum,
    and check top-9 == 2*ell - 6 + a."""
    gamma = list(WITNESS["gamma"])
    p, ell = WITNESS["p"], WITNESS["ell"]
    if tamper:
        gamma[0] = (gamma[0] + 1) % p
    spec = spectrum_coset_key(gamma, p, ell)
    # the single largest entry is the planted big fiber; count how many of
    # the REMAINING entries are >= 3 (the "a" of the reduction formula).
    a = sum(1 for mu in spec[1:] if mu >= 3)
    t9 = topk(spec, 9)
    rhs = 2 * ell - 6 + a
    ok = (a == 6) and (t9 == rhs) and (t9 == WITNESS["top9"])
    return ok, ("a=%d(exp 6) top9=%d  2*ell-6+a=%d  identity holds=%s  crosses(a>=6)=%s"
                % (a, t9, rhs, t9 == rhs, a >= 6))

def gate_iv_structural(tamper=False):
    gamma = list(WITNESS["gamma"])
    p, ell, m = WITNESS["p"], WITNESS["ell"], WITNESS["m"]
    n = (p - 1) // ell
    if tamper:
        gamma[0] = (gamma[0] + 1) % p
    eligible = (n >= 2 * m - 1)
    n_nonzero = sum(1 for x in gamma if x % p)
    mixed = n_nonzero > 1
    spec = spectrum_coset_key(gamma, p, ell)
    mu1, mu2 = spec[0], spec[1]
    cap_ok = (mu1 + mu2 <= ell)
    cap_tight = (mu1 + mu2 == ell)
    ok = eligible and mixed and cap_ok and cap_tight
    return ok, ("eligible(n=%d>=2m-1=%d)=%s  mixed(%d nonzero coeffs)=%s  "
                "mu1+mu2=%d<=ell=%d tight=%s"
                % (n, 2 * m - 1, eligible, n_nonzero, mixed, mu1 + mu2, ell, cap_tight))

GATES = [
    ("(i)   witness (m=9,p=571) spectrum        ", gate_i_spectrum),
    ("(ii)  full 16-gate run_witness_chain       ", gate_ii_full_chain),
    ("(iii) reduction-formula (a=6) check        ", gate_iii_reduction_formula),
    ("(iv)  structural/eligibility checks        ", gate_iv_structural),
]

def main():
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 92)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is flipped")
    else:
        print(" verify_l1_ell19_band_refuted  (zero-arg)   m*(19) <= 9 -- vacancy band")
        print(" REFUTED at p=571 (experimental/notes/l1/l1_ell19_band_refuted.md)")
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
