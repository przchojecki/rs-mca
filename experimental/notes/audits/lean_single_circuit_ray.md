# Lean: single MDS-circuit ray compiler instance

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only theorem instance.
No sorry, no mathlib.

## Object
Instance of thm:single-mds-circuit-ray (RC_circ) on R=3, |U|=4, t=2:

```text
|Z| ≤ binom(R+1, 2) = C(4,2) = 6
zSize = 4 ≤ 6
nPairs = |{(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)}| = 6 = circuitBound
t < R
```

## Build
```
cd experimental/lean/single_circuit_ray && lake build
# ✔ Built SingleCircuitRay
```

## Dual routes
- generator: Lean kernel `native_decide` on binom / pair enumeration / |Z|≤bound
- checker: alternate `decide` proofs of the same Nat goals

## Nonclaims
- Toy instance only; not a formalization of the general circuit-ray proof.
- Pair list encodes the injection codomain size, not a full RS syndrome line.

## Weave
Second proved compiler variant in-kernel (complements moving-root #537).
