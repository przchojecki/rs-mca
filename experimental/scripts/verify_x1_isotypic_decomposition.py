#!/usr/bin/env python3
r"""
Isotypic refinement: how far does confinement-from-stabilizer actually reach?

QUESTION (from x1_confinement_from_stabilizer.md): the confinement theorem needs
U to be zeta-equivariant. Does equivariance hold for ALL words realizing the
QuotientBudget stratum (which would make "L1 = non-confined slope density" an
exact split), or only the extremal (cap / lem:fiber) words?

ANSWER (proved + verified here): NO -- not all. But there is a clean refinement.
Over a K_d-stable support S, ANY function t : S -> F decomposes into d
zeta-isotypic components via the finite-Fourier projection
    t_m(x) = (1/d) sum_{j=0}^{d-1} zeta^{-j m} t(zeta^j x),   t = sum_m t_m,
well-defined because S is K_d-stable and p does not divide d (so 1/d exists).
Each t_m is zeta-equivariant with eigen-character zeta^m, hence by the
confinement theorem interpolates to a FOLDED polynomial X^{r_m} G_m(X^d),
r_m = m mod d. Therefore for ANY received word U and any K_d-stable S in the
fiber,
    P_S(X) = sum_{m=0}^{d-1} X^{r_m} G_m(X^d),
    z_S = P_S(alpha) = sum_{m=0}^{d-1} alpha^{r_m} G_m(alpha^d)
        = a sum of d CONFINED pieces.

CONSEQUENCES (honest):
  * U single-isotypic (equivariant)  => z_S is ONE folded term => CONFINED.
    (lem:fiber / cap words are this case.)
  * U general                        => z_S is a sum of d confined pieces,
    which need NOT be confined. So the combinatorial QuotientBudget/Q_1 split
    does NOT exactly equal the slope confined/non-confined split; confinement is
    a per-CHARACTER statement, exact only on the equivariant stratum.

So "L1 = non-confined MCA-bad-slope density" is rigorous on the equivariant
words (which carry the cap mass), but the general alignment is per-isotypic --
a finer statement than the naive stabilizer split. This guards the unifying
picture against overclaiming.

Checks (exact F_{17^2}, d=4, K_d-stable S):
  (1) t = sum_m t_m  (isotypic projections reconstruct the data);
  (2) each t_m is equivariant: t_m(zeta x) = zeta^m t_m(x);
  (3) each interpolant P^{(m)} is folded at i == m mod d;
  (4) P_S = sum_m P^{(m)}  (full interpolant = sum of folded pieces);
  (5) z_S = sum_m alpha^{r_m} G_m(alpha^d);
  (6) single-isotypic data => z_S confined (in B) when alpha^d in B;
  (7) WITNESS: a genuinely 2-isotypic data set on the SAME S gives a
      NON-confined slope (z_S not in B) at alpha^d in B -- so the QuotientBudget
      is not entirely confined for general U.

Status: AUDIT / PROVED (isotypic decomposition) + verified; refines the
confine<=>stabilizer correspondence.

Run:
    python3 experimental/scripts/verify_x1_isotypic_decomposition.py
    python3 experimental/scripts/verify_x1_isotypic_decomposition.py --json
"""

from __future__ import annotations

import argparse
import json


class GF:
    def __init__(self, p, g): self.p, self.g = p, g
    def add(self, a, b): return ((a[0]+b[0]) % self.p, (a[1]+b[1]) % self.p)
    def sub(self, a, b): return ((a[0]-b[0]) % self.p, (a[1]-b[1]) % self.p)
    def mul(self, a, b):
        p, g = self.p, self.g
        return ((a[0]*b[0]+a[1]*b[1]*g) % p, (a[0]*b[1]+a[1]*b[0]) % p)
    def inv(self, a):
        p, g = self.p, self.g
        nrm = (a[0]*a[0]-a[1]*a[1]*g) % p
        ni = pow(nrm, p-2, p)
        return ((a[0]*ni) % p, ((-a[1])*ni) % p)
    def pw(self, a, e):
        r = (1, 0); b = a
        while e > 0:
            if e & 1: r = self.mul(r, b)
            b = self.mul(b, b); e >>= 1
        return r
    def base(self, u): return (u % self.p, 0)
    def is_zero(self, a): return a[0] % self.p == 0 and a[1] % self.p == 0
    def eq(self, a, b): return self.sub(a, b) == (0, 0)
    def in_B(self, a): return a[1] % self.p == 0
    def scal(self, a, s): return ((a[0]*s) % self.p, (a[1]*s) % self.p)


def is_nonsquare(g, p): return pow(g % p, (p-1)//2, p) == p-1


def poly_eval(F, c, x):
    acc = (0, 0)
    for cc in reversed(c): acc = F.add(F.mul(acc, x), cc)
    return acc


def lagrange(F, xs, ys):
    npt = len(xs); acc = [(0, 0)]*npt
    for i in range(npt):
        num = [(1, 0)]; den = (1, 0)
        for m in range(npt):
            if m != i:
                nxt = [(0, 0)]*(len(num)+1); negx = F.sub((0, 0), xs[m])
                for j, c in enumerate(num):
                    nxt[j] = F.add(nxt[j], F.mul(c, negx)); nxt[j+1] = F.add(nxt[j+1], c)
                num = nxt; den = F.mul(den, F.sub(xs[i], xs[m]))
        scale = F.mul(ys[i], F.inv(den))
        for j in range(len(num)): acc[j] = F.add(acc[j], F.mul(num[j], scale))
    while len(acc) > 1 and F.is_zero(acc[-1]): acc.pop()
    return acc


def isotypic(F, S, data, zeta, d, m, dinv):
    """t_m(x) = (1/d) sum_j zeta^{-jm} t(zeta^j x), over x in S (K_d-stable)."""
    idx = {x: i for i, x in enumerate(S)}
    out = {}
    for x in S:
        acc = (0, 0)
        xj = x
        for j in range(d):
            coef = F.pw(zeta, (-j*m) % d)
            acc = F.add(acc, F.mul(coef, data[idx[xj]]))
            xj = F.mul(zeta, xj)
        out[x] = F.scal(acc, dinv)
    return out


def folded_at(F, P, r, d):
    return all(F.is_zero(P[i]) for i in range(len(P)) if i % d != r)


def run():
    p = 17
    g = next(x for x in range(2, p) if is_nonsquare(x, p))
    F = GF(p, g)
    n, d, k = 16, 4, 8
    dinv = pow(d, p-2, p)
    # omega gen of order-16 subgroup of F_17^*; zeta primitive 4th root (in B)
    omega = next((c, 0) for c in range(2, p) if pow(c, n, p) == 1 and pow(c, n//2, p) != 1)
    zeta = F.pw(omega, n//d)
    # K_d-stable S: two zeta-orbits (size d each) -> |S|=8=k
    reps = [F.pw(omega, 1), F.pw(omega, 2)]
    S = []
    for rep in reps:
        xj = rep
        for _ in range(d):
            S.append(xj); xj = F.mul(zeta, xj)
    # pole alpha NOT in B but alpha^d in B: the field generator t=(0,1) has
    # t^2 = g in B, so t^4 = g^2 in B, while t not in B. This is the regime where
    # confinement is nontrivial (alpha in B would make everything trivially in B).
    alpha_B = (0, 1)
    assert F.in_B(F.pw(alpha_B, d)) and not F.in_B(alpha_B)

    def analyze(data):
        P = lagrange(F, S, data)
        pieces = {}
        recon = [(0, 0)]*len(P)
        sum_t = {x: (0, 0) for x in S}
        equ_ok = True; fold_ok = True
        zS_pieces = (0, 0)
        for m in range(d):
            tm = isotypic(F, S, data, zeta, d, m, dinv)
            for x in S: sum_t[x] = F.add(sum_t[x], tm[x])
            # equivariance of t_m
            for x in S:
                if not F.eq(tm[F.mul(zeta, x)], F.mul(F.pw(zeta, m), tm[x])):
                    equ_ok = False
            Pm = lagrange(F, S, [tm[x] for x in S])
            r = m % d
            if not folded_at(F, Pm, r, d): fold_ok = False
            for i in range(len(Pm)):
                if i < len(recon): recon[i] = F.add(recon[i], Pm[i])
                else: recon.append(Pm[i])
            # z piece = alpha^r G_m(alpha^d)
            Gm = [Pm[i] for i in range(r, len(Pm), d)]
            zS_pieces = F.add(zS_pieces, F.mul(F.pw(alpha_B, r), poly_eval(F, Gm, F.pw(alpha_B, d))))
        while len(recon) > 1 and F.is_zero(recon[-1]): recon.pop()
        data_sum_ok = all(F.eq(sum_t[x], data[i]) for i, x in enumerate(S))
        P_sum_ok = (len(recon) == len(P)) and all(F.eq(recon[i], P[i]) for i in range(len(P)))
        zS = poly_eval(F, P, alpha_B)
        z_formula_ok = F.eq(zS, zS_pieces)
        return {"P": P, "data_sum_ok": data_sum_ok, "equ_ok": equ_ok,
                "fold_ok": fold_ok, "P_sum_ok": P_sum_ok, "z_formula_ok": z_formula_ok,
                "zS_in_B": F.in_B(zS)}

    # Sweep B-valued amplitudes (robust to accidental cancellations).
    # (a) single-isotypic m=0 (constant on each orbit): z_S must ALWAYS be in B.
    # (b) mixed m=0+m=1 (t = ta + tb*zeta^j): z_S escapes B for SOME amplitudes
    #     (existence witness that the QuotientBudget is not entirely confined).
    single_all_confined = True
    res_eq = None
    for a1 in range(1, p):
        for a2 in range(1, p):
            data = []
            for ridx, rep in enumerate(reps):
                t0 = F.base(a1 if ridx == 0 else a2)
                data += [t0] * d
            r = analyze(data)
            res_eq = res_eq or r
            if not r["zS_in_B"]:
                single_all_confined = False
    mixed_escapes = False
    res_mix = None
    for a1 in range(0, p):
        for b1 in range(1, p):
            data = []
            for ridx, rep in enumerate(reps):
                ta = F.base(a1 if ridx == 0 else (a1 + 2) % p)
                tb = F.base(b1 if ridx == 0 else (b1 + 1) % p)
                for j in range(d):
                    data.append(F.add(ta, F.mul(F.pw(zeta, j % d), tb)))
            r = analyze(data)
            res_mix = res_mix or r
            if not r["zS_in_B"]:
                mixed_escapes = True
                res_mix = r
                break
        if mixed_escapes:
            break

    checks = {
        "isotypic identity: data = sum_m t_m": res_eq["data_sum_ok"] and res_mix["data_sum_ok"],
        "components equivariant (t_m(zeta x)=zeta^m t_m(x))": res_eq["equ_ok"],
        "each component interpolant folded at i==m mod d": res_eq["fold_ok"] and res_mix["fold_ok"],
        "P_S = sum of folded pieces": res_eq["P_sum_ok"] and res_mix["P_sum_ok"],
        "z_S = sum_m alpha^r G_m(alpha^d)": res_eq["z_formula_ok"] and res_mix["z_formula_ok"],
        "single-isotypic m=0: z_S ALWAYS confined (in B), all amplitudes":
            single_all_confined,
        "mixed: z_S escapes B for some amplitudes (QuotientBudget not all confined)":
            mixed_escapes,
    }
    return {"all_ok": all(checks.values()), "checks": checks,
            "single_isotypic_always_confined": single_all_confined,
            "mixed_can_escape_B": mixed_escapes}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("Isotypic refinement of confinement-from-stabilizer (F_17^2, d=4, K_d-stable S):")
    print("  Any periodic-support interpolant = sum of d folded (confined) pieces.")
    print(f"  single-isotypic m=0 word: z_S always confined (in B)? {out['single_isotypic_always_confined']}")
    print(f"  genuinely 2-isotypic word: z_S can escape B?          {out['mixed_can_escape_B']}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (isotypic decomposition holds; confinement is per-character, "
          "exact only on the equivariant stratum)" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
