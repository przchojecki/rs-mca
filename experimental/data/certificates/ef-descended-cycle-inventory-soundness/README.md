# EF Descended-Cycle Inventory Soundness Certificate

This directory contains the replayable certificate for
`experimental/notes/ef/ef_descended_cycle_inventory_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_inventory_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_descended_cycle_inventory_soundness.py \
  --check experimental/data/certificates/ef-descended-cycle-inventory-soundness/ef_descended_cycle_inventory_soundness.json
```

The verifier checks proof-note anchors and a small inventory-semantics sample.
It does not construct or certify the actual descended-cycle inventory.
