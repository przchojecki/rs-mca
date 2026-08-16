---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_commit: 2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804
status: PROVED_RANK11_REPAIR_AND_RANK12_ROUTE_CUT
active_v4_ledger_movement: 0
---

# Contract

This packet supersedes the unsubmitted candidate
`d01c546f4dca70e256c18c142873821b3bb48ab5`.

The earlier candidate's heavy-core dichotomy, shortening semantics, recurrence,
and rank-one endpoint arithmetic were correct, but its induction omitted one
ambient-dimension case: a rank drop before `K=s` can create a lower-rank family
before the endpoint row.  The new uniform rank-one weighted-line theorem closes
that gap for every shortened dimension and makes the rank-eleven payment
history-uniform.

The packet then attacks affine error rank twelve.  It proves a dense-pair-core
Cauchy bound, installs exact descending barriers through ranks eleven to three,
and emits an exact rank-two/rank-one residual.

## Exact outputs

- complete affine error rank eleven: paid;
- uniform rank-one cap over all shortened rows: `4,070,947`;
- rank-twelve descendant: at least `8,681,730` slopes, rank at most two;
- full rank-two endpoint low family: at least `8,550,040` slopes;
- pair types: between `9` and `15`;
- deficiency-one pair types: at least `3`;
- independent-capacity excess left to remove: `279,911`;
- rank twelve: not paid;
- KoalaBear: not closed;
- active-v4 ledger movement: `0`.

All loads count distinct finite affine slopes.  Complete scalar agreement
domains—not coordinate-swapped supports—are used for shortening.
