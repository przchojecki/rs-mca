# Regular-Minor Extractor Rank-Witness Toy

This directory contains a deterministic toy replay for the extractor's
`rank_witness_bound` mode.  The mode is intended for large rows where a
`rank_at_nodes` full-rank specialization already proves that a selected maximal
minor is nonzero, so the packet can record the degree bound without interpolating
the determinant polynomial.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_witness_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-witness-toy/f17_n10_k4_a8_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-witness-toy/f17_n10_k4_a8_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-witness-toy/invalid_rank_witness_root_hash_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-witness-toy/invalid_singular_rank_witness_packet.json
```

The second negative packet recomputes the correct rank-witness hash for the
claimed row set `[0,1,2]`, but that row set is singular at the claimed pivot
node.  It must therefore fail the replayed finite-field rank check rather than
the metadata hash check.
