# Finite Proxy-Occupancy Inversion (not the extremality functional)

## Claim

The packet records finite split-locator alignment rows where a non-null
aperiodic slope fiber exceeds the best point-dictator occupancy in the same
slope fiber.

## Status

**Status:** EXPERIMENTAL / AUDIT. Finite inversion of a NON-CANONICAL within-bucket occupancy proxy (aperiodic-aligned total-count vs per-point subcount). It is NOT a counterexample to prop:v13-johnson-exchange (a Johnson-exchange collision inequality, separately PASS-on-range in the exchange-compression packet) and NOT to the N_w(z) <= N_w(0) mode-at-null statement; the proxy differs from both.

## Parameters

- Prime fields `F_5`, `F_7`, `F_11`, `F_13`, and `F_17`.
- `q_gen = q_line = q_chal = p` in every row.
- Domains are multiplicative subgroups `mu_n <= F_p^*`.
- The checked object is split-locator alignment for signed locator
  coefficients of degree `j`, with aperiodic supports tagged by cyclic
  periodicity scale.

## Existing Paper Dependency

This is a finite test for the worst-case argmax gap left open by the
first-moment calculation and related point-dictator extremality heuristic.

## Proof Idea Or Experiment

For every `j`-subset support, the scanner computes the split-locator
coefficients, evaluates the recorded Hankel syndrome forms for `u` and `v`,
and places the support into the unique slope fiber where `A(l)=z B(l)` with
`B(l) != 0`. For each slope it compares the aperiodic occupancy against the
largest point-dictator occupancy in the same fiber.

The verifier reconstructs the full table with exact integer arithmetic and
checks every recorded flagged example.

The committed scanner uses exact CPU enumeration for these small rows. It does
not implement a CuPy or RawKernel accelerator path.

## Ledger Impact

The finite rows show that the tested non-null aperiodic fiber can exceed the
best point-dictator occupancy under this proxy. This records a proxy inversion
only; it does not block the named exchange-compression or mode-at-null
functionals.

## Constants

The recorded packet includes:

```text
F_5,n=4,j=2,codim=1
F_7,n=6,j=2,codim=1
F_7,n=6,j=3,codim=1
F_11,n=10,j=3,codim=2
F_13,n=12,j=3,codim=2
F_17,n=16,j=3,codim=2
F_17,n=16,j=4,codim=2
```

The `F_17` rows are included as the split-locator oracle gate.

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/mode_at_null_extremality.py --emit-defaults
py -3.13 experimental/scripts/verify_mode_at_null.py --check experimental/data/certificates/mode-at-null/mode_at_null_rows.json
```

## Non-Claims

This does not prove a global worst-case bound, does not resolve `prob:band`,
and does not redo the first-moment calculation. It is a finite extremality
test for the recorded alignment family.
