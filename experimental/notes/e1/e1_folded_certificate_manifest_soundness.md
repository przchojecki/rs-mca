# E1 Folded Certificate Manifest Soundness

Status: PROVED.

Source DAG node: `e1_folded_certificate_manifest_soundness`.

## Statement

If a manifest covers `N' in {128,256}` with named exhibit fields and complete
folded kernel certificate records, each returning zero nonzero
non-cyclotomic folded vectors, then `e1_open_cell_control_payload` holds by
the named folded-certificate route.

## Proof

The named folded-certificate route in `e1_open_cell_control_payload` requires
exactly two open-cell entries, one for `N'=128` and one for `N'=256`.

Assume the manifest supplies both entries.  Each entry names the exhibit field
being certified, marks the folded kernel search as complete, and records zero
nonzero non-cyclotomic folded vectors.

Those are precisely the fields required by the payload's accepted
folded-certificate route: named exhibit fields with complete folded kernel
certificates returning no nonzero non-cyclotomic folded vector.  Therefore the
manifest satisfies `e1_open_cell_control_payload`.

## Non-Claims

This packet is route-shape soundness only.  It does not provide the actual
certificate transcripts for the two open cells.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_manifest_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_manifest_soundness.py \
  --check experimental/data/certificates/e1-folded-certificate-manifest-soundness/e1_folded_certificate_manifest_soundness.json
```
