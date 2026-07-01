# F17^32 M3 Rank-6..11 Low-Rank Known-Ledger Table

This directory contains a compact M4-style residual table for the synthetic
low-rank M3 block at ranks `6..11` and `385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_known_ledger_table.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_known_ledger_table.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json
```

The verifier rebuilds all `252` rank/agreement rows from existing certificates:
exact finite-root slack, the projective-infinity endpoint audit,
tangent/common-code-line exclusion, proper-subfield exclusion, and the
rank-2..11 endpoint quotient-support audit.

Result: after these known ledgers, every checked synthetic row has projective
regular-root upper count at most `5`, below the `F_17^32` projective budget
numerator `6`.  The projective endpoint support is excluded from all
nontrivial proper quotient-remainder support families; finite regular-root
quotient support and quotient image are explicitly recorded as `not_audited`.

Non-claims: this is a synthetic-family ledger only.  It is not an actual-row M3
threshold bound, not a finite-root quotient-image subtraction certificate, and
not a proof that finite regular-minor roots are actual bad slopes.
