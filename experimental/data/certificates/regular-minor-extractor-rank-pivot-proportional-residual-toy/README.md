# Rank-Pivot Proportional Residual Toy

This directory contains a small `F_17` v9 packet exercising the proportional
window residual classifier in the regular-minor extractor.

The input has `n=10`, `k=4`, `A=8`, so `j=2`, `t=4`, and the regular minors
are `3 x 3`.  It sets

```text
u = 5 v,
v = (1,2,4,8,16,15),
```

so the visible Hankel window is proportional, but `H(v)` has rank one.  The
input does not use `certificate_mode=scalar_multiple_roots`; the extractor
detects the visible scalar `c=5` from the ordinary syndrome-pencil data.  The
`rank_at_nodes` proof tests `j+2=4` finite slopes and proves all maximal regular
minors vanish identically.  The proportional-window lemma then labels the
residual as tangent/common-code-line with single slope `12=-5`.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_scalar5_rank_pivot_tangent_residual_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_tangent_residual_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_tangent_residual_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/invalid_bad_tangent_residual_audit_packet.json
```

Non-claims: this is a toy residual-classification packet, not actual M3 row
data and not a prize-row bound.
