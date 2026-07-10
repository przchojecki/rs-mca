# Lean: listUnion length laws (∀)

## Status
GENERAL ∀-lemmas by induction. lake PASS. Hard input (a).

## Theorems
```
listUnion_length_le (a b) : (listUnion a b).length ≤ a.length + b.length
listUnion_length_eq_of_disjoint (a b) (nodup a) (disjoint a b) :
  (listUnion a b).length = a.length + b.length
```
Proof: foldl length invariant; equality adds disjoint+nodup so every element of a is newly appended.

## unfinished-goals=0; extra-axioms=0
