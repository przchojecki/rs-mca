# XR pencil cascade

DAG node: `xr_pencil_cascade`.

Status: PROVED.

## Critical-path role

This is a proof-spine packet for the conditional prize route.  The clean-rate
compiler now reduces the post-strip face-4 obligation to a polynomial residual
bound, recorded as `R_post(u,v; A) <= 16 n^3` in
`xr_clean_poly_forcing_reduction.md`.  This packet removes the largest-core
boundary of that residual: any distinct-slope pair with common core
`>= A-1` is not an unstructured residue at all, but a paid tangent-pencil
cell.

Thus later packets only need to count the small-core spread remainder, plus
the terminal active-core/PTE residue currently isolated as
`active_core_count_bound`.  This theorem is unconditional; the conditional
part of the prize path enters only when the downstream compiler consumes the
remaining polynomial residue bound.

## Statement

Let `C = RS[H,k]`, `|H| = n`, and let the agreement threshold be

```text
A = k + t.
```

For a fixed received pair `(u,v)` and finite slope `z`, write
`w_z = u + z v`.  Suppose two distinct slopes `z_1 != z_2` have explaining
codewords `c_1,c_2 in C` and full agreement sets `S_1,S_2`, and put

```text
R = S_1 cap S_2,       r = |R|.
```

If

```text
r >= A - 1 = k + t - 1,
```

then the pair is in the tangent-pencil stratum:

1. The two slopes force a unique codeword pair `(U,V)` on `R`.
2. If `r >= A`, every finite slope is already `A`-bad on `R`.
3. If `r = A-1`, all finite slopes generated through the core are exactly the
   residual ratios

```text
z_x = -e_u(x) / e_v(x),       e_u = u-U, e_v = v-V,
```

for off-core points `x notin R` with `e_v(x) != 0`, with collisions allowed.
Thus one core produces at most `n-r` distinct finite slopes unless a universal
zero enlarges the core.

Consequently, after removing paid tangent-pencil cells, no residual
distinct-slope pair can have common core `>= A-1`; the face-4 remainder is the
small-core spread problem.

## Proof

On `R` the two alignments give

```text
u + z_1 v = c_1,
u + z_2 v = c_2.
```

Because `z_1 != z_2`, define

```text
V = (c_1 - c_2)/(z_1 - z_2),
U = (z_1 c_2 - z_2 c_1)/(z_1 - z_2).
```

Both `U` and `V` are codewords, since `C` is linear.  Substituting the two
displayed equations shows that `u=U` and `v=V` on `R`.  This is the forced
codeword line.

Set

```text
e_u = u - U,       e_v = v - V.
```

Then `e_u=e_v=0` on `R`, and for every finite slope `z`,

```text
w_z - (U + zV) = e_u + z e_v.
```

If `r >= A`, the right-hand side vanishes on at least `A` points for every
finite `z`, so every slope is explained by the codeword `U+zV` on the common
core.  This is already a paid tangent-pencil cell.

If `r = A-1`, one further zero is necessary and sufficient for agreement
`>=A` through the forced core.  For an off-core point `x`, the equation

```text
e_u(x) + z e_v(x) = 0
```

has:

- no finite solution if `e_v(x)=0` and `e_u(x) != 0`;
- every finite solution if `e_u(x)=e_v(x)=0`, in which case `x` belongs to the
  common zero core and the previous `r >= A` case applies after enlarging `R`;
- the unique finite solution `z_x = -e_u(x)/e_v(x)` if `e_v(x) != 0`.

Therefore the entire threshold cascade is the image of the off-core residual
ratio map `x -> z_x`.  Multiple off-core points may have the same ratio; then
one slope gains several extra agreement points.  In all cases the cascade is a
single tangent-pencil object of depth

```text
r-k >= t-1.
```

This proves the claimed threshold and explains the E27 multiplicity-2 hole at
cores `>= A-1`: those pairs are not part of the residual spread count; they are
paid by the pencil.

## Verifier

`experimental/scripts/verify_xr_pencil_cascade.py` checks deterministic toy
instances over `F_17` with `n=9`, `k=3`, `A=5`:

- the threshold case `r=A-1`, where each off-core residual ratio gives exactly
  the predicted agreement support;
- a collision case, where two off-core points generate the same slope;
- the `r=A` case, where all finite slopes are bad on the common core;
- a blocked off-core point with `e_v=0` and `e_u!=0`, which contributes no
  slope;
- recovery of `(U,V)` from two distinct slopes by the displayed formulas.

The recomputed summary is pinned in
`experimental/data/certificates/xr-pencil-cascade/toy_pencil_cascade.json`.
