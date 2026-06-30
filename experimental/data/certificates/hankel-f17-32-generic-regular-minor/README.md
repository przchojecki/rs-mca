# F17^32 M3 Generic Regular-Minor Certificate

This directory contains a replayable certificate for the generic contiguous
regular Hankel row-set minors in the M3 window

```text
385 <= A <= 426
```

for `RS[F_17^32,H,256]`, `|H|=512`.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_generic_regular_minor.py \
  --write experimental/data/certificates/hankel-f17-32-generic-regular-minor/f17_32_n512_k256_m3_generic_contiguous_regular_minor_certificate.json

python3 experimental/scripts/verify_f17_32_m3_generic_regular_minor.py \
  --check experimental/data/certificates/hankel-f17-32-generic-regular-minor/f17_32_n512_k256_m3_generic_contiguous_regular_minor_certificate.json
```

The certificate proves that, for every agreement in the window, every
contiguous maximal row-set minor with row set `s..s+j` is not identically zero
as a generic Hankel-pencil determinant and has exact degree `j+1`.  Across the
window this gives `1806` generic contiguous charts.  It does not prove any
particular deployed syndrome pencil is nonsingular, enumerate roots over
`F_17^32`, or clear the `2^-128` safe-side budget.
