# M1 Same-Slope One-Exchange Root-Slice Lemma

**Status:** PROVED-LOCAL / ROOT-SLICE REDUCTION / TWO-EXCHANGE PLANE LIFT /
FULL ELEMENTARY PACKET LIFT / RULED-CORE DICHOTOMY / RULED-CORE COLLAPSE /
HIGHER-SLACK LIFT / TRIANGLE CLASSIFICATION / TOP-PACKET LIFT /
TOP-PACKET LEDGER / SIMULTANEOUS KERNEL RECURSION / HYPERPLANE-FIBER
REDUCTION / AFFINE-FIBER REDUCTION / MOVING-FIBER DIMENSION DROP /
FIBER-COUNTING COROLLARY / BOUNDARY-CORE SLOPE-FIBER INJECTION /
BOUNDARY QUARTIC KUMMER GATE / ROOT-CORE RECURRENCE CHART /
ROOT-CORE SLOPE COVER /
ROOT-CORE DOMAIN KUMMER FILTER /
SQUARE-MAP PACKET INTERSECTION GATE /
SQUARE-NORM ENDPOINT PALETTE /
SQUARE-NORM REPEATED-ENDPOINT GATE /
SQUARE-NORM DOUBLE-ROOT CERTIFICATE /
SQUARE-NORM RAW-COEFFICIENT ENDPOINT CERTIFICATE /
SQUARE-NORM RAW-ENDPOINT DISCRIMINANT CERTIFICATE /
SQUARE-NORM HANKEL-MINOR DISCRIMINANT CERTIFICATE /
SQUARE-NORM PLUCKER-MINOR DISCRIMINANT CERTIFICATE /
SQUARE-NORM PLUCKER-CHART DECOMPOSITION /
SQUARE-NORM PLUCKER-CHART ROW RECURRENCE /
SQUARE-NORM PLUCKER-CHART HANKEL SQUARE FACTORIZATION /
SQUARE-NORM PLUCKER-CHART ENDPOINT SLOPE MAP /
SQUARE-NORM OVERLAPPING PLUCKER-CHART RECURRENCE /
SQUARE-NORM OVERLAPPING ENDPOINT-PAIR INVERSION /
SQUARE-NORM PROJECTIVE ENDPOINT-PAIR INVERSION /
SQUARE-NORM PROJECTIVE DIAGONAL ENDPOINT COLLAPSE /
SQUARE-NORM OFF-DIAGONAL ENDPOINT-PAIR COUNT /
SQUARE-NORM CANONICAL ENDPOINT-PAIR NORM FACTORIZATION /
SQUARE-NORM FIXED ENDPOINT-PAIR COSET PALETTE /
SQUARE-NORM FIXED-BASIS ENDPOINT-PALETTE BOUND /
SQUARE-NORM ENDPOINT-CHARGE COROLLARY /
SQUARE-MAP PACKET-COUNT COROLLARY /
RESIDUAL-DEGREE COROLLARY / AUDIT.

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

The same normal form also controls mixed-domain boundary traces.  Let `L` be a
non-fixed affine line in the elementary plane, and fix a `(j-2)` core `R`.
The mixed trace over `R` is

```text
Trace_off(L,R)
 = { (beta,y) in (F\D) x (D\R) : (beta+y,beta y) in L }.
```

If `L` is the fixed-sum line `s=s_0`, then

```text
beta=s_0-y.                                      (FS-OFF)
```

If `L` is the nondegenerate product-Mobius line

```text
(x-c)(y-c)=mu,        mu != 0,
```

then

```text
beta=c+mu/(y-c).                                (PM-OFF)
```

Thus the mixed boundary trace of every surviving non-fixed line packet is the
graph of the same involution used by the all-domain packet, restricted to
domain roots whose partner escapes `D`.  In particular each such line has at
most `|D\R|=n-j+2` mixed boundary pairs, and its external-anchor image is no
larger.  If `mu=0`, the line is the fixed-root line `(x-c)(y-c)=0`, and the
large vertical/horizontal mixed fibers are precisely the fixed-root
root-slice case already charged.

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

The shadow condition also has an intrinsic rank-one form.  For a fixed shadow
`S` and finite slope `z`, put `w_z=u+zv` and

```text
c_i=row_i(H_{3,j-1}(w_z)ell_S),        0<=i<=2.
```

An anchor `beta in F` satisfies

```text
H_{2,j}(w_z)ell_{S,beta}=0
```

if and only if either

```text
(c_0,c_1,c_2)=(0,0,0),                         (BZ0)
```

or

```text
c_0 != 0,        c_1^2=c_0 c_2,        beta=c_1/c_0.     (BR1)
```

Indeed, the boundary equation is

```text
c_1-beta c_0=0,        c_2-beta c_1=0.
```

If `c_0 != 0`, the first equation forces `beta=c_1/c_0`, and the second is
exactly `c_1^2=c_0c_2`.  If `c_0=0`, then the first equation forces `c_1=0`,
and the second forces `c_2=0`.  Thus, away from the already charged lifted
boundary root-slice core (BZ0), the external anchor over a shadow and slope is
unique and recovered from the lifted Hankel triple.  The residual one-outside
shadow image is therefore contained in the rank-one scalar Hankel locus

```text
c_1^2=c_0c_2,        c_0 != 0,        c_1/c_0 notin D,          (BRANK)
```

with the usual active filter `H_{2,j}(v)ell_{S,c_1/c_0} != 0`.  This is the
concrete shadow-image target left by the boundary reduction.

There is one more local simplification over each fixed shadow.  Write

```text
a_i=row_i(H_{3,j-1}(u)ell_S),        b_i=row_i(H_{3,j-1}(v)ell_S),
c_i(z)=a_i+z b_i,                    0<=i<=2.
```

Then the rank-one condition (BRANK) is cut out by the quadratic slope
polynomial

```text
Q_S(z)=c_1(z)^2-c_0(z)c_2(z).
```

If `Q_S` is not the zero polynomial, then at most two finite slopes over the
shadow can pass the recovered-anchor gate, and each such slope has the unique
anchor `beta(z)=c_1(z)/c_0(z)`.

It remains to understand the degenerate case `Q_S=0` as a polynomial in `z`.
The affine line

```text
z |-> (c_0(z),c_1(z),c_2(z)) = a+z b
```

then lies on the rank-one cone `x_1^2=x_0x_2`.  This forces `a` and `b` to lie
on one cone generator.  Indeed, the coefficient identities are

```text
a_1^2=a_0a_2,        b_1^2=b_0b_2,
2a_1b_1=a_0b_2+b_0a_2.                (BCONE)
```

If `a_0=0`, then `a_1=0`; when `a_2 != 0`, the polar identity in (BCONE)
forces `b_0=0`, and then `b_1=0`, so `b` is proportional to `a`.  If
`a_0 != 0`, write `alpha=a_1/a_0`, so `a_2=alpha^2 a_0`.  When `b_0=0`,
(BCONE) gives `b=0`.  When `b_0 != 0`, writing `gamma=b_1/b_0`, the polar
identity becomes `(alpha-gamma)^2=0`, hence `alpha=gamma`, again making `b`
proportional to `a`.  The same computation is valid in characteristic two.

Thus an identically-zero gate has either no recovered finite anchor
(`c_0=c_1=0`, the point at infinity), or a single fixed recovered anchor
`beta` for every nonzero point of the line.  In the latter case

```text
H_{2,j}(u)ell_{S,beta}=0,        H_{2,j}(v)ell_{S,beta}=0,
```

so the active filter `H_{2,j}(v)ell_{S,beta} != 0` removes the branch.  The
zero triples themselves are the already charged lifted boundary root-slice
core (BZ0).  Therefore every active residual boundary shadow that survives this
local reduction is governed by a nonzero quadratic slope gate.  The remaining
boundary task is to bound shadows for which this explicit nonzero quadratic has
an outside-domain active recovered root.

Equivalently, the same obstruction has a conic-secant form in the external
anchor coordinate.  For `beta in F`, put

```text
r_beta=(1,beta,beta^2),
h_beta(c)=(c_1-beta c_0, c_2-beta c_1).
```

Define the anchor gate

```text
A_S(beta)=det(a,b,r_beta)
         =(a_1b_2-a_2b_1)
          +(a_2b_0-a_0b_2) beta
          +(a_0b_1-a_1b_0) beta^2.                 (BANCH)
```

For every `beta`, this is exactly

```text
A_S(beta)=det(h_beta(a),h_beta(b)).
```

Thus, if `h_beta(b) != 0`, there is a unique finite slope `z` with

```text
h_beta(a+z b)=0
```

if and only if `A_S(beta)=0`; the slope is recovered from any nonzero
coordinate of `h_beta(b)`.  If the resulting triple `a+z b` is nonzero, it is
a nonzero multiple of `r_beta`, hence it satisfies (BRANK) and has recovered
anchor `beta`.  If `a+z b=0`, the pair is the already charged lifted boundary
core (BZ0).

The degenerate anchor gate is also harmless.  If `A_S` is identically zero,
then the three displayed coefficients in (BANCH) vanish, so `a` and `b` are
linearly dependent.  A nonzero common point which is not on the cone gives no
rank-one recovered anchor; a common point on the finite cone has a fixed
anchor `beta` and then `h_beta(b)=0`, so the active filter removes it.  The
remaining proportional zero-triple point is again (BZ0).  Hence no residual
active one-outside target comes from an identically zero anchor gate.

The two gates are the same projective conic intersection in different affine
coordinates.  Their formal discriminants agree:

```text
disc_z(Q_S)=disc_beta(A_S)
 =(2a_1b_1-a_0b_2-b_0a_2)^2
   -4(a_1^2-a_0a_2)(b_1^2-b_0b_2).                 (BDISC)
```

Consequently the residual boundary-shadow image is contained in the explicit
conic-secant target

```text
{ S : A_S is nonzero and A_S(beta)=0 for some beta in F\D,
      h_beta(b) != 0, and a+z(beta)b is not the zero triple },
```

with `z(beta)` recovered from `h_beta(a)+z h_beta(b)=0`.  This is equivalent
to the nonzero slope-quadratic target above, but it puts the outside-domain
condition directly on the root of a quadratic in the external anchor.

The conic-secant target also has a one-root fiber reduction after the external
anchor is fixed.  Let `R subset D` have size `j-2`, let `beta in F\D`, and set

```text
P_{R,beta}=(X-beta)ell_R.
```

For `y in D\R`, the one-outside locator is

```text
ell_{R,beta,y}=(X-y)P_{R,beta}.
```

Put

```text
a_y=H_{2,j}(u)ell_{R,beta,y},        b_y=H_{2,j}(v)ell_{R,beta,y}.
```

As before, `a_y` and `b_y` are affine-linear in `y`, and the active finite
slope condition is

```text
b_y != 0,        det(a_y,b_y)=0.                  (BETADET)
```

The determinant `Delta_{R,beta}(y)=det(a_y,b_y)` is a quadratic polynomial in
`y`.  If it is nonzero, then at most two domain anchors `y` over the fixed
boundary core `(R,beta)` can pass (BETADET).  If it is identically zero, the
same Hankel ruled-core collapse applies with `P_{R,beta}` in place of the
all-domain core: the branch is inactive, or it has one fixed finite slope
`z_0`.  In the fixed-slope case two distinct domain anchors give, by
subtraction,

```text
H_{3,j-1}(u+z_0v)P_{R,beta}=0,                    (BETA-LIFT)
```

so the branch is a one-outside lifted boundary-core root slice.  After these
fixed-slope boundary-core slices are charged, each `(R,beta)` supports at most
two residual domain extensions.  Moreover two residual extensions over the
same `(R,beta)` cannot have the same finite slope, because the same subtraction
would again give (BETA-LIFT).

Thus the conic-secant boundary image can be pushed one level lower: after the
one-outside lifted boundary-core charges, projection

```text
(R union {y}, beta) |-> (R,beta)
```

has residual fibers of size at most two.  Equivalently, for `j>=2`, if
`Core_off^res` is the image of all `(j-2)`-domain cores together with their
external anchor, then the residual one-outside target image satisfies the
incidence bound

```text
(j-1)|Boundary_off^res| <= 2 |Core_off^res|.        (BOCORE)
```

This still does not bound the boundary-core image itself; it identifies the
next lower-dimensional object that must be controlled or charged.

There is a fixed-core graph form which combines the two boundary fiber
reductions.  Fix `R subset D` with `|R|=j-2`, and let `G_R` be the residual
one-outside boundary graph whose left vertices are external anchors `beta` and
whose right vertices are domain anchors `y in D\R`; put an edge

```text
beta -- y
```

when `R union {y,beta}` is a residual active one-outside target.  After the
fixed-slope boundary root slices and the one-outside lifted boundary-core root
slices have both been charged, every vertex of `G_R` has degree at most two.

Indeed, fixing `y` is the boundary-shadow fiber result for the shadow
`S=R union {y}`: at most two external anchors remain, and their finite slopes
are distinct.  Fixing `beta` is the fixed-anchor boundary-core fiber result
above: at most two domain anchors remain, again with distinct finite slopes.
Thus `G_R` is a graph of maximum degree two on both sides.

Let `Core_off^res(R)` be the left vertex image and let
`E_off^res(R)` be the edge set.  Since every left vertex is incident to an
edge,

```text
|Core_off^res(R)| <= |E_off^res(R)| <= 2 |D\R| = 2(n-j+2).       (RCORE)
```

Equivalently, if `Root_off^res` is the image of `(j-2)`-domain cores `R` that
support at least one residual boundary-core vertex, then

```text
|Core_off^res| <= 2(n-j+2) |Root_off^res|.          (ROOTCORE)
```

This is not yet a global M1 bound, because the active core image
`Root_off^res` still has to be charged or bounded.  It does, however, remove
uncontrolled external-anchor multiplicity over each fixed core and isolates the
next object as a domain-core image.

Finally, the fixed-core graph is cut out by one explicit bidegree-two
determinant.  For a fixed `(j-2)`-core `R`, set

```text
U_m=H_{2,j}(u)(X^m ell_R),        V_m=H_{2,j}(v)(X^m ell_R),     0<=m<=2.
```

For roots `beta,y` put

```text
C_R(beta,y)
  = U_2-(beta+y)U_1+beta y U_0,
D_R(beta,y)
  = V_2-(beta+y)V_1+beta y V_0.
```

Then

```text
C_R(beta,y)=H_{2,j}(u)((X-beta)(X-y)ell_R),
D_R(beta,y)=H_{2,j}(v)((X-beta)(X-y)ell_R).
```

The fixed-core boundary determinant is therefore

```text
Delta_R(beta,y)=det(C_R(beta,y),D_R(beta,y)).       (BIDET)
```

It is symmetric in `beta,y` and has bidegree at most `(2,2)`.  Its vertical
specialization `Delta_R(beta, -)` is the fixed-anchor quadratic
`Delta_{R,beta}(y)` above; its horizontal specialization `Delta_R(-,y)` is the
boundary-shadow quadratic for `S=R union {y}`.  Thus the two fiber reductions
are exactly the statement that all residual vertical and horizontal fibers of
the bidegree `(2,2)` curve (BIDET) have size at most two after the corresponding
root-slice charges.

The residual fixed-core target can consequently be stated as

```text
beta in F\D,        y in D\R,
Delta_R(beta,y)=0, D_R(beta,y) != 0,
```

with the finite slope recovered from `C_R(beta,y)+zD_R(beta,y)=0`, after
charged zero triples and fixed-slope vertical/horizontal fibers have been
removed.  This bidegree form is the precise low-dimensional incidence object
left by the one-outside boundary reductions.

This determinant is not a new plane object.  It is exactly the pullback of the
ordinary two-root elementary determinant.  Define

```text
F_R(s,p)=det(U_2-sU_1+pU_0, V_2-sV_1+pV_0).
```

Then

```text
Delta_R(beta,y)=F_R(beta+y,beta y).                (PULL)
```

Thus the one-outside fixed-core incidence is the mixed-domain slice of the same
two-root determinant curve already used in the all-domain line-packet
classification.  Fixing `beta` or fixing `y` cuts this curve by the fixed-root
line

```text
p=alpha s-alpha^2,        alpha=beta or y,
```

in the elementary `(s,p)` plane.  Consequently the boundary-shadow and
fixed-anchor root-slice charges are precisely fixed-root line charges in the
same two-root determinant geometry.  After those fixed-root lines are removed,
any further positive-dimensional same-slope component of the boundary-core
incidence must be one of the already classified non-fixed line packets:
fixed-sum or nondegenerate product-Mobius, with constant-slope instances
charged to the full-plane lift.  This connects the boundary-core image to the
existing two-root line-packet ledger rather than introducing a separate
geometric species.

The same observation also removes hidden slope multiplicity from the
remaining fixed-core conic branch.  Fix a finite slope `z` and put

```text
W_m=U_m+zV_m,        0<=m<=2.
```

The same-slope equations on the elementary plane are

```text
W_2-sW_1+pW_0=0,                                  (ZFIB)
```

a pair of affine-linear equations in `(s,p)`.  Hence their common zero set is
empty, one point, an affine line, or the whole elementary plane.  If two
distinct boundary-core points over the same fixed `R` have the same finite
slope `z` and have distinct elementary coordinates `(s,p)`, then (ZFIB)
contains the affine line through them.  If that line is a fixed-root line, it
is charged by the boundary/root-slice ledger.  If it is non-fixed, the
two-root line classification makes it fixed-sum or product-Mobius, and the
constant-slope line-collapse above charges it to the full-plane lift.  If the
whole plane is killed, it is exactly the two-exchange full-plane lift.

Thus, after fixed-root, constant-slope non-fixed line-packet, and full-plane
charges have been removed, the finite-slope label is injective on the live
boundary-core conic points for each fixed `R`.  Counting live boundary-core
slopes is therefore the same as counting live points of the quartic anchor
gate below, up to the already charged branches and the filters which only
remove points.

For such a surviving line packet the mixed boundary-core trace is explicit:
fixed-sum packets contribute only pairs `beta=s_0-y`, while product-Mobius
packets contribute only pairs `beta=c+mu/(y-c)`.  Hence, over a fixed core
`R`, a non-fixed line packet contributes at most `n-j+2` one-outside
boundary-core pairs, exactly the escaped-root trace of its packet involution.

The complementary conic case has an equally explicit anchor gate.  Write the
ordinary elementary determinant as

```text
F_R(s,p)=f_20 s^2+f_11 sp+f_02 p^2+f_10 s+f_01 p+f_00.
```

For a fixed domain root `y`, the external-anchor equation is the quadratic

```text
F_R(beta+y,beta y)
 = A_R(y) beta^2+B_R(y) beta+C_R(y),              (BQ)
```

where

```text
A_R(y)=f_20+f_11 y+f_02 y^2,
B_R(y)=f_10+(2f_20+f_01)y+f_11 y^2,
C_R(y)=f_00+f_10 y+f_20 y^2.
```

Thus in odd characteristic the unfiltered number of external-anchor solutions
over `y` is governed by the quartic discriminant

```text
Disc_R(y)=B_R(y)^2-4A_R(y)C_R(y).                (BDISC)
```

If `A_R(y) != 0`, the number of anchor roots in the ambient field is
`1+chi(Disc_R(y))`, with `chi(0)=0`.  If `A_R(y)=0` but `B_R(y) != 0`, there
is one anchor root; if `A_R(y)=B_R(y)=0` and `C_R(y) != 0`, there are none.
The remaining case `A_R(y)=B_R(y)=C_R(y)=0` means that `F_R` vanishes on the
fixed-root line `p=y s-y^2`, so that fixed-root component is charged by the
root-slice ledger.  The outside-domain, distinct-root, and active filters only
remove roots from this count.  Consequently the uncharged boundary-core conic
target is a concrete quartic Kummer/discriminant trace over `D\R`, rather than
a separate bidegree-incidence problem.

The identically-zero discriminant case is not a new residual branch.  In odd
characteristic, if `Disc_R(y)` is the zero polynomial, then the elementary
conic is one of the following two types:

```text
F_R(s,p)=lambda L(s,p)^2
```

for an affine line `L`, or

```text
F_R(s,p)=lambda(s^2-4p).                         (ENV)
```

This follows by comparing the five coefficients of `Disc_R(y)` with zero.
The first case is already the affine line-packet branch: by the two-root line
classification, `L=0` is fixed-sum, fixed-root, or nondegenerate
product-Mobius.  The second case restricts to

```text
F_R(beta+y,beta y)=lambda(beta-y)^2,
```

so its mixed boundary roots have `beta=y`; these are removed by the
outside-domain/distinct-root filters.  Hence after line-packet and fixed-root
charges, the live conic boundary-core target has a nonzero quartic
discriminant.

This live target has bounded geometry.  If `A_R` is identically zero, then
`F_R` is affine-linear in `(s,p)` and belongs to the line-packet branch already
classified.  Otherwise `A_R` has at most two roots.  Away from those roots,
the quadratic formula gives a bijection between ambient anchor roots and the
double cover

```text
W_R^2=Disc_R(y).                                  (BCOV)
```

The maps are

```text
W_R=2A_R(y)beta+B_R(y),
beta=(-B_R(y)+W_R)/(2A_R(y)).
```

After replacing `Disc_R` by its squarefree part, the normalization of (BCOV)
has genus at most one, because `deg Disc_R<=4`.  The omitted roots of `A_R`
give at most two linear fibers, hence only `O(1)` exceptional anchors before
the outside-domain and active filters.  Therefore the residual non-line
boundary-core problem is a uniformly bounded genus-zero/genus-one Kummer
trace, not a family whose conductor grows with the Hankel depth or with the
core.

The full multiplicative-subgroup version has an exact Kummer nontriviality
gate.  Assume now that the ambient field is `F_p`, `p` odd, and that
`D <= F_p^*` has index `e`.  Let `chi` be a character of order `e` with
kernel `D`, and extend characters by zero.  For a fixed live core, ignore the
already charged fixed-root fibers and the at most two `A_R(y)=0` exceptional
linear fibers.  The unfiltered full-subgroup anchor count satisfies

```text
N_R(D) = |D| + (1/e) sum_{a=0}^{e-1} S_a + O(1),
S_a    = sum_{y in F_p^*} chi^a(y) chi_2(Disc_R(y)).       (KEXP)
```

The actual boundary-core target over `D\R`, with outside-domain and active
filters imposed, is bounded above by this full-subgroup count because those
conditions only delete candidate points.

Let `ell=lcm(e,2)`, and choose a character `omega` of order `ell` with
`chi=omega^{ell/e}` and `chi_2=omega^{ell/2}`.  Then

```text
S_a = sum_{y in F_p^*} omega(y^{a ell/e} Disc_R(y)^{ell/2}).   (KCOMB)
```

Thus the only way this full-subgroup Kummer term can be geometrically
trivial is the explicit power-divisor gate

```text
div(y^{a ell/e} Disc_R(y)^{ell/2}) == 0 mod ell.              (KPOW)
```

Equivalently, every nonzero finite root of `Disc_R` has even multiplicity,
and

```text
a ell/e + (ell/2) ord_0(Disc_R) == 0 mod ell.
```

The condition at infinity then follows from degree zero of the divisor.  Thus
the squarefree part of a no-cancellation quartic is forced to be monomial:

```text
Disc_R(y)=c G(y)^2
```

or

```text
Disc_R(y)=c y G(y)^2.                             (KMON)
```

The character label is forced as well.  In the first case `a=0`.  In the
second case `e` must be even and `a=e/2`.  Therefore no other subgroup
Fourier term can be geometrically trivial.  If (KPOW) fails, the rational
function in (KCOMB) is not an `ell`-th power over `\overline{F}_p(y)`.  The
standard one-dimensional Kummer-Weil bound on `P^1` then gives

```text
|S_a| <= (R_a-2) sqrt(p) <= 4 sqrt(p),
```

because the zero-pole support is contained in `y=0`, `y=infinity`, and the
at most four geometric roots of `Disc_R`.  Hence every non-power term has
depth-independent conductor.  Failure of cancellation is not hidden in the
quartic cover; it is exactly the monomial-square discriminant gate (KPOW),
which is now a concrete algebraic branch to charge or exclude.

In that branch the cover is explicitly genus zero.  If
`Disc_R=cG^2`, then either `c` is a nonsquare and there are no nonsingular
ambient anchor roots, or `c=d^2` and the two sheets are

```text
W_R=+-dG(y),
beta=(-B_R(y)+-dG(y))/(2A_R(y)).
```

If `Disc_R=c y G^2`, then the cover is pulled back from the fixed square-root
cover `t^2=c y`; after adjoining `t`, the sheets are

```text
W_R=+-t G(y),
beta=(-B_R(y)+-t G(y))/(2A_R(y)).
```

Thus the entire no-cancellation locus is a rational graph or a fixed
square-root rational graph, plus the already isolated `A_R=0` exceptions.
It is not an additional high-conductor Kummer family.

Consequently the full-subgroup quartic branch has a closed per-core bound.
Let `N_R^{live}(D)` denote the live non-line fixed-core boundary points with
`y in D`, after fixed-root lines, non-fixed constant-slope lines, full-plane
lifts, and the at most two `A_R=0` exceptional fibers have been removed.  The
standard `P^1` Kummer input gives

```text
N_R^{live}(D) <= |D| + 4 sqrt(p) + O(1)       if (KPOW) never occurs,
N_R^{live}(D) <= 2|D| + 4 sqrt(p) + O(1)      in general.      (KBD)
```

Indeed, the character expansion (KEXP) has the principal term `|D|`.  By
(KMON), at most one Fourier term can be geometrically trivial: either the
principal term for `Disc_R=cG^2`, or the quadratic subgroup term `a=e/2` for
`Disc_R=c y G^2`.  That single term contributes at most another `|D|+O(1)`.
All remaining terms are bounded by `4 sqrt(p)`, and the prefactor `1/e` in
(KEXP) keeps their total contribution below `4 sqrt(p)`.  The deleted
outside-domain, distinct-root, and active filters only reduce the count, and
the previous same-slope fiber injection turns this point bound into the same
bound for live boundary-core slopes over the fixed core.

For substitution into the boundary-core ledger, combine this with the
degree-two graph bound (RCORE).  The live non-line conic branch over a fixed
core satisfies

```text
N_R^{conic}(D)
 <= min(2(n-j+2), |D|+4 sqrt(p)+O(1))       if (KPOW) never occurs,
N_R^{conic}(D)
 <= min(2(n-j+2), 2|D|+4 sqrt(p)+O(1))      in general.        (KROOT)
```

The reducible line-packet branch is still handled by the fixed-sum/product-
Mobius graph ledger above.  Hence the only remaining global boundary-core
input is the size of the active `(j-2)` root-core image; the fixed-core
conic geometry itself no longer supplies an uncontrolled multiplicity or
depth-dependent conductor.

There is also a slope-side form of the same fixed-core target.  For
`0<=i<=3`, write

```text
a_i=row_i(H_{4,j-2}(u)ell_R),        b_i=row_i(H_{4,j-2}(v)ell_R),
c_i(z)=a_i+z b_i.
```

For a finite slope `z`, a formal monic two-root factor
`P(X)=X^2-sX+p` satisfies

```text
H_{2,j}(u+zv)(P ell_R)=0
```

if and only if

```text
c_2-sc_1+pc_0=0,        c_3-sc_2+pc_1=0.          (REC)
```

Put

```text
Q_R(z)=c_0c_2-c_1^2.
```

If `Q_R(z) != 0`, the recurrence coefficients are unique:

```text
s_R(z)=(c_0c_3-c_1c_2)/Q_R(z),
p_R(z)=(c_1c_3-c_2^2)/Q_R(z).                    (SREC)
```

The split-root condition is therefore controlled by the quartic numerator

```text
Theta_R(z)
 =(c_0c_3-c_1c_2)^2
  -4(c_0c_2-c_1^2)(c_1c_3-c_2^2),                (ZDISC)
```

since `s_R(z)^2-4p_R(z)=Theta_R(z)/Q_R(z)^2`.  Thus, outside charged
exceptional slopes, the root-core target is a one-variable quartic split test
in the slope `z`, followed by the filters requiring one recovered root in
`D\R`, the other outside `D`, and `H_{2,j}(v)(P ell_R) != 0`.

The denominator-zero solvable case is already charged.  If `Q_R(z)=0` and
(REC) has a solution, then either all four `c_i(z)` vanish, giving the
full-plane lift `H_{4,j-2}(u+zv)ell_R=0`, or there is a scalar `alpha` with

```text
c_i(z)=c_0(z) alpha^i,        0<=i<=3,
```

and every solution `P` of (REC) satisfies `P(alpha)=0`.  Hence the solution
set is a fixed-root line in the elementary `(s,p)` plane, which is already in
the fixed-root/root-slice ledger.  The residual non-line root-core target
therefore lives in the `Q_R(z) != 0` recurrence chart.

This chart is a bounded cover of the slope line, not a growing-depth source.
Let

```text
A_R(z)=c_0c_3-c_1c_2,        B_R(z)=c_1c_3-c_2^2,
Theta_R(z)=A_R(z)^2-4Q_R(z)B_R(z).
```

Since every `c_i(z)` is linear in `z`, the three polynomials `Q_R,A_R,B_R`
have degree at most two, and `Theta_R` has degree at most four.  On
`Q_R(z) != 0`, a split ordered lift with roots `r_1,r_2` gives

```text
y=Q_R(z)(r_1-r_2),        y^2=Theta_R(z),
```

and conversely a point `(z,y)` on `Y^2=Theta_R(z)` gives the formal roots

```text
r_1,r_2=(s_R(z) +/- y/Q_R(z))/2.
```

Thus, after the denominator-zero fixed-root/full-plane cases have been
charged, residual split root-core slopes are filtered points on the cover

```text
C_R:        Y^2=Theta_R(z).
```

After squarefree reduction this cover has genus at most one.  If `Theta_R`
is a square, the roots are rational functions of `z`; otherwise the usual
Kummer-Weil estimate on `P^1` has conductor bounded by the four finite branch
points and infinity, independent of `j`, depth, or the ambient domain.  The
requirements that one root lie in `D\R`, the other outside `D`, and the
extension be active are deleting filters on this bounded-cover chart.

The domain/outside filter also has bounded conductor.  Assume here that `D`
is the index-`e` multiplicative subgroup of `F_p^*`, with quotient character
`chi` of order `e` and kernel `D`, and extend all multiplicative characters
by `0` at the origin.  On the cover `C_R`, away from the denominator divisor
`Q_R=0`, put

```text
r_+(z,Y)=(A_R(z)+Y)/(2Q_R(z)),
r_-(z,Y)=(A_R(z)-Y)/(2Q_R(z)).
```

The ordered cover point `(z,Y)` has the plus-root in `D` and the minus-root
outside `D` exactly when

```text
1_D(r_+) (1-1_D(r_-)) = 1,
```

where

```text
1_D(x)= e^{-1} sum_{a=0}^{e-1} chi^a(x).          (RKEXP)
```

Thus the filtered root-core count is an explicit finite sum of Kummer traces
on the genus-at-most-one curve `C_R`:

```text
sum_{(z,Y) in C_R, Q_R(z) != 0}
  chi^a(r_+(z,Y)) chi^b(r_-(z,Y)).
```

The zero-pole support of each `r_+` or `r_-` is bounded independently of
`j` and of the recursion depth.  Finite poles lie over the at-most-two roots
of `Q_R`; finite zeros lie over the at-most-two roots of `B_R`, since
`r_+=0` or `r_-=0` implies `Y=+-A_R` and hence `Q_RB_R=0`.  The remaining
support is at infinity, and the cover itself has at most four finite branch
points.  Consequently every non-geometrically-trivial summand in (RKEXP) has
standard Kummer-Weil size `O_e(sqrt p)` with an absolute conductor constant
for fixed subgroup index `e`.  The only no-cancellation cases are the explicit
power-divisor congruences for products

```text
r_+^a r_-^b
```

on this bounded divisor support.  Hence the domain/outside filter introduces
no multiplicative depth loss: it leaves a finite list of bounded-degree power
branches plus bounded-conductor genus-zero/genus-one character sums.

This gives a per-core mixed-domain ledger whenever those power branches are
absent.  First remove the fixed-zero-root case: if `B_R` is identically zero,
then on `Q_R(z) != 0` one has `p_R(z)=0`, so every formal two-root extension
has root `0`.  This is the fixed-root line `p=0` in the elementary plane and
is already charged by the fixed-root/root-slice ledger.  Hence in the residual
mixed-domain branch we may assume `B_R` is nonzero; then the points with
`r_+=0` or `r_-=0` lie over the at-most-two roots of `B_R` and contribute only
`O(1)` exceptional cover points.

Let `C_R^x` be the open cover points with `Q_R != 0` and
`r_+ r_- != 0`.  Put

```text
N_R(z)=B_R(z)/Q_R(z)=r_+(z,Y)r_-(z,Y).
```

Then the outside-domain condition can be moved to the slope line:

```text
1_D(r_+) (1-1_D(r_-)) = 1_D(r_+) (1-1_D(N_R(z))).        (RKNORM)
```

Indeed, on `C_R^x` the quotient `r_-=N_R/r_+`; if `r_+ in D`, then
`r_- in D` is equivalent to `N_R in D`.  Thus slopes with `N_R(z) in D`
contribute no mixed ordered points at all, and slopes with `N_R(z) notin D`
contribute exactly the plus-sheet points whose plus-root lies in `D`.  This is
the clean separation used below: the outside-root filter is a slope-line norm
filter, while the remaining cover-level condition is only `r_+ in D`.

Equivalently, the character expansion can be reindexed as

```text
N_R^{+,-}(D)
 = e^{-1} sum_a sum_{C_R^x} chi^a(r_+) (1-1_D(N_R(z))) + O(1)

 = e^{-1} sum_a S_a^+
   - e^{-2} sum_{a,b} sum_{C_R^x} chi^a(r_+) chi^b(N_R(z))
   + O(1).                                           (RKNORMEXP)
```

The second line is the same as (RKCOUNT) after the change of variables
`S_{a+b,b}=sum chi^a(r_+)chi^b(N_R)`, but it makes the analytic roles
separate: the outside filter is a bounded-support `P^1` character of
`B_R/Q_R`, and only the `r_+` factor remains on the cover.

It also gives a genus-free fallback bound.  For a fixed slope with
`Q_R(z)B_R(z) != 0`, the two sheets have root product `N_R(z)`.  If
`N_R(z) in D`, then either both roots lie in `D` or neither root lies in `D`,
so the mixed condition contributes nothing.  If `N_R(z) notin D`, at most one
of the two roots can lie in `D`, since two domain roots would have product in
`D`.  Hence the mixed ordered cover points inject into the norm-outside slope
set

```text
{ z : Q_R(z)B_R(z) != 0,  N_R(z) notin D }.              (RKNINJ)
```

That slope set has the exact `P^1` expansion

```text
Z_R^{norm-out}
 = sum_{Q_RB_R != 0} (1-1_D(B_R/Q_R))

 = (1-1/e) #{z:Q_RB_R != 0}
   - e^{-1} sum_{a=1}^{e-1} sum_{Q_RB_R != 0} chi^a(B_R/Q_R).  (RKNOUT)
```

Every nonprincipal term in (RKNOUT) has zero-pole support contained in the
roots of `B_R`, `Q_R`, and infinity.  Thus, unless `B_R/Q_R` is a quotient
character power, the standard `P^1` Kummer bound gives

```text
N_R^{+,-}(D) <= Z_R^{norm-out}
 <= (e-1)|D| + C_e sqrt(p) + O_e(1).                 (RKNOUTBD)
```

The exceptional norm-power branch is explicit because `B_R` and `Q_R` have
degree at most two.  For a nonprincipal quotient character `chi^a`, put
`m=e/gcd(e,a)`.  The `P^1` term `chi^a(B_R/Q_R)` is geometrically trivial
only when

```text
div(B_R/Q_R) == 0 mod m.                             (RKNPOW)
```

If `m>=3`, all finite and infinite valuations of the degree-two rational
function have absolute value at most two, so (RKNPOW) forces every valuation to
be zero.  Thus `B_R/Q_R` is constant.  If `m=2`, (RKNPOW) says exactly that
the reduced rational function `B_R/Q_R` is a square up to scalar.  Consequently:

```text
nonquadratic norm-power branch  =>  B_R/Q_R constant,
quadratic norm-power branch     =>  B_R/Q_R square up to scalar.       (RKNP)
```

For odd index `e`, the only nonprincipal norm-power exception is therefore
constant norm.  For even `e`, the only additional nonconstant exception is the
quadratic square-norm branch.  These are slope-line algebraic branches, not
new cover-level conductor sources.

The constant-norm branch is already part of the line-packet ledger.  If
`B_R/Q_R=gamma` on the open slope line, then the recovered elementary
coefficient satisfies

```text
p_R(z)=gamma.
```

Thus every live formal two-root extension lies on the elementary line
`p=gamma`.  For `gamma=0` this is the fixed-root line already charged by the
root-slice ledger.  For `gamma!=0` it is the product-Mobius packet

```text
x y = gamma,                                           (RKCONST)
```

namely the center-zero case of `(x-c)(y-c)=mu`.  Therefore the nonquadratic
norm-power exception introduces no new root-core geometry: it returns to the
existing non-fixed line-packet ledger after the fixed-root case is removed.

The remaining square-norm branch has only one possible large norm-filter
coefficient.  Suppose `e` is even and the reduced nonconstant norm has the
form

```text
B_R/Q_R = gamma M(z)^2
```

as a divisor on `P^1`.  Then in (RKNOUT) all nonprincipal terms are
bounded-support `P^1` Kummer sums except the quadratic quotient character
`chi^{e/2}`.  On the open set `Q_RB_RM != 0`,

```text
chi^{e/2}(B_R/Q_R)=chi^{e/2}(gamma)=epsilon in {+1,-1}.
```

Consequently

```text
Z_R^{norm-out}
 = ((e-1-epsilon)/e) #{z:Q_RB_R != 0}
   + O_e(sqrt(p)) + O_e(1).                         (RKSQOUT)
```

If `epsilon=+1`, the quadratic part of the norm filter saves an additional
`|D|` worth of slopes:

```text
epsilon=+1  =>  N_R^{+,-}(D)
 <= (e-2)|D| + C_e sqrt(p) + O_e(1).                (RKSQ+)
```

This positive-parity square-norm branch is also explicit slope-line geometry.
Write `N_R=gamma M^2` with `M` reduced.  Then `N_R(z) in D` is

```text
chi(M(z))^2 = chi(gamma)^{-1}.                      (RKSQPARAM)
```

Because `chi^{e/2}(gamma)=+1`, the right side lies in the square subgroup of
the quotient group and (RKSQPARAM) cuts out exactly two quotient-character
classes of the degree-one parameter `M`.  The norm-outside slopes are the
remaining `e-2` classes.  Thus (RKSQ+) is not merely an estimate: after
deleting zeros, poles, and charged constant-norm cases, it is the
`(e-2)`-coset rational square-map packet on the slope line.

For `e=2` this gives no main term, in agreement with the index-two
sheet-symmetry closure below.  If `epsilon=-1`, the norm filter alone gives
the full slope-line main term

```text
epsilon=-1  =>  Z_R^{norm-out}
 <= e|D| + C_e sqrt(p) + O_e(1),                    (RKSQ-)
```

so the negative-parity square-norm case is the only surviving slope-line
square-norm obstruction and must be handled by the cover-level `r_+` sums or
by a further algebraic charge.

In fact the negative-parity branch removes all pair terms.  Since
`chi^{e/2}(N_R)=-1`, the norm can never lie in `D` on the open slope line.
Thus `1_D(N_R)=0` there, and (RKNORMEXP) collapses to

```text
N_R^{+,-}(D)
 = e^{-1}|C_R^x| + e^{-1} sum_{a=1}^{e-1} S_a^+ + O(1).       (RKSQNEG)
```

For a one-root term `S_a^+`, norm pushforward gives the necessary condition
`div(N_R^a)==0 mod e`.  In the negative square-norm branch this can occur only
for `a=e/2`; all other nonprincipal one-root terms are nontrivial
bounded-conductor cover sums.  Hence the only remaining no-cancellation term
is the explicit quadratic one-root square branch

```text
r_+ is a square in k(C_R)^*.                              (RKSQROOT)
```

Moreover `deg(r_+)<=2`, because its finite zeros project into the at-most-two
roots of `B_R`.  If `r_+` is a nonconstant square, its square root has degree
one, so the normalized cover is rational.  If `r_+` is constant, this is a
fixed-root branch.  Therefore the negative-parity square-norm branch has no
genuine cover-level power term on genus-one root-core covers after fixed-root
charging; its genus-one bound is

```text
N_R^{+,-}(D) <= |D| + C_e sqrt(p) + O_e(1).              (RKSQGENUS)
```

On the rational one-root-square branch, there is one final sign.  If
`r_+=alpha H^2`, put `delta=chi^{e/2}(alpha)`.  The large part of
`S_{e/2}^+` is `delta |C_R^x|`, and it enters (RKSQNEG) with the positive
coefficient `e^{-1}`.  Hence

```text
delta=-1  =>  N_R^{+,-}(D) <= C_e sqrt(p) + O_e(1),
delta=+1  =>  N_R^{+,-}(D) <= 2|D| + C_e sqrt(p) + O_e(1).  (RKSQROOTSGN)
```

The positive-sign case has a concrete normal form.  Because the square-root
`H` has degree one, use `h=H` as a rational parameter on the normalized cover.
Then

```text
r_+(h)=alpha h^2,        chi^{e/2}(alpha)=+1.
```

The condition `r_+(h) in D` is

```text
chi(h)^2 = chi(alpha)^{-1}.                         (RKSQPARAM)
```

Since the right side has trivial quadratic quotient character, this equation
has exactly two quotient-character classes of `h`.  Thus the positive
one-root-square branch is precisely a two-coset rational square-map packet,
with `2|D|+O_e(1)` points after deleting zeros, poles, and charged fixed-root
fibers.  This identifies the last large square-norm subbranch as explicit
coset geometry in a degree-one parameter, not an uncontrolled Kummer failure.

These square-map packets have a clean overlap gate.  Let `M_1,M_2` be
nonconstant degree-one rational functions on the slope line, and let `chi`
have order `e`.  If

```text
sum_z chi^a(M_1(z)) chi^b(M_2(z))
```

has a geometrically trivial Kummer summand with `0<a,b<e`, then exactly one of
the following quotient-Mobius relations holds:

```text
M_2 = lambda M_1       and       a+b == 0 mod e,
M_2 = lambda/M_1       and       a-b == 0 mod e.        (RKSQINT)
```

Indeed, a degree-one rational function has one zero and one pole on `P^1`.
If the divisor of `M_1^a M_2^b` is divisible by `e`, then any zero or pole
belonging to only one of the two functions would carry valuation `+-a` or
`+-b`, impossible modulo `e`.  Hence the two zero-pole supports coincide.
If the orientations agree then `M_2/M_1` is constant and divisibility requires
`a+b==0`; if the orientations are reversed then `M_1M_2` is constant and
divisibility requires `a-b==0`.

Consequently, two quotient-class packets pulled back by degree-one parameters
have only the expected product-density intersection, up to `O_e(sqrt p)`,
unless their parameters are quotient-parallel or quotient-inverse as in
(RKSQINT).  For two square-map packets this gives

```text
|P(M_1,kappa_1) cap P(M_2,kappa_2)|
  = 4e^{-2} p + O_e(sqrt p)
```

off the parallel/inverse relations, where
`P(M,kappa)={z: chi(M(z))^2=kappa}` with zeros and poles deleted.  On the
parallel or inverse relations the intersection is again a single explicit
quotient-class packet in one degree-one parameter; in particular a two-coset
square-map packet intersects any parallel/inverse two-coset square-map packet
in at most `2|D|+O_e(1)` slopes.  Thus the square-norm and one-root-square
branches create structured slope-coset packets whose large overlaps are
exactly the quotient-parallel/inverse cases, not hidden high-energy Kummer
families.

The same gate gives a finite palette for each high-overlap class.  A
quotient-parallel or quotient-inverse relation is exactly equality of the
unordered zero-pole support

```text
Pi(M)={zero(M), pole(M)} subset P^1.
```

Fix such a support `Pi={alpha,beta}` and choose one parameter `M_Pi` with
`div(M_Pi)=alpha-beta`.  Every other degree-one parameter with support `Pi`
is either `lambda M_Pi` or `lambda/M_Pi`.  Therefore its square-map packet

```text
{ z : chi(M(z))^2 = kappa }
```

is one of the packets

```text
P_Pi(theta)={ z : chi(M_Pi(z))^2 = theta },
        theta in (Z/eZ)^2.                           (RKSQPAL)
```

There are exactly `e/2` such packets, they are disjoint on
`P^1\Pi`, and they partition `P^1\Pi`.  Thus a whole quotient-parallel/inverse
high-overlap component contributes at most `e/2` distinct square-map slope
sets; any further occurrences are duplicate multiplicity of this finite
palette, not new slope growth.  Equivalently, the global square-map branch can
be summed by first bounding the image of zero-pole supports `Pi`, then paying
only an `O_e(1)` palette factor per support.

For the square-norm branch this support is not an additional parameter.  If
the reduced norm satisfies

```text
N_R(z)=B_R(z)/Q_R(z)=gamma M(z)^2
```

with `M` nonconstant of degree one, then

```text
div(N_R)=2 div(M).                                  (RKSQEND)
```

Thus `Pi(M)` is exactly the support of the nonzero divisor of `N_R`, with the
orientation remembered by the signs of the valuations.  Equivalently, after
removing common factors from `B_R` and `Q_R`, the numerator and denominator are
scalar multiples of squares of linear forms on `P^1`, and their two roots are
the zero and pole endpoints of the palette.  Finite zero endpoints lie among
the at-most-two roots of `B_R`; finite pole endpoints lie among the at-most-two
roots of `Q_R`, with infinity included when the degrees differ.  Hence the
square-norm packet palette is indexed by the bounded norm-boundary divisor of
the root-core recurrence chart.  Choosing a different square root of `N_R`
only rescales or inverts the degree-one parameter, so by (RKSQPAL) it does not
create new slope packets beyond the same finite support palette.

The degree-two norm also gives a sharper algebraic gate for this endpoint
image.  Replace `B_R,Q_R` by the reduced numerator and denominator
`bar B_R,bar Q_R` of `B_R/Q_R`.  Since both have degree at most two, a
nonconstant square-norm branch is equivalent to

```text
bar B_R = gamma_0 L_0^2   or   bar B_R constant,
bar Q_R = gamma_1 L_1^2   or   bar Q_R constant,
```

with at least one nonconstant factor and with the degree imbalance equal to
`0` or `+-2`.  Equivalently, every finite zero or pole of the reduced norm has
valuation `+-2`, and the point at infinity has valuation `0` or `+-2`.
Thus no simple reduced root can occur in the square-norm exception:

```text
B_R/Q_R nonconstant square
  => every finite endpoint is a repeated root of bar B_R or bar Q_R.   (RKSQREP)
```

In coefficient terms, after cancellation each nonconstant reduced quadratic
has zero discriminant, while reduced degree-one factors are forbidden.  Thus
the square-norm packet image is supported on repeated-root/discriminant-zero
norm-boundary loci, plus the two infinity cases coming from degree imbalance.
This is stronger than merely saying that endpoints are roots of `B_R` and
`Q_R`: it identifies the exceptional endpoint image as a low-codimension
algebraic locus that can be charged separately from generic norm-boundary
roots.

Equivalently, every finite endpoint has a first-derivative certificate.  Write
`bar B_R,bar Q_R` for the reduced numerator and denominator.  Since the
characteristic is odd in the root-core applications and the reduced degrees
are at most two, a finite point `z_0` is a repeated zero of the reduced norm
if and only if

```text
bar B_R(z_0)=0,        bar B_R'(z_0)=0,        bar Q_R(z_0)!=0,
```

and it is a repeated pole if and only if

```text
bar Q_R(z_0)=0,        bar Q_R'(z_0)=0,        bar B_R(z_0)!=0.       (RKSQDR)
```

Thus finite square-norm packet endpoints are not arbitrary points in the root
image of the degree-two norm boundary.  They lie in the projection of the
double-root systems `(bar B_R,bar B_R')` or `(bar Q_R,bar Q_R')`.  This is the
form needed for a global endpoint-support charge: as the active root core
varies, the exceptional support image is controlled by discriminant-zero
certificates, not by generic roots of moving quadratics.

In fact, for square-norm endpoints the reduction bars can be removed.  If a
finite endpoint survived cancellation while both `B_R` and `Q_R` vanished
there, the finite valuation of `B_R/Q_R` at that point would have absolute
value at most one, because both original multiplicities are at most two.  That
contradicts the square-norm valuation `+-2`.  Hence in a nonconstant
square-norm branch every finite zero endpoint is already a double root of the
unreduced numerator away from the denominator, and every finite pole endpoint
is already a double root of the unreduced denominator away from the numerator:

```text
zero endpoint:  B_R(z_0)=0, B_R'(z_0)=0, Q_R(z_0)!=0,
pole endpoint:  Q_R(z_0)=0, Q_R'(z_0)=0, B_R(z_0)!=0.       (RKSQRAW)
```

Thus the global endpoint-support image can be charged directly through the
raw recurrence coefficient equations `(B_R,B_R')` and `(Q_R,Q_R')`; no
separate bookkeeping of cancelled common factors is needed for finite
square-norm endpoints.

Since `B_R` and `Q_R` have degree at most two, these raw equations have a
one-scalar discriminant form.  Write

```text
B_R(z)=b_0+b_1 z+b_2 z^2,        Q_R(z)=q_0+q_1 z+q_2 z^2.
```

Then a finite zero endpoint can occur only when

```text
Delta_B=b_1^2-4 b_0 b_2=0,        B_R nonconstant,        Q_R(z_B)!=0,
```

where the repeated root is `z_B=-b_1/(2b_2)` if `b_2!=0`, and
there is no finite double root for a nonzero degree-one polynomial in odd
characteristic.  If `B_R` is identically zero, that is the fixed-zero-root
branch already charged before the residual mixed-domain ledger.  Thus the
live finite zero endpoint is the quadratic double-root slope.  The pole
endpoint has the identical certificate with `Q_R`:

```text
Delta_Q=q_1^2-4 q_0 q_2=0,        Q_R nonconstant,        B_R(z_Q)!=0.  (RKSQDISC)
```

Thus a moving square-norm endpoint-support family forces the discriminant of
one of the raw recurrence quadratics to vanish.  The endpoint slope itself is
then a rational function of the quadratic coefficients, not a free parameter.

The discriminants are explicit Hankel-minor expressions in the fixed-core row
data.  Write `c_i(z)=a_i+z b_i`.  For any adjacent triple `i,i+1,i+2`, put

```text
H_i(z)=c_i(z)c_{i+2}(z)-c_{i+1}(z)^2
     =h_{i,0}+h_{i,1}z+h_{i,2}z^2,
```

where

```text
h_{i,0}=a_i a_{i+2}-a_{i+1}^2,
h_{i,1}=a_i b_{i+2}+a_{i+2} b_i-2a_{i+1}b_{i+1},
h_{i,2}=b_i b_{i+2}-b_{i+1}^2.                  (RKSQHCOEFF)
```

Then

```text
Q_R=H_0,        B_R=H_1,
Delta_{H_i}=h_{i,1}^2-4h_{i,0}h_{i,2}.           (RKSQHDISC)
```

Thus finite square-norm pole endpoints force `Delta_{H_0}=0`, while finite
square-norm zero endpoints force `Delta_{H_1}=0`.  If `h_{i,2}!=0`, the
corresponding endpoint slope is

```text
z_i=-h_{i,1}/(2h_{i,2}).
```

The endpoint-support image is therefore controlled by the vanishing of two
explicit binary-Hankel discriminants in the active root-core row data.  This is
the form that can be fed into a global core-image charge.

There is also a rank-minor form.  Define the three row-pair minors

```text
P_i = a_i b_{i+1}-a_{i+1}b_i,
R_i = a_{i+1}b_{i+2}-a_{i+2}b_{i+1},
S_i = a_i b_{i+2}-a_{i+2}b_i.
```

Then direct expansion gives

```text
Delta_{H_i}=S_i^2-4P_iR_i.                         (RKSQPL)
```

Thus a finite square-norm endpoint forces the three adjacent Plucker minors
of the two row triples to lie on the conic `S_i^2=4P_iR_i`.  The fully
rank-one case `P_i=R_i=S_i=0` is the proportional-row degeneracy; every other
endpoint-support family must satisfy a genuine conic relation among these
three minors.  This is the minor-level form of the endpoint-support charge.

The conic has a useful chart decomposition.  On the chart `P_i!=0`, put

```text
lambda_i=S_i/(2P_i).
```

Then (RKSQPL) is equivalent to

```text
S_i=2P_i lambda_i,        R_i=P_i lambda_i^2.       (RKSQPLCH)
```

On the complementary chart `P_i=0`, the conic forces `S_i=0`.  If also
`R_i!=0`, then the two rows `(a_{i+1},b_{i+1})` and `(a_{i+2},b_{i+2})` are
independent, while `(a_i,b_i)` has zero determinant with both of them; hence
`(a_i,b_i)=(0,0)`.  Symmetrically, if `R_i=0` and `P_i!=0`, then
`(a_{i+2},b_{i+2})=(0,0)`.  Thus endpoint-support production splits into a
zero-row/fully-proportional degeneracy and the nonzero Plucker chart
(RKSQPLCH).  The latter is the only genuinely moving minor-conic case.

The nonzero chart also has a row-level recurrence form.  Write

```text
r_j=(a_j,b_j).
```

If `P_i!=0`, then `r_i,r_{i+1}` are a basis, so
`r_{i+2}=alpha r_i+beta r_{i+1}`.  The minors give

```text
beta=S_i/P_i=2lambda_i,        alpha=-R_i/P_i=-lambda_i^2.
```

Therefore the moving chart is equivalently

```text
r_{i+2}=2lambda_i r_{i+1}-lambda_i^2 r_i.          (RKSQROW)
```

On the reverse chart `R_i!=0`, with `mu_i=S_i/(2R_i)`, the same argument gives

```text
r_i=2mu_i r_{i+1}-mu_i^2 r_{i+2}.
```

Thus, after the zero-row and proportional degeneracies are charged, the
endpoint-support row triples are not a two-dimensional conic family in the
row data: they are one-parameter second-order recurrences in the adjacent
row basis.

The same chart gives a square factorization of the Hankel minor itself.  Since
`c_j(z)=a_j+z b_j` is linear in the row vector `r_j`, (RKSQROW) gives

```text
c_{i+2}=2lambda_i c_{i+1}-lambda_i^2 c_i,
```

and hence

```text
H_i=c_i c_{i+2}-c_{i+1}^2
   =-(c_{i+1}-lambda_i c_i)^2.                    (RKSQSQ)
```

On the reverse chart `R_i!=0`, the corresponding form is

```text
H_i=-(c_{i+1}-mu_i c_{i+2})^2.
```

Thus the moving endpoint condition is not merely a discriminant-zero
quadratic: after choosing a nonzero Plucker chart, its double endpoint is the
zero of an explicit row-linear form, with the constant-linear case moving the
double endpoint to infinity in the projective degree-two normalization.

Equivalently, finite endpoints are fractional-linear images of the chart
parameter.  On `P_i!=0`, if

```text
b_{i+1}-lambda_i b_i != 0,
```

then the finite double endpoint is

```text
z_i=(lambda_i a_i-a_{i+1})/(b_{i+1}-lambda_i b_i).       (RKSQZ)
```

If `b_{i+1}-lambda_i b_i=0`, then `a_{i+1}-lambda_i a_i!=0` because
`P_i!=0`, so there is no finite root of the linear factor and the double
endpoint is the point at infinity.  The reverse chart has the symmetric finite
endpoint formula

```text
z_i=(mu_i a_{i+2}-a_{i+1})/(b_{i+1}-mu_i b_{i+2}).
```

Thus, for fixed adjacent row basis, the moving endpoint image is a projective
line map in the single Plucker parameter; it is not an arbitrary quadratic
root image.

The two adjacent endpoint conditions overlap rigidly.  Suppose the Plucker
conics for `i=0` and `i=1` both hold, and suppose `P_0!=0`.  Let
`lambda_0=S_0/(2P_0)`.  Then

```text
r_2=2lambda_0 r_1-lambda_0^2 r_0,
P_1=R_0=P_0 lambda_0^2.
```

If `lambda_0=0`, then `r_2=0`; the second conic has
`P_1=R_1=S_1=0`, so `r_1,r_2,r_3` are in the proportional-row degeneracy.
If `lambda_0!=0`, then `P_1!=0`, and the second chart has
`lambda_1=S_1/(2P_1)` with

```text
r_3=2lambda_1 r_2-lambda_1^2 r_1
   =-2lambda_1 lambda_0^2 r_0
    +(4lambda_0 lambda_1-lambda_1^2) r_1.          (RKSQOV)
```

Thus simultaneous finite zero/pole endpoint production is either already in
the charged proportional-row ledger or lies in an explicit two-step
row-recurrence packet controlled by the two scalars `lambda_0,lambda_1` and
the initial adjacent row basis.

The finite-finite endpoint pair determines those two scalars.  Stay in the
nondegenerate overlapping chart `P_0!=0`, `lambda_0!=0`, and suppose the
finite endpoints of `H_0` and `H_1` are `z_0,z_1`.  Since `P_0!=0`, the
linear forms `c_0` and `c_1` have no common finite zero.  From
`c_1(z_0)-lambda_0 c_0(z_0)=0` one gets

```text
c_0(z_0)!=0,        lambda_0=c_1(z_0)/c_0(z_0).        (RKSQINV0)
```

The second endpoint satisfies

```text
(2lambda_0-lambda_1)c_1(z_1)-lambda_0^2 c_0(z_1)=0.
```

If `c_1(z_1)=0`, then `c_0(z_1)!=0`, contradicting `lambda_0!=0`; hence

```text
c_1(z_1)!=0,        lambda_1
  =2lambda_0-lambda_0^2 c_0(z_1)/c_1(z_1).          (RKSQINV1)
```

Thus, for a fixed initial row basis `r_0,r_1`, an ordered finite zero/pole
endpoint pair carries at most one nondegenerate overlapping Plucker packet.
All multiplicity in this square-norm endpoint branch must therefore come from
varying the row basis or from the already charged zero-row/proportional and
projective-infinity alternatives.

The same inversion is projective.  Write a projective slope endpoint as
`E=[Z:W]`, with affine `z=Z/W`, and put

```text
c_j(E)=a_j W+b_j Z.
```

In the nondegenerate overlapping chart, let `E_0` be the projective double
endpoint of `H_0` and `E_1` the projective double endpoint of `H_1`.  Since
`P_0!=0`, the two forms `c_0,c_1` have no common projective zero, and the
first endpoint gives

```text
c_0(E_0)!=0,        lambda_0=c_1(E_0)/c_0(E_0).    (RKSQPINV0)
```

The second endpoint satisfies

```text
(2lambda_0-lambda_1)c_1(E_1)-lambda_0^2 c_0(E_1)=0.
```

If `c_1(E_1)=0`, then `c_0(E_1)=0`, contradicting `P_0!=0`; hence

```text
c_1(E_1)!=0,        lambda_1
  =2lambda_0-lambda_0^2 c_0(E_1)/c_1(E_1).         (RKSQPINV1)
```

Thus an ordered projective endpoint pair `(E_0,E_1)` supports at most one
nondegenerate overlapping Plucker packet over a fixed initial row basis.  The
finite formulas (RKSQINV0/RKSQINV1) are the affine chart `W_0,W_1!=0`.

The diagonal projective endpoint is not a residual square-norm case.  If
`E_0=E_1=E`, then `lambda_0=c_1(E)/c_0(E)`.  Substituting this into
(RKSQPINV1) gives `lambda_1=lambda_0`.  Therefore

```text
c_2-lambda_1 c_1
  =lambda_0(c_1-lambda_0 c_0),
H_1=lambda_0^2 H_0.                               (RKSQPDIAG)
```

So the slope-line norm `H_1/H_0` is constant on the chart.  Hence a
nonconstant square-norm branch cannot have coincident projective zero and pole
endpoints in the nondegenerate overlapping Plucker chart; the diagonal
endpoint case is already charged to the constant-norm packet ledger.

Consequently, after the zero-row/proportional and constant-norm ledgers are
removed, the nondegenerate overlapping square-norm chart injects into ordered
off-diagonal projective endpoint pairs:

```text
packet |-> (E_0,E_1),        E_0 != E_1.           (RKSQOFF)
```

For a finite endpoint palette `Omega`, a fixed initial row basis therefore
supports at most `|Omega|(|Omega|-1)` nonconstant overlapping packets.  Over a
finite field `F_q` with the full projective endpoint palette, this gives the
local bound `q(q+1)` for the nonconstant nondegenerate overlapping chart.  The
remaining multiplicity is basis variation, not endpoint-pair multiplicity.

The off-diagonal projective endpoint pair also identifies the norm map.  For
`E=[Z:W]`, let

```text
L_E(z)=W z-Z
```

be the affine representative of the projective linear form vanishing at `E`
(`L_infty` is constant).  Since
`c_1-lambda_0 c_0` and `c_2-lambda_1 c_1` vanish at `E_0` and `E_1`,
respectively, there are nonzero scalars `alpha_0,alpha_1` with

```text
c_1-lambda_0 c_0=alpha_0 L_{E_0},
c_2-lambda_1 c_1=alpha_1 L_{E_1}.
```

Using the signed-square factorization (RKSQSQ),

```text
H_1/H_0 = (alpha_1/alpha_0)^2 (L_{E_1}/L_{E_0})^2.  (RKSQRAT)
```

Thus every off-diagonal nondegenerate overlapping branch is exactly a
degree-one square-map packet with divisor `2E_1-2E_0`, up to an overall square
scalar.  The residual support question for this chart is therefore a
square-map coset question over ordered endpoint pairs, not a moving quadratic
root problem.

In particular, for an even character order `e`, a fixed ordered endpoint pair
`(E_0,E_1)` has only the standard square-coset palette.  Put
`M_{E_0,E_1}=L_{E_1}/L_{E_0}`.  As the square scalar varies, the possible
slope sets are

```text
P_{E_0,E_1}(theta)
  = { z in P^1 \ {E_0,E_1} : chi(M_{E_0,E_1}(z))^2 = theta },
theta in 2Z/eZ.                                  (RKSQPAIRPAL)
```

There are at most `e/2` such sets; on the open line
`P^1 \ {E_0,E_1}` they are disjoint and partition the slopes where the
degree-one parameter is defined and nonzero.  Hence after endpoint-pair
injection, the residual nondegenerate overlapping square-norm branch pays
only the existing `O_e(1)` square-map coset palette per ordered endpoint pair.

Combining (RKSQOFF) and (RKSQPAIRPAL) gives the fixed-basis endpoint-palette
bound:

```text
# distinct nonconstant slope sets
  <= (e/2) |Omega|(|Omega|-1).                    (RKSQBASIS)
```

Here `Omega` is any projective endpoint palette containing the possible
endpoints of `H_0` and `H_1` for the fixed initial row basis, and `e` is even.
With the full projective line over `F_q`, this is at most
`(e/2) q(q+1)`.  Thus the nondegenerate overlapping square-norm chart has no
additional local slope-set growth beyond the endpoint-pair image and the
already isolated square-coset palette.

The finite endpoints themselves are not residual live mixed-domain slopes.
Let `z_0` be a finite endpoint of the reduced square norm.

If `z_0` is a zero endpoint and `Q_R(z_0) != 0`, then

```text
p_R(z_0)=B_R(z_0)/Q_R(z_0)=0.
```

Thus the recovered two-root locator lies on the fixed-root line `p=0`, so one
root is `0`; this is the fixed-root/root-slice charge already removed from
the residual ledger.  If the same zero endpoint also has `Q_R(z_0)=0`, then it
is a denominator-zero slope and falls under the denominator-zero alternative:
the recurrence is either unsolvable, or it is the full-plane lift or a
fixed-root line.

If `z_0` is a pole endpoint, then `Q_R(z_0)=0`, so it is outside the
`Q_R != 0` recurrence chart.  Again the denominator-zero alternative says that
a solvable endpoint is already charged to the full-plane or fixed-root ledger,
while an unsolvable endpoint produces no formal two-root extension.  Hence

```text
finite square-norm endpoint
  => fixed-root/full-plane charged or no live recurrence solution.     (RKSQEPCH)
```

The endpoint at infinity is the same statement in the reciprocal slope chart.
Thus the square-map packet is an open slope-line packet whose finite boundary
points are ledger charges, not additional residual aperiodic slopes.

This gives the counting form needed by the global ledger.  Let `S` be any
finite family of square-map packets

```text
P(M,kappa)={z: chi(M(z))^2=kappa}
```

with degree-one parameters `M`.  Let `Pi(S)` be the set of unordered zero-pole
supports of the parameters appearing in `S`.  Then the number of distinct
packet slope sets in `S` is at most

```text
(e/2) |Pi(S)|.                                      (RKSQCOUNT)
```

Moreover, for each nonconstant square-norm branch `B_R/Q_R=gamma M^2`, the set
`Pi(S)` has size one: it is the zero-pole support of the reduced norm divisor.
Thus repeated square roots, quotient-parallel parameters, or quotient-inverse
parameters can create multiplicity inside a fixed packet palette, but they
cannot create new slope-set growth beyond the endpoint support image.

This bound is cruder than (RKBD), but it is completely genus-free: it uses only
the slope-line norm map.  The cover-level sums below are precisely the extra
input needed to save the missing factor `e`.

Now define

```text
S_a^+    = sum_{C_R^x} chi^a(r_+),
S_{a,b}  = sum_{C_R^x} chi^a(r_+) chi^b(r_-).
```

The ordered mixed-domain count is exactly

```text
N_R^{+,-}(D)
 = e^{-1} sum_a S_a^+
   - e^{-2} sum_{a,b} S_{a,b}
   + O(1).                                             (RKCOUNT)
```

The principal contribution in (RKCOUNT) is

```text
((e-1)/e^2) |C_R^x| + O(1).
```

The norm map also filters possible cover-level power branches.  Let
`pi:C_R->P^1_z` be the slope projection and put

```text
F_{a,b}=r_+^a r_-^b.
```

If the Kummer summand `chi^a(r_+)chi^b(r_-)` is geometrically trivial on
`C_R^x`, then `div_C(F_{a,b})` is divisible by `e`.  Pushing forward by
`pi` gives the necessary slope-line condition

```text
div_{P^1}(N_R^{a+b}) == 0 mod e,       N_R=B_R/Q_R.       (RKPUSH)
```

Indeed, `Norm_{C_R/P^1}(r_+)=Norm_{C_R/P^1}(r_-)=N_R`, so
`Norm(F_{a,b})=N_R^{a+b}`.  Thus with
`m=e/gcd(e,a+b)`, the same degree-two classification applies to every
cover-level term:

```text
a+b not 0 mod e, m>=3  =>  N_R constant,
a+b not 0 mod e, m=2   =>  N_R square up to scalar.      (RKPCLASS)
```

After the constant-norm line-packet branch and the square-norm parity branch
above have been charged or isolated, every one-root term `S_a^+` with
`a!=0` and every pair term with `a+b!=0 mod e` is therefore a genuinely
nontrivial bounded-conductor Kummer sum on the cover.  The only cover-level
power branches not seen by norm pushforward are the anti-norm ratio terms

```text
a+b == 0 mod e,       chi^a(r_+/r_-).                  (RKANTI)
```

For `e=2` these are exactly the diagonal terms handled below by sheet
symmetry and descent to `P^1`.  For `e>2`, (RKANTI) is the remaining
cover-level power target in this root-core reduction.

This anti-ratio target has only one genuinely new order.  Put

```text
Phi_R=r_+/r_-=(A_R+Y)/(A_R-Y).
```

The identity

```text
(A_R+Y)(A_R-Y)=4Q_RB_R
```

shows that all finite zeros and poles of `Phi_R` project into the divisor
`Q_RB_R=0`; on the compactified degree-four double cover the numerator and
denominator have pole degree at most four.  Hence the map degree of
`Phi_R:C_R->P^1` is at most four.  Also

```text
Phi_R / N_R = 1/r_-^2,       N_R=r_+r_-=B_R/Q_R.       (RKPHIN)
```

Thus `Phi_R` and `N_R` have the same square class in the cover function
field.  Consequently:

```text
even-order anti-ratio power branch  =>  square-norm branch,
odd order m>=5 anti-ratio branch    =>  Phi_R constant,
Phi_R constant                      =>  square-norm branch.       (RKANTIRED)
```

The second implication uses `deg(Phi_R)<=4`, since a nonconstant `m`-th power
has map degree divisible by `m`.  The last implication follows from
`N_R=Phi_R r_-^2`.  Therefore, after the square-norm algebraic branch has been
isolated, the only possible nonconstant anti-ratio power branch has order
`m=3`:

```text
div_C(r_+/r_-) == 0 mod 3.                         (RKANTICUBIC)
```

In particular, if `3` does not divide the subgroup index `e`, then after the
constant-norm and square-norm branches above have been charged or isolated,
there are no cover-level power branches left in the root-core mixed-domain
expansion.

Even when `3|e`, this cubic branch is only a genuine no-cancellation branch on
the rational-cover locus.  Geometric triviality of the cubic anti-ratio
Kummer term means

```text
Phi_R = c G^3        in k(C_R)^*
```

after base change to the algebraic closure.  Since `deg(Phi_R)<=4` and
`Phi_R` is nonconstant after the square-norm branch is removed, this forces

```text
deg(Phi_R)=3,        deg(G)=1.                       (RKANTIGENUS)
```

A smooth projective curve with a degree-one map to `P^1` is rational.  Hence
on a geometrically integral genus-one normalization of `C_R`, the cubic
anti-ratio term is still geometrically nontrivial and has the usual
bounded-conductor Weil bound.  The only genuine cubic no-cancellation case is
a rational-cover algebraic branch where `Phi_R` is the cube of a degree-one
function.  Thus the nonsplit genus-one root-core cover has no cover-level
power branch left after the constant-norm and square-norm exceptions.

The rational cubic branch also has an explicit ledger.  In the anti-diagonal
sum `S_{a,-a}`, geometric triviality of `chi^a(Phi_R)` can occur only when

```text
3a == 0 mod e.
```

Thus there are no such nonprincipal coefficients unless `3|e`, and if `3|e`
there are exactly two:

```text
a=e/3,  2e/3.                                      (RKANTICOEFF)
```

All other one-root, non-anti-diagonal, and anti-diagonal coefficients are
bounded-conductor Kummer sums after the constant-norm and square-norm
exceptions above are removed.  The two large anti-diagonal constants are
conjugate cubic roots.  Writing

```text
lambda = chi^{e/3}(c),
```

the large part of `S_{e/3,-e/3}+S_{2e/3,-2e/3}` is
`(lambda+lambda^{-1})|C_R^x|`, and it enters (RKCOUNT) with the negative
coefficient `-e^{-2}`.  Since

```text
lambda+lambda^{-1} in {2,-1},
```

the worst sign adds only `e^{-2}|C_R^x|`, not `2e^{-2}|C_R^x|`.  Therefore on
the rational cubic branch

```text
N_R^{+,-}(D)
 <= ((e-1)/e^2)|C_R^x| + (1/e^2)|C_R^x|
    + C_e sqrt(p) + O_e(1)

 <= (1/e)|C_R^x| + C_e sqrt(p) + O_e(1).             (RKCUBBD)
```

For a geometrically integral rational normalization, `|C_R^x|<=p+O(1)`, so
this gives

```text
N_R^{+,-}(D) <= |D| + C_e sqrt(p) + O_e(1)
```

on the rational cubic anti-ratio branch.  This is weaker than the generic
cover saving but is still a proportional per-core bound and leaves only an
explicit algebraic rational-cover branch, not an uncontrolled character-sum
failure.

The diagonal product terms in (RKCOUNT) descend to the slope line.  Since

```text
r_+(z,Y) r_-(z,Y)=B_R(z)/Q_R(z),
```

one has, on the open locus `Q_R B_R != 0`,

```text
S_{a,a}
 = sum_z (1+chi_2(Theta_R(z))) chi^a(B_R(z)/Q_R(z)).       (RKDIAG)
```

Thus every diagonal pair term is the sum of two `P^1` Kummer traces: the
untwisted rational term `chi^a(B_R/Q_R)` and the quadratic-twisted quartic
term `chi_2(Theta_R) chi^a(B_R/Q_R)`.  Their zero-pole support is contained in
the roots of `B_R`, `Q_R`, `Theta_R`, and infinity, hence is bounded by an
absolute constant.  The only diagonal no-cancellation branches are the explicit
power-divisor congruences

```text
div((B_R/Q_R)^a) == 0 mod e,
div((B_R/Q_R)^{a ell/e} Theta_R^{ell/2}) == 0 mod ell,
ell=lcm(e,2).
```

Consequently the diagonal part of (RKCOUNT) never requires a new
depth-dependent genus-one estimate; it is a bounded-support `P^1` Kummer
problem.  The genuinely cover-level terms are the off-diagonal `S_{a,b}` with
`a != b`, together with the one-root sums `S_a^+`.

There is a useful index-two closure.  If `e=2`, write `rho=chi` for the
quadratic quotient character.  The sheet involution gives
`S_1^+=S_1^-`, so the one-root terms cancel in (RKCOUNT), and on `C_R^x`

```text
N_R^{+,-}(D)
 = (1/4) ( |C_R^x| - S_{1,1} ) + O(1)

 = (1/4) |C_R^x|
   - (1/4) sum_z (1+rho(Theta_R(z))) rho(B_R(z)/Q_R(z))
   + O(1).                                             (RK2)
```

Thus for quadratic-residue domains the residual mixed root-core count has no
genuinely cover-level character terms at all after the fixed-zero-root branch
is charged.  It is a `P^1` Kummer problem with only two explicit parity gates:
`B_R/Q_R` a square, or `Theta_R B_R/Q_R` a square, as divisors on the slope
line.  If neither gate occurs, the standard `P^1` Kummer bound gives

```text
N_R^{+,-}(D) <= (1/2)|D| + C sqrt(p) + O(1)
```

on each geometrically integral nonsplit cover branch, and

```text
N_R^{+,-}(D) <= |D| + C sqrt(p) + O(1)
```

on the split-square rational branch.  This index-two case therefore has no
residual genus-one analytic input; only the explicit square-divisor branches
remain to charge or exclude.

If no nonprincipal `chi^a(r_+)` or `chi^a(r_+)chi^b(r_-)` term is
geometrically trivial on `C_R`, the standard curve Kummer-Weil input gives

```text
N_R^{+,-}(D)
 <= ((e-1)/e^2) |C_R^x| + C_e sqrt(p) + O_e(1).       (RKBD)
```

Since the squarefree cover has genus at most one, Hasse gives
`|C_R^x|<=p+O(sqrt p)` on each geometrically integral nonsplit cover branch
(with conjugate or no-point degeneracies only smaller), while the split-square
rational branch has `|C_R^x|<=2p+O(1)`.  Therefore (RKBD) gives, respectively,

```text
N_R^{+,-}(D) <= (1-1/e)|D| + C_e sqrt(p) + O_e(1),
N_R^{+,-}(D) <= 2(1-1/e)|D| + C_e sqrt(p) + O_e(1).  (RKBD')
```

Combining the norm-power, anti-ratio, and rational-cubic reductions gives the
classified per-core form needed downstream.  After the fixed-zero-root branch
and constant-norm line-packet branch have been charged, and after the
negative-parity rational one-root-square subbranch has been separately
isolated:

```text
positive-parity square-norm branch:
  N_R^{+,-}(D) <= (e-2)|D| + C_e sqrt(p) + O_e(1),

negative-parity square-norm genus-one branch:
  N_R^{+,-}(D) <= |D| + C_e sqrt(p) + O_e(1),

negative-parity square-norm rational one-root-square branch:
  if chi^{e/2}(alpha)=-1:
    N_R^{+,-}(D) <= C_e sqrt(p) + O_e(1),
  if chi^{e/2}(alpha)=+1:
    N_R^{+,-}(D) <= 2|D| + C_e sqrt(p) + O_e(1)
    and the branch is the two-coset packet chi(h)^2=chi(alpha)^{-1},

geometrically integral genus-one branch:
  N_R^{+,-}(D) <= (1-1/e)|D| + C_e sqrt(p) + O_e(1),

geometrically integral rational cubic branch:
  N_R^{+,-}(D) <= |D| + C_e sqrt(p) + O_e(1),

split-square rational branch:
  N_R^{+,-}(D) <= 2(1-1/e)|D| + C_e sqrt(p) + O_e(1),

index-two branch away from the two square gates:
  N_R^{+,-}(D) <= (1/2)|D| + C sqrt(p) + O(1)
  on nonsplit covers, and <= |D| + C sqrt(p) + O(1) on split covers.
                                                              (RKCLASS)
```

The positive-parity square-norm line is the genus-free norm-outside injection
(RKSQ+) and the slope-line square-map packet (RKSQPARAM).  The
negative-parity square-norm lines use the collapse to one-root sums (RKSQNEG)
and the degree-two one-root square gate (RKSQROOT).  The
genus-one line uses that genus-one covers have no genuine cover-level power
branch after the norm exceptions.  The rational cubic line is exactly the
rational cubic coefficient ledger (RKCUBBD).  The split-square line is the
older split-square fallback; it is kept separate because the split cover has
two rational sheets.

An unordered mixed split pair contributes to exactly one of the two ordered
cover points `(z,Y)` and `(z,-Y)`, and repeated-root points contribute
nothing to the mixed-domain condition.  Thus the same bound applies to the
residual mixed root-core slopes over this fixed core.  This is still a
per-core statement: the global M1 task remains to charge or bound the active
`(j-2)` root-core image.

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
image with fibers of size at most two and a rank-one scalar Hankel
anchor-recovery condition plus equivalent quadratic slope and anchor gates,
identifies the conic-secant form of the remaining shadow target, reduces fixed
external-anchor one-root fibers to the boundary-core image after lifted
boundary-core root-slice charges, packages each fixed-domain-core boundary
incidence as a bidegree-two graph cut out by an explicit `(2,2)` determinant,
identifies that determinant as the pullback of the ordinary two-root elementary
determinant, identifies the mixed-domain trace of each surviving non-fixed
line packet as the escaped-root graph of the fixed-sum or product-Mobius
involution, reduces the complementary fixed-core conic trace to the quartic
discriminant gate above, classifies the identically-zero discriminant case as
line-packet or envelope-filtered, identifies the nonzero-discriminant target
with a genus-at-most-one double cover up to two linear exceptions, proves that
same finite-slope multiplicity on the live boundary-core conic has already
returned to a fixed-root line, a constant-slope non-fixed line packet, or the
full-plane lift, gives the exact full-subgroup quartic character expansion
and its Kummer power-divisor gate, closes the non-line fixed-core conic branch
with the ledger multiplier (KROOT), identifies the slope-side root-core
recurrence chart and its quartic discriminant numerator, realizes the residual
split slopes as a genus-at-most-one cover of the slope line, pushes the
domain/outside filter to bounded-conductor Kummer traces on that cover, derives
the per-core mixed-domain Kummer bound (RKBD) after fixed-zero-root and
nonprincipal power branches are removed, descends the diagonal pair terms in
that mixed-domain expansion to bounded-support `P^1` Kummer sums, closes the
index-two mixed-domain cover-level terms by sheet-symmetry cancellation,
factors the outside-root test through the slope-line norm `B_R/Q_R`, obtains
the genus-free norm-outside fallback bound (RKNOUTBD), classifies the
degree-two norm-power exceptions as constant norm or quadratic square norm,
charges constant norm to the fixed-root/product-Mobius line-packet ledger,
isolates the single large quadratic coefficient in the nonconstant square-norm
filter, proves the norm-pushforward obstruction that leaves only anti-diagonal
cover-ratio power branches after those norm exceptions, reduces the
anti-diagonal obstruction further to the cubic ratio branch, shows that a
genuine cubic no-cancellation term forces the rational-cover locus, gives the
explicit rational-cubic coefficient ledger (RKCUBBD), packages the resulting
per-core classified bound (RKCLASS), including the positive-parity square-norm
norm-filter bound and the negative-parity one-root collapse, and gives the
local max-degree bound and average-collinearity corollary above, including the
packet-level higher-exchange ledger substitution, and extracts the
square-norm repeated-endpoint gate (RKSQREP), the double-root endpoint
certificate (RKSQDR), the raw-coefficient endpoint certificate (RKSQRAW), the
raw-endpoint discriminant certificate (RKSQDISC), the Hankel-minor
discriminant certificate (RKSQHCOEFF/RKSQHDISC), the Plucker-minor
discriminant certificate (RKSQPL), the Plucker-chart decomposition
(RKSQPLCH), the Plucker-chart row recurrence (RKSQROW), the Hankel square
factorization (RKSQSQ), the endpoint slope map (RKSQZ), the overlapping
Plucker-chart recurrence (RKSQOV), the endpoint-pair inversion
(RKSQINV0/RKSQINV1), the projective endpoint-pair inversion
(RKSQPINV0/RKSQPINV1), the projective diagonal endpoint collapse
(RKSQPDIAG), the off-diagonal endpoint-pair count (RKSQOFF), the canonical
endpoint-pair norm factorization (RKSQRAT), the fixed endpoint-pair coset
palette (RKSQPAIRPAL), the fixed-basis endpoint-palette bound (RKSQBASIS),
the finite endpoint-charge corollary (RKSQEPCH), and square-map packet-count
corollary (RKSQCOUNT) from the support palette.

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
fiber reduction over sampled small domains, including the rank-one
anchor-recovery, quadratic slope-gate, conic-secant anchor-gate, and
fixed-anchor boundary-core fiber, fixed-core graph, and bidegree determinant
pullback criteria, the mixed-domain line-packet trace formulas, and the
boundary-core quadratic/discriminant anchor gate and its zero-discriminant
classification, and the bounded-cover parametrization of the live quartic
target.  It also checks the elementary same-slope fiber alternatives for
fixed-core boundary conics: empty, point, affine line, or full plane, with
multi-point fibers returning to the charged line/plane ledgers.  Finally, it
checks the degree-four Kummer power gate for the full-subgroup quartic
character terms on structured monomial-square discriminants and random
quartics over small prime fields, and checks the slope-side recurrence chart
for fixed root cores, including its denominator-zero fixed-root/full-plane
classification, quartic degree bound, split-root cover criterion, and exact
finite-field subgroup-character expansion for the domain/outside filter and
the mixed-domain count formula (RKCOUNT), including the diagonal descent
(RKDIAG), index-two cancellation formula (RK2), and norm-filter identity
(RKNORM) with norm-outside injection (RKNINJ) and degree-two norm-power gate
(RKNP), including the constant-norm line-packet charge and the single-large
square-norm Fourier term, and the cover-term norm-pushforward obstruction
(RKPUSH), including the anti-ratio square-class and degree-four reduction
(RKANTIRED) and the genus-one exclusion for genuine cubic anti-ratio powers
(RKANTIGENUS), plus the rational cubic coefficient ledger (RKCUBBD) and the
classified per-core bound (RKCLASS), the degree-one square-map packet
intersection gate (RKSQINT), the finite support-class palette (RKSQPAL), and
the square-norm endpoint palette (RKSQEND), the repeated-endpoint gate
(RKSQREP), the double-root endpoint certificate (RKSQDR), the raw-coefficient
endpoint certificate (RKSQRAW), the raw-endpoint discriminant certificate
(RKSQDISC), the Hankel-minor discriminant certificate
(RKSQHCOEFF/RKSQHDISC), the Plucker-minor discriminant certificate (RKSQPL),
the Plucker-chart decomposition (RKSQPLCH), the Plucker-chart row recurrence
(RKSQROW), the Hankel square factorization (RKSQSQ), the endpoint slope map
(RKSQZ), the overlapping Plucker-chart recurrence (RKSQOV), the endpoint-pair
inversion (RKSQINV0/RKSQINV1), the projective endpoint-pair inversion
(RKSQPINV0/RKSQPINV1), the projective diagonal endpoint collapse
(RKSQPDIAG), the off-diagonal endpoint-pair count (RKSQOFF), the canonical
endpoint-pair norm factorization (RKSQRAT), the fixed endpoint-pair coset
palette (RKSQPAIRPAL), the fixed-basis endpoint-palette bound (RKSQBASIS),
the finite endpoint-charge corollary (RKSQEPCH), and the packet-count
corollary (RKSQCOUNT).
