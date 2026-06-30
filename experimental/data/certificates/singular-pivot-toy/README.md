# Singular Pivot Toy Packet

This directory contains a small nonzero `F_17` v9 pivot-atlas packet.

```text
F = F_17, n = 10, k = 4, A = 8, j = 2, t = 4.
```

The syndrome pencil satisfies

```text
u = 5v,
rank H(v) = 2,
H(u) + Z H(v) = (Z+5)H(v).
```

Therefore every maximal `3 x 3` regular Hankel minor vanishes identically, so
the regular bucket is genuinely singular.  The affine support-image map is then
closed by the pivot cover `B_h != 0`: 42 split co-supports use pivot `B_0`, 2
use pivot `B_1`, and the remaining co-support has `B=0`, hence is contained
because `A=5B`.

The only finite slope produced by the noncontainment pivots is `Z=12`, the root
of `Z+5` over `F_17`.

Run:

```sh
python3 experimental/scripts/verify_singular_pivot_toy_packet.py \
  --check-certificate experimental/data/certificates/singular-pivot-toy/f17_n10_k4_a8_singular_pivot_certificate.json \
  --check-packet experimental/data/certificates/singular-pivot-toy/f17_n10_k4_a8_singular_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/singular-pivot-toy/f17_n10_k4_a8_singular_pivot_packet.json
```

Non-claims: this is a toy row only, not an `F_17^32` row-data packet, not a
prize-row threshold theorem, and not a uniform singular-pivot algorithm.
