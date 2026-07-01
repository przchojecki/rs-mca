# F17^32 M3 Low-Rank2-12 Paid-Residual Ledger

This certificate composes the two standalone low-rank2..12 packets in this PR:

- the affine-gcd packet proves that the v10 canonical finite affine rank-drop
  root set is empty in all `462` synthetic rank/agreement rows;
- the endpoint quotient-image packet charges the projective endpoint `[0:1]`
  to an explicit `c=2` quotient-remainder witness in the same `462` rows.

The combined conclusion is an M3/M4-style paid-root residual statement:
for the synthetic low-rank M3 ladder at ranks `2..12` and agreements
`385 <= A <= 426`, the regular projective rank-drop residual after paid
quotient-image endpoint removal is zero in every row.

Run:

```bash
python3 experimental/scripts/verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-paid-residual-ledger/f17_32_n512_k256_m3_low_rank2_12_paid_residual_ledger.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-paid-residual-ledger/f17_32_n512_k256_m3_low_rank2_12_paid_residual_ledger.json
```

Nonclaims: this is only the synthetic low-rank ladder, it consumes the two
source certificates rather than recomputing their proofs, it is not an
arbitrary-row M3 threshold theorem, and it does not classify singular pivot
charts.
