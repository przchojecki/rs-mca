# Regular Hankel-Minor Extractor F17^2 Toy Packet

This directory contains the polynomial-basis extension-field replay for the
regular Hankel-minor extractor.

Input:

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json
```

The field model is

```text
F_17^2 = F_17[x]/(x^2 - 3),
```

with modulus `[14, 0, 1]` in low-degree-first form.  Field elements in packet
root tables are encoded as base-17 low-to-high integers.

Regenerate and check:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json \
  --write experimental/data/certificates/regular-minor-extractor-f17-2-toy/f17_2_n16_k8_a13_regular_minor_extractor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-f17-2-toy/f17_2_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-toy/f17_2_n16_k8_a13_regular_minor_extractor_packet.json
```

This is an adapter replay, not a prize-row packet.  It verifies that the
extractor can interpolate regular minors and enumerate roots over an explicit
prime-power field before the `F_17^32` row-data adapter is supplied.
