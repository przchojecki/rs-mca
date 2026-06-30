# M1 equal-line resultant popularity gate

**Status:** PROVED-LOCAL / CONDITIONAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note instantiates the projective divisor-gate handoff from
`m1_popularity_divisor_gate.md` with an actual M1 resultant already isolated in
`m1_depth_two_equal_line_diagonal_reduction.md`.

It does not prove that the global M1 high-overlap leaves are always governed by
this resultant.  It proves the local gate: once an endpoint-disjoint
high-overlap star is reduced to the equal-line diagonal kernel resultant, each
fixed center residue sees at most a quadratic projective leaf-parameter gate,
up to explicitly charged exceptional fibers.

## Resultant

The equal-line diagonal reduction records the kernel resultant

```text
R(x,y) =
  16x^2y^2 - 8xy^2 + 4xy + y^2 - 2y + 1.
```

Homogenize on `P^1_x x P^1_y`:

```text
R_h(X,Z;Y,W)
 =
 16X^2Y^2 - 8XZY^2 + 4XZYW
 + Z^2Y^2 - 2Z^2YW + Z^2W^2.
```

For fixed `x=[X:Z]`, this is the binary form in `y=[Y:W]`

```text
R_x(Y,W)
 =
 (4X-Z)^2 Y^2 + 2Z(2X-Z)YW + Z^2W^2.              (RY)
```

For fixed `y=[Y:W]`, it is the binary form in `x=[X:Z]`

```text
R^y(X,Z)
 =
 16Y^2X^2 + 4Y(W-2Y)XZ + (Y-W)^2Z^2.              (RX)
```

## Fiber nonvanishing

For every projective center point `x=[X:Z]`, the form `R_x` is nonzero.
Indeed, if `Z != 0`, the `W^2` coefficient is `Z^2 != 0`; if `Z=0`, the
`Y^2` coefficient is `16X^2 != 0`.

Similarly, for every projective leaf value `y=[Y:W]`, the form `R^y` is
nonzero.  If `Y != 0`, the `X^2` coefficient is `16Y^2 != 0`; if `Y=0`, the
`Z^2` coefficient is `W^2 != 0`.

Therefore every fixed fiber of the resultant cuts out at most two projective
points on the opposite `P^1`.

## Popularity cap

Suppose an endpoint-disjoint high-overlap star in the equal-line diagonal
branch has a projective leaf parameter

```text
theta : leaves -> P^1_y(F)
```

with fiber multiplicity at most `mu`.  Fix a center residue `x`.  Assume the
leaves containing `x` are contained in

```text
Z_exc union { y in P^1 : R_x(y)=0 },
```

where `|Z_exc| <= E`.  Then the projective divisor gate gives

```text
pop_x <= mu(E+2).                                  (EQG)
```

Consequently the popularity-cap support criterion of
`m1_high_overlap_graph_budget.md` applies with

```text
U = mu(E+2).
```

Thus, in the equal-line diagonal branch, a leaf-containment reduction to
`R_h=0` outside the charged exceptional fibers is enough to close the
far-from-star small-support residual whenever

```text
F_pop(K,s,h,D,Lambda,mu(E+2)) > R_budget.
```

The finite ordinary split-fiber containment case is discharged in
`m1_equal_line_split_fiber_containment.md`.  The remaining nonlocal task is to
show that the relevant global endpoint-independent high-overlap leaves enter
that split-fiber chart, and that all denominator, branch, quotient, tangent,
projective-boundary, and fixed-root exceptions are charged into `Z_exc` or
earlier ledgers.

## Verification

The companion verifier checks the bidegree `(2,2)` homogenization, nonzero
projective fibers, root-count caps in both directions, and composition with the
popularity support floor:

```sh
python3 experimental/scripts/verify_m1_equal_line_resultant_popularity_gate.py
```
