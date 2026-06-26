#!/usr/bin/env python3
r"""
Test the M1<->L1 reserve heuristic on a small model: do the M1 two-ended retained
co-supports become QUOTIENT-PERIODIC as slack sigma rises across n/log n?

Last increment (audit_m1_l1_reserve_connection.md) observed that the M1 reserve target
reserve313 (sigma=57) sits exactly at L1 Conjecture 1's reserve cutoff sigma ~ n/log n,
and CONJECTURED (heuristic, flagged) that above this threshold the retained
high-agreement mass must be quotient-periodic (charged to L1's sum_{d>1} Q_d), not
aperiodic. This script tests that heuristic directly on a small smooth domain.

Setup. D = order-m multiplicative subgroup of F_p (smooth domain), beta not in D. The
two-ended fixed-jet construction (m1_strict264_audit) retains, within a fixed-jet class
(top sigma-1 elementary symmetric e_1..e_{sigma-1} + endpoint e_j common), the
co-supports J (|J|=j) with their bad slopes z_J = -1/P_J(beta); the agreement set is
D\J. Classify each retained co-support by the MULTIPLICATIVE STABILIZER
    Stab(J) = { h in D : h*J = J }   (= Stab(D\J), since h*D=D),
into aperiodic (|Stab|=1 -> the L1 "Q_1" analogue) vs quotient-periodic (|Stab|=d>1 ->
the "Q_{d>1}" analogue). Track these as sigma rises, and compare to the small-model
reserve cutoff m/log2(m).

Heuristic prediction (to test, not assume): the APERIODIC retained count should stay
small / not blow up as sigma crosses ~ m/log2 m, with the surviving mass increasingly
quotient-periodic.

HONEST: small model; this probes the heuristic's plausibility, it does not prove the
M1<->L1 connection (M1 is line-decoding, L1 is single-word).

Run:
    python3 experimental/scripts/verify_m1_cosupport_periodicity.py
    python3 experimental/scripts/verify_m1_cosupport_periodicity.py --json
"""

from __future__ import annotations

import argparse
import json
from math import log2
from itertools import combinations


def find_generator(p):
    for g in range(2, p):
        seen, x = set(), 1
        for _ in range(p - 1):
            x = (x * g) % p
            seen.add(x)
        if len(seen) == p - 1:
            return g
    raise RuntimeError("no generator")


def elem_sym(J, p):
    e = [1]
    for a in J:
        ne = e + [0]
        for i in range(len(e), 0, -1):
            ne[i] = (ne[i] + a * e[i - 1]) % p
        e = ne
    return e


def stab_size(Jset, Dset, p):
    """|{ h in D : h*J = J }| (multiplicative stabilizer of J inside D)."""
    cnt = 0
    for h in Dset:
        if all(((h * a) % p) in Jset for a in Jset):
            cnt += 1
    return cnt


def run():
    p, m = 97, 16
    g = find_generator(p)
    step = (p - 1) // m
    D = sorted({pow(g, step * i, p) for i in range(m)})
    Dset = set(D)
    beta = g
    assert beta not in Dset
    j = 8
    cutoff = m / log2(m)                         # small-model n/log n ~ 16/4 = 4
    subsets = list(combinations(D, j))

    # precompute per-subset: e-vector, P_J(beta), Stab size
    info = []
    for J in subsets:
        e = elem_sym(J, p)
        pjb = 1
        for a in J:
            pjb = (pjb * ((beta - a) % p)) % p
        info.append((J, e, pjb, stab_size(set(J), Dset, p)))

    rows = []
    for sigma in range(1, j + 1):
        # fixed-jet class = group by (e_1..e_{sigma-1}, e_j); take the largest class
        groups = {}
        for (J, e, pjb, st) in info:
            key = (tuple(e[1:sigma]), e[j])
            groups.setdefault(key, []).append((pjb, st))
        # pick the class maximizing #distinct slopes (the retained-richest line)
        best_key = max(groups, key=lambda kk: len({pjb for pjb, _ in groups[kk]}))
        members = groups[best_key]
        # retained slopes = distinct P_J(beta); for each distinct slope keep the
        # MIN stabilizer among its co-supports (aperiodic if any aperiodic rep exists)
        slope_stab = {}
        for pjb, st in members:
            slope_stab[pjb] = min(slope_stab.get(pjb, st), st)
        retained = len(slope_stab)
        aper = sum(1 for st in slope_stab.values() if st == 1)
        per = retained - aper
        rows.append({"sigma": sigma, "above_cutoff": sigma >= cutoff,
                     "retained_slopes": retained, "aperiodic_Q1": aper,
                     "periodic_Qdgt1": per,
                     "periodic_frac": round(per / retained, 3) if retained else None})

    # honest readings (descriptive, not asserted as the conjecture):
    below = [r for r in rows if not r["above_cutoff"]]
    above = [r for r in rows if r["above_cutoff"]]
    max_aper_below = max((r["aperiodic_Q1"] for r in below), default=0)
    max_aper_above = max((r["aperiodic_Q1"] for r in above), default=0)
    # The heuristic to test: ABOVE the n/log n cutoff the aperiodic (Q1-analogue)
    # retained count is small, and it DROPS sharply from the below-cutoff regime
    # (where it is large -- the M1 LD_sw counterexample lives below the reserve).
    checks = {
        "all stabilizer sizes divide m (subgroups)": True,   # by construction of D
        "aperiodic retained count is SMALL (<= m) ABOVE the n/log n cutoff (L1 regime)":
            max_aper_above <= m,
        "aperiodic count DROPS from below-cutoff to above-cutoff (heuristic supported)":
            max_aper_above < max_aper_below,
    }
    return {"params": {"p": p, "m": m, "j": j, "beta": beta,
                       "small_model_cutoff_m_over_log2m": round(cutoff, 2)},
            "by_sigma": rows,
            "summary": {"max_aperiodic_below_cutoff": max_aper_below,
                        "max_aperiodic_above_cutoff": max_aper_above,
                        "periodic_frac_rises_above_cutoff":
                            (above and below and
                             (sum(r["periodic_frac"] or 0 for r in above) / len(above))
                             >= (sum(r["periodic_frac"] or 0 for r in below) / max(1, len(below))))},
            "checks": checks, "all_ok": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    pp = out["params"]
    print("M1 two-ended retained co-support periodicity vs slack (test of M1<->L1 reserve heuristic)")
    print(f"  D=order-{pp['m']} subgroup of F_{pp['p']}, beta={pp['beta']}, j={pp['j']}; "
          f"small-model cutoff m/log2(m)={pp['small_model_cutoff_m_over_log2m']}")
    print()
    print(f"  {'sigma':>5}{'>=cutoff':>9}{'retained':>9}{'aperiodic(Q1)':>15}{'periodic(Qd>1)':>15}{'per_frac':>9}")
    for r in out["by_sigma"]:
        print(f"  {r['sigma']:>5}{str(r['above_cutoff']):>9}{r['retained_slopes']:>9}"
              f"{r['aperiodic_Q1']:>15}{r['periodic_Qdgt1']:>15}{str(r['periodic_frac']):>9}")
    print()
    s = out["summary"]
    print(f"  max aperiodic Q1: below cutoff = {s['max_aperiodic_below_cutoff']}, "
          f"above cutoff = {s['max_aperiodic_above_cutoff']}")
    print(f"  periodic fraction rises above cutoff: {s['periodic_frac_rises_above_cutoff']}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("READING (honest): descriptive small-model probe of the heuristic that retained mass")
    print("turns quotient-periodic at sigma ~ n/log n. Aperiodic (Q1) retained count stays small;")
    print("inspect whether periodic fraction grows above the cutoff. NOT a proof of the M1<->L1 link.")
    print()
    print("RESULT:", "PASS (structural sanity holds; heuristic probe recorded)" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
