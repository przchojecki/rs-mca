# M720 Residual Slice Metadata

This directory stores the replayable certificate for
`experimental/notes/m720/m720_residual_slice_metadata.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_m720_residual_slice_metadata.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_residual_slice_metadata.py \
  --check experimental/data/certificates/m720-residual-slice-metadata/m720_residual_slice_metadata.json
```

The verifier replays the Modal count-ceiling window classifier. It does not
prove zero survivors for residual cells.
