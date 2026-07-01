# F17^32 M3 One-Spike M4 Budget Table

Status: PROVED / AUDIT for this synthetic family.

This directory records the M4 budget table for the one-spike canonical-empty
family in the M3 regular window.

The finite affine contribution is zero at every agreement because the v10
canonical finite root table is empty.  The projective sampler adds only the
M5 projective-infinity one-point upper bound, so the projective numerator is at
most one.

Both printed denominators have the same `2^-128` budget:

```text
floor(|F_17^32| / 2^128) = 6,
floor((|F_17^32| + 1) / 2^128) = 6.
```

Thus the synthetic family is safe for both finite affine and projective
samplers:

```text
finite:     0 <= 6,
projective: 1 <= 6.
```

This is not a threshold-pinning theorem and does not classify arbitrary
non-proportional pencils.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_one_spike_m4_budget.py \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-m4-budget/f17_32_n512_k256_m3_one_spike_m4_budget.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_m4_budget.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-m4-budget/f17_32_n512_k256_m3_one_spike_m4_budget.json
```
