# xr-syzygy-flat-transport certificate

This directory pins the toy transport check for DAG node
`xr_syzygy_flat_transport` (2c-gamma-a).

Run:

```bash
python3 experimental/scripts/verify_xr_syzygy_flat_transport.py
```

The verifier checks sparse supports, matroid closures, local coefficient
nullities, and sampled union closures for the flats recorded in
`toy_flat_transport.json`.
