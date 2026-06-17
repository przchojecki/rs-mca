# MCA Slope Scan Certificate

- **Status:** PROVED
- **Agent/model:** Codex acting autonomously through AllenGrahamHart
- **Script:** `experimental/mca_slope_scan.py`
- **Date:** 2026-06-17

## Purpose

This note records a small reproducible run for the planned
`experimental/mca_slope_scan.py` utility. The script exhausts support-wise
canonical-line MCA bad slopes for the quotient-locator line

```text
u_z(x) = x^(k+a) + z*x^k
```

over a small prime field.

## Command

```sh
python3 experimental/mca_slope_scan.py \
  --prime 13 \
  --n 12 \
  --k 6 \
  --quotient-order 6 \
  --pretty
```

## Recorded Output

```text
canonical-line MCA slope scan
  p=13 n=12 k=6
  quotient_order=6 a=2
  locator slopes: 13
  MCA-bad slopes: 13
  density: 1
  supports examined: 794
  locator subset of MCA: True
```

The JSON result reports `status = PROVED`, theorem/problem support
`RS_disproof_v3.tex lem:locator; proximity_blueprint_v3.tex M1`, and the exact
slope set:

```text
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
```

## Interpretation

For `F_13^*`, `k=6`, quotient order `6`, and `a=2`, the scanner verifies that
every slope in `F_13` is support-wise MCA-bad for the canonical line at radius

```text
1 - k/n - 1/Nq = 1/3.
```

The locator restricted-sum slopes are a subset of the exhaustively detected MCA
bad slopes, as required by the quotient-locator lemma.
