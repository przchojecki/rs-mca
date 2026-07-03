# M1 Deficiency-One U1-U5 Chart Chain Certificate

This directory contains the replayable certificate for
`experimental/notes/m1/m1_deficiency_one_u1_u5_chain.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_m1_deficiency_one_u1_u5_chain.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m1_deficiency_one_u1_u5_chain.py \
  --check experimental/data/certificates/m1-deficiency-one-u1-u5-chain/m1_deficiency_one_u1_u5_chain.json
```

The certificate checks the Cramer-kernel chart, nondegeneracy certificates,
the divisibility gate, pseudo-remainder equivalence, and the U5 eliminant
dichotomy on exact finite-field toy families.
