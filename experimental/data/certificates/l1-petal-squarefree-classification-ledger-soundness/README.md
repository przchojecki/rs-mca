# L1 Petal Squarefree Classification Ledger-Soundness Certificate

This directory contains the replayable certificate for
`experimental/notes/l1/l1_petal_squarefree_classification_ledger_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_ledger_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_ledger_soundness.py \
  --check experimental/data/certificates/l1-petal-squarefree-classification-ledger-soundness/l1_petal_squarefree_classification_ledger_soundness.json
```

The verifier checks proof-note anchors and a small ledger-semantics sample.
It does not construct or certify the missing squarefree classification ledger.
