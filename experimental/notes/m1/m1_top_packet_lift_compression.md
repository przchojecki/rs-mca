# M1 top-packet lift and compression

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note extracts a compact top-packet package from the broad same-slope
packet in PR #138.  It is meant to be read after the local one-exchange
reductions: once star triangles have been charged to one-exchange cores, every
residual one-exchange triangle is a top-packet triangle, and such packets lift
to a simultaneous `t=1` Hankel kernel.

## Scope and non-claims

This is local algebra in the `t=2` Hankel-pencil normal form.  It does not
prove the all-line M1 aperiodic local limit, does not bound the global
residual slope image, and does not add a leaderboard or threshold row.

Field ledger: the statement is over an arbitrary field `F`.  In an MCA
application the slopes are finite line slopes in `q_line`.  No generated-field,
challenge-field, denominator, or radius endpoint convention enters this local
step.  Domain-root, split-root, quotient-periodic, contained/tangent, and
noncontainment filters remain external filters.

## Triangle classification

Let `T_1,T_2,T_3` be distinct `j`-sets with

```text
|T_i cap T_h| = j-1        for every i != h.
```

Then exactly one of the following holds.

1. **Star triangle.** The three sets share a common `(j-1)` core:

   ```text
   T_i = R union {y_i},        |R|=j-1.
   ```

2. **Top-packet triangle.** The three sets lie in a common `(j+1)` set:

   ```text
   T_i = U \ {x_i},        |U|=j+1.
   ```

Proof: put `A=T_1 cap T_2`, so `|A|=j-1`, and write

```text
T_1=A union {x},        T_2=A union {y},        x != y.
```

Let `eps_x,eps_y` indicate whether `x,y` lie in `T_3`, and put
`m=|T_3 cap A|`.  Since `T_3` is adjacent to both `T_1` and `T_2`,

```text
m+eps_x=j-1,        m+eps_y=j-1.
```

Thus `eps_x=eps_y`.  If both are zero, then `A subset T_3`, giving the star
case.  If both are one, then `T_3` is obtained from `A` by deleting one element
and adjoining both `x` and `y`; all three sets are obtained from
`U=A union {x,y}` by deleting one element, giving the top-packet case.

In the `t=2` determinant graph, star triangles are three-anchor events through
one `(j-1)` core.  After ruled one-exchange cores and fixed-slope root slices
have been charged, residual one-exchange triangles are therefore top-packet
triangles.

## Top-packet lift

Let `U` be a `(j+1)` set and, for `x in U`, put

```text
T_x = U \ {x},        ell_U = (X-x) ell_{T_x}.
```

For any syndrome vector `w`, the Hankel rows obey

```text
H_{1,j+1}(w) ell_U
 =
 row_1(H_{2,j}(w) ell_{T_x})
 - x row_0(H_{2,j}(w) ell_{T_x}).                 (TOP1)
```

Consequently, if `T_x` contributes finite slope `z`, so that

```text
(H_{2,j}(u)+zH_{2,j}(v)) ell_{T_x} = 0,
```

then

```text
(H_{1,j+1}(u)+zH_{1,j+1}(v)) ell_U = 0.           (TOP2)
```

If two top-packet members `T_x` and `T_y` contribute distinct slopes
`z_x != z_y`, then

```text
H_{1,j+1}(u)ell_U = 0,
H_{1,j+1}(v)ell_U = 0.                            (TOPK)
```

Proof: writing `ell_{T_x}=p_0+p_1X+...+p_jX^j`, the coefficient of `X^b` in
`ell_U=(X-x)ell_{T_x}` is `p_{b-1}-x p_b`, with `p_{-1}=p_{j+1}=0`.  This gives
`(TOP1)` by expanding the Hankel sums.  Applying `(TOP1)` to `w=u+zv` gives
`(TOP2)`.  If two distinct slopes lift to the same top locator, then

```text
A+z_xB=0,        A+z_yB=0,
```

where `A=H_{1,j+1}(u)ell_U` and `B=H_{1,j+1}(v)ell_U`.  Subtracting gives
`B=0`, hence `A=0`.

After fixed-slope root-slice charging, any residual one-exchange edge has
distinct slopes, so every residual top-packet edge lies over a simultaneous
lifted `t=1` kernel.

## Compression ledger

Define the simultaneous lifted top-kernel family

```text
K_top(u,v)
 =
 { U subset D : |U|=j+1,
   H_{1,j+1}(u)ell_U=0 and H_{1,j+1}(v)ell_U=0 }.
```

Let `A_res` be a residual `t=2` active locator family after fixed-slope root
slices have been charged.  For `U` of size `j+1`, write

```text
A_U = { x in U : U\{x} in A_res }.
```

If `|A_U|>=2`, every pair of members in this packet is a residual one-exchange
edge with distinct slopes, so `U in K_top(u,v)` by `(TOPK)`.  Therefore
residual top-packet edges inject into

```text
{ (U,{x,y}) : U in K_top(u,v), x,y in U, x != y },
```

via `{U\{x},U\{y}} |-> (U,{x,y})`.  Hence

```text
E_top(A_res) <= binom(j+1,2) |K_top(u,v)|.        (TE)
```

Likewise, after star triangles have been charged to one-exchange cores,
residual one-exchange triangles inject into

```text
{ (U,{x,y,z}) : U in K_top(u,v), x,y,z in U distinct },
```

so

```text
Tri_1(A_res) <= binom(j+1,3) |K_top(u,v)|.        (TT)
```

Inside a lifted top packet the `t=2` slope equation is scalar.  For
`U in K_top(u,v)` and `x in U`, put

```text
rho_x(w)=row_0(H_{2,j}(w)ell_{U\{x}}).
```

Since `H_{1,j+1}(w)ell_U=0`, identity `(TOP1)` gives

```text
H_{2,j}(w)ell_{U\{x}} = rho_x(w)(1,x),        w in {u,v}.
```

Thus the active finite slope on `U\{x}` is determined by the scalar equation

```text
rho_x(u)+z rho_x(v)=0,        rho_x(v) != 0.
```

The top-packet branch is reduced to `K_top(u,v)` plus a one-dimensional slope
label.  It is not an independent two-row `t=2` residual phenomenon.

## Top-kernel root-slice recursion

For `r>=1` and locator size `d`, define

```text
K_{r,d}(u,v)
 =
 { U subset D : |U|=d,
   H_{r,d}(u)ell_U=0 and H_{r,d}(v)ell_U=0 }.
```

Thus `K_top(u,v)=K_{1,j+1}(u,v)`.  Fix a `(d-1)` core `R` and write

```text
U_y = R union {y},        ell_{U_y}=(X-y)ell_R.
```

If two distinct extensions through `R` lie in `K_{r,d}(u,v)`, then, for both
`w in {u,v}`, subtraction gives the padded equation

```text
H_{r,d}(w)(ell_R,0)=0,
```

and substitution gives

```text
H_{r,d}(w)(0,ell_R)=0.
```

These two padded row blocks are exactly the first `r` and last `r` rows of

```text
H_{r+1,d-1}(w)ell_R=0.
```

Therefore

```text
R in K_{r+1,d-1}(u,v).                            (KREC)
```

Every one-exchange collision inside the lifted top-kernel family is charged to
the next simultaneous Hankel kernel.  After such `K_{r+1,d-1}` root slices have
been charged, the residual part of `K_{r,d}(u,v)` has no one-exchange edges.
This is an exact residual-depth shift, not a multiplicative loss.

## Verification

The companion verifier checks the triangle classification, the Hankel row
identity `(TOP1)`, the distinct-slope implication `(TOPK)`, the compression
injections, the scalar slope label, and the top-kernel recursion over exact
small finite fields and Johnson graphs:

```sh
python3 experimental/scripts/verify_m1_top_packet_lift_compression.py
```
