
# Deep low-energy observability (W52-M2)

## Status
EXPERIMENTAL. **Rung: MEASURED-SUPPORT.** Observability fixed vs W51.

## Phase 0
cube3 E=216.

## Fix vs W51
At thr=0.5 absolute, deep low-energy class still empty (confirms W51).
With thr grid + adaptive percentiles, **14/14 deep charts become nonempty**.

## Measurement (cert-sourced)
```text
n_deep = 14
n_deep_nonempty_primary = 14
observability_fixed = true
n_deep_nonempty_at_thr_0.5 = 0
max_deep_ratio ≈ 1.97  (O(1), not asymptotic CE)
max_deep_log_ratio_over_N ≈ 0.077
trend = GROW (small-N thr artifact; ratio stays O(1))
any_counterexample = false
```

## CE policy
Deep + log(ratio)/N >= eta + N>=12 + ratio >= max(8,N). O(1) ratios do not count.

## Dual routes
- generator: thr sweep + adaptive + adversarial
- checker: sum-histogram / re-analyze + ratio algebra

## Reproducibility
payload_sha256: 69d969fd2cee1e6f50b1ab9359cde40890e8437e818ae210eeabc4f59c044801
