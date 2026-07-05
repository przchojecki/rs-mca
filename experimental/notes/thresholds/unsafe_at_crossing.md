# Unsafe At Crossing

Status: PROVED.

Source DAG node: `unsafe_at_crossing`.

## Statement

For each admissible row, the adjacent grid point has an unsafe witness:

```text
B_C(a_safe - 1) > B*.
```

The proof is by an exhaustive two-branch split.

```text
collision-free branch -> qfloor_exact witness family
collided branch       -> averaged_slope_conversion
```

## Dependency Sub-DAG

```text
qfloor_exact              -> unsafe_at_crossing
averaged_slope_conversion -> unsafe_at_crossing
```

The current source DAG marks both inputs as `PROVED`.  In the upstream repo,
`qfloor_exact` is anchored by `prop:qfloor` in `tex/slackMCA_v4.tex`; the
collided branch is anchored by
`experimental/notes/m1/m1_averaged_slope_conversion.md`.

## Proof

The branch predicate is whether the adjacent-row witness family is
collision-free.

If it is collision-free, the quotient-floor family supplies more than `B*`
distinct bad slopes at the adjacent grid point.  This is the `qfloor_exact`
route.

If it is collided, the averaged locator-to-slope conversion applies to the
post-paid family.  Its occupancy inequality converts enough aligned locators,
after the same-slope correction, into a received pair with at least `B*`
distinct bad slopes.  This is the `averaged_slope_conversion` route.

The two cases are exhaustive, and both route predicates are green in the
integrated prize DAG.  Therefore every admissible row has the adjacent unsafe
witness.

## Non-Claims

This packet does not recompute `prop:qfloor`, does not rerun the
averaged-slope ledger, does not choose deployed v13 rows, and does not alter
Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_unsafe_at_crossing.py --emit
python3 experimental/scripts/verify_unsafe_at_crossing.py \
  --check experimental/data/certificates/unsafe-at-crossing/unsafe_at_crossing.json
```
