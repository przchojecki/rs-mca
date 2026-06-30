# Aperiodic Hankel regular-minor toy certificate

This directory contains a deterministic Paper D v9
`aperiodic-hankel-eliminant-v1` certificate for the toy row

```text
F = F_17
D = F_17^*
n = 16
k = 8
a = 13
```

Regenerate or check the passing packet with:

```sh
python3 experimental/scripts/verify_aperiodic_hankel_regular_minor_toy.py \
  --write experimental/data/certificates/aperiodic-hankel-regular-minor-toy/f17_n16_k8_a13_regular_minor_certificate.json

python3 experimental/scripts/verify_aperiodic_hankel_regular_minor_toy.py \
  --check experimental/data/certificates/aperiodic-hankel-regular-minor-toy/f17_n16_k8_a13_regular_minor_certificate.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/aperiodic-hankel-regular-minor-toy/f17_n16_k8_a13_regular_minor_certificate.json
```

The standalone checker uses the Python `jsonschema` package for the schema
pass, then applies repo-specific arithmetic checks.

The directory also contains `invalid_bad_j_packet.json`, an intentionally
failing packet whose `j` field does not equal `n-A`.  The expected checker
result is:

```sh
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/aperiodic-hankel-regular-minor-toy/invalid_bad_j_packet.json
```

This is a toy atlas certificate, not a prize-row threshold claim.
