# SOV Forced-Root Recursion Algebra

This directory stores the replayable certificate for
`experimental/notes/sov/sov_forced_root_recursion_algebra.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_sov_forced_root_recursion_algebra.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_forced_root_recursion_algebra.py \
  --check experimental/data/certificates/sov-forced-root-recursion-algebra/sov_forced_root_recursion_algebra.json
```

The verifier checks the triangular forced-root recursion and shifted-constant
midpoint cases. It does not prove the full SOV value-set bound.
