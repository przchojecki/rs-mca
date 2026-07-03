# E13 sparse-greedy syzygy branch

- **Status:** EXPERIMENTAL / AUDIT.
- **DAG nodes:** `spread_exception_classification`, `spread_regime_bound`.
- **Verifier:** `experimental/scripts/verify_e13_sparse_greedy_syzygy_branch.py`.
- **Artifact:**
  `experimental/data/certificates/spread-regime-design-evidence/e13_sparse_greedy_syzygy_branch.json`.

This note refines the negative part of
`e13_spread_exception_finite_geometry_census.md`.  The earlier E13 census
showed that the bounded `n=32` greedy controls contain `71` nondegenerate
below-cap rank-loss exceptions outside the current `AG(2,4)` line-net
classifier.  This verifier asks whether those exceptions at least share a
uniform algebraic shape.

## Outcome

Every replayed `n=32` control exception is a one-dimensional full-support
syzygy among the split-locator moment rows.

```text
total sparse-greedy syzygy exceptions: 71
one-dimensional left nullspace: true
full locator support: true
```

By cell:

```text
greedy_32_j5_lambda1, distinct_geometric, size 5:
    1 nondegenerate syzygy exception

greedy_32_j6_lambda2, distinct_linear, size 6:
    36 nondegenerate syzygy exceptions
    22 degenerate below-cap losses

greedy_32_j6_lambda2, distinct_geometric, size 6:
    34 nondegenerate syzygy exceptions
    22 degenerate below-cap losses
```

For each nondegenerate exception, the verifier computes the left-nullspace
relation and checks the two polynomial identities already used in the E3
dependency certificate:

```text
sum_{T,m} c_{T,m} X^m ell_T(X) = 0,
sum_{T,m} c_{T,m} z_T X^m ell_T(X) = 0.
```

The artifact stores the locator family, the subset indices, the rank, the
degree deficiency, and the relation coefficients by locator block.  The
relations are full-support: no locator block has all coefficients zero.  Most
relations use all three moment rows in every block; the only exception is five
geometric `j=6` cases where one block has two nonzero coefficients and the
other five blocks use all three.

## Interpretation

This does not repair the finite-geometry-only conjecture.  It gives a sharper
replacement target:

```text
below-cap spread rank loss is either
  finite-geometry/net shaped,
  v-syndrome degenerate,
  or a full-support sparse-greedy syzygy.
```

The new branch is now exact enough to attack.  A useful next theorem would
show that full-support sparse-greedy syzygies are either bounded uniformly,
paid by an existing ledger after a change of coordinates, or impossible once
the toy control restrictions are replaced by the actual prize-scale
hypotheses.

## Non-claims

This packet does not prove `spread_regime_bound`.

This packet does not classify every `n=32` support family.  It replays the
bounded controls from E13.

This packet does not show the sparse-greedy syzygy branch is paid, bounded
uniformly, or asymptotically harmless.  It only replaces an opaque
unclassified bucket with exact algebraic certificates.

## Reproduce

```bash
python3 experimental/scripts/verify_e13_sparse_greedy_syzygy_branch.py
python3 experimental/scripts/verify_e13_sparse_greedy_syzygy_branch.py --emit
python3 experimental/scripts/verify_e13_sparse_greedy_syzygy_branch.py --check experimental/data/certificates/spread-regime-design-evidence/e13_sparse_greedy_syzygy_branch.json
```
