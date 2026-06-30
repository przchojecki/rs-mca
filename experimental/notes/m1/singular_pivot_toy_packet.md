# Singular pivot toy packet

Status: **PROVED / AUDIT** for a finite toy packet.

This note records the first checked `pivot_atlas` packet in this branch.  It is
not a prize-row theorem; it is a small exact example showing how the v9 atlas
should represent a singular regular bucket once affine pivots close it.

The row is

```text
F = F_17, n = 10, k = 4, A = 8, j = 2, t = 4.
```

The syndrome pencil is nonzero and satisfies

```text
u = 5v,
rank H(v) = 2,
H(u) + ZH(v) = (Z+5)H(v).
```

Since the maximal regular minors are `3 x 3`, this matrix has rank less than
`3` for every finite slope.  Equivalently, the `rank_at_nodes` singular proof
tests the `j+2=4` slopes `0,1,2,3`; all maximal minors have degree at most
`3`, so vanishing at those nodes proves every maximal regular minor is the zero
polynomial.

The singular bucket is then closed by the exact support-image map.  For each
split co-support `T` of size `2`, let

```text
A_T = H(u) ell_T,
B_T = H(v) ell_T.
```

Because `A_T=5B_T`, every noncontained finite bad support with `B_T != 0`
contributes the same slope

```text
Z = -5 = 12 mod 17.
```

The verifier enumerates all `binom(10,2)=45` split co-supports:

```text
B_0 pivot: 42 supports
B_1 pivot:  2 supports
B_2 pivot:  0 supports
B_3 pivot:  0 supports
B = 0 contained residual: 1 support
```

Thus the pivot eliminant is `Z+5`, the exact root union is `{12}`, and the
declared aperiodic numerator is `1`.

Artifacts:

```text
experimental/data/certificates/singular-pivot-toy/
  f17_n10_k4_a8_singular_pivot_certificate.json
  f17_n10_k4_a8_singular_pivot_packet.json
```

Verification:

```sh
python3 experimental/scripts/verify_singular_pivot_toy_packet.py \
  --check-certificate experimental/data/certificates/singular-pivot-toy/f17_n10_k4_a8_singular_pivot_certificate.json \
  --check-packet experimental/data/certificates/singular-pivot-toy/f17_n10_k4_a8_singular_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/singular-pivot-toy/f17_n10_k4_a8_singular_pivot_packet.json
```

Next step: use the same packet shape only when an actual lower-agreement row
produces a genuine singular bucket.  Until then this is a machinery certificate,
not M3 row data.
