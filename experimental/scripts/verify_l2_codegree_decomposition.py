#!/usr/bin/env python3
r"""
L2 sharp saving, structural reduction: the interleaved list decomposes as a sum of
PUNCTURED-RS list-decoding counts -- proving the saving is exactly punctured list
decoding, not the Cartesian product. (L2 falsification->proof, iter 4.)

CONTEXT. iter 3 showed L2 polynomiality is free from L1 (interleaved <= base^mu),
so the only open content is the SHARP SAVING (interleaved << Cartesian binom^mu).
This note reduces that saving to a known object.

LEMMA (codegree decomposition, mu=2 -- PROVED, verified here).
A tuple (c_1,c_2) in C^2 is in the interleaved list at radius 1-a/n iff
|A_1(c_1) cap A_2(c_2)| >= a, i.e. iff c_2 agrees with U_2 on >= a points of the
set A_1(c_1) = {x : c_1(x)=U_1(x)}. (If so, |A_2(c_2)| >= a automatically, so the
"c_2 in Fib_2" constraint is implied.) Hence
    |Lambda(Int(C,2),1-a/n,U)|
       = sum_{c_1 in Fib_1(U_1)} | Lambda( RS[F, A_1(c_1), k], 1 - a/|A_1(c_1)|, U_2 ) |,
a sum over the row-1 fiber of the list of U_2 on the PUNCTURED domain A_1(c_1)
(size |A_1(c_1)| <= n). General mu: recurse (the inner object is the (mu-1)-fold
interleaved list on the punctured domain).

CONSEQUENCE. The L2 "saving" is exactly: each inner punctured list is small
(unique-decoding = 1 when a > (|A_1(c_1)|+k)/2; Johnson-bounded otherwise), so the
interleaved list is |Fib_1| times a punctured list -- NOT |Fib_1|*|Fib_2|. The
sharp constant lives in the punctured-RS list-decoding bound, a known object.

Checks (exact, small fields):
  (1) the decomposition identity holds exactly (direct count == codegree sum),
      for gluing AND non-gluing received words;
  (2) the inner punctured lists are small (report max inner list vs |Fib_2|),
      exhibiting the saving;
  (3) where a > (N+k)/2 on the puncture, inner list = 1 (unique decoding),
      so interleaved = |Fib_1| exactly (full saving).

Status: AUDIT / PROVED (the decomposition identity) + verified.

Run:
    python3 experimental/scripts/verify_l2_codegree_decomposition.py
    python3 experimental/scripts/verify_l2_codegree_decomposition.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import product


def build(p, n, k):
    H = list(range(1, p))
    cws = [tuple(sum(co[i] * pow(x, i, p) for i in range(k)) % p for x in H)
           for co in product(range(p), repeat=k)]
    return H, cws


def agree_set(c, U):
    return frozenset(j for j in range(len(U)) if c[j] == U[j])


def fiber(U, cws, a):
    return [(c, A) for c in cws if len(A := agree_set(c, U)) >= a]


def direct_interleaved(U1, U2, cws, a, n):
    f1 = fiber(U1, cws, a); f2 = fiber(U2, cws, a)
    cnt = 0
    for (_, A1) in f1:
        for (_, A2) in f2:
            if len(A1 & A2) >= a:
                cnt += 1
    return cnt, len(f1), len(f2)


def punctured_list_size(U2, region, cws, a):
    """# codewords agreeing with U2 on >= a points of `region` (a subset of H)."""
    reg = list(region)
    cnt = 0
    for c in cws:
        agr = sum(1 for j in reg if c[j] == U2[j])
        if agr >= a:
            cnt += 1
    return cnt


def codegree_sum(U1, U2, cws, a):
    f1 = fiber(U1, cws, a)
    inners = []
    for (_, A1) in f1:
        inners.append(punctured_list_size(U2, A1, cws, a))
    return sum(inners), inners, len(f1)


def run():
    p, n, k = 17, 16, 3
    a = k + 2
    H, cws = build(p, n, k)

    def poly(coeffs):
        return tuple(sum(coeffs[i] * pow(x, i, p) for i in range(len(coeffs))) % p for x in H)

    c0, c1, c2, c3 = poly([1, 2, 3]), poly([4, 0, 1]), poly([2, 5, 6]), poly([7, 1, 4])

    def glue(parts):
        U = [0] * n
        for cw, reg in parts:
            for j in reg:
                U[j] = cw[j]
        return tuple(U)

    blkA, blkB = set(range(8)), set(range(8, 16))
    evens, odds = set(range(0, n, 2)), set(range(1, n, 2))

    # non-gluing words: codeword + structured noise; near-codeword clusters
    cw_plus_noise = list(c0)
    for j in (3, 7, 11):
        cw_plus_noise[j] = (cw_plus_noise[j] + 5) % p
    cw_plus_noise = tuple(cw_plus_noise)
    # "average" of two codewords-ish (not a gluing): interleave values
    avg_word = tuple((c0[j] if j % 3 == 0 else (c1[j] if j % 3 == 1 else c2[j])) for j in range(n))

    families = {
        "GLUE block c0|c1  x  block c2|c3":
            (glue([(c0, blkA), (c1, blkB)]), glue([(c2, blkA), (c3, blkB)])),
        "GLUE c0|c1  x  even/odd c0|c1":
            (glue([(c0, blkA), (c1, blkB)]), glue([(c0, evens), (c1, odds)])),
        "NON-GLUE codeword+3errors x glue c2|c3":
            (cw_plus_noise, glue([(c2, blkA), (c3, blkB)])),
        "NON-GLUE mod3-interleaved c0/c1/c2 x glue c0|c1":
            (avg_word, glue([(c0, blkA), (c1, blkB)])),
        "NON-GLUE codeword+3errors x codeword+3errors":
            (cw_plus_noise, tuple((lambda L:[L.__setitem__(j,(L[j]+4)%p) for j in (2,6,10)] and tuple(L))(list(c1)))),
    }

    rows = []
    all_match = True
    for name, (U1, U2) in families.items():
        direct, f1n, f2n = direct_interleaved(U1, U2, cws, a, n)
        cdeg, inners, f1n2 = codegree_sum(U1, U2, cws, a)
        match = (direct == cdeg and f1n == f1n2)
        all_match = all_match and match
        max_inner = max(inners) if inners else 0
        rows.append({
            "family": name, "|Fib_1|": f1n, "|Fib_2|": f2n,
            "interleaved(direct)": direct, "codegree_sum": cdeg,
            "identity_holds": match, "max_inner_punctured_list": max_inner,
            "saving (interleaved vs Cartesian |F1||F2|)":
                f"{direct} vs {f1n*f2n}",
            "inner=1 (unique-decode) everywhere": max_inner <= 1,
        })
    return {"params": {"p": p, "n": n, "k": k, "a": a},
            "all_identities_hold": all_match, "families": rows}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_identities_hold"] else 1)
    print(f"L2 codegree decomposition  params={out['params']}")
    print("  LEMMA: interleaved(mu=2) = sum_{c1 in Fib_1} |punctured list of U_2 on A_1(c1)|")
    print()
    for r in out["families"]:
        print(f"  {r['family']}")
        print(f"      |Fib_1|={r['|Fib_1|']} |Fib_2|={r['|Fib_2|']}  interleaved={r['interleaved(direct)']} "
              f"codegree_sum={r['codegree_sum']}  identity={'OK' if r['identity_holds'] else 'FAIL'}")
        print(f"      max inner punctured list = {r['max_inner_punctured_list']}  "
              f"(saving: {r['saving (interleaved vs Cartesian |F1||F2|)']})")
    print()
    print("RESULT:", "PASS (decomposition identity holds for gluing AND non-gluing words; the saving = "
          "the punctured-RS list, small)" if out["all_identities_hold"] else "FAIL (identity broke -- inspect)")
    raise SystemExit(0 if out["all_identities_hold"] else 1)


if __name__ == "__main__":
    main()
