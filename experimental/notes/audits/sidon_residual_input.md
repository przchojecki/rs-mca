# w36-sidon-residual-input

## Status
EXPERIMENTAL / AUDIT. **Verdict: OPEN GAP**.

## Dual routes
- generator: Counter energy Gsid on residual fibers; SFM1 ratio R*sqrt(p)/N
- checker: 4-fold energy Gsid; independent SFM1 ratio recompute

## Reproducibility
```
py -3.13 experimental/scripts/verify_sidon_residual_input.py --emit-defaults --check
py -3.13 experimental/scripts/verify_sidon_residual_input_check.py --check
```
