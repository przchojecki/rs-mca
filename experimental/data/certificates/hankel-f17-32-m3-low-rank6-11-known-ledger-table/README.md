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
rank-2..11 endpoint quotient-support audit.  Version `v4` also consumes the
rank-6..11 shifted-minor exclusion and the rank-2..11 endpoint quotient-image
witness audit.

Result: after these known ledgers, every checked synthetic row has projective
regular-root upper count at most `5`, below the `F_17^32` projective budget
numerator `6`.  The shifted-minor ledger proves that all `238` finite
first-minor roots are not full-Hankel exact-support witnesses, so the
full-Hankel witness column has residual projective upper count at most `1`
per row, coming from the projective endpoint.  The projective endpoint support
is excluded from all nontrivial proper quotient-remainder support families, but
the same endpoint parameter has an explicit `c=2` quotient-remainder witness
support.  After charging that endpoint to quotient-image, the aperiodic
full-Hankel residual upper count is `0` in every checked row.  Finite
regular-root quotient support and quotient image are explicitly recorded as
`not_audited`.

Non-claims: this is a synthetic-family ledger only.  It is not an actual-row M3
threshold bound, not a finite-root quotient-image subtraction certificate, and
not a statement about arbitrary M3 rows.
