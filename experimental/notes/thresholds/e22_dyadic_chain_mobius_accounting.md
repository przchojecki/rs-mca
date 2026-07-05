# E22 Dyadic-Chain Mobius Accounting

Status: PROVED.

Source DAG node: `e22_dyadic_chain_mobius_accounting`.

Depends on: `e22_minimal_scale_partition`.

## Statement

Let the admissible dyadic quotient scales be a finite chain

```text
M_1 < M_2 < ... < M_r.
```

For each scale `M_j`, let:

- `A_j` be the raw number of support classes counted by the scale-`M_j`
  staircase summand;
- `N_j` be the number of selected classes whose minimal admissible scale is
  `M_j`;
- `O_{i,j}` for `i<j` be the number of classes selected at `M_i` that are also
  counted by the raw scale-`M_j` summand.

Then the dyadic scale accounting is triangular:

```text
A_j = N_j + sum_{i<j} O_{i,j}.
```

Consequently, exact selected minimal-scale counts are recovered by

```text
N_j = A_j - sum_{i<j} O_{i,j}.
```

## Proof

By the minimal-scale partition, every class counted at scale `M_j` has a unique
minimal admissible scale `M_i` with `i <= j`.  Splitting the raw scale-`M_j`
classes by this unique minimum gives a disjoint union.  The `i=j` part is
`N_j`; the `i<j` parts are exactly the overlaps `O_{i,j}`.

The replay script checks this triangular identity for all nonempty
admissible-scale subsets of finite chains of lengths one through eight.

## Non-Claims

This packet proves the formal triangular accounting identity only.  It does not
compute the arithmetic overlap formulas, does not evaluate an E22 pricing
column, and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_e22_dyadic_chain_mobius_accounting.py --emit
python3 experimental/scripts/verify_e22_dyadic_chain_mobius_accounting.py \
  --check experimental/data/certificates/e22-dyadic-chain-mobius-accounting/e22_dyadic_chain_mobius_accounting.json
```
