# Hankel Smoke Packet: F17^32, Agreements 506/507

This directory is the M2 smoke test from `towards-prize.md`.

It packages the already-settled high-agreement finite-slope support-wise MCA
threshold for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The point is format validation, not a new theorem.  The proof input is the
high-agreement tangent staircase:

```text
LD_sw(C,a) = n-a+1
```

in the exact range `n-a <= floor((n-k)/3)`.  For this row, the relevant values
are

```text
A = 506: LD_sw = 7, unsafe at 2^-128;
A = 507: LD_sw = 6, safe at 2^-128.
```

Files:

```text
f17_32_n512_k256_a506_507_hankel_smoke_packet.json
  v9 schema-conforming packet.  It declares the aperiodic bucket empty after
  the tangent/common-code-line ledger is removed.

f17_32_n512_k256_a506_507_numerator_table.json
  root/numerator table for the known settled rows.
```

Verifier:

```sh
python3 experimental/scripts/verify_hankel_smoke_f17_506_507.py
python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_n512_k256_a506_507_hankel_smoke_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/hankel-smoke-f17-506-507/invalid_missing_removed_ledger_ref_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/hankel-smoke-f17-506-507/invalid_external_numerator_packet.json
```
