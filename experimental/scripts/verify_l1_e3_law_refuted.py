#!/usr/bin/env python3
"""verify_l1_e3_law_refuted.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_e3_law_refuted.md`, which REFUTES:

  - the NEW KEY LEMMA CANDIDATE `E_3 <= ell` of
    `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (its Sec 3), and
  - the Residual Conjecture RC (`T >= 5 => E_3 <= ell`) of
    `experimental/notes/l1/l1_sigma_calculus.md`,

by six explicit, realizable, re-verified `Gamma` at `ell in {17, 23, 29}` with
observed maximum `E_3 = ell + 2`. Theorem 1 (`T <= 4 => E_3 <= ell`), the
pairwise cap, and the master identity all SURVIVE -- they hold *on* the six
counterexamples, which all live on the (still-conjectural) `T >= 5` chart.

Ground rule: self-contained. This script does NOT import from, edit, or
depend on any other script's claims being true (in particular it does not
import `verify_l1_sigma_calculus.py`; the sigma/dimU/rho machinery below is a
fresh port of that note's exact computational conventions, applied to a new
witness set). Every object is reconstructed here from its raw `gamma` alone,
via two independent spectrum sub-implementations, and every invariant
(`sigma`, `dimU`, `rho`, `E_3`, `T`, `K`) is computed here from scratch by
exact `F_p` linear algebra.

Seven gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)   spectrum / E_3 / mu1+mu2 / violation-margin recompute, all six
  (ii)  structural: constant-free + mixed, T>=5, n>=K, all six
  (iii) master identity sigma==E_3+K-ell+dimU + falsifier signature
        sigma>=K+dimU+1, all six (sigma/dimU/rho recomputed from scratch
        per the sigma-calculus conventions)
  (iv)  pairwise-cap sanity mu1+mu2<=ell, all six
  (v)   min-mu>=3 peel of W1, W2 preserves (E_3, T) exactly
  (vi)  realizability-free demo: [6,6] at ell=7 satisfies the master
        identity while violating the pairwise cap
  (vii) Theorem-1 boundary: the companion ell=19,p=647 attainment witnesses
        (m=10, m=11) have T<=4 -- disjoint chart from the six residual
        (T>=5) counterexamples above

Hidden self-test:  python3 verify_l1_e3_law_refuted.py --tamper-selftest
    flips one datum per gate class and asserts each gate then FAILS (proves
    every gate has teeth). The shipped default is zero-arg.

All arithmetic is exact over F_p, stdlib only. No network, no files, no CLI
args required. Runtime target < 60s.
"""
import sys
import time

# =====================================================================================
# exact F_p polynomial + linear-algebra arithmetic (self-contained; a fresh
# port of verify_l1_sigma_calculus.py's conventions -- NOT an import of it)
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

# =====================================================================================
# spectrum reconstruction: TWO independent implementations (grouped-by-x^ell
# Horner vs generator-coset power-sum), exactly as in verify_l1_sigma_calculus.py
# =====================================================================================
def gamma_eval(gamma, x, p):
    """Gamma(x) = sum_{r=1}^{ell-1} gamma[r-1] x^r  (constant-free)."""
    v = 0
    for c in reversed(gamma):
        v = (v * x + c) % p
    return v * x % p

def fibers_group_by_xell(gamma, p, ell):
    """Impl A: group F_p^* by x^ell, take the (x, value)-modal class per group."""
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
    return fibers

def fibers_coset_power_sum(gamma, p, ell):
    """Impl B: independent -- generator-power cosets g^i*H, ascending power-sum
    evaluation (no x^ell grouping, no Horner)."""
    g = find_gen(p)
    n = (p - 1) // ell
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    fibers = []
    for i in range(n):
        b = pow(g, i, p)
        pts = [b * h % p for h in H]
        w = pow(b, ell, p)
        byval = {}
        for x in pts:
            v = 0
            xr = 1
            for r in range(1, ell):
                xr = xr * x % p
                if gamma[r - 1]:
                    v = (v + gamma[r - 1] * xr) % p
            byval.setdefault(v, []).append(x)
        best_v = max(byval, key=lambda v: len(byval[v]))
        fibers.append((w, sorted(byval[best_v])))
    return fibers

def full_coset(W, ell, p):
    """All ell points x with x^ell == W (brute force; p is small throughout)."""
    return [x for x in range(1, p) if pow(x, ell, p) == W]

def build_config(gamma, p, ell):
    """Return (fibers [largest-first, mu>=2 only], Ws, specA, specA==specB)."""
    fA = fibers_group_by_xell(gamma, p, ell)
    fB = fibers_coset_power_sum(gamma, p, ell)
    specA = sorted((len(xs) for _, xs in fA), reverse=True)
    specB = sorted((len(xs) for _, xs in fB), reverse=True)
    match = (specA == specB)
    fibers_all = [xs for _, xs in fA if len(xs) >= 2]
    Ws_all = [w for w, xs in fA if len(xs) >= 2]
    order = sorted(range(len(fibers_all)), key=lambda i: -len(fibers_all[i]))
    fibers = [fibers_all[i] for i in order]
    Ws = [Ws_all[i] for i in order]
    return fibers, Ws, specA, match

class Config:
    """A reconstructed config: K max-fibers (largest-first), with all sigma
    calculus invariants computed from scratch (a fresh port of
    verify_l1_sigma_calculus.py's Config; not imported)."""
    def __init__(self, gamma, p, ell):
        self.gamma, self.p, self.ell = gamma, p, ell
        self.fibers, self.Ws, self.spectrum, self.spec_match = build_config(gamma, p, ell)
        self.K = len(self.fibers)
        self.mus = [len(F) for F in self.fibers]
        self.P = sum(self.mus)
        self.E3 = sum(mu - 2 for mu in self.mus)
        self.n = (p - 1) // ell
        self.gks = [poly_from_roots(F, p) for F in self.fibers]
        self.hks = []
        for k in range(self.K):
            xell = [0] * ell + [1]
            num = padd(xell, [(-self.Ws[k]) % p], p)
            self.hks.append(poly_div_exact(num, self.gks[k], p))

def fiber_generators(cfg, k):
    """The mu_k-1 generator vectors X^d*h_k (d=0..mu_k-2), as length-(ell-1)
    coefficient vectors (degrees 0..ell-2) -- a basis for V_k."""
    ell, p = cfg.ell, cfg.p
    hk = cfg.hks[k]
    mu = cfg.mus[k]
    gens = []
    for d in range(mu - 1):
        prod = pmul([0] * d + [1], hk, p)
        if len(prod) > ell - 1:
            raise AssertionError("a_k h_k exceeded the ell-2 degree bound")
        gens.append(prod + [0] * (ell - 1 - len(prod)))
    return gens

def dim_Vsum_via_syzygy(cfg):
    vecs = []
    for k in range(cfg.K):
        vecs.extend(fiber_generators(cfg, k))
    return rank_Fp(vecs, cfg.ell - 1, cfg.p)

def sigma_via_syzygy(cfg):
    return (cfg.P - cfg.K) - dim_Vsum_via_syzygy(cfg)

def vpow(x, ell, p):
    return [pow(x, r, p) for r in range(1, ell)]

def pattern_rows(cfg):
    ell, p = cfg.ell, cfg.p
    rows = []
    for F in cfg.fibers:
        if len(F) < 2:
            continue
        v0 = vpow(F[0], ell, p)
        for x in F[1:]:
            vx = vpow(x, ell, p)
            rows.append([(v0[r] - vx[r]) % p for r in range(ell - 1)])
    return rows

def rho_dim(cfg):
    return rank_Fp(pattern_rows(cfg), cfg.ell - 1, cfg.p)

def dimU_dim(cfg):
    return cfg.ell - rho_dim(cfg)

def Tval_mus(mus):
    """T = sum_{k>=3}(mu_k-2)_+ on the descending spectrum from the THIRD
    largest fiber onward (mus assumed already sorted descending)."""
    return sum(mu - 2 for mu in mus[2:] if mu >= 3)

def E3_mus(mus):
    return sum(mu - 2 for mu in mus if mu >= 3)

# =====================================================================================
# the six E_3<=ell law-refutation witnesses (verbatim gammas from
# experimental/notes/l1/l1_e3_law_refuted.md Sec 1 and the certificate JSON;
# "expect" = the note's claimed invariants, independently cross-checked via
# lane-B2 tooling before shipping -- this verifier recomputes every one of
# them from scratch and must reproduce "expect" exactly)
# =====================================================================================
WITNESSES = [
    {"id": "W3", "ell": 17, "p": 137,
     "gamma": [95, 83, 94, 43, 16, 101, 72, 52, 93, 129, 47, 76, 80, 45, 64, 1],
     "expect": {"spectrum": [14, 3, 3, 3, 3, 3, 3, 3], "E3": 19, "T": 6, "K": 8,
                "mu1_plus_mu2": 17, "cap_tight": True, "rho": 15, "dimU": 2, "sigma": 12, "n": 8}},
    {"id": "W1", "ell": 29, "p": 233,
     "gamma": [126, 24, 50, 214, 172, 207, 131, 212, 64, 48, 179, 143, 189, 59,
               86, 107, 196, 67, 125, 47, 63, 162, 110, 189, 69, 218, 156, 1],
     "expect": {"spectrum": [15, 14, 4, 3, 3, 3, 2, 2], "E3": 30, "T": 5, "K": 8,
                "mu1_plus_mu2": 29, "cap_tight": True, "rho": 27, "dimU": 2, "sigma": 11, "n": 8}},
    {"id": "W2", "ell": 23, "p": 139,
     "gamma": [91, 120, 12, 78, 12, 136, 48, 11, 118, 111, 69, 66, 43, 110, 6,
               14, 54, 38, 104, 2, 76, 1],
     "expect": {"spectrum": [14, 9, 4, 4, 3, 2], "E3": 24, "T": 5, "K": 6,
                "mu1_plus_mu2": 23, "cap_tight": True, "rho": 21, "dimU": 2, "sigma": 9, "n": 6}},
    {"id": "EXTRA1_ell29_p233_a", "ell": 29, "p": 233,
     "gamma": [17, 195, 160, 138, 183, 48, 208, 127, 215, 127, 165, 216, 5, 154,
               15, 168, 221, 41, 15, 96, 205, 78, 67, 200, 8, 208, 182, 1],
     "expect": {"spectrum": [20, 9, 4, 3, 3, 3, 2, 2], "E3": 30, "T": 5, "K": 8,
                "mu1_plus_mu2": 29, "cap_tight": True, "rho": 27, "dimU": 2, "sigma": 11, "n": 8}},
    {"id": "EXTRA2_ell29_p233_b", "ell": 29, "p": 233,
     "gamma": [83, 0, 6, 232, 143, 192, 212, 48, 86, 182, 127, 17, 104, 134,
               194, 213, 17, 205, 118, 19, 45, 203, 39, 182, 145, 212, 102, 1],
     "expect": {"spectrum": [16, 13, 4, 3, 3, 3, 2, 2], "E3": 30, "T": 5, "K": 8,
                "mu1_plus_mu2": 29, "cap_tight": True, "rho": 27, "dimU": 2, "sigma": 11, "n": 8}},
    {"id": "EXTRA3_ell17_p103", "ell": 17, "p": 103,
     "gamma": [1, 30, 67, 2, 86, 41, 28, 85, 62, 87, 80, 84, 36, 89, 76, 1],
     "expect": {"spectrum": [11, 5, 5, 4, 3, 2], "E3": 18, "T": 6, "K": 6,
                "mu1_plus_mu2": 16, "cap_tight": False, "rho": 15, "dimU": 2, "sigma": 9, "n": 6}},
]

# W1, W2 peeled (min-mu>=3, drop the size-2 fibers) forms, per the note Sec 2 item 2
PEEL_TARGETS = {
    "W1": [15, 14, 4, 3, 3, 3],
    "W2": [14, 9, 4, 4, 3],
}

# =====================================================================================
# companion ell=19, p=647 attainment witnesses (concurrent companion note,
# disjoint chart): both gammas embedded verbatim for gate vii
# =====================================================================================
ATTAINMENT = [
    {"id": "ATT_m10", "ell": 19, "p": 647, "m": 10,
     "gamma": [298, 638, 143, 294, 14, 111, 237, 78, 464, 166, 355, 385, 207,
               68, 465, 369, 316, 1],
     "expect_T": 3, "expect_E3": 18},
    {"id": "ATT_m11", "ell": 19, "p": 647, "m": 11,
     "gamma": [318, 474, 374, 319, 297, 217, 24, 346, 0, 609, 514, 362, 499,
               309, 174, 383, 93, 1],
     "expect_T": 2, "expect_E3": 17},
]

def make_config(w, tamper=False):
    gamma = list(w["gamma"])
    if tamper:
        gamma[0] = (gamma[0] + 1) % w["p"]
    return Config(gamma, w["p"], w["ell"])

# =====================================================================================
# GATES (each returns (ok: bool, summary: str))
# =====================================================================================
def gate_i_spectrum(tamper=False):
    ok = True
    lines = []
    for wi, w in enumerate(WITNESSES):
        cfg = make_config(w, tamper=(tamper and wi == 0))
        exp = w["expect"]
        spec_ok = (cfg.spectrum == exp["spectrum"]) and cfg.spec_match
        e3_ok = (cfg.E3 == exp["E3"])
        m1m2 = cfg.mus[0] + cfg.mus[1]
        m1m2_ok = (m1m2 == exp["mu1_plus_mu2"])
        margin_ok = (cfg.E3 - cfg.ell == exp["E3"] - w["ell"])
        good = spec_ok and e3_ok and m1m2_ok and margin_ok
        ok = ok and good
        lines.append("%s: specA==specB==expect:%s E3=%d(expect %d) mu1+mu2=%d margin(E3-ell)=%+d"
                      % (w["id"], spec_ok, cfg.E3, exp["E3"], m1m2, cfg.E3 - cfg.ell))
    return ok, " | ".join(lines)

def gate_ii_structural(tamper=False):
    ok = True
    lines = []
    for wi, w in enumerate(WITNESSES):
        gamma = list(w["gamma"])
        if tamper and wi == 0:
            gamma = [0] * len(gamma)  # break mixedness
        ell, p = w["ell"], w["p"]
        len_ok = (len(gamma) == ell - 1)
        mixed_ok = sum(1 for c in gamma if c % p) >= 2  # monomials are not mixed
        range_ok = all(0 <= c < p for c in gamma)
        ell_prime_ok = is_prime(ell)
        pair_ok = is_prime(p) and ((p - 1) % ell == 0)
        cfg = Config(w["gamma"], p, ell)  # untampered recompute for T/n/K (mixedness checked above)
        T = Tval_mus(cfg.mus)
        n = cfg.n
        t_ok = (T >= 5) and (T == w["expect"]["T"])
        n_ok = (n == w["expect"]["n"]) and (n >= cfg.K)
        # W3 near-miss closure (note §4): spectrum-side gate crossing at m=(ell-1)/2,
        # blocked from a codeword only by n < 2m-1
        w3_ok = True
        if w["id"] == "W3":
            mm = (w["ell"] - 1) // 2
            topm = sum(sorted(cfg.mus, reverse=True)[:mm])
            w3_ok = (topm == 35) and (topm >= 2 * w["ell"]) and (n < 2 * mm - 1)
        good = len_ok and mixed_ok and range_ok and ell_prime_ok and pair_ok and t_ok and n_ok and w3_ok
        ok = ok and good
        lines.append("%s: len==ell-1:%s mixed:%s ell_prime:%s ell|p-1:%s T=%d(>=5:%s) n=%d>=K=%d:%s"
                      % (w["id"], len_ok, mixed_ok, ell_prime_ok, pair_ok, T, T >= 5, n, cfg.K, n_ok))
    return ok, " | ".join(lines)

def gate_iii_master_identity(tamper=False):
    off = 1 if tamper else 0
    ok = True
    lines = []
    for w in WITNESSES:
        cfg = make_config(w)
        sig = sigma_via_syzygy(cfg)
        rho = rho_dim(cfg)
        dU = dimU_dim(cfg)
        exp = w["expect"]
        rho_ok = (rho == exp["rho"])
        dU_ok = (dU == exp["dimU"])
        sig_ok = (sig == exp["sigma"])
        claimed_sig = sig + off
        master_ok = (claimed_sig == cfg.E3 + cfg.K - cfg.ell + dU)
        falsifier_ok = (claimed_sig >= cfg.K + dU + 1)
        good = rho_ok and dU_ok and sig_ok and master_ok and falsifier_ok
        ok = ok and good
        lines.append("%s: rho=%d(exp %d) dimU=%d(exp %d) sigma=%d(exp %d) master(sigma==E3+K-ell+dimU):%s falsifier(sigma>=K+dimU+1):%s"
                      % (w["id"], rho, exp["rho"], dU, exp["dimU"], sig, exp["sigma"], master_ok, falsifier_ok))
    return ok, " | ".join(lines)

def gate_iv_pairwise_cap(tamper=False):
    ok = True
    lines = []
    for w in WITNESSES:
        cfg = make_config(w)
        m1m2 = cfg.mus[0] + cfg.mus[1]
        bound = cfg.ell - (1 if tamper else 0)  # tamper: falsely tighten by 1
        cap_ok = (m1m2 <= bound)
        tight_ok = ((m1m2 == cfg.ell) == w["expect"]["cap_tight"])
        good = cap_ok and tight_ok
        ok = ok and good
        lines.append("%s: mu1+mu2=%d <= ell=%d : %s (cap_tight=%s expect=%s)"
                      % (w["id"], m1m2, cfg.ell, cap_ok, m1m2 == cfg.ell, w["expect"]["cap_tight"]))
    return ok, " | ".join(lines)

def gate_v_peel(tamper=False):
    ok = True
    lines = []
    for wid, target in PEEL_TARGETS.items():
        w = next(x for x in WITNESSES if x["id"] == wid)
        cfg = Config(w["gamma"], w["p"], w["ell"])
        peeled = [m for m in cfg.mus if m >= 3]
        if tamper:
            peeled = peeled[:-1] if len(peeled) > 1 else peeled  # corrupt: drop one min-mu>=3 fiber too
        peel_match = (peeled == target)
        e3_before, e3_after = E3_mus(cfg.mus), E3_mus(peeled)
        t_before, t_after = Tval_mus(cfg.mus), Tval_mus(peeled)
        preserved = (e3_before == e3_after) and (t_before == t_after)
        good = peel_match and preserved
        ok = ok and good
        lines.append("%s: peeled=%s(expect %s, match=%s) E3 %d->%d T %d->%d preserved=%s"
                      % (wid, peeled, target, peel_match, e3_before, e3_after, t_before, t_after, preserved))
    return ok, " | ".join(lines)

def build_manual_fiber_config(fibers, Ws, ell, p):
    """A Config-like object built directly from explicit (fiber, coset-label)
    pairs, with NO underlying Gamma required (realizability-free). Only the
    fields needed for the sigma/dimU/rho/E3 computation are populated."""
    cfg = Config.__new__(Config)
    cfg.gamma, cfg.p, cfg.ell = None, p, ell
    cfg.fibers = fibers
    cfg.Ws = Ws
    order = sorted(range(len(fibers)), key=lambda i: -len(fibers[i]))
    cfg.fibers = [fibers[i] for i in order]
    cfg.Ws = [Ws[i] for i in order]
    cfg.spectrum = sorted((len(F) for F in fibers), reverse=True)
    cfg.spec_match = True
    cfg.K = len(cfg.fibers)
    cfg.mus = [len(F) for F in cfg.fibers]
    cfg.P = sum(cfg.mus)
    cfg.E3 = sum(mu - 2 for mu in cfg.mus)
    cfg.n = None
    cfg.gks = [poly_from_roots(F, p) for F in cfg.fibers]
    cfg.hks = []
    for k in range(cfg.K):
        xell = [0] * ell + [1]
        num = padd(xell, [(-cfg.Ws[k]) % p], p)
        cfg.hks.append(poly_div_exact(num, cfg.gks[k], p))
    return cfg

def gate_vi_realizability_free_demo(tamper=False):
    """The [6,6] profile at ell=7: two size-(ell-1) fibers on two DISTINCT
    cosets of F_29^* (7 | 28), each an arbitrary 6-of-7 subset of its coset
    (no realizing Gamma is constructed or required). Demonstrates that the
    master identity sigma=E_3+K-ell+dimU holds even though mu_1+mu_2=12>7=ell
    (excluded by the PROVED pairwise cap for any REALIZABLE Gamma) -- i.e.
    the identity is pure linear bookkeeping, not a consequence of
    realizability. Expect sigma=4=8+2-7+1 (dimU=1), matching the note Sec 2
    item 1 exactly."""
    ell, p = 7, 29
    g = find_gen(p)
    n = (p - 1) // ell
    zeta = pow(g, n, p)
    H = sorted(pow(zeta, j, p) for j in range(ell))
    coset0 = sorted(H)                                  # c=1 * H
    coset1 = sorted((g * h) % p for h in H)              # c=g * H (distinct label)
    W0, W1 = pow(coset0[0], ell, p), pow(coset1[0], ell, p)
    assert W0 != W1, "cosets must be distinct for the demo to be meaningful"
    F1 = coset0[:-1]   # drop one arbitrary point (any choice gives the same sigma/dimU -- see note Sec 2 item 1)
    F2 = coset1[:-1]
    mus_ok = (len(F1) == 6) and (len(F2) == 6)
    cfg = build_manual_fiber_config([F1, F2], [W0, W1], ell, p)
    sig = sigma_via_syzygy(cfg)
    rho = rho_dim(cfg)
    dU = dimU_dim(cfg)
    m1m2 = cfg.mus[0] + cfg.mus[1]
    cap_violated = (m1m2 > ell)
    claimed_sig = sig + (1 if tamper else 0)
    master_ok = (claimed_sig == cfg.E3 + cfg.K - ell + dU)
    values_ok = (cfg.E3 == 8) and (cfg.K == 2) and (sig == 4) and (dU == 1) and (rho == 6)
    ok = mus_ok and cap_violated and master_ok and values_ok
    return ok, ("ell=7 p=29 F1=%s F2=%s (distinct cosets W0=%d,W1=%d): E3=%d K=%d rho=%d dimU=%d sigma=%d "
                "(claimed=%d) master(sigma==E3+K-ell+dimU):%s mu1+mu2=%d>ell=%d(pairwise cap VIOLATED):%s"
                % (F1, F2, W0, W1, cfg.E3, cfg.K, rho, dU, sig, claimed_sig, master_ok, m1m2, ell, cap_violated))

def gate_vii_theorem1_boundary(tamper=False):
    ok = True
    lines = []
    for a in ATTAINMENT:
        cfg = make_config(a)
        T = Tval_mus(cfg.mus)
        e3_ok = (cfg.E3 == a["expect_E3"])
        t_ok = (T == a["expect_T"])
        bound = 4 - (3 if tamper else 0)  # tamper: falsely tighten Theorem-1 boundary to 1 (< both T=3, T=2)
        covered_ok = (T <= bound)
        good = e3_ok and t_ok and covered_ok
        ok = ok and good
        lines.append("%s: ell=%d p=%d m=%d E3=%d(exp %d) T=%d(exp %d) T<=%d:%s [disjoint from the T>=5 residual witnesses above]"
                      % (a["id"], a["ell"], a["p"], a["m"], cfg.E3, a["expect_E3"], T, a["expect_T"], bound, covered_ok))
    return ok, " | ".join(lines)

GATES = [
    ("(i)   spectrum / E3 / mu1+mu2 / margin      ", gate_i_spectrum),
    ("(ii)  structural (constfree/mixed/T>=5/n>=K)", gate_ii_structural),
    ("(iii) master identity + falsifier signature ", gate_iii_master_identity),
    ("(iv)  pairwise-cap sanity                   ", gate_iv_pairwise_cap),
    ("(v)   min-mu>=3 peel (W1, W2)                ", gate_v_peel),
    ("(vi)  realizability-free demo ([6,6] ell=7)  ", gate_vi_realizability_free_demo),
    ("(vii) Theorem-1 boundary (ell=19 attainment) ", gate_vii_theorem1_boundary),
]

def main():
    # data-presence guards: gates must never vacuously pass on empty input
    assert len(WITNESSES) == 6, "expected 6 witnesses"
    assert len(PEEL_TARGETS) == 2, "expected 2 peel targets"
    assert len(ATTAINMENT) == 2, "expected 2 attainment witnesses"
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 94)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum/claim is corrupted")
    else:
        print(" verify_l1_e3_law_refuted  (zero-arg)   E_3<=ell REFUTED at T>=5 (max E_3=ell+2)")
        print(" (experimental/notes/l1/l1_e3_law_refuted.md)")
    print("=" * 94)
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
    print("=" * 94)
    if selftest:
        print(" SELF-TEST RESULT: %s   (%.1fs)"
              % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)" % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)

if __name__ == "__main__":
    main()
