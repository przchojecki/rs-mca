# F17^32 M3 Zero-Slope Subtraction Sidecar

Status: PROVED / AUDIT for the synthetic rank-witness packets.

This directory contains a deterministic M4-style subtraction sidecar for the
synthetic M3 rank-witness packets in:

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/
```

The raw regular packets have root union `{0}`.  The sidecar checks that every
source input has identically zero `u` syndrome.  Since

```text
Syn(f + Zg) = u + Z v,
```

the root `Z=0` is a zero-syndrome codeword/common-code-line slope.  It is
therefore paid by the tangent ledger, leaving residual synthetic aperiodic
numerator `0` for these packets.

This is not a worst-case M3 row theorem and does not subtract quotient,
extension, or singular-pivot ledgers.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py \
  --write experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/f17_32_n512_k256_rank_witness_zero_slope_subtraction.json

python3 experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/f17_32_n512_k256_rank_witness_zero_slope_subtraction.json
```
