# Regular-Minor GCD Toy Packet

This directory contains the first v9 packet using the `regular_minor_gcd`
certificate mode.

The input is the `F_17`, `n=16`, `k=8` regular-minor toy, but with all
contiguous maximal row-set minors audited.  For each exact agreement, the
packet stores the determinant polynomial for every audited row set, the common
gcd polynomial, and the exact roots of that gcd.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-toy/f17_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-toy/f17_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-toy/invalid_omitted_gcd_root_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-toy/invalid_bad_minor_replay_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-toy/invalid_proper_gcd_divisor_packet.json
```

Non-claims: this is a finite prime-field toy replay, not an F17^32
regular-window bound.  A companion `F_17^2` replay now exercises the same
common-gcd gate over a polynomial-basis extension field.

The `invalid_bad_minor_replay_packet.json` fixture keeps gcd divisibility and
the root table intact, but scales one recorded minor away from the SHA-checked
Hankel input.  The generic checker must reject it by replaying determinant
values from the extractor input.  The `invalid_proper_gcd_divisor_packet.json`
fixture advertises the proper common divisor `1`; it must fail because the
reduction needs the greatest common divisor, not just any divisor of all
audited minors.
