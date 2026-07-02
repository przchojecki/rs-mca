# Integrality margin tables certificate

This directory contains the E14 replay packet for
`experimental/notes/thresholds/integrality_margin_tables.md`.

Replay:

```bash
python3 experimental/scripts/verify_integrality_margin_tables.py --emit
python3 experimental/scripts/verify_integrality_margin_tables.py \
  --check experimental/data/certificates/integrality-margin-tables/integrality_margin_tables.json
```

The packet evaluates MCA FM and list extras entropy-upper margins at the
candidate crossing scales used by the quotient-census and planted-list
arithmetic packets.  It is a margin table, not a proof of the structural
safe-side inputs.
