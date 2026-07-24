# M31 root-lift bridge stop certificate

This directory contains the canonical exact certificate for the corrected
one-error root-lift census.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_rootlift_bridge.py --check
python3 experimental/scripts/verify_m31_rootlift_bridge.py --tamper-selftest
```

The verifier is deterministic, uses exact integer arithmetic, exhausts the
finite `F_37` counterexample, and does not read `agents.md`, `PR_BODY.md`, or an
agents-log file. Steering-file hashes are provenance only and never gate replay.
