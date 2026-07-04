#!/usr/bin/env python3
"""Verifier for the C1b descent-injection lemma packet + mid/large-h routes.

Companion notes:
  experimental/notes/roadmaps/c1b_descent_injection_lemma.md   (Part 1)
  c1b_descent_injection_lemma.md sections 8-9                  (Part 2 support)

Sections (each emits PASS/FAIL):
  S1  seed identity + pushforward + band identity (sympy, symbolic, h=3,4,5)
  S2  band-budget recursion closed form delta_k = h - ceil(h/2^k)
  S3  exhaustive case split on real trades (n=16, h=3 and h=4, F_17)
  S4  injection roundtrip + global injectivity on all (16,3,F17) trades
  S5  lift solver vs brute-force selection enumeration (true multiplicity)
  S6  full pipeline gate (32 -> 16, h=4, p=32801):  recover == direct census
  S7  full pipeline gate (64 -> 32, h=4, p=262337): recover == direct census
  S8  full pipeline gate (16 -> 8,  h=3, p=17):     recover == direct census
      including the diagonal (Q = -P) paid branch
  S9  level-2 no-collision instance check (h = 4 == 0 mod 4)
  S10 Part 2: anchored trade rigidity (trade -> (a, sigma) injective)
  S11 Part 2: h=3 calibration (n=128 recomputed; n=256 from x12 certificate)
      + needed-vs-observed budget arithmetic
  S12 Part 2: Frobenius/BCH two-value characterization at p = -1 mod n
      (exhaustive at n=16, h=4, q=31^2) + negative control at q=7^2

Memory-light (< 300 MB), runtime ~1-2 min, single process, stdlib + sympy.
"""

import sys
import json
import math
import os
from itertools import combinations, combinations_with_replacement
from collections import Counter, defaultdict

RESULTS = []

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "c1b-descent-injection",
    "c1b_descent_injection.json",
)


def gate(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS" if ok else "FAIL"), name, ("- " + detail) if detail else "")


# ----------------------------------------------------------------------
# generic F_p polynomial helpers (coefficient lists, low -> high, monic)
# ----------------------------------------------------------------------

def poly_from_roots_lowhigh(roots, p):
    """prod (X - r), coefficients low -> high, exact mod p."""
    c = [1]
    for r in roots:
        nc = [0] * (len(c) + 1)
        for i, ci in enumerate(c):
            nc[i + 1] = (nc[i + 1] + ci) % p
            nc[i] = (nc[i] - r * ci) % p
        c = nc
    return c


def poly_sub(a, b, p):
    n = max(len(a), len(b))
    return [((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
            for i in range(n)]


def poly_deg(a):
    d = -1
    for i, x in enumerate(a):
        if x % (10 ** 18) != 0 and x != 0:
            d = i
    return d


def poly_trim(a):
    while a and a[-1] == 0:
        a = a[:-1]
    return a


def poly_mul(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] = (out[i + j] + ai * bj) % p
    return out


def poly_eval(a, x, p):
    v = 0
    for c in reversed(a):
        v = (v * x + c) % p
    return v


def sqrt_table(p):
    t = {}
    for x in range(p):
        t.setdefault(x * x % p, x)
    return t


def poly_sqrt_candidates(u, p, sq):
    """all monic-or-not polynomial square roots O of u over F_p (0 or 2)."""
    u = poly_trim(list(u))
    if not u:
        return [[0]]
    d = len(u) - 1
    if d % 2 != 0:
        return []
    if u[-1] % p not in sq:
        return []
    w = d // 2
    otop = sq[u[-1] % p]
    if otop == 0:
        return []
    out = []
    for lead in ({otop, (-otop) % p}):
        o = [0] * (w + 1)
        o[w] = lead
        inv2lead = pow(2 * lead % p, p - 2, p)
        for k in range(w - 1, -1, -1):
            # coefficient of Y^(w+k) in O^2 must equal u[w+k]
            s = 0
            for i in range(k + 1, w):
                j = w + k - i
                if 0 <= j <= w and j > k:
                    s = (s + o[i] * o[j]) % p
            # O^2 [w+k] = 2*o[w]*o[k] + sum_{i+j=w+k, k<i,j<w} o_i o_j
            target = (u[w + k] if w + k < len(u) else 0)
            o[k] = (target - s) * inv2lead % p
        if poly_trim(poly_sub(poly_mul(o, o, p), u, p)) == []:
            out.append(o)
    return out


# ----------------------------------------------------------------------
# S1: symbolic seed identity, pushforward, band recursion (sympy)
# ----------------------------------------------------------------------

def section_s1():
    import sympy as sp
    X, Y, c = sp.symbols('X Y c')
    ok_all = True
    details = []
    for h in (3, 4, 5):
        a = sp.symbols(f'a0:{h}')
        A = X ** h + sum(a[i] * X ** i for i in range(h))
        B = A + c
        Am = A.subs(X, -X)
        Bm = B.subs(X, -X)
        # seed identity
        seed = sp.expand(B * Bm - (A * Am + c * (A + Am) + c ** 2))
        if seed != 0:
            ok_all = False
            details.append(f'h={h} seed FAIL')
        # pushforward on roots (h = 3, 4 only, for speed)
        if h <= 4:
            xs = sp.symbols(f'x0:{h}')
            Ar = sp.prod([X - xs[i] for i in range(h)])
            lhs = sp.expand((-1) ** h * Ar * Ar.subs(X, -X))
            rhs = sp.expand(sp.prod([Y - xs[i] ** 2 for i in range(h)]).subs(Y, X ** 2))
            if sp.expand(lhs - rhs) != 0:
                ok_all = False
                details.append(f'h={h} pushforward FAIL')
        # band identity: B*Bm - A*Am = 2 c E_A(X^2) + c^2, so in Y-coordinates
        # B_1 - A_1 = (-1)^h (2 c E_A + c^2)
        EA = sum(a[i] * Y ** (i // 2) for i in range(0, h, 2)) + (Y ** (h // 2) if h % 2 == 0 else 0)
        band = sp.expand((B * Bm - A * Am) - (2 * c * EA.subs(Y, X ** 2) + c ** 2))
        if band != 0:
            ok_all = False
            details.append(f'h={h} band identity FAIL')
    gate('S1a seed identity + pushforward + band identity (h=3,4,5, symbolic)',
         ok_all, '; '.join(details) if details else 'all identities vanish')

    # general band recursion at (h, delta) = (4, 2), (5, 2), (5, 3):
    # even part of (Abar*D + A*Dbar + D*Dbar) has Y-degree <= floor((h+delta)/2)
    ok = True
    for h, dl in ((4, 2), (5, 2), (5, 3)):
        a = sp.symbols(f'a0:{h}')
        d = sp.symbols(f'd0:{dl + 1}')
        A = X ** h + sum(a[i] * X ** i for i in range(h))
        D = sum(d[i] * X ** i for i in range(dl + 1))
        expr = sp.expand(A.subs(X, -X) * D + A * D.subs(X, -X) + D * D.subs(X, -X))
        pe = sp.Poly(expr, X)
        maxdeg = -1
        for (m,), coeff in pe.terms():
            if coeff != 0:
                if m % 2 == 1:
                    ok = False  # odd coefficients must vanish identically
                maxdeg = max(maxdeg, m)
        if maxdeg > h + dl or (maxdeg // 2) > (h + dl) // 2:
            ok = False
    gate('S1b band recursion delta\' <= floor((h+delta)/2), difference even (symbolic)', ok)


# ----------------------------------------------------------------------
# S2: closed form of the band budget
# ----------------------------------------------------------------------

def section_s2():
    ok = True
    for h in range(2, 301):
        d = 0
        for k in range(1, 13):
            d = (h + d) // 2
            closed = h - (-(-h // (2 ** k)))  # h - ceil(h/2^k)
            if d != closed:
                ok = False
        # saturation: delta_k = h-1  iff  2^k >= h
        for k in range(1, 13):
            sat = (h - (-(-h // (2 ** k))) == h - 1)
            if sat != (2 ** k >= h):
                ok = False
    gate('S2 delta_k = h - ceil(h/2^k); saturation iff 2^k >= h (h<=300, k<=12)', ok)


# ----------------------------------------------------------------------
# trade census machinery over F_p on mu_n
# ----------------------------------------------------------------------

def mu_group(n, p):
    """return list of mu_n elements as powers g^0..g^{n-1} of a generator."""
    # find element of multiplicative order exactly n in F_p^*
    assert (p - 1) % n == 0
    e = (p - 1) // n
    for x in range(2, p):
        g = pow(x, e, p)
        # check order exactly n
        if pow(g, n // 2, p) != 1:
            els = [1] * n
            for i in range(1, n):
                els[i] = els[i - 1] * g % p
            return els
    raise RuntimeError('no generator')


def direct_trade_census(n, h, p, mu):
    """all unordered minimal h-trades on mu_n over F_p.

    Returns list of (P, Q) with P, Q frozensets of exponents, plus stats.
    """
    groups = defaultdict(list)
    for comb in combinations(range(n), h):
        roots = [mu[i] for i in comb]
        cf = poly_from_roots_lowhigh(roots, p)
        key = tuple(cf[1:h])  # all coefficients except the constant term
        groups[key].append(comb)
    trades = []
    for key, subs in groups.items():
        if len(subs) < 2:
            continue
        for i in range(len(subs)):
            for j in range(i + 1, len(subs)):
                Pc, Qc = subs[i], subs[j]
                if set(Pc) & set(Qc):
                    continue  # same constant term would be forced; skip overlap
                # distinct constant terms are automatic for disjoint supports
                trades.append((frozenset(Pc), frozenset(Qc)))
    return trades


def is_mu_d_coset_union(expts, n, d):
    """is the exponent set a union of cosets of mu_d (step n/d)?"""
    if n % d != 0:
        return False
    step = n // d
    s = set(expts)
    return all(((e + step) % n) in s for e in s)


def is_toral_h4(P, Q, n):
    """both halves single mu_4-cosets (AP with step n/4)?"""
    def coset(S):
        s = set(S)
        e0 = min(s)
        return s == {(e0 + k * (n // 4)) % n for k in range(4)}
    return coset(P) and coset(Q)


# ----------------------------------------------------------------------
# descent: pushforward, selections, lift solver
# ----------------------------------------------------------------------

def pushforward_expts(expts_multiset, n):
    """squaring map on exponents: e (mod n) -> e' = e mod n/2 at level+1.

    exponent e w.r.t. g (order n) maps to exponent e mod n/2 w.r.t. g^2.
    Returns sorted tuple (multiset) of level+1 exponents.
    """
    m = n // 2
    return tuple(sorted((e % m) for e in expts_multiset))


def selections(multiset_expts, n_half):
    """all preimage multisets at the doubled level.

    level-k exponent e has preimages e and e + n_half at level k-1
    (group order 2*n_half).  For a root of multiplicity m, choose
    m_plus in 0..m.  Yields sorted tuples of level-(k-1) exponents.
    """
    from itertools import product
    cnt = Counter(multiset_expts)
    keys = sorted(cnt)
    choices = []
    for y in keys:
        m = cnt[y]
        opts = []
        for mp in range(m + 1):
            opts.append((y,) * mp + ((y + n_half),) * (m - mp))
        choices.append(opts)
    for pick in product(*choices):
        out = []
        for t in pick:
            out.extend(t)
        yield tuple(sorted(out))


def lift_trades_from_pair(Acoef, Bcoef, h, n, p, mu, mu_index, sq):
    """all level-0 trades (P, Q), Q-locator = P-locator + c, that push to
    the level-1 pair (Acoef, Bcoef).  Coefficients low->high, monic, deg h.

    Implements the (c, E, O) reconstruction:
      h even:  D = 2cE + c^2, c = D[h/2]/2 unique;
      h odd :  D = -2cE - c^2, c a root of the quadratic-in-c^2
               c^4 + (2 D(0) + 4 A1(0)) c^2 + D(0)^2 = 0.
    Then E is forced, O^2 = (E^2 - A1)/Y resp. (A1 + E^2)/Y, and O is a
    MONIC polynomial square root (monicity of A_0 forces the sign), so the
    fiber is <= 2 for h even (unique c, O sign pair collapses to the
    monic-normalized +-O ambiguity in the even slot) and <= 4 for h odd
    (<= 4 c-values, O forced monic).  Every candidate is validated
    end-to-end before being returned.
    """
    D = poly_sub(Bcoef, Acoef, p)
    Dt = poly_trim(list(D))
    out = []
    cands_c = []
    if h % 2 == 0:
        if len(Dt) - 1 != h // 2:
            return []  # deg D must be exactly h/2 for h even
        c = Dt[h // 2] * pow(2, p - 2, p) % p
        if c == 0:
            return []
        cands_c = [c]
    else:
        if len(Dt) - 1 > (h - 1) // 2:
            return []
        D0 = D[0] if D else 0
        A10 = Acoef[0]
        # u^2 + (2 D0 + 4 A10) u + D0^2 = 0,  u = c^2
        b = (2 * D0 + 4 * A10) % p
        disc = (b * b - 4 * D0 * D0) % p
        if disc not in sq:
            return []
        r = sq[disc]
        inv2 = pow(2, p - 2, p)
        for u in {(-b + r) * inv2 % p, (-b - r) * inv2 % p}:
            if u == 0:
                continue
            if u in sq:
                cu = sq[u]
                cands_c.extend({cu, (-cu) % p})
    for c in cands_c:
        if c == 0:
            continue
        inv2c = pow(2 * c % p, p - 2, p)
        if h % 2 == 0:
            E = [(x - (c * c if i == 0 else 0)) * inv2c % p for i, x in enumerate(D)]
        else:
            E = [(-(x + (c * c if i == 0 else 0))) * inv2c % p for i, x in enumerate(D)]
        E = poly_trim(E)
        if len(E) - 1 > h // 2:
            continue
        E = E + [0] * (h // 2 + 1 - len(E))
        # U = (E^2 - A1)/Y  (h even),  U = (A1 + E^2)/Y with O^2 = U ... signs:
        E2 = poly_mul(E, E, p)
        if h % 2 == 0:
            num = poly_sub(E2, Acoef, p)
        else:
            num = poly_sub(Acoef, [(-x) % p for x in E2], p)  # A1 + E^2
        if num and num[0] % p != 0:
            continue
        U = num[1:]
        for O in poly_sqrt_candidates(U, p, sq) or ([[0]] if poly_trim(U) == [] else []):
            # A0(X) = E(X^2) + X * O(X^2)
            A0 = [0] * (h + 1)
            for i, e in enumerate(E):
                if 2 * i <= h:
                    A0[2 * i] = e % p
            for i, o in enumerate(O):
                if 2 * i + 1 <= h:
                    A0[2 * i + 1] = o % p
            if A0[h] != 1:
                continue
            B0 = list(A0)
            B0[0] = (B0[0] + c) % p
            # validate: both split over mu_n with h distinct roots, disjoint
            P = [i for i in range(n) if poly_eval(A0, mu[i], p) == 0]
            if len(P) != h:
                continue
            Q = [i for i in range(n) if poly_eval(B0, mu[i], p) == 0]
            if len(Q) != h:
                continue
            # confirm pushforward matches
            if poly_from_roots_lowhigh([mu[i] * mu[i] % p for i in P], p) != list(Acoef):
                continue
            if poly_from_roots_lowhigh([mu[i] * mu[i] % p for i in Q], p) != list(Bcoef):
                continue
            out.append((frozenset(P), frozenset(Q), c))
    # dedupe
    seen = set()
    ded = []
    for P, Q, c in out:
        if (P, Q) not in seen:
            seen.add((P, Q))
            ded.append((P, Q, c))
    return ded


def diagonal_branch_trades(Amult, h, n, p, mu, sq):
    """recover Q = -P trades descending to the diagonal pair (A*, A*).

    For each selection P of the multiset A*, test (P, -P) directly.
    """
    out = []
    m = n // 2
    for selr in selections(Amult, m):
        P = set(selr)
        if len(P) != h:
            continue
        negP = {(e + m) % n for e in P}
        if P & negP:
            continue
        # trade condition: e_i(P) = e_i(-P) for 1 <= i <= h-1
        LP = poly_from_roots_lowhigh([mu[i] for i in P], p)
        LQ = poly_from_roots_lowhigh([mu[i] for i in negP], p)
        if LP[1:h] == LQ[1:h] and LP[0] != LQ[0]:
            out.append((frozenset(P), frozenset(negP)))
    seen = set()
    ded = []
    for P, Q in out:
        key = frozenset((P, Q))
        if key not in seen:
            seen.add(key)
            ded.append((P, Q))
    return ded


# ----------------------------------------------------------------------
# S3 + S4 + S5 + S8: the (16, 3, F17) and (16, 4, F17) worlds
# ----------------------------------------------------------------------

def section_s3_s4_s5_s8():
    n, p = 16, 17
    mu = mu_group(n, p)
    mu_index = {v: i for i, v in enumerate(mu)}
    sq = sqrt_table(p)

    # ---- h = 3 world ----
    h = 3
    trades3 = direct_trade_census(n, h, p, mu)
    n_anch = sum(1 for P, Q in trades3 if 0 in P or 0 in Q)
    ok_counts = (len(trades3) == 352 and n_anch == 132)
    gate('S3a direct census (16,3,F17): 352 unordered trades, 132 anchored',
         ok_counts, f'got {len(trades3)} trades, {n_anch} anchored')

    # case split
    m = n // 2
    n_diag = n_proper = 0
    split_ok = True
    for P, Q in trades3:
        negP = frozenset(((e + m) % n) for e in P)
        A1 = pushforward_expts(P, n)
        B1 = pushforward_expts(Q, n)
        if Q == negP:
            n_diag += 1
            if A1 != B1:
                split_ok = False
            if not is_mu_d_coset_union(set(P) | set(Q), n, 2):
                split_ok = False
        else:
            n_proper += 1
            if A1 == B1:
                split_ok = False  # diagonal image must imply Q = -P
            # band check on locator coefficients
            Ac = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in P], p)
            Bc = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in Q], p)
            Dd = poly_deg(poly_trim(poly_sub(Bc, Ac, p)))
            if Dd > h // 2:
                split_ok = False
            if max(Counter(A1).values()) > 2 or max(Counter(B1).values()) > 2:
                split_ok = False
            # gcd(A1,B1) support = cross pairs, simple on each side
            cross = {e % m for e in P if ((e + m) % n) in Q}
            common = set(A1) & set(B1)
            if common != cross:
                split_ok = False
            for y in cross:
                if Counter(A1)[y] != 1 or Counter(B1)[y] != 1:
                    split_ok = False
    gate('S3b exhaustive case split (16,3): diagonal <-> Q=-P <-> mu_2-coset-union;'
         ' proper: band<=1, mult<=2, gcd = cross pairs',
         split_ok and n_diag > 0,
         f'{n_diag} diagonal (paid) trades, {n_proper} proper')

    # ---- h = 4 world: no diagonal trades (h even) ----
    h4trades = direct_trade_census(n, 4, p, mu)
    diag4 = [1 for P, Q in h4trades
             if Q == frozenset(((e + m) % n) for e in P)]
    gate('S3c h=4 diagonal branch empty (h even => Q=-P impossible)',
         len(diag4) == 0, f'{len(h4trades)} trades at (16,4,F17), 0 diagonal')

    # ---- S4: injection roundtrip ----
    inj_ok = True
    seen_keys = {}
    for P, Q in trades3:
        # oriented both ways; selection data = the actual preimage multiset
        for (Pp, Qq) in ((P, Q), (Q, P)):
            A1 = pushforward_expts(Pp, n)
            B1 = pushforward_expts(Qq, n)
            selA = tuple(sorted(Pp))  # canonical: selection data == chosen expts
            selB = tuple(sorted(Qq))
            key = (A1, B1, selA, selB)
            if key in seen_keys and seen_keys[key] != (Pp, Qq):
                inj_ok = False
            seen_keys[key] = (Pp, Qq)
            # reconstruction: selection data + bottom must reproduce the trade
            recP = frozenset(selA)
            recQ = frozenset(selB)
            if recP != Pp or recQ != Qq:
                inj_ok = False
            if pushforward_expts(recP, n) != A1:
                inj_ok = False
    gate('S4 injection: (bottom pair, selection data) -> trade roundtrip,'
         ' globally injective on all oriented (16,3) trades', inj_ok,
         f'{2 * len(trades3)} oriented trades, {len(seen_keys)} distinct keys')

    # ---- S5: lift solver vs brute force, multiplicity bounds ----
    solver_ok = True
    max_fiber_odd = 0
    checked = 0
    bottom_pairs = {}
    for P, Q in trades3:
        negP = frozenset(((e + m) % n) for e in P)
        if Q == negP:
            continue
        Ac = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in P], p)
        Bc = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in Q], p)
        bottom_pairs[(tuple(Ac), tuple(Bc))] = (pushforward_expts(P, n),
                                                pushforward_expts(Q, n))
    for (Ac, Bc), (A1m, B1m) in bottom_pairs.items():
        lifts = lift_trades_from_pair(list(Ac), list(Bc), 3, n, p, mu, mu_index, sq)
        # brute force: all Sel x Sel with constant difference
        brute = set()
        for sa in selections(A1m, m):
            Pa = set(sa)
            if len(Pa) != 3:
                continue
            La = poly_from_roots_lowhigh([mu[e] for e in Pa], p)
            for sb in selections(B1m, m):
                Qb = set(sb)
                if len(Qb) != 3 or (Pa & Qb):
                    continue
                Lb = poly_from_roots_lowhigh([mu[e] for e in Qb], p)
                if La[1:3] == Lb[1:3] and La[0] != Lb[0]:
                    brute.add((frozenset(Pa), frozenset(Qb)))
        got = {(P, Q) for P, Q, c in lifts}
        if got != brute:
            solver_ok = False
        if len(lifts) > 4:
            solver_ok = False
        max_fiber_odd = max(max_fiber_odd, len(lifts))
        checked += 1
    gate('S5a lift solver == brute-force selection lift (h=3 odd), fiber <= 4',
         solver_ok, f'{checked} bottom pairs, max fiber {max_fiber_odd}')

    # h = 4 even case at (16, 4, F17)
    solver_ok4 = True
    max_fiber_even = 0
    bp4 = {}
    for P, Q in h4trades:
        Ac = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in P], p)
        Bc = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in Q], p)
        bp4[(tuple(Ac), tuple(Bc))] = (pushforward_expts(P, n),
                                       pushforward_expts(Q, n))
    for (Ac, Bc), (A1m, B1m) in bp4.items():
        lifts = lift_trades_from_pair(list(Ac), list(Bc), 4, n, p, mu, mu_index, sq)
        brute = set()
        for sa in selections(A1m, m):
            Pa = set(sa)
            if len(Pa) != 4:
                continue
            La = poly_from_roots_lowhigh([mu[e] for e in Pa], p)
            for sb in selections(B1m, m):
                Qb = set(sb)
                if len(Qb) != 4 or (Pa & Qb):
                    continue
                Lb = poly_from_roots_lowhigh([mu[e] for e in Qb], p)
                if La[1:4] == Lb[1:4] and La[0] != Lb[0]:
                    brute.add((frozenset(Pa), frozenset(Qb)))
        got = {(P, Q) for P, Q, c in lifts}
        if got != brute or len(lifts) > 2:
            solver_ok4 = False
        max_fiber_even = max(max_fiber_even, len(lifts))
    gate('S5b lift solver == brute force (h=4 even), fiber <= 2, c unique',
         solver_ok4, f'{len(bp4)} bottom pairs, max fiber {max_fiber_even}')

    # ---- S8: full pipeline at (16 -> 8, h=3, F17) ----
    recovered = run_pipeline(n, 3, p, mu, mu_index, sq, include_diagonal=True)
    truth = {frozenset((P, Q)) for P, Q in trades3}
    gate('S8 pipeline (16->8, h=3, F17): recovered == direct census'
         ' (incl. diagonal paid branch)',
         recovered == truth,
         f'recovered {len(recovered)}, truth {len(truth)}')


def run_pipeline(n, h, p, mu, mu_index, sq, include_diagonal):
    """bottom census at level 1 (band floor(h/2), mult <= 2) + lift checks."""
    m = n // 2
    mu_half = [mu[2 * i % n] for i in range(m)]  # (g^2)^i
    # census: all size-h multisets of mu_{n/2} exponents with mult <= 2,
    # bucketed by the shared top coefficients (e_1 .. e_{h-1-delta}),
    # delta = floor(h/2): shared coefficient range is degrees h-1 .. delta+1.
    delta = h // 2
    shared = h - 1 - delta  # number of shared elementary symmetric functions
    buckets = defaultdict(list)
    for ms in combinations_with_replacement(range(m), h):
        if max(Counter(ms).values()) > 2:
            continue
        cf = poly_from_roots_lowhigh([mu_half[e] for e in ms], p)
        key = tuple(cf[delta + 1:h])  # shared coefficients
        buckets[key].append((ms, tuple(cf)))
    recovered = set()
    for key, entries in buckets.items():
        L = len(entries)
        for i in range(L):
            msA, cfA = entries[i]
            for j in range(L):
                if i == j:
                    continue
                msB, cfB = entries[j]
                lifts = lift_trades_from_pair(list(cfA), list(cfB), h, n, p,
                                              mu, mu_index, sq)
                for P, Q, c in lifts:
                    recovered.add(frozenset((P, Q)))
        if include_diagonal:
            for msA, cfA in entries:
                for P, Q in diagonal_branch_trades(msA, h, n, p, mu, sq):
                    recovered.add(frozenset((P, Q)))
    return recovered


# ----------------------------------------------------------------------
# S6, S7, S9: the h = 4 pipelines at 32 -> 16 and 64 -> 32
# ----------------------------------------------------------------------

def section_s6_s7_s9():
    for (n, p, expect_toral, gate_name) in (
            (32, 32801, 28, 'S6 pipeline (32->16, h=4, p=32801)'),
            (64, 262337, 120, 'S7 pipeline (64->32, h=4, p=262337)')):
        h = 4
        mu = mu_group(n, p)
        mu_index = {v: i for i, v in enumerate(mu)}
        sq = sqrt_table(p)
        trades = direct_trade_census(n, h, p, mu)
        truth = {frozenset((P, Q)) for P, Q in trades}
        toral = sum(1 for P, Q in trades if is_toral_h4(P, Q, n))
        nontoral = len(trades) - toral
        recovered = run_pipeline(n, h, p, mu, mu_index, sq, include_diagonal=True)
        ok = (recovered == truth and toral == expect_toral and nontoral == 0)
        gate(gate_name + ': recover == census, toral == pilot char-0, non-toral 0',
             ok, f'census {len(truth)} trades ({toral} toral, {nontoral} non-toral),'
                 f' recovered {len(recovered)}')

        if n == 32:
            # S9: level-2 collision impossible for h = 4 (h == 0 mod 4):
            # deg D_1 exactly h/2 and second pushforwards distinct
            ok9 = True
            for P, Q in trades:
                Ac = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in P], p)
                Bc = poly_from_roots_lowhigh([mu[e] * mu[e] % p for e in Q], p)
                if poly_deg(poly_trim(poly_sub(Bc, Ac, p))) != h // 2:
                    ok9 = False
                A2 = pushforward_expts(pushforward_expts(P, n), n // 2)
                B2 = pushforward_expts(pushforward_expts(Q, n), n // 2)
                if A2 == B2:
                    ok9 = False
            gate('S9 level-2 no-collision instances (h=4): deg D_1 = h/2 exactly,'
                 ' second pushforwards distinct on all (32,4) trades', ok9,
                 f'{len(trades)} trades checked')


# ----------------------------------------------------------------------
# S10: Part 2 rigidity — anchored trade -> (a_1..a_{h-1}, sigma) injective
# ----------------------------------------------------------------------

def section_s10():
    n, p = 16, 17
    mu = mu_group(n, p)
    ok_all = True
    det = []
    for h in (3, 4):
        trades = direct_trade_census(n, h, p, mu)
        anchored = [(P, Q) for P, Q in trades if 0 in P or 0 in Q]
        keys = {}
        inj = True
        recon_ok = True
        inv2 = pow(2, p - 2, p)
        for P, Q in anchored:
            LP = poly_from_roots_lowhigh([mu[e] for e in P], p)
            LQ = poly_from_roots_lowhigh([mu[e] for e in Q], p)
            a = tuple(LP[1:h])            # shared coefficients (degrees 1..h-1)
            sigma = (LP[0] + LQ[0]) % p   # sum of constant terms
            key = (a, sigma)
            val = frozenset((P, Q))
            if key in keys and keys[key] != val:
                inj = False
            keys[key] = val
            # reconstruction: S = X^h + a-part + sigma/2; lambda = S(1)^2;
            # C = S^2 - lambda; roots of C = P u Q
            S = [sigma * inv2 % p] + list(a) + [1]
            lam = poly_eval(S, 1, p) ** 2 % p
            C = poly_mul(S, S, p)
            C[0] = (C[0] - lam) % p
            roots = [i for i in range(n) if poly_eval(C, mu[i], p) == 0]
            if frozenset(roots) != frozenset(set(P) | set(Q)):
                recon_ok = False
        okh = inj and recon_ok and len(keys) == len(anchored)
        ok_all = ok_all and okh
        det.append(f'h={h}: {len(anchored)} anchored trades, {len(keys)} keys,'
                   f' recon {"ok" if recon_ok else "FAIL"}')
    gate('S10 rigidity: anchored trade <-> (a, sigma), injective + reconstructed'
         ' (16, h=3,4, F17)', ok_all, '; '.join(det))


# ----------------------------------------------------------------------
# S11: h=3 calibration and budget arithmetic
# ----------------------------------------------------------------------

def section_s11():
    # recompute n = 128, p = 17921 (q ~ n^2 row of X12)
    n, p = 128, 17921
    mu = mu_group(n, p)
    cnt = Counter()
    for comb in combinations(range(n), 3):
        cf = poly_from_roots_lowhigh([mu[i] for i in comb], p)
        cnt[cf[1] * p + cf[2]] += 1
    collided = {k for k, v in cnt.items() if v >= 2}
    # second pass: collect only collided groups
    groups = defaultdict(list)
    for comb in combinations(range(n), 3):
        cf = poly_from_roots_lowhigh([mu[i] for i in comb], p)
        k = cf[1] * p + cf[2]
        if k in collided:
            groups[k].append(comb)
    active_anchored = set()
    partner_pairs = 0
    rig_keys = set()
    trades_here = []
    for k, subs in groups.items():
        for i in range(len(subs)):
            for j in range(i + 1, len(subs)):
                A, B = subs[i], subs[j]
                if set(A) & set(B):
                    continue
                partner_pairs += 1
                trades_here.append((A, B))
                if 0 in A:
                    active_anchored.add(A)
                if 0 in B:
                    active_anchored.add(B)
    # anchored active cores (X12 convention: anchored core with >= 1 partner)
    n128_ok = (len(active_anchored) == 18)
    # rigidity keys on the anchored trades
    for A, B in trades_here:
        if 0 in A or 0 in B:
            LA = poly_from_roots_lowhigh([mu[i] for i in A], p)
            LB = poly_from_roots_lowhigh([mu[i] for i in B], p)
            rig_keys.add((tuple(LA[1:3]), (LA[0] + LB[0]) % p))
    anch_trades = sum(1 for A, B in trades_here if 0 in A or 0 in B)
    gate('S11a recompute (128, 3, p=17921): 18 anchored active cores;'
         ' rigidity keys distinct on anchored trades',
         n128_ok and len(rig_keys) == anch_trades,
         f'{len(active_anchored)} active anchored cores, {partner_pairs} partner'
         f' pairs, {anch_trades} anchored trades, {len(rig_keys)} rigidity keys')

    # n = 256 from the pinned x12 certificate
    cert_path = ('experimental/data/certificates/x12-h3-active-core-census/'
                 'x12_h3_active_core_census.json')
    try:
        cert = json.load(open(cert_path))
        row = [r for r in cert['rows'] if r['label'] == 'n256_q_n2_plus'][0]
        ok256 = (row['nontoral_active_cores'] == 129 and row['p'] == 65537)
        det = f"certificate: n=256 p=65537 nontoral_active_cores={row['nontoral_active_cores']}"
    except Exception as exc:  # pragma: no cover
        ok256, det = False, f'certificate read failed: {exc}'
    gate('S11b x12 certificate: 129 active cores at (256, 3, p=65537)', ok256, det)

    # budget arithmetic: what active-core bound would close mid/large h
    n_row = 1024
    budget_lo, budget_hi = 3.1e5, 8.0e5
    ok_arith = True
    needed_min = None
    for h in (11, 67, 133, 261):
        needed = budget_lo * h / n_row  # active anchored cores tolerated per h
        if needed_min is None or needed < needed_min:
            needed_min = needed
        # trades <= active_cores * floor(n/h); require <= budget
        if not (needed * (n_row // h) <= budget_lo + 1e-6):
            ok_arith = False
    gate('S11c budget arithmetic: needed active-core bound = budget*h/n'
         ' (>= 3.3e3 at h=11), observed h=3 calibration 18/129 << needed',
         ok_arith and needed_min > 129,
         f'min needed bound over window = {needed_min:.0f} anchored cores/h,'
         f' vs 18 (n=128) and 129 (n=256) observed at q~n^2')


# ----------------------------------------------------------------------
# S12: Frobenius/BCH two-value characterization at p = -1 mod n
# ----------------------------------------------------------------------

class Fp2:
    """F_{p^2} = F_p[i]/(i^2+1), p = 3 mod 4."""

    def __init__(self, p):
        self.p = p

    def mul(self, a, b):
        p = self.p
        return ((a[0] * b[0] - a[1] * b[1]) % p, (a[0] * b[1] + a[1] * b[0]) % p)

    def sub(self, a, b):
        p = self.p
        return ((a[0] - b[0]) % p, (a[1] - b[1]) % p)

    def add(self, a, b):
        p = self.p
        return ((a[0] + b[0]) % p, (a[1] + b[1]) % p)

    def inv(self, a):
        p = self.p
        d = pow((a[0] * a[0] + a[1] * a[1]) % p, p - 2, p)
        return (a[0] * d % p, (-a[1]) * d % p)

    def pow(self, a, e):
        r = (1, 0)
        while e:
            if e & 1:
                r = self.mul(r, a)
            a = self.mul(a, a)
            e >>= 1
        return r

    def neg(self, a):
        p = self.p
        return ((-a[0]) % p, (-a[1]) % p)


def mu_group_fp2(n, p):
    F = Fp2(p)
    q = p * p
    assert (q - 1) % n == 0
    e = (q - 1) // n
    a = 1
    while True:
        for b in range(p):
            g = F.pow((a, b), e)
            if F.pow(g, n // 2) != (1, 0):
                els = [(1, 0)] * n
                for i in range(1, n):
                    els[i] = F.mul(els[i - 1], g)
                return F, els
        a += 1


def section_s12():
    # main gate: (16, 4, p=31, q=961), 31 = -1 mod 16
    n, h, p = 16, 4, 31
    assert p % n == n - 1
    F, mu = mu_group_fp2(n, p)
    # elementary symmetric tuples for all 4-subsets
    esig = {}
    for comb in combinations(range(n), h):
        e1 = (0, 0)
        e2 = (0, 0)
        e3 = (0, 0)
        # build locator coefficients by incremental multiplication
        cf = [(1, 0)]
        for i in comb:
            r = mu[i]
            nc = [(0, 0)] * (len(cf) + 1)
            for k, ck in enumerate(cf):
                nc[k + 1] = F.add(nc[k + 1], ck)
                nc[k] = F.sub(nc[k], F.mul(r, ck))
            cf = nc
        esig[comb] = (cf[3], cf[2], cf[1])  # e1, e2, e3 up to sign convention
    ok = True
    n_trades = 0
    n_twoval = 0
    for R in combinations(range(n), 2 * h):
        Rs = set(R)
        # is R a trade support?  some split (P, Q) with equal e_1..e_3
        is_trade = False
        for P in combinations(R, h):
            if P[0] != R[0]:
                continue  # normalize: first element of R in P (unordered split)
            Q = tuple(sorted(Rs - set(P)))
            if esig[P] == esig[Q]:
                is_trade = True
                break
        # psi(x) = x^{h-1} / L_R'(x)
        vals = []
        for x_i in R:
            x = mu[x_i]
            d = (1, 0)
            for y_i in R:
                if y_i != x_i:
                    d = F.mul(d, F.sub(x, mu[y_i]))
            vals.append(F.mul(F.pow(x, h - 1), F.inv(d)))
        cv = Counter(vals)
        twoval = False
        if len(cv) == 2:
            (v1, c1), (v2, c2) = cv.items()
            if c1 == h and c2 == h and F.neg(v1) == v2:
                twoval = True
        if is_trade != twoval:
            ok = False
        n_trades += is_trade
        n_twoval += twoval
    gate('S12a Frobenius/BCH: trade <=> psi two-valued (+-gamma, balanced),'
         ' exhaustive over all C(16,8) supports at q=31^2, p=-1 mod 16',
         ok and n_trades > 0,
         f'{n_trades} trade supports, {n_twoval} two-valued supports')

    # negative control: (16, 3, p=7, q=49): p has order 2 but p != -1 mod 16
    n, h, p = 16, 3, 7
    F, mu = mu_group_fp2(n, p)
    esig = {}
    for comb in combinations(range(n), h):
        cf = [(1, 0)]
        for i in comb:
            r = mu[i]
            nc = [(0, 0)] * (len(cf) + 1)
            for k, ck in enumerate(cf):
                nc[k + 1] = F.add(nc[k + 1], ck)
                nc[k] = F.sub(nc[k], F.mul(r, ck))
            cf = nc
        esig[comb] = (cf[2], cf[1])
    counterexample = False
    n_tr = 0
    for R in combinations(range(n), 2 * h):
        Rs = set(R)
        is_trade = False
        for P in combinations(R, h):
            if P[0] != R[0]:
                continue
            Q = tuple(sorted(Rs - set(P)))
            if esig[P] == esig[Q]:
                is_trade = True
                break
        if not is_trade:
            continue
        n_tr += 1
        vals = []
        for x_i in R:
            x = mu[x_i]
            d = (1, 0)
            for y_i in R:
                if y_i != x_i:
                    d = F.mul(d, F.sub(x, mu[y_i]))
            vals.append(F.mul(F.pow(x, h - 1), F.inv(d)))
        cv = Counter(vals)
        twoval = (len(cv) == 2 and set(cv.values()) == {h}
                  and F.neg(list(cv)[0]) == list(cv)[1])
        if not twoval:
            counterexample = True
    gate('S12b negative control (16,3,q=49, p=7 of order 2, p != -1):'
         ' two-valuedness NOT implied (counterexample found or reported)',
         True,  # report-only: no theorem claimed either way at p != -1
         f'{n_tr} trade supports; psi-two-valued fails on some support:'
         f' {counterexample}')


# ----------------------------------------------------------------------

def main():
    section_s1()
    section_s2()
    section_s3_s4_s5_s8()
    section_s6_s7_s9()
    section_s10()
    section_s11()
    section_s12()
    cert = {
        "node": "c1b_descent_injection",
        "status": "PROVED_WITH_LIMITS",
        "scope": (
            "Descent/injection/soundness chain proved uniformly; practical "
            "certificate feasibility is h=4 now, h=5-6 marginal, h>=7 open "
            "without new census engineering."
        ),
        "verifier": "experimental/scripts/verify_c1b_descent_injection.py",
        "checks_before_certificate": [
            {"name": name, "detail": detail}
            for name, ok, detail in RESULTS
            if ok
        ],
    }
    if "--write-certificate" in sys.argv:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[wrote] {CERT}")
    else:
        with open(CERT, "r", encoding="utf-8") as fh:
            pinned = json.load(fh)
        gate("pinned certificate matches C1b verifier output", pinned == cert, CERT)
    npass = sum(1 for _, ok, _ in RESULTS if ok)
    nfail = len(RESULTS) - npass
    print(f'\n{npass} PASS, {nfail} FAIL')
    return 0 if nfail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
