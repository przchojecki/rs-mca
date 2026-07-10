# lean: first-match atlas partition Nat identity (hard input a)

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only Nat anchors. No sorry, no mathlib.

## Build
```
cd experimental/lean/first_match_partition && lake build
# ✔ Built FirstMatchPartition
```

## Dual routes
- generator: Lean kernel native_decide on sum of bucket sizes = total
- checker: alternate decide proofs of the same Nat equalities

## Hard inputs
a

## Weave
Disjoint from holmbuar asymptotic_spine. Precedent: #506/#507 lean anchors.
