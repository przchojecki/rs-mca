# Projective Regular-Minor GCD Toy Packet

This directory contains a finite `F_17`, `n=16`, `k=8` projective-line v9
replay for the `regular_minor_gcd` packet mode.

For a common-gcd regular bucket, the projective endpoint `[0:1]` is excluded
when at least one audited maximal-minor homogenization has nonzero top
coefficient.  The packet records the top coefficient of every audited minor,
not only the top coefficient of the common gcd.  In this toy, infinity is empty
for `A=13,14,15,16`, so the projective numerator remains the finite root union
`{11}`.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_projective_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-projective-toy/f17_n16_k8_a13_projective_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-projective-toy/f17_n16_k8_a13_projective_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-projective-toy/invalid_bad_projective_gcd_top_packet.json
```

Non-claims: this is a toy-row projective endpoint replay, not an `F_17^32`
regular-window root table and not a threshold-pinning certificate.
