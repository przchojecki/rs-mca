# Rank-eleven best-single adjacent payment at `K'=85`

This supplemental certificate extends the base-field-normalized
adjacent-support program from the closed rank-nine prefix `K'=10..84`
through `K'=85`.

The exact partition is one ordinary lane plus offsets `1..74`. A paired raw
scan proves that offsets `42..74` are entirely safe and isolates exactly
331,533 unsafe units in offsets `1..41`. Paired exhaustive carrier traversals
then prove that every residual profile is paid by its best individually valid
single adjacent edge. The packet does not compose overlapping edges.

```text
python3 experimental/scripts/verify_kb_mca_rank11_k85_best_single_adjacent_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_k85_best_single_adjacent_payment_v1.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_rank11_k85_best_single_adjacent_payment_v1_independent.py
```

Manifest SHA-256:
`ae598632a204181a0ef0cc8895c077af22d16587f2ab209b7cebb3e26c2cb5ee`.
Primary and independent verifier SHA-256 values are
`527b5f8be7863d67e59d338fa95871aa087a38513585efc89f4f87db80db50e7`
and
`15b58870dbaff03768c4d8bfa196cede8302bfc9ac7c3ac5e06f65f5813e4e6c`.

The compact verifiers check source custody, the ordinary and offset coverage
identities, residual conservation, the exact premium ceiling, and the
component ledger. The manifest pins all three paired finite waves and the
component-payment output; it does not embed the large raw captures.

This moves no deployed v4 atom, pays no remaining rank-eight or chronology
branch, and does not close error rank eleven, KoalaBear, or either prize
problem. The first open rank-nine row is `K'=86`; no adjacent extrapolation
is claimed.
