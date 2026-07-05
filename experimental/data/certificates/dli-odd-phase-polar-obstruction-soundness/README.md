# DLI Odd-Phase Polar Obstruction Soundness

This directory stores the replayable certificate for
`experimental/notes/dli/dli_odd_phase_polar_obstruction_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_odd_phase_polar_obstruction_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_odd_phase_polar_obstruction_soundness.py \
  --check experimental/data/certificates/dli-odd-phase-polar-obstruction-soundness/dli_odd_phase_polar_obstruction_soundness.json
```

The verifier checks note anchors and the reduced-pole predicate. It does not
construct the reduced-phase manifest.
