# Exact Worst-Case eca/emca Staircases

Date: 2026-07-03. Status: EXPERIMENTAL / AUDIT.

## Claim

For six complete toy rows, the verifier computes the exact worst-case
finite-slope numerators

```text
eca_C(r)  = max over pairs of # CA-bad finite slopes
emca_C(r) = max over pairs of # MCA-bad finite slopes
```

and checks the numerical sparsification identity

```text
emca_C(r) = max(eca_C(r), sigma_C(r))
```

at every sub-capacity radius in the row.

## Endpoint Conventions

```text
agreement a = n - r
radius r = floor(delta*n), with r in [0, n-k-1]
slopes are finite gamma in F_q only
denominator q_line = q for every toy row here
CA uses the same radius r for point closeness and pair-far distance
MCA witness: exists S with |S| >= n-r, point restricted to S in C|S,
and eps2|S not in C|S
```

These are toy finite-slope rows over the base field. They are not deployed-row
certificates, not leaderboard entries, and not protocol `q_chal` claims.

## Method

The verifier uses translation invariance by codeword pairs: the worst case over
all received-word pairs is attained on syndrome-class representatives. For an
`[n,k]` RS code, this gives `q^(n-k)` representatives per word and
`q^(2(n-k))` pair classes.

Restricted-code membership is checked two ways: nullspace parity-check matrices
for `C|S`, and Vandermonde interpolation high-coefficient tests for the same
restricted word. The two engines agree for every listed radius. No `q^k`
codeword table is materialized.

## Results

| q | n | k | m=n-k | radii | eca_num | emca_num | sigma_num |
|---:|---:|---:|---:|---|---|---|---|
| 5 | 4 | 2 | 2 | r=0,1 | 1,4 | 1,4 | 0,1 |
| 7 | 6 | 5 | 1 | r=0 | 1 | 1 | 0 |
| 7 | 6 | 3 | 3 | r=0,1,2 | 1,2,7 | 1,2,7 | 0,1,7 |
| 11 | 10 | 8 | 2 | r=0,1 | 1,10 | 1,10 | 0,1 |
| 13 | 12 | 10 | 2 | r=0,1 | 1,12 | 1,12 | 0,1 |
| 17 | 16 | 14 | 2 | r=0,1 | 1,16 | 1,16 | 0,1 |

The `F_7,n=6,k=3,r=2` row saturates: all seven finite slopes are MCA-bad for
an extremal pair. This agrees with the sparse-sigma toy row packaged in PR
#229. The sigma values here are used only to check the sparsification identity;
larger sigma_C sparse-census rows belong to the sparse-census certificates.

## Reproducibility

```powershell
python experimental/scripts/verify_exact_worstcase_eca_emca_staircase.py --check experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_cpu_rows.json
python experimental/scripts/verify_exact_worstcase_eca_emca_staircase.py --json
python -m py_compile experimental/scripts/verify_exact_worstcase_eca_emca_staircase.py
python experimental/scripts/script_reproducibility_audit.py --format json
git diff --check
```

## Non-Claims

- No deployed-size row is certified.
- No `q>=97` row is certified.
- No protocol soundness or challenge-field ledger is claimed.
- No GPU-tier row is included in this certificate.
- The high-rate rows avoid materialized-codeword oracles because `q^k` is the
  infeasible object; their second exact check is the interpolation-membership
  engine.
