# Large fiber vs low energy at linear density R=2 (W53-M1)

## Status
EXPERIMENTAL. **Rung: MEASURED-SUPPORT** (no CE under strict bar).

## Phase 0
cube3 E=216.

## Linear density range
densities in [0.25, 0.5], N in [8, 16], R=2.

## Findings (cert-sourced)
```text
n_linear = 108
any_counterexample = false
max_f_low_linear = 32
max_ratio_low_linear ≈ 4.07  (below CE bar max(8,N))
n_largest_near_sidon = 106/108
```
Honest: largest fibers often sit near the Sidon energy floor (minimal energy),
so the naive "large => high energy" hope fails at the CS/Sidon level. That does
not by itself yield a payment CE under the strict exp-large ratio bar.

## CE policy
density>=0.25, N>=10, max_f_low>=max(8,N), ratio_low>=max(8,N).

## Dual routes
- generator: linear-density fiber census + adversarial
- checker: re-run chart + Delta=E/f^3 + cube3

## Reproducibility
payload_sha256: f0e1f3bec7c8369d9cb7929890c3991047ee9bd6ff6885e2ac6b6ab972dfc185
