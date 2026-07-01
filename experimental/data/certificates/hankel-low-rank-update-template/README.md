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
rank-deficient singular residual row.  When the base Hankel block is
nonsingular it also verifies the compressed determinant-lemma form
`Delta(Z)=det(H_X) det(I+Z V_Y^T H_X^{-1} V_Y)`, reducing the large minor to
the update-rank kernel.  For rank-2 update rows it also records the exact
quadratic discriminant gate, including split, repeated-root, and nonsquare
no-root cases over `F_17`.

The v2 certificate also records the `F_17^32` M3 budget envelope.  Since
`floor(17^32/2^128)=floor((17^32+1)/2^128)=6`, every nonzero regular
low-rank update chart of rank `s <= 6` has at most `s` finite regular roots and
at most `s` projective regular roots.  A zero determinant is not counted by this
envelope; it remains a singular bucket for the pivot/residual atlas.

This is a reusable algebraic template for future v9 packets, not an actual
`F_17^32` safe-side row bound.
