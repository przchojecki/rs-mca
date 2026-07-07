#!/usr/bin/env python3
"""The (41,20,10,2) mode-at-null datum: exhaustive computation + structure
classification of the argmax prefix fiber.

At (p, N, m, w) = (41, 20, 10, 2), D = mu_20 subset F_41* (the quadratic
residues), the depth-2 power-sum prefix map has

    N(0,0) = 66   (null fiber; mean = C(20,10)/41^2 = 109.9)
    N(11,0) = 133 = max,

so the raw mode-at-null inequality N_w(z) <= N_w(0) of
prob:capfr1-mode-null FAILS at this row — and it fails by NULL
SUPPRESSION, not by a spiked maximum: the max is 2.2 sigma above mean,
BELOW the Poisson-expected maximum (~150 over 41^2 cells), while the null
fiber sits 4.2 sigma BELOW the mean. This script recomputes the histogram
exhaustively (independent of the DP code path), extracts the argmax,
verifies dilation equivariance (the whole line (mu_20*11, 0) carries equal
fibers), and classifies every member of the argmax fiber:

    coset-union members (unions of mu_2-antipodal pairs): 0
    dilation-stable members (gS = S for some g != 1):     0

so the fiber is not charged by the obvious quotient-pullback classifiers.
The sibling half-group row (101, 50, 25, 2) has null = max to float
precision (see qsp_fiber_census.py), so the suppression is row-arithmetic
finer than the p = 2N+1 pattern; the explanation is open.

Runtime: seconds. Writes experimental/data/rowsharp_q_modeatnull_datum.json.
"""
import itertools
import json
import math
import os
from collections import defaultdict

P, N, M, W = 41, 20, 10, 2


def main():
    g = next(c for c in range(2, P)
             if all(pow(c, (P - 1) // r, P) != 1 for r in (2, 5)))
    h = pow(g, (P - 1) // N, P)
    D = sorted(pow(h, i, P) for i in range(N))
    fib = defaultdict(list)
    for S in itertools.combinations(D, M):
        fib[(sum(S) % P, sum(x * x for x in S) % P)].append(S)
    null = len(fib[(0, 0)])
    zstar, members = max(fib.items(), key=lambda kv: len(kv[1]))
    mx = len(members)
    mean = math.comb(N, M) / P ** W
    sd = math.sqrt(mean)
    orbit_sizes = sorted({len(fib[((g_ * zstar[0]) % P,
                                   (g_ * g_ * zstar[1]) % P)]) for g_ in D})

    def is_pair_union(S):
        Ss = set(S)
        return all((P - x) % P in Ss for x in S)

    def dilation_stable(S):
        Ss = set(S)
        return any(all((g_ * x) % P in Ss for x in S) for g_ in D if g_ != 1)

    pair_unions = sum(1 for S in members if is_pair_union(S))
    dil_stable = sum(1 for S in members if dilation_stable(S))
    out = {"row": {"p": P, "N": N, "m": M, "w": W},
           "null_fiber": null, "max_fiber": mx, "argmax_prefix": list(zstar),
           "mean": mean,
           "null_sigmas_below_mean": (mean - null) / sd,
           "max_sigmas_above_mean": (mx - mean) / sd,
           "dilation_orbit_fiber_sizes": orbit_sizes,
           "argmax_members_coset_union": pair_unions,
           "argmax_members_dilation_stable": dil_stable,
           "mode_at_null_raw": null >= mx}
    print(json.dumps(out, indent=1))
    assert null == 66 and mx == 133 and zstar[1] == 0
    assert orbit_sizes == [133] and pair_unions == 0 and dil_stable == 0
    here = os.path.dirname(os.path.abspath(__file__))
    dst = os.path.join(here, "..", "data", "rowsharp_q_modeatnull_datum.json")
    with open(dst, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {os.path.normpath(dst)}")


if __name__ == "__main__":
    main()
