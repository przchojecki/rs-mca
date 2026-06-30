# F17^32 Hankel Row Descriptor

This directory pins the concrete row/domain data needed before M3 regular-window
packets can be generated for

```text
RS[F_17^32,H,256],    |H| = 512.
```

The descriptor fixes:

```text
field model:       polynomial basis over F_17
modulus encoding:  low-degree-first
domain:            order-512 multiplicative subgroup
domain hash:       hash of the encoded domain list
M3 window:         385 <= A <= 426
```

Regenerate and check:

```sh
python3 experimental/scripts/emit_f17_32_hankel_row_descriptor.py \
  --write experimental/data/certificates/hankel-f17-32-row-descriptor/f17_32_n512_k256_hankel_row_descriptor.json

python3 experimental/scripts/emit_f17_32_hankel_row_descriptor.py \
  --check experimental/data/certificates/hankel-f17-32-row-descriptor/f17_32_n512_k256_hankel_row_descriptor.json
```

This descriptor does not supply syndrome-pencil line data and does not compute
any regular minor.  Its purpose is to make the field/domain input to future
`F_17^32` packets canonical and replayable.
