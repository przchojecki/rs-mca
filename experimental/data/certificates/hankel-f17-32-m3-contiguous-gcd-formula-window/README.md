# F17^32 M3 All-Contiguous GCD Formula

Status: PROVED / AUDIT for the synthetic zero-`u` nested-prefix family.

This directory contains a compact formula certificate for every contiguous
maximal row set in the M3 regular window

```text
385 <= A <= 426.
```

For each agreement, set `j=512-A` and let `X_A` be the first `j+1`
descriptor-domain elements.  The synthetic syndrome pencil is

```text
u_m = 0,
v_m = sum_{x in X_A} x^m.
```

For the contiguous row set `R_s={s,...,s+j}`, the leading determinant factors
as

```text
det(v_{s+a+b})_{0<=a,b<=j}
  = (prod_{x in X_A} x)^s * Vandermonde(X_A)^2.
```

The first `128` descriptor-domain elements are distinct and nonzero.  Hence
every nested prefix `X_A` has nonzero Vandermonde square and nonzero support
product.  Therefore every one of the `1806` contiguous row-window determinants
in `385 <= A <= 426` is nonzero, and the monic common gcd at agreement `A` is

```text
Z^(j+1)
```

with root table `{0}`.

This is still a contiguous-subatlas result for a synthetic family, not the
canonical all-row-set gcd/lcm theorem for arbitrary M3 row data.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_all_contiguous_gcd_formula.py \
  --write experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-window/f17_32_n512_k256_m3_contiguous_gcd_formula_window.json

python3 experimental/scripts/verify_f17_32_m3_all_contiguous_gcd_formula.py \
  --check experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-window/f17_32_n512_k256_m3_contiguous_gcd_formula_window.json
```
