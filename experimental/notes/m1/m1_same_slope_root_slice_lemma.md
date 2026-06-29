# M1 Same-Slope One-Exchange Root-Slice Lemma

**Status:** PROVED-LOCAL / ROOT-SLICE REDUCTION / RULED-CORE DICHOTOMY /
HIGHER-SLACK LIFT / TRIANGLE CLASSIFICATION / TOP-PACKET LIFT / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-29.

This note proves the first local reduction requested in
`m1_all_line_hankel_aperiodic_packet_audit.md`: same-slope one-exchange
collisions in the Hankel-pencil model are not a residual aperiodic codegree
phenomenon.  They force a whole fixed-slope root slice.

## Setup

Work in the Hankel-pencil normal form.  Let

```text
L_z = H_{t,j}(u)+zH_{t,j}(v)
```

be the finite-slope linear landing map on monic split locator polynomials of
degree `j`, with values in the `t` syndrome coordinates.  For a `(j-1)`-set
`R subset D` and `y in D\R`, write

```text
T_y=R union {y},        ell_{T_y}=(X-y)ell_R.
```

A finite-slope support `T_y` satisfies the slope equation when

```text
L_z ell_{T_y}=0.
```

The noncontainment condition `H_{t,j}(v)ell_{T_y} != 0` is a separate active
filter and is not used in the slice-forcing step.

## Lemma

Suppose `y_1 != y_2` and

```text
L_z ell_{T_{y_1}}=L_z ell_{T_{y_2}}=0.
```

Then

```text
L_z ell_R=0,        L_z(X ell_R)=0,
```

and consequently

```text
L_z ell_{T_y}=0        for every y in F.
```

In particular, every same-slope one-exchange edge is contained in the
fixed-slope root slice with core `R`.

## Proof

Since

```text
ell_{T_y}=X ell_R-y ell_R,
```

subtracting the two equations gives

```text
0=L_z(ell_{T_{y_1}}-ell_{T_{y_2}})
 =(y_2-y_1)L_z ell_R.
```

Thus `L_z ell_R=0`.  Substituting back into either endpoint equation gives

```text
0=L_z(X ell_R-y_1 ell_R)=L_z(X ell_R).
```

Therefore, for every scalar `y`,

```text
L_z ell_{T_y}=L_z(X ell_R-y ell_R)=0.
```

This proves the lemma.

## Residual Consequence

Let `A_res` be any active locator family after fixed-slope root slices have
been charged or removed.  Then the one-exchange graph on `A_res` has no
same-slope edges.  Equivalently, every residual one-exchange edge is a
different-slope edge:

```text
{T,T'} subset A_res, |T cap T'|=j-1
    => z_T != z_T'.
```

Thus the one-exchange codegree residual in the all-line Hankel program is
exactly the different-slope one-exchange ledger after root-slice charging.
This is useful because it prevents same-slope multiplicity from being counted
again as an aperiodic residual obstruction.

## Higher-Slack Root-Slice Lift

The fixed-slope root slice is also a genuine higher-slack Hankel core.  Put

```text
w_z=u+zv.
```

Let `ell_R` have degree `j-1`, and interpret

```text
L_z ell_R=0,        L_z(X ell_R)=0
```

as the two padded `H_{t,j}(w_z)` equations on the coefficient vectors

```text
(ell_R,0),        (0,ell_R).
```

Then these two equations are equivalent to

```text
H_{t+1,j-1}(w_z) ell_R=0.                         (LIFT)
```

Indeed, the first padded equation gives rows `0,...,t-1` of (LIFT), while the
second padded equation gives rows `1,...,t`.  Thus every same-slope
one-exchange root slice is charged to the lifted `(t+1,j-1)` Hankel core with
the same finite slope.  It is not a new residual `t`-level aperiodic
multiplicity.

## The `t=2` Determinant Gate

In the `t=2` Hankel window there is a second elementary one-exchange
separation.  For a fixed `(j-1)`-core `R`, put

```text
a_y=H(u)ell_{T_y},        b_y=H(v)ell_{T_y}        in F^2.
```

Since `ell_{T_y}=Xell_R-yell_R`, there are vectors
`a_X,a_0,b_X,b_0 in F^2` such that

```text
a_y=a_X-y a_0,        b_y=b_X-y b_0.
```

The finite-slope determinant gate is

```text
Delta_R(y)=det(a_y,b_y)=0,        b_y != 0.
```

The determinant is a polynomial of degree at most two:

```text
Delta_R(y)
 =
 det(a_X,b_X)
 - y(det(a_0,b_X)+det(a_X,b_0))
 + y^2 det(a_0,b_0).                              (DET2)
```

Consequently, if `Delta_R` is not the zero polynomial, at most two anchors
`y in F` can pass the determinant gate.  If three distinct anchors pass the
determinant gate, then `Delta_R` vanishes identically and the core `R` lies in
a ruled determinant branch:

```text
det(a_y,b_y)=0        for every y in F.
```

After fixed-slope root slices have been charged, this says that any fixed core
supporting three or more residual one-exchange anchors must be ruled but not
same-slope.  Non-ruled cores contribute at most one unordered one-exchange edge
through that core.

## Ruled-Core Dichotomy

The ruled determinant branch itself has a sharp local classification.  Let

```text
a(y)=a_X-y a_0,        b(y)=b_X-y b_0        in F^2
```

and suppose

```text
det(a(y),b(y)) == 0        as a polynomial in y.       (RULED)
```

Then one of the following holds.

1. **Fixed finite slope.** There is `z_0 in F` such that

   ```text
   a(y)+z_0 b(y)=0        for every y.
   ```

   Every active anchor on this core has the same finite slope `z_0`, so two
   such anchors force the fixed-slope root slice already proved above.

2. **Inactive direction.** `b(y)=0` for every `y`.  This gives no active finite
   slope anchors because the active filter requires `b(y) != 0`.

3. **Rank-one moving slope.** All four vectors
   `a_X,a_0,b_X,b_0` lie in one output line.  Thus for some nonzero
   `c in F^2`,

   ```text
   a(y)=alpha(y)c,        b(y)=beta(y)c
   ```

   with affine scalar functions `alpha,beta`.  If this branch is not fixed
   finite slope, then `alpha` and `beta` are not proportional, and the active
   slope map

   ```text
   y |-> z(y)=-alpha(y)/beta(y),        beta(y) != 0,
   ```

   is injective.

Consequently a ruled determinant core that survives the active filter and the
fixed-slope root-slice charge is necessarily a rank-one moving-slope core, and
it contributes at most one anchor to each finite slope.

### Proof

Let `V=F^2`.  If the affine pencil `a(y)` spans `V`, choose a basis in which
`a(y)=u-yv` with `u,v` independent.  Write

```text
b(y)=(alpha-y gamma)u+(beta-y delta)v.
```

The identity `det(a(y),b(y)) == 0` gives

```text
beta + y(alpha-delta) - y^2 gamma == 0,
```

hence `beta=gamma=0` and `delta=alpha`.  Therefore `b(y)=alpha a(y)` for all
`y`.  If `alpha != 0` this is the fixed finite slope `z_0=-alpha^(-1)`; if
`alpha=0` it is the inactive direction branch.

The same argument with `a` and `b` interchanged applies when `b(y)` spans `V`;
then either `a(y)=-z_0 b(y)` for a fixed finite slope `z_0`, or `a(y)=0`, which
is the fixed slope `z_0=0` on all active anchors.

It remains to consider the case where neither pencil spans `V`.  If their
images lay in two distinct output lines, the determinant would be a nonzero
constant multiple of the product of two nonzero affine scalar functions, which
cannot vanish identically.  Thus either one pencil is identically zero, already
covered above, or both images lie in the same output line.  This is the
rank-one case.

In the rank-one case write `a(y)=alpha(y)c` and `b(y)=beta(y)c`.  If
`alpha` and `beta` are proportional and `beta` is not identically zero, then
all active anchors have one fixed finite slope.  If they are not proportional
and two active anchors `y_1,y_2` have the same slope, then

```text
alpha(y_1) beta(y_2) = alpha(y_2) beta(y_1).
```

For affine `alpha,beta`, the left-minus-right expression is
`(y_2-y_1)(alpha_0 beta_X-alpha_X beta_0)`, whose second factor is nonzero
exactly because the two affine functions are not proportional.  Hence
`y_1=y_2`, proving injectivity.

## One-Exchange Triangle Classification

There is also no third combinatorial source of one-exchange triangles.  Let
`T_1,T_2,T_3` be distinct `j`-sets with

```text
|T_i cap T_h|=j-1        for every i != h.
```

Then exactly one of the following holds.

1. **Star triangle.** The three sets share a common `(j-1)`-core:

   ```text
   T_i=R union {y_i},        |R|=j-1.
   ```

2. **Top-packet triangle.** The three sets lie in a common `(j+1)`-set:

   ```text
   T_i=U \ {x_i},        |U|=j+1.
   ```

Consequently, in the `t=2` active determinant graph, every star triangle is a
three-anchor event through one `(j-1)` core.  By (DET2), such a core is ruled.
After ruled determinant cores have been charged or removed, every residual
one-exchange triangle is therefore a top-packet triangle.  After only
fixed-slope root-slice charging, a residual star triangle can occur only inside
the rank-one moving-slope ruled branch above, and its three anchors have three
distinct finite slopes.

### Proof

Put `A=T_1 cap T_2`, so `|A|=j-1`, and write

```text
T_1=A union {x},        T_2=A union {y},        x != y.
```

Let `eps_x` and `eps_y` indicate whether `x` and `y` lie in `T_3`, and put
`m=|T_3 cap A|`.  Since `T_3` is adjacent to both `T_1` and `T_2`,

```text
m+eps_x=j-1,        m+eps_y=j-1.
```

Thus `eps_x=eps_y`.

If `eps_x=eps_y=0`, then `m=j-1`, so `A subset T_3` and
`T_3=A union {z}` for some `z` distinct from `x,y`.  This is the star case.

If `eps_x=eps_y=1`, then `m=j-2`, so `T_3` is obtained from `A` by deleting
one element `a` and adjoining both `x` and `y`.  With

```text
U=A union {x,y},
```

one has

```text
T_1=U\{y},        T_2=U\{x},        T_3=U\{a}.
```

This is the top-packet case.  The two cases are mutually exclusive for
distinct sets, and no other value of `eps_x=eps_y` is possible.

## Top-Packet Lift to a Common `t=1` Kernel

The top-packet branch has its own exact lift.  Let `U` be a `(j+1)`-set and,
for `x in U`, put

```text
T_x=U\{x},        ell_U=(X-x)ell_{T_x}.
```

For any syndrome vector `w`, the Hankel rows obey

```text
H_{1,j+1}(w) ell_U
 =
 row_1(H_{2,j}(w) ell_{T_x})
 - x row_0(H_{2,j}(w) ell_{T_x}).                 (TOP1)
```

Consequently, if `T_x` contributes a finite slope `z`, so that

```text
(H_{2,j}(u)+zH_{2,j}(v))ell_{T_x}=0,
```

then the lifted top locator satisfies

```text
(H_{1,j+1}(u)+zH_{1,j+1}(v))ell_U=0.             (TOP2)
```

If two top-packet members `T_x` and `T_y` contribute distinct slopes
`z_x != z_y`, then

```text
H_{1,j+1}(u)ell_U=0,        H_{1,j+1}(v)ell_U=0.  (TOPK)
```

Thus every residual top-packet edge after fixed-slope charging lies over a
common lifted `t=1` Hankel kernel.  In particular, after star triangles have
been charged to ruled cores, every residual one-exchange triangle is a
top-packet triangle whose top locator satisfies (TOPK).

### Proof

Write `ell_{T_x}=p_0+p_1X+...+p_jX^j`.  Since

```text
ell_U=(X-x)ell_{T_x},
```

the coefficient of `X^b` in `ell_U` is `p_{b-1}-x p_b`, with
`p_{-1}=p_{j+1}=0`.  Therefore

```text
H_{1,j+1}(w)ell_U
 = sum_{b=0}^{j+1} w_b(p_{b-1}-x p_b)
 = sum_{b=0}^j w_{b+1}p_b - x sum_{b=0}^j w_b p_b,
```

which is (TOP1).  Applying (TOP1) to `w=u+zv` gives (TOP2).

Now suppose `T_x` and `T_y` contribute distinct slopes `z_x` and `z_y`.  By
(TOP2),

```text
A+z_xB=0,        A+z_yB=0,
```

where

```text
A=H_{1,j+1}(u)ell_U,        B=H_{1,j+1}(v)ell_U.
```

Subtracting gives `(z_x-z_y)B=0`, hence `B=0`, and then `A=0`.  This proves
(TOPK).  After fixed-slope charging, any residual one-exchange edge has
different slopes by the root-slice lemma, so the final residual statement
follows.

## Non-Ruled One-Exchange Degree Bound

Let `A_nr` be a residual `t=2` active locator family after fixed-slope root
slices and ruled determinant cores have been charged or removed.  Let
`G_1(A_nr)` be its one-exchange graph:

```text
T ~ T'        iff        |T cap T'|=j-1.
```

Then every vertex has one-exchange degree at most `j`:

```text
Gamma_1(A_nr) <= j.                              (DEG1)
```

Indeed, a locator `T` has exactly `j` possible `(j-1)` cores `R=T\{y}`.  For
each such core, the non-ruled determinant gate leaves at most two anchors in
total.  Since one of them is the anchor defining `T`, there is at most one
neighbor of `T` through that core.  Summing over the `j` cores gives (DEG1).

Equivalently, if `E_1(A_nr)` denotes unordered one-exchange edges, then

```text
E_1(A_nr) <= j |A_nr| / 2,
E_1(A_nr) <= binom(|D|,j-1).                     (EDGE1)
```

The second bound counts cores directly: after ruled cores are removed, each
core supports at most one unordered edge.  Thus high one-exchange codegree in
the `t=2` all-line Hankel branch can only come from fixed-slope root slices or
ruled determinant cores.

## Average-Collinearity Ledger Corollary

The degree bound plugs directly into the average support-collinearity ledger in
`experimental/notes/m1/m1_average_support_collinearity.md`.  To avoid a
notation clash with the locator degree `j`, write the line-field size as `Q`.
For `t=2`, the max-codegree bound in that ledger is

```text
B_2^max(A) = (1 - p_z)/(M p_z) + (4/M) Gamma_1(A) Q,
        p_z = Q^(-2)(1 - Q^(-2)),     M=|A|.
```

Therefore the non-ruled residual family satisfies

```text
B_2^max(A_nr) <= (1 - p_z)/(M p_z) + 4jQ/M.      (AVG1)
```

Consequently, in any parameter regime where `M p_z -> infinity` and
`M/(jQ) -> infinity`, the non-ruled one-exchange part contributes
`o(1)` to the missing-slope density in the average-collinearity ledger.  In the
usual heuristic scale `p_z ~ Q^(-2)`, this means the two visible average-ledger
requirements are `M >> Q^2` and `M >> jQ`.

This does not prove the worst-case M1 packing theorem.  It identifies the
remaining average-ledger obstruction after this local reduction: small residual
family size, fixed-slope root slices, ruled determinant cores, or higher
packet/two-exchange structure.

## Non-Claims

This lemma does not bound the remaining different-slope one-exchange graph, the
rank-one moving-slope ruled branch, top-packet triangles, the two-exchange
packet-edge ledger, or the one-outside boundary image.  It only proves that
same-slope one-exchange collisions belong to the fixed-slope root-slice ledger,
that such root slices lift to `(t+1,j-1)` Hankel cores,
classifies the ruled determinant core into fixed-slope, inactive, and rank-one
moving-slope cases, shows that star triangles are exactly ruled-core events
while residual top-packet edges lift to a common `t=1` Hankel kernel, shows
that non-ruled `t=2` one-exchange cores have at most two determinant anchors,
and gives the local max-degree bound and average-collinearity corollary above.

## Verification

The dependency-free verifier

```bash
python3 experimental/scripts/verify_m1_same_slope_root_slice_lemma.py
```

checks the subtraction identity over sampled small prime fields and exhaustively
checks the row-wise linear-map implication in small dimensions.  It checks the
higher-slack lift identity (LIFT), the quadratic determinant formula (DET2) and
the "three roots imply ruled" criterion in sampled small prime fields, then
stress-tests the ruled-core dichotomy, the injectivity of the residual rank-one
moving-slope branch, and the Johnson-graph star/top triangle classification.
Finally, it checks the top-packet lift identity (TOP1) and the distinct-slope
implication (TOPK).
