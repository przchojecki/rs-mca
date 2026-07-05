# Lean Anchor And Fiber Triage

## Claim

The `towards_prize` Lean package now includes finite arithmetic anchors for
selected sparse mutual, EMCA, and identity-prefix rows. The Paper D
`Fiber.lean` skeleton is triaged by proof dependency rather than silently
closing a statement with an unreliable proof.

## Status

PROVED for the finite arithmetic anchors. AUDIT for the `Fiber.lean` triage.

## Parameters

- Lean package: `experimental/lean/towards_prize`.
- Anchors: `(7,6,3,2)->sigma_C=7`, `(5,4,1,2)->sigma_C=3`, the `(7,6,3)`
  EMCA sparsify rows, and `C(16,9)=11440`.
- Fiber skeleton: `experimental/lean/cs25_cap_v12/cs25_cap_v12/Fiber.lean`.

## Existing Paper Dependency

The anchors map finite certificate numerators used by `towards-prize.tex`. The
Fiber triage concerns the Paper D v12 map-smooth fiber inputs consumed by the
universal cap formalization.

## Proof Idea Or Experiment

The anchors are kernel-checked finite arithmetic statements in
`TowardsPrize.FiniteAnchors`, with a map in `CERTIFICATION_MAP.md`. The full
enumeration semantics stay with the Python certificate verifiers.

For `Fiber.lean`, the tractable entry point is `lem_fiber_ii`: it is the
specialized multiplicative-coset construction and should be attacked before the
map-smooth generalization. `lem_phi_fiber_ii` then needs the divisibility-free
map-smooth version of the same locator-fiber construction. `thm_phi_cap` should
be closed only after the previous lemma supplies the exact `HasList` input in
the form consumed by `RSCap.universal_cap_of_fiber_list`.

## Ledger Impact

The package gains a theorem-by-theorem map for verifier-backed finite rows while
keeping proof status separated: Lean checks arithmetic anchors; Python verifiers
check exhaustive RS/MCA/list semantics.

## Constants

The new constants are `7`, `3`, `max(1,0)=1`, `max(2,1)=2`, `max(7,7)=7`, and
`Nat.choose 16 9 = 11440`.

## Reproducibility

```powershell
cd experimental/lean/towards_prize
lake build
```

Trust-placeholder sweep for the new anchors:

```powershell
rg -n "\b(sorry|admit|native_decide|ofReduceBool)\b" experimental/lean/towards_prize/TowardsPrize.lean
```

## Non-Claims

This does not close the three `Fiber.lean` skeleton theorems. It does not claim
Lean has proved full sparse-census or EMCA-census exhaustiveness.
