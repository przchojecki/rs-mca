# XR syzygy support lemma (2c-alpha)

DAG node: `xr_syzygy_support_lemma`.

Status: PROVED in the rank-linear algebra model used by `qx13_pair_rank_ledger`.

## Critical-path role

This is a proof-spine packet for the conditional prize route.  After
`xr_pencil_cascade.md` and `xr_smallcore_rungs_2a_2b.md` remove the paid
large-core, list, and tangent-depth bands, the remaining face-4 work is the
irreducible `r <= k` rank/spread shell.  This lemma is the first structural
filter on that shell: if adding a new distinct-slope support does not raise
the stacked rank by the expected `t`, then a shortened-dual syzygy must exist,
and its nonzero support must be covered by pairwise intersections with overlap
budget at least `k+1`.

The lemma therefore converts an abstract rank-stagnation event into a finite
support geometry problem.  Downstream sunflower and eliminant packets classify
or charge those geometries; the separate terminal condition remains the
`active_core_count_bound` / PTE polynomial residue consumed by the clean-rate
compiler.

## Statement

Let `C` be the length-`n`, dimension-`k` Reed-Solomon evaluation code on a
set `H` of distinct field points. Write `A = k + t`.

For an agreement support `T subset H` with `|T| = A`, define

```text
Lambda_T = { lambda in C^perp : supp(lambda) subset T }.
```

Then `dim Lambda_T = t`, every nonzero member of `Lambda_T` has weight at
least `k + 1`, and the alignment condition for slope `z` has row block

```text
R(T,z) = { (lambda, z lambda) : lambda in Lambda_T } subset F^H x F^H.
```

Now take distinct finite slopes `z_1, ..., z_m` and agreement supports
`T_1, ..., T_m`, each of size `A`. Suppose the last block has deficient
increment:

```text
rank(R(T_1,z_1) + ... + R(T_m,z_m))
  < rank(R(T_1,z_1) + ... + R(T_{m-1},z_{m-1})) + t.
```

Then there are dual words `lambda_i in Lambda_{T_i}`, not all zero and with
`lambda_m != 0`, such that

```text
sum_i lambda_i = 0,
sum_i z_i lambda_i = 0.
```

Consequently

```text
supp(lambda_m) subset union_{i<m} (T_m cap T_i)
```

and hence

```text
sum_{i<m} |T_m cap T_i| >= k + 1.
```

The same conclusion holds for any nonzero member of any syzygy after relabeling.

## Proof

The space `Lambda_T` is the shortening of the MDS dual `C^perp` to the set
`T`. Equivalently, it is the kernel of the `k x A` Vandermonde moment matrix
`(x^d)_{0 <= d < k, x in T}`. Since the evaluation points are distinct and
`A >= k`, this matrix has rank `k`, so `dim Lambda_T = A - k = t`.
The dual of an `[n,k]` RS code is MDS with minimum distance `k + 1`, so every
nonzero `lambda in Lambda_T` has support size at least `k + 1`.

Alignment on `T` at slope `z` means that `u + z v` restricts to a codeword on
`T`. Testing this against all dual words supported in `T` gives exactly the
rows `(lambda, z lambda)`, with `lambda in Lambda_T`. The block has rank `t`
because `lambda -> (lambda, z lambda)` is injective.

If the last block does not contribute its full `t` new rows, some nonzero row
from the last block lies in the span of the previous blocks. Equivalently,
there are `lambda_i in Lambda_{T_i}` with `lambda_m != 0` and

```text
sum_i (lambda_i, z_i lambda_i) = 0.
```

This is the pair of coordinate identities

```text
sum_i lambda_i = 0,
sum_i z_i lambda_i = 0.
```

Subtracting `z_m` times the first identity from the second removes
`lambda_m`:

```text
sum_{i<m} (z_i - z_m) lambda_i = 0.
```

The twists `z_i - z_m` are nonzero because the slopes are distinct. More
importantly, the first coordinate identity already gives the support
containment. If `x in supp(lambda_m)` and `x` lies in no earlier `T_i`, then
all earlier `lambda_i(x)` vanish, so `sum_i lambda_i(x) = lambda_m(x) != 0`,
contradiction. Therefore every point of `supp(lambda_m)` lies in some
intersection `T_m cap T_i`, `i < m`.

Finally,

```text
k + 1 <= |supp(lambda_m)|
      <= | union_{i<m} (T_m cap T_i) |
      <= sum_{i<m} |T_m cap T_i|.
```

This proves the overlap budget.

## Consequences

In the far-spread regime, where each pairwise overlap is `< k`, a stagnation
event cannot be paid by a single partner: one overlap contributes at most
`k - 1`, below the forced `k + 1` budget. Thus the minimal stagnating
configuration has at least three supports.

The lemma is a necessary condition, not a sufficient condition. Meeting the
overlap budget does not by itself produce stagnation: the twisted previous
sum `sum_{i<m} (z_i - z_m) lambda_i` must vanish, and the first-coordinate
sum must land as a nonzero member of `Lambda_{T_m}`.

## Verifier

`experimental/scripts/verify_xr_syzygy_support_lemma.py` recomputes the
shortened dual spaces and syzygy kernels over two toy rows:

```text
F_7:  n=6, k=2, A=4, t=2, slopes 1,2,3
F_11: n=7, k=3, A=5, t=2, slopes 1,3,7
```

For every ordered triple of agreement supports in those rows it verifies:

- `dim Lambda_T = t`;
- nonzero shortened-dual words have weight at least `k+1`;
- deficient rank increment is equivalent to a syzygy with nonzero new block;
- every nonzero block projection in every syzygy is supported inside the union
  of its pairwise intersections and satisfies the `k+1` overlap budget.

The recomputed summary is pinned in
`experimental/data/certificates/xr-syzygy-support-lemma/toy_linear_algebra.json`.
