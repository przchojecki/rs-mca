# F17^32 M3 One-Spike Window Full-Hankel Ledger

This directory contains a compact all-window certificate for the non-proportional
one-spike branch in the Paper D v9 M3 regular window:

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

For each agreement `A`, with `j=512-A`, the verifier uses

```text
u_m = sum_{x in X} x^m,  |X| = j+1,
v_m = y^m,
```

where `X` is the first `j+1` points of the pinned subgroup row and `y` is the
next point.  The one-spike Cauchy-Binet formula gives a linear prefix regular
minor `C0(A)+Z*C1(A)` and hence one finite first-minor root in every row.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_one_spike_window_full_hankel.py \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-window-full-hankel/f17_32_n512_k256_m3_one_spike_window_full_hankel.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_window_full_hankel.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-window-full-hankel/f17_32_n512_k256_m3_one_spike_window_full_hankel.json
```

Result: all `42` finite first-minor roots are excluded from the full-Hankel
witness column by the row-shift-1 minor.  The projective endpoint `[0:1]`
contributes one full-Hankel witness before quotient-image charging, and each
endpoint has an explicit `c=2` quotient-image witness.  Therefore the
aperiodic full-Hankel projective residual upper bound is `0` in every checked
one-spike row.

Non-claims: this is a synthetic one-spike branch only, not arbitrary M3 row
data, not a finite-root quotient-image/support audit, and not a worst-case MCA
threshold theorem.
