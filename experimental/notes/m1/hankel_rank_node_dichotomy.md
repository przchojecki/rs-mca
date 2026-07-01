# M3 Rank-Node Dichotomy

Status: PROVED / AUDIT.

In the M3 regular window for

```text
C = RS[F_17^32,H,256],    385 <= A <= 426,
```

write

```text
j = 512 - A,
t = A - 256,
s = j + 1.
```

For the affine regular pencil

```text
M(Z)=H_{t,j}(u)+Z H_{t,j}(v),
```

every maximal `s x s` minor is a polynomial in `Z` of degree at most `s`.

This gives a deterministic dichotomy.  If a finite node `z0` has
`rank M(z0)=s`, Gaussian elimination returns an `s`-row set `R` with
`det M_R(z0) != 0`; hence `det M_R(Z)` is a nonzero regular minor.  If instead
`rank M(z_i)<s` at `s+1` distinct finite nodes, every maximal minor vanishes at
`s+1` points while having degree at most `s`, so every maximal minor is
identically zero.  The bucket is then a genuine singular residual and should be
sent to the M5 pivot atlas rather than treated as a weak root-count bound.

The replay packet is:

```text
experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/
  f17_32_n512_k256_m3_rank_node_dichotomy.json
```

The packet also records a sharpness sanity check: a degree-`s` determinant can
vanish at `s` tested nodes and still be nonzero, so `s+1=j+2` nodes are really
needed for the singular conclusion.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m3_rank_node_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/f17_32_n512_k256_m3_rank_node_dichotomy.json
```
