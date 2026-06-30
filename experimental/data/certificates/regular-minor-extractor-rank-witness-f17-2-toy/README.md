# Regular-Minor Rank-Witness Extension Toy

This directory contains the `F_17^2` companion to the prime-field
`rank_witness_bound` replay.  It uses the same embedded-base-field pencil as
the `F_17^2` rank-pivot toy, but records only the degree bound certified by a
full-rank specialization.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_rank_witness_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-witness-f17-2-toy/f17_2_n10_k4_a8_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-witness-f17-2-toy/f17_2_n10_k4_a8_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-witness-f17-2-toy/invalid_singular_rank_witness_packet.json
```

The negative packet keeps a correct rank-witness hash for the claimed row set,
but the claimed row set is singular at the pivot node over the polynomial-basis
field.
