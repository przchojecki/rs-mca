# F17^32 M3 Projective Split-Locator Gate

Status: PROVED / AUDIT.

This packet is the projective-infinity companion to the finite
null-polynomial split-locator gate.  It applies to the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For the homogenized M3 pencil

```text
M_A[Z0:Z1] = Z0 H_{t,j}(u) + Z1 H_{t,j}(v),
```

the ambient projective-infinity chart is

```text
H_{t,j}(v) ell = 0,     H_{t,j}(u) ell != 0.
```

This chart is still an ambient Hankel chart.  It becomes a genuine support-wise
split-locator endpoint only when the kernel vector `ell` normalizes to a monic
degree-`j` polynomial `L(X)` that divides `X^512-1`.  Because the descriptor
domain is an exact order-512 subgroup and characteristic 17 does not divide
512, `X^512-1` is squarefree and its monic degree-`j` divisors are exactly the
locators of `j`-subsets of `H`.

For direction rank `6`, the ambient projective kernel dimension is
`j+1-6`, ranging from `81` to `122` across the M3 window.  This large ambient
kernel is therefore not by itself an endpoint count: future rank-6 packets must
intersect it with the split-locator divisor gate and then test noncontainment.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m3_projective_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/f17_32_n512_k256_m3_projective_split_locator_gate.json
```
