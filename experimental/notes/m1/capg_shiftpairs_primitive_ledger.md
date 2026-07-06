# Primitive Shift-Pair Toy Ledger

## Claim

The canonical finite object in `thm:capg-second-moment`,
`sp_w(e;D')`, is exactly enumerable on small multiplicative-subgroup rows.  In
the recorded rows, the quotient prototype mass of `rem:capg-prototype` is
present and is classified as common pullback mass; after removing such common
pullback pairs, some toy rows still have primitive residue.

## Status

EXPERIMENTAL / AUDIT.  This is a finite toy ledger for
`prob:capg-shiftpairs` and `prob:capg-active-shiftpairs`; it is not an
asymptotic primitive shift-pair bound, not a deployed adjacent-row constant,
and not a resolution of `prob:band`.

## Pinned Statements

- `thm:capg-second-moment`, `experimental/cap25_cap_v13_raw.tex`, lines
  9575-9588: defines `sp_w(e;D')` as ordered disjoint monic split locator
  pairs with `deg(A-B) <= e-w-1`.
- `rem:capg-prototype`, lines 9649-9665: the full-fiber binomial prototype
  gives `sp_w(w+1;mu_n) >= n/(w+1)(n/(w+1)-1)` when `(w+1)|n`, and calls a
  shift pair primitive if it is not a pullback at any scale `c>=2`.
- `prob:capg-shiftpairs`, lines 9667-9679: asks for a bound on the primitive
  part of `sp_w(e;D')` for multiplicative cosets.
- `prob:capg-active-shiftpairs`, lines 9926-9932: restates the active input as
  primitive shift-pair control after quotient-pullback pairs are removed.

## Finite Rows

The count is ordered, matching the prototype expression.  A pullback pair means
both root sets are unions of complete fibers for at least one common divisor
scale `c>=2` of `n`.

| row | w | e | sp pairs | pullback | primitive | prototype |
|---|---:|---:|---:|---:|---:|---:|
| `oracle_f5_mu4_w1_e2` | 1 | 2 | 2 | 2 | 0 | 2 |
| `f17_mu16_w1_e2` | 1 | 2 | 728 | 56 | 672 | 56 |
| `f17_mu16_w2_e3` | 2 | 3 | 704 | 0 | 704 | n/a |
| `f17_mu16_w3_e4` | 3 | 4 | 252 | 28 | 224 | 12 |
| `f17_mu16_w2_e4` | 2 | 4 | 2988 | 28 | 2960 | n/a |
| `f17_mu16_minus_one_w1_e2` | 1 | 2 | 546 | 42 | 504 | n/a |
| `f31_mu15_w2_e3` | 2 | 3 | 110 | 20 | 90 | 20 |
| `f31_mu15_w4_e5` | 4 | 5 | 6 | 6 | 0 | 6 |
| `f97_mu16_w2_e3` | 2 | 3 | 32 | 0 | 32 | n/a |
| `f97_mu16_w3_e4` | 3 | 4 | 12 | 12 | 0 | 12 |

The oracle row is hand-sized: `F_5^*` has two opposite pairs, they are the two
fibers of the square map, and the ordered count is exactly `2`.

## Proof Idea Or Experiment

The generator builds `mu_n` inside `F_p`, enumerates every size-`e` support in
`D'`, forms its monic locator polynomial, and buckets supports by the top `w`
non-leading coefficients.  Ordered disjoint pairs in the same bucket are
exactly the pairs with `deg(A-B) <= e-w-1`.  The script then marks a pair as
pullback-explained when both supports are periodic at a common divisor scale.

The independent checker recomputes the same rows by power-sum signatures
`sum x^j`, `1<=j<=w`, and tests periodicity by explicit multiplication by the
subgroup element of each candidate scale.  The recorded certificate must match
this second enumeration exactly.

## Ledger Impact

This supplies a small exact table for the live primitive shift-pair input.  It
confirms the printed quotient prototype on applicable toy rows and records that
primitive residue can remain after common quotient-pullback deletion.  It does
not estimate the polynomial factor requested in `prob:capg-shiftpairs`.

## Deviations

The audit is restricted to small prime-field subgroup rows and one deleted
support row `D'=D\{1}`.  It does not enumerate all deleted sets `R`, does not
cover extension rows, and does not test the finite constants required by
`cor:capg-adjacent-pairs`.

## Non-Overlap

This does not redo the finite-testability map, Q/R1 input audit,
split-pencil floor audit, adjacent-pair margin audit, prefix-collision ledgers,
annulus packets, or earlier flatness enumerators.  It targets only the
currently named primitive shift-pair residue.

## Self-Red-Team

An adversarial reviewer could object that the ledger is only a small-row count
and gives no bound of the kind requested in `prob:capg-shiftpairs`.  That is
correct.  The contribution is the exact separation of pullback and primitive
mass on finite rows, not a claim that the active primitive input is solved.

## Reproducibility

```text
py -3.13 experimental/scripts/verify_capg_shiftpairs_primitive_ledger.py --emit-defaults --check
py -3.13 experimental/scripts/verify_capg_shiftpairs_primitive_ledger_check.py --check
```
