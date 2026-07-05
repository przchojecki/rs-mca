# XR Coordinate Hypersurface Reduction Certificate

This directory contains the replayable dependency certificate for
`experimental/notes/m1/xr_coordinate_hypersurface_reduction.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_xr_coordinate_hypersurface_reduction.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_coordinate_hypersurface_reduction.py \
  --check experimental/data/certificates/xr-coordinate-hypersurface-reduction/xr_coordinate_hypersurface_reduction.json
```

The certificate checks the determinantal-locus implication and the dependency
on a nonzero profile minor. It is not a point-counting certificate.
