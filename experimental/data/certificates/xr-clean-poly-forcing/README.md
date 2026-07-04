# XR clean-rate polynomial forcing certificate

This directory contains the deterministic certificate emitted by
`experimental/scripts/verify_xr_clean_poly_forcing.py`.

The certificate supports the proof note
`experimental/notes/roadmaps/xr_clean_poly_forcing_reduction.md` for DAG node
`xr_clean_residual_any_gate`: at every clean-rate candidate, the post-strip
residual reserve `16 n^3` fits below the exact integer allowance left after
the quotient and tangent ledgers.

Regenerate and verify:

```bash
python3 experimental/scripts/verify_xr_clean_poly_forcing.py --write-certificate
python3 experimental/scripts/verify_xr_clean_poly_forcing.py
```
