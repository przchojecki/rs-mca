# F17^32 M3 Rank-6 A426 Finite-Affine Packet

This directory contains a v9 finite-affine regular-minor packet for the
synthetic rank-6 low-rank M3 row at `A=426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_finite_packet.py \
  --write

python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_finite_packet.py \
  --check

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-finite-affine/f17_32_n512_k256_a426_rank6_finite_affine_packet.json
```

The packet uses the prefix regular minor at `j=86`, `t=170`.  Its determinant
has degree `6`, and the exact finite `F_17^32` root table has one root.  The
packet checker replays the low-rank input and verifies the
`gcd(Delta,Z^q-Z)` root-count certificate, so the listed finite root is not
just a sampled root.

This is the finite-affine companion to the rank-6, `A=426`
projective-infinity packet.  Together they turn one synthetic rank-6 row into a
v9 finite/projective chart pair.

Non-claims: this is a synthetic syndrome-pencil packet only, regular-minor roots
are an upper-bound root table rather than proved actual bad slopes, quotient
image is not audited here, and this is not an actual-row M3 threshold bound.
