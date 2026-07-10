# Lean: prefix-rigidity packing / Johnson fiber cap instance

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only theorem instance.
No sorry, no mathlib.

## Object
Instance of prop:prefix-rigidity-full / eq:packing-fiber-cap on
(n,m,w,t) = (6,3,2,1):

```text
packingCap = binom(6,3) / V_1 = 20 / 10 = 2
fiberToy * V_t ≤ totalSets    (2 * 10 ≤ 20)
johnsonMin = w+1 = 3
```

## Build
```
cd experimental/lean/anticode_packing && lake build
# ✔ Built AnticodePacking
```

## Dual routes
- generator: Lean kernel `native_decide` on binom / V_t / packingCap inequalities
- checker: alternate `decide` proofs of the same Nat goals

## Nonclaims
- Toy instance only; not a formalization of the general prefix-rigidity proof.
- Does not claim an anticode theorem beyond the paper's Johnson packing form.

## Weave
Complements moving-root / deployed-bracket Lean anchors with the packing fiber cap.
