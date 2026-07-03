#!/usr/bin/env python3
r"""
Verifier for l1_prime_ell_onset.md.

Background-free coset sunflower over F_p: H = mu_ell (order ell, ell | p-1);
t coset petals T_i = a_i H (locators X^ell - alpha_i, alpha_i = a_i^ell); m core
cosets, C = union of b_j H (beta_j = b_j^ell); distinct nonzero scalars c_i;
received word U = c_i L_C on petal i, 0 on C.  k = m*ell+1, s = (m+1)*ell.  By the
PR #219 bijection (l1_general_reconstruction_collapse.md) listed full-petal
codewords biject with divisibility-minimal kernel sets E (ell <= |E| <= (t-1)ell,
deg W_E <= |E|), E = exact missed core.  MIXED = not a union of full H-cosets.

Reduction: no mixed minimal kernel set <=> every mixed full-petal codeword is
UNLISTED, i.e. retained R = sum_j rho_j < (m-t+1)ell.

For m = t+1 a full-petal codeword is P(X) = w(X^ell) + phi(X^ell) g(X) with each
sector g_r (r>=1) a CONSTANT gamma_r, so Gamma(X) = sum_{r>=1} gamma_r X^r is a
single fixed polynomial (mixed iff Gamma != 0); retained on core coset j is a level
set { x in b_j H : Gamma(x) = lambda_j }, the lambda_j free.

Gates:

  (i)   LEMMA R (pair-count): every mixed m=t+1 codeword has
        sum_j rho_j(rho_j-1) <= (ell-1)(ell-2).  The maximum over the free levels
        lambda_j is sum_j F_j(F_j-1) with F_j = maxfiber_j(Gamma); we verify this
        <= (ell-1)(ell-2) EXHAUSTIVELY over projective Gamma at ell=5 (p in 41,61;
        equality attained) and on a deterministic sample at ell in {7,11,13}.  We
        also verify the prime-specific engine (*): for every omega in H\{1},
        Q_omega = Gamma(X)-Gamma(omega X) is nonzero with <= ell-2 nonzero roots.

  (ii)  MIXED VACANCY at (t=3, m=4).  ell=5, p in {41,61}: EXHAUSTIVE projective
        Gamma gives max retained = 2ell-1 = 9 < 2ell; AND a direct minimal-kernel-
        set lattice enumeration over a deterministic scalar bank gives 0 mixed
        minimal kernel sets (only the C(m,t-1) coset unions).  ell=7, p in {71,113}:
        the exact integer program  max sum_j rho_j s.t. sum rho_j(rho_j-1) <=
        (ell-1)(ell-2), 0<=rho_j<=ell-1, m=4  equals 2ell-1 < 2ell (brute, given
        Lemma R), so retained <= 2ell-1 => every mixed missed core has size
        >= |C|-(2ell-1) = 2ell+1 > (t-1)ell, OUT of the kernel-set range: no mixed
        minimal kernel set.  A deterministic mixed codeword is built and confirmed
        unlisted with out-of-range missed core.

  (iii) TIGHTNESS CERTIFICATE.  An explicit degree-19 mixed codeword at (p=41,
        ell=5, t=3, m=4), scalars (27,1,16), embedded and RE-VERIFIED FROM SCRATCH:
        agrees with U on all 15 petal points, has exactly 9 = 2ell-1 retained core
        points, missed core of size |M| = 11 = (t-1)ell+1 that is NOT a coset union
        (mixed), unlisted (9 < 2ell).  The exact projective max = 9 at p=41,61
        certifies the bound is razor-tight (no slack).

  (iv)  LEMMA Psi_1 spot check:  #{ j : n_j = 1 } <= 1 + ell*(m-t-1), where
        n_j = ell - rho_j, verified by deliberately constructing cosets with a
        single geometric ratio (n_j=1) up to the bound.

HONEST SCOPE: pair-counting closes EXACTLY t=3 (the same IP has max >= 2ell for
t>=4 -- a PROVED limitation, exhibited here); t>=4 and general m>t+1 are numerically
vacant but OPEN.  The engine (*) needs ell PRIME (omega^r != 1); for composite ell it
fails and the onset is earlier (companion note's ell=6 witnesses).

Run:
    python3 verify_l1_prime_ell_onset.py [--json]

stdlib-only, offline, deterministic; exit 0 iff every gate passes.
"""
from __future__ import annotations
import argparse
import itertools
import json
import random


# ---------- polynomial algebra over F_p (own, stdlib-only) ----------
def pmul(a, b, p):
    if not a or not b:
        return []
    C = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                C[i + j] = (C[i + j] + ai * bj) % p
    while len(C) > 1 and C[-1] == 0:
        C.pop()
    return C


def padd(a, b, p):
    n = max(len(a), len(b))
    C = [0] * n
    for i in range(len(a)):
        C[i] = (C[i] + a[i]) % p
    for i in range(len(b)):
        C[i] = (C[i] + b[i]) % p
    while len(C) > 1 and C[-1] == 0:
        C.pop()
    return C


def loc(roots, p):
    o = [1]
    for r in roots:
        o = pmul(o, [(-r) % p, 1], p)
    return o


def peval(a, x, p):
    v = 0
    for c in reversed(a):
        v = (v * x + c) % p
    return v


def interp(xs, ys, p):
    """Lagrange interpolation; coeff list low->high, trimmed."""
    res = []
    for j in range(len(xs)):
        num, den = [1], 1
        for k in range(len(xs)):
            if k == j:
                continue
            num = pmul(num, [(-xs[k]) % p, 1], p)
            den = den * (xs[j] - xs[k]) % p
        sca = ys[j] * pow(den % p, -1, p) % p
        term = [c * sca % p for c in num]
        if len(term) > len(res):
            res += [0] * (len(term) - len(res))
        for i, c in enumerate(term):
            res[i] = (res[i] + c) % p
    while res and res[-1] == 0:
        res.pop()
    return res


def poly_divmod(A, B, p):
    """A = B*q + r; return (q, r), deg r < deg B.  B monic-or-not."""
    A = A[:]
    binv = pow(B[-1], -1, p)
    q = [0] * (max(len(A) - len(B), 0) + 1)
    while len(A) >= len(B) and any(A):
        d = len(A) - len(B)
        c = A[-1] * binv % p
        q[d] = c
        for i, bi in enumerate(B):
            A[d + i] = (A[d + i] - c * bi) % p
        while A and A[-1] == 0:
            A.pop()
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q, A


def subst_Xell(poly, ell, p):
    """coeffs of q(X^ell) given q."""
    if not poly:
        return []
    o = [0] * ((len(poly) - 1) * ell + 1)
    for d, c in enumerate(poly):
        if c:
            o[d * ell] = (o[d * ell] + c) % p
    while len(o) > 1 and o[-1] == 0:
        o.pop()
    return o


# ---------- coset construction (smallest primitive root; deterministic) ----------
def prim_root(p):
    n, f, d = p - 1, set(), 2
    while d * d <= n:
        while n % d == 0:
            f.add(d)
            n //= d
        d += 1
    if n > 1:
        f.add(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in f):
            return g
    raise RuntimeError("no primitive root")


def all_cosets(p, ell):
    g = prim_root(p)
    h = pow(g, (p - 1) // ell, p)
    H = sorted({pow(h, j, p) for j in range(ell)})
    out, used = [], set()
    for x in range(1, p):
        if x in used:
            continue
        cs = sorted(x * e % p for e in H)
        if len(cs) == ell and not (set(cs) & used):
            out.append(cs)
            used |= set(cs)
    return out, H


def is_coset_union(E, H, p):
    Es = set(E)
    return all((x * h) % p in Es for x in E for h in H)


# ---------- m=t+1 sector machinery ----------
def config_labels(p, ell, t, m):
    cs, H = all_cosets(p, ell)
    assert len(cs) >= t + m, "not enough cosets"
    petals, core_cosets = cs[:t], cs[t:t + m]
    b = [min(cc) for cc in core_cosets]
    beta = [pow(bj, ell, p) for bj in b]
    alpha = [pow(min(pt), ell, p) for pt in petals]
    return cs, H, petals, core_cosets, b, beta, alpha


def gamma_eval(gamma, x, p):
    """Gamma(x) = sum_{r=1..ell-1} gamma_{r-1} x^r  (gamma indexed r-1)."""
    v = 0
    xr = x % p
    for g in gamma:
        v = (v + g * xr) % p
        xr = xr * x % p
    return v


def maxfibers(gamma, b, H, p):
    """for each core coset j (rep b_j), fiber-size multiset of x->Gamma(b_j x) on H;
    return list of max fiber sizes F_j."""
    F = []
    for bj in b:
        cnt = {}
        for h in H:
            v = gamma_eval(gamma, bj * h % p, p)
            cnt[v] = cnt.get(v, 0) + 1
        F.append(max(cnt.values()))
    return F


def projective_reps(dim, p):
    """vectors in F_p^dim with first nonzero coord == 1 (P^{dim-1} reps)."""
    for lead in range(dim):
        for tail in itertools.product(range(p), repeat=dim - 1 - lead):
            yield [0] * lead + [1] + list(tail)


_SCAN = {}


def projective_scan(p, ell, t):
    """EXHAUSTIVE over projective Gamma (mixed codewords, m=t+1): return
    (max_retained, max_paircount, equality_attained).  Memoized.  max over the
    free per-coset levels of retained = sum_j F_j and of the pair-count
    sum_j F_j(F_j-1), F_j = maxfiber_j(Gamma)."""
    key = (p, ell, t)
    if key not in _SCAN:
        _, H, _, _, b, _, _ = config_labels(p, ell, t, t + 1)
        B = (ell - 1) * (ell - 2)
        maxret, maxpair, eq = 0, 0, False
        for gamma in projective_reps(ell - 1, p):
            F = maxfibers(gamma, b, H, p)
            maxret = max(maxret, sum(F))
            pc = sum(f * (f - 1) for f in F)
            if pc > maxpair:
                maxpair = pc
            if pc == B:
                eq = True
        _SCAN[key] = (maxret, maxpair, eq)
    return _SCAN[key]


# ---------- CRT kernel-set oracle (self-contained; PR #219 Lemma 7/8) ----------
class Sunflower:
    def __init__(self, p, petals, scalars, core):
        self.p, self.petals, self.scalars = p, petals, scalars
        self.core = list(core)
        self.t, self.ell = len(petals), len(petals[0])
        self.N = self.t * self.ell
        self.pts = [x for pt in petals for x in pt]
        self.cvec = [c for pt, c in zip(petals, scalars) for _ in pt]
        self.diff = [[(x - r) % p for r in self.core] for x in self.pts]
        self.vinv = self._vinv_rows()

    def _vinv_rows(self):
        p, pts, N = self.p, self.pts, self.N
        rows = [[0] * N for _ in range(N)]
        for j in range(N):
            num, den = [1], 1
            for mm in range(N):
                if mm == j:
                    continue
                num = pmul(num, [(-pts[mm]) % p, 1], p)
                den = den * (pts[j] - pts[mm]) % p
            inv = pow(den % p, -1, p)
            for a in range(N):
                rows[a][j] = (num[a] * inv) % p if a < len(num) else 0
        return rows

    def _is_kernel_from_prod(self, prod, d):
        p, N = self.p, self.N
        y = [(self.cvec[j] * prod[j]) % p for j in range(N)]
        for a in range(d + 1, N):
            row = self.vinv[a]
            s = 0
            for j in range(N):
                s += row[j] * y[j]
            if s % p != 0:
                return False
        return True

    def enumerate_kernel_sets(self, max_d):
        p, N = self.p, self.N
        ncore, diff = len(self.core), self.diff
        by_size = {d: set() for d in range(1, max_d + 1)}

        def dfs(start, chosen, prod):
            d = len(chosen)
            if 1 <= d <= max_d and self._is_kernel_from_prod(prod, d):
                by_size[d].add(frozenset(chosen))
            if d == max_d:
                return
            for r in range(start, ncore):
                nprod = [(prod[j] * diff[j][r]) % p for j in range(N)]
                dfs(r + 1, chosen + (r,), nprod)

        dfs(0, tuple(), [1] * N)
        return by_size

    def minimal_kernel_sets(self, max_d):
        by_size = self.enumerate_kernel_sets(max_d)
        minimals, cbd = [], {}
        for d in range(self.ell, max_d + 1):
            prev = by_size.get(d - 1, set())
            for D in by_size.get(d, set()):
                if prev and any((D - {x}) in prev for x in D):
                    continue
                minimals.append(tuple(sorted(self.core[i] for i in D)))
                cbd[d] = cbd.get(d, 0) + 1
        return sorted(minimals, key=lambda z: (len(z), z)), cbd


# ---------- build an explicit m=t+1 codeword from Gamma via free levels ----------
def build_codeword(p, ell, t, m, gamma):
    """Deterministic mixed full-petal codeword with lambda_j = argmax fiber (so
    retained = sum_j F_j).  Returns dict or None if no distinct-nonzero scalars."""
    cs, H, petals, core_cosets, b, beta, alpha = config_labels(p, ell, t, m)
    phi = loc(alpha, p)
    Lam = loc(beta, p)
    Lam_alpha = [peval(Lam, al, p) for al in alpha]
    # per coset argmax level
    lam = []
    for bj in b:
        cnt = {}
        for h in H:
            v = gamma_eval(gamma, bj * h % p, p)
            cnt[v] = cnt.get(v, 0) + 1
        lam.append(max(cnt, key=lambda v: cnt[v]))
    targ = [(-lam[j] * peval(phi, beta[j], p)) % p for j in range(m)]
    base = interp(beta, targ, p)
    for mu in range(p):
        P0 = padd(base, [mu * c % p for c in Lam], p)
        g0, w = poly_divmod(P0, phi, p)
        if len(w) - 1 > t - 1 or len(g0) - 1 > m - t:
            continue
        c = [peval(w, alpha[i], p) * pow(Lam_alpha[i], -1, p) % p for i in range(t)]
        if len(set(c)) == t and all(ci != 0 for ci in c):
            break
    else:
        return None
    gX = subst_Xell(g0, ell, p)
    for r in range(1, ell):
        gX = padd(gX, [0] * r + subst_Xell([gamma[r - 1]], ell, p), p)
    P = padd(subst_Xell(w, ell, p), pmul(subst_Xell(phi, ell, p), gX, p), p)
    core = sorted(x for cc in core_cosets for x in cc)
    return {"P": P, "c": c, "petals": petals, "core_cosets": core_cosets,
            "core": core, "H": H}


def codeword_facts(P, c, petals, core, H, p, ell, t, m):
    """Independent facts about an explicit codeword P: petal agreement, retained,
    missed, mixed, listed."""
    LC = loc(core, p)
    pts = [x for pt in petals for x in pt]
    cvec = [c[i] for i, pt in enumerate(petals) for _ in pt]
    petal_ok = all(peval(P, x, p) == cv * peval(LC, x, p) % p for x, cv in zip(pts, cvec))
    missed = [x for x in core if peval(P, x, p) != 0]
    retained = len(core) - len(missed)
    mixed = not is_coset_union(missed, H, p) if missed else False
    s = (m + 1) * ell
    agreement = t * ell + retained
    return {"deg": len(P) - 1, "petal_ok": petal_ok, "retained": retained,
            "missed": len(missed), "mixed": mixed, "listed": agreement >= s,
            "agreement": agreement, "s": s}


# ---------- gate (i): Lemma R (pair-count) + (*) root bound ----------
def gate_pair_lemma():
    B = lambda ell: (ell - 1) * (ell - 2)
    rng = random.Random(20260704)
    detail = []
    ok = True
    # exhaustive projective Gamma at ell=5
    for p in (41, 61):
        _, worst_pair, eq_hit = projective_scan(p, 5, 3)
        good = worst_pair <= B(5) and eq_hit
        ok = ok and good
        detail.append({"p": p, "ell": 5, "mode": "exhaustive-Gamma",
                       "max_paircount": worst_pair, "bound": B(5),
                       "equality_attained": eq_hit, "ok": good})
    # sampled Gamma at larger ell (exhaustive infeasible)
    for (ell, p) in ((7, 71), (11, 89), (13, 131)):
        cs, H, petals, core_cosets, b, beta, alpha = config_labels(p, ell, 3, 4)
        worst_pair = 0
        for _ in range(4000):
            gamma = [rng.randrange(p) for _ in range(ell - 1)]
            if not any(gamma):
                gamma[0] = 1
            F = maxfibers(gamma, b, H, p)
            worst_pair = max(worst_pair, sum(f * (f - 1) for f in F))
        good = worst_pair <= B(ell)
        ok = ok and good
        detail.append({"p": p, "ell": ell, "mode": "sampled-Gamma",
                       "max_paircount": worst_pair, "bound": B(ell), "ok": good})
    # engine (*): Q_omega nonzero with <= ell-2 nonzero roots
    star_ok = True
    star_tests = 0
    for (ell, p) in ((5, 41), (7, 71), (11, 89), (13, 131)):
        cs, H, petals, core_cosets, b, beta, alpha = config_labels(p, ell, 3, 4)
        Hno1 = [w for w in H if w != 1]
        for _ in range(300):
            gamma = [rng.randrange(p) for _ in range(ell - 1)]
            if not any(gamma):
                gamma[0] = 1
            for om in Hno1:
                # Q_omega(x) = Gamma(x) - Gamma(omega x)
                nz_roots = sum(1 for x in range(1, p)
                               if gamma_eval(gamma, x, p) == gamma_eval(gamma, om * x % p, p))
                nonzero = any((g * (1 - pow(om, r + 1, p))) % p
                              for r, g in enumerate(gamma))
                star_tests += 1
                if not nonzero or nz_roots > ell - 2:
                    star_ok = False
    ok = ok and star_ok
    return {"detail": detail, "star_ok": star_ok, "star_tests": star_tests, "ok": ok}


# ---------- gate (ii): mixed vacancy at (t=3, m=4) ----------
def ip_max_retained(ell, m):
    """exact max sum rho_j, rho_j in [0,ell-1], m cosets, sum rho_j(rho_j-1) <= B."""
    B = (ell - 1) * (ell - 2)
    best = -1
    for rho in itertools.product(range(ell), repeat=m):
        if sum(r * (r - 1) for r in rho) <= B:
            best = max(best, sum(rho))
    return best


def scalar_bank(p, t, alpha):
    """deterministic bank incl. moment-spike vectors (extremal for mixed sets)."""
    rng = random.Random(9090 + p)
    bank = [[1, 2, 3, 4, 5, 6][:t],
            [1] + [pow(2, i, p) for i in range(1, t)]]
    # moment spikes: solve Vandermonde(alpha)^T w = e_kappa, c_i = w_i * L'(a_i)
    for kappa in range(t):
        V = [[pow(alpha[i], j, p) for i in range(t)] for j in range(t)]
        M = [row[:] + [1 if j == kappa else 0] for j, row in enumerate(V)]
        singular = False
        for col in range(t):
            piv = next((r for r in range(col, t) if M[r][col] % p), None)
            if piv is None:
                singular = True
                break
            M[col], M[piv] = M[piv], M[col]
            inv = pow(M[col][col], -1, p)
            M[col] = [(v * inv) % p for v in M[col]]
            for r in range(t):
                if r != col and M[r][col] % p:
                    f = M[r][col]
                    M[r] = [(a - f * b2) % p for a, b2 in zip(M[r], M[col])]
        if singular:
            continue
        w = [M[i][t] % p for i in range(t)]
        Lp = [1] * t
        for i in range(t):
            for kk in range(t):
                if kk != i:
                    Lp[i] = Lp[i] * (alpha[i] - alpha[kk]) % p
        bank.append([(w[i] * Lp[i]) % p for i in range(t)])
    for _ in range(3):
        bank.append([1] + [rng.randrange(1, p) for _ in range(t - 1)])
    seen, out = set(), []
    for c in bank:
        key = tuple(c)
        if key in seen:
            continue
        seen.add(key)
        if len(set(c)) == t and all(ci != 0 for ci in c):
            out.append(c)
    return out


def gate_vacancy():
    t, m = 3, 4
    ok = True
    detail = []
    # ell=5: exhaustive projective Gamma max-retained + direct kernel-set enumeration
    for p in (41, 61):
        cs, H, petals, core_cosets, b, beta, alpha = config_labels(p, 5, t, m)
        maxret, _, _ = projective_scan(p, 5, t)
        core = sorted(x for cc in core_cosets for x in cc)
        bank = scalar_bank(p, t, alpha)
        tot_mixed, tot_min = 0, 0
        for c in bank:
            mins, _ = Sunflower(p, petals, c, core).minimal_kernel_sets((t - 1) * 5)
            tot_min += len(mins)
            tot_mixed += sum(1 for D in mins
                             if not is_coset_union(frozenset(D), H, p))
        good = (maxret == 2 * 5 - 1 < 2 * 5) and tot_mixed == 0
        ok = ok and good
        detail.append({"p": p, "ell": 5, "exhaustive_maxret": maxret,
                       "2ell": 2 * 5, "scalars": len(bank),
                       "minimal_kernel_sets": tot_min, "mixed_minimal": tot_mixed,
                       "ok": good})
    # ell=7: exact IP-max + kernel-range exclusion + one explicit unlisted witness
    for p in (71, 113):
        ell = 7
        ipm = ip_max_retained(ell, m)
        # retained <= ipm => |missed| >= m*ell - ipm ; kernel range top = (t-1)ell
        min_missed = m * ell - ipm
        exclude = min_missed > (t - 1) * ell            # out of kernel-set range
        # explicit deterministic mixed codeword, confirmed unlisted
        wit = None
        for seed in range(1, 40):
            gamma = [0] * (ell - 1)
            gamma[0] = 1
            gamma[seed % (ell - 1)] = (gamma[seed % (ell - 1)] + seed) % p
            cw = build_codeword(p, ell, t, m, gamma)
            if cw is None:
                continue
            f = codeword_facts(cw["P"], cw["c"], cw["petals"], cw["core"],
                               cw["H"], p, ell, t, m)
            if f["mixed"] and f["retained"] > 0:
                wit = f
                break
        wit_ok = (wit is not None and wit["petal_ok"] and not wit["listed"]
                  and wit["retained"] < 2 * ell
                  and (m * ell - wit["retained"]) > (t - 1) * ell)
        good = (ipm == 2 * ell - 1 < 2 * ell) and exclude and wit_ok
        ok = ok and good
        detail.append({"p": p, "ell": ell, "ip_max_retained": ipm, "2ell": 2 * ell,
                       "min_missed": min_missed, "kernel_top": (t - 1) * ell,
                       "out_of_range": exclude,
                       "witness_retained": (wit or {}).get("retained"),
                       "witness_unlisted": wit_ok, "ok": good})
    # PROVED limitation: the SAME pair-count IP does NOT close t>=4 (IP-max >= 2ell),
    # so t=3 is exactly the reach of pair-counting.
    boundary = []
    for (tt, ell) in ((4, 7), (4, 11), (5, 13)):
        ipm = ip_max_retained(ell, tt + 1)
        fails = ipm >= 2 * ell
        ok = ok and fails
        boundary.append({"t": tt, "ell": ell, "ip_max": ipm, "2ell": 2 * ell,
                         "pair_count_fails": fails})
    return {"detail": detail, "method_boundary_t_ge_4": boundary, "ok": ok}


# ---------- gate (iii): embedded tightness witness ----------
WIT = {
    "p": 41, "ell": 5, "t": 3, "m": 4,
    "scalars": [27, 1, 16],
    "petals": [[1, 10, 16, 18, 37], [2, 20, 32, 33, 36], [3, 7, 13, 29, 30]],
    "core_cosets": [[4, 23, 25, 31, 40], [5, 8, 9, 21, 39],
                    [6, 14, 17, 19, 26], [11, 12, 28, 34, 38]],
    "P": [16, 14, 0, 14, 23, 1, 15, 0, 15, 10, 33, 11, 0, 11, 21, 36, 1, 0, 1, 28],
}


def gate_tightness():
    p, ell, t, m = WIT["p"], WIT["ell"], WIT["t"], WIT["m"]
    cs, H, petals, core_cosets, b, beta, alpha = config_labels(p, ell, t, m)
    # geometry reproduces the embedded labelling (deterministic all_cosets)
    geom_ok = (petals == WIT["petals"] and core_cosets == WIT["core_cosets"])
    core = sorted(x for cc in core_cosets for x in cc)
    P, c = WIT["P"], WIT["scalars"]
    f = codeword_facts(P, c, petals, core, H, p, ell, t, m)
    dnz = len(set(c)) == t and all(ci != 0 for ci in c)
    checks = {
        "geometry_reproduced": geom_ok,
        "deg_le_m_ell": f["deg"] <= m * ell,
        "scalars_distinct_nonzero": dnz,
        "petal_agreement": f["petal_ok"],
        "retained_eq_2ell_minus_1": f["retained"] == 2 * ell - 1,
        "missed_eq_11": f["missed"] == 11 and f["missed"] == (t - 1) * ell + 1,
        "mixed": f["mixed"],
        "unlisted": not f["listed"] and f["retained"] < 2 * ell,
    }
    # razor-tightness: EXACT projective max = 2ell-1 at p in {41,61}
    exact = {}
    for pp in (41, 61):
        mx, _, _ = projective_scan(pp, ell, t)
        exact[pp] = mx
        checks[f"exact_projective_max_{pp}_eq_9"] = (mx == 2 * ell - 1)
    ok = all(checks.values())
    return {"witness": {"retained": f["retained"], "missed": f["missed"],
                        "deg": f["deg"], "agreement": f["agreement"], "s": f["s"]},
            "exact_projective_max": exact, "checks": checks, "ok": ok}


# ---------- gate (iv): Lemma Psi_1 spot check ----------
def construct_n1(p, ell, t, m, rng):
    """build codewords deliberately giving cosets with n_j=1 (single geometric
    ratio) and return the max #(n_j=1) achieved; must be <= 1 + ell*(m-t-1)."""
    cs, H, petals, core_cosets, b, beta, alpha = config_labels(p, ell, t, m)
    phi = loc(alpha, p)
    D = m - t - 1
    best = 0
    for _ in range(200):
        J = rng.sample(range(m), min(D + 1, m))
        thetas, es = {}, {}
        for j in J:
            binv = pow(b[j], -1, p)
            thetas[j] = binv * rng.choice(H) % p   # theta^ell = beta_j^{-1}
            es[j] = rng.randrange(1, p)
        gs = []
        ok = True
        for r in range(1, ell):
            xs = [beta[j] for j in J]
            ys = [es[j] * pow(thetas[j], r, p) % p for j in J]
            gr = interp(xs, ys, p)
            if len(gr) - 1 > D:
                ok = False
                break
            gs.append(gr)
        if not ok:
            continue
        # pick scalars -> w ; then g0 so that P0(beta_j) = phi(beta_j) e_j, giving,
        # with P_r(beta_j)=e_j theta_j^r and (b_j theta_j)^ell=1, exactly one
        # non-retained point per coset j in J (n_j = 1).
        c = [1] + [rng.randrange(2, p) for _ in range(t - 1)]
        while len(set(c)) < t:
            c = [1] + [rng.randrange(2, p) for _ in range(t - 1)]
        Lam = loc(beta, p)
        Lam_alpha = [peval(Lam, al, p) for al in alpha]
        w = interp(alpha, [c[i] * Lam_alpha[i] % p for i in range(t)], p)
        xs = [beta[j] for j in J]
        ys = []
        for j in J:
            phib = peval(phi, beta[j], p)
            ys.append((es[j] - peval(w, beta[j], p) * pow(phib, -1, p)) % p)
        g0 = interp(xs, ys, p)
        if len(g0) - 1 > D + 1:
            continue
        n1 = 0
        for j in range(m):
            phib = peval(phi, beta[j], p)
            v = [0] * ell
            v[0] = (peval(w, beta[j], p) + phib * peval(g0, beta[j], p)) % p
            bp = 1
            for r in range(1, ell):
                bp = bp * b[j] % p
                v[r] = bp * phib % p * peval(gs[r - 1], beta[j], p) % p
            rho = 0
            for h in H:
                s, hp = 0, 1
                for r in range(ell):
                    s = (s + v[r] * hp) % p
                    hp = hp * h % p
                if s == 0:
                    rho += 1
            if ell - rho == 1:
                n1 += 1
        best = max(best, n1)
    return best


def gate_psi1():
    rng = random.Random(31337)
    detail = []
    ok = True
    for (ell, t, m) in [(5, 3, 4), (7, 3, 5), (7, 3, 6), (11, 3, 5), (11, 3, 7)]:
        pp = None
        cand = ell + 1
        while cand < 4000:
            if cand % ell == 1 and all(cand % d for d in range(2, int(cand ** 0.5) + 1)) \
                    and (cand - 1) // ell >= t + m + 1:
                pp = cand
                break
            cand += 1
        bound = 1 + ell * (m - t - 1)
        got = construct_n1(pp, ell, t, m, rng)
        good = got <= bound
        ok = ok and good
        detail.append({"ell": ell, "t": t, "m": m, "p": pp, "D": m - t - 1,
                       "bound": bound, "constructed_n1": got, "ok": good})
    return {"detail": detail, "ok": ok}



# ---------- gate (v): t=2, m=4, ell=5 all-scalar exhaustive vacancy ----------
def gate_t2_m4():
    """(t=2, m=t+2=4, ell=5): outside every stated theorem; EXHAUSTIVE all-scalar
    check.  The kernel condition is linear in the scalar vector, so E kernel for c
    iff kernel for lambda*c: wlog c = (1, x), x != 0, 1.  Kernel range at t=2 is
    the single defect d = ell = (t-1)*ell, so every kernel set is minimal (sub-ell
    kernel sets are impossible for distinct scalars).  Gate: for EVERY x, every
    size-ell kernel set is one of the m full core cosets (zero mixed)."""
    t, m, ell = 2, 4, 5
    ok = True
    detail = []
    for p in (31, 41):
        cs, H, petals, core_cosets, b, beta, alpha = config_labels(p, ell, t, m)
        core = sorted(x for cc in core_cosets for x in cc)
        full = {frozenset(cc) for cc in core_cosets}
        n_mixed = 0
        n_kernel = 0
        n_sub = 0
        for x in range(2, p):
            by_size = Sunflower(p, petals, [1, x], core).enumerate_kernel_sets(ell)
            for d in range(1, ell):
                n_sub += len(by_size.get(d, ()))
            for E in by_size.get(ell, ()):
                n_kernel += 1
                if frozenset(core[i] for i in E) not in full:
                    n_mixed += 1
        good = (n_mixed == 0 and n_sub == 0 and n_kernel > 0)
        ok = ok and good
        detail.append({"p": p, "scalars_tested": p - 2, "kernel_sets": n_kernel,
                       "mixed": n_mixed, "sub_ell": n_sub, "ok": good})
    return {"detail": detail, "ok": ok}


# ---------- driver ----------
def run():
    g1 = gate_pair_lemma()
    g2 = gate_vacancy()
    g3 = gate_tightness()
    g4 = gate_psi1()
    g5 = gate_t2_m4()
    checks = {
        "(i) Lemma R pair-count + (*) root bound (exhaustive ell=5, sampled ell>=7)": g1["ok"],
        "(ii) mixed vacancy (t=3,m=4): ell=5 exhaustive+kernel-sets, ell=7 exact IP": g2["ok"],
        "(iii) tightness witness retained=2ell-1=9, |M|=11, razor-tight": g3["ok"],
        "(iv) Psi_1 spot check #{n_j=1} <= 1+ell(m-t-1)": g4["ok"],
        "(v) (t=2,m=4,ell=5) exhaustive all-scalar vacancy": g5["ok"],
    }
    return {"pair_lemma": g1, "vacancy": g2, "tightness": g3, "psi1": g4,
            "t2_m4": g5, "checks": checks, "all_ok": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(description="verify l1_prime_ell_onset.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str))
        raise SystemExit(0 if out["all_ok"] else 1)
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    for d in out["pair_lemma"]["detail"]:
        eq = d.get("equality_attained")
        print(f"    (i) ell={d['ell']} p={d['p']} {d['mode']}: "
              f"max pair-count={d['max_paircount']} <= (ell-1)(ell-2)={d['bound']}"
              + (f"  [equality attained]" if eq else ""))
    print(f"    (i) (*) engine: {out['pair_lemma']['star_tests']} (Gamma,omega) tests, "
          f"all Q_omega!=0 with <= ell-2 roots: {out['pair_lemma']['star_ok']}")
    for d in out["vacancy"]["detail"]:
        if d["ell"] == 5:
            print(f"    (ii) ell=5 p={d['p']}: exhaustive max retained={d['exhaustive_maxret']}"
                  f" < 2ell={d['2ell']}; {d['scalars']} scalars -> "
                  f"{d['minimal_kernel_sets']} minimal kernel sets, "
                  f"{d['mixed_minimal']} mixed")
        else:
            print(f"    (ii) ell=7 p={d['p']}: exact IP-max={d['ip_max_retained']}"
                  f" < 2ell={d['2ell']}; min|missed|={d['min_missed']} > "
                  f"(t-1)ell={d['kernel_top']} (out of range={d['out_of_range']}); "
                  f"explicit witness unlisted={d['witness_unlisted']}")
    for d in out["vacancy"]["method_boundary_t_ge_4"]:
        print(f"    (ii) limitation: t={d['t']} ell={d['ell']} IP-max={d['ip_max']}"
              f" >= 2ell={d['2ell']} => pair-count does NOT close t>=4 (PROVED)")
    tw = out["tightness"]["witness"]
    print(f"    (iii) witness (41,5,3,4): retained={tw['retained']}=2ell-1, "
          f"|M|={tw['missed']}, deg={tw['deg']}, agreement={tw['agreement']}<s={tw['s']}; "
          f"exact max={out['tightness']['exact_projective_max']}")
    for d in out["psi1"]["detail"]:
        print(f"    (iv) ell={d['ell']} t={d['t']} m={d['m']} p={d['p']}: "
              f"#(n_j=1) constructed={d['constructed_n1']} <= 1+ell*D={d['bound']}")
    for d in out["t2_m4"]["detail"]:
        print(f"    (v) t=2 m=4 ell=5 p={d['p']}: {d['scalars_tested']} scalar classes, "
              f"{d['kernel_sets']} kernel sets, mixed={d['mixed']}, sub-ell={d['sub_ell']}")
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
