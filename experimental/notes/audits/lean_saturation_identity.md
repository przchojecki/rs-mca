# Lean: exact saturation identity on F_5 (K=1)

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only theorem instance.
No sorry, no mathlib.

## Object
Instance of thm:saturation (grande_finale):
Cen(U;m) = ∑_c binom(s_c(U), m) on U=(0,0,0,1,1) over F_5, K=1, m=2:
LHS (enumerated pairs) = RHS (∑ binom(s_c,2)) = 4.

## Build
```
cd experimental/lean/saturation_identity && lake build
# ✔ Built SaturationIdentity
```

## Dual routes
- generator: Lean kernel native_decide on agreement sizes + pair enumeration
- checker: alternate decide proofs of the same Nat goals

## Nonclaims
- Toy: constants only (K=1), not general RS; not the general thm proof.
- Disjoint from experimental/lean/saturation_toys (W24 bare binoms).
