# F17^32 M3 Direction-Rank Degree Cap

Status: PROVED / AUDIT.

This directory records a finite-affine regular-minor theorem for the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A` and `t=A-256`.  Let

```text
M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v),
r = rank H_{t,j}(v).
```

For every maximal row set `R`, the determinant

```text
Delta_R(Z)=det(H_R(u)+Z H_R(v))
```

has degree at most `r`.  Indeed, the coefficient of `Z^d` is a sum of
determinants using `d` columns from `H_R(v)`, and all such determinants vanish
when `d>rank H_R(v)`.

Consequences:

```text
if the regular bucket is nonsingular:
  deg canonical_gcd <= r;
  finite affine root count <= r.

for this row:
  floor(17^32/2^128)=6,
  so direction rank r<=6 gives a finite regular root count within budget.
```

This is only a finite-affine cap.  Projective infinity is governed by the
separate projective-infinity rank criterion: full direction rank excludes
`[0:1]`, while deficient direction rank leaves a singular infinity chart.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_direction_rank_degree_cap.py \
  --write experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/f17_32_n512_k256_m3_direction_rank_degree_cap.json

python3 experimental/scripts/verify_m1_hankel_direction_rank_degree_cap.py \
  --check experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/f17_32_n512_k256_m3_direction_rank_degree_cap.json
```
