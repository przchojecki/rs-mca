# Correspondence — M31 T32 skeleton flatness keystone

## Source claim

The proof source is
`experimental/notes/thresholds/m31_t32_skeleton_flatness_keystone.md`.
For a fixed canonical remainder, the polynomial argument reduces equality of the
first 32 nonleading locator coefficients to equality of the selector sigma sum.
The finite selector atlas then gives the sharp cap 3,432.

## Lean declarations

`M31FlatnessKeystone.SelectorAtlas.selector_relation_atlas_exact` checks:

- both 234,375-entry meet-in-the-middle half tables and their injectivity;
- the exact intersection: zero plus 18 nonzero signed relations, represented by
  nine canonical rows;
- all nine modular relation equalities;
- relation realization counts summing to 68,896 edges;
- 137,792 pairwise distinct endpoints, hence a matching;
- nontrivial collision maximum 482;
- binomial-pattern maximum and selector cap 3,432.

`M31FlatnessKeystone.quotient_average_exact` checks the exact floor and ceiling
3,614,119 and 3,614,120 for `binom(1022,479)/p^32`.

`M31FlatnessKeystone.keystone_threshold_arithmetic` checks the 1,054- and
4,889-remainder thresholds, the 4,888-remainder budget margin, and the cited
3,440 integrated floor arithmetic.

## Trust boundary

The package imports only `Std`; it has no Mathlib dependency.  The finite atlas
and large integer calculations use `native_decide`.  The general polynomial
factorization, degree comparison, canonical-remainder decomposition, and the
inference from the checked matching summary to the sharp cap are written in the
proof note and must be audited against the declarations above.  No row theorem,
first-match survivor, received word, or codeword projection is formalized.
