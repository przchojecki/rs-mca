# W_z Slope-Sweep Aperiodic Incidence Check

## Claim

The packet records exact split-locator counts for small finite `W_z`
Hankel-pencil rows. For every slope `z` in the base field, it counts split
locators solving `A(l)+zB(l)=0`, separates aperiodic from periodic supports,
and flags slopes whose aperiodic count exceeds the naive density ceiling.

## Status

EXPERIMENTAL / AUDIT. The finite counts are replayed exactly; no theorem for
the full aperiodic kernel is claimed.

## Parameters

- Prime fields `F_31` and `F_41`.
- `q_gen = q_line = q_chal = p` in every row.
- Domains are multiplicative subgroups `mu_n <= F_p^*`.
- The recorded split-locator degree is `j=3`.

## Existing Paper Dependency

This is a finite stress test for the `W_z` syndrome-annihilator object used on
the `(A)` side of the master-flatness program.

## Proof Idea Or Experiment

The scanner records deterministic source vectors `f` and `g`, computes the
syndrome sequences `u` and `v`, and for each slope counts degree-`j` split
locators whose coefficient vector solves the first recorded Hankel-pencil
equations. The verifier reconstructs every component with exact integer
arithmetic and recomputes the complete slope table.

## Ledger Impact

The `F_41` deep-gate row has maximum aperiodic occupancy `1`, matching the
recorded `n-a+1` gate. The `F_31` and `F_41` sweep rows record finite
over-density flags against the naive density ceiling for this deterministic
Hankel pencil.

## Constants

```text
deep_gate_f41:  p=41, n=40, j=3, codim=3
band_sweep_f31: p=31, n=30, j=3, codim=2
band_sweep_f41: p=41, n=40, j=3, codim=2
```

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/wz_slope_sweep.py --emit-defaults
py -3.13 experimental/scripts/verify_wz_slope_sweep.py --check experimental/data/certificates/wz-slope-sweep/deep_gate_f41.json experimental/data/certificates/wz-slope-sweep/band_sweep_f41_f31.json
```

## Scope

This is not a proof of `prob:band`, not a complete search over received lines,
and not the full `F_41,n=40,j=10` accelerator run. It is an exact small-row
Hankel-pencil incidence packet with CPU replay.
