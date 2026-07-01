# F17^32 M3 Rank-Node Dichotomy

Status: PROVED / AUDIT.

This packet records a finite test for deciding whether a regular M3 Hankel
bucket has a nonzero maximal minor or is genuinely singular.

For exact agreement `A`, put

```text
j = 512 - A,
t = A - 256,
s = j + 1.
```

For a finite affine pencil

```text
M(Z) = H_{t,j}(u) + Z H_{t,j}(v),
```

every `s x s` maximal minor has degree at most `s`.

Therefore:

```text
if rank M(z0)=s at one finite node z0:
  a rank-revealing row set gives a nonzero maximal minor;

if rank M(z_i)<s at s+1 distinct finite nodes:
  every maximal minor vanishes at s+1 roots despite degree <=s,
  so every maximal minor is identically zero.
```

For the pinned `F_17^32` row, the deterministic nodes encoded by
`0,1,...,s` are distinct for every `385 <= A <= 426`.  This gives a replayable
singular/nonsingular gate for future M3 root-table packets.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m3_rank_node_dichotomy.py \
  --write experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/f17_32_n512_k256_m3_rank_node_dichotomy.json

python3 experimental/scripts/verify_m1_hankel_m3_rank_node_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/f17_32_n512_k256_m3_rank_node_dichotomy.json
```
