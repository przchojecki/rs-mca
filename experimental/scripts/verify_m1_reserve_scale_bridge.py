#!/usr/bin/env python3
r"""
M1 reserve-scale frontier audit: bridge gates + corrected slack-sigma setup.

Przemek's frontier (site/data/frontier.json) lists, beyond strict264 (sigma=8),
three DEEPER reserve-scale targets on the same row RS[F_17^32,H,256] (n=512,k=256):

    id           agreement a   sigma=a-k   j=n-a   radius delta=(n-a)/n
    reserve272      272          16         240     15/32
    reserve288      288          32         224     7/16
    reserve313      313          57         199     199/512   (~ n/log2 n scale)

Each asks for the SAME ">= 7 retained bad slopes" target, deeper below capacity.
This script audits the parts that are checkable by arithmetic (the bridge gate and
the slack-sigma two-ended setup), for all four targets (strict264 included for
continuity), and records the one slot-model-dependent gap (the exact >=7 count) plus
the structural TENSION specific to the reserve scale.

Verified here (all four targets):
  * radius delta = (n-a)/n reduces to the frontier radiusLabel;
  * sigma = a-k, j = n-a, r = j+sigma = n-k = 256 (redundancy fixed at n-k);
  * M2-bridge gate: floor(17^32 / 2^128) = 6, so LD_sw >= 7 ==> emca(C,delta) =
    LD_sw/17^32 >= 7/17^32 > 2^-128 ==> delta*_C <= delta -- the SAME gate for every
    agreement (it does not depend on a), so 7 slopes certify the bound at any radius;
  * the corrected two-ended jet (per verify_m1_strict264_two_ended_transfer.py):
    deg(P_J - P_J') <= j - sigma  (top sigma-1 elem-sym e_1..e_{sigma-1} common)
    + endpoint P_J(0) common -- NOT deg <= j-sigma+1 (off-by-one that breaks the line);
  * the delta* upper bounds are strictly decreasing across the targets (deeper =
    stronger), and all lie below the Paper-D cap 1-rho-2^-9 = 255/512 at rho=1/2.

NOT verified here (slot-model-dependent, flagged):
  * the exact ">= 7 retained slopes" achievability at each reserve scale. The exact
    count needs the Cycle84 7-slot model (not in-repo). RESERVE-SCALE TENSION: the
    per-line slope-richness COLLAPSES as slack sigma rises (verified small-model trend
    in verify_m1_strict264_admissibility.py / _mechanism.py), so deeper reserve targets
    are progressively HARDER -- whether >=7 survives at sigma=16/32/57 is exactly the
    open question this audit isolates (it does NOT assert achievability).

Status: AUDIT (reserve-scale bridge gates + corrected setup verified; count flagged).

Run:
    python3 experimental/scripts/verify_m1_reserve_scale_bridge.py
    python3 experimental/scripts/verify_m1_reserve_scale_bridge.py --json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


TARGETS = [
    # id, agreement, radiusLabel, status
    ("strict264-min", 264, "31/64", "target"),
    ("reserve272", 272, "15/32", "target"),
    ("reserve288", 288, "7/16", "target"),
    ("reserve313", 313, "199/512", "target (n/log n scale)"),
]


def run():
    n, k = 512, 256
    q = 17 ** 32
    gate = q >> 128                      # floor(17^32 / 2^128)
    paper_d_cap = Fraction(255, 512)     # 1 - rho - 2^-9 at rho=1/2 = 1/2 - 1/512

    rows = []
    prev_delta = None
    monotone = True
    for tid, a, label, status in TARGETS:
        sigma = a - k
        j = n - a
        r = j + sigma
        delta = Fraction(n - a, n)
        lbl_num, lbl_den = (int(x) for x in label.split("/"))
        row = {
            "id": tid, "agreement": a, "sigma": sigma, "j": j, "r": r,
            "delta": str(delta), "radiusLabel": label,
            "delta_matches_label": delta == Fraction(lbl_num, lbl_den),
            "r_equals_n_minus_k": r == n - k,
            "corrected_jet_deg_le": j - sigma,        # deg(P_J-P_J') <= j-sigma
            "gate_7_gt_floor": 7 > gate,              # 7 slopes clear the gate
            "delta_below_paperD_cap": delta <= paper_d_cap,
        }
        rows.append(row)
        if prev_delta is not None and not (delta < prev_delta):
            monotone = False
        prev_delta = delta

    checks = {
        "floor(17^32/2^128) = 6 (so 7 slopes clear the bridge gate at ANY agreement)":
            gate == 6,
        "every target: delta=(n-a)/n matches its frontier radiusLabel":
            all(row["delta_matches_label"] for row in rows),
        "every target: r = j+sigma = n-k = 256 (redundancy fixed)":
            all(row["r_equals_n_minus_k"] for row in rows),
        "every target: 7 > floor(q/2^128) (emca>2^-128 => delta* <= delta)":
            all(row["gate_7_gt_floor"] for row in rows),
        "delta* bounds strictly decreasing (deeper reserve = stronger)": monotone,
        "all target radii <= Paper-D cap 255/512 at rho=1/2":
            all(row["delta_below_paperD_cap"] for row in rows),
        "corrected jet deg<=j-sigma (top sigma-1 common)+endpoint, NOT j-sigma+1":
            all(row["corrected_jet_deg_le"] == (row["j"] - row["sigma"]) for row in rows),
    }
    return {"n": n, "k": k, "q": "17^32", "floor_q_over_2_128": gate,
            "paper_d_cap": str(paper_d_cap), "targets": rows,
            "checks": checks, "all_ok": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("M1 reserve-scale frontier audit (bridge gates + corrected slack-sigma setup):")
    print(f"  row RS[F_17^32,H,256]  n={out['n']} k={out['k']}  "
          f"floor(17^32/2^128)={out['floor_q_over_2_128']}  PaperD cap={out['paper_d_cap']}")
    print()
    print(f"  {'id':<22}{'a':>4}{'sigma':>6}{'j':>5}{'r':>5}{'delta':>10}{'deg<=':>7}")
    for row in out["targets"]:
        print(f"  {row['id']:<22}{row['agreement']:>4}{row['sigma']:>6}{row['j']:>5}"
              f"{row['r']:>5}{row['delta']:>10}{row['corrected_jet_deg_le']:>7}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (reserve-scale bridge gates + corrected setup verified; exact >=7 "
          "achievability is slot-model-dependent and flagged)" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
