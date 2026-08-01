# Aligned-positive q-slice atlas certificate

This directory contains the fail-closed certificate for the complete
`12 x 3 = 36` aligned-positive diagonal `(1,1,2)` q-slice atlas.

Files:

- `kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.json` — generated exact
  registry, source-reconstruction metrics, equation hashes, localizer
  provenance, literal symmetry checks, and zero-ledger semantic cells.
- `schema.json` — structural JSON Schema.  The Python verifier adds the
  cross-field semantic checks that JSON Schema cannot express.

Replay:

```bash
env HOME=/private/tmp/rs_mca_sage_home /usr/local/bin/sage \
  experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.sage \
  --check

python3 \
  experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.py \
  --check --tamper-selftest

'/Applications/Wolfram Engine.app/Contents/Resources/Wolfram Player.app/Contents/MacOS/WolframKernel' \
  -script \
  experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.wls
```

The Sage replay is bounded symbolic compilation only.  It performs no
Groebner search or generic saturation.  The Python replay independently
reconstructs all 36 systems at two exact rational fixtures and rejects
twenty-five fail-closed scope/coverage/localizer mutations.  Wolfram independently
replays the 72 exact fixture cells and 144 literal `c<->d` / `b<->b^-1`
controls.

Every cell has status `UNCLASSIFIED_QSLICE_GENERATED`.  External PR pins are
annotations only; their scopes and conclusions are not imported.
