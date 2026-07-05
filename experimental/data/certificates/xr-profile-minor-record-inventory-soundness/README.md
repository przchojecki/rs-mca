# XR Profile Minor Record-Inventory Soundness

This directory stores the replayable certificate for
`experimental/notes/m1/xr_profile_minor_record_inventory_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_xr_profile_minor_record_inventory_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_profile_minor_record_inventory_soundness.py \
  --check experimental/data/certificates/xr-profile-minor-record-inventory-soundness/xr_profile_minor_record_inventory_soundness.json
```

The verifier checks a small inventory-shape sample. It does not construct the
actual XR profile inventory.
