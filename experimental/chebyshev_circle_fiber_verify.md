# Chebyshev Circle-Domain Fiber Verification

**Status:** EXPERIMENTAL / AUDIT.

This note accompanies `experimental/chebyshev_circle_fiber_verify.py`.  It
checks the finite identities behind the Dickson--Chebyshev transfer in
`tex/slackMCA_v3.tex`.

For an odd prime `p` and even `N | p+1`, define the circle `x`-coordinate
domain

```text
X_N = {zeta + zeta^{-1} : zeta in mu_N(F_{p^2})} subset F_p.
```

For `m | N`, the monic Dickson polynomial `D_m` is characterized by

```text
D_m(z + z^{-1}) = z^m + z^{-m}.
```

The verifier constructs the norm-one subgroup of `F_{p^2}`, forms `X_N`, builds
`D_m` by the recurrence

```text
D_0 = 2,  D_1 = X,  D_m = X D_{m-1} - D_{m-2},
```

and checks, for each requested case:

```text
D_m(X_N) = X_{N/m},
|D_m^{-1}(w) cap X_N| = m for every w in X_{N/m} \\ {+2,-2},
locator(D_m^{-1}(w) cap X_N) = D_m(X) - w.
```

The default run uses `p=31`, so `p+1=32`, and verifies all nontrivial even
cases with `N >= 8` and `N/m >= 4`.

Example commands:

```bash
python3 experimental/chebyshev_circle_fiber_verify.py
python3 experimental/chebyshev_circle_fiber_verify.py --case 32:4 --format json
python3 experimental/chebyshev_circle_fiber_verify.py --prime 127
```

This is not a new asymptotic theorem.  It is a reproducible finite audit of the
fiber-locator mechanism that lets multiplicative quotient-core constructions
transfer to circle `x`-coordinate Reed-Solomon constituents.
