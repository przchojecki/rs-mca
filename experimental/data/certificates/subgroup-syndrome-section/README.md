# Subgroup Syndrome Section

This directory contains a reusable audit certificate for the multiplicative
subgroup syndrome section used by the M3 line-value lift.

For a subgroup `H <= F^*` of order `n`, the Reed-Solomon dual weights are

```text
lambda_x = x / n.
```

Thus every syndrome vector `s_0,...,s_{r-1}` with `r <= n` has the explicit
received-word section

```text
y_s(x) = sum_m s_m x^(-m-1).
```

Run:

```sh
python3 experimental/scripts/verify_m1_subgroup_syndrome_section.py \
  --check experimental/data/certificates/subgroup-syndrome-section/subgroup_syndrome_section_certificate.json
```

Non-claims: this proves a row-data adapter for subgroup rows; it does not prove
an MCA upper bound, quotient/tangent subtraction, or a singular-pivot
classification.
