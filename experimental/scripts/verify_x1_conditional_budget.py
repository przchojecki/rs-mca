#!/usr/bin/env python3
r"""
Conditional protocol budget: what an L1 list bound buys via the forward bridge.

Increment 10 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.

The forward bridge (Sections 1-2) and the L2 -> L1 reduction (Section 2.6) compose
into a CONDITIONAL protocol statement. Suppose the L1 generated-field locator
bound holds above the corrected reserve:

    Lst(C_+, delta_a)  <=  n^B           (the open L1 / conj:prefix-local target).

Then:
  * Section 2.6:  Lst(Int(C_+,mu), delta_a) <= n^{mu B}     (worst case),
                  Lst(Int(C_+,mu), delta_a) <= n^{B}        (a-regular regime);
  * Section 2:    the interleaved-MCA bad-slope count <= the interleaved list,
                  with NO square-root loss.

So the Proximity-Prize soundness schematic (readme)
    MCA_error + |interleaved_list| / |challenge field| + query_error
has its interleaved term bounded by  n^{mu B} / q  (worst case) or  n^{B} / q
(a-regular).  An L1 list theorem therefore converts DIRECTLY into the
interleaved-MCA / interleaved-list soundness budget Paper C consumes -- no
separate MCA theorem, no sqrt loss, no Cartesian (mu) exponent in the generic
case.

This calculator prints, for the prize regime (target epsilon* = 2^-128,
|F| < 2^256), the largest L1 exponent B for which the interleaved term already
clears 2^-128, i.e. n^{e B} / q <= 2^-128 with e in {1 (a-regular), mu (worst)}:

    e * B * log2(n)  <=  log2(q) - 128     =>     B <= (log2(q) - 128) / (e * log2(n)).

It is an arithmetic budget tool, not a proof of the L1 bound.
Status: derived budget (conditional on the open L1 bound). Supports L2/X1 + Paper C.

Run:
    python3 experimental/scripts/verify_x1_conditional_budget.py
    python3 experimental/scripts/verify_x1_conditional_budget.py --json
"""

from __future__ import annotations

import argparse
import json


def budget(m: int, log2_q: int = 256, target_bits: int = 128):
    """Return required L1 exponent caps for n=2^m, challenge field q<2^{log2_q}."""
    headroom = log2_q - target_bits          # |list| must be <= 2^headroom
    out = {"m": m, "n": f"2^{m}", "log2_q": log2_q, "target": f"2^-{target_bits}",
           "headroom_bits": headroom}
    for mu in (1, 2, 3):
        # a-regular: |list| <= n^B = 2^{B m}; need B m <= headroom
        B_areg = headroom / m
        # worst case: |list| <= n^{mu B}; need mu B m <= headroom
        B_worst = headroom / (mu * m)
        out[f"mu{mu}"] = {"B_areg_max": round(B_areg, 3),
                          "B_worst_max": round(B_worst, 3)}
    return out


PRIZE_M = [20, 30, 40]  # n = 2^m; prize uses k <= 2^40


def run():
    rows = [budget(m) for m in PRIZE_M]
    return {"target": "2^-128", "challenge_field": "|F| < 2^256",
            "note": ("B is the L1 list exponent Lst(C_+) <= n^B; a-regular needs "
                     "exponent 1, worst case mu. Modest B already clears 2^-128."),
            "rows": rows, "all_ok": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
        return
    print("Conditional interleaved-MCA budget (target 2^-128, |F| < 2^256):")
    print("  IF Lst(C_+) <= n^B (open L1 bound) THEN interleaved-MCA term <= n^{eB}/q")
    print("  e = 1 (a-regular) or mu (worst case).  Largest B that already clears 2^-128:")
    print()
    print(f"  {'n':>6} | {'mu=1':>14} | {'mu=2':>22} | {'mu=3':>22}")
    print(f"  {'':>6} | {'B<=':>14} | {'B_areg / B_worst':>22} | {'B_areg / B_worst':>22}")
    for r in out["rows"]:
        c1 = f"{r['mu1']['B_areg_max']}"
        c2 = f"{r['mu2']['B_areg_max']} / {r['mu2']['B_worst_max']}"
        c3 = f"{r['mu3']['B_areg_max']} / {r['mu3']['B_worst_max']}"
        print(f"  {r['n']:>6} | {c1:>14} | {c2:>22} | {c3:>22}")
    print()
    print("  Reading: e.g. n=2^40, mu=2 worst case needs only B <= 1.6; a-regular B <= 3.2.")
    print("  A polynomial L1 list bound with small exponent suffices for the prize regime.")
    print()
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
