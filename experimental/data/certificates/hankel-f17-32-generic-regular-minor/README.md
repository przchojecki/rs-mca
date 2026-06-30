# F17^32 M3 Generic Regular-Minor Certificate

This directory contains a replayable certificate for generic maximal row-set
regular Hankel minors in the M3 window

```text
385 <= A <= 426
```

for `RS[F_17^32,H,256]`, `|H|=512`.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_generic_regular_minor.py \
  --write experimental/data/certificates/hankel-f17-32-generic-regular-minor/f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json

python3 experimental/scripts/verify_f17_32_m3_generic_regular_minor.py \
  --check experimental/data/certificates/hankel-f17-32-generic-regular-minor/f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json
```

The certificate proves that, for every agreement in the window, every maximal
row-set minor is not identically zero as a generic Hankel-pencil determinant
and has exact degree `j+1`.  Across the window this covers
`155193154203428426778689566118132250614039201839551` formal row-set charts.
It also keeps a concrete shifted-Vandermonde audit for the `1806` contiguous
charts.  It does not prove any particular deployed syndrome pencil is
nonsingular, enumerate roots over `F_17^32`, or clear the `2^-128` safe-side
budget.
