# 433-1b cell-11 signed-pair route cut

`raw.json` is the compact output of
`replay_kb_mca_v4_433_1b_cell11_signed_pair_guard_v1.py`.

The exact degree-16 resultant has the factorization

```text
N0 * D0^5 * (w0-t^2) * (w0+1) * Q2(w0),
```

where `Q2` is quadratic and its discriminant is not a square in the declared
degree-four function tower.  The certificate also contains one guarded
deployed-field point on the residual signed-pair incidence.  This cuts the
attempted transplantation of the 433-1a guard factorization; it does not close
cell 11 or change a v4 ledger atom.

Replay:

```bash
python3 experimental/scripts/replay_kb_mca_v4_433_1b_cell11_signed_pair_guard_v1.py \
  --output experimental/data/certificates/kb-mca-v4-433-1b-cell11-signed-pair-route-cut-v1/raw.json \
  --scan-r-values 256
python3 experimental/scripts/verify_kb_mca_v4_433_1b_cell11_signed_pair_route_cut_v1.py
```
