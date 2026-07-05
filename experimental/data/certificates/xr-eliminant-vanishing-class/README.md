# XR Eliminant Vanishing Class Certificate

This directory contains the replayable dependency certificate for
`experimental/notes/m1/xr_eliminant_vanishing_class.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_xr_eliminant_vanishing_class.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_eliminant_vanishing_class.py \
  --check experimental/data/certificates/xr-eliminant-vanishing-class/xr_eliminant_vanishing_class.json
```

The certificate composes the profile-nonvanishing and coordinate-hypersurface
reductions. It does not count points on the resulting hypersurface.
