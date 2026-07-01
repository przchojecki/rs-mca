# F17^32 M3/M4 Projective Budget Split

Status: PROVED / AUDIT.

This directory records the M4 budget consequence obtained by combining two
proved local packets for the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A`, `t=A-256`, and

```text
M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v),
r = rank H_{t,j}(v).
```

The direction-rank degree cap gives, for a nonsingular regular bucket,

```text
finite affine root count <= r.
```

The projective-infinity kernel chart separates the single endpoint `[0:1]`.
It is empty under kernel containment and otherwise contributes at most one
projective parameter.  Thus the projective regular contribution satisfies

```text
B_projective <= r + e_infty,    e_infty in {0,1} as an upper-bound indicator.
```

For this row,

```text
floor(17^32/2^128) = floor((17^32+1)/2^128) = 6.
```

Therefore:

```text
r <= 5:
  projective-safe without an endpoint payment, since r+1 <= 6.

r = 6:
  finite-safe, but projective endpoint-sensitive; it needs endpoint empty/paid
  or an exact finite root table with at most 5 surviving roots.

r > 6:
  rank cap alone is not enough; exact root tables or further ledgers are needed.
```

This is an abstract M4 decision-table refinement for arbitrary nonsingular
regular buckets.  It does not duplicate the separate synthetic low-rank
quotient-image packets.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_projective_budget_split.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/f17_32_n512_k256_m3_m4_projective_budget_split.json

python3 experimental/scripts/verify_m1_hankel_m4_projective_budget_split.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/f17_32_n512_k256_m3_m4_projective_budget_split.json
```
