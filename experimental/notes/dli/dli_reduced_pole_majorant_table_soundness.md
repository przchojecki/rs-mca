# DLI Reduced-Pole Majorant Table Soundness

Status: PROVED.

Source DAG node: `dli_reduced_pole_majorant_table_soundness`.

## Statement

Suppose a table covers every DLI tuple

```text
(central profile, nonzero frequency, harmonic, square-root component)
```

used by the odd-evaluation Weyl sums. If the table gives a certified upper
bound for the Artin-Schreier-reduced polar divisor of each covered phase, and
the sum of those majorants over the DLI harmonic ranges is `o(t)`, then the
true reduced-pole harmonic ledger is also `o(t)`.

## Proof

Let `T` be a table indexed by the DLI tuple universe. Completeness means every
tuple appears exactly once, or is represented by a stated disjoint row class
whose multiplicity is included in the table total.

For each tuple `tau`, let `D_tau` be the true degree or weighted size of the
Artin-Schreier-reduced polar divisor of the actual phase

```text
P_lambda(sigma(y)).
```

The table supplies a certified majorant `M_tau` satisfying

```text
D_tau <= M_tau.
```

Summing over any covered collection gives

```text
sum_tau D_tau <= sum_tau M_tau.
```

By hypothesis, the full table sum over the DLI harmonic ranges is `o(t)`.
Therefore the true reduced-pole contribution over all central profiles,
nonzero frequencies, harmonics, and square-root components is also `o(t)`.
This is exactly the reduced-pole harmonic ledger assertion.

## Non-Claims

This packet proves the soundness of a supplied complete majorant table. It does
not construct the table, prove Artin-Schreier nontriviality, or close the
remaining analytic DLI estimate.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_reduced_pole_majorant_table_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_reduced_pole_majorant_table_soundness.py \
  --check experimental/data/certificates/dli-reduced-pole-majorant-table-soundness/dli_reduced_pole_majorant_table_soundness.json
```

The verifier checks note anchors and a toy coverage/domination/budget table.
