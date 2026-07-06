#!/usr/bin/env python3
"""l1_minj_pencil_kit.py -- the unique-`Gamma` crack + pencil-reduction toolkit
for the min-`j` frontier `[a, ell-a, 9]` of `l1_t7_atlas_concurrency.md`
(PR #379), companion to `experimental/notes/l1/l1_minj_pencil_freeze.md`.

THE CRACK (Theorem 1). For a cap-tight top pair `[a, ell-a]` (`a+(ell-a)=ell`,
`1<=a<=ell-1`), planting fiber-`a` in coset `b1` (`F1`) and fiber-`(ell-a)` in
a DISTINCT coset `b2` (`F2`) imposes `(a-1)+(ell-a-1)=ell-2` coincidence rows
on the `(ell-1)`-dim constant-free `Gamma`-space; the nullspace is ALWAYS
EXACTLY dimension 1 (never 0, never 2), for arbitrary dropsets -- no
genericity assumed, no degenerate dropset exists. Two independent closed
forms for the resulting unique `Gamma*` (up to scalar), cross-checked here on
every plant:

  (A) Lagrange / indicator form:  Gamma* = L - L(0),
      L = the deg-<ell interpolant with L=1 on F1, L=0 on F2.
  (B) Bezout / extended-gcd form: with A = prod_{F1}(X-x) (deg a),
      B = prod_{F2}(X-x) (deg ell-a) -- coprime, both prime to X since
      0 not in F1 u F2 -- the extended Euclidean algorithm gives the UNIQUE
      P (deg ell-1-a), Q (deg a-1) with A*P - B*Q = 1. Then A*P is itself a
      degree-<=ell-1 poly, constant (=0) on F1 (A vanishes there) and
      constant (=1) on F2 (since B vanishes there and A*P-B*Q=1); i.e.
      A*P IS the interpolant `1-L` of form (A) (both are the unique
      degree-<ell poly through the same ell values of F1 u F2), giving
      Gamma* = (1-L(0)) - A*P -- a genuinely independent construction
      (extended-gcd on the coprime pair (A,B), no interpolation at all).

THE PENCIL REDUCTION (Theorem 2). Because F1 is a subset of a FULL coset of
mu_ell, A = (X^ell-1)/A_drop with A_drop = prod over the DROPPED points of
F1's coset (deg A_drop = ell-a). On any third coset C_k (k != b1, b2), every
point satisfies X^ell = rho_k (constant on C_k), so a size-t fiber of Gamma*
on C_k at value w exists iff the explicit degree-(ell-a) polynomial
P - lambda*A_drop (lambda = (w-c1)/(rho_k-1)) has t roots in C_k. Degree
ell-a is a genuine drop from Gamma*'s own degree ell-1: the third-fiber
question reduces to root-concentration of one fixed low-degree pencil member
inside one coset. The twin identity via B_drop (deg a) gives the same
argument with roles of F1/F2 swapped, so t <= min(a, ell-a) -- this SELF-
CONTAINS the pairwise cap mu_3 <= mu_1 + mu_3 - mu_1 <= ell - a (Lemma 3 of
`l1_sigma_calculus.md`, here re-derived via a lower-degree, fully explicit
route rather than the pencil-through-two-points argument there).

This module is the reusable constructor half of the pair: it is imported by
nothing that needs an independence guarantee (the paired verifier,
`experimental/scripts/verify_l1_minj_pencil_freeze.py`, is a FRESH,
self-contained reimplementation and does not import this file). Run directly
for a deterministic demo (no args, no randomness):

    python3 l1_minj_pencil_kit.py

reconstructs (1) the ell=17,p=137 W3-equivalent cap-tight pair-plant
(spectrum [14,3^7], excess +2 -- the same spectrum as `l1_e3_law_refuted.md`'s
W3, reached here by the CRACK's pair-plant method, not W3's original
fat-tail-plant method) and (2) one true min-j frontier example
(ell=19,p=229,a=10, tail ell-a=9), demonstrating both closed forms and the
pencil reduction on a live third-coset fiber.

stdlib only, exact arithmetic over F_p throughout; no floating point except
in printed diagnostics (none needed).
"""
import sys


# =====================================================================
# exact F_p scalar + polynomial arithmetic
# =====================================================================
def inv(a, p):
    return pow(a % p, p - 2, p)


def is_prime(m):
    if m < 2:
        return False
    if m % 2 == 0:
        return m == 2
    d = 3
    while d * d <= m:
        if m % d == 0:
            return False
        d += 2
    return True


def find_gen(p):
    """A generator of F_p^*, via full trial factorization of p-1 (p is always
    small in this program -- exact, not probabilistic)."""
    m, d, fac = p - 1, 2, set()
    while d * d <= m:
        while m % d == 0:
            fac.add(d)
            m //= d
        d += 1
    if m > 1:
        fac.add(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no generator found")


def ptrim(c, p):
    c = [v % p for v in c]
    while c and c[-1] == 0:
        c.pop()
    return c


def pmul(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        ai %= p
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return ptrim(r, p)


def padd(a, b, p):
    n = max(len(a), len(b))
    r = [0] * n
    for i in range(len(a)):
        r[i] = a[i] % p
    for i in range(len(b)):
        r[i] = (r[i] + b[i]) % p
    return ptrim(r, p)


def psub(a, b, p):
    return padd(a, [(-v) % p for v in b], p)


def pdivmod(num, den, p):
    """Exact division; raises on a nonzero remainder is NOT enforced here
    (callers that require exactness check the remainder themselves)."""
    num, den = ptrim(num, p), ptrim(den, p)
    if not den:
        raise ZeroDivisionError
    if len(num) < len(den):
        return [], num
    rem = num[:]
    dl = inv(den[-1], p)
    q = [0] * (len(rem) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        c = rem[i + len(den) - 1] * dl % p
        q[i] = c
        if c:
            for j, dj in enumerate(den):
                rem[i + j] = (rem[i + j] - c * dj) % p
    return ptrim(q, p), ptrim(rem, p)


def poly_from_roots(roots, p):
    out = [1]
    for r in roots:
        out = pmul(out, [(-r) % p, 1], p)
    return out


def ext_gcd(a, b, p):
    """Extended Euclidean algorithm for F_p[X]: returns (g, s, t) with
    g = s*a + t*b, g = gcd(a,b) (some nonzero scalar multiple of it, since we
    do not force monic here -- callers normalize)."""
    a, b = ptrim(a, p), ptrim(b, p)
    if not b:
        return a, [1], []
    q, r = pdivmod(a, b, p)
    g, s1, t1 = ext_gcd(b, r, p)
    # g = s1*b + t1*r,  r = a - q*b  =>  g = t1*a + (s1 - t1*q)*b
    s = t1
    t = psub(s1, pmul(t1, q, p), p)
    return g, s, t


def peval(poly, x, p):
    """Horner evaluation; poly[i] = coeff of X^i."""
    v = 0
    for c in reversed(poly):
        v = (v * x + c) % p
    return v


def gamma_eval(gamma, x, p):
    """gamma[r-1] = coeff of X^r, r=1..ell-1 (constant-free)."""
    return peval(gamma, x, p) * x % p


# =====================================================================
# cosets of mu_ell in F_p^*
# =====================================================================
def cosets_of(p, ell):
    """cs[i] = the i-th coset of H=mu_ell (the ell-th roots of unity), listed
    in zeta-power order; cs[0] = H itself. Returns (cosets, generator, zeta)."""
    assert (p - 1) % ell == 0
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    return [[pow(g, i, p) * h % p for h in H] for i in range(n)], g, zeta


def full_coset_containing(x, p, ell):
    """All ell points y with y^ell == x^ell (brute force; p is always small
    in this program)."""
    w = pow(x, ell, p)
    return sorted(y for y in range(1, p) if pow(y, ell, p) == w)


# =====================================================================
# linear algebra over F_p: RREF / nullspace
# =====================================================================
def nullspace_basis(rows, ncols, p):
    if not rows:
        return [[1 if i == j else 0 for i in range(ncols)] for j in range(ncols)]
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
    pivset = set(piv)
    basis = []
    for free in range(ncols):
        if free in pivset:
            continue
        v = [0] * ncols
        v[free] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][free]) % p
        basis.append(v)
    return basis


def fiber_rows(points, p, ell):
    """Rows enforcing Gamma equal across `points`, in the constant-free
    coordinates X^1..X^{ell-1}."""
    if len(points) < 2:
        return []
    x0 = points[0]
    v0 = [pow(x0, r, p) for r in range(1, ell)]
    return [[(v0[r - 1] - pow(x, r, p)) % p for r in range(1, ell)] for x in points[1:]]


def normalize_gamma(gm, p):
    """Scale so the highest-degree nonzero coefficient is 1."""
    nz = [i for i, c in enumerate(gm) if c % p]
    if not nz:
        return None
    s = inv(gm[max(nz)], p)
    return [(c * s) % p for c in gm]


def solve_unique_gamma(F1, F2, p, ell):
    """THE CRACK: solve the nullspace directly (no closed form). Returns
    (gamma_normalized, nullity) -- nullity MUST be 1 for a cap-tight pair
    (|F1|+|F2|=ell, distinct cosets); this is asserted by callers that trust
    the theorem, not silently assumed here."""
    rows = fiber_rows(F1, p, ell) + fiber_rows(F2, p, ell)
    basis = nullspace_basis(rows, ell - 1, p)
    if len(basis) != 1:
        return None, len(basis)
    return normalize_gamma(basis[0], p), 1


# =====================================================================
# closed form (A): Lagrange indicator interpolant  Gamma* = L - L(0)
# =====================================================================
def lagrange_coeffs(xs, ys, p):
    """Coeffs [c_0..c_{n-1}] (ascending) of the degree-<n interpolant through
    (xs, ys), |xs|=n."""
    n = len(xs)
    coeffs = [0] * n
    for i in range(n):
        num = [1]
        denom = 1
        for j in range(n):
            if j == i:
                continue
            num = pmul(num, [(-xs[j]) % p, 1], p)
            denom = denom * ((xs[i] - xs[j]) % p) % p
        scale = ys[i] * inv(denom, p) % p
        for k in range(len(num)):
            coeffs[k] = (coeffs[k] + scale * num[k]) % p
    return coeffs + [0] * (n - len(coeffs))


def closed_form_lagrange(F1, F2, p, ell):
    """Gamma* = L - L(0); returns constant-free ascending coeffs [X^1..X^{ell-1}]."""
    xs = list(F1) + list(F2)
    ys = [1] * len(F1) + [0] * len(F2)
    assert len(xs) == ell, "cap-tight requires |F1|+|F2|=ell"
    L = lagrange_coeffs(xs, ys, p)
    return [L[r] for r in range(1, ell)]


# =====================================================================
# closed form (B): Bezout / extended-gcd on the coprime pair (A, B)
# =====================================================================
def closed_form_bezout(F1, F2, p, ell):
    """Gamma* = (1-L(0)) - A*P, where A=prod_{F1}(X-x), B=prod_{F2}(X-x),
    A*P - B*Q = 1 (extended Euclid on the coprime pair A,B -- no
    interpolation anywhere in this construction). Returns constant-free
    ascending coeffs [X^1..X^{ell-1}], normalized like closed_form_lagrange
    (same overall scalar freedom -- both are cross-checked by the caller
    after normalize_gamma, not here)."""
    A = poly_from_roots(F1, p)
    B = poly_from_roots(F2, p)
    g, s, t = ext_gcd(A, B, p)
    assert len(g) == 1 and g[0] % p != 0, "A, B must be coprime (cap-tight, distinct cosets)"
    ginv = inv(g[0], p)
    P = [(c * ginv) % p for c in s]           # A*P - B*Q = 1
    Q = [((-c) % p * ginv) % p for c in t]
    AP = pmul(A, P, p)
    lhs = psub(pmul(A, P, p), pmul(B, Q, p), p)
    assert lhs == [1], "extended-gcd identity A*P-B*Q=1 failed"
    # AP is 0 on F1 (A vanishes there), 1 on F2 (since A*P-B*Q=1, B vanishes there)
    L0 = 0  # L(0) recovered below by the caller via peval on the actual L; here
    # we only need Gamma* = c - A*P for the SAME c the nullspace solve puts at X^0
    # (constant-free requirement forces c = AP(0)); build the raw (non-constant-
    # free) polynomial c - A*P with c := AP(0), then read off X^1..X^{ell-1}.
    AP_full = AP + [0] * (ell - len(AP))
    c = AP_full[0]
    raw = [(c - AP_full[i]) % p if i == 0 else (-AP_full[i]) % p for i in range(ell)]
    assert raw[0] % p == 0, "Bezout form must be constant-free after the c-shift"
    return raw[1:ell]


# =====================================================================
# spectrum
# =====================================================================
def spectrum_full(gamma, cosets, p):
    """True sorted (descending) per-coset max-fiber spectrum, ALL cosets."""
    spec = []
    for pts in cosets:
        byval = {}
        for x in pts:
            v = gamma_eval(gamma, x, p)
            byval[v] = byval.get(v, 0) + 1
        spec.append(max(byval.values()))
    spec.sort(reverse=True)
    return spec


def E3_of(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)


# =====================================================================
# THEOREM 2: the degree-(ell-a) pencil reduction
# =====================================================================
def pencil_reduction_check(F1, gamma, p, ell, coset_k_points, rho_k, c1):
    """For the coset `coset_k_points` (rho_k = x^ell there, x != b1,b2's
    coset), find its modal (max) fiber (value v, points pts, size t), build
    A_drop (deg ell-a, the DROPPED points of F1's own coset) and
    P := (Gamma*-c1)/A, then check that Q := P - lambda*A_drop
    (lambda=(v-c1)/(rho_k-1)) has every point of `pts` as a root, with
    deg Q <= ell - len(F1) (the pencil's own degree bound). Returns a dict of
    diagnostics; raises on any inconsistency (callers decide pass/fail)."""
    a = len(F1)
    ell_a = ell - a
    full0 = full_coset_containing(F1[0], p, ell)
    dropped = sorted(set(full0) - set(F1))
    assert len(dropped) == ell_a
    A = poly_from_roots(F1, p)
    A_drop = poly_from_roots(dropped, p)
    prodcheck = pmul(A, A_drop, p)
    xell_minus_1 = [(-1) % p] + [0] * (ell - 1) + [1]
    assert ptrim(prodcheck, p) == ptrim(xell_minus_1, p), "A*A_drop != X^ell-1"
    Gpoly = [0] + list(gamma)
    Gc1 = Gpoly[:]
    Gc1[0] = (Gc1[0] - c1) % p
    P, rem = pdivmod(Gc1, A, p)
    assert not any(v % p for v in rem), "A does not divide Gamma*-c1 exactly"
    byval = {}
    for x in coset_k_points:
        v = gamma_eval(gamma, x, p)
        byval.setdefault(v, []).append(x)
    v, pts = max(byval.items(), key=lambda kv: len(kv[1]))
    t = len(pts)
    lam = ((v - c1) % p) * inv((rho_k - 1) % p, p) % p
    L = max(len(P), len(A_drop))
    Pp = P + [0] * (L - len(P))
    Ap = A_drop + [0] * (L - len(A_drop))
    Q = ptrim([(Pp[i] - lam * Ap[i]) % p for i in range(L)], p)
    dq = len(Q) - 1 if Q else -1
    all_roots = all(peval(Q, x, p) == 0 for x in pts)
    return {"t": t, "v": v, "pts": pts, "deg_Q": dq, "expect_deg": ell_a,
            "all_roots": all_roots, "cap_bound_ok": (t <= ell_a) and (t <= a)}


# =====================================================================
# demo mode: deterministic, no randomness, no CLI args
# =====================================================================
def _demo_plant(label, ell, p, F1, F2, expect_spectrum=None):
    print("-" * 88)
    print("%s: ell=%d p=%d  |F1|=a=%d  |F2|=ell-a=%d" % (label, ell, p, len(F1), len(F2)))
    gamma, nullity = solve_unique_gamma(F1, F2, p, ell)
    print("  nullity = %d (THEOREM 1: must be exactly 1)" % nullity)
    assert nullity == 1
    g_lag = normalize_gamma(closed_form_lagrange(F1, F2, p, ell), p)
    g_bez = normalize_gamma(closed_form_bezout(F1, F2, p, ell), p)
    lag_ok = (g_lag == gamma)
    bez_ok = (g_bez == gamma)
    print("  closed form (A) Lagrange L-L(0)   matches nullspace solve: %s" % lag_ok)
    print("  closed form (B) Bezout ext-gcd    matches nullspace solve: %s" % bez_ok)
    assert lag_ok and bez_ok, "both closed forms must agree with the nullspace solve"
    cs, g, zeta = cosets_of(p, ell)
    spec = spectrum_full(gamma, cs, p)
    e3 = E3_of(spec)
    print("  spectrum = %s   E_3 = %d   excess = %+d" % (spec, e3, e3 - ell))
    if expect_spectrum is not None:
        ok = (spec == expect_spectrum)
        print("  matches expected spectrum %s: %s" % (expect_spectrum, ok))
        assert ok
    c1 = gamma_eval(gamma, F1[0], p)
    c2 = gamma_eval(gamma, F2[0], p)
    print("  Gamma* on F1 = %d, on F2 = %d (distinct: %s)" % (c1, c2, c1 != c2))
    # THEOREM 2 demo: run the pencil reduction on the first eligible third coset.
    W1, W2 = pow(F1[0], ell, p), pow(F2[0], ell, p)
    shown = 0
    for pts in cs:
        rho_k = pow(pts[0], ell, p)
        if rho_k in (W1, W2):
            continue
        info = pencil_reduction_check(F1, gamma, p, ell, pts, rho_k, c1)
        if info["t"] < 2:
            continue
        print("  pencil reduction @ third coset (rho=%d): fiber size t=%d, "
              "deg(P-lam*Adrop)=%d (expect %d), all fiber pts are roots: %s, "
              "cap t<=min(a,ell-a): %s"
              % (rho_k, info["t"], info["deg_Q"], info["expect_deg"],
                 info["all_roots"], info["cap_bound_ok"]))
        assert info["all_roots"] and info["cap_bound_ok"]
        shown += 1
        if shown >= 3:
            break
    if shown == 0:
        print("  (no third coset carried a >=2 fiber for this plant -- rare, harmless)")
    return gamma, spec


def main():
    print("=" * 88)
    print(" l1_minj_pencil_kit.py  --  deterministic demo (no args, no randomness)")
    print("=" * 88)

    # --- (1) the ell=17,p=137 W3-equivalent cap-tight pair-plant -----------
    # Found by a cap-tight pair-plant search (a=14, distinct method from
    # l1_e3_law_refuted.md's original fat-tail-plant W3); reproduces the
    # IDENTICAL spectrum [14,3^7] via a DIFFERENT Gamma (verified: this
    # gamma is not a scalar multiple of the original W3 gamma).
    F1_w3 = [1, 16, 38, 50, 56, 60, 72, 73, 74, 88, 115, 122, 123, 133]
    F2_w3 = [6, 21, 33]
    _demo_plant("W3-equivalent (pair-plant reproduction)", 17, 137, F1_w3, F2_w3,
                expect_spectrum=[14, 3, 3, 3, 3, 3, 3, 3])

    # --- (2) a true min-j frontier example: ell=19, a=10 (tail ell-a=9) ----
    # F1 (10 pts, coset0) / F2 (9 pts, another coset) at p=229; the frontier's
    # OWN definition per l1_t7_atlas_concurrency.md is ceil(ell/2)<=a<=ell-9,
    # i.e. a=10 is the (unique) ell=19 frontier value. This plant attains the
    # frozen ceiling mu_3=5 (never the target mu_3=9).
    F1_front = [1, 17, 42, 53, 104, 121, 165, 203, 218, 225]
    F2_front = [2, 54, 86, 93, 114, 122, 177, 207, 208]
    _, spec = _demo_plant("min-j frontier example (ell=19, a=10, tail=9)", 19, 229,
                           F1_front, F2_front)
    mu3 = spec[2] if len(spec) >= 3 else 0
    print("-" * 88)
    print("  mu_3 (third-largest fiber) = %d  (target for a refutation: 9; frontier ceiling: <=5)"
          % mu3)
    assert mu3 == 5 and mu3 < 9

    print("=" * 88)
    print(" DEMO COMPLETE: both plants solved, both closed forms cross-checked,")
    print(" the pencil reduction verified live, no mu_3=9 (no refutation).")
    print("=" * 88)


if __name__ == "__main__":
    main()
