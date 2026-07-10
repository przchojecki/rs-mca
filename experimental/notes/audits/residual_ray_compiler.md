# w33-residual-ray-compiler

## Status
EXPERIMENTAL / AUDIT. Verdict: NO ISSUE.

## Dual routes
- generator: enumerate F_q^d residual grid; set of gamma(p)
- checker: linear-form image rank formula |im|=q

## Reproducibility
```
py -3.13 experimental/scripts/verify_residual_ray_compiler.py --emit-defaults --check
py -3.13 experimental/scripts/verify_residual_ray_compiler_check.py --check
```
