# Quotient Census Window Compiler Certificate

This directory contains the emitted certificate for:

```text
experimental/notes/thresholds/quotient_census_window_compiler.md
```

Replay:

```text
python3 experimental/scripts/verify_quotient_census_window_compiler.py --emit
python3 experimental/scripts/verify_quotient_census_window_compiler.py
```

The certificate verifies exact 2-power quotient-count bignums, bounded
scale-crossing tables, exact budget-window arithmetic, and exact dyadic
quotient-profile evaluation.  It does not count primes inside the windows or
resolve quotient collisions below the norm threshold.
