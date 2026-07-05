# DLI Reduced-Pole Majorant Table Soundness

This directory stores the replayable certificate for
`experimental/notes/dli/dli_reduced_pole_majorant_table_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_reduced_pole_majorant_table_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_reduced_pole_majorant_table_soundness.py \
  --check experimental/data/certificates/dli-reduced-pole-majorant-table-soundness/dli_reduced_pole_majorant_table_soundness.json
```

The verifier checks note anchors and a toy coverage/domination/budget table.
It does not construct the DLI majorant table.
