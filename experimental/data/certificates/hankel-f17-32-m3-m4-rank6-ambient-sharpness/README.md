# F17^32 M3/M4 Rank-6 Ambient Sharpness

Status: COUNTEREXAMPLE / AUDIT.

This packet records a sharpness example for the M4 rank-6 projective boundary
in the pinned M3 dimensions

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

It is deliberately an **ambient regular-pencil** example, not a Hankel
moment-pencil example.

For exact agreement `A`, set `m=j+1=513-A` and `t=A-256`.  Choose distinct
row parameters `alpha_0,...,alpha_{t-1}` from the descriptor domain and form

```text
C_{r,i} = alpha_r^i,      0 <= i < m.
```

Every maximal row-set minor of `C` is a nonzero Vandermonde determinant.  Let

```text
D(Z)=diag(Z-1,Z-2,Z-3,Z-4,Z-5,Z-6,1,...,1),
M(Z)=C D(Z)=A+ZB.
```

Then

```text
rank B = 6,
det M_R(Z) = det(C_R) * prod_{a=1}^6 (Z-a)
```

for every maximal row set `R`.  Hence the canonical regular gcd has exactly
six finite roots.  Also `e_7` lies in `ker B`, while `A e_7` is the nonzero
seventh column of `C`, so the projective-infinity ambient chart is nonempty.

Consequently the rank-6 endpoint-sensitive boundary from the M4 budget split
is sharp at the ambient regular-pencil level:

```text
six finite roots + one projective endpoint = 7 > budget 6.
```

The next proof step cannot use only direction rank, regular nonsingularity, and
the one-point projective endpoint bound.  It must use extra structure: Hankel
moment constraints, exact finite root tables, paid endpoint ledgers, or
split-locator equations beyond the ambient linear chart.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_rank6_ambient_sharpness.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json

python3 experimental/scripts/verify_m1_hankel_m4_rank6_ambient_sharpness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json
```
