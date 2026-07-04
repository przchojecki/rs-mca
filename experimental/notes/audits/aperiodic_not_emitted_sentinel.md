# Aperiodic Packet `not_emitted:` Sentinel Audit

Date: 2026-07-03. Status: AUDIT.

## Claim

`root_union_table_ref: "not_emitted:<reason>"` is a valid v12 packet
reference only when the packet explicitly records an unclosed
`residual_obstruction` branch. It is not a filesystem path and it is not a
claim that a root-union table exists.

## Context

The A=384 M5 underdetermined-boundary packet records the full-rank top Cramer
locator chart as a labelled residual:

```text
root_union_table_ref = not_emitted:top_chart_residual_unknown
```

The packet also states the relevant nonclaim: no F17 root table is claimed. The
old checker treated the sentinel as a local path and failed before reaching the
packet's mathematical status.

This is the schema-checker lane named in `towards-prize.md`: validate v12 proof
packets before new math is claimed. The change touches the shared checker under
`scripts/`, but it does not edit the schema JSON or any packet JSON.

## Contract

- `inline:` still requires an inline root-union table.
- normal relative references still have to resolve to committed files.
- `not_emitted:` is accepted for `root_union_table_ref` only when the packet
  has a residual obstruction, either as a top-level exact-agreement status or
  inside a pivot-atlas record.
- `not_emitted:` with no reason, or with no residual-obstruction branch, is
  rejected.

This keeps the sentinel faithful to the packet's nonclaim instead of forcing a
root table for a deliberately open residual branch.

## Reproducibility

```powershell
python scripts/check_aperiodic_eliminant_packet.py experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/f17_32_n512_k256_a384_m5_residual_packet.json
python experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py
python scripts/check_aperiodic_eliminant_packet.py experimental/data/certificates/aperiodic-hankel-regular-minor-toy/f17_n16_k8_a13_regular_minor_certificate.json
python scripts/check_aperiodic_eliminant_packet.py --expect-fail experimental/data/certificates/aperiodic-hankel-regular-minor-toy/invalid_bad_j_packet.json
python scripts/check_aperiodic_eliminant_packet.py experimental/data/certificates/m5-stratification-partition/valid_stratified_packet.json
python scripts/check_aperiodic_eliminant_packet.py --expect-fail experimental/data/certificates/m5-stratification-partition/invalid_wrong_leaf_stratified_packet.json
python scripts/check_aperiodic_eliminant_packet.py --expect-fail experimental/data/certificates/m5-stratification-partition/invalid_missing_removed_ledger_ref_packet.json
git diff --check
```

## Non-Claims

This audit does not close the A=384 residual branch, does not emit an F17 root
table, and does not change any numerical threshold. It only makes the checker
recognize a guarded deliberate-absence sentinel.
