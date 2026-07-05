# DLI Truncated-Log Transfer

This directory stores the replayable certificate for
`experimental/notes/dli/dli_truncated_log_transfer.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_truncated_log_transfer.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_truncated_log_transfer.py \
  --check experimental/data/certificates/dli-truncated-log-transfer/dli_truncated_log_transfer.json
```

The verifier checks note anchors and a toy nonnegative-loss truncation budget.
