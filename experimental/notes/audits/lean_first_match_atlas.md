# Lean: first-match occupancy atlas (W44-FIX structural)

## Status
EXPERIMENTAL / AUDIT. lake build PASS.
**Hard input:** (a) witness-exhaustive first-match atlas

## Labels (rule 1b)
```
3744:\label{thm:canonical-partial-occupancy-atlas}
3609:\label{thm:exact-partial-occupancy}
```

## Fix
|Z_λ°|≤|Ω_λ| is STRUCTURAL: Z from firstOccurrences(slopesOf(Ω)) via
slopeOf on cells — no hand-declared constant slope lists.
Deliberate collisions: Ω_A slopes [0,0] ⇒ |ZAraw|=1 < 2.

## Object
Ω sizes (2,4,4) sum=10; ZAraw/B/C lengths (1,3,3) all < |Ω|;
cross-slice Z° sizes (1,2,2); sumZ=|unionZ|=5≤10.

## Dual routes
- generator: native_decide on slopeOf/firstOccurrences/filterNotIn
- checker: decide proofs of the same Nat goals

## Nonclaims
Toy occupancy + explicit slopeOf; not full RS witness geometry.
