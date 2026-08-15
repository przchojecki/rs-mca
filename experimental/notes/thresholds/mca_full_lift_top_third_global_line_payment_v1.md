# MCA full-lift top-third global-line payment v1

## Status

PROVED / EXACT FINITE CALIBRATION.

The preceding full-lift theorem puts each exact top-third deficit layer on
an affine explanation line.  The triple-overlap argument is stronger: it
synchronizes the lines across all those layers.

Put

```text
s=floor((e-K)/3),  H=e-s-1,  u=floor(e/2).
```

If explanations have missed-coordinate allowances `r_i<=s`, then every
three inside agreement sets intersect in at least

```text
e-(r_1+r_2+r_3) >= e-3s >= K
```

coordinates.  Restriction injectivity therefore identifies their normalized
pair directions.  The entire high-deficit union lies on one affine codeword
line, not one line per layer.

Pair noncontainment limits the total common agreement core of this line to
`m-1`.  Off that core, agreement sets for distinct line parameters are
disjoint.  Thus the whole high union costs only

```text
N-m+1
```

once.  Combining this with the punctured-Johnson prefix gives

```text
|Z| <= (e-1) J_floor(e/2) + J_H + (N-m+1).
```

## Exact walls

Exact integer scans give

```text
KoalaBear:   e <= 95943, endpoint bound 6336049
Mersenne-31: e <= 97908, endpoint bound 6682339
```

The largest Mersenne bound is `6683188` at `e=97907`.  At the adjacent
supports the `H`-prefix Johnson denominators are `-1037` and `-965`.
Consequently the residual intervals are

```text
KoalaBear:   95944 <= e <= 1044238
Mersenne-31: 97909 <= e <= 1044241
```

The adjacent failures are failures of this proof profile, not unsafe
certificates.  No deployed v4 ledger atom moves.

## Provenance and replay

The source theorem, contract, primary verifier, and independent audit are
pinned at
`AllenGrahamHart/rs-mca-prize-dag@62ef043e0`.  This repository replay is
self-contained:

```bash
python3 experimental/verify_mca_full_lift_top_third_global_line_payment_v1.py
python3 -O experimental/verify_mca_full_lift_top_third_global_line_payment_v1.py
```

It scans every support in both newly paid intervals using exact integer
arithmetic, reconstructs both endpoint and adjacent records, checks a sharp
finite common-core model, and rejects four hostile mutations.
