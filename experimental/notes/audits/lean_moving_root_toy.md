# Lean: moving-root bound on an explicit F_5 pencil

## Status
EXPERIMENTAL / AUDIT. Kernel-checked Lean 4.14 core-only theorem instance.
No sorry, no mathlib.

## Object
Instance of prop:split-pencil-payment / eq:moving-root-bound on
A = X², B = X over F_5 with G = X, g = 1, h = 1, n = 5:

```text
nWithH ≤ floor((n − g) / h)    i.e.  4 ≤ 4
```

Parameters enumerated in-kernel; root counts proved by `native_decide` /
`decide` (dual routes).

## Build
```
cd experimental/lean/moving_root_toy && lake build
# ✔ Built MovingRootToy
```

## Dual routes
- generator: Lean kernel `native_decide` on enumerated countMoving / nWithH / bound
- checker: alternate `decide` proofs of the same Nat goals

## Nonclaims
- Not a formalization of the general prop:split-pencil-payment proof.
- Toy field only; anchors the incidence shape on one explicit pencil.

## Weave
Complements Nat-only deployed brackets / first-match partition anchors with a
theorem-instance (enumeration + inequality), not bare table constants.
