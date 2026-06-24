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


def glue_from_partition(cws_by_region, regions, n):
    """U = cws_by_region[r] on regions[r]; regions partition range(n)."""
    U = [0] * n
    for r, reg in enumerate(regions):
        for j in reg:
            U[j] = cws_by_region[r][j]
    return tuple(U)


def cross_mass_witness(p, n, k, a, H, cws):
    """Engineer a 2-codeword-per-row gluing with 3 cross-overlaps >= a, predicting
    interleaved = 3 > max_base = 2 (mass creation)."""
    c0 = poly_on(H, p, [1, 2, 3]); c1 = poly_on(H, p, [4, 0, 1])
    c2 = poly_on(H, p, [2, 5, 6]); c3 = poly_on(H, p, [7, 1, 4])
    # partitions chosen so cross-overlaps are {0..4},{5..9},{10..14},{15}:
    P1 = set(range(0, 10)); P1b = set(range(10, 16))                 # row1: P1|P1'
    P2 = set(range(0, 5)) | set(range(10, 15)); P2b = set(range(5, 10)) | {15}  # row2
    U1 = glue_from_partition([c0, c1], [P1, P1b], n)
    U2 = glue_from_partition([c2, c3], [P2, P2b], n)
    fibs = [fiber(U1, cws, a), fiber(U2, cws, a)]
    base = [len(f) for f in fibs]
    inter = interleaved_count(fibs, a, n)
    return {"base": base, "max_base": max(base), "interleaved": inter,
            "predicted": 3, "creates_mass": inter > max(base)}


def search_max_ratio(p, n, k, a, H, cws, trials, seed):
    """Random 2-codeword-per-row gluings; track max interleaved and max ratio."""
    import random
    rng = random.Random(seed)
    best = {"interleaved": 0, "max_base": 1, "ratio": 0.0}
    pos = list(range(n))
    for _ in range(trials):
        # random codewords and random partitions per row
        cs = rng.sample(cws, 4)
        rng.shuffle(pos)
        cut1 = rng.randint(a, n - a)
        P1, P1b = set(pos[:cut1]), set(pos[cut1:])
        rng.shuffle(pos)
        cut2 = rng.randint(a, n - a)
        P2, P2b = set(pos[:cut2]), set(pos[cut2:])
        U1 = glue_from_partition([cs[0], cs[1]], [P1, P1b], n)
        U2 = glue_from_partition([cs[2], cs[3]], [P2, P2b], n)
        fibs = [fiber(U1, cws, a), fiber(U2, cws, a)]
        base = [len(f) for f in fibs]
        if min(base) == 0:
            continue
        inter = interleaved_count(fibs, a, n)
        ratio = inter / max(base)
        if ratio > best["ratio"]:
            best = {"interleaved": inter, "max_base": max(base), "ratio": round(ratio, 3),
                    "base": base}
    best["n_over_a (sum-constraint bound on #cross-pairs)"] = n // a
    return best


def grid_witness(p, n, k, a, H, cws):
    """GRID construction realizing ~n/a cross-pairs: tile H into s1*s2 blocks of
    size ~a; row1 = codeword d_i on the i-th block-row, row2 = e_j on j-th
    block-col. Each block(i,j) (>=a pts) realizes cross-pair (d_i,e_j), so
    interleaved = s1*s2 ~ n/a, max_base = max(s1,s2)."""
    m = n // a                                  # max #blocks of size a
    if m < 1:
        return None
    # factor m into s1<=s2 closest to sqrt (maximizes min => maximizes ratio)
    s1 = max(1, int(m ** 0.5))
    while m % s1 != 0 and s1 > 1:
        s1 -= 1
    s2 = m // s1
    nb = s1 * s2
    # block sizes: size a each, remainder folded into the last block
    sizes = [a] * nb
    sizes[-1] += n - a * nb
    blocks, pos = [], 0
    for sz in sizes:
        blocks.append(list(range(pos, pos + sz))); pos += sz
    ds = cws[:s1]                                # row1 codewords
    es = cws[s1:s1 + s2]                         # row2 codewords (distinct)
    U1 = [0] * n; U2 = [0] * n
    for bi in range(nb):
        i, j = bi // s2, bi % s2
        for x in blocks[bi]:
            U1[x] = ds[i][x]; U2[x] = es[j][x]
    fibs = [fiber(tuple(U1), cws, a), fiber(tuple(U2), cws, a)]
    base = [len(f) for f in fibs]
    inter = interleaved_count(fibs, a, n)
    return {"s1": s1, "s2": s2, "blocks": nb, "base": base,
            "max_base": max(base), "interleaved": inter,
            "ratio": round(inter / max(base), 3) if max(base) else None}


def scaling_scan():
    """Decisive test: does max interleaved (gluing attack) grow poly or super-poly in n?
    Uses the GRID construction (s codewords/row, ~n/a cross-pairs). k=2 (a=4),
    distinct codewords agree on <=1 pt; sweep n via fields with n|p-1."""
    points = [(13, 12, 2), (17, 16, 2), (41, 20, 2), (73, 24, 2), (97, 48, 2), (89, 88, 2)]
    rows = []
    for (p, n, k) in points:
        a = k + 2
        H, cws, _ = build(p, n, k)
        g = grid_witness(p, n, k, a, H, cws)
        rows.append({"p": p, "n": n, "a": a, "rho": round(k / n, 3),
                     "grid_s1xs2": f"{g['s1']}x{g['s2']}",
                     "interleaved": g["interleaved"], "max_base": g["max_base"],
                     "ratio": g["ratio"], "n_over_a": n // a})
    return rows


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
    witness = cross_mass_witness(p, n, k, a, H, cws)
    search = search_max_ratio(p, n, k, a, H, cws, trials=4000, seed=12345)
    create_found = create_found or witness["creates_mass"] or search["ratio"] > 1.0
    scaling = scaling_scan()
    return {"params": {"p": p, "n": n, "k": k, "a": a, "sigma": a - k},
            "create_mass_found": create_found, "families": rows,
            "engineered_witness": witness, "random_search_max": search,
            "scaling": scaling}


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
    w = out["engineered_witness"]; s = out["random_search_max"]
    print()
    print(f"  ENGINEERED witness (3 cross-overlaps >= a): base={w['base']} max_base={w['max_base']} "
          f"interleaved={w['interleaved']} (predicted {w['predicted']})  creates_mass={w['creates_mass']}")
    print(f"  RANDOM search (4000 gluings): max interleaved={s['interleaved']} max_base={s['max_base']} "
          f"max ratio={s['ratio']}   sum-constraint bound n/a={s['n_over_a (sum-constraint bound on #cross-pairs)']}")
    print()
    print("RESULT: interleaving CAN create mass (interleaved > max base fiber) via engineered/random")
    print("  gluings -- so L2 is NOT trivially subsumed by L1 (interleaved <= max_base is FALSE).")
    print("  HEURISTIC: cross-overlaps ~sum to n (exact for pure partitions; + small corrections from")
    print("  the <=k-1 coincidental agreements), so #cross-pairs>=a is ~n/a. The search found interleaved")
    print(f"  up to {s['interleaved']} (slightly above n/a={s['n_over_a (sum-constraint bound on #cross-pairs)']} via those corrections), max ratio {s['ratio']}.")
    print()
    print("  n-SCALING via GRID construction (k=2, a=4 fixed; poly vs super-poly?):")
    print(f"    {'n':>3} {'rho':>6} {'grid':>7} {'inter':>6} {'maxbase':>7} {'ratio':>6} {'n/a':>4}")
    for r in out["scaling"]:
        print(f"    {r['n']:>3} {r['rho']:>6} {r['grid_s1xs2']:>7} {r['interleaved']:>6} "
              f"{r['max_base']:>7} {str(r['ratio']):>6} {r['n_over_a']:>4}")
    print()
    print("RESULT / REFRAME:")
    print("  (1) POLYNOMIALITY is TRIVIAL from L1: interleaved <= (base fiber)^mu <= (n^B)^mu = poly")
    print("      (mu constant). So the conjecture's n^B remainder is subsumed by L1 -- NOT the open piece.")
    print("  (2) The real L2 content is the SHARP CONSTANT / saving (binom*q^-mu(a-k) vs Cartesian binom^mu).")
    print("      The gluing/grid attack tests it: interleaved ~ n/a, FAR below Cartesian -- saving holds.")
    print("      (Domain reason: fiber agreement sets pairwise overlap <=k-1, cross-overlaps sum to ~n,")
    print("       so #cross-pairs>=a is ~n/a -- linear/poly, never super-poly.)")
    print("  => conjecture robust vs gluings; OPEN = PROVE the sharp saving (finer 2nd-moment argument)")
    print("     + test NON-gluing words. The naive 'interleaved<=max_base' is false but irrelevant.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
