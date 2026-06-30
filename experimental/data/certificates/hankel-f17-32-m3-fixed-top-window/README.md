# F17^32 M3 Fixed Top-Window Packet

This directory contains a single-syndrome synthetic Paper D v9 packet for the
top of the regular non-tangent window:

```text
RS[F_17^32,H,256], |H|=512, 421 <= A <= 426.
```

The input uses one fixed syndrome pencil

```text
u_m = 0,
v_m = sum_i x_i^m
```

for the first `92` descriptor-domain elements.  For each agreement
`A=421..426`, the prefix determinant is a nonzero scalar times `Z^(513-A)`, so
the exact synthetic root union is `{0}` and the packet declares numerator `1`.

Run:

```sh
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
```

Non-claims: this is a synthetic one-pencil stress packet, not a worst-case MCA
row bound, not actual M3 row data, and not a quotient/tangent subtraction table.
