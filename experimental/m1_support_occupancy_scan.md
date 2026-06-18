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
canonical_small_residual_active_size
canonical_superboundary_active_depth
canonical_superboundary_active_depth_remainder_check
canonical_small_residual_depth_gate_check
canonical_positive_dither_clearance_applies
canonical_positive_dither_inferred_r
canonical_positive_dither_exact_dimension
canonical_positive_dither_prefix_max_fiber_size
canonical_positive_dither_dyadic_prefix_scale_count
canonical_positive_dither_finite_prefix_check
canonical_positive_dither_residual_floor
canonical_positive_dither_clearance_check
canonical_small_residual_support_count_check
canonical_small_residual_slope_count_check
canonical_small_residual_slope_multiplicity_check
canonical_residual_packet_lift_count_check
canonical_residual_packet_slope_consistency_check
canonical_terminal_pure_zero_chain_check
canonical_terminal_pure_zero_packet_count_check
canonical_terminal_pure_zero_support_count_check
canonical_first_nonzero_frontier_check
canonical_first_nonzero_frontier_partition_check
canonical_first_nonzero_frontier_original_slope_check
canonical_first_superboundary_zero_slope_packet_count_check
canonical_first_superboundary_zero_slope_support_count_check
canonical_first_superboundary_zero_slope_coset_check
canonical_first_superboundary_lift_gate_active
canonical_first_superboundary_lift_gate_remainder
canonical_first_superboundary_lift_gate_whole_fibers
canonical_first_superboundary_lift_gate_check
canonical_first_superboundary_shape_orbit_factor
canonical_first_superboundary_shape_orbit_quotient_check
canonical_first_superboundary_shape_active_nonzero_orbit_check
canonical_first_superboundary_shape_packet_count_check
canonical_first_superboundary_shape_support_slope_histogram_check
canonical_first_superboundary_shape_active_nonzero_power_coset_count
canonical_first_superboundary_shape_power_coset_slope_count
canonical_first_superboundary_shape_power_coset_slope_count_check
canonical_first_superboundary_shape_power_coset_slope_bound
canonical_first_superboundary_shape_power_coset_slope_bound_check
canonical_second_superboundary_lift_gate_active
canonical_second_superboundary_lift_gate_remainder
canonical_second_superboundary_lift_gate_whole_fibers
canonical_second_superboundary_lift_gate_check
canonical_second_superboundary_shape_packet_count_check
canonical_second_superboundary_shape_support_slope_histogram_check
canonical_second_superboundary_shape_zero_next_slack_parameter_count
canonical_second_superboundary_next_slack_parameter_check
canonical_second_superboundary_next_slack_active_parameter_check
canonical_second_superboundary_next_slack_packet_count_check
canonical_second_superboundary_next_slack_support_count_check
canonical_second_superboundary_shape_active_nonzero_orbit_check
canonical_second_superboundary_shape_nonzero_power_coset_count
canonical_second_superboundary_shape_active_nonzero_power_coset_count
canonical_second_superboundary_shape_power_image_size
canonical_second_superboundary_shape_power_coset_slope_count
canonical_second_superboundary_shape_power_coset_slope_count_check
canonical_second_superboundary_shape_power_coset_slope_bound_check
canonical_slack_two_shape_packet_count_check
canonical_slack_two_shape_support_slope_histogram_check
canonical_slack_two_shape_nonzero_square_coset_count
canonical_slack_two_shape_active_nonzero_square_coset_count
canonical_slack_two_shape_total_nonzero_square_coset_count
canonical_slack_two_shape_nonzero_square_coset_coverage_density
canonical_slack_two_shape_active_nonzero_square_coset_coverage_density
canonical_slack_two_shape_saturates_nonzero_square_cosets
canonical_slack_two_shape_active_saturates_nonzero_square_cosets
canonical_slack_two_shape_square_image_size
canonical_slack_two_shape_abstract_square_coset_slope_count
canonical_slack_two_shape_square_coset_slope_count
canonical_slack_two_shape_square_coset_slope_count_check
canonical_slack_two_shape_square_coset_slope_bound_check
canonical_slack_two_second_superboundary_lift_gate_active
canonical_slack_two_second_superboundary_lift_gate_remainder
canonical_slack_two_second_superboundary_lift_gate_whole_fibers
canonical_slack_two_second_superboundary_lift_gate_check
canonical_slack_two_second_superboundary_packet_count
canonical_slack_two_second_superboundary_support_count
canonical_slack_two_second_superboundary_slope_count
canonical_slack_two_second_shape_packet_count_check
canonical_slack_two_second_shape_support_slope_histogram_check
canonical_slack_two_second_shape_zero_conic_parameter_count
canonical_slack_two_second_shape_nonzero_square_coset_count
canonical_slack_two_second_shape_active_nonzero_square_coset_count
canonical_slack_two_second_shape_square_image_size
canonical_slack_two_second_shape_square_coset_slope_count
canonical_slack_two_second_shape_square_coset_slope_count_check
canonical_slack_two_second_shape_square_coset_slope_bound_check
canonical_slack_two_second_shape_high_index_slope_bound
canonical_slack_two_second_shape_high_index_nontrivial
canonical_slack_two_second_shape_high_index_bound_check
canonical_slack_two_second_full_domain_saturates_nonzero_slopes
canonical_slack_two_second_full_domain_nonzero_slope_image
canonical_slack_two_second_full_domain_coset_count_check
canonical_slack_two_full_domain_alpha_square_count
canonical_slack_two_full_domain_alpha_nonsquare_count
canonical_slack_two_full_domain_alpha_zero_count
canonical_slack_two_full_domain_alpha_character_sum
canonical_slack_two_full_domain_slope_image
canonical_slack_two_full_domain_slope_count
canonical_slack_two_full_domain_slope_count_check
canonical_slack_two_cyclotomic_character_order
canonical_slack_two_cyclotomic_shape_count_bound
canonical_slack_two_cyclotomic_shape_count_bound_check
canonical_slack_two_cyclotomic_slope_bound
canonical_slack_two_cyclotomic_slope_bound_density
canonical_slack_two_cyclotomic_slope_bound_check
canonical_slack_two_cyclotomic_slope_bound_nontrivial
canonical_slack_three_shape_packet_count_check
canonical_slack_three_shape_support_slope_histogram_check
canonical_slack_three_shape_beta_count
canonical_slack_three_shape_beta_parameter_count_check
canonical_slack_three_split_cubic_beta_count
canonical_slack_three_split_cubic_parameter_count_check
canonical_slack_three_split_cubic_root_count_histogram
canonical_slack_three_split_cubic_nonzero_cube_coset_count
canonical_slack_three_split_cubic_cube_coset_beta_counts_check
canonical_slack_three_shape_active_nonzero_cube_coset_count
canonical_slack_three_shape_nonzero_cube_coset_beta_counts
canonical_slack_three_shape_active_nonzero_cube_coset_beta_counts
canonical_slack_three_shape_cube_coset_slope_count
canonical_slack_three_shape_cube_coset_slope_count_check
canonical_slack_three_full_domain_ordered_shape_count
canonical_slack_three_full_domain_ordered_shape_count_check
canonical_slack_three_full_domain_beta_count
canonical_slack_three_full_domain_beta_count_check
canonical_slack_three_full_domain_zero_beta_count
canonical_slack_three_full_domain_nonzero_beta_count
canonical_slack_three_full_domain_cube_surjective
canonical_slack_three_full_domain_cube_coset_beta_lower_bound
canonical_slack_three_full_domain_cube_coset_saturation_certificate
canonical_slack_three_full_domain_exact_cube_coset_beta_counts
canonical_slack_three_full_domain_exact_cube_coset_saturates
canonical_slack_three_full_domain_slope_image
canonical_slack_three_full_domain_slope_count
canonical_slack_three_full_domain_slope_count_check
canonical_slack_three_cyclotomic_character_order
canonical_slack_three_cyclotomic_conic_weil_constant
canonical_slack_three_cyclotomic_shape_count_bound
canonical_slack_three_cyclotomic_shape_count_bound_check
canonical_slack_three_cyclotomic_slope_bound
canonical_slack_three_cyclotomic_slope_bound_density
canonical_slack_three_cyclotomic_slope_bound_check
canonical_slack_three_cyclotomic_slope_bound_nontrivial
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

More generally, it reports the small-residual depth gate. If a residual packet
has size `t+d<m`, then it can lift only when

```text
m | k-d.
```

Equivalently, with `k=k0-r` and `m | k0`, depth `d` can survive only when
`m | r+d`. The field `canonical_superboundary_active_depth` is the unique
small-superboundary depth allowed by the support residue, when it exists, and
`canonical_small_residual_depth_gate_check` verifies that every scanned
canonical zero-prefix support with residual size below one fiber has exactly
that residue size.

When `0 < (k+t mod m) < t`, the fields
`canonical_positive_dither_clearance_*` record the local positive-dither
certificate. Writing `b=(k+t mod m)` and `r=t-b`, the scanner checks that no
canonical zero-prefix support has residual size below one quotient fiber and
that the residual-size floor is exactly `m+b`.
It also records the inferred exact dimension `k0=k+r`, the finite-prefix
bound `m<=t`, and the number `floor(log2(t))` of possible nontrivial dyadic
fiber sizes in that prefix. The field
`canonical_positive_dither_finite_prefix_check` verifies the local instance
of the hierarchy statement: the scanned scale divides the inferred exact
dimension and is already beyond the prefix.

For every canonical scan with `t<m`, the scanner also aggregates supports by
their residual partial-fiber packet `P`. A packet touching `tau(P)` quotient
fibers and having size `r` has expected lift multiplicity

```text
binom(N-tau(P), (k+t-r)/m),
```

when `k+t-r` is divisible by `m`, and zero otherwise. The fields
`canonical_residual_packet_lift_count_check` and
`canonical_residual_packet_slope_consistency_check` verify that these packet
weights reconstruct both the observed canonical zero-prefix support count and
the weighted slope histogram. The size and touched-fiber histograms of the
residual packet catalog are reported as
`canonical_residual_packet_size_histogram` and
`canonical_residual_packet_touched_fiber_histogram`.
The terminal pure-zero fields additionally check every active residual size
`h=t+d<m` whose inherited zero chain reaches the power-coset endpoint:
the observed packets must be exactly the `h`-power cosets, have slope zero,
touch `h/gcd(h,m)` quotient fibers, and lift with the theorem's binomial
multiplicity.
The first-nonzero frontier fields partition every superboundary residual
packet by the first nonzero coefficient `e_(t+j)`. They check that this
partition exhausts the packet/support weights and that, at the original
slack `t`, only the `j=0` frontier contributes nonzero slopes; later
frontiers are inherited zero-slope packets for the original slack.

The first superboundary layer has residual size `t+1`. In this layer the
scanner checks the zero-slope classification: a zero-slope packet is exactly a
`(t+1)`-power coset. In cyclic domains, when the support residue is `t+1`,
the expected zero-slope packet count is `n/(t+1)` if `t+1|n`, and zero
otherwise. The corresponding lifted support count is

```text
1_{t+1 | n} * (n/(t+1))
  * binom(N - (t+1)/gcd(t+1,m), (k+t-(t+1))/m).
```

The fields `canonical_first_superboundary_zero_slope_*` compare these exact
counts with the scan and verify the power-coset condition. Nonzero first
superboundary slopes are left as the sparse-trinomial residual catalog.

The same layer has an exact-support dither gate. Since the residual size is
`t+1` and the support size is `k+t`, the first-superboundary catalog can lift
only when

```text
m | (k-1).
```

The `canonical_first_superboundary_lift_gate_*` fields report this remainder,
the whole-fiber count `(k-1)/m` when the gate is active, and check that the
directly enumerated first-superboundary packet/support counts are zero when
the gate is closed.

For small scanned slack, the scanner also audits the general
first-superboundary shape-coset theorem. It enumerates

```text
C_t(D) = { (u_1,...,u_t) in D^t :
           1,u_1,...,u_t distinct,
           e_j(1,u_1,...,u_t)=0 for 1<=j<t },
```

uses the `(t+1)!`-to-one map
`(x,u_1,...,u_t) -> x{1,u_1,...,u_t}`, and checks

```text
M_t(z) = (1/(t+1)!) sum_{u in C_t(D)}
         binom(N-tau(u), (k+t-(t+1))/m)
         * #{x in D : x^t a_t(u)=z},
a_t(u)=(-1)^t e_t(1,u_1,...,u_t).
```

The `canonical_first_superboundary_shape_*` fields report the orbit factor,
the quotient check, reconstructed packet/support counts and slope histograms,
and the exact active coset-compressed slope count
`1_{zero active} + #{active nonzero a_t(u)D^t cosets} * |D^t|`.
They also check nonzero active shape divisibility by `(t+1)!` and report the
general field-capped power-coset slope bound

```text
1_{zero active} + (active nonzero shape orbits) * |D^t|.
```

The dedicated slack-two and slack-three ledgers below are lower-dimensional
descriptions of this same theorem.

The scanner also audits the generic second-superboundary shape-coset theorem
for small slack. For residual packets of size `t+2`, it enumerates

```text
C_t^(2)(D) = { (u_1,...,u_(t+1)) in D^(t+1) :
               1,u_1,...,u_(t+1) distinct,
               e_j(1,u_1,...,u_(t+1))=0 for 1<=j<t },
```

and checks

```text
M_t^(2)(z) = (1/(t+2)!) sum_{u in C_t^(2)(D)}
             binom(N-tau(u), (k+t-(t+2))/m)
             * #{x in D : x^t b_t(u)=z},
b_t(u)=(-1)^t e_t(1,u_1,...,u_(t+1)).
```

The `canonical_second_superboundary_*` fields report the lift gate `m | k-2`,
the `(t+2)!` quotient check, reconstructed packet/support histograms, and the
coset-compressed `D^t` slope count. The zero-slope parameter count is the
first-superboundary shape catalog for slack `t+1`, making the scanner check
the depth-two/next-slack transition explicitly.
The `canonical_second_superboundary_next_slack_*_check` fields compare this
zero-slope subcatalog with the first-superboundary ledger at fixed support
size, equivalently after the dimension shift `(t,k) -> (t+1,k-1)`.
The accompanying proof note states the same hierarchy for every residual
depth `d`: zero slope at `(t,k,d)` is the depth-`d-1` catalog at
`(t+1,k-1,d-1)`. The scanner currently audits the first nontrivial case
`d=2`.
Iterating this shift leaves only a finite first-nonzero-coefficient frontier;
the scanner now records the exact frontier partition, while pure zero chains
terminate in the counted power-coset ledger.

For slack `t=2`, the scanner also verifies the complete first-superboundary
shape ledger. It enumerates

```text
C_2(D) = { u in D : v=-1-u in D, 1,u,v distinct },
```

uses the six-to-one map `(x,u) -> x{1,u,-1-u}` onto residual packets, and
checks the lifted slope formula

```text
M(z) = (1/6) sum_{u in C_2(D)}
       binom(N-tau(u), (k+2-3)/m) * #{x in D : x^2 alpha(u)=z},
alpha(u)=-(1+u+u^2).
```

The `canonical_slack_two_shape_*` fields report the shape-parameter count and
check that this formula reconstructs the first-superboundary packet count,
lifted support count, packet slope histogram, and support slope histogram.
They also report `canonical_slack_two_shape_square_coset_slope_bound`, the
field-capped bound obtained from the union of square cosets
`alpha(u)D^2`, and check that the observed first-superboundary slope count is
below it.
The sharper field `canonical_slack_two_shape_square_coset_slope_count`
records the exact coset-compressed count

```text
1_{zero active} + #{active nonzero alpha(u)D^2 cosets} * |D^2|,
```

and checks equality against the observed first-superboundary slope count.
The companion non-active fields report the abstract coset coverage of
`alpha(C_2(D))` in `F_p^*/D^2` before quotient-lift filtering. The boolean
`canonical_slack_two_shape_saturates_nonzero_square_cosets` records whether
the abstract slack-two catalog hits every nonzero `D^2`-coset, while
`canonical_slack_two_shape_active_saturates_nonzero_square_cosets` applies the
same test after the exact-support lift filter.

For slack `t=2`, the scanner also verifies the second-superboundary layer
when the residual packet size four is below one quotient fiber. It enumerates

```text
P=x{1,u,v,-1-u-v}
```

and checks the twenty-four-to-one lifted slope formula

```text
M_2^(2)(z) = (1/24) sum_{u,v}
             binom(N-tau(u,v), (k+2-4)/m)
             * #{x in D : -x^2(u^2+v^2+uv+u+v+1)=z}.
```

The `canonical_slack_two_second_*` fields report the depth-two lift gate
`m | k-2`, reconstructed packet/support counts and slope histograms, and the
exact square-coset compressed slope count. The zero-slope parameter count is
the slack-three conic catalog, so this audit checks the first concrete link
between the slack-two depth-two layer and the slack-three depth-one layer.
The `canonical_slack_two_second_shape_high_index_*` fields record the
unconditional subgroup-size ceiling

```text
|Bad_{t=2,d=2}| <= min(p, 1+|D|^3/gcd(2,|D|)).
```

This bound is intentionally coarse, but it gives a quick non-field-filling
certificate whenever the right side is below `p`.
When `D=F_p^*`, the
`canonical_slack_two_second_full_domain_*` fields also record the full-domain
frontier saturation certificate: for `p>=11`, the values
`-(u^2+v^2+uv+u+v+1)` hit both quadratic classes on admissible shapes, so
the nonzero depth-two slope image is all of `F_p^*`. The analytic proof covers
`p>=23`; `experimental/verify_m1_slack_two_depth_two_full_domain.py` checks
`p=11,13,17,19` and records the tiny failures `p=5,7`.

When `D=F_p^*`, the `canonical_slack_two_full_domain_*` fields also check the
quadratic-character formula for the classes of `alpha(u)=-(1+u+u^2)`. For
`p>=17`, this predicts slope image `F_p` when `p==1 mod 3` and `F_p^*` when
`p==2 mod 3`; the same formula records the small exceptional primes. The
slope-count equality check is only asserted when every full-domain shape has
an active quotient lift at the queried support size.

For prime fields, `canonical_slack_two_cyclotomic_*` reports the coarser
character-sum bound obtained from the index `e=(p-1)/|D|`:

```text
|C_2(D)| <= ceil((p-2 + (e^2-1)sqrt(p))/e^2).
```

The scanner uses an integer ceiling for `sqrt(p)`, checks the shape count
against this bound, and reports the induced field-capped slope bound
`min(p, 1+ceil(|C_2(D)|/6)|D|/gcd(2,|D|))` and its density.
The boolean `canonical_slack_two_cyclotomic_slope_bound_nontrivial` records
whether this induced bound is strictly below the full field size.

For slack `t=3`, the scanner verifies the next first-superboundary shape
ledger. It enumerates the conic shape set

```text
C_3(D) = { (u,v) in D^2 :
           w=-1-u-v in D,
           1,u,v,w distinct,
           u^2+v^2+uv+u+v+1=0 },
```

uses the twenty-four-to-one map `(x,u,v) -> x{1,u,v,w}` onto residual packets,
and checks the lifted slope formula

```text
M_3(z) = (1/24) sum_{(u,v) in C_3(D)}
         binom(N-tau(u,v), (k+3-4)/m)
         * #{x in D : x^3 beta(u,v)=z},
beta(u,v)=-(1+uvw).
```

Equivalently, it checks the one-parameter split-cubic ledger

```text
G_beta(Y)=Y^3+Y^2+Y+beta+1,
```

where each admissible `beta` gives three distinct roots in `D\{1}` and hence
six ordered pairs `(u,v)`.

The `canonical_slack_three_split_cubic_*` fields audit this reduction by
grouping the one-dimensional values

```text
beta(y)=-(y^3+y^2+y+1),        y in D\{1}.
```

A beta value is admissible exactly when it has three distinct roots in
`D\{1}`. The scanner reports the root-count histogram, the resulting beta
count, and the exact nonzero `D^3` coset counts, then checks them against the
two-dimensional conic enumeration. This gives a fast finite-audit path for
coset-coverage questions without full support-incidence enumeration.

The `canonical_slack_three_shape_*` fields report the conic parameter count,
the beta count and sixfold beta check, the 24-fold quotient check,
reconstructed packet/support counts and histograms, and the exact cube-coset
slope count
`1_{zero active} + #{active nonzero beta(u,v)D^3 cosets} * |D^3|`.

When `D=F_p^*`, `canonical_slack_three_full_domain_*` checks the exact
quadratic-character count

```text
|C_3(F_p^*)| = p - 9 - 4 chi(-3) - 6 chi(-2).
```

It also records the exact beta count, the zero-beta criterion
`chi(-1)=1`, and the cube-surjective slope image. In particular, for
`p==2 mod 3` and `p>=23`, the full-domain slack-three first-superboundary
catalog hits every nonzero slope; it hits zero too exactly when
`p==1 mod 4`. The slope-count equality check is asserted only when every
full-domain shape has an active quotient lift at the queried support size.
When `p==1 mod 3`, the fields
`canonical_slack_three_full_domain_cube_coset_*` report the cubic-character
lower bound for each nonzero cube coset. The scanner uses the certificate

```text
ceil((A_nonzero - 12 sqrt(p) - 36)/18),
```

where `A_nonzero` is the ordered full-domain shape count with `beta != 0`.
If this lower bound is positive, every cube coset is hit. The crude estimate
`A_nonzero>=p-25` implies this for every prime `p>=271` with `p==1 mod 3`.
The exact finite-audit fields report the sorted number of beta values in each
hit nonzero cube coset and whether all three cube cosets are hit directly.
This exact audit improves the full-domain `p==1 mod 3` saturation threshold
to `p>=103`; the only unsaturated primes below the analytic threshold are
`7,13,19,31,37,43,61,67,73,79,97`.
Run

```bash
python3 experimental/verify_m1_slack_three_full_domain_audit.py
```

to reproduce this finite range check without enumerating full support
incidences.

For prime fields, `canonical_slack_three_cyclotomic_*` reports the conditional
genus-zero character-sum bound for this ordered conic shape count. If
`e=(p-1)/|D|`, the scanner uses the conservative certificate

```text
|C_3(D)| <= ceil((p+1 + 6(e^3-1)sqrt(p))/e^3),
```

with integer ceiling for `sqrt(p)`. It checks the exact enumerated conic
parameter count against this bound and reports the induced field-capped
cube-coset slope bound
`min(p, 1+ceil(|C_3(D)|/24)|D|/gcd(3,|D|))`.
The constant `6` comes from the eight-point geometric zero/pole support of
`u^a v^b w^c` on the smooth projective conic. The estimate is conditional on
the standard multiplicative character-sum bound on genus-zero curves; the
scanner fields are an audit of the resulting numerical certificate, not a
proof of that imported estimate.

The fields `canonical_slack_three_cube_coset_coverage_*` report the
complementary low-index cube-coset coverage certificate. With
`e=(p-1)/|D|`, `g=gcd(3,|D|)`, and `h=eg=[F_p^*:D^3]`, the scanner uses the
conditional lower bound

```text
ceil((p - 9 - 4 chi_2(-3) - (12 sqrt(p)+12)e^3 h)/(e^3 h))
```

for the number of admissible ordered slack-three shape parameters in each
nonzero `D^3` coset. The constant `12` in the square-root term comes from
the fourteen-point zero/pole support of `u^a v^b w^c beta^d` on the conic;
the second `12` is the worst-case cost of the six degeneracy sections. If
this lower bound is positive, the abstract slack-three first-superboundary
catalog hits every nonzero `D^3` coset. The scanner checks that certificate
against the exact enumerated cube-coset coverage and also reports the exact
minimum ordered parameter count across all nonzero `D^3` cosets.
It also reports the fixed-denominator uniform threshold `P_M`, where
`M=e^3h`, defined by the least bucket start

```text
P_M=(s_M-1)^2+1,
(s_M-1)^2 + 1 - 13 > (12 s_M + 12)M.
```

For every prime `p>=P_M` with the same denominator `M`, the lower-bound
numerator is positive regardless of `chi_2(-3)`. Thus the certificate fires
uniformly for that fixed index/cube-kernel regime; for example `M=16` gives
`P_M=38026`.
For quadratic-residue domains with `p==5 mod 6`, this is the index-two case
`D=(F_p^*)^2` and `D^3=D`. The exact split-cubic finite audit below `38026`
improves the practical saturation threshold to `p>=1049`: the only
unsaturated primes in that finite range are
`5,11,17,23,29,41,47,53,59,71,83,89,101,107,113,131,137,149,167,173,179,
191,197,227,233,239,251,257,269,281,317,347,359,383,401,431,467,491,503,
587,617,647,653,701,1031`.
Run

```bash
python3 experimental/verify_m1_slack_three_qr_index_two_audit.py
```

to reproduce this finite audit.
The broader split-cubic sample verifier remains

```bash
python3 experimental/verify_m1_slack_three_cube_coset_coverage.py
```

for a split-cubic exact audit of one proper-subgroup sample where this
certificate fires, one full-domain sample, and one small noncertified control.

For dithered residues in the range

```text
0 < (k+t mod m) < t < m,
```

the scanner reports `canonical_subboundary_residual_floor=m+(k+t mod m)` and
checks that every canonical zero-prefix support has residual size at least
this floor. This is the executable form of the small-residual exclusion caused
by a nonzero support residue below the slack. In a quotient hierarchy with
`k=k0-r`, `1<=r<t`, and `m | k0`, every scale `m>t` falls in this range with
residue `t-r`. Thus positive dither reduces the canonical small-residual work
to the finite prefix `m<=t`; for dyadic fiber sizes this prefix has at most
`floor(log2(t))` nontrivial scales.

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
In the remaining `b>t` superboundary range, the residual-packet lift check
separates the additive residual zero-prefix catalog from the already solved
quotient-core choice of whole fibers.
Inherited zero chains in that catalog terminate in the same power-coset
ledger at residual size `h=t+d`; the scanner checks this terminal piece
separately so it is not recounted as new aperiodic structure.
The first-nonzero frontier check gives the complementary partition of the
nonterminal packets by the coefficient that first survives the residual-depth
shift.
At residual size `t+1`, the zero-slope slice is also separated as a counted
power-coset source.
For `t=2`, the whole residual size-three catalog is separated further into
the finite unit-equation shape set `C_2(D)`.
