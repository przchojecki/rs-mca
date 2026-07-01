# F17^32 M3 Rank-2..11 Endpoint Quotient Support

This directory contains a deterministic quotient-support audit for the actual
projective endpoint supports in the synthetic low-rank M3 ladder.
The JSON certificate is stored in compressed form: the verifier rebuilds all
`420` rank/agreement endpoint rows and `3360` nontrivial quotient-fiber checks.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_endpoint_quotient_support.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-endpoint-quotient-support/f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_support.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_endpoint_quotient_support.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-endpoint-quotient-support/f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_support.json
```

For the endpoint support `D \ Y`, where `Y` is the consecutive low-rank update
block of size `s`, the verifier checks every nontrivial proper quotient fiber
size

```text
c in {2,4,8,16,32,64,128,256}.
```

Quotient fibers in the order-512 cyclic domain are exponent classes modulo
`512/c`.  A support `D \ Y` of size `512-s` can be a quotient-remainder support
for fiber size `c` only if `Y` meets exactly `ceil(s/c)` quotient fibers.  In
all checked rows, the consecutive update block meets strictly more than this
minimum, so the actual projective endpoint support is not a nontrivial proper
quotient-remainder support.

Non-claims: this does not exclude the trivial fiber sizes `c=1` or `c=512`,
does not audit finite affine regular-minor roots, does not audit quotient-image
supports, and is not an actual-row M3 threshold bound.
