# Hankel Rank-6 A385 Two-Core High-Core Quotient Normal Form

Status: PROVED / AUDIT.

This note records the quotient normal form for the high-core part of the
fixed two-core moving-slope residual at

```text
A = 385.
```

It consumes

```text
experimental/notes/m1/hankel_rank6_a385_two_core_moving_slope_incidence.md
```

and does not close the quotient branches.

After a fixed forced two-point base core is factored, write

```text
Q = E R,       deg R < 3.
```

The residual vector space `W` has dimension three.  For each external subgroup
point `s`, define

```text
ev_s(R) = L_{E R}(s).
```

This is a linear functional on `W`.  The corresponding root hyperplane is
`P(ker ev_s)` if `ev_s` is nonzero, and the whole residual plane if `ev_s=0`.

For a component `G`, let `e_G` be the number of external points whose root
hyperplanes contain `G`.  A positive-dimensional component cannot have
`e_G >= 127`: then every `L_{E R}` on the component would be divisible by the
same degree-`127` external locator and hence scalar-multiple to it, contradicting
injectivity of `R |-> L_{E R}` on a positive-dimensional component.

For a line component `P(U)`, a forced external root is exactly

```text
ev_s|_U = 0.
```

Thus the forced external core

```text
C_E(T) = prod_{s in forced core} (T-s)
```

divides every `L_{E R}` with `R in U`.  The split-locator gate on the line is
therefore a quotient-locator pencil after dividing by `C_E`.

For an irreducible conic component, if `G` is contained in a root hyperplane,
then that hyperplane cannot be a proper projective line.  Hence `ev_s=0` on
the whole residual plane.  Thus the forced external core of an irreducible
conic is a global common divisor for all residual-plane kernel polynomials.

Since `C_E` is a squarefree divisor of `X^512-1`, a candidate

```text
L_{E R} = C_E F_R
```

passes the degree-`127` split-locator divisor gate only if, after normalization
and the exact-degree check,

```text
F_R | (X^512-1)/C_E,
deg F_R = 127 - e_G.
```

The incidence packet leaves the line high-core range

```text
e_G >= 71.
```

So the high-core line branch is a quotient pencil of degree at most

```text
127 - 71 = 56.
```

It leaves the irreducible-conic high-core range

```text
e_G >= 68.
```

So the high-core conic branch is a quotient family of degree at most

```text
127 - 68 = 59.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_high_core_quotient.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-high-core-quotient/f17_32_n512_k256_m3_rank6_a385_two_core_high_core_quotient.json
```

Nonclaims:

```text
no A385 high-core product-collapse theorem;
no claim that the high-core quotient pencils or families are empty or paid;
no closure of the full fixed two-core nonconstant moving-slope branch;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem;
no row-level M3 safe-side bound.
```
