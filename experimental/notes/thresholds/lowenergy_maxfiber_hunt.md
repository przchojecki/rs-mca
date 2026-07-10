# Low-energy max-fiber hunt on deep power-sum charts (W51-M1)

## Status
EXPERIMENTAL. **Rung: MEASURED-SUPPORT.**

Reduced C9 input (W50 Lemma II / #575): on deep charts,
\(\max\{f_s:\Delta_s\le thr\}/\bar N=\exp(o(N))\).

## Phase 0
`image_scale_mi_ma` cube3: **E=216**, Δ=**27/64**.

## Dual routes
- **generator:** power-sum fibers; Boolean Δ; max low-energy ratio; adversarial sparse/no-AP/heavy-fiber; log(ratio)/N trend
- **checker:** sum-histogram energy; algebraic ratio recompute; trend recompute

## Sweep (cert-sourced)
```text
n_sweep = 28
n_deep = 20
n_deep_with_low_energy_fiber = 0
n_deep_ce = 0
borderline_max_ratio ≈ 2.29  (O(1), not asymptotic CE)
max_log_ratio_over_N ≈ 0.083  (only on borderline tiny-N)
deep_max_log_ratio_over_N = null  (no low-energy fibers on deep toys)
trend = SHRINK
any_counterexample = false
```

## Failure-gate policy (honest)
A headline negative is allowed only if **deep** regime and log(ratio)/N ≥ η and N≥10.
O(1) borderline ratios (ratio~2 ⇒ log/N = O(1/N)→0) do **not** break exp(o(N)).

## Verdict
**MEASURED-SUPPORT.** Deep toys show empty low-energy heavy-fiber class under the finite thr;
adversarial search found no deep CE. Borderline O(1) ratios recorded honestly.

## Nonclaims
Not a proof of the reduced input at deployed scale. thr is a finite stand-in for e^{-σN}.

## Reproducibility
```text
py -3.13 experimental/scripts/verify_lowenergy_maxfiber_hunt.py --check
payload_sha256: 1c78632cc65298a666ddf40c06b4a602a447497a6e59f0efe31bd00fd05226d9
```
