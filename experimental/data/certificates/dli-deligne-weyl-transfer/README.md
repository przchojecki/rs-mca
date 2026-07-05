# DLI Deligne-Weil Transfer

This directory stores the replayable certificate for
`experimental/notes/dli/dli_deligne_weyl_transfer.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_deligne_weyl_transfer.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_deligne_weyl_transfer.py \
  --check experimental/data/certificates/dli-deligne-weyl-transfer/dli_deligne_weyl_transfer.json
```

The verifier checks note anchors and a toy conductor-budget schema. It does
not prove the DLI noncollapse/conductor input.
