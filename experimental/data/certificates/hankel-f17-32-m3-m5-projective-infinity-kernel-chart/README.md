# F17^32 M3/M5 Projective-Infinity Kernel Chart

Status: PROVED.

This directory records the M5 projective-infinity chart refinement for the
pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A`, `t=A-256`, and

```text
A_matrix = H_{t,j}(u),    B_matrix = H_{t,j}(v).
```

The projective-infinity chart is the locus

```text
B_matrix * ell = 0,
A_matrix * ell != 0.
```

Therefore the ambient linear chart is empty exactly when

```text
ker H_{t,j}(v) subset ker H_{t,j}(u),
```

equivalently when

```text
rank stack(H_{t,j}(v), H_{t,j}(u)) = rank H_{t,j}(v).
```

If the containment fails, the projective parameter contribution is still only
the single endpoint `[0:1]`.  The packet records this as a `dimension_degree`
fallback of degree `1`.  It does not claim that the split-locator chart is
nonempty whenever the ambient linear chart is nonempty.

Immediate consequences:

```text
rank H(v)=j+1:
  infinity chart empty.

u=c v:
  ker H(v) subset ker H(u), so infinity chart empty even when H(v) is
  rank-deficient.

v=0:
  the ambient chart is empty iff H(u)=0; if nonempty, the single endpoint is
  paid by the zero-v tangent/common-code-line endpoint ledger.
```

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m5_projective_infinity_kernel_chart.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json

python3 experimental/scripts/verify_m1_hankel_m5_projective_infinity_kernel_chart.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json
```
