# F17^32 M3 Zero-Slope Subtraction

This directory contains a narrow M4-style subtraction sidecar for the synthetic
top-window packet

```text
RS[F_17^32,H,256], |H|=512, 421 <= A <= 426.
```

The source v9 packet has exact regular-minor root union `{0}`.  The line-value
lift has `f(x)=0` for every `x in H`, so the finite slope `z=0` is the
zero-codeword tangent/common-code-line branch.  After that paid branch is
removed, the synthetic packet has residual aperiodic root union `empty`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/f17_32_n512_k256_a421_426_zero_slope_subtraction.json
```

Non-claims: this is a subtraction check for one synthetic packet, not actual
M3 row data, not a worst-case MCA bound, not a Prime192 subtraction table, and
not a singular-pivot packet.
