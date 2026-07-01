# F17^32 M3/M4 Affine-Pivot Compression

Status: PROVED / AUDIT.

This packet records a chart-local determinant compression for the M3 regular
window

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For a maximal row set `R`, put

```text
M_R(z)=H_R(u)+z H_R(v).
```

Suppose `z0` is a finite affine pivot with `M_R(z0)` invertible, and factor the
direction block as

```text
H_R(v)=P_R Q_R,    rank H_R(v) <= r.
```

Then, with `w=z-z0`,

```text
det M_R(z)
  = det M_R(z0) * det(I_r + w Q_R M_R(z0)^(-1) P_R).
```

This is Sylvester's determinant identity applied after factoring out
`M_R(z0)`.  It has the same finite roots in the affine pivot chart, but the
determinant size drops from `(j+1) x (j+1)` to `r x r`.

For the current rank-6 boundary this means:

```text
A=385: 128 x 128 determinant -> 6 x 6 determinant
...
A=426:  87 x  87 determinant -> 6 x 6 determinant
```

The companion ambient sharpness packet shows rank `6` cannot be closed by
ambient rank and endpoint accounting alone.  This compression theorem identifies
the next finite-root object to attack: the common root table of the `6 x 6`
affine-pivot compressed determinants across row-set charts, plus a separate
endpoint payment or emptiness certificate.

This is not the synthetic low-rank Cauchy reduction.  It applies to any
regular bucket once a finite affine pivot `z0` with `M_R(z0)` invertible and a
rank factorization of `H_R(v)` are available.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_compression.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/f17_32_n512_k256_m3_m4_affine_pivot_compression.json

python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_compression.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/f17_32_n512_k256_m3_m4_affine_pivot_compression.json
```
