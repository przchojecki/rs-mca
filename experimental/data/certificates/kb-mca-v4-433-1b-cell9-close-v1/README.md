---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every one of the 105 raw direct labels in positive 433-1b cell 9 is empty on the deployed guarded route.
architecture: positive-433-1b-coordinate-guarded-route
partition_digest: sha256:82df776b06b375e9bee6fcc77aead1ebca4594028fa2e51df6318422a9d2f9bb
atom_or_cell: coordinate-positive 433-1b cell 9
quantifier: every raw direct label in the declared cell
projection_and_unit: raw workboard labels, not distinct bad slopes
claimed_bound: 0 surviving labels out of 105
status: PROVED
impact: LOCAL_ONLY
falsifier: a deployed guarded-route solution in any label, an omitted label, or an invalid orbit transport
replay: tools/ramguard local -- python3 <node path>/verify.py && tools/ramguard local -- python3 <node path>/verify_audit.py
---

# Complete closure of coordinate-positive cell 9 of the 433-1b workboard (all 105 labeled slices)

The JSON certificate in this directory summarizes 28 PROVED nodes of the
public campaign repository https://github.com/AllenGrahamHart/rs-mca-prize-dag
at commit `68ac9e383172`. Each node carries its own machine verifier
(`verify.py`, sha256-pinned in the certificate) and independent audit. The
aggregate verifier reconstructs the universal label router rather than
trusting a copied orbit table.

The exact census is 30 endpoint labels plus 75 active labels in 24 orbits.
Seventeen exclusion packets pay one representative of every active orbit,
giving 105/105 labeled slices. All 56 node verifier and audit scripts were
replayed by the campaign coordinator at the pinned commit.

This packet moves no ledger value and does not close K3 or the KoalaBear row.
Fresh independent proof review remains required before promotion to a GREEN
banked result.
