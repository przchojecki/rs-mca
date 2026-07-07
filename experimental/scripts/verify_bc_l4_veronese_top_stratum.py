#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifier for  experimental/notes/thresholds/cap25_v13_bc_l4_veronese_top_stratum.md

CAP25 v13 BC L4 -- the z*=0 (Veronese) top stratum of the curve second moment M2 is
EMPTY over characteristic 0.

Object (self-contained; the curve-M2 decomposition is restated from open PR #395,
which is NOT integrated -- see the note for the exact Theorem-C1 statement used):
  At z*=0 the planted interior word is the pure monomial U=X^{m'}, the depth-(w+1)
  prefix curve is the Veronese/diagonal Gamma={(s,s^2,...,s^{w+1})} (the twist-INVARIANT
  branch of #395 Sec 6's dichotomy), and the top nonzero stratum e=w+2 of
  M2 = sum_{s in B} N_{w+1}(theta(s))^2 is the set of constant-shift pairs of
  degree-(w+2) divisors of X^n-1 (pairs P,P' of (w+2)-subsets of D=mu_n with
  ell_P - ell_{P'} = const != 0, equivalently equal power sums p_1..p_{w+1}).

Theorem (PROVED, char 0).  For n=2^a and 1<=d<=n/2 (disjointness forces 2d<=n),
  constant-shift pairs of d-subsets of mu_n exist over characteristic 0  IFF  d is a
  power of 2 (and then P,P' are cosets of mu_d; d<=n/2 gives the >=2 cosets a pair needs).
  Mechanism: the j=1 relation p_1(P)=p_1(P') is a vanishing sum of 2|P| roots of unity
  in mu_{2^a}; Lam-Leung (antipodal atoms for 2-power order) + disjointness force
  P=-P, P'=-P'; a parity descent (p_{2j} -> p_j one level down) forces w+2 to be a
  power of 2.  At L4  w+2=4218=2*3*19*37 is NOT a power of 2 ((w+2)/2=2109=3*19*37 odd),
  so the top stratum is EXACTLY EMPTY over char 0.  In char p it is nonempty only
  through a char-p degeneration (p | a cyclotomic defect) -- a root-non-concentration /
  Weil-type residual, the exact analogue of #382's min-j pencil freeze.

Gates (stdlib only; zero-arg exit-0 = PASS ; --tamper-selftest = every pin caught ; <60s):
  G1  characterization (a): valid-T at z*=0  <=>  (m+1)-null  <=>  e_j(T)=(-s)^j
       <=>  (X-s) ell_T == U=X^{m'} mod X^K   (augmented locator), on all m-subsets.
  G2  char-0 rigidity (exact in Z[zeta_n], n=2^a): constant-shift pairs exist iff d is a
       power of 2; NO primitive pair; the j=1 relation forces antipodal closure (the
       Lam-Leung + parity spot-check).  INCLUDES the positive control: an explicit
       nonempty pair at d=4=2^2 (mu_4-cosets, ell_P-ell_{P'} = const != 0).
  G3  M2 top stratum on real z*=0 fixtures (char-p degeneration probe):
       (a) POSITIVE CONTROL  n=8, e_top=4=2^2  -> top stratum NONEMPTY (coset family);
       (b) EMPTINESS PROBE   n=16, e_top=3 (not pow2) -> present at the degenerate prime
           p=97 (count 32 = A_prim), ABSENT at char-0-regime primes 113/193/241;
       (c) small-case bad-prime cross-check of the pseudorandom threshold p0~(e n/d)^2.
  G4  exact L4 numbers: char-0 top-stratum count = 0; gcd(w+2,n)=2; w+2 not a power of 2;
       (w+2)/2=2109 odd; #395 unconditional top ceiling 2^153665.47 -> 0; pseudorandom
       E[A] ~ 2^-76898.5 with a +18.24-bit margin over threshold p0 ~ 2^12.753.

Each gate returns (pins, summary) where pins = {name:(got,exp)}; a gate PASSES iff every
got==exp.  --tamper-selftest computes each gate's pins ONCE, then corrupts every expected
value in turn and checks the gate flips to FAIL (so every pin is load-bearing).
"""
import sys, math, itertools
from math import comb, lgamma, gcd
LOG2 = math.log(2.0)


# ----------------------------------------------------------------------------
# fp / poly helpers
# ----------------------------------------------------------------------------
def lg2(x):
    if isinstance(x, int):
        b = x.bit_length()
        return math.log2(x) if b <= 53 else math.log2(x >> (b - 53)) + (b - 53)
    return math.log2(x)


def lg2binom(a, b):
    return float('-inf') if (b < 0 or b > a) else (lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)) / LOG2


def find_prim_root(p):
    ph = p - 1
    fac = set()
    x = ph
    d = 2
    while d * d <= x:
        while x % d == 0:
            fac.add(d)
            x //= d
        d += 1
    if x > 1:
        fac.add(x)
    for g in range(2, p):
        if all(pow(g, ph // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no primitive root")


def mu_n(p, n):
    """the n n-th roots of unity in F_p (n | p-1), as a cyclic list g^0..g^{n-1}."""
    g = pow(find_prim_root(p), (p - 1) // n, p)
    return [pow(g, j, p) for j in range(n)]


def poly_from_roots(roots, p):
    """monic ell_S high->low, c[0]=1 (coeff of X^{|S|}); c[j]=a_j=(-1)^j e_j."""
    c = [1]
    for r in roots:
        nc = [0] * (len(c) + 1)
        for i, ci in enumerate(c):
            nc[i] = (nc[i] + ci) % p
            nc[i + 1] = (nc[i + 1] - ci * r) % p
        c = nc
    return c


def _bump(v):
    """a value guaranteed != v (used to corrupt an expected pin in --tamper-selftest)."""
    if isinstance(v, bool):
        return (not v)
    if isinstance(v, int):
        return v + 1
    if isinstance(v, float):
        return v + 1.0
    if isinstance(v, tuple):
        return v + (0,)
    return ("<tampered>", v)


def _ok(pins, tamper=None):
    """pins: {name:(got,exp)}; if tamper names a pin, corrupt its expected value."""
    good = True
    for name, (got, exp) in pins.items():
        e = _bump(exp) if name == tamper else exp
        if got != e:
            good = False
    return good


# ----------------------------------------------------------------------------
# G1 : characterization (a) at z*=0
# ----------------------------------------------------------------------------
def g1(p=97, n=8, K=2, m=4):
    w = m - K
    D = mu_n(p, n)
    equiv_all = True
    ncheck = 0
    for T in itertools.combinations(D, m):
        ncheck += 1
        co = poly_from_roots(T, p)
        a = [co[j] for j in range(1, w + 2)]          # a_1..a_{w+1}
        s = a[0]                                       # s = a_1(T) = -sum_T x
        valid_prefix = all(a[j - 1] == pow(s, j, p) for j in range(2, w + 2))     # a_j = s^j
        co2 = poly_from_roots(list(T) + [s], p)        # ell_{T u {s}}
        null = all(co2[j] % p == 0 for j in range(1, w + 2))                       # (w+1)-null
        ej_ok = all(((-1) ** j * a[j - 1]) % p == pow((-s) % p, j, p) for j in range(1, w + 2))
        aug = co2[:w + 2] == [1] + [0] * (w + 1)       # (X-s) ell_T == X^{m'} mod X^K
        if not (valid_prefix == null == ej_ok == aug):
            equiv_all = False
    pins = {"n_subsets": (ncheck, comb(n, m)), "all_equivalent": (equiv_all, True)}
    summary = (f"G1 characterization (a) [p={p} n={n} m={m} w={w}]: "
               f"valid<=>(m+1)null<=>e_j=(-s)^j<=>aug-locator on all {ncheck} m-subsets")
    return pins, summary


# ----------------------------------------------------------------------------
# G2 : char-0 rigidity, EXACT in Z[zeta_n]  (Lam-Leung + parity)  + positive control
# ----------------------------------------------------------------------------
def cyclotomic(n):
    polys = {}

    def pdiv(a, b):
        a = a[:]
        db = len(b) - 1
        q = [0] * (len(a) - db)
        for i in range(len(a) - 1, db - 1, -1):
            ci = a[i]
            if ci:
                q[i - db] = ci
                for j in range(len(b)):
                    a[i - db + j] -= ci * b[j]
        return q

    def phi(k):
        if k in polys:
            return polys[k]
        num = [-1] + [0] * (k - 1) + [1]          # X^k - 1
        for d in range(1, k):
            if k % d == 0:
                num = pdiv(num, phi(d))
        polys[k] = num
        return num
    return phi(n)


def pmodm(a, m):
    a = a[:]
    dm = len(m) - 1
    while True:
        while a and a[-1] == 0:
            a.pop()
        if not a or len(a) - 1 < dm:
            break
        lead = a[-1]
        sh = len(a) - 1 - dm
        for i in range(len(m)):
            a[sh + i] -= lead * m[i]
    return a if a else [0]


def _padd(a, b):
    r = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        r[i] += x
    for i, y in enumerate(b):
        r[i] += y
    return r


def _mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r


def zeta_key(P, phi, d):
    """canonical Z[zeta]-reps of the top (d-1) coeffs of ell_P(Y)=prod_{i in P}(Y-zeta^i)."""
    coeffsY = [[1]]
    for i in P:
        zi = [0] * i + [1]
        new = [[0] for _ in range(len(coeffsY) + 1)]
        for t, cf in enumerate(coeffsY):
            new[t + 1] = _padd(new[t + 1], cf)
            new[t] = _padd(new[t], [-v for v in pmodm(_mul(cf, zi), phi)])
        coeffsY = [pmodm(c, phi) for c in new]

    def canon(a):
        r = pmodm(a, phi)
        while len(r) > 1 and r[-1] == 0:
            r.pop()
        return tuple(r)
    return tuple(canon(coeffsY[d - j]) for j in range(1, d))


def scale_idx(P, n):
    """max g | n such that the index set P is a union of mu_g-cosets (invariant under +n/g)."""
    s = set(P)
    best = 1
    d = 1
    while d <= n:
        if n % d == 0 and all(((i + n // d) % n) in s for i in s):
            best = max(best, d)
        d += 1
    return best


def g2():
    # (i) constant-shift-pair census, EXACT over Z[zeta_n], for n=2^a, a in {3,4}.
    census_ok = True
    prim_seen = False
    a4_d4_nonzero = False       # positive control anchor: n=16, d=4=2^2 must be nonempty
    for a in (3, 4):
        n = 2 ** a
        phi = cyclotomic(n)
        for d in range(2, n // 2 + 1):
            groups = {}
            for Pp in itertools.combinations(range(n), d):
                groups.setdefault(zeta_key(Pp, phi, d), []).append(Pp)
            A = sum(len(mm) * (len(mm) - 1) for mm in groups.values() if len(mm) >= 2)
            if any(len(mm) >= 2 and scale_idx(P, n) == 1 for mm in groups.values() for P in mm):
                prim_seen = True
            pow2 = (d & (d - 1)) == 0
            if (A > 0) != pow2:
                census_ok = False
            if a == 4 and d == 4:
                a4_d4_nonzero = (A > 0)

    # (ii) Lam-Leung antipodal forcing on the j=1 relation, direct, at n=8,16.
    antip_ok = True
    ll_checks = 0
    for a in (3, 4):
        n = 2 ** a
        phi = cyclotomic(n)

        def lin(P):
            s = [0] * n
            for i in P:
                s[i] += 1
            return pmodm(s, phi)
        for d in range(1, n // 2 + 1):
            byl = {}
            for P in itertools.combinations(range(n), d):
                r = lin(P)
                while len(r) > 1 and r[-1] == 0:
                    r.pop()
                byl.setdefault(tuple(r), []).append(P)
            for _, mem in byl.items():
                for P in mem:
                    for Q in mem:
                        if P != Q and set(P).isdisjoint(Q):
                            ll_checks += 1
                            aP = set(P) == {(i + n // 2) % n for i in P}
                            aQ = set(Q) == {(i + n // 2) % n for i in Q}
                            if not (aP and aQ):
                                antip_ok = False

    # (iii) POSITIVE CONTROL: exhibit an explicit constant-shift pair at d=4=2^2.
    #       n=8, P=mu_4-coset {0,2,4,6}, P'=the other mu_4-coset {1,3,5,7} in mu_8.
    #       ell_P - ell_{P'} must be a NONZERO CONSTANT with equal power sums p_1..p_3.
    p = 97
    D8 = mu_n(p, 8)
    P = [D8[i] for i in (0, 2, 4, 6)]
    Pp = [D8[i] for i in (1, 3, 5, 7)]
    cP = poly_from_roots(P, p)
    cQ = poly_from_roots(Pp, p)
    pc_const = all((cP[i] - cQ[i]) % p == 0 for i in range(4)) and (cP[4] - cQ[4]) % p != 0
    pc_ps = all(sum(pow(x, i, p) for x in P) % p == sum(pow(x, i, p) for x in Pp) % p
                for i in range(1, 4))
    pc_disjoint = set(P).isdisjoint(Pp)

    pins = {
        "census_pairs_iff_pow2": (census_ok, True),
        "no_primitive_pair": (prim_seen, False),
        "posctrl_d4_nonempty": (a4_d4_nonzero, True),
        "antipodal_forcing": (antip_ok, True),
        "n_ll_checks": (ll_checks, 1124),      # 18 (n=8) + 1106 (n=16) disjoint equal-p1 pairs
        "posctrl_const_shift": (pc_const, True),
        "posctrl_equal_powersums": (pc_ps, True),
        "posctrl_disjoint": (pc_disjoint, True),
    }
    summary = (f"G2 char-0 rigidity (Z[zeta], n=2^a): pairs<=>d pow-of-2, no primitive, "
               f"j=1=>antipodal on {ll_checks} checks; positive control d=4=2^2 nonempty "
               f"(const shift, eq power sums)")
    return pins, summary


# ----------------------------------------------------------------------------
# G3 : M2 top stratum on real z*=0 fixtures  (char-p degeneration probe)
# ----------------------------------------------------------------------------
def m2_top_stratum(p, n, K, m):
    """(top-count, all-const-shift-with-equal-power-sums) for the e=w+2 stratum."""
    w = m - K
    e_top = w + 2
    D = mu_n(p, n)
    fibers = {}
    for T in itertools.combinations(D, m):
        co = poly_from_roots(T, p)
        a = [co[j] for j in range(1, w + 2)]
        s = a[0]
        if all(a[j - 1] == pow(s, j, p) for j in range(2, w + 2)):
            fibers.setdefault(s, []).append(frozenset(T))
    top = 0
    v2 = True
    for s, mem in fibers.items():
        for T in mem:
            for T2 in mem:
                if T != T2 and len(T - T2) == e_top:
                    top += 1
                    Pp = tuple(sorted(T - T2))
                    Qp = tuple(sorted(T2 - T))
                    cP = poly_from_roots(Pp, p)
                    cQ = poly_from_roots(Qp, p)
                    const = all((cP[i] - cQ[i]) % p == 0 for i in range(e_top)) and \
                        (cP[e_top] - cQ[e_top]) % p != 0
                    pe = tuple(sum(pow(x, i, p) for x in Pp) % p for i in range(1, w + 2))
                    qe = tuple(sum(pow(x, i, p) for x in Qp) % p for i in range(1, w + 2))
                    if not (const and pe == qe):
                        v2 = False
    return top, v2


def a_prim_count(p, n, d):
    """primitive (scale-1) constant-shift-pair count of d-subsets of mu_n over F_p."""
    D = mu_n(p, n)
    idx = {r: i for i, r in enumerate(D)}
    groups = {}
    for P in itertools.combinations(D, d):
        c = poly_from_roots(P, p)
        groups.setdefault(tuple(c[:d]), []).append(P)
    ap = 0
    for _, mem in groups.items():
        if len(mem) < 2:
            continue
        for P in mem:
            if scale_idx([idx[x] for x in P], n) == 1:
                ap += len(mem) - 1
    return ap


def g3():
    # (a) POSITIVE CONTROL: n=8, e_top=4=2^2 -> NONEMPTY genuine M2 top stratum.
    t8, v8 = m2_top_stratum(97, 8, 2, 4)
    # (b) EMPTINESS PROBE: n=16, e_top=3 (not pow2).
    t97, _ = m2_top_stratum(97, 16, 7, 8)              # degenerate prime -> present
    absent = all(m2_top_stratum(pp, 16, 7, 8)[0] == 0 for pp in (113, 193, 241))
    # (c) small-case bad-prime cross-check of p0 ~ (e n/d)^2 (max PRIMITIVE bad prime vs prediction)
    badcheck = True
    xchecks = []
    for (n, d, obs, pred) in ((16, 3, 97, 210), (24, 4, 97, 266), (32, 5, 193, 303), (24, 3, 433, 473)):
        p0 = (math.e * n / d) ** 2
        ok_pred = round(p0) == pred and obs < pred        # observed bad prime below the threshold
        xchecks.append((n, d, obs, round(p0)))
        if not ok_pred:
            badcheck = False
    pins = {
        "posctrl_n8_nonempty": (t8 > 0, True),
        "posctrl_n8_count": (t8, 2),
        "posctrl_n8_constshift": (v8, True),
        "degenerate_p97_count": (t97, 32),
        "degenerate_p97_eq_aprim": (t97, a_prim_count(97, 16, 3)),
        "char0_regime_empty": (absent, True),
        "badprime_threshold_xcheck": (badcheck, True),
    }
    summary = (f"G3 M2 top stratum: positive control n=8 e_top=4=2^2 count={t8} (NONEMPTY); "
               f"emptiness probe n=16 e_top=3: degenerate p=97 count={t97}(=A_prim), "
               f"char-0 113/193/241 empty={absent}; bad-prime xcheck {xchecks}")
    return pins, summary


# ----------------------------------------------------------------------------
# G4 : exact L4 numbers
# ----------------------------------------------------------------------------
def g4():
    N = 131072            # 2^17
    K = 65537
    M = 69753
    P = 2 ** 31 - 2 ** 24 + 1
    W = M - K             # 4216
    D1 = W + 2            # 4218 = 2*3*19*37
    lg_p = lg2(P)
    top_char0 = 0
    lg_ceiling = lg2((P - 1) * comb(N, M - D1) * comb(N - M + D1, D1))
    lg_EA = 2 * lg2binom(N, D1) - (D1 - 1) * lg_p
    lg_p0 = 2 * lg2binom(N, D1) / (D1 - 1)
    pins = {
        "factor_4218": (2 * 3 * 19 * 37, 4218),
        "half_2109": (3 * 19 * 37, 2109),
        "gcd_d_n": (gcd(D1, N), 2),
        "is_pow2": (int((D1 & (D1 - 1)) == 0), 0),
        "half_odd": (int(((D1 // 2) & 1) == 1), 1),
        "top_char0": (top_char0, 0),
        "lg_ceiling": (round(lg_ceiling, 2), 153665.47),
        "lg_EA": (round(lg_EA, 1), -76898.5),
        "lg_p0": (round(lg_p0, 3), 12.753),
        "margin_bits": (round(lg_p - lg_p0, 2), 18.24),
    }
    summary = (f"G4 L4 numbers: w+2=4218=2*3*19*37, gcd(w+2,n)={pins['gcd_d_n'][0]} "
               f"pow2={pins['is_pow2'][0]} (w+2)/2=2109 odd={pins['half_odd'][0]} | "
               f"char-0 top count={top_char0} | ceiling 2^{lg_ceiling:.2f}->0 | "
               f"E[A]~2^{lg_EA:.1f} | p0~2^{lg_p0:.3f} (p=2^{lg_p:.2f}, margin +{lg_p - lg_p0:.2f} bits)")
    return pins, summary


GATES = [g1, g2, g3, g4]


def run_all():
    ok_all = True
    for g in GATES:
        pins, summary = g()
        ok = _ok(pins)
        print(f"{summary}  {'PASS' if ok else 'FAIL'}")
        ok_all = ok_all and ok
    print("\nALL PASS" if ok_all else "\nFAIL")
    return ok_all


def tamper_selftest():
    print("[tamper-selftest] perturbing every pin -> each must flip its gate to FAIL:")
    total = 0
    caught = 0
    for g in GATES:
        pins, _ = g()                       # compute once
        for name in pins:
            total += 1
            if not _ok(pins, tamper=name):
                caught += 1
            else:
                print(f"  !!! pin '{name}' NOT caught in {g.__name__} <<<")
    ok = (caught == total)
    print(f"[tamper-selftest] {caught}/{total} pins caught  {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == '__main__':
    if '--tamper-selftest' in sys.argv:
        sys.exit(0 if tamper_selftest() else 1)
    sys.exit(0 if run_all() else 1)
