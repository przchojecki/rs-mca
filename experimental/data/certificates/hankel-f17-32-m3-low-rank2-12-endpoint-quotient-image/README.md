# F17^32 M3 Low-Rank2-12 Endpoint Quotient-Image Witness

This certificate is a standalone companion to the low-rank2..12 affine-gcd
packet.  It covers the synthetic M3 low-rank ladder at ranks `2..12` and
agreements `385 <= A <= 426`, using only accepted upstream inputs: the
`F_17^32`, `n=512`, `k=256` Hankel row descriptor and Paper D v12.

For the projective endpoint `[0:1]`, the synthetic update direction is
`v_m = sum_{y in Y} y^m`.  The verifier constructs an agreement-size
quotient-remainder support `S` from `c=2` quotient fibers, plus the parity
remainder when `A` is odd, while avoiding the update block `Y`.  Hence the
co-support `T = D \ S` contains `Y`, so `v` is explained on `T`.

The base direction `u_m = sum_{x in X} x^m` is not explained on the same
co-support: `|X|=j+1`, `|T|=j`, and the verifier records
`|X union T| <= 255 <= n-k`, so Vandermonde independence forbids a nontrivial
containment relation.  Thus `[0:1]` is charged to the quotient-image branch in
all `462` rank/agreement rows.

Generate and check the deterministic certificate with:

```bash
python3 experimental/scripts/verify_f17_32_m3_low_rank2_12_endpoint_quotient_image.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-endpoint-quotient-image/f17_32_n512_k256_m3_low_rank2_12_endpoint_quotient_image.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_12_endpoint_quotient_image.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-endpoint-quotient-image/f17_32_n512_k256_m3_low_rank2_12_endpoint_quotient_image.json
```

Nonclaims: this is only a synthetic low-rank endpoint packet, it does not
audit finite affine regular-minor roots, it does not assert that the minimal
endpoint support `D \ Y` is quotient-remainder, and it is not an arbitrary-row
M3 threshold theorem.
