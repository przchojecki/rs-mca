# F17^32 M3/M5 Regular-Root Rank-Drop Bridge

Status: PROVED.

This directory records the bridge between v10 regular-minor root tables and
the M5 finite-affine kernel filter for the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A`, `t=A-256`, and

```text
M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v).
```

Let `G_A(Z)` be the v10 canonical regular gcd: the gcd of all nonzero maximal
row-set minors of `M_A(Z)`.

The bridge is:

```text
z root of G_A  =>  rank M_A(z) <= j.
```

All nonzero maximal minors vanish at `z` by definition of the gcd root, and
the identically zero maximal minors vanish at every slope.  Hence every
maximal minor of `M_A(z)` is zero.

Conversely, in a nonsingular regular bucket, if `rank M_A(z)<=j` for a finite
field element `z`, then all nonzero maximal-minor polynomials vanish at `z`, so
`z` is a root of `G_A`.

Combining this with the finite-affine kernel chart:

```text
rank H_{t,j}(v) > rank M_A(z)
  => z survives the ambient noncontainment filter.
```

In particular, if `H_{t,j}(v)` has full column rank `j+1`, then every finite
regular root survives the ambient kernel filter.  Such roots need actual root
tables and then quotient, extension, subfield, or split-locator audits; they
cannot be removed by same-support kernel containment.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m5_regular_root_rank_drop.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/f17_32_n512_k256_m3_m5_regular_root_rank_drop.json

python3 experimental/scripts/verify_m1_hankel_m5_regular_root_rank_drop.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/f17_32_n512_k256_m3_m5_regular_root_rank_drop.json
```
