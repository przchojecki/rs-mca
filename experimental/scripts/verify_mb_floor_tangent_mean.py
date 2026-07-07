#!/usr/bin/env python3
"""The subfield census floor M_B(d1) as a tangent-column mean: identity,
replay of the printed values, and the per-level subfield table.

IDENTITY (one line). In prop:capg-census-floor's notation, m' = K - 1 + d1
gives d1 - 1 = m' - K, hence

    M_B(d1) = C(m',m) * ceil( C(n,m') * p^-(d1-1) )
            = C(m',m) * ceil( C(n,m') * p^(K-m') ),

and C(n,m') * p^(K-m') is exactly the first-moment ("tangent-column") mean:
the expected number of base-field codewords (p^K of them, each hitting a
fixed m'-set with probability p^-m') at agreement m', each contributing
C(m',m) size-m supports through the binomial-moment formula. The floors
are therefore first-moment means achieved by prefix pigeonhole — which is
also why the deployed pair locations are first-moment-predictable (the
list-row unsafe test IS "tangent mean > floor(q*eps)").

This script replays, with exact integers / lgamma cross-checks:
  (a) the eight printed floor values (67.1/56.0/43.9/31.3 KoalaBear;
      52.1/41.0/28.9/16.2 Mersenne-31) at the deployed (K,m);
  (b) the boundary values by exact bit-length arithmetic (67.10, 52.11);
  (c) the per-level subfield table at the KoalaBear row: replacing p by
      p^d for the intermediate subfields d | 6 kills the floor by
      ~2.09M / 4.18M / 10.45M bits at the deployed profiles — the
      subfield correction is exactly ONE level deep there (only the base
      level carries mass; the d = 6 column is the q-scale model the
      proposition itself refutes as a global normalizer).

Runtime ~1 minute. Writes experimental/data/mb_floor_tangent_mean.json.
"""
import json
import math
import os
from math import lgamma, log2

LN2 = math.log(2)


def log2_comb(n, m):
    return (lgamma(n + 1) - lgamma(m + 1) - lgamma(n - m + 1)) / LN2


def log2_int(x):
    b = x.bit_length()
    if b <= 64:
        return log2(x)
    return (b - 64) + log2(x >> (b - 64))


def main():
    N, K = 1 << 21, 1 << 20
    rows = [("KoalaBear list", 2**31 - 2**24 + 1, 6, 1116046,
             [67.1, 56.0, 43.9, 31.3]),
            ("Mersenne-31 list", 2**31 - 1, 4, 1116022,
             [52.1, 41.0, 28.9, 16.2])]
    out = []
    for name, p, ext_deg, m, printed in rows:
        w = m - K
        lp = log2(p)
        vals = []
        for j in range(4):
            d1 = w + 1 + j
            mp = K - 1 + d1
            assert mp == m + j and (d1 - 1) == (mp - K)   # the identity
            bits = log2_comb(mp, m) + log2_comb(N, mp) - (d1 - 1) * lp
            vals.append(round(bits, 1))
        boundary_exact = round(
            log2_int(math.comb(N, m)) - log2_int(pow(p, w)), 2)
        ok = vals == printed
        print(f"{name}: M_B bits {vals} (printed {printed}) "
              f"{'REPLAY OK' if ok else 'MISMATCH'}; boundary exact "
              f"{boundary_exact}")
        out.append({"row": name, "p": p, "ext_deg": ext_deg, "m": m,
                    "w": w, "mb_bits": vals, "printed": printed,
                    "replay_ok": ok, "boundary_exact_bits": boundary_exact})
        assert ok
    # per-level subfield table at the KoalaBear row
    p, m = 2**31 - 2**24 + 1, 1116046
    w, lp = m - K, log2(p)
    table = []
    for j in range(2):
        d1 = w + 1 + j
        mp = m + j
        lc = log2_comb(mp, m) + log2_comb(N, mp)
        row = {"d1_offset": j,
               **{f"level_p^{d}": round(lc - (d1 - 1) * d * lp, 1)
                  for d in (1, 2, 3, 6)}}
        table.append(row)
        print("per-level:", row)
    out.append({"per_level_koalabear": table,
                "reading": "subfield correction is ONE level deep at the "
                           "deployed profiles; d>=2 levels dead by ~2-10 "
                           "million bits"})
    here = os.path.dirname(os.path.abspath(__file__))
    dst = os.path.join(here, "..", "data", "mb_floor_tangent_mean.json")
    with open(dst, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {os.path.normpath(dst)}")


if __name__ == "__main__":
    main()
