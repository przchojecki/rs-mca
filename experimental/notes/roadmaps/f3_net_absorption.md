# F3: affine-net absorption by mixed degree-1 pullbacks

- **DAG node:** `p3_affine_net_richline_residue`.
- **Task:** F3.
- **Status:** PROVED for the P3 fixed-subcore affine-plane model, under the
  unified pullback strip.
- **Verifier:** `experimental/scripts/verify_f3_net_absorption.py`.

## Statement

In the P1/P3 fixed-subcore reduction, each off-core point contributes an
affine branch

```text
L_i(z) = alpha_i + beta_i z
```

in the `(z,a)` parameter plane.  A partner through the fixed subcore is a
`(t+1)`-rich point `(z0,a0)`, meaning at least `t+1` branches satisfy
`L_i(z0)=a0`.

Every multi-direction affine-net rich point is paid by the unified pullback
strip: it decomposes into mixed `b=2` degree-1 pullback cells.

## Proof

Let `I` be the incident branches at a rich point `(z0,a0)`.

If all incident branches have the same direction, then distinct branches are
parallel and cannot meet.  Thus either the incident lines are duplicate copies
of one line, which is tangent/pencil bookkeeping, or the point is not a genuine
multi-direction net.

Otherwise choose a pivot branch `L_0` and, after discarding duplicate copies,
choose the pivot so every other incident branch has a nonzero direction
difference from it.  For every `i in I \ {0}` define

```text
Delta_i(Z) = L_i(Z) - L_0(Z).
```

Since the directions differ, `Delta_i` is a nonzero degree-1 polynomial.  Since
both branches pass through `(z0,a0)`, it has the unique root

```text
Delta_i(z0) = 0.
```

This is exactly the `b=2` fiber dictionary.  The unordered pair of affine
branches is represented by

```text
(Y - L_0(Z))(Y - L_i(Z))
  = Y^2 - e_1(Z) Y + e_2(Z),
```

where the block symmetric functions

```text
e_1(Z) = L_0(Z) + L_i(Z),
e_2(Z) = L_0(Z)L_i(Z)
```

are the map coefficients.  At `Z=z0`, these specialize to

```text
e_1(z0)=2a0,      e_2(z0)=a0^2,
```

so the pair is a double fiber over the rich value.  The `|I|-1` pair cells
from the pivot to the other incident branches form a spanning tree covering
the whole rich block.  The strip allows mixed maps, so these pair cells need
not come from one global map.

Therefore every multi-direction affine-net rich point is removed by the
unified degree-1 pullback strip.  There is no remaining U3 affine-net residue;
the Vinh/incidence route is not needed for this obstruction.

## Verification

The verifier enumerates the original P3 toy net over `F_193` and additional
generic/adversarial affine-net templates:

```text
case count                 14
rich points charged        342
b=2 pair trades            726
local fiber identities     4314
```

The original P3 fixture is replayed exactly: it has `65` post-anchor rich
parameters, and all `65` are charged by mixed `b=2` degree-1 pullback cells.

Run:

```bash
python3 experimental/scripts/verify_f3_net_absorption.py
```
