---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The complete positive 433-1b to O0a raw workboard is empty in all 15 role cells, 1575 labels, and 25200 signed principal systems; the global rank-drop branch is empty separately.
architecture: positive-433-1b-coordinate-guarded-route
partition_digest: sha256:82df776b06b375e9bee6fcc77aead1ebca4594028fa2e51df6318422a9d2f9bb
atom_or_cell: complete coordinate-positive 433-1b to O0a raw workboard
quantifier: every raw principal system and the complementary global rank-drop branch in the declared route
projection_and_unit: raw workboard labels and signed principal systems, not distinct bad slopes
claimed_bound: 0 surviving raw systems out of 25200
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: an omitted or multiply owned role cell, a failed owner packet, an invalid cell-9-to-cell-10 transport, or a surviving guarded raw system
replay: python3 experimental/data/certificates/kb-mca-v4-433-1b-raw-workboard-close-v1/verify.py --source-root /path/to/rs-mca-prize-dag
---

# Complete raw `433-1b -> O0a` workboard exclusion

This certificate closes the exported raw workboard, including the previously
implicit cell-10 step. The exact `B<->C` duplicate-role map fixes the `BC+`
singleton, flips the second source sign, gauges the outside records, and
bijects all 105 labels and 1,680 signed principal systems in cells 9 and 10.

The complete role-cell partition is

```text
[0] | [1,2] | [3,6] | [4,7] | [5,8] | [9,10] | [11] | [12,13] | [14].
```

These nine proved owner packets cover all 15 role cells disjointly. Each cell
has 105 raw labels and 16 signed principal systems per label, giving exactly
1,575 labels and 25,200 systems. The separate global product-rank-drop theorem
excludes the complementary branch.

The JSON certificate pins the three new aggregate nodes, their verifiers, and
their hostile audits in the public campaign repository at commit
`8df0903391a228eed6e24398fca9d40d72d546cf`.

This is not K3 closure. It does not prove exhaustive balanced-core routing,
convert raw labels to distinct affine slopes, pay the eleven other positive
routes, assemble source-cover orientations, or move a row ledger value.

Replay the certificate and its ten pinned blobs with:

```bash
python3 experimental/data/certificates/kb-mca-v4-433-1b-raw-workboard-close-v1/verify.py \
  --source-root /path/to/rs-mca-prize-dag
```
