# Lean: general firstOccurrences length bound (∀)

## Status
EXPERIMENTAL / AUDIT. lake build PASS. **General ∀-lemma by induction.**
**Hard input:** (a)

## Headline
```
theorem firstOccurrences_length_le (l : List Nat) :
    (firstOccurrences l).length ≤ l.length
```
Proof: invariant foldl_step_length_le by induction on l; step grows length by ≤1.

## Dual routes
- generator: structural induction (List.rec / induction … with)
- checker: toy native_decide instances (collision lists)

## Nonclaims
Does not prove full PO6 ray geometry; formalizes the dedup injectivity core.
unfinished-goals=0; extra-axioms=0
