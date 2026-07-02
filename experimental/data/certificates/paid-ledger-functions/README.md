# Paid Ledger Functions Certificate

This directory contains the emitted arithmetic certificate for:

```text
experimental/notes/thresholds/paid_ledger_functions.md
```

Replay:

```text
python3 experimental/scripts/verify_paid_ledger_functions.py --emit
python3 experimental/scripts/verify_paid_ledger_functions.py
```

The certificate verifies compiler arithmetic for `Paid_tan`, `Paid_quot`, and
`Paid_ext`.  It does not certify global branch exhaustion or the aperiodic
local-limit theorem.

