# Adjacency Staircase Localization Certificate

This directory contains the emitted arithmetic certificate for

```text
experimental/notes/thresholds/adjacency_staircase_localization.md
```

Replay:

```text
python3 experimental/scripts/verify_adjacency_staircase_localization.py --emit
python3 experimental/scripts/verify_adjacency_staircase_localization.py
```

The certificate is a compiler-arithmetic artifact.  It proves the generic
staircase, corridor, list-staircase, and steepness-envelope checks used by
later row-specific packets; it does not certify a new row threshold.
