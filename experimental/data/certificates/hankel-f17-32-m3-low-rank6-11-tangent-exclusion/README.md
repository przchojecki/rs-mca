# F17^32 M3 Rank-6..11 Low-Rank Tangent Exclusion

This directory contains a deterministic tangent/common-code-line exclusion
audit for the synthetic low-rank finite-slack families in the M3 regular
window `385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_tangent_exclusion.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_tangent_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json
```

For rank `s`, moment zero gives

```text
Syn_0(u+zv)=|X|+s z.
```

Since `6 <= s <= 11` is nonzero in characteristic `17`, the only possible
common-code-line slope is `z=-|X|/s`.  The verifier recomputes the compressed
regular-minor polynomial and checks `Delta_s(-|X|/s) != 0` for all `252`
rank/agreement pairs.

The source finite-root certificates count `238` finite roots across ranks
`6..11`.  This audit proves common-code-line tangent overlap `0`, so all `238`
remain after tangent/common-code-line subtraction.

Non-claims: this is a synthetic-family tangent audit only, not a quotient-image
subtraction table, not a universal M3 row bound, and not a classification of
arbitrary non-proportional pencils.
