# Regular Hankel-Minor Projective Toy Packet

This directory contains the projective-line replay of the finite
regular-minor extractor toy.

Input:

```text
experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_projective_toy.json
```

Output:

```text
f17_n16_k8_a13_projective_regular_minor_packet.json
```

Regenerate and check:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_projective_toy.json \
  --write experimental/data/certificates/regular-minor-extractor-projective-toy/f17_n16_k8_a13_projective_regular_minor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_projective_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-projective-toy/f17_n16_k8_a13_projective_regular_minor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-projective-toy/f17_n16_k8_a13_projective_regular_minor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-projective-toy/invalid_missing_projective_infinity_regular_packet.json
```

This is the same toy syndrome pencil as the finite-affine replay, but with
`sampler=projective_line`.  The packet records the homogenized determinant at
`[0:1]` for each regular minor.  In this toy all four top coefficients are
nonzero, so infinity is empty and the projective numerator remains the finite
root-union size.
