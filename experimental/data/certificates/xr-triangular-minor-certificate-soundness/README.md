# XR Triangular Minor Certificate Soundness

This directory stores the replayable certificate for
`experimental/notes/m1/xr_triangular_minor_certificate_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_xr_triangular_minor_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_triangular_minor_certificate_soundness.py \
  --check experimental/data/certificates/xr-triangular-minor-certificate-soundness/xr_triangular_minor_certificate_soundness.json
```

The verifier checks triangular determinant examples and a zero-diagonal
control. It does not construct the profile inventory.
