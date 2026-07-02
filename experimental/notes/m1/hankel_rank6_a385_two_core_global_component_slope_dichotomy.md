# Hankel Rank-6 A385 Two-Core Global-Component Slope Dichotomy

Status: PROVED / AUDIT.

This note refines the fixed two-core global-component residual left by

```text
experimental/notes/m1/hankel_rank6_a385_two_core_component_cut_safety.md
```

It applies to the separated rank-6 boundary at

```text
A = 385.
```

After a fixed forced two-point base core is factored, write

```text
Q = E R,       deg R < 3.
```

The residual `Q`-space is a projective plane.  The component-cut packet leaves
the case where an irreducible component `G` of that plane is contained in all
pairwise direction-consistency conics.

For each direction node `y`, put

```text
N_y(R) = Omega_y E(y) R(y),
D_y(R) = b_y L_{E R}(y).
```

Both are linear forms on the residual `Q`-plane.  The pairwise consistency
conics are

```text
C_{y,y'}(R) = N_y(R)D_{y'}(R) - N_{y'}(R)D_y(R).
```

Let `G` be an irreducible component contained in all these conics.  If some
pair `(N_y,D_y)` is not identically zero on `G`, then

```text
zeta_G = [N_y:D_y] : G --> P^1
```

is a rational projective slope map.  The pairwise conics make this map
independent of `y` wherever two such pairs are both defined.

Every finite root represented by a `Q`-class on the domain of definition of
`zeta_G` has finite slope

```text
z = N_y(R) / D_y(R),
```

before the split-locator gate possibly removes it.  Therefore, if `zeta_G` is
constant, the non-base part of `G` contributes at most one finite slope.  The
endpoint-uniform theorem contributes one projective endpoint, so the
projective contribution of this non-base branch is at most

```text
1 + 1 = 2 <= 6.
```

The remaining fixed two-core global-component residuals are now explicit:

```text
determined nonconstant slope map;
slope-free base locus or slope-free global component.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_global_component_slope_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy/f17_32_n512_k256_m3_rank6_a385_two_core_global_component_slope_dichotomy.json
```

Nonclaims:

```text
no closure of fixed two-core nonconstant moving-slope components;
no closure of fixed two-core slope-free base loci or components;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem, only endpoint-budget accounting;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
