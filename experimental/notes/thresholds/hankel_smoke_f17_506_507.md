# M2 Hankel Smoke Packet for the F17^32 Threshold Row

**Status:** PROVED-SMOKE-PACKET / AUDIT.

**Date:** 2026-06-30.

This note records the M2 smoke test from `towards-prize.md`.  It does not add
a new theorem.  It packages the already-settled high-agreement finite-slope
support-wise MCA threshold for

```text
C = RS[F_17^32,H,256],    |H| = 512,
q_line = 17^32.
```

The proof input is the promoted high-agreement tangent staircase:

```text
LD_sw(C,a)=n-a+1
```

in the range

```text
n-a <= floor((n-k)/3).
```

For `n=512`, `k=256`, this exact range starts at `a=427`, so both `a=506` and
`a=507` are inside it.

## Threshold rows

Since

```text
floor(17^32 / 2^128) = 6,
6*2^128 < 17^32 < 7*2^128,
```

the settled finite-slope support-wise MCA rows are:

```text
A = 506, r = 6: LD_sw = 7, unsafe;
A = 507, r = 5: LD_sw = 6, safe.
```

Equivalently, the largest safe closed integer radius is `5/512`, and the first
unsafe closed integer radius is `6/512 = 3/256`.  As a real supremum, the safe
interval is `[0,6/512)`.

## Packet interpretation

The packet

```text
experimental/data/certificates/hankel-smoke-f17-506-507/
  f17_32_n512_k256_a506_507_hankel_smoke_packet.json
```

uses the v9 aperiodic schema but declares the exact-agreement buckets `empty`
after removing the tangent/common-code-line ledger.  Thus the declared
aperiodic numerator is `0`.

This is intentional: M2 is a format test on a row whose threshold is already
known.  It should not be read as a new aperiodic eliminant proof.

## Verification

Run:

```sh
python3 experimental/scripts/verify_hankel_smoke_f17_506_507.py
python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_n512_k256_a506_507_hankel_smoke_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/hankel-smoke-f17-506-507/invalid_missing_removed_ledger_ref_packet.json
```
