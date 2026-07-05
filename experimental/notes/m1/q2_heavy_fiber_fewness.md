# Q2 Heavy-Fiber Fewness Ledger

## Claim

The packet records exact r=3 and r=4 heavy-tail ledgers for top-prefix locator
fibers on the recorded toy rows.

## Status

EXPERIMENTAL / AUDIT.

## Parameters

- `q_gen = q_line = q_chal = 97` or `257`, row by row.
- Domain `mu_16`.
- Support size `8`.
- Prefix widths `2` and `3` over `F_97`, and prefix width `2` over `F_257`.

## Existing Paper Dependency

The packet targets the Q2 heavy-fiber fewness input associated with
`cor:periodic-support-count`. It is distinct from the r=2 prefix-collision
ledger and from aggregate `Gamma_r` moment scans.

## Proof Idea Or Experiment

The enumerator assigns every support to its top-prefix locator key and records
the complete finite fiber histogram. For r=3 and r=4 it computes the exact
power moment, unordered collision count, common-core histogram, pairwise
intersection-profile histogram, and Markov tail table using exact rational
arithmetic.

The checker enumerates the full recorded parameter space and recomputes each
fiber by direct elementary-symmetric assignment, rather than by multiplying
locator polynomials.

## Ledger Impact

This supplies exact finite tail data for the Q2 heavy-fiber fewness object. It
does not prove the quotient-fiber equidistribution upper theorem.

## Constants

The recorded rows are:

```text
F_97,mu_16,support=8,width=2
F_97,mu_16,support=8,width=3
F_257,mu_16,support=8,width=2
```

No recorded tail exceeds its exact `excess/T^r` bound.

## Reproducibility

```powershell
py -3.13 experimental/scripts/verify_q2_heavy_fiber_fewness.py --emit-defaults
py -3.13 experimental/scripts/verify_q2_heavy_fiber_fewness_check.py --check experimental/data/certificates/q2-heavy-fiber-fewness/q2_heavy_fiber_fewness.json
```

## Non-Claims

This is not a worst-case equidistribution theorem, not a deployed-size tail
bound, and not a resolution of `prob:band`.
