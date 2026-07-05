# SOV Nonconstant Affine Character Cancellation

This directory stores the replayable certificate for
`experimental/notes/sov/sov_nonconstant_affine_character_cancellation.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_sov_nonconstant_affine_character_cancellation.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_nonconstant_affine_character_cancellation.py \
  --check experimental/data/certificates/sov-nonconstant-affine-character-cancellation/sov_nonconstant_affine_character_cancellation.json
```

The verifier checks note anchors and enumerates small finite-field affine
character sums. It does not construct the actual SOV affine-piece partitions.
