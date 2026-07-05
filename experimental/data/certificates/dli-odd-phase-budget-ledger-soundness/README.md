# DLI Odd-Phase Budget Ledger Soundness

This directory stores the replayable certificate for
`experimental/notes/dli/dli_odd_phase_budget_ledger_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_odd_phase_budget_ledger_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_odd_phase_budget_ledger_soundness.py \
  --check experimental/data/certificates/dli-odd-phase-budget-ledger-soundness/dli_odd_phase_budget_ledger_soundness.json
```

The verifier checks note anchors and a toy complete-ledger schema. It does not
construct the DLI odd-phase ledger.
