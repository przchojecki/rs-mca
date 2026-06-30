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
  f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json
```

## Claim

For every exact agreement `385 <= A <= 426`, put

```text
j = 512 - A,        t = A - 256.
```

Let

```text
R = {r_0 < r_1 < ... < r_j} subset {0,...,t-1}
```

be any row set of size `j+1`.  Then the maximal regular minor

```text
Delta_{A,R}(Z) =
  det((H_{t,j}(u) + Z H_{t,j}(v))_{R,0..j})
```

is not the zero polynomial for a generic syndrome pencil `(u,v)`, and has exact
degree `j+1`.  The contiguous minor

```text
Delta_{A,s}(Z) =
  det((H_{t,j}(u) + Z H_{t,j}(v))_{s..s+j,0..j})
```

is the special case `R={s,...,s+j}`.

## Proof

Write the leading coefficient of `Delta_{A,R}(Z)` as

```text
L_R(y) = det(y_{r_a+c})_{0<=a,c<=j},
```

where the `y_m` are independent syndrome variables.  In the determinant
expansion, the identity permutation contributes the monomial

```text
M_id = prod_{a=0}^j y_{r_a+a}
```

with coefficient `+1`.  This monomial is unique: the smallest index appearing
in `M_id` is `r_0`, and in any determinant term it can only arise from row
`0` and column `0`.  Removing that forced row and column and repeating proves
by induction that any term with the same multiset of variables must be the
identity term.  Therefore `M_id` cannot cancel, and `L_R` is not the zero
polynomial over any field, including characteristic `17`.

Since the coefficient of `Z^{j+1}` in `Delta_{A,R}(Z)` is nonzero, the generic
degree is exactly `j+1`.

## Contiguous Audit

The certificate also keeps an explicit finite-field audit for the contiguous
subatlas.  Choose any `j+1` distinct elements

```text
x_0,...,x_j in H.
```

The descriptor supplies 512 distinct elements of `H`, so the first `j+1`
descriptor-domain elements are available throughout the M3 window.  Specialize

```text
u = 0,
v_m = sum_{i=0}^j x_i^m.
```

For the contiguous row set `s..s+j`, the specialized Hankel matrix has
determinant

```text
det H(v)_{s..s+j,0..j}
  = (prod_i x_i^s) det(B)^2
  = (prod_i x_i^s) prod_{i<h}(x_h-x_i)^2 != 0.
```

The verifier checks this specialization in the pinned `F_17^32` model by
computing the Vandermonde products for the descriptor-domain prefixes of sizes
`87` through `128`, and then applying the shifted formula above to all
contiguous starts.  Across the whole M3 window this certifies `1806`
contiguous regular charts.  All leading coefficients are nonzero.

This is a syndrome-pencil statement.  It identifies a nonsingular point in the
ambient syndrome space; it is not a claim that a particular hard line from the
MCA problem has this specialization.

## Consequence

No maximal row-set regular failure in the M3 window is forced by Hankel
geometry.  For every `A`, every maximal row-set determinant is a genuine
nonzero equation on the actual syndrome pencil.  Thus a concrete packet that
finds many vanished minors is identifying a special determinant-zero stratum of
that line, not a structural collapse of the regular Hankel method.

Across `385<=A<=426`, the certificate covers

```text
155193154203428426778689566118132250614039201839551
```

formal maximal row-set charts, with `1806` contiguous charts singled out as a
practical first-search subatlas.

Non-claims: this note does not prove any particular syndrome pencil is
nonsingular, does not enumerate roots over `F_17^32`, and does not clear the
finite-slope `2^-128` budget.  The degree-bound sum is still `4515`, while the
budget numerator is `6`.
