#!/usr/bin/env python3
r"""
Line-decoding reading of the deep-point bridge  (M2 / X1).

Increment 9 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.

The simple-pole line `f_alpha + z g_alpha` is a concrete one-parameter (line)
family. Its **line-decoding list** at radius `delta_a = 1-a/n` is the set of
slopes `z` for which the line passes within `delta_a` of a codeword of
`C = RS[F,D,k]`:

    LD(alpha; delta_a) = { z : exists c in C, |{x : f_alpha(x)+z g_alpha(x)=c(x)}| >= a }.

By the base identity (§1), `f_alpha + z g_alpha` is `delta_a`-close to `C` iff
`z in Deep_alpha(U,a)`, and the closing codeword is unique (global far
condition). Therefore on this line family

    LD(alpha; delta_a) = Bad_MCA(alpha; delta_a) = Bad_CA(alpha; delta_a) = Deep_alpha(U,a),

i.e. **support-wise MCA, no-loss CA, and line-decoding all COINCIDE** on the
simple-pole family, each equal to the deep image (the SLOPE sets coincide; a
single slope may have several closing codewords -- distinct `C_+` list elements
`P` with the same `P(alpha)` -- so the incidence multiplicity tracks list size).

M2 consequence: no MCA-vs-line-decoding separation occurs on this line family
(they are equal), so any genuine separation must come from other line families;
and the line-decoding count here is `list`-controlled (`<= |Lambda(C_+,delta_a,U)|`),
exactly as the MCA count.  The interleaved `mu`-row shared-pole curve has
simultaneous line-decoding list `Deep_alpha^{mu}(U,a)` (§2).

This is an honest reading/corollary of the base identity, not a new theorem.
Status: AUDIT / PROVED-by-check.  Supports M2 (line-decoding form) and X1.

Run:
    python3 experimental/scripts/verify_x1_line_decoding.py
    python3 experimental/scripts/verify_x1_line_decoding.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_x1_deep_point_identity import (   # noqa: E402
    multiplicative_subgroup, interpolate, poly_eval, degree,
    support_close_slope, deep_image, bad_mca, global_far_condition, make_words,
)


def line_decoding_incidences(U, D, k, a, alpha, p):
    """Return {z: frozenset(codeword poly keys)} : the (slope, codeword) incidences
    of the simple-pole line f_alpha + z g_alpha that decode within delta_a."""
    inv = {x: pow((x - alpha) % p, -1, p) for x in D}
    f = {x: (U[x] * inv[x]) % p for x in D}
    g = {x: (-inv[x]) % p for x in D}
    incidences = {}
    for S in combinations(D, a):
        fI = interpolate([(x, f[x]) for x in S], p)
        gI = interpolate([(x, g[x]) for x in S], p)
        z = support_close_slope(fI, gI, k, a, p)
        if z is None:
            continue
        # the closing codeword c = (f + z g) interpolated on S (deg < k)
        cI = interpolate([(x, (f[x] + z * g[x]) % p) for x in S], p)
        if degree(cI, p) < k:
            incidences.setdefault(z, set()).add(tuple(cI))
    return incidences


def run():
    results = []
    all_ok = True
    for (p, n, k, a) in [(17, 8, 3, 5), (17, 8, 4, 6), (41, 8, 3, 5)]:
        D = multiplicative_subgroup(p, n)
        Dset = set(D)
        deep_points = [al for al in range(p) if al not in Dset]
        cfg = {"p": p, "n": n, "k": k, "a": a, "checks": 0, "ok": True,
               "max_codewords_per_slope": 0}
        for alpha in deep_points:
            assert global_far_condition(D, k, alpha, p)
            for name, U in make_words(D, k, p):
                deep = deep_image(U, D, k, a, alpha, p)
                mca = bad_mca(U, D, k, a, alpha, p)
                inc = line_decoding_incidences(U, D, k, a, alpha, p)
                ld_slopes = set(inc.keys())
                # CLAIM: the three SLOPE sets coincide (MCA = CA = line-decoding).
                # A slope may have several closing codewords -- distinct C_+ list
                # elements P with the same P(alpha) -- so incidence multiplicity
                # tracks the list size, not a failure.
                coincide = (ld_slopes == mca == deep)
                cfg["max_codewords_per_slope"] = max(
                    cfg["max_codewords_per_slope"],
                    max((len(c) for c in inc.values()), default=0))
                cfg["checks"] += 1
                if not coincide:
                    cfg["ok"] = False
                    all_ok = False
        results.append(cfg)
    return {"all_ok": all_ok, "configs": results}


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
    print("Line-decoding reading: LD(alpha) = Bad_MCA = Bad_CA = Deep_alpha(U,a)")
    print("(support-wise MCA, no-loss CA, and line-decoding COINCIDE on the simple-pole family)")
    print()
    for c in out["configs"]:
        print(f"  [{'OK ' if c['ok'] else 'FAIL'}] p={c['p']} n={c['n']} k={c['k']} a={c['a']}"
              f"  coincidence_checks={c['checks']}"
              f"  max_codewords_per_slope={c['max_codewords_per_slope']} (= list multiplicity)")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
