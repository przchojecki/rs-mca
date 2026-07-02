# Hankel Rank-6 A385 Two-Core High-Core Closure

Status: PROVED / AUDIT.

This note closes the separated `A=385` rank-6 fixed two-core high-core
line/conic residual left by

```text
experimental/notes/m1/hankel_rank6_a385_two_core_moving_slope_incidence.md
experimental/notes/m1/hankel_rank6_a385_two_core_high_core_quotient.md
experimental/notes/m1/hankel_rank6_a385_two_core_conic_product_collapse.md
```

The setting is still local: fixed two-core, separated support, positive
dimensional line/conic moving-slope components in the residual `Q`-plane.

The conic side is already reduced by the product-collapse packet.  It closes
the irreducible-conic high-core range

```text
68 <= e_G <= 122.
```

For a line component, let `U` be the two-dimensional residual subspace and let
`U^perp=<phi>` in the dual `Q`-plane.  A forced external root `s` means
`ev_s|_U=0`.  With

```text
G = q_0 P_X + H,        deg H < 128,
H = A T^127 + B T^126 + ...,
P_X = T^128 + p T^127 + ...,
C = B - A p,
```

the external evaluation functional has coefficients

```text
H(s),        s H(s)-A P_X(s),        s^2 H(s)-(A s+C)P_X(s).
```

Two distinct forced roots give the same line-product dichotomy as in the
`A=386` closure, with the degrees shifted by one and the fixed two-core base
factor retained.

In the common-root-pencil case, `U` is the pencil `R(alpha)=0`; writing
`R=(T-alpha)S`,

```text
L_{E R} = F S,        F=(T-alpha)H-A P_X,        deg F <= 126.
```

The factor `F` has the two fixed base-core roots and at most one additional
base root `x=alpha`; the residual factor `S` has at most one further subgroup
root.  Therefore a degree-`127` split locator needs `e_G>=123`.

In every remaining two-forced-root line case, modular reduction vanishes on
the line:

```text
L_{E R}=H R        for R in U.
```

Here `H` carries the two fixed base roots and the forced external core, while
`R` contributes at most two further subgroup roots.  Again, a degree-`127`
split locator needs `e_G>=123`.  Hence the line product collapse closes

```text
71 <= e_G <= 122.
```

The high-core tail is projective-safe by puncturing the forced external core.
After removing `E`, the residual row has

```text
n' = 512-|E|,        a' = 385,        r' = 127-|E|.
```

The high-agreement projective tangent staircase applies throughout the
high-core ranges and gives at most

```text
r' + 1 = 128-|E|
```

projective bad slopes.  For `|E|>=122`, this is at most `6`, exactly the
projective budget for the pinned row.  Thus the line and conic high-core tails
are projective-safe for

```text
e_G >= 122.
```

Combining incidence, product collapse, and the punctured tangent tail:

```text
line components:
  e_G <= 70       incidence safe
  71 <= e_G <=122 product-collapse impossible
  e_G >= 122      punctured-tangent projective safe

irreducible conic components:
  e_G <= 67       incidence/pair-overlap safe
  68 <= e_G <=122 product-collapse impossible
  e_G >= 122      punctured-tangent projective safe
```

Thus all separated fixed two-core line/conic moving-slope components are
projective-budget safe.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_high_core_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-high-core-closure/f17_32_n512_k256_m3_rank6_a385_two_core_high_core_closure.json
```

Nonclaims:

```text
no row-level M3 safe-side bound;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment outside the projective tangent/tail accounting used here;
no quotient or extension overlap audit for arbitrary root tables.
```
