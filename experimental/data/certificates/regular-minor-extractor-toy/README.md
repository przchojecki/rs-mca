# Regular Hankel-Minor Extractor Toy Packet

This directory contains a deterministic output packet for the reusable regular
Hankel-minor extractor.

Input:

```text
experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json
```

Output:

```text
f17_n16_k8_a13_regular_minor_extractor_packet.json
```

Regenerate and check:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json \
  --write experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-toy/invalid_synthetic_threshold_scope_packet.json
```

This is a reusable extractor smoke test.  It is not a prize-row threshold
claim and does not provide an extension-field adapter for the `F_17^32`
regular window.  The valid toy packet declares this through `claim_scope`; the
negative fixture checks that synthetic evidence cannot mark itself as
threshold-pinning material.
