# F17^32 M3 Syndrome-Realizability Certificate

This directory records the row-realizability reduction for the M3 regular
window

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

For every exact agreement in this window,

```text
t+j = (A-k)+(n-A) = n-k = 256.
```

Since `256 <= |H|`, the subgroup inverse-Fourier section proves that every
length-256 syndrome vector is realized by explicit line values on `H`.  Applied
to both `u` and `v`, every length-256 syndrome pencil is actual line-valued row
data for the pinned subgroup row.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_syndrome_realizability.py \
  --check experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/f17_32_n512_k256_m3_syndrome_realizability_certificate.json
```

Non-claims: this does not compute root tables, remove quotient/tangent ledgers,
or prove a worst-case MCA bound.  It says the remaining M3 regular-window task
is universal syndrome-pencil classification, not row-data construction.
