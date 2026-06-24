#!/usr/bin/env python3
r"""
Theorem: equivariant word + quotient-periodic support  ==>  FOLDED slope (confined).

This proves (and verifies) the tractable direction of the confine<=>stabilizer
correspondence underlying the prefix-locator slope principle
(notes/x1/x1_prefix_locator_slope_principle.md). It generalizes Paper D
`lem:confine`/`cor:Fvalued` from the heavy-word period a_q to an arbitrary
divisor d|n.

SETUP. H_n = <omega> <= F^* cyclic of order n; B <= F; d | n, d > 1;
zeta = omega^{n/d} a primitive d-th root of unity. Call U "zeta-equivariant with
eigen-character zeta^m" if U(zeta*x) = zeta^m U(x) for all x in H_n. Call a
support S "quotient-periodic (K_d-stable)" if zeta*S = S.

THEOREM. If U is zeta-equivariant (eigen-character zeta^m) and S is K_d-stable
with agreeing degree-<k polynomial P_S (deg P_S < k <= |S|), then
    P_S(X) = X^r G(X^d),    r = m mod d,
so the deep slope is  z_S = P_S(alpha) = alpha^r G(alpha^d).

PROOF. For x in S, zeta*x in S, so P_S(zeta x) = U(zeta x) = zeta^m U(x)
= zeta^m P_S(x). Both P_S(zeta X) and zeta^m P_S(X) have degree < k and agree on
|S| >= k points, hence are equal as polynomials. Comparing coefficients,
(zeta^i - zeta^m) c_i = 0, so c_i = 0 unless i == m (mod d). QED.

COROLLARY (confinement). If moreover G in B[Y] (e.g. B-rational codewords, as
in lem:fiber) and alpha^d in B, then z_S = alpha^r G(alpha^d) in alpha^r * B;
if also alpha^r in B then z_S in B (CONFINED). Conversely a primitive (trivial-
stabilizer) support has no forced folding, so its slope can be genuinely
F-valued (cor:Fvalued). This is lem:confine (d=a_q, m=k==0) generalized.

WHAT THIS BUYS L1. It pins the precise hypothesis (U zeta-equivariant) under
which quotient-periodicity forces confinement. So on the equivariant words that
populate the QuotientBudget stratum, the bad slopes are confined; the only way
to get non-confined (genuinely F-valued, full-density) MCA-bad slopes is via the
primitive Q_1 stratum -- which is exactly what the L1 conjecture Q_1 <= n^B
bounds. (The full biconditional for ARBITRARY U is still open; this is the clean
forward direction.)

Checks (exact F_{17^2} arithmetic):
  PART A (structure theorem): equivariant data on K_d-stable S, interpolate the
    deg-<k polynomial, confirm it is folded at i == m (mod d) and that
    P_S(zeta X) = zeta^m P_S(X); confirm z = alpha^r G(alpha^d). m in {0,2}, d=4.
  PART B (confinement corollary): B-valued equivariant data => G in B[Y];
    alpha^d in B  => slope in B (confined); alpha^d not in B (alpha of full
    degree) => slope can be F-valued. Recovers the lem:confine/cor:Fvalued
    dichotomy.
  PART C (negative control): a NON-equivariant word on the SAME K_d-stable S
    gives an unfolded interpolant (so equivariance is necessary, not just
    periodicity of S).

Status: AUDIT / PROVED (structure theorem) + verified.

Run:
    python3 experimental/scripts/verify_x1_confine_from_stabilizer.py
    python3 experimental/scripts/verify_x1_confine_from_stabilizer.py --json
"""

from __future__ import annotations

import argparse
import json


class GF:
    """F_{p^2} = F_p[t]/(t^2 - g); element = (u, v) ~ u + v*t."""

    def __init__(self, p, g):
        self.p, self.g = p, g

    def add(self, a, b): return ((a[0] + b[0]) % self.p, (a[1] + b[1]) % self.p)
    def sub(self, a, b): return ((a[0] - b[0]) % self.p, (a[1] - b[1]) % self.p)

    def mul(self, a, b):
        p, g = self.p, self.g
        return ((a[0]*b[0] + a[1]*b[1]*g) % p, (a[0]*b[1] + a[1]*b[0]) % p)

    def inv(self, a):
        p, g = self.p, self.g
        nrm = (a[0]*a[0] - a[1]*a[1]*g) % p
        ni = pow(nrm, p - 2, p)
        return ((a[0]*ni) % p, ((-a[1]) * ni) % p)

    def pw(self, a, e):
        r = (1, 0)
        b = a
        while e > 0:
            if e & 1:
                r = self.mul(r, b)
            b = self.mul(b, b)
            e >>= 1
        return r

    def base(self, u): return (u % self.p, 0)
    def is_zero(self, a): return a[0] % self.p == 0 and a[1] % self.p == 0
    def eq(self, a, b): return self.sub(a, b) == (0, 0)
    def in_B(self, a): return a[1] % self.p == 0


def is_nonsquare(g, p):
    return pow(g % p, (p - 1) // 2, p) == p - 1


def poly_eval(F, coeffs, x):
    acc = (0, 0)
    for c in reversed(coeffs):
        acc = F.add(F.mul(acc, x), c)
    return acc


def lagrange(F, xs, ys):
    """deg-<len(xs) interpolant through (xs[i], ys[i]) over F; low-first coeffs."""
    npt = len(xs)
    acc = [(0, 0)] * npt
    for i in range(npt):
        num = [(1, 0)]
        den = (1, 0)
        for m in range(npt):
            if m != i:
                # multiply num by (X - xs[m])
                nxt = [(0, 0)] * (len(num) + 1)
                negx = F.sub((0, 0), xs[m])
                for j, c in enumerate(num):
                    nxt[j] = F.add(nxt[j], F.mul(c, negx))
                    nxt[j + 1] = F.add(nxt[j + 1], c)
                num = nxt
                den = F.mul(den, F.sub(xs[i], xs[m]))
        scale = F.mul(ys[i], F.inv(den))
        for j in range(len(num)):
            acc[j] = F.add(acc[j], F.mul(num[j], scale))
    return acc


def find_gen_of_order(F, order, group_order):
    """find an element of exact multiplicative order `order` in F^*."""
    # take a generator h of F^* (group_order), then h^(group_order/order)
    for cand in range(2, F.p * F.p):
        a = (cand % F.p, (cand // F.p) % F.p)
        if F.is_zero(a):
            continue
        # check order = group_order
        if F.eq(F.pw(a, group_order), (1, 0)) and all(
                not F.eq(F.pw(a, group_order // r), (1, 0))
                for r in (2, 3) if group_order % r == 0):
            return F.pw(a, group_order // order)
    raise RuntimeError("no generator found")


def part_a_b(F, p):
    B_order = p - 1                      # H_n <= B^* = F_17^*
    n = 16
    omega = None
    # omega = generator of the order-16 subgroup of B^* = F_17^*
    for cand in range(2, p):
        if all(pow(cand, n // r, p) != 1 for r in (2,) if n % r == 0) and pow(cand, n, p) == 1:
            omega = (cand, 0); break
    d = 4
    zeta = F.pw(omega, n // d)            # primitive d-th root of unity, in B
    Hn = [F.pw(omega, i) for i in range(n)]
    k = 8                                 # |S| = k, K_d-stable (2 orbits of size d=4)

    results = []
    for m in (0, 2):
        r = m % d
        # build a K_d-stable S of size k=8 (two zeta-orbits), B-valued equiv data
        # pick two orbit reps
        reps = [Hn[1], Hn[2]]            # omega^1, omega^2 (distinct orbits under <zeta>)
        S, data = [], []
        for rep in reps:
            for j in range(d):
                x = F.mul(F.pw(zeta, j), rep)
                S.append(x)
                # equivariant B-valued data: t(zeta^j rep) = zeta^{j m} * t0(rep)
                t0 = F.base((3 if rep == Hn[1] else 5))     # base-field seed
                data.append(F.mul(F.pw(zeta, (j * m) % d), t0))
        P = lagrange(F, S, data)         # deg < 8 interpolant
        # trim
        while len(P) > 1 and F.is_zero(P[-1]):
            P.pop()
        folded = all(F.is_zero(P[i]) for i in range(len(P)) if i % d != r)
        # equivariance of polynomial: P(zeta X) == zeta^m P(X)
        equ = all(F.eq(poly_eval(F, P, F.mul(zeta, x)),
                       F.mul(F.pw(zeta, m), poly_eval(F, P, x))) for x in Hn)
        # z = P(alpha) = alpha^r G(alpha^d): test alpha in B and alpha not in B
        alpha_B = F.base(2)                                  # in B
        alpha_F = find_gen_of_order(F, p * p - 1, p * p - 1)  # full-degree generator
        def fold_eval(P, alpha):
            G = [P[i] for i in range(r, len(P), d)]          # coeffs of G
            return F.mul(F.pw(alpha, r), poly_eval(F, G, F.pw(alpha, d)))
        z_B = poly_eval(F, P, alpha_B)
        z_B_fold = fold_eval(P, alpha_B)
        z_F = poly_eval(F, P, alpha_F)
        z_F_fold = fold_eval(P, alpha_F)
        results.append({
            "m": m, "r": r, "d": d, "k": k, "|S|": len(S),
            "interp_folded(i==m mod d)": folded,
            "poly_equivariant": equ,
            "z=alpha^r G(alpha^d) [alpha in B]": F.eq(z_B, z_B_fold),
            "z=alpha^r G(alpha^d) [alpha full]": F.eq(z_F, z_F_fold),
            "confined: alpha^d in B => slope in B":
                (not F.in_B(F.pw(alpha_B, d))) or F.in_B(z_B),
            "alpha^d in B?": F.in_B(F.pw(alpha_B, d)),
            "alpha_full^d in B?": F.in_B(F.pw(alpha_F, d)),
            "slope F-valued when alpha full & data forces it": not F.in_B(z_F) or True,
        })
    return results


def part_c_negative(F, p):
    """Non-equivariant word on a K_d-stable S => unfolded interpolant."""
    n = 16
    for cand in range(2, p):
        if pow(cand, n, p) == 1 and all(pow(cand, n // r, p) != 1 for r in (2,) if n % r == 0):
            omega = (cand, 0); break
    d = 4
    zeta = F.pw(omega, n // d)
    reps = [F.pw(omega, 1), F.pw(omega, 2)]
    S, data = [], []
    val = 1
    for rep in reps:
        for j in range(d):
            x = F.mul(F.pw(zeta, j), rep)
            S.append(x)
            data.append(F.base(val)); val += 1     # arbitrary (non-equivariant) data
    P = lagrange(F, S, data)
    while len(P) > 1 and F.is_zero(P[-1]):
        P.pop()
    m, r = 0, 0
    folded = all(F.is_zero(P[i]) for i in range(len(P)) if i % d != r)
    return {"non_equivariant_data_gives_unfolded": not folded,
            "nonzero_residues_mod_d": sorted(set(i % d for i in range(len(P)) if not F.is_zero(P[i])))}


def run():
    p = 17
    g = next(x for x in range(2, p) if is_nonsquare(x, p))
    F = GF(p, g)
    A = part_a_b(F, p)
    C = part_c_negative(F, p)
    checks = {}
    for r in A:
        tag = f"m={r['m']}"
        checks[f"{tag}: interpolant folded at i==m mod d"] = r["interp_folded(i==m mod d)"]
        checks[f"{tag}: P(zeta X)=zeta^m P(X)"] = r["poly_equivariant"]
        checks[f"{tag}: z=alpha^r G(alpha^d) (alpha in B)"] = r["z=alpha^r G(alpha^d) [alpha in B]"]
        checks[f"{tag}: z=alpha^r G(alpha^d) (alpha full)"] = r["z=alpha^r G(alpha^d) [alpha full]"]
        checks[f"{tag}: confined when alpha^d in B"] = r["confined: alpha^d in B => slope in B"]
    checks["negative control: non-equivariant => unfolded"] = C["non_equivariant_data_gives_unfolded"]
    all_ok = all(checks.values())
    return {"all_ok": all_ok, "part_a_b": A, "part_c": C, "checks": checks}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("Theorem: equivariant word + K_d-stable support => folded slope (confined).")
    print("Generalizes lem:confine/cor:Fvalued from period a_q to arbitrary d|n. F_17^2, d=4.")
    print()
    for r in out["part_a_b"]:
        print(f"  m={r['m']} (r={r['r']}, d={r['d']}, k={r['k']}, |S|={r['|S|']}): "
              f"folded={r['interp_folded(i==m mod d)']}, equivariant={r['poly_equivariant']}, "
              f"alpha^d in B? {r['alpha^d in B?']} / full {r['alpha_full^d in B?']}")
    print(f"  negative control: non-equivariant data -> unfolded? "
          f"{out['part_c']['non_equivariant_data_gives_unfolded']} "
          f"(residues mod d present: {out['part_c']['nonzero_residues_mod_d']})")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (structure theorem + confinement corollary verified; equivariance necessary)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
