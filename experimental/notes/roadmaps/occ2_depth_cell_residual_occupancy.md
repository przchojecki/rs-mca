# OCC-2: depth-cell residual occupancy audit

- **DAG node:** `a2_depth_cell_residual_occupancy`.
- **Task:** OCC-2.
- **Status:** CONDITIONAL / RESIDUE.  The A2 routing table is complete, but
  direct depth-cell packing does not prove the quantitative ledger.
- **Verifier:** `experimental/scripts/verify_occ2_depth_cell_occupancy.py`.
- **Certificate:**
  `experimental/data/certificates/occ2-depth-cell-occupancy/occ2_depth_cell_occupancy.json`.

## Setup

W2/A2 routes every partial-tangent pair to a depth cell

```text
d = r-k,        s = A-r,        d+s=t,
1 <= d <= t-2, 2 <= s <= t-1.
```

For a fixed anchor support `T0` of size `A`, a formal depth-`d` overlap core
inside `T0` is a `(k+d)`-subset.  Therefore the number of possible formal
cores at complementary codimension `s=t-d` is

```text
C(A,k+d) = C(A,s).
```

This is only a formal lattice count; it is not an aligned-support
construction.  It tests whether a constant cap per cell, summed over all
cells, could ever close the ledger.

## Verdict

The direct packing proof fails at every clean-rate candidate.  Even one event
in each formal depth cell at the shallow checked boundary already exceeds a
linear budget.

```text
RowC 1/4:   C(261,2) = 33,930      > 1024
RowC 1/8:   C(133,2) = 8,778       > 1024
RowC 1/16:  C(67,2)  = 2,211       > 1024
```

The same obstruction is much larger at the prize rows:

```text
prize 1/4:   log2(C(A,2)/n) = 36.0447
prize 1/8:   log2(C(A,2)/n) = 34.0888
prize 1/16:  log2(C(A,2)/n) = 32.0888
```

The Row-C rows are checked at every partial depth; the prize rows use exact
small-`s` binomial lower bounds (`s=2,3,4`) to avoid large enumeration.

## Named Residue

The replacement statement is:

```text
a2_depth_cell_active_shadow_bound
```

After the unified paid strip, for each fixed anchor support `T0` and depth
`d`, the occupied tangent-depth cells, or their weighted emissions, form a
linear active shadow; otherwise a positive-density subfamily must be one of
the already paid structures:

```text
tangent pencil,
quotient / Luroth pullback,
dihedral,
extension,
moment/PTE trade.
```

This is the depth-graded analogue of the lower-overlap active-shadow theorem
needed by A1.  A constant per-cell emission cap is still useful, but it must be
paired with an incidence theorem controlling which cells are actually active.

## Verification

Run:

```bash
python3 experimental/scripts/verify_occ2_depth_cell_occupancy.py
```
