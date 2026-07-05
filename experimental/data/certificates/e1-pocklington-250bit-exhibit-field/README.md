# E1 Pocklington 250-bit Exhibit Field Certificate

This directory contains the replayable certificate for
`experimental/notes/e1/e1_pocklington_250bit_exhibit_field.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_e1_pocklington_250bit_exhibit_field.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_pocklington_250bit_exhibit_field.py \
  --check experimental/data/certificates/e1-pocklington-250bit-exhibit-field/e1_pocklington_250bit_exhibit_field.json
```

The verifier checks the Pocklington conditions and primitive root orders.  It
does not certify the folded no-vector payloads.
