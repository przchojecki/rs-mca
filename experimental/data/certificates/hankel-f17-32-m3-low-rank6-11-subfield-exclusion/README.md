# F17^32 M3 Rank-6..11 Low-Rank Subfield Exclusion

This directory contains a deterministic proper-subfield/confinement audit for
the synthetic low-rank finite-slack families in the M3 regular window
`385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_subfield_exclusion.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_subfield_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json
```

The proper subfields of `F_17^32` are exactly `F_17^d` for
`d in {1,2,4,8,16}`.  The verifier tests the Frobenius fixedness condition

```text
z^(17^d)=z
```

on listed roots, and intersects count-only root polynomials with
`Z^(17^d)-Z`.  For the rank-9..11 count-only rows, it reconstructs the
compressed regular-minor polynomial and checks the stored coefficient hash
before running the subfield gcds.

The source finite-root certificates count `238` finite roots across ranks
`6..11`.  This audit proves proper-subfield overlap `0`, so none of those
roots is confined to a proper subfield of `F_17^32`.

Non-claims: this is a synthetic-family subfield audit only, not a quotient-image
subtraction table, not a universal M3 row bound, and not a classification of
arbitrary extension-valued or non-proportional pencils.
