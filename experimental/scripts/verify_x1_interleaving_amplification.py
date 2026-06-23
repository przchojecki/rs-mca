#!/usr/bin/env python3
r"""
Interleaving amplification: a K_{2,2} overlap design where the interleaved list
strictly exceeds BOTH participating row lists  (L2 / X1, over-agreement regime).

Increment 6 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.

Section 2.4 reduced the open L2 core to the bipartite ">=a-overlap" graph and
showed a separation needs two-sided over-agreement (support > a on both rows).
This script realizes the smallest such design and measures it.

Construction over F_41, n=20, k=4, a=8 (code C_+ = RS deg < k+1 = deg <= 4;
distinct codewords agree on <= k = 4 points; over-agreement support = 12 = 2a-k):

  T   = {d_0,d_1,d_2,d_3}                       (shared 4-set, |T| = k)
  A_1 = T u {d_4..d_7}  u {d_12..d_15}          row-1 support 1  (size 12)
  A_2 = T u {d_8..d_11} u {d_16..d_19}          row-1 support 2  (size 12)
  B_1 = T u {d_4..d_11}                         row-2 support 1  (size 12)
  B_2 = T u {d_12..d_19}                        row-2 support 2  (size 12)

By design: |A_i cap A_j| = |B_i cap B_j| = 4 = k (i != j), and ALL four cross
overlaps |A_i cap B_j| = 8 = a.  Realizing each support with a codeword
(g_1,g_2 on row 1 and h_1,h_2 on row 2, each pair agreeing exactly on T via
g_2 = g_1 + prod_{x in T}(X-x)) and the words U_1,U_2 that produce exactly those
agreement supports, the ">=a-overlap" graph is the complete bipartite K_{2,2}:

  interleaved list = 4 edges,   row-1 list = row-2 list = 2.

So interleaved = 4 > 2 = max(L_1, L_2): interleaving STRICTLY amplifies beyond
the max participating row list -- impossible in the a-regular regime (Section
2.3, where interleaved <= min row list).  This is the over-agreement separation
that Section 2.4 localized, now realized concretely with codewords.

Whether the amplification (m^2 from a K_{m,m} design) ever beats the GLOBAL base
list Lst(C_+) -- a true Lst(Int) > Lst(C_+) separation -- is reported against
the largest single-row list observed here and posed as the sharp open question
(it needs the overlap design to scale, i.e. larger n).

Finite toy evidence + exact construction; no cap / deployed claim.
Status: PROVED-by-check (construction).  Supports L2 and X1.

Run:
    python3 experimental/scripts/verify_x1_interleaving_amplification.py
    python3 experimental/scripts/verify_x1_interleaving_amplification.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_x1_interleaved_deep_point import (   # noqa: E402
    multiplicative_subgroup, interpolate, poly_eval, degree,
    quotient_locator_word, interleaved_list_and_deep,
)
from verify_x1_overlap_graph import single_row_codewords, overlap_graph   # noqa: E402


def vanishing_poly(points, p):
    poly = [1]
    for r in points:
        new = [0] * (len(poly) + 1)
        for d, b in enumerate(poly):
            new[d] = (new[d] - r * b) % p
            new[d + 1] = (new[d + 1] + b) % p
        poly = new
    return poly


def build_k22(p=41, n=20, k=4, a=8):
    D = multiplicative_subgroup(p, n)
    assert n == 20 and k == 4 and a == 8
    T = [0, 1, 2, 3]
    A1 = set(T + [4, 5, 6, 7] + [12, 13, 14, 15])
    A2 = set(T + [8, 9, 10, 11] + [16, 17, 18, 19])
    B1 = set(T + [4, 5, 6, 7, 8, 9, 10, 11])
    B2 = set(T + [12, 13, 14, 15, 16, 17, 18, 19])
    # design sanity
    assert all(len(s) == 12 for s in (A1, A2, B1, B2))
    assert len(A1 & A2) == k and len(B1 & B2) == k
    for Ai in (A1, A2):
        for Bj in (B1, B2):
            assert len(Ai & Bj) == a, (sorted(Ai), sorted(Bj), len(Ai & Bj))
    V = vanishing_poly([D[i] for i in T], p)          # deg k, zero exactly on T
    g1 = [1]
    g2 = [(g1[i] if i < len(g1) else 0) + V[i] for i in range(len(V))]
    h1 = [2]
    h2 = [(h1[i] if i < len(h1) else 0) + V[i] for i in range(len(V))]
    U1, U2 = {}, {}
    for i, x in enumerate(D):
        U1[x] = poly_eval(g1, x, p) if i in A1 else poly_eval(g2, x, p)  # A1 u A2 = all
        U2[x] = poly_eval(h1, x, p) if i in B1 else poly_eval(h2, x, p)  # B1 u B2 = all
    return D, U1, U2


def run() -> dict:
    p, n, k, a = 41, 20, 4, 8
    D, U1, U2 = build_k22(p, n, k, a)
    alpha0 = [x for x in range(p) if x not in set(D)][0]

    inter, _ = interleaved_list_and_deep([U1, U2], D, k, a, alpha0, p)
    edges, d1, d2, L1, L2, _ = overlap_graph(U1, U2, D, k, a, p)

    # over-agreement check: supports of size > a on both rows
    s1 = [len(A) for _, A in single_row_codewords(U1, D, k, a, p)]
    s2 = [len(A) for _, A in single_row_codewords(U2, D, k, a, p)]
    two_sided_overagreement = (max(s1) > a) and (max(s2) > a)

    # base reference: largest single-row list over a few comparison words
    refs = {"U1": L1, "U2": L2}
    qloc = quotient_locator_word(D, k, n, n // 2, p)
    refs["qloc"] = len(single_row_codewords(qloc, D, k, a, p))
    base_seen = max(refs.values())

    interleaved = len(inter)
    out = {
        "p": p, "n": n, "k": k, "a": a,
        "interleaved": interleaved, "edges": edges,
        "L1": L1, "L2": L2, "max_row_list": max(L1, L2),
        "max_support_row1": max(s1), "max_support_row2": max(s2),
        "two_sided_overagreement": two_sided_overagreement,
        "edge_eq_interleaved": interleaved == edges,
        "amplifies_beyond_rows": interleaved > max(L1, L2),
        "single_row_lists_seen": refs,
        "max_single_row_seen": base_seen,
        "beats_base_seen": interleaved > base_seen,
    }
    out["ok"] = (out["edge_eq_interleaved"] and out["amplifies_beyond_rows"]
                 and out["two_sided_overagreement"])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    o = run()
    if args.json:
        print(json.dumps(o, indent=2))
        if not o["ok"]:
            raise SystemExit(1)
        return
    print("Interleaving amplification: K_{2,2} overlap design (F_41, n=20, k=4, a=8)")
    print()
    print(f"  interleaved list = {o['interleaved']}  (== edges {o['edges']}? {o['edge_eq_interleaved']})")
    print(f"  row lists L1={o['L1']}  L2={o['L2']}  -> max row list = {o['max_row_list']}")
    print(f"  interleaved > max row list?  {o['amplifies_beyond_rows']}"
          f"   (impossible in the a-regular regime)")
    print(f"  two-sided over-agreement: max supports = "
          f"({o['max_support_row1']}, {o['max_support_row2']}) > a={o['a']}?"
          f" {o['two_sided_overagreement']}")
    print()
    print(f"  single-row lists seen: {o['single_row_lists_seen']}"
          f"  -> max single-row = {o['max_single_row_seen']}")
    print(f"  interleaved beats max single-row seen (separation candidate)? "
          f"{o['beats_base_seen']}")
    print()
    print("RESULT:", "PASS" if o["ok"] else "FAIL")
    if not o["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
