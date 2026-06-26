#!/usr/bin/env python3
r"""
Verify that Codex's strict352 quotient-core floor SUBSUMES the three M1 frontier-board
reserve targets reserve272 / reserve288 / reserve313 (site/data/frontier.json).

Context. The M1 reserve targets were posted on the public board as OPEN search targets,
each asking for ">= 7 retained support-wise bad slopes" deeper below capacity on the
single smooth rate-1/2 row

    C = RS[F_17^32, H, 256],   n = 512,  k = 256,  |H| = 512,  q = 17^32.

My own reserve-scale audit (experimental/notes/m1/m1_reserve_scale_audit.md) certified
the bridge gate + the slack-sigma two-ended setup + free-dimension non-degeneracy, but
left the EXACT ">= 7 achievability" flagged OPEN ("Cycle84-slot-model-dependent, not
in-repo").

Codex's strict352 result (experimental/data/strict352/strict352_quotient_core_summary.md)
proves, by an in-repo DYADIC QUOTIENT-CORE construction (no slot model), under the SAME
finite-slope support-wise MCA convention and on the SAME row:

    LD_sw(C, a) >= 7   for EVERY  264 <= a <= 352,    and    LD_sw(C, 352) >= 16,

producing DISTINCT support-wise MCA-bad slopes. The canonical proved per-agreement floor
M(a) is recorded in experimental/data/strict352/strict352_quotient_core_output.txt.

This script checks, with EXACT integer arithmetic, that for each of the three reserve
targets the strict352 floor settles the only piece that was open:

  (1) same row / same convention / same bridge gate as the reserve targets;
  (2) the target agreement a lies in the proved range [264, 352];
  (3) the strict352 PROVED slope count M(a) meets the target's ">= 7" requirement;
  (4) the bridge gate fires: M(a) * 2^128 > q = 17^32, i.e. emca(C, delta) > 2^-128;
  (5) the board radius delta = (n - a)/n matches the strict352 radius convention.

Non-vacuity guard: the live frontier a = 353 is NOT covered (M(353) = 3 < 7), so the
three reserve targets sit strictly inside the proved range, just below the wall.

HONEST SCOPE. This is an arithmetic/bookkeeping subsumption check: it confirms the
strict352 THEOREM (taken as proved upstream) covers exactly what the reserve ROWS asked
for. It does not re-prove strict352's quotient-core construction; that proof and its
verifier (verify_strict352_quotient_core.py) live in experimental/data/strict352/.

Run:
    python3 experimental/scripts/verify_m1_reserve_subsumed_by_strict352.py
    python3 experimental/scripts/verify_m1_reserve_subsumed_by_strict352.py --json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

# ---------------------------------------------------------------------------
# Row constants (RS[F_17^32, H, 256]); identical on the reserve rows and strict352.
N = 512
K = 256
Q = 17 ** 32                      # |F| = q_line
TARGET = 2 ** -128                # security threshold; gate uses 2^128 integer form
CONVENTION = "finite-slope support-wise MCA"

# ---------------------------------------------------------------------------
# The three reserve targets, verbatim from site/data/frontier.json (status "target").
# badSlopesNeeded is the board's ">= 7 retained bad slopes" requirement.
RESERVE_TARGETS = [
    {"id": "reserve272", "a": 272, "radius": "15/32",  "badSlopesNeeded": 7},
    {"id": "reserve288", "a": 288, "radius": "7/16",   "badSlopesNeeded": 7},
    {"id": "reserve313", "a": 313, "radius": "199/512", "badSlopesNeeded": 7},
]

# strict352 PROVED per-agreement floor M(a), copied from the canonical output file
# experimental/data/strict352/strict352_quotient_core_output.txt (column M).
PROVED_M = {
    272: 19399767849168,
    288: 1631266,
    313: 295,
    352: 16,        # deepest guaranteed rung
    353: 3,         # the new frontier: M < 7 (NOT covered) -- non-vacuity guard
}
# The minimum proved floor over the whole guaranteed range [264, 352], read from the
# same canonical output (the smallest M occurs on the c=32 rows a=321..351, M=11).
MIN_M_OVER_RANGE = 11
RANGE_LO, RANGE_HI = 264, 352


def emca_clears_threshold(slopes: int) -> bool:
    """emca = slopes / q > 2^-128  <=>  slopes * 2^128 > q   (exact integers)."""
    return slopes * (2 ** 128) > Q


def run():
    checks = {}

    # Global gate sanity: floor(q / 2^128) = 6, so >=7 slopes is the exact bar, and
    # the strict352 summary's "7 * 2^128 > q" holds.
    floor_q = Q // (2 ** 128)
    checks["floor(17^32 / 2^128) = 6 (so >=7 slopes is the exact MCA bar)"] = (floor_q == 6)
    checks["bridge gate: 7 * 2^128 > 17^32 (7 slopes clear 2^-128)"] = emca_clears_threshold(7)
    checks["6 * 2^128 < 17^32 (6 slopes do NOT clear -- bar is tight at 7)"] = not emca_clears_threshold(6)

    # strict352 covers the whole proved range with margin (min floor >= 7).
    checks[f"strict352 min proved floor over [{RANGE_LO},{RANGE_HI}] = {MIN_M_OVER_RANGE} >= 7"] = (
        MIN_M_OVER_RANGE >= 7)

    per_target = []
    for t in RESERVE_TARGETS:
        a = t["a"]
        Ma = PROVED_M[a]
        sigma = a - K
        delta_board = Fraction(*map(int, t["radius"].split("/")))
        delta_conv = Fraction(N - a, N)
        row = {
            "id": t["id"], "a": a, "sigma": sigma,
            "in_proved_range": RANGE_LO <= a <= RANGE_HI,
            "proved_floor_M": Ma,
            "needed": t["badSlopesNeeded"],
            "meets_need": Ma >= t["badSlopesNeeded"],
            "gate_fires_emca_gt_2^-128": emca_clears_threshold(Ma),
            "board_radius": t["radius"],
            "convention_radius_(n-a)/n": f"{delta_conv.numerator}/{delta_conv.denominator}",
            "radius_matches": delta_board == delta_conv,
        }
        per_target.append(row)
        # each target must satisfy ALL of: in range, meets >=7, gate fires, radius matches
        checks[f"{t['id']}: a={a} in [{RANGE_LO},{RANGE_HI}]"] = row["in_proved_range"]
        checks[f"{t['id']}: proved floor {Ma} >= needed {t['badSlopesNeeded']}"] = row["meets_need"]
        checks[f"{t['id']}: gate fires (emca > 2^-128)"] = row["gate_fires_emca_gt_2^-128"]
        checks[f"{t['id']}: board radius {t['radius']} == (n-a)/n"] = row["radius_matches"]

    # Non-vacuity: the live frontier a=353 is strictly past the proved range and NOT
    # covered (M=3 < 7). So the reserve targets are genuinely interior, not at the edge.
    checks["non-vacuity: a=353 NOT covered (M(353)=3 < 7)"] = (
        PROVED_M[353] < 7 and 353 > RANGE_HI)
    checks["non-vacuity: deepest reserve a=313 < 353 (interior to proved range)"] = (
        max(t["a"] for t in RESERVE_TARGETS) < 353)

    all_ok = all(checks.values())
    return {
        "row": {"n": N, "k": K, "q": "17^32", "convention": CONVENTION},
        "strict352_claim": f"LD_sw(C,a) >= 7 for {RANGE_LO} <= a <= {RANGE_HI}; LD_sw(C,352) >= 16",
        "per_target": per_target,
        "checks": checks,
        "all_ok": all_ok,
        "verdict": ("SUBSUMED: strict352 proves >=7 distinct support-wise bad slopes at "
                    "every reserve agreement, on the same row / convention / gate -- "
                    "closing the only piece (exact >=7) the reserve audit left open.")
        if all_ok else "NOT subsumed (a check failed).",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str))
        raise SystemExit(0 if out["all_ok"] else 1)

    r = out["row"]
    print("Reserve targets subsumed by strict352?  Row RS[F_17^32,H,256] "
          f"(n={r['n']}, k={r['k']}, q={r['q']})")
    print(f"  convention: {r['convention']}")
    print(f"  strict352 proved: {out['strict352_claim']}")
    print()
    hdr = f"  {'id':<11}{'a':>4}{'sigma':>6}{'inRange':>8}{'provedFloor':>16}{'need':>6}{'gate':>6}{'radius==':>10}"
    print(hdr)
    for t in out["per_target"]:
        print(f"  {t['id']:<11}{t['a']:>4}{t['sigma']:>6}{str(t['in_proved_range']):>8}"
              f"{t['proved_floor_M']:>16}{t['needed']:>6}"
              f"{str(t['gate_fires_emca_gt_2^-128']):>6}{str(t['radius_matches']):>10}")
    print()
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    print()
    print("VERDICT:", out["verdict"])
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
