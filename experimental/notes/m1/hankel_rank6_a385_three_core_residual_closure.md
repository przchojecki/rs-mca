# Hankel Rank-6 A385 Three-Core Residual Closure

Status: PROVED / AUDIT.

This note closes the ratio-identically-consistent fixed three-core residual
left by

```text
experimental/notes/m1/hankel_rank6_a385_three_core_quadratic_cut.md
```

The setting is still local to the separated `A=385` rank-6 boundary branch.
After a fixed forced three-point base core is factored, write

```text
Q = E R,        deg R < 2.
```

The residual `Q`-space is a projective line.  The quadratic-cut packet closed
the case where some pairwise direction-consistency equation is a nonzero
binary quadratic on this line.  The residual considered here is the complementary
case where all those quadratics vanish identically, so the direction ratios are
consistent on the whole residual line.

A degree-`127` split locator has the three fixed base roots and at most one
additional base root from `R`.  If `e_G` external roots are forced on the whole
residual line, every finite class still needs at least

```text
123 - e_G
```

non-forced external roots.  The line-incidence bound therefore gives
projective-budget safety for

```text
e_G <= 70.
```

For the high-core range, let `G=S E` and write

```text
G = q_0 P_X + H,        deg H < 128,
H = A T^127 + lower terms.
```

If an external point `s` is forced on the whole residual line, then the
evaluation functionals for `1` and `T` vanish:

```text
H(s)=0,        sH(s)-A P_X(s)=0.
```

Since `s` is external, `P_X(s) != 0`, hence `A=0` and `deg H<=126`.  Therefore
no modular reduction occurs:

```text
L_{E R}=H R        for all deg R<2.
```

The factor `H` has the three fixed base roots and the forced external core;
`R` contributes at most one further subgroup root.  Thus a degree-`127` split
locator would require `e_G>=123`, so the product-collapse argument excludes

```text
71 <= e_G <= 122.
```

Finally, after puncturing a forced external core `E`, the residual tangent
radius is `r'=127-|E|` and the projective tangent staircase gives at most
`r'+1=128-|E|` projective bad slopes.  This is at most the budget `6` for

```text
e_G >= 122.
```

Thus the fixed three-core residual line is projective-budget safe for every
external forced-core size.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_three_core_residual_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-residual-closure/f17_32_n512_k256_m3_rank6_a385_three_core_residual_closure.json
```

Nonclaims:

```text
no proof that every A=385 over-budget branch has a fixed three-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment outside the projective tangent/tail accounting used here;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
