# F17^32 M3 Rank-8 A393 Projective-Line Packet

This directory contains a v9 projective-line regular-minor packet for the
synthetic rank-8 low-rank M3 row at `A=393`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank_rank8_a393_projective_line_packet.py \
  --write

python3 experimental/scripts/verify_f17_32_m3_low_rank_rank8_a393_projective_line_packet.py \
  --check

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-rank8-a393-projective-line/f17_32_n512_k256_a393_rank8_projective_line_packet.json
```

The packet uses the prefix regular minor at `j=119`, `t=137`.  Degree-only
projective accounting would give `8+1=9`, above the M3 budget numerator `6`.
The Frobenius gcd for this row has four linear factors; the generator splits
that degree-4 gcd deterministically and records the four finite roots.  The
projective-line packet also checks the original top degree `j+1=120`; that top
coefficient is zero, so `[0:1]` contributes one endpoint.

Thus this hard synthetic row has projective-line numerator `5`: four finite
regular-minor roots plus one projective-infinity endpoint, still below the M3
budget numerator `6`.

Non-claims: this is a synthetic syndrome-pencil packet only, regular-minor roots
are an upper-bound root table rather than proved actual bad slopes, quotient
image is not audited here, and this is not an actual-row M3 threshold bound.
