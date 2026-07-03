# Clean-rate corridor pipeline certificate

This directory contains the deterministic skeleton emitted by:

```bash
python3 experimental/scripts/verify_clean_rate_corridor_pipeline.py --write
```

The packet aggregates existing arithmetic certificates for Q3R.3 / C-2 at
rates `1/4`, `1/8`, and `1/16`.  It records corridor crossings, integrality
margin rows, adjacent pinned-class power-of-two probes, and Row-C e1
norm-height frontiers.

Replay:

```bash
python3 experimental/scripts/verify_clean_rate_corridor_pipeline.py --check
python3 -m py_compile experimental/scripts/verify_clean_rate_corridor_pipeline.py
```

The verifier does not run Row-C value-set sampling or any large numerical
experiment.
