# Rank-Node Family Regular-Minor GCD Toy Packet

This directory contains a finite `F_17`, `n=16`, `k=8` v9 replay for the
rank-node family common-gcd gate.

The extractor scans deterministic slope nodes, records each distinct row set
witnessed by a full-rank specialization, and takes the common gcd of the
corresponding determinant polynomials.  The packet shows that this deterministic
witness family recovers the same root union `{11}` as the all-contiguous gcd
toy while auditing fewer row sets.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_rank_node_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/f17_n16_k8_a13_rank_node_family_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/f17_n16_k8_a13_rank_node_family_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/invalid_bad_rank_node_witness_packet.json
```

Non-claims: this is a toy-row mechanism packet, not an `F_17^32` M3 root table
and not a threshold-pinning certificate.
