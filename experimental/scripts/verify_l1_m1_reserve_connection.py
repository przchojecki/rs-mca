#!/usr/bin/env python3
r"""
Cross-lane observation (audit): the M1 reserve frontier meets L1's reserve at sigma ~ n/log n.

VERIFIED ARITHMETIC (this script):
  * For the M1 row RS[F_17^32,H,256] (n=512, k=256, q=17^32), the frontier targets
    sit at slack sigma = a-k:
        strict264 sigma=8, reserve272 sigma=16, reserve288 sigma=32, reserve313 sigma=57.
  * L1 Conjecture 1 (l1_full_list_quotient_proof_program.md) holds ABOVE the reserve
        sigma >= C n / log n,    sigma log2(q) >= (1+eps) log2 binom(n,s).
  * n / log2(n) = 512 / 9 = 56.9, so reserve313's sigma = 57 ~ n/log2(n) -- exactly the
    L1 lower cutoff (the frontier even names it the "n/log n scale" target). The other
    three targets (sigma = 8,16,32) are BELOW this cutoff.
  * The entropy reserve sigma log2(q) >= (1+eps) log2 binom(n,s) clears with huge margin
    at reserve313 because q = 17^32 is enormous (so the binding reserve is the n/log n cutoff).

HEURISTIC INTERPRETATION (NOT proven here -- flagged):
  The M1 obstruction is a LINE-decoding (LD_sw) phenomenon and L1 is single-word list
  decoding, so this is a structural coincidence, not a rigorous implication. But it is
  suggestive: the four M1 targets sweep sigma from 8 (deep below reserve) up to 57 (AT the
  L1 reserve / n/log n cutoff). IF L1's aperiodic bound Q_1^list <= n^B holds above the
  reserve, then at/above sigma ~ n/log n the retained high-agreement mass must be
  QUOTIENT-PERIODIC (charged to sum_{d>1} Q_d), not aperiodic -- consistent with the
  Cycle84 SLOT model being an inherently periodic/coset structure (badSlopes = 2187 = 3^7
  is slot combinatorics). So the M1 reserve frontier and L1's quotient/aperiodic split
  appear to meet at the same n/log n threshold. This is an observation to pursue, not a claim.

Run:
    python3 experimental/scripts/verify_l1_m1_reserve_connection.py
    python3 experimental/scripts/verify_l1_m1_reserve_connection.py --json
"""

from __future__ import annotations

import argparse
import json
from math import log2, comb


def run():
    n, k = 512, 256
    q_bits = 32 * log2(17)                    # log2(17^32)
    cutoff = n / log2(n)                       # L1 lower cutoff scale n/log2 n
    targets = [("strict264", 264), ("reserve272", 272),
               ("reserve288", 288), ("reserve313", 313)]
    rows = []
    for tid, a in targets:
        sigma = a - k
        s = a                                  # s = k+sigma = a
        log_binom = log2(comb(n, s))
        entropy_reserve = sigma * q_bits       # sigma log2 q
        rows.append({
            "id": tid, "a": a, "sigma": sigma,
            "sigma_vs_cutoff(n/log2 n=%.1f)" % cutoff: round(sigma / cutoff, 3),
            "above_n_over_logn_cutoff": sigma >= cutoff,
            "entropy_reserve_sigma_log2q": round(entropy_reserve, 1),
            "log2_binom(n,s)": round(log_binom, 1),
            "entropy_reserve_clears": entropy_reserve >= log_binom,
        })

    r313 = next(r for r in rows if r["id"] == "reserve313")
    checks = {
        "n/log2(n) = 512/9 ~ 56.9": abs(cutoff - 56.9) < 0.2,
        "reserve313 sigma=57 ~ n/log2(n) (the L1 lower cutoff)":
            abs(57 - cutoff) < 1.0,
        "reserve313 reaches the n/log n cutoff (sigma >= n/log2 n)":
            r313["above_n_over_logn_cutoff"],
        "strict264/reserve272/reserve288 are BELOW the n/log n cutoff":
            all(not r["above_n_over_logn_cutoff"] for r in rows if r["id"] != "reserve313"),
        "entropy reserve clears at every target (q=17^32 huge)":
            all(r["entropy_reserve_clears"] for r in rows),
    }
    return {"n": n, "k": k, "q_bits": round(q_bits, 2), "n_over_log2n": round(cutoff, 2),
            "targets": rows, "checks": checks, "all_ok": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("Cross-lane: M1 reserve frontier vs L1 reserve (n/log n cutoff)")
    print(f"  row n={out['n']} k={out['k']}  log2(q)={out['q_bits']}  n/log2(n)={out['n_over_log2n']}")
    print()
    print(f"  {'id':<12}{'a':>4}{'sigma':>6}{'sigma/cutoff':>13}{'>=cutoff':>9}"
          f"{'sig*log2q':>11}{'log2 C(n,s)':>12}")
    for r in out["targets"]:
        key = [k2 for k2 in r if k2.startswith("sigma_vs_cutoff")][0]
        print(f"  {r['id']:<12}{r['a']:>4}{r['sigma']:>6}{r[key]:>13}"
              f"{str(r['above_n_over_logn_cutoff']):>9}{r['entropy_reserve_sigma_log2q']:>11}"
              f"{r['log2_binom(n,s)']:>12}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("VERIFIED: reserve313 (sigma=57) sits at the L1 n/log n reserve cutoff; the other")
    print("M1 targets are below it. HEURISTIC (flagged, not proven): above this shared threshold")
    print("L1's aperiodic bound would force the retained mass to be quotient-periodic (Cycle84")
    print("slot/coset structure), so the M1 reserve frontier and L1's quotient ledger appear to")
    print("meet at sigma ~ n/log n. An observation to pursue, not a claim.")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
