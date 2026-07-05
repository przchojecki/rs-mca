# SOV First-Obstruction Sensitivity

This directory stores the replayable certificate for
`experimental/notes/sov/sov_first_obstruction_sensitivity.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_sov_first_obstruction_sensitivity.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_first_obstruction_sensitivity.py \
  --check experimental/data/certificates/sov-first-obstruction-sensitivity/sov_first_obstruction_sensitivity.json
```

The verifier reuses the forced-root recursion helper. It does not prove the
full SOV value-set bound.
