#!/usr/bin/env python3
"""Exact prefix-fiber and shift-pair censuses for the row-sharp Q calibration.

(Q side)  Full fiber histogram of the depth-w power-sum prefix map on
m-subsets of the order-N subgroup D of F_p* (Newton-equivalent to the
elementary-symmetric prefix map for w < p: identical fibers). Reports
max fiber, null fiber, mean, and the exact second moment
sum_z N_w(z)^2 (= C(n,m) + total shift-pair mass, thm:capg-second-moment).

(SP side) Exact top shift-pair stratum sp_w(w+1; D): ordered pairs of
DISJOINT (w+1)-subsets with matching depth-w prefixes (equivalently pairs
(A, c) with A and A - c both split, top stratum of the second-moment
ledger), by a joint (|S|, |T|, prefix-difference) dynamic program.

Arithmetic: int64 (exact) whenever C(N,m) < 2^62; float64 otherwise
(flagged in output; validated against the exact path on overlapping rows;
checksum sum_z N_w(z) = C(N,m) printed for both). Memory-lean slice
updates: peak ~ (m+1) * p^w * 8 bytes.

Usage:
    python3 qsp_fiber_census.py            # full calibration + ladder set
    python3 qsp_fiber_census.py fiber:257,64,34,2 sp:101,50,2   # selection

Appends results to experimental/data/rowsharp_q_external_calibration.json.
"""
import json
import math
import os
import sys

import numpy as np

FIBER_DEFAULT = [
    (17, 16, 8, 1), (17, 16, 8, 2), (17, 16, 8, 3),
    (41, 20, 10, 1), (41, 20, 10, 2), (41, 20, 10, 3),
    (257, 64, 34, 1), (257, 64, 34, 2),
    (101, 50, 25, 2), (101, 50, 25, 3),
    (577, 96, 48, 2), (1153, 128, 64, 2),
]
SP_DEFAULT = [
    (17, 16, 2), (41, 20, 2), (101, 50, 2), (257, 64, 2), (577, 96, 2),
    (1153, 128, 2), (17, 16, 3), (41, 20, 3), (101, 50, 3),
]


def subgroup(p, N):
    g = next(c for c in range(2, p)
             if all(pow(c, (p - 1) // r, p) != 1
                    for r in set(_factors(p - 1))))
    h = pow(g, (p - 1) // N, p)
    return sorted(pow(h, i, p) for i in range(N))


def _factors(x):
    out, d = [], 2
    while d * d <= x:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    if x > 1:
        out.append(x)
    return out


def ndroll(a, shifts):
    for ax, s in enumerate(shifts):
        a = np.roll(a, s, axis=ax)
    return a


def fiber_census(p, N, m, w):
    D = subgroup(p, N)
    exact = math.comb(N, m) < (1 << 62)
    dtype = np.int64 if exact else np.float64
    dp = [np.zeros((p,) * w, dtype=dtype) for _ in range(m + 1)]
    dp[0][(0,) * w] = 1
    for x in D:
        v = [pow(x, h, p) for h in range(1, w + 1)]
        for c in range(m - 1, -1, -1):
            dp[c + 1] += ndroll(dp[c], v)
    fib = dp[m]
    total = fib.sum()
    expected = math.comb(N, m)
    if exact:
        assert int(total) == expected, (int(total), expected)
        second = int((fib.astype(object) ** 2).sum())
    else:
        assert abs(float(total) - expected) / expected < 1e-12
        second = float((fib.astype(np.float64) ** 2).sum())
    mx, nullf = fib.max(), fib[(0,) * w]
    mean = expected / p ** w
    return {"kind": "fiber", "p": p, "N": N, "m": m, "w": w,
            "exact_int64": exact,
            "max": int(mx) if exact else float(mx),
            "null": int(nullf) if exact else float(nullf),
            "mean": mean,
            "max_over_mean_minus_1": float(mx) / mean - 1.0,
            "null_over_mean_minus_1": float(nullf) / mean - 1.0,
            "sum_N2": str(second),
            "sp_total_mass": str(second - expected) if exact else None}


def sp_top_census(p, N, w):
    k = w + 1
    D = subgroup(p, N)
    dp = np.zeros((k + 1, k + 1) + (p,) * w, dtype=np.int64)
    dp[(0, 0) + (0,) * w] = 1
    for x in D:
        v = [pow(x, h, p) for h in range(1, w + 1)]
        vneg = [(-s) % p for s in v]
        add_S = np.stack([np.stack([ndroll(dp[a, b], v)
                                    for b in range(k + 1)]) for a in range(k)])
        add_T = np.stack([np.stack([ndroll(dp[a, b], vneg)
                                    for b in range(k)]) for a in range(k + 1)])
        dp[1:, :] += add_S
        dp[:, 1:] += add_T
    sp = int(dp[(k, k) + (0,) * w])
    model = math.comb(N, k) * math.comb(N - k, k) / p ** w
    return {"kind": "sp_top", "p": p, "N": N, "w": w, "k": k,
            "sp_top_ordered_pairs": sp, "model": model,
            "sp_over_model": sp / model}


def main():
    fiber_jobs, sp_jobs = [], []
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            tag, nums = a.split(":")
            tup = tuple(int(x) for x in nums.split(","))
            (fiber_jobs if tag == "fiber" else sp_jobs).append(tup)
    else:
        fiber_jobs, sp_jobs = FIBER_DEFAULT, SP_DEFAULT
    results = []
    for job in fiber_jobs:
        r = fiber_census(*job)
        results.append(r)
        print(f"fiber ({r['p']},{r['N']},{r['m']},{r['w']})"
              f"{' EXACT' if r['exact_int64'] else ' f64'}: "
              f"max/mean-1 = {r['max_over_mean_minus_1']:.4e}, "
              f"null/mean-1 = {r['null_over_mean_minus_1']:.4e}, "
              f"max = {r['max']}, null = {r['null']}")
    for job in sp_jobs:
        r = sp_top_census(*job)
        results.append(r)
        print(f"sp    ({r['p']},{r['N']},{r['w']}): sp_top = "
              f"{r['sp_top_ordered_pairs']}, sp/model = {r['sp_over_model']:.3f}")
    here = os.path.dirname(os.path.abspath(__file__))
    dst = os.path.join(here, "..", "data",
                       "rowsharp_q_external_calibration.json")
    old = []
    if os.path.exists(dst):
        old = json.load(open(dst))
    keyf = lambda r: (r["kind"],) + tuple(r.get(x) for x in ("p", "N", "m", "w"))
    seen = {keyf(r) for r in results}
    merged = [r for r in old if keyf(r) not in seen] + results
    with open(dst, "w") as f:
        json.dump(merged, f, indent=1)
    print(f"wrote {os.path.normpath(dst)} ({len(merged)} entries)")


if __name__ == "__main__":
    main()
