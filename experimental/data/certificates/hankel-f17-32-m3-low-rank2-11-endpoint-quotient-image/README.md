# F17^32 M3 Low-Rank2-11 Endpoint Quotient-Image Witness

This directory contains a deterministic audit for the projective endpoint
`[0:1]` in the synthetic M3 low-rank ladder at ranks `2..11`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_endpoint_quotient_image.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-endpoint-quotient-image/f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_image.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_endpoint_quotient_image.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-endpoint-quotient-image/f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_image.json
```

The earlier endpoint quotient-support audit proves that the minimal endpoint
support `D \ Y` is not itself a nontrivial quotient-remainder support.  This
certificate proves a complementary quotient-image fact: the same projective
parameter `[0:1]` has another witness support, of size exactly `A`, built from
`c=2` quotient fibers and avoiding the update block `Y`.

The reusable criterion behind the construction is recorded in
`experimental/notes/m1/hankel_endpoint_quotient_image_criterion.md`.  It says
that if a quotient-remainder support `S` avoids `Y` and the Vandermonde columns
on `X union (D\S)` are independent, then the endpoint syndrome is explained on
the quotient co-support while the base syndrome is not.

Result: all `420` projective endpoint rows in ranks `2..11` have an explicit
`c=2` quotient-image witness.

Non-claims: this covers only the synthetic low-rank endpoint rows.  It does not
audit finite affine regular-minor roots and does not claim that the minimal
support `D \ Y` is quotient-remainder.
