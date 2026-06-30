# Extension Regular-Minor GCD Toy Packet

This directory contains the first polynomial-basis extension-field v9 packet
using the `regular_minor_gcd` certificate mode.

The input is the `F_17^2`, `n=16`, `k=8` embedded-base-field toy.  The packet
audits all contiguous maximal row-set minors, stores their determinant
polynomials with coefficients encoded as base-17 low-to-high integers, and
checks that the reported common gcd divides every audited minor over
`F_17[x]/(x^2-3)`.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-f17-2-toy/f17_2_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-f17-2-toy/f17_2_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-f17-2-toy/invalid_missing_extension_gcd_roots_packet.json
```

Non-claims: this is a finite extension-field toy replay, not an F17^32
regular-window bound.
