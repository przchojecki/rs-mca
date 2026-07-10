# w36-ray-compiler-input

## Status
EXPERIMENTAL / AUDIT. **Verdict: OPEN GAP**.

## Dual routes
- generator: enumerate F_q^d evaluate Phi; |set| of values
- checker: linear closed-form |im|; odd-q square-image formula (q+1)/2

## Reproducibility
```
py -3.13 experimental/scripts/verify_ray_compiler_input.py --emit-defaults --check
py -3.13 experimental/scripts/verify_ray_compiler_input_check.py --check
```
