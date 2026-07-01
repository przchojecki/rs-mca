# F17^32 M3 Low-Rank6-11 Shifted-Minor Exclusion

This directory contains a deterministic audit for the synthetic rank-6..11
low-rank M3 slack ladder.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_shifted_minor_exclusion.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-shifted-minor-exclusion/f17_32_n512_k256_m3_low_rank6_11_shifted_minor_exclusion.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_shifted_minor_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-shifted-minor-exclusion/f17_32_n512_k256_m3_low_rank6_11_shifted_minor_exclusion.json
```

The source slack ledgers count finite roots of a selected first regular square
Hankel minor.  A genuine exact-support witness must make the full
`t x (j+1)` Hankel matrix rank-deficient, so every consecutive
`(j+1) x (j+1)` square minor must vanish.  This audit computes the row-shift-1
minor for every root-bearing rank/agreement row in the rank-6..11 low-rank
ladder and checks that none of the certified finite roots also vanishes there.

Result: all `238` finite first-minor roots counted by the rank-6..11 slack
certificates are excluded as actual full-Hankel support witnesses.

Non-claims: this is only for the synthetic low-rank slack ladder, only for
finite first-minor roots, and not a quotient-image/support audit or a
replacement for the general singular/pivot chart program.
