# F17^32 M3 Regular-Window Status

This directory contains a compact audit ledger for the Paper D v9 M3 regular
window

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

It hashes and cross-checks the regular-window plan, the generic all-row-set
minor certificate, the synthetic rank-witness family, the fixed top-window v9
packet, the explicit line-value lift of that fixed packet, and the reusable
subgroup syndrome-section theorem behind the lift.  It also references the
zero-slope subtraction sidecar showing that the fixed top-window packet's
synthetic root `{0}` is paid by the zero-codeword tangent branch, and the
extension-denominator audit showing that the line-value lift is genuinely
`F_17^32`-valued.  Its purpose is to make the frontier explicit: generic and
synthetic regular-minor facts are proved, while tangent/quotient-deduped actual-row root tables and
singular-bucket outcomes are still not supplied.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_regular_window_status.py \
  --check experimental/data/certificates/hankel-f17-32-m3-regular-window-status/f17_32_n512_k256_m3_regular_window_status.json
```

Non-claims: this is not a worst-case MCA bound, not actual M3 row data, not a
full quotient/tangent subtraction table, and not a singular-pivot packet.
