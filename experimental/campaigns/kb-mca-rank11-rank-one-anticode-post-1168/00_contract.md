---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_commit: 6a5dcdae1591fc7f044eda6a942bfe178521a48c
status: PROVED_STRUCTURAL_ROUTER
active_v4_ledger_movement: 0
---

# Contract

This packet is a stacked successor to PR #1168 at exact parent
`6a5dcdae1591fc7f044eda6a942bfe178521a48c`. It attacks the first cross-pair joint left by that PR:
simultaneous compatibility of distinct minimizing-pair cores in the
post-near affine-error-rank-eleven branch.

The direct theorem classifies every family of actual minimizing pairs whose
coefficient matrices have pairwise rank distance at most one. Such a family
is forced into one of two geometries:

1. a fixed polynomial correction ray, paid by a new common-core-aware
   affine-ray count; or
2. a fixed two-vector multiplier times a correction space of dimension at
   most ten. Its affine-linear arrangement is paid by an exact `1031`-slope
   bound when proper, and otherwise emits a concrete positive-dimensional
   linear correction component.

A pair-core clique with pairwise intersection `K-1` is automatically in this
rank-one class by the Reed--Solomon two-dimensional common-zero bound.
Therefore maximal-overlap pair cliques are no longer an untyped rank-eleven
terminal.

## Quantifier

Uniform over the actual KoalaBear line field, every received pair, every
gauged post-near explanation flat of affine dimension at most ten, and every
selected family of distinct actual minimizing pairs satisfying the stated
pairwise rank-one condition.

## Projection

All counts remain counts of distinct affine slopes. A selected slope maps
injectively to its correction parameter because the slope is retained as the
first parameter coordinate.

## Exact impact

- fixed correction-ray branch: at most `8,147,918` slopes;
- proper rank-`r<=10` affine correction-space branch: at most
  `floor(C(n,r+1)/C(m,r+1)) <= 1,031` slopes;
- nonproper branch: an explicit nonempty positive-dimensional affine-linear
  intersection of `r+1` coordinate hyperplanes, source-bound to the existing
  positive-dimensional correction-component lane.

This is a structural router, not a rank-eleven payment and not a KoalaBear
closure.
