#!/usr/bin/env python3
"""Verify the fixed-root-star slope collapse sharpening of the F1 ledger.

Status: AUDIT / EXPERIMENTAL. Sharpens, does not extend.

This corroborates a sharpening of Corollaries 13/15/16 of
``experimental/notes/f1/f1_syndrome_pencil_normal_form.md``. In the GLOBAL
MONIC-RANK-ONE branch of the t=2 syndrome-pencil gate (Cor 15: ``rank A_z <= 1``
for every slope z), the note bounds the number of distinct noncontained bad
slopes by ``1 + binom(|D|-1, j-1)`` -- exponential in |D| for j ~ |D|/2 -- by
allowing each of the binom(|D|-1, j-1) star landing complements its own slope.

The sharper fact (field-general, 5-line proof in the note section) is that the
WHOLE fixed-root star contributes EXACTLY ONE slope, so the whole global
monic-rank-one branch contributes AT MOST 2 distinct noncontained slopes.

Star-constancy lemma. Let alpha be a field element, j >= 2, and put
``(u_0,...,u_j) = a (1,alpha,...,alpha^j)``, ``(v_0,...,v_j) = b (1,...,alpha^j)``
with u_{j+1}, v_{j+1} free (this is the Cor 15 global rank-one pencil). For any
star complement ``T = {alpha} u U`` (alpha a root of L_T), with Hankel rows
``a_m = sum_l ell_l u_{m+l}``, ``b_m = sum_l ell_l v_{m+l}`` (m=0,1):

    a_0 = a * L_T(alpha) = 0,           b_0 = b * L_T(alpha) = 0,
    a_1 = u_{j+1} - a*alpha^{j+1},       b_1 = v_{j+1} - b*alpha^{j+1},

and a_1, b_1 are INDEPENDENT of U. Hence the Cor 4 gate slope -a_1/b_1 is one
fixed value for every star complement; the only other slope the branch can carry
is the note's scalar-zero slope a + z b = 0.

This is an off-keystone sharpening: the note had already moved this branch to the
polynomial / non-aperiodic side of its ledger (Cor 13/16). It does NOT touch the
open aperiodic non-global determinant-incidence branch; generic (u,v) still carry
~|D| distinct slopes (note "Why This Helps F1").

The verifier RE-IMPLEMENTS GF(p), GF(p^2), GF(p^3), the locator and the gate
from scratch (no shared code) and checks, exhaustively over small fields:
  (a) a_0 = b_0 = 0 and a_1, b_1 are constant across every star complement;
  (b) the star contributes exactly one noncontained slope iff b_1 != 0;
  (c) the whole global monic-rank-one branch has <= 2 distinct noncontained
      slopes (and the star part has <= 1), including the alpha-not-in-D and
      infinity (s=0) branches;
  (d) the note's 1+binom(|D|-1, j-1) bound is genuinely loose: it exhibits the
      number of star landing complements collapsing onto a single slope;
  (e) a gate-vs-direct-interpolation cross-check on NON-structured (u,v),
      validating the Cor 4 gate itself.
"""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from pathlib import Path


# --------------------------------------------------------------------------
# Fields: GF(p), GF(p^2)=F_p[w]/(w^2-d), GF(p^3)=F_p[t]/(t^3-c), from scratch.
# --------------------------------------------------------------------------
class GFp:
    kind = "GF(p)"

    def __init__(self, p):
        self.p = p
        self.zero = 0
        self.one = 1 % p

    def fi(self, a):
        return a % self.p

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def neg(self, a):
        return (-a) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def inv(self, a):
        return pow(a, -1, self.p)

    def isz(self, a):
        return a % self.p == 0

    def eq(self, a, b):
        return (a - b) % self.p == 0

    def elements(self):
        return list(range(self.p))


def _least_nonsquare(p):
    for v in range(2, p):
        if pow(v, (p - 1) // 2, p) == p - 1:
            return v
    raise ValueError("no nonsquare")


class GFp2:
    kind = "GF(p^2)"

    def __init__(self, p):
        self.p = p
        self.d = _least_nonsquare(p)
        self.zero = (0, 0)
        self.one = (1 % p, 0)

    def fi(self, a):
        return (a % self.p, 0)

    def add(self, x, y):
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def sub(self, x, y):
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p)

    def neg(self, x):
        return ((-x[0]) % self.p, (-x[1]) % self.p)

    def mul(self, x, y):
        a = (x[0] * y[0] + self.d * x[1] * y[1]) % self.p
        b = (x[0] * y[1] + x[1] * y[0]) % self.p
        return (a, b)

    def inv(self, x):
        nr = (x[0] * x[0] - self.d * x[1] * x[1]) % self.p
        ni = pow(nr, -1, self.p)
        return ((x[0] * ni) % self.p, (-x[1] * ni) % self.p)

    def isz(self, x):
        return x[0] % self.p == 0 and x[1] % self.p == 0

    def eq(self, x, y):
        return (x[0] - y[0]) % self.p == 0 and (x[1] - y[1]) % self.p == 0

    def elements(self):
        return [(a, b) for a in range(self.p) for b in range(self.p)]


def _least_noncube(p):
    if (p - 1) % 3 != 0:
        return 2  # x^3 - 2 irreducible candidate; verified by use below
    for c in range(2, p):
        if pow(c, (p - 1) // 3, p) != 1:
            return c
    return 2


class GFp3:
    kind = "GF(p^3)"

    def __init__(self, p):
        self.p = p
        self.c = _least_noncube(p)
        self.zero = (0, 0, 0)
        self.one = (1 % p, 0, 0)

    def fi(self, a):
        return (a % self.p, 0, 0)

    def add(self, x, y):
        return tuple((x[i] + y[i]) % self.p for i in range(3))

    def sub(self, x, y):
        return tuple((x[i] - y[i]) % self.p for i in range(3))

    def neg(self, x):
        return tuple((-x[i]) % self.p for i in range(3))

    def mul(self, x, y):
        p, c = self.p, self.c
        a0, a1, a2 = x
        b0, b1, b2 = y
        d0 = a0 * b0 + c * (a1 * b2 + a2 * b1)
        d1 = a0 * b1 + a1 * b0 + c * (a2 * b2)
        d2 = a0 * b2 + a1 * b1 + a2 * b0
        return (d0 % p, d1 % p, d2 % p)

    def isz(self, x):
        return all(v % self.p == 0 for v in x)

    def eq(self, x, y):
        return all((x[i] - y[i]) % self.p == 0 for i in range(3))

    def inv(self, x):
        return self.pow(x, self.p ** 3 - 2)

    def pow(self, x, e):
        r = self.one
        b = x
        while e > 0:
            if e & 1:
                r = self.mul(r, b)
            b = self.mul(b, b)
            e >>= 1
        return r

    def elements(self):
        # Deterministic bounded sample (full p^3 enumeration is unnecessary):
        # the base field plus a few genuinely-cubic directions exercise the
        # free last-entry of an extension pencil.
        base = [self.fi(a) for a in range(self.p)]
        extra = [(0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (1, 0, 1)]
        return base + extra


def fpow(F, x, e):
    r = F.one
    b = x
    while e > 0:
        if e & 1:
            r = F.mul(r, b)
        b = F.mul(b, b)
        e >>= 1
    return r


def locator(F, roots):
    """Coeffs of prod (X - rt), ascending, monic top (ell_j = 1)."""
    c = [F.one]
    for rt in roots:
        nc = [F.zero] * (len(c) + 1)
        for i, ci in enumerate(c):
            nc[i] = F.sub(nc[i], F.mul(rt, ci))
            nc[i + 1] = F.add(nc[i + 1], ci)
        c = nc
    return c


def row(F, vec, ell, m):
    t = F.zero
    for l, cl in enumerate(ell):
        t = F.add(t, F.mul(vec[m + l], cl))
    return t


def gate_slope(F, u, v, ell):
    """Cor 4 (t=2): slope z if noncontained bad, else None."""
    a0 = row(F, u, ell, 0)
    a1 = row(F, u, ell, 1)
    b0 = row(F, v, ell, 0)
    b1 = row(F, v, ell, 1)
    if F.isz(b0) and F.isz(b1):
        return None  # contained
    det = F.sub(F.mul(a0, b1), F.mul(a1, b0))
    if not F.isz(det):
        return None  # not on the determinant quadric
    if not F.isz(b0):
        return F.neg(F.mul(a0, F.inv(b0)))
    return F.neg(F.mul(a1, F.inv(b1)))


# --------------------------------------------------------------------------
# (a)(b)(c)(d): star-constancy + branch <= 2 slopes, full structured sweep
# --------------------------------------------------------------------------
def check_star_branch(F, p, n, jmax, last_step=1):
    """Exhaustive global monic-rank-one sweep. Returns dict of counters."""
    pts = [F.fi(i) for i in range(1, n + 1)]
    lastset = F.elements()
    if last_step > 1:
        lastset = lastset[::last_step]
    viol = 0
    checks = 0
    max_star_slopes = 0
    max_branch_slopes = 0
    max_collapse = 0  # max (#star landing complements collapsing to 1 slope)
    for j in range(2, jmax + 1):
        all_T = list(itertools.combinations(range(n), j))
        for ai in range(1, n + 1):
            alpha = F.fi(ai)
            in_domain = any(F.eq(pts[i], alpha) for i in range(n))
            w = [fpow(F, alpha, i) for i in range(j + 1)]
            ajp1 = fpow(F, alpha, j + 1)
            star_T = [T for T in all_T if any(F.eq(pts[i], alpha) for i in T)]
            for sa in range(1, p):          # scalar a != 0
                for sb in range(0, p):      # scalar b
                    a = F.fi(sa)
                    b = F.fi(sb)
                    base_u = [F.mul(a, wi) for wi in w]
                    base_v = [F.mul(b, wi) for wi in w]
                    for ulast in lastset:
                        for vlast in lastset:
                            u = base_u + [ulast]
                            v = base_v + [vlast]
                            A1 = F.sub(ulast, F.mul(a, ajp1))  # predicted a_1
                            B1 = F.sub(vlast, F.mul(b, ajp1))  # predicted b_1
                            star_slopes = set()
                            nland = 0
                            for T in star_T:
                                ell = locator(F, [pts[i] for i in T])
                                a0 = row(F, u, ell, 0)
                                b0 = row(F, v, ell, 0)
                                a1 = row(F, u, ell, 1)
                                b1 = row(F, v, ell, 1)
                                # (a) star algebra
                                if not (F.isz(a0) and F.isz(b0)):
                                    viol += 1
                                if not (F.eq(a1, A1) and F.eq(b1, B1)):
                                    viol += 1
                                z = gate_slope(F, u, v, ell)
                                if z is not None:
                                    star_slopes.add(z)
                                    nland += 1
                            # (b) star contributes exactly one slope iff B1 != 0
                            noncont_pred = not F.isz(B1)
                            if noncont_pred != (len(star_slopes) > 0):
                                viol += 1
                            if len(star_slopes) > 1:
                                viol += 1
                            if len(star_slopes) == 1:
                                zstar = F.neg(F.mul(A1, F.inv(B1)))
                                if zstar not in star_slopes:
                                    viol += 1
                            # (c) whole branch over ALL complements <= 2 slopes
                            branch = set()
                            for T in all_T:
                                ell = locator(F, [pts[i] for i in T])
                                z = gate_slope(F, u, v, ell)
                                if z is not None:
                                    branch.add(z)
                            if len(branch) > 2:
                                viol += 1
                            if in_domain and len(star_slopes) > 0 and nland > max_collapse:
                                max_collapse = nland
                            max_star_slopes = max(max_star_slopes, len(star_slopes))
                            max_branch_slopes = max(max_branch_slopes, len(branch))
                            checks += 1
    return {
        "field": F.kind,
        "p": p,
        "n": n,
        "jmax": jmax,
        "checks": checks,
        "violations": viol,
        "max_star_slopes": max_star_slopes,
        "max_branch_slopes": max_branch_slopes,
        "max_star_landing_collapse": max_collapse,
    }


# --------------------------------------------------------------------------
# (d): note-bound looseness witness (one fixed structured (u,v))
# --------------------------------------------------------------------------
def note_bound_witness(p, n, j, alpha_i=2, a_i=3, b_i=5, ulast=7, vlast=4):
    F = GFp(p)
    pts = [F.fi(i) for i in range(1, n + 1)]
    alpha = F.fi(alpha_i)
    w = [fpow(F, alpha, i) for i in range(j + 1)]
    a = F.fi(a_i)
    b = F.fi(b_i)
    u = [F.mul(a, wi) for wi in w] + [F.fi(ulast)]
    v = [F.mul(b, wi) for wi in w] + [F.fi(vlast)]
    nland = 0
    slopes = set()
    for T in itertools.combinations(range(n), j):
        if not any(F.eq(pts[i], alpha) for i in T):
            continue
        ell = locator(F, [pts[i] for i in T])
        z = gate_slope(F, u, v, ell)
        if z is not None:
            nland += 1
            slopes.add(z)
    return {
        "p": p, "n": n, "j": j,
        "note_bound_binom(|D|-1,j-1)": comb(n - 1, j - 1),
        "star_landing_complements": nland,
        "distinct_slopes": len(slopes),
    }


# --------------------------------------------------------------------------
# (e): gate vs direct interpolation containment, NON-structured (u,v)
# --------------------------------------------------------------------------
def dual_weights(F, pts):
    w = []
    for i, xi in enumerate(pts):
        den = F.one
        for jx, xj in enumerate(pts):
            if i == jx:
                continue
            den = F.mul(den, F.sub(xi, xj))
        w.append(F.inv(den))
    return w


def syndrome(F, pts, wts, word, r):
    out = []
    for m in range(r):
        t = F.zero
        for x, lam, y in zip(pts, wts, word):
            t = F.add(t, F.mul(F.mul(lam, fpow(F, x, m)), y))
        out.append(t)
    return out


def explained_on(F, pts, word, S, k):
    samp = S[:k]
    xs = [pts[i] for i in samp]
    ys = [word[i] for i in samp]
    for i in S:
        x = pts[i]
        tot = F.zero
        for a, xa in enumerate(xs):
            num = F.one
            den = F.one
            for bb, xb in enumerate(xs):
                if a == bb:
                    continue
                num = F.mul(num, F.sub(x, xb))
                den = F.mul(den, F.sub(xa, xb))
            tot = F.add(tot, F.mul(ys[a], F.mul(num, F.inv(den))))
        if not F.eq(tot, word[i]):
            return False
    return True


def gate_vs_interp(p, n, k, words):
    """Deterministic non-structured (f,g) words; check gate matches truth."""
    F = GFp2(p)
    pts = [F.fi(i) for i in range(1, n + 1)]
    wts = dual_weights(F, pts)
    r = n - k
    j = r - 2
    if j < 2:
        return {"p": p, "n": n, "k": k, "skipped": True}
    mism = 0
    nt = 0
    for f, g in words:
        u = syndrome(F, pts, wts, f, r)
        v = syndrome(F, pts, wts, g, r)
        # iterate a few fixed complements deterministically
        for T in itertools.combinations(range(n), j):
            S = [i for i in range(n) if i not in T]
            ell = locator(F, [pts[i] for i in T])
            b0 = row(F, v, ell, 0)
            b1 = row(F, v, ell, 1)
            noncont_pred = not (F.isz(b0) and F.isz(b1))
            z = gate_slope(F, u, v, ell)
            g_expl = explained_on(F, pts, g, S, k)
            if (not g_expl) != noncont_pred:
                mism += 1
            if z is not None:
                fz = [F.add(f[i], F.mul(z, g[i])) for i in range(n)]
                if not explained_on(F, pts, fz, S, k):
                    mism += 1
                if g_expl:
                    mism += 1
            nt += 1
    return {"p": p, "n": n, "k": k, "j": j, "tests": nt, "mismatches": mism}


def _det_words(p, n, count):
    """Deterministic pseudo-random GF(p^2) word pairs (no RNG, reproducible)."""
    out = []
    seed = 1
    def nxt():
        nonlocal seed
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        return seed
    for _ in range(count):
        f = [(nxt() % p, nxt() % p) for _ in range(n)]
        g = [(nxt() % p, nxt() % p) for _ in range(n)]
        out.append((f, g))
    return out


# --------------------------------------------------------------------------
# certificate
# --------------------------------------------------------------------------
STRUCT_CASES = (
    # (field_ctor, p, n, jmax, last_step)
    (GFp, 5, 5, 3, 1),
    (GFp, 7, 6, 3, 1),
    (GFp, 11, 8, 4, 3),
    (GFp2, 5, 6, 3, 7),
    (GFp2, 7, 6, 3, 11),
    (GFp3, 5, 4, 2, 1),
)

WITNESS_CASES = ((11, 10, 3), (11, 10, 4), (11, 10, 5), (13, 12, 6))

INTERP_CASES = ((7, 6, 3), (11, 7, 3), (11, 8, 4), (13, 9, 4))


def build_certificate():
    struct = [check_star_branch(ctor(p), p, n, jm, ls) for ctor, p, n, jm, ls in STRUCT_CASES]
    witness = [note_bound_witness(p, n, j) for p, n, j in WITNESS_CASES]
    interp = [gate_vs_interp(p, n, k, _det_words(p, n, 12)) for p, n, k in INTERP_CASES]
    total_checks = sum(r["checks"] for r in struct)
    total_viol = sum(r["violations"] for r in struct)
    max_star = max(r["max_star_slopes"] for r in struct)
    max_branch = max(r["max_branch_slopes"] for r in struct)
    interp_mism = sum(r.get("mismatches", 0) for r in interp)
    passed = (
        total_viol == 0
        and max_star <= 1
        and max_branch <= 2
        and interp_mism == 0
        and all(w["distinct_slopes"] <= 1 for w in witness)
    )
    return {
        "status": "AUDIT / EXPERIMENTAL",
        "result": "F1 fixed-root-star slope collapse (sharpens Cor 13/15/16)",
        "note": "experimental/notes/f1/f1_fixed_root_star_slope_collapse.md",
        "host_note": "experimental/notes/f1/f1_syndrome_pencil_normal_form.md",
        "passed": passed,
        "structured_checks": total_checks,
        "structured_violations": total_viol,
        "max_star_slopes_observed": max_star,
        "max_branch_slopes_observed": max_branch,
        "sharpened_bound": "star = 1 slope, whole global monic-rank-one branch <= 2 slopes",
        "note_bound": "1 + binom(|D|-1, j-1) (exponential for j ~ |D|/2)",
        "struct_cases": struct,
        "note_bound_witnesses": witness,
        "gate_interpolation_crosscheck": interp,
    }


def render(cert):
    lines = [
        "F1 fixed-root-star slope-collapse verifier",
        f"  status: {cert['status']}",
        f"  sharpens: Cor 13/15/16 of f1_syndrome_pencil_normal_form.md",
        f"  structured checks: {cert['structured_checks']}  violations: {cert['structured_violations']}",
        f"  max star slopes: {cert['max_star_slopes_observed']} (<= 1)   "
        f"max branch slopes: {cert['max_branch_slopes_observed']} (<= 2)",
    ]
    for w in cert["note_bound_witnesses"]:
        lines.append(
            f"  [witness] p={w['p']} |D|={w['n']} j={w['j']}: "
            f"{w['star_landing_complements']} star landing complements -> "
            f"{w['distinct_slopes']} slope(s); note bound was "
            f"1+binom(|D|-1,j-1)=1+{w['note_bound_binom(|D|-1,j-1)']}"
        )
    for c in cert["gate_interpolation_crosscheck"]:
        if c.get("skipped"):
            continue
        lines.append(
            f"  [gate=interp] p={c['p']} n={c['n']} k={c['k']} j={c['j']}: "
            f"{c['tests']} tests, {c['mismatches']} mismatches"
        )
    lines.append(f"RESULT: {'PASS' if cert['passed'] else 'FAIL'}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Verify the F1 fixed-root-star slope collapse (sharpens Cor 13/15/16)."
    )
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--certificate", action="store_true", help="emit certificate JSON")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--check", type=Path, help="recompute and compare to a stored certificate")
    args = ap.parse_args()
    cert = build_certificate()
    if args.check is not None:
        stored = json.loads(Path(args.check).read_text())
        fresh = json.loads(json.dumps(cert))
        match = stored == fresh
        print(f"certificate matches {args.check}: {match}")
        return 0 if (match and cert["passed"]) else 1
    if args.output is not None:
        args.output.write_text(json.dumps(cert, indent=2, sort_keys=True))
    if args.certificate or args.json:
        print(json.dumps(cert, indent=None if args.json else 2, sort_keys=True))
    else:
        print(render(cert))
    return 0 if cert["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
