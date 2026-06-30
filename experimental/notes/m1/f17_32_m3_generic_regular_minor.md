# F17^32 M3 Generic Regular Minor

Status: PROVED / AUDIT.

This note records a small structural result for the M3 regular non-tangent
window of

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The concrete field and domain are the row descriptor in

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
  f17_32_n512_k256_hankel_row_descriptor.json
```

The verifier

```text
experimental/scripts/verify_f17_32_m3_generic_regular_minor.py
```

emits the certificate

```text
experimental/data/certificates/hankel-f17-32-generic-regular-minor/
  f17_32_n512_k256_m3_generic_contiguous_regular_minor_certificate.json
```

## Claim

For every exact agreement `385 <= A <= 426`, put

```text
j = 512 - A,        t = A - 256.
```

Then every contiguous regular minor

```text
Delta_{A,s}(Z) =
  det((H_{t,j}(u) + Z H_{t,j}(v))_{s..s+j,0..j}),
  0 <= s <= t-j-1,
```

is not the zero polynomial for a generic syndrome pencil `(u,v)`, and has exact
degree `j+1`.  The prefix minor

```text
Delta_A(Z) = det((H_{t,j}(u) + Z H_{t,j}(v))_{0..j,0..j})
```

is the case `s=0`.

## Proof

Choose any `j+1` distinct elements

```text
x_0,...,x_j in H.
```

The descriptor supplies 512 distinct elements of `H`, so the first `j+1`
descriptor-domain elements are available throughout the M3 window.  Specialize

```text
u = 0,
v_m = sum_{i=0}^j x_i^m,        0 <= m <= 2j.
```

For the contiguous row set `s..s+j`, the specialized Hankel matrix of `v` is

```text
H(v)_{s+r,c} = v_{s+r+c}
             = sum_i x_i^s x_i^r x_i^c
             = (A_s B^T)_{r,c},
```

where `B_{i,c}=x_i^c` is the square Vandermonde matrix and
`(A_s)_{r,i}=x_i^{s+r}`.  Thus

```text
det H(v)_{s..s+j,0..j}
  = (prod_i x_i^s) det(B)^2
  = (prod_i x_i^s) prod_{i<h}(x_h-x_i)^2 != 0.
```

For this specialization,

```text
Delta_{A,s}(Z) = det(Z H(v)_{s..s+j,0..j})
               = Z^{j+1} det H(v)_{s..s+j,0..j},
```

so the coefficient of `Z^{j+1}` is nonzero under a specialization.  Hence the
generic leading coefficient is not the zero polynomial, and the generic degree
is exactly `j+1` for every contiguous start `s`.

The verifier checks this specialization in the pinned `F_17^32` model by
computing the Vandermonde products for the descriptor-domain prefixes of sizes
`87` through `128`, and then applying the shifted formula above to all
contiguous starts.  Across the whole M3 window this certifies `1806`
contiguous regular charts.  All leading coefficients are nonzero.

This is a syndrome-pencil statement.  It identifies a nonsingular point in the
ambient syndrome space; it is not a claim that a particular hard line from the
MCA problem has this specialization.

## Consequence

Contiguous-row regular failure in the M3 window is not forced by Hankel
geometry.  It is a special determinant-zero condition on the actual syndrome
pencil.  Thus future M3 packets can first try the `1806` contiguous row charts;
if all relevant contiguous minors vanish, that is a genuine singular stratum to
be handled by non-contiguous row sets or pivot charts, not evidence that the
whole regular Hankel method is unavailable.

Non-claims: this note does not prove any particular syndrome pencil is
nonsingular, does not enumerate roots over `F_17^32`, and does not clear the
finite-slope `2^-128` budget.  The degree-bound sum is still `4515`, while the
budget numerator is `6`.
