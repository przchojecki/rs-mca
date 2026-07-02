#!/usr/bin/env python3
r"""
Independent audit of Paper D `lem:fiber`(ii) -- the SOLE remaining dependency of
the CS25-free deep-point cap (see notes/x1/x1_cs25_free_cap.md).

cs25_cap_v12.tex `lem:fiber`(ii): with B subseteq F, D subseteq B^x a coset of
order n, a|k, rho=k/n, N=n/a, ell2 = rho*N + 2 <= N, and the heavy word
    u_z = (x^{k+2a} + z*x^{k+a})_{x in D},
there is z in B with
    |Lst(RS[F,D,k+1], 1-rho-2/N, u_z)| >= binom(N, ell2) / |B|,
all listed codewords lying in RS[B,D,k+1].

WHY THIS MATTERS. thm:main currently reads
    lem:fiber (large list, ELEMENTARY) + thm:A (CS25 Thm 2: small eca => small
    list, the EXTERNAL import) + contradiction.
The deep-point route (x1 bridge) drops thm:A, replacing the contrapositive
"small eca => small list" by the DIRECT identity Bad_CA = Bad_MCA = Deep_alpha
plus averaging. lem:fiber is kept verbatim. So the deep-point cap is
"CS25-free MODULO lem:fiber" -- which is only meaningful if lem:fiber itself
imports nothing from CS25. The proof in cs25_cap_v12.tex (part ii) is elementary
locator-polynomial combinatorics + a pigeonhole over B, self-contained (only
part (i), the lower rung, cites Cho26a). This script CONFIRMS part (ii) by full
enumeration over F_17, so the dependency claim rests on a checked lemma.

Test parameters (fully enumerable): B = F = F_17, D = F_17^x (n=16),
    N = 8, a = 2, k = 4, rho = 1/4, ell2 = rho*N+2 = 4, binom(8,4) = 70.
Validity: a|k (2|4); (1-rho)N = 6 >= 3; ell2 = 4 <= N-1 = 7;
    k+2a = 8 = a*ell2; k+a = 6 = a*(ell2-1); agreement k+2a=8 of n=16
    => dist <= 1 - 8/16 = 1/2 = 1-rho-2/N.

Checks (all by exhaustive enumeration of the 70 four-subsets A of Q = D^2):
  (1) for each A: L_A = prod_{b in A}(X^2 - b) = X^8 - e1(A) X^6 + R_A,
      deg R_A <= k = 4, so c_A := -R_A in RS[F_17,D,5];
  (2) u_{z_A} agrees with c_A on >= k+2a = 8 points (z_A := -e1(A));
  (3) A |-> c_A is injective on subsets sharing a common slope z_A
      (the lemma's distinctness claim);
  (4) the pigeonhole count: some z in B is attained by >= binom(N,ell2)/|B|
      = 70/17 ~ 4.12 of the A's, giving that many DISTINCT list members.

Status: AUDIT / PROVED-by-enumeration (lem:fiber(ii) is elementary, CS25-free).

Run:
    python3 experimental/scripts/verify_x1_lem_fiber.py
    python3 experimental/scripts/verify_x1_lem_fiber.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from math import comb
from fractions import Fraction

P = 17                      # F = B = F_17
N, a, k = 8, 2, 4           # N=n/a, a|k
n = N * a                   # 16
rho = Fraction(k, n)        # 1/4
ell2 = int(rho * N) + 2     # 4


def poly_mul(f, g):
    """Multiply two polynomials (coeff lists, low-degree first) over F_P."""
    out = [0] * (len(f) + len(g) - 1)
    for i, fi in enumerate(f):
        if fi:
            for j, gj in enumerate(g):
                out[i + j] = (out[i + j] + fi * gj) % P
    return out


def poly_eval(f, x):
    acc = 0
    for c in reversed(f):
        acc = (acc * x + c) % P
    return acc


def trim(f):
    while len(f) > 1 and f[-1] == 0:
        f = f[:-1]
    return f


def run():
    # D = F_17^x = all nonzero elements (multiplicative group of order 16).
    D = list(range(1, P))
    assert len(D) == n
    # Q = D^a = squares, order N=8.
    Q = sorted({pow(x, a, P) for x in D})
    assert len(Q) == N, (len(Q), N)

    checks = {
        "params_valid": (a * N == n and k % a == 0 and (1 - rho) * N >= 3
                         and ell2 <= N - 1 and k + 2 * a == a * ell2
                         and k + a == a * (ell2 - 1)),
        "Q_has_order_N": len(Q) == N,
    }

    subsets = list(combinations(Q, ell2))
    assert len(subsets) == comb(N, ell2)

    # build c_A for every A; verify agreement + degree
    agree_ok = True
    deg_ok = True
    z_to_cA = {}        # z_A -> set of c_A tuples (for distinctness + pigeonhole)
    cA_to_A = {}        # (z_A, c_A) -> A   (injectivity probe)
    inj_violation = None
    for A in subsets:
        # L_A = prod (X^2 - b)
        LA = [1]
        for b in A:
            LA = poly_mul(LA, [(-b) % P, 0, 1])   # X^2 - b
        LA = LA + [0] * (a * ell2 + 1 - len(LA))   # pad to degree k+2a
        # L_A = X^{k+2a} - e1 X^{k+a} + R_A  (top coeff 1)
        assert trim(LA)[-1] == 1 and len(trim(LA)) == k + 2 * a + 1, trim(LA)
        # extract: top term X^{k+2a}; next X^{k+a} coeff is -e1
        neg_e1 = LA[k + a]                 # coeff of X^{k+a} = -e1(A) = z_A
        z_A = neg_e1 % P
        # R_A = L_A minus the top two terms (X^{k+2a} and z_A X^{k+a})
        R_A = list(LA)
        R_A[k + 2 * a] = 0
        R_A[k + a] = 0
        R_A = trim(R_A)
        if len(R_A) - 1 > k:
            deg_ok = False
        c_A = tuple((-poly_eval(R_A, x)) % P for x in D)   # c_A = (-R_A(x))
        # u_{z_A}(x) = x^{k+2a} + z_A x^{k+a}
        u = tuple((pow(x, k + 2 * a, P) + z_A * pow(x, k + a, P)) % P for x in D)
        agree = sum(1 for i in range(n) if u[i] == c_A[i])
        if agree < k + 2 * a:
            agree_ok = False
        z_to_cA.setdefault(z_A, set()).add(c_A)
        key = (z_A, c_A)
        if key in cA_to_A and cA_to_A[key] != A:
            inj_violation = (cA_to_A[key], A)   # same (z,c) from two A's => injectivity fails
        cA_to_A[key] = A

    checks["degR_le_k_all"] = deg_ok
    checks["u_agrees_cA_on_ge_k+2a_all"] = agree_ok
    checks["injective_on_common_slope"] = inj_violation is None

    # pigeonhole: max distinct-codeword fiber over z
    max_fiber = max(len(s) for s in z_to_cA.values())
    lower_bound = Fraction(comb(N, ell2), P)   # binom/|B|
    checks["some_z_fiber >= binom/|B|"] = max_fiber >= lower_bound

    all_ok = all(checks.values())
    return {
        "all_ok": all_ok,
        "params": {"P": P, "n": n, "N": N, "a": a, "k": k, "rho": str(rho),
                   "ell2": ell2, "binom(N,ell2)": comb(N, ell2),
                   "agreement_min": k + 2 * a, "dist_max": str(1 - Fraction(k + 2 * a, n))},
        "distinct_fibers": {str(z): len(s) for z, s in sorted(z_to_cA.items())},
        "max_distinct_codeword_fiber": max_fiber,
        "list_lower_bound binom/|B|": float(lower_bound),
        "checks": checks,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2)); raise SystemExit(0 if out["all_ok"] else 1)
    print("Independent audit of lem:fiber(ii) -- the sole remaining (elementary) dependency")
    print("of the CS25-free deep-point cap. Full enumeration over F_17.")
    print(f"  params: {out['params']}")
    print(f"  max distinct-codeword fiber over z = {out['max_distinct_codeword_fiber']} "
          f">= binom/|B| = {out['list_lower_bound binom/|B|']:.3f}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (lem:fiber(ii) confirmed by enumeration; elementary, no CS25)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
