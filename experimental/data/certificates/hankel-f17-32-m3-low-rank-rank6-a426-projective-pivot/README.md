# F17^32 M3 Rank-6 A426 Projective-Infinity Pivot Packet

This directory contains a narrow v9 pivot-atlas packet for the synthetic
low-rank M3 row at `A=426`, update rank `6`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_projective_pivot.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json

python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_projective_pivot.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json
```

The packet exercises the projective-line `pivot_atlas` path: the
`projective_infinity` chart has coverage target `status=nonempty` and
`support_count=1`, witnessing the single endpoint `[0:1]`.  The witness support
is `D \ Y`, where `Y` is the rank-6 update node set.  Simultaneous containment
is ruled out by scaled Vandermonde independence on `X union Y`.

Non-claims: this is a synthetic chart packet only.  It does not enumerate finite
affine roots, does not provide quotient-image subtraction, and is not an
actual-row M3 threshold bound.
