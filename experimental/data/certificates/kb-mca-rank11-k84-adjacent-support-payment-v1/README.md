# Rank-eleven adjacent-support carrier payment at `K'=84`

This supplemental certificate extends the base-field-normalized
adjacent-support census from the closed rank-nine prefix `K'=10..83`
through `K'=84`.

It uses no new analytic theorem. The exact support-two/support-three
partition has one ordinary lane and offsets `1..73`; the primary and
independent routers agree on all 74 lanes, and exact component arithmetic
leaves a positive gap. The prior `K'=83` packet is pinned as the immediate
certificate dependency.

```text
python3 experimental/scripts/verify_kb_mca_rank11_k84_adjacent_support_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_k84_adjacent_support_payment_v1.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_rank11_k84_adjacent_support_payment_v1_independent.py
```

Manifest SHA-256:
`4317c574e73626e2491e3dcfc777ab7e09c98333493f9161eb432a5ecfa355e3`.
Primary and independent verifier SHA-256 values are
`55c2586177919e5d9141a5f42e89d6f94e7a8692c8f197c009a5349e1b663b3d`
and
`73d3b364336197b403dcfa13fc2f8c37bdd8ccb8499a387e062f9642220f4c51`.

The compact verifiers check source custody, complete coverage counts, and
the exact premium ceiling and component ledger. The manifest pins the two
full lane-wave captures, compact merger output, component-payment output,
and both router implementations; it does not embed the 74 large raw lane
outputs.

This moves no deployed v4 atom, pays no remaining rank-eight or chronology
branch, and does not close error rank eleven, KoalaBear, or either prize
problem. The first open rank-nine row is `K'=85`; no adjacent extrapolation
is claimed.
