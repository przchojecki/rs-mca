# Conjecture F Consumer-Scope Audit Certificate

This directory contains the replayable source-marker certificate for
`experimental/notes/audits/f_consumer_scoped_audit.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_f_consumer_scoped_audit.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_f_consumer_scoped_audit.py \
  --check experimental/data/certificates/f-consumer-scoped-audit/f_consumer_scoped_audit.json
```

The certificate records the conservative A0 outcome: coordinate-prefix and
Hankel-kernel Conjecture F consumers are scoped, but the L1 mixed-petal
sunflower residual remains an escaping consumer.

