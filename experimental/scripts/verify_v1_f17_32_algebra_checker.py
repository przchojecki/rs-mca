#!/usr/bin/env python3
"""Verifier 1 (towards-prize.md A.3): independent high-level algebra checker
for the board row C = RS[F_17^32, H, 256], n=512, k=256, rho=1/2.

WHY THIS EXISTS
---------------
towards-prize.md A.3 asks for *two independent* verifiers that must agree:
  - Verifier 1: a high-level algebra verifier (Sage / Magma / PARI suggested);
  - Verifier 2: a low-level arithmetic verifier (Rust / C++ / minimal Python).
The 134 `verify_*.py` scripts in this repo are the bespoke exact-integer stack
they are meant to be cross-checked *against*, not an independent re-implementation.

Sage / PARI-GP / Magma are not assumed present.  This verifier therefore builds
F_17^32 on top of sympy's `galoistools` finite-field primitives -- a code path
entirely independent of the repo's hand-rolled arithmetic, which is exactly what
"two verifiers must agree" requires.  (sympy ships a native GF(p) but no turnkey
GF(p^32); we construct the extension field ourselves, ~one screen of code.)

A.3 CHECKLIST COVERAGE (this file grows one item per loop iteration):
  [x] field construction
  [x] domain construction
  [x] locator splitting
  [x] interpolation
  [x] degree bound
  [x] agreement count
  [x] slope distinctness
  [x] noncontainment rank
  -- hardening --
  [x] 2nd-irreducible representation-invariance
  [x] on-main board-record cross-checks (tangent506 / strict352 / strict264)

HONEST SCOPE / LIMITS
---------------------
  * This verifier cross-checks the *algebra and the exact-integer gates*
    independently.  It does NOT brute-force the bad-slope counts over
    binom(512, .) -- that enumeration is infeasible for every verifier on
    this row, and no safety/threshold status is asserted here.
  * The pinned irreducible below is an *independent* choice (not yet the frozen
    A.1 field polynomial), so the isomorphism-invariant facts (gate arithmetic,
    |H|=512 = full 2-Sylow, field laws) are checked now; certificate-*hash*
    agreement, which needs the frozen basis, is a later hardening item.
  * sympy `galoistools` is pure-Python: fine for field laws, the gate, and the
    handful of certificate slopes; not for mass enumeration.

Run:  python3 experimental/scripts/verify_v1_f17_32_algebra_checker.py
Exit non-zero iff any *implemented* check fails.
"""
from __future__ import annotations

from sympy.polys.domains import ZZ
from sympy.polys import galoistools as gt

# ----------------------------------------------------------------------------
# Row parameters (frozen board row)
# ----------------------------------------------------------------------------
P = 17
N = 32                       # extension degree
Q = P ** N                   # |F_17^32|
K = 256                      # RS dimension
N_CODE = 512                 # block length = |H|
RHO = (K, N_CODE)            # 1/2
TWO128 = 2 ** 128

# Independently pinned degree-32 irreducible over F_17 (reproducible;
# irreducibility re-asserted at runtime in check_field_construction).
MODULUS = [1, 14, 0, 4, 4, 2, 0, 2, 14, 7, 5, 5, 12, 6, 11, 11, 7,
           6, 1, 12, 3, 9, 3, 4, 5, 9, 11, 3, 13, 5, 8, 7, 16]
# A SECOND, independent degree-32 irreducible (for the hardening invariance check;
# also re-asserted irreducible at runtime).  GF(17^32) is unique up to isomorphism.
MODULUS2 = [1, 14, 6, 10, 0, 11, 1, 10, 9, 4, 8, 5, 16, 9, 12, 13, 14,
            10, 13, 11, 10, 9, 12, 13, 8, 10, 0, 15, 2, 12, 7, 9, 6]

# ----------------------------------------------------------------------------
# Independent GF(17^32) arithmetic on sympy galoistools (dense, high-deg-first;
# [] is the zero element).
# ----------------------------------------------------------------------------
ONE = [1]
ZERO: list = []


def fadd(a, b):
    return gt.gf_add(a, b, P, ZZ)


def fsub(a, b):
    return gt.gf_sub(a, b, P, ZZ)


def fmul(a, b):
    return gt.gf_rem(gt.gf_mul(a, b, P, ZZ), MODULUS, P, ZZ)


def fpow(a, e):
    return gt.gf_pow_mod(a, e, MODULUS, P, ZZ)


def finv(a):
    # Fermat inverse in F_17^32: a^(q-2).
    return fpow(a, Q - 2)


def feval(coeffs, x):
    """Horner-free eval of poly given low-degree-first coeff list `coeffs`."""
    acc, xp = ZERO, ONE
    for c in coeffs:
        acc = fadd(acc, fmul(c, xp))
        xp = fmul(xp, x)
    return acc


def int_to_elem(m):
    """Canonical field element for a non-negative integer (base-17 digits)."""
    if m == 0:
        return ZERO
    digits = []
    while m:
        digits.append(m % P)
        m //= P
    return gt.gf_strip(list(reversed(digits)))


def find_subgroup_generator(order=512):
    """Deterministic generator of the unique order-`order` subgroup of F*.
    Requires `order` a power of 2 dividing Q-1 (true here: 512 = 2^9)."""
    assert (order & (order - 1)) == 0, "order must be a power of two"
    e = (Q - 1) // order
    half = order // 2
    m = 2
    while m < 10_000:
        r = int_to_elem(m)
        cand = fpow(r, e)
        if fpow(cand, half) != ONE and fpow(cand, order) == ONE:
            return cand, m
        m += 1
    raise RuntimeError("no order-%d generator found in search bound" % order)


# --- polynomials OVER GF(17^32): coeff lists are themselves field elements,
# stored low-degree-first ([] = zero coeff).  galoistools is prime-field only,
# so these extension-field polynomial ops are done here. -----------------------
def fneg(a):
    return fsub(ZERO, a)


def pmul(a, b):
    res = [ZERO] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == ZERO:
            continue
        for j, bj in enumerate(b):
            res[i + j] = fadd(res[i + j], fmul(ai, bj))
    return res


def pderiv(a):
    if len(a) <= 1:
        return [ZERO]
    return [fmul(int_to_elem(i), a[i]) for i in range(1, len(a))]


def field_solve(matrix, rhs):
    """Solve `matrix @ x = rhs` over GF(17^32) by Gauss-Jordan elimination.
    Raises ValueError if singular.  (Reused for the noncontainment-rank check.)"""
    n = len(matrix)
    M = [row[:] for row in matrix]
    b = list(rhs)
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != ZERO), None)
        if piv is None:
            raise ValueError("singular matrix")
        M[col], M[piv] = M[piv], M[col]
        b[col], b[piv] = b[piv], b[col]
        inv = finv(M[col][col])
        M[col] = [fmul(x, inv) for x in M[col]]
        b[col] = fmul(b[col], inv)
        for r in range(n):
            if r != col and M[r][col] != ZERO:
                f = M[r][col]
                M[r] = [fsub(M[r][j], fmul(f, M[col][j])) for j in range(n)]
                b[r] = fsub(b[r], fmul(f, b[col]))
    return b


_H_GEN = None


def H_generator():
    """Memoized deterministic order-512 generator (the domain anchor)."""
    global _H_GEN
    if _H_GEN is None:
        _H_GEN = find_subgroup_generator(512)
    return _H_GEN


# ----------------------------------------------------------------------------
# Checks.  Each returns (status, details) where status is True/False (PASS/FAIL)
# for an implemented check, or None for a PENDING (not-yet-covered) item.
# ----------------------------------------------------------------------------
def check_gate_and_acceptance():
    """A.1 acceptance checklist + the bad-slope bridge gate (exact integers)."""
    d = []
    q_line = Q
    floor_q = q_line // TWO128
    ok = True
    d.append(f"q_line = 17^32 = {q_line}")
    d.append(f"2^128  = {TWO128}")
    d.append(f"floor(q_line / 2^128) = {floor_q}  (expect 6)")
    ok &= (floor_q == 6)
    d.append(f"7 * 2^128 > q_line : {7 * TWO128 > q_line}  (expect True)")
    ok &= (7 * TWO128 > q_line)
    d.append(f"6 * 2^128 < q_line : {6 * TWO128 < q_line}  (expect True)")
    ok &= (6 * TWO128 < q_line)
    # gate consequence: LD_sw >= 7  <=>  emca = LD_sw/q_line > 2^-128
    d.append("=> LD_sw(C,a) >= 7  iff  emca(C,delta) > 2^-128  (a-independent gate)")
    d.append(f"n={N_CODE}, k={K}, rho={RHO[0]}/{RHO[1]}")
    ok &= (N_CODE == 512 and K == 256 and 2 * K == N_CODE)
    return ok, d


def check_field_construction():
    """A.3: field construction.  Independent GF(17^32) on galoistools."""
    d = []
    ok = True
    # (a) modulus is a genuine degree-32 irreducible over F_17.
    deg_ok = (len(MODULUS) - 1 == N) and (MODULUS[0] == 1)
    irr_ok = gt.gf_irreducible_p(MODULUS, P, ZZ)
    d.append(f"modulus monic degree-32 : {deg_ok}")
    d.append(f"modulus irreducible over F_17 : {irr_ok}")
    ok &= deg_ok and irr_ok
    # (b) field laws on sample elements: distributivity, inverse, Frobenius.
    a = int_to_elem(3); b = int_to_elem(17 + 5); c = int_to_elem(17 ** 4 + 2)
    distrib = fmul(a, fadd(b, c)) == fadd(fmul(a, b), fmul(a, c))
    d.append(f"distributivity a*(b+c)=ab+ac : {distrib}")
    inv_ok = (fmul(a, finv(a)) == ONE) and (fmul(c, finv(c)) == ONE)
    d.append(f"multiplicative inverse a*a^-1=1 : {inv_ok}")
    # Frobenius: x^17 is additive and (a)^(q)=a (Fermat in the field).
    frob_fixes = fpow(a, Q) == a
    d.append(f"Frobenius / field order a^q = a : {frob_fixes}")
    ok &= distrib and inv_ok and frob_fixes
    return ok, d


def check_domain_construction():
    """A.3: domain construction.  H = order-512 subgroup; |H|=512 full 2-Sylow."""
    d = []
    ok = True
    # 2-adic valuation of Q-1 -> 512 = 2^9 is the FULL 2-Sylow (and 1024 is not).
    v2, t = 0, Q - 1
    while t % 2 == 0:
        t //= 2; v2 += 1
    d.append(f"v2(17^32 - 1) = {v2}  => 512=2^9 divides Q-1 exactly: {v2 == 9}")
    d.append(f"1024 | Q-1 ? {(Q - 1) % 1024 == 0}  (expect False: 512 is full 2-Sylow)")
    ok &= (v2 == 9)
    h, witness = H_generator()
    d.append(f"order-512 generator found (from base-17 element {witness})")
    # build H, check 512 distinct, closure, and that it's a subgroup of F*.
    pts, cur = [], ONE
    for _ in range(512):
        pts.append(tuple(cur))
        cur = fmul(cur, h)
    distinct = len(set(pts)) == 512
    closes = (cur == ONE)                       # h^512 = 1
    has_one = tuple(ONE) in set(pts)
    no_zero = tuple(ZERO) not in set(pts)
    d.append(f"|H| = 512 distinct points : {distinct}")
    d.append(f"H closes (h^512 = 1) : {closes}")
    d.append(f"1 in H : {has_one} ;  0 not in H : {no_zero}")
    # exact order 512 (no smaller): h^256 != 1
    d.append(f"generator order exactly 512 (h^256 != 1) : {fpow(h, 256) != ONE}")
    ok &= distinct and closes and has_one and no_zero and (fpow(h, 256) != ONE)
    return ok, d


def check_locator_splitting():
    """A.3: locator splitting.  Build a split squarefree locator L_T(X)=prod_{x in T}(X-x)
    over GF(17^32) on a runnable support T subset H, and verify it really splits.

    This is the genuine 'split squarefree locator' object of the F1/M1 program
    (cf. the a=265 'split squarefree degree-247 locator'); here |T| is small and
    RUNNABLE -- this checks the locator ALGEBRA, not any enumeration over H."""
    d = []
    ok = True
    h, _ = H_generator()
    # support T = six distinct domain points h^0..h^5
    T, cur = [], ONE
    for _ in range(6):
        T.append(cur)
        cur = fmul(cur, h)
    # monic locator over GF(17^32), low-degree-first
    L = [ONE]
    for x in T:
        L = pmul(L, [fneg(x), ONE])            # times (X - x)
    deg_ok = (len(L) - 1 == 6) and (L[-1] == ONE)
    d.append(f"deg L_T = {len(L) - 1} (expect 6), monic : {deg_ok}")
    ok &= deg_ok
    # splits over F: vanishes exactly on T (and on no other tested H point)
    on_support = all(feval(L, x) == ZERO for x in T)
    others, cur = [], T[-1]
    for _ in range(6):
        cur = fmul(cur, h)
        others.append(cur)
    off_support = all(feval(L, y) != ZERO for y in others)
    d.append(f"L_T vanishes on all 6 support points : {on_support}")
    d.append(f"L_T nonzero on 6 disjoint H points    : {off_support}")
    ok &= on_support and off_support
    # squarefree / all-roots-simple via the derivative test (no gcd needed):
    Lp = pderiv(L)
    simple = all(feval(Lp, x) != ZERO for x in T)
    d.append(f"all roots simple => squarefree split (L' != 0 on T) : {simple}")
    ok &= simple
    # Vieta: the coefficient prefix IS the elementary-symmetric / prefix map Phi
    e1 = ZERO
    for x in T:
        e1 = fadd(e1, x)
    prod = ONE
    for x in T:
        prod = fmul(prod, x)
    vieta_top = (L[5] == fneg(e1))             # [X^5] = -e_1
    vieta_const = (L[0] == prod)               # [X^0] = (-1)^6 prod = prod
    d.append(f"Vieta [X^5] = -sum(roots) (= -e_1 = prefix Phi_1) : {vieta_top}")
    d.append(f"Vieta [X^0] = prod(roots) (= e_6)                 : {vieta_const}")
    ok &= vieta_top and vieta_const
    # negative control: a repeated factor is NOT split-squarefree and is caught.
    Ldup = pmul(L, [fneg(T[0]), ONE])          # double the root T[0]
    caught = (feval(Ldup, T[0]) == ZERO) and (feval(pderiv(Ldup), T[0]) == ZERO)
    d.append(f"negative control: doubled root caught (L,L' both vanish) : {caught}")
    ok &= caught
    return ok, d


def check_interpolation():
    """A.3: interpolation.  RS encode/decode on a runnable RS analog over GF(17^32):
    a degree-<k polynomial is the unique interpolant through any k distinct nodes.
    Cross-validates a Vandermonde solve against an independent Lagrange interpolant
    (k small and RUNNABLE; this checks the interpolation algebra, not enumeration)."""
    d = []
    ok = True
    h, _ = H_generator()
    k = 5
    nodes, cur = [], ONE
    for _ in range(k):
        nodes.append(cur)
        cur = fmul(cur, h)
    # secret degree-<k message polynomial (deterministic coeffs, low-degree-first)
    coeffs = [int_to_elem(v) for v in (3, 17 + 2, 5, 17 * 17 + 1, 11)]
    vals = [feval(coeffs, x) for x in nodes]               # the RS codeword on `nodes`
    # (1) Vandermonde solve recovers the message coefficients EXACTLY
    V = [[fpow(nodes[i], j) for j in range(k)] for i in range(k)]
    rec = field_solve(V, vals)
    d.append(f"Vandermonde solve recovers deg<{k} message exactly : {rec == coeffs}")
    d.append(f"interpolant has {len(rec)} coeffs (deg < k={k})       : {len(rec) == k}")
    ok &= (rec == coeffs) and (len(rec) == k)
    # (2) INDEPENDENT Lagrange interpolant agrees with P at a fresh point
    t = fmul(cur, h)                                       # an H point outside `nodes`
    lag = ZERO
    for i in range(k):
        num, den = ONE, ONE
        for j in range(k):
            if j == i:
                continue
            num = fmul(num, fsub(t, nodes[j]))
            den = fmul(den, fsub(nodes[i], nodes[j]))
        lag = fadd(lag, fmul(vals[i], fmul(num, finv(den))))
    d.append(f"independent Lagrange value agrees with P at fresh point : {lag == feval(coeffs, t)}")
    ok &= (lag == feval(coeffs, t))
    # (3) uniqueness: interpolating from a DISJOINT k-node set yields the same message
    nodes2, cur2 = [], t
    for _ in range(k):
        nodes2.append(cur2)
        cur2 = fmul(cur2, h)
    vals2 = [feval(coeffs, x) for x in nodes2]
    V2 = [[fpow(nodes2[i], j) for j in range(k)] for i in range(k)]
    rec2 = field_solve(V2, vals2)
    d.append(f"uniqueness: disjoint node set recovers the same message : {rec2 == coeffs}")
    ok &= (rec2 == coeffs)
    return ok, d


def check_degree_bound():
    """A.3: degree bound = the MDS / Singleton property.  On a runnable RS analog
    RS[GF(17^32), H, k] (real |H|=512, small k), a nonzero degree-d polynomial has
    at most d roots, so two DISTINCT degree-<k codewords agree on at most k-1 of the
    512 domain points -- the bound underpinning the agreement staircase and the
    meaning of 'noncontainment'.  Verified in miniature, then stated for the row."""
    d = []
    ok = True
    h, _ = H_generator()
    k = 5
    H = []
    cur = ONE
    for _ in range(512):
        H.append(cur)
        cur = fmul(cur, h)
    # difference locator D: monic, degree exactly k-1, with k-1 distinct roots in H.
    roots = H[:k - 1]
    D = [ONE]
    for x in roots:
        D = pmul(D, [fneg(x), ONE])
    deg_ok = (len(D) - 1 == k - 1)
    nz_roots = sum(1 for x in H if feval(D, x) == ZERO)
    d.append(f"nonzero deg-{k - 1} poly has exactly {nz_roots} roots in |H|=512 "
             f"(<= k-1={k - 1}) : {deg_ok and nz_roots == k - 1}")
    ok &= deg_ok and (nz_roots == k - 1)
    # two distinct deg-<k codewords whose difference IS D => agree exactly on roots(D)
    P1 = [int_to_elem(v) for v in (2, 3, 5, 7, 11)]
    P2 = [fadd(P1[i], D[i]) for i in range(k)]
    diff_is_D = all(fsub(P2[i], P1[i]) == D[i] for i in range(k))
    distinct = (P1 != P2)
    d.append(f"P2 = P1 + D : distinct, deg < {k}, and P2 - P1 = D : {diff_is_D and distinct}")
    ok &= diff_is_D and distinct
    # MDS agreement bound, and it is TIGHT (Singleton achieved)
    d.append(f"MDS: distinct deg<{k} codewords agree on {nz_roots} of 512 pts "
             f"(<= k-1={k - 1}, tight) : {nz_roots == k - 1}")
    ok &= (nz_roots == k - 1)
    d.append("row in miniature: k=256 => distinct codewords agree <= 255 pts, "
             "min distance n-k+1 = 257 (MDS).")
    return ok, d


def check_agreement_count():
    """A.3: agreement count.  For a received word w on H and a codeword P (deg<k),
    agreement(w,P) = #{x in H : w(x) = P(x)} -- the quantity LD_sw / the bad-slope
    machinery counts.  On a runnable analog with the real |H|=512 (small k), plant a
    word agreeing with P on a chosen set of size a and verify the count is exactly a,
    that the error locator has degree n-a, and the MDS consequence for a 2nd codeword.
    Scope: counts agreement for GIVEN codewords; does NOT enumerate the LD_sw list."""
    d = []
    ok = True
    h, _ = H_generator()
    n, k = 512, 5
    H = []
    cur = ONE
    for _ in range(n):
        H.append(cur)
        cur = fmul(cur, h)
    P = [int_to_elem(v) for v in (1, 2, 3, 4, 5)]          # planted codeword, deg<k
    cw = [feval(P, x) for x in H]                          # its codeword values
    a = 300                                                # planted agreement (> (n+k)/2)
    w = [cw[i] if i < a else fadd(cw[i], ONE) for i in range(n)]  # corrupt the last n-a
    # (1) exact agreement count
    agree = sum(1 for i in range(n) if w[i] == cw[i])
    d.append(f"agreement(w, P) = {agree} (planted a={a}) : {agree == a}")
    ok &= (agree == a)
    # (2) error locator: vanishes exactly on the n-a disagreement points (degree n-a)
    n_err = sum(1 for i in range(n) if w[i] != cw[i])
    d.append(f"#disagreements = {n_err} = n-a = {n - a} (error-locator degree) : {n_err == n - a}")
    ok &= (n_err == n - a)
    # (3) unique-decoding regime: a > (n+k)/2 => P is the unique codeword within n-a errors
    d.append(f"a={a} > (n+k)/2={ (n + k) / 2 } => unique-decoding regime : {a > (n + k) / 2}")
    ok &= (a > (n + k) / 2)
    # (4) MDS consequence: a DISTINCT codeword agrees with w on < a points
    P2 = [int_to_elem(v) for v in (7, 1, 4, 1, 5)]
    cw2 = [feval(P2, x) for x in H]
    agree2 = sum(1 for i in range(n) if w[i] == cw2[i])
    d.append(f"distinct codeword agrees with w on {agree2} < a={a} (MDS-consistent) : {agree2 < a}")
    ok &= (P != P2) and (agree2 < a)
    d.append("scope: agreement for GIVEN codewords on the real 512-domain analog; "
             "NOT the agreement-a codeword LIST (the infeasible LD_sw count).")
    return ok, d


def check_slope_distinctness():
    """A.3: slope distinctness (the dedup property).  A bad slope is a deep-point image
    z = P(alpha); a moving family P_i = P0 + c_i*M gives slopes z_i = P0(alpha)+c_i*M(alpha).
    With alpha outside H (a genuine deep point) and M(alpha) != 0, distinct configs give
    pairwise-DISTINCT field slopes -- so a bad-slope COUNT is a count of distinct field
    elements, not inflated by duplicates.  Negative control: at a root of M the slopes
    collapse to one (dedup).  Faithful to the deep-point bridge / moving-root tangent
    floor; this is slope DEDUP, not an LD_sw count."""
    d = []
    ok = True
    k = 5
    # deep point alpha OUTSIDE H (nonzero constants all lie in H since 16 | 512, so use x...)
    bump = 16
    alpha = int_to_elem(bump)
    while fpow(alpha, 512) == ONE:
        bump += 1
        alpha = int_to_elem(bump)
    d.append(f"deep point alpha (base-17 elt {bump}) outside H (alpha^512 != 1) : {fpow(alpha, 512) != ONE}")
    P0 = [int_to_elem(v) for v in (1, 1, 1, 1, 1)]        # base deg<k poly
    M = [int_to_elem(v) for v in (0, 1, 0, 0, 0)]         # moving direction M(X)=X
    Ma = feval(M, alpha)
    d.append(f"moving direction M(alpha) != 0 : {Ma != ZERO}")
    ok &= (Ma != ZERO)
    cs = [int_to_elem(c) for c in range(1, 11)]           # 10 distinct configs
    slopes = [feval([fadd(P0[j], fmul(c, M[j])) for j in range(k)], alpha) for c in cs]
    n_distinct = len({tuple(z) for z in slopes})
    d.append(f"{len(cs)} moving-root configs give {n_distinct} DISTINCT slopes : {n_distinct == len(cs)}")
    ok &= (n_distinct == len(cs))
    # injectivity reason: z_i - z_j = (c_i - c_j) * M(alpha), nonzero for distinct configs
    inj = True
    for i in range(len(cs)):
        for j in range(i + 1, len(cs)):
            lhs = fsub(slopes[i], slopes[j])
            rhs = fmul(fsub(cs[i], cs[j]), Ma)
            if lhs != rhs or lhs == ZERO:
                inj = False
    d.append(f"slope injectivity z_i - z_j = (c_i - c_j)*M(alpha) != 0 : {inj}")
    ok &= inj
    # dedup negative control: at a root of M the configs collapse to ONE slope
    slopes_root = [feval([fadd(P0[j], fmul(c, M[j])) for j in range(k)], ZERO) for c in cs]
    collapsed = (len({tuple(z) for z in slopes_root}) == 1)
    d.append(f"dedup control: at an M-root the {len(cs)} configs collapse to 1 slope : {collapsed}")
    ok &= collapsed
    d.append("scope: distinctness/dedup of deep-image bad slopes on a runnable family; "
             "NOT an LD_sw count.")
    return ok, d


def check_noncontainment_rank():
    """A.3: noncontainment rank certificate (the strict264 mechanism).  A retained
    slope is genuinely noncontained iff the beta-column of the Vandermonde at nodes
    J u {beta} is independent of the j support columns -- i.e. the (j+1)x(j+1)
    Vandermonde (rows = degrees 0..j) is nonsingular, which needs redundancy r >= j+1.
    Certified two independent ways (Vandermonde determinant and field_solve), with the
    r'=j deficiency as the negative control.  Runnable miniature (j=4); the row uses
    r=n-k=256, j=n-a -- not verified by enumeration."""
    d = []
    ok = True
    h, _ = H_generator()
    j = 4
    J, cur = [], ONE
    for _ in range(j):
        J.append(cur)
        cur = fmul(cur, h)
    beta = int_to_elem(17)                                # = x : a deep point (beta not in D)
    nodes = J + [beta]
    distinct = (len({tuple(z) for z in nodes}) == j + 1)
    beta_deep = (fpow(beta, 512) != ONE)
    d.append(f"nodes J u {{beta}} distinct ({j + 1}) and beta outside H (deep) : {distinct and beta_deep}")
    ok &= distinct and beta_deep
    # (A) independent full-rank certificate: Vandermonde determinant prod(node_b - node_a)
    det = ONE
    for b_ in range(j + 1):
        for a_ in range(b_):
            det = fmul(det, fsub(nodes[b_], nodes[a_]))
    d.append(f"Vandermonde det = prod(node_b - node_a) != 0 => full column rank {j + 1} : {det != ZERO}")
    ok &= (det != ZERO)
    # (B) noncontainment: (j+1)x(j+1) Vandermonde nonsingular, solution reconstructs RHS
    Wfull = [[fpow(nodes[l], i) for l in range(j + 1)] for i in range(j + 1)]
    rhs = [int_to_elem(v) for v in (2, 3, 5, 7, 11)]
    try:
        sol = field_solve(Wfull, rhs)
        recon_ok = all(_vand_combo(sol, nodes, i) == rhs[i] for i in range(j + 1))
        nonsing = True
    except ValueError:
        nonsing, recon_ok = False, False
    d.append(f"(j+1)x(j+1) Vandermonde nonsingular & solves => beta-col indep of J-cols "
             f"(noncontainment) : {nonsing and recon_ok}")
    ok &= nonsing and recon_ok
    # (C) negative control: with only r'=j rows, beta-col IS a combo of the J-cols
    VJ = [[fpow(J[l], i) for l in range(j)] for i in range(j)]
    beta_restr = [fpow(beta, i) for i in range(j)]
    lam = field_solve(VJ, beta_restr)
    dep_ok = all(_vand_combo(lam, J, i) == beta_restr[i] for i in range(j))
    d.append(f"negative control: with only j rows beta-col = combo of J-cols (containment) "
             f"=> r >= j+1 essential : {dep_ok}")
    ok &= dep_ok
    d.append("scope: noncontainment rank certificate on a runnable support (j=4); the row "
             "uses r=n-k=256, j=n-a -- checked in miniature, not by enumeration.")
    return ok, d


def _vand_combo(coeffs, node_list, power):
    """sum_l coeffs[l] * node_list[l]^power  (column combination in a Vandermonde)."""
    acc = ZERO
    for l in range(len(node_list)):
        acc = fadd(acc, fmul(coeffs[l], fpow(node_list[l], power)))
    return acc


def check_second_irreducible():
    """HARDENING: re-verify the representation-invariant facts under a SECOND,
    independent degree-32 irreducible (MODULUS2 != MODULUS).  GF(17^32) is unique up
    to isomorphism, so the gate, the field laws, and |H|=512 (full 2-Sylow) must NOT
    depend on the chosen irreducible -- this guards against a representation artifact."""
    d = []
    ok = True
    irr2 = (len(MODULUS2) - 1 == N) and (MODULUS2[0] == 1) and gt.gf_irreducible_p(MODULUS2, P, ZZ)
    d.append(f"2nd modulus monic deg-32 irreducible and != MODULUS : {irr2 and MODULUS2 != MODULUS}")
    ok &= irr2 and (MODULUS2 != MODULUS)

    def m2(a, b):
        return gt.gf_rem(gt.gf_mul(a, b, P, ZZ), MODULUS2, P, ZZ)

    def p2(a, e):
        return gt.gf_pow_mod(a, e, MODULUS2, P, ZZ)

    def a2(a, b):
        return gt.gf_add(a, b, P, ZZ)

    A = gt.gf_strip([(7 * i + 3) % P for i in range(N)])
    B = gt.gf_strip([(5 * i + 1) % P for i in range(N)])
    Cc = gt.gf_strip([(3 * i + 2) % P for i in range(N)])
    distrib = m2(A, a2(B, Cc)) == a2(m2(A, B), m2(A, Cc))
    inv_ok = (m2(A, p2(A, Q - 2)) == ONE)
    frob = (p2(A, Q) == A)
    d.append(f"field laws under 2nd irreducible (distrib, inverse, a^q=a) : {distrib and inv_ok and frob}")
    ok &= distrib and inv_ok and frob
    d.append(f"gate floor(17^32/2^128)=6 is representation-independent : {Q // TWO128 == 6}")
    # |H|=512 full 2-Sylow reconstructed in the SECOND representation
    e = (Q - 1) // 512
    h2 = None
    for m in range(2, 300):
        cand = p2(int_to_elem(m), e)
        if p2(cand, 256) != ONE and p2(cand, 512) == ONE:
            h2 = cand
            break
    pts, cur = set(), ONE
    if h2 is not None:
        for _ in range(512):
            pts.add(tuple(cur))
            cur = m2(cur, h2)
    h_ok = (h2 is not None) and (len(pts) == 512) and (cur == ONE)
    d.append(f"|H|=512 full 2-Sylow reconstructed under 2nd irreducible : {h_ok}")
    ok &= h_ok
    d.append("=> gate, field laws, and |H|=512 are field-representation-INVARIANT "
             "(independent of the chosen irreducible).")
    return ok, d


def check_on_main_records():
    """HARDENING: independently recompute the integer arithmetic behind the on-main
    board records (site/data/frontier.json) for n=512,k=256,q=17^32 -- the tangent
    staircase LD_sw(C,a)=513-a (a>=427), the agreement-independent >=7 gate, and that
    each record's badSlopes is gate-consistent with its safe/unsafe status, with the
    recorded count and the tangent floor agreeing on the gate.  Scope: recomputes the
    recorded ARITHMETIC / gates, NOT the slope counts by enumeration."""
    d = []
    ok = True
    gate_ok = (Q // TWO128 == 6) and (6 * TWO128 < Q < 7 * TWO128)
    d.append(f"gate: floor(17^32/2^128)=6 and 6*2^128 < 17^32 < 7*2^128 : {gate_ok}")
    ok &= gate_ok

    def tangent(a):
        return N_CODE + 1 - a                              # LD_sw(C,a) = 513 - a (a >= 427)

    t506, t507 = tangent(506), tangent(507)
    d.append(f"tangent staircase: LD_sw(C,506)={t506} (unsafe, >=7), "
             f"LD_sw(C,507)={t507} (safe, <7) : {t506 == 7 and t507 == 6}")
    ok &= (t506 == 7 and t507 == 6)
    # (id, agreement a, recorded badSlopes, is_tangent_floor_record, recorded status)
    records = [
        ("tangent257-lower-floor",  257, 256,          True,  "unsafe"),
        ("cycle116",                262, 52747567092,  False, "unsafe"),
        ("cycle119",                263, 52747567092,  False, "unsafe"),
        ("strict264-min",           264, 9,            False, "unsafe"),
        ("strict352-quotient-core", 352, 16,           False, "unsafe"),
        ("reserve272",              272, 241,          True,  "unsafe"),
        ("reserve288",              288, 225,          True,  "unsafe"),
        ("reserve313",              313, 200,          True,  "unsafe"),
        ("tangent506-exact-gate",   506, 7,            True,  "unsafe"),
    ]
    all_ok = True
    for rid, a, bad, is_tf, status in records:
        tf = tangent(a)
        tf_match = (not is_tf) or (bad == tf)             # tangent-floor records: badSlopes == 513-a
        clears = (bad >= 7)
        tf_clears = (tf >= 7)
        gate_status = "unsafe" if clears else "safe"
        rec_ok = tf_match and (gate_status == status) and (clears == tf_clears)
        all_ok &= rec_ok
        tag = "tangent-floor" if is_tf else "mechanism"
        d.append(f"  {rid}: a={a}, badSlopes={bad} ({tag}); 513-a={tf}; "
                 f"gate={gate_status}=='{status}' : {rec_ok}")
    d.append(f"all {len(records)} board records gate-consistent (recorded count & tangent floor "
             f"agree on the gate) : {all_ok}")
    ok &= all_ok
    d.append("scope: recomputes recorded ARITHMETIC/gates (513-a, floor(17^32/2^128)=6, >=7), "
             "NOT slope counts by enumeration.")
    return ok, d


def _pending():
    return None, ["PENDING -- added in a later loop iteration"]


# Ordered A.3 coverage registry.  PENDING items are filled in priority order.
CHECKS = [
    ("foundational gate / A.1 acceptance", check_gate_and_acceptance),
    ("field construction",                 check_field_construction),
    ("domain construction",                check_domain_construction),
    ("locator splitting",                  check_locator_splitting),
    ("interpolation",                      check_interpolation),
    ("degree bound",                       check_degree_bound),
    ("agreement count",                    check_agreement_count),
    ("slope distinctness",                 check_slope_distinctness),
    ("noncontainment rank",                check_noncontainment_rank),
    ("hardening: 2nd irreducible",         check_second_irreducible),
    ("hardening: on-main records",         check_on_main_records),
]


def main():
    print("=" * 74)
    print("Verifier 1 (A.3) -- independent algebra checker  C = RS[F_17^32, H, 256]")
    print("independent stack: sympy.galoistools (NOT the repo's bespoke arithmetic)")
    print("=" * 74)
    failed = 0
    done = 0
    pending = 0
    for title, fn in CHECKS:
        status, details = fn()
        if status is None:
            tag = "PENDING"
            pending += 1
        elif status:
            tag = "PASS"
            done += 1
        else:
            tag = "FAIL"
            failed += 1
        print(f"\n[{tag:7}] {title}")
        for line in details:
            print(f"          {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {done}   FAIL: {failed}   PENDING: {pending}")
    print("-" * 74)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
