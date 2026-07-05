# A0 Witness-Bucket Periodicity Check

## Claim

The packet records exact agreement-support periodicity buckets for one
explicit pole-line-style slope in each of four small prime-field rows.

## Status

EXPERIMENTAL / AUDIT. The finite bucket counts are replayed exactly; no
asymptotic theorem is claimed.

## Parameters

- Prime fields `F_5`, `F_7`, `F_13`, and `F_17`.
- `q_gen = q_line = q_chal = p` in every row.
- The domain is a multiplicative subgroup `mu_n <= F_p^*`.
- The checked object is support-wise agreement for the recorded line
  `f + z g`, followed by cyclic-periodicity tagging of every support of size
  at least `a`.

## Existing Paper Dependency

This is a finite A0-style audit for the support-bucket step used when
separating aperiodic witness supports from paid periodic strata.

## Proof Idea Or Experiment

For each row the scanner records one explicit slope. The verifier reconstructs
the subgroup, checks that the base support is a nonzero parallel witness for
`f` and `g`, enumerates every support of size at least `a`, interpolates the
restricted word, and counts exactly those supports agreeing with a degree
`< k` polynomial. Each such support is then tagged by the cyclic
periodicity-scale test.

## Ledger Impact

The `F_7`, `F_13`, and `F_17` rows have only aperiodic agreement supports for
the recorded slope. The `F_5` row records one periodic support, which is useful
as a guard that the periodic detector is active.

## Constants

The recorded rows are:

```text
F_5:  n=4,  k=1, a=2
F_7:  n=6,  k=2, a=3
F_13: n=12, k=4, a=5
F_17: n=16, k=6, a=7
```

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/a0_witness_bucket_sweep.py --emit-defaults
py -3.13 experimental/scripts/verify_a0_witness_bucket.py --check experimental/data/certificates/a0-witness-bucket/f5.json experimental/data/certificates/a0-witness-bucket/f7.json experimental/data/certificates/a0-witness-bucket/f13.json experimental/data/certificates/a0-witness-bucket/f17.json
```

## Scope

This is not a full identity-prefix-floor conversion theorem, not a proof of the
corrected aperiodic bound, and not a complete search over all received lines.
It is a small exact witness-bucket packet with a visible periodic guard row.
