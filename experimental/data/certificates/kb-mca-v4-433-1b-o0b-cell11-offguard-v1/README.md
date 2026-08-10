---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: All 720 repeated-BC O0b cell-11 DE+/DF+/EF representative systems are empty at every deployed off-guard source value.
architecture: positive-433-1b-O0b-common-repeat-cell11
atom_or_cell: repeated-BC O0b cell-11 uncolored representative systems
quantifier: every deployed source value on the registered nonzero-guard chart
projection_and_unit: uncolored representative systems, not distinct bad slopes
claimed_bound: 0 surviving endpoints out of 720 representative systems
status: PROVED
impact: ROUTE_CUT
falsifier: a non-guard deployed source value at which all three paired-product Sylvester matrices are singular, an omitted representative, or a pinned-blob mismatch
replay: python3 experimental/data/certificates/kb-mca-v4-433-1b-o0b-cell11-offguard-v1/verify.py --source-root /path/to/rs-mca-prize-dag
---

# Repeated-BC `O0b` cell-11 deployed off-guard exclusion

This packet exports a theorem that is separate from the closed
`433-1b -> O0a` raw workboard.  It covers the repeated-BC `O0b` cell-11
systems with missing representative `DE+`, `DF+`, or `EF`, both outside
signs, all 15 residual matchings, and all eight source towers.  The exact
census is `8 * 3 * 2 * 15 = 720` systems.

For each system, an exact quartic resultant is normed down the symmetric
source tower to the deployed base field.  Of the 720 systems, 288 have no
off-guard deployed root.  The other 432 produce 1,584 exceptional-root
occurrences over 126 base values.  At every occurrence, all three equation
pairs are replayed and at least one Sylvester matrix has full rank.  Thus no
common endpoint survives on the registered nonzero-guard chart.

The certificate pins two PROVED campaign nodes and 19 source artifacts at
`AllenGrahamHart/rs-mca-prize-dag@81f218e38285`.  Its verifier independently
checks the source-blob custody and the aggregate norm/replay census.

This is a route cut, not K3 closure.  It does not cover missing `BE/CF`, any
registered guard or selected-cofactor boundary, cell 14, source orientation,
distinct-slope allocation, or independent review.  It moves no row ledger
value.

## Provenance annotation

The `provenance.commit` hash is the durable source pin.  It is published on
the source repository branch
`codex/full-prize-resolution-v12-20260807`; it need not yet be an ancestor of
source `master` when this packet first lands.  Replay from a checkout that
contains the pinned commit and do not infer proof status from the branch name.
