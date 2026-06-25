#!/usr/bin/env python3
r"""
L2 codegree theorem: is the two-regime corollary's input M_2(a+sigma) <= poly
weaker than L1, or does it need the same aperiodic bound? (verify-first.)

The two-regime theorem (verify_l2_reduction_bound.py) gives
    |Lambda_2| <= |Fib_2| + M_2(2a-k) |Fib_1|,   2a-k = a+sigma,
so the saving (exponent B) holds iff M_2(a+sigma) <= poly, where
M_2(s) = #{codewords agreeing with U_2 on >= s of n points} = base list at
agreement s. Since a+sigma = k+2sigma is far below the unique-decoding radius
(n+k)/2 at near capacity, M_2(a+sigma) is a list-decoding-regime count, NOT
automatically small; L1 only gives the monotone M_2(a+sigma) <= M_2(a) <= n^B,
which yields |Lambda_2| <= n^{2B} (no saving).

CLAIM TESTED: M_2(a+sigma) <= poly is an APERIODIC statement -- quotient-periodic
words (U_2 a function of x^M, M|gcd(n,k)) keep a LARGE list at agreement a+sigma
(the quotient mass), while generic/aperiodic words drop. So the saving needs the
aperiodic restriction (an L1-family input), not weaker than L1.

Measures, per word type, the profile ratio M_2(a+sigma)/M_2(a): if periodic words
keep it ~1 while generic words drop it, the corollary's hypothesis is aperiodic.

Status: AUDIT / VERIFY-FIRST (honest check of the two-regime corollary's input).

Run:
    python3 experimental/scripts/verify_l2_profile_decay.py
"""

from __future__ import annotations

import argparse
import json
import random
from itertools import product


def build_cws(p, H, k):
    return [tuple(sum(co[j] * pow(x, j, p) for j in range(k)) % p for x in H)
            for co in product(range(p), repeat=k)]


def list_at(U, cws, s):
    return sum(1 for c in cws if sum(1 for i in range(len(U)) if c[i] == U[i]) >= s)


def run():
    p = 17
    H = [pow(3, i, p) for i in range(p - 1)]   # F_17^* (n=16), 3 a generator
    n = len(H)
    rng = random.Random(7)
    out = {}
    for k in (2, 4):                            # k=4 so M=2|gcd(16,4); a+sigma meaningful
        cws = build_cws(p, H, k)
        sigma = 1
        a = k + sigma
        types = {}
        # generic random words
        gmax = 0
        for _ in range(300):
            U = [rng.randrange(p) for _ in range(n)]
            m_a = list_at(U, cws, a)
            if m_a >= 2:
                ratio = list_at(U, cws, a + sigma) / m_a
                gmax = max(gmax, ratio)
        types["generic_random_max_ratio"] = round(gmax, 3)
        # quotient-periodic words: U = function of x^M (folded), M=2
        M = 2
        pmax = 0
        pbest = None
        for _ in range(300):
            # value depends only on x^M  => U(x) = g(x^M)
            gtab = {}
            U = []
            for x in H:
                key = pow(x, M, p)
                if key not in gtab:
                    gtab[key] = rng.randrange(p)
                U.append(gtab[key])
            m_a = list_at(U, cws, a)
            if m_a >= 2:
                r = list_at(U, cws, a + sigma) / m_a
                if r > pmax:
                    pmax = r; pbest = (m_a, list_at(U, cws, a + sigma))
        types["periodic(x^M)_max_ratio"] = round(pmax, 3)
        types["periodic_best (M_a, M_{a+sigma})"] = pbest
        # codewords themselves (extreme periodic-ish / structured): U = a codeword
        cmax = 0
        for c in rng.sample(cws, min(50, len(cws))):
            m_a = list_at(list(c), cws, a)
            if m_a >= 2:
                cmax = max(cmax, list_at(list(c), cws, a + sigma) / m_a)
        types["codeword_max_ratio"] = round(cmax, 3)
        out[f"k={k},a={a},sigma={sigma}"] = types
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0)
    print("L2 profile decay: M_2(a+sigma)/M_2(a) by word type (F_17). Does the higher-agreement")
    print("list drop (generic) or persist (quotient-periodic)? -> is the saving input aperiodic?")
    for key, t in out.items():
        print(f"  {key}:")
        for name, v in t.items():
            print(f"      {name}: {v}")
    print()
    print("READING: if periodic ratio >> generic ratio, M_2(a+sigma)<=poly is an APERIODIC")
    print("  statement (quotient mass survives at a+sigma) -> saving needs L1-family input, NOT weaker.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
