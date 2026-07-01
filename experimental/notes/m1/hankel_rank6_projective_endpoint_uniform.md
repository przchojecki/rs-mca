# Hankel Rank-6 Projective Endpoint Uniformity

Status: PROVED / AUDIT.

This note records the support- and weight-uniform endpoint half of the rank-6
M3 boundary.  It is separate from finite-root closure: it proves robust
projective endpoint nonemptiness, not safety of arbitrary rank-6 buckets.

Work in the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426,
```

and write

```text
j = 512 - A,    t = A - 256.
```

Let `X,Y` be disjoint subsets of `H` with

```text
|X| = j+1,     |Y| = 6,
```

and choose nonzero weights `a_x` and `b_y`.  Define the Hankel syndromes

```text
u_m = sum_{x in X} a_x x^m,
v_m = sum_{y in Y} b_y y^m.
```

The direction block has rank exactly `6`:

```text
H(v) = V_t(Y) diag(b_y) V_{j+1}(Y)^T,
```

because `Y` is distinct, all `b_y` are nonzero, and both Vandermonde factors
have rank `6`.

Now choose any seven surviving base nodes `R subset X`.  Let `L` be the monic
locator whose roots are

```text
Y union (X \ R).
```

Then `deg L = 6 + ((j+1)-7) = j`, and all roots lie in `H`; since
`X^512-1` is separable in characteristic `17`, this is a split locator divisor
of `X^512-1`.

Every direction node is a root of `L`, so `H(v)ell=0`.  For `H(u)ell`, only
the seven surviving base nodes contribute:

```text
(H(u)ell)_r = sum_{x in R} a_x L(x) x^r.
```

The first seven rows form a `7 x 7` Vandermonde system on the distinct nodes
in `R`.  Since each `a_x L(x)` is nonzero, these seven rows cannot all vanish.
Therefore `H(u)ell != 0`, and `[0:1]` is a genuine support-wise
split-locator endpoint.

This is the robust endpoint obstruction for rank 6: endpoint nonemptiness is
not caused by the prefix/unit-weight specialization.  Consequently, a general
rank-6 closure cannot rely on projective endpoint emptiness.  It must use
endpoint payment, finite-root refinement, or a sharper classification of which
rank-6 endpoint branches are harmless.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_projective_endpoint_uniform.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json
```

Nonclaims:

```text
no finite affine root-table computation;
no arbitrary rank-6 Hankel-pencil safe-side bound;
no endpoint quotient/extension payment theorem;
the many locators all witness the same projective slope [0:1].
```
