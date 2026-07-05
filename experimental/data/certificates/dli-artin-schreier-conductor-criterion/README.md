# DLI Artin-Schreier Conductor Criterion

This directory stores the replayable certificate for
`experimental/notes/dli/dli_artin_schreier_conductor_criterion.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_artin_schreier_conductor_criterion.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_artin_schreier_conductor_criterion.py \
  --check experimental/data/certificates/dli-artin-schreier-conductor-criterion/dli_artin_schreier_conductor_criterion.json
```

The verifier checks note anchors and a finite-field sanity case. It does not
construct the DLI reduced-phase manifest.
