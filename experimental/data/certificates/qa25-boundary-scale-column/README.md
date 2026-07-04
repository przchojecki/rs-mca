# QA.25 Boundary-Scale Column Certificate

This certificate pins the exact crossover arithmetic for DAG node
`u2c_boundary_scale_column`.

Run:

```bash
python3 experimental/scripts/verify_qa25_boundary_scale_column.py
```

The verifier reads the QA.22 staircase certificate, recomputes the
`M = t` boundary-scale zero-sum column for the six campaign rows, and checks
that the repaired budget remains below `B*` on every row.
