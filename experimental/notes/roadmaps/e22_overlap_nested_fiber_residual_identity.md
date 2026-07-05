# E22 Nested-Fiber Residual Identity

- **DAG node:** `e22_overlap_nested_fiber_residual_identity`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_overlap_nested_fiber_residual_identity/`
- **Depends on:** `e22_cross_scale_support_canonical_form`
- **Verifier:** `python3 experimental/scripts/verify_e22_overlap_nested_fiber_residual_identity.py`

## Statement

Let `M_i < M_j` be dyadic quotient scales.  Every `M_j`-fiber is a disjoint
union of

```text
q = M_j / M_i
```

many `M_i`-fibers.

For a support `R`, recover the canonical scale-`M_i` data

```text
R = B_i disjoint_union U_i,
```

where `U_i` is the union of all full `M_i`-fibers contained in `R`, and
`B_i = R \ U_i`.  Let `S_i` be the selected full `M_i`-fibers.

A full `M_j`-fiber is contained in `R` exactly when all of its `M_i`-children
belong to `S_i`.  Consequently the canonical scale-`M_j` tail is

```text
B_j =
  B_i disjoint_union
  {selected M_i-fibers whose M_j-parent is not completely selected},
```

and

```text
|B_j| = |B_i| + M_i * r_{i,j}(S_i),
```

where `r_{i,j}(S_i)` is the number of selected `M_i`-fibers whose
`M_j`-parent is not completely selected.  Therefore `R` is raw-admissible at
scale `M_j` exactly when

```text
|B_i| + M_i * r_{i,j}(S_i) < M_j.
```

## Proof

The quotient partitions are nested.  Every coarse `M_j`-fiber is the disjoint
union of `M_j/M_i` fine `M_i`-fibers.

Let `S_i` be the fine `M_i`-fibers fully contained in `R`, let `U_i` be their
union, and let `B_i = R \ U_i`.  This is the canonical full-fiber recovery
from `e22_cross_scale_support_canonical_form`.

For a coarse `M_j`-fiber `C`, if every fine child of `C` belongs to `S_i`,
then all points of `C` lie in `U_i`, so `C` is fully contained in `R`.
Conversely, if `C` is fully contained in `R`, then each fine child of `C` is
also fully contained in `R`, hence each child belongs to `S_i`.

Thus the full coarse fibers are exactly the coarse parents whose fine children
are all selected.  Removing those coarse parents from `R` leaves exactly two
disjoint pieces: the original fine-scale tail `B_i`, and the selected fine
fibers whose coarse parent is not complete.  This gives

```text
|B_j| = |B_i| + M_i * r_{i,j}(S_i).
```

By the cross-scale support canonical-form node, raw scale-`M_j`
admissibility is equivalent to `|B_j| < M_j`; substituting the displayed
formula proves the criterion.

## Role In The Program

This is the local overlap identity needed by the `(Q)` quotient-ledger route:
it converts cross-scale admissibility into a residual fine-fiber statistic,
which later generating-function and overlap-count packets can price exactly.

