# C2 GCD Harness Self-Test Certificate

This certificate pins the no-argument self-test of
`verify_c2_gcd_harness.py`.

Run:

```bash
python3 experimental/scripts/verify_c2_gcd_harness.py
```

The verifier reconstructs `D_pt(16,3)`, recovers the toy exceptional row
primes `{7,17,97}` by both the GCD route and an independent pointwise route,
checks the Row-C/prize `h`-window arithmetic, checks the toy partner cap, and
confirms that the pinned JSON certificate matches the recomputed summary.
