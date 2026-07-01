# F17^32 M3 One-Spike A=426 Packet

This directory contains a deterministic v9 packet for the non-proportional
one-spike Hankel template at the M3 endpoint `A=426`.

The extractor input is

```text
experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json
```

It uses

```text
u_m = sum_{x in X} x^m,  |X|=87,
v_m = y^m,
```

where `X` is the first 87 nodes of the pinned `F_17^32` row descriptor and `y`
is the next descriptor node.  The prefix regular minor has degree 1 in the
slope, with Cauchy-Binet/Vandermonde-square coefficients replayed by the
checker.

Run:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --one-spike-linear \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  --expect-fail \
  experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/invalid_one_spike_linear_coefficient_packet.json
```

The invalid fixture changes one linear coefficient and must fail replay.

Non-claims: this is a synthetic syndrome-pencil stress packet, not a universal
M3 row root table, quotient/tangent subtraction ledger, or safe-side MCA bound.
