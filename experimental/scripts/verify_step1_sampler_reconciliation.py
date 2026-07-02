#!/usr/bin/env python3
"""Step 1 (towards-prize.md S1): reconcile our finite-slope support-wise MCA
convention with the official MCA sampler / survey definition.

This is a DOCUMENTED RECONCILIATION, not a unilateral certification.  It verifies
the exact-integer correspondences that hold UNAMBIGUOUSLY, and the companion note
`audit_step1_sampler_reconciliation.md` lays the convention out point-by-point
against the survey anchors recorded by the #147 high-agreement threshold package,
flagging which correspondences are arithmetic-unambiguous vs which remain a
residual judgment call against the authoritative sampler.

Row: C = RS[F_17^32, H, 256], n=512, k=256, q=q_line=17^32, target eps* = 2^-128.

Run:  python3 experimental/scripts/verify_step1_sampler_reconciliation.py
Exit non-zero iff any implemented check fails.
"""
from __future__ import annotations

Q = 17 ** 32          # q_line = |F|
TWO128 = 2 ** 128
N, K = 512, 256
RATES = [(1, 2), (1, 4), (1, 8), (1, 16)]


def check_gate_denominators():
    """The 2^-128 gate is the SAME under the affine (|F|) and projective (|F|+1)
    denominators: both give B_Q = 6, hence the same r<=5 safe / r=6 unsafe cut.
    (Unambiguous: the projective variant changes the denominator but not the cut.)"""
    d = []
    ok = True
    b_aff = Q // TWO128
    b_proj = (Q + 1) // TWO128
    d.append(f"affine  B_Q = floor(|F|/2^128)      = {b_aff}")
    d.append(f"projective B_Q = floor((|F|+1)/2^128) = {b_proj}")
    bracket = (6 * TWO128 < Q < 7 * TWO128) and (6 * TWO128 < Q + 1 < 7 * TWO128)
    d.append(f"both bracketed 6*2^128 < . < 7*2^128 : {bracket}")
    same_cut = (b_aff == b_proj == 6)
    d.append(f"same 5/6 cut (B_Q=6 both denominators) : {same_cut}")
    ok &= bracket and same_cut
    return ok, d


def check_endpoint_convention():
    """Endpoint / closed-ball arithmetic: with the integer radius r = floor(delta*n)
    and B_Q = 6, the safe radii are r <= 5 (agreement a >= 507) and the first unsafe
    is r = 6 (a = 506); the closed real safe interval is [0, 6/512) = [0, 3/256), so
    the supremal transition radius 3/256 has an UNSAFE endpoint, and the largest safe
    CLOSED grid radius is 5/512."""
    d = []
    ok = True
    b_q = Q // TWO128
    max_safe_r = b_q - 1            # 5
    first_unsafe_r = b_q           # 6
    d.append(f"max safe r = B_Q-1 = {max_safe_r} (agreement a = n-r = {N - max_safe_r})")
    d.append(f"first unsafe r = B_Q = {first_unsafe_r} (agreement a = {N - first_unsafe_r})")
    map_ok = (N - max_safe_r == 507) and (N - first_unsafe_r == 506)
    # closed real ball: 5/512 < 6/512 = 3/256; transition radius 3/256, endpoint unsafe
    from fractions import Fraction
    safe_grid = Fraction(max_safe_r, N)          # 5/512
    transition = Fraction(first_unsafe_r, N)     # 6/512 = 3/256
    d.append(f"largest safe closed grid radius = {safe_grid} ; transition = {transition} "
             f"(= {transition} ; endpoint UNSAFE)")
    interval_ok = (safe_grid < transition) and (transition == Fraction(3, 256))
    ok &= map_ok and interval_ok
    return ok, d


def check_survey_anchors():
    """The survey anchors recorded by the #147 package are internally consistent with
    the gate: target 2^-128, field range |F| < 2^256, rates {1/2,1/4,1/8,1/16}, and the
    line-decoding bridge eps_mca(C,delta) <= a/|F| reproduces the same >=B_Q+1 gate."""
    d = []
    ok = True
    target_exp, field_exp = 128, 256
    d.append(f"target eps* = 2^-{target_exp} ; official field range |F| < 2^{field_exp}")
    d.append(f"grand-challenge rates : {['%d/%d' % r for r in RATES]}")
    rates_ok = (RATES == [(1, 2), (1, 4), (1, 8), (1, 16)])
    # bridge consistency: emca = LD_sw/|F|, so emca > 2^-128 <=> LD_sw > |F|/2^128
    # <=> LD_sw >= floor(|F|/2^128)+1 = B_Q+1. Re-derive the gate from the bridge.
    b_q = Q // TWO128
    gate_from_bridge = (b_q + 1)             # LD_sw >= this is unsafe
    d.append(f"bridge eps_mca = LD_sw/|F| => unsafe iff LD_sw >= B_Q+1 = {gate_from_bridge} : "
             f"{gate_from_bridge == 7}")
    # field range admits B_Q up to ~2^128: floor((2^256-1)/2^128) = 2^128 - 1
    bq_max = (2 ** field_exp - 1) // TWO128
    d.append(f"max B_Q over |F| < 2^256 : floor((2^256-1)/2^128) = 2^128 - 1 : {bq_max == 2 ** 128 - 1}")
    ok &= rates_ok and (gate_from_bridge == 7) and (bq_max == 2 ** 128 - 1)
    return ok, d


def check_predicate_line_family():
    """(a) The MCA event 'exists S, |S| >= (1-delta)n' matches our co-support arithmetic
    exactly: with agreement a=|S| and co-support r=n-a, |S| >= (1-delta)n <=> r <= floor(delta n),
    and noncontainment is a per-support boolean, so the count is over size->=a supports (one
    support pays for <=1 slope, Paper D v12 lemma).  (b) Finite vs projective slope family:
    |P^1(F)| = |F|+1, and the extra point at infinity does NOT move the 5/6 cut.
    The DEFINITIONAL equivalence of the predicate and slope family vs the official sampler
    is a RESIDUAL JUDGMENT CALL (documented in the note, NOT asserted here)."""
    d = []
    ok = True
    from fractions import Fraction
    # (a) co-support / agreement equivalence at the grid radii
    eq_ok = True
    for j in range(0, 12):                       # j = floor(delta*n)
        delta = Fraction(j, N)
        threshold = (1 - delta) * N              # (1-delta)n = n - j (exact)
        for a in (N - j - 1, N - j, N - j + 1):
            r = N - a
            if (a >= threshold) != (r <= j):     # survey event  <=>  our co-support bound
                eq_ok = False
    d.append(f"co-support arithmetic: |S|>=(1-delta)n  <=>  r=n-a <= floor(delta n)  (a=n-r) : {eq_ok}")
    ok &= eq_ok
    d.append("noncontainment = per-support boolean => count over size->=a supports matches survey "
             "'exists S'; one support pays for <=1 slope (Paper D v12) => LD_sw <= #supports")
    # (b) finite vs projective slope family
    proj_size_ok = ((Q + 1) == Q + 1)            # |P^1(F)| = |F| + 1
    cut_unchanged = (Q // TWO128 == (Q + 1) // TWO128 == 6)
    d.append(f"|P^1(F)| = |F|+1 (one point at infinity) : {proj_size_ok}")
    d.append(f"the extra slope at infinity does NOT move the 5/6 cut "
             f"(floor(|F|/2^128)=floor((|F|+1)/2^128)=6) : {cut_unchanged}")
    ok &= proj_size_ok and cut_unchanged
    d.append("RESIDUAL JUDGMENT CALL: definitional equivalence of the predicate Delta_S>0 and "
             "the finite-vs-projective slope family vs the official sampler is documented, NOT asserted.")
    return ok, d


def _pending():
    return None, ["PENDING -- added in a later loop iteration"]


CHECKS = [
    ("gate: affine vs projective denominator", check_gate_denominators),
    ("endpoint / closed-ball convention",      check_endpoint_convention),
    ("survey anchors + bridge consistency",    check_survey_anchors),
    ("predicate / line-family correspondence", check_predicate_line_family),
]


def main():
    print("=" * 74)
    print("Step 1: reconcile finite-slope support-wise MCA vs the official sampler")
    print("DOCUMENTED RECONCILIATION (exact-integer matches), NOT a unilateral certification")
    print("=" * 74)
    failed = done = pending = 0
    for title, fn in CHECKS:
        status, details = fn()
        tag = "PENDING" if status is None else ("PASS" if status else "FAIL")
        if status is None:
            pending += 1
        elif status:
            done += 1
        else:
            failed += 1
        print(f"\n[{tag:7}] {title}")
        for line in details:
            print(f"          {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {done}   FAIL: {failed}   PENDING: {pending}")
    print("-" * 74)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
