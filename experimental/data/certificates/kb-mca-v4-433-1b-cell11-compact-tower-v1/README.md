# KoalaBear K3: 433-1b cell-11 compact tower

This experimental packet replaces the public cell-11 pilot's nonexact
nine-generator quotient by three exact reduced towers.  The selected
`c_row=5` chart has no deployed-field point on either leading-coefficient
boundary.  A primitive eight-coordinate coefficient kernel also reduces all
ten common Vieta rows to zero on the guarded locus.

The mathematical replay uses local SymPy and Singular and pins the public DAG
checkout at commit `28b3bc8ab13e94c25088e904251eb5cf49e68ad2`:

```bash
python3 experimental/scripts/replay_kb_mca_v4_433_1b_cell11_compact_tower_v1.py \
  --dag-root /path/to/rs-mca-prize-dag \
  --output /tmp/cell11_raw.json
python3 experimental/scripts/verify_kb_mca_v4_433_1b_cell11_compact_tower_v1.py \
  --assemble /tmp/cell11_raw.json --mutations
python3 experimental/scripts/verify_kb_mca_v4_433_1b_cell11_compact_tower_v1.py \
  --mutations
```

Wolfram Cloud independently reproduced both quartic factorizations and the
two quadratic nonresidue checks.  It is not needed by the committed verifier.

Status is `EXPERIMENTAL_REVIEW_REQUIRED`.  This is the structural input for
the next complete cell-11 signed-pair resultant computation.  It does not
perform that computation, transport the result through all sign or role
charts, count affine slopes, move a v4 ledger atom, or close K3.  It also does
not use the falsified FLOOR-v2 first-moment route or claim an upper bound for
the exact sparse-layer maximum `S_sparse`.

