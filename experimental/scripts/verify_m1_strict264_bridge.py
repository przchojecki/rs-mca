#!/usr/bin/env python3
r"""
M1 strict264 audit: the M2-bridge gate and the slack-8 two-ended setup (exact).

Target (Przemek frontier, strict264-min): for C = RS[F_17^32, H, 256] (n=512,
k=256), seven retained bad slopes at agreement 264 certify emca(C,31/64) > 2^-128,
strengthening the Cycle119 endpoint delta*_C <= 249/512 to delta*_C <= 31/64.

This script verifies the parts that need NO Cycle84 slot model:
  (1) M2 bridge: emca(C,delta) = LD_sw(C, ceil((1-delta)n))/|F|; agreement 264
      <-> delta = 1 - 264/512 = 31/64;
  (2) denominator gate: floor(17^32 / 2^128) = 6, so LD_sw >= 7 => emca > 2^-128;
  (3) strict improvement: 31/64 = 248/512 < 249/512 (Cycle119);
  (4) slack-8 two-ended parameters: agreement = n - j with j=248, sigma=n-k-j=8,
      r=j+sigma=256=n-k (Cycle119 was j=249, sigma=7).

The survivor COUNT (>=7 or 2187=3^7) depends on the Cycle84 seven-slot model
(not in-repo) and is NOT checked here.

Status: AUDIT / PROVED-by-arithmetic (the bridge gate + slack-8 setup).

Run:
    python3 experimental/scripts/verify_m1_strict264_bridge.py
    python3 experimental/scripts/verify_m1_strict264_bridge.py --json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def run():
    p, e = 17, 32
    q = p ** e
    n, k = 512, 256
    agreement = 264
    delta = 1 - Fraction(agreement, n)            # M2 bridge: agreement = (1-delta)n
    floor_gate = q // (2 ** 128)
    min_slopes = floor_gate + 1                    # smallest count clearing 2^-128
    j = n - agreement                              # co-support size
    sigma = n - k - j                              # slack
    r = j + sigma
    cyc119_delta = Fraction(249, 512)
    checks = {
        "delta = 1 - 264/512 = 31/64": delta == Fraction(31, 64),
        "floor(17^32/2^128) = 6": floor_gate == 6,
        "min slopes to clear 2^-128 is 7": min_slopes == 7,
        "7/q > 2^-128": Fraction(7, q) > Fraction(1, 2 ** 128),
        "6/q <= 2^-128 (so 7 is tight)": Fraction(floor_gate, q) <= Fraction(1, 2 ** 128),
        "strict264 stronger than Cycle119 (31/64 < 249/512)": delta < cyc119_delta,
        "two-ended setup: j=248": j == 248,
        "slack sigma = n-k-j = 8": sigma == 8,
        "r = j+sigma = n-k = 256": r == 256 and r == n - k,
        "agreement = n - j = 264": n - j == agreement,
        "one rung deeper than Cycle119 (sigma 7->8)": sigma == 7 + 1,
    }
    return {
        "params": {"q": "17^32", "n": n, "k": k, "agreement": agreement,
                   "delta": str(delta), "delta_float": float(delta)},
        "floor(17^32/2^128)": floor_gate, "min_retained_slopes": min_slopes,
        "two_ended": {"j": j, "sigma": sigma, "r": r},
        "checks": checks, "all_ok": all(checks.values()),
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("M1 strict264 audit: M2-bridge gate + slack-8 two-ended setup (exact).")
    print(f"  params: {out['params']}")
    print(f"  floor(17^32/2^128) = {out['floor(17^32/2^128)']}  => min retained slopes = {out['min_retained_slopes']}")
    print(f"  two-ended: j={out['two_ended']['j']}, sigma={out['two_ended']['sigma']}, r={out['two_ended']['r']}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (strict264 bridge gate + slack-8 setup verified; survivor count needs slot model)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
