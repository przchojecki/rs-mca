# F17^32 M3 Weight-Uniform Canonical GCD

Status: PROVED / AUDIT for zero-`u` weighted power-sum syndromes from every
distinct support subset of size `j+1`, with all weights nonzero.

This directory contains a formula certificate for the v10 canonical
regular-minor gcd over the M3 regular window

```text
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A`, `t=A-256`, choose any distinct
support subset

```text
S={x_0,...,x_j} subset H
```

and any nonzero weights `w_i in F_17^32^*`.  The synthetic syndrome pencil is

```text
u_m = 0,
v_m = sum_i w_i x_i^m.
```

For any maximal row set `R={r_0<...<r_j} subset {0,...,t-1}`,

```text
(v_{r_a+b})_{a,b}
  = (x_i^{r_a})_{a,i} * diag(w_i) * (x_i^b)_{i,b},
```

and therefore

```text
Delta_{A,S,w,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i}
      * (prod_i w_i) * det(x_i^b)_{i,0<=b<=j}.
```

Every nonzero maximal minor is a scalar multiple of `Z^(j+1)`.  The prefix row
set `R={0,...,j}` is nonzero because both determinant factors are ordinary
Vandermonde determinants on `S`, and `prod_i w_i != 0`.  Hence the v10
canonical gcd over all nonzero maximal minors is `Z^(j+1)` for every distinct
support subset and every nonzero weight vector, with root table `{0}`.

This removes the unit-weight restriction from the support-uniform branch.  It
still does not classify arbitrary length-256 M3 syndrome pencils, supports of
other sizes, or weight vectors with zero entries.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_weight_uniform_canonical_gcd.py \
  --write experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/f17_32_n512_k256_m3_weight_uniform_canonical_gcd.json

python3 experimental/scripts/verify_f17_32_m3_weight_uniform_canonical_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/f17_32_n512_k256_m3_weight_uniform_canonical_gcd.json
```
