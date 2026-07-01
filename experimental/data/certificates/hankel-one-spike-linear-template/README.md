# Hankel One-Spike Linear Template

This directory contains the deterministic certificate for the M1/M3 one-spike
linear determinant template.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_one_spike_linear_template.py \
  --write experimental/data/certificates/hankel-one-spike-linear-template/hankel_one_spike_linear_template_certificate.json

python3 experimental/scripts/verify_m1_hankel_one_spike_linear_template.py \
  --check experimental/data/certificates/hankel-one-spike-linear-template/hankel_one_spike_linear_template_certificate.json
```

This is a reusable algebraic template for future v9 packets, not an actual
`F_17^32` safe-side row bound.
