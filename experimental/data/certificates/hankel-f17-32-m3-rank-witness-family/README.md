# F17^32 M3 Rank-Witness Family Certificate

This directory contains a compact finite-field certificate for the whole M3
regular non-tangent window

```text
385 <= A <= 426
```

of `RS[F_17^32,H,256]`.

For each agreement, the certificate uses the synthetic moment syndrome

```text
u_m = 0,
v_m = sum_i x_i^m
```

with the first `j+1` descriptor-domain elements.  At slope `1`, the prefix
regular Hankel minor is a Vandermonde square, so it is nonzero.  The certificate
records the resulting degree bound for all 42 agreements and links the endpoint
v9 packets at `A=385` and `A=426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank_witness_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/f17_32_n512_k256_m3_rank_witness_family_certificate.json
```

Non-claims: this is a synthetic witness-family certificate, not a worst-case MCA
bound, not a root table over `F_17^32`, and not a quotient/tangent subtraction
table.
