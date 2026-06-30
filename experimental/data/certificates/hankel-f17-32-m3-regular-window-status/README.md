# F17^32 M3 Regular-Window Status

This directory contains a compact audit ledger for the Paper D v9 M3 regular
window

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

It hashes and cross-checks the regular-window plan, the generic all-row-set
minor certificate, the synthetic rank-witness family, and the fixed top-window
v9 packet.  Its purpose is to make the frontier explicit: generic and
synthetic regular-minor facts are proved, while actual-row root tables and
singular-bucket outcomes are still not supplied.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_regular_window_status.py \
  --check experimental/data/certificates/hankel-f17-32-m3-regular-window-status/f17_32_n512_k256_m3_regular_window_status.json
```

Non-claims: this is not a worst-case MCA bound, not actual M3 row data, not a
quotient/tangent subtraction table, and not a singular-pivot packet.
