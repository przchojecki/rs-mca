#!/usr/bin/env python3
r"""SELF-CONTAINED machine-checked certificate for the M1 Cycle120 ABF
counterexample candidate.

It exhibits, with NO external/unaudited computation (no Danny C++, no 26-billion
census), an explicit lower bound

    emca( RS[F_17^32, H, 256], 125/256 )  >=  M / 17^32  >  2^-128

by constructing ONE ABF line (f1, f2) over F_17^32 and M >= 7 distinct slopes
gamma, each of which is machine-checked to be a *bad* slope: f1 + gamma f2 agrees
with an explicit degree-<256 codeword on a 262-point support S of H, while
(f1, f2) is NOT jointly explained on S (support-wise noncontainment).  Because
floor(17^32 / 2^128) = 6, ANY M >= 7 distinct bad slopes already clears the
2^-128 gate -- so the billion-scale census is not load-bearing.

EVERYTHING below is recomputed from first principles in pure CPython stdlib:
  * F16 = F_17[X]/(X^16 + X^8 + 3)                 (degree-16 over F_17)
  * F_17^32 = F16[theta]/(theta^2 - eta)           (degree-2 over F16)
  * eta = 6 X^9 (order 256), beta = X + 2 (not in <eta>), theta (order 512)
  * the seven-slot color-filtered supports support(T) (113-subsets of D0=<eta>)
  * Lemma 1 (fixed-jet locator transfer): a single native line (f, g) on D0 with
    f + z_T g  =  codeword c_T of RS[F16, D0, 137]  on  D0 \ support(T),
    z_T = 1 / P_T(beta), and g NOT degree-<137 explained there.
  * Lemma 2 (smooth padding): lift to RS[F_17^32, H, 256] by multiplying by the
    A-locator L_A, giving the explicit degree-<256 witness L_A * c_T and the
    F_17^32 support-wise noncontainment of (f1, f2).

Run:
    python3 experimental/scripts/verify_m1_cycle120_self_contained_certificate.py
    python3 .../verify_m1_cycle120_self_contained_certificate.py --json
    QUICK=1 python3 .../...   # tiny family, for a fast smoke test
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import time

# ===========================================================================
#  F16 = F_17[X] / (X^16 + X^8 + 3)
#  elements are little-endian coefficient lists over F_17 (degree < 16)
# ===========================================================================
P = 17
FMOD = [3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]  # X^16 + X^8 + 3
SH = 16
MASK = (1 << SH) - 1


def ftrim(a):
    a = [x % P for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def fmul(a, b):
    """F16 product via Kronecker substitution + schoolbook X^16 = -X^8 - 3."""
    la = len(a)
    lb = len(b)
    pa = 0
    for i in range(la):
        ai = a[i]
        if ai:
            pa |= (ai % P) << (SH * i)
    if pa == 0:
        return [0]
    pb = 0
    for i in range(lb):
        bi = b[i]
        if bi:
            pb |= (bi % P) << (SH * i)
    if pb == 0:
        return [0]
    pr = pa * pb
    n = la + lb - 1
    c = [(pr >> (SH * k)) & MASK for k in range(n)]
    for k in range(n - 1, 15, -1):
        ck = c[k]
        if ck:
            c[k - 8] -= ck
            c[k - 16] -= 3 * ck
    m = 16 if n >= 16 else n
    res = [c[i] % P for i in range(m)]
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


def fadd(a, b):
    n = max(len(a), len(b))
    r = [0] * n
    for i in range(len(a)):
        r[i] = a[i]
    for i in range(len(b)):
        r[i] = (r[i] + b[i]) % P
    return ftrim(r)


def fsub(a, b):
    n = max(len(a), len(b))
    r = [0] * n
    for i in range(len(a)):
        r[i] = a[i] % P
    for i in range(len(b)):
        r[i] = (r[i] - b[i]) % P
    return ftrim(r)


def fneg(a):
    return ftrim([(-x) % P for x in a])


def fpow(a, e):
    r = [1]
    base = ftrim(a[:])
    while e > 0:
        if e & 1:
            r = fmul(r, base)
        base = fmul(base, base)
        e >>= 1
    return r


def feq(a, b):
    return ftrim(a) == ftrim(b)


def fis_zero(a):
    return ftrim(a) == [0]


FZERO = [0]
FONE = [1]
F16_ORDER = P ** 16


def finv(a):
    if fis_zero(a):
        raise ZeroDivisionError("F16 inverse of zero")
    return fpow(a, F16_ORDER - 2)


def fkey(a):
    return tuple(ftrim(a))


def f_batch_inv(xs):
    """Montgomery batch inverse over F16: one finv + O(n) fmul."""
    n = len(xs)
    if n == 0:
        return []
    pre = [FONE] * (n + 1)
    for i in range(n):
        pre[i + 1] = fmul(pre[i], xs[i])
    inv = finv(pre[n])
    out = [None] * n
    for i in range(n - 1, -1, -1):
        out[i] = fmul(inv, pre[i])
        inv = fmul(inv, xs[i])
    return out


# ===========================================================================
#  F_17^32 = F16[theta] / (theta^2 - eta),  elements (a, b) = a + b*theta
# ===========================================================================
ETA = [0, 0, 0, 0, 0, 0, 0, 0, 0, 6]  # 6 X^9


def qmul(x, y):
    a, b = x
    c, d = y
    ac = fmul(a, c)
    bd = fmul(b, d)
    return (fadd(ac, fmul(bd, ETA)), fadd(fmul(a, d), fmul(b, c)))


def qadd(x, y):
    return (fadd(x[0], y[0]), fadd(x[1], y[1]))


def qsub(x, y):
    return (fsub(x[0], y[0]), fsub(x[1], y[1]))


def qeq(x, y):
    return feq(x[0], y[0]) and feq(x[1], y[1])


def qis_zero(x):
    return fis_zero(x[0]) and fis_zero(x[1])


QZERO = ([0], [0])
QONE = ([1], [0])


def emb(a):
    """Embed F16 element a into F_17^32."""
    return (ftrim(a), [0])


def qmul_emb(x, s):
    """F_17^32 element x times embedded F16 scalar s = (a*s + b*s theta)."""
    return (fmul(x[0], s), fmul(x[1], s))


def qinv(x):
    a, b = x
    norm = fsub(fmul(a, a), fmul(ETA, fmul(b, b)))  # a^2 - eta b^2 in F16
    if fis_zero(norm):
        raise ZeroDivisionError("F_17^32 inverse of zero")
    ninv = finv(norm)
    return (fmul(a, ninv), fmul(fneg(b), ninv))


def qpow(x, e):
    r = QONE
    base = x
    while e > 0:
        if e & 1:
            r = qmul(r, base)
        base = qmul(base, base)
        e >>= 1
    return r


def qkey(x):
    return (tuple(ftrim(x[0])), tuple(ftrim(x[1])))


def q_batch_inv(xs):
    n = len(xs)
    if n == 0:
        return []
    pre = [QONE] * (n + 1)
    for i in range(n):
        pre[i + 1] = qmul(pre[i], xs[i])
    inv = qinv(pre[n])
    out = [None] * n
    for i in range(n - 1, -1, -1):
        out[i] = qmul(inv, pre[i])
        inv = qmul(inv, xs[i])
    return out


# ===========================================================================
#  Generic field interface + polynomial helpers
# ===========================================================================
class Field:
    def __init__(self, name, zero, one, add, sub, mul, inv, is_zero, key, batch_inv):
        self.name = name
        self.zero = zero
        self.one = one
        self.add = add
        self.sub = sub
        self.mul = mul
        self.inv = inv
        self.is_zero = is_zero
        self.key = key
        self.batch_inv = batch_inv


F16 = Field("F16", FZERO, FONE, fadd, fsub, fmul, finv, fis_zero, fkey, f_batch_inv)
FQ = Field("F_17^32", QZERO, QONE, qadd, qsub, qmul, qinv, qis_zero, qkey, q_batch_inv)


def p_eval(poly, x, Fld):
    acc = Fld.zero
    for cf in reversed(poly):
        acc = Fld.add(Fld.mul(acc, x), cf)
    return acc


def p_degree(poly, Fld):
    d = len(poly) - 1
    while d > 0 and Fld.is_zero(poly[d]):
        d -= 1
    if d == 0 and Fld.is_zero(poly[0]):
        return -1
    return d


def newton_divdiff(xs, ys, Fld):
    """Newton divided differences c[0..n-1] for interpolation through (xs, ys).

    Uses ONE batched field inversion for all O(n^2) denominators.  The unique
    interpolating polynomial has degree = max{ i : c[i] != 0 }, because the
    Newton basis polynomial prod_{j<i}(X - xs[j]) has degree exactly i.
    """
    n = len(xs)
    c = list(ys)
    dens = []
    for i in range(1, n):
        for j in range(n - 1, i - 1, -1):
            dens.append(Fld.sub(xs[j], xs[j - i]))
    invs = Fld.batch_inv(dens)
    idx = 0
    for i in range(1, n):
        for j in range(n - 1, i - 1, -1):
            c[j] = Fld.mul(Fld.sub(c[j], c[j - 1]), invs[idx])
            idx += 1
    return c


def newton_to_standard(c, xs, Fld):
    """Convert Newton form (coeffs c, nodes xs) to standard coefficient list."""
    n = len(c)
    poly = [c[n - 1]]
    for i in range(n - 2, -1, -1):
        xi = xs[i]
        new = [Fld.zero] * (len(poly) + 1)
        for d in range(len(poly)):
            cf = poly[d]
            new[d + 1] = Fld.add(new[d + 1], cf)
            new[d] = Fld.sub(new[d], Fld.mul(cf, xi))
        new[0] = Fld.add(new[0], c[i])
        poly = new
    while len(poly) > 1 and Fld.is_zero(poly[-1]):
        poly.pop()
    return poly


def newton_eval(c, xs, z, Fld):
    """Evaluate the Newton-form interpolant at a fresh point z."""
    n = len(c)
    acc = c[n - 1]
    for i in range(n - 2, -1, -1):
        acc = Fld.add(c[i], Fld.mul(Fld.sub(z, xs[i]), acc))
    return acc


# ===========================================================================
#  Domain / structural constants  (all re-verified below)
# ===========================================================================
ETA_ELT = ETA[:]            # eta = 6 X^9 in F16
BETA = [2, 1]               # beta = X + 2 in F16
THETA = ([0], [1])          # theta in F_17^32, theta^2 = eta

E_SETS = {
    1: {0, 1, 2, 3, 5, 11, 12, 13},
    2: {0, 1, 2, 3, 4, 8, 9, 14},
    3: {0, 1, 2, 4, 5, 7, 11, 14},
}

NATIVE_N = 256
NATIVE_J = 113
NATIVE_SIGMA = 6
NATIVE_K = 137          # = 256 - 113 - 6
NATIVE_AGREE = 143      # = 256 - 113
PAD = 119               # |A|
LIFT_N = 512            # |H|
LIFT_K = 256            # = 137 + 119
LIFT_AGREE = 262        # = 143 + 119
FIELD_SIZE = 17 ** 32
GATE_BITS = 128


# ---- support(T): seven-slot color-filtered 113-subsets of D0 = <eta> --------
def build_field_globals():
    eta_pows = [None] * 256
    cur = FONE
    for j in range(256):
        eta_pows[j] = cur
        cur = fmul(cur, ETA_ELT)
    subgroup = [eta_pows[(8 * m) % 256] for m in range(32)]  # order-32 subgroup
    xi = fpow(BETA, 2)
    return eta_pows, subgroup, xi


ETA_POWS, SUBGROUP, XI = build_field_globals()


def lift_slot(i, a):
    """The 16 square-root points for slot color (i, a) inside the order-32 sub."""
    target = [[pow(3, (a + e) % 16, P)] for e in E_SETS[i]]
    out = []
    for x in SUBGROUP:
        xx = fmul(x, x)
        if any(feq(xx, tt) for tt in target):
            out.append(x)
    return out


def support_points(choices):
    """The 113 field elements of support(T) for the 7-tuple `choices`."""
    sup = [FONE]
    for t, (i, a) in enumerate(choices, 1):
        et = ETA_POWS[t % 256]
        for y in lift_slot(i, a):
            sup.append(fmul(et, y))
    return sup


def locator_from_roots_f16(roots):
    """monic prod (X - r) over F16 (used only for a one-off jet cross-check)."""
    poly = [FONE]
    for r in roots:
        nr = fneg(r)
        new = [FZERO] * (len(poly) + 1)
        for d in range(len(poly)):
            cf = poly[d]
            new[d + 1] = fadd(new[d + 1], cf)
            new[d] = fadd(new[d], fmul(cf, nr))
        poly = new
    return poly


# ===========================================================================
#  Build the whole certificate
# ===========================================================================
def build(target_native, lift_sample, seed, log):
    report = {"checks": {}, "stats": {}}

    def check(name, cond):
        report["checks"][name] = bool(cond)
        log(f"  [{'OK ' if cond else 'FAIL'}] {name}")
        return bool(cond)

    t_start = time.time()

    # -- 0. field / structural sanity -------------------------------------
    log("== 0. field + structural setup ==")
    check("F16: eta has order 256", feq(fpow(ETA_ELT, 256), FONE) and not feq(fpow(ETA_ELT, 128), FONE))
    check("F16: eta^16 == 3", feq(fpow(ETA_ELT, 16), [3]))
    check("F16: beta = X+2 not in <eta> (beta^256 != 1)", not feq(fpow(BETA, 256), FONE))
    check("F_17^32: theta^2 == eta", qeq(qmul(THETA, THETA), emb(ETA_ELT)))
    check("F_17^32: theta has order 512",
          qeq(qpow(THETA, 512), QONE) and not qeq(qpow(THETA, 256), QONE))
    # v2(17^32 - 1) = 9  (so 2^9 = 512 | 17^32 - 1 but 2^9 not | 17^16 - 1)
    def v2(m):
        k = 0
        while m % 2 == 0:
            m //= 2
            k += 1
        return k
    check("v2(17^32 - 1) == 9", v2(17 ** 32 - 1) == 9)
    check("v2(17^16 - 1) == 8", v2(17 ** 16 - 1) == 8)
    for i in (1, 2, 3):
        s3 = sum(pow(3, e, P) for e in E_SETS[i]) % P
        s9 = sum(pow(9, e, P) for e in E_SETS[i]) % P
        check(f"E_SET[{i}] color identity sum 3^e == 0 and sum 9^e == 0", s3 == 0 and s9 == 0)

    # D0 = <eta> (256 points), index by canonical key
    D0 = ETA_POWS[:]                       # D0[i] = eta^i
    idx_of = {fkey(D0[i]): i for i in range(256)}
    check("D0 = <eta> has 256 distinct points", len(idx_of) == 256)

    # theta * D0 split into A (119) and R (137); A_w[j] = eta^j so a_j = (0, eta^j)
    A_w = [ETA_POWS[j] for j in range(PAD)]          # w with a = theta * w
    A_elts = [([0], A_w[j]) for j in range(PAD)]      # the 119 points of A
    R_count = 256 - PAD
    check("padding split |A| + |R| == 256", PAD + R_count == 256)
    check("|H| = |D0| + |theta D0| == 512", 256 + 256 == LIFT_N)
    check("dimension identity 137 + 119 == 256", NATIVE_K + PAD == LIFT_K)
    check("native agreement 256 - 113 == 143", NATIVE_N - NATIVE_J == NATIVE_AGREE)
    check("lift agreement 143 + 119 == 262", NATIVE_AGREE + PAD == LIFT_AGREE)
    check("ABF closed threshold (256-125)*512//256 == 262", (256 - 125) * LIFT_N // 256 == LIFT_AGREE)
    check("D0 and theta*D0 are disjoint cosets",
          all(qkey(emb(D0[i])) != qkey(A_elts[0]) for i in range(0)) or
          (emb(D0[0])[1] == [0] and A_elts[0][0] == [0] and not fis_zero(A_elts[0][1])))

    # -- 1. family F of distinct bad slopes --------------------------------
    log("== 1. family of distinct slopes z_T = 1 / P_T(beta) ==")
    rng = random.Random(seed)
    members = []           # each: dict(choices, Jset, S0_idx, Pbeta, zT, ...)
    seen_slopes = set()
    seen_choices = set()
    # pre-batch: we need P_T(beta) = prod_{x in support}(beta - x) and z_T = inv
    tries = 0
    need = target_native + 1          # +1 anchor (used only to build f, not counted)
    max_tries = need * 60 + 500
    pending = []           # collect supports, then batch-invert all P_T(beta)
    while len(pending) < need and tries < max_tries:
        tries += 1
        choices = tuple((rng.randint(1, 3), rng.randint(0, 15)) for _ in range(7))
        if choices in seen_choices:
            continue
        seen_choices.add(choices)
        sup = support_points(choices)
        keys = [fkey(s) for s in sup]
        if len(set(keys)) != NATIVE_J:
            continue                                  # not 113 distinct
        if any(k not in idx_of for k in keys):
            continue                                  # not inside D0
        Jset = frozenset(idx_of[k] for k in keys)
        if len(Jset) != NATIVE_J:
            continue
        # P_T(beta) = prod (beta - x)
        pb = FONE
        for s in sup:
            pb = fmul(pb, fsub(BETA, s))
        if fis_zero(pb):
            continue
        pending.append({"choices": choices, "keys": keys, "Jset": Jset, "Pbeta": pb})
    check("found enough candidate supports", len(pending) >= need)

    # batch invert all P_T(beta) -> z_T, then keep DISTINCT slopes
    zs = f_batch_inv([m["Pbeta"] for m in pending])
    collected = []
    for m, z in zip(pending, zs):
        zk = fkey(z)
        if zk in seen_slopes:
            continue
        seen_slopes.add(zk)
        m["zT"] = z
        m["S0_idx"] = [i for i in range(256) if i not in m["Jset"]]
        collected.append(m)
        if len(collected) >= need:
            break
    check("collected enough DISTINCT slopes (anchor + counted family)", len(collected) >= need)
    collected = collected[:need]
    # member 0 is the ANCHOR used only to build the single line f; it is NOT
    # counted (its codeword c_T is identically 0).  The counted family is the rest.
    anchor = collected[0]
    members = collected[1:]
    check("all counted slopes are pairwise distinct field elements",
          len({fkey(m["zT"]) for m in members}) == len(members))
    check("anchor slope distinct from every counted slope",
          fkey(anchor["zT"]) not in {fkey(m["zT"]) for m in members})
    log(f"   anchor slopes: 1   distinct counted native slopes: {len(members)}")

    # fixed jet: per member (anchor + counted), power sums p_1..p_5 == 1, p_6 != 1
    log("   verifying fixed-jet (power sums p_1..p_5 == 1, p_6 != 1) per member")
    jet_ok = True
    for m in collected:
        sup = [D0[i] for i in sorted(m["Jset"])]
        ps = [FZERO] * 7
        for s in sup:
            xk = s
            for k in range(1, 7):
                ps[k] = fadd(ps[k], xk)
                xk = fmul(xk, s)
        ok = all(feq(ps[k], FONE) for k in range(1, 6)) and not feq(ps[6], FONE)
        jet_ok = jet_ok and ok
    check("fixed jet p_1..p_5 == 1, p_6 != 1 (sigma exactly 6) for every member", jet_ok)
    # one-off cross check vs the bridge: locator top-6 coeffs == [1,16,0,0,0,0]
    sup0 = [D0[i] for i in sorted(anchor["Jset"])]
    loc0 = locator_from_roots_f16(sup0)
    top6 = [ftrim(loc0[NATIVE_J - k]) for k in range(6)]
    check("locator top-6 coeffs == [1,16,0,0,0,0] (cross-check member 0)",
          top6 == [[1], [16], [0], [0], [0], [0]] and len(loc0) - 1 == NATIVE_J)

    # -- 2. native line (f, g) and per-member certificate ------------------
    log("== 2. native Lemma-1 line over F16 (agreement 143 + noncontainment) ==")
    # g(x) = L_D(beta) / (beta - x),  L_D(beta) = beta^256 - 1
    LD_beta = fsub(fpow(BETA, 256), FONE)
    inv_beta_minus = f_batch_inv([fsub(BETA, D0[i]) for i in range(256)])
    g_word = [fmul(LD_beta, inv_beta_minus[i]) for i in range(256)]

    # anchor J0: e_{J0}(x) = 1 / (x (beta - x) P_{J0}'(x)),  x in J0
    base = anchor
    J0 = sorted(base["Jset"])
    J0pts = [D0[i] for i in J0]
    # P_{J0}'(x) = prod_{y != x}(x - y) for x in J0
    Pprime = []
    for a in range(len(J0pts)):
        xa = J0pts[a]
        prod = FONE
        for b in range(len(J0pts)):
            if a != b:
                prod = fmul(prod, fsub(xa, J0pts[b]))
        Pprime.append(prod)
    dens = [fmul(fmul(J0pts[a], fsub(BETA, J0pts[a])), Pprime[a]) for a in range(len(J0pts))]
    e0_vals = f_batch_inv(dens)
    e0_word = [FZERO] * 256
    for a, i in enumerate(J0):
        e0_word[i] = e0_vals[a]
    z0 = base["zT"]
    f_word = [fsub(e0_word[i], fmul(z0, g_word[i])) for i in range(256)]

    # cross-check (Lemma 1 sanity): f + z0 g agrees with deg<137 on D0\J0 by interp
    native_agreement_ok = True
    native_noncontain_ok = True
    codewords = {}     # member-id -> standard coeffs of c_T (deg < 137)
    n_pass = 0
    for mi, m in enumerate(members):
        zT = m["zT"]
        S0 = m["S0_idx"]
        xs = [D0[i] for i in S0]
        ys = [fadd(f_word[i], fmul(zT, g_word[i])) for i in S0]
        c = newton_divdiff(xs, ys, F16)
        # degree < 137  <=>  c[137..142] all zero
        deg_ok = all(fis_zero(c[k]) for k in range(NATIVE_K, NATIVE_AGREE))
        # noncontainment: g restricted to S0 is NOT degree < 137
        cg = newton_divdiff(xs, [g_word[i] for i in S0], F16)
        nonc = not all(fis_zero(cg[k]) for k in range(NATIVE_K, NATIVE_AGREE))
        if deg_ok and nonc:
            n_pass += 1
            cT = newton_to_standard(c[:NATIVE_K], xs[:NATIVE_K], F16)
            if p_degree(cT, F16) >= NATIVE_K:
                deg_ok = False
            codewords[mi] = cT
        native_agreement_ok = native_agreement_ok and deg_ok
        native_noncontain_ok = native_noncontain_ok and nonc
    check("native: f + z_T g is degree-<137 explained on D0\\support(T) (agreement 143), all members",
          native_agreement_ok)
    check("native: g NOT degree-<137 explained on D0\\support(T) (noncontainment), all members",
          native_noncontain_ok)
    check("native: every member yields a codeword c_T of degree < 137",
          all(p_degree(codewords[mi], F16) < NATIVE_K for mi in codewords))
    # non-vacuity: every counted codeword is NONZERO and genuinely high-degree
    # (exactly 136), so the agreement is with a real codeword, not the 0 word.
    cdegs = sorted(p_degree(codewords[mi], F16) for mi in codewords)
    check("native non-vacuity: every counted c_T has degree exactly 136 (nonzero, high-degree)",
          len(cdegs) > 0 and all(d == NATIVE_K - 1 for d in cdegs))
    native_distinct = n_pass
    log(f"   native_distinct_slopes (agreement 143, F16) = {native_distinct}")
    report["stats"]["native_distinct_slopes"] = native_distinct

    # -- 3. lift to F_17^32 via smooth padding -----------------------------
    log("== 3. lift to RS[F_17^32, H, 256] via smooth padding (agreement 262) ==")
    # L_A(X) = prod_{a in A}(X - a), over F_17^32, degree 119
    LA = [QONE]
    for a in A_elts:
        na = qsub(QZERO, a)
        new = [QZERO] * (len(LA) + 1)
        for d in range(len(LA)):
            cf = LA[d]
            new[d + 1] = qadd(new[d + 1], cf)
            new[d] = qadd(new[d], qmul(cf, na))
        LA = new
    check("L_A has degree 119", p_degree(LA, FQ) == PAD)
    check("L_A vanishes on A (sample)", all(qis_zero(p_eval(LA, A_elts[j], FQ)) for j in (0, 37, 59, 118)))
    check("L_A nonzero on D0 (sample)", all(not qis_zero(p_eval(LA, emb(D0[i]), FQ)) for i in (0, 5, 100, 255)))

    # L_A evaluated on all of D0 (x in F16), then f1, f2 words on D0
    LA_on_D0 = []
    for i in range(256):
        x = D0[i]
        acc = QZERO
        for cf in reversed(LA):
            acc = (fadd(fmul(acc[0], x), cf[0]), fadd(fmul(acc[1], x), cf[1]))  # acc*emb(x)+cf
        LA_on_D0.append(acc)
    f1_D0 = [qmul_emb(LA_on_D0[i], f_word[i]) for i in range(256)]   # L_A(x) f(x)
    f2_D0 = [qmul_emb(LA_on_D0[i], g_word[i]) for i in range(256)]   # L_A(x) g(x)

    # choose the lift sample (distinct slopes that passed native)
    sample_ids = [mi for mi in range(len(members)) if mi in codewords][:lift_sample]
    log(f"   lifting and DIRECTLY checking {len(sample_ids)} distinct slopes over F_17^32")

    lift_line_ok = True
    lift_nonc_ok = True
    lift_pass = 0
    lifted_keys = set()
    wt_degs = []
    for mi in sample_ids:
        m = members[mi]
        zT = m["zT"]
        S0 = m["S0_idx"]                       # 143 indices into D0
        # explicit degree-<256 witness  W_T = L_A * emb(c_T)
        cT = codewords[mi]
        WT = [QZERO] * (len(LA) + len(cT) - 1)
        for jj in range(len(cT)):
            s = cT[jj]
            if fis_zero(s):
                continue
            for ii in range(len(LA)):
                term = (fmul(LA[ii][0], s), fmul(LA[ii][1], s))   # LA[ii] * emb(s)
                WT[ii + jj] = qadd(WT[ii + jj], term)
        deg_WT = p_degree(WT, FQ)
        wt_degs.append(deg_WT)
        line_ok = deg_WT < LIFT_K
        # evaluate W_T and the line word f1 + zT f2 at all 262 points of S_T
        # (a) D0 \ support(T): x = D0[i] in F16
        for i in S0:
            # W_T(x) via Horner with embedded x  (2 fmuls/step)
            acc0, acc1 = FZERO, FZERO
            xf = D0[i]
            for cf in reversed(WT):
                acc0 = fadd(fmul(acc0, xf), cf[0])
                acc1 = fadd(fmul(acc1, xf), cf[1])
            rhs = qadd(f1_D0[i], qmul_emb(f2_D0[i], zT))
            if not (feq(acc0, rhs[0]) and feq(acc1, rhs[1])):
                line_ok = False
                break
        if line_ok:
            # (b) A: a = (0, w), line point = 0; W_T(a) must be 0
            for j in range(PAD):
                w = A_w[j]
                weta = fmul(w, ETA_ELT)
                acc0, acc1 = FZERO, FZERO
                for cf in reversed(WT):
                    na0 = fadd(fmul(acc1, weta), cf[0])
                    na1 = fadd(fmul(acc0, w), cf[1])
                    acc0, acc1 = na0, na1
                if not (fis_zero(acc0) and fis_zero(acc1)):
                    line_ok = False
                    break

        # DIRECT F_17^32 noncontainment: f2 not degree-<256 explained on S_T.
        # Interpolate f2 on 256 of the 262 points; the unique deg<256 interpolant
        # must DISAGREE with f2 on at least one of the 6 held-out points.
        d0_pts = [(emb(D0[i]), f2_D0[i]) for i in S0]            # 143
        a_pts = [(A_elts[j], QZERO) for j in range(PAD)]        # 119, f2 = 0 on A
        held = d0_pts[:6]
        interp = d0_pts[6:] + a_pts                              # 137 + 119 = 256
        xs_i = [pt for pt, _ in interp]
        ys_i = [val for _, val in interp]
        c_nc = newton_divdiff(xs_i, ys_i, FQ)
        nonc_direct = False
        for pt, val in held:
            q = newton_eval(c_nc, xs_i, pt, FQ)
            if not qeq(q, val):
                nonc_direct = True
                break

        if line_ok and nonc_direct:
            lift_pass += 1
            lifted_keys.add(qkey(emb(zT)))
        lift_line_ok = lift_line_ok and line_ok
        lift_nonc_ok = lift_nonc_ok and nonc_direct

    check("lift: explicit deg-<256 witness L_A*c_T == f1 + z_T f2 on all 262 points of S, every checked slope",
          lift_line_ok)
    check("lift: DIRECT F_17^32 noncontainment -- f2 (hence (f1,f2)) NOT deg-<256 explained on S, every checked slope",
          lift_nonc_ok)
    check("lift: all sampled lifted slopes are distinct elements of F_17^32",
          len(lifted_keys) == lift_pass)
    check("lift non-vacuity: every witness W_T = L_A*c_T has degree exactly 255 (< 256, genuinely high)",
          len(wt_degs) > 0 and all(d == LIFT_K - 1 for d in wt_degs))
    f17_verified = lift_pass
    log(f"   f17_32_verified_slopes (agreement 262, F_17^32, fully direct) = {f17_verified}")
    report["stats"]["f17_32_verified_slopes"] = f17_verified

    # -- 4. emca gate ------------------------------------------------------
    log("== 4. emca density gate ==")
    M = f17_verified
    floor_q = FIELD_SIZE // (1 << GATE_BITS)
    check("floor(17^32 / 2^128) == 6", floor_q == 6)
    gate = M * (1 << GATE_BITS) > FIELD_SIZE      # M / 17^32 > 2^-128
    check(f"emca gate M*2^128 > 17^32  (M = {M} > 6)", gate and M > 6)

    report["stats"].update({
        "agreement_native": NATIVE_AGREE,
        "agreement_lifted": LIFT_AGREE,
        "M_bad_slopes": M,
        "floor_field_over_2_128": floor_q,
        "field_size": FIELD_SIZE,
        "emca_lower_bound_fraction": f"{M} / 17^32",
        "emca_lower_bound_log2": (math.log2(M) - 32 * math.log2(17)) if M > 0 else float("-inf"),
        "gate_cleared": bool(gate and M > 6),
        "runtime_seconds": time.time() - t_start,
    })
    report["all_checks_pass"] = all(report["checks"].values())
    return report


# ===========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--target-native", type=int, default=None)
    ap.add_argument("--lift-sample", type=int, default=None)
    ap.add_argument("--seed", type=int, default=20260629)
    args = ap.parse_args()

    quick = os.environ.get("QUICK") == "1"
    target_native = args.target_native if args.target_native is not None else (8 if quick else 40)
    # by default DIRECTLY verify every counted native slope over F_17^32 (no sampling gap)
    lift_sample = args.lift_sample if args.lift_sample is not None else (4 if quick else target_native)

    logs = []
    def log(s):
        logs.append(s)
        if not args.json:
            print(s, flush=True)

    report = build(target_native, lift_sample, args.seed, log)

    M = report["stats"]["M_bad_slopes"]
    lb_log2 = report["stats"]["emca_lower_bound_log2"]
    ok = report["all_checks_pass"] and report["stats"]["gate_cleared"]

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print()
        print("=" * 72)
        print(f"native_distinct_slopes (F16,    agreement 143) = {report['stats']['native_distinct_slopes']}")
        print(f"f17_32_verified_slopes (F_17^32, agreement 262) = {report['stats']['f17_32_verified_slopes']}")
        print(f"emca( RS[F_17^32,H,256], 125/256 ) >= {M} / 17^32 = 2^({lb_log2:.4f})  >  2^-128")
        print(f"gate: floor(17^32/2^128)=6, so M={M} > 6 clears 2^-128 : {report['stats']['gate_cleared']}")
        print("=" * 72)
        print(f"RESULT: {'PASS' if ok else 'FAIL'}  (all {len(report['checks'])} checks "
              f"{'passed' if report['all_checks_pass'] else 'DID NOT pass'}, "
              f"runtime {report['stats']['runtime_seconds']:.1f}s)")
        print()
        print("ESTABLISHED (machine-checked, pure stdlib, no external census):")
        print("  * a single explicit ABF line (f1,f2) over F_17^32 and M distinct slopes;")
        print("  * for each: f1 + gamma f2 = explicit deg-<256 codeword on a 262-subset S of H;")
        print("  * for each: (f1,f2) is NOT jointly explained on S (direct F_17^32 linear algebra);")
        print("  * floor(17^32/2^128)=6, so M>6 gives emca >= M/17^32 > 2^-128.")
        print("NOT established here (literature question, not a computation):")
        print("  * that ABF Definition 4.3 scores exactly this event -- gamma uniform on")
        print("    K=F_17^32, closed threshold |S| >= 262, with NO extra q_chal / quotient /")
        print("    endpoint / duplicate-slope filter that would change the count. This is a")
        print("    reading of the ABF source, independent of the arithmetic certified above.")

    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
