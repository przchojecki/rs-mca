# M1 Occupancy-Profile Scanner

**Status:** AUDIT / EXPERIMENTAL.

This note accompanies `experimental/m1_occupancy_profile_scan.py`. It is the
executable form of the general quotient-fiber occupancy theorem in
`experimental/m1_quotient_periodic_overlap_profile.md`.

For a quotient partition with `N` fibers of size `M`, a support `S` has
occupancy histogram

```text
h_a(S) = |{ i : |S cap B_i| = a }|,        0 <= a <= M.
```

At a fixed support size `s`, the scanner enumerates every histogram satisfying

```text
sum_a h_a=N,        sum_a a h_a=s,
```

checks that the histogram support counts sum to `binom(NM,s)`, and evaluates
the exact fixed-support exchange enumerator `H_h(y)` for each class. It reports
the strict M1 range

```text
1 <= j < t
```

as `strict_codegree_mass`, `max_strict_codegree`, and, when a line-field size
is supplied, the weighted random-line correction

```text
R_h(t,q) = sum_{1 <= j < t} [y^j] H_h(y) q^(t-j).
```

The scanner also evaluates the cross-histogram coefficient formula
`H_{h->g}` and reports `union_cross_histogram_ledger`. This is the exact
ordered-pair and max-codegree ledger for the union of all feasible occupancy
classes at the requested support size. In particular, the full support layer
can now be audited by histogram transitions rather than by support-pair
enumeration. The field `strict_johnson_recovery` checks that this union ledger
recovers the ordinary Johnson support-layer profile in the strict range.

Example:

```bash
python3 experimental/m1_occupancy_profile_scan.py \
  --quotient-order 4 --fiber-size 3 --support-size 4 --slack 3 \
  --line-field-size 17
```

JSON output is available with `--format json`. The fields
`histogram_supports_match_binomial` and `top_histograms` are the main audit
outputs.

This scanner does not prove the M1 local limit. It gives an exact structured
ledger for quotient-fiber content classes and their cross-content transitions;
the remaining hard problem is to prove that the line data cannot concentrate
bad slopes on the resulting structured ledgers beyond the corrected reserve.
