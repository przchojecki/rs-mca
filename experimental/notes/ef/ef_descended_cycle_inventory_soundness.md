# EF Descended-Cycle Inventory Soundness

Status: PROVED.

Source DAG node: `ef_descended_cycle_inventory_soundness`.

## Statement

If an inventory covers every `B`-defined pole-free horizontal cycle produced
after full-orbit descent and labels each cycle with a verified
base-descended, proper-subfield/tower-confined, or noncontainment-degenerate
certificate, then `ef_descended_cycle_classification_payload` holds.

## Proof

Let `C` be the set of `B`-defined pole-free horizontal cycles produced after
full-orbit descent.

The inventory covers `C`, so every cycle appears in exactly one entry or in a
declared disjoint entry class.  Each entry carries one of the accepted labels:
base-descended, proper-subfield/tower-confined, or
noncontainment-degenerate.  The certificate attached to the entry verifies the
asserted label.

Therefore every cycle in `C` is classified into one of the three cases named
by `ef_descended_cycle_classification_payload`.  This is exactly the payload's
classification statement.

## Non-Claims

This packet does not construct or certify the actual descended-cycle
inventory.  It only proves that an inventory with the stated coverage,
disjointness, and label-certificate semantics is sound for the classification
payload.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_inventory_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_inventory_soundness.py \
  --check experimental/data/certificates/ef-descended-cycle-inventory-soundness/ef_descended_cycle_inventory_soundness.json
```

The verifier checks the proof-note anchors and a small inventory-semantics
sample.
