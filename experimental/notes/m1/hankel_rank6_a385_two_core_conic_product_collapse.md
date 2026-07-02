# Hankel Rank-6 A385 Two-Core Conic Product Collapse

Status: PROVED / AUDIT.

This note records a product-collapse refinement for the irreducible-conic part
of the high-core branch in

```text
experimental/notes/m1/hankel_rank6_a385_two_core_high_core_quotient.md
```

The setting is the separated `A=385` rank-6 fixed two-core moving-slope branch.
After factoring the fixed two-point base core, write

```text
Q = E R,        deg R < 3.
```

Let `S` be the degree-`<m` interpolant with `S(x)=Omega_x/a_x` on the base
support `X`, with `m=128`, and put

```text
G = S E.
```

For each residual `R`, let `L_{E R}` be the remainder of `G R` modulo

```text
P_X = prod_{x in X}(T-x).
```

In the irreducible-conic high-core branch, the high-core quotient normal form
shows that every forced external root is global: its evaluation functional
vanishes on the whole residual `Q`-plane.

Write

```text
G = q_0 P_X + H,        deg H < m.
```

If an external point `s` lies in the global forced core, then the functionals
for `1`, `T`, and `T^2` vanish at `s`.  Comparing

```text
ev_s(T) - s ev_s(1),        ev_s(T^2) - s ev_s(T)
```

forces the `T^(m-1)` and `T^(m-2)` coefficients of `H` to vanish, because
`P_X(s) != 0`.  Hence

```text
deg H <= m-3 = 125.
```

Since `deg R<3`, no reduction modulo `P_X` occurs:

```text
L_{E R} = H R.
```

On the base support, `H(x)R(x)=a_x^{-1}Omega_x E(x)R(x)`, so `H` has exactly
the two fixed base-core roots on `X` and no other base roots.  On the external
subgroup points, the roots of `H` are exactly the global forced external core.
A nonzero residual `R` contributes at most two additional subgroup roots.

Thus, if the global forced external core has size `e_G<=122`, every product
`H R` has at most

```text
e_G + 2 + 2 <= 126
```

subgroup roots, fewer than the `127` roots required by the degree-`127`
split-locator gate.  Conversely, since `H` is nonzero of degree at most `125`
and already has the two fixed base roots, `e_G>=124` is impossible.  The only
irreducible-conic high-core quotient tail left by this packet is therefore

```text
e_G = 123.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_conic_product_collapse.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-conic-product-collapse/f17_32_n512_k256_m3_rank6_a385_two_core_conic_product_collapse.json
```

Nonclaims:

```text
no closure of the e_G=123 irreducible-conic quotient tail;
no product-collapse theorem for A=385 high-core line components;
no closure of the full fixed two-core nonconstant moving-slope branch;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem;
no row-level M3 safe-side bound.
```
