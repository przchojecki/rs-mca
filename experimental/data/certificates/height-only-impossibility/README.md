# Height-Only Certification Limit

This directory contains the replayable arithmetic packet for
`experimental/notes/thresholds/height_only_impossibility.md`.

Replay:

```text
python3 experimental/scripts/verify_height_only_impossibility.py
```

Regenerate:

```text
python3 experimental/scripts/verify_height_only_impossibility.py --emit
```

The packet computes exact full-cell height thresholds for the official rates
and verifies that `N=128` already lies beyond pure-height full-cell
certification in the `p < 2^256` prize range.
