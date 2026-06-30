# F17^32 M3 Rank-Witness Packet at A=426

This directory contains a concrete Paper D v9 regular-window stress packet for
the pinned row

```text
RS[F_17^32,H,256], |H|=512, A=426.
```

The input is synthetic: `u=0` and `v_m=sum_i x_i^m` for the first `j+1=87`
descriptor-domain elements, stored as base-`17` low-to-high encoded integers.
Because `u=0`, the prefix determinant is a nonzero scalar times `Z^87`.
The extractor checks the prefix row set directly, computes the nonzero
Vandermonde-square leading coefficient, and the packet records the exact
synthetic root table `{0}` without interpolating the determinant polynomial.
It also carries a split-linear root certificate for `Z^87`, so the checker can
replay the compressed factorization over `F_17^32` without enumerating the
whole slope field.

Run:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/f17_32_n512_k256_a426_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/invalid_omitted_monomial_root_packet.json
```

The expected-failure packet lists the large-field monomial `Z` but omits its
root `0`; the checker rejects it without enumerating `F_17^32`.

Non-claims: this is not a worst-case MCA bound, not a worst-case row root table
over `F_17^32`, and not a quotient/tangent subtraction table.
