# F17^32 M3 Rank-10 A411 Projective-Line Packet

This directory contains a v9 projective-line regular-minor packet for the
synthetic rank-10 low-rank M3 row at `A=411`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank_rank10_11_projective_line_packets.py \
  --write

python3 experimental/scripts/verify_f17_32_m3_low_rank_rank10_11_projective_line_packets.py \
  --check

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-rank10-a411-projective-line/f17_32_n512_k256_a411_rank10_projective_line_packet.json
```

The source rank-9..11 sweep stores this row compactly by hashes.  The packet
generator recomputes the degree-10 regular minor, checks its coefficient and
Frobenius-gcd hashes against the sweep, splits the degree-3 Frobenius gcd, and
records the three finite roots.  Degree-only projective accounting would give
`10+1=11`, above the M3 budget numerator `6`; the exact projective-line
numerator is `4`: three finite regular-minor roots plus the `[0:1]` endpoint.

Non-claims: this is a synthetic syndrome-pencil packet only, regular-minor roots
are an upper-bound root table rather than proved actual bad slopes, quotient
image is not audited here, and this is not an actual-row M3 threshold bound.
