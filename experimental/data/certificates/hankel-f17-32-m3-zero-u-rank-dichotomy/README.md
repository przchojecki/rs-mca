# F17^32 M3 Zero-u Rank Dichotomy

Status: PROVED / AUDIT for arbitrary zero-`u` regular buckets.

This directory contains the conceptual endpoint of the zero-`u` part of the
M3 regular-window packet.  For exact agreement `A`, write

```text
j = 512-A,
t = A-256.
```

If the stored syndrome pencil has `u=0`, then the regular Hankel pencil is

```text
M_A(Z) = H_{t,j}(u) + Z H_{t,j}(v) = Z H_{t,j}(v).
```

For every maximal row set `R` of size `j+1`,

```text
Delta_R(Z) = det(Z H_R(v)) = Z^(j+1) det(H_R(v)).
```

Therefore the v10 regular branch has an exact dichotomy:

```text
rank H_{t,j}(v) = j+1:
  at least one maximal minor is nonzero;
  the canonical monic gcd over all nonzero maximal minors is Z^(j+1);
  the only root is Z=0, paid by the tangent/common-code-line ledger.

rank H_{t,j}(v) <= j:
  every maximal minor vanishes;
  the regular bucket is singular and must go to M5 pivots or a separate
  paid-branch classification.
```

This certificate subsumes the weighted rank-size zero-`u` formula as a
full-rank example and uses the lower-rank weighted power-sum certificate as an
example of a separately paid singular boundary.  It does not classify arbitrary
rank-deficient zero-`u` data.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_zero_u_rank_dichotomy.py \
  --write experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/f17_32_n512_k256_m3_zero_u_rank_dichotomy.json

python3 experimental/scripts/verify_f17_32_m3_zero_u_rank_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/f17_32_n512_k256_m3_zero_u_rank_dichotomy.json
```
