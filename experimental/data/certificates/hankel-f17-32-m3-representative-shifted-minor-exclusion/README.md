# F17^32 M3 Representative Shifted-Minor Exclusion

This directory contains a deterministic audit for the six representative
rank-6..11 projective-line packets in the synthetic low-rank M3 ladder.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_representative_shifted_minor_exclusion.py \
  --write experimental/data/certificates/hankel-f17-32-m3-representative-shifted-minor-exclusion/f17_32_n512_k256_m3_representative_shifted_minor_exclusion.json

python3 experimental/scripts/verify_f17_32_m3_representative_shifted_minor_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-representative-shifted-minor-exclusion/f17_32_n512_k256_m3_representative_shifted_minor_exclusion.json
```

The first regular minor in each packet gives an upper-bound finite root table.
A genuine exact-support witness would make the full `t x (j+1)` Hankel matrix
rank-deficient, so every consecutive `(j+1) x (j+1)` square minor would vanish.
The verifier recomputes the first minor, computes the row-shift-1 minor using
the same low-rank determinant lemma, and checks that the gcd of the first-minor
root gcd with the shifted minor has degree `0`.

Result: all `18` listed finite roots across the six representative packets are
excluded as actual full-Hankel support witnesses.

Non-claims: this covers only the representative packet rows.  It is not a
quotient-image audit, not a statement about every rank-6..11 row, and not a
replacement for the singular/pivot chart program.
