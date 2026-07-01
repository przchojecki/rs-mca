# F17^32 M3 Rank-2..11 Low-Rank Projective Infinity

This directory contains a deterministic endpoint audit for the synthetic
low-rank families in the M3 regular window `385 <= A <= 426`.
The JSON certificate is stored in compressed form: the verifier rebuilds all
`420` rank/agreement endpoint rows and records their digest plus boundary
samples.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_projective_infinity.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_projective_infinity.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json
```

For the nested low-rank construction

```text
u_m = sum_{x in X} x^m,      v_m = sum_{y in Y} y^m,
```

the projective endpoint `[0:1]` is the word with syndrome `v`.  It is explained
on `D \ Y`, while `u` is not explained on that same support.  The reason is
Vandermonde independence: `u` lies in the parity-column span of `X`, `v` lies in
the parity-column span of `Y`, and `X union Y` has at most `139 <= n-k = 256`
distinct domain points throughout this rank/agreement block.

The support `D \ Y` has size at least `512-11=501`, so it covers every threshold
`A <= 426`.  Thus `[0:1]` is an actual support-wise noncontained projective
parameter for every checked rank/agreement row, not merely a point left
unexcluded by the top-degree regular minor.

Non-claims: this is a synthetic-family endpoint audit only, not finite affine
root enumeration, not a quotient-image subtraction table, not a universal M3 row
bound, and not a classification of arbitrary non-proportional pencils.
