# Row-C E1 value-set sampling pilot

This directory contains deterministic evidence artifacts for the E1 / Q3.1
Row-C slack-one quotient value-set sampler.

- `row_c_e1_sampling_pilot.json` records the Row-C prime, compatible quotient
  orders, skipped non-divisor orders from the original E1 sketch, sample counts,
  duplicate-pair counts, and the zero-collision effective-support lower bound.
- `row_c_e1_sampling_n64_2pow24_exact.json` records the larger exact
  `N'=64`, `2^24`-sample follow-up.  It observes one duplicate pair, consistent
  with the full-value-set birthday expectation rather than a heavy-collision
  signal.  The duplicate-witness replay shows that duplicate is the same
  antipodal class sampled twice, not a distinct-class `e_1` collision.
- `row_c_e1_collision_norm_criterion.json` records the Q2.15 cyclotomic norm
  gate: fixed-embedding collisions imply norm divisibility, and norm
  divisibility produces a collision in some Galois-conjugate embedding.  It
  also records the distinct exceptional-prime divisor budget for the checked
  pair families, the Row-C graded collision-radius table, and the QA.14
  cluster-certificate lemmas.
- `e1_sharp_norm_height_constants.json` records the sharp height exponent
  `phi(N') log(2 ell')`, the deployed bit-budget transfer frontiers, and the
  Row-C pure-height stopping point.
- The generating script is
  `experimental/scripts/verify_row_c_e1_value_set_sampler.py`.
- Companion notes:
  `experimental/notes/roadmaps/e1_row_c_value_set_sampling.md`,
  `experimental/notes/roadmaps/e1_collision_norm_criterion.md`, and
  `experimental/notes/roadmaps/e1_cluster_certificates.md`,
  `experimental/notes/roadmaps/e1_sharp_norm_height_constants.md`.

Replay:

```bash
python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py --emit
python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py \
  --orders 64 --samples 16777216 --mode exact-set --emit \
  --output experimental/data/certificates/row-c-e1-sampling/row_c_e1_sampling_n64_2pow24_exact.json
python3 experimental/scripts/verify_row_c_e1_collision_norm_criterion.py --emit
python3 experimental/scripts/verify_e1_sharp_norm_height_constants.py --emit
```
