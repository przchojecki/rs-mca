# DLI Reduced-Phase Manifest Soundness

This directory stores the replayable certificate for
`experimental/notes/dli/dli_reduced_phase_manifest_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_reduced_phase_manifest_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_reduced_phase_manifest_soundness.py \
  --check experimental/data/certificates/dli-reduced-phase-manifest-soundness/dli_reduced_phase_manifest_soundness.json
```

The verifier checks note anchors and a toy complete-manifest schema. It does
not construct the DLI reduced-phase manifest.
