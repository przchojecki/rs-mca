# F17^32 M3 Syndrome-Realizability Certificate

Status: PROVED / AUDIT for the listed synthetic syndrome inputs.

This directory contains a deterministic certificate showing that the synthetic
M3 rank-witness syndrome pencils are realized by received-line values on the
pinned subgroup row.

For the order-512 subgroup `H`, the verifier uses the weighted syndrome map

```text
s_m = (1/512) sum_{x in H} x*y(x)*x^m
```

and the inverse subgroup section

```text
y_s(x) = sum_{m=0}^{255} s_m x^(-m-1).
```

The verifier audits the pinned subgroup as the powers of an exact order-512
generator and checks character orthogonality for exponents `-(255)..255`.
It then applies the section formula to the `u` and `v` components of the
A=385, A=426, A=421..426, and A=426 contiguous-gcd synthetic inputs.

The reusable section theorem is recorded separately at

```text
experimental/data/certificates/subgroup-syndrome-section/
  subgroup_syndrome_section_certificate.json
```

This packet checks that the listed synthetic inputs use the same row descriptor
and consumes that general theorem as a dependency.

This is not a worst-case M3 theorem.  It only removes the possible ambiguity
that the synthetic rank-witness packets are free syndrome vectors rather than
actual received-line data on the pinned row.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_syndrome_realizability.py \
  --write experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/f17_32_n512_k256_rank_witness_syndrome_realizability.json

python3 experimental/scripts/verify_m1_subgroup_syndrome_section.py \
  --check experimental/data/certificates/subgroup-syndrome-section/subgroup_syndrome_section_certificate.json

python3 experimental/scripts/verify_f17_32_m3_syndrome_realizability.py \
  --check experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/f17_32_n512_k256_rank_witness_syndrome_realizability.json
```
