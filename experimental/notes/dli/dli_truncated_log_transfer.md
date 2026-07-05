# DLI Truncated-Log Transfer

Status: PROVED.

Source DAG node: `dli_truncated_log_transfer`.

## Statement

If the odd-evaluation sequence satisfies the stated truncated-log discrepancy
bounds for the Dirichlet kernel and the stated peak-mass tail bounds near its
singular peaks, with total error `sum_j eps_j=o(t)`, then the DLI
odd-evaluation discrepancy predicate follows.

## Proof

Let

```text
F(theta) = -log |mu_hat(theta)|^2
```

be the nonnegative logarithmic Dirichlet loss after DLI normalization, and let
`F_T = min(F,T)` be its truncation at height `T`. For any finite sequence
`theta_y`,

```text
sum_y F(theta_y) >= sum_y F_T(theta_y).
```

The truncated-log discrepancy hypothesis says that the empirical average of
`F_T` along the odd-evaluation sequence is within the stated error of the
circle average of `F_T`. The peak-mass tail hypothesis controls the missing
tail between `F_T` and `F` near the singular Dirichlet peaks. Hence

```text
sum_y F(theta_y)
  >= (#y) * int F(theta) dtheta - error_j.
```

Using `dli_circle_log_integral_constant`, the circle integral is the model
value that becomes `2 L_j log q` under DLI normalization. Writing the combined
truncated-discrepancy and peak-tail error as `2 eps_j log q + O(1)` gives

```text
-sum_y log |mu_hat_y(P_lambda(sigma(y)))|^2
    >= 2(L_j - eps_j) log q - O(1).
```

If the per-profile errors satisfy `sum_j eps_j=o(t)`, the DLI odd-evaluation
discrepancy predicate follows. This transfer is deterministic; the arithmetic
content remains in the peak-mass discrepancy hypotheses.

## Non-Claims

This packet proves only the truncation transfer. It does not prove the
truncated-log discrepancy hypothesis, the peak-mass tail hypothesis, or the
finite-frequency Weyl bounds that can imply them.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_truncated_log_transfer.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_truncated_log_transfer.py \
  --check experimental/data/certificates/dli-truncated-log-transfer/dli_truncated_log_transfer.json
```

The verifier checks note anchors and a toy nonnegative-loss truncation budget.
