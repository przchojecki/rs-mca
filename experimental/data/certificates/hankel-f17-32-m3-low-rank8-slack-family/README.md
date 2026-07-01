# F17^32 M3 Rank-8 Low-Rank Finite-Slack Family

This directory contains a deterministic all-window finite-slack certificate for
the synthetic rank-8 low-rank family in the M3 regular window `385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank8_slack_family.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank8_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json
```

Rank `8` is beyond the v4 low-rank degree envelope: degree-only finite
accounting gives `8 > 6`, and degree-only projective accounting gives `9 > 6`.
This certificate supplies exact finite-root slack for the nested synthetic
family by computing `gcd(Delta,Z^q-Z)` over `F_17^32` for every agreement.

The exact finite-root histogram is:

```text
0 roots: 22 rows
1 root : 10 rows
2 roots:  7 rows
3 roots:  2 rows
4 roots:  1 row
```

Thus every agreement has at most four finite regular roots, and after the one
corrected projective infinity point every agreement has at most five projective
regular roots against budget numerator `6`.

Non-claims: this is a synthetic family only, not a universal row table, not a
quotient/tangent subtraction table, and not a worst-case M3 bound.
