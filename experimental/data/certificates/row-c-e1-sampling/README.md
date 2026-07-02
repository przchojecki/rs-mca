# Row-C E1 value-set sampling pilot

This directory contains the deterministic pilot artifact for the E1 / Q3.1
Row-C slack-one quotient value-set sampler.

- `row_c_e1_sampling_pilot.json` records the Row-C prime, compatible quotient
  orders, skipped non-divisor orders from the original E1 sketch, sample counts,
  duplicate-pair counts, and the zero-collision effective-support lower bound.
- The generating script is
  `experimental/scripts/verify_row_c_e1_value_set_sampler.py`.
- The companion note is
  `experimental/notes/roadmaps/e1_row_c_value_set_sampling.md`.

Replay:

```bash
python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py --emit
```
