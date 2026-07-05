# E1 Two-Cell Folded Manifest Assembly Soundness

Status: PROVED.

Source DAG node: `e1_two_cell_folded_manifest_assembly_soundness`.

## Statement

If the two E1 cell payloads supply complete named folded-certificate
transcripts for `N'=128` and `N'=256`, each with zero nonzero
non-cyclotomic folded vectors, then
`e1_folded_certificate_manifest_payload` holds.

## Proof

The E1 folded manifest asks for exactly two entries:

```text
N'=128
N'=256
```

Assume `e1_folded_certificate_cell_128_payload` supplies a named exhibit field,
a complete folded kernel certificate, and zero nonzero non-cyclotomic folded
vectors for the first cell.  Assume
`e1_folded_certificate_cell_256_payload` supplies the analogous data for the
second cell.

Form the manifest with those two records.  Its cell set is exactly
`{128,256}`.  Each entry names the field being certified, is marked complete,
and records zero nonzero folded vectors.  These are precisely the records
required by `e1_folded_certificate_manifest_payload`.

Therefore the two cell payloads assemble to the named folded-certificate
manifest for the E1 open cells.

## Non-Claims

This packet does not prove either cell payload.  It only proves that two valid
cell payload records assemble to the manifest schema.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_e1_two_cell_folded_manifest_assembly_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_two_cell_folded_manifest_assembly_soundness.py \
  --check experimental/data/certificates/e1-two-cell-folded-manifest-assembly-soundness/e1_two_cell_folded_manifest_assembly_soundness.json
```
