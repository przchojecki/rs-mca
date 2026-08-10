---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every one of the 105 raw direct labels in positive 433-1b source-role cell 11 is empty on the deployed guarded route.
architecture: positive-433-1b-coordinate-guarded-route
partition_digest: sha256:82df776b06b375e9bee6fcc77aead1ebca4594028fa2e51df6318422a9d2f9bb
atom_or_cell: coordinate-positive 433-1b source-role cell 11
quantifier: every raw direct label in the declared source-role cell
projection_and_unit: raw workboard labels, not distinct bad slopes
claimed_bound: 0 surviving labels out of 105
status: PROVED
impact: LOCAL_ONLY
falsifier: a deployed guarded-route solution in cell 11, an omitted quotient orbit, an invalid endpoint rootlessness certificate, or a verifier digest mismatch
replay: tools/ramguard local -- python3 <node path>/verify.py && tools/ramguard local -- python3 <node path>/verify_audit.py
---

# Complete closure of source-role cell 11 of the positive 433-1b workboard

The JSON certificate in this directory summarizes 22 PROVED nodes of the
public campaign repository https://github.com/AllenGrahamHart/rs-mca-prize-dag
at commit `7824a826a28360fabcb1e50bf36f1cec14685292`. Each node carries a
machine verifier whose sha256 is pinned in the certificate. All 44 cell-11
verifier and hostile-audit scripts passed at that exact commit.

Cell 11 has 75 active labels in 24 exact quotient orbits. Sixteen owner
packets pay one representative of every orbit. The remaining 30 endpoint
labels are excluded by the independent endpoint rootlessness theorem. The
aggregate verifiers reconstruct the exact `75+30=105` disjoint cover.

The final outside-role packet closes pairings 7, 8, and 11. Pairings 7 and 8
each retain 64 compatible lifts and 128 colored lanes; pairing 11 retains 16
lifts and 32 lanes. Every colored value is nonzero. A shared independent
FLINT reconstruction covers 61 polynomial profiles, 302 deployed roots, and
degrees through 5192. Three direct audits replay every candidate union,
source relation, paired-scalar equation, and cell-11 leading-boundary
payment.

This closes the last role orbit named as open by the preceding living K3
packet. Thus the exported positive-433-1b workboard has no remaining raw
label cell. This packet moves no ledger value and does not close K3 or the
KoalaBear row: conversion from raw labels to distinct affine slopes, the
genuine-pencil ledger, and fresh independent proof review remain required.

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
