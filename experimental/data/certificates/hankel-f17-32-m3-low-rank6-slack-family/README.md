# F17^32 M3 Rank-6 Low-Rank Finite-Slack Family

This directory contains a deterministic all-window finite-slack certificate for
the synthetic rank-6 low-rank family in the M3 regular window `385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank6_slack_family.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json
```

Rank `6` is the first low-rank update size where the v4 packet gate cannot use
degree-only projective accounting: degree `6` plus the corrected projective
infinity point would give `7 > 6`.  This certificate supplies the missing
extra evidence for the nested synthetic family by computing
`gcd(Delta,Z^q-Z)` over `F_17^32` for every agreement.

The exact finite-root histogram is:

```text
0 roots: 16 rows
1 root : 17 rows
2 roots:  9 rows
```

Thus every agreement has at most two finite regular roots, and after the one
corrected projective infinity point every agreement has at most three
projective regular roots against budget numerator `6`.

Non-claims: this is a synthetic family only, not a universal row table, not a
quotient/tangent subtraction table, and not a worst-case M3 bound.
