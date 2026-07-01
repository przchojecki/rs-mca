# F17^32 M3 A=426 One-Spike Packet

Status: PROVED / AUDIT for this synthetic finite replay.

This directory contains a replayable `aperiodic-hankel-eliminant-v1` packet for
one non-proportional synthetic syndrome pencil at the upper endpoint `A=426`
of the M3 regular non-tangent window of
`RS[F_17^32,H,256]`, `|H|=512`.

At `A=426`, the regular parameters are

```text
j = 86,
t = 170,
j+1 = 87.
```

The input uses the first `87` elements of the pinned `F_17^32` row descriptor
as base nodes and the next descriptor-domain element as a one-spike direction:

```text
u_m = sum_{x in X} x^m,
v_m = y^m.
```

It is genuinely non-proportional.  If `u=c v`, then the signed measure with
weight `1` on each point of `X` and weight `-c` at `y` would have its first
`88` moments equal to zero.  Since the `88` support points are distinct, the
Vandermonde matrix is invertible, contradicting the nonzero weights.

For the prefix row set `[0,...,86]`, the extractor replays the Cauchy-Binet
rank-one update formula.  The determinant is affine in the finite slope:

```text
Delta_426(Z) = c0 + c1 Z,
c1 != 0.
```

The packet records the exact split-linear root table, with one encoded
`F_17^32` root, and declares numerator `1`.

This is the first non-proportional selected-root packet in this PR.  It is not
a worst-case row bound, not a complete M3 root table, and not a
quotient/extension subtraction table.

Regenerate and check:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --one-spike-linear \
  --write experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --one-spike-linear \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json
```
