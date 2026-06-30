# F17^32 M3 Rank-Witness Packet at A=426

This directory contains a concrete Paper D v9 regular-window stress packet for
the pinned row

```text
RS[F_17^32,H,256], |H|=512, A=426.
```

The input is synthetic: `u=0` and `v_m=sum_i x_i^m` for the first `j+1=87`
descriptor-domain elements, stored as base-`17` low-to-high encoded integers.
At slope `1`, the prefix Hankel minor is a shifted Vandermonde square, so
`rank_at_nodes` finds a full-rank row set and the extractor emits the
`rank_witness_bound` degree certificate without determinant interpolation.

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

Non-claims: this is not a worst-case MCA bound, not a root table over
`F_17^32`, and not a quotient/tangent subtraction table.
