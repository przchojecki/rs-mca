# KoalaBear rank-eleven rank-one pair-anticode certificate

Schema: `kb-mca-rank11-rank-one-pair-anticode-router-v1`

Exact parent: `6a5dcdae1591fc7f044eda6a942bfe178521a48c`

The canonical payload records:

- the full `GF(3)` maximal-clique control for `2 x 2` rank-one matrix
  anticodes;
- the full `GF(5)` degree-`<3` common-root control;
- the common-core-aware affine-ray scan over all `0<=u<=K-1`;
- the proper affine-space caps for dimensions `0` through `10`;
- explicit nonclaims and zero active-v4 movement.

Canonical payload SHA-256:
`7190997f4e6e464ce41aa3c8389968985686604ad81e9b272ca7c07130d323a5`.

Replay:

```bash
python experimental/scripts/verify_kb_mca_rank11_rank_one_pair_anticode_router_v1.py
python experimental/scripts/verify_kb_mca_rank11_rank_one_pair_anticode_router_v1.py --json
python experimental/scripts/verify_kb_mca_rank11_rank_one_pair_anticode_router_v1.py --tamper-selftest
python experimental/scripts/verify_kb_mca_rank11_rank_one_pair_anticode_router_v1_independent.py
wolframscript -file experimental/scripts/verify_kb_mca_rank11_rank_one_pair_anticode_router_v1.wl
```
