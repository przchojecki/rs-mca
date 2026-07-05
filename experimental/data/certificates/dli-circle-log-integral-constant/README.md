# DLI Circle Log-Integral Constant

This directory stores the replayable certificate for
`experimental/notes/dli/dli_circle_log_integral_constant.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_dli_circle_log_integral_constant.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_circle_log_integral_constant.py \
  --check experimental/data/certificates/dli-circle-log-integral-constant/dli_circle_log_integral_constant.json
```

The verifier checks note anchors and a numerical sanity check. The proof note
contains the symbolic reduction to the classical integral.
