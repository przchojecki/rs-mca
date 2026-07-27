# KoalaBear first-gap source interpolation pencil certificate

This directory contains the exact certificate for the source-bound normal
form at the first open full-outside slack:

```text
r=67,471
x=1
|Sigma|=134,944
reduced degree=67,472
source interpolation dimension=2
```

Replay:

```bash
python3 experimental/scripts/verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1.py --tamper-selftest
```

The certificate proves the exact source interpolation pencil, locator
determinant, off-source evaluation isomorphism, and the split-locator
corollary that the common-zero set determines the complete graph line. It
also records the `67,471` source RS parity constraints per quotient
coordinate. It does not pay the determinant-weighted graph-line mass or
move the KoalaBear ledger.
