# F17^32 M3 Low-Rank2-5 Shifted-Minor Exclusion

This directory contains a deterministic audit for the synthetic rank-2..5
low-rank M3 ladder.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_5_shifted_minor_exclusion.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-5-shifted-minor-exclusion/f17_32_n512_k256_m3_low_rank2_5_shifted_minor_exclusion.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_5_shifted_minor_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-5-shifted-minor-exclusion/f17_32_n512_k256_m3_low_rank2_5_shifted_minor_exclusion.json
```

The source rank-2 and rank-3 ledgers enumerate exact finite first-minor roots.
The rank-4 and rank-5 ledgers only need degree bounds for projective budget
safety.  This audit applies the shifted-minor exclusion criterion uniformly:
for every row, the first regular minor and the row-shift-1 minor are coprime in
`F_17^32[Z]`.  Thus the whole finite first-minor root locus is excluded as a
full-Hankel exact-support witness, even in the degree-bound-only ranks.

Result: the audit clears the `82` exact finite roots from ranks 2..3 and the
degree-bound finite root-locus upper total `378` from ranks 4..5.  The surviving
finite full-Hankel witness upper bound is `0`.

Non-claims: this is only for the synthetic low-rank ladder, only for finite
first-minor roots, and not a quotient-image/support audit or a replacement for
the general singular/pivot chart program.
