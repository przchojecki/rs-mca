---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The deployed positive 433-1b to O0a route is empty in source role cell 3.
architecture: positive-433-1b-coordinate-guarded-route
partition_digest: sha256:b2083fd9336497c67b8394cb79c7a6a6d24e7fc3a15d84203dcb092c2dedf896
atom_or_cell: coordinate-positive 433-1b source role cell 3
quantifier: every common rank-drop row and every principal missing-record/matching/sign/lane system in the declared cell
projection_and_unit: raw workboard systems, not distinct bad slopes
claimed_bound: 0 surviving systems out of 1680 principal systems plus the common rank-drop branch
status: PROVED
impact: LOCAL_ONLY
falsifier: a surviving common rank-drop row, a surviving principal system, an omitted system, or an overlapping supplier payment
replay: tools/ramguard modal -- modal run experiments/prize_resolution/modal_verifier_replay.py --match rate_half_kb_m2_r4_coordinate_positive_433_1b_cell3
---

# Complete closure of source role cell 3 of the positive 433-1b workboard

The JSON certificate in this directory summarizes 28 PROVED nodes of the
public campaign repository https://github.com/AllenGrahamHart/rs-mca-prize-dag
at commit `a001708ae134`. Each node carries its own machine verifier
(`verify.py`, sha256-pinned in the certificate) and independent audit.

The aggregate verifier pays the rank-drop common branch in all four source
sign rows, then reconstructs a disjoint cover of all
`7 * 15 * 4 * 4 = 1680` principal systems. This includes all 240 `xi4`
systems via the exact signed outside-role involution to the proved `xi3`
slice. Modal app `ap-jYkVRdvSHQuofSrzIJzAG1` replayed all 28 primary
verifiers and all 28 independent audits with 56/56 PASS.

This packet moves no ledger value and does not close K3 or the KoalaBear row.
Fresh independent proof review remains required before promotion to a GREEN
banked result.

## Provenance annotation (2026-08-10, coordinator)

The `provenance.commit` hash is the durable pin; the
`provenance.branch` field names a worker-local branch that is not
published. As of source-repo master
`711fcb9775ef6561fde1f6e7eb11d28e0a04d205`
(https://github.com/AllenGrahamHart/rs-mca-prize-dag), the pinned
commit and every node listed in this certificate are reachable from
public master with their verifiers. Worker certificate pushes land
on this PR ahead of the coordinator's audited merge to master, so a
pinned commit may be briefly unreachable (typically hours) between
the two — replay against master at or after the commit above.
