# F17^32 Zero-U Regular-Minor GCD Toy Packet

This directory contains a small `n=16`, `k=8` replay over the pinned
`F_17^32` polynomial-basis model using the closed-form
`zero_u_monomial` common-gcd method.

For a zero-`u` pencil, every nonzero audited maximal minor has the form
`c Z^(j+1)`.  The extractor therefore computes only the leading determinant of
each audited row set, takes the common gcd, and emits the exact root `{0}` with
a split-linear root certificate.  This exercises the large-field exact-root
path without enumerating `F_17^32`.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n16_k8_a13_zero_u_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-f17-32-zero-u-toy/f17_32_n16_k8_a13_zero_u_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-f17-32-zero-u-toy/f17_32_n16_k8_a13_zero_u_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-f17-32-zero-u-toy/invalid_zero_u_gcd_root_certificate_packet.json
```

Non-claims: this is a toy row over the actual extension-field model, not
F17^32 prize-row data and not a regular-window bound.
