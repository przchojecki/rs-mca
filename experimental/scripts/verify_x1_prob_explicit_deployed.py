#!/usr/bin/env python3
r"""
prob:explicit at cor:deployed parameters -- the deployed-scale density arithmetic.

Companion to `verify_x1_prob_explicit_mechanism.py` (which validates the
deep-point bad-slope = deep-image mechanism, the F-valued/confine dichotomy
alpha^{a_q} in/notin B, and the averaging count on a small F_{p^2} model).

Here we do the exact big-integer arithmetic at Paper D's `cor:deployed`
parameters and show the explicit deep-point line clears the `prob:explicit`
density `2^-22`, via the deep-point bridge (not the CS25 conversion).

Parameters (cs25_cap_v12.tex cor:deployed; ABF 6.3):
    B = F_p, p = 2^31 - 2^24 + 1 (KoalaBear);  F = F_{p^6}, q = p^6 ~ 2^185.93;
    D = order-n subgroup, n = 2^21;  k = 2^20;  rho = 1/2;  gap 2^-7.
    lem:fiber(ii): N = n/a_q with gap 2/N = 2^-7 => N = 256, a_q = 2^13, ell2 = 130;
    heavy word u_z = x^{k+2a_q} + z x^{k+a_q}; list L >= binom(N,ell2)/|B| (RS[F,D,k+1]).

Explicit line: f = u_z/(x-alpha), g = -1/(x-alpha), alpha a degree-6 generator of
F_{p^6} (so alpha^{a_q} keeps full degree 6, since v2(p^6-1)=25 >= 13; slopes are
genuinely F-valued, non-B-rational). Bad slopes = deep image {P(alpha)}, size M.

Averaging expansion (avdeevvadim Lemma 2.1):
    best alpha:        M >= L/(1 + k(L-1)/|Omega|)             (|Omega| = q - n);
    >= half of alpha:  M >= L/(1 + 2k(L-1)/|Omega|)  (Markov on collision count).
Density = M/q. We check both clear 2^-22.

Status: AUDIT / PROVED-by-arithmetic (deployed-scale density).

Run:
    python3 experimental/scripts/verify_x1_prob_explicit_deployed.py
    python3 experimental/scripts/verify_x1_prob_explicit_deployed.py --json
"""

from __future__ import annotations

import argparse
import json
from math import comb, log2
from fractions import Fraction


def run():
    p = 2**31 - 2**24 + 1
    q = p**6
    n, k = 2**21, 2**20
    N = 256
    a_q = n // N
    ell2 = N // 2 + 2
    assert a_q * N == n and k % a_q == 0 and a_q == 2**13
    gap = Fraction(2, N)
    # v2(p^6-1) >= log2(a_q): alpha^{a_q} keeps full degree 6 for a generator alpha
    v2 = 0
    t = q - 1
    while t % 2 == 0:
        v2 += 1; t //= 2
    L = comb(N, ell2) // p                      # lem:fiber(ii) list lower bound
    Omega = q - n
    M_best = Fraction(L, 1) / (1 + Fraction(k * (L - 1), Omega))
    M_half = Fraction(L, 1) / (1 + Fraction(2 * k * (L - 1), Omega))
    d_best = M_best / q
    d_half = M_half / q
    target = Fraction(1, 2**22)

    checks = {
        "gap_is_2^-7": gap == Fraction(1, 2**7),
        "alpha^aq_keeps_degree6 (v2(q-1) >= 13)": v2 >= 13,
        "best_alpha_clears_2^-22": d_best > target,
        "half_of_alpha_clears_2^-22": d_half > target,
        "matches_cor_deployed_1/k": abs(log2(float(d_best)) - (-(k.bit_length()-1))) < 1.5,
    }
    all_ok = all(checks.values())
    return {
        "all_ok": all_ok,
        "params": {"p": p, "q~2^": round(log2(q), 2), "n": "2^21", "k": "2^20",
                   "N": N, "a_q": "2^13", "ell2": ell2, "gap": "2^-7",
                   "v2(q-1)": v2},
        "L~2^": round(log2(comb(N, ell2)) - log2(p), 2),
        "|Omega|~2^": round(log2(Omega), 2),
        "M_best~2^": round(log2(float(M_best)), 2),
        "M_half~2^": round(log2(float(M_half)), 2),
        "density_best~2^": round(log2(float(d_best)), 2),
        "density_half~2^": round(log2(float(d_half)), 2),
        "target": "2^-22",
        "checks": checks,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2)); raise SystemExit(0 if out["all_ok"] else 1)
    print("prob:explicit at cor:deployed (KoalaBear sextic) -- deployed-scale density:")
    print(f"  params: {out['params']}")
    print(f"  heavy-word list L ~ 2^{out['L~2^']}   |Omega| ~ 2^{out['|Omega|~2^']}")
    print(f"  deep-image size M (best alpha) ~ 2^{out['M_best~2^']}  "
          f"=> density ~ 2^{out['density_best~2^']}")
    print(f"  deep-image size M (>= half of alpha) ~ 2^{out['M_half~2^']}  "
          f"=> density ~ 2^{out['density_half~2^']}")
    print(f"  target {out['target']}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (explicit deep-point line clears 2^-22 at deployed params)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
