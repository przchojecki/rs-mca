# F17^32 M3 Rank-Witness Packet

Status: PROVED / AUDIT for this synthetic finite replay.

This note records the first concrete `F_17^32` regular-window packets produced
by the regular-minor extractor in the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The row descriptor is

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
  f17_32_n512_k256_hankel_row_descriptor.json
```

The endpoint packets are

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/
  f17_32_n512_k256_m3_rank_witness_family_certificate.json

experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/
  f17_32_n512_k256_a385_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
  f17_32_n512_k256_a426_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/
  f17_32_n512_k256_a421_426_fixed_prefix92_packet.json

experimental/data/certificates/hankel-f17-32-m3-proportional-a426/
  f17_32_n512_k256_a426_scalar5_packet.json
```

## Construction

At exact agreement `A=426`,

```text
j = 512 - 426 = 86,
t = 426 - 256 = 170,
j+1 = 87.
```

The input generator

```text
experimental/scripts/emit_f17_32_m3_rank_witness_input.py
```

uses the first `87` descriptor-domain elements `x_i` and sets

```text
u_m = 0,
v_m = sum_i x_i^m,       0 <= m < 256.
```

The generated input stores these `F_17^32` elements as base-`17`
low-to-high encoded integers, and the extractor decodes that compact format
before extracting the prefix minor.

The coefficient of `Z^87` in the prefix minor is the Hankel moment matrix of
those `87` distinct nonzero elements.  Its determinant is a shifted
Vandermonde square, so it is nonzero in the pinned `F_17^32` model.  The
extractor's `zero_u_monomial_roots` mode therefore checks the prefix row set
`[0,...,86]` directly, computes the nonzero leading coefficient of

```text
Delta_426(Z) = c_426 Z^87,
```

and emits the exact synthetic root table `{0}` without interpolating the
determinant polynomial.  This certifies a nonzero regular maximal minor for one
actual degree-32 field syndrome pencil and records the exact roots of that
synthetic pencil.

At the other endpoint, `A=385`,

```text
j = 512 - 385 = 127,
t = 385 - 256 = 129,
j+1 = 128.
```

The same construction with the first `128` descriptor-domain elements gives a
closed-form endpoint packet with

```text
Delta_385(Z) = c_385 Z^128,
root_union = {0}.
```

Thus the concrete replay covers both endpoint minor sizes in the M3 regular
window: `128` at `A=385` and `87` at `A=426`.

The family certificate records the same Vandermonde prefix construction for
every agreement in `385..426` without emitting all 42 full v9 packets.  It
stores one compact record per agreement and hashes the two endpoint v9 packets
as concrete replays of the extractor/checker path.

For the whole synthetic family, the same closed-form root certificate applies.
Since `u=0`, the prefix determinant is

```text
Delta_A(Z) = c_A Z^(j+1),
```

where `c_A` is the nonzero Vandermonde-square leading coefficient recorded in
the certificate.  Thus the exact synthetic root table is `{0}` for every
`A=385..426`; the certificate records root union `{0}` and per-agreement root
count sum `42`.

## Why This Matters

The previous generic theorem proves that regular minors are not structurally
zero in the M3 window.  These packets are different: they run the real v9
packet pipeline over the pinned `F_17^32` field model and row descriptor.  They
are concrete large-field stress tests for the M3 regular-window audit at the
largest and smallest minor sizes.

The endpoint v9 packets now carry exact synthetic root tables, and the family
certificate records the same closed-form root union compactly across all 42
agreements.  This does not close the safe side for the row: a future threshold
packet needs actual M3 row data, tangent/quotient subtraction, and root tables
or pivot-chart classifications for those actual pencils.

There is also one fixed-syndrome top-window packet for `A=421..426`.  It uses a
single `u=0` moment syndrome from the first `92` descriptor-domain elements, and
the extractor verifies that the prefix leading coefficient is nonzero for each
minor size `87..92`.  Thus a single v9 packet has root union `{0}` across six
agreements, which is closer to the eventual M3 packet shape than the separate
endpoint stress tests.

The fixed top-window packet also has an explicit line-value lift:

```text
experimental/data/certificates/hankel-f17-32-m3-line-value-lift/
  f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json
```

For the order-512 subgroup, `lambda_x=x/512`, so the verifier uses the inverse
Fourier section `y(x)=sum_m s_m x^(-m-1)` to produce values
`f,g:H -> F_17^32` whose syndromes are exactly the fixed top-window input.  This
does not make the packet a worst-case row bound, but it closes the gap between
the syndrome-only synthetic pencil and an explicit received line on the pinned
row.

The subgroup-section theorem is recorded separately in
`experimental/notes/m1/subgroup_syndrome_section.md`; the certificate
cross-checks the `F_17^32` section hashes against the line-value lift.

The zero-slope subtraction sidecar is recorded in
`experimental/notes/m1/f17_32_m3_zero_slope_subtraction.md`.  It checks that
the fixed top-window packet's single synthetic root `{0}` is the
zero-codeword tangent/common-code-line slope, leaving no residual synthetic
aperiodic root after that paid branch is removed.

The proportional A=426 packet is a shifted version of the same closed-form
mechanism.  It sets `u=5v`, so

```text
H(u)+Z H(v) = (5+Z) H(v),
Delta_426(Z) = c_426 (Z+5)^87,
```

and the exact finite root union is `{12}`.  The sidecar

```text
experimental/data/certificates/hankel-f17-32-m3-proportional-a426/
  f17_32_n512_k256_a426_scalar5_subtraction.json
```

verifies that this root is the common-code-line slope `Z=-5`, because the
stored syndrome of `f+Zg` vanishes there.  Thus it is removed by the tangent
ledger and leaves no synthetic aperiodic residual.  This is still a synthetic
packet, not actual worst-case M3 row data.

The reusable theorem behind this shifted packet is recorded in
`experimental/notes/m1/m1_hankel_proportional_pencil_tangent_lemma.md`: every
proportional syndrome pencil `u=c v` is a tangent branch in the v9 atlas, even
when a selected regular minor vanishes and the bucket must be viewed through
affine pivots.

The F1 denominator audit is recorded in
`experimental/notes/f1/f17_32_m3_extension_denominator_audit.md`.  It checks
that the line-value lift is genuinely `F_17^32`-valued, so finite affine
slopes in this packet are counted with denominator `17^32`, not `17`.

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
  --syndrome-scalar 5 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_scalar5_rank_witness_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_scalar5_rank_witness_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-proportional-a426/f17_32_n512_k256_a426_scalar5_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-proportional-a426/f17_32_n512_k256_a426_scalar5_packet.json

python3 experimental/scripts/verify_f17_32_m3_proportional_slope_subtraction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-proportional-a426/f17_32_n512_k256_a426_scalar5_subtraction.json

python3 experimental/scripts/verify_f17_32_m3_line_value_lift.py \
  --check experimental/data/certificates/hankel-f17-32-m3-line-value-lift/f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json

python3 experimental/scripts/verify_m1_subgroup_syndrome_section.py \
  --check experimental/data/certificates/subgroup-syndrome-section/subgroup_syndrome_section_certificate.json

python3 experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/f17_32_n512_k256_a421_426_zero_slope_subtraction.json

python3 experimental/scripts/verify_f17_32_m3_extension_denominator_audit.py \
  --check experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/f17_32_n512_k256_a421_426_extension_denominator_audit.json

python3 experimental/scripts/verify_f17_32_m3_rank_witness_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/f17_32_n512_k256_m3_rank_witness_family_certificate.json
```

Non-claims: this is a synthetic syndrome pencil, not a worst-case MCA row bound,
and not a worst-case row root table over `F_17^32`.  The zero-slope sidecar is
only a one-packet tangent-subtraction check, not a full quotient/tangent
subtraction table.
