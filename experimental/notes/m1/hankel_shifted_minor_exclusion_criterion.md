# Hankel Shifted-Minor Exclusion Criterion

Status: PROVED / AUDIT.

This note records the criterion used by the M3 shifted-minor audits.  It
separates roots of one regular maximal minor from genuine exact-support
witnesses for the full Hankel incidence problem.

## Criterion

Let `s=(s_0,...,s_{r-1})` be a syndrome sequence and fix an exact agreement
level `A`.  Put

```text
j = n-A,
t = A-k.
```

Assume `t >= j+2`, so the first two consecutive square Hankel minors of size
`j+1` are defined:

```text
Delta_0 = det(s_{a+b})_{0<=a,b<=j},
Delta_1 = det(s_{a+b+1})_{0<=a,b<=j}.
```

If a slope is an exact-support witness with co-support size at most `j`, then
both `Delta_0` and `Delta_1` vanish.  Therefore any finite root of `Delta_0`
at which `Delta_1` is nonzero is only a first-minor upper-bound root; it is not
an actual full-Hankel exact-support witness.

More generally, every `(j+1) x (j+1)` minor of the full `t x (j+1)` Hankel
matrix must vanish at an exact-support witness.

## Proof

If a syndrome is explained on a co-support `T` with `|T| <= j`, then

```text
s_m = sum_{x in T} c_x x^m
```

for some coefficients `c_x`.  The infinite Hankel matrix

```text
H_{a,b}=s_{a+b}
```

factors as

```text
H_{a,b} = sum_{x in T} (c_x x^a) x^b.
```

Thus every finite Hankel submatrix has rank at most `|T| <= j`.  In particular,
each `(j+1) x (j+1)` square minor of the full `t x (j+1)` regular bucket has
determinant zero.  Hence a root of one selected square minor that fails another
square minor cannot be an exact-support witness.

## Low-rank prefix update formula

The M3 low-rank shifted-minor audits use the following replay formula.  Let
`X={x_1,...,x_m}` be the prefix base nodes, and let `Y={y_1,...,y_s}` be the
low-rank update nodes.  For the row shift `q`, the base shifted Gram matrix is

```text
G_q(X) = (sum_{x in X} x^(a+b+q))_{0<=a,b<m}.
```

For `q=0`, this is the usual Vandermonde Gram matrix.  For `q=1` and nonzero
domain points, it is the same Gram matrix with node weights `x`.  It is
invertible for distinct nonzero `x_i`.

If `L_i` are the Lagrange basis polynomials for `X`, the matrix-determinant
lemma gives

```text
det(G_q(X) + Z G_q(Y))
  = det(G_q(X)) det(I_s + Z K_q),
```

where

```text
(K_q)_{a,b} = y_a^q sum_i x_i^(-q) L_i(y_a)L_i(y_b).
```

For `q=1`, this is exactly the row-shift-1 square minor formula used in the
`F_17^32` M3 low-rank audits.  Checking

```text
gcd(root_gcd(Delta_0), Delta_1) = 1
```

therefore clears every listed first-minor root as a full-Hankel witness.

## M3 low-rank instantiation

For the `F_17^32`, `n=512`, `k=256` M3 regular window:

```text
385 <= A <= 426,
j = 512-A,
t = A-256.
```

The smallest `t-(j+2)` occurs at `A=385`:

```text
t-(j+2) = 129-129 = 0.
```

So the row-shift-1 minor exists throughout the whole window.  The rank `6..11`
low-rank shifted-minor audit applies the criterion to every finite first-minor
root counted by the source slack certificates.

Non-claims: this criterion does not bound roots of the first minor by itself,
does not audit quotient-image/support, does not handle projective infinity, and
does not close arbitrary singular buckets.  It only says when a first-minor
root is not a genuine full-Hankel exact-support witness.
