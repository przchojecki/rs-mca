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

The companion local-tail input extends the stored syndrome by one moment.  The
first `t+j=6` visible moments still satisfy `u=5v`, but the seventh moment
breaks full proportionality.  Its packet therefore records
`proportional_window_single_slope`, `residual_single_slope=12`,
`full_syndrome_proportional=false`, and `residual_charge=tail_check_required`.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_scalar5_rank_pivot_tangent_residual_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_tangent_residual_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_scalar5_rank_pivot_local_residual_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_local_single_slope_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_tangent_residual_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_local_single_slope_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/invalid_bad_tangent_residual_audit_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/invalid_bad_proportional_replay_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/invalid_local_window_tangent_charge_packet.json
```

Non-claims: this is a toy residual-classification packet, not actual M3 row
data and not a prize-row bound.

The replay-failure packet points at the same SHA-checked proportional input but
claims scalar `6` and slope `11`; the checker recomputes scalar `5` and slope
`12`.

The `invalid_bad_tangent_residual_audit_packet.json` fixture also points at the
same input but falsely sets `full_syndrome_proportional=false`; replay shows the
stored syndrome is fully proportional.

The local-window tangent-charge negative fixture points at the local-tail input
but falsely claims the tangent/common-code-line ledger can pay the slope; replay
keeps the one-slope compression but rejects the full-syndrome flag.
