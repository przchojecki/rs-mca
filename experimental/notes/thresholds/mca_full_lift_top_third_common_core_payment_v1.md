# MCA full-lift top-third common-core payment v1

## Status

PROVED / EXACT FINITE CALIBRATION.

The top-third affine-line theorem remains valid for `e>=d`.  The new issue
is that the highest possible outside deficit is `m` and some exact layers
have at most `K-1` outside agreements.

On an affine explanation line, a coordinate agreeing for every parameter is
a simultaneous base/direction agreement for one codeword pair.  Pair
noncontainment limits this total common core to `m-1`.  Off the core,
agreement sets are disjoint, so every exact line layer has

```text
L <= N-m+1.
```

When the outside agreement `A_r` exceeds `K-1`, the sharper outside
zero-core cap remains available.  The piecewise cap is

```text
Q_r = N-m+1                                      if A_r<=K-1,
Q_r = floor((N-e-(K-1))/(A_r-(K-1)))           otherwise.
```

Combining these top-third layers with the Johnson prefix gives

```text
KoalaBear:   e<=95943, endpoint bound 27414298;
Mersenne-31: e<=67452, endpoint bound 16266965.
```

KoalaBear `e=95944` has prefix denominator `-1037`.  Mersenne
`e=67453` has valid bound `17248067`, over budget by `470852`.  The
remaining intervals are

```text
KoalaBear:   95944 <= e <= 1044238
Mersenne-31: 67453 <= e <= 1044241.
```

## Replay

```bash
python3 experimental/verify_mca_full_lift_top_third_common_core_payment_v1.py
```

The verifier checks the total-core cap on a sharp finite model, direct
endpoint floor sums, uniform KoalaBear prefix maxima, all five new Mersenne
cells, both adjacent stops, and hostile mutations.
