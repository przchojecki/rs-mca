# Hankel Regular-Window Plan for the F17^32 Row

Status: AUDIT.

This note fixes the arithmetic target for the M3 regular-window audit in
`towards-prize.md`.

For the row

```text
C = RS[F_17^32,H,256],    |H| = 512,
```

we have `n=512` and `k=256`.  For exact agreement `A`, the v9 Hankel parameters
are

```text
j = n - A,
t = A - k.
```

The regular overdetermined condition is

```text
t >= j+1,
```

equivalently `2A >= n+k+1`.  Therefore the first regular agreement is

```text
A = ceil((512+256+1)/2) = 385.
```

The tangent-exact theorem starts at

```text
A = n - floor((n-k)/3) = 512 - 85 = 427.
```

Thus the first prize-facing non-tangent regular window is exactly

```text
385 <= A <= 426.
```

The concrete field/domain descriptor for this row is

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
  f17_32_n512_k256_hankel_row_descriptor.json
```

with domain hash

```text
35904a892e0319b3805e91438ec2733427a351a72ce9654428d6a33bd3575b92
```

For the prefix maximal minor with rows `0..j` and columns `0..j`, the largest
syndrome index used is `2j`.  Across the window this ranges from `254` down to
`172`, so every prefix minor is syntactically available from a syndrome vector
of length `n-k=256`.  The full Hankel window also uses no index beyond `255`.

The minor sizes run from `128` at `A=385` down to `87` at `A=426`.  Interpolating
one determinant polynomial per agreement would require `4557` determinant
evaluations in total.

The important negative audit is that degree bounds alone cannot close the
safe-side budget.  The finite-slope `2^-128` budget is

```text
floor(17^32 / 2^128) = 6,
```

while the regular degree-bound sum over this window is `4515`.  Therefore the
next useful M3 packet must compute actual root tables, or else identify the
first agreement where the regular bucket is singular and pass that residual to
pivot charts.  A degree-only certificate for this whole window would be far too
weak.

The follow-up note

```text
experimental/notes/m1/f17_32_m3_generic_regular_minor.md
```

proves that every maximal row-set minor is generically nonzero, with exact
degree `j+1`, for every agreement in this window.  Across the window this
covers
`155193154203428426778689566118132250614039201839551` formal row-set charts,
with `1806` contiguous charts singled out as the practical first-search
subatlas.  Thus vanished regular minors for an actual syndrome pencil are
special singular strata, not a forced failure of the regular Hankel chart.

The first concrete large-field stress packet for this window is

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
  f17_32_n512_k256_a426_rank_witness_packet.json
```

It uses a synthetic `F_17^32` syndrome pencil at `A=426` and proves a nonzero
regular minor by a rank witness.  This exercises the pinned field/domain
arithmetic, but it is not a worst-case safe-side bound and does not provide a
root table.

Reproduce the audit packet:

```sh
python3 experimental/scripts/plan_f17_regular_hankel_window.py \
  --check experimental/data/certificates/hankel-regular-window-f17-385-426/f17_32_n512_k256_regular_window_plan.json
```

Non-claims: this note does not compute any determinant over `F_17^32`, does not
enumerate root sets, and does not prove a safe-side MCA bound.
