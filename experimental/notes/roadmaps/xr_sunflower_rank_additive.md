# XR sunflower rank additivity (2c-beta-1)

DAG node: `xr_sunflower_rank_additive`.

Status: PROVED.

## Critical-path role

This is a proof-spine packet for the conditional prize route.  The syzygy
support lemma says that residual `r <= k` rank stagnation must be carried by
overlap geometry.  This packet proves that one large class of such geometry,
sunflowers with common core below the RS dual distance, cannot stagnate at all:
the tensor row rank is exactly additive.

Consequently planted-sunflower/list-lane configurations are not a separate
unpaid MCA residue in the distinct-slope face-4 branch.  They either stay in
the list lane already isolated by `xr_smallcore_rungs_2a_2b.md`, or they are
rank-additive and bounded by the ambient `2n` dimension cap.  The remaining
conditional terminal work is still the non-sunflower active-core/PTE
polynomial residue.

## Statement

Let `C` be the length-`n`, dimension-`k` Reed-Solomon evaluation code on
distinct field points `H`, and write `A = k + t`.

For an agreement support `T` with `|T| = A`, let

```text
Lambda_T = { lambda in C^perp : supp(lambda) subset T }.
```

For a finite slope `z`, the alignment row block is

```text
R(T,z) = { (lambda, z lambda) : lambda in Lambda_T }.
```

If `T_1, ..., T_m` form a sunflower with common core `Y`,

```text
T_i cap T_j = Y for all i != j,
```

and `|Y| < k+1`, while the slopes `z_1, ..., z_m` are distinct, then

```text
rank(R(T_1,z_1) + ... + R(T_m,z_m)) = m t.
```

In particular, any aligned sunflower family of this kind satisfies

```text
m <= floor(2n/t).
```

The DAG's far-spread version assumes `|Y| < k`, so it is covered.

## Proof

As in `qx13_pair_rank_ledger`, `Lambda_T` is the shortened dual of the RS
code on `T`. The RS dual is MDS with minimum distance `k+1`, and
`dim Lambda_T = |T| - k = t`.

Suppose a linear relation exists among the sunflower row blocks:

```text
sum_i (lambda_i, z_i lambda_i) = 0,
lambda_i in Lambda_{T_i}.
```

Taking first coordinates gives

```text
sum_i lambda_i = 0.
```

Fix `i` and let `x in T_i \ Y`. Since the supports are a sunflower, `x` lies
in no other `T_j`. Evaluating the first-coordinate relation at `x` gives
`lambda_i(x) = 0`. Hence every `lambda_i` is supported inside the common core
`Y`.

But `|Y| < k+1`, and no nonzero word of `C^perp` has support below `k+1`.
Therefore every `lambda_i` is zero. Thus there is no nontrivial row syzygy
among the blocks. Each block has rank `t`, so the stacked rank is exactly
`m t`.

All rows live in the ambient pair space `F^H x F^H`, of dimension `2n`.
Therefore an aligned sunflower family cannot have `m t > 2n`, proving
`m <= floor(2n/t)`.

## Interpretation

This is the safe side of the 2c-beta split. Planted-sunflower configurations
that are hard for the same-slope list lane are harmless for the distinct-slope
MCA lane: the petal coordinates forbid cancellation, and the common core is
too small to carry a nonzero RS dual word.

The result is rank-level and worst-case; it does not use randomness or moment
averaging.

## Verifier

`experimental/scripts/verify_xr_sunflower_rank_additive.py` rebuilds the
shortened duals and tensor row blocks over two packed toy rows:

```text
F_11: n=10, k=2, A=4, t=2, core size 1
F_13: n=11, k=3, A=5, t=2, core size 2
```

It exhausts every ordered sunflower triple in these rows and checks:

- `dim Lambda_T = t`;
- the shortened dual minimum weight is `k+1`;
- no common core carries a nonzero shortened-dual word;
- every sunflower triple has stacked rank `3t`;
- the `2n/t` cap arithmetic is consistent.

The recomputed summary is pinned in
`experimental/data/certificates/xr-sunflower-rank-additive/toy_sunflower_rank.json`.
