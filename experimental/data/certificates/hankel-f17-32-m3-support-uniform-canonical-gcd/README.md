# F17^32 M3 Support-Uniform Canonical GCD

Status: PROVED / AUDIT for zero-`u` power-sum syndromes from every distinct
support subset of size `j+1`.

This directory contains a formula certificate for the v10 canonical
regular-minor gcd over the M3 regular window

```text
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A`, `t=A-256`, and choose any distinct
support subset

```text
S={x_0,...,x_j} subset H.
```

The synthetic syndrome pencil is

```text
u_m = 0,
v_m = sum_{x in S} x^m.
```

For any maximal row set `R={r_0<...<r_j} subset {0,...,t-1}`,

```text
(v_{r_a+b})_{a,b} = (x_i^{r_a})_{a,i} * (x_i^b)_{i,b}
```

and therefore

```text
Delta_{A,S,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i} * det(x_i^b)_{i,0<=b<=j}.
```

Every nonzero maximal minor is a scalar multiple of `Z^(j+1)`.  The prefix row
set `R={0,...,j}` is nonzero because both determinant factors are ordinary
Vandermonde determinants on the distinct support `S`.  Hence the v10 canonical
gcd over all nonzero maximal minors is `Z^(j+1)` for every distinct support
subset `S` of size `j+1`, with root table `{0}`.

This removes the nested-prefix support restriction for this synthetic
rank-size family.  It still does not classify arbitrary length-256 M3 syndrome
pencils or supports of other sizes.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_support_uniform_canonical_gcd.py \
  --write experimental/data/certificates/hankel-f17-32-m3-support-uniform-canonical-gcd/f17_32_n512_k256_m3_support_uniform_canonical_gcd.json

python3 experimental/scripts/verify_f17_32_m3_support_uniform_canonical_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-support-uniform-canonical-gcd/f17_32_n512_k256_m3_support_uniform_canonical_gcd.json
```
