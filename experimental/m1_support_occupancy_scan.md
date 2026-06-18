# M1 Support-Occupancy Scanner

**Status:** AUDIT / EXPERIMENTAL.

This note accompanies `experimental/m1_support_occupancy_scan.py`. It combines
two proved experimental notes:

- `experimental/m1_support_coefficient_test.md`: a support `S` contributes a
  bad slope exactly when `Pi_S(f)` and `Pi_S(g)` are collinear and not both
  zero;
- `experimental/m1_quotient_periodic_overlap_profile.md`: exact supports
  decompose into quotient-fiber occupancy classes with closed support counts
  and exchange ledgers.

For a small prime field and multiplicative subgroup domain, the scanner
enumerates exact supports of size `k+t`, computes the top-coefficient vectors
`Pi_S(f)` and `Pi_S(g)`, records the contributed slope when it exists, and
labels the support by its quotient-fiber occupancy histogram.

Example:

```bash
python3 experimental/m1_support_occupancy_scan.py \
  --prime 17 --n 8 --k 4 --slack 2 --quotient-order 4
```

By default the line is the canonical monomial line

```text
f = X^(k+t),        g = X^k.
```

The output checks four consistency conditions:

```text
histogram_counts_match_binomial
histogram_counts_match_formula
support_outcome_partition
low_deficit_whole_fiber_invisibility
```

The first says the scanned histogram counts exhaust `binom(n,k+t)`. The second
says each histogram count matches the closed quotient-occupancy formula. The
third says every exact support is classified as contained, no-slope, or
incidence-producing, both globally and inside each retained histogram.
The fourth verifies the quotient-core factorization from
`experimental/m1_support_coefficient_test.md`: after deleting all whole
quotient fibers from a support `S`, the elementary symmetric coefficients
`e_d(S)` with `d<m` agree with those of the residual partial-fiber set.

For the default canonical line, the scanner additionally reports

```text
canonical_symmetric_formula_check
canonical_zero_prefix_support_count
canonical_residual_zero_prefix_match
canonical_low_residual_exclusion_check
canonical_boundary_residual_coset_check
canonical_boundary_residual_count_check
canonical_boundary_slope_count_check
canonical_boundary_slope_multiplicity_check
canonical_boundary_touched_fiber_check
canonical_small_residual_regime
canonical_small_residual_support_count_check
canonical_small_residual_slope_count_check
canonical_small_residual_slope_multiplicity_check
canonical_subboundary_residual_floor_check
canonical_residual_slope_check
canonical_boundary_slope_decomposition_check
```

These check that the interpolated `Pi_S` slope agrees with the canonical
formula `z=(-1)^t e_t(S)`, count supports with
`e_1(S)=...=e_(t-1)(S)=0`, and, when `t<=m`, verify that this zero-prefix
condition is equivalent to the same condition on the residual partial-fiber
set. They also verify the low-residual exclusion

```text
0 < |R(S)| < t        =>        no canonical zero-prefix support,
```

and the boundary classification: when `|R(S)|=t` and the zero-prefix holds,
all residual points have the same `t`-th power. The JSON field
`residual_size_histogram` records the scanned residual sizes.
For cyclic multiplicative domains, the scanner also compares the observed
boundary count with the exact formula

```text
1_{t | n} * (n/t) * binom(N - t/gcd(t,m), L),
```

where `s=k+t=Lm+t` and `N=n/m`; otherwise the expected count is zero. Actual
boundary residual cosets are also checked to touch exactly `t/gcd(t,m)`
quotient fibers.

The corresponding slope image is checked too. When the boundary family is
present, the expected slope set has size `n/t`, and every boundary slope has
support multiplicity

```text
binom(N - t/gcd(t,m), L).
```

The JSON field `canonical_boundary_slope_histogram` records the observed
boundary-only slope multiplicities.

The `canonical_small_residual_*` fields package the closed large-fiber
small-residual ledger for support residues `b=(k+t) mod m` with `b<=t`:

```text
b=0       whole_fiber_zero_slope
0<b<t     subboundary_absent
b=t       boundary_power_cosets, or boundary_absent if t does not divide n
```

In these regimes the scanner checks the exact small-residual support count,
slope count, and uniform slope multiplicity. Residues `b>t` are reported as
`superboundary_unclassified`, because they are the first genuinely partial
small-residual regime not decided by the quotient-core theorem.

For dithered residues in the range

```text
0 < (k+t mod m) < t < m,
```

the scanner reports `canonical_subboundary_residual_floor=m+(k+t mod m)` and
checks that every canonical zero-prefix support has residual size at least
this floor. This is the executable form of the small-residual exclusion caused
by a nonzero support residue below the slack.

The slope checks audit the exact canonical quotient-core decomposition. For
`t<m`, the contributed slope is computed from the residual set alone:

```text
z = (-1)^t e_t(R(S)).
```

For `t=m`, the scanner verifies the boundary formula

```text
z = (-1)^m e_m(R(S)) - sum_{B_i subset S} y_i,
```

where `B_i={x:x^m=y_i}`.

This scanner does not prove the M1 local limit. It makes the quotient-content
label visible on actual support-collinearity incidences, so tiny examples can
separate whole-fiber, one-remainder, mixed-partial, and candidate aperiodic
support patterns. The canonical symmetric checks make the monomial
quotient-locator case more transparent: once whole fibers are stripped away,
the residual partial-fiber set is the object that must satisfy the zero-prefix
conditions, and residual packets below the slack are ruled out over a
multiplicative domain. At the boundary `t=m`, any remaining whole-fiber
dependence is reduced to the quotient-level sum over the selected whole
fibers. For `t<m`, the remaining boundary residuals form a counted family of
power-kernel cosets rather than an unstructured partial-fiber family, and
their slope image is the explicit set `-D^t`.
If the support residue lies strictly between `0` and `t`, then even those
boundary residuals disappear and any canonical residual incidence must use
more than one full fiber's worth of residual points.
