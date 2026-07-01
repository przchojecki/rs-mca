# Hankel Rank-6 Separated Six-Spike Closure

Status: PROVED / AUDIT.

This note records a complete finite-plus-projective closure for a robust
rank-6 family in the tall part of the pinned M3 window.  It is narrower than an
arbitrary rank-6 bucket theorem, but it removes both prefix and unit-weight
specialization from a natural six-spike perturbation family.

Work in

```text
C = RS[F_17^32,H,256],    |H| = 512,
388 <= A <= 426,
```

and write

```text
j = 512 - A,    t = A - 256,    m = j+1.
```

Let `X,Y` be disjoint subsets of `H` with

```text
|X| = m,     |Y| = 6,
```

and choose nonzero weights `a_x` and `b_y`.  Define

```text
u_r = sum_{x in X} a_x x^r,
v_r = sum_{y in Y} b_y y^r.
```

For a finite slope `z`, the Hankel block is

```text
H(u+zv) = V_t(S_z) diag(w_z) V_m(S_z)^T,
```

where `S_0=X`, and for `z!=0`,

```text
S_z = X union Y.
```

At `z=0`, `|S_0|=m` and `t>=m`, so the weighted Vandermonde factorization has
rank `m`.  At `z!=0`, all weights on `X union Y` remain nonzero, and

```text
|X union Y| = m+6 = j+7 <= t
```

throughout `388 <= A <= 426`.  Hence `V_t(S_z)` has full column rank `m+6`,
`diag(w_z)` is invertible, and `V_m(S_z)^T` has full column rank `m`; the
product has rank `m`.  No finite slope causes rank drop, so the canonical
finite root table is empty.

The projective endpoint is supplied by

```text
experimental/notes/m1/hankel_rank6_projective_endpoint_uniform.md
```

for the same supports and weights: choose a locator whose roots are the six
direction nodes plus all but seven base nodes.  This gives a genuine
split-locator endpoint at `[0:1]`.  Therefore this separated six-spike family
has total projective contribution exactly `1`, safely below the projective
budget `6`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_separated_six_spike_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-separated-six-spike-closure/f17_32_n512_k256_m3_rank6_separated_six_spike_closure.json
```

Nonclaims:

```text
no claim for the boundary agreements A=385,386,387;
no arbitrary rank-6 Hankel-pencil classification;
no overlapping-support cancellation analysis;
no endpoint quotient/extension/tangent payment theorem.
```
