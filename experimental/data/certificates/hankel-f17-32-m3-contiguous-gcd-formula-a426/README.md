# F17^32 M3 A=426 Contiguous-GCD Formula

Status: PROVED / AUDIT for the synthetic A=426 zero-`u` pencil.

This directory contains a compact formula certificate for all contiguous
maximal row sets at `A=426`.

For the A=426 rank-witness input, let `X` be the first `87` descriptor-domain
elements.  The syndrome pencil has

```text
u_m = 0,
v_m = sum_{x in X} x^m.
```

For the contiguous row set `R_s={s,...,s+86}`, the leading determinant is

```text
det(v_{s+a+b})_{0<=a,b<87}
  = (prod_{x in X} x)^s * Vandermonde(X)^2.
```

All nodes in `X` are distinct and nonzero, so every one of the `84` contiguous
row-set determinants is nonzero.  Hence every audited determinant polynomial is
`c_s Z^87`, and the monic common gcd over the all-contiguous subatlas is
`Z^87` with exact root table `{0}`.

This extends the bounded four-window packet:

```text
experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/
```

from a replayed prefix of four contiguous windows to a formula certificate for
all `84` contiguous windows.  It is still not the all-maximal-minor canonical
gcd over every row set.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_a426_contiguous_gcd_formula.py \
  --write experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-a426/f17_32_n512_k256_a426_contiguous_gcd_formula.json

python3 experimental/scripts/verify_f17_32_m3_a426_contiguous_gcd_formula.py \
  --check experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-a426/f17_32_n512_k256_a426_contiguous_gcd_formula.json
```
