#!/usr/bin/env python3
"""Verifier for A3 (good reduction of W_h's torsion structure) and the
(A) closure assembly arithmetic.

Sections
  S1  quasi-homogeneity of the obstructions O_j at h = 3, 4 (symbolic)
  S2  Lemma 0 graph/triangularity at h = 3, 4 (symbolic)
  S3  Lemma 1 norm facts at n = 16 (exact resultants)
  S4  end-to-end A3 mechanism at (n,h) = (16,3):
        - Lemma 2 integrality of 2^(4h-2) O_j at all anchored supports
        - char-0 emptiness (X24 instance: no (16,3)-candidates over K)
        - per-prime exceptional test == brute-force row trades,
          for all rows q = p <= 700 (p = 1 mod 16) and the extension
          rows q = p^2, p in {7, 23}
  S5  anchored/orbit accounting identity  #T * 2h = n * #anchored
  S6  budget arithmetic against banked QA.22 / W4 certificates

Light compute only (the heavy per-window pilot runs elsewhere).
"""

import itertools
import json
import os
import sys
from fractions import Fraction

import sympy as sp

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "a3-good-reduction",
    "a3_good_reduction.json",
)

PASS = []
FAIL = []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    status = "PASS" if ok else "FAIL"
    msg = f"[{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


# ----------------------------------------------------------------------
# shared symbolic machinery: the x83 recursion in coefficient space
# ----------------------------------------------------------------------

def forced_square_root(h, c):
    """c: dict j -> coeff of X^j of monic C, deg 2h. Returns s: dict of
    S's coefficients (s[h] = 1) via the x83 division-by-2 recursion."""
    s = {h: sp.Integer(1)}
    for j in range(h - 1, -1, -1):
        # [X^(h+j)] S^2 = sum_{a+b=h+j, 0<=a,b<=h} s_a s_b ; only s_j unknown
        known = sp.Integer(0)
        for a in range(j + 1, h + 1):
            b = h + j - a
            if 0 <= b <= h and b > j:
                known += s[a] * s[b]
        # the unknown appears as 2 s_j s_h = 2 s_j (min index = j iff max = h)
        s[j] = sp.expand((c[h + j] - known) / 2)
    return s


def obstructions(h, c):
    """Returns (O dict j->expr for 1<=j<=h-1, lam expr, s dict)."""
    s = forced_square_root(h, c)
    out = {}
    for j in range(0, h):
        sq = sp.Integer(0)
        for a in range(0, h + 1):
            b = j - a
            if 0 <= b <= h:
                sq += s[a] * s[b]
        out[j] = sp.expand(sq - c[j])
    lam = out.pop(0)
    return out, lam, s


def section_1_and_2():
    for h in (3, 4):
        c = {j: sp.Symbol(f"c{j}") for j in range(2 * h)}
        gam = sp.Symbol("gamma")
        O, lam, s = obstructions(h, c)

        # S1: quasi-homogeneity O_j(gamma.R) = gamma^(2h-j) O_j(R),
        # where c_j has weight 2h - j.
        subs = {c[j]: gam ** (2 * h - j) * c[j] for j in range(2 * h)}
        ok = True
        for j in range(1, h):
            lhs = sp.expand(O[j].subs(subs))
            rhs = sp.expand(gam ** (2 * h - j) * O[j])
            if sp.expand(lhs - rhs) != 0:
                ok = False
        lam_ok = sp.expand(lam.subs(subs) - gam ** (2 * h) * lam) == 0
        check(f"S1 h={h} quasi-homogeneity of O_j (weights 2h-j) and lambda (2h)",
              ok and lam_ok)

        # S2: graph structure O_j = P_j(c_h..c_{2h-1}) - c_j
        ok = True
        for j in range(1, h):
            for i in range(0, h):
                d = sp.diff(O[j], c[i])
                want = sp.Integer(-1) if i == j else sp.Integer(0)
                if sp.simplify(d - want) != 0:
                    ok = False
        # and the forced s_j depend only on high coefficients
        for j in range(0, h):
            for i in range(0, h):
                if sp.diff(s[j], c[i]) != 0:
                    ok = False
        check(f"S2 h={h} triangular graph: dO_j/dc_i = -delta_ij (i<h), "
              f"s_* free of low c", ok)


# ----------------------------------------------------------------------
# exact arithmetic in Z[zeta_16] (basis 1..y^7, y^8 = -1)
# ----------------------------------------------------------------------

DEG = 8  # [Q(zeta_16):Q]


def zmul(a, b):
    out = [Fraction(0)] * DEG
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            k = i + j
            if k >= DEG:
                out[k - DEG] -= ai * bj
            else:
                out[k] += ai * bj
    return out


def zadd(a, b):
    return [x + y for x, y in zip(a, b)]


def zsub(a, b):
    return [x - y for x, y in zip(a, b)]


def zscale(a, r):
    return [x * r for x in a]


def zeta_pow(k):
    """zeta_16^k as a basis vector."""
    k %= 16
    v = [Fraction(0)] * DEG
    if k < DEG:
        v[k] = Fraction(1)
    else:
        v[k - DEG] = Fraction(-1)
    return v


ZERO = [Fraction(0)] * DEG
ONE = zeta_pow(0)


def poly_from_roots(exps):
    """Locator C(X) = prod (X - zeta^e), coefficients as ring vectors,
    returned as list coeffs[0..deg]."""
    coeffs = [ONE[:]]  # constant poly 1
    for e in exps:
        r = zeta_pow(e)
        new = [ZERO[:] for _ in range(len(coeffs) + 1)]
        for i, ci in enumerate(coeffs):
            new[i + 1] = zadd(new[i + 1], ci)          # X * ci
            new[i] = zsub(new[i], zmul(r, ci))          # -r * ci
        coeffs = new
    return coeffs


def obstruction_vectors_16_3(exps):
    """(n,h) = (16,3): supports = 6 exponents in Z/16.  Returns
    (O1, O2, lam) as ring vectors (Fractions), from the recursion."""
    C = poly_from_roots(exps)  # degree 6, C[6] = 1
    c = {j: C[j] for j in range(6)}
    half = Fraction(1, 2)
    s2 = zscale(c[5], half)
    s1 = zscale(zsub(c[4], zmul(s2, s2)), half)
    s0 = zscale(zsub(c[3], zscale(zmul(s2, s1), 2)), half)
    O2 = zsub(zadd(zmul(s1, s1), zscale(zmul(s2, s0), 2)), c[2])
    O1 = zsub(zscale(zmul(s1, s0), 2), c[1])
    lam = zsub(zmul(s0, s0), c[0])
    return O1, O2, lam


def section_3():
    # Lemma 1: norms of differences of distinct 16th roots of unity are
    # (up to sign) powers of 2.  Norm via Res_y(y^8 + 1, e(y)).
    y = sp.Symbol("y")
    phi = y ** 8 + 1
    ok = True
    for a in range(16):
        for b in range(a + 1, 16):
            e = zsub(zeta_pow(a), zeta_pow(b))
            ep = sum(int(coef) * y ** i for i, coef in enumerate(e))
            nm = sp.resultant(phi, ep)
            nm = int(nm)
            if nm == 0:
                ok = False
                break
            m = abs(nm)
            while m % 2 == 0:
                m //= 2
            if m != 1:
                ok = False
    check("S3 n=16 norms of zeta^a - zeta^b are nonzero powers of 2 "
          "(120 pairs)", ok)


# ----------------------------------------------------------------------
# S4/S5: end-to-end at (n,h) = (16,3)
# ----------------------------------------------------------------------

CLEAR = 2 ** 10  # 2^(4h-2), h = 3


def anchored_supports_16_3():
    for rest in itertools.combinations(range(1, 16), 5):
        yield (0,) + rest


def integral_cleared(v):
    out = []
    for x in v:
        y_ = x * CLEAR
        if y_.denominator != 1:
            return None
        out.append(int(y_))
    return out


class GF2:
    """F_{p^2} as a + b t, t^2 = d (d a nonresidue mod p)."""

    def __init__(self, p):
        self.p = p
        d = 2
        while pow(d, (p - 1) // 2, p) != p - 1:
            d += 1
        self.d = d

    def mul(self, x, y_):
        p, d = self.p, self.d
        a, b = x
        c, e = y_
        return ((a * c + d * b * e) % p, (a * e + b * c) % p)

    def add(self, x, y_):
        p = self.p
        return ((x[0] + y_[0]) % p, (x[1] + y_[1]) % p)

    def sub(self, x, y_):
        p = self.p
        return ((x[0] - y_[0]) % p, (x[1] - y_[1]) % p)

    def pw(self, x, k):
        r = (1, 0)
        while k:
            if k & 1:
                r = self.mul(r, x)
            x = self.mul(x, x)
            k >>= 1
        return r

    def order16_element(self):
        p = self.p
        q = p * p
        for a in range(1, p):
            for b in range(1, p):
                x = self.pw((a, b), (q - 1) // 16)
                if self.pw(x, 8) != (1, 0) and self.pw(x, 16) == (1, 0):
                    return x
        raise RuntimeError("no order-16 element found")


def mu16_elements_prime(p):
    """Elements of order dividing 16 in F_p^*, p = 1 mod 16, as a list
    [w^0..w^15] for w of exact order 16."""
    for g in range(2, p):
        w = pow(g, (p - 1) // 16, p)
        if pow(w, 8, p) != 1 and pow(w, 16, p) == 1:
            return [pow(w, i, p) for i in range(16)]
    raise RuntimeError("no order-16 element")


def trades_16_3_prime_field(p):
    """All unordered h=3 trades {P,Q} in mu_16 subset F_p.  Returns
    (n_unordered, n_anchored) where anchored means 1 in P union Q."""
    M = mu16_elements_prime(p)
    return _trades_from_elems(M, one=1 % p,
                              mul=lambda a, b: a * b % p,
                              add=lambda a, b: (a + b) % p)


def trades_16_3_ext_field(p):
    F = GF2(p)
    w = F.order16_element()
    M = [F.pw(w, i) for i in range(16)]
    return _trades_from_elems(M, one=(1, 0), mul=F.mul, add=F.add)


def _trades_from_elems(M, one, mul, add):
    n_elems = len(M)
    triples = list(itertools.combinations(range(n_elems), 3))
    buckets = {}
    for t in triples:
        x, y_, z = M[t[0]], M[t[1]], M[t[2]]
        e1 = add(add(x, y_), z)
        e2 = add(add(mul(x, y_), mul(x, z)), mul(y_, z))
        buckets.setdefault((e1, e2), []).append(t)
    n_unordered = 0
    n_anchored = 0
    for key, ts in buckets.items():
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                if set(ts[i]).isdisjoint(ts[j]):
                    n_unordered += 1
                    support = set(ts[i]) | set(ts[j])
                    if 0 in support:  # M[0] = 1
                        n_anchored += 1
    return n_unordered, n_anchored


def section_4_and_5():
    # precompute cleared obstruction integer vectors at all anchored
    # supports; check Lemma 2 integrality and char-0 emptiness (X24).
    cleared = []  # (exps, O1int, O2int)
    integral_ok = True
    char0_candidates = 0
    for exps in anchored_supports_16_3():
        O1, O2, lam = obstruction_vectors_16_3(exps)
        i1 = integral_cleared(O1)
        i2 = integral_cleared(O2)
        if i1 is None or i2 is None:
            integral_ok = False
            continue
        if all(v == 0 for v in i1) and all(v == 0 for v in i2):
            char0_candidates += 1
        cleared.append((exps, i1, i2))
    check("S4 Lemma 2 integrality: 2^10 * O_j integral at all 3003 "
          "anchored supports", integral_ok)
    check("S4 X24 instance: zero char-0 (16,3)-candidates "
          "(h=3 not a 2-power)", char0_candidates == 0,
          f"candidates found: {char0_candidates}")

    def exceptional_prime_field(p):
        """p = 1 mod 16: exists (support, root w of y^8=-1 in F_p) with
        both cleared obstructions = 0 mod p."""
        roots = [w for w in range(1, p) if pow(w, 8, p) == p - 1]
        assert len(roots) == 8
        pows = {w: [pow(w, i, p) for i in range(DEG)] for w in roots}
        for exps, i1, i2 in cleared:
            v1 = [x % p for x in i1]
            v2 = [x % p for x in i2]
            for w in roots:
                pw = pows[w]
                if sum(a * b for a, b in zip(v1, pw)) % p == 0 and \
                   sum(a * b for a, b in zip(v2, pw)) % p == 0:
                    return True
        return False

    def exceptional_ext_field(p):
        """p odd with ord_16(p) = 2: same test with w of order 16 in
        F_{p^2} (roots of y^8 + 1 live there)."""
        F = GF2(p)
        w0 = F.order16_element()
        roots = [F.pw(w0, k) for k in range(1, 16, 2)]  # 8 primitive ones
        for exps, i1, i2 in cleared:
            for w in roots:
                pw = [(1, 0)]
                for _ in range(DEG - 1):
                    pw.append(F.mul(pw[-1], w))
                s1 = (0, 0)
                s2 = (0, 0)
                for a, b in zip(i1, pw):
                    s1 = F.add(s1, F.mul((a % p, 0), b))
                for a, b in zip(i2, pw):
                    s2 = F.add(s2, F.mul((a % p, 0), b))
                if s1 == (0, 0) and s2 == (0, 0):
                    return True
        return False

    primes_1mod16 = [17, 97, 113, 193, 241, 257, 337, 353, 401, 433,
                     449, 577, 593, 641, 673]
    all_match = True
    trade_rows = []
    for p in primes_1mod16:
        exc = exceptional_prime_field(p)
        n_un, n_anch = trades_16_3_prime_field(p)
        has = n_un > 0
        if exc != has:
            all_match = False
            print(f"  MISMATCH p={p}: exceptional={exc} trades={n_un}")
        if has:
            trade_rows.append((p, n_un, n_anch))
    check("S4 A3 biconditional at (16,3), rows q=p<=700: trades exist "
          "iff p exceptional", all_match,
          f"rows with trades: {[(p, u) for p, u, a in trade_rows]}")

    ext_match = True
    ext_detail = []
    for p in (7, 23):
        exc = exceptional_ext_field(p)
        n_un, n_anch = trades_16_3_ext_field(p)
        has = n_un > 0
        ext_detail.append((p, n_un, exc))
        if exc != has:
            ext_match = False
        if has:
            trade_rows.append((p, n_un, n_anch))
    check("S4 A3 biconditional at (16,3), extension rows q=p^2, "
          "p in {7,23} (care point iv)", ext_match,
          f"(p, trades, exceptional): {ext_detail}")

    # S5: orbit/anchor accounting  #T * 2h = n * #anchored, 2h=6, n=16
    acct_ok = len(trade_rows) > 0
    for p, n_un, n_anch in trade_rows:
        if n_un * 6 != 16 * n_anch:
            acct_ok = False
            print(f"  ACCOUNTING FAIL p={p}: {n_un}*6 != 16*{n_anch}")
    check("S5 anchored/orbit accounting #T*2h = n*#anchored on all "
          "trade-bearing rows", acct_ok,
          f"checked on {len(trade_rows)} rows")
    return {
        "anchored_supports": len(cleared),
        "char0_candidates": char0_candidates,
        "prime_trade_rows": [
            {"p": p, "unordered_trades": n_un, "anchored_trades": n_anch}
            for p, n_un, n_anch in trade_rows
            if p in primes_1mod16
        ],
        "extension_rows": [
            {"p": p, "unordered_trades": n_un, "exceptional": exc}
            for p, n_un, exc in ext_detail
        ],
        "all_trade_rows": [
            {"p": p, "unordered_trades": n_un, "anchored_trades": n_anch}
            for p, n_un, n_anch in trade_rows
        ],
    }


# ----------------------------------------------------------------------
# S6: assembly budget arithmetic against banked certificates
# ----------------------------------------------------------------------

def section_6():
    qa22_path = os.path.join(
        REPO, "experimental/data/certificates/qa22-staircase-budget/"
        "qa22_staircase_budget.json")
    w4_path = os.path.join(
        REPO, "experimental/data/certificates/w4-direct-column-rewiring/"
        "w4_direct_column_rewiring.json")
    qa22 = json.load(open(qa22_path))
    w4 = json.load(open(w4_path))

    ok = True
    for r in qa22["rows"]:
        if r["poly_16n3"] != 16 * r["n"] ** 3:
            ok = False
    check("S6 QA.22 poly column = 16 n^3 on all six rows", ok)

    ok = True
    rowc_rooms = []
    for r in w4["row_room"]:
        if r["direct_column_n3"] != r["n"] ** 3:
            ok = False
        if r["remaining_room"] != r["B_star"] - r["repaired_budget_total"]:
            ok = False
        if r["max_full_n3_columns_in_remaining_room"] < 1:
            ok = False
        if r["n"] == 1024:
            rowc_rooms.append(r["max_full_n3_columns_in_remaining_room"])
    check("S6 W4 direct column = n^3, room = B* - repaired, >= 1 column "
          "available on every row", ok,
          f"RowC spare n^3 columns: {min(rowc_rooms):.3e}" if rowc_rooms else "")

    # tolerance table: max uniform anchored multiplicity E per h with
    # sum_{h in window} (n/h) * E <= n^3  i.e.  E <= n^2 / sum(1/h)
    n = 1024
    table = {}
    for (t, hmax) in [(5, 20), (3, 20), (5, 100), (3, 100)]:
        hs = range(t + 1, hmax + 1)
        s = sum(Fraction(1, h) for h in hs)
        e_max = int(Fraction(n * n) / s)
        # verify by direct summation
        total = sum(Fraction(n, h) * e_max for h in hs)
        assert total <= n ** 3
        table[(t, hmax)] = e_max
    ok = all(v > 0 for v in table.values())
    check("S6 tolerance table: uniform anchored-extras bound per h "
          "within one n^3 column", ok,
          "; ".join(f"t={t},hmax={hm}: E<={v}" for (t, hm), v in
                    sorted(table.items())))

    # window sanity from the banked u2a numbers: RowC windows nonempty,
    # prize base-row windows empty (t huge)
    prize_t = {"1/4": 2 ** 33 + 1, "1/8": 2 ** 33 + 1, "1/16": 2 ** 32 + 1}
    prize_n = 2 ** 41
    ok = all(t + 1 > 2 * 41 and t + 1 > 41 ** 2 for t in prize_t.values())
    rowc_ok = (5 + 1 <= 20) and (3 + 1 <= 20)
    check("S6 windows: prize base rows empty at both 2 log2 n and "
          "(log2 n)^2; Row-C windows nonempty", ok and rowc_ok,
          f"prize t+1 = {min(prize_t.values()) + 1} > 1681 = (log2 n)^2")
    return {
        "qa22_row_count": len(qa22["rows"]),
        "rowc_min_spare_n3_columns": min(rowc_rooms),
        "tolerance": {
            f"t={t},hmax={hm}": v for (t, hm), v in sorted(table.items())
        },
        "prize_min_t_plus_1": min(prize_t.values()) + 1,
        "prize_log2n_squared": 41 ** 2,
    }


def section_7(s4, s6):
    cert = json.load(open(CERT))
    ok = (
        cert["node"] == "a3_good_reduction_lemma"
        and cert["status"] == "PROVED_WITH_CONDITIONAL_CONSUMER"
        and cert["toy"]["anchored_supports"] == s4["anchored_supports"]
        and cert["toy"]["char0_candidates"] == s4["char0_candidates"]
        and cert["toy"]["prime_trade_rows"] == s4["prime_trade_rows"]
        and cert["toy"]["extension_rows"] == s4["extension_rows"]
        and cert["budget"]["qa22_row_count"] == s6["qa22_row_count"]
        and cert["budget"]["rowc_min_spare_n3_columns"]
        == s6["rowc_min_spare_n3_columns"]
        and cert["budget"]["tolerance"] == s6["tolerance"]
        and cert["budget"]["prize_min_t_plus_1"] == s6["prize_min_t_plus_1"]
        and cert["budget"]["prize_log2n_squared"] == s6["prize_log2n_squared"]
    )
    check("S7 pinned A3 certificate matches toy mechanism and budget constants", ok)


def main():
    print("== A3 good-reduction verifier ==")
    section_1_and_2()
    section_3()
    s4 = section_4_and_5()
    s6 = section_6()
    section_7(s4, s6)
    print(f"\n{len(PASS)} PASS, {len(FAIL)} FAIL")
    if FAIL:
        for f in FAIL:
            print(f"  FAILED: {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
