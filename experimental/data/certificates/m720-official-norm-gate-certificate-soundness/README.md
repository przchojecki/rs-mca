# M720 Official Norm-Gate Certificate Soundness

This directory stores the replayable certificate for
`experimental/notes/m720/m720_official_norm_gate_certificate_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_certificate_soundness.py \
  --check experimental/data/certificates/m720-official-norm-gate-certificate-soundness/m720_official_norm_gate_certificate_soundness.json
```

The verifier checks note anchors and a toy payload schema. It does not run the
M720 MITM certificates.
