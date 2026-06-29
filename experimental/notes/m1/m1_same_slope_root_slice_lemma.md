# M1 Same-Slope One-Exchange Root-Slice Lemma

**Status:** PROVED-LOCAL / ROOT-SLICE REDUCTION / TWO-EXCHANGE PLANE LIFT /
FULL ELEMENTARY PACKET LIFT / RULED-CORE DICHOTOMY / RULED-CORE COLLAPSE /
HIGHER-SLACK LIFT / TRIANGLE CLASSIFICATION / TOP-PACKET LIFT /
TOP-PACKET LEDGER / SIMULTANEOUS KERNEL RECURSION / HYPERPLANE-FIBER
REDUCTION / AFFINE-FIBER REDUCTION / MOVING-FIBER DIMENSION DROP /
FIBER-COUNTING COROLLARY / RESIDUAL-DEGREE COROLLARY / AUDIT.

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

## Two-Exchange Full-Plane Lift

There is an exact two-exchange analogue.  Fix a `(j-2)`-set `R`, and write a
formal two-root locator through `R` in elementary coordinates

```text
T_{s,p}:        ell_{T_{s,p}}=(X^2-sX+p)ell_R.
```

For a fixed finite slope `z`, put again `L_z=H_{t,j}(u)+zH_{t,j}(v)`.  The
same-slope equation on this two-root plane is affine-linear in `(s,p)`:

```text
L_z ell_{T_{s,p}}
 =
 L_z(X^2 ell_R) - s L_z(X ell_R) + p L_z(ell_R).       (PLANE)
```

If three affinely non-collinear elementary points `(s_i,p_i)` satisfy

```text
L_z ell_{T_{s_i,p_i}}=0,        i=1,2,3,
```

then all three coefficient vectors vanish:

```text
L_z ell_R=0,        L_z(X ell_R)=0,        L_z(X^2 ell_R)=0.   (PLIFT0)
```

Equivalently,

```text
H_{t+2,j-2}(u+zv)ell_R=0.                         (PLIFT)
```

Indeed, the three padded equations in (PLIFT0) give respectively the row
blocks `0,...,t-1`, `1,...,t`, and `2,...,t+1` of (PLIFT).

Thus a same-slope two-exchange family through `R` that contains a
non-collinear triple is a full two-root plane and is charged to the lifted
`(t+2,j-2)` Hankel-core ledger.  After fixed-slope root slices and full-plane
lifts have been charged, any residual same-slope two-exchange family through a
fixed `(j-2)` core is contained in an affine line in the elementary `(s,p)`
plane.  This is the line-packet residual treated by
`m1_hankel_variable_line_packet_lemma.md`.

## Full Elementary Packet Lift

The same argument works in every exchange dimension.  Fix `h>=1` and a
`(j-h)`-core `R`.  Write a formal `h`-root factor in coefficient coordinates as

```text
P_c(X)=X^h+c_{h-1}X^{h-1}+...+c_0,
        c=(c_0,...,c_{h-1}) in F^h,
```

and put

```text
ell_{R,c}=P_c(X)ell_R.
```

For a fixed finite slope `z`, the landing map is affine-linear in `c`:

```text
L_z ell_{R,c}
 =
 L_z(X^h ell_R)+sum_{m=0}^{h-1} c_m L_z(X^m ell_R).   (HPKT)
```

If `h+1` affinely independent coefficient points
`c^{(0)},...,c^{(h)}` satisfy

```text
L_z ell_{R,c^{(i)}}=0        for 0<=i<=h,
```

then all coefficient vectors in (HPKT) vanish:

```text
L_z(X^m ell_R)=0        for 0<=m<=h.              (HLIFT0)
```

Equivalently,

```text
H_{t+h,j-h}(u+zv)ell_R=0.                         (HLIFT)
```

Indeed, the padded equation `L_z(X^m ell_R)=0` gives rows
`m,...,m+t-1` of (HLIFT), and the row blocks for `0<=m<=h` cover exactly
`0,...,t+h-1`.

Thus a same-slope `h`-exchange packet whose elementary coefficient points have
full affine span is not a new residual packet.  It is charged losslessly to the
lifted `(t+h,j-h)` Hankel-core ledger.  The root-slice lift is the case `h=1`,
and the two-exchange full-plane lift is the case `h=2`.

There is also a simultaneous-kernel version.  With

```text
K_{r,d}(u,v)
 =
 { U subset D : |U|=d,
   H_{r,d}(u)ell_U=0 and H_{r,d}(v)ell_U=0 },
```

if `h+1` affinely independent `h`-exchange extensions through a fixed
`(d-h)`-core `R` lie in `K_{r,d}(u,v)`, then applying (HLIFT) separately to
`u` and `v` gives

```text
R in K_{r+h,d-h}(u,v).                            (KHLIFT)
```

Consequently residual simultaneous-kernel packets can be organized by affine
rank: full-rank elementary packets move to the next `h` levels of the Hankel
ladder, while lower-rank packets are the true residual objects to classify.
This is the general form of the lossless residual-depth frontier shift used by
the top-packet recursion below.

## Affine-Span Normal Form for Rank-Defect Packets

The lower-rank residual packets also have an exact normal form.  Keep the
`h`-exchange notation above and write

```text
V_m=L_z(X^m ell_R),        0<=m<=h.
```

Let `C subset F^h` be a set of coefficient points satisfying

```text
L_z ell_{R,c}=0        for every c in C.
```

Let `A=aff(C)=c_*+W` be its affine span, with direction subspace
`W subset F^h`.  Then the equations on `C` are equivalent to

```text
V_h+sum_{m=0}^{h-1} c_{*,m} V_m=0,               (ASP0)
sum_{m=0}^{h-1} w_m V_m=0        for every w in W.   (ASPD)
```

Consequently

```text
L_z ell_{R,c}=0        for every c in A.          (ASPA)
```

So a same-slope packet is always a whole formal affine subpacket in elementary
coefficient space, not just a finite accidental set of killed points.

Choose coordinates so that the rank `r=dim W` directions of `W` are written as
columns of an `h x r` matrix `B`, and write `c(theta)=c_*+B theta`.  Then the
packet identity is

```text
L_z ell_{R,c(theta)}
 =
 (V_h+sum_m c_{*,m}V_m)
 + sum_{a=1}^r theta_a (sum_m B_{m,a}V_m).        (ASPC)
```

Thus rank `r` packets impose exactly `r+1` independent affine-span equations
on the shifted Hankel landing vectors.  The full-rank lift above is the case
`r=h`, where these equations force every `V_m` to vanish.  After the full-rank
charge, every remaining same-slope `h`-exchange packet lies in a proper affine
subspace of coefficient space, and the next classification problem is to bound
or charge those rank-defect affine subpackets.

For `h=2`, a proper nontrivial affine span is exactly a line

```text
A s+B p+C=0
```

in the two-root elementary plane.  The next section classifies the split-root
points on such a line as fixed-root, fixed-sum, or product-Mobius packets.

## Fixed-Root Hyperplane Criterion

The codimension-one rank-defect packets have a clean root-slice test.  In the
`h`-exchange coefficient coordinates above, let

```text
P_c(X)=X^h+c_{h-1}X^{h-1}+...+c_0
```

and let `H(a,b)` be the affine hyperplane

```text
b+sum_{m=0}^{h-1} a_m c_m=0,        a=(a_0,...,a_{h-1}) != 0.
```

Then `H(a,b)` is exactly the coefficient hyperplane of monic `h`-root factors
containing one fixed finite root `alpha` if and only if there is a scalar
`lambda != 0` such that

```text
a_m=lambda alpha^m        for 0<=m<h,
b=lambda alpha^h.                                      (FROOT)
```

Indeed, the condition `P_c(alpha)=0` is

```text
alpha^h+sum_{m=0}^{h-1} alpha^m c_m=0,
```

which is (FROOT) after multiplying by `lambda`.  Conversely, if (FROOT) holds,
then `H(a,b)` is exactly `P_c(alpha)=0`.  Every split locator in this
hyperplane has the fixed root `alpha`, so it factors as

```text
P_c(X)=(X-alpha)Q(X),
```

and the whole packet is charged to the `(h-1)`-exchange root-slice ledger
through the enlarged core `R union {alpha}`.  Thus, after fixed-root
hyperplanes are charged, the remaining codimension-one rank-defect packets are
precisely non-evaluation hyperplanes in coefficient space.

For `h=2` and `P=X^2-sX+p`, the criterion gives

```text
p-alpha s+alpha^2=0,
```

equivalently `(x-alpha)(y-alpha)=0`.  This is exactly the fixed-root line
removed in the two-root classification below.

## One-Root Fibers of Hyperplane Packets

Every coefficient hyperplane also has a one-root fiber dichotomy.  Keep
`H(a,b)` as above, and fix a monic `(h-1)`-root factor

```text
Q_d(X)=X^{h-1}+d_{h-2}X^{h-2}+...+d_0.
```

Put `d_{h-1}=1` and `d_{-1}=0`.  The one-root extensions through `Q_d` are

```text
P_y(X)=(X-y)Q_d(X)
      =X^h+c_{h-1}(y)X^{h-1}+...+c_0(y),
```

with

```text
c_m(y)=d_{m-1}-y d_m,        0<=m<h.             (HFIB)
```

Therefore the hyperplane equation on this fiber is affine-linear in `y`:

```text
b+sum_m a_m c_m(y)
 =
 (b+sum_m a_m d_{m-1}) - y (sum_m a_m d_m).      (HLINE)
```

Consequently a fixed core `Q_d` has either at most one extension in `H(a,b)`,
or the whole affine one-root line `{(X-y)Q_d : y in F}` lies in `H(a,b)`.  The
second case is exactly the pair of lower-degree equations

```text
sum_m a_m d_m=0,
b+sum_m a_m d_{m-1}=0.                            (HFULL)
```

Thus a codimension-one rank-defect packet cannot contain an accidental
one-exchange edge.  If two same-slope `h`-exchange locators in such a packet
share an `(h-1)` core, then the whole one-root affine fiber through that core
is in the packet.  In the Hankel landing problem this full fiber is charged by
the one-exchange root-slice lift already proved above:

```text
L_z(ell_R Q_d)=0,        L_z(X ell_R Q_d)=0,
```

equivalently to the lifted `(t+1,j-1)` Hankel core on `ell_R Q_d`.  After
these full one-root fibers are charged, the residual part of every
codimension-one coefficient-hyperplane packet has no one-exchange edges.

## Affine-Subpacket One-Root Fiber Dichotomy

The same dichotomy holds for every lower-rank affine subpacket, not only
hyperplanes.  Let

```text
A=c_*+W subset F^h
```

be any affine coefficient subspace, and keep the one-root fiber

```text
c(y)=(c_0(y),...,c_{h-1}(y)),
c_m(y)=d_{m-1}-y d_m,
```

through a fixed monic `(h-1)`-root factor `Q_d`, with `d_{h-1}=1`.  Put

```text
d_vec=(d_0,d_1,...,d_{h-1}) in F^h.              (ADIR)
```

If two distinct extensions `c(y_1),c(y_2)` lie in `A`, then

```text
c(y_2)-c(y_1)=-(y_2-y_1)d_vec in W.
```

Since `y_2-y_1 != 0`, this gives `d_vec in W`, and hence

```text
c(y)=c(y_1)-(y-y_1)d_vec in A        for every y.  (AFIB)
```

Thus an affine rank-defect packet meets a fixed one-root fiber in at most one
point, unless it contains the whole one-root fiber.  Equivalently, after full
one-root fibers are charged to the lifted root-slice ledger, no residual
rank-defect affine packet has one-exchange edges.  This upgrades the
codimension-one hyperplane statement to the entire affine-span filtration from
the previous section.

## Affine-Subpacket Two-Root Fiber Dichotomy

There is an analogous two-exchange filtration.  Assume `h>=2`, fix a monic
`(h-2)`-root factor

```text
Q_e(X)=X^{h-2}+e_{h-3}X^{h-3}+...+e_0,
```

and put `e_{h-2}=1`, while `e_i=0` outside `0<=i<=h-2`.  The two-root
extensions through `Q_e` are

```text
P_{s,p}(X)=(X^2-sX+p)Q_e(X)
          =X^h+c_{h-1}(s,p)X^{h-1}+...+c_0(s,p),
```

where

```text
c_m(s,p)=e_{m-2}-s e_{m-1}+p e_m,        0<=m<h.   (TFIB)
```

Thus the coefficient image of the two-root fiber is an affine plane in `F^h`
with direction vectors

```text
d_s=(-e_{m-1})_{0<=m<h},        d_p=(e_m)_{0<=m<h}.  (TDIR)
```

Let `A=c_*+W` be any affine rank-defect packet.  If three affinely
non-collinear points `(s_i,p_i)` of the two-root parameter plane have
`c(s_i,p_i) in A`, then the two independent differences among those points
show that both `d_s` and `d_p` lie in `W`.  Hence

```text
c(s,p) in A        for every (s,p) in F^2.          (TWHOLE)
```

So an affine rank-defect packet meets a fixed two-root fiber in an affine
subspace of the `(s,p)` plane: either the whole plane, or a line, or a point,
or the empty set.  In the killed same-slope Hankel setting, the whole-plane
case is exactly the two-exchange full-plane lift already proved above,

```text
L_z(ell_R Q_e)=L_z(X ell_R Q_e)=L_z(X^2 ell_R Q_e)=0,
```

equivalently the lifted `(t+2,j-2)` Hankel core on `ell_R Q_e`.  After those
full planes are charged, every residual affine rank-defect packet has only
line-packet intersections on each fixed two-root fiber.  For `h=2`, this is
precisely the residual two-root line classification below.

## General Moving-Fiber Dimension Drop

The one-root and two-root statements are the first cases of a uniform
moving-fiber rule.  Fix `1<=r<=h` and a monic `(h-r)`-root factor

```text
Q(X)=X^{h-r}+e_{h-r-1}X^{h-r-1}+...+e_0,
```

with `e_{h-r}=1` and `e_i=0` outside `0<=i<=h-r`.  Let

```text
B_a(X)=X^r+a_{r-1}X^{r-1}+...+a_0,        a in F^r,
P_a(X)=B_a(X)Q(X)
      =X^h+c_{h-1}(a)X^{h-1}+...+c_0(a).
```

Then the coefficient map `a |-> c(a)` is the affine embedding

```text
c_m(a)=e_{m-r}+sum_{i=0}^{r-1} a_i e_{m-i},       0<=m<h.  (RFIB)
```

Its direction vectors

```text
d_i=(e_{m-i})_{0<=m<h},        0<=i<r,             (RDIR)
```

are linearly independent: a relation among them would make
`(sum_i a_i X^i)Q(X)=0`, hence `sum_i a_i X^i=0`.

Let `A=c_*+W subset F^h` be an affine rank-defect packet.  The intersection
of `A` with the moving `r`-root fiber is the preimage of `A` under this affine
embedding, hence an affine subspace of `F^r`.  If this preimage has full
affine rank `r` -- equivalently, if it contains `r+1` affinely independent
parameter points -- then every direction `d_i` lies in `W`, and the whole
moving `r`-root fiber lies in `A`.  Otherwise the intersection has affine rank
at most `r-1`.

In the killed same-slope Hankel setting, the full-fiber case is exactly the
full elementary-packet lift with moving size `r`:

```text
L_z(X^i ell_R Q)=0        for 0<=i<=r,
```

equivalently the lifted `(t+r,j-r)` Hankel core on `ell_R Q`.  Therefore,
after all full moving `r`-root fibers are charged, residual affine
rank-defect packets meet each fixed `r`-root fiber only in lower-dimensional
affine subpackets.  This is the general lossless dimension drop behind the
one-root edge removal and the two-root line-packet reduction.

## Finite-Field Fiber Counting Corollary

Over a finite field `F` with `|F|=Q_F`, the preceding dimension drop has an
immediate counting form.  Fix `r`, a fixed `(h-r)` core `Q`, and an affine
rank-defect packet `A=c_*+W`.  If the moving `r`-root fiber over `Q` has not
been charged as a full fiber, then

```text
# { a in F^r : coeff(B_a Q) in A } <= Q_F^{r-1}.     (RCOUNT)
```

Indeed, the parameter set is an affine subspace of `F^r` of rank at most
`r-1`.  Split-root, distinct-root, domain-root, noncontainment, quotient, or
tangent filters can only shrink this formal count.

Thus every fixed `(h-r)` core contributes at most `Q_F^{r-1}` residual formal
same-slope `r`-exchange parameters after the full moving-fiber charge.  For
`r=1` this recovers the residual no-one-exchange-edge statement; for `r=2` it
recovers the line-packet ceiling.  The corollary is not an all-line M1 bound
by itself, but it is the finite-field counting input supplied by the
rank-defect packet filtration.

## Residual Exchange-Degree Corollary

The same count gives a local exchange-degree bound.  Work inside one affine
rank-defect `h`-exchange packet after all full moving `r`-root fibers have
been charged.  Let `G_r^{res}` be the graph on the remaining split `h`-root
locators where two vertices are adjacent when they share exactly `h-r` of the
moving roots, equivalently when they lie in a common fixed `(h-r)` fiber.

For a fixed residual locator, there are `binom(h,r)` choices of the shared
`(h-r)` subfactor.  For each such choice, the finite-field fiber count leaves
at most `Q_F^{r-1}` residual formal parameters in that fiber, one of which is
the original locator.  Hence

```text
Delta(G_r^{res}) <= binom(h,r)(Q_F^{r-1}-1).        (RDEG)
```

Domain-root, distinct-root, split-root, quotient, tangent, and noncontainment
filters can only reduce this degree.  In particular `r=1` gives
`Delta(G_1^{res})=0`, while `r=2` gives the line-packet degree ceiling
`binom(h,2)(Q_F-1)`.  This is the graph-codegree form of the moving-fiber
filtration and is the version most directly consumable by the remaining
different-slope and average-ledger estimates.

## Two-Root Line Classification

The residual affine lines in the elementary two-root plane have only the
expected forms.  Let

```text
A s + B p + C = 0,        (A,B) != (0,0),
```

be an affine line in `(s,p)=(x+y,xy)`.

If `B=0`, then the line is a fixed-sum packet

```text
x+y=s_0,        s_0=-C/A,
```

with involution `x |-> s_0-x`.

If `B != 0`, write

```text
c=-A/B,        beta=-C/B,        mu=c^2+beta.
```

Then the line equation is equivalent to

```text
(x-c)(y-c)=mu.
```

If `mu=0`, every split pair on the line contains the fixed root `c`; this is
the fixed-root line already charged by the one-exchange root-slice ledger
through `R union {c}`.  If `mu != 0`, the line is a product-Mobius packet with
involution

```text
x |-> c + mu/(x-c).
```

Thus after full-plane and fixed-root line charges, the only same-slope
two-exchange line packets left are fixed-sum and nondegenerate product-Mobius
packets.  These are exactly the two models used in
`m1_hankel_variable_line_packet_lemma.md`.

## Non-Fixed Line-Packet Constant-Slope Collapse

In the `t=2` Hankel setting, the two non-fixed line models cannot be
constant-slope residuals.  Fix a `(j-2)` core `R`, a finite slope `z`, and put
`w_z=u+zv`.  Write the four shifted scalar landing rows as

```text
d_i=row_i(H_{4,j-2}(w_z)ell_R),        0<=i<=3.
```

For a two-root locator

```text
T_{s,p}=R union {x,y},        s=x+y,        p=xy,
```

the killed equation is

```text
H_{2,j}(w_z)ell_{T_{s,p}}
 =
 (d_2-sd_1+pd_0,  d_3-sd_2+pd_1).        (TLIN)
```

First consider a fixed-sum line `s=s_0`.  If (TLIN) vanishes for every point
on this affine line, as a polynomial in the free coordinate `p`, then

```text
(d_0,d_1)=0,        (d_2,d_3)=s_0(d_1,d_2).
```

The Hankel overlap forces `d_0=d_1=d_2=d_3=0`, hence

```text
H_{4,j-2}(w_z)ell_R=0.                         (FSCOLL)
```

So a constant-slope fixed-sum line is already charged to the full-plane
`(t+2,j-2)` Hankel lift.

Now consider a product-Mobius line

```text
(x-c)(y-c)=mu,        mu != 0,
```

equivalently `p=cs-c^2+mu`.  If (TLIN) vanishes for every point of this line,
then

```text
(d_1,d_2)=c(d_0,d_1),
(d_2,d_3)=(c^2-mu)(d_0,d_1).
```

The first relation gives `d_1=cd_0` and `d_2=c^2d_0`; comparing with the first
coordinate of the second relation gives `mu d_0=0`.  Since `mu != 0`, all
four `d_i` vanish, so again `H_{4,j-2}(w_z)ell_R=0`.

Therefore, after full two-root planes and fixed-root lines have been charged,
no surviving fixed-sum or nondegenerate product-Mobius line packet is killed
at one finite slope.  Consequently the active finite-slope map on every
surviving non-fixed line packet is injective: if two distinct packet points had
the same slope `z`, the affine-linear function (TLIN) restricted to the line
would vanish at two points and hence on the whole line, contradicting the
collapse just proved.

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

## Hankel Shift Collapse of Ruled Cores

For the actual Hankel one-exchange pencils, the rank-one moving-slope branch
from the abstract affine dichotomy cannot occur.  Keep the `(j-1)` core `R`
and write, for any syndrome vector `w`,

```text
c_i(w)=row_i(H_{3,j-1}(w)ell_R),        i=0,1,2.
```

Then

```text
H_{2,j}(w)ell_{T_y}
 =
 (c_1(w)-y c_0(w),  c_2(w)-y c_1(w)).             (SHIFT)
```

Suppose the determinant core is ruled:

```text
det(a_y,b_y)=0        for every y.
```

Then either `b_y=0` for every `y`, or there is a fixed finite slope
`z_0 in F` such that

```text
a_y+z_0 b_y=0        for every y.                 (HC)
```

Thus every active ruled core is already a fixed-slope root-slice core.  After
fixed-slope root slices have been charged, ruled determinant cores contribute
no residual one-exchange edges.

### Proof

By the ruled-core dichotomy above, it remains only to eliminate the rank-one
moving-slope case.  In that case all vectors

```text
a_X,a_0,b_X,b_0
```

lie in one output line `C subset F^2`.  Choose a nonzero linear form
`m=(m_0,m_1)` killing `C`.  For `w=u` and `w=v`, equation (SHIFT) lies in `C`
for every `y`, so

```text
m_0(c_1(w)-y c_0(w))+m_1(c_2(w)-y c_1(w))=0
        for every y.
```

Therefore

```text
m_0 c_0(w)+m_1 c_1(w)=0,
m_0 c_1(w)+m_1 c_2(w)=0.                         (REC)
```

The two equations (REC) have a one-dimensional solution space in
`(c_0,c_1,c_2)`, since `m != 0`.  Hence the triples
`(c_0(u),c_1(u),c_2(u))` and `(c_0(v),c_1(v),c_2(v))` are proportional.  By
(SHIFT), the affine vector pencils `a_y` and `b_y` are proportional by the same
constant for every `y`.  If the `v` triple is zero then `b_y=0` for every `y`;
otherwise the proportionality gives one fixed finite slope `z_0` satisfying
(HC).  This rules out a genuine moving-slope ruled Hankel core.

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
Since ruled cores collapse to fixed-slope or inactive Hankel cores, every
residual one-exchange triangle after fixed-slope root-slice charging is
therefore a top-packet triangle.

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

## Top-Packet Compression Ledger

The previous lift also turns residual top-packet triangles into a named
higher-slack ledger.  Define the simultaneous lifted top-kernel family

```text
K_top(u,v)
 =
 { U subset D : |U|=j+1,
   H_{1,j+1}(u)ell_U=0 and H_{1,j+1}(v)ell_U=0 }.
```

Let `A_res` be a residual `t=2` active locator family after fixed-slope
root slices have been charged.  For `U` of size `j+1`, write

```text
A_U={ x in U : U\{x} in A_res }.
```

If `|A_U|>=2`, then every two members of this packet form a residual
one-exchange edge, hence have distinct slopes.  By (TOPK), such a packet
satisfies `U in K_top(u,v)`.

Therefore residual top-packet edges inject into

```text
{ (U,{x,y}) : U in K_top(u,v), x,y in U, x != y },
```

via the union map `{U\{x},U\{y}} |-> (U,{x,y})`.  In particular

```text
E_top(A_res) <= binom(j+1,2) |K_top(u,v)|.        (TE)
```

Likewise, every residual one-exchange triangle is a top-packet triangle after
star triangles have been charged to ruled cores, so residual triangles inject
into

```text
{ (U,{x,y,z}) : U in K_top(u,v), x,y,z in U distinct },
```

and hence

```text
Tri_1(A_res) <= binom(j+1,3) |K_top(u,v)|.        (TT)
```

Inside a lifted top packet the `t=2` slope equation is only scalar.  For
`U in K_top(u,v)` and `x in U`, put

```text
rho_x(w)=row_0(H_{2,j}(w)ell_{U\{x}}).
```

Since `H_{1,j+1}(w)ell_U=0`, identity (TOP1) gives

```text
H_{2,j}(w)ell_{U\{x}} = rho_x(w) (1,x),
        w in {u,v}.
```

Thus the active finite slope on `U\{x}` is determined by the scalar ratio

```text
rho_x(u)+z rho_x(v)=0,        rho_x(v) != 0.
```

The top-packet branch is therefore reduced to the lifted `t=1` kernel family
`K_top(u,v)` plus this one-dimensional slope label.  It is not an independent
two-row `t=2` residual phenomenon.

## Simultaneous Top-Kernel Root-Slice Recursion

The lifted top-kernel family has the same lossless root-slice recursion.  For
`r>=1` and locator size `d`, define

```text
K_{r,d}(u,v)
 =
 { U subset D : |U|=d,
   H_{r,d}(u)ell_U=0 and H_{r,d}(v)ell_U=0 }.
```

Thus `K_top(u,v)=K_{1,j+1}(u,v)`.  Fix a `(d-1)`-core `R` and write

```text
U_y=R union {y},        ell_{U_y}=(X-y)ell_R.
```

If two distinct extensions through `R` lie in `K_{r,d}(u,v)`, then for both
`w in {u,v}`,

```text
H_{r,d}(w)ell_{U_{y_1}}=H_{r,d}(w)ell_{U_{y_2}}=0.
```

Subtracting gives the padded equation

```text
H_{r,d}(w)ell_R=0,
```

and substituting back gives

```text
H_{r,d}(w)(Xell_R)=0.
```

These two padded blocks are exactly the first `r` and last `r` rows of

```text
H_{r+1,d-1}(w)ell_R=0.
```

Therefore

```text
R in K_{r+1,d-1}(u,v).                            (KREC)
```

In particular, every one-exchange collision inside the lifted top-kernel
family is charged to the next simultaneous Hankel kernel.  After such
`K_{r+1,d-1}` root slices have been charged, the residual part of
`K_{r,d}(u,v)` has no one-exchange edges.  This is the top-kernel version of
the residual-depth frontier shift: the shift is an identity, so this source of
depth recursion is additive by construction rather than a new multiplicative
loss at level `r`.

## Boundary-Off External-Anchor Corollary

The same one-exchange algebra also applies to one-outside boundary targets.
Let `S subset D` have size `j-1`, and let `beta in F\D` be an external anchor.
Write the formal one-outside locator as

```text
B_beta=S union {beta},        ell_{S,beta}=(X-beta)ell_S.
```

For the `t=2` Hankel landing vectors

```text
a_beta=H(u)ell_{S,beta},        b_beta=H(v)ell_{S,beta}        in F^2,
```

the determinant gate is again a quadratic polynomial in the anchor:

```text
Delta_S(beta)=det(a_beta,b_beta).
```

If `Delta_S` is not identically zero, then at most two external anchors
`beta in F\D` pass the rank-one landing condition.  If three external anchors
pass, then `Delta_S` vanishes identically on `F`, and the Hankel shift collapse
above applies with `y` replaced by the external coordinate `beta`.  Hence the
ruled external-anchor branch is either inactive,

```text
b_beta=0        for every beta,
```

or fixed finite slope,

```text
a_beta+z_0 b_beta=0        for every beta.
```

In the fixed finite-slope case the same subtraction argument gives

```text
(H_{2,j}(u)+z_0H_{2,j}(v))ell_S=0,
(H_{2,j}(u)+z_0H_{2,j}(v))(Xell_S)=0,
```

equivalently the lifted `H_{3,j-1}(u+z_0v)ell_S=0` core.  Thus the ruled
one-outside branch is not a separate quotient-periodic or aperiodic residual:
after fixed-slope boundary root slices are charged, each `(j-1)` shadow
supports at most two active non-ruled external anchors.

There is a ledger-facing shadow form.  Let `Boundary_off^res` be the residual
active one-outside target family after fixed-slope boundary root slices have
been charged, and project

```text
pi(B_beta)=S,        B_beta=S union {beta}, beta notin D.
```

For each shadow `S`,

```text
# pi^{-1}(S) <= 2.                              (BOFIB)
```

Moreover the finite-slope map is injective on each residual shadow fiber.  If
two distinct external anchors `beta_1,beta_2` over the same `S` had the same
finite slope `z`, then for `w_z=u+zv`,

```text
H_{2,j}(w_z)ell_{S,beta_i}=0,        i=1,2.
```

Subtracting gives `H_{2,j}(w_z)ell_S=0`, and substituting back gives
`H_{2,j}(w_z)(Xell_S)=0`.  These are exactly the overlapping row blocks of

```text
H_{3,j-1}(w_z)ell_S=0,
```

so the pair was already charged as a fixed-slope boundary root slice.  Hence,
after that charge, a boundary shadow has at most two residual external anchors,
and if two remain then they carry distinct finite slopes.  Consequently

```text
|Boundary_off^res| <= 2 |Shadow_off^res|,        (BOSH)
```

where `Shadow_off^res=pi(Boundary_off^res)`.  This still does not bound the
shadow image itself, but it removes external-anchor multiplicity from the
one-outside ledger.

## Residual One-Exchange Degree Bound

Let `A_res` be a residual `t=2` active locator family after fixed-slope root
slices have been charged or removed.  Let `G_1(A_res)` be its one-exchange
graph:

```text
T ~ T'        iff        |T cap T'|=j-1.
```

Then every vertex has one-exchange degree at most `j`:

```text
Gamma_1(A_res) <= j.                             (DEG1)
```

Indeed, a locator `T` has exactly `j` possible `(j-1)` cores `R=T\{y}`.  For
each such core, either `Delta_R` is nonzero, in which case the determinant gate
leaves at most two anchors in total, or `Delta_R` is ruled, in which case the
Hankel shift collapse makes the core fixed-slope or inactive.  A ruled active
core with two anchors would have been charged as a fixed-slope root slice, so
it contributes no residual edge.  Thus each core supplies at most one residual
neighbor of `T`.  Summing over the `j` cores gives (DEG1).

Equivalently, if `E_1(A_res)` denotes unordered one-exchange edges, then

```text
E_1(A_res) <= j |A_res| / 2,
E_1(A_res) <= binom(|D|,j-1).                    (EDGE1)
```

The second bound counts cores directly: after fixed-slope root slices are
charged, each core supports at most one unordered residual edge.  Thus high
one-exchange codegree in the `t=2` all-line Hankel branch can only come from
the fixed-slope root-slice ledger, not from a separate ruled-core residual.

## Average-Collinearity Ledger Corollary

The degree bound plugs directly into the average support-collinearity ledger in
`experimental/notes/m1/m1_average_support_collinearity.md`.  To avoid a
notation clash with the locator degree `j`, write the line-field size as `Q`.
For `t=2`, the max-codegree bound in that ledger is

```text
B_2^max(A) = (1 - p_z)/(M p_z) + (4/M) Gamma_1(A) Q,
        p_z = Q^(-2)(1 - Q^(-2)),     M=|A|.
```

Therefore the residual family after fixed-slope root-slice charging satisfies

```text
B_2^max(A_res) <= (1 - p_z)/(M p_z) + 4jQ/M.     (AVG1)
```

Consequently, in any parameter regime where `M p_z -> infinity` and
`M/(jQ) -> infinity`, the residual one-exchange part contributes
`o(1)` to the missing-slope density in the average-collinearity ledger.  In the
usual heuristic scale `p_z ~ Q^(-2)`, this means the two visible average-ledger
requirements are `M >> Q^2` and `M >> jQ`.

This does not prove the worst-case M1 packing theorem.  It identifies the
remaining average-ledger obstruction after this local reduction: small residual
family size, fixed-slope root slices, or higher packet/two-exchange structure.

There is also a packet-level higher-exchange form.  Let the support slack in
the average-collinearity ledger be `tau`, and let the field size be `Q_F`.
Suppose `A_res` is contained in one same-slope affine `h`-exchange packet after
all full moving `r`-root fibers have been charged for
`1<=r<=min(h,tau-1)`.  Then the residual exchange-degree corollary gives

```text
Gamma_r(A_res) <= binom(h,r)(Q_F^{r-1}-1),   1<=r<=min(h,tau-1),
Gamma_r(A_res) = 0,                          r>h.              (GAMH)
```

Substituting (GAMH) into the same maximum-codegree average ledger yields

```text
B_tau^max(A_res)
 <= (1 - p_z)/(M p_z)
    + (4/M) sum_{r=1}^{min(h,tau-1)}
        binom(h,r)(Q_F^{r-1}-1) Q_F^{tau-r},

p_z = Q_F^{-tau}(1 - Q_F^{-tau}),    M=|A_res|.                 (AVGH)
```

In particular,

```text
B_tau^max(A_res)
 <= (1 - p_z)/(M p_z)
    + (4 Q_F^{tau-1}/M) sum_{r=1}^{min(h,tau-1)} binom(h,r).     (AVGHc)
```

The `r=1` summand is zero, recovering the no residual one-exchange statement
inside a charged moving-fiber packet.  Formula (AVGH) is still local to a
single affine packet; a global M1 bound must also sum over packet choices and
the quotient, tangent/contained, split-root, and fixed-slope ledgers.

## Non-Claims

This lemma does not bound the isolated lifted top-kernel family `K_top(u,v)`,
the two-exchange packet-edge ledger, or the full one-outside boundary image.  It
only proves that
same-slope one-exchange collisions belong to the fixed-slope root-slice ledger,
that such root slices lift to `(t+1,j-1)` Hankel cores,
that non-collinear same-slope two-exchange planes lift to `(t+2,j-2)` Hankel
cores, that full affine-rank `h`-exchange elementary packets lift to
`(t+h,j-h)` Hankel cores, identifies the affine-span normal form for
rank-defect elementary packets, gives the fixed-root criterion for
codimension-one coefficient hyperplanes, proves the one-root fiber dichotomy
for coefficient hyperplanes and then for all affine rank-defect packets,
proves the two-root fiber dichotomy for affine rank-defect packets, and shows
the general moving-fiber dimension drop and finite-field fiber-counting
corollary, gives the residual exchange-degree corollary, and shows that
residual two-root lines are fixed-root, fixed-sum, or product-Mobius packets,
proves that constant-slope non-fixed two-root lines collapse to the full-plane
Hankel lift and hence surviving non-fixed line packets have injective slope
maps,
classifies the ruled determinant core into fixed-slope, inactive, and rank-one
moving-slope cases for abstract affine pencils, proves the Hankel shift
collapse that eliminates the moving-slope ruled residual, shows that star
triangles are exactly ruled-core events while residual top-packet edges lift to
a common `t=1` Hankel kernel, compresses residual top-packet edges and
triangles into the lifted top-kernel ledger, proves the exact simultaneous
top-kernel root-slice recursion, classifies the ruled external-anchor boundary
branch, reduces the residual one-outside target image to a boundary-shadow
image with fibers of size at most two, and gives the local max-degree bound and
average-collinearity corollary above, including the packet-level
higher-exchange ledger substitution.

## Verification

The dependency-free verifier

```bash
python3 experimental/scripts/verify_m1_same_slope_root_slice_lemma.py
```

checks the subtraction identity over sampled small prime fields and exhaustively
checks the row-wise linear-map implication in small dimensions.  It checks the
higher-slack lift identity (LIFT), the two-exchange full-plane lift (PLIFT),
the full elementary packet lift (HLIFT), the two-root line classification, the
affine-span normal form for rank-defect packets, the fixed-root hyperplane
criterion, the hyperplane one-root fiber dichotomy, the quadratic determinant
formula (DET2), the affine-subpacket one-root and two-root fiber dichotomies,
the general moving-fiber dimension drop and counting corollary, and the
residual exchange-degree and average-ledger corollaries, and the "three roots
imply ruled" criterion in sampled small prime fields.  It checks the
constant-slope non-fixed two-root line collapse, then stress-tests the abstract
ruled-core dichotomy and the Hankel ruled-core collapse.  It also checks the
Johnson-graph star/top triangle classification, the top-packet lift identity
(TOP1), the distinct-slope implication (TOPK), and the top-packet edge/triangle
compression ledger.  It checks the simultaneous kernel root-slice recursion
(KREC) over exhaustive and sampled small-field instances.  The same verifier
also checks the boundary-off external-anchor corollary and boundary-shadow
fiber reduction over sampled small domains.
