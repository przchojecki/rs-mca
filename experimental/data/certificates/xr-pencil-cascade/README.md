# XR Pencil Cascade Certificate

This certificate pins the W1 verifier for DAG node `xr_pencil_cascade`.

Run:

```bash
python3 experimental/scripts/verify_xr_pencil_cascade.py
```

The verifier uses deterministic `F_17` toy rows to check the exact residual
ratio form of the pencil cascade:

- threshold core `r=A-1`;
- off-core slope collisions;
- core `r=A`, where all finite slopes are bad;
- blocked off-core points with no finite slope;
- recovery of the forced codeword pair `(U,V)` from two slopes.
