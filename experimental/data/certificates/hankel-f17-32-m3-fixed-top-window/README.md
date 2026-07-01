# F17^32 M3 Fixed Top-Window Packet

Status: PROVED / AUDIT for this synthetic finite replay.

This directory contains one replayable `aperiodic-hankel-eliminant-v1` packet
covering the selected top subrange

```text
421 <= A <= 426
```

in the M3 regular non-tangent window of `RS[F_17^32,H,256]`, `|H|=512`.

The input uses the first `92` elements of the pinned `F_17^32` row descriptor
and the fixed synthetic syndrome pencil

```text
u_m = 0,
v_m = sum_i x_i^m.
```

The extractor checks the prefix row set of size `j+1` for each exact agreement.
It emits

```text
Delta_A(Z) = c_A Z^(j+1),
roots = {0}.
```

The packet has root union `{0}` across the six exact agreements and declared
aperiodic numerator `1`.  It is a selected-subrange checker replay, not a
worst-case row bound or a paid-root subtraction table.

Regenerate and check:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 421 \
  --agreement-max 426 \
  --witness-prefix-count 92 \
  --write experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a421_426_fixed_prefix92_input.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 421 \
  --agreement-max 426 \
  --witness-prefix-count 92 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a421_426_fixed_prefix92_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a421_426_fixed_prefix92_input.json \
  --write experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/f17_32_n512_k256_a421_426_fixed_prefix92_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a421_426_fixed_prefix92_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/f17_32_n512_k256_a421_426_fixed_prefix92_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/f17_32_n512_k256_a421_426_fixed_prefix92_packet.json
```
