# M3 Low-Rank Affine Spectral Reduction

Status: PROVED / AUDIT.

This note records the structural lemma behind the synthetic low-rank affine
packets in PR #170.  It does not extend the packet to arbitrary M3 row data.
Its role is to replace the opaque statement "two minors are coprime" by an
explicit spectral-disjointness target for two small kernels.

## Setup

Let `F` be a field.  Let

```text
X = (x_0,...,x_{m-1}),    Y = (y_0,...,y_{r-1})
```

with the `x_i` distinct, nonzero, and disjoint from the `y_a`.  Let `L_i(T)`
be the Lagrange basis polynomial for `X`, so `L_i(x_l)=1` if `i=l` and `0`
otherwise.

For `h=0,1`, define the square shifted Hankel moment matrices

```text
H_X^(h)[a,b] = sum_i x_i^(a+b+h),
H_Y^(h)[a,b] = sum_c y_c^(a+b+h),        0 <= a,b < m.
```

The synthetic low-rank pencil is

```text
H_X^(h) + Z H_Y^(h).
```

In the `F_17^32` M3 packet, `m=j+1`, `X` is the first `j+1` descriptor-domain
nodes, and `Y` is the next `rank` descriptor-domain nodes.

## Adjacent-Shift Lemma

Define two `r x r` kernels

```text
K_0[a,b] = sum_i L_i(y_a) L_i(y_b),

K_1[a,b] = y_a * sum_i x_i^(-1) L_i(y_a) L_i(y_b).
```

Then

```text
det(H_X^(0) + Z H_Y^(0))
  = det(V_X)^2 * det(I_r + Z K_0),

det(H_X^(1) + Z H_Y^(1))
  = det(V_X)^2 * (prod_i x_i) * det(I_r + Z K_1),
```

where `V_X[a,i]=x_i^a`.

Proof.  Write

```text
H_X^(0) = V_X V_X^T,
H_Y^(0) = V_Y V_Y^T,
H_X^(1) = V_X D_X V_X^T,
H_Y^(1) = V_Y D_Y V_Y^T,
```

with `D_X=diag(x_i)` and `D_Y=diag(y_a)`.  Since the `x_i` are distinct and
nonzero, both `V_X` and `D_X` are invertible.  The matrix determinant lemma
gives

```text
det(V_X V_X^T + Z V_Y V_Y^T)
  = det(V_X)^2 det(I_r + Z V_Y^T V_X^(-T) V_X^(-1) V_Y),

det(V_X D_X V_X^T + Z V_Y D_Y V_Y^T)
  = det(V_X)^2 det(D_X)
    det(I_r + Z D_Y V_Y^T V_X^(-T) D_X^(-1) V_X^(-1) V_Y).
```

The coordinate vector `V_X^(-1) v(y)` is `(L_i(y))_i`.  Substituting these
coordinates gives the displayed formulas.

## Contiguous-Shift Lemma

More generally, for every integer `h >= 0`, put

```text
H_X^(h)[a,b] = sum_i x_i^(a+b+h),
H_Y^(h)[a,b] = sum_c y_c^(a+b+h),

K_h[a,b] = y_a^h * sum_i x_i^(-h) L_i(y_a)L_i(y_b).
```

Then

```text
det(H_X^(h) + Z H_Y^(h))
  = det(V_X)^2 * (prod_i x_i^h) * det(I_r + Z K_h).
```

Proof.  The same determinant-lemma computation applies with
`D_X^h=diag(x_i^h)` and `D_Y^h=diag(y_a^h)`:

```text
H_X^(h) = V_X D_X^h V_X^T,
H_Y^(h) = V_Y D_Y^h V_Y^T.
```

Since every `x_i` is nonzero, `D_X^h` is invertible.  Therefore

```text
det(V_X D_X^h V_X^T + Z V_Y D_Y^h V_Y^T)
  = det(V_X)^2 det(D_X^h)
    det(I_r + Z D_Y^h V_Y^T V_X^(-T) D_X^(-h) V_X^(-1) V_Y),
```

and substituting the Lagrange coordinates of `V_X^(-1)v(y_a)` gives `K_h`.
The adjacent-shift lemma is the special case `h=0,1`.

## Cauchy-Binet Coefficient Formula

The same shifted determinant also has a replacement-subset expansion.  Let
`S` run through the `m`-element subsets of `X union Y`, and put

```text
c_s = 1 if s in X,
c_s = Z if s in Y.
```

Then

```text
det(H_X^(h) + Z H_Y^(h))
  = sum_{|S|=m} det(V_S)^2 * prod_{s in S} s^h c_s.
```

Equivalently, the coefficient of `Z^d` is

```text
sum_{I subset X, J subset Y, |I|=|J|=d}
  det(V_{(X minus I) union J})^2
  * prod_{s in (X minus I) union J} s^h.
```

Proof.  Write the shifted pencil as one weighted Vandermonde Gram matrix over
`X union Y`:

```text
H_X^(h) + Z H_Y^(h)
  = V_{X union Y} diag(s^h c_s) V_{X union Y}^T.
```

Cauchy-Binet gives the displayed sum over `m` chosen columns.  Grouping terms
by the number `d` of chosen elements from `Y` gives the replacement formula.

After dividing by the nonzero base factor `det(V_X)^2 prod_{x in X} x^h`, the
normalized coefficient is

```text
sum_{I,J, |I|=|J|=d}
  (det(V_{(X minus I) union J}) / det(V_X))^2
  * prod_{y in J} y^h / prod_{x in I} x^h.
```

Thus, for consecutive subgroup nodes, the affine spectral-disjointness problem
can be attacked either through the small kernels `K_h` or through explicit
replacement sums over the interval of exponents.  The PR #170 verifier uses the
kernel form; this formula is the coefficient-level proof target for a future
symbolic or q-binomial argument.

## Consequence For The v10 GCD Ledger

The common finite affine roots of the two displayed maximal minors are exactly
the common roots of

```text
det(I_r + Z K_0),    det(I_r + Z K_1).
```

Equivalently, the relevant nonzero reciprocal spectra of `K_0` and `K_1` are
disjoint.  Therefore the finite affine part of the v10 rank-drop ledger is
empty whenever

```text
gcd(det(I_r + Z K_0), det(I_r + Z K_1)) = 1.
```

This is the formal reason the PR #170 affine packet can certify zero finite
affine roots by checking only the prefix and row-shift-1 maximal minors: the
canonical v10 affine rank-drop gcd divides the gcd of any two nonzero maximal
minors.  The contiguous-shift lemma gives the same small-kernel representation
for every contiguous row-set minor `h..h+m-1`; future pivot packets can use
additional shifts by replacing `K_0,K_1` with the corresponding `K_h` family.

## Current Certified Instance

The verifier

```text
experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py
```

implements this reduction for the accepted `F_17^32`, `n=512`, `k=256` row.
For every `385 <= A <= 426` and every synthetic rank `2..12`, it checks:

```text
deg det(I + Z K_0) = rank,
deg det(I + Z K_1) = rank,
gcd(det(I + Z K_0), det(I + Z K_1)) = 1.
```

Thus the finite affine v10 rank-drop root set is empty for those structured
low-rank branches.

## Next Proof Target

The endpoint side of the same synthetic ladder is now exact for the `c=2`
full-fiber mechanism up to `rank <= 256-floor(A/2)`.  The affine bottleneck is
therefore the following spectral problem:

```text
For the consecutive subgroup nodes X={alpha^0,...,alpha^j}
and Y={alpha^(j+1),...,alpha^(j+r)}, prove that K_0 and K_1 have no common
nonzero reciprocal eigenvalue for the desired rank range.
```

A proof of this statement through the endpoint capacity range would close the
synthetic low-rank regular projective packet after quotient-image endpoint
subtraction.  It would still not be an arbitrary-row M3 theorem; it would be a
clean model result explaining why this low-rank branch has no unpaid regular
projective residual.

A stronger pivot-ready form is:

```text
For the same consecutive subgroup nodes, prove that the reciprocal spectra of
the kernels K_h have empty total intersection over the contiguous shifts needed
by the v10 regular gcd.
```

The current PR only uses `h=0,1`; the all-shift formula identifies the exact
small matrices that have to be compared if a later packet needs more shifts.
