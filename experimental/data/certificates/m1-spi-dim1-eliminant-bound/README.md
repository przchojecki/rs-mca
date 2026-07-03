# M1 SPI Dimension-One Eliminant Bound Certificate

This directory contains the replayable certificate for
`experimental/notes/m1/m1_spi_dim1_eliminant_bound.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_m1_spi_dim1_eliminant_bound.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m1_spi_dim1_eliminant_bound.py \
  --check experimental/data/certificates/m1-spi-dim1-eliminant-bound/m1_spi_dim1_eliminant_bound.json
```

The certificate checks the pseudo-division degree propagation and records the
pinned-row arithmetic giving the global dimension-one cap `49408`.
