# E26 dihedral window arithmetic certificate

This directory contains the deterministic certificate emitted by:

```bash
python3 experimental/scripts/verify_e26_dihedral_window_arithmetic.py --write
```

The packet enumerates achievable dihedral and mixed
dihedral-multiplicative window scales for the E26 rate-`1/2` coverage-gap
question.  It is arithmetic-only: no pair search, no M5 chart run, and no heavy
computation.

Replay:

```bash
python3 experimental/scripts/verify_e26_dihedral_window_arithmetic.py --check
python3 -m py_compile experimental/scripts/verify_e26_dihedral_window_arithmetic.py
```

The certificate finds a strict new pure-dihedral scale at `2^33 + 2`, inside
the previously uncovered prize-max rate-`1/2` band, conditional on the E25
dihedral ledger audit classifying the stratum as paid.
