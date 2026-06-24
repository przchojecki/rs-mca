#!/usr/bin/env python3
r"""
INDEPENDENT AUDIT of PR #100's Cycle120 gate arithmetic + list->MCA implication.

PR #100 (`notes/m1/m1_cycle120_gate_arithmetic_contract.md`, Codex) packages a
deterministic gate/arithmetic layer for the M1 Cycle120 ABF-facing candidate:

    K = F_17^32, |K| = 17^32 < 2^256;  H = <theta>, |H| = n = 512 = 2^9;
    C = RS[K,H,256], k = 256, rho = 1/2;  delta = 125/256;  epsilon* = 2^-128;
    N = 52,747,567,092  (the Cycle84 finite occupancy count).

This script recomputes ONLY the deterministic arithmetic and the implication
thresholds, with exact big integers, independently of Codex's verifier:

  (1) closed agreement threshold (1-delta)n = 262; distance radius delta*n = 250;
  (2) Cycle116 agreement 262 meets the closed threshold; Cycle119 agreement 263
      gives distance 512-263 = 249 < 250, and 263 = (1-249/512)*512;
  (3) field cap 17^32 < 2^256; |H| = 2^9; rate 256/512 = 1/2; k <= 2^40;
  (4) floor(17^32 / 2^128) = 6 and N > 6, equivalently N*2^128 > 17^32, so
      N/|K| > 2^-128; density log2(N/17^32) ~ -95.18;
  (5) the implication: IF some pair (f1,f2) has >= N bad gamma in K each with a
      common support |S| >= 262, THEN emca(C,125/256) >= N/|K| > 2^-128, hence
      delta*_C <= 125/256 (and <= 249/512 under the Cycle119 strict transfer).

What this audit DOES NOT and CANNOT verify (flagged, not checked):
  * N = 52,747,567,092 itself -- the Cycle84 finite occupancy/census (Danny's
    large generated computation); needs independent reproduction;
  * the Cycle116/Cycle119 fixed-jet transfer proofs (that such a pair exists);
  * the official ABF ePrint 2026/680 wording (gate/sampler/predicate/threshold);
  * smoothness/generator of H=<theta>.

Status: AUDIT (deterministic arithmetic + implication logic only; result stays
CONDITIONAL on the finite imports above).

Run:
    python3 experimental/scripts/verify_audit_pr100_cycle120_gate.py
    python3 experimental/scripts/verify_audit_pr100_cycle120_gate.py --json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import comb, log2


def run() -> dict:
    p, e = 17, 32
    K = p ** e                      # |K| = 17^32, exact big int
    n, k = 512, 256
    delta = Fraction(125, 256)
    N = 52_747_567_092
    checks = {}

    # (1) thresholds
    closed_threshold = (1 - delta) * n      # (131/256)*512
    dist_radius = delta * n                  # (125/256)*512
    checks["closed_threshold_262"] = (closed_threshold == 262)
    checks["distance_radius_250"] = (dist_radius == 250)

    # (2) Cycle116 / Cycle119
    checks["c116_agreement_262_meets_closed"] = (262 == closed_threshold)
    checks["c119_distance_249_lt_250"] = (512 - 263 == 249 and 249 < 250)
    checks["c119_263_eq_closed_of_249over512"] = (263 == (1 - Fraction(249, 512)) * 512)

    # (3) parameter envelope
    checks["field_cap_17e32_lt_2e256"] = (K < 2 ** 256)
    checks["domain_512_is_2e9"] = (n == 2 ** 9)
    checks["rate_one_half"] = (Fraction(k, n) == Fraction(1, 2))
    checks["k_le_2e40"] = (k <= 2 ** 40)

    # (4) denominator comparison (the crux)
    floor_ratio = K // (2 ** 128)
    checks["floor_17e32_over_2e128_eq_6"] = (floor_ratio == 6)
    checks["N_gt_floor"] = (N > floor_ratio)
    checks["N_times_2e128_gt_K"] = (N * (2 ** 128) > K)   # exact form of N/K > 2^-128
    density_log2 = log2(N) - e * log2(p)
    checks["density_log2_about_-95"] = (-96.0 < density_log2 < -95.0)

    # (5) implication arithmetic (the bound N/|K|, and the radius statements)
    #     emca >= N/|K| > 2^-128  ==>  not safe at delta=125/256.
    checks["emca_bound_exceeds_target"] = (Fraction(N, K) > Fraction(1, 2 ** 128))
    #     Cycle119 cleaner statement uses 249/512 < 125/256:
    checks["249over512_lt_125over256"] = (Fraction(249, 512) < Fraction(125, 256))

    all_ok = all(checks.values())
    return {
        "all_ok": all_ok,
        "K_eq_17e32": str(K),
        "floor_17e32_over_2e128": floor_ratio,
        "N": N,
        "density_log2_N_over_K": round(density_log2, 2),
        "checks": checks,
        "unverified_imports": [
            "N=52,747,567,092 (Cycle84 finite occupancy census) -- NOT reproduced here",
            "Cycle116/Cycle119 fixed-jet transfer proofs -- NOT checked",
            "official ABF ePrint 2026/680 wording -- NOT fetched",
            "H=<theta> smoothness/generator -- NOT certified here",
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
        raise SystemExit(0 if out["all_ok"] else 1)
    print("AUDIT of PR #100 Cycle120 gate arithmetic (deterministic layer only):")
    print()
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    print()
    print(f"  17^32 = {out['K_eq_17e32']}")
    print(f"  floor(17^32 / 2^128) = {out['floor_17e32_over_2e128']}   N = {out['N']}")
    print(f"  density log2(N/17^32) = {out['density_log2_N_over_K']}")
    print()
    print("  NOT verified here (conditional imports):")
    for s in out["unverified_imports"]:
        print(f"    - {s}")
    print()
    print("RESULT:", "PASS (gate arithmetic + implication logic check out; "
          "result remains CONDITIONAL on the finite imports)"
          if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
