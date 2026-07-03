# Census Dodge Selection Certificate

This directory contains the replayable certificate for
`experimental/notes/thresholds/census_dodge_selection.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_census_dodge_selection.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_census_dodge_selection.py \
  --check experimental/data/certificates/census-dodge-selection/census_dodge_selection.json
```

The certificate records relaxed and dyadic adjacent quotient-census crossings
for the official rates at budget bits `64`, `96`, and `128`, including the
safe margins and lower-certificate missing-mass tolerances.
