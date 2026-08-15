# Sparse-direction near-Johnson centered-Gram payment

## Status

PROVED, field-general, exact finite arithmetic.

## List lemma

For equal-size `A`-blocks in an `n`-set with pairwise intersections at most
`c`, put

```text
g=nc-A^2>=0,
G=(A-c)^2-cg.
```

When `G>0`, the centered incidence Gram matrix gives

```text
L <= floor(n*A*(A-c)/G).
```

The key exact rank improvement is `rank(BB^T-cJ)<=rank(B)<=n`: equal row
sums put the all-ones vector inside `col(B)`.  Trace-rank, Cauchy incidence,
and the integer inequality `delta^2<=c*delta` complete the proof.

## MCA compiler

After puncturing a gauged direction support of size `e`, split transformed
explanations at deficit `u=floor(e/2)`.  The low-deficit count has the
ordinary Johnson cap `J_u`; all remaining explanations own one slope.  If
`Q_e` is the centered-Gram cap at agreement `m-e`, then

```text
|Z| <= (e-1)J_u+Q_e.
```

## Exact walls

```text
KoalaBear:   e<=64037, bound 198047217;
Mersenne-31: e<=65418, bound  16759641.
```

At KoalaBear `e=64038`, the Gram denominator is `-36911`.  At Mersenne
`e=65419`, it remains positive, but the valid bound `18212004` exceeds the
budget `16777215`.

The full-lift residual intervals become

```text
KoalaBear: 64038<=e<=1044238;
Mersenne:  65419<=e<=1044241.
```

## Audit

`experimental/verify_mca_sparse_direction_near_johnson_gram_rank_v1.py`
checks all 311 newly paid supports, both adjacent records, a rational replay,
an explicit finite block control, and two hostile mutations.

## Nonclaims

No adjacent cell or official row is closed.  A negative Gram denominator or
an over-budget upper bound is not an unsafe certificate.
