# Hankel Proportional-Pencil Tangent Lemma

Status: PROVED / AUDIT.

This directory records a reusable M3/M4 subtraction lemma for the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

For exact agreement `A` in the regular window `385 <= A <= 426`, write

```text
j = 512-A,
t = A-256.
```

Assume the full stored syndrome vectors satisfy

```text
u_m = c v_m,        0 <= m < 256.
```

Then for every maximal row set `R` of size `j+1`,

```text
M_A(Z) = H_{t,j}(u) + Z H_{t,j}(v) = (Z+c) H_{t,j}(v),
Delta_R(Z) = (Z+c)^(j+1) det(H_R(v)).
```

Thus the regular branch has the same dichotomy as the zero-`u` branch after
the translation `Z -> Z+c`:

```text
rank H_{t,j}(v) = j+1:
  the canonical monic gcd over all nonzero maximal minors is (Z+c)^(j+1);
  the only finite root is Z=-c;
  at Z=-c the full stored syndrome is zero, so the root is paid by the
  tangent/common-code-line ledger.

rank H_{t,j}(v) <= j:
  every maximal minor vanishes;
  the regular bucket is singular and must go to M5 pivots or a separate
  paid-branch classification.
```

In this M3 window `t+j=256` for every agreement, so the visible Hankel relation
uses exactly the full stored syndrome.  There is no hidden tail beyond the
proportionality check.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --write experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json

python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --check experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json
```
