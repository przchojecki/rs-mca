# Gamma Dyadic Rung-Transfer Constants

## Claim

For the recorded dyadic toy rows, the image-level transfer from exact
scale-`c` parent supports to exact aperiodic quotient supports has
`kappa_c = 1`. The packet also records the separate power-curve sampler
multiplicity for degrees `1`, `2`, and `3`.

## Status

EXPERIMENTAL / AUDIT.

## Parameters

- `q_gen = q_line = q_chal = 97`.
- `n = 2^m` for `m in {2,3,4,5}` and `j = n/2`.
- Dyadic scales are `c in {2,4,8}` when `c` divides both `n` and `j`.

## Existing Paper Dependency

The packet targets Route-gamma for `prob:band` and cites
`def:periodicity-scale`, `cor:periodic-support-count`,
`lem:v13-quot-pullback`, and `thm:fiber-descent`.

## Proof Idea Or Experiment

The enumerator uses the integrated reduction primitives to compare the
`g(Y) -> g(X^c)` pullback image with the parent supports that are unions of
complete `c`-fibers. It then applies the intrinsic stabilizer filter to isolate
exact scale `c` and compares that count with exact aperiodic quotient supports.

The independent checker ignores the pullback map and recomputes the same
constants by brute support enumeration and the closed inclusion-exclusion count
from `cor:periodic-support-count`.

## Ledger Impact

This measures the fold constant needed by the Route-gamma transfer object. It
is distinct from PR #329's rung-margin calculation: that item computes the
acceptance ceiling, while this packet measures the finite fold constant and
the separate sampler multiplicity on toy rows.

## Constants

```text
m  n   active c      identity transfer product
2  4   2             1
3  8   2,4           1
4  16  2,4,8         1
5  32  2,4,8         1
```

Sampler-adjusted products for degree `2` exceed the recorded acceptance
ceilings in the toy comparison table. Those are named finite over-ceiling
signals for the sampler-adjusted quantity only; the image-level transfer
constant remains `1`.

## Reproducibility

```powershell
py -3.13 experimental/scripts/verify_gamma_dyadic_rung_transfer.py --emit-defaults
py -3.13 experimental/scripts/verify_gamma_dyadic_rung_transfer_check.py --check experimental/data/certificates/gamma-dyadic-rung-transfer/gamma_dyadic_rung_transfer.json
```

## Non-Claims

This is not an asymptotic tower-transfer theorem, not a deployed-depth claim,
and not a resolution of `prob:band`.
