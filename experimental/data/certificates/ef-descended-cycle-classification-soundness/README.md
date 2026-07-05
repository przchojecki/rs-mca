# EF Descended-Cycle Classification Soundness Certificate

This directory contains the replayable certificate for
`experimental/notes/ef/ef_descended_cycle_classification_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_classification_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_classification_soundness.py \
  --check experimental/data/certificates/ef-descended-cycle-classification-soundness/ef_descended_cycle_classification_soundness.json
```

The verifier checks proof-note anchors and a small exhaustive classification
sample.  It does not construct or certify the actual classification payload.
