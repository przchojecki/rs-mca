#!/usr/bin/env python3
r"""
FALSIFICATION SCANNER for the L2 sharp-constant interleaved conjecture (iter 1-2).

Conjecture (l2_interleaved_dilation_constants.md §2): above the corrected reserve,
    Lst(Int(C,mu), 1-a/n)  <=  binom(n,a) q^{-mu(a-k)} + Quot_mu + n^B,
the genuine open piece being the APERIODIC mu-fold intersection remainder n^B.

The interleaved list at radius 1-a/n with rows U=(U_1,...,U_mu) is
    |{ (c_1,...,c_mu) in C^mu : | intersection_i A_i(c_i) | >= a }|,
A_i(c) = {x : c(x)=U_i(x)}. Because distinct deg-<k codewords agree on <= k-1 < a
points, each common agreement support of size >= a pins ONE codeword per row, so a
listed tuple is exactly (interp(U_1,S),...,interp(U_mu,S)) for a common support S.

DECISIVE QUESTION (does L2 have content beyond L1?):
    can interleaving CREATE mass, i.e. interleaved > max_i |Fib(U_i)| ?
If interleaved <= max_i |Fib_i| robustly, then above the reserve (base fibers
poly by L1) the interleaved list is poly -> L2 aperiodic subsumed by L1. If some
adversarial word gives interleaved > max base fiber, L2 has genuine independent
content (and a super-poly such remainder would threaten the conjecture).

The adversarial construction that can create cross-mass is MISALIGNED multi-
codeword gluings: row i is a different codeword on a different partition of H, so
distinct cross pairs (interp(U_1,S),interp(U_2,S)) get realized on different
common supports S. Aligned gluings only realize the diagonal.

Word families (mu rows over H=F_p^*): exact codeword; near-codeword (codeword +
few errors); ALIGNED 2/3-codeword gluings; MISALIGNED gluings (shifted/interleaved
partitions -- the adversarial case); monomial; quotient-periodic.

Output per family: each base fiber, max/min base, interleaved count, product,
saving ratio, and FLAGS: [CREATE] interleaved > max_base (interleaving creates
mass), and the random-baseline term binom(n,a) q^{-mu(a-k)} for reference.

Status: AUDIT / FALSIFICATION SCAN (exact enumeration, small fields).

Run:
    python3 experimental/scripts/verify_l2_falsify_interleaved.py
    python3 experimental/scripts/verify_l2_falsify_interleaved.py --json
"""

from __future__ import annotations

import argparse
import json
from math import comb
from itertools import product


def build(p, n, k):
    H = list(range(1, p))
    cws = [tuple(sum(co[i] * pow(x, i, p) for i in range(k)) % p for x in H)
           for co in product(range(p), repeat=k)]
    cwset = set(cws)
    return H, cws, cwset


def poly_on(H, p, coeffs):
    return tuple(sum(coeffs[i] * pow(x, i, p) for i in range(len(coeffs))) % p for x in H)


def fiber(U, cws, a):
    out = []
    for c in cws:
        A = frozenset(j for j in range(len(U)) if c[j] == U[j])
        if len(A) >= a:
            out.append((c, A))
    return out


def interleaved_count(fibs, a, n):
    if not fibs or any(len(f) == 0 for f in fibs):
        return 0
    cnt = 0

    def rec(i, acc):
        nonlocal cnt
        if len(acc) < a:
            return
        if i == len(fibs):
            cnt += 1
            return
        for (_, A) in fibs[i]:
            rec(i + 1, acc & A)
    rec(0, frozenset(range(n)))
    return cnt


def run():
    p, n, k = 17, 16, 3
    a = k + 2                         # 5, slack 2
    H, cws, cwset = build(p, n, k)

    c0 = poly_on(H, p, [1, 2, 3])
    c1 = poly_on(H, p, [4, 0, 1])
    c2 = poly_on(H, p, [2, 5, 6])
    c3 = poly_on(H, p, [7, 1, 4])

    def glue_parts(parts):
        """parts: list of (codeword, set_of_positions); fill H by region."""
        U = [0] * n
        for cw, pos in parts:
            for j in pos:
                U[j] = cw[j]
        return tuple(U)

    # aligned: contiguous blocks; misaligned: interleaved residue classes
    blkA = set(range(0, 8)); blkB = set(range(8, 16))
    # misaligned row2 partition: even vs odd positions
    evens = set(j for j in range(n) if j % 2 == 0)
    odds = set(j for j in range(n) if j % 2 == 1)
    # finer misalignment: residues mod 3
    r3 = [set(j for j in range(n) if j % 3 == t) for t in range(3)]

    near0 = list(c0); near0[0] = (near0[0] + 1) % p; near0[1] = (near0[1] + 1) % p
    near0 = tuple(near0)                       # c0 with 2 errors
    mono = tuple(pow(x, k, p) for x in H)      # x^k, not a codeword
    per = tuple((pow(x, 2, p) * 3 + 1) % p for x in H)

    families = {
        "exact codeword c0 x glued(c0,c1,c2)":
            [c0, glue_parts([(c0, r3[0] | {9, 12}), (c1, r3[1] | {10}), (c2, r3[2] | {11})])],
        "near-codeword x near-codeword":
            [near0, tuple((lambda L: (L.__setitem__(5, (L[5]+1) % p), L.__setitem__(6, (L[6]+1) % p), tuple(L))[-1])(list(c1)))],
        "aligned glue(c0,c1) x aligned glue(c0,c1)":
            [glue_parts([(c0, blkA), (c1, blkB)]), glue_parts([(c0, blkA), (c1, blkB)])],
        "MISALIGNED glue(c0,c1)[block] x glue(c0,c1)[even/odd]":
            [glue_parts([(c0, blkA), (c1, blkB)]), glue_parts([(c0, evens), (c1, odds)])],
        "MISALIGNED 3-way glue (block) x (mod3) x (even/odd) mu=3":
            [glue_parts([(c0, blkA), (c1, blkB)]),
             glue_parts([(c0, r3[0] | r3[1] & set(range(6))), (c1, r3[2] | set(range(6, 16)) & r3[1])]),
             glue_parts([(c0, evens), (c1, odds)])],
        "MISALIGNED glue(c0,c1,c2) 3 partitions mu=2":
            [glue_parts([(c0, r3[0]), (c1, r3[1]), (c2, r3[2])]),
             glue_parts([(c0, blkA), (c1, blkB)])],
        "monomial x periodic":
            [mono, per],
        "periodic x periodic":
            [per, tuple((pow(x, 2, p) * 5 + 2) % p for x in H)],
    }

    rows = []
    create_found = False
    for name, Us in families.items():
        mu = len(Us)
        fibs = [fiber(U, cws, a) for U in Us]
        base = [len(f) for f in fibs]
        max_base = max(base) if base else 0
        min_base = min(base) if base else 0
        prod = 1
        for b in base:
            prod *= b
        inter = interleaved_count(fibs, a, n)
        baseline = comb(n, a) * (p ** (-mu * (a - k)))   # binom q^{-mu(a-k)}, float
        create = inter > max_base
        if create:
            create_found = True
        rows.append({
            "family": name, "mu": mu, "base": base, "max_base": max_base,
            "min_base": min_base, "interleaved": inter, "product": prod,
            "saving_ratio": round(inter / prod, 4) if prod else None,
            "rand_baseline binom*q^-mu(a-k)": round(baseline, 4),
            "CREATE interleaved>max_base": create,
        })
    return {"params": {"p": p, "n": n, "k": k, "a": a, "sigma": a - k},
            "create_mass_found": create_found, "families": rows}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0)
    print(f"L2 interleaved falsification scan (iter)  params={out['params']}")
    print("  DECISIVE: does interleaving CREATE mass (interleaved > max single-row fiber)?")
    print(f"  random baseline term binom(n,a) q^-mu(a-k) is ~0 here, so any interleaved mass is structured/aperiodic.")
    print()
    print(f"  {'family':<52} {'mu':>2} {'base':>10} {'maxF':>4} {'inter':>5} {'prod':>5}  CREATE")
    for r in out["families"]:
        print(f"  {r['family']:<52} {r['mu']:>2} {str(r['base']):>10} {r['max_base']:>4} "
              f"{r['interleaved']:>5} {r['product']:>5}  {'!! YES' if r['CREATE interleaved>max_base'] else 'no'}")
    print()
    if out["create_mass_found"]:
        print("RESULT: interleaving CREATES mass in some family (interleaved > max base fiber)")
        print("  => L2 has genuine content beyond L1; measure how it scales (next iter).")
    else:
        print("RESULT: NO mass creation (interleaved <= max base fiber across the sweep)")
        print("  => evidence the interleaved list is bounded by a single-row fiber (<= L1 poly).")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
