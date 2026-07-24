# M31 flatness-keystone Lean correspondence

## Source statement

The proof source is
`experimental/notes/thresholds/m31_flatness_keystone_constant_shift_obstruction.md`.
Its symbolic theorem says that pairwise disjoint degree-`d` blocks with locators
`H(X)-lambda_i` have selection-independent locator coefficients through every
prefix depth below `d`.  The explicit specialization uses `d=33`, depth `32`,
30 intact blocks, 14 selected blocks, and a 17-point core.

## Declared results

| Lean declaration | Source claim |
|---|---|
| `parameter_arithmetic` | `1024-2=1022`, `17+14*33=479`, `32+1=33`, and the 31-block base-domain count. |
| `degree_gap_exact` | The selection-dependent tail has degree at most `446`, while the first observed boundary is degree `447`. |
| `family_size_exact` | `binomial(30,14)=145422675`. |
| `ambient_average_exact` | The exact values of `p^32`, `binomial(1022,479)`, quotient `3614119`, nonzero remainder, and ceiling average `3614120`. |
| `obstruction_margins_exact` | The four exact budget/average margins printed in the note. |
| `packet_arithmetic` | The final arithmetic obstruction: the certified family exceeds eight budgets and forty ceiling averages. |

## Kernel and axiom census

The package imports `Std` only.  It contains no `axiom`, `sorry`, `admit`, or
Mathlib dependency.  Each theorem is followed by `#print axioms`.

`native_decide` is used in all six declared results.  It certifies closed
natural-number computations only.  The finite-field coset construction and the
polynomial locator-prefix theorem remain source proofs checked independently by
the deterministic packet verifier; they are not promoted as Lean theorems here.
