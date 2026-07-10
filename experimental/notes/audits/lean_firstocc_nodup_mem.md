# Lean: firstOccurrences mem + nodup (∀)

## Status
GENERAL ∀-lemmas by induction. lake PASS. Hard input (a).

## Theorems
```
firstOccurrences_mem (l x) : mem x (firstOccurrences l) = mem x l
firstOccurrences_nodup (l) : nodup (firstOccurrences l) = true
```
Proof: acc-general mem_foldl_step / nodup_foldl_step by List induction.

## unfinished-goals=0; extra-axioms=0
