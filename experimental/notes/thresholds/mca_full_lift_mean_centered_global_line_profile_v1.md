# MCA full-lift mean-centered global-line profile v1

## Status

PROVED / EXACT FINITE CALIBRATION.

The cross-layer global-line theorem stopped when the coarse Johnson cap at
`H=e-floor((e-K)/3)-1` changed sign.  The proved mean-centered Gram cap is
legal at this boundary.  Use the full cumulative prefix profile:

```text
C_h = punctured Johnson cap, when its denominator is positive;
C_h = mean-centered Gram cap, otherwise when its hypotheses hold;
B_h = min_(h<=v<=H) C_v.
```

If `A_H=m-H>K-1`, the ordinary set-system proof applies even when `e>=d`:
after puncturing the direction support, every selected explanation supplies
an `A_h`-block, and two distinct degree-`<K` explanations intersect in at
most `K-1` coordinates.  Combining this prefix with the one-time
cross-layer line charge gives

```text
|Z| <= sum_(h=1)^H (B_h-B_(h-1))*floor(e/h) + (N-m+1).
```

## Exact walls

Exact scans give

```text
KoalaBear:   e <= 96150, endpoint 479693401
Mersenne-31: e <= 98229, endpoint 16488216
```

The largest Mersenne value is `16489118` at `e=98228`.  At adjacent
KoalaBear `e=96151`, the first undefined cap is `h=H=64105`, with
mean-centered denominator `-4625043784`.  At adjacent Mersenne
`e=98230`, every cap is legal but the exact profile `17415873` exceeds
budget by `638658`.  Thus the residual intervals are

```text
KoalaBear:   96151 <= e <= 1044238
Mersenne-31: 98230 <= e <= 1044241
```

Neither adjacent failure is unsafe.  No v4 first-match atom moves.

## Replay and provenance

The source theorem, contract, and independent audit are pinned at
`AllenGrahamHart/rs-mca-prize-dag@ad316370b`.  Replay here with

```bash
python3 experimental/verify_mca_full_lift_mean_centered_global_line_profile_v1.py
python3 -O experimental/verify_mca_full_lift_mean_centered_global_line_profile_v1.py
```

The verifier scans all 528 newly paid official supports and every prefix
threshold with exact integer arithmetic, reconstructs both adjacent failure
modes, and rejects four hostile mutations.
