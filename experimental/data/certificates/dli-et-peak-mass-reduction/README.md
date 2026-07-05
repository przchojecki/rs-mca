# DLI Erdos-Turan Peak-Mass Reduction

This directory stores the replayable certificate for
`experimental/notes/dli/dli_et_peak_mass_reduction.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_et_peak_mass_reduction.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_et_peak_mass_reduction.py \
  --check experimental/data/certificates/dli-et-peak-mass-reduction/dli_et_peak_mass_reduction.json
```

The verifier checks note anchors and a toy annular-discrepancy budget schema.
