# F17^32 M3 Rank-Witness Packets

Status: PROVED / AUDIT for these synthetic finite replays.

This note records the first concrete selected-agreement packets for the M3
regular non-tangent window in the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

It is aligned with the M3 milestone in `towards-prize.md`: compute actual root
tables, or identify singular buckets, for selected agreements in
`385 <= A <= 426`.

The row descriptor is

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
  f17_32_n512_k256_hankel_row_descriptor.json
```

The generated inputs are

```text
experimental/data/hankel-regular-minor-inputs/
  f17_32_n512_k256_a385_rank_witness_input.json
  f17_32_n512_k256_a426_rank_witness_input.json
  f17_32_n512_k256_a421_426_fixed_prefix92_input.json
  f17_32_n512_k256_a426_contiguous_gcd4_input.json
```

The generated packets are

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/
  f17_32_n512_k256_a385_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
  f17_32_n512_k256_a426_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/
  f17_32_n512_k256_a421_426_fixed_prefix92_packet.json

experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/
  f17_32_n512_k256_a426_contiguous_gcd4_packet.json

experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-a426/
  f17_32_n512_k256_a426_contiguous_gcd_formula.json

experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-window/
  f17_32_n512_k256_m3_contiguous_gcd_formula_window.json

experimental/data/certificates/hankel-f17-32-m3-canonical-gcd-formula-window/
  f17_32_n512_k256_m3_canonical_gcd_formula_window.json

experimental/data/certificates/hankel-f17-32-m3-support-uniform-canonical-gcd/
  f17_32_n512_k256_m3_support_uniform_canonical_gcd.json

experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/
  f17_32_n512_k256_m3_weight_uniform_canonical_gcd.json

experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/
  f17_32_n512_k256_m3_lower_rank_contained.json

experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/
  f17_32_n512_k256_m3_zero_u_rank_dichotomy.json

experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/
  hankel_proportional_pencil_tangent_lemma_certificate.json

experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/
  f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json

experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/
  f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json

experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/
  f17_32_n512_k256_m3_projective_infinity_rank_criterion.json

experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/
  f17_32_n512_k256_m3_zero_v_projective_endpoint.json

experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/
  f17_32_n512_k256_m3_direction_rank_degree_cap.json

experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/
  f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json

experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/
  f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json
```

The M4 zero-slope subtraction sidecar is

```text
experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/
  f17_32_n512_k256_rank_witness_zero_slope_subtraction.json
```

The subgroup syndrome-realizability sidecar is

```text
experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/
  f17_32_n512_k256_rank_witness_syndrome_realizability.json
```

## Construction

For exact agreement `A`,

```text
j = 512 - A,
t = A - 256.
```

The input generator

```text
experimental/scripts/emit_f17_32_m3_rank_witness_input.py
```

uses a prefix of descriptor-domain elements `x_i` and sets

```text
u_m = 0,
v_m = sum_i x_i^m,       0 <= m < 256.
```

The generated input stores these `F_17^32` elements as base-`17`
low-to-high encoded integers.  The extractor decodes that compact format and
checks the declared prefix row set.

For the two endpoint packets, the selected agreements are

```text
A=385: j=127, t=129, minor size 128;
A=426: j=86,  t=170, minor size 87.
```

For the fixed top-window packet, one synthetic syndrome pencil from the first
`92` descriptor-domain elements is checked for every exact agreement

```text
421 <= A <= 426.
```

The A=426 contiguous-gcd packet uses the same zero-`u` synthetic pencil as the
endpoint packet but checks the first four contiguous maximal row sets and emits
their monic common gcd.  This is a bounded subatlas step toward the v10
canonical common-gcd branch.

The contiguous-gcd formula certificate extends this from four checked windows
to all `84` contiguous maximal row sets at `A=426`.  If
`R_s={s,...,s+86}`, then

```text
det(v_{s+a+b})_{0<=a,b<87}
  = (prod_{x in X} x)^s * Vandermonde(X)^2,
```

where `X` is the first `87` descriptor-domain elements.  Since the nodes in
`X` are distinct and nonzero, every contiguous determinant is nonzero and the
monic common gcd over the all-contiguous subatlas is `Z^87`.

The all-window formula certificate applies the same argument for every
agreement in the M3 regular window `385 <= A <= 426`, with
`X_A` the first `j+1` descriptor-domain elements.  For each contiguous row set
`R_s={s,...,s+j}`,

```text
det(v_{s+a+b})_{0<=a,b<=j}
  = (prod_{x in X_A} x)^s * Vandermonde(X_A)^2.
```

The first `128` descriptor-domain elements are distinct and nonzero, so all
nested prefixes used in this window have nonzero support product and
Vandermonde square.  This covers all `1806` contiguous row windows in
`385 <= A <= 426`; at agreement `A`, the monic contiguous-subatlas common gcd
is `Z^(j+1)` with root table `{0}`.

The canonical-gcd formula certificate removes the contiguous-row-set
restriction for this same synthetic family.  For any maximal row set
`R={r_0<...<r_j} subset {0,...,t-1}`,

```text
Delta_{A,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i} * det(x_i^b)_{i,0<=b<=j}.
```

Every nonzero maximal minor is therefore a scalar multiple of `Z^(j+1)`.
The prefix row set `R={0,...,j}` is nonzero by the ordinary Vandermonde
determinant, so the v10 canonical gcd over all nonzero maximal row-set minors
is exactly `Z^(j+1)` at each agreement.  This covers
`155193154203428426778689566118132250614039201839551` formal row-set charts
across the M3 window without enumerating them.

The support-uniform canonical certificate removes the nested-prefix support
restriction from that formula.  For any distinct support subset
`S={x_0,...,x_j}` of the descriptor domain and any maximal row set
`R={r_0<...<r_j}`,

```text
(v_{r_a+b})_{a,b} = (x_i^{r_a})_{a,i} * (x_i^b)_{i,b},
Delta_{A,S,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i} * det(x_i^b)_{i,0<=b<=j}.
```

The prefix row set is nonzero for every distinct `S` by Vandermonde, so the
v10 canonical gcd over all nonzero maximal row-set minors is `Z^(j+1)` for
every support subset of size `j+1`.  This is still a zero-`u` rank-size
power-sum family, not arbitrary M3 row data.

The weight-uniform canonical certificate removes the unit-weight restriction.
For any distinct support subset `S={x_0,...,x_j}`, any nonzero weights
`w_i in F_17^32`, and any maximal row set `R={r_0<...<r_j}`,

```text
(v_{r_a+b})_{a,b}
  = (x_i^{r_a})_{a,i} * diag(w_i) * (x_i^b)_{i,b},
Delta_{A,S,w,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i}
      * (prod_i w_i) * det(x_i^b)_{i,0<=b<=j}.
```

The prefix row set is nonzero because the two Vandermonde determinants and
the weight product are nonzero.  Thus the same canonical gcd `Z^(j+1)` holds
uniformly over every nonzero residue weighting on every support subset of size
`j+1`.

The lower-rank companion treats the singular boundary `0 <= r <= j` for the
same zero-`u` weighted power-sum family.  There `rank H(v) <= r < j+1`, so
every maximal regular minor vanishes.  This singular bucket is contained, not
aperiodic: if a degree-`<256` codeword explains an agreement-at-least-`A`
support `W`, then it has at least

```text
|W \ S| >= A-r >= A-j = 2A-512 >= 258 > 256
```

zeros outside the rank support `S`, hence is the zero codeword.  The witness
support is therefore contained in `D\S`, where both line generators are zero
codeword restrictions, so the support-wise noncontained aperiodic contribution
is `0`.

The zero-`u` rank dichotomy certificate abstracts the preceding formulas.  For
an arbitrary zero-`u` syndrome vector `v`, every maximal regular minor has the
form

```text
Delta_R(Z) = det(Z H_R(v)) = Z^(j+1) det(H_R(v)).
```

Thus if `H_{t,j}(v)` has full column rank `j+1`, the v10 canonical gcd over
all nonzero maximal minors is `Z^(j+1)`, and the only root `Z=0` is paid by
the tangent/common-code-line ledger.  If `H_{t,j}(v)` has rank at most `j`,
all maximal regular minors vanish and the bucket is a named singular residual
for M5 pivots unless a separate paid-branch classification applies.  The
lower-rank weighted power-sum certificate is one such paid singular boundary.

The proportional-pencil tangent lemma translates this statement to every
finite common-code-line slope.  If the full stored syndrome vectors satisfy
`u=c v`, then throughout the M3 window

```text
H_{t,j}(u)+Z H_{t,j}(v) = (Z+c) H_{t,j}(v),
Delta_R(Z) = (Z+c)^(j+1) det(H_R(v)).
```

Thus full column rank gives canonical gcd `(Z+c)^(j+1)` and the single finite
root `Z=-c`.  Since `Syn(f+Zg)=u+Zv`, the full stored syndrome is zero at
`Z=-c`, so that root is paid by the tangent/common-code-line ledger and the
residual aperiodic numerator is `0`.  Rank deficiency remains a singular
boundary for M5 pivots unless separately paid.

The finite tangent-overlap criterion gives the converse needed for M4
no-double-counting.  In the M3 window, `t+j=256`, so the regular Hankel chart
uses the full stored syndrome.  A finite slope is tangent/common-code-line iff
`u+zv=0` in all stored coordinates.  Hence a non-proportional pencil has no
finite tangent overlap at all, while a nondegenerate proportional pencil has
the unique paid slope `z=-c`.

The M5 finite-affine kernel chart gives the per-root noncontainment filter.  For
a fixed finite root `z`, put

```text
M_z = H_{t,j}(u) + z H_{t,j}(v).
```

The ambient affine pivot chart `M_z ell=0, H(v)ell!=0` is empty exactly when
`ker M_z subset ker H(v)`, equivalently
`rank stack(M_z,H(v)) = rank M_z`.  If containment fails, the fixed root `z`
contributes at most one finite parameter before the split-locator,
quotient-image, and extension audits.  This packet does not compute finite
root tables; it explains how future root tables should subtract contained
roots.

The projective-infinity rank criterion supplies the corresponding endpoint
rule.  For the homogenized pencil

```text
M_A[Z0:Z1] = Z0 H_{t,j}(u) + Z1 H_{t,j}(v),
```

each maximal minor satisfies `Delta_R(0,1)=det(H_R(v))`.  Thus if the direction
Hankel block `H_{t,j}(v)` has full column rank, the projective-infinity point
`[0:1]` is excluded by a nonzero regular minor and contributes `0`.  If
`rank H_{t,j}(v)<=j`, all infinity minors vanish and the endpoint is a named
singular projective chart for M5 or a separate paid endpoint classification.

The M5 projective-infinity kernel chart refines that singular endpoint.  The
ambient linear infinity chart is

```text
H_{t,j}(v) ell = 0,     H_{t,j}(u) ell != 0.
```

It is empty exactly when `ker H_{t,j}(v) subset ker H_{t,j}(u)`, equivalently
when `rank stack(H(v),H(u)) = rank H(v)`.  If the containment fails, the chart
is recorded as a one-point `dimension_degree` fallback: it can only add the
single projective endpoint `[0:1]`.  This proves empty/projective-one-point
accounting for the ambient chart and does not claim that ambient nonemptiness
implies split-locator nonemptiness.

The zero-`v` projective endpoint certificate handles the codeword-direction
boundary.  If `v=0`, the finite affine pencil is constant:

```text
M_A(Z)=H_{t,j}(u).
```

Full column rank of `H_{t,j}(u)` gives no finite affine roots.  Rank deficiency
leaves a finite singular bucket for M5 or a separate paid classification.  In
both cases, the projective endpoint `[0:1]` has zero direction syndrome and is
paid by the tangent/common-code-line ledger, so its residual projective
aperiodic contribution is `0`.

The direction-rank degree cap is a finite-affine theorem for arbitrary regular
pencils.  If

```text
r = rank H_{t,j}(v),
```

then every maximal row-set determinant
`det(H_R(u)+Z H_R(v))` has degree at most `r`: the coefficient of `Z^d` uses
`d` columns from `H_R(v)`, and these columns are dependent once `d>r`.  Thus
the v10 canonical gcd over all nonzero maximal minors also has degree at most
`r`, giving at most `r` finite roots before paid-ledger subtraction.  Since
the finite-slope budget is `6`, every nonsingular exact bucket with direction
rank at most `6` is finite-root budget safe.  Projective infinity remains
governed by the separate infinity criterion above.

The M4 regular-bucket synthesis certificate composes these local lemmas into a
decision table.  The closed branches are zero-`v` with full-rank `H(u)` and
proportional nonzero-`v` with full-rank `H(v)`; the zero-`u` full-rank branch is
the `c=0` proportional subcase.  A genuinely non-proportional nonsingular
finite bucket with direction rank at most `6` is finite-root budget safe and
has zero finite tangent overlap, but projective infinity is still a singular
endpoint unless separately closed.  Rank-deficient finite buckets,
direction-rank-deficient infinity endpoints, high-rank non-proportional finite
root tables, and quotient/extension overlaps remain named residual work.

In the selected-minor packets, the chosen prefix determinant has the closed form

```text
Delta_A(Z) = c_A Z^(j+1)
```

with `c_A != 0`; in the contiguous-gcd packet each audited nonzero minor has
this form and the common gcd is `Z^87`.  Hence the exact finite root table is
`{0}`.  The endpoint and contiguous-gcd packets each have declared aperiodic
numerator `1`, and the top-window packet has root union `{0}` across all six
exact agreements, again with declared aperiodic numerator `1`.

The subtraction sidecar verifies that every source input, including the
contiguous-gcd input, has `u_m=0` for all
stored syndrome coordinates.  Since `Syn(f+Zg)=u+Zv`, the unique raw root
`Z=0` is a zero-syndrome common-code-line slope and is paid by the tangent
ledger.  For these synthetic packets, the residual aperiodic numerator after
this paid-root subtraction is therefore `0`.

The syndrome-realizability sidecar verifies that these syndrome pencils are
not free formal vectors: on the pinned order-512 subgroup, the inverse section
`y_s(x)=sum_a s_a x^(-a-1)` realizes every stored length-256 syndrome vector
under the weighted syndrome map.  Thus the synthetic packets correspond to
actual received-line values on the pinned row.

## What This Proves

These packets prove, for the pinned `F_17^32` arithmetic model and the listed
synthetic syndrome pencils, that the selected regular prefix minors are not the
zero polynomial and have the exact finite root set `{0}`.

This is stronger than the generic-minor audit in one direction: it is an
actual finite-field replay through the aperiodic packet checker at both
endpoint minor sizes and across a small selected top subrange.  It is still a
stress packet, not a worst-case M3 row bound.

## Nonclaims

These packets do not claim any of the following:

```text
a worst-case support-wise MCA upper bound for the row;
a complete root table for every received line;
a quotient or extension paid-root subtraction table;
a singular-bucket classification;
a closed safe-side proof for the prize threshold.
```

The tangent subtraction is only for these synthetic rank-witness packets.  It
does not classify arbitrary non-proportional M3 syndrome pencils.

## Verification

Run:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 385 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a385_rank_witness_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a385_rank_witness_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/f17_32_n512_k256_a385_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/f17_32_n512_k256_a385_rank_witness_packet.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 421 \
  --agreement-max 426 \
  --witness-prefix-count 92 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a421_426_fixed_prefix92_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a421_426_fixed_prefix92_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/f17_32_n512_k256_a421_426_fixed_prefix92_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/f17_32_n512_k256_a421_426_fixed_prefix92_packet.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --minor-gcd-contiguous-limit 4 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_contiguous_gcd4_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_contiguous_gcd4_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/f17_32_n512_k256_a426_contiguous_gcd4_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/f17_32_n512_k256_a426_contiguous_gcd4_packet.json

python3 experimental/scripts/verify_f17_32_m3_a426_contiguous_gcd_formula.py \
  --check experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-a426/f17_32_n512_k256_a426_contiguous_gcd_formula.json

python3 experimental/scripts/verify_f17_32_m3_all_contiguous_gcd_formula.py \
  --check experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-window/f17_32_n512_k256_m3_contiguous_gcd_formula_window.json

python3 experimental/scripts/verify_f17_32_m3_canonical_gcd_formula.py \
  --check experimental/data/certificates/hankel-f17-32-m3-canonical-gcd-formula-window/f17_32_n512_k256_m3_canonical_gcd_formula_window.json

python3 experimental/scripts/verify_f17_32_m3_support_uniform_canonical_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-support-uniform-canonical-gcd/f17_32_n512_k256_m3_support_uniform_canonical_gcd.json

python3 experimental/scripts/verify_f17_32_m3_weight_uniform_canonical_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/f17_32_n512_k256_m3_weight_uniform_canonical_gcd.json

python3 experimental/scripts/verify_f17_32_m3_lower_rank_contained.py \
  --check experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/f17_32_n512_k256_m3_lower_rank_contained.json

python3 experimental/scripts/verify_f17_32_m3_zero_u_rank_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/f17_32_n512_k256_m3_zero_u_rank_dichotomy.json

python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --check experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json

python3 experimental/scripts/verify_m1_hankel_finite_tangent_overlap_criterion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json

python3 experimental/scripts/verify_m1_hankel_m5_finite_affine_kernel_chart.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json

python3 experimental/scripts/verify_m1_hankel_projective_infinity_rank_criterion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/f17_32_n512_k256_m3_projective_infinity_rank_criterion.json

python3 experimental/scripts/verify_m1_hankel_zero_v_projective_endpoint.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/f17_32_n512_k256_m3_zero_v_projective_endpoint.json

python3 experimental/scripts/verify_m1_hankel_direction_rank_degree_cap.py \
  --check experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/f17_32_n512_k256_m3_direction_rank_degree_cap.json

python3 experimental/scripts/verify_m1_hankel_m5_projective_infinity_kernel_chart.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json

python3 experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json

python3 experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/f17_32_n512_k256_rank_witness_zero_slope_subtraction.json

python3 experimental/scripts/verify_f17_32_m3_syndrome_realizability.py \
  --check experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/f17_32_n512_k256_rank_witness_syndrome_realizability.json
```

## Next Steps

The natural next M3 steps are:

```text
extend the selected-agreement replay beyond this synthetic prefix family;
replace synthetic pencils with adversarial or universally quantified row-level pencils;
combine non-synthetic root tables with tangent, quotient, and extension subtraction;
build pivot charts for any singular buckets produced by the regular extractor.
```
