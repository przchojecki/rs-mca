# Deployed F_17^32 Sparse Moving-Zero Witness

Status: PROVED / EXPERIMENTAL.

This packet instantiates the moving-zero lower bound from
`experimental/notes/thresholds/cap25_v12_sparse_sigma_first_layer_audit.md`
at the deployed-shaped row

```text
C = RS[F_17^32, H, 256], |H| = 512, r = 129.
```

It certifies one sparse pair whose support union has size `129` and has
`258 = n-k+2` distinct finite MCA-bad slopes.

The committed certificate blob is `2,117,771` bytes.  The size is intentional:
it stores 258 first-principles per-slope witness records at `n=512`, including
supports and closing-codeword data.  A slimmer sampled-record packet would be
possible if the maintainer prefers it, but that would trade away this packet's
full per-slope replay surface.

Replay:

```powershell
py -3.13 experimental\scripts\verify_deployed_sparse_witness_f17_32.py --check experimental\data\certificates\deployed-sparse-witness-f17-32\deployed_sparse_witness_f17_32_r129.json --full
```

Fast spot check:

```powershell
py -3.13 experimental\scripts\verify_deployed_sparse_witness_f17_32.py --check experimental\data\certificates\deployed-sparse-witness-f17-32\deployed_sparse_witness_f17_32_r129.json --sample 16
```

Regenerate:

```powershell
py -3.13 experimental\scripts\verify_deployed_sparse_witness_f17_32.py --write experimental\data\certificates\deployed-sparse-witness-f17-32\deployed_sparse_witness_f17_32_r129.json
```

Non-claims: this is not an upper bound on `sigma_C`, not a deployed soundness
claim, not a leaderboard row, and not a replacement for the CAP25 sparse
first-layer audit.
