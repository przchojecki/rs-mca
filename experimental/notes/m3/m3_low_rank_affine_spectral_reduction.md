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

## Trace / One-Replacement Coefficient

The first nonconstant coefficient of the normalized shifted determinant is the
trace of the shifted kernel:

```text
[Z] det(I_r+ZK_h)
  = tr(K_h)
  = sum_a y_a^h sum_i x_i^(-h) L_i(y_a)^2.
```

This follows either from the determinant identity
`det(I+ZK_h)=1+Z tr(K_h)+O(Z^2)` or from the `d=1` case of the replacement
formula.

For the normalized consecutive subgroup window

```text
X={1,alpha,...,alpha^(m-1)},
Y={alpha^m,...,alpha^(m+r-1)},
```

this becomes

```text
[Z] det(I_r+ZK_h)
  = sum_{a=0}^{r-1} sum_{i=0}^{m-1}
      L_i(alpha^(m+a))^2 * alpha^(h(m+a-i)).
```

Equivalently,

```text
L_i(alpha^(m+a))
  = prod_{0 <= ell < m, ell != i}
      (alpha^(m+a-ell)-1)/(alpha^(i-ell)-1).
```

All denominators are nonzero because the row domain has order `512` and the
M3 window has `m <= 128`; hence the exponents `i-ell` are nonzero modulo the
domain order.  Thus the trace is a completely explicit subgroup sum.  Any
eventual proof that the adjacent spectra are disjoint must, in particular,
control the two first coefficients

```text
tr(K_0),    tr(K_1).
```

The verifier does not currently use this closed form; it is included to expose
the first algebraic invariant one would attack in a hand proof.

For later symbolic work, the Lagrange value above can be written without a
hidden product over deleted nodes.  Put

```text
P_s = prod_{t=1}^s (1-alpha^t),    P_0=1,
R_i = m-1-i.
```

For `0 <= i < m` and `0 <= a < r`,

```text
L_i(alpha^(m+a))
  = (-1)^R_i alpha^(R_i(R_i+1)/2)
    * P_{a+m} /
      (P_a P_i P_{R_i} (1-alpha^(m+a-i))).
```

Proof.  Starting from

```text
L_i(alpha^(m+a))
  = prod_{ell != i} (alpha^(m+a-ell)-1)/(alpha^(i-ell)-1),
```

the numerator is

```text
(-1)^(m-1) P_{a+m} / (P_a (1-alpha^(m+a-i))).
```

The denominator is

```text
(-1)^i alpha^(-R_i(R_i+1)/2) P_i P_{R_i}.
```

Dividing gives the displayed formula.  In the current M3 window the relevant
exponents are all strictly between `0` and `512`, so the displayed factors are
nonzero in the order-512 subgroup.

## Window Normalization

Two elementary invariances reduce the consecutive-subgroup case to a normalized
window.

First, if `beta` is nonzero and

```text
beta X = (beta x_0,...,beta x_{m-1}),
beta Y = (beta y_0,...,beta y_{r-1}),
```

then

```text
det(H_{beta X}^(h) + Z H_{beta Y}^(h))
  = beta^(hm+m(m-1)) det(H_X^(h) + Z H_Y^(h)).
```

Indeed, with `D_beta=diag(1,beta,...,beta^(m-1))`, the shifted moment matrix
for `beta X` is

```text
H_{beta X}^(h) = beta^h D_beta H_X^(h) D_beta,
```

and the same formula holds for `Y`.  Taking determinants gives the displayed
scalar factor.  Since this factor is nonzero, affine roots and gcds of shifted
minors are unchanged by multiplying the whole window by `beta`.

Second, if all nodes lie in a multiplicative subgroup of order `N`, then

```text
H_X^(h+N) = H_X^(h),     H_Y^(h+N) = H_Y^(h),
```

so the shifted determinants and kernels are periodic in `h` modulo `N`.

For the accepted `F_17^32` row, the domain is the order-512 subgroup

```text
1, alpha, alpha^2, ..., alpha^511.
```

Therefore a consecutive low-rank window

```text
X = beta {1,alpha,...,alpha^(m-1)},
Y = beta {alpha^m,...,alpha^(m+r-1)}
```

has the same finite affine root data as the normalized window with `beta=1`,
and only `h mod 512` matters.  This is why the synthetic packet can use the
prefix `X={1,alpha,...,alpha^j}` without losing any case that differs only by
a cyclic domain rotation.

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
