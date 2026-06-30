# Rank-At-Nodes Regular Bucket Audit

This directory contains a compact audit certificate for the reusable
rank-at-nodes regular-bucket lemma used by the Hankel regular-minor extractor.

The lemma says that a regular bucket matrix pencil with `j+1` columns has
maximal minors of degree at most `j+1`.  Therefore one full-rank specialization
gives a nonzero regular minor, while failure at `j+2` distinct tested nodes
proves all maximal minors vanish identically.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_rank_at_nodes_regular_bucket.py \
  --write experimental/data/certificates/rank-at-nodes-regular-bucket/rank_at_nodes_regular_bucket_audit.json

python3 experimental/scripts/verify_m1_rank_at_nodes_regular_bucket.py \
  --check experimental/data/certificates/rank-at-nodes-regular-bucket/rank_at_nodes_regular_bucket_audit.json
```

The certificate audits every current non-invalid v9 packet item whose
`extractor_audit.row_set_source` is `rank_at_nodes`.
