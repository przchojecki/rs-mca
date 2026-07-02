# Hankel Rank-6 A385 Three-Core Quadratic Cut

Status: PROVED / AUDIT.

This note records the next fixed-core criterion for the separated rank-6
boundary at

```text
A = 385.
```

It does not close all of `A=385`.  It closes the branch where, after the
four-point base-core branch has been removed, the counted split-locator
candidates share a fixed forced base-root core

```text
E subset X,       |E| = 3,
```

and at least one pairwise direction-consistency equation cuts the resulting
projective `Q`-line by a nonzero binary quadratic.

At `A=385`, the boundary low-degree transfer gives

```text
h = |X union Y| - t = 5,        [Q] in P^4.
```

For a base node `x in X`, the transfer satisfies

```text
a_x L_Q(x) = Omega_x Q(x).
```

The base weight `a_x` and barycentric residue `Omega_x` are nonzero, so a
forced split-locator root at `x` is equivalent to

```text
Q(x) = 0.
```

Three distinct base roots impose three independent linear conditions on the
five-dimensional space of polynomials `deg Q < 5`.  After factoring the fixed
core `E`, one has

```text
Q = E R,       deg R < 2,
```

so the residual search space is a projective line.

For direction nodes `y,y'`, the equality of the two displayed ratios is

```text
N_y(Q)D_y'(Q) - N_y'(Q)D_y(Q) = 0.
```

On the residual `Q`-line this is a binary quadratic.  If at least one such
quadratic is not identically zero, every compatible finite root lies among at
most two projective `Q`-classes.  For each compatible non-slope-free `Q`-class,
the six direction equations determine at most one finite slope.  Slope-free
classes have `H(v)L_Q=0` and contribute no finite noncontained parameter.

Thus the branch has

```text
finite noncontained slopes <= 2.
```

Adding the single projective endpoint gives

```text
support-wise projective contribution <= 3 <= 6.
```

The remaining fixed-three-core residual is therefore precise: all pairwise
direction-consistency quadratics vanish identically on the residual `Q`-line.
That residual should be attacked through slope-map, quotient, or split-locator
structure rather than by another degree-only count.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_three_core_quadratic_cut.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-quadratic-cut/f17_32_n512_k256_m3_rank6_a385_three_core_quadratic_cut.json
```

Nonclaims:

```text
no closure of the ratio-identically-consistent fixed three-core Q-line residual;
no proof that every A=385 over-budget branch has a fixed three-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem, only endpoint-budget accounting;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
