# Lean: general ∑N² ≤ max·∑N (∀)

## Status
EXPERIMENTAL / AUDIT. lake build PASS. **General ∀-lemma by induction.**
**Hard input:** (b)

## Headline
```
theorem sumSq_le_max_mul_sum (l : List Nat) :
    sumSq l ≤ maxList l * sumList l
```
Proof: induction on l; x² ≤ M·x and maxList xs ≤ M lift the IH.

## Dual routes
- generator: structural induction + Nat.mul_le_mul_right / Nat.le_max_*
- checker: toy native_decide instances (#557 [6,3,3], tight [8])

## Nonclaims
q=2 form only; not higher-moment sandwich.
unfinished-goals=0; extra-axioms=0
