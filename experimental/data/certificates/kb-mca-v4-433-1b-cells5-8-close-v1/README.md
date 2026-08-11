---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every one of the 210 raw direct labels in positive 433-1b role orbit [5,8] is empty on the deployed guarded route.
architecture: positive-433-1b-coordinate-guarded-route
partition_digest: sha256:82df776b06b375e9bee6fcc77aead1ebca4594028fa2e51df6318422a9d2f9bb
atom_or_cell: coordinate-positive 433-1b role orbit [5,8]
quantifier: every raw direct label in both declared role cells
projection_and_unit: raw workboard labels, not distinct bad slopes
claimed_bound: 0 surviving labels out of 210
status: PROVED
impact: LOCAL_ONLY
falsifier: a deployed guarded-route solution in either role cell, an omitted label, an invalid endpoint rootlessness certificate, or an invalid duplicate-role transport
replay: tools/ramguard local -- python3 <node path>/verify.py && tools/ramguard local -- python3 <node path>/verify_audit.py
---

# Complete closure of the [5,8] common-role orbit of the positive 433-1b workboard

The JSON certificate in this directory summarizes 23 PROVED nodes of the
public campaign repository https://github.com/AllenGrahamHart/rs-mca-prize-dag
at commit `3fa2987430242cb631ab76be4ebbee549ce95fb8`. Each node carries a
machine verifier whose sha256 is pinned in the certificate. The closure-layer
verifiers and hostile audits were replayed at that exact commit.

Cell 5 has 75 active labels in 24 exact quotient orbits. Sixteen owner
packets pay one representative of every orbit. Its remaining 30 endpoint
labels are source-incompatible: all eight degree-16/degree-11 eliminants
have `gcd(E(r),r^p-r)=1` over `p=2130706433`. Thus cell 5 is closed at
105/105. A separately verified B/C symmetry bijects all 1,680 signed
principal systems from cell 5 to cell 8, while the global rank-drop theorem
pays the complement, closing role orbit `[5,8]` at 210/210 labels.

This packet moves no ledger value and does not close K3 or the KoalaBear row.
Within this exported workboard, role orbit `[11]` remains open. Fresh
independent proof review remains required before promotion to a GREEN banked
result.

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
