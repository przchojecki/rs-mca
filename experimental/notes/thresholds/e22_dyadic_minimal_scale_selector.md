# E22 Dyadic Minimal-Scale Selector

Status: PROVED.

Source DAG node: `e22_dyadic_minimal_scale_selector`.

## Statement

For dyadic domains `n = 2^m`, the admissible quotient moduli are powers of two
and therefore form a finite chain.  Every canonical E22 support-scale class with
at least one admissible quotient modulus has a unique minimal admissible modulus.

Selecting this minimal modulus, together with the recovered tail and full-fiber
data at that modulus, gives a canonical representative of the cross-scale class.

## Proof

For a support `R`, define the admissible set

```text
A(R) = {M : M > t and |B_M(R)| < M},
```

where `B_M(R)` is the canonical tail recovered after deleting all full
`M`-fibers contained in `R`.  Since the dyadic moduli are totally ordered,
every nonempty finite set `A(R)` has a unique minimum.

The replay script exhausts all supports of a toy dyadic domain `n=16`, verifies
that every nonempty admissible set is sorted by the dyadic chain, and checks
that the selected modulus is always the unique minimum.

## Non-Claims

This packet proves only canonical dyadic minimal-scale selection.  It does not
compute cross-scale overlaps, does not assemble a pricing column, and does not
alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_e22_dyadic_minimal_scale_selector.py --emit
python3 experimental/scripts/verify_e22_dyadic_minimal_scale_selector.py \
  --check experimental/data/certificates/e22-dyadic-minimal-scale-selector/e22_dyadic_minimal_scale_selector.json
```
