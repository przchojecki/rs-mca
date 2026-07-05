# EF Full-Orbit Cycle Descent Certificate

This directory contains the replayable certificate for
`experimental/notes/ef/ef_full_orbit_cycle_descent.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_ef_full_orbit_cycle_descent.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_full_orbit_cycle_descent.py \
  --check experimental/data/certificates/ef-full-orbit-cycle-descent/ef_full_orbit_cycle_descent.json
```

The verifier checks proof-note anchors and finite orbit-permutation samples.
It does not exclude the descended pole-free cycles.
