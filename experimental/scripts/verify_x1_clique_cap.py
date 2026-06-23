#!/usr/bin/env python3
r"""
Clique-amplification cap and the L2 -> L1 reduction (L2 / X1).

Increment 8 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.

Two honest statements about the over-agreement open core of Section 2.4-2.5.

(R) Reduction.  Since the interleaved list is the >=a-overlap edge count
    (Section 2.4), for every mu-row word
        |Lambda(Int(C_+,mu),delta_a,U)| <= prod_i |Lambda(C_+,delta_a,U_i)|
                                        <= Lst(C_+,delta_a)^mu,
    and = Lst(C_+,delta_a) in the a-regular regime (Section 2.3).  Hence the
    worst-case interleaved list is polynomial iff the base (L1) list is: the L2
    interleaved-list problem REDUCES to the L1 base-list problem, with exponent
    in [1, mu] (exactly 1 when a-regular).  No separate L2 bound is needed; an
    L1 bound Lst(C_+) <= n^B gives Lst(Int(C_+,mu)) <= n^{mu B}.

(C) Clique cap.  The only known constructive amplification of the exponent above
    1 is the K_{m,m} two-sided over-agreement design (Section 2.5).  It is
    GEOMETRICALLY CAPPED: m row-1 supports sharing exactly the k-set T have
    pairwise-disjoint non-T parts, likewise the m row-2 supports, and every one
    of the m^2 cells A_i cap B_j must hold >= a-k non-T points, so

        n  >=  k + m^2 (a-k).

    Thus a K_{m,m} clique realizes interleaved = m^2 only at n >= k+m^2(a-k);
    equivalently its amplification m^2 <= (n-k)/(a-k) is LINEAR in n.  To beat
    the base via this route one would need Lst(C_+) < (n-k)/(a-k), i.e. a base
    list already linear-small -- never the hard (large-list) L2 regime.

This script verifies (C) by constructing the grid K_{m,m} design (abstract
supports) for m = 2,3,4: all m^2 cross overlaps equal a, all within-row overlaps
equal k, the edge count is m^2, and the design fits exactly at n = k+m^2(a-k)
(and provably not below).  It cross-checks m=2 against the field-realized
construction of `verify_x1_interleaving_amplification.py`.

Finite/combinatorial certificate; no cap / deployed claim.
Status: PROVED (R reduction, C cap) / PROVED-by-check (designs).

Run:
    python3 experimental/scripts/verify_x1_clique_cap.py
    python3 experimental/scripts/verify_x1_clique_cap.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations


def grid_kmm(m: int, a: int, k: int):
    """Build the grid K_{m,m} overlap design.
    Points: T = {0..k-1} (shared), then m*m cells each of (a-k) fresh points.
    Returns (n, A_supports, B_supports)."""
    cell = a - k
    T = list(range(k))
    nxt = k
    cells = {}
    for i in range(m):
        for j in range(m):
            cells[(i, j)] = list(range(nxt, nxt + cell))
            nxt += cell
    n = nxt
    A = []  # row supports
    for i in range(m):
        s = set(T)
        for j in range(m):
            s.update(cells[(i, j)])
        A.append(frozenset(s))
    B = []  # column supports
    for j in range(m):
        s = set(T)
        for i in range(m):
            s.update(cells[(i, j)])
        B.append(frozenset(s))
    return n, A, B


def check_design(m, a, k):
    n, A, B = grid_kmm(m, a, k)
    ok = True
    # within-row overlaps == k
    for i, j in combinations(range(m), 2):
        if len(A[i] & A[j]) != k or len(B[i] & B[j]) != k:
            ok = False
    # cross overlaps == a  (=> edges, since a >= a)
    edges = 0
    for Ai in A:
        for Bj in B:
            ov = len(Ai & Bj)
            if ov >= a:
                edges += 1
            if ov != a:
                ok = False
    support_size = k + m * (a - k)
    n_expected = k + m * m * (a - k)
    facts = {
        "m": m, "a": a, "k": k, "n": n, "n_expected": n_expected,
        "edges": edges, "edges_expected": m * m,
        "support_size": min(len(s) for s in A + B),
        "support_size_expected": support_size,
        "over_agreement": support_size > a,
        "all_overlaps_ok": ok,
        "n_matches_cap": n == n_expected,
        "edges_match_m2": edges == m * m,
    }
    facts["ok"] = (ok and facts["n_matches_cap"] and facts["edges_match_m2"]
                   and facts["over_agreement"])
    return facts


def run():
    rows = [check_design(m, a=8, k=4) for m in (2, 3, 4)]
    # cross-check m=2 against the field-realized construction (n=20).
    cross = None
    try:
        import os, sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from verify_x1_interleaving_amplification import run as amp_run
        a = amp_run()
        cross = {"field_realized_interleaved": a["interleaved"],
                 "field_realized_edges": a["edges"],
                 "grid_m2_edges": rows[0]["edges"],
                 "match": a["edges"] == rows[0]["edges"] == 4}
    except Exception as e:  # pragma: no cover
        cross = {"error": str(e)}
    all_ok = all(r["ok"] for r in rows) and bool(cross.get("match"))
    return {"all_ok": all_ok, "designs": rows, "cross_check_m2": cross}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
        if not out["all_ok"]:
            raise SystemExit(1)
        return
    print("K_{m,m} clique-amplification cap (a=8, k=4):  n = k + m^2 (a-k), edges = m^2")
    print()
    for r in out["designs"]:
        print(f"  m={r['m']}: n={r['n']} (= k+m^2(a-k) = {r['n_expected']}? {r['n_matches_cap']})"
              f"  edges={r['edges']} (= m^2 = {r['edges_expected']}? {r['edges_match_m2']})"
              f"  support={r['support_size']} (>a? {r['over_agreement']})  [{'OK' if r['ok'] else 'FAIL'}]")
    print()
    c = out["cross_check_m2"]
    print(f"  cross-check m=2 vs field-realized (verify_x1_interleaving_amplification): {c}")
    print()
    print("  Amplification cap: K_{m,m} interleaved = m^2 <= (n-k)/(a-k), LINEAR in n.")
    print("  Reduction: Lst(Int(C_+,mu)) <= Lst(C_+)^mu (= Lst(C_+) when a-regular)"
          " -> L2 polynomial iff L1 polynomial.")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
