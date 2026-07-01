# F17^32 M3 Finite Tangent-Overlap Criterion

Status: PROVED / AUDIT.

This certificate records the finite tangent/common-code-line overlap rule for
the pinned M3 regular window

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

For `j=512-A` and `t=A-256`, the largest Hankel syndrome index is

```text
(t-1)+j = 255.
```

Thus every regular Hankel chart in this window sees exactly the full stored
length-256 syndrome.  A finite slope `z` is tangent/common-code-line precisely
when

```text
Syn(f+zg) = u + z v = 0
```

in all stored coordinates.  Therefore:

```text
v != 0:
  finite tangent overlap exists iff u=c v for one scalar c;
  the unique tangent slope is z=-c.

u and v non-proportional:
  no finite regular root is tangent/common-code-line.

v=0, u!=0:
  no finite tangent slope exists.

u=v=0:
  the whole finite line is a degenerate codeword-line branch and is removed
  before aperiodic accounting.
```

This is an M4 no-double-counting lemma.  It does not compute
non-proportional regular root tables; it says future non-proportional finite
root tables have zero tangent/common-code-line overlap.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_finite_tangent_overlap_criterion.py \
  --write experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json

python3 experimental/scripts/verify_m1_hankel_finite_tangent_overlap_criterion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json
```
