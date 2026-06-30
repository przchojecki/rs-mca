#!/usr/bin/env python3
r"""Exact characteristic-zero canonical slope count on {2,3}-smooth domains.

Status: CONDITIONAL (agents.md rule 4: the proof depends on the imported
vanishing-sum theorem thm:vsimport, exactly as Paper B's thm:23rigidity is
labelled "conditional on the import") / AUDIT cross-check (the finite values
below are certified unconditionally against brute force).

Paper B (slackMCA_v4) proves the closed form for 2-power domains
(thm:exactcount): the number of distinct canonical slopes -e_1(B) of size-l'
subsets B of mu_{N'}, N'=2^a, is

    A(N', l') = sum_{u>=0, t=l'-2u>=0, u<=n1-t} binom(n1, t) 2^t,   n1 = N'/2.

rem:23count then asks, as "future combinatorics", for the {2,3}-smooth
(mixed-radix FFT) analogue A_{2,3}(N', l') for N'=2^a 3^b, with the class
invariant a "signed pair profile together with a triangle profile". This script
supplies and machine-verifies the exact A_{2,3}(N', l') via a per-cell transfer,
and recovers thm:exactcount as the b=0 specialization.

THE STRUCTURE (proof skeleton; the verifier certifies it against brute force).
  mu_{N'} = mu_{2^a} x mu_{3^b}. By thm:23rigidity (conditional on thm:vsimport),
  e_1(S)=e_1(T) iff S \sqcup (-T) is an N-combination of rotated PAIRS {z,-z} and
  (when b>=1) rotated TRIANGLES {z, z w, z w^2}. Pairs act only on the 2-part
  (antipodal), triangles only on the 3-part (a mu_3-coset). So mu_{N'} partitions
  into n_c = 2^{a-1} * 3^{max(b-1,0)} independent CELLS, each a 2x3 block
  (one antipodal 2-part pair) x (one mu_3-coset of the 3-part); for b=0 the cell
  is the bare antipodal pair. In the antipodal-pair Z-basis {zeta_i} of
  Z[zeta_{2^a}] and the {1,w} Z-basis of Z[zeta_3], a subset's e_1 is a Z-basis
  vector whose per-cell block is the "difference type"
      d = (c^{(1)}-c^{(w2)}, c^{(w)}-c^{(w2)}),   c^{(y)} in {-1,0,1},
  the signed occupancy of the three columns of the cell. Hence DISTINCT e_1 <=>
  DISTINCT cell-type vector, and the cells are independent, so

    A_{2,3}(N', l') = #{ cell-type vectors (d_1,...,d_{n_c})
                         : l' in  (+)_c  Sizes(d_c) }                     (*)

  where Sizes(d) is the set of total sizes realizing d in one cell (Minkowski
  sum over cells). The per-cell alphabet (computed below from the 4^3 column
  occupancies) has 19 types in 4 size-classes:
      6 types with Sizes = {3};         6 types with Sizes = {2,4};
      6 types with Sizes = {1,2,3,4,5}; 1 type  with Sizes = {0,2,3,4,6}.
  For b=0 the cell is a bare pair with 3 types: {+1},{-1} (Sizes {1}) and
  {0} (Sizes {0,2}); (*) then collapses to thm:exactcount.

  (*) is evaluated exactly by a Boolean-Minkowski transfer over the n_c cells.

The number is the size of the characteristic-zero canonical bad-slope set; the
finite-field/density transfer is per-class and unchanged (rem:23count: "the norm
sieve transfers unchanged once the characteristic-zero classes are fixed").
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from math import comb, log, log2
from pathlib import Path

# ---------------------------------------------------------------------------
# Per-cell alphabets (derived, not hand-entered)
# ---------------------------------------------------------------------------
# one column occupancy of an antipodal pair: (signed count c, size)
_COL = [(0, 0), (1, 1), (-1, 1), (0, 2)]  # empty / {+} / {-} / both


def cell_alphabet_b_ge_1():
    """2x3 cell: 3 columns (mu_3 fibers) over one antipodal pair.
    Returns dict: difference-type d -> sorted achievable sizes."""
    table: dict[tuple[int, int], set[int]] = {}
    for (c1, s1), (cw, sw), (cw2, sw2) in product(_COL, _COL, _COL):
        d = (c1 - cw2, cw - cw2)
        table.setdefault(d, set()).add(s1 + sw + sw2)
    return {d: sorted(s) for d, s in table.items()}


def cell_alphabet_b_eq_0():
    """Bare antipodal pair (no 3-part): type c in {-1,0,1}."""
    return {(1,): [1], (-1,): [1], (0,): [0, 2]}


# ---------------------------------------------------------------------------
# Structural count via Boolean-Minkowski transfer  (the closed form (*))
# ---------------------------------------------------------------------------
def struct_count(a: int, b: int, lmax: int) -> list[int]:
    """A_{2,3}(2^a 3^b, l') for l'=0..lmax."""
    if b == 0:
        alpha = cell_alphabet_b_eq_0()
        n_c = 1 << (a - 1)
    else:
        alpha = cell_alphabet_b_ge_1()
        n_c = (1 << (a - 1)) * (3 ** (b - 1))
    keep = (1 << (lmax + 1)) - 1
    masks = []
    for sizes in alpha.values():
        m = 0
        for s in sizes:
            if s <= lmax:
                m |= 1 << s
        masks.append(m)
    dist = Counter({1: 1})  # state = reachable-size bitmask; start reachable={0}
    for _ in range(n_c):
        nd: Counter = Counter()
        for state, cnt in dist.items():
            for m in masks:
                ns = 0
                mm = m
                while mm:
                    s = (mm & -mm).bit_length() - 1
                    ns |= state << s
                    mm &= mm - 1
                nd[ns & keep] += cnt
        dist = nd
    out = [0] * (lmax + 1)
    for state, cnt in dist.items():
        for l in range(lmax + 1):
            if state & (1 << l):
                out[l] += cnt
    return out


def exactcount_2power(a: int, l: int) -> int:
    """Paper B thm:exactcount closed form for N'=2^a."""
    n1 = 1 << (a - 1)
    tot = 0
    u = 0
    while l - 2 * u >= 0:
        t = l - 2 * u
        if u <= n1 - t and t <= n1:
            tot += comb(n1, t) * (2 ** t)
        u += 1
    return tot


# ---------------------------------------------------------------------------
# Entropy exponent  beta_{2,3}(rho) = lim_{N'->oo} (1/N') log2 A_{2,3}(N', rho N')
# ---------------------------------------------------------------------------
# Each cell draws one of the 19 (b>=1) / 3 (b=0) types; the size it contributes
# lies in [min Sizes(d), max Sizes(d)]. The per-cell min/max multisets:
_MIN23 = [0] + [1] * 6 + [2] * 6 + [3] * 6          # {0:1,1:6,2:6,3:6}
_MAX23 = [6 - m for m in _MIN23]                    # {6:1,5:6,4:6,3:6}; min<->6-max
_MIN2 = [0, 1, 1]                                    # b=0 pair: {0}->{0,2},{+1},{-1}->{1}
_MAX2 = [2, 1, 1]


def saddle_beta(rho: float, MINv=_MIN23, MAXv=_MAX23, cell: int = 6) -> float:
    """Large-deviation exponent of A = #{type-vectors : l' in (+)_c Sizes(d_c)}.

    To exponential order l' in the Minkowski sum  <=>  sum_c min_c <= l' <= sum_c
    max_c (one step-1 type {1..5} closes every gap), so by Cramer / the method of
    types

        beta(rho) = (1 / (cell*ln2)) * max{ H(p) : p in simplex_T,
                       sum_i p_i min_i <= cell*rho <= sum_i p_i max_i }.

    Plateau = log2(T)/cell wherever the uniform p is feasible; off the plateau the
    binding constraint gives the tilted (Gibbs) optimiser p_i ~ exp(-lam*min_i),
    lam>=0 fixed by sum p_i min_i = cell*rho.  cell = N'/n_c = 6 (resp. 2 for b=0).
    """
    nt = len(MINv)
    lo = sum(MINv) / nt / cell                       # uniform sum(p*min)/cell
    hi = sum(MAXv) / nt / cell                        # uniform sum(p*max)/cell
    if lo <= rho <= hi:
        return log2(nt) / cell
    if rho > hi:                                      # reflect onto the min-binding side
        MINv = [cell - m for m in MAXv]
        rho = 1.0 - rho
    target = cell * rho
    mean = lambda x: sum(m * x ** m for m in MINv) / sum(x ** m for m in MINv)
    a_, b_ = 1e-308, 1.0                              # bisection for x = exp(-lam) in (0,1)
    for _ in range(400):
        x = (a_ * b_) ** 0.5
        if mean(x) < target:
            a_ = x
        else:
            b_ = x
    x = (a_ * b_) ** 0.5
    Z = sum(x ** m for m in MINv)
    return (log(Z) - target * log(x)) / (cell * log(2))


def _sum_dist(vals, nc):
    """Distribution of the sum of nc i.i.d. draws from the multiset `vals`."""
    d = {0: 1}
    for _ in range(nc):
        nd: dict[int, int] = {}
        for s, c in d.items():
            for v in vals:
                nd[s + v] = nd.get(s + v, 0) + c
        d = nd
    return d


def band_count(a: int, b: int, l: int) -> int:
    """Interval relaxation of (*): #{type-vectors : sum min <= l <= sum max}
    = T^{n_c} - (#sum-min>l) - (#sum-max<l).  Shares the exact A_{2,3} exponent
    (the two differ only on gap-only vectors, an exponentially negligible set)."""
    if b == 0:
        nt, MINv, MAXv = 3, _MIN2, _MAX2
        nc = 1 << (a - 1)
    else:
        nt, MINv, MAXv = 19, _MIN23, _MAX23
        nc = (1 << (a - 1)) * (3 ** (b - 1))
    dmin = _sum_dist(MINv, nc)
    dmax = _sum_dist(MAXv, nc)
    over = sum(c for s, c in dmin.items() if s > l)
    under = sum(c for s, c in dmax.items() if s < l)
    return nt ** nc - over - under


# ---------------------------------------------------------------------------
# Brute force, certified by two faithful degree-1 primes
# ---------------------------------------------------------------------------
def is_prime(num: int) -> bool:
    if num < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if num % sp == 0:
            return num == sp
    d = num - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(r - 1):
            x = x * x % num
            if x == num - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int):
    f = set()
    d = 2
    m = n
    while d * d <= m:
        while m % d == 0:
            f.add(d)
            m //= d
        d += 1
    if m > 1:
        f.add(m)
    return f


def euler_phi(n: int) -> int:
    r = n
    for q in prime_factors(n):
        r -= r // q
    return r


def prime_1modN_above(N: int, lo: int) -> int:
    t = max(1, (lo - 1 + N - 1) // N)
    while True:
        p = 1 + N * t
        if p >= lo and is_prime(p):
            return p
        t += 1


def primitive_root(p: int, N: int) -> int:
    pf = prime_factors(N)
    cof = (p - 1) // N
    for a in range(2, p):
        g = pow(a, cof, p)
        if g != 1 and all(pow(g, N // q, p) != 1 for q in pf):
            return g
    raise RuntimeError("no root")


def _distinct_e1(N: int, l: int, p: int) -> int:
    g = primitive_root(p, N)
    pw = [pow(g, a, p) for a in range(N)]
    return len({sum(pw[a] for a in B) % p for B in combinations(range(N), l)})


def brute_count(N: int, l: int):
    """Certified #distinct e_1 (two independent faithful primes); None on mismatch."""
    lo = max(10 ** 7, (2 * l + 1) ** euler_phi(N))
    p1 = prime_1modN_above(N, lo)
    c1 = _distinct_e1(N, l, p1)
    p2 = prime_1modN_above(N, p1 + 1)
    c2 = _distinct_e1(N, l, p2)
    return c1 if c1 == c2 else None


# ---------------------------------------------------------------------------
# certificate
# ---------------------------------------------------------------------------
# (a, b): brute-checked across all l' up to where binom(N, l') is feasible.
CROSS = ((1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2))
BRUTE_BUDGET = 30_000_000


def build_certificate():
    cross = []
    ok = True
    for a, b in CROSS:
        N = (2 ** a) * (3 ** b)
        lmax = N // 2
        s = struct_count(a, b, lmax)
        rows = []
        for l in range(1, lmax + 1):
            if comb(N, l) > BRUTE_BUDGET:
                break
            bt = brute_count(N, l)
            match = bt is not None and bt == s[l]
            ok = ok and match
            rows.append({"l": l, "struct": s[l], "brute": bt, "match": match})
        cross.append({"N": N, "a": a, "b": b, "rows": rows})

    # b=0 specialization recovers thm:exactcount
    b0 = []
    for a in (2, 3, 4, 5):
        N = 2 ** a
        s = struct_count(a, 0, N // 2)
        rows = []
        for l in range(1, N // 2 + 1):
            f = exactcount_2power(a, l)
            match = s[l] == f
            ok = ok and match
            rows.append({"l": l, "struct": s[l], "thm_exactcount": f, "match": match})
        b0.append({"N": N, "a": a, "rows": rows})

    # entropy exponent beta_{2,3}(rho) = lim log2 A_{2,3}(N', rho N') / N'
    plateau = log2(19) / 6
    band_lo, band_hi = 6 / 19, 13 / 19          # uniform feasible <=> rho in [6/19,13/19]
    # plateau is exact on the whole band (and 2-power value reproduces Paper B)
    plateau_exact = (
        abs(saddle_beta(band_lo) - plateau) < 1e-12
        and abs(saddle_beta(0.5) - plateau) < 1e-12
        and abs(saddle_beta(band_hi) - plateau) < 1e-12
        and abs(saddle_beta(0.5, _MIN2, _MAX2, 2) - log2(3) / 2) < 1e-12
    )
    # prize rates: {2,3} exponent, the 2-power baseline, and the (lowering) gap
    prize = []
    lowers = True
    for name, num, den in (("1/2", 1, 2), ("1/4", 1, 4), ("1/8", 1, 8), ("1/16", 1, 16)):
        rho = num / den
        b23 = saddle_beta(rho)
        b2 = saddle_beta(rho, _MIN2, _MAX2, 2)
        lowers = lowers and b2 >= b23 - 1e-12
        prize.append({"rho": name, "beta_2_3": b23, "beta_2pow": b2, "drop": b2 - b23})
    # convergence: exact band-count exponent climbs monotonically toward the saddle
    conv = []
    conv_ok = True
    for name, num, den in (("1/16", 1, 16), ("1/8", 1, 8), ("1/4", 1, 4)):
        rho = num / den
        s = saddle_beta(rho)
        ladder = []
        for a in range(5, 9):                   # N' = 96,192,384,768 (fast, exact)
            N = (2 ** a) * 3
            l = round(rho * N)
            ladder.append({"Np": N, "beta_band": log2(band_count(a, 1, l)) / N})
        mono = all(ladder[i]["beta_band"] < ladder[i + 1]["beta_band"]
                   for i in range(len(ladder) - 1))
        below = all(r["beta_band"] < s for r in ladder)
        gap = s - ladder[-1]["beta_band"]
        conv_ok = conv_ok and mono and below and gap < 0.01
        conv.append({"rho": name, "saddle": s, "ladder": ladder,
                     "monotone_up": mono, "below_saddle": below, "gap_at_N768": gap})
    # exact Minkowski count and its interval relaxation share the exponent
    ratio_192 = None
    for a in (5, 6):
        N = (2 ** a) * 3
        l = round(N / 8)
        ratio_192 = struct_count(a, 1, l)[l] / band_count(a, 1, l)
    same_exponent = ratio_192 is not None and ratio_192 > 0.9999
    exponent_ok = plateau_exact and lowers and conv_ok and same_exponent
    ok = ok and exponent_ok

    cert = {
        "result": "{2,3}-smooth exact canonical slope count A_{2,3}(2^a 3^b, l')",
        "status": "CONDITIONAL (proof depends on import thm:vsimport, as thm:23rigidity) "
                  "/ AUDIT (finite values certified unconditionally vs brute force)",
        "status_label": "CONDITIONAL",
        "paper_dependency": "slackMCA_v4 thm:exactcount (b=0), rem:23count (open target), "
                            "thm:23rigidity, thm:vsimport (import)",
        "note": "experimental/notes/m1/paperb_23_smooth_exact_count.md",
        "closed_form": "A_{2,3}=#{cell-type vectors with l' in Minkowski sum of per-cell "
                       "Sizes}; n_c=2^{a-1}3^{max(b-1,0)} cells; per-cell alphabet 19 types "
                       "(b>=1) in size-classes 6x{3},6x{2,4},6x{1..5},1x{0,2,3,4,6}, or 3 "
                       "types (b=0) recovering thm:exactcount.",
        "cross_check_struct_vs_brute": cross,
        "b0_recovers_thm_exactcount": b0,
        "entropy_exponent": {
            "formula": "beta_{2,3}(rho) = (1/(6 ln2)) max{H(p): sum p*min <= 6rho <= "
                       "sum p*max}; plateau log2(19)/6 on rho in [6/19,13/19], tilted "
                       "(Gibbs) optimiser p_i~exp(-lam*min_i) off the plateau; "
                       "beta(rho)=beta(1-rho).",
            "plateau_beta": plateau,
            "plateau_rho_band": [band_lo, band_hi],
            "plateau_exact_and_2pow_baseline": plateau_exact,
            "prize_rates": prize,
            "lowered_by_radix3_at_all_prize_rates": lowers,
            "convergence_band_count_to_saddle": conv,
            "struct_vs_band_ratio_N192": ratio_192,
            "struct_band_share_exponent": same_exponent,
            "passed": exponent_ok,
        },
        "passed": ok,
    }
    return cert


def render(cert) -> str:
    L = [
        "{2,3}-smooth exact canonical slope count  A_{2,3}(2^a 3^b, l')",
        f"  status: {cert['status']}",
        f"  closed form: {cert['closed_form']}",
        "  cross-check structural transfer vs certified brute force:",
    ]
    for blk in cert["cross_check_struct_vs_brute"]:
        nrows = len(blk["rows"])
        allm = all(r["match"] for r in blk["rows"])
        L.append(f"    N={blk['N']:>3} (2^{blk['a']} 3^{blk['b']}): {nrows} sizes l'  "
                 f"-> {'ALL MATCH' if allm else 'MISMATCH'}")
    L.append("  b=0 specialization recovers Paper B thm:exactcount:")
    for blk in cert["b0_recovers_thm_exactcount"]:
        allm = all(r["match"] for r in blk["rows"])
        L.append(f"    N={blk['N']:>3}: {'ALL MATCH' if allm else 'MISMATCH'}")
    ee = cert["entropy_exponent"]
    L.append(f"  entropy exponent  beta_2,3(rho)=lim log2 A/N'  (plateau "
             f"{ee['plateau_beta']:.6f}=log2(19)/6 on rho in [6/19,13/19]):")
    for r in ee["prize_rates"]:
        L.append(f"    rho={r['rho']:>4}: beta_2,3={r['beta_2_3']:.6f}   "
                 f"2-power baseline={r['beta_2pow']:.6f}   (radix-3 drop {r['drop']:.4f})")
    for c in ee["convergence_band_count_to_saddle"]:
        L.append(f"    rho={c['rho']:>4}: band-count exponent -> saddle "
                 f"{c['saddle']:.6f}  (monotone={c['monotone_up']}, "
                 f"gap@N'=768 {c['gap_at_N768']:.4f})")
    L.append(f"    exact/band exponent agree (ratio@N'=192 "
             f"{ee['struct_vs_band_ratio_N192']:.6f}); exponent block "
             f"{'PASS' if ee['passed'] else 'FAIL'}")
    L.append(f"RESULT: {'PASS' if cert['passed'] else 'FAIL'}")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify the {2,3}-smooth exact slope count.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--certificate", action="store_true")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--check", type=Path)
    args = ap.parse_args()
    cert = build_certificate()
    if args.check is not None:
        stored = json.loads(args.check.read_text())
        fresh = json.loads(json.dumps(cert))
        match = stored == fresh
        print(f"certificate matches {args.check}: {match}")
        return 0 if (match and cert["passed"]) else 1
    if args.output is not None:
        args.output.write_text(json.dumps(cert, indent=2, sort_keys=True))
    if args.certificate or args.json:
        print(json.dumps(cert, indent=None if args.json else 2, sort_keys=True))
    else:
        print(render(cert))
    return 0 if cert["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
