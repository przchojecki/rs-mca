# L1 coset-chart residue-line bridge certificate

This directory contains generated artifacts for `l1_coset_chart_residue_bridge_v1`.

## Files

- `l1_coset_chart_residue_bridge_v1.json`: finite verifier certificate for the coset-chart quotient-or-residue-line-bridge classification.

## Regeneration

Run from the repository root:

```bash
python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --write
python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --check
```

## Claim

Every capped full-petal coset-chart kernel set is quotient-coset or carries a degree-`<=t-2` residue-line projective-pair certificate. After simultaneous active basepoints are cancelled, the certificate is an ordinary residue-line datum on the surviving quotient labels, with denominator nonzero and the sharp degree bound `<= active_count-2`.

## Non-claims

This is not a full L1 local-limit theorem, not an arbitrary-petal theorem, not a quotient-only classification, not a primitive-vacancy theorem under the current stabilizer-primitive ledger, and not a global quantitative bound for residue-line packing.
