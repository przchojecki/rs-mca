# Hankel Rank-6 A385 Two-Core Conic-Pair Safety

Status: PROVED / AUDIT.

This note records the fixed two-core conic-pair criterion for the separated
rank-6 boundary at

```text
A = 385.
```

It does not close all of `A=385`.  It closes the branch where the counted
split-locator candidates share a fixed forced base-root core

```text
E subset X,       |E| = 2,
```

and two residual direction-consistency conics on the resulting projective
`Q`-plane have no common component over the algebraic closure.

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

Two distinct base roots impose two independent linear conditions on the
five-dimensional space of polynomials `deg Q < 5`.  After factoring the fixed
core `E`, one has

```text
Q = E R,       deg R < 3,
```

so the residual search space is a projective plane.

Choose a direction node `y0` and comparison nodes `y1,y2`.  The equality of
finite-slope ratios with `y0` gives two conics on the residual projective
plane:

```text
F_i(R) =
  N_{y_i}(R)D_{y0}(R) - N_{y0}(R)D_{y_i}(R),
  i = 1,2.
```

Every finite root satisfies all direction consistency equations, hence lies in

```text
F_1(R) = F_2(R) = 0.
```

If `F_1` and `F_2` have no common component over the algebraic closure, Bezout
gives intersection length at most `4`.  Therefore there are at most four
compatible projective `Q`-classes.  For each compatible non-slope-free class,
the six direction equations determine at most one finite slope; slope-free
classes have `H(v)L_Q=0` and add no finite noncontained parameter.

Thus the branch has

```text
finite noncontained slopes <= 4.
```

Adding the single projective endpoint gives

```text
support-wise projective contribution <= 5 <= 6.
```

The remaining fixed two-core residual is exactly the common-component case on
the residual `Q`-plane.  This is the `A=385` analogue of the earlier `A=386`
conic-pair residual, but now reached after factoring two forced base roots.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_conic_pair_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-conic-pair-safety/f17_32_n512_k256_m3_rank6_a385_two_core_conic_pair_safety.json
```

Nonclaims:

```text
no closure of the fixed two-core common-component residual;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem, only endpoint-budget accounting;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
