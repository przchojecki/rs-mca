# L1 PMA Auxiliary-Johnson Certificate

This directory contains the replayable certificate for
`experimental/notes/l1/l1_pma_auxiliary_johnson.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_l1_pma_auxiliary_johnson.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_pma_auxiliary_johnson.py \
  --check experimental/data/certificates/l1-pma-auxiliary-johnson/l1_pma_auxiliary_johnson.json
```

The certificate packages the auxiliary-list reduction and the ordinary
Johnson-covered few-petal regime.  It does not close mixed-petal sunflower
amplification.

