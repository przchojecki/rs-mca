# F17^32 M3 Regular-Window Status

This directory contains a compact audit ledger for the Paper D v9 M3 regular
window

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

It hashes and cross-checks the regular-window plan, the generic all-row-set
minor certificate, two synthetic all-window families, the fixed top-window v9
packet, the explicit line-value lift of that fixed packet, and the reusable
subgroup syndrome-section theorem behind the lift.  The synthetic families are
the closed-form rank-witness family with root union `{0}` and the rank-2
low-rank family with degree-bound-only aggregate `84`.

The ledger also references the M3 syndrome-realizability certificate, which
proves that every length-256 syndrome pencil in this window is realized by
explicit line values on the pinned subgroup row.  The zero-slope subtraction
sidecar shows that the fixed top-window packet's synthetic root `{0}` is paid
by the zero-codeword tangent branch, the extension-denominator audit shows that
the line-value lift is genuinely `F_17^32`-valued, and the projective endpoint
sidecar proves that `[0:1]` is empty for the fixed top-window regular minors.
Its purpose is to make the frontier explicit: generic and synthetic
regular-minor facts are proved and row-realizability is discharged, while
universal tangent/quotient-deduped root tables and singular-bucket outcomes are
still not supplied.

For `A=421..426`, the ledger also records the fixed synthetic packet's M4
mini-table:

```text
B_tan=1, B_quot_support=B_quot_image=B_ext=0,
B_ap_regular_before_removed=1, B_ap_after_removed=0,
B_projective_infinity=0, deduped total upper bound=1 <= budget 6.
```

This is a no-double-counting check for the fixed synthetic packet only.

The ledger also imports the proportional-pencil tangent lemma.  Since
`t+j=256` is the full stored syndrome length for every agreement in this
window, any proportional syndrome pencil `u=c v` has no hidden tail check:
after the tangent/common-code-line ledger is removed, that branch leaves
aperiodic residual `0`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_regular_window_status.py \
  --check experimental/data/certificates/hankel-f17-32-m3-regular-window-status/f17_32_n512_k256_m3_regular_window_status.json
```

Non-claims: this is not a worst-case MCA bound, not a universal M3 row outcome,
not a full quotient/tangent subtraction table, and not a singular-pivot packet.
