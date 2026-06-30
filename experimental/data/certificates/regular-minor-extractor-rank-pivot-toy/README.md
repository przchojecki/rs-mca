# Regular Minor Rank-Pivot Toy

This replay exercises the `rank_at_nodes` row-set strategy in

```text
experimental/scripts/extract_regular_hankel_minors.py
```

The toy row has

```text
F = F_17,   n = 10,   k = 4,   A = 8,   j = 2,   t = 4.
```

The prefix rows `0,1,2` are singular for the supplied syndrome pencil, but the
deterministic rank-at-nodes selector evaluates the pencil at finite slopes and
finds a nonzero maximal minor on row set `[0,1,3]` at node `1`.

Regenerate and check:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_toy.json \
  --write experimental/data/certificates/regular-minor-extractor-rank-pivot-toy/f17_n10_k4_a8_rank_pivot_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-toy/f17_n10_k4_a8_rank_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-toy/f17_n10_k4_a8_rank_pivot_packet.json
```

This is a machinery test, not a prize-row result.
