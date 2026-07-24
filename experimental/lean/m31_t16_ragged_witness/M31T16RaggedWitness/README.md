# M31 depth-32 T16-completeness refutation

Two independent support-level refutations of universal depth-32 T16 alignment on
the pinned Mersenne-31 quotient profile.  The package is stdlib-only and depends
only on the upstream `experimental/lean/m31_quotient_t16_mixing_floor/` package
for the frozen domain machinery.

## Explicit ragged witness

`RaggedWitness.lean` constructs two valid 479-supports from a 287-point common
core and twenty-four opposite pairs of intact T8 half-classes.  The exchange
sets have 192 points each.  The theorem

```text
M31T16RaggedWitness.RaggedWitness.explicit_ragged_collision
```

checks directly from the 479 roots that

```text
deficiency                    = 192,
first 39 locator coefficients = equal,
coefficient 40                = different,
first 32 coefficients         = the printed common target.
```

The companion theorem

```text
M31T16RaggedWitness.RaggedWitness.t16_class_five_is_partial_on_both_sides
```

checks the promised ragged class.  In intact T16 class 5, the anchor-only points
are exactly the eight-point T8 half with representative 5, while the
neighbor-only points are the opposite eight-point T8 half with representative
251.  Neither difference is a union of intact T16 classes.

The mechanism theorem

```text
M31T16RaggedWitness.RaggedWitness.signed_t8_relation_exact
```

checks the 24 paired half-classes, opposite T8 parameters, and the vanishing
first and third odd parameter moments.  Direct locator computation, rather than
this mechanism alone, validates the witness.

## Independent counting refutation

`CountingRefutation.lean` checks the finite deployed class census and exact
arithmetic behind a separate existence proof.  Let `Omega` be the 479-supports
whose occupancy in every intact T16 class lies in `1,...,15`.  The union bound

```text
|Omega| >= C(1022,479)
           - 62 * (C(1006,479) + C(1006,463))
```

has ceiling quotient `3,604,924` by `p^32`.  One depth-32 fiber therefore has
more than 1022 such supports.  Pairwise deficiency 33 would give rational Gram
matrix `33 I + 446 J`, forcing at most 1022 incidence vectors.  Newton
identities exclude deficiency at most 32, so a ragged collision with
`34 <= e <= 479` exists independently of the printed witness.

## Validation boundary

All ten theorems use `native_decide` except
`depth_and_rank_boundary_arithmetic`, which uses ordinary `decide`.  Every
theorem has a `#print axioms` census.  The package is stdlib-only.

The explicit witness theorem checks support validity, deficiency, locator
prefixes, and the partial class in Lean.  The counting module checks its finite
class census and large integer gates but does not formalize the union-bound,
pigeonhole, Newton, or rational linear-algebra argument.  Neither module makes a
received-word, codeword, ray, slope, or row-ledger claim.
