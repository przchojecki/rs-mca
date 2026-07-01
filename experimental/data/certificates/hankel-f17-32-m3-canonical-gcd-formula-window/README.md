# F17^32 M3 Canonical GCD Formula

Status: PROVED / AUDIT for the synthetic zero-`u` nested-prefix family.

This directory contains the formula certificate for the v10 canonical
regular-minor gcd over every maximal row set in the M3 regular window

```text
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A`, `t=A-256`, and let `X_A` be the
first `j+1` descriptor-domain elements.  The synthetic syndrome pencil is

```text
u_m = 0,
v_m = sum_{x in X_A} x^m.
```

For any maximal row set `R={r_0<...<r_j} subset {0,...,t-1}`,

```text
Delta_{A,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i} * det(x_i^b)_{i,0<=b<=j}.
```

Thus every nonzero maximal minor is a scalar multiple of `Z^(j+1)`.  The
prefix row set `R={0,...,j}` is nonzero because both determinant factors are
ordinary Vandermonde determinants on distinct nodes.  Therefore the monic v10
canonical gcd over all nonzero maximal minors at agreement `A` is exactly

```text
Z^(j+1),
```

with root table `{0}`.  Across the whole M3 window this covers
`155193154203428426778689566118132250614039201839551` formal maximal-row-set
charts without enumerating them.

This removes the contiguous-subatlas restriction for this synthetic family.  It
still does not classify arbitrary M3 row data.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_canonical_gcd_formula.py \
  --write experimental/data/certificates/hankel-f17-32-m3-canonical-gcd-formula-window/f17_32_n512_k256_m3_canonical_gcd_formula_window.json

python3 experimental/scripts/verify_f17_32_m3_canonical_gcd_formula.py \
  --check experimental/data/certificates/hankel-f17-32-m3-canonical-gcd-formula-window/f17_32_n512_k256_m3_canonical_gcd_formula_window.json
```
