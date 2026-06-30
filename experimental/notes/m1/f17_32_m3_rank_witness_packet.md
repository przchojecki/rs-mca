# F17^32 M3 Rank-Witness Packet

Status: PROVED / AUDIT for this synthetic finite replay.

This note records the first concrete `F_17^32` regular-window packet produced
by the regular-minor extractor in the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The row descriptor is

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
  f17_32_n512_k256_hankel_row_descriptor.json
```

and the packet is

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
  f17_32_n512_k256_a426_rank_witness_packet.json
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
before running the rank test.

At slope `1`, the prefix minor is the Hankel moment matrix of those `87`
distinct nonzero elements.  Its determinant is a shifted Vandermonde square, so
it is nonzero in the pinned `F_17^32` model.  The extractor's `rank_at_nodes`
selector therefore tests node `0`, then node `1`, finds the prefix row set
`[0,...,86]`, and emits the rank-witness packet

```text
degree_bound = j+1 = 87,
regular_root_bound_sum = 87.
```

This certifies a nonzero regular maximal minor for one actual degree-32 field
syndrome pencil without interpolating the determinant polynomial.

## Why This Matters

The previous generic theorem proves that regular minors are not structurally
zero in the M3 window.  This packet is different: it runs the real v9 packet
pipeline over the pinned `F_17^32` field model and row descriptor.  It is a
first concrete large-field stress test for the M3 regular-window audit.

The result is still too weak to close the safe side: a degree bound of `87`
already exceeds the finite-slope budget numerator `6`.  To become a threshold
certificate, a future packet needs root enumeration/compression, a sharper
eliminant, or a pivot-chart classification after tangent and quotient ledgers
are subtracted.

## Verification

Run:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json
```

Non-claims: this is a synthetic syndrome pencil, not a worst-case MCA row bound,
not a root table over `F_17^32`, and not a quotient/tangent subtraction table.
