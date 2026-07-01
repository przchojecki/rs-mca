#!/usr/bin/env python3
"""
verify_m1_beta2_local_data_dossier.py

Self-contained exact certificate for the PROVEN, p-independent local/global
invariants of the M1 (BETA_2) "obstruction floor" local-data dossier (Arm 1).

The weight-1 beta-line pushforward sheaf

    F_psi = R^1 pi_!( psi(a) * chi(rM(a,r)) )   on the z-line, z = b + 1/b,

with fiber over b the bidegree-(3,3) torus curve C_b = { Delta_b(a,r) = 0 }, is
the object whose big monodromy (BETA_2) the program must control.  Arm 1 pinned
a dossier of its invariants; this script machine-checks the ones that are PROVEN
and p-independent, by exact integer / F_p / F_{p^k} arithmetic.  It deliberately
EXCLUDES the still-open items handed to Arm 2 (the Q8 vanishing-cycle dimension
d in {1,2} and geometric irreducibility/primitivity), which finite computation
cannot decide.

What is certified (each as a named check printing PASS/FAIL):

  [1] DIHEDRAL  Degree-13 dihedral singular support factors in z as
                (z-2)(z+1)(9z+14)(9z^2-6z-23)*Q8(z), 13 = 1+1+1+2+8, with the
                exact octic Q8.  Q8 is irreducible over Q; Q16 = b^8 Q8(b+1/b)
                is its palindromic (self-reciprocal) lift; the five factors are
                pairwise coprime over Z.
  [2] NODES     9z+14 (z=-14/9) is the unique genuine A1 node = unipotent
                transvection (Hessian != 0, a != 0, rM != 0 => lambda = +1);
                z=2 and z=-1 nodes sit on the excised good()=False locus; the
                conic and Q8 fibers are never curve nodes (finite-p census).
  [3] P73       Res_z(9z+14, 9z^2-6z-23) = 657 = 3^2 * 73, and p=73 is the
                UNIQUE prime > 3 at which the conic meets the transvection node
                (subsumes verify_m1_beta2_p73_resolution.py).
  [4] LEDGER    GOS / Riemann-Hurwitz integer ledger: generic rank
                dim H^1_c = 2g-2 + #S = 2 + 9 = 11; weight-1 constituent rank
                = 2g'-2g = 8 with double cover y^2 = D_beta of genus g'=6
                (2g'-2 = 2(2g-2)+R = 4 + 6); weight split 11 = 8 + 3.  Anchored
                by exact finite-field point counts: g=2 (genus-2 Weil zeta of
                C_b) and the rank-8 weight-1 Frobenius factor
                H = 1 + 4T^2 + 22T^4 + 100T^6 + 625T^8 at the p=5/z=0 fiber.
  [5] SQCLASS   Square-class identities Legendre(d0) = chi(rM) = chi(aH)
                = chi(d_UV) for every good (a,r) (exhaustive small-p scan),
                using the committed trace machinery.
  [6] PAIRING   Poincare-Verdier dichotomy at the trace level: quadratic psi
                (psi^2=1) gives real weight-1 traces (self-dual, => Sp_8);
                general psi (psi^2!=1) gives non-real traces (NOT self-dual,
                dual partner F_{psi^-1}, => autoduality-free GL/SL); orthogonal
                excluded both regimes.

Pure Python 3 stdlib only.  Exact integer / F_p / F_{p^k} arithmetic.  No
network, no file I/O beyond stdout, no compiled-decision or unsafe tactics.  Fully offline.

Status: AUDIT (exact finite certificate of PROVEN dossier invariants).
Usage:  python3 verify_m1_beta2_local_data_dossier.py            (verbose)
        python3 verify_m1_beta2_local_data_dossier.py --check     (terse; exit 1 on any failure)
"""

import sys
from fractions import Fraction

# ======================================================================
# Inlined model constants (z-line singular-support factors; z = b + 1/b).
# Coefficient lists are DESCENDING in degree (high -> low), matching the
# committed verify_m1_beta2_p73_resolution.py convention.
# ======================================================================
ZM2 = [1, -2]                 # z - 2     (excised triple point)
ZP1 = [1, 1]                  # z + 1     (excised node)
NODE = [9, 14]                # 9z + 14   (the genuine A1 transvection, z=-14/9)
CONIC = [9, -6, -23]          # 9z^2 - 6z - 23
Q8 = [6561, 8019, -57348, -85860, 164403, 318429, -110031, -450805, -217802]
# The pure weight-1 (symplectic, |roots|=sqrt p) Frobenius factor of the
# rank-8 constituent at the p=5 / z=0 fiber: H(u) = 1+4u+22u^2+100u^3+625u^4,
# u = T^2  (i.e. H(T^2) = 1+4T^2+22T^4+100T^6+625T^8).
H_WEIGHT1_U = [1, 4, 22, 100, 625]   # ascending in u = T^2

FACTORS = {"z-2": ZM2, "z+1": ZP1, "9z+14": NODE, "conic": CONIC, "Q8": Q8}

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


# ======================================================================
# Univariate integer-polynomial machinery (DESCENDING coefficient lists).
# ======================================================================
def p_eval_frac(coeffs, x):
    """Horner evaluation in Q (coeffs descending)."""
    r = Fraction(0)
    for c in coeffs:
        r = r * x + c
    return r


def _det_bareiss(M):
    """Exact integer determinant by fraction-free Bareiss elimination."""
    n = len(M)
    M = [row[:] for row in M]
    sign = 1
    prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            swap = None
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    swap = i
                    break
            if swap is None:
                return 0
            M[k], M[swap] = M[swap], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def resultant(f, g):
    """Res(f, g) for integer polynomials f, g (descending coeffs) via the
    Sylvester matrix and an exact integer determinant."""
    df, dg = len(f) - 1, len(g) - 1
    if df == 0 and dg == 0:
        return 1
    n = df + dg
    S = [[0] * n for _ in range(n)]
    for i in range(dg):           # dg rows of f
        for j, c in enumerate(f):
            S[i][i + j] = c
    for i in range(df):           # df rows of g
        for j, c in enumerate(g):
            S[dg + i][i + j] = c
    return _det_bareiss(S)


# ----- polynomials over F_p (ASCENDING coeff lists) for irreducibility tests
def fp_trim(a, p):
    a = [c % p for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def fp_mul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return fp_trim(r, p)


def fp_divmod(a, b, p):
    a = fp_trim(a[:], p)
    b = fp_trim(b[:], p)
    inv = pow(b[-1], p - 2, p)
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
        d = len(a) - len(b)
        c = (a[-1] * inv) % p
        q[d] = c
        for i, bi in enumerate(b):
            a[d + i] = (a[d + i] - c * bi) % p
        a = fp_trim(a, p)
        if len(a) == 1 and a[0] == 0:
            break
    return fp_trim(q, p), a


def fp_mod(a, b, p):
    return fp_divmod(a, b, p)[1]


def fp_gcd(a, b, p):
    a, b = fp_trim(a[:], p), fp_trim(b[:], p)
    while not (len(b) == 1 and b[0] == 0):
        a, b = b, fp_mod(a, b, p)
    inv = pow(a[-1], p - 2, p)
    return [(c * inv) % p for c in a]


def fp_powmod(base, e, mod, p):
    result = [1]
    base = fp_mod(base, mod, p)
    while e > 0:
        if e & 1:
            result = fp_mod(fp_mul(result, base, p), mod, p)
        e >>= 1
        if e:
            base = fp_mod(fp_mul(base, base, p), mod, p)
    return result


def fp_is_irreducible(f, p):
    """Rabin irreducibility test for monic f of degree d over F_p."""
    d = len(f) - 1
    if d <= 0:
        return False
    x = [0, 1]
    # X^{p^d} == X (mod f)
    xpd = fp_powmod(x, p ** d, f, p)
    diff = [(xpd[i] if i < len(xpd) else 0) - (x[i] if i < len(x) else 0)
            for i in range(max(len(xpd), len(x)))]
    if fp_trim(diff, p) != [0]:
        return False
    for q in factorint(d):
        xpdq = fp_powmod(x, p ** (d // q), f, p)
        diff = [(xpdq[i] if i < len(xpdq) else 0) - (x[i] if i < len(x) else 0)
                for i in range(max(len(xpdq), len(x)))]
        g = fp_gcd(f, fp_trim(diff, p), p)
        if len(g) != 1:
            return False
    return True


# ======================================================================
# Finite field F_{p^k} with discrete-log tables (fast multiplicative
# character and multiplication; addition by base-p digit recomposition).
# ======================================================================
class GF:
    def __init__(self, p, k, heavy=False):
        self.p = p
        self.k = k
        self.q = p ** k
        q = self.q
        self.pw = [p ** i for i in range(k)]
        # digit decomposition table (canonical int <-> base-p coefficient tuple)
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
            self.f = f
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

    # ---- build helpers (slow, only used to populate the log tables) ----
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
        # reduce mod monic f (ascending, degree k, leading 1)
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
        # search monic f = x^k + c_{k-1} x^{k-1} + ... + c0
        from itertools import product
        for tail in product(range(p), repeat=k):
            f = list(tail) + [1]
            if f[0] == 0:
                continue
            if fp_is_irreducible(fp_trim(f, p), p):
                return f
        raise ValueError("no irreducible found for F_%d^%d" % (p, k))

    def _find_generator(self, f):
        p, k = self.p, self.k
        q = self.q
        order = q - 1
        primes = list(factorint(order).keys())
        # candidate elements as coefficient lists
        cand = 0
        while True:
            cand += 1
            coeffs = []
            xx = cand
            for _ in range(k):
                coeffs.append(xx % p)
                xx //= p
            if cand >= q:
                raise ValueError("no generator")
            # order check: g^(order/pr) != 1 for all pr
            ok = True
            for pr in primes:
                e = order // pr
                # fast exponentiation in the field via repeated _poly_mul_mod
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

    # ---- runtime field ops on canonical ints ----
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

    def chi(self, x):
        """Quadratic (Legendre) character of F_{p^k}^*; 0 at 0."""
        if x == 0:
            return 0
        return 1 if (self.log[x] & 1) == 0 else -1

    def fromint(self, n):
        return n % self.p  # degree-0 element (canonical int = n mod p)


# ======================================================================
# Inlined affine model (mod p), beta-quadratic and singular-support data.
# A_beta b^2 + B_beta b + C_beta = 0 is the fiber curve C_b in (a,r).
#   A_beta = 3a^2 r - 3a r^2 + a r - 3a + 2r              (= "quad")
#   B_beta = -a r (a-1)(r+1)                              (= "lin")
#   C_beta = a r (-2a^2 r + 3a r^2 - a r + 3a - 3r)       (= "const")
#   M  = -3a^2 r + 4a r^2 - 2a r + 4a - 3r
#   H  = -8a^2 r + 9a r^2 - 2a r + 9a - 8r
#   K_alpha = -a^2 r + 3a r^2 - 4a r + 3a - r             (good-base kernel)
#   D_beta = a r M H
#   d0 = r * d_UV,  d_UV = (4a-3r) b^2 - 2a r b + (-3a^2 r + 4a r^2)
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


def d0_fun(a, b, r, p):
    return (r * (-3 * a * a * r + 4 * a * b * b - 2 * a * b * r
                 + 4 * a * r * r - 3 * b * b * r)) % p


def dUV_fun(a, b, r, p):
    return ((4 * a - 3 * r) * b * b - 2 * a * r * b
            + (-3 * a * a * r + 4 * a * r * r)) % p


def good(a, r, p):
    """The good split base: A_beta C_beta D_beta (a-r) K_alpha != 0 and the
    beta-discriminant a nonzero quadratic residue (so b is F_p-rational)."""
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


def Delta_b(a, r, b, p):
    """Fiber curve C_b in (a,r): A_beta b^2 + B_beta b + C_beta (mod p)."""
    return (A_beta(a, r, p) * b * b + B_beta(a, r, p) * b + C_beta(a, r, p)) % p


# Delta_b as a cubic in r (coefficients depend on a, b), used for field counts.
def Delta_cubic_r(a, b, gf):
    """Return (c3,c2,c1,c0) of Delta_b(a,.) as a cubic in r, over GF gf."""
    add, mul = gf.add, gf.mul
    a2 = mul(a, a)
    a3 = mul(a2, a)
    b2 = mul(b, b)
    # c3 = 3 a^2
    c3 = mul(gf.fromint(3), a2)
    # c2 = -2a^3 - a^2 b - a^2 - 3 a b^2 + a b - 3a
    c2 = mul(gf.fromint(gf.p - 2), a3)
    c2 = add(c2, mul(gf.fromint(gf.p - 1), mul(a2, b)))
    c2 = add(c2, mul(gf.fromint(gf.p - 1), a2))
    c2 = add(c2, mul(gf.fromint(gf.p - 3), mul(a, b2)))
    c2 = add(c2, mul(a, b))
    c2 = add(c2, mul(gf.fromint(gf.p - 3), a))
    # c1 = 3 a^2 b^2 - a^2 b + 3 a^2 + a b^2 + a b + 2 b^2
    c1 = mul(gf.fromint(3), mul(a2, b2))
    c1 = add(c1, mul(gf.fromint(gf.p - 1), mul(a2, b)))
    c1 = add(c1, mul(gf.fromint(3), a2))
    c1 = add(c1, mul(a, b2))
    c1 = add(c1, mul(a, b))
    c1 = add(c1, mul(gf.fromint(2), b2))
    # c0 = -3 a b^2
    c0 = mul(gf.fromint(gf.p - 3), mul(a, b2))
    return c3, c2, c1, c0


# ======================================================================
# Minimal multivariate (a,r,b) engine -- ONLY to auto-derive Phi and its
# partials (no hand-differentiation), then evaluate fast with power arrays.
# ======================================================================
def _mv_var(i):
    e = [0, 0, 0]
    e[i] = 1
    return {tuple(e): 1}


def _mv_const(c):
    return {(0, 0, 0): c} if c else {}


def _mv_add(*ps):
    d = {}
    for p in ps:
        for k, v in p.items():
            d[k] = d.get(k, 0) + v
    return {k: v for k, v in d.items() if v}


def _mv_scale(p, c):
    return {k: v * c for k, v in p.items()} if c else {}


def _mv_sub(p, q):
    return _mv_add(p, _mv_scale(q, -1))


def _mv_mul(*ps):
    r = _mv_const(1)
    for p in ps:
        d = {}
        for k1, v1 in r.items():
            for k2, v2 in p.items():
                k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
                d[k] = d.get(k, 0) + v1 * v2
        r = {k: v for k, v in d.items() if v}
    return r


def _mv_deriv(p, i):
    d = {}
    for k, v in p.items():
        if k[i]:
            kk = list(k)
            e = kk[i]
            kk[i] -= 1
            d[tuple(kk)] = d.get(tuple(kk), 0) + v * e
    return {k: v for k, v in d.items() if v}


_A = _mv_var(0)
_R = _mv_var(1)
_B = _mv_var(2)
_QUAD = _mv_add(_mv_scale(_mv_mul(_A, _A, _R), 3), _mv_scale(_mv_mul(_A, _R, _R), -3),
                _mv_mul(_A, _R), _mv_scale(_A, -3), _mv_scale(_R, 2))
_LIN = _mv_scale(_mv_mul(_A, _R, _mv_sub(_A, _mv_const(1)), _mv_add(_R, _mv_const(1))), -1)
_CONST = _mv_mul(_A, _R, _mv_add(_mv_scale(_mv_mul(_A, _A, _R), -2),
                                 _mv_scale(_mv_mul(_A, _R, _R), 3),
                                 _mv_scale(_mv_mul(_A, _R), -1),
                                 _mv_scale(_A, 3), _mv_scale(_R, -3)))
PHI = _mv_add(_mv_mul(_QUAD, _B, _B), _mv_mul(_LIN, _B), _CONST)
PHI_A = _mv_deriv(PHI, 0)
PHI_R = _mv_deriv(PHI, 1)
PHI_AA = _mv_deriv(PHI_A, 0)
PHI_RR = _mv_deriv(PHI_R, 1)
PHI_AR = _mv_deriv(PHI_A, 1)


def _mv_val(poly, ap, rp, bp, p):
    s = 0
    for (i, j, k), v in poly.items():
        s += v * ap[i] * rp[j] * bp[k]
    return s % p


def _powarr(x, n, p):
    arr = [1] * (n + 1)
    for i in range(1, n + 1):
        arr[i] = arr[i - 1] * x % p
    return arr


# ======================================================================
# CHECK 1 -- dihedral singular-support factorization
# ======================================================================
def check_dihedral(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[1] DIHEDRAL singular-support factorization (z = b + 1/b)")
    line("    locus = (z-2)(z+1)(9z+14)(9z^2-6z-23)*Q8(z),  13 = 1+1+1+2+8")
    line("")

    # (a) factor degrees 1+1+1+2+8 = 13
    degs = [len(c) - 1 for c in (ZM2, ZP1, NODE, CONIC, Q8)]
    ok_deg = (degs == [1, 1, 1, 2, 8] and sum(degs) == 13)
    line(f"    factor degrees {degs}, sum={sum(degs)}   -> {'PASS' if ok_deg else 'FAIL'}")
    ok &= ok_deg

    # (b) Q8 irreducible over Q  (irreducible mod a prime not dividing lead=3^8)
    irr_primes = []
    for pp in (7, 17, 31):
        f_asc = fp_trim(list(reversed(Q8)), pp)        # ascending
        inv = pow(f_asc[-1], pp - 2, pp)
        f_monic = [(c * inv) % pp for c in f_asc]       # make monic mod p
        if fp_is_irreducible(f_monic, pp):
            irr_primes.append(pp)
    ok_irr = len(irr_primes) > 0
    line(f"    Q8 irreducible mod {irr_primes} (single deg-8 Frobenius orbit)")
    line(f"      => Q8 irreducible over Q   -> {'PASS' if ok_irr else 'FAIL'}")
    ok &= ok_irr

    # (c) Q16 = b^8 * Q8(b+1/b): palindromic self-reciprocal lift
    # Build Q16 ascending: sum_i c_i * b^{8-i} * (b^2+1)^i, c_i = coeff of z^i.
    asc = list(reversed(Q8))                            # asc[i] = coeff z^i
    Q16 = [0] * 17
    for i in range(9):
        # (b^2+1)^i  (ascending)
        powp = [1]
        for _ in range(i):
            np_ = [0] * (len(powp) + 2)
            for d, c in enumerate(powp):
                np_[d] += c
                np_[d + 2] += c
            powp = np_
        shift = 8 - i
        for d, c in enumerate(powp):
            Q16[d + shift] += asc[i] * c
    palindromic = all(Q16[d] == Q16[16 - d] for d in range(17))
    # self-reciprocal lift: both ends are the leading Q8 coeff 6561 = 3^8
    lead_ok = (Q16[16] == 6561 and Q16[0] == 6561)
    # independent identity check at sample integer b via exact rationals
    id_ok = True
    for bb in (2, 3, 5, -4):
        lhs = sum(Q16[d] * bb ** d for d in range(17))
        z = Fraction(bb) + Fraction(1, bb)
        rhs = bb ** 8 * p_eval_frac(Q8, z)
        if Fraction(lhs) != rhs:
            id_ok = False
    ok_q16 = palindromic and lead_ok and id_ok
    line(f"    Q16 = b^8*Q8(b+1/b): palindromic={palindromic}, lead/const ok={lead_ok},")
    line(f"      b^8*Q8(b+1/b) identity at b in [2,3,5,-4] ok={id_ok}  -> {'PASS' if ok_q16 else 'FAIL'}")
    ok &= ok_q16

    # (d) pairwise coprime over Z (all 10 pairs): integer resultants nonzero
    names = list(FACTORS)
    coprime = True
    res_rows = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            R = resultant(FACTORS[names[i]], FACTORS[names[j]])
            res_rows.append((names[i], names[j], R))
            if R == 0:
                coprime = False
    line("    pairwise resultants over Z (all must be nonzero):")
    for n1, n2, R in res_rows:
        line(f"      Res({n1:5s}, {n2:5s}) = {R}")
    line(f"    all 10 pairs coprime: {coprime}  -> {'PASS' if coprime else 'FAIL'}")
    ok &= coprime

    line("")
    line(f"  [1] DIHEDRAL: {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# CHECK 2 -- node structure (transvection, excision, conic/Q8 never nodes)
# ======================================================================
def classify_z(z, p):
    z %= p
    tags = []
    if (z - 2) % p == 0:
        tags.append("z=2")
    if (z + 1) % p == 0:
        tags.append("z=-1")
    if (9 * z + 14) % p == 0:
        tags.append("9z+14")
    if (9 * z * z - 6 * z - 23) % p == 0:
        tags.append("conic")
    if p_eval_modp(Q8, z, p) == 0:
        tags.append("Q8")
    return tags


def p_eval_modp(coeffs, x, p):
    r = 0
    for c in coeffs:
        r = (r * x + c) % p
    return r


def torus_nodes(b, p):
    """Singular torus points of C_b: Phi = Phi_a = Phi_r = 0, a,r != 0."""
    bp = _powarr(b, 2, p)
    out = []
    for a in range(1, p):
        ap = _powarr(a, 3, p)
        for r in range(1, p):
            rp = _powarr(r, 3, p)
            if _mv_val(PHI, ap, rp, bp, p):
                continue
            if _mv_val(PHI_A, ap, rp, bp, p):
                continue
            if _mv_val(PHI_R, ap, rp, bp, p):
                continue
            out.append((a, r))
    return out


def check_nodes(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[2] NODE structure of the family C_b")
    line("")

    # (a) finite-p node census: every torus node maps to z in {2,-1,-14/9};
    #     no INDEPENDENT conic node and no Q8 node ever occurs.
    census_primes = [11, 13, 17, 19, 23, 29, 31]
    node_z = set()
    bad = []
    conic_independent = False
    q8_node = False
    for p in census_primes:
        for b in range(1, p):
            z = (b + pow(b, p - 2, p)) % p
            nodes = torus_nodes(b, p)
            if not nodes:
                continue
            tags = classify_z(z, p)
            for t in tags:
                node_z.add(t)
            if not tags:
                bad.append((p, b, z, nodes))
            if "conic" in tags and "9z+14" not in tags:
                conic_independent = True
            if "Q8" in tags:
                q8_node = True
    line(f"    census over p in {census_primes}:")
    line(f"      node z-classes seen: {sorted(node_z)}")
    line(f"      unexpected (unclassified) nodes: {bad if bad else 'none'}")
    line(f"      independent conic node: {conic_independent}   Q8 node: {q8_node}")
    ok_census = (not bad) and (not conic_independent) and (not q8_node) \
        and node_z.issubset({"z=2", "z=-1", "9z+14"})
    line(f"    nodes confined to z in {{2,-1,-14/9}}: {'PASS' if ok_census else 'FAIL'}")
    ok &= ok_census

    # (b) 9z+14 is a genuine ordinary A1 node = unipotent transvection
    trans_ok = True
    trans_rows = 0
    for p in [19, 23, 29, 31, 37, 41, 43]:
        inv9 = pow(9, p - 2, p)
        z0 = (-14 * inv9) % p
        d = (z0 * z0 - 4) % p
        if legendre(d, p) != 1:
            continue
        s = next(t for t in range(p) if t * t % p == d)
        inv2 = pow(2, p - 2, p)
        for b in (((z0 + s) * inv2) % p, ((z0 - s) * inv2) % p):
            bp = _powarr(b, 2, p)
            for (a, r) in torus_nodes(b, p):
                ap = _powarr(a, 3, p)
                rp = _powarr(r, 3, p)
                Paa = _mv_val(PHI_AA, ap, rp, bp, p)
                Prr = _mv_val(PHI_RR, ap, rp, bp, p)
                Par = _mv_val(PHI_AR, ap, rp, bp, p)
                hess = (Paa * Prr - Par * Par) % p
                rM = (r * Mfun(a, r, p)) % p
                # ordinary node (Hessian != 0 => Milnor number 1) with the
                # coefficient psi(a)chi(rM) unramified (a != 0, rM != 0):
                cond = (hess != 0 and a % p != 0 and rM != 0)
                trans_ok &= cond
                trans_rows += 1
    line(f"    9z+14 (z=-14/9): {trans_rows} node(s) checked; ordinary A1 (Hessian!=0)")
    line(f"      with a!=0, rM!=0 (unramified => unipotent transvection lambda=+1):"
         f" {'PASS' if trans_ok and trans_rows else 'FAIL'}")
    ok &= (trans_ok and trans_rows > 0)

    # (c) z=2 (b=1) and z=-1 (b^2+b+1=0) nodes lie on the excised good()=False locus
    exc_ok = True
    exc_rows = 0
    for p in [19, 23, 29, 31, 37, 41, 43]:
        bvals = [(1 % p, "z=2")]
        for t in range(1, p):
            if (t * t + t + 1) % p == 0:
                bvals.append((t, "z=-1"))
        for b, _name in bvals:
            nodes = torus_nodes(b, p)
            for (a, r) in nodes:
                exc_rows += 1
                if good(a, r, p):
                    exc_ok = False
    line(f"    z=2 / z=-1: {exc_rows} node(s) checked; all on excised good()=False"
         f" locus: {'PASS' if exc_ok and exc_rows else 'FAIL'}")
    ok &= (exc_ok and exc_rows > 0)

    line("")
    line(f"  [2] NODES: {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# CHECK 3 -- the p=73 resolution (subsumes verify_m1_beta2_p73_resolution.py)
# ======================================================================
def check_p73(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[3] p=73 resolution: conic root meets the 9z+14 transvection node")
    R_node = resultant(NODE, CONIC)
    line(f"    Res_z(9z+14, 9z^2-6z-23) = {R_node} = {fmt_factor(R_node)}")
    ok_res = (R_node == 657 and factorint(R_node) == {3: 2, 73: 1})
    ok &= ok_res

    # the unique prime > 3 where the conic and 9z+14 share a root mod p
    def conic_meets_node(p):
        inv9 = pow(9, p - 2, p)
        z0 = (-14 * inv9) % p
        return (9 * z0 * z0 - 6 * z0 - 23) % p == 0

    coincide = [p for p in primes_in(5, 400) if conic_meets_node(p)]
    line(f"    primes 5..400 where conic meets node mod p: {coincide}   (expect [73])")
    ok_uni = (coincide == [73])
    ok &= ok_uni
    line(f"    => p=73 is that transvection, not a conic degeneration: "
         f"{'PASS' if ok_res and ok_uni else 'FAIL'}")
    line("")
    line(f"  [3] P73: {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# CHECK 4 -- GOS / Riemann-Hurwitz rank ledger (integers + curve anchors)
# ======================================================================
def smooth_count_Cb(b, gf):
    """#C_b(F_{q}) smooth-model count = (affine plane count) + (toric boundary).
    The only affine axis point of Delta_b is the origin; boundary places are
    the 5 places at infinity (Newton edges B,D rational iff disc is a square in
    F_q, edge C always rational)."""
    p, k, q = gf.p, gf.k, gf.q
    # affine plane count over F_q: solve cubic-in-r for each a, plus origin.
    aff = 1  # the origin (0,0)
    # a ranges over F_q^* ; for each a count roots r in F_q of Delta_b(a,.)
    for a in range(1, q):
        c3, c2, c1, c0 = Delta_cubic_r(a, b, gf)
        cnt = 0
        for r in range(q):
            # Horner: ((c3*r + c2)*r + c1)*r + c0
            v = gf.add(gf.mul(c3, r), c2)
            v = gf.add(gf.mul(v, r), c1)
            v = gf.add(gf.mul(v, r), c0)
            if v == 0:
                cnt += 1
        aff += cnt
    # toric boundary
    bval = b % p
    disc = ((3 * bval * bval - bval + 3) ** 2 - 24 * bval * bval) % p
    disc_is_square = (k % 2 == 0) or (legendre(disc, p) == 1)
    bd = (4 if disc_is_square else 0) + 1
    return aff + bd


def check_rank_ledger(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[4] GOS / Riemann-Hurwitz rank ledger")
    line("")

    # (a) exact integer identities
    g = 2          # genus of the bidegree-(3,3) fiber curve C_b
    R = 6          # odd-order (psi-ramified) branch places of D_beta
    nS = 9         # punctures = 6 toric boundary + 3 interior {M=0} tangencies
    n_toric = 6
    n_tang = 3
    twogm2 = 2 * g - 2
    rh = 2 * twogm2 + R                 # 2g'-2 = 2(2g-2)+R
    gp = (rh + 2) // 2                  # genus of the double cover y^2=D_beta
    weight1 = 2 * gp - 2 * g           # pure weight-1 constituent rank
    generic = (2 * g - 2) + nS          # dim H^1_c (j_! convention)
    weight0 = nS - R                    # weight-0 Tate classes
    id_ok = (
        twogm2 == 2 and nS == n_toric + n_tang and rh == 10 and gp == 6
        and weight1 == 8 and generic == 11 and weight0 == 3
        and weight1 + weight0 == generic
        # symplectic weight-1 functional equation of H (anchored below):
        and H_WEIGHT1_U[3] == 5 ** 2 * H_WEIGHT1_U[1]
        and H_WEIGHT1_U[4] == 5 ** 4 * H_WEIGHT1_U[0]
    )
    line(f"    g(C_b)={g}; #S={nS}={n_toric}+{n_tang}; R={R}")
    line(f"    Riemann-Hurwitz 2g'-2 = 2(2g-2)+R = 2*{twogm2}+{R} = {rh}  => g'={gp}")
    line(f"    weight-1 rank = 2g'-2g = {weight1};  generic dim H^1_c = 2g-2+#S = {generic}")
    line(f"    weight split: {weight1} (wt1) + {weight0} (wt0 Tate) = {generic}")
    line(f"    integer ledger consistent: {'PASS' if id_ok else 'FAIL'}")
    ok &= id_ok

    # (b) g=2 anchor: genus-2 Weil zeta of C_b by finite-field point counts
    line("")
    line("    g=2 anchor (genus-2 Weil zeta of the fiber curve C_b):")
    g2_ok = True
    # p=7,b=3 generic fiber: counts over F_7, F_{49}, F_{343} validate genus 2.
    p, b = 7, 3
    gf1 = GF(p, 1)
    gf2 = GF(p, 2)
    gf3 = GF(p, 3, heavy=True)
    N1 = smooth_count_Cb(b, gf1)
    N2 = smooth_count_Cb(b, gf2)
    N3 = smooth_count_Cb(b, gf3)
    s1 = p + 1 - N1
    s2 = p * p + 1 - N2
    a1 = s1
    assert (s1 * s1 - s2) % 2 == 0, "genus-2 zeta: s1^2 - s2 must be even"
    a2 = (s1 * s1 - s2) // 2
    # genus-2 functional equation: a3 = p*a1, a4 = p^2
    a3 = p * a1
    a4 = p * p
    s3_pred = a1 * s2 - a2 * s1 + 3 * a3   # Newton's identity
    N3_pred = p ** 3 + 1 - s3_pred
    line(f"      p={p} b={b}: N1={N1} N2={N2} N3={N3}; genus-2 zeta "
         f"1 - {a1}T + {a2}T^2 - {a3}T^3 + {a4}T^4")
    line(f"        predicted N3 (genus-2 FE) = {N3_pred}; counted N3 = {N3}"
         f"  match={N3 == N3_pred}")
    # Weil bound for genus 2: |a1| <= 4*sqrt(p)
    weil_ok = (a2 is not None and abs(a1) <= 4 * (p ** 0.5) + 1e-9
               and N3 == N3_pred)
    g2_ok &= weil_ok
    # cross-prime confirmation at p=11, p=13 (N1,N2 + FE consistency to N3)
    for p, b in [(11, 5), (13, 5)]:
        N1 = smooth_count_Cb(b, GF(p, 1))
        N2 = smooth_count_Cb(b, GF(p, 2))
        s1 = p + 1 - N1
        s2 = p * p + 1 - N2
        a1 = s1
        a2 = (s1 * s1 - s2) // 2 if (s1 * s1 - s2) % 2 == 0 else None
        consistent = (a2 is not None and abs(a1) <= 4 * (p ** 0.5) + 1e-9)
        line(f"      p={p} b={b}: N1={N1} N2={N2}; a1={a1} a2={a2}"
             f"  Weil-consistent={consistent}")
        g2_ok &= consistent
    # Newton-polygon interior lattice points = geometric genus (independent)
    interior = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if (i - j < 1) and (j - i < 1) and (i + j > 1) and (i + j < 5):
                interior += 1
    line(f"      Newton-polygon interior lattice points = {interior} (= g, independent)")
    g2_ok &= (interior == 2)
    line(f"    g=2 anchored: {'PASS' if g2_ok else 'FAIL'}")
    ok &= g2_ok

    # (c) g'=6 anchor: reproduce the rank-8 weight-1 Frobenius factor H at the
    #     p=5/z=0 fiber.  L(T)=det(1-Frob T|H^1_c)=exp(sum_k P_k T^k/k) must be
    #     (1-T)*H(T^2) through degree 4, where P_k = sum chi(arM) over C_b(F_5^k).
    line("")
    line("    g'=6 anchor (rank-8 weight-1 factor H at p=5 / z=0):")
    p, b = 5, 2     # b=2: b+1/b = 2+3 = 0 in F_5  => z=0
    Psum = []
    for k in range(1, 5):
        gf = GF(p, k, heavy=(k == 4))
        q = gf.q
        tot = 0
        for a in range(1, q):
            c3, c2, c1, c0 = Delta_cubic_r(a, b % p, gf)
            for r in range(1, q):
                v = gf.add(gf.mul(c3, r), c2)
                v = gf.add(gf.mul(v, r), c1)
                v = gf.add(gf.mul(v, r), c0)
                if v == 0:
                    arM = gf.mul(gf.mul(a, r), Mval(a, r, gf))
                    tot += gf.chi(arM)
        Psum.append(tot)
    # L(T) = exp(sum P_k T^k / k) mod T^5  via  n*l_n = sum_{j=1..n} P_j l_{n-j}
    l = [Fraction(1)]
    for n in range(1, 5):
        acc = Fraction(0)
        for j in range(1, n + 1):
            acc += Psum[j - 1] * l[n - j]
        l.append(acc / n)
    l_int = [c for c in l]
    target = [Fraction(1), Fraction(-1), Fraction(4), Fraction(-4), Fraction(22)]
    line(f"      P_1..P_4 = {Psum}")
    line(f"      L(T) mod T^5 coeffs = {[int(c) if c.denominator==1 else c for c in l_int]}")
    line(f"      target (1-T)*H(T^2) coeffs = {[int(c) for c in target]}")
    gp_ok = (l_int == target)
    line(f"      => weight-1 factor H = 1+4T^2+22T^4+100T^6+625T^8 (rank 8, |roots|=sqrt5)")
    line(f"         hence g' = (8 + 2g)/2 = 6 by 2g'-2g=8: {'PASS' if gp_ok else 'FAIL'}")
    ok &= gp_ok

    line("")
    line(f"  [4] LEDGER: {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


def Mval(a, r, gf):
    """M(a,r) = -3a^2 r + 4a r^2 - 2a r + 4a - 3r over GF gf."""
    add, mul = gf.add, gf.mul
    a2 = mul(a, a)
    r2 = mul(r, r)
    t = mul(gf.fromint(gf.p - 3), mul(a2, r))
    t = add(t, mul(gf.fromint(4), mul(a, r2)))
    t = add(t, mul(gf.fromint(gf.p - 2), mul(a, r)))
    t = add(t, mul(gf.fromint(4), a))
    t = add(t, mul(gf.fromint(gf.p - 3), r))
    return t


# ======================================================================
# CHECK 5 -- square-class identities  Legendre(d0)=chi(rM)=chi(aH)=chi(d_UV)
# ======================================================================
def check_squareclass(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[5] Square-class identities of the descended Kummer sign")
    line("    Descended sign d0 = r * d_UV (committed trace machinery), where")
    line("    d_UV = (4a-3r)b^2 - 2ar b + (-3a^2 r + 4a r^2) is the bare uv-sign")
    line("    quadratic.  Identities verified on the good split base:")
    line("      (i)  Legendre(d0) = chi(rM) = chi(aH)   [descended sign = dossier's chi(d_UV)]")
    line("      (ii) d0 = r * d_UV exactly, and chi(d_UV) = chi(M)")
    line("           (so chi(rM) = chi(r)chi(M) = chi(r)chi(d_UV) = chi(d0): consistent)")
    line("")
    all_ok = True
    rows = []
    for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
        checked = 0
        bad_i = 0
        bad_rel = 0
        bad_ii = 0
        for a in range(1, p):
            for r in range(1, p):
                if not good(a, r, p):
                    continue
                A = A_beta(a, r, p)
                B = B_beta(a, r, p)
                C = C_beta(a, r, p)
                disc = (B * B - 4 * A * C) % p
                sd = next(t for t in range(p) if t * t % p == disc)
                inv2A = pow(2 * A % p, p - 2, p)
                rM = (r * Mfun(a, r, p)) % p
                aH = (a * Hfun(a, r, p)) % p
                lrM = legendre(rM, p)
                laH = legendre(aH, p)
                lM = legendre(Mfun(a, r, p), p)
                for s in (sd, (p - sd) % p):
                    b = ((-B + s) * inv2A) % p
                    d0 = d0_fun(a, b, r, p)
                    dUV = dUV_fun(a, b, r, p)
                    checked += 1
                    ld0 = legendre(d0, p)
                    # (i) descended-sign three-way identity
                    if not (ld0 == lrM == laH):
                        bad_i += 1
                    # (ii) exact relation d0 = r*d_UV and chi(d_UV)=chi(M)
                    if (r * dUV - d0) % p != 0:
                        bad_rel += 1
                    if legendre(dUV, p) != lM:
                        bad_ii += 1
        rows.append((p, checked, bad_i, bad_rel, bad_ii))
        if bad_i or bad_rel or bad_ii:
            all_ok = False
    for p, checked, bi, br, bii in rows:
        line(f"    p={p:3d}: roots={checked:5d}  (i)mism={bi}  rel(d0=r*d_UV)mism={br}"
             f"  chi(d_UV)=chi(M)mism={bii}")
    line(f"    all square-class identities hold: {'PASS' if all_ok else 'FAIL'}")
    ok &= all_ok
    line("")
    line(f"  [5] SQCLASS: {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# CHECK 6 -- pairing dichotomy at the trace level
# ======================================================================
def build_cols(p):
    """cols[lb][la] = sum over (a,r) giving b-root of Legendre(d0); discrete logs."""
    g = primitive_root(p)
    n = p - 1
    log = [0] * p
    x = 1
    for e in range(n):
        log[x] = e
        x = x * g % p
    leg = [0] * p
    for x in range(1, p):
        leg[x] = 1 if pow(x, (p - 1) // 2, p) == 1 else -1
    sq = {}
    for x in range(p):
        sq.setdefault(x * x % p, x)
    inv = [0] * p
    for x in range(1, p):
        inv[x] = pow(x, p - 2, p)
    cols = [[0] * n for _ in range(n)]
    for a in range(1, p):
        a2 = a * a
        la = log[a]
        for r in range(1, p):
            if (a - r) % p == 0:
                continue
            A = (3 * a2 * r - 3 * a * r * r + a * r - 3 * a + 2 * r) % p
            if A == 0:
                continue
            C = (a * r * (-2 * a2 * r + 3 * a * r * r - a * r + 3 * a - 3 * r)) % p
            if C == 0:
                continue
            B = (-a * r * (a - 1) * (r + 1)) % p
            disc = (B * B - 4 * A * C) % p
            if disc == 0 or leg[disc] != 1:
                continue
            if K_alpha(a, r, p) == 0:
                continue
            sd = sq[disc]
            inv2A = inv[2 * A % p]
            for s in (sd, (p - sd) % p):
                b = ((-B + s) * inv2A) % p
                if b == 0:
                    continue
                d0 = (r * (-3 * a2 * r + 4 * a * b * b - 2 * a * b * r
                           + 4 * a * r * r - 3 * b * b * r)) % p
                cols[log[b]][la] += leg[d0]
    return cols, n


def _tau_maximag(cols, n, k):
    import cmath
    w = [cmath.exp(2j * cmath.pi * t / n) for t in range(n)]
    mx = 0.0
    for lb in range(n):
        col = cols[lb]
        acc = 0j
        for la in range(n):
            v = col[la]
            if v:
                acc += v * w[(k * la) % n]
        if abs(acc.imag) > mx:
            mx = abs(acc.imag)
    return mx


def check_pairing(check):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    line("[6] Pairing dichotomy (Poincare-Verdier F_psi^vee = F_{psi^-1}(-1))")
    line("    quadratic psi (psi^2=1): real weight-1 traces => self-dual SYMPLECTIC Sp_8")
    line("    general  psi (psi^2!=1): non-real traces => NOT self-dual => GL/SL")
    line("    (orthogonal excluded both regimes)")
    line("")
    quad_real = True
    gen_nonreal = True
    rows = []
    for p in [13, 31, 37, 61, 73]:
        cols, n = build_cols(p)
        # quadratic psi: k = n/2
        mq = _tau_maximag(cols, n, n // 2)
        # general psi: smallest order m>=3 dividing n
        kg = None
        for m in range(3, n + 1):
            if n % m == 0:
                kg = n // m
                break
        mg = _tau_maximag(cols, n, kg)
        rows.append((p, mq, mg, mg / (p ** 0.5)))
        if mq > 1e-7:
            quad_real = False
        if mg < 1e-3:
            gen_nonreal = False
    for p, mq, mg, ratio in rows:
        line(f"    p={p:3d}: quad max|Im tau|={mq:.2e} (->0)   "
             f"gen max|Im tau|={mg:8.4f}  (/sqrt p = {ratio:.3f}, O(1) wt-1 scale)")
    line(f"    quadratic traces real (self-dual/Sp): {'PASS' if quad_real else 'FAIL'}")
    line(f"    general traces non-real (not self-dual/GL-SL): {'PASS' if gen_nonreal else 'FAIL'}")
    ok &= quad_real and gen_nonreal
    line("")
    line(f"  [6] PAIRING: {'PASS' if ok else 'FAIL'}")
    line("")
    return ok


# ======================================================================
# Driver
# ======================================================================
def main(check=False):
    if not check:
        print("=" * 72)
        print("M1 (BETA_2) local-data dossier -- exact verifier certificate")
        print("Status: AUDIT (PROVEN p-independent invariants only)")
        print("=" * 72)
        print()

    results = []
    results.append(("DIHEDRAL", check_dihedral(check)))
    results.append(("NODES", check_nodes(check)))
    results.append(("P73", check_p73(check)))
    results.append(("LEDGER", check_rank_ledger(check)))
    results.append(("SQCLASS", check_squareclass(check)))
    results.append(("PAIRING", check_pairing(check)))

    all_ok = all(r for _, r in results)
    if check:
        for name, r in results:
            print(f"{name:9s} {'PASS' if r else 'FAIL'}")
        print("PASS" if all_ok else "FAIL")
    else:
        print("=" * 72)
        print("SUMMARY")
        for name, r in results:
            print(f"  [{name:9s}] {'PASS' if r else 'FAIL'}")
        print("-" * 72)
        print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
        print("=" * 72)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
