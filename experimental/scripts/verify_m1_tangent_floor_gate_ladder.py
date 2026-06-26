#!/usr/bin/env python3
r"""
Machine-check the MOVING-ROOT TANGENT FLOOR gate ladder: which recorded
"target"/"candidate"/"conditional" results on the row C = RS[F_17^32, H, 256]
are ALREADY subsumed by the proved tangent floor.

Proved input (experimental/data/tangent/tangent_staircase_section.tex,
Thm "moving-root tangent floor", elementary MDS argument, no smoothness / no
Cycle84 slot model / no analytic input):

    LD_sw(C, a) >= n - a + 1   for every  k+1 <= a <= n.

Bridge (M2, exact): emca(C, delta) = LD_sw(C, ceil((1-delta)n)) / q, delta=(n-a)/n.
Gate: emca > 2^-128  <=>  LD_sw * 2^128 > q  <=>  LD_sw >= 7, since
floor(17^32 / 2^128) = 6.

Consequence: n - a + 1 >= 7  <=>  a <= 506. So the tangent floor clears the
>=7 gate for the ENTIRE range a in [k+1, 506] = [257, 506], UNCONDITIONALLY.
The exact staircase (LD_sw = n-a+1) starts at a >= ceil((2n+k)/3) = 427, pinning
the threshold between a=506 (last unsafe, LD_sw=7) and a=507 (first safe, LD_sw=6).

This script does NOT re-prove the tangent floor; it checks the arithmetic that
turns that proved floor into the gate verdict for each recorded ledger item,
and flags which recorded statuses are therefore subsumed.

Run:
    python3 experimental/scripts/verify_m1_tangent_floor_gate_ladder.py
    python3 experimental/scripts/verify_m1_tangent_floor_gate_ladder.py --json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

N = 512
K = 256
Q = 17 ** 32
TWO128 = 2 ** 128

# Recorded ledger items keyed by agreement a, with their CURRENT recorded status
# and the gate they need (all need LD_sw >= 7 to clear 2^-128).
LEDGER = [
    # a,    id,                         recorded_status,         note
    (262, "cycle116/cycle120 gate",     "conditional(Cycle84 N)", "emca(C,125/256)>2^-128; prize-facing negative counterexample"),
    (263, "cycle119 strict263",         "conditional(Cycle84 N)", "delta*_C <= 249/512 strict strengthening"),
    (264, "strict264 gate",             "proved(min>=9)/cand(2187)", "strict264-min already proved; 2187 count separate"),
    (272, "reserve272",                 "target",                 "frontier.json"),
    (288, "reserve288",                 "target",                 "frontier.json"),
    (313, "reserve313",                 "target",                 "frontier.json (n/log n scale)"),
    (352, "strict352 deepest rung",     "proved(quotient-core)",  "tangent subsumes the whole 264..352 range for the GATE"),
    (506, "tangent506 last unsafe",     "proved/exact-gate",      "LD_sw=7 exact"),
    (507, "tangent507 first safe",      "proved/exact-gate",      "LD_sw=6 exact -> safe (gate must FAIL here)"),
]


def gate_clears(slopes: int) -> bool:
    """emca = slopes/Q > 2^-128  <=>  slopes * 2^128 > Q (exact integers)."""
    return slopes * TWO128 > Q


def run():
    checks = {}
    floor_q = Q // TWO128
    a_exact_min = (2 * N + K + 2) // 3  # ceil((2n+k)/3)

    checks["floor(17^32/2^128) = 6 (>=7 is the exact gate bar)"] = (floor_q == 6)
    checks["6*2^128 < 17^32 < 7*2^128 (gate tight at 7)"] = (6 * TWO128 < Q < 7 * TWO128)
    checks["exact-staircase starts at a = ceil((2n+k)/3) = 427"] = (a_exact_min == 427)
    # The proved floor applies for all k+1 <= a <= n; gate boundary a<=506.
    checks["tangent floor clears gate iff a <= 506 (n-a+1>=7)"] = all(
        ((N - a + 1) >= 7) == (a <= 506) for a in range(K + 1, N + 1))

    rows = []
    for a, ident, status, note in LEDGER:
        floor = N - a + 1                     # proved tangent lower bound
        applies = (K + 1) <= a <= N           # hypothesis of the tangent theorem
        clears = gate_clears(floor)
        exact = a >= a_exact_min
        delta = Fraction(N - a, N)
        rows.append({
            "a": a, "id": ident, "recorded_status": status,
            "tangent_floor_LDsw>=": floor,
            "theorem_applies(k+1<=a<=n)": applies,
            "gate_emca>2^-128": clears,
            "exact(3a-2n>=k)": exact,
            "delta=(n-a)/n": f"{delta.numerator}/{delta.denominator}",
            "subsumed_by_tangent": applies and clears,
            "note": note,
        })
        # a<=506 must clear; a=507 must NOT (safety boundary)
        if a <= 506:
            checks[f"a={a} ({ident}): tangent floor {floor} clears gate"] = (applies and clears)
        else:
            checks[f"a={a} ({ident}): tangent floor {floor} does NOT clear (safe)"] = (not clears)

    # strict352's entire proved range [264,352] is subsumed by the tangent floor
    # for the GATE: min over the range is at a=352 -> n-352+1 = 161 >= 7.
    min_floor_352 = min(N - a + 1 for a in range(264, 353))
    checks["tangent floor subsumes strict352 gate range [264,352] (min floor 161>=7)"] = (
        min_floor_352 == 161 and min_floor_352 >= 7)

    all_ok = all(checks.values())
    return {
        "row": {"n": N, "k": K, "q": "17^32"},
        "tangent_theorem": "LD_sw(C,a) >= n-a+1 for k+1<=a<=n (proved, elementary MDS)",
        "ledger": rows,
        "checks": checks,
        "all_ok": all_ok,
        "summary": {
            "gate_boundary": "a<=506 unsafe (emca>2^-128); a>=507 safe",
            "threshold_pinned": "delta*_C between 5/512 (safe) and 3/256 (unsafe)",
            "subsumed_recorded_items": [r["id"] for r in rows if r["subsumed_by_tangent"] and r["a"] <= 506],
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str))
        raise SystemExit(0 if out["all_ok"] else 1)

    print("Tangent-floor gate ladder on C = RS[F_17^32, H, 256] (n=512, k=256, q=17^32)")
    print(f"  proved input: {out['tangent_theorem']}")
    print(f"  gate: emca>2^-128 <=> LD_sw>=7 (floor(17^32/2^128)=6)")
    print()
    print(f"  {'a':>4}{'LDsw>=':>8}{'gate':>6}{'exact':>7}{'delta':>10}  recorded_status -> subsumed?")
    for r in out["ledger"]:
        sub = "SUBSUMED" if (r["subsumed_by_tangent"] and r["a"] <= 506) else ("safe" if r["a"] > 506 else "-")
        print(f"  {r['a']:>4}{r['tangent_floor_LDsw>=']:>8}{str(r['gate_emca>2^-128']):>6}"
              f"{str(r['exact(3a-2n>=k)']):>7}{r['delta=(n-a)/n']:>10}  {r['recorded_status']:<26} {sub}")
    print()
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    print()
    print("READING: every recorded item at a<=506 (cycle120/cycle119 prize gates, strict264 gate,")
    print("reserve272/288/313, and the whole strict352 range) has its >=7 GATE subsumed by the proved")
    print("tangent floor -- UNCONDITIONALLY (no Cycle84 census, no slot model). Exact counts/densities")
    print("(2187, N=5.27e10, ~2^-95) are NOT established by this and remain separate.")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
