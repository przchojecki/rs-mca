# Hankel Rank-6 A385 Two-Core Slope-Free Emptiness

Status: PROVED / AUDIT.

This note closes the slope-free residual left by

```text
experimental/notes/m1/hankel_rank6_a385_two_core_global_component_slope_dichotomy.md
```

for the separated rank-6 boundary at

```text
A = 385.
```

After a fixed forced two-point base core is factored, write

```text
Q = E R,       deg R < 3.
```

Here `E` is the product over the two fixed base nodes, and `[R]` is the
residual projective `Q`-class in `P^2`.  For each direction node `y`,

```text
N_y(R) = Omega_y E(y) R(y),
D_y(R) = b_y L_{E R}(y).
```

The separated-support hypothesis gives `y` outside the base support, hence
`E(y) != 0`; the barycentric residue `Omega_y` is also nonzero.  Therefore
`N_y(R)` is a nonzero scalar multiple of the residual evaluation `R(y)`.

The slope-free condition requires

```text
N_y(R) = D_y(R) = 0       for every direction node y.
```

In particular, `R` vanishes at all six distinct direction nodes.  But `R` is a
nonzero residual polynomial of degree `<3`, so it has at most two roots.  This
contradiction rules out slope-free projective classes.

The same pointwise obstruction rules out a slope-free global component: any
nonempty component over the algebraic closure contains a point, and no such
point exists.

Consequently the fixed two-core slope-free base-locus/global-component branch
contributes

```text
0 finite noncontained slopes;
0 projective endpoint parameters.
```

The remaining fixed two-core global-component residual is now only the
determined nonconstant moving-slope branch.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_slope_free_empty.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-slope-free-empty/f17_32_n512_k256_m3_rank6_a385_two_core_slope_free_empty.json
```

Nonclaims:

```text
no closure of fixed two-core nonconstant moving-slope components;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem, because the slope-free branch is empty;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
