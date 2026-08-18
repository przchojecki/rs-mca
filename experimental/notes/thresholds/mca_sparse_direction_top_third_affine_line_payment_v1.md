# MCA sparse-direction top-third affine-line payment v1

## Status

PROVED / EXACT FINITE CALIBRATION.

For an exact deficit layer `h=e-r`, every selected explanation misses at
most `r` exceptional agreement coordinates.  If `e-3r>=K`, any three
explanations share at least `K` exceptional agreements.  Restriction
injectivity synchronizes all normalized pair differences, so the entire
exact layer lies on one affine codeword line.

With `c=K-1` and `n=N-e`, outside-core packing gives

```text
L_r <= floor((n-c)/(m-e+r-c)).
```

Take all layers `0<=r<=floor((e-K)/3)` this way.  The remaining lower
deficits retain the positive punctured-Johnson cumulative profile.  A
uniform two-threshold estimate gives

```text
prefix <= (e-1)J_floor(e/2)+J_H,
H=e-floor((e-K)/3)-1.
```

On both official rows, conservative endpoint substitution proves
`J_floor(e/2)<=31` and `J_H<=47` for every `e<d`.  The affine-line sum is
termwise nondecreasing in `e` and is therefore maximal at `e=d-1`:

```text
KoalaBear:   31*(67472-2)+47+9405342 = 11496959;
Mersenne-31: 31*(67448-2)+47+9405365 = 11496238.
```

This pays every sparse-direction support.  The remaining full-lift
intervals are

```text
KoalaBear:   67472 <= e <= 1044238
Mersenne-31: 67448 <= e <= 1044241.
```

The result does not treat `e>=d` or prove either deployed row.

## Replay

```bash
python3 experimental/verify_mca_sparse_direction_top_third_affine_line_payment_v1.py
```

The verifier checks the endpoint indices, raw Johnson fractions, grouped
floor sums, exact row comparisons, a sharp triple-overlap model, and hostile
mutations.
