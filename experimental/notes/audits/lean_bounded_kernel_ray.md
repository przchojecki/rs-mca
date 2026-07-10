# Lean: bounded residual-kernel ray compiler instance

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only theorem instance.
No sorry, no mathlib.

## Object
Instance of thm:bounded-residual-kernel-ray (RC_ker):
|Z| ≤ (t+1)·q^κ with κ=max(0,|U|−R) on q=3, R=2, |U|=3, t=1 → bound=6; zSize=4≤6.
Also κ=0 specialization bound=t+1.

## Build
```
cd experimental/lean/bounded_kernel_ray && lake build
# ✔ Built BoundedKernelRay
```

## Dual routes
- generator: Lean kernel native_decide on κ formula and bound inequality
- checker: alternate decide proofs of the same Nat goals

## Nonclaims
- Toy Nat instance of the bound formula; not a formalization of the general proof.
