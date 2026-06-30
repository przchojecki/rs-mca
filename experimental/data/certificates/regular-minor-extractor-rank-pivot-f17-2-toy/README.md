# Extension Regular Minor Rank-Pivot Toy

This replay exercises the `rank_at_nodes` row-set strategy over an explicit
polynomial-basis extension field:

```text
F_17^2 = F_17[x]/(x^2-3).
```

It embeds the `F_17` rank-pivot toy in `F_17^2`.  The deterministic selector
tests node `0`, then node `1`, and finds row set `[0,1,3]`; the extracted
determinant is `13 Z^3`, with root union `{0}` encoded as a base-17 integer.

Regenerate and check:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_rank_pivot_toy.json \
  --write experimental/data/certificates/regular-minor-extractor-rank-pivot-f17-2-toy/f17_2_n10_k4_a8_rank_pivot_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_rank_pivot_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-f17-2-toy/f17_2_n10_k4_a8_rank_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-f17-2-toy/f17_2_n10_k4_a8_rank_pivot_packet.json
```

This is a machinery test for the extension-field path, not a prize-row result.
