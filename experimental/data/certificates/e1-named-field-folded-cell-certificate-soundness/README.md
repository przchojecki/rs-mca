# E1 Named-Field Folded Cell Certificate Soundness

This directory contains the replayable certificate for
`experimental/notes/e1/e1_named_field_folded_cell_certificate_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_e1_named_field_folded_cell_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_named_field_folded_cell_certificate_soundness.py \
  --check experimental/data/certificates/e1-named-field-folded-cell-certificate-soundness/e1_named_field_folded_cell_certificate_soundness.json
```

The verifier checks the named field/root schema for the `128` and `256` cells.
It does not supply the no-vector payloads.
