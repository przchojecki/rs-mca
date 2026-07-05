# F1 Minimal Field Descent Certificate

This directory contains the replayable certificate for
`experimental/notes/f1/f1_minimal_field_descent.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_f1_minimal_field_descent.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_f1_minimal_field_descent.py \
  --check experimental/data/certificates/f1-minimal-field-descent/f1_minimal_field_descent.json
```

The verifier checks the finite-field subfield lattice, the unique minimal
field calculation, and concrete Frobenius-orbit descent on small fields. It
does not prove the full F1 pole-forcing theorem.
