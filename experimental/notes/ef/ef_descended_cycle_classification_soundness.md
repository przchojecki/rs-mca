# EF Descended-Cycle Classification Soundness

Status: PROVED.

Source DAG node: `ef_descended_cycle_classification_soundness`.

## Statement

If every `B`-defined pole-free horizontal cycle produced by
`ef_full_orbit_cycle_descent` is certified as one of:

- base-descended;
- proper-subfield/tower-confined; or
- noncontainment-degenerate;

then `ef_pole_free_cycle_exclusion` holds.

## Proof

By `ef_full_orbit_cycle_descent`, any pole-free full Galois orbit that could
falsify `ef_full_orbit_pole_forcing` descends to a `B`-defined reduced
horizontal cycle in the extension-pole complement.

Assume the classification certificate covers every such descended cycle.  If a
cycle is base-descended, it is paid by the base component.  If it is
proper-subfield or tower-confined, it is not a full-field hidden leakage class.
If it is noncontainment-degenerate, it is excluded by the noncontainment gate.

These three classes are exactly the removals named in
`ef_pole_free_cycle_exclusion`.  Therefore no descended pole-free horizontal
cycle remains that is simultaneously non-base, non-tower, nondegenerate, and
unpaid.  This proves the EF pole-free hidden-cycle exclusion.

## Non-Claims

This packet does not produce the classification certificate.  It only proves
that a complete base/tower/noncontainment classification is sound for excluding
the pole-free hidden-cycle leakage class.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_classification_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_classification_soundness.py \
  --check experimental/data/certificates/ef-descended-cycle-classification-soundness/ef_descended_cycle_classification_soundness.json
```

The verifier checks the proof-note anchors and a small exhaustive
classification sample.
