# DLI Reduced-Phase Manifest Soundness

Status: PROVED.

Source DAG node: `dli_reduced_phase_manifest_soundness`.

## Statement

Suppose a reduced-phase manifest covers every central profile, nonzero
frequency, DLI harmonic, and relevant square-root component. For each covered
tuple, suppose it supplies:

- the Artin-Schreier-reduced local expansion of `P_lambda(sigma(y))`;
- a pole of positive order not divisible by `p`;
- a certified upper bound for the reduced polar divisor of the same phase; and
- a proof that the harmonic sum of the majorants is `o(t)`.

Then the manifest supplies both DLI payloads:

- `dli_odd_phase_polar_obstruction_payload`;
- `dli_reduced_pole_majorant_table_payload`.

## Proof

Let `M` be a reduced-phase manifest satisfying the stated predicates.

The manifest covers the same tuple universe used by both DLI payloads:

```text
(central profile, nonzero frequency, harmonic, square-root component).
```

For each tuple, it gives the Artin-Schreier-reduced local expansion of the
actual phase `P_lambda(sigma(y))` and records a pole of positive order not
divisible by `p`. These are exactly the local certificates required by
`dli_odd_phase_polar_obstruction_payload`. The proved packet
`dli_odd_phase_polar_obstruction_soundness` gives the intended
non-Artin-Schreier meaning of this certificate format.

For the same tuple, the manifest records a certified upper bound for the
reduced polar divisor. It also proves that the harmonic sum of those majorants
is `o(t)`. These are exactly the table rows and summation assertion required
by `dli_reduced_pole_majorant_table_payload`. The proved packet
`dli_reduced_pole_majorant_table_soundness` gives the intended reduced-pole
ledger meaning of this table format.

Thus one verified reduced-phase manifest supplies both former payloads.

## Non-Claims

This packet proves manifest soundness only. It does not construct the actual
manifest, prove the harmonic `o(t)` estimate independently, or close the
remaining DLI analytic gap.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_reduced_phase_manifest_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_reduced_phase_manifest_soundness.py \
  --check experimental/data/certificates/dli-reduced-phase-manifest-soundness/dli_reduced_phase_manifest_soundness.json
```

The verifier checks note anchors and a toy manifest with coverage, reduced-pole
predicate, domination, and budget checks.
