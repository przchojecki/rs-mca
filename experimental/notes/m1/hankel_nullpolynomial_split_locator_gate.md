# M3 Null-Polynomial Split-Locator Gate

Status: PROVED / AUDIT.

This note separates three objects that are easy to conflate in the M3 regular
window:

1. the ambient regular root table;
2. the domain split-locator condition;
3. the support-wise noncontainment condition.

For exact agreement `A`, set

```text
j = 512 - A,
t = A - 256.
```

For a finite slope `z`, write `s_m(z)=u_m+zv_m`.  The rectangular Hankel pencil
has a rank drop

```text
rank H_{t,j}(s(z)) <= j
```

if and only if there is a nonzero polynomial

```text
L(X)=ell_0 + ... + ell_j X^j
```

such that

```text
sum_{b=0}^j s_{a+b}(z) ell_b = 0
```

for every `0 <= a < t`.  In a nonsingular regular bucket, these finite slopes
are exactly the v10 canonical regular roots.

The split-locator gate is stricter.  The ambient null-polynomial is a genuine
exact-`A` complement locator only when it has degree exactly `j`, is monic, and
divides the subgroup polynomial

```text
X^512 - 1.
```

The descriptor subgroup has order `512`; its generator powers are all the
roots of this polynomial.  Since the characteristic is `17` and
`512 = 2 mod 17`, the polynomial is squarefree.  Thus monic degree-`j` divisors
of `X^512-1` are exactly the split squarefree locators of `j`-subsets of the
domain.

The support-wise finite-affine noncontainment gate is

```text
H_{t,j}(v) ell != 0.
```

If both `H(u+zv)ell=0` and `H(v)ell=0`, then `H(u)ell=0` too, so the same
support explains both endpoints and the slope belongs to the contained branch.

Consequence: an ambient M3 regular root table is a safe upper bound for actual
split-locator bad slopes, but future packets should record enough data to
apply both filters:

```text
finite slope z;
kernel vector ell;
normalization/degree of L;
divisor proof for L | X^512-1;
H(u+zv)ell;
H(v)ell.
```

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m3_nullpolynomial_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json
```
