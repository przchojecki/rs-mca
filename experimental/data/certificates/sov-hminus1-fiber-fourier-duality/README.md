# SOV H-minus-1 Fiber Fourier Duality

This directory stores the replayable certificate for
`experimental/notes/sov/sov_hminus1_fiber_fourier_duality.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_sov_hminus1_fiber_fourier_duality.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_hminus1_fiber_fourier_duality.py \
  --check experimental/data/certificates/sov-hminus1-fiber-fourier-duality/sov_hminus1_fiber_fourier_duality.json
```

The verifier checks note anchors and a tiny prime-field Fourier inversion
sample. It does not prove the actual SOV character-sum bounds.
