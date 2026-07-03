# A407/A408 residual-design threshold certificate

This directory contains the generated artifacts for the A407/A408 residual-design threshold packet.

## Files

- `m1_a407_a408_residual_design_threshold_v1.json`: machine-readable certificate for the A=408 and A=407 exact `LD_sw` rows, the A=406 first-failure diagnostic for this method, and the exact-budget prime gate.
- `tangent_witness_A408_A407_A406_v1.json`: symbolic moving-root tangent lower witnesses for A=408, A=407, and A=406.

## Regeneration

Run from the repository root:

```bash
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --write
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --check
```

## Claims

- For every finite field `F` and every distinct 512-point RS domain `D`, `LD_sw(RS[F,D,256],408)=105`.
- For every finite field `F` and every distinct 512-point RS domain `D`, `LD_sw(RS[F,D,256],407)=106`.
- For `p=27168*2^120+1`, the row `RS[F_p,H,256]` has an adjacent finite-slope support-wise MCA gate: A=407 is safe and A=406 is unsafe at `2^-128`.

## Non-claims

- No exact A=406 upper bound is claimed.
- No full M1 closure is claimed.
- No ordinary list-decoding, interleaved-list, protocol soundness, or challenge-field ledger claim is made.
- The candidate site fragments are review artifacts; live `site/data/*.json` arrays should be updated only after review.
