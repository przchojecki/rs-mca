# E1 Folded Certificate Soundness Certificate

This directory contains the replayable certificate for
`experimental/notes/e1/e1_folded_certificate_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_soundness.py \
  --check experimental/data/certificates/e1-folded-certificate-soundness/e1_folded_certificate_soundness.json
```

The verifier checks proof-note anchors and a toy `N'=16` folded-kernel example.
It does not run the `N'=128` or `N'=256` no-vector searches.
