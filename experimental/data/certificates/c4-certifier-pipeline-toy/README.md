# C-4 Certifier Pipeline Toy Certificate

Deterministic certificate for the C-4 toy certifier pipeline.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_c4_certifier_pipeline_toy.py --write
python3 experimental/scripts/verify_c4_certifier_pipeline_toy.py --check
```

The JSON records the direct MITM relation set hash, the complete
branch-and-bound totality anchor, and the corrected `N'=128` state-count table
for `w=12,14,16`.
