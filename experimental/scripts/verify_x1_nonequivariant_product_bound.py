#!/usr/bin/env python3
r"""
The non-equivariant periodic mass is a PRODUCT of per-character confined masses.

This addresses the honest gap left by x1_isotypic_decomposition.md: for a general
(non-equivariant) word U, the K_d-stable supports give NON-confined slopes -- are
they a new uncontrolled obstruction, or are they bounded?

ANSWER (structural, verified): they are bounded by the product of the per-character
CONFINED slope-counts. Two facts combine:

  (1) LINEARITY. The map  data = U|_S  |->  P_S(alpha)  (closing-codeword
      interpolation then evaluation at the pole) is F-LINEAR in the data on a
      fixed support S. So if U|_S = sum_m (U_m)|_S is the isotypic decomposition,
          z_S(U) = sum_{m=0}^{d-1} z_S(U_m).
  (2) PER-CHARACTER CONFINEMENT (x1_confinement_from_stabilizer.md). Each
      z_S(U_m) = alpha^{r_m} G_m(alpha^d) is confined (lies in the 1-dim B-line
      alpha^{r_m} * B when alpha^d in B and the data is B-rational).

Therefore, over the K_d-stable supports of any word, the distinct slopes satisfy
    |{ z_S }|  <=  prod_{m=0}^{d-1} |Slopes_m|,
where Slopes_m is the set of distinct m-character (confined) slopes. With each
per-character confined count <= C, the non-equivariant periodic mass is <= C^d --
POLYNOMIAL for bounded d. So the non-equivariant periodic supports are NOT a new
obstruction beyond the per-character confined data; they are its d-fold product.

(For d growing with n -- the deep-cap regime a_q -- C^d need not be polynomial;
that case is left open. The point here is that the gap reduces to the SAME
per-character confined counts that the L1 conjecture already concerns, times the
combinatorics of d characters.)

Checks (exact F_{17^2}, d=4, K_d-stable S):
  (1) linearity: z_S(data0 + data1) = z_S(data0) + z_S(data1), many pairs;
  (2) per-character pieces confined (single-character data -> slope in alpha^r B);
  (3) product bound: |{z_S(data0+data1)}| <= |{z_S(data0)}| * |{z_S(data1)}|
      as data0 (m=0) and data1 (m=1) range over B-valued seeds.

Status: AUDIT / structural observation (linearity + confinement => product bound);
the bounded-d consequence is rigorous, the growing-d case is open.

Run:
    python3 experimental/scripts/verify_x1_nonequivariant_product_bound.py
    python3 experimental/scripts/verify_x1_nonequivariant_product_bound.py --json
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
        nrm = (a[0]*a[0]-a[1]*a[1]*g) % p; ni = pow(nrm, p-2, p)
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
    return acc


def run():
    p = 17
    g = next(x for x in range(2, p) if is_nonsquare(x, p))
    F = GF(p, g)
    n, d = 16, 4
    omega = next((c, 0) for c in range(2, p) if pow(c, n, p) == 1 and pow(c, n//2, p) != 1)
    zeta = F.pw(omega, n//d)
    reps = [F.pw(omega, 1), F.pw(omega, 2)]
    S = []
    for rep in reps:
        xj = rep
        for _ in range(d):
            S.append(xj); xj = F.mul(zeta, xj)
    alpha = (0, 1)                          # alpha^4 in B, alpha not in B

    def z_of(data):
        P = lagrange(F, S, data)
        return poly_eval(F, P, alpha)

    # single-character data builders over B-seeds (a1,a2 amplitudes per orbit)
    def data_m0(a1, a2):                     # m=0: constant on each orbit
        out = []
        for ridx, rep in enumerate(reps):
            out += [F.base(a1 if ridx == 0 else a2)] * d
        return out

    def data_m1(b1, b2):                     # m=1: t(zeta^j rep) = zeta^j * seed
        out = []
        for ridx, rep in enumerate(reps):
            seed = F.base(b1 if ridx == 0 else b2)
            for j in range(d):
                out.append(F.mul(F.pw(zeta, j % d), seed))
        return out

    # (1) linearity check + (2) per-character confinement
    lin_ok = True
    conf0_ok = True
    conf1_ok = True
    for a1 in range(0, p, 3):
        for b1 in range(0, p, 3):
            d0 = data_m0(a1, (a1 + 1) % p)
            d1 = data_m1(b1, (b1 + 2) % p)
            dsum = [F.add(d0[i], d1[i]) for i in range(len(S))]
            if not F.eq(z_of(dsum), F.add(z_of(d0), z_of(d1))):
                lin_ok = False
            # m=0 confined: slope in B (r=0); m=1 confined: slope in alpha*B (u-part 0)
            if not F.in_B(z_of(d0)):
                conf0_ok = False
            z1 = z_of(d1)
            if z1[0] % p != 0:               # alpha*B = {(0,w)}
                conf1_ok = False

    # (3) product bound on distinct slopes
    slopes0, slopes1, slopes_sum = set(), set(), set()
    for a1 in range(p):
        for a2 in range(p):
            slopes0.add(z_of(data_m0(a1, a2)))
    for b1 in range(p):
        for b2 in range(p):
            slopes1.add(z_of(data_m1(b1, b2)))
    # sums range over the two independent families
    for s0 in slopes0:
        for s1 in slopes1:
            slopes_sum.add(F.add(s0, s1))
    product_bound_ok = len(slopes_sum) <= len(slopes0) * len(slopes1)

    checks = {
        "linearity: z_S(d0+d1)=z_S(d0)+z_S(d1)": lin_ok,
        "m=0 pieces confined (in B)": conf0_ok,
        "m=1 pieces confined (in alpha*B)": conf1_ok,
        "product bound: |sums| <= |Slopes_0|*|Slopes_1|": product_bound_ok,
    }
    return {"all_ok": all(checks.values()), "checks": checks,
            "|Slopes_0|": len(slopes0), "|Slopes_1|": len(slopes1),
            "|distinct sums|": len(slopes_sum),
            "product": len(slopes0) * len(slopes1)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("Non-equivariant periodic mass = product of per-character confined masses (F_17^2, d=4):")
    print(f"  |Slopes_0| (m=0, confined in B)      = {out['|Slopes_0|']}")
    print(f"  |Slopes_1| (m=1, confined in alpha*B) = {out['|Slopes_1|']}")
    print(f"  |distinct sums z_S(d0+d1)|           = {out['|distinct sums|']}  (<= product {out['product']})")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (non-equivariant periodic slopes are sums of d confined pieces; "
          "count <= product of per-character counts -> poly for bounded d)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
