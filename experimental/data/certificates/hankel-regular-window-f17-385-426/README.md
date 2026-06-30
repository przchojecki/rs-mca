# F17^32 Regular Hankel-Window Plan

This directory contains an audit packet for the M3 regular non-tangent window
from `towards-prize.md`.

Row:

```text
RS[F_17^32,H,256],    |H| = 512.
```

Window:

```text
385 <= A <= 426.
```

In this window the regular overdetermined condition `t >= j+1` holds, while
the high-agreement tangent-exact theorem has not yet started.  The packet
records the exact `j`, `t`, prefix-minor size, degree bound, interpolation
cost, and syndrome-index requirements for every agreement in the window.

Regenerate and check:

```sh
python3 experimental/scripts/plan_f17_regular_hankel_window.py \
  --write experimental/data/certificates/hankel-regular-window-f17-385-426/f17_32_n512_k256_regular_window_plan.json

python3 experimental/scripts/plan_f17_regular_hankel_window.py \
  --check experimental/data/certificates/hankel-regular-window-f17-385-426/f17_32_n512_k256_regular_window_plan.json
```

This is an audit and extraction plan, not a proof packet for the prize row.  It
does not compute determinants over `F_17^32`, enumerate roots, prove a safe-side
MCA bound, or classify singular buckets.
