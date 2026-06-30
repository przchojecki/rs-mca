# F17^32 Regular-Minor GCD Toy Packet

This directory contains a small `n=16`, `k=8` toy replay over the pinned
`F_17^32` polynomial-basis model.  It uses the same embedded-base-field
syndrome pencil as the prime-field gcd toy, but the field is large enough that
the extractor intentionally does not enumerate roots.

The packet therefore exercises the `regular_minor_gcd` degree-bound path needed
for large extension fields: it stores the common gcd of all audited contiguous
maximal row-set minors, verifies that gcd over `F_17^32`, and reports
`regular_root_bound_sum = 6` rather than an exact numerator.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n16_k8_a13_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-f17-32-toy/f17_32_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-f17-32-toy/f17_32_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-f17-32-toy/invalid_extension_gcd_nondivisor_packet.json
```

Non-claims: this is a toy row over the actual extension-field model, not
F17^32 prize-row data and not a regular-window bound.
