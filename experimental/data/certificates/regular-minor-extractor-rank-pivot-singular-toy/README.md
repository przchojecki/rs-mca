# Regular Minor Rank-Pivot Singular Toy

This replay exercises the singular-declaration side of the `rank_at_nodes`
row-set strategy.

The toy row has

```text
F = F_17,   n = 10,   k = 4,   A = 8,   j = 2,   t = 4.
```

The supplied syndrome pencil is identically zero.  The selector tests `j+2=4`
finite nodes and finds no full-rank specialization.  Since every maximal minor
has degree at most `j+1=3`, vanishing at four distinct nodes proves that every
maximal regular minor is identically zero.

Regenerate and check:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_singular_toy.json \
  --write experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/f17_n10_k4_a8_rank_pivot_singular_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_singular_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/f17_n10_k4_a8_rank_pivot_singular_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/f17_n10_k4_a8_rank_pivot_singular_packet.json
```

This is a machinery test for singular regular-bucket declarations, not a
singular pivot-chart certificate.
