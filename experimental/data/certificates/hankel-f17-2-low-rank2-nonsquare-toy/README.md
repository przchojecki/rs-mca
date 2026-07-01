# F17^2 Low-Rank-2 Nonsquare Toy Packet

This directory contains a deterministic v9 packet for a small rank-2 low-rank
Hankel update over `F_17[x]/(x^2-3)`.

The extractor input is

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_low_rank2_nonsquare_toy.json
```

It uses base nodes `{1,2,3}` and update nodes `{4,1+x}`.  The prefix regular
minor has compressed determinant

```text
Delta(Z)=4+(3+x)Z+15x Z^2,
```

whose discriminant is `12+4x`.  The Euler witness
`(12+4x)^144=-1` proves that the discriminant is nonsquare in `F_17^2`, so the
quadratic has no slope roots.  The packet therefore records
`declared_aperiodic_numerator=0` with an inline empty root table.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_low_rank2_nonsquare_toy.json \
  --check experimental/data/certificates/hankel-f17-2-low-rank2-nonsquare-toy/f17_2_n10_k4_a8_low_rank2_nonsquare_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-2-low-rank2-nonsquare-toy/f17_2_n10_k4_a8_low_rank2_nonsquare_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  --expect-fail \
  experimental/data/certificates/hankel-f17-2-low-rank2-nonsquare-toy/invalid_low_rank2_nonsquare_euler_packet.json
```

The invalid fixture changes the recorded Euler witness and must fail the
nonsquare discriminant replay.

Non-claims: this is a toy packet-checker smoke test for the extension-field
nonsquare branch, not an `F_17^32` prize-row root table, quotient/tangent
subtraction ledger, or safe-side MCA bound.
