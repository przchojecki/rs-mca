# List crossing localization certificate

This directory contains the toy endpoint replay for
`experimental/notes/l1/list_crossing_localization.md`.

Replay:

```bash
python3 experimental/scripts/verify_list_crossing_localization.py --emit
python3 experimental/scripts/verify_list_crossing_localization.py \
  --check experimental/data/certificates/list-crossing-localization/list_crossing_localization.json
```

The theorem is the elementary monotonicity and adjacent-crossing argument for
the exact list staircase.  The JSON packet only fixes the endpoint convention
on a tiny Reed-Solomon row.
