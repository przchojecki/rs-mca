# L1 Petal Squarefree Classification Counting-Soundness Certificate

This directory contains the replayable certificate for
`experimental/notes/l1/l1_petal_squarefree_classification_counting_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_counting_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_counting_soundness.py \
  --check experimental/data/certificates/l1-petal-squarefree-classification-counting-soundness/l1_petal_squarefree_classification_counting_soundness.json
```

The verifier checks the proof-note anchors and finite-union inequality samples.
It does not construct the missing squarefree classification ledger.
