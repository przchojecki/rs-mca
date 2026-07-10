# Lean: second-moment identity for prefix fibers

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only theorem instance.
No sorry, no mathlib.

## Object
Instance of lem:second-moment-identity: for Q=[3,2,1],
∑ Q(s)² = 14 = ordered common-prefix pairs; and SP ≤ Qmax·total (14 ≤ 18).

## Build
```
cd experimental/lean/second_moment_identity && lake build
# ✔ Built SecondMomentIdentity
```

## Dual routes
- generator: Lean kernel native_decide on sumSq fold and pair expansion
- checker: alternate decide proofs of the same Nat goals

## Nonclaims
- Toy fiber sizes only; not a formalization of the general lemma proof.
