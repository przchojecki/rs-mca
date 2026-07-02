# Hankel Rank-6 A385 Base-Core Closure

Status: PROVED / AUDIT.

This note records a fixed-core closure criterion for the separated rank-6
boundary at

```text
A = 385.
```

It does not close all of `A=385`.  It closes the branch where all candidate
split locators in the branch share a forced base-root core

```text
E subset X,       |E| >= 4.
```

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

Four distinct base roots impose four independent linear conditions on the
five-dimensional space of polynomials `deg Q < 5`.  Thus a fixed four-point
base core leaves a one-dimensional vector space of `Q`'s, or one projective
`Q`-class.

For a single `Q`-class, the six direction equations are either inconsistent,
slope-free/contained, or determine one finite slope.  The slope-free case has
`H(v)L_Q=0`, so it does not contribute a finite noncontained parameter.  Hence
the branch has at most one finite noncontained slope.  Adding the single
projective endpoint gives

```text
support-wise projective contribution <= 2 <= 6.
```

Equivalently, any over-budget separated `A=385` rank-6 boundary obstruction
must avoid a common forced four-point base core in the counted branch.  This
pushes the remaining `A=385` work toward low-base-core or moving-core
configurations, not fixed high-base-core ones.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_base_core_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-base-core-closure/f17_32_n512_k256_m3_rank6_a385_base_core_closure.json
```

Nonclaims:

```text
no closure of A=385 branches without a common forced four-point base core;
no proof that every A=385 over-budget branch has such a core;
no overlapping-support rank-6 classification;
no endpoint payment theorem, only endpoint-budget accounting;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
