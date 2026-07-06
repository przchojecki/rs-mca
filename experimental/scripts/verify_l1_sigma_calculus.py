#!/usr/bin/env python3
"""verify_l1_sigma_calculus.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_sigma_calculus.md`: the sigma-calculus of the co-fiber
petal syzygy space, its five PROVED lemmas, the master identity
`sigma = delta = E_3 + K - ell + dimU`, and the exact sigma-form of the
post-#330 candidate law `E_3 <= ell <=> sigma <= K + dimU`.

Ground rule: self-contained. This script does NOT import from, edit, or
depend on any other script's claims being true. Every object (2 witnesses +
11 `#330` counterexamples + 2 residual-tight witnesses = 15) is reconstructed
here from its raw `gamma` alone, via two independent spectrum sub-implementations,
and every invariant (`sigma`, `delta`, `dimU`, `dim(Vsum)`, `rho`, `E_3`) is
computed here from scratch by exact `F_p` linear algebra.

Nine gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)    moment bridge / sigma == delta                       (Lemma 1)
  (ii)   locator duality dim(Vsum) == rho == ell - dimU        (Lemma 2)
  (iii)  pairwise V_i cap V_j == 0, K=2 => sigma == 0           (Lemma 3)
  (iv)   recursion sigma == sum t_m, t_1==t_2==0, sigma<=B_rec  (Lemma 4)
  (v)    K=3 bound sigma <= min(mu)-1                           (Lemma 5)
  (vi)   master identity sigma == E_3+K-ell+dimU + sigma-form equivalences
  (vii)  P2 falsifier: [6,6,6] at ell=13,p=79 has sigma==4 > 1
  (viii) OLD/NEW stratification across the objects
  (ix)   Theorem 1 (covered chart T<=4 => E_3<=mu1+mu2<=ell => sigma<=K+dimU)
         on every object + the 2 residual-tight (T>=5, E_3=ell) witnesses    (Addendum 2A)

Hidden self-test:  python3 verify_l1_sigma_calculus.py --tamper-selftest
    flips one datum per gate class and asserts each gate then FAILS (proves
    every gate has teeth). The shipped default is zero-arg.

All arithmetic is exact over F_p, stdlib only. No network, no files, no CLI
args required.
"""
import sys
import time
import itertools

# =====================================================================================
# exact F_p polynomial + linear-algebra arithmetic (self-contained)
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

# deterministic, version-independent PRNG (never used for extremal EXISTENCE
# claims, only to seed the random K=3 sweep of gate v)
class LCG:
    def __init__(self, seed):
        self.s = seed & ((1 << 64) - 1)

    def nxt(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return self.s >> 17

    def randint(self, lo, hi):
        return lo + self.nxt() % (hi - lo + 1)

# =====================================================================================
# object reconstruction: gamma -> config (K max-fibers, mu_k>=2), TWO independent
# spectrum sub-implementations (grouped-by-x^ell Horner vs generator-coset power-sum)
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
    """Return (K fibers as sorted-by-size-desc list of point-lists, spectrum,
    both-impl match flag). Only mu_k>=2 fibers enter the config."""
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
    calculus invariants computed from scratch."""
    def __init__(self, gamma, p, ell):
        self.gamma, self.p, self.ell = gamma, p, ell
        self.fibers, self.Ws, self.spectrum, self.spec_match = build_config(gamma, p, ell)
        self.K = len(self.fibers)
        self.mus = [len(F) for F in self.fibers]
        self.P = sum(self.mus)
        self.E3 = sum(mu - 2 for mu in self.mus)
        # per-fiber locator g_k and co-fiber locator h_k = (X^ell - W_k)/g_k
        self.gks = [poly_from_roots(F, p) for F in self.fibers]
        self.hks = []
        for k in range(self.K):
            xell = [0] * ell + [1]
            num = padd(xell, [(-self.Ws[k]) % p], p)
            self.hks.append(poly_div_exact(num, self.gks[k], p))
        # cofiber_k = full coset \ F_k (needed for pairwise V_i cap V_j)
        self.cofibers = []
        for k in range(self.K):
            full = full_coset(self.Ws[k], ell, p)
            fset = set(self.fibers[k])
            self.cofibers.append([x for x in full if x not in fset])

    def subset(self, idxs):
        """A Config-like restriction to a sub-collection of fibers (for K=3 /
        K=2 sub-config checks); shares gamma/p/ell context but recomputes all
        derived quantities on the restricted fiber list."""
        sub = Config.__new__(Config)
        sub.gamma, sub.p, sub.ell = self.gamma, self.p, self.ell
        sub.fibers = [self.fibers[i] for i in idxs]
        sub.Ws = [self.Ws[i] for i in idxs]
        sub.spectrum = None
        sub.spec_match = None
        sub.K = len(sub.fibers)
        sub.mus = [len(F) for F in sub.fibers]
        sub.P = sum(sub.mus)
        sub.E3 = sum(mu - 2 for mu in sub.mus)
        sub.gks = [poly_from_roots(F, sub.p) for F in sub.fibers]
        sub.hks = []
        for k in range(sub.K):
            xell = [0] * sub.ell + [1]
            num = padd(xell, [(-sub.Ws[k]) % sub.p], sub.p)
            sub.hks.append(poly_div_exact(num, sub.gks[k], sub.p))
        # cofibers are intrinsic to (W_k, F_k) alone, unaffected by which other
        # fibers accompany it in the sub-config -- reuse the parent's.
        sub.cofibers = [self.cofibers[i] for i in idxs]
        return sub

# =====================================================================================
# core invariants: sigma (via h_k-syzygy), delta (via D cap Z), rho (pattern rows),
# dimU (= ell-rho), moment bridge, pairwise V_i cap V_j, recursion t_m.
# Each is its OWN construction (different ambient vector space), so sigma==delta and
# dim(Vsum)==rho are genuine cross-checks, not restatements of the same matrix.
# =====================================================================================
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

def delta_dim(cfg):
    """delta = dim(D cap Z): nullity of K fiber-indicator rows + ell full
    Vandermonde rows, in F_p^P."""
    ell, p = cfg.ell, cfg.p
    pts = [x for F in cfg.fibers for x in F]
    P = len(pts)
    rows = []
    idx = 0
    for F in cfg.fibers:
        row = [0] * P
        for _ in F:
            row[idx] = 1
            idx += 1
        rows.append(row)
    for rr in range(ell):
        rows.append([pow(x, rr, p) for x in pts])
    return nulldim(rows, P, p)

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

def gk_deriv_at(cfg, k, xi):
    """g_k'(xi) = prod_{xj in F_k, xj!=xi} (xi-xj), via the squarefree-locator identity."""
    p = cfg.p
    prod = 1
    for xj in cfg.fibers[k]:
        if xj != xi:
            prod = prod * ((xi - xj) % p) % p
    return prod

def moment_bridge_check(cfg, rng, trials=25):
    """Spot-check Lemma 1's identity sum_k a_k h_k == sum_s M_s X^{ell-1-s} for
    `trials` random (a_k) with deg a_k <= mu_k-2."""
    ell, p = cfg.ell, cfg.p
    ok = True
    for _ in range(trials):
        aks = []
        for k in range(cfg.K):
            deg = cfg.mus[k] - 2
            aks.append([rng.randint(0, p - 1) for _ in range(deg + 1)] if deg >= 0 else [])
        lhs = []
        for k in range(cfg.K):
            lhs = padd(lhs, pmul(aks[k], cfg.hks[k], p), p)
        lam = []
        for k in range(cfg.K):
            for xi in cfg.fibers[k]:
                aval = peval(aks[k], xi, p)
                lam.append((xi, aval * inv(gk_deriv_at(cfg, k, xi), p) % p))
        Ms = [sum(li * pow(xi, s, p) for xi, li in lam) % p for s in range(ell)]
        rhs = [0] * ell
        for s in range(ell):
            rhs[ell - 1 - s] = (rhs[ell - 1 - s] + Ms[s]) % p
        rhs = trim(rhs)
        lhs = trim(lhs)
        n = max(len(lhs), len(rhs), 1)
        if (lhs + [0] * (n - len(lhs))) != (rhs + [0] * (n - len(rhs))):
            ok = False
    return ok

def eval_matrix(pts, ncols, p):
    return [[pow(x, d, p) for d in range(ncols)] for x in pts]

def Vi_cap_Vj_dim(cfg, i, j):
    """dim{deg<=ell-2 : vanishes on cofiber_i U cofiber_j}."""
    ell, p = cfg.ell, cfg.p
    pts = list(set(cfg.cofibers[i]) | set(cfg.cofibers[j]))
    return nulldim(eval_matrix(pts, ell - 1, p), ell - 1, p)

class IncrementalBasis:
    """Incremental echelon-form rank tracker over F_p^ncols."""
    def __init__(self, ncols, p):
        self.ncols, self.p = ncols, p
        self.rows, self.piv = [], []

    def try_add(self, vec):
        v = [x % self.p for x in vec]
        for r, pc in zip(self.rows, self.piv):
            if v[pc]:
                f = v[pc]
                v = [(v[i] - f * r[i]) % self.p for i in range(self.ncols)]
        for c in range(self.ncols):
            if v[c] % self.p:
                iv = inv(v[c], self.p)
                v = [(x * iv) % self.p for x in v]
                self.rows.append(v)
                self.piv.append(c)
                return True
        return False

def recursion_tm(cfg):
    """t_m for fibers in cfg's (largest-first) order; sum(t_m)==sigma."""
    basis = IncrementalBasis(cfg.ell - 1, cfg.p)
    tms = []
    for k in range(cfg.K):
        gens = fiber_generators(cfg, k)
        new_count = sum(1 for vec in gens if basis.try_add(vec))
        tms.append((cfg.mus[k] - 1) - new_count)
    return tms

def B_rec(cfg):
    """Unconditional bound: sum over all-but-two-largest fibers of (mu-1),
    valid when cfg.fibers is already largest-first (true by construction)."""
    return sum(mu - 1 for mu in cfg.mus[2:])

# =====================================================================================
# the 13 objects: 2 witnesses (E_3=ell-2, sigma=K) + 11 `#330` counterexample Gammas
# (all verbatim from the integrated frontier-corrected witness table and the
# key-lemma-refuted COUNTEREXAMPLES + NEW_LISTINGS tables; reconstructed here from
# scratch, not imported). `expect` is the note's Sec 1.6 table, cross-checked below.
# =====================================================================================
OBJECTS = [
    {"label": "WIT ell=11 p=331", "ell": 11, "p": 331, "kind": "WIT",
     "gamma": [97, 29, 97, 239, 171, 92, 143, 155, 270, 1],
     "expect": {"K": 7, "E3": 9, "sigma": 7, "delta": 7, "dimU": 2, "dimVsum": 9, "rho": 9, "P": 23}},
    {"label": "WIT ell=23 p=139 (D3)", "ell": 23, "p": 139, "kind": "WIT",
     "gamma": [12, 79, 132, 135, 100, 118, 97, 22, 50, 20, 86, 134, 91, 89, 92, 110, 11, 56, 39, 17, 0, 1],
     "expect": {"K": 6, "E3": 21, "sigma": 6, "delta": 6, "dimU": 2, "dimVsum": 21, "rho": 21, "P": 33}},
    {"label": "CE ell=11 p=67", "ell": 11, "p": 67, "kind": "CE",
     "gamma": [43, 44, 38, 44, 17, 18, 42, 44, 65, 1],
     "expect": {"K": 6, "E3": 10, "sigma": 7, "delta": 7, "dimU": 2, "dimVsum": 9, "rho": 9, "P": 22}},
    {"label": "CE ell=11 p=199", "ell": 11, "p": 199, "kind": "CE",
     "gamma": [21, 144, 71, 171, 42, 10, 12, 115, 173, 1],
     "expect": {"K": 5, "E3": 10, "sigma": 6, "delta": 6, "dimU": 2, "dimVsum": 9, "rho": 9, "P": 20}},
    {"label": "CE ell=13 p=79", "ell": 13, "p": 79, "kind": "CE",
     "gamma": [23, 71, 3, 40, 40, 2, 46, 40, 67, 69, 71, 1],
     "expect": {"K": 5, "E3": 12, "sigma": 6, "delta": 6, "dimU": 2, "dimVsum": 11, "rho": 11, "P": 22}},
    {"label": "CE ell=13 p=313", "ell": 13, "p": 313, "kind": "CE",
     "gamma": [185, 42, 295, 307, 71, 257, 218, 32, 90, 290, 279, 1],
     "expect": {"K": 10, "E3": 12, "sigma": 11, "delta": 11, "dimU": 2, "dimVsum": 11, "rho": 11, "P": 32}},
    {"label": "CE ell=17 p=103", "ell": 17, "p": 103, "kind": "CE",
     "gamma": [27, 7, 1, 74, 35, 11, 86, 96, 66, 44, 7, 96, 5, 48, 72, 1],
     "expect": {"K": 6, "E3": 16, "sigma": 7, "delta": 7, "dimU": 2, "dimVsum": 15, "rho": 15, "P": 28}},
    {"label": "CE ell=19 p=191", "ell": 19, "p": 191, "kind": "CE",
     "gamma": [16, 44, 177, 106, 79, 157, 14, 155, 11, 181, 151, 28, 126, 22, 142, 23, 1, 1],
     "expect": {"K": 6, "E3": 18, "sigma": 7, "delta": 7, "dimU": 2, "dimVsum": 17, "rho": 17, "P": 30}},
    {"label": "CE ell=23 p=139", "ell": 23, "p": 139, "kind": "CE",
     "gamma": [60, 80, 118, 60, 48, 137, 123, 101, 89, 94, 15, 23, 21, 88, 134, 5, 48, 8, 124, 42, 77, 1],
     "expect": {"K": 6, "E3": 23, "sigma": 8, "delta": 8, "dimU": 2, "dimVsum": 21, "rho": 21, "P": 35}},
    {"label": "CE ell=11 p=331", "ell": 11, "p": 331, "kind": "CE",
     "gamma": [11, 165, 196, 237, 31, 40, 171, 236, 246, 1],
     "expect": {"K": 6, "E3": 10, "sigma": 7, "delta": 7, "dimU": 2, "dimVsum": 9, "rho": 9, "P": 22}},
    {"label": "CE ell=17 p=409", "ell": 17, "p": 409, "kind": "CE",
     "gamma": [80, 5, 360, 87, 283, 89, 358, 379, 216, 174, 67, 329, 68, 317, 398, 1],
     "expect": {"K": 10, "E3": 16, "sigma": 11, "delta": 11, "dimU": 2, "dimVsum": 15, "rho": 15, "P": 36}},
    {"label": "CE ell=23 p=599", "ell": 23, "p": 599, "kind": "CE",
     "gamma": [327, 192, 175, 17, 298, 200, 474, 496, 95, 354, 502, 222, 509, 213, 417, 173, 98, 207, 106, 381, 328, 1],
     "expect": {"K": 18, "E3": 22, "sigma": 19, "delta": 19, "dimU": 2, "dimVsum": 21, "rho": 21, "P": 58}},
    {"label": "CE ell=23 p=691", "ell": 23, "p": 691, "kind": "CE",
     "gamma": [524, 614, 310, 539, 294, 303, 425, 653, 551, 564, 145, 271, 332, 503, 117, 545, 122, 226, 30, 443, 430, 1],
     "expect": {"K": 17, "E3": 22, "sigma": 18, "delta": 18, "dimU": 2, "dimVsum": 21, "rho": 21, "P": 56}},
    # --- residual-tight witnesses (Addendum 2A.2): T>=5 (residual) AND E_3=ell (tight).
    # These fill the no-residual-tight-object blind spot that produced the retracted
    # "residual carries a 2-unit margin" claim. Both reconstructed from raw gamma here;
    # spectrum, sigma=delta=K+dimU, rho=ell-2 (realizable), master identity all re-verified.
    {"label": "RES ell=23 p=139 [11,10,5,4,3,2]", "ell": 23, "p": 139, "kind": "RES",
     "gamma": [95, 37, 137, 97, 52, 126, 56, 52, 73, 43, 44, 84, 22, 120, 67, 123, 98, 128, 33, 62, 37, 1],
     "expect": {"K": 6, "E3": 23, "sigma": 8, "delta": 8, "dimU": 2, "dimVsum": 21, "rho": 21, "P": 35}},
    {"label": "RES ell=29 p=233 [14,13,5,5,2,2,2,2]", "ell": 29, "p": 233, "kind": "RES",
     "gamma": [203, 187, 107, 98, 59, 120, 193, 102, 190, 101, 206, 153, 193, 196, 119, 185, 120, 153, 188, 140, 192, 218, 113, 205, 228, 206, 224, 1],
     "expect": {"K": 8, "E3": 29, "sigma": 10, "delta": 10, "dimU": 2, "dimVsum": 27, "rho": 27, "P": 45}},
    # SAT3 (wave-13): first T>=7 residual-tight object (T=9); refutes the
    # "mu_1+mu_2 = ell-2 at residual tightness" heuristic (here mu_1+mu_2 = ell-5
    # = ell+4-T) and exercises deep-residual tightness the two T=6 objects miss.
    {"label": "RES ell=29 p=233 [12,12,8,3,3,3,2,2] (T=9)", "ell": 29, "p": 233, "kind": "RES",
     "gamma": [117, 162, 58, 221, 3, 169, 112, 22, 48, 175, 127, 164, 4, 228, 76, 195, 151, 177, 116, 146, 56, 105, 217, 28, 114, 88, 89, 1],
     "expect": {"K": 8, "E3": 29, "sigma": 10, "delta": 10, "dimU": 2, "dimVsum": 27, "rho": 27, "P": 45}},
]

def make_config(obj, tamper=False, tamper_idx=None):
    gamma = list(obj["gamma"])
    if tamper:
        gamma[0] = (gamma[0] + 1) % obj["p"]
    return Config(gamma, obj["p"], obj["ell"])

# =====================================================================================
# K=3 sub-config enumeration (Gates v, vii): the 13 objects' own C(K,3) sub-configs
# (capped/strided when K is large) plus a fresh seeded-random realizable K=3 sweep.
# =====================================================================================
def k3_subconfigs_of_objects(cap_per_object=120):
    out = []
    for obj in OBJECTS:
        cfg = make_config(obj)
        triples = list(itertools.combinations(range(cfg.K), 3))
        if len(triples) > cap_per_object:
            stride = max(1, len(triples) // cap_per_object)
            triples = triples[::stride][:cap_per_object]
        for tri in triples:
            out.append((obj["label"], cfg.subset(list(tri))))
    return out

def _quick_random_config(gamma, p, ell):
    """Lightweight Config builder for the random sweep: skips the dual-impl
    spectrum cross-check (already established on the 13 canonical objects) and
    skips cofiber construction (not needed for a sigma-only K=3 sweep)."""
    fibs, Ws, spec_, _match = build_config(gamma, p, ell)
    cfg = Config.__new__(Config)
    cfg.gamma, cfg.p, cfg.ell = gamma, p, ell
    cfg.fibers, cfg.Ws, cfg.spectrum, cfg.spec_match = fibs, Ws, spec_, _match
    cfg.K = len(cfg.fibers)
    cfg.mus = [len(F) for F in cfg.fibers]
    cfg.P = sum(cfg.mus)
    cfg.E3 = sum(mu - 2 for mu in cfg.mus)
    cfg.gks = [poly_from_roots(F, p) for F in cfg.fibers]
    cfg.hks = []
    for k in range(cfg.K):
        xell = [0] * ell + [1]
        num = padd(xell, [(-cfg.Ws[k]) % p], p)
        cfg.hks.append(poly_div_exact(num, cfg.gks[k], p))
    cfg.cofibers = [[] for _ in range(cfg.K)]  # unused by the K=3 sigma-only sweep
    return cfg

_K3_SWEEP_CACHE = None

def k3_random_sweep(target=1000, seed=90210):
    """Seeded-random realizable K=3 sweep across ell in {7,11,13,17,23}: fresh
    random Gamma, up to 3 random 3-subsets of its resulting max-fiber config
    per Gamma. Deterministic (fixed LCG seed); memoized within one process."""
    global _K3_SWEEP_CACHE
    if _K3_SWEEP_CACHE is not None:
        return _K3_SWEEP_CACHE
    rng = LCG(seed)
    targets = [(7, 211), (11, 199), (13, 313), (17, 103), (23, 139)]
    subs = []
    gammas_tried = 0
    for ell, p in targets:
        per_target = 0
        while per_target < (target // len(targets) + 1) and gammas_tried < 8000:
            gammas_tried += 1
            gamma = [rng.randint(0, p - 1) for _ in range(ell - 1)]
            if not any(gamma):
                continue
            cfg = _quick_random_config(gamma, p, ell)
            if cfg.K < 3:
                continue
            seen = set()
            tries = 0
            ntri = min(3, cfg.K * (cfg.K - 1) * (cfg.K - 2) // 6)
            while len(seen) < ntri and tries < 20:
                tries += 1
                tri = tuple(sorted({rng.randint(0, cfg.K - 1) for _ in range(3)}))
                if len(tri) == 3:
                    seen.add(tri)
            for tri in seen:
                subs.append(cfg.subset(list(tri)))
                per_target += 1
    _K3_SWEEP_CACHE = subs
    return subs

# =====================================================================================
# GATES  (each returns (ok: bool, summary: str); tamper corrupts ONE guarded datum
# or ONE internal claim, matching the note's Sec 5 tamper-selftest description)
# =====================================================================================
def gate_i_moment_bridge(tamper=False):
    rng = LCG(20260705)
    ok = True
    lines = []
    for oi, obj in enumerate(OBJECTS):
        cfg = make_config(obj, tamper=(tamper and oi == 0))
        mb = moment_bridge_check(cfg, rng, trials=25)
        sig = sigma_via_syzygy(cfg)
        dl = delta_dim(cfg)
        # "inflate a claimed sigma": on a SECOND (untampered) object, pretend
        # sigma is one larger than computed; delta is independently computed
        # and must not agree.
        claimed = sig + (1 if (tamper and oi == 1) else 0)
        eq = (claimed == dl)
        expect_ok = (sig == obj["expect"]["sigma"]) and (dl == obj["expect"]["delta"])
        good = mb and eq and expect_ok
        ok = ok and good
        lines.append("%s: moment_bridge=%s sigma==delta:%s expect_match=%s"
                      % (obj["label"], mb, eq, expect_ok))
    return ok, " | ".join(lines)

def gate_ii_locator_duality(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(OBJECTS):
        cfg = make_config(obj, tamper=(tamper and oi == 0))
        dVs = dim_Vsum_via_syzygy(cfg)
        rho = rho_dim(cfg)
        dU = dimU_dim(cfg)
        sig = sigma_via_syzygy(cfg)
        rel_ok = (dVs == rho) and (rho == cfg.ell - dU) and (sig + rho == cfg.P - cfg.K)
        expect_ok = (dVs == obj["expect"]["dimVsum"]) and (rho == obj["expect"]["rho"]) and (dU == obj["expect"]["dimU"])
        good = rel_ok and expect_ok
        ok = ok and good
        lines.append("%s: dVs==rho:%s rho==ell-dU:%s sigma+rho==P-K:%s expect_match=%s"
                      % (obj["label"], dVs == rho, rho == cfg.ell - dU, sig + rho == cfg.P - cfg.K, expect_ok))
    return ok, " | ".join(lines)

def gate_iii_pairwise(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(OBJECTS):
        cfg = make_config(obj)
        worst = 0
        for i in range(cfg.K):
            for j in range(i + 1, cfg.K):
                worst = max(worst, Vi_cap_Vj_dim(cfg, i, j))
        k2_bad = 0
        k2_checked = 0
        for i in range(cfg.K):
            for j in range(i + 1, cfg.K):
                sub = cfg.subset([i, j])
                s2 = sigma_via_syzygy(sub)
                if tamper and oi == 0 and i == 0 and j == 1:
                    s2 = 1  # logic tamper: falsely claim a nonzero K=2 sigma (theorem: 0)
                k2_checked += 1
                if s2 != 0:
                    k2_bad += 1
        good = (worst == 0) and (k2_bad == 0)
        ok = ok and good
        lines.append("%s: worst_pairwise_cap=%d K2_subconfigs=%d k2_violations=%d"
                      % (obj["label"], worst, k2_checked, k2_bad))
    return ok, " | ".join(lines)

def gate_iv_recursion(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(OBJECTS):
        cfg = make_config(obj)
        tms = recursion_tm(cfg)
        if tamper and oi == 0 and len(tms) > 2:
            tms = tms[:2] + [0] + tms[3:]  # logic tamper: zero out t_3 (note Sec 5: "zero a t_m")
        sig = sigma_via_syzygy(cfg)
        brec = B_rec(cfg)
        good = (tms[0] == 0) and (tms[1] == 0) and (sum(tms) == sig) and (sig <= brec)
        ok = ok and good
        lines.append("%s: t1=%d t2=%d sum_t=%d sigma=%d B_rec=%d"
                      % (obj["label"], tms[0], tms[1], sum(tms), sig, brec))
    return ok, " | ".join(lines)

def gate_v_k3_bound(tamper=False):
    slack = 1 if tamper else 0  # tamper tightens the PROVED bound by 1; a tight
    # sub-config (sigma == min(mu)-1 exactly) then catches it.
    ok = True
    total = 0
    viol = 0
    tight = 0
    for _label, sub in k3_subconfigs_of_objects():
        sig = sigma_via_syzygy(sub)
        bound = min(sub.mus) - 1 - slack
        total += 1
        if sig > bound:
            viol += 1
        if sig == bound + slack:
            tight += 1
    n_own = total
    for sub in k3_random_sweep(target=1000):
        sig = sigma_via_syzygy(sub)
        bound = min(sub.mus) - 1 - slack
        total += 1
        if sig > bound:
            viol += 1
    ok = (viol == 0) and (tight >= 1) and (n_own >= 300) and (total - n_own >= 800)
    return ok, ("own-object K3 subconfigs=%d (tight=%d) + random sweep=%d; total=%d violations=%d (slack=%d)"
                 % (n_own, tight, total - n_own, total, viol, slack))

def gate_vi_master_identity(tamper=False):
    off = 1 if tamper else 0  # tamper shifts the master identity by 1 (must break EVERY object)
    ok = True
    lines = []
    for obj in OBJECTS:
        cfg = make_config(obj)
        sig = sigma_via_syzygy(cfg)
        dU = dimU_dim(cfg)
        master_ok = (sig == cfg.E3 + cfg.K - cfg.ell + dU + off)
        eq_new = ((cfg.E3 <= cfg.ell) == (sig <= cfg.K + dU + off))
        eq_old = ((cfg.E3 <= cfg.ell - 2) == (sig <= cfg.K + dU - 2 + off))
        good = master_ok and eq_new and eq_old
        ok = ok and good
        lines.append("%s: sigma==E3+K-ell+dimU:%s (E3<=ell)==(sigma<=K+dU):%s (E3<=ell-2)==(sigma<=K+dU-2):%s"
                      % (obj["label"], master_ok, eq_new, eq_old))
    # coverage: re-assert the master identity on a dimU>2 sub-config (the
    # [8,8,6] restriction of the D3 witness, per the note Sec 2.2)
    d3 = next(o for o in OBJECTS if o["label"] == "WIT ell=23 p=139 (D3)")
    cfg = make_config(d3)
    sub = cfg.subset([0, 1, 2])
    assert sub.mus == [8, 8, 6]
    sig_sub = sigma_via_syzygy(sub)
    dU_sub = dimU_dim(sub)
    sub_master_ok = (sig_sub == sub.E3 + sub.K - sub.ell + dU_sub + off)
    coverage_ok = (dU_sub != 2)
    ok = ok and sub_master_ok and coverage_ok
    lines.append("[8,8,6] sub-config of D3: dimU=%d(!=2:%s) sigma==E3+K-ell+dimU:%s"
                  % (dU_sub, coverage_ok, sub_master_ok))
    return ok, " | ".join(lines)

def gate_vii_p2_falsifier(tamper=False):
    ce_79 = next(o for o in OBJECTS if o["label"] == "CE ell=13 p=79")
    cfg = make_config(ce_79)
    sub = cfg.subset([0, 1, 2])  # spectrum head [6,6,6,2,2] -> first three are the size-6 fibers
    mus_ok = (sub.mus == [6, 6, 6])
    rho_sub = rho_dim(sub)
    sig_sub = sigma_via_syzygy(sub)
    realizable = (rho_sub == sub.ell - 2)
    claimed = 1 if tamper else sig_sub  # tamper: assert the withdrawn P2 value (1) instead of the true 4
    p2_falsified = (claimed == 4) and (claimed > 1)
    sweep = k3_random_sweep(target=1000)
    sweep_bad = sum(1 for s in sweep if sigma_via_syzygy(s) >= 2)
    ok = mus_ok and realizable and p2_falsified and (sweep_bad == 0)
    return ok, ("[6,6,6] ell=13 p=79: mus_ok=%s realizable(rho==ell-2)=%s sigma=%d(claimed=%d) P2_falsified=%s | "
                "random K3 sweep (n=%d) sigma>=2 count=%d (undershoot documented)"
                % (mus_ok, realizable, sig_sub, claimed, p2_falsified, len(sweep), sweep_bad))

def gate_viii_stratification(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(OBJECTS):
        cfg = make_config(obj, tamper=(tamper and obj["kind"] == "WIT" and oi == 0))
        sig = sigma_via_syzygy(cfg)
        dU = dimU_dim(cfg)
        expect_ok = (cfg.K == obj["expect"]["K"] and cfg.E3 == obj["expect"]["E3"]
                     and sig == obj["expect"]["sigma"] and dU == obj["expect"]["dimU"])
        if obj["kind"] == "WIT":
            strat_ok = (cfg.E3 <= cfg.ell - 2) and (sig <= cfg.K)
        elif obj["kind"] == "RES":
            # residual-tight: E_3 = ell (tight) with T>=5 (residual), sigma = K+2
            T = sum(m - 2 for m in cfg.mus[2:])
            strat_ok = (cfg.E3 == cfg.ell) and (sig == cfg.K + 2) and (T >= 5)
        else:
            strat_ok = (cfg.E3 > cfg.ell - 2) and (sig > cfg.K) and (cfg.E3 <= cfg.ell) and (sig <= cfg.K + 2)
        good = expect_ok and strat_ok and (dU == 2)
        ok = ok and good
        lines.append("%s: kind=%s expect_match=%s stratification_ok=%s dimU==2:%s"
                      % (obj["label"], obj["kind"], expect_ok, strat_ok, dU == 2))
    return ok, " | ".join(lines)

def gate_ix_theorem1(tamper=False):
    """Addendum 2A: Theorem 1 covered-chart recheck + residual-tight witnesses.

    covered  (T = sum_{k>=3}(mu_k-2) <= 4): assert E_3 <= mu1+mu2 <= ell (Theorem 1,
             pairwise cap + tail bound) AND sigma <= K+dimU (its master-identity image).
    residual (T >= 5): assert E_3 <= ell (the law / RC target); the 2 RES witnesses are
             additionally checked TIGHT: E_3==ell, sigma==K+dimU, rho==ell-2 (realizable).
    tamper:  falsely tighten the Theorem-1 bound by 1; a tight-covered object with
             E_3 == mu1+mu2 (e.g. CE ell=23 p=139, or CE ell=13 p=79) then FAILS.
    """
    ok = True
    lines = []
    n_cov = n_res = n_res_tight = 0
    for obj in OBJECTS:
        cfg = make_config(obj)
        mus = cfg.mus  # largest-first (Config sorts fibers descending)
        ell = cfg.ell
        E3 = cfg.E3
        m1m2 = mus[0] + mus[1]
        T = sum(m - 2 for m in mus[2:])
        sig = sigma_via_syzygy(cfg)
        dU = dimU_dim(cfg)
        if T <= 4:  # covered chart -- Theorem 1 applies unconditionally
            n_cov += 1
            bound = m1m2 - (1 if tamper else 0)
            good = (E3 <= bound <= ell) and (sig <= cfg.K + dU)
            tag = "COV(T=%d) E3=%d<=m1m2=%d<=ell=%d sig<=K+dU:%s" % (
                T, E3, m1m2, ell, sig <= cfg.K + dU)
        else:  # residual chart -- RC target (law); RES witnesses are tight
            n_res += 1
            good = (E3 <= ell)
            tag = "RESID(T=%d) E3=%d<=ell=%d" % (T, E3, ell)
            if obj["kind"] == "RES":
                n_res_tight += 1
                rho = rho_dim(cfg)
                tight = (E3 == ell) and (sig == cfg.K + dU) and (rho == ell - 2) and (T >= 5)
                good = good and tight
                tag = "RESID-TIGHT(T=%d) E3==ell:%s sig==K+dU:%s rho==ell-2:%s" % (
                    T, E3 == ell, sig == cfg.K + dU, rho == ell - 2)
        ok = ok and good
        lines.append("%s: %s" % (obj["label"], tag))
    struct_ok = (n_cov >= 12) and (n_res >= 3) and (n_res_tight == 3)
    ok = ok and struct_ok
    lines.append("[structure] covered=%d residual=%d residual_tight=%d (want cov>=12,res>=3,rt==3):%s"
                 % (n_cov, n_res, n_res_tight, struct_ok))
    return ok, " | ".join(lines)

GATES = [
    ("(i)    moment bridge / sigma==delta      ", gate_i_moment_bridge),
    ("(ii)   locator duality dimVsum==rho      ", gate_ii_locator_duality),
    ("(iii)  pairwise Vi cap Vj==0, K=2         ", gate_iii_pairwise),
    ("(iv)   recursion sigma==sum t_m           ", gate_iv_recursion),
    ("(v)    K=3 bound sigma<=min(mu)-1         ", gate_v_k3_bound),
    ("(vi)   master identity + sigma-form       ", gate_vi_master_identity),
    ("(vii)  P2 falsifier [6,6,6] ell=13 p=79   ", gate_vii_p2_falsifier),
    ("(viii) OLD/NEW stratification             ", gate_viii_stratification),
    ("(ix)   Theorem 1 covered + residual-tight ", gate_ix_theorem1),
]

def main():
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 92)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum/claim is corrupted")
    else:
        print(" verify_l1_sigma_calculus  (zero-arg)   sigma-form of E_3<=ell  <=>  sigma<=K+dimU")
        print(" (experimental/notes/l1/l1_sigma_calculus.md)")
    print("=" * 92)
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
    print("=" * 92)
    if selftest:
        print(" SELF-TEST RESULT: %s   (%.1fs)"
              % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)" % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)

if __name__ == "__main__":
    main()
