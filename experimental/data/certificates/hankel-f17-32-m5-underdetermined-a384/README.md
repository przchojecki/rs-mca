# F17^32 M5 underdetermined A=384 residual packet

This directory contains the first M5 underdetermined-boundary packet for

```text
C = RS[F_17^32, H, 256], |H| = 512, A = 384.
```

Generate and validate it with:

```bash
python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py --emit
python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/f17_32_n512_k256_a384_m5_residual_packet.json
```

The packet is intentionally a labelled residual, not a threshold proof.  It
records that rank-drop and low-degree Cramer branches contribute no new
exact-`A` mass after higher-agreement deduplication, while the full-rank top
pseudo-remainder chart remains `residual_label=unknown`.  The named finite
object for that residual is the top-coefficient-saturated gcd of the
pseudo-remainder coefficients of `X^512-1` by the Cramer locator.
