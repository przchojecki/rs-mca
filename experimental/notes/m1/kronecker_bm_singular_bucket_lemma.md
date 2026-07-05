# Kronecker/BM Singular-Bucket Check

## Claim

The packet records finite nonzero Hankel pencils `H(u)+Z H(v)` whose determinant
vanishes identically and whose split-locator occupants are periodic in the
recorded range.

## Status

EXPERIMENTAL / AUDIT. The rows are exact finite checks; no asymptotic
singular-pencil theorem is claimed.

## Parameters

- Prime fields `F_7`, `F_11`, `F_13`, and `F_17`.
- `q_gen = q_line = q_chal = p` in every row.
- Domains are multiplicative subgroups `mu_n <= F_p^*`.
- Each row uses a recorded periodic split-locator kernel vector and two
  nonzero Hankel sequences satisfying the same recurrence.

## Existing Paper Dependency

This is a finite test for the singular bucket associated with
`lem:singular-pencil` and the class of identically rank-deficient Hankel
pencils.

## Proof Idea Or Experiment

For each row, a periodic split locator supplies a constant kernel vector
`lambda`. The scanner builds two Hankel sequences obeying the recurrence
defined by `lambda`, so both `H(u) lambda = 0` and `H(v) lambda = 0`. It then
enumerates all split locators in `Dloc_j(mu_n)` that lie in the common kernel
of both Hankel matrices and tags their periodicity scale.

The verifier recomputes the determinant polynomial of `H(u)+Z H(v)` over
`F_p[Z]`, confirms it is identically zero, checks the constant kernel chain,
and replays the full split-locator bucket.

The committed scanner uses exact CPU enumeration for these small rows. It does
not implement a CuPy or RawKernel accelerator path.

## Ledger Impact

The recorded finite rows have no aperiodic singular-bucket occupants. This is
pass-on-range evidence for the singular branch, not a proof of the general
statement.

The pass-on-range statement is over the constant-kernel periodic-seed rows
enumerated here and does not claim that no aperiodic singular occupant exists
in general; it is a seeding-scoped finite check, evidence for
`cor:singular-deep` only within that scope.

## Constants

```text
F_7,n=6,j=2
F_11,n=10,j=2
F_13,n=12,j=3
F_17,n=16,j=4
```

The `F_17` row is the split-locator oracle gate.

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/kronecker_bm_singular_bucket.py --emit-defaults
py -3.13 experimental/scripts/verify_kronecker_bm_singular_bucket.py --check experimental/data/certificates/kronecker-bm-singular-bucket/singular_bucket_rows.json
```

## Non-Claims

This does not close the singular-pencil theorem, does not resolve `prob:band`,
and does not redo the split-top-chart collapse. It is a finite pass-on-range
packet for the recorded singular buckets.
