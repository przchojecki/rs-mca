# Crossing Localization

Status: PROVED.

Source DAG node: `crossing_localization`.

## Statement

For a fixed row, let `B_C(a)` be the certified unsafe count at integer agreement
index `a`, and let `B*` be the row challenge budget. Since `B_C(a)` is finite,
integer-valued, and nonincreasing in `a`, a bracket

```text
B_C(a_lo - 1) > B*
B_C(a_hi) <= B*
```

contains a unique first safe index `a*` satisfying

```text
B_C(a* - 1) > B* >= B_C(a*).
```

If the real corridor has width `w`, it contains at most `ceil(w) + 1` integer
grid points. Thus the threshold problem reduces to finitely many pointwise
integer decisions in the corridor.

## Proof

Increasing the agreement index removes admissible witnesses from the counted
set, so `B_C(a)` is nonincreasing. It is integer-valued because it counts a
finite certificate set.

Given the bracket above, define `a*` to be the first integer `a` in
`[a_lo, a_hi]` with `B_C(a) <= B*`. Existence follows from
`B_C(a_hi) <= B*`. Minimality gives `B_C(a* - 1) > B*`, and the definition gives
`B_C(a*) <= B*`. Since `B*` is integer-valued, this is the displayed adjacent
crossing inequality.

The number of integer grid points in an interval of real width `w` is at most
`ceil(w) + 1`. Therefore an already-computed corridor of width two or less
leaves only two or three integer agreements to decide. No asymptotic estimate is
used in this reduction.

## Non-Claims

This packet proves only the monotone integer-staircase localization step. It
does not prove the pointwise safe upper certificate `U(a*) <= B*`, the unsafe
lower certificate `L(a*-1) > B*`, or any row-level adjacent theorem.

## Replay

```bash
python3 experimental/scripts/verify_crossing_localization.py --emit
python3 experimental/scripts/verify_crossing_localization.py \
  --check experimental/data/certificates/crossing-localization/crossing_localization.json
```
