# Interleaved Budget Calculator Certificate

- **Status:** AUDIT for the script; PROVED for the arithmetic transformations
  of the stated Paper C inequalities.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This note certifies `experimental/interleaved_budget.py`, a small
  calculator for the list-over-field, MCA-over-field, and toy query-count
  budgets in Paper C.

## Claim Audited

Paper C records the list-over-field budget

```text
L_mu(delta) / q_line <= 2^(-lambda_list)
```

and the corrected MCA numerator budget

```text
N_mca / q_line <= 2^(-lambda_mca).
```

Taking base-2 logarithms gives the challenge-size target

```text
log2(q_line) >= max(
  lambda_list + log2 L_mu(delta),
  lambda_mca + log2 N_mca
).
```

The script computes these two required bit widths and, when an actual
`q_line` or `log2(q_line)` is supplied, the remaining margin.  For the
conservative trivial product bound it uses Paper C's
`L_mu <= L_1^mu`; if `L_1 <= n^B_L`, this gives
`log2 L_mu <= mu B_L log2 n`.

For the corrected RS MCA numerator it computes

```text
N_mca = nu * (n^A_M + 2^(beta_over_Hbin * Qprof + Gamma_M)),
```

omitting the quotient-profile term when the profile is empty or not supplied.

When `lambda_query` and `delta` are supplied, the script also computes the
toy-protocol query count

```text
t >= lambda_query / log2(1 / (1 - delta)).
```

## Reproducible Checks

The KoalaBear-style toy ledger in Paper C says that with `n=2^18`, `mu=2`,
`B_L=1`, `nu=8`, empty quotient profile, and `A_M=1`, the list side asks for
about `128 + 2 log2 n = 164` bits and the MCA side asks for about
`128 + log2(8n) = 149` bits.  This is reproduced by:

```bash
python3 experimental/interleaved_budget.py \
  --n 262144 \
  --mu 2 \
  --base-list-exponent 1 \
  --lambda-list 128 \
  --lambda-mca 128 \
  --nu 8 \
  --mca-exponent 1 \
  --qprofile-empty \
  --qline-bits 185.9 \
  --delta 7/16 \
  --lambda-query 128
```

## Use in the Program

This supports the P2 certificate-scanner lane from the blueprint: after entropy,
quotient-profile, and lower-bound audits produce their numerators, this script
turns those numerators into the minimum line-field bit width and, for the toy
query model, the required number of spot checks.

## Limits

The script is a ledger calculator, not a theorem checker.  The caller must still
supply the theorem, assumption, or experimental certificate that justifies the
input list and MCA numerators.
