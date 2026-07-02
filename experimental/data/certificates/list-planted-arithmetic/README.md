# List Planted Arithmetic Certificate

This directory contains the deterministic certificate for
`experimental/notes/l1/list_planted_arithmetic_compiler.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_list_planted_arithmetic_compiler.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_list_planted_arithmetic_compiler.py \
  --check experimental/data/certificates/list-planted-arithmetic/list_planted_arithmetic_compiler.json
```

The packet checks exact quotient-core planted counts and exact
`floor(q/2^128)` Diophantine budget windows. It is a planted lower-bound
arithmetic certificate, not a safe-side `ImgFib` upper-bound proof.

