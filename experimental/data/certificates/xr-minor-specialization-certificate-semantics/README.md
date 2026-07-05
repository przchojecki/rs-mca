# XR Minor-Specialization Certificate Semantics

This directory stores the replayable certificate for
`experimental/notes/m1/xr_minor_specialization_certificate_semantics.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_xr_minor_specialization_certificate_semantics.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_minor_specialization_certificate_semantics.py \
  --check experimental/data/certificates/xr-minor-specialization-certificate-semantics/xr_minor_specialization_certificate_semantics.json
```

The verifier checks note anchors and a toy polynomial determinant
specialization. It does not produce the profile-by-profile certificates.
