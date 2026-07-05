# M720 Certificate Semantics

This directory stores the replayable certificate for
`experimental/notes/m720/m720_certificate_semantics.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_m720_certificate_semantics.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_certificate_semantics.py \
  --check experimental/data/certificates/m720-certificate-semantics/m720_certificate_semantics.json
```

The verifier checks note anchors and a toy truth table for the completeness
rule. It does not run the MITM scanner.
