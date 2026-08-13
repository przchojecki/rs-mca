---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Missing BE and CF are impossible on every deployed off-guard repeated-BC O0b cell-11 source value.
architecture: positive-433-1b-O0b-common-repeat-cell11
atom_or_cell: repeated-BC O0b cell-11 colored missing records
quantifier: all eight source towers and both colored missing records on the registered rational open
projection_and_unit: source consistency cases, not distinct bad slopes
claimed_bound: 0 surviving colored source cases out of 16
status: PROVED
impact: ROUTE_CUT
falsifier: a deployed non-guard root of either exact source-algebra norm, a missing source tower, or a pinned-blob mismatch
replay: python3 experimental/data/certificates/kb-mca-v4-433-1b-o0b-cell11-colored-offguard-v1/verify.py --source-root /path/to/rs-mca-prize-dag
---

# Repeated-BC `O0b` cell-11 colored off-guard exclusion

The common-kernel reconstruction gives the missing endpoint product `q` and
squared sum `s^2`.  If `BE` is missing, then `e=q/b` and
`(b+q/b)^2=s^2` is necessary; the `CF` identity is symmetric.  Exact
source-algebra norms test these identities before residual matching.

All 16 cases are units on the deployed rational open.  For `BC-`, the only
base-field norm roots are `x=0,1`; for `BC+`, they are `x=0,-1`.  Every root
is a registered chart guard, so there is no deployed off-guard source point
with missing `BE` or `CF`.

The certificate pins one PROVED node and four evidence files at
`AllenGrahamHart/rs-mca-prize-dag@96868562394e`.  It does not cover guard or
selected-cofactor boundaries, cell 14, orientation, slope allocation,
independent review, K3, or the KoalaBear row.  Ledger movement is zero.

## Provenance annotation

The `provenance.commit` hash is the durable source pin.  It is published on
`codex/full-prize-resolution-v12-20260807` and need not yet be an ancestor of
source `master`.  Replay from a checkout containing the pinned commit.

