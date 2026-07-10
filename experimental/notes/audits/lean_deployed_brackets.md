# lean: deployed-row unsafe/quiet Nat brackets (hard inputs d,e)

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only Nat anchors. No sorry, no mathlib.

## Build
```
cd experimental/lean/deployed_brackets && lake build
# ✔ Built DeployedBrackets
```

## Dual routes
- generator: Lean kernel native_decide on concrete Nat inequalities U0>B*, U1≤B*, a1=a0+1, gaps
- checker: alternate decide proofs of the same Nat goals

## Hard inputs
d,e

## Weave
Disjoint from holmbuar asymptotic_spine. Precedent: #506/#507 lean anchors.
