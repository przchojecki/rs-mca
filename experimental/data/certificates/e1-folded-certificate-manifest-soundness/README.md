# E1 Folded Certificate Manifest Soundness

This directory contains the replayable certificate for
`experimental/notes/e1/e1_folded_certificate_manifest_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_manifest_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_manifest_soundness.py \
  --check experimental/data/certificates/e1-folded-certificate-manifest-soundness/e1_folded_certificate_manifest_soundness.json
```

The verifier checks manifest coverage and record-shape semantics.  It does not
provide the actual open-cell certificate transcripts.
