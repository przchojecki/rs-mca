---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The selected product-rank cofactor is nonzero at every guarded base-field source point in all eight repeated-BC O0b cell-11 common rows.
architecture: positive-433-1b-O0b-common-repeat-cell11
atom_or_cell: repeated-BC O0b cell-11 selected-cofactor chart boundary
quantifier: all eight epsilon/sign guarded common-source rows
projection_and_unit: source tower x-roots, not distinct bad slopes
claimed_bound: 0 guarded selected-cofactor boundary points
status: PROVED
impact: ROUTE_CUT
falsifier: a guarded base-field common-source point on the selected-cofactor zero fiber, a missing source row, or a pinned-blob mismatch
replay: python3 experimental/data/certificates/kb-mca-v4-433-1b-o0b-cell11-cofactor-boundary-v1/verify.py --source-root /path/to/rs-mca-prize-dag
---

# Repeated-BC `O0b` cell-11 selected-cofactor chart cut

The exact degree-seven product-rank cofactor is substituted into each finite
symmetric tower algebra and normed to `F_2130706433(x)`.  Over the base field,
the BC- norm has only `x=1` as a root and the BC+ norm has only `x=-1`.
Registered tower guards vanish at both roots.  The pinned chart-coverage unit
ideals independently prove that no original guarded common-source point lies
on `x*y*(x-1)*(x+1)=0`.  Hence the selected-cofactor zero fiber has no
guarded base-field source point.

The irreducible factor profiles are `(degree 2)^2 (degree 1)^10` for BC- and
`(degree 3)^2 (degree 2)^4 (degree 1)^4` for BC+.  This is a finite-field
chart cut for the exact second-moment ledger, not a statement that the
cofactor boundary is empty over extension fields.

The certificate pins two PROVED nodes and seven evidence files at
`AllenGrahamHart/rs-mca-prize-dag@1f757c1a1af9`.  It does not cover later
guards introduced by missing-record reconstruction or outside resultants,
cell 14, orientation, slope allocation, independent review, K3, or the
KoalaBear row.  Ledger movement is zero.

## Provenance annotation

The `provenance.commit` hash is the durable source pin.  It is published on
`codex/full-prize-resolution-v12-20260807` and need not yet be an ancestor of
source `master`.  Replay from a checkout containing the pinned commit.
