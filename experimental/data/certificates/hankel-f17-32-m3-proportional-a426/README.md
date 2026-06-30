# F17^32 M3 Proportional Packet at A=426

This directory contains a synthetic Paper D v9 regular-window packet for

```text
RS[F_17^32,H,256], |H|=512, A=426.
```

The input uses the same pinned row descriptor as the other M3 packets, but sets

```text
u = 5 v,
v_m = sum_i x_i^m
```

for the first `87` descriptor-domain elements.  Therefore

```text
H(u) + Z H(v) = (5+Z) H(v),
```

and the prefix determinant is a nonzero scalar times `(Z+5)^87`.  The exact
finite root union is `{12}` in `F_17`, encoded as `12` inside `F_17^32`.
The packet carries the split-linear certificate `(Z+5)^87`, so the checker
reconstructs the compressed factorization and verifies the exact root table
without enumerating the full extension field.

Run:

```sh
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
```

The subtraction certificate verifies that the root `12=-5` is paid by the
tangent/common-code-line ledger: at that slope the stored syndrome vector is
zero.  Non-claims: this is not a worst-case MCA bound, not actual M3 row data,
and not a full quotient/tangent subtraction table.

The reusable theorem form is recorded in:

```text
experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/
```
