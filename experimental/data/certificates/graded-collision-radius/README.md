# Graded Collision Radius Certificate

This directory contains the replayable arithmetic packet for
`experimental/notes/thresholds/graded_collision_radius.md`.

Replay:

```text
python3 experimental/scripts/verify_graded_collision_radius.py
```

Regenerate:

```text
python3 experimental/scripts/verify_graded_collision_radius.py --emit
```

The packet records exact toy cyclotomic norm checks, the certified
swap-radius table `d_*(N,L)`, and rate-cell full-certification frontiers.
