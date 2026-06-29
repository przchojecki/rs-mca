# M1 Boundary-Off External-Anchor Audit

Date: 2026-06-29

Source PR: #131, AllenGrahamHart.

Updated by PR #138, AllenGrahamHart / Codex.

Status: PROVED-LOCAL / RULED-BRANCH CLASSIFIED / BOUNDARY-CORE SLOPE-FIBER /
BOUNDARY QUARTIC KUMMER GATE / PROOF-PROGRAM / AUDIT.

## Claim Distilled

The PR isolates the one-outside `Boundary_off` residual in the M1 Hankel-pencil
program.  For a domain shadow `S subset D` of size `j-1` and an external anchor
`beta notin D`, the one-outside locator has the affine form

```text
ell_{S,beta} = ell_S^+ - beta ell_S^0.
```

Consequently the Hankel landing matrix

```text
M_S(beta) =
[ H(u) ell_{S,beta}   H(v) ell_{S,beta} ]
```

has columns affine-linear in `beta`, and the rank-one landing condition is
equivalent to quadratic minor equations in `beta`.

For fixed `S`, either one of these quadratic minors is nonzero, giving at most
two external anchors, or all minors vanish identically and the branch is a ruled
rank-one pencil.  In the `t=2` case this gives a three-scalar coefficient test
for the ruled branch.

The ruled `t=2` Hankel branch is now classified by
`m1_same_slope_root_slice_lemma.md`.  Writing

```text
c_i(w)=row_i(H_{3,j-1}(w)ell_S),        i=0,1,2,
```

one has

```text
H_{2,j}(w)ell_{S,beta}
 =
 (c_1(w)-beta c_0(w), c_2(w)-beta c_1(w)).
```

If the affine landing pencil is ruled, the Hankel shift collapse forces it to
be inactive or fixed finite slope:

```text
H_{2,j}(v)ell_{S,beta}=0        for every beta,
```

or

```text
(H_{2,j}(u)+z_0H_{2,j}(v))ell_{S,beta}=0
        for every beta.
```

The fixed finite-slope case is a boundary root slice and lifts to

```text
H_{3,j-1}(u+z_0v)ell_S=0.
```

Thus, after fixed-slope boundary root slices are charged, each shadow `S`
supports at most two active non-ruled external anchors.  The ruled
external-anchor branch no longer has to be mixed into quotient-periodic mass.

The same root-slice subtraction gives the shadow-image form now recorded in
`m1_same_slope_root_slice_lemma.md`.  If two external anchors over the same
shadow have the same finite slope `z`, then the lifted boundary core

```text
H_{3,j-1}(u+zv)ell_S=0
```

has already been charged.  Therefore, in the residual family, the projection

```text
S union {beta} |-> S
```

has fibers of size at most two and the finite-slope labels inside each fiber
are distinct.  Equivalently,

```text
|Boundary_off^res| <= 2 |Shadow_off^res|.
```

The remaining global task is to bound the shadow image, not to handle
uncontrolled external-anchor multiplicity over a fixed shadow.

There is also no hidden quantifier over external anchors in that shadow task.
For a fixed finite slope `z`, write

```text
c_i=row_i(H_{3,j-1}(u+zv)ell_S),        0<=i<=2.
```

Then `H_{2,j}(u+zv)ell_{S,beta}=0` for some `beta` iff either the lifted
boundary core is already zero,

```text
(c_0,c_1,c_2)=(0,0,0),
```

or

```text
c_0 != 0,        c_1^2=c_0c_2,        beta=c_1/c_0.
```

Thus the residual shadow-image problem is a scalar rank-one Hankel condition
on `S`, with the recovered anchor required to lie outside `D` and satisfy the
usual active filter.

As the finite slope varies, write

```text
a_i=row_i(H_{3,j-1}(u)ell_S),        b_i=row_i(H_{3,j-1}(v)ell_S),
c_i(z)=a_i+z b_i.
```

The recovered-anchor gate is the quadratic

```text
Q_S(z)=c_1(z)^2-c_0(z)c_2(z).
```

If `Q_S` is nonzero, the fixed shadow contributes at most two candidate
slopes/anchors.  If `Q_S=0` as a polynomial, then the line `a+z b` lies on one
rank-one cone generator.  Any finite recovered anchor is therefore independent
of `z`, and both `H_{2,j}(u)ell_{S,beta}` and
`H_{2,j}(v)ell_{S,beta}` vanish, so the active filter removes that branch.
Thus the remaining boundary-shadow problem is a nonzero quadratic-root
problem over the shadows.

The same target can be written directly in the external-anchor coordinate.
With `r_beta=(1,beta,beta^2)` and
`h_beta(c)=(c_1-beta c_0,c_2-beta c_1)`, define

```text
A_S(beta)=det(a,b,r_beta).
```

Then `A_S(beta)=det(h_beta(a),h_beta(b))`.  Therefore, whenever
`h_beta(b) != 0`, the equation `A_S(beta)=0` is equivalent to the existence of
a unique finite slope `z` with `h_beta(a+z b)=0`; if `a+z b` is nonzero, this
is exactly the recovered-anchor condition above.  If `A_S` is identically
zero, then `a` and `b` are proportional, and the branch is either inactive or
already charged to the lifted zero core.  The remaining one-outside shadow
target is therefore a nondegenerate conic-secant incidence: `A_S` is a nonzero
quadratic with an outside-domain root passing the active filter.

There is a second fiber reduction after the external anchor is fixed.  Let
`R subset D` have size `j-2`, let `beta notin D`, and put
`P_{R,beta}=(X-beta)ell_R`.  For a domain extension
`ell_{R,beta,y}=(X-y)P_{R,beta}`, the determinant

```text
det(H_{2,j}(u)ell_{R,beta,y}, H_{2,j}(v)ell_{R,beta,y})
```

is quadratic in `y`.  If it is nonzero, at most two domain anchors lie over
the fixed boundary core `(R,beta)`.  If it is identically zero, the Hankel
ruled-core collapse is inactive or fixed finite slope; the fixed-slope case
lifts to `H_{3,j-1}(u+zv)P_{R,beta}=0` and is charged as a one-outside
boundary-core root slice.  Hence, after those lifted boundary-core slices are
charged, projection `(R union {y}, beta) -> (R,beta)` has residual fibers of
size at most two.  The next unbounded object is the boundary-core image, not a
domain-anchor multiplicity over a fixed external anchor.

Combining the shadow-fiber and fixed-anchor fiber reductions gives a fixed-core
graph form.  For fixed `R`, residual one-outside targets define a bipartite
graph between external anchors `beta` and domain roots `y in D\R`; both sides
have degree at most two after the corresponding root-slice charges.  Hence each
fixed core supports at most `2(n-j+2)` residual external anchors, and globally

```text
|Core_off^res| <= 2(n-j+2)|Root_off^res|,
```

where `Root_off^res` is the image of active `(j-2)` domain cores.  This isolates
the next object as a domain-core image.

For fixed `R`, this graph is cut out by an explicit bidegree `(2,2)`
determinant.  With

```text
U_m=H_{2,j}(u)(X^m ell_R),        V_m=H_{2,j}(v)(X^m ell_R),
```

put

```text
Delta_R(beta,y)
 = det(U_2-(beta+y)U_1+beta y U_0,
       V_2-(beta+y)V_1+beta y V_0).
```

Then `Delta_R(beta,y)=0` is exactly the rank-one boundary landing condition for
`(X-beta)(X-y)ell_R`; the active filter is the nonvanishing of the second
vector.  The fixed-shadow and fixed-anchor quadratics are the two coordinate
specializations of this same determinant.  Thus the remaining boundary-core
image is a concrete bidegree-two incidence target.

Equivalently, if

```text
F_R(s,p)=det(U_2-sU_1+pU_0, V_2-sV_1+pV_0),
```

then

```text
Delta_R(beta,y)=F_R(beta+y,beta y).
```

So the boundary-core target is the mixed-domain slice of the ordinary two-root
elementary determinant curve.  Fixing either coordinate is the fixed-root line
`p=alpha s-alpha^2` in the `(s,p)` plane; after those root-slice charges, any
positive-dimensional same-slope component is one of the already classified
fixed-sum or nondegenerate product-Mobius line packets.

There is no additional same-slope multiplicity hidden on the complementary
conic.  For a fixed finite slope `z`, the two coordinates of

```text
(U_2+zV_2)-s(U_1+zV_1)+p(U_0+zV_0)
```

are affine-linear in `(s,p)`, so the same-slope fiber in the elementary plane
is empty, one point, an affine line, or the whole plane.  A two-point fiber
therefore lies on a constant-slope affine line.  Fixed-root lines are already
boundary/root-slice charges; non-fixed lines are fixed-sum or product-Mobius
packets, and the constant-slope collapse charges them to the full-plane lift.
Thus, after those charges, the finite-slope label is injective on each live
fixed-core boundary conic.

On those surviving non-fixed packets the mixed-domain slice is a graph, not a
new incidence surface.  A fixed-sum packet `x+y=s_0` contributes only

```text
beta=s_0-y,
```

and a nondegenerate product-Mobius packet `(x-c)(y-c)=mu`, `mu != 0`,
contributes only

```text
beta=c+mu/(y-c).
```

Thus, for a fixed core `R`, every non-fixed line packet contributes at most
`|D\R|=n-j+2` one-outside boundary-core pairs, namely the domain roots whose
packet partner escapes the domain.  The degenerate `mu=0` case is exactly the
fixed-root line already charged by the boundary/root-slice ledger.

The remaining conic case can be written as a one-variable discriminant target.
Write

```text
F_R(s,p)=f_20 s^2+f_11 sp+f_02 p^2+f_10 s+f_01 p+f_00.
```

For fixed `y in D\R`,

```text
F_R(beta+y,beta y)=A_R(y) beta^2+B_R(y) beta+C_R(y),
```

with

```text
A_R(y)=f_20+f_11 y+f_02 y^2,
B_R(y)=f_10+(2f_20+f_01)y+f_11 y^2,
C_R(y)=f_00+f_10 y+f_20 y^2.
```

In odd characteristic, nondegenerate fibers are counted by the quartic
discriminant `Disc_R(y)=B_R(y)^2-4A_R(y)C_R(y)`.  The fully zero quadratic is
exactly the fixed-root line component `p=y s-y^2`, already charged; the
outside-domain and active filters can only shrink the resulting root count.
Thus the residual non-line boundary-core problem is a quartic
Kummer/discriminant trace over the domain roots.

The case where `Disc_R(y)` is identically zero is also already classified.  In
odd characteristic, coefficient comparison gives either

```text
F_R(s,p)=lambda L(s,p)^2
```

for an affine line `L`, or

```text
F_R(s,p)=lambda(s^2-4p).
```

The first case is exactly a fixed-sum, fixed-root, or product-Mobius
line-packet branch.  The second restricts to
`lambda(beta-y)^2` on the mixed boundary slice, so it contributes only
`beta=y`, which is removed by the outside-domain/distinct-root filters.  Thus,
after line-packet and fixed-root charges, the remaining conic target has a
nonzero quartic discriminant.

The live nonzero-discriminant target is a bounded double-cover problem.  If
`A_R` is identically zero, then `F_R` is affine-linear and has already returned
to the line-packet branch.  Otherwise `A_R` has at most two roots.  Away from
those roots, anchor roots are in bijection with

```text
W_R^2=Disc_R(y),
```

through `W_R=2A_R(y)beta+B_R(y)` and
`beta=(-B_R(y)+W_R)/(2A_R(y))`.  Since `deg Disc_R<=4`, the squarefree
normalization has genus at most one.  The roots of `A_R` contribute only at
most two linear exceptional fibers before the outside-domain and active
filters.  Thus the remaining analytic target is a uniform genus-zero/genus-one
Kummer trace.

For the full multiplicative-subgroup upper bound this trace has an exact
character expansion.  If `D <= F_p^*` has index `e` and `chi` has kernel `D`,
then away from the charged fixed-root fibers and the at most two `A_R=0`
exceptions,

```text
N_R(D)=|D|+(1/e) sum_a sum_{y in F_p^*} chi^a(y) chi_2(Disc_R(y)) + O(1).
```

Writing `ell=lcm(e,2)` and combining `chi` with `chi_2`, the `a`-term is
geometrically trivial only when

```text
div(y^{a ell/e} Disc_R(y)^{ell/2}) == 0 mod ell.
```

Equivalently, every nonzero root of `Disc_R` has even multiplicity and the
zero-root parity matches `a`.  Otherwise the standard one-dimensional
Kummer-Weil input has support contained in the four discriminant roots plus
`0` and `infinity`, giving a depth-independent `4 sqrt(p)` term.  Thus the
boundary quartic cannot hide a growing conductor; any no-cancellation case is
the explicit monomial-square discriminant gate above.

## Integration Decision

The full PR was not merged wholesale.  It included a very large generated
draft, stale site/Paper D changes, and proof-program material that should not
be promoted as a solved M1 theorem.  The useful content is this local normal
form and the suggested exact primitive quotient-normal target.

The exact target proposed in the PR is:

```text
|Bad_nc(f,g,a)| <= M1QuotBudget(f,g,a) + n^B
```

after tangent, contained, quotient-periodic, presentation, reciprocal, and
finite-domain alias contributions have been charged.  This remains
CONJECTURAL / FALSIFICATION-FIRST.

## Use

This note is useful for the M1 residue-line local-limit program because it
turns the opaque one-outside boundary image into an explicit external-anchor
incidence problem.  It gives a route for future agents:

1. Prove polynomial bounds for the residual boundary shadow image.
2. Charge fixed-slope boundary root slices to the lifted Hankel ledger.
3. Keep the primitive quotient-normal target separate from exact quotient
   support budgets.

## Non-Claims

This note does not prove the all-line M1 polynomial packing theorem.  It gives
per-shadow quadratic slope/anchor gates, the shadow-fiber reduction, and the
fixed-anchor boundary-core fiber reduction after fixed-slope boundary slices
are charged, plus the fixed-core degree-two graph form and the non-fixed
line-packet mixed-trace formulas, and the quadratic/discriminant anchor gate.
It does not bound the total active domain-core image or prove the needed
nonzero quartic character-sum cancellation, does not give a leaderboard row,
and does not change any public MCA or interleaved-list threshold.
