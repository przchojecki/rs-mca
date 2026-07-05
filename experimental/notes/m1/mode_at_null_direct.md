# Direct Mode-At-Null Prefix-Fiber Test

## Claim

The packet directly tests the finite statement `N_w(z) <= N_w(0)` for the
signed prefix map `Phi_w` on all `m`-subsets of small multiplicative subgroup
domains, and separates rows where the zero prefix is not realized.

## Status

EXPERIMENTAL.

## Parameters

- `q_gen = q_line = q_chal = p` for `p in {5,7,11,13,17}`.
- Domains are `mu_n <= F_p^*` with `n=p-1`.
- Prefix lengths are `w=2` and `w=3`, where listed in the certificate.
- Two additional `F_17` control rows use `m=6` and `m=10` at `w=2`.

## Existing Paper Dependency

This is a finite test for the `prob:band` mode-at-null/Q3 crux. It is
distinct from PR #337, which tested a non-canonical within-bucket occupancy
proxy rather than the literal `N_w(z) <= N_w(0)` statement. It is also
distinct from PR #332, which records an aggregate second-moment collision
ledger and does not isolate `N_w(0)`, the argmax fiber, or the exact
`kappa = N_w/avg` constants.

## Proof Idea Or Experiment

The enumerator computes `Phi_w(S)=((-1)^j e_j(S))_{j=1..w}` by the elementary
symmetric recurrence and records the complete realized fiber histogram
`N_w(z)`. It records whether the zero prefix is realized, the strict margin
`max_z N_w(z) - N_w(0)`, and exact `kappa_null` and `kappa_max` as rational
numbers.

The checker rebuilds the same fibers from raw power sums using Newton's
identities, recomputes `N_w(0)`, the argmax, the vacuous-zero split, the
strict realized-null rows, and the `kappa` constants, and compares the
complete histogram to the certificate.

## Ledger Impact

The finite rows are mild evidence for the mode-at-null heuristic, not a
negative result on the named object. Three rows are vacuous because `z=0` is
not realized. On the nine rows where `z=0` is realized, it is the exact mode
on six rows and one below the mode on three rows, so the recorded range has
`N_w(0) >= max_z N_w(z) - 1` whenever the zero prefix exists.

The literal strict inequality is therefore not automatic on these toy rows,
but the near-mode property is stable across every realized-null row tested.

## Constants

```text
row                   N_w(0)  max N_w(z)  zero realized  strict margin
F_5,n=4,m=2,w=2       0       1           no             vacuous
F_5,n=4,m=2,w=3       0       1           no             vacuous
F_7,n=6,m=3,w=2       2       2           yes            0
F_7,n=6,m=3,w=3       0       1           no             vacuous
F_11,n=10,m=5,w=2     2       3           yes            1
F_11,n=10,m=5,w=3     2       2           yes            0
F_13,n=12,m=6,w=2     6       7           yes            1
F_13,n=12,m=6,w=3     2       2           yes            0
F_17,n=16,m=8,w=2     54      54          yes            0
F_17,n=16,m=8,w=3     6       7           yes            1
F_17,n=16,m=6,w=2     32      32          yes            0
F_17,n=16,m=10,w=2    32      32          yes            0
```

Realized-null summary:

```text
realized rows: 9
exact mode rows: 6
one-below-mode rows: 3
max strict margin on realized rows: 1
vacuous zero-prefix rows: 3
```

## Reproducibility

```powershell
py -3.13 experimental/scripts/verify_mode_at_null_direct.py --emit-defaults
py -3.13 experimental/scripts/verify_mode_at_null_direct_check.py --check experimental/data/certificates/mode-at-null-direct/mode_at_null_direct.json
```

## Non-Claims

This is not an asymptotic extremality theorem, not a proof or refutation of
`prob:band`, and not evidence about untested larger rows. The vacuous rows are
not counted as mode-at-null failures.
