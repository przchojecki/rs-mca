# Pull request title

[MCA] Repair rank eleven and cut rank twelve to a saturated rank-two atlas

# Pull request body

## Summary

This is a one-commit successor to PR #1173 at exact parent
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

It supersedes the unsubmitted candidate
`d01c546f4dca70e256c18c142873821b3bb48ab5`.  The earlier candidate's
heavy-core dichotomy and endpoint arithmetic were sound, but its descent
induction omitted the possibility that an early rank drop creates a rank-one
family before the `K=1` endpoint.

This PR repairs that gap with a weighted projective-line theorem uniform over
all shortened dimensions.  For a rank-one direction polynomial, nonzero
coordinates become graph lines, nonuniversal zeros become vertical lines, and
the universal core is deleted.  An exact scan over all

```text
1 <= residual dimension j <= 1,048,576
```

gives the uniform bound

```text
rank-one slopes <= 4,070,947.
```

The corrected complete-core induction then forces `5,201,865` rank-one slopes
from any over-budget affine-error-rank-eleven line, with contradiction slack

```text
1,130,918.
```

Thus the complete affine-error-rank-eleven branch is paid, uniformly over all
shortening histories.

## Rank-twelve route cut

The PR also proves a dense-core pair-type theorem.  If low-margin pair cores
have size at least `h` and distinct cores intersect in at most `K-1`
coordinates, a Cauchy second-moment calculation bounds the number of pair
types.  Combining that bound with fixed-pair exception packing gives exact
direct barriers through ranks eleven to three.

Every over-budget affine-error-rank-twelve line therefore emits a source-bound
descendant with

```text
at least 8,681,730 slopes
direction dimension at most 2
ambient shortened dimension at least 4,280.
```

A rank-one descendant at this point is already excluded by the new uniform
rank-one theorem, so the immediate survivor has exact direction rank two.

If full rank two reaches the `K=2` row, the exact `T=1922` split gives

```text
high-margin slopes              131,690
low-margin slopes             8,550,040
represented pair types          9 to 15
deficiency-one pair types       at least 3
independent capacity          8,829,951
remaining cross-pair saving      279,912
```

If rank two drops earlier, the surviving rank-one descendant has at least
`558,412` slopes.  These are the two honest rank-twelve residuals.

## Scope

- affine error rank eleven: paid;
- rank-eleven proof made history-uniform;
- rank-twelve dense-core route: proved;
- affine error rank twelve: not paid;
- active-v4 ledger movement: `0`;
- KoalaBear closure: not claimed.

No unrelated local owners are summed.  Complete agreement domains are used
for shortening, minimizing pairs are refrozen after every shortening, and the
`279,911` value is only an independent-capacity excess—not a constructed
extremizer.

## Verification

- all `1,048,576` residual rank-one dimensions scanned;
- all deployed rank-eleven descent cells checked;
- all rank-twelve barrier cells checked;
- primary exact verifier: PASS;
- separate product/recurrence audit: PASS;
- weighted-line endpoint enumeration: PASS;
- small dense-core set-system controls: PASS;
- hostile mutations: rejected;
- Wolfram exact barrier and endpoint replay: PASS;
- manifest and file hashes: PASS;
- adversarial mathematics audit: GREEN for the stated repair and route;
- primary-literature sweep: no external theorem is load-bearing.

## Dependency and next theorem

This PR must integrate after #1173.

The first open implication is now precise.  At `K=2`, the remaining low family
is carried by at most fifteen affine pair types, at least three with core
deficiency one.  Independent fixed-pair capacities miss closure by only
`279,911` slopes.

The next theorem must couple the simultaneous ratio maps

```text
rho_e(x)=-(r_0(x)-a_e(x))/(r_1(x)-b_e(x))
```

and prove that the near-perfect two-fiber matchings cannot coexist unless the
pair matrices enter an already-paid rank-one anticode or rational-owner
geometry.  Pairwise Möbius/subgroup incidence alone is insufficient because
the cores are arbitrary subsets and the slope field is the sextic extension.

## Review boundary

- head repository: `scottdhughes/rs-mca`;
- head branch: `codex/kb-mca-rank11-repair-rank12-route-post-1173`;
- exact parent: `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.
