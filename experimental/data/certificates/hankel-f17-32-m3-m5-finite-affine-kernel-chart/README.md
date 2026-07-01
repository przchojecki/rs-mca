# F17^32 M3/M5 Finite-Affine Kernel Chart

Status: PROVED.

This directory records the M5 finite-affine noncontainment refinement for the
pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A`, `t=A-256`, and for a fixed finite
slope `z` set

```text
M_z = H_{t,j}(u) + z H_{t,j}(v),
B   = H_{t,j}(v).
```

The ambient finite-affine noncontainment chart is

```text
M_z ell = 0,
B ell != 0.
```

It is empty exactly when

```text
ker M_z subset ker B,
```

equivalently when

```text
rank stack(M_z, B) = rank M_z.
```

If containment fails, the fixed slope `z` contributes at most one finite
parameter.  The packet records this as a per-root `dimension_degree` fallback
of degree `1`.  It does not claim that the split-locator chart is nonempty
whenever the ambient linear chart is nonempty.

This is the finite-affine analogue of the projective-infinity kernel chart.
Future root tables can apply this test to each regular root before counting it
as an aperiodic support-wise MCA candidate.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m5_finite_affine_kernel_chart.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json

python3 experimental/scripts/verify_m1_hankel_m5_finite_affine_kernel_chart.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json
```
