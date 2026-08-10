# Denominator-root puncture-trivialization certificate

This packet corroborates the two local theorems in
`experimental/notes/m2/denominator_root_puncture_trivialization.md`.

Run from the repository root:

```bash
python3 experimental/scripts/verify_denominator_root_puncture_trivialization.py --check
python3 -O experimental/scripts/verify_denominator_root_puncture_trivialization.py --check
python3 experimental/scripts/verify_denominator_root_puncture_trivialization.py --tamper-selftest
python3 -O experimental/scripts/verify_denominator_root_puncture_trivialization.py --tamper-selftest
```

The checker uses only the Python standard library. It pins the upstream
scalar-locator definition and pole-tolerant cancellation theorem, checks the
two deployed rows, replays finite-field puncture and pole-defect seams,
exhausts small slope-recovery instances, checks shadow disjointness, and
proves the exact non-payment fence without floating point.

The universal theorem is the proof in the note. The checker does not prove a
row-sharp cardinality bound, `(S)`, `(A)`, `(E)`, or an adjacent endpoint.
