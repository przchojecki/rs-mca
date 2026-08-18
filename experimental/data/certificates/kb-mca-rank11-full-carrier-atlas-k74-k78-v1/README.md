# Rank-eleven full-carrier atlas at `K'=74..78`

This supplemental certificate extends the base-field-normalized split-pencil
census from the closed prefix `K'=10..73` through `K'=78`. It imports five
commit-, tree-, and contract-pinned public prize-DAG row closures.

The manifest is compact: it records canonical SHA-256 digests of the exact
exceptional defect tuples instead of embedding 25,733 tuples. The primary
and independent scripts replay all row and payment arithmetic. The optional
full-frontier script reconstructs one selected row's conservative frontier,
tuple digest, and complete pairwise-atlas reroute; run it in a bounded remote
worker rather than as a default local check.

```text
python3 experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k74_k78_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k74_k78_v1.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k74_k78_v1_independent.py
python3 experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k74_k78_v1_full.py --row 78
```

Manifest SHA-256:
`20dff5ce1c9634f9cd99e2cbacd4809fc860894f4549265a6f8b69176c0843c4`.
Primary verifier SHA-256:
`b3be282aa7ecc1696c53bc46a1a96702a03f7892db672ff1292090981480157a`.
Independent verifier SHA-256:
`55717ab77ccae0fdb7b774867ab95d1bb7b02b55a2979ad016114f01a36196a1`.
Full-frontier verifier SHA-256:
`4da8cfa98aa22cfde6cf14ebfda687371cff28a35c7e8c04ffca10c8bebcdbe5`.

This closes only rank-nine component rows `K'=74..78`. It moves no deployed
v4 atom, pays no rank-eight or chronology branch, and does not close error
rank eleven, KoalaBear, or either prize problem.
