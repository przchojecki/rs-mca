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
```

The generated packets are

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/
  f17_32_n512_k256_a385_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
  f17_32_n512_k256_a426_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/
  f17_32_n512_k256_a421_426_fixed_prefix92_packet.json
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

In all three packets, the selected prefix determinant has the closed form

```text
Delta_A(Z) = c_A Z^(j+1)
```

with `c_A != 0`.  Hence the exact finite root table is `{0}`.  The endpoint
packets each have declared aperiodic numerator `1`, and the top-window packet
has root union `{0}` across all six exact agreements, again with declared
aperiodic numerator `1`.

The subtraction sidecar verifies that every source input has `u_m=0` for all
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
