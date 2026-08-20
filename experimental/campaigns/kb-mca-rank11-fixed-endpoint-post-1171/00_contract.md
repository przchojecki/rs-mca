---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_pr: 1171
parent_commit: a3fc2d5aea86577cd50d8b95b6eb2155d4d940f6
status: PROVED_DIRECT_BRANCH_PAYMENT_AND_ROUTE_CUT
active_v4_ledger_movement: 0
---

# Contract

This packet is a stacked successor to PR #1171 at exact parent
`a3fc2d5aea86577cd50d8b95b6eb2155d4d940f6`.  It completes the rank-one
minimizing-pair anticode branch left partially routed there.

At the fixed cutoff `tau=439`, split the post-near affine-error-rank-eleven
family into support margins `theta<=439` and `theta>=440`.  If the coefficient
matrices of all low-margin minimizing pair types have pairwise rank distance at
most one, PR #1171 puts them in one of two geometries.

1. The fixed-right-factor geometry is paid by #1171's common-core-aware ray
   cap `8,147,918`.
2. The fixed-left-factor geometry has one nonzero linear combination of the
   two endpoints fixed.  On its complete agreement set `G`, the varying
   endpoint is one ordinary affine Reed--Solomon list.  Same-support pair
   noncontainment forces every nonexceptional owning slope to use a coordinate
   outside `G`, which injects the pair's slopes into `D\\G`.

The exact fixed-left bound at `tau=439` is

```text
low rank-one branch       32,215,263,489,919,749
high-margin tail         242,314,927,584,173,240
near-rational add-back               134,944
------------------------------------------------
total                    274,530,191,074,227,933
slack                        450,537,037,167,154
```

Thus every over-budget line contains two low-margin minimizing pair types with
coefficient-matrix difference of rank two.  Their complete pair cores each
have size at least `1,115,609`, hence meet in at least `134,066` coordinates.
The two independent endpoint-difference polynomials therefore have a common
evaluation-root factor of degree at least `134,066`.

## Quantifier

Uniform over the deployed sextic KoalaBear line field, every received pair,
every gauged post-near explanation flat of affine dimension at most ten, and
every actual minimizing-pair selection used by the parent support-margin
compiler.

## Projection

All counts are distinct finite affine slopes.  The endpoint row operation
induces an injective projective map on the original affine challenge set.  At
most one slope maps to the fixed-endpoint projective direction and is reserved
explicitly.  Every other slope is injected, for its fixed pair type, into one
coordinate outside the common endpoint agreement set.

## Exact impact

- pays the complete low-margin rank-one anticode branch at `tau=439`;
- sharpens the successor terminal to a rank-two pair difference with a common
  factor of degree at least `134,066`;
- makes no active-v4 ledger movement and does not close rank eleven or
  KoalaBear.
