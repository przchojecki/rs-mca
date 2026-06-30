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
from math import comb, log2
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
    def beta(rho_num, rho_den):
        vals = []
        for a in range(2, 9):  # b=1 family, N'=2^a*3
            N = (2 ** a) * 3
            l = N * rho_num // rho_den
            A = struct_count(a, 1, l)[l]
            vals.append((N, log2(A) / N))
        return vals

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
        "entropy_exponent_beta_2_3_half_samples": beta(1, 2),
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
    bvals = cert["entropy_exponent_beta_2_3_half_samples"]
    L.append("  entropy exponent beta_{2,3}(1/2) = lim log2 A / N'  (b=1 family):")
    L.append("    " + ", ".join(f"N'={n}:{b:.4f}" for n, b in bvals[-4:]))
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
