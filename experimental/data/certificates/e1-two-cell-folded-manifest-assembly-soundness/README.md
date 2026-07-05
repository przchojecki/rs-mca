# E1 Two-Cell Folded Manifest Assembly Soundness

This directory contains the replayable certificate for
`experimental/notes/e1/e1_two_cell_folded_manifest_assembly_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_e1_two_cell_folded_manifest_assembly_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_two_cell_folded_manifest_assembly_soundness.py \
  --check experimental/data/certificates/e1-two-cell-folded-manifest-assembly-soundness/e1_two_cell_folded_manifest_assembly_soundness.json
```

The verifier checks two-cell manifest assembly semantics.  It does not prove
either folded cell payload.
