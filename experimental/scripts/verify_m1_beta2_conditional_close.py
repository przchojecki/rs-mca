#!/usr/bin/env python3
"""
verify_m1_beta2_conditional_close.py

Self-contained exact certificate for the NET-NEW, PROVEN-EXACT results of the
M1 (BETA_2) "conditional-close" note.  The weight-1 beta-line pushforward sheaf

    F_psi = R^1 pi_!( psi(a) (x) chi(rM(a,r)) )   on the z-line, z = b + 1/b,

with fiber over b the bidegree-(3,3) torus curve C_b = { Delta_b(a,r) = 0 },
Delta_b = A_beta b^2 + B_beta b + C_beta, is the object whose big monodromy
(BETA_2) the program must control.  The conditional-close note pins down three
PROVEN-EXACT local facts (the transvection in the weight-1 constituent, the Q8
interior-benign verdict, the z=+-2 branch-fiber structure with the descent
involution) plus ONE structural reduction (why the elementary Lefschetz route to
the eigenvalue split is BLOCKED for general psi).  This script machine-checks all
four by exact integer / F_p / F_{p^k} arithmetic.

What is certified (each a named function printing PASS/FAIL):

  [A]  PROVEN-EXACT.  9z+14 (z=-14/9) is a genuine unipotent transvection IN the
       rank-8 weight-1 constituent F = gr_1^W H^1_c.  Over the small primes
       11..43 with b0 (a root of 9b^2+14b+9) rational, C_{b0} has a UNIQUE
       ordinary A1 torus node (Phi=Phi_a=Phi_r=0, Hessian!=0 => Milnor mu=1 =>
       rank drop exactly 1), with a!=0 and rM!=0 (L lisse => the ODP vanishing
       cycle is pure weight 1), and the node is NOT on M=0 (the 3-dim weight-0
       Tate part W_0 is undisturbed).  Hence the unit of rank drop lands in
       gr_1^W = F: a genuine rank-8 transvection.

  [B]  PROVEN-EXACT.  Q8 is benign for EVERY psi by interior-point localization.
       Q8(0) = -217802 = -2*13*8377 and lc(Q8) = 3^8, so every one of the 8 Q8
       roots is an INTERIOR point z != 0,inf except at the already-excised bad
       primes {2,3,13,8377}; a rank-1 tame Kummer sheaf (lisse at interior pts)
       cannot be hosted at Q8.  Includes the exact branch-divisor identity
       disc_b = lin^2 - 4 q const = a*r*M*H over Z[a,r].

  [D]  PROVEN-EXACT.  The z=+-2 branch fibers.  C_{b=-1} (z=-2) is SMOOTH (zero
       torus + zero axis singular points over 11..73) and genus 2 (Weil genus-2
       zeta consistent, full functional-equation anchor at p=7) => F is lisse at
       z=-2 with gamma^2=1.  C_{b=1} (z=2) is SINGULAR at (1,1) -- the degenerate
       ordinary triple point, with M(1,1)=0 (chi ramified).  The descent
       involution sigma(a,r)=(1/a,1/r) is a genuine involution (sigma^2=id) that
       covers the deck swap b<->1/b ([A:B:C](1/a,1/r) ~ [C:B:A](a,r)), preserves
       C_{-1} and chi(rM), with genuine torus fixed point (-1,-1).

  [II] STRUCTURAL / CITABLE-CONDITIONAL (documents a LIMITATION, does NOT close
       item (II)).  The elementary Lefschetz fixed-point route to Tr(gamma|V) is
       BLOCKED for general psi: sigma permutes a (a -> 1/a), so psi(a) -> psi(a)^{-1};
       for any non-quadratic psi (ord psi > 2) there are points with
       psi(a) != psi(1/a), hence sigma^*L is NOT iso L.  With no L-equivariant
       involution there is no finite fixed-point trace.  This check PASSES by
       CONFIRMING the obstruction (sigma^*L !~= L); it records WHY (II) is not
       closable by this method, it does not close (II).

Pure Python 3 stdlib only (sys, itertools).  Exact integer / F_p / F_{p^k}
arithmetic.  No network, no file I/O beyond stdout, no eval/exec, no
compiled-decision/unsafe tactics.  Fully offline.

Status: AUDIT.  Exact finite certificate of the PROVEN-EXACT note results
(A, B, D) plus the structural (II) obstruction.  It deliberately does NOT decide
the still-open big-monodromy item (II) itself, nor the Q8 vanishing-cycle
dimension d in {1,2}; those are not finite-computation decidable.

Usage:  python3 verify_m1_beta2_conditional_close.py            (verbose)
        python3 verify_m1_beta2_conditional_close.py --check     (terse; exit 1 on any failure)

Exit 0 iff all checks pass (A,B,D proven-exact AND II confirms the obstruction).
"""

import sys
from itertools import product


# ======================================================================
# Elementary number theory
# ======================================================================
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def primes_in(lo, hi):
    return [n for n in range(lo, hi + 1) if is_prime(n)]


def factorint(n):
    n = abs(n)
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def fmt_factor(n):
    f = factorint(n)
    if not f:
        return str(n)
    body = " * ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(f.items()))
    return ("-" if n < 0 else "") + body


def legendre(x, p):
    x %= p
    if x == 0:
        return 0
    return 1 if pow(x, (p - 1) // 2, p) == 1 else -1


def primitive_root(p):
    if p == 2:
        return 1
    fs = list(factorint(p - 1).keys())
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g
    raise ValueError("no primitive root for %d" % p)


def sqrt_modp(d, p):
    """A square root of d mod p, or None if d is not a residue."""
    d %= p
    if d == 0:
        return 0
    if legendre(d, p) != 1:
        return None
    for t in range(1, p):
        if t * t % p == d:
            return t
    return None


# ======================================================================
# Minimal multivariate engine over (a, r, b) = vars (0, 1, 2).  Used ONLY to
# build Phi from the model constants and AUTO-derive its partials (no hand
# differentiation) and to project to the (a,r) plane for the disc identity and
# the genus point-counts.  Polynomials are dicts {(i,j,k): int}.
# ======================================================================
def mv_var(i):
    e = [0, 0, 0]
    e[i] = 1
    return {tuple(e): 1}


def mv_const(c):
    return {(0, 0, 0): c} if c else {}


def mv_add(*ps):
    d = {}
    for p in ps:
        for k, v in p.items():
            d[k] = d.get(k, 0) + v
    return {k: v for k, v in d.items() if v}


def mv_scale(p, c):
    return {k: v * c for k, v in p.items()} if c else {}


def mv_sub(p, q):
    return mv_add(p, mv_scale(q, -1))


def mv_mul(*ps):
    r = mv_const(1)
    for p in ps:
        d = {}
        for k1, v1 in r.items():
            for k2, v2 in p.items():
                k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
                d[k] = d.get(k, 0) + v1 * v2
        r = {k: v for k, v in d.items() if v}
    return r


def mv_deriv(p, i):
    d = {}
    for k, v in p.items():
        if k[i]:
            kk = list(k)
            e = kk[i]
            kk[i] -= 1
            d[tuple(kk)] = d.get(tuple(kk), 0) + v * e
    return {k: v for k, v in d.items() if v}


_A = mv_var(0)
_R = mv_var(1)
_B = mv_var(2)
# A_beta:  3a^2 r - 3a r^2 + a r - 3a + 2r
QUAD = mv_add(mv_scale(mv_mul(_A, _A, _R), 3), mv_scale(mv_mul(_A, _R, _R), -3),
              mv_mul(_A, _R), mv_scale(_A, -3), mv_scale(_R, 2))
# B_beta:  -a r (a-1)(r+1)
LIN = mv_scale(mv_mul(_A, _R, mv_sub(_A, mv_const(1)), mv_add(_R, mv_const(1))), -1)
# C_beta:  a r (-2a^2 r + 3a r^2 - a r + 3a - 3r)
CONST = mv_mul(_A, _R, mv_add(mv_scale(mv_mul(_A, _A, _R), -2),
                              mv_scale(mv_mul(_A, _R, _R), 3),
                              mv_scale(mv_mul(_A, _R), -1),
                              mv_scale(_A, 3), mv_scale(_R, -3)))
# M, H, K_alpha
MPOLY = mv_add(mv_scale(mv_mul(_A, _A, _R), -3), mv_scale(mv_mul(_A, _R, _R), 4),
               mv_scale(mv_mul(_A, _R), -2), mv_scale(_A, 4), mv_scale(_R, -3))
HPOLY = mv_add(mv_scale(mv_mul(_A, _A, _R), -8), mv_scale(mv_mul(_A, _R, _R), 9),
               mv_scale(mv_mul(_A, _R), -2), mv_scale(_A, 9), mv_scale(_R, -8))
KPOLY = mv_add(mv_scale(mv_mul(_A, _A, _R), -1), mv_scale(mv_mul(_A, _R, _R), 3),
               mv_scale(mv_mul(_A, _R), -4), mv_scale(_A, 3), mv_scale(_R, -1))

PHI = mv_add(mv_mul(QUAD, _B, _B), mv_mul(LIN, _B), CONST)
PHI_A = mv_deriv(PHI, 0)
PHI_R = mv_deriv(PHI, 1)
PHI_AA = mv_deriv(PHI_A, 0)
PHI_RR = mv_deriv(PHI_R, 1)
PHI_AR = mv_deriv(PHI_A, 1)


def powarr(x, n, p):
    arr = [1] * (n + 1)
    for i in range(1, n + 1):
        arr[i] = arr[i - 1] * x % p
    return arr


def ev3(poly, ap, rp, bp, p):
    s = 0
    for (i, j, k), v in poly.items():
        s += v * ap[i] * rp[j] * bp[k]
    return s % p


# ======================================================================
# Scalar model functions (explicit; identical to the committed dossier).
# A self-consistency assertion against the multivariate engine is run in [A].
# ======================================================================
def A_beta(a, r, p):
    return (3 * a * a * r - 3 * a * r * r + a * r - 3 * a + 2 * r) % p


def B_beta(a, r, p):
    return (-a * r * (a - 1) * (r + 1)) % p


def C_beta(a, r, p):
    return (a * r * (-2 * a * a * r + 3 * a * r * r - a * r + 3 * a - 3 * r)) % p


def Mfun(a, r, p):
    return (-3 * a * a * r + 4 * a * r * r - 2 * a * r + 4 * a - 3 * r) % p


def Hfun(a, r, p):
    return (-8 * a * a * r + 9 * a * r * r - 2 * a * r + 9 * a - 8 * r) % p


def K_alpha(a, r, p):
    return (-a * a * r + 3 * a * r * r - 4 * a * r + 3 * a - r) % p


def Phi_scalar(a, r, b, p):
    return (A_beta(a, r, p) * b * b + B_beta(a, r, p) * b + C_beta(a, r, p)) % p


def good(a, r, p):
    a %= p
    r %= p
    if a == r:
        return False
    A = A_beta(a, r, p)
    C = C_beta(a, r, p)
    if A == 0 or C == 0:
        return False
    if Mfun(a, r, p) == 0 or Hfun(a, r, p) == 0:
        return False
    if K_alpha(a, r, p) == 0:
        return False
    B = B_beta(a, r, p)
    disc = (B * B - 4 * A * C) % p
    if disc == 0 or legendre(disc, p) != 1:
        return False
    return True


# ----- bivariate (a,r) helpers (project the 3-var polys; b numeric) -----
def poly_at_b(poly3, bnum):
    """Collapse a (a,r,b) poly to a (a,r) integer poly by substituting b=bnum."""
    d = {}
    for (i, j, k), c in poly3.items():
        d[(i, j)] = d.get((i, j), 0) + c * (bnum ** k)
    return {k: v for k, v in d.items() if v}


def project_ab(poly3):
    """A (a,r,b) poly with all b-exponents 0 -> (a,r) poly."""
    d = {}
    for (i, j, k), c in poly3.items():
        assert k == 0, "project_ab: nonzero b-exponent"
        d[(i, j)] = d.get((i, j), 0) + c
    return {k: v for k, v in d.items() if v}


def ab_mul(P, Q):
    R = {}
    for (i, j), c in P.items():
        for (k, l), d in Q.items():
            key = (i + k, j + l)
            R[key] = R.get(key, 0) + c * d
    return {k: v for k, v in R.items() if v}


def ab_add(*Ps):
    R = {}
    for P in Ps:
        for k, v in P.items():
            R[k] = R.get(k, 0) + v
    return {k: v for k, v in R.items() if v}


def ab_scale(P, s):
    return {k: v * s for k, v in P.items()} if s else {}


# ======================================================================
# F_{p^k} via discrete-log tables (re-implemented; add by digit recomposition,
# optional heavy add-table; mul by log/exp).  Used for the genus-2 point counts.
# ======================================================================
def _fp_trim(a, p):
    a = [c % p for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _fp_mul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return _fp_trim(r, p)


def _fp_divmod(a, b, p):
    a = _fp_trim(a[:], p)
    b = _fp_trim(b[:], p)
    inv = pow(b[-1], p - 2, p)
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
        d = len(a) - len(b)
        c = (a[-1] * inv) % p
        q[d] = c
        for i, bi in enumerate(b):
            a[d + i] = (a[d + i] - c * bi) % p
        a = _fp_trim(a, p)
        if len(a) == 1 and a[0] == 0:
            break
    return _fp_trim(q, p), a


def _fp_mod(a, b, p):
    return _fp_divmod(a, b, p)[1]


def _fp_gcd(a, b, p):
    a, b = _fp_trim(a[:], p), _fp_trim(b[:], p)
    while not (len(b) == 1 and b[0] == 0):
        a, b = b, _fp_mod(a, b, p)
    inv = pow(a[-1], p - 2, p)
    return [(c * inv) % p for c in a]


def _fp_powmod(base, e, mod, p):
    result = [1]
    base = _fp_mod(base, mod, p)
    while e > 0:
        if e & 1:
            result = _fp_mod(_fp_mul(result, base, p), mod, p)
        e >>= 1
        if e:
            base = _fp_mod(_fp_mul(base, base, p), mod, p)
    return result


def _fp_is_irreducible(f, p):
    d = len(f) - 1
    if d <= 0:
        return False
    x = [0, 1]
    xpd = _fp_powmod(x, p ** d, f, p)
    diff = [(xpd[i] if i < len(xpd) else 0) - (x[i] if i < len(x) else 0)
            for i in range(max(len(xpd), len(x)))]
    if _fp_trim(diff, p) != [0]:
        return False
    for q in factorint(d):
        xpdq = _fp_powmod(x, p ** (d // q), f, p)
        diff = [(xpdq[i] if i < len(xpdq) else 0) - (x[i] if i < len(x) else 0)
                for i in range(max(len(xpdq), len(x)))]
        g = _fp_gcd(f, _fp_trim(diff, p), p)
        if len(g) != 1:
            return False
    return True


class GF:
    """Finite field F_{p^k} on canonical ints 0..q-1 (base-p digit packing)."""

    def __init__(self, p, k, heavy=False):
        self.p = p
        self.k = k
        self.q = p ** k
        q = self.q
        self.pw = [p ** i for i in range(k)]
        digits = [None] * q
        for x in range(q):
            t = []
            xx = x
            for _ in range(k):
                t.append(xx % p)
                xx //= p
            digits[x] = tuple(t)
        self.digits = digits
        if k == 1:
            g = primitive_root(p)
            exp = [0] * (q - 1)
            v = 1
            for i in range(q - 1):
                exp[i] = v
                v = v * g % p
        else:
            f = self._find_irreducible()
            g0 = self._find_generator(f)
            exp = [0] * (q - 1)
            v = [1]
            for i in range(q - 1):
                exp[i] = self._pack(v)
                v = self._poly_mul_mod(v, g0, f)
        self.exp = exp
        log = [0] * q
        for i, e in enumerate(exp):
            log[e] = i
        self.log = log
        self.addtab = None
        if heavy:
            addtab = [0] * (q * q)
            for x in range(q):
                dx = digits[x]
                base = x * q
                for y in range(q):
                    dy = digits[y]
                    s = 0
                    for i in range(k):
                        s += ((dx[i] + dy[i]) % p) * self.pw[i]
                    addtab[base + y] = s
            self.addtab = addtab

    def _pack(self, coeffs):
        s = 0
        for i, c in enumerate(coeffs):
            s += (c % self.p) * self.pw[i]
        return s

    def _poly_mul_mod(self, a, b, f):
        p = self.p
        r = [0] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    r[i + j] = (r[i + j] + ai * bj) % p
        k = self.k
        for d in range(len(r) - 1, k - 1, -1):
            c = r[d]
            if c:
                r[d] = 0
                for i in range(k):
                    r[d - k + i] = (r[d - k + i] - c * f[i]) % p
        return [r[i] % p for i in range(k)]

    def _find_irreducible(self):
        p, k = self.p, self.k
        for tail in product(range(p), repeat=k):
            f = list(tail) + [1]
            if f[0] == 0:
                continue
            if _fp_is_irreducible(_fp_trim(f, p), p):
                return f
        raise ValueError("no irreducible for F_%d^%d" % (p, k))

    def _find_generator(self, f):
        p, k = self.p, self.k
        order = self.q - 1
        primes = list(factorint(order).keys())
        cand = 0
        while True:
            cand += 1
            if cand >= self.q:
                raise ValueError("no generator")
            coeffs = []
            xx = cand
            for _ in range(k):
                coeffs.append(xx % p)
                xx //= p
            ok = True
            for pr in primes:
                e = order // pr
                res = [1]
                base = coeffs[:]
                ee = e
                while ee > 0:
                    if ee & 1:
                        res = self._poly_mul_mod(res, base, f)
                    ee >>= 1
                    if ee:
                        base = self._poly_mul_mod(base, base, f)
                if self._pack(res) == 1:
                    ok = False
                    break
            if ok:
                return coeffs

    def add(self, x, y):
        if self.addtab is not None:
            return self.addtab[x * self.q + y]
        dx = self.digits[x]
        dy = self.digits[y]
        p = self.p
        s = 0
        for i in range(self.k):
            s += ((dx[i] + dy[i]) % p) * self.pw[i]
        return s

    def mul(self, x, y):
        if x == 0 or y == 0:
            return 0
        return self.exp[(self.log[x] + self.log[y]) % (self.q - 1)]

    def fromint(self, n):
        return n % self.p


# ----- genus-2 smooth-model point count of C_b over a finite field -----
def _delta_r_coeffs(bnum):
    """r-graded coefficients of Delta_b(a,r) (b=bnum) as integer polys in a.
    Returns rco[j] = list of (i, c) with term c*a^i*r^j, j=0..3."""
    Db = poly_at_b(PHI, bnum)
    rco = {0: [], 1: [], 2: [], 3: []}
    for (i, j), c in Db.items():
        rco[j].append((i, c))
    return rco


def smooth_count_Cb(bnum, gf, rco):
    """#C_b(F_q) for the smooth model: affine torus/axis points + toric boundary.
    The only affine point with a=0 is the origin (Delta_b(0,r)=2r b^2)."""
    p, k, q = gf.p, gf.k, gf.q
    aff = 1  # the origin (0,0)
    for a in range(1, q):
        a2 = gf.mul(a, a)
        a3 = gf.mul(a2, a)
        apow = (1, a, a2, a3)
        cj = [0, 0, 0, 0]
        for j in range(4):
            s = 0
            for (i, c) in rco[j]:
                s = gf.add(s, gf.mul(gf.fromint(c % p), apow[i]))
            cj[j] = s
        c3, c2, c1, c0 = cj[3], cj[2], cj[1], cj[0]
        cnt = 0
        for r in range(q):
            v = gf.add(gf.mul(c3, r), c2)
            v = gf.add(gf.mul(v, r), c1)
            v = gf.add(gf.mul(v, r), c0)
            if v == 0:
                cnt += 1
        aff += cnt
    bval = bnum % p
    disc = ((3 * bval * bval - bval + 3) ** 2 - 24 * bval * bval) % p
    disc_is_square = (k % 2 == 0) or (legendre(disc, p) == 1)
    bd = (4 if disc_is_square else 0) + 1
    return aff + bd


# ======================================================================
# Singular-point machinery (auto-derived Phi + partials).
# ======================================================================
def singular_points(b, p):
    """All affine singular points of C_b: Phi=Phi_a=Phi_r=0.  Returns
    (torus, axis) with torus = {a,r != 0}, axis = {a=0 or r=0}."""
    bp = powarr(b % p, 2, p)
    torus = []
    axis = []
    for a in range(p):
        ap = powarr(a, 3, p)
        for r in range(p):
            rp = powarr(r, 3, p)
            if ev3(PHI, ap, rp, bp, p):
                continue
            if ev3(PHI_A, ap, rp, bp, p):
                continue
            if ev3(PHI_R, ap, rp, bp, p):
                continue
            if a % p and r % p:
                torus.append((a, r))
            else:
                axis.append((a, r))
    return torus, axis


def hessian(a, r, b, p):
    ap = powarr(a, 3, p)
    rp = powarr(r, 3, p)
    bp = powarr(b % p, 2, p)
    Paa = ev3(PHI_AA, ap, rp, bp, p)
    Prr = ev3(PHI_RR, ap, rp, bp, p)
    Par = ev3(PHI_AR, ap, rp, bp, p)
    return (Paa * Prr - Par * Par) % p, (Paa, Prr, Par)


# ======================================================================
# CHECK [A] -- 9z+14 unipotent transvection in the weight-1 constituent F
# Status: PROVEN-EXACT
# ======================================================================
def check_A_transvection(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[A] 9z+14 (z=-14/9): unipotent transvection IN the rank-8 weight-1 F")
    line("    z=-14/9 <=> b0 a root of 9b^2+14b+9 (disc=-128; b0 rational iff -2 a QR).")
    line("    Per fiber: unique ordinary A1 torus node (Hessian!=0 => mu=1 => drop 1),")
    line("    a!=0 & rM!=0 (L lisse => ODP cycle pure wt 1), node off M=0 (W_0 intact).")
    line("")

    # model self-consistency: explicit scalars == multivariate-engine projection
    sc_ok = True
    for (a, r, b, p) in [(2, 3, 5, 11), (4, 1, 2, 13), (5, 6, 3, 17), (7, 2, 4, 19)]:
        ap, rp, bp = powarr(a, 3, p), powarr(r, 3, p), powarr(b, 2, p)
        if A_beta(a, r, p) != ev3(QUAD, ap, rp, bp, p):
            sc_ok = False
        if B_beta(a, r, p) != ev3(LIN, ap, rp, bp, p):
            sc_ok = False
        if C_beta(a, r, p) != ev3(CONST, ap, rp, bp, p):
            sc_ok = False
        if Mfun(a, r, p) != ev3(MPOLY, ap, rp, bp, p):
            sc_ok = False
        if Phi_scalar(a, r, b, p) != ev3(PHI, ap, rp, bp, p):
            sc_ok = False
    line(f"    model self-consistency (explicit == engine): {'PASS' if sc_ok else 'FAIL'}")
    ok &= sc_ok

    # primes 11..43 with b0 rational (-2 a QR), excluding 2,3,73
    test_primes = [p for p in primes_in(11, 43)
                   if legendre(-2, p) == 1 and p not in (2, 3, 73)]
    line(f"    test primes (b0 rational, 11..43): {test_primes}")
    line("")

    fibers = 0
    all_fib_ok = True
    for p in test_primes:
        inv9 = pow(9, p - 2, p)
        z_expect = (-14 * inv9) % p
        s = sqrt_modp((-128) % p, p)
        if s is None:
            continue
        inv18 = pow(18, p - 2, p)
        b0s = sorted({((-14 + s) * inv18) % p, ((-14 - s) * inv18) % p})
        for b0 in b0s:
            if b0 == 0:
                all_fib_ok = False
                continue
            # z = b0 + 1/b0 must equal -14/9
            z = (b0 + pow(b0, p - 2, p)) % p
            z_ok = (z == z_expect)
            torus, axis = singular_points(b0, p)
            unique_torus = (len(torus) == 1)
            no_axis = (len(axis) == 0)
            node_ok = ord_ok = lisse_ok = w0_ok = False
            a0 = r0 = hv = Mv = rM = None
            if unique_torus:
                a0, r0 = torus[0]
                hv, _ = hessian(a0, r0, b0, p)
                Mv = Mfun(a0, r0, p)
                rM = (r0 * Mv) % p
                node_ok = True
                ord_ok = (hv != 0)                    # ordinary A1 => mu=1
                lisse_ok = (a0 % p != 0 and rM != 0)  # psi,chi unramified at node
                # weight-0 part: the M=0 punctures persist and the node is off them
                bp = powarr(b0, 2, p)
                m0 = [(a, r) for a in range(1, p) for r in range(1, p)
                      if ev3(PHI, powarr(a, 3, p), powarr(r, 3, p), bp, p) == 0
                      and Mfun(a, r, p) == 0]
                w0_ok = (Mv != 0) and (len(m0) >= 1) and ((a0, r0) not in m0)
            fib_ok = (z_ok and unique_torus and no_axis and node_ok
                      and ord_ok and lisse_ok and w0_ok)
            all_fib_ok &= fib_ok
            fibers += 1
            if not check:
                desc = (f"node=({a0},{r0}) Hess={hv} M={Mv}!=0 rM={rM}!=0"
                        if unique_torus else f"torus={torus} axis={axis}")
                line(f"    p={p:3d} b0={b0:3d}: z=-14/9?{z_ok} uniqueA1?{unique_torus} "
                     f"noAxisSing?{no_axis} | {desc}  -> {'PASS' if fib_ok else 'FAIL'}")
    ok &= (all_fib_ok and fibers > 0)
    line("")
    line(f"    {fibers} fiber(s) checked; every one a single ordinary A1 node with L")
    line(f"    lisse and W_0 intact => unit rank drop lands in gr_1^W=F (transvection).")
    line(f"  [A] TRANSVECTION (PROVEN-EXACT): {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# CHECK [B] -- Q8 interior-benign for every psi
# Status: PROVEN-EXACT
# ======================================================================
Q8 = [6561, 8019, -57348, -85860, 164403, 318429, -110031, -450805, -217802]  # high->low


def _q8_eval_modp(z, p):
    r = 0
    for c in Q8:
        r = (r * z + c) % p
    return r


def check_B_q8_benign(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[B] Q8 benign for EVERY psi by interior-point localization")
    line("    All 8 Q8 roots are interior z!=0,inf (off the only places where a rank-1")
    line("    tame Kummer could be a sub/quotient), except at excised bad primes.")
    line("")

    # (a) endpoints Q8(0) and lc(Q8)
    q0 = Q8[-1]
    lc = Q8[0]
    a_ok = (q0 == -217802 and 2 * 13 * 8377 == 217802 and is_prime(8377)
            and lc == 6561 and lc == 3 ** 8)
    bad = sorted(set(factorint(217802)) | set(factorint(lc)))
    line(f"    Q8(0) = {q0} = -{fmt_factor(217802)}   (8377 prime: {is_prime(8377)})")
    line(f"    lc(Q8) = {lc} = {fmt_factor(lc)}")
    line(f"    => endpoints collide (z=0 or z=inf) only at bad primes {bad} = {{2,3,13,8377}}")
    line(f"    endpoints exact: {'PASS' if a_ok else 'FAIL'}")
    ok &= a_ok and bad == [2, 3, 13, 8377]

    # (b) branch-divisor identity  disc_b = lin^2 - 4 q const = a*r*M*H over Z[a,r]
    q2 = project_ab(QUAD)
    lin2 = project_ab(LIN)
    const2 = project_ab(CONST)
    M2 = project_ab(MPOLY)
    H2 = project_ab(HPOLY)
    disc = ab_add(ab_mul(lin2, lin2), ab_scale(ab_mul(q2, const2), -4))
    arMH = ab_mul(ab_mul({(1, 0): 1}, {(0, 1): 1}), ab_mul(M2, H2))
    id_ok = (disc == arMH)
    line("")
    line(f"    disc_b = lin^2 - 4 q const  ==  a*r*M*H  (exact Z[a,r] identity): "
         f"{'PASS' if id_ok else 'FAIL'}")
    ok &= id_ok

    # (c) interior localization: no Q8 root at z=0 (Q8(0)!=0) or z=inf (lc!=0)
    #     for any prime off {2,3,13,8377}.
    interior_ok = True
    bad_set = {2, 3, 13, 8377}
    for p in primes_in(5, 100):
        if p in bad_set:
            continue
        if _q8_eval_modp(0, p) == 0 or lc % p == 0:
            interior_ok = False
    line(f"    over primes 5..100 \\ {{2,3,13,8377}}: no root at z=0 and lc!=0 "
         f"(=> all 8 roots interior): {'PASS' if interior_ok else 'FAIL'}")
    ok &= interior_ok

    line("")
    line("    All 8 Q8 fibers interior => a rank-1 Kummer L_{phi^-1} (lisse at interior")
    line("    pts) cannot be hosted at Q8; Q8 adds NO odd rank-1 reflection. (d in {1,2}")
    line("    stays open but does not affect this benign verdict.)")
    line(f"  [B] Q8 BENIGN (PROVEN-EXACT): {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# CHECK [D] -- z=+-2 branch fibers and the descent involution sigma
# Status: PROVEN-EXACT
# ======================================================================
def check_D_branch_fibers(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[D] z=+-2 branch fibers and the descent involution sigma(a,r)=(1/a,1/r)")
    line("")

    primes = primes_in(11, 73)

    # (1) z=-2 (b=-1): SMOOTH (no torus, no axis singular point) over 11..73
    line("    (1) z=-2 (b=-1): C_{-1} smooth (0 torus + 0 axis singular points)")
    smooth_ok = True
    bad = []
    for p in primes:
        torus, axis = singular_points((-1) % p, p)
        if torus or axis:
            smooth_ok = False
            bad.append((p, torus, axis))
    line(f"        over {len(primes)} primes 11..73: singular pts found = "
         f"{bad if bad else 'none'}  -> {'PASS' if smooth_ok else 'FAIL'}")
    ok &= smooth_ok

    # (2) z=-2 genus 2: Weil genus-2 zeta consistency + functional-equation anchor.
    line("    (2) z=-2 genus 2 (Weil genus-2 zeta; parity asserted, never None):")
    rco_m1 = _delta_r_coeffs(-1)
    genus_ok = True
    for p in [7, 11, 13, 17, 19]:
        N1 = smooth_count_Cb(-1, GF(p, 1), rco_m1)
        N2 = smooth_count_Cb(-1, GF(p, 2), rco_m1)
        s1 = p + 1 - N1
        s2 = p * p + 1 - N2
        a1 = s1
        parity = ((s1 * s1 - s2) % 2 == 0)   # genus-2 a2 integrality (asserted)
        if not parity:
            genus_ok = False
            line(f"        p={p:3d}: PARITY FAIL s1^2-s2={s1*s1-s2} odd (a2 non-integral)")
            continue
        a2 = (s1 * s1 - s2) // 2
        weil = (abs(a1) <= 4 * (p ** 0.5) + 1e-9)
        genus_ok &= weil
        line(f"        p={p:3d}: N1={N1:4d} N2={N2:5d}  genus-2 zeta numerator "
             f"[1, {-a1}, {a2}, {-p*a1}, {p*p}]  a1={a1} a2={a2}  Weil-g2={weil}")
    # full functional-equation anchor at p=7: predict N3, compare to counted N3
    p = 7
    N1 = smooth_count_Cb(-1, GF(p, 1), rco_m1)
    N2 = smooth_count_Cb(-1, GF(p, 2), rco_m1)
    N3 = smooth_count_Cb(-1, GF(p, 3, heavy=True), rco_m1)
    s1 = p + 1 - N1
    s2 = p * p + 1 - N2
    assert (s1 * s1 - s2) % 2 == 0, "genus-2 a2 parity (p=7) -- non-integral, model broken"
    a1 = s1
    a2 = (s1 * s1 - s2) // 2
    a3 = p * a1
    s3_pred = a1 * s2 - a2 * s1 + 3 * a3
    N3_pred = p ** 3 + 1 - s3_pred
    fe_ok = (N3 == N3_pred)
    genus_ok &= fe_ok
    line(f"        FE anchor p=7: counted N3={N3}, genus-2 predicted N3={N3_pred}  "
         f"match={fe_ok}  => g(C_-1)=2")
    line(f"        genus-2 consistent: {'PASS' if genus_ok else 'FAIL'}")
    ok &= genus_ok

    # (3) z=2 (b=1): SINGULAR at (1,1), degenerate ordinary triple point, M(1,1)=0.
    line("    (3) z=2 (b=1): C_1 singular at (1,1) -- degenerate triple point, M(1,1)=0")
    triple_ok = True
    for p in primes:
        torus, _ = singular_points(1 % p, p)
        if torus != [(1, 1)]:
            triple_ok = False
            continue
        hv, (Paa, Prr, Par) = hessian(1, 1, 1, p)
        two_jet_zero = (Paa % p == 0 and Prr % p == 0 and Par % p == 0)  # triple pt
        degenerate = (A_beta(1, 1, p) == 0 and C_beta(1, 1, p) == 0
                      and Mfun(1, 1, p) == 0 and Hfun(1, 1, p) == 0
                      and K_alpha(1, 1, p) == 0)
        B = B_beta(1, 1, p)
        disc = (B * B - 4 * A_beta(1, 1, p) * C_beta(1, 1, p)) % p  # branch point disc=0
        if not (two_jet_zero and degenerate and disc == 0):
            triple_ok = False
    line(f"        over {len(primes)} primes: unique node (1,1), 2-jet=0 (triple point),")
    line(f"        A=C=M=H=K=0 & branch disc=0 & M(1,1)=0 (chi ramified): "
         f"{'PASS' if triple_ok else 'FAIL'}")
    ok &= triple_ok

    # (4) sigma(a,r)=(1/a,1/r): genuine involution; covers b<->1/b; preserves
    #     C_{-1} and chi(rM); genuine torus fixed point (-1,-1).
    line("    (4) sigma(a,r)=(1/a,1/r): involution, deck swap, chi(rM)-preserving,")
    line("        genuine fixed point (-1,-1):")
    sigma_ok = True
    sprimes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    for p in sprimes:
        inv = [0] * p
        for x in range(1, p):
            inv[x] = pow(x, p - 2, p)
        involution = descent = preserve = chi_pres = True
        for a in range(1, p):
            ai = inv[a]
            for r in range(1, p):
                ri = inv[r]
                # involution sigma^2 = id
                if (inv[ai], inv[ri]) != (a, r):
                    involution = False
                # descent: [A:B:C](1/a,1/r) ~ [C:B:A](a,r) (A<->C swap, B fixed)
                A1, B1, C1 = A_beta(ai, ri, p), B_beta(ai, ri, p), C_beta(ai, ri, p)
                A0, B0, C0 = A_beta(a, r, p), B_beta(a, r, p), C_beta(a, r, p)
                v1 = (A1, B1, C1)
                v2 = (C0, B0, A0)
                if any((v1[i] * v2[j] - v1[j] * v2[i]) % p
                       for i in range(3) for j in range(i + 1, 3)):
                    descent = False
                # preserve C_{-1}
                on = (Phi_scalar(a, r, (-1) % p, p) == 0)
                on_s = (Phi_scalar(ai, ri, (-1) % p, p) == 0)
                if on != on_s:
                    preserve = False
                # chi(rM) preserved on C_{-1} (away from chi-zeros)
                if on:
                    rM = (r * Mfun(a, r, p)) % p
                    rMs = (ri * Mfun(ai, ri, p)) % p
                    if rM and rMs and legendre(rM, p) != legendre(rMs, p):
                        chi_pres = False
        # genuine fixed point (-1,-1): sigma fixes it, it lies on C_{-1}, and it
        # is NOT the (A=B=C=0) base point.
        m1 = (p - 1) % p
        fp_on = (Phi_scalar(m1, m1, (-1) % p, p) == 0)
        fp_fixed = (inv[m1] == m1)
        fp_genuine = not (A_beta(m1, m1, p) == 0 and B_beta(m1, m1, p) == 0
                          and C_beta(m1, m1, p) == 0)
        # the OTHER coordinate-fixed point (1,1) is exactly the base point:
        base_pt = (A_beta(1, 1, p) == 0 and B_beta(1, 1, p) == 0 and C_beta(1, 1, p) == 0)
        good_p = (involution and descent and preserve and chi_pres
                  and fp_on and fp_fixed and fp_genuine and base_pt)
        sigma_ok &= good_p
        if not check and p in (11, 23, 43):
            line(f"        p={p:3d}: invol={involution} descent={descent} "
                 f"preserveC_-1={preserve} chi(rM)pres={chi_pres} "
                 f"(-1,-1) genuine-fixed={fp_on and fp_fixed and fp_genuine}")
    line(f"        sigma genuine chi(rM)-preserving involution, fixed pt (-1,-1) "
         f"genuine [(1,1)=base pt]: {'PASS' if sigma_ok else 'FAIL'}")
    ok &= sigma_ok

    line("")
    line(f"  [D] BRANCH FIBERS (PROVEN-EXACT): {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# CHECK [II] -- the elementary Lefschetz route is BLOCKED for general psi.
# Status: STRUCTURAL / CITABLE-CONDITIONAL.  PASSES by confirming the obstruction
# (sigma^*L !~= L); documents a LIMITATION, does NOT close item (II).
# ======================================================================
def check_II_lefschetz_blocked(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[II] LIMITATION (does NOT close (II)): elementary Lefschetz route blocked")
    line("     sigma sends a -> 1/a, so psi(a) -> psi(1/a) = psi(a)^{-1}.  For any")
    line("     non-quadratic psi (ord psi > 2) there are points with psi(a)!=psi(1/a),")
    line("     so sigma^*L !~= L: no L-equivariant involution => no finite fixed-point")
    line("     trace.  This check PASSES by confirming that obstruction.")
    line("")

    # representative non-quadratic psi = a CUBIC character (order 3), via discrete
    # log mod 3, on primes with 3 | p-1.  psi(a)!=psi(1/a) <=> 2*dlog3(a) != 0 mod 3.
    obstruct_ok = True
    test_primes = [p for p in [13, 19, 31, 37, 43, 61, 73] if (p - 1) % 3 == 0]
    for p in test_primes:
        g = primitive_root(p)
        n = 3  # representative non-quadratic order
        dlog = [0] * p
        x = 1
        for e in range(p - 1):
            dlog[x] = e
            x = x * g % p
        # global witness a=g: psi(g)=zeta_3 != psi(1/g)=zeta_3^{-1}
        eg = dlog[g] % n
        eg_inv = (-dlog[g]) % n
        witness_global = (eg != eg_inv)
        # on-curve witnesses: (a,r) on C_{-1} with a genuinely moved (a not in
        # {1,-1}) and psi(a) != psi(1/a).
        moved_diff = 0
        example = None
        inv = [pow(x, p - 2, p) if x else 0 for x in range(p)]
        for a in range(2, p - 1):           # a != 1 and a != p-1=-1
            for r in range(1, p):
                if Phi_scalar(a, r, (-1) % p, p) != 0:
                    continue
                if (2 * dlog[a]) % n != 0:   # psi(a) != psi(1/a)
                    moved_diff += 1
                    if example is None:
                        example = (a, r, dlog[a] % n, (-dlog[a]) % n)
        on_curve_witness = (moved_diff > 0)
        good_p = witness_global and on_curve_witness
        obstruct_ok &= good_p
        if not check:
            ex = (f"e.g. (a,r)=({example[0]},{example[1]}): "
                  f"psi-exp(a)={example[2]} vs psi-exp(1/a)={example[3]}"
                  if example else "(none)")
            line(f"     p={p:3d}: psi=cubic char; psi(g)!=psi(1/g): {witness_global}; "
                 f"on C_-1 #(a-moved & psi differs)={moved_diff}  {ex}")
    line("")
    line(f"     obstruction confirmed (sigma^*L !~= L for non-quadratic psi): "
         f"{'PASS' if obstruct_ok else 'FAIL'}")
    line("     => the Lefschetz local terms Tr(sigma|L_x) are undefined; (II) is NOT")
    line("        closable by this finite fixed-point method (limitation documented,")
    line("        not a closure).  chi(rM) IS preserved (see [D]); the obstruction is")
    line("        purely the psi-part.")
    ok &= obstruct_ok
    line(f"  [II] LEFSCHETZ-BLOCKED (limitation; obstruction confirmed): "
         f"{'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# Driver
# ======================================================================
def main(check=False):
    if not check:
        print("=" * 72)
        print("M1 (BETA_2) conditional-close -- exact verifier certificate")
        print("Status: AUDIT (PROVEN-EXACT note results A,B,D + structural (II))")
        print("=" * 72)
        print()

    results = []
    results.append(("A-TRANSVEC", check_A_transvection(check), "PROVEN-EXACT"))
    results.append(("B-Q8BENIGN", check_B_q8_benign(check), "PROVEN-EXACT"))
    results.append(("D-BRANCH", check_D_branch_fibers(check), "PROVEN-EXACT"))
    results.append(("II-BLOCKED", check_II_lefschetz_blocked(check), "LIMITATION"))

    all_ok = all(r for _, r, _ in results)
    if check:
        for name, r, tag in results:
            print(f"{name:11s} [{tag:12s}] {'PASS' if r else 'FAIL'}")
        print("PASS" if all_ok else "FAIL")
    else:
        print("=" * 72)
        print("SUMMARY")
        for name, r, tag in results:
            print(f"  [{name:11s}] {tag:12s}  {'PASS' if r else 'FAIL'}")
        print("-" * 72)
        print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
        print("  (A,B,D are PROVEN-EXACT; II PASSES by confirming the obstruction,")
        print("   documenting why item (II) is not closable by this method.)")
        print("=" * 72)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
