# L1 dyadic quotient-profile evaluation certificate

This directory contains the replayable certificate for
`experimental/notes/l1/l1_dyadic_profile_evaluation.md`.

Replay:

```bash
python3 experimental/scripts/verify_l1_dyadic_profile_evaluation.py --emit
python3 experimental/scripts/verify_l1_dyadic_profile_evaluation.py \
  --check experimental/data/certificates/l1-dyadic-profile-evaluation/l1_dyadic_profile_evaluation.json
```

The JSON records the exact active dyadic quotient orders for rates
`1/2, 1/4, 1/8, 1/16`, reserve grid `eta=2^-1,...,2^-12`, exact attaining
binomial counts, 128-bit crossing orders, and finite direct-scan validations.
All intermediate binomial counts are recomputed by the verifier.
