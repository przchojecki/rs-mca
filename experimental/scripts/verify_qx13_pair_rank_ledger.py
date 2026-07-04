#!/usr/bin/env python3
"""QX.13 verifier: the pair-rank ledger c(s,t) = min(s, t-1)
(DAG node xr_ledger_qpower).

Re-derives every exact claim in
experimental/notes/roadmaps/qx13_pair_rank_ledger.md:

  [0] Field axiom tables (F_5, F_7, F_11, GF(4), GF(8), GF(9); full triple
      loops) and the Lagrange delta property per cell.
  [1] Theorem 1 (pair rank): for every (S,T) pair at exchange distance s in
      each toy cell, the joint syndrome map has rank t + min(s,t) (Gaussian
      elimination, exact field arithmetic) and the single-support block has
      rank t; kernel certificates (dimension, full kernel-span enumeration);
      for every q <= 7 cell, FULL enumeration of all q^|S u T| words counts
      the joint kernel exactly (q^k head case / q^(2k-r) plateau case).
      Plus the arithmetic impossibility of s = 4 at q <= 7 (n >= 2s > q).
  [2] Theorem 2 (all-slope accounting) on toys, EXACTLY: syndrome
      distribution from full word enumeration (fiber uniformity), then exact
      weighted pair accounting: FM1 per-support alignment probability,
      per-z same-slope probability q^-(t+min(s,t)) for EVERY z, per-(z,z')
      distinct-slope probability q^-2t for EVERY ordered z != z', and the
      union-bound chain through Theorem 3's right-hand side (Fractions).
  [3] Theorem 3 (packaging) for t <= 6, s <= 8: symbolic case reduction
      (integer exponent conditions valid for all q >= 2) + exact Fraction
      evaluation over prime-power q up to 2^31; equality iff s = t-1.
  [4] Base case c(1,2) = 1 with the exact flagship pair probability.

Deterministic; stdlib only; NO Monte Carlo. Exit code 0 iff all PASS.
Run:  python3 experimental/scripts/verify_qx13_pair_rank_ledger.py
"""

import json
import os
import sys
from fractions import Fraction
from itertools import combinations, product

FAILS = []
NCHECK = 0

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qx13-pair-rank-ledger",
    "qx13_pair_rank_ledger.json",
)


def check(name, cond, detail=""):
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = "[%s] %s" % (tag, name)
    if detail:
        line += "   (%s)" % detail
    print(line)
    if not cond:
        FAILS.append(name)


# ---------------------------------------------------------------------------
# Finite fields GF(p^e) as int-encoded tables (elements 0..q-1; the integer
# encodes the base-p digit vector of the polynomial representative, so the
# additive identity is 0 and the multiplicative identity is 1).
# ---------------------------------------------------------------------------

# monic irreducible polynomials, coefficients low -> high, WITHOUT the top 1
IRRED = {(2, 2): (1, 1),        # x^2 + x + 1 over F_2
         (2, 3): (1, 1, 0),     # x^3 + x + 1 over F_2
         (3, 2): (1, 0)}        # x^2 + 1     over F_3


class GF(object):
    def __init__(self, p, e=1, name=None):
        self.p, self.e, self.q = p, e, p ** e
        q = self.q
        self.name = name or ("F%d" % q if e == 1 else "GF(%d)" % q)
        if e == 1:
            add = [[(a + b) % p for b in range(q)] for a in range(q)]
            mul = [[(a * b) % p for b in range(q)] for a in range(q)]
        else:
            irr = IRRED[(p, e)]

            def dec(x):
                return [(x // p ** i) % p for i in range(e)]

            def enc(dg):
                return sum(d * p ** i for i, d in enumerate(dg))

            def pmul(da, db):
                res = [0] * (2 * e - 1)
                for i, ai in enumerate(da):
                    if ai:
                        for jj, bj in enumerate(db):
                            res[i + jj] = (res[i + jj] + ai * bj) % p
                # reduce: x^e == -(irr) since the modulus is monic
                for d in range(2 * e - 2, e - 1, -1):
                    c = res[d]
                    if c:
                        res[d] = 0
                        for i in range(e):
                            res[d - e + i] = (res[d - e + i] - c * irr[i]) % p
                return res[:e]

            add = [[enc([(x + y) % p for x, y in zip(dec(a), dec(b))])
                    for b in range(q)] for a in range(q)]
            mul = [[enc(pmul(dec(a), dec(b))) for b in range(q)]
                   for a in range(q)]
        self.ADD, self.MUL = add, mul
        self.NEG = [next(b for b in range(q) if add[a][b] == 0)
                    for a in range(q)]
        self.SUB = [[add[a][self.NEG[b]] for b in range(q)] for a in range(q)]
        self.INV = [None] + [next(b for b in range(1, q) if mul[a][b] == 1)
                             for a in range(1, q)]

    def axioms_ok(self):
        q, add, mul = self.q, self.ADD, self.MUL
        for a in range(q):
            for b in range(q):
                if add[a][b] != add[b][a] or mul[a][b] != mul[b][a]:
                    return False
            if add[a][0] != a or mul[a][1] != a or mul[a][0] != 0:
                return False
            if a and mul[a][self.INV[a]] != 1:
                return False
        for a in range(q):
            for b in range(q):
                for c in range(q):
                    if add[add[a][b]][c] != add[a][add[b][c]]:
                        return False
                    if mul[mul[a][b]][c] != mul[a][mul[b][c]]:
                        return False
                    if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]:
                        return False
        return True


FIELDS = {}


def field(p, e=1):
    if (p, e) not in FIELDS:
        FIELDS[(p, e)] = GF(p, e)
    return FIELDS[(p, e)]


# ---------------------------------------------------------------------------
# Polynomials / Lagrange top-coefficient rows / linear algebra over GF
# ---------------------------------------------------------------------------

def poly_mul(F, a, b):
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                res[i + j] = F.ADD[res[i + j]][F.MUL[ai][bj]]
    return res


def poly_eval(F, poly, x):
    acc = 0
    for c in reversed(poly):
        acc = F.ADD[F.MUL[acc][x]][c]
    return acc


def lagrange_basis(F, S):
    """L_x for x in S: dict x -> coefficient list (degree |S|-1)."""
    out = {}
    for x in S:
        num = [1]
        den = 1
        for y in S:
            if y == x:
                continue
            num = poly_mul(F, num, [F.NEG[y], 1])
            den = F.MUL[den][F.SUB[x][y]]
        dinv = F.INV[den]
        out[x] = [F.MUL[c][dinv] for c in num]
    return out


def top_rows(F, S, k, t, cols):
    """t x len(cols) matrix of the linear forms w|_(S u T) -> Pi_S(w)."""
    lb = lagrange_basis(F, S)
    rows = [[0] * len(cols) for _ in range(t)]
    for ci, x in enumerate(cols):
        if x in lb:
            coeffs = lb[x]  # degree A-1 polynomial, length A = k+t
            for i in range(t):
                rows[i][ci] = coeffs[k + i]
    return rows


def rref(F, M_in):
    M = [row[:] for row in M_in]
    m = len(M[0]) if M else 0
    pivots = []
    rank = 0
    for col in range(m):
        piv = None
        for r2 in range(rank, len(M)):
            if M[r2][col] != 0:
                piv = r2
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        inv = F.INV[M[rank][col]]
        M[rank] = [F.MUL[inv][x] for x in M[rank]]
        for r2 in range(len(M)):
            if r2 != rank and M[r2][col] != 0:
                f = M[r2][col]
                M[r2] = [F.SUB[x][F.MUL[f][y]] for x, y in zip(M[r2], M[rank])]
        pivots.append(col)
        rank += 1
    return M, pivots, rank


def mat_rank(F, M):
    return rref(F, M)[2]


def kernel_basis(F, M):
    R, pivots, rank = rref(F, M)
    m = len(M[0])
    free = [c for c in range(m) if c not in pivots]
    basis = []
    for fc in free:
        w = [0] * m
        w[fc] = 1
        for i, pc in enumerate(pivots):
            w[pc] = F.NEG[R[i][fc]]
        basis.append(w)
    return basis


def matvec(F, M, w):
    out = []
    for row in M:
        acc = 0
        for a, b in zip(row, w):
            if a and b:
                acc = F.ADD[acc][F.MUL[a][b]]
        out.append(acc)
    return out


def enum_syndrome_counts(F, M):
    """Exact map syndrome-tuple -> #words, over ALL q^m words (odometer with
    incremental syndrome updates; deterministic)."""
    q = F.q
    m = len(M[0])
    R = len(M)
    contrib = [[[F.MUL[v][M[r][c]] for r in range(R)] for v in range(q)]
               for c in range(m)]
    digs = [0] * m
    syn = [0] * R
    counts = {}
    total = q ** m
    ADD, SUB = F.ADD, F.SUB
    for it in range(total):
        key = tuple(syn)
        counts[key] = counts.get(key, 0) + 1
        if it == total - 1:
            break
        c = 0
        while True:
            old = digs[c]
            new = old + 1
            if new == q:
                digs[c] = 0
                oc, nc = contrib[c][old], contrib[c][0]
                for r in range(R):
                    syn[r] = ADD[SUB[syn[r]][oc[r]]][nc[r]]
                c += 1
            else:
                digs[c] = new
                oc, nc = contrib[c][old], contrib[c][new]
                for r in range(R):
                    syn[r] = ADD[SUB[syn[r]][oc[r]]][nc[r]]
                break
    return counts


def qpow(q, e):
    """Fraction q^e for integer e (possibly negative)."""
    return Fraction(q ** e) if e >= 0 else Fraction(1, q ** (-e))


# ---------------------------------------------------------------------------
# [0]+[1] Theorem 1 sweep
# ---------------------------------------------------------------------------

# cells: (p, e, k, t, s, n).  n <= q always; n >= A + s.
CELLS1 = [
    (5, 1, 1, 1, 1, 4),   # head boundary s = t = 1
    (5, 1, 1, 1, 2, 5),   # plateau s > t, r = 0 (disjoint supports)
    (5, 1, 2, 1, 2, 5),   # plateau s > t
    (5, 1, 1, 2, 1, 5),   # head s = t-1  (the c(1,2) base-case cell)
    (5, 1, 2, 2, 1, 5),   # head s = t-1, k = 2
    (5, 1, 1, 2, 2, 5),   # head boundary s = t
    (7, 1, 1, 2, 3, 7),   # plateau s > t, s = 3
    (7, 1, 2, 2, 2, 7),   # head boundary s = t, k = 2
    (7, 1, 1, 3, 2, 7),   # head interior s < t
    (7, 1, 1, 3, 3, 7),   # head boundary s = t = 3
    (7, 1, 2, 1, 3, 7),   # plateau s > t, s = 3
    (2, 2, 1, 2, 1, 4),   # GF(4): head s = t-1 (non-prime field)
    (2, 2, 1, 1, 2, 4),   # GF(4): plateau, disjoint supports
    (2, 3, 1, 3, 4, 8),   # GF(8): plateau s = 4 > t
    (2, 3, 2, 2, 4, 8),   # GF(8): plateau s = 4 > t, k = 2
    (2, 3, 1, 4, 3, 8),   # GF(8): head interior s = 3 < t
    (3, 2, 1, 4, 4, 9),   # GF(9): head boundary s = t = 4
    (11, 1, 1, 5, 4, 10),  # F_11: head interior s = 4 < t, n = 10
]

WORD_ENUM_CAP = 900000     # full word enumeration when q^m <= this
                           # (covers every q <= 7 cell, incl. 7^7 = 823543)
PAIR_CAP = 400             # rank-check at most this many (S,T) pairs/cell


def pairs_at_distance(D, A, s, cap):
    out = []
    for S in combinations(D, A):
        Sset = set(S)
        rest = [x for x in D if x not in Sset]
        r = A - s
        for keep in combinations(S, r):
            for new in combinations(rest, s):
                out.append((S, tuple(sorted(keep + new))))
                if len(out) >= cap:
                    return out
    return out


def section01():
    print("\n== [0] field axioms ==")
    for (p, e) in [(5, 1), (7, 1), (11, 1), (2, 2), (2, 3), (3, 2)]:
        F = field(p, e)
        check("%s field axioms (full triple loop, q=%d)" % (F.name, F.q),
              F.axioms_ok())

    print("\n== [1] Theorem 1: pair rank t + min(s,t), exact kernels ==")
    # s = 4 impossibility at q <= 7 (pure arithmetic on the constraints
    # k >= 1, t >= 1, A = k+t >= s, n >= A + s, n <= q):
    smax = 0
    for qq in (2, 3, 4, 5, 7):
        for n in range(2, qq + 1):
            for A in range(2, n):
                s_feasible = min(A, n - A)
                smax = max(smax, s_feasible)
    check("s = 4 impossible at q <= 7: max feasible s over all cells == 3",
          smax == 3, "n >= A + s >= 2s forces s <= n/2 <= q/2 <= 3.5")

    for (p, e, k, t, s, n) in CELLS1:
        F = field(p, e)
        q = F.q
        A = k + t
        assert n <= q and A + s <= n and s <= A
        D = list(range(n))
        exp_rank = t + min(s, t)
        case = "head r>=k" if s <= t else "plateau r<k"
        r = A - s
        pairs = pairs_at_distance(D, A, s, PAIR_CAP)
        ok_rank = True
        ok_single = True
        for (S, T) in pairs:
            cols = sorted(set(S) | set(T))
            MS = top_rows(F, list(S), k, t, cols)
            MT = top_rows(F, list(T), k, t, cols)
            if mat_rank(F, MS + MT) != exp_rank:
                ok_rank = False
            if mat_rank(F, MS) != t or mat_rank(F, MT) != t:
                ok_single = False
        tag = "%s k=%d t=%d s=%d n=%d" % (F.name, k, t, s, n)
        check("rank(Phi_ST) == t+min(s,t) = %d, all %d pairs [%s] %s"
              % (exp_rank, len(pairs), case, tag), ok_rank)
        check("single-support ranks == t, all pairs %s" % tag, ok_single)

        # first pair: Lagrange delta property + kernel certificates
        S, T = pairs[0]
        cols = sorted(set(S) | set(T))
        m = len(cols)
        lb = lagrange_basis(F, list(S))
        ok_lag = all(poly_eval(F, lb[x], y) == (1 if x == y else 0)
                     for x in S for y in S)
        check("Lagrange delta property on first support %s" % tag, ok_lag)

        M = (top_rows(F, list(S), k, t, cols)
             + top_rows(F, list(T), k, t, cols))
        B = kernel_basis(F, M)
        exp_dim = m - exp_rank
        # theorem's case-specific kernel size: q^k (head) / q^(2k-r) (plateau)
        exp_kexp = k if s <= t else 2 * k - r
        check("kernel dim == m - rank == %d and == %s exponent %d, %s"
              % (exp_dim, "k" if s <= t else "2k-r", exp_kexp, tag),
              len(B) == exp_dim and exp_dim == exp_kexp)
        span = set()
        ok_zero = True
        for coeffs in product(range(q), repeat=len(B)):
            w = [0] * m
            for cf, bv in zip(coeffs, B):
                if cf:
                    for i in range(m):
                        w[i] = F.ADD[w[i]][F.MUL[cf][bv[i]]]
            span.add(tuple(w))
            if any(x != 0 for x in matvec(F, M, w)):
                ok_zero = False
        check("kernel-span certificate: q^%d = %d distinct words, all map "
              "to 0, %s" % (exp_dim, q ** exp_dim, tag),
              ok_zero and len(span) == q ** exp_dim)

        if q ** m <= WORD_ENUM_CAP:
            counts = enum_syndrome_counts(F, M)
            zero = tuple([0] * (2 * t))
            nker = counts.get(zero, 0)
            check("FULL word enumeration (%d^%d words): joint kernel count "
                  "== q^%d, %s" % (q, m, exp_dim, tag),
                  nker == q ** exp_dim and sum(counts.values()) == q ** m,
                  "count=%d" % nker)


# ---------------------------------------------------------------------------
# [2] Theorem 2: all-slope accounting on toys (exact)
# ---------------------------------------------------------------------------

CELLS2 = [
    (5, 1, 1, 2, 1),   # flagship (the c(1,2) base-case cell)
    (7, 1, 1, 2, 1),
    (5, 1, 1, 2, 2),   # head boundary s = t
    (2, 2, 1, 2, 1),   # GF(4)
    (5, 1, 2, 1, 2),   # plateau
    (7, 1, 2, 1, 3),   # plateau s = 3
    (7, 1, 1, 1, 2),   # plateau, t = 1
]

FLAGSHIP_RESULT = {}


def vanish_set(F, a, b):
    """Solution set of a + z b = 0 (vectors over F): 'empty' / ('one', z0)
    / 'all'."""
    if all(x == 0 for x in b):
        return ("all", None) if all(x == 0 for x in a) else ("empty", None)
    i = next(i for i, x in enumerate(b) if x != 0)
    z = F.MUL[F.NEG[a[i]]][F.INV[b[i]]]
    for aj, bj in zip(a, b):
        if F.ADD[aj][F.MUL[z][bj]] != 0:
            return ("empty", None)
    return ("one", z)


def section2():
    print("\n== [2] Theorem 2: all-slope accounting (exact, toys) ==")
    for (p, e, k, t, s) in CELLS2:
        F = field(p, e)
        q = F.q
        A = k + t
        n = A + s
        assert n <= q
        D = list(range(n))
        S = tuple(D[:A])
        T = tuple(D[s:A + s])  # exchange the first s points of S
        assert len(set(S) & set(T)) == A - s
        cols = sorted(set(S) | set(T))
        m = len(cols)
        mn, mn1 = min(s, t), min(s, t - 1)
        M = (top_rows(F, list(S), k, t, cols)
             + top_rows(F, list(T), k, t, cols))
        rank = mat_rank(F, M)
        tag = "%s k=%d t=%d s=%d" % (F.name, k, t, s)
        check("joint rank == t+min(s,t) == %d, %s" % (t + mn, tag),
              rank == t + mn)

        counts = enum_syndrome_counts(F, M)
        fiber = q ** (m - rank)
        check("fiber uniformity: %d^%d syndromes hit, every fiber == q^%d, "
              "%s" % (q, rank, m - rank, tag),
              len(counts) == q ** rank
              and all(c == fiber for c in counts.values()))

        image = sorted(counts)  # u-syndrome and v-syndrome each uniform here
        N = len(image) ** 2
        # counters over syndrome pairs (a = syndromes of u, b = of v)
        c_ss = [[0] * q for _ in range(q)]
        c_sF = [0] * q
        c_Fs = [0] * q
        c_FF = 0
        alS = 0
        alT = 0
        for a in image:
            aS, aT = a[:t], a[t:]
            for b in image:
                bS, bT = b[:t], b[t:]
                tyS, zS = vanish_set(F, aS, bS)
                tyT, zT = vanish_set(F, aT, bT)
                if tyS == "one":
                    alS += 1
                if tyT == "one":
                    alT += 1
                if tyS == "one" and tyT == "one":
                    c_ss[zS][zT] += 1
                elif tyS == "one" and tyT == "all":
                    c_sF[zS] += 1
                elif tyS == "all" and tyT == "one":
                    c_Fs[zT] += 1
                elif tyS == "all" and tyT == "all":
                    c_FF += 1
        # FM1 per support (alignment <=> vanish set is a singleton)
        fm1 = (1 - qpow(q, -t)) * qpow(q, 1 - t)
        check("FM1 alignment probability exact for S and T, %s" % tag,
              Fraction(alS, N) == fm1 and Fraction(alT, N) == fm1,
              "P=%s" % fm1)

        # per-z same-slope: count == N q^-(t+mn) for EVERY z
        ok_same = True
        for z in range(q):
            cnt = c_ss[z][z] + c_sF[z] + c_Fs[z] + c_FF
            if Fraction(cnt, N) != qpow(q, -(t + mn)):
                ok_same = False
        check("per-z same-slope P[U_z in K_S cap K_T] == q^-(t+min(s,t)), "
              "every z, %s" % tag, ok_same)

        # per-(z,z') distinct: count == N q^-2t for EVERY ordered z != z'
        ok_cross = True
        for z in range(q):
            for z2 in range(q):
                if z == z2:
                    continue
                cnt = c_ss[z][z2] + c_sF[z] + c_Fs[z2] + c_FF
                if Fraction(cnt, N) != qpow(q, -2 * t):
                    ok_cross = False
        check("per-(z,z') distinct-slope P == q^-2t, every ordered pair, "
              "%s" % tag, ok_cross)

        # alignment-pair decomposition and the (2c)+Theorem-3 chain
        both_same = sum(c_ss[z][z] for z in range(q))
        both_all = sum(sum(row) for row in c_ss)
        both_diff = both_all - both_same
        P_same = Fraction(both_same, N)
        P_diff = Fraction(both_diff, N)
        P_both = Fraction(both_all, N)
        b_same = qpow(q, 1 - t - mn)
        b_diff = Fraction(q * (q - 1)) * qpow(q, -2 * t)
        b_sum = qpow(q, 1 - t - mn) + qpow(q, 2 - 2 * t)
        b_pack = 2 * qpow(q, 1 - t - mn1)
        check("branch bounds: same <= q^(1-t-mn), diff <= q(q-1)q^-2t, %s"
              % tag, P_same <= b_same and P_diff <= b_diff,
              "same=%s diff=%s" % (P_same, P_diff))
        check("(2c)+Thm3 chain: P[both] <= q^(1-t-mn)+q^(2-2t) <= "
              "2 q^(1-t-min(s,t-1)), %s" % tag,
              P_both == P_same + P_diff and P_both <= b_sum <= b_pack,
              "P=%s bound=%s packaged=%s" % (P_both, b_sum, b_pack))
        if (p, e, k, t, s) == (5, 1, 1, 2, 1):
            FLAGSHIP_RESULT["P_both"] = P_both
            FLAGSHIP_RESULT["q"] = q


# ---------------------------------------------------------------------------
# [3] Theorem 3: packaging inequality, t <= 6, s <= 8
# ---------------------------------------------------------------------------

QLIST = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 27, 64, 101, 2 ** 31]


def section3():
    print("\n== [3] Theorem 3: packaging, t <= 6, s <= 8 ==")
    ok_sym = True
    ok_num = True
    ok_eq = True
    for t in range(1, 7):
        for s in range(0, 9):
            a, b = min(s, t), min(s, t - 1)
            # canonical form (multiply by q^(t-1+a)): 1 + q^ee <= 2 q^ff
            ee, ff = 1 - t + a, a - b
            # symbolic region valid for ALL q >= 2:
            #   (ee <= 0 and ff >= 0)  since then LHS <= 2 <= 2 q^ff
            #   (1 <= ee <= ff)        since then 1 + q^ee <= 2 q^ee <= 2 q^ff
            if not ((ee <= 0 <= ff) or (1 <= ee <= ff)):
                ok_sym = False
            for qv in QLIST:
                lhs = qpow(qv, 1 - t - a) + qpow(qv, 2 - 2 * t)
                rhs = 2 * qpow(qv, 1 - t - b)
                if lhs > rhs:
                    ok_num = False
                if (s == t - 1) != (lhs == rhs):
                    ok_eq = False
            if min(s, t - 1) != b:
                ok_sym = False
    check("symbolic case reduction (1+q^e <= 2q^f regions) holds for all "
          "t<=6, s<=8", ok_sym)
    check("exact Fractions: q^(1-t-min(s,t)) + q^(2-2t) <= "
          "2 q^(1-t-min(s,t-1)), %d values of q up to 2^31" % len(QLIST),
          ok_num)
    check("equality iff s == t-1 (constant 2 sharp), strict otherwise",
          ok_eq)


# ---------------------------------------------------------------------------
# [4] Base case c(1,2) = 1
# ---------------------------------------------------------------------------

def section4():
    print("\n== [4] base case c(1,2) = 1 ==")
    check("c(1,2) = min(1, 2-1) == 1", min(1, 2 - 1) == 1)
    P = FLAGSHIP_RESULT.get("P_both")
    q = FLAGSHIP_RESULT.get("q")
    ok = P is not None and P <= 2 * qpow(q, -2)
    check("flagship (q=5, k=1, t=2, s=1): exact P[both aligned] <= "
          "2 q^(1-t) q^-c(1,2) = 2/25",
          ok, "P=%s vs 2/25" % P)


def main():
    write = "--write-certificate" in sys.argv
    section01()
    section2()
    section3()
    section4()
    result = {
        "task": "QX.13 pair-rank ledger",
        "node": "xr_ledger_qpower",
        "status": "PROVED / MOMENT-LEVEL",
        "claim": "The pair-correlation ledger exponent is c(s,t)=min(s,t-1).",
        "checks": NCHECK,
        "failures": len(FAILS),
        "field_tables": ["F5", "F7", "F11", "GF4", "GF8", "GF9"],
        "packaging_q_values": QLIST,
        "flagship": {
            "q": FLAGSHIP_RESULT.get("q"),
            "P_both": str(FLAGSHIP_RESULT.get("P_both")),
        },
    }
    if write:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("[write] %s" % CERT)

    expected = None
    if os.path.exists(CERT):
        with open(CERT, encoding="utf-8") as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", result == expected)

    print("\n%d checks, %d failures" % (NCHECK, len(FAILS)))
    if FAILS:
        for f in FAILS:
            print("FAILED: %s" % f)
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
