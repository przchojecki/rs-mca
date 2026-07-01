# F17^32 M3 Rank-6 A426 Projective-Line Packet

This directory contains a v9 projective-line regular-minor packet for the
synthetic rank-6 low-rank M3 row at `A=426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_projective_line_packet.py \
  --write

python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_projective_line_packet.py \
  --check

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-line/f17_32_n512_k256_a426_rank6_projective_line_packet.json
```

The packet uses the prefix regular minor at `j=86`, `t=170`.  Its finite
determinant has degree `6` and exactly one finite `F_17^32` root, checked by
the same `gcd(Delta,Z^q-Z)` certificate as the finite-affine companion.  The
projective-line packet also checks the original top degree `j+1=87`; that top
coefficient is zero, so `[0:1]` contributes one regular-minor endpoint.  The
companion pivot packet records an actual support witness for this endpoint.

Thus this single v9 packet records projective-line numerator `2`: one finite
regular-minor root plus one projective-infinity endpoint.

Non-claims: this is a synthetic syndrome-pencil packet only, regular-minor roots
are an upper-bound root table rather than proved actual bad slopes, quotient
image is not audited here, and this is not an actual-row M3 threshold bound.
