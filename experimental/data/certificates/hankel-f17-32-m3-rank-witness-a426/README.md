# F17^32 M3 A=426 Rank-Witness Packet

Status: PROVED / AUDIT for this synthetic finite replay.

This directory contains a replayable `aperiodic-hankel-eliminant-v1` packet for
the upper endpoint of the M3 regular non-tangent window of
`RS[F_17^32,H,256]`, `|H|=512`.

At `A=426`, the regular parameters are

```text
j = 86,
t = 170,
j+1 = 87.
```

The input uses the first `87` elements of the pinned `F_17^32` row descriptor
and the synthetic syndrome pencil

```text
u_m = 0,
v_m = sum_i x_i^m.
```

The extractor checks the prefix row set `[0,...,86]` and emits

```text
Delta_426(Z) = c Z^87,
roots = {0},
declared_aperiodic_numerator = 1.
```

This is a concrete checker replay and endpoint root-table packet.  It is not a
worst-case row bound, not a tangent/quotient subtraction table, and not a
complete M3 closure.

The tangent subtraction for the raw root `{0}` is recorded separately in:

```text
experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/
```

Regenerate and check:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --write experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json \
  --write experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json
```
