#!/usr/bin/env python3
r"""
Verifier for l1_prime_ell_pv_refutation.md.

Background-free coset sunflower over F_p: H = mu_ell (order ell, ell | p-1);
t coset petals T_i = a_i H (locators X^ell - alpha_i, alpha_i = a_i^ell); m core
cosets, C = union of b_j H (beta_j = b_j^ell); distinct nonzero scalars c_i;
received word U = c_i * L_C on petal i, 0 on C.  k = m*ell+1, s = (m+1)*ell.  By
the PR #219 reduction (items 2 "Agreement formula" + 4 "Bijection" of
l1_general_reconstruction_collapse.md) a LISTED full-petal codeword (agreements
>= s) biject with a divisibility-minimal kernel set E = its exact missed core;
E is MIXED (not a union of full H-cosets)  <=>  the codeword is not H-periodic.
At PRIME ell the only subgroups of mu_ell are {1}, mu_ell, so a mixed minimal
kernel set is automatically stabilizer-PRIMITIVE.

At m = t+1 a full-petal codeword is P(X) = w(X^ell) + phi(X^ell)*g(X) with each
DFT sector g_r (r>=1) a CONSTANT gamma_r, so Gamma(X) = sum_{r>=1} gamma_r X^r is
one fixed polynomial (mixed <=> Gamma != 0); the retained set on core coset j is a
level set { x in b_j H : Gamma(x) = lambda_j }, lambda_j = -P_0(beta_j)/phi(beta_j),
P_0 = w + phi*g_0, g_0 = u + v*Y.

CLAIM REFUTED.  #224's "Named open target" PV(t,d,m) (l1_stabilizer_descent.md
L160-164) specializes at prime d=ell to: for ell prime and t < m < ell there is
no stabilizer-primitive mixed minimal kernel set (#222 "Corrected open target",
l1_coset_mixed_vacancy_threshold.md L91-94).  This verifier exhibits explicit
counterexamples at (t,ell,m) = (5,7,6) and (4,7,5), i.e. m = t+1 < ell.

Everything below is EMBEDDED + REPLAYED (no search): the witness constants
(gamma, coset reps, scalars c, u, v) are constants; the verifier reconstructs the
degree-<= m*ell codeword and checks every link by INDEPENDENT exact F_p polynomial
arithmetic (kernel/minimality via polynomial long division, not via the #219
reduction).  stdlib only, offline, deterministic; exit 0 iff every gate passes.

Gates:
  W5a/W5b : full t=5,m=6 witness replay at p=211 / p=421 (top6=16, R=16,
            agreements 51 >= 49, deg 41, mixed, |M|=26; kernel by division,
            per-coset rho_j = max fiber mu(b_j) of Gamma, minimality criterion
            discriminated on a synthetic non-minimal set, primitive traces).
  W4a/W4b : t=4,m=5 witness replay at p=211 / p=421, ZERO-MARGIN razor
            (R = 2*ell = 14 exactly, agreements 42 = s = 42, |M|=21).
  LF      : lambda-freeness at m=t+1 -- the map (c_1..c_t, u, v) -> (lambda_j) is
            surjective (rank m).  Checked as rank m for both witnesses and seeded
            distinct-coset draws (ell=7,11,13); plus the general N(Z) proof
            instantiated (bridge identity + top-2 coefficients + partial-fraction
            + reduced-system rank == m).
  SB      : salvage bound R <= (m + sqrt(m^2 + 4mB))/2, B=(ell-1)(ell-2), vs the
            exact integer program at ell=5,7 (all m); m=4 slice re-derives
            Theorem R (floor = 2ell-1 < 2ell); extras are Theta(ell^{3/2}).
  MM      : moment-method boundary -- the concentrated Gamma = X+X^2+...+X^{ell-1}
            saturates the pair-cap B=(ell-1)(ell-2) with a SINGLE coset yet has
            triple-count (ell-1)(ell-2)(ell-3) = Theta(ell^3); T3/B = ell-3 -> inf,
            so no triple-cap sits below Theta(ell^3).
  PB      : pair-budget equality -- both t=5 witness Gamma saturate
            sum_b rho(rho-1) = (ell-1)(ell-2) (a generic ell=7 extremal profile is
            [3,3,3,3,2,2,2]).
  FR      : corrected frontier -- fiber accounting gives onset m0 = ceil(2ell/3);
            EMBEDDED ell=11 (m0=8) and ell=13 (m0=10) Gamma replay their honest
            full-coset spectra to top-m0 >= 2ell and, by monotonicity, list for
            every m0 <= m <= ell-1.
  RP      : Replication Lemma mu_Gamma(bH) = mu_{Gtilde}(b^2 H), Gamma=Gtilde(X^2).
  TR      : Theorem-R consistency -- EXHAUSTIVE projective max at ell=5,t=3,m=4
            is 2ell-1 = 9 (never 2ell) at p=41 and p=61.
"""

import itertools
import math
import random
import sys

# ======================================================================= WITNESSES
# Embedded constants (from the end-to-end witness chain; see artifacts table in the
# note).  Per prime: gamma = (gamma_1..gamma_{ell-1}) sector polynomial; petal_reps
# a_i and core_reps b_j (actual F_p coset representatives); scalars c_i; g_0 = u+vY.
ELL = 7
WIT = {
    "t5": {  # (t, m) = (5, 6); listing threshold R >= (m-t+1)ell = 2ell = 14
        211: dict(gen=2, zeta=171,
                  gamma=[161, 178, 120, 90, 1, 10],
                  petal_reps=[1, 8, 16, 32, 64],
                  core_reps=[2, 4, 137, 117, 149, 92],
                  c=[116, 25, 171, 73, 27], u=187, v=0,
                  exp=dict(degP=41, R=16, top=16, agr=51, s=49, M=26, degWM=25,
                           prof=[3, 3, 3, 3, 2, 2], Mtrace=[4, 4, 4, 4, 5, 5])),
        421: dict(gen=2, zeta=370,
                  gamma=[110, 284, 49, 179, 1, 347],
                  petal_reps=[1, 8, 16, 32, 64],
                  core_reps=[2, 4, 134, 351, 188, 303],
                  c=[378, 74, 252, 420, 287], u=344, v=0,
                  exp=dict(degP=41, R=16, top=16, agr=51, s=49, M=26, degWM=25,
                           prof=[4, 3, 3, 2, 2, 2], Mtrace=[3, 4, 4, 5, 5, 5])),
    },
    "t4": {  # (t, m) = (4, 5); threshold 2ell = 14, hit with ZERO margin (R = 14)
        211: dict(gen=2, zeta=171,
                  gamma=[103, 84, 153, 136, 1, 146],
                  petal_reps=[1, 8, 16, 32],
                  core_reps=[2, 4, 117, 46, 82],
                  c=[179, 186, 152, 122], u=118, v=0,
                  exp=dict(degP=34, R=14, top=14, agr=42, s=42, M=21, degWM=20,
                           prof=[3, 3, 3, 3, 2], Mtrace=[4, 4, 4, 4, 5])),
        421: dict(gen=2, zeta=370,
                  gamma=[110, 284, 49, 179, 1, 347],
                  petal_reps=[1, 8, 16, 32],
                  core_reps=[2, 4, 134, 351, 188],
                  c=[163, 150, 106, 293], u=37, v=0,
                  exp=dict(degP=34, R=14, top=14, agr=42, s=42, M=21, degWM=20,
                           prof=[4, 3, 3, 2, 2], Mtrace=[3, 4, 4, 5, 5])),
    },
}

# Embedded FRONTIER witnesses for larger prime ell (gate FR).  Each is an explicit
# fixed sector polynomial Gamma (deg <= ell-1, constant-free) whose honest full-coset
# spectrum reaches the listing threshold 2ell at the onset m0 = ceil(2ell/3): ell=11
# (m0=8) and ell=13 (m0=10).  These are the ell=11/13 rows of the frontier table;
# the verifier REPLAYS their spectra (no search), so those NUMERIC numbers are gated,
# not merely asserted.  g = a generator of F_p^*, zeta = g^{(p-1)/ell} generates mu_ell.
FRONTIER = {
    11: {  # onset m0 = ceil(2*11/3) = 8
        353: dict(g=3, zeta=140, onset=8, top=23,
                  gamma=[291, 184, 121, 345, 205, 40, 36, 303, 2, 1]),
        419: dict(g=2, zeta=334, onset=8, top=22,
                  gamma=[14, 374, 280, 201, 331, 366, 361, 282, 2, 1]),
    },
    13: {  # onset m0 (best found) = 10 = ceil(2*13/3)+1 (prediction 9; +1 search-limited)
        313: dict(g=10, zeta=103, onset=10, top=26,
                  gamma=[55, 1, 200, 140, 185, 153, 47, 105, 111, 152, 2, 3]),
        443: dict(g=2, zeta=35, onset=10, top=26,
                  gamma=[274, 433, 255, 266, 86, 45, 56, 98, 370, 5, 3, 2]),
    },
}

# ==================================================================== F_p arithmetic
def inv(a, p):
    return pow(a % p, p - 2, p)


def pmul(a, b, p):
    if not a or not b:
        return []
    o = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                o[i + j] = (o[i + j] + ai * bj) % p
    while o and o[-1] == 0:
        o.pop()
    return o


def padd(a, b, p):
    n = max(len(a), len(b))
    o = [0] * n
    for i in range(len(a)):
        o[i] = a[i] % p
    for i in range(len(b)):
        o[i] = (o[i] + b[i]) % p
    while o and o[-1] == 0:
        o.pop()
    return o


def peval(coeffs, x, p):
    v = 0
    for c in reversed(coeffs):
        v = (v * x + c) % p
    return v


def poly_from_roots(roots, p):
    o = [1]
    for r in roots:
        o = pmul(o, [(-r) % p, 1], p)
    return o


def substitute_xk(coeffs, k):
    if not coeffs:
        return []
    o = [0] * ((len(coeffs) - 1) * k + 1)
    for i, c in enumerate(coeffs):
        o[i * k] = c
    return o


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
        res = padd(res, [(c * s) % p for c in num], p)
    return res


def divmod_poly(num, den, p):
    """exact long division num = q*den + r over F_p; return (q, r)."""
    num = num[:]
    dl = len(den) - 1
    dinv = inv(den[-1], p)
    q = [0] * (max(0, len(num) - dl))
    while len(num) - 1 >= dl and any(num):
        if num[-1] == 0:
            num.pop()
            continue
        deg = len(num) - 1
        coef = num[-1] * dinv % p
        q[deg - dl] = coef
        for i, dc in enumerate(den):
            num[deg - dl + i] = (num[deg - dl + i] - coef * dc) % p
        while num and num[-1] == 0:
            num.pop()
    while q and q[-1] == 0:
        q.pop()
    return q, num


# ================================================================= linear algebra
def row_rank(rows, ncols, p):
    A = [[x % p for x in r] for r in rows]
    nr = len(A)
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
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(ncols)]
        r += 1
        if r == nr:
            break
    return r


# ======================================================================= field setup
def find_gen(p):
    n = p - 1
    fac = set()
    m, d = n, 2
    while d * d <= m:
        while m % d == 0:
            fac.add(d)
            m //= d
        d += 1
    if m > 1:
        fac.add(m)
    for g in range(2, p):
        if all(pow(g, n // q, p) != 1 for q in fac):
            return g
    raise RuntimeError


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def prime_1_mod(ell):
    """smallest prime p > ell with ell | p-1 (so mu_ell <= F_p^* exists)."""
    q = ell + 1
    while True:
        q += 1
        if (q - 1) % ell == 0 and is_prime(q):
            return q


def eval_gamma(gamma, x, p, ell):
    v = 0
    xr = 1
    for r in range(1, ell):
        xr = xr * x % p
        v = (v + gamma[r - 1] * xr) % p
    return v


def pair_cap(gamma, p, ell, reps, H):
    tot = 0
    for b in reps:
        counts = {}
        for h in H:
            v = eval_gamma(gamma, b * h % p, p, ell)
            counts[v] = counts.get(v, 0) + 1
        for cc in counts.values():
            tot += cc * (cc - 1)
    return tot


# ================================================================== gate bookkeeping
FAILS = []


def check(name, ok, detail=""):
    ok = bool(ok)
    print(f"   [{'PASS' if ok else 'FAIL'}] {name:42s} {detail}")
    if not ok:
        FAILS.append(name)
    return ok


# ============================================================ witness replay (W*)
def replay(tag, p, W, t, m, ell=ELL):
    """Reconstruct P from embedded constants and verify the full chain by
    independent exact polynomial arithmetic.  Returns nothing; records gates."""
    print(f" -- [{tag}] p={p}: (t,ell,m)=({t},{ell},{m})  gamma={W['gamma']}"
          f"  c={W['c']} u={W['u']} v={W['v']}")
    E = W["exp"]
    zeta = W["zeta"]
    H = [pow(zeta, j, p) for j in range(ell)]
    a = W["petal_reps"]
    b = W["core_reps"]
    alpha = [pow(x, ell, p) for x in a]
    beta = [pow(x, ell, p) for x in b]
    c, u, v, gamma = W["c"], W["u"], W["v"], W["gamma"]

    # order/shape sanity: mu_ell genuine, distinct cosets, distinct nonzero scalars
    check(f"{tag}: H = mu_{ell} order {ell}",
          len(set(H)) == ell and pow(zeta, ell, p) == 1 and zeta != 1)
    labels = alpha + beta
    check(f"{tag}: {t+m} coset labels distinct & nonzero",
          len(set(labels)) == t + m and 0 not in labels)
    check(f"{tag}: {t} scalars c distinct & nonzero",
          len(set(c)) == t and 0 not in [x % p for x in c])

    # reconstruct P(X) = w(X^ell) + phi(X^ell)*(g0(X^ell) + Gamma(X))
    w = lagrange_interp(alpha, list(c), p)            # deg <= t-1, w(alpha_i)=c_i
    phi = poly_from_roots(alpha, p)                   # deg t
    gpoly = [0] * (ell + 1)
    gpoly[0] = u % p
    gpoly[ell] = v % p
    for r in range(1, ell):
        gpoly[r] = (gpoly[r] + gamma[r - 1]) % p
    while gpoly and gpoly[-1] == 0:
        gpoly.pop()
    P = padd(substitute_xk(w, ell), pmul(substitute_xk(phi, ell), gpoly, p), p)
    degP = len(P) - 1
    check(f"{tag}: deg P = {E['degP']} (<= m*ell = {m*ell})",
          degP == E["degP"] and degP <= m * ell, f"degP={degP}")
    check(f"{tag}: mixed (Gamma != 0)", any(x % p for x in gamma))

    # petals: P == c_i on all t*ell petal points
    petal_pts, petal_c = [], []
    pok = True
    for i in range(t):
        for h in H:
            x = a[i] * h % p
            petal_pts.append(x)
            petal_c.append(c[i] % p)
            if peval(P, x, p) != c[i] % p:
                pok = False
    check(f"{tag}: P = c_i on all {t*ell} petal points", pok)

    # core retention: retained = {P=0}, missed M = {P!=0}
    retained, missed, prof = [], [], []
    for j in range(m):
        rj = 0
        for h in H:
            x = b[j] * h % p
            if peval(P, x, p) % p == 0:
                retained.append(x)
                rj += 1
            else:
                missed.append(x)
        prof.append(rj)
    R = len(retained)
    agr = t * ell + R
    check(f"{tag}: retained R = {E['R']} (= top{m} = {E['top']})",
          R == E["R"], f"R={R} per-coset={prof}")
    check(f"{tag}: per-coset retained profile", prof == E["prof"], f"{prof}")
    # LISTED: agreements >= s = (m+1)ell  <=>  retained R >= (m-t+1)ell
    check(f"{tag}: LISTED  agreements {agr} >= s = {E['s']}"
          + ("  (zero margin, R = 2ell)" if agr == E["s"] else f"  (margin {agr-E['s']})"),
          agr >= (m + 1) * ell and agr == E["agr"])
    check(f"{tag}: retention threshold  R >= (m-t+1)ell = {(m-t+1)*ell}",
          R >= (m - t + 1) * ell)

    # domain sanity
    allpts = petal_pts + retained + missed
    check(f"{tag}: {(t+m)*ell} distinct evaluation points",
          len(set(allpts)) == (t + m) * ell)

    # ---- minimal kernel set M by INDEPENDENT polynomial long division ----
    # P is a codeword <=> P = W_M * L_{C\M} with L_{C\M} = prod over retained (X - x).
    # M is a KERNEL SET <=> deg W_M <= |M|.  Division is independent of the CRT
    # interpolation / #219 reduction that produced the witness.
    Lret = poly_from_roots(retained, p)               # L_{C\M}
    Q, rem = divmod_poly(P, Lret, p)
    degWM = len(Q) - 1
    check(f"{tag}: P / L_(C\\M) exact (remainder 0)", rem == [] or not any(rem))
    check(f"{tag}: reassemble Q * L_(C\\M) == P", pmul(Q, Lret, p) == P)
    check(f"{tag}: kernel  deg W_M = {E['degWM']} <= |M| = {E['M']}",
          degWM == E["degWM"] and degWM <= len(missed), f"degWM={degWM} |M|={len(missed)}")
    check(f"{tag}: |M| = {E['M']} = (t-1)ell - (R-2ell) = {(t-1)*ell}-{R-2*ell}",
          len(missed) == E["M"] and len(missed) == (t - 1) * ell - (R - 2 * ell))

    # per-coset EXTREMALITY (independent of the witness's chosen c/u/v):  on each
    # core coset the retained set is a MAXIMUM level set of the fixed Gamma, i.e.
    # rho_j equals the top fiber mu(b_j) of Gamma's own value-multiset on b_j H,
    # read straight off Gamma.  This is a genuine falsifiable necessary condition --
    # a mis-stated retained profile or wrong Gamma breaks it (it does NOT hold for
    # an arbitrary level choice, only for the modal one the witness targets).
    mu_spec = []
    for j in range(m):
        cnt = {}
        for h in H:
            val = eval_gamma(gamma, b[j] * h % p, p, ell)
            cnt[val] = cnt.get(val, 0) + 1
        mu_spec.append(max(cnt.values()))
    check(f"{tag}: per-coset rho_j = max fiber mu(b_j) of Gamma  {prof}",
          mu_spec == prof, f"mu={mu_spec}")

    # divisibility-minimality criterion (shared code path):  for a candidate missed
    # core M' with complement retained' in C, a point x in M' is DELETABLE (M'\{x}
    # is still a kernel set) iff P is divisible by L_{(C\M') + x} with quotient
    # degree <= |M'|-1.  M' is MINIMAL iff no point is deletable.
    def deletable_points(missed_set, retained_set):
        Lr = poly_from_roots(retained_set, p)
        out = []
        for x in missed_set:
            Ld = pmul(Lr, [(-x) % p, 1], p)           # L_{(C\M') + x}
            Qd, rd = divmod_poly(P, Ld, p)
            if (rd == [] or not any(rd)) and (len(Qd) - 1 <= len(missed_set) - 1):
                out.append(x)
        return out

    # (a) the actual missed core M is MINIMAL: no deletable point.
    delM = deletable_points(missed, retained)
    check(f"{tag}: MINIMAL (no single-point deletion of M is a kernel set)",
          delM == [], "" if not delM else f"deletable {delM[:3]}")
    # (b) the criterion is NOT vacuous -- exercise the identical code path on the
    #     deliberately NON-minimal kernel set M+{r0} (r0 = a retained point): it must
    #     flag exactly r0 and nothing else, since (M+{r0})\{r0} = M is a kernel set.
    #     This shows deletable_points CAN return "non-minimal", so (a)'s PASS carries
    #     content (the missed-core minimality is otherwise structural, cf. the note).
    r0 = retained[0] if retained else None            # listed => retained nonempty
    adv = deletable_points(missed + [r0], [x for x in retained if x != r0]) if retained else None
    check(f"{tag}: minimality criterion discriminates (flags r0 in M+{{r0}}, only r0)",
          adv == [r0], f"flagged={adv if adv is None else adv[:3]}")

    # primitive: M meets each core coset in a proper nonempty subset => (prime ell)
    # setwise stabilizer trivial.
    trace = []
    for j in range(m):
        cj = set(b[j] * h % p for h in H)
        trace.append(len(set(missed) & cj))
    check(f"{tag}: MIXED / PRIMITIVE  traces {trace} (all 0 < . < {ell})",
          all(0 < x < ell for x in trace) and sum(trace) == len(missed)
          and trace == E["Mtrace"])

    # self-consistency: also equals the recorded codeword shape (mixed => Gamma!=0
    # already checked); nothing else embedded to compare.


# =========================================================== lambda-freeness (LF)
def lam_columns(alpha, beta, p):
    """Columns of the linear map (c_1..c_t, u, v) -> (lambda_1..lambda_m),
    lambda_j = -w(beta_j)/phi(beta_j) - (u + v beta_j).  Returns list of m columns
    for inputs [c_1..c_t, u, v] (each column is a length-m F_p vector) and phi."""
    t = len(alpha)
    m = len(beta)
    phi = poly_from_roots(alpha, p)
    phib = [peval(phi, beta[j], p) for j in range(m)]

    def lam_of(cc, u, v):
        w = lagrange_interp(alpha, list(cc), p)
        out = []
        for j in range(m):
            wbj = peval(w, beta[j], p)
            out.append((-(wbj + phib[j] * ((u + v * beta[j]) % p)) * inv(phib[j], p)) % p)
        return out

    base = lam_of([0] * t, 0, 0)
    cols = []
    for i in range(t):
        e = [1 if k == i else 0 for k in range(t)]
        cols.append([(lam_of(e, 0, 0)[j] - base[j]) % p for j in range(m)])
    cols.append([(lam_of([0] * t, 1, 0)[j] - base[j]) % p for j in range(m)])
    cols.append([(lam_of([0] * t, 0, 1)[j] - base[j]) % p for j in range(m)])
    return cols, base, phib


def gate_LF():
    print("=== GATE LF: lambda-freeness at m=t+1 (surjective; N(Z) proof instantiated) ===")
    ell = ELL
    # (1) rank m for the two witnesses' actual configs
    for tag, t, m in [("t5", 5, 6), ("t4", 4, 5)]:
        for p, W in WIT[tag].items():
            alpha = [pow(x, ell, p) for x in W["petal_reps"]]
            beta = [pow(x, ell, p) for x in W["core_reps"]]
            cols, base, _ = lam_columns(alpha, beta, p)
            check(f"LF {tag} p={p}: zero constant & rank {m}",
                  all(z == 0 for z in base) and row_rank(cols, m, p) == m)

    # (2) rank m over seeded distinct-coset draws at several (ell, t)
    for ellx, t, primes, ndraw in [(7, 5, [211, 337, 421], 40),
                                    (11, 9, [331, 419], 12),
                                    (13, 11, [313, 521], 8)]:
        m = t + 1
        allok = True
        for p in primes:
            g = find_gen(p)
            n = (p - 1) // ellx
            reps = [pow(g, i, p) for i in range(n)]
            rng = random.Random(1000 + p)
            for _ in range(ndraw):
                idx = rng.sample(range(n), t + m)
                al = [pow(reps[i], ellx, p) for i in idx[:t]]
                be = [pow(reps[i], ellx, p) for i in idx[t:]]
                cols, base, _ = lam_columns(al, be, p)
                if not (all(z == 0 for z in base) and row_rank(cols, m, p) == m):
                    allok = False
        check(f"LF ell={ellx} t={t}: rank {m} on all seeded distinct-coset draws", allok)

    # (3) the general N(Z) proof, instantiated on a seeded config (ell=11, t=9):
    #   left-null kappa of the map  <=>  (A) sum kappa = 0, (B) sum kappa*beta = 0,
    #   (C') sum_j kappa_j/(beta_j - alpha_i) = 0 for all i.  With
    #   N(Z) = sum_j kappa_j prod_{j'!=j}(Z - beta_{j'})  (deg m-1):
    #     [Z^{m-1}] N = sum kappa          (A kills the top coeff)
    #     [Z^{m-2}] N = sum kappa*beta - S*sum kappa   (B then kills the next)
    #     N(alpha_i)  = prod_j(alpha_i - beta_j) * sum_j kappa_j/(alpha_i - beta_j)
    #                                       (C' <=> N(alpha_i) = 0, t roots)
    #   deg N <= m-3 = t-2 with t distinct roots => N == 0 => kappa == 0.
    for ellx, t, p in [(7, 5, 421), (11, 9, 331)]:
        m = t + 1
        g = find_gen(p)
        n = (p - 1) // ellx
        reps = [pow(g, i, p) for i in range(n)]
        rng = random.Random(55 + p)
        idx = rng.sample(range(n), t + m)
        al = [pow(reps[i], ellx, p) for i in idx[:t]]
        be = [pow(reps[i], ellx, p) for i in idx[t:]]
        phi = poly_from_roots(al, p)

        # bridge identity: phi(beta_j) = (beta_j - alpha_i) * prod_{i'!=i}(beta_j-alpha_i')
        bridge = True
        for j in range(m):
            for i in range(t):
                rest = 1
                for ii in range(t):
                    if ii != i:
                        rest = rest * (be[j] - al[ii]) % p
                if peval(phi, be[j], p) != (be[j] - al[i]) * rest % p:
                    bridge = False
        check(f"LF N(Z) ell={ellx}: bridge phi(beta)=(beta-alpha_i)*prod_(i'!=i)", bridge)

        # coefficient + partial-fraction identities for a random kappa
        kap = [rng.randrange(1, p) for _ in range(m)]
        Ncoef = []
        for j in range(m):
            fac = poly_from_roots([be[jj] for jj in range(m) if jj != j], p)
            Ncoef = padd(Ncoef, [kap[j] * x % p for x in fac], p)
        S = sum(be) % p
        top1 = Ncoef[m - 1] if len(Ncoef) > m - 1 else 0
        top2 = Ncoef[m - 2] if len(Ncoef) > m - 2 else 0
        idA = (top1 == sum(kap) % p)
        idB = (top2 == (sum(kap[j] * be[j] for j in range(m)) - S * sum(kap)) % p)
        pf = True
        for i in range(t):
            lhs = peval(Ncoef, al[i], p)
            prod = 1
            for j in range(m):
                prod = prod * (al[i] - be[j]) % p
            rhs = prod * sum(kap[j] * inv(al[i] - be[j], p) for j in range(m)) % p
            if lhs != rhs:
                pf = False
        check(f"LF N(Z) ell={ellx}: deg-{m-1} coeff [Z^(m-1)]=sum k, [Z^(m-2)]=sum k*b - S*sum k",
              idA and idB)
        check(f"LF N(Z) ell={ellx}: partial-fraction  N(alpha_i)=prod(a_i-b)*sum k/(a_i-b)", pf)

        # the conclusion: reduced system {(A),(B),(C')} on kappa has rank m => kappa=0.
        red = [[1] * m, [be[j] % p for j in range(m)]]
        for i in range(t):
            red.append([inv(be[j] - al[i], p) for j in range(m)])
        rk = row_rank(red, m, p)
        # and consistency with the direct map rank
        cols, _, _ = lam_columns(al, be, p)
        check(f"LF N(Z) ell={ellx}: reduced-system rank {m} (=> kappa=0) == map rank",
              rk == m and row_rank(cols, m, p) == m)


# ================================================================= salvage bound (SB)
def brute_ip(m, ell, B):
    best = 0

    def rec(i, ssum, scost):
        nonlocal best
        if scost > B:
            return
        if i == m:
            best = max(best, ssum)
            return
        for val in range(1, ell):
            rec(i + 1, ssum + val, scost + val * (val - 1))

    rec(0, 0, 0)
    return best


def greedy_ip(m, ell, B):
    import heapq
    rho = [1] * m
    cost, S = 0, m
    heap = [(2, j) for j in range(m)]
    heapq.heapify(heap)
    while heap:
        c, j = heapq.heappop(heap)
        if rho[j] >= ell - 1 or cost + c > B:
            if rho[j] >= ell - 1:
                continue
            break
        cost += c
        rho[j] += 1
        S += 1
        if rho[j] < ell - 1:
            heapq.heappush(heap, (2 * rho[j], j))
    return S


def gate_SB():
    print("=== GATE SB: salvage bound R <= (m+sqrt(m^2+4mB))/2 vs exact IP (PROVED) ===")
    # all m at ell=5,7: greedy == brute <= closed form
    for ell in (5, 7):
        B = (ell - 1) * (ell - 2)
        allok = True
        detail = []
        for m in range(2, ell):
            gr = greedy_ip(m, ell, B)
            br = brute_ip(m, ell, B)
            cf = (m + math.sqrt(m * m + 4 * m * B)) / 2
            detail.append(f"m={m}:IP={br}<=cf={cf:.2f}")
            if not (gr == br and br <= cf + 1e-9):
                allok = False
        check(f"SB ell={ell}: greedy IP == brute IP <= closed form (all m)", allok,
              " ".join(detail))
    # m=4 slice re-derives Theorem R: floor(closed form) = 2ell-1 < 2ell
    allok = True
    for ell in (5, 7, 11, 13, 17, 23):
        B = (ell - 1) * (ell - 2)
        cf4 = (4 + math.sqrt(16 + 16 * B)) / 2
        if not (math.floor(cf4) == 2 * ell - 1 and cf4 < 2 * ell):
            allok = False
    check("SB m=4 slice: floor(closed form) = 2ell-1 < 2ell (re-derives Theorem R)", allok)
    # extras R-2ell at m=ell-1 are super-linear (Theta(ell^{3/2})), not O(ell)
    ratios = []
    for ell in (13, 17, 23, 31, 41):
        B = (ell - 1) * (ell - 2)
        m = ell - 1
        cf = (m + math.sqrt(m * m + 4 * m * B)) / 2
        ratios.append((cf - 2 * ell) / ell)
    check("SB m=ell-1: extras/ell increasing (Theta(ell^{3/2}), not O(ell))",
          ratios[-1] > 1.5 * ratios[0], f"extras/ell={[round(r,2) for r in ratios]}")


# ============================================================= moment method (MM)
def gate_MM():
    print("=== GATE MM: concentrated Gamma saturates pair-cap on ONE coset, T3=Theta(ell^3) (PROVED) ===")
    # Gamma(X) = X + X^2 + ... + X^{ell-1}.  On H=mu_ell it takes value -1 exactly
    # ell-1 times (h != 1 => sum_{r=1}^{ell-1} h^r = -1) and ell-1 once (h=1), so a
    # SINGLE coset already has mu=ell-1 and saturates the pair-cap B=(ell-1)(ell-2);
    # its triple-count is (ell-1)(ell-2)(ell-3)=Theta(ell^3).  These counts are
    # p-independent (they only use mu_ell), so any prime p = 1 mod ell exhibits them.
    T3overB = []
    for ell in (7, 11, 13, 19, 31):
        p = prime_1_mod(ell)
        g = find_gen(p)
        zeta = pow(g, (p - 1) // ell, p)
        H = [pow(zeta, j, p) for j in range(ell)]
        gamma = [1] * (ell - 1)
        cnt = {}
        for h in H:
            val = eval_gamma(gamma, h, p, ell)
            cnt[val] = cnt.get(val, 0) + 1
        mu = max(cnt.values())
        pair1 = sum(c * (c - 1) for c in cnt.values())
        trip1 = sum(c * (c - 1) * (c - 2) for c in cnt.values())
        B = (ell - 1) * (ell - 2)
        T3 = (ell - 1) * (ell - 2) * (ell - 3)
        check(f"MM ell={ell}: one coset mu={ell-1}, pair={B}=B, triple={T3}=Theta(ell^3)",
              mu == ell - 1 and pair1 == B and trip1 == T3,
              f"mu={mu} pair={pair1} trip={trip1}")
        T3overB.append(T3 / B if B else 0.0)
    check("MM: triple/pair ratio T3/B = ell-3 strictly increasing (no triple-cap below Theta(ell^3))",
          all(T3overB[i] < T3overB[i + 1] for i in range(len(T3overB) - 1)),
          f"T3/B={[round(x, 1) for x in T3overB]}")


# =============================================================== frontier onset (FR)
def spectrum_desc(gamma, p, ell, g, zeta):
    """honest full-coset spectrum: per-coset max fiber of Gamma over ALL (p-1)/ell
    cosets, sorted descending (no lemma used, exhaustive value-multiset)."""
    n = (p - 1) // ell
    H = [pow(zeta, j, p) for j in range(ell)]
    fibers = []
    for i in range(n):
        b = pow(g, i, p)
        cnt = {}
        for h in H:
            val = eval_gamma(gamma, b * h % p, p, ell)
            cnt[val] = cnt.get(val, 0) + 1
        fibers.append(max(cnt.values()))
    fibers.sort(reverse=True)
    return fibers


def gate_FR():
    print("=== GATE FR: frontier onset m0=ceil(2ell/3) -- fiber accounting + embedded ell=11,13 (NUMERIC) ===")
    # (1) exact fiber accounting: reach 2ell with k=2(ell-m) three-fibers +
    #     (3m-2ell) two-fibers over m cosets, feasible iff k+twos = m and k <= m,
    #     i.e. iff m >= 2ell/3; the onset is m0 = ceil(2ell/3), and m0-1 is infeasible.
    for ell in (7, 11, 13, 17):
        m0 = math.ceil(2 * ell / 3)
        k, twos = 2 * (ell - m0), 3 * m0 - 2 * ell
        feasible = (k >= 0 and twos >= 0 and k + twos == m0 and 2 * m0 + k == 2 * ell and k <= m0)
        m1 = m0 - 1
        infeasible_below = (2 * (ell - m1) > m1)      # k > m at m0-1
        check(f"FR ell={ell}: onset m0=ceil(2ell/3)={m0} ({k} threes + {twos} twos), m0-1 infeasible",
              feasible and infeasible_below)
    # (2) embedded frontier witnesses: replay the honest spectrum, confirm listing at
    #     the onset AND (monotonicity: top-m nondecreasing) at every m0 <= m <= ell-1.
    for ell in sorted(FRONTIER):
        for p, F in sorted(FRONTIER[ell].items()):
            g, zeta, gamma, m0 = F["g"], F["zeta"], F["gamma"], F["onset"]
            check(f"FR ell={ell} p={p}: mu_{ell} genuine, g a generator",
                  pow(zeta, ell, p) == 1 and zeta != 1 and find_gen(p) == g)
            spec = spectrum_desc(gamma, p, ell, g, zeta)
            top = sum(spec[:m0])
            check(f"FR ell={ell} p={p}: top-{m0} spectrum = {top} >= 2ell = {2 * ell} (lists at onset)",
                  top == F["top"] and top >= 2 * ell, f"spec[:m0]={spec[:m0]}")
            nondec = all(sum(spec[:i + 1]) >= sum(spec[:i]) for i in range(1, ell - 1))
            band = all(sum(spec[:m]) >= 2 * ell for m in range(m0, ell))
            check(f"FR ell={ell} p={p}: top-m nondecreasing => lists for all {m0} <= m <= ell-1",
                  nondec and band)


# ================================================================= pair budget (PB)
def gate_PB():
    print("=== GATE PB: pair-budget equality of the extremal ell=7 profile (LEMMA/NUMERIC) ===")
    ell = ELL
    B = (ell - 1) * (ell - 2)
    # a GENERIC ell=7 extremal profile [3,3,3,3,2,2,2] (the p-independent shape S1
    # found saturating the budget; not either witness's own m) has sum rho(rho-1) = B
    prof = [3, 3, 3, 3, 2, 2, 2]
    check(f"PB generic extremal profile {prof}: sum rho(rho-1) = {B} = (ell-1)(ell-2)",
          sum(r * (r - 1) for r in prof) == B)
    # the two t=5 witness Gamma actually SATURATE the global pair budget
    for p, W in WIT["t5"].items():
        g = find_gen(p)
        zeta = W["zeta"]
        H = [pow(zeta, j, p) for j in range(ell)]
        n = (p - 1) // ell
        reps = [pow(g, i, p) for i in range(n)]
        pc = pair_cap(W["gamma"], p, ell, reps, H)
        check(f"PB t5 p={p}: Gamma saturates sum_b rho(rho-1) = {B}", pc == B, f"pc={pc}")
    # Lemma R (upper bound) holds for every witness Gamma
    allok = True
    for tag in ("t5", "t4"):
        for p, W in WIT[tag].items():
            g = find_gen(p)
            H = [pow(W["zeta"], j, p) for j in range(ell)]
            reps = [pow(g, i, p) for i in range((p - 1) // ell)]
            if pair_cap(W["gamma"], p, ell, reps, H) > B:
                allok = False
    check(f"PB Lemma R: every witness Gamma has sum_b rho(rho-1) <= {B}", allok)


# ============================================================== replication (RP)
def gate_RP():
    print("=== GATE RP: Replication Lemma mu_Gamma(bH)=mu_Gtilde(b^2 H), Gamma=Gtilde(X^2) (PROVED) ===")
    for ell, p, D in [(7, 337, 3), (11, 353, 5), (13, 313, 6)]:
        g = find_gen(p)
        n = (p - 1) // ell
        reps = [pow(g, i, p) for i in range(n)]
        zeta = pow(g, n, p)
        H = [pow(zeta, j, p) for j in range(ell)]
        rng = random.Random(2024 + p)
        allok = True
        for _ in range(5):
            tg = [rng.randrange(p) for _ in range(D)]
            if not any(tg):
                continue
            gamma = [0] * (ell - 1)
            for j in range(1, D + 1):
                gamma[2 * j - 1] = tg[j - 1]           # Gamma(X) = Gtilde(X^2)
            for b in reps:
                cnt = {}
                for h in H:
                    val = eval_gamma(gamma, b * h % p, p, ell)
                    cnt[val] = cnt.get(val, 0) + 1
                muG = max(cnt.values())
                bc = pow(b, 2, p)                       # b^2 H
                cntT = {}
                for h in H:
                    y = bc * h % p
                    val = 0
                    yr = 1
                    for j in range(1, D + 1):
                        yr = yr * y % p
                        val = (val + tg[j - 1] * yr) % p
                    cntT[val] = cntT.get(val, 0) + 1
                if muG != max(cntT.values()):
                    allok = False
        check(f"RP ell={ell} p={p} D={D}: identity on all cosets", allok)


# =============================================================== Theorem R (TR)
def gate_TR():
    print("=== GATE TR: Theorem-R exhaustive max at ell=5,t=3,m=4 stays 2ell-1=9 (never 2ell) ===")
    ell, m = 5, 4
    for p in (41, 61):
        g = find_gen(p)
        n = (p - 1) // ell
        reps = [pow(g, i, p) for i in range(n)]
        zeta = pow(g, n, p)
        H = [pow(zeta, j, p) for j in range(ell)]
        # precompute (b*h)^r tables for exact exhaustive projective scan of Gamma
        tab = [[[pow(b * h % p, r, p) for h in H] for r in range(1, ell)] for b in reps]
        best = 0
        L = ell - 1
        for lead in range(L):                          # first nonzero coeff == 1
            for tail in itertools.product(range(p), repeat=L - 1 - lead):
                gamma = [0] * lead + [1] + list(tail)
                spec = []
                for ci in range(n):
                    rr = tab[ci]
                    counts = {}
                    for hi in range(ell):
                        val = 0
                        for r in range(1, ell):
                            gr = gamma[r - 1]
                            if gr:
                                val = (val + gr * rr[r - 1][hi]) % p
                        counts[val] = counts.get(val, 0) + 1
                    spec.append(max(counts.values()))
                spec.sort(reverse=True)
                s = sum(spec[:m])
                if s > best:
                    best = s
        check(f"TR p={p}: exhaustive max top{m} = 2ell-1 = {2*ell-1} (< 2ell = {2*ell})",
              best == 2 * ell - 1 and best < 2 * ell, f"max={best}")


# ==================================================================== driver
def main():
    print("#" * 78)
    print("# PV(prime) REFUTATION at m = t+1 < ell  --  witness replay + support lemmas")
    print("#" * 78)
    print("\n=== GATES W5a/W5b : t=5, m=6, ell=7 witness replay (primary refutation) ===")
    replay("W5a", 211, WIT["t5"][211], t=5, m=6)
    replay("W5b", 421, WIT["t5"][421], t=5, m=6)
    print("\n=== GATES W4a/W4b : t=4, m=5, ell=7 witness replay (zero-margin razor) ===")
    replay("W4a", 211, WIT["t4"][211], t=4, m=5)
    replay("W4b", 421, WIT["t4"][421], t=4, m=5)
    print()
    gate_LF()
    print()
    gate_SB()
    print()
    gate_MM()
    print()
    gate_FR()
    print()
    gate_PB()
    print()
    gate_RP()
    print()
    gate_TR()
    print("\n" + "=" * 78)
    if FAILS:
        print(f"RESULT: {len(FAILS)} FAILURE(S): {FAILS}")
        sys.exit(1)
    print("RESULT: ALL GATES PASS  -- PV(prime) refuted at (5,7,6) and (4,7,5);"
          " support lemmas verified.")
    sys.exit(0)


if __name__ == "__main__":
    main()
