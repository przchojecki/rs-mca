# E22 Minimal-Scale Partition

Status: PROVED.

Source DAG node: `e22_minimal_scale_partition`.

Depends on: `e22_dyadic_minimal_scale_selector`.

## Statement

For dyadic E22 support-scale data, support classes with at least one admissible
quotient modulus decompose disjointly by their unique minimal admissible
modulus.

Equivalently, the tail-minimal predicates

```text
|B_M(R)| < M
and |B_{M'}(R)| >= M' for every smaller admissible M' < M
```

form a disjoint and exhaustive partition of selected canonical representatives.

## Proof

The selector packet gives every nonempty dyadic admissible-scale set a unique
minimum.  A support class belongs to the cell indexed by that minimum.  It cannot
belong to two cells because a finite totally ordered set cannot have two
distinct minima, and it cannot be omitted because every nonempty admissible set
has a minimum.

The replay script checks this as a pure finite-chain identity for dyadic chains
of lengths up to eight: every nonempty subset has exactly one tail-minimal cell,
the cells are disjoint, and their union covers all nonempty admissible subsets.

## Non-Claims

This packet proves the partition structure only.  It does not compute
cross-scale overlap counts, does not evaluate a pricing column, and does not
alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_e22_minimal_scale_partition.py --emit
python3 experimental/scripts/verify_e22_minimal_scale_partition.py \
  --check experimental/data/certificates/e22-minimal-scale-partition/e22_minimal_scale_partition.json
```
