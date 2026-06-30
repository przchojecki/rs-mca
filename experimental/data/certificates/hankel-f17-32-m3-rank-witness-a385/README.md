# F17^32 M3 Rank-Witness Packet at A=385

This directory contains the largest-minor endpoint stress packet for the M3
regular non-tangent window of

```text
RS[F_17^32,H,256], |H|=512.
```

At `A=385`, `j=127`, `t=129`, so the maximal regular minor has size `128`.
The input is synthetic: `u=0` and `v_m=sum_i x_i^m` for the first `128`
descriptor-domain elements, stored as base-`17` low-to-high encoded integers.
Because `u=0`, the prefix determinant is a nonzero scalar times `Z^128`.
The extractor checks the prefix row set directly, computes the nonzero
Vandermonde-square leading coefficient, and the packet records the exact
synthetic root table `{0}` without interpolating the determinant polynomial.
It also carries a split-linear root certificate for `Z^128`, so the checker can
replay the compressed factorization over `F_17^32` without enumerating the
whole slope field.

Run:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 385 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a385_rank_witness_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a385_rank_witness_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/f17_32_n512_k256_a385_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/f17_32_n512_k256_a385_rank_witness_packet.json
```

Non-claims: this is not a worst-case MCA bound, not a worst-case row root table
over `F_17^32`, and not a quotient/tangent subtraction table.
