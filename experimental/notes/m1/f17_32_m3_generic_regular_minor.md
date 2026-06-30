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
  f17_32_n512_k256_m3_generic_prefix_regular_minor_certificate.json
```

## Claim

For every exact agreement `385 <= A <= 426`, put

```text
j = 512 - A,        t = A - 256.
```

Then the prefix regular minor

```text
Delta_A(Z) = det((H_{t,j}(u) + Z H_{t,j}(v))_{0..j,0..j})
```

is not the zero polynomial for a generic syndrome pencil `(u,v)`, and has exact
degree `j+1`.

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

The prefix Hankel matrix of `v` is

```text
H(v)_{r,c} = v_{r+c}
           = sum_i x_i^r x_i^c
           = (V^T V)_{r,c},
```

where `V_{i,c}=x_i^c` is the square Vandermonde matrix.  Therefore

```text
det H(v) = det(V)^2 = prod_{i<h}(x_h-x_i)^2 != 0.
```

For this specialization,

```text
Delta_A(Z) = det(Z H(v)) = Z^{j+1} det H(v),
```

so the coefficient of `Z^{j+1}` is nonzero under a specialization.  Hence the
generic leading coefficient is not the zero polynomial, and the generic degree
is exactly `j+1`.

The verifier checks this specialization in the pinned `F_17^32` model by
computing the Vandermonde products for the descriptor-domain prefixes of sizes
`87` through `128`.  All leading coefficients are nonzero.

This is a syndrome-pencil statement.  It identifies a nonsingular point in the
ambient syndrome space; it is not a claim that a particular hard line from the
MCA problem has this specialization.

## Consequence

Regular-prefix failure in the M3 window is not forced by Hankel geometry.  It
is a special determinant-zero condition on the actual syndrome pencil.  Thus
future M3 packets should treat a vanished prefix minor as a genuine singular
stratum to be handled by alternate row sets or pivot charts, not as evidence
that the whole regular chart is unavailable.

Non-claims: this note does not prove any particular syndrome pencil is
nonsingular, does not enumerate roots over `F_17^32`, and does not clear the
finite-slope `2^-128` budget.  The degree-bound sum is still `4515`, while the
budget numerator is `6`.
