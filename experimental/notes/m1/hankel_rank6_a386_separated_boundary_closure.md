# Hankel Rank-6 A386 Separated Boundary Closure

Status: PROVED / AUDIT.

This note composes the `A=386` separated rank-6 boundary packets into one
closed branch statement.  It applies only to separated supports:

```text
|X| = j+1 = 127,     |Y| = 6,     X cap Y = empty,
A = 386,             j = 126.
```

For arbitrary nonzero base and direction weights on such supports, the
boundary low-degree transfer gives

```text
h = |X union Y| - t = 3,        [Q] in P^2.
```

Every finite bad slope is represented by a projective `Q`-class satisfying the
six direction-consistency equations before the split-locator divisor gate is
applied.  The branch partition is:

```text
1. Two direction-consistency conics have no common component.
   Bezout gives at most four finite Q-classes; with the endpoint, the total is
   <= 5 <= 6.

2. A common component is present, and each irreducible component is cut by some
   direction-consistency conic.
   The component-cut plus off-component Bezout bound gives at most four finite
   Q-classes; with the endpoint, the total is again <= 5 <= 6.

3. An irreducible component is contained in every direction-consistency conic.
   The global-component slope dichotomy splits this into constant-slope,
   slope-free, and nonconstant moving-slope branches.
```

The constant-slope branch contributes at most one finite parameter off the base
locus, hence at most two projective parameters after the endpoint.  The
slope-free transfer vectors satisfy both

```text
H(v)L_Q = 0,     H(u)L_Q = 0,
```

so they fail the finite and projective noncontainment gates and add no
support-wise parameter.  If the same finite parameter also has an independent
noncontained vector, that parameter is charged once through the non-slope-free
branch; the slope-free vector is only a contained shadow.

The only remaining non-slope-free residual is a nonconstant moving-slope
component.  In the `A=386` conic tree, every irreducible global component is a
line or an irreducible conic.  The moving-slope split-incidence packet closes
both types for every external forced-core size after the product-collapse,
punctured-tail, and exact-tail refinements.  Thus no separated-support
rank-6 `A=386` boundary residual remains live.

The conclusion is:

```text
For separated supports and arbitrary nonzero weights at A=386, the support-wise
projective contribution of the rank-6 boundary branch is <= 6.
```

This is a local M3/M4 branch theorem, not a row-level safe-side theorem.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_separated_boundary_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-separated-boundary-closure/f17_32_n512_k256_m3_rank6_a386_separated_boundary_closure.json
```

Nonclaims:

```text
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem, only endpoint-budget accounting;
no arbitrary non-separated rank-6 root table;
no row-level M3 safe-side bound.
```
