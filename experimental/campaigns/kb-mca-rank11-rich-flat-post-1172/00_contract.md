---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_pr: 1172
parent_commit: 193b7bf99a5cc7ccea042f25677e698d9f988eee
status: PROVED_DIRECT_BRANCH_PAYMENT_AND_ROUTE_CUT
active_v4_ledger_movement: 0
---

# Contract

This packet is a stacked successor to PR #1172 at exact parent
`193b7bf99a5cc7ccea042f25677e698d9f988eee`.

It anchors one actual low-margin record and partitions every other represented
minimizing pair by the rank-one or rank-two row space of its coefficient-matrix
difference from the anchor.  A row space with no heavy proper annihilator flat
owns many disjoint ordered coordinate bases; this bounds the number of such row
spaces.  Rank-one groups are paid by PR #1171's common-core-aware ray theorem,
and rank-two groups are paid by a dimension-two sub-square interleaved-list
cap.

At the optimized cutoff `tau=1547`, every `h=42452`-transverse family is paid:

```text
low branch       206,103,676,872,450,147
high tail         68,875,044,016,173,272
near add-back                    134,944
------------------------------------------------
total            274,978,720,888,758,363
slack                  2,007,222,636,724
```

Therefore every over-budget line emits an actual represented row space `U` of
rank one or two and a strictly larger direction subspace `W` such that:

- `U<W<=C'`;
- `dim W>=dim U+1`;
- every polynomial in `W` vanishes on at least `42,453` common actual
  coordinates contained in the anchor's good support.

In the rank-two case the original plane still has the stronger anchor-overlap
floor `131,850`, while its extension has dimension at least three and common
factor degree at least `42,453`.

## Quantifier

Uniform over the deployed sextic KoalaBear line field, every received pair,
every selected post-near affine-error-rank-eleven family, every explanation
direction space of dimension at most ten, and the fixed actual minimizing-pair
selection inherited from the predecessor compiler.

## Projection

All quantities count distinct finite affine slopes.  Pair types are grouped by
the unique row space of their coefficient-matrix difference from one actual
anchor pair.  These groups are disjoint; no uncontrolled sum of overlapping
local certificates is used.

## Exact impact

- pays the complete anchored `42,452`-transverse row-space branch;
- replaces the generic rank-two edge terminal by a dimension/core tradeoff:
  larger direction dimension and at least `42,453` common factor coordinates;
- makes zero active-v4 ledger movement;
- does not pay rank eleven or close KoalaBear.
