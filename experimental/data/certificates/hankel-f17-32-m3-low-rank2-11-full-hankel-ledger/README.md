# F17^32 M3 Low-Rank2-11 Full-Hankel Ledger

This directory contains a compact residual ledger for the synthetic low-rank M3
ladder at ranks `2..11` and `385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_full_hankel_ledger.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-full-hankel-ledger/f17_32_n512_k256_m3_low_rank2_11_full_hankel_ledger.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_full_hankel_ledger.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-full-hankel-ledger/f17_32_n512_k256_m3_low_rank2_11_full_hankel_ledger.json
```

The verifier rebuilds all `420` rank/agreement rows from existing certificates:
the rank-2..5 shifted-minor exclusion, the rank-6, rank-7, rank-8, and
rank-9..11 exact slack root tables, the rank-6..11 shifted-minor exclusion,
the rank-6..11 known ledger as an aggregate cross-check, the
projective-infinity endpoint audit, and the endpoint quotient-support and
quotient-image audits.

Result: across the whole synthetic rank-2..11 low-rank ladder, finite
first-minor roots or degree-bound root loci contribute zero full-Hankel witness
mass after shifted-minor exclusion.  The projective endpoint contributes one
full-Hankel witness before quotient-image charging, and the endpoint
quotient-image certificate charges it.  Therefore the aperiodic full-Hankel
projective residual upper bound is `0` in every checked row.

Non-claims: this is only for the synthetic low-rank ladder.  It is not an
actual-row M3 threshold theorem, not a finite-root quotient-image/support audit
for regular-minor roots, and not a replacement for the singular/pivot chart
program.
