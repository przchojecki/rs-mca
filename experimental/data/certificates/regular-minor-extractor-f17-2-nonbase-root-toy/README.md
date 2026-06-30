# Regular Hankel-Minor Extractor F17^2 Non-Base-Root Toy

This directory contains a tiny extension-field regression for the regular
Hankel-minor extractor and v9 checker.

Input:

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json
```

The field model is

```text
F_17^2 = F_17[x]/(x^2 - 3).
```

At `A=4`, `n=5`, `k=2`, we have `j=1`, `t=2`, and the prefix minor is

```text
[[Z, x],
 [x, Z]]
```

so the determinant is `Z^2 - 3`.  Its roots are the two non-base elements
`x` and `-x`, encoded as `17` and `272` in the packet.

Regenerate and check:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json \
  --write experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/f17_2_n5_k2_a4_nonbase_root_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/f17_2_n5_k2_a4_nonbase_root_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/f17_2_n5_k2_a4_nonbase_root_packet.json
```

Negative control:

```sh
python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/invalid_reducible_field_model_packet.json
```

The negative packet must fail: it replaces the irreducible modulus `x^2-3` by
the reducible modulus `x^2-1`.
