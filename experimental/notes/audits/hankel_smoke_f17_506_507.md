# Hankel smoke packet for F_17^32 agreements 506 and 507

**Status:** AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note records the v9 packet smoke test requested in `towards-prize.md`.
The row is the already-settled finite support-wise MCA row

```text
C = RS[F_17^32,H,256],
n = 512,
k = 256.
```

The source certificate is

```text
experimental/data/certificates/high-agreement-threshold-package/
  f17_512_high_agreement_threshold_certificate.json
```

and the smoke packet is

```text
experimental/data/certificates/hankel-smoke-f17-506-507/
  f17_32_hankel_smoke_506_507_packet.json
```

## What the packet checks

The generator replays the source certificate's pure finite-slope MCA rows at
`A=506` and `A=507`.  It checks:

```text
A=506: j=6, t=250, LD_sw numerator = 7, unsafe at 2^-128;
A=507: j=5, t=251, LD_sw numerator = 6, safe at 2^-128.
```

These are the high-agreement tangent staircase values

```text
LD_sw(C,A) = n-A+1
```

inside the exact tangent range.  In v9 packet language, this smoke test charges
those numerators to removed tangent ledgers and declares the residual aperiodic
root union empty.

## Non-claims

This is not a new proof of the high-agreement theorem, not a regular-minor
calculation for `F_17^32`, and not a lower-agreement M1 theorem.  It is a
schema and ledger-format test on a row whose answer is already known.

## Verification

Run:

```sh
python3 experimental/scripts/verify_hankel_smoke_f17_506_507.py
python3 experimental/scripts/verify_hankel_smoke_f17_506_507.py \
  --check experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_hankel_smoke_506_507_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_hankel_smoke_506_507_packet.json
```
