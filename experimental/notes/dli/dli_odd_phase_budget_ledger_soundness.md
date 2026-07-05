# DLI Odd-Phase Budget Ledger Soundness

Status: PROVED.

Source DAG node: `dli_odd_phase_budget_ledger_soundness`.

## Statement

Suppose a DLI odd-phase ledger covers every tuple

```text
(central profile, nonzero frequency, harmonic, square-root component)
```

used by the DLI odd-evaluation Weyl sums. If the ledger marks every covered
phase as not Artin-Schreier-trivial and gives reduced polar-divisor bounds
whose harmonic total is `o(t)`, then `dli_odd_phase_reduced_pole_budget` holds.

## Proof

The reduced-pole budget statement has two requirements for every DLI odd phase:

1. the phase is not of Artin-Schreier form `g^p - g + c`; and
2. the Artin-Schreier-reduced polar-divisor bounds have harmonic total `o(t)`.

Ledger coverage means that no central profile, nonzero frequency, harmonic, or
square-root component used by the DLI odd-evaluation Weyl sums is omitted.

For each covered tuple, the ledger's nontriviality entry supplies requirement
1. Its reduced polar-divisor entry is a certified upper bound for the
corresponding reduced polar divisor. Summing those upper bounds over exactly
the DLI harmonic ranges gives the ledger's declared harmonic total, which is
`o(t)` by hypothesis. Therefore the true harmonic total is also `o(t)`.

Both requirements of `dli_odd_phase_reduced_pole_budget` hold for the actual
list of DLI odd phases.

## Non-Claims

This packet proves the soundness of a supplied complete odd-phase ledger. It
does not construct the ledger, prove the individual nontriviality certificates,
or prove the remaining DLI equidistribution theorem.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_odd_phase_budget_ledger_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_odd_phase_budget_ledger_soundness.py \
  --check experimental/data/certificates/dli-odd-phase-budget-ledger-soundness/dli_odd_phase_budget_ledger_soundness.json
```

The verifier checks note anchors and a toy complete-ledger schema with
coverage, nontriviality, and budget failure cases.
