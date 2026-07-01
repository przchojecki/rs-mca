# Hankel Low-Rank Update Template

This directory contains the deterministic certificate for the M1/M3 low-rank
Hankel update determinant template.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_low_rank_update_template.py \
  --write experimental/data/certificates/hankel-low-rank-update-template/hankel_low_rank_update_template_certificate.json

python3 experimental/scripts/verify_m1_hankel_low_rank_update_template.py \
  --check experimental/data/certificates/hankel-low-rank-update-template/hankel_low_rank_update_template_certificate.json
```

The certificate verifies the Cauchy-Binet coefficient formula against direct
determinants over `F_17` for update ranks `1`, `2`, and `3`, including a
rank-deficient singular residual row.

This is a reusable algebraic template for future v9 packets, not an actual
`F_17^32` safe-side row bound.
