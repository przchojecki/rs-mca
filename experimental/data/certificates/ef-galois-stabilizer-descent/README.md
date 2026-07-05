# EF Galois Stabilizer Descent Certificate

This directory contains the replayable certificate for
`experimental/notes/ef/ef_galois_stabilizer_descent.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_ef_galois_stabilizer_descent.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_galois_stabilizer_descent.py \
  --check experimental/data/certificates/ef-galois-stabilizer-descent/ef_galois_stabilizer_descent.json
```

The verifier checks proof-note anchors and the stabilizer trichotomy for cyclic
Galois groups of small extension degrees.  It does not exclude the full-orbit
case.
