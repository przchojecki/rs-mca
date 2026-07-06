#!/usr/bin/env python3
"""l1_t7_atlas.py -- the excess=3 (E_3 = ell+3, equivalently tail T=7+capslack)
candidate atlas for `experimental/notes/l1/l1_t7_atlas_concurrency.md`.

Enumerates ALL spectrum shapes (min-mu>=3 normalized descending fiber sizes
mu_1 >= mu_2 >= ... >= mu_j >= 3) that WOULD refute the uniform ceiling
`C' <= 2` (equivalently `E_3 <= ell+2`), i.e. with `excess := E_3-ell = 3`,
subject to the two PROVED combinatorial caps:

  (i)  pairwise cap        mu_1 + mu_2 <= ell
       (`l1_sigma_calculus.md` Lemma 3, PROVED)
  (ii) Lemma R (quad bud)  sum_k mu_k(mu_k-1) <= (ell-1)(ell-2)
       (`l1_e3_charsum_paircap.md`, PROVED)

and reports, for each shape, the smallest prime `p == 1 (mod ell)` admitting
enough cosets (`n = (p-1)/ell >= j`) to host it.

Why excess=3, not excess>=3: removing one size-3 fiber preserves realizability
(a sub-collection of the same Gamma's fibers) and lowers E_3 by exactly 1, so
any realizable excess>=3 config yields a realizable excess=3 one. Hence the
excess=3 atlas is exactly the boundary that a `C'<=2` refutation must occupy.

Bookkeeping identity (PROVED, `l1_bounded_excess_structure.md` Sec 1, PR #368):
  excess = T - 4 - capslack,  capslack := ell - (mu_1+mu_2) >= 0,
  T := sum_{k>=3}(mu_k-2).  So excess=3  <=>  T = 7 + capslack.
The capslack=0 slice is exactly "T=7 at a cap-tight top pair" -- the
"cap-tight T=7" column of the summary table.

This script is the atlas's replayable definition: it is deterministic,
stdlib-only, and regenerates the per-ell shape counts, the cap-tight (T=7)
slice, and the minimal-j frontier from nothing but the two caps above.
`experimental/scripts/verify_l1_t7_atlas.py` re-derives it independently
(a fresh reimplementation, not an import of this file) as part of its gate i.

Usage:
    l1_t7_atlas.py [ELL ...] [--json PATH] [--quiet]
        ELL ...   one or more odd primes (default: 17 19 23 29 31)
        --json    write the full per-ell shape list to PATH (large; the
                   shipped certificate `l1_t7_atlas_summary.json` carries
                   only the compact counts/tables, NOT this full dump)
        --quiet   suppress the per-shape listing, print only the summary

stdlib only, exact integer arithmetic throughout.
"""
import sys
import json


def is_prime(m):
    if m < 2:
        return False
    if m % 2 == 0:
        return m == 2
    d = 3
    while d * d <= m:
        if m % d == 0:
            return False
        d += 2
    return True


def min_prime_for(ell, j):
    """Smallest prime p == 1 (mod ell) with (p-1)/ell >= j."""
    k = j
    while True:
        p = ell * k + 1
        if is_prime(p):
            return p, k
        k += 1


def partitions_desc(total, maxpart):
    """All descending partitions of `total` into parts in [1, maxpart]."""
    def rec(rem, cap):
        if rem == 0:
            yield []
            return
        top = min(rem, cap)
        for first in range(top, 0, -1):
            for tail in rec(rem - first, first):
                yield [first] + tail
    yield from rec(total, maxpart)


def enumerate_atlas(ell, excess=3):
    """All excess=`excess` shapes obeying the pairwise cap + Lemma R.

    A shape is a descending fiber-size list mu (each >= 3). Writing the
    "excess parts" e_k := mu_k-2 >= 1, the defining equation is
    sum_k e_k = ell+excess. Enumerated as descending partitions of
    `ell+excess` with e_1 <= ell-5 (since e_2 >= 1 and the pairwise cap
    forces mu_1+mu_2 <= ell, i.e. e_1+e_2 <= ell-4, so e_1 <= ell-5),
    then filtered by the pairwise cap and Lemma R exactly.
    """
    E = ell + excess                      # = sum_k (mu_k - 2)
    LR = (ell - 1) * (ell - 2)            # Lemma R budget
    maxpart = ell - 5                     # = max possible e_1 = mu_1-2
    shapes = []
    for part in partitions_desc(E, maxpart):
        mu = [e + 2 for e in part]        # fiber sizes >= 3, descending
        if mu[0] + mu[1] > ell:            # pairwise cap
            continue
        if sum(m * (m - 1) for m in mu) > LR:   # Lemma R
            continue
        j = len(mu)
        capslack = ell - (mu[0] + mu[1])
        T = sum(m - 2 for m in mu[2:])
        assert T == 7 + capslack, (mu, T, capslack)          # identity self-check
        overdet = sum(m - 1 for m in mu) - (ell - 2)         # see note Sec 1, Theorem
        assert overdet == j + 5, (mu, overdet, j)            # j+5 self-check
        p, n = min_prime_for(ell, j)
        shapes.append(dict(mu=mu, j=j, capslack=capslack, T=T, overdet=overdet,
                            lemmaR=sum(m * (m - 1) for m in mu), LR=LR,
                            min_p=p, min_n=n))
    shapes.sort(key=lambda s: (s['capslack'], [-x for x in s['mu']]))
    return shapes


def fmt_mu(mu):
    """Compact exponent form, e.g. [14,3,3,3,3,3,3,3] -> '[14,3^7]'."""
    out = []
    i = 0
    while i < len(mu):
        j = i
        while j < len(mu) and mu[j] == mu[i]:
            j += 1
        c = j - i
        out.append("%d^%d" % (mu[i], c) if c > 1 else "%d" % mu[i])
        i = j
    return "[" + ",".join(out) + "]"


def atlas_summary(ell, shapes):
    """Per-ell summary dict: totals, cap-tight slice, min-j frontier, fat tail."""
    ntight = sum(1 for s in shapes if s['capslack'] == 0)
    minj = min(s['j'] for s in shapes)
    minj_shapes = [s for s in shapes if s['j'] == minj]
    minj_tight = [s for s in minj_shapes if s['capslack'] == 0]
    fat = [s for s in shapes if s['mu'][0] == ell - 3 and all(m == 3 for m in s['mu'][1:])]
    return dict(
        ell=ell, total=len(shapes), cap_tight_T7=ntight,
        min_j=minj, min_j_overdet=minj + 5,
        min_j_count=len(minj_shapes), min_j_cap_tight_count=len(minj_tight),
        min_j_example=fmt_mu(sorted(minj_shapes, key=lambda s: -s['mu'][0])[0]['mu']),
        fat_tail_shape=fmt_mu(fat[0]['mu']) if fat else None,
        fat_tail_j=fat[0]['j'] if fat else None,
        fat_tail_overdet=fat[0]['overdet'] if fat else None,
        fat_tail_min_p=fat[0]['min_p'] if fat else None,
        fat_tail_min_n=fat[0]['min_n'] if fat else None,
    )


def main(argv):
    ells = []
    json_path = None
    quiet = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            i += 1
            json_path = argv[i]
        elif a == "--quiet":
            quiet = True
        else:
            ells.append(int(a))
        i += 1
    if not ells:
        ells = [17, 19, 23, 29, 31]

    grand = {}
    summaries = []
    for ell in ells:
        shapes = enumerate_atlas(ell, excess=3)
        grand[ell] = shapes
        summ = atlas_summary(ell, shapes)
        summaries.append(summ)
        if not quiet:
            print("=" * 90)
            print("ell=%d  |  excess=3 (E_3=ell+3=%d) candidate shapes: %d total, %d cap-tight (T=7, capslack=0)"
                  % (ell, ell + 3, summ['total'], summ['cap_tight_T7']))
            print("-" * 90)
            print("  %-26s %3s %4s %4s %4s %8s %6s" % ("shape (mu)", "j", "cslk", "T", "od", "lemmaR", "min_p"))
            for s in shapes:
                print("  %-26s %3d %4d %4d %4d %8d %6d(n=%d)"
                      % (fmt_mu(s['mu']), s['j'], s['capslack'], s['T'], s['overdet'],
                         s['lemmaR'], s['min_p'], s['min_n']))

    if json_path:
        with open(json_path, "w") as f:
            json.dump({str(k): v for k, v in grand.items()}, f, indent=1)
        print("\n[wrote %s]" % json_path)

    print("\nSUMMARY (excess=3 atlas; min-j frontier; fat-tail [ell-3,3^k]):")
    print("%-4s %-8s %-10s %-6s %-8s %-14s %-18s" %
          ("ell", "shapes", "cap-tight", "min-j", "od(j+5)", "fat-tail od", "fat-tail min(p,n)"))
    for s in summaries:
        print("%-4d %-8d %-10d %-6d %-8d %-14d (p=%d,n=%d)"
              % (s['ell'], s['total'], s['cap_tight_T7'], s['min_j'], s['min_j_overdet'],
                 s['fat_tail_overdet'], s['fat_tail_min_p'], s['fat_tail_min_n']))
    return summaries


if __name__ == "__main__":
    main(sys.argv[1:])
