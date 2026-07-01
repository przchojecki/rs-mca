# F17^32 M3 Rank-9..11 Low-Rank Finite-Slack Sweep

This directory contains a deterministic all-window finite-slack sweep for the
synthetic low-rank family in the M3 regular window `385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank9_11_slack_sweep.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank9_11_slack_sweep.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json
```

Ranks `9`, `10`, and `11` are beyond the v4 low-rank degree envelope:
degree-only projective accounting gives `10`, `11`, and `12` against budget
numerator `6`.  The sweep computes `gcd(Delta,Z^q-Z)` over `F_17^32` for every
rank/agreement pair.

The exact finite-root histograms are:

```text
rank 9 : {0:17, 1:17, 2:6, 3:2}
rank 10: {0:8, 1:23, 2:9, 3:2}
rank 11: {0:15, 1:16, 2:5, 3:6}
```

Thus every checked rank/agreement pair has at most three finite regular roots,
and after the one corrected projective infinity point at most four projective
regular roots against budget numerator `6`.

Non-claims: this is a synthetic family only, not a universal row table, not a
quotient/tangent subtraction table, not a worst-case M3 bound, and not a claim
about ranks beyond `11`.
