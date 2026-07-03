# E26 Dihedral Window Arithmetic

- **Task:** E26.
- **DAG nodes:** `rate_half_coverage_gap`, `dihedral_quotient_stratum`.
- **Status:** PROVED ARITHMETIC / coverage found, conditional on the E25
  dihedral ledger audit.
- **Verifier:** `experimental/scripts/verify_e26_dihedral_window_arithmetic.py`.
- **Artifact:** `experimental/data/certificates/e26-dihedral-window-arithmetic/e26_dihedral_window_arithmetic.json`.

This packet answers the arithmetic part of E26.  It does not solve alignment
systems and does not prove that the dihedral stratum is paid.  It only checks
whether Chebyshev/dihedral twin-fiber window scales can land in the rate-`1/2`
prize-max coverage gap.

## Model

On a `2`-power multiplicative row, inversion groups points into twin fibers.
After an optional multiplicative quotient, the relevant window scale has the
form

```text
d = m * ell,
```

where `m` is the twin-fiber size and `ell` is the number of twin fibers used.
The pure dihedral case is `m = 2`.  The mixed multiplicative-dihedral cases
are `m = 4, 8, ...`.

For a moving twin-fiber window on a row of length `n`, the corresponding count
formula is

```text
binom(n/m, ell).
```

The verifier records log2 Robbins brackets for prize-scale formulas rather
than constructing enormous binomial integers.

## Rate-1/2 Prize-Max Result

The old multiplicative 2-power endpoint is

```text
M_max = 2^33 = 8,589,934,592.
```

The QX.14 crossing gives

```text
sigma* = 8,592,912,738.
```

The inclusive interval `[M_max, sigma*]` has `2,978,147` radii.  The strict
new interval `(M_max, sigma*]` has `2,978,146` radii.  Pure dihedral windows
hit `1,489,073` distinct strict new scales, starting at

```text
d = 2^33 + 2 = 8,589,934,594.
```

At that first new scale,

```text
m = 2,
ell = 2^32 + 1,
count = binom(2^40, 2^32 + 1),
log2(count) >= 40,543,948,385.302246.
```

This is far above the prize budget scale `B*` (`log2 B* = 127.9` in the
QX.14 stand-in convention).  Mixed windows also hit the strict interval, with
twin-fiber sizes through

```text
m = 2^21 = 2,097,152.
```

Thus the E26 arithmetic answer is:

```text
coverage found, conditional on E25 paying the dihedral/Chebyshev stratum.
```

## Calibration Rows

The pinned row `n=512, k=256` and Row C `n=1024, k=512` both have the analogue
`sigma* = 4` and old endpoint `4`.  The endpoint itself has a dihedral formula,
but there is no strict interval beyond the old endpoint:

```text
(4, 4] is empty.
```

So these rows are calibration checks only; they do not test a positive coverage
gap.

## Replay

```bash
python3 experimental/scripts/verify_e26_dihedral_window_arithmetic.py --write
python3 experimental/scripts/verify_e26_dihedral_window_arithmetic.py --check
python3 -m py_compile experimental/scripts/verify_e26_dihedral_window_arithmetic.py
python3 -m json.tool experimental/data/certificates/e26-dihedral-window-arithmetic/e26_dihedral_window_arithmetic.json >/dev/null
```

## Nonclaims

This packet does not prove `dihedral_quotient_stratum`, does not classify
received-word pairs, does not run M5 chart machinery, and does not prove that
the first new scale is paid.  It supplies the arithmetic input for E25/E28:
if E25 classifies the dihedral stratum as paid, then rate `1/2` has a
dihedral window inside the previously uncovered band.
