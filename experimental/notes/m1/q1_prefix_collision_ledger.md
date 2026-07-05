# Q1 Prefix-Collision Ledger

## Claim

The packet records exact prefix-fiber histograms and second moments for
`Phi_w` on fixed-size subsets without replacement. Direct ordered-pair strata
are included for rows where that replay is small enough to audit locally.

## Status

EXPERIMENTAL / AUDIT. The direct pair-strata rows give finite PROVED arithmetic
inside their stated scope; the beta table is measured evidence.

## Parameters

- Prime fields `F_5`, `F_7`, `F_11`, `F_17`, and `F_41`.
- `q_gen = q_line = q_chal = p` in every row.
- Object: `Phi_w(M)=((-1)^i e_i(M))_{i<=w}` on `m`-subsets of `mu_n`.

## Existing Paper Dependency

This supports the `(Q)` quotient-fiber equidistribution side of the
master-flatness program and supplies measured constants for the generated-field
prefix map. It is distinct from the E3 key-lemma refutation track.

## Proof Idea Or Experiment

The scanner enumerates all `m`-subsets, builds the prefix histogram, and computes

```text
sum_z N_w(z)^2
```

from the exact bucket sizes. For small rows it also enumerates all ordered
same-prefix pairs, classifies exchange size, and checks the finite rigidity
condition `e >= w+1` for nontrivial pairs.

## Ledger Impact

The rows give exact L2 flatness constants for the recorded prefix maps and a
measured beta-envelope table. They do not imply worst-case flatness.

## Constants

The `F_17,n=16,m=6,w=4` row has `8008` subsets, `7968` prefix values, maximum
fiber size `2`, and second moment `8088`, matching the existing F17 prefix
collision constants.

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/q1_prefix_collision_ledger.py --emit-defaults
py -3.13 experimental/scripts/verify_q1_prefix_collision_ledger.py --check experimental/data/certificates/q1-prefix-collision/l2_constant.json experimental/data/certificates/q1-prefix-collision/beta_envelope_table.json
```

## Non-Claims

This is not a worst-case max-over-prefix theorem, not a local-limit theorem, and
not a resolution of `prob:band`.
