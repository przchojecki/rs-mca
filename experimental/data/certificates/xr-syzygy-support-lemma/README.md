# xr-syzygy-support-lemma certificate

This directory pins the toy linear-algebra recomputation for DAG node
`xr_syzygy_support_lemma` (2c-alpha).

Run:

```bash
python3 experimental/scripts/verify_xr_syzygy_support_lemma.py
```

The verifier rebuilds the shortened RS dual spaces, tensor alignment rows, and
triple syzygy kernels over the two rows recorded in
`toy_linear_algebra.json`.
