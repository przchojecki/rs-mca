# M1 SPI Post-Strip Genericity Certificate

This directory contains the replayable certificate for
`experimental/notes/m1/m1_spi_post_strip_genericity.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_m1_spi_post_strip_genericity.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m1_spi_post_strip_genericity.py \
  --check experimental/data/certificates/m1-spi-post-strip-genericity/m1_spi_post_strip_genericity.json
```

The certificate checks the periodic-stratum count, fixed-locus equivalence,
intersection law, and trivial stabilizer of the post-strip aperiodic complement
on representative cyclic toy domains.

