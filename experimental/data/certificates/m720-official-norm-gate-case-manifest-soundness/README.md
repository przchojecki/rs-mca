# M720 Official Norm-Gate Case Manifest Soundness

This directory stores the replayable certificate for
`experimental/notes/m720/m720_official_norm_gate_case_manifest_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_case_manifest_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_case_manifest_soundness.py \
  --check experimental/data/certificates/m720-official-norm-gate-case-manifest-soundness/m720_official_norm_gate_case_manifest_soundness.json
```

The verifier checks note anchors and a toy manifest schema. It does not
construct the official norm-gate manifest.
