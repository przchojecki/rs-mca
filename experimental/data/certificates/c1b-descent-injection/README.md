# C1b Descent-Injection Certificate

This certificate pins the `c1b_descent_injection` proof packet.

Run:

```bash
python3 experimental/scripts/verify_c1b_descent_injection.py
```

The verifier checks the symbolic seed and band identities, the band-budget
closed form, exhaustive toy trade splits, descent/lift injection roundtrips,
pipeline recovery gates at `16 -> 8`, `32 -> 16`, and `64 -> 32`, the
level-2 no-collision case for `h=4`, active-core calibration rows, the
Frobenius/BCH two-value characterization at `p = -1 mod n`, and this pinned
JSON certificate. The same S10-S12 gates support the companion route analysis
in `experimental/notes/roadmaps/midlarge_h_routes.md`.
