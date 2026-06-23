#!/usr/bin/env python3
r"""
Interleaved list as a bipartite overlap-graph edge count (L2 / X1).

Increment 5 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.

For mu=2 the bridge note's full-agreement formula says the interleaved
(column-distance) list is the number of pairs of full agreement supports with
intersection >= a:

    |Lambda(Int(C_+,2),1-a/n,(U_1,U_2))|
      = #{ (c_1,c_2) in list(U_1) x list(U_2) : |A_{c_1}(U_1) cap A_{c_2}(U_2)| >= a }
      = #edges of the bipartite ">= a-overlap" graph G(list(U_1), list(U_2)).

Two structural facts (proved in the note, checked here):

  * tight-support degree bound: a codeword with full agreement support of size
    exactly a has degree <= 1 in G (any two opposite-side codewords whose
    support contains the same a-set agree on > k points, hence coincide).  So if
    every row is a-regular, G is a MATCHING and |interleaved| <= min row list
    <= base list -- recovering the Section 2.3 collapse from the graph view.

  * over-agreement breaks the matching: a codeword whose support has size > a can
    have degree >= 2.  A constructed witness (c_1,c_1' tight on overlapping
    a-sets S,S' inside a size-(2a-k) support A_2 of an over-agreeing c_2) gives
    degree(c_2)=2.  Hence the a-regular hypothesis of Section 2.3 is NECESSARY:
    without it G need not be a matching.

This localizes the remaining L2 question precisely: a worst-case interleaved list
exceeding the base list requires SIMULTANEOUS over-agreement on both sides (both
rows having codewords of support > a with the right overlap geometry), which is
geometrically constrained (needs n >~ 2a-k).  Whether that ever beats the global
base list Lst(C_+) is the open over-agreement core of L2.

Finite toy evidence + exact-count check; no cap / deployed claim.
Status: PROVED (edge-count identity, tight-degree bound) / PROVED-by-check.

Run:
    python3 experimental/scripts/verify_x1_overlap_graph.py
    python3 experimental/scripts/verify_x1_overlap_graph.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_x1_interleaved_deep_point import (   # noqa: E402
    multiplicative_subgroup, interpolate, poly_eval, degree,
    quotient_locator_word, interleaved_list_and_deep,
)


def single_row_codewords(U, D, k, a, p):
    """Return list of (poly_key, frozenset full-agreement support) for codewords
    (deg < k+1) agreeing with U on >= a points."""
    seen = {}
    for S in combinations(D, a):
        P = interpolate([(x, U[x]) for x in S], p)
        if degree(P, p) >= k + 1:
            continue
        key = tuple(P)
        if key not in seen:
            A = frozenset(x for x in D if poly_eval(P, x, p) == U[x])
            seen[key] = A
    return list(seen.items())


def overlap_graph(U1, U2, D, k, a, p):
    """Return (edges, deg1, deg2, L1, L2): edge count and per-side max degrees."""
    r1 = single_row_codewords(U1, D, k, a, p)
    r2 = single_row_codewords(U2, D, k, a, p)
    edges = 0
    deg1 = [0] * len(r1)
    deg2 = [0] * len(r2)
    for i, (_k1, A1) in enumerate(r1):
        for j, (_k2, A2) in enumerate(r2):
            if len(A1 & A2) >= a:
                edges += 1
                deg1[i] += 1
                deg2[j] += 1
    return edges, (max(deg1) if deg1 else 0), (max(deg2) if deg2 else 0), len(r1), len(r2), r1


def poly_eval_list(P, x, p):
    return poly_eval(list(P), x, p)


def build_overagreement(p, D, k, a):
    """Construct a degree-2 witness: c_2 over-agrees (support 2a-k) and is
    adjacent to two tight row-1 codewords c_1, c_1'."""
    assert len(D) >= 2 * a - k, "need n >= 2a-k for the construction"
    K = D[:k]
    extraS = D[k:a]            # a-k points
    extraSp = D[a:2 * a - k]   # a-k points (disjoint from extraS)
    S = K + list(extraS)
    Sp = K + list(extraSp)
    A2 = S + list(extraSp)     # = K + extraS + extraSp, size 2a-k
    # vanishing poly on K (degree k)
    VK = [1]
    for x in K:
        new = [0] * (len(VK) + 1)
        for d, b in enumerate(VK):
            new[d] = (new[d] - x * b) % p
            new[d + 1] = (new[d + 1] + b) % p
        VK = new
    c1 = [1, 1]                # 1 + X
    c1p = [(c1[i] if i < len(c1) else 0) + VK[i] for i in range(len(VK))]
    c1p = [v % p for v in c1p]
    c2 = [2, 3]                # 2 + 3X
    A2set = set(A2)
    U1, U2 = {}, {}
    for x in D:
        # row 1
        if x in set(S):
            U1[x] = poly_eval(c1, x, p)
        elif x in set(Sp):
            U1[x] = poly_eval(c1p, x, p)
        else:
            v = (poly_eval(c1, x, p) + 1) % p
            if v == poly_eval(c1p, x, p):
                v = (v + 1) % p
            U1[x] = v
        # row 2
        if x in A2set:
            U2[x] = poly_eval(c2, x, p)
        else:
            U2[x] = (poly_eval(c2, x, p) + 1) % p
    return U1, U2


def run() -> dict:
    out = {"tight": [], "overagreement": None, "all_ok": True}

    # 1. tight (a-regular) words: edge count == interleaved, graph is a matching.
    for (p, n, k, a) in [(97, 16, 8, 12), (193, 16, 8, 12)]:
        D = multiplicative_subgroup(p, n)
        N = n // 2
        V = quotient_locator_word(D, k, n, N, p)
        # use V and a 'shift' word (multiply argument) for a 2-row tight pair
        Vs = {x: V[(x * D[1]) % p] for x in D}
        alpha0 = [x for x in range(p) if x not in set(D)][0]
        inter, _ = interleaved_list_and_deep([V, Vs], D, k, a, alpha0, p)
        edges, d1, d2, L1, L2, _ = overlap_graph(V, Vs, D, k, a, p)
        ok = (len(inter) == edges) and (max(d1, d2) <= 1)
        out["tight"].append({"p": p, "n": n, "k": k, "a": a,
                             "interleaved": len(inter), "edges": edges,
                             "max_deg": max(d1, d2), "L1": L1, "L2": L2,
                             "edge_eq_interleaved": len(inter) == edges,
                             "is_matching": max(d1, d2) <= 1, "ok": ok})
        if not ok:
            out["all_ok"] = False

    # 2. over-agreement witness: degree 2, matching broken.
    p, n, k, a = 97, 16, 4, 8
    D = multiplicative_subgroup(p, n)
    U1, U2 = build_overagreement(p, D, k, a)
    alpha0 = [x for x in range(p) if x not in set(D)][0]
    inter, _ = interleaved_list_and_deep([U1, U2], D, k, a, alpha0, p)
    edges, d1, d2, L1, L2, r1 = overlap_graph(U1, U2, D, k, a, p)
    # supports of the over-agreeing side
    r2 = single_row_codewords(U2, D, k, a, p)
    max_supp2 = max((len(A) for _, A in r2), default=0)
    witness_ok = (len(inter) == edges) and (max(d1, d2) >= 2) and (max_supp2 > a)
    out["overagreement"] = {
        "p": p, "n": n, "k": k, "a": a,
        "interleaved": len(inter), "edges": edges,
        "max_deg_row1": d1, "max_deg_row2": d2,
        "L1": L1, "L2": L2, "max_support_row2": max_supp2,
        "edge_eq_interleaved": len(inter) == edges,
        "degree_ge_2": max(d1, d2) >= 2,
        "over_agreement": max_supp2 > a,
        "exceeds_base_of_participants": len(inter) > max(L1, L2),
        "ok": witness_ok}
    if not witness_ok:
        out["all_ok"] = False
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
        if not out["all_ok"]:
            raise SystemExit(1)
        return
    print("Interleaved list = bipartite >=a-overlap edge count (mu=2):")
    print()
    print("  tight / a-regular rows  ->  graph is a matching (max degree <= 1):")
    for t in out["tight"]:
        print(f"    p={t['p']} n={t['n']} k={t['k']} a={t['a']}:"
              f" interleaved={t['interleaved']} == edges={t['edges']}?"
              f" {t['edge_eq_interleaved']};  max_deg={t['max_deg']}"
              f" (matching={t['is_matching']})  L1={t['L1']} L2={t['L2']}")
    print()
    o = out["overagreement"]
    print("  over-agreement witness  ->  matching broken (degree >= 2):")
    print(f"    p={o['p']} n={o['n']} k={o['k']} a={o['a']}:"
          f" interleaved={o['interleaved']} == edges={o['edges']}?"
          f" {o['edge_eq_interleaved']}")
    print(f"    max_support_row2={o['max_support_row2']} (> a={o['a']}? "
          f"{o['over_agreement']});  max_deg_row2={o['max_deg_row2']}"
          f" (>=2? {o['degree_ge_2']})")
    print(f"    L1={o['L1']} L2={o['L2']}  interleaved>max(L1,L2)? "
          f"{o['exceeds_base_of_participants']}")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
