# Lower reserve / unsafe-side (hard input e)

## Status
EXPERIMENTAL / AUDIT. Verdict: NO ISSUE. W34-R1: dual-route is genuine.

## Dual routes
- generator: nested (num+den-1)//den ceilings (eq:exact-unsafe-budget)
- checker: binary-search ceil_div (least k with k*den>=num) + Fraction ceil for L

## Reproducibility
```
py -3.13 experimental/scripts/verify_lower_reserve_unsafe.py --emit-defaults --check
py -3.13 experimental/scripts/verify_lower_reserve_unsafe_check.py --check
```
