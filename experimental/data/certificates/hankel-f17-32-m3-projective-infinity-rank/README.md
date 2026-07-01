# F17^32 M3 Projective-Infinity Rank Criterion

Status: PROVED / AUDIT.

This directory records the projective-infinity endpoint criterion for the M3
regular window of the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A` and `t=A-256`.  Homogenize the
regular pencil as

```text
M_A[Z0:Z1] = Z0 H_{t,j}(u) + Z1 H_{t,j}(v).
```

For every maximal row set `R` of size `j+1`, the projective minor satisfies

```text
Delta_R(0,1) = det(H_R(v)).
```

Therefore:

```text
rank H_{t,j}(v) = j+1:
  some maximal row set has det(H_R(v)) != 0;
  the regular minors exclude the projective-infinity point [0:1];
  projective-infinity contribution is 0.

rank H_{t,j}(v) <= j:
  every maximal minor vanishes at [0:1];
  the endpoint is a singular projective-infinity chart requiring a pivot packet
  or a separate paid endpoint classification.
```

This is a projective accounting lemma.  It does not prove that a
rank-deficient infinity endpoint is an actual support-wise bad slope; it says
the regular-minor chart does not close that endpoint.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_projective_infinity_rank_criterion.py \
  --write experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/f17_32_n512_k256_m3_projective_infinity_rank_criterion.json

python3 experimental/scripts/verify_m1_hankel_projective_infinity_rank_criterion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/f17_32_n512_k256_m3_projective_infinity_rank_criterion.json
```
