#!/usr/bin/env python3
"""Verifier for the quantitative claims of the r2 roadmap + proof-sketch tree
(experimental/notes/roadmaps/).  AUDIT status: this re-derives every number
quoted by the planning notes from first principles (stdlib only); it proves
no theorem and promotes nothing.

Checks: pinned-row regression; gate addition certificates; master per-rate
crossing table with its ordering; corridor widths; poly/exponent budgets;
zone-(a) norm-threshold boundaries; window first-moment exponents; the
regular-boundary-vs-Johnson gap identity; m-sweep caps.

Run:  python3 experimental/scripts/verify_roadmap_r2_numbers.py
Exit non-zero iff any check fails.
"""
from __future__ import annotations

import math

lg = math.log2


def H(x: float) -> float:
    return -x * lg(x) - (1 - x) * lg(1 - x) if 0 < x < 1 else 0.0


def beta(rho: float) -> float:
    return 0.5 * lg(3) if rho >= 1 / 3 else 0.5 * (H(2 * rho) + 2 * rho)


def taustar(rho: float, lgq: float) -> float:
    lo, hi = 1e-12, 1 - rho - 1e-12
    for _ in range(300):
        mid = (lo + hi) / 2
        if mid * lgq - H(rho + mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


RATES = [(1 / 2, 9), (1 / 4, 9), (1 / 8, 9), (1 / 16, 10)]

# expected values as quoted in the notes (6 decimal places)
EXPECT = {
    1 / 2: dict(cap=0.498047, quot=0.493809, tau=0.496094, lw=(0.492188, 0.496094), width=2.17),
    1 / 4: dict(cap=0.748047, quot=0.744141, tau=0.746811, lw=(0.743662, 0.746831), width=2.00),
    1 / 8: dict(cap=0.873047, quot=0.870854, tau=0.872853, lw=(0.870753, 0.872877), width=1.12),
    1 / 16: dict(cap=0.936523, quot=0.934888, tau=0.936162, lw=(0.934865, 0.936182), width=1.67),
}


def check_pinned_row():
    Q = 17 ** 32
    d = []
    ok = True
    b_aff, b_proj = Q // 2 ** 128, (Q + 1) // 2 ** 128
    d.append(f"gates: affine {b_aff}, projective {b_proj}")
    ok &= b_aff == 6 and b_proj == 6
    o, x = 1, 17 % 512
    while x != 1:
        x = x * 17 % 512
        o += 1
    d.append(f"ord(17 mod 512) = {o} (generating: q_gen = q_line)")
    ok &= o == 32
    cap = (512 - 256) // 3
    d.append(f"staircase cap = {cap}; B_Q = 6 <= cap; a_safe = n - B_Q + 1 = {512 - 6 + 1}")
    ok &= cap == 85 and 512 - 6 + 1 == 507
    return ok, d


def check_gate_witnesses():
    Q, G = 17 ** 32, 2 ** 128
    w1 = Q - 6 * G
    w2 = 7 * G - Q
    ok = (6 * G + w1 == Q) and (Q + w2 == 7 * G) and w1 > 0 and w2 > 0
    return ok, [f"addition certificates: 6*2^128 + {w1} = 17^32 ; 17^32 + {w2} = 7*2^128 : {ok}"]


def check_master_table():
    d = []
    ok = True
    for rho, capexp in RATES:
        e = EXPECT[rho]
        cap = 1 - rho - 2 ** -capexp
        quot = 1 - rho - beta(rho) / 128
        tau = 1 - rho - taustar(rho, 256)
        lw = (1 - rho - H(rho) / 128, 1 - rho - H(rho) / 256)
        row_ok = (abs(cap - e["cap"]) < 5e-6 and abs(quot - e["quot"]) < 5e-6
                  and abs(tau - e["tau"]) < 5e-6
                  and abs(lw[0] - e["lw"][0]) < 5e-6 and abs(lw[1] - e["lw"][1]) < 5e-6
                  and lw[0] < quot < tau < cap and abs(lw[1] - tau) < 3e-4)
        width = (cap - quot) / 2 ** -capexp
        row_ok &= abs(width - e["width"]) < 0.01
        d.append(f"rho=1/{round(1/rho)}: quot {quot:.6f} tau* {tau:.6f} cap {cap:.6f} "
                 f"lw [{lw[0]:.6f},{lw[1]:.6f}] width {width:.2f} : {row_ok}")
        ok &= row_ok
    d.append("ordering list_lo < quot < tau* = list_hi < cap at every rate: True")
    return ok, d


def check_budgets():
    d = []
    ok = True
    ok &= 3 * 41 < 128 and 4 * 41 > 128
    d.append(f"R2 poly budget at n=2^41: 3*41 = {3*41} < 128 < {4*41} = 4*41 (B <= 3)")
    for m, exp in [(2, 1.60), (3, 1.07), (4, 0.80), (16, 0.20)]:
        v = 128 / (m * 40)
        ok &= abs(v - exp) < 0.01
        d.append(f"interleaved worst-case m={m}: B <= {v:.2f}; a-regular: B <= {128/40:.2f}")
    ok &= 128 // 40 == 3
    d.append("worst-case route with base exponent 1 covers m <= 3 only")
    return ok, d


def check_zone_a():
    d = []
    ok = True
    def nmax(L):
        N = 2
        while (N / 2) * lg(2 * (N // 2 + 1)) <= L:
            N += 2
        return N - 2
    for L, exp in [(32 * lg(17), 46), (192, 62), (256, 80)]:
        v = nmax(L)
        ok &= v == exp
        d.append(f"log2 q = {L:5.1f}: zone-(a) proved-exact to N' = {v} (expected {exp})")
    return ok, d


def check_window_fm():
    from math import lgamma
    lgC = lambda n, j: (lgamma(n + 1) - lgamma(j + 1) - lgamma(n - j + 1)) / math.log(2)
    lgq = 32 * lg(17)
    d = []
    ok = True
    for A, lo, hi in [(385, -16340, -16320), (426, -21790, -21760)]:
        t, j = A - 256, 512 - A
        v = lgC(512, j) + (1 - t) * lgq
        ok &= lo < v < hi
        d.append(f"A={A}: log2 E[#aligned] = {v:.0f} (in ({lo},{hi}))")
    d.append("=> any window alignment is structured (fraction <= ~2^-16000)")
    return ok, d


def check_johnson_gap_identity():
    d = []
    ok = True
    for rho in [r for r, _ in RATES]:
        gap = (1 - math.sqrt(rho)) - (1 - rho) / 2
        ident = (1 - math.sqrt(rho)) ** 2 / 2
        ok &= abs(gap - ident) < 1e-12 and gap > 0
    d.append("J - (1-rho)/2 = (1-sqrt(rho))^2/2 > 0 at all rates "
             "(the regular branch never reaches the band)")
    m_caps = [round(math.sqrt((1 - r) * 2 ** (10 if r == 1 / 16 else 9)), 1) for r, _ in RATES]
    ok &= m_caps == [16.0, 19.6, 21.2, 31.0]
    d.append(f"m-sweep caps near the cap: {m_caps}")
    return ok, d


CHECKS = [
    ("pinned-row regression", check_pinned_row),
    ("gate addition certificates", check_gate_witnesses),
    ("master per-rate crossing table + ordering", check_master_table),
    ("poly / interleaved exponent budgets", check_budgets),
    ("zone-(a) norm-threshold boundaries", check_zone_a),
    ("window first-moment exponents", check_window_fm),
    ("regular-vs-Johnson gap identity + m-caps", check_johnson_gap_identity),
]


def main():
    print("=" * 74)
    print("AUDIT: re-derive the quantitative claims of the r2 roadmap + sketch tree")
    print("=" * 74)
    failed = 0
    for title, fn in CHECKS:
        ok, details = fn()
        print(f"\n[{'PASS' if ok else 'FAIL':4}] {title}")
        for line in details:
            print(f"        {line}")
        failed += 0 if ok else 1
    print("\n" + "-" * 74)
    print(f"checks: {len(CHECKS)}   failed: {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
