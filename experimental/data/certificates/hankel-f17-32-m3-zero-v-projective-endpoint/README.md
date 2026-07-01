# F17^32 M3 Zero-v Projective Endpoint

Status: PROVED / AUDIT.

This directory records the zero-direction-syndrome branch for the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A` and `t=A-256`.  If the full direction
syndrome is `v=0`, then

```text
M_A(Z) = H_{t,j}(u),
M_A[Z0:Z1] = Z0 H_{t,j}(u).
```

Thus:

```text
rank H_{t,j}(u) = j+1:
  some maximal minor is a nonzero constant;
  there are no finite affine regular roots.

rank H_{t,j}(u) <= j:
  every finite regular minor vanishes;
  the finite bucket is singular and must go to M5 pivots or a separate paid
  classification.
```

In both cases, the projective endpoint `[0:1]` has direction syndrome `v=0`.
It is a codeword direction, paid by the tangent/common-code-line ledger, so its
residual projective aperiodic contribution is `0`.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_zero_v_projective_endpoint.py \
  --write experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/f17_32_n512_k256_m3_zero_v_projective_endpoint.json

python3 experimental/scripts/verify_m1_hankel_zero_v_projective_endpoint.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/f17_32_n512_k256_m3_zero_v_projective_endpoint.json
```
