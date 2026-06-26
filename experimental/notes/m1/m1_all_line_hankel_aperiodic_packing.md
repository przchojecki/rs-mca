# M1 All-Line Hankel Aperiodic Packing Target

## Status

PROVED finite normal form / AUDIT verifier / NOT the final M1 theorem.

This note records the first M1 packet following the maintainer target:

```text
#{z : exists an aperiodic split locator T} <= n^B
```

after tangent/contained and quotient-periodic locator classes are charged.
It uses the Hankel-pencil normal form from `experimental/experiments.tex`.

## Set-Up

Let `F` be a finite field, let `D subset F` have size `n`, and let
`C=RS[F,D,k]`.  Put

```text
r=n-k,        j+t=r,        a=k+t=n-j.
```

For a line `(f,g):D->F^2`, write

```text
u=Syn(f),        v=Syn(g),
```

using the usual RS parity-check syndrome.  For each `j`-point complement
`T subset D`, let

```text
L_T(X)=prod_{x in T}(X-x),
ell_T=(ell_0,...,ell_j)^T
```

be its monic locator vector.  The Hankel-pencil test says that a finite slope
`z` is explained on `S=D\T` if and only if

```text
(H_{t,j}(u)+zH_{t,j}(v)) ell_T = 0.        (1)
```

It is support-wise noncontained on that support if and only if

```text
H_{t,j}(v) ell_T != 0.                      (2)
```

## Charged/Aperiodic Split-Locator Ledger

For fixed `(f,g,t,j)`, define `Bad(T)` to mean that `T` is a split complement
whose locator satisfies (1) for some slope and satisfies (2).  When this holds,
the slope is unique unless the whole vector `H(v)ell_T` vanishes, which is
exactly the contained/tangent-core class removed by (2).

When `D=H` is a cyclic multiplicative subgroup, a split complement `T` is
called whole-fiber quotient-periodic at scale `m|n`, `1<m<n`, if it is a union
of cosets of the subgroup of `H` of size `m`.  Let `QP(T)` mean that this
holds for at least one charged scale.

The finite all-line slope ledger is therefore the disjoint accounting

```text
Bad slopes
  = charged quotient-periodic slope image
    union aperiodic slope image,

AperSlope(f,g;t,j)
  = { z_T : Bad(T) and not QP(T) }.
```

The maintainer target is to prove a polynomial bound for this last image,
uniformly in the line `(f,g)`, after the tangent/contained and
quotient-periodic ledgers have been paid.

## Exactness Lemma

The ledger above is exact for every finite instance.

1. The Hankel-pencil theorem gives equivalence between support-wise line
   incidence and the existence of a split locator satisfying (1).
2. Condition (2) is exactly the noncontainment condition on the same support,
   so contained/tangent-core locators are removed before aperiodicity is
   counted.
3. The quotient-periodic predicate depends only on the support complement and
   the selected quotient scales, so charging it before taking slope images
   cannot create or remove aperiodic locators.
4. Every remaining bad locator contributes the unique slope forced by
   `H(u)ell_T + zH(v)ell_T=0`, and the set of these slopes is precisely
   `AperSlope(f,g;t,j)`.

Thus the residual M1 problem is no longer a question about support-wise MCA
definitions.  It is the slope image of the aperiodic split-locator incidence
inside the Hankel pencil.

## The `t=2` Determinant And Strict-Exchange Profile

In the first nontrivial slack window `t=2`, put

```text
a_T = H_{2,j}(u) ell_T,        b_T = H_{2,j}(v) ell_T  in F^2.
```

Then a split complement contributes a noncontained bad slope if and only if

```text
b_T != 0,        det[a_T b_T] = 0.
```

When this holds, the slope is the unique scalar

```text
z_T = -a_{T,i}/b_{T,i}
```

for any coordinate `i` with `b_{T,i} != 0`.  Thus the residual aperiodic M1
object in this window is the image of a rational slope map on the aperiodic
part of the split-locator determinant locus.

The support-overlap form of the same object is also explicit.  Since
`S=D\T` has size `n-j=k+t`, two supports have strict high overlap
`|S cap S'|>k` exactly when the complements satisfy

```text
|T \ T'| = |T' \ T| < t.
```

For `t=2`, this is the one-exchange graph on complement locators.  After
quotient-periodic locators are charged, the verifier reports the one-exchange
profile of the remaining aperiodic determinant locus: total strict edges,
maximum strict degree, maximum slope-fiber size, and same-slope strict edges.
These are not the final M1 theorem, but they are the finite statistics that a
packing or inverse theorem must eventually control uniformly.

## Same-Slope One-Exchange Root Slice

The same-slope part of the strict one-exchange profile has an exact structural
explanation.  Fix `t=2` and a slope `z`, and write

```text
A_z = H_{2,j}(u)+zH_{2,j}(v).
```

Let `R subset D` have size `j-1`, and write

```text
L_R(X)=c_0+c_1X+...+c_{j-1}X^{j-1}.
```

For `x notin R`,

```text
L_{R union {x}}(X) = X L_R(X) - x L_R(X).
```

Thus its locator vector is affine in `x`:

```text
ell_{R union {x}} = s_R - x p_R,
```

where `s_R` is the coefficient vector of `X L_R` and `p_R` is the coefficient
vector of `L_R`, padded to length `j+1`.  If two distinct exchanged roots
`x,y` give the same slope `z`, then

```text
A_z(s_R-xp_R)=0,        A_z(s_R-yp_R)=0.
```

Subtracting gives `A_z p_R=0`, and then also `A_z s_R=0`.  Therefore

```text
A_z ell_{R union {w}}=0        for every w in D\R.
```

So every same-slope strict one-exchange edge lies in a full fixed-slope
root-slice incidence packet.  The only remaining support-wise filter on that
slice is noncontainment, namely whether

```text
H_{2,j}(v) ell_{R union {w}} != 0.
```

This separates two jobs in the M1 proof search: same-slope strict collisions
belong to root-slice/tangent-style ledgers, while the genuinely aperiodic
packing problem is the slope image of determinant-locus packets after these
root slices and the quotient-periodic classes are charged.

## Different-Slope One-Exchange Quadratic Slice

The different-slope part of the one-exchange profile has a complementary
finite-degree constraint.  Keep `t=2` and a fixed `(j-1)`-root core `R`.  With

```text
ell_x = ell_{R union {x}} = s_R-xp_R,
```

the two Hankel vectors

```text
a(x)=H_{2,j}(u)ell_x,        b(x)=H_{2,j}(v)ell_x
```

are affine functions of `x`.  Hence the determinant

```text
Delta_R(x)=det[a(x) b(x)]
```

is a polynomial in `x` of degree at most two.  Therefore a one-root slice has
only two determinant roots unless `Delta_R` is identically zero.  In
particular, a different-slope strict one-exchange edge is either:

1. the whole determinant root set of a nonzero quadratic slice; or
2. part of an exceptional zero-determinant root slice, where every exchanged
   root passes the determinant gate and the slope map along the slice must be
   controlled separately.

The verifier checks this dichotomy on every `(j-1)`-core slice in the finite
audit rows by evaluating `Delta_R` on the ambient prime field.  Thus the
residual `t=2` M1 packing target is further localized: after quotient-periodic
classes and same-slope root slices are charged, different-slope strict edges
can only accumulate through zero-determinant root slices or through many
isolated nonzero quadratic slices.

## Zero-Determinant Slice Slope Dichotomy

The exceptional zero-determinant branch also has an exact local dichotomy.
Assume `Delta_R` vanishes identically on the one-root slice for a fixed core
`R`.  Write

```text
a(x)=a_s-xa_p,        b(x)=b_s-xb_p,
```

where `a_s=H(u)s_R`, `a_p=H(u)p_R`, and similarly for `b`.  If the direction
pencil `span{b_s,b_p}` has rank two in `F^2`, then the identities

```text
det[a_s b_s]=0,
det[a_p b_s]+det[a_s b_p]=0,
det[a_p b_p]=0
```

force `a_s=-z b_s` and `a_p=-z b_p` for a single scalar `z`.  Thus every
noncontained point of the slice has the same slope.

If instead `span{b_s,b_p}` has rank zero, the whole slice is contained and
contributes no noncontained slopes.  The remaining rank-one case is also
constant-slope because the two locator vectors are not arbitrary affine
vectors: for every syndrome `y`,

```text
H_{2,j}(y)s_R=(S_0,S_1),        H_{2,j}(y)p_R=(P_0,S_0).
```

Thus, writing `b_s=(B_0,B_1)` and `b_p=(C,B_0)`, rank one gives
`CB_1=B_0^2`.  The three zero-determinant identities force `a_s` and `a_p` to
lie on the same one-dimensional direction as `b_s` and `b_p`; the displayed
Hankel overlap then forces the two scalar ratios to agree.  The edge cases
`B_0=0` say that one of `b_s,b_p` vanishes, and the same identities force the
matching `a` vector to vanish, again giving a single slope on every
noncontained point.

Equivalently, if two distinct exchanged roots `x,y` have the same slope `z`,
then the same subtraction argument as above gives

```text
(H_{2,j}(u)+zH_{2,j}(v))p_R=0,
(H_{2,j}(u)+zH_{2,j}(v))s_R=0.
```

Consequently every noncontained member of that zero-determinant slice has the
same slope `z`.  Thus zero-determinant one-root slices split into:

1. constant-slope root-slice packets, already handled by the same-slope
   root-slice ledger; or
2. contained/tangent slices, which contribute no noncontained aperiodic slope.

The verifier certifies this split by checking the three determinant
coefficients of `Delta_R`, computing the direction-pencil rank, and then
checking that every noncontained zero-determinant slice is constant-slope.

## Root-Slice Peeling Corollary

For `t=2`, the fixed-slope one-exchange graph can be peeled exactly.  For each
same-slope strict edge, include the full fixed-slope root slice supplied by the
root-slice lemma, and remove every aperiodic locator lying in one of these
packets.  The remaining aperiodic locator family has no same-slope
one-exchange edge.

Indeed, any same-slope one-exchange edge in the residual family would generate
one of the root slices used in the peeling step, so both of its endpoints would
have been removed.  Thus repeated-slope high-overlap structure is completely
charged to constant root-slice packets; the residual slope fibers are
one-exchange independent and must be controlled by a different mechanism.

## Residual One-Exchange Degree Bound

After the same-slope root-slice packets are peeled, the remaining `t=2`
one-exchange graph has bounded local degree.  More precisely, every residual
aperiodic locator has strict one-exchange degree at most `j`.

Fix a residual complement `T`.  Any strict one-exchange neighbor is obtained by
choosing one deleted root `r in T`, putting `R=T\{r}`, and replacing `r` by one
new root.  The residual graph has no same-slope edge by the peeling corollary.
If the determinant polynomial `Delta_R` were identically zero, the
zero-determinant dichotomy would make every noncontained point of that slice
constant-slope, hence any residual edge on the slice would have been peeled.
Thus a residual edge through this core lies on a nonzero quadratic slice.

But a nonzero quadratic slice has at most two roots in the ambient field, and
one of them is the original point `r`.  For this fixed core `R`, there is
therefore at most one residual neighbor.  Since `T` has only `j` choices of the
deleted root `r`, the residual strict one-exchange degree is at most `j`.

This is still not the final slope-image packing theorem.  It is, however, an
exact local sparsity result: after quotient-periodic locators, contained
locators, and constant root-slice packets are charged, the high-overlap graph
on the remaining `t=2` aperiodic determinant locus has degree `O(j)`, not
`O(j(n-j))`.

## Quadratic Companion Map

The residual edges are not merely sparse; they are algebraically forced.  For
each one-root core `R`, write

```text
Delta_R(X)=c_0+c_1X+c_2X^2.
```

After zero-determinant slices are charged, any residual strict edge through
the core `R` must lie on a nonzero quadratic slice.  If one endpoint replaces
the deleted root by `x`, then the other endpoint, when it exists, replaces it
by

```text
psi_R(x)=-c_1/c_2-x.        (c_2 != 0)
```

If `c_2=0`, the nonzero slice is linear and cannot contain two distinct
exchanged roots.  Thus the residual one-exchange graph is a subgraph of the
union, over all `(j-1)`-cores `R`, of the involutions `psi_R` restricted to
the determinant roots in `D\R`.

This companion-map form is the local object a future packing proof should
control: long residual slope structure would have to persist through many
compatible quadratic involutions, not through arbitrary one-root exchanges.

## Common Companion Anchor

The companion map is actually anchored at each residual locator.  Fix a
residual locator `T` with slope `z`, and put

```text
b_T = H_{2,j}(v)ell_T = (beta_0,beta_1) != 0.
```

For `r in T`, write `R=T\{r}` and let `m_R` be the coefficient vector of
`L_R`, padded to length `j+1`.  Since

```text
L_T(X)=(X-r)L_R(X)
```

and `(H(u)+zH(v))ell_T=0`, the Hankel shift gives

```text
(H(u)+zH(v))m_R = c_R(1,r)
```

for some scalar `c_R`.  If `c_R=0`, then the whole root slice through `R` has
the same slope `z`, so every noncontained point of that slice was already
removed by the root-slice peeling.

Otherwise vary the exchanged root by writing

```text
ell_{R union {x}} = ell_T + (r-x)m_R.
```

Set `lambda=r-x`.  Using `H(u)ell_T=-zH(v)ell_T`, the determinant on this
one-root slice is

```text
Delta_R(x)
 = lambda det((H(u)+zH(v))m_R, b_T)
   + lambda^2 det((H(u)+zH(v))m_R, H(v)m_R).
```

If `H(v)m_R=(B_0,B_1)`, then `beta_0=B_1-rB_0`, and the displayed identity
becomes

```text
Delta_R(x) = lambda c_R[(beta_1-r beta_0)+lambda beta_0].
```

Thus, after root-slice peeling, every finite different-slope companion of `T`
has the same added root

```text
xi_T = beta_1/beta_0,
```

when `beta_0 != 0`.  If `beta_0=0`, then `beta_1 != 0` and the nonpeeled slice
is linear with only the original root `x=r`, so it gives no strict residual
neighbor.

Consequently all residual one-exchange neighbors of a fixed locator `T`, if
any exist, are obtained by adding the same root `xi_T` and deleting one root of
`T`.  This upgrades the residual graph from bounded-degree to packet-local:
each residual locator is incident to at most one top packet.

## Residual Anchor Ledger

The same anchor accounts for isolated residual locators as well as top
packets.  For a residual locator `T`, write

```text
H_{2,j}(v)ell_T=(beta_0,beta_1).
```

If `beta_0 != 0`, set

```text
xi_T=beta_1/beta_0.
```

There are two cases.

First suppose `xi_T in D\T`.  Put `W=T union {xi_T}`.  The denominator lift
identity gives

```text
H_{1,j+1}(v)ell_W=beta_1-xi_T beta_0=0.
```

Since `T` is a residual bad locator, `H_{2,j}(u)ell_T=-z_T H_{2,j}(v)ell_T`.
Writing `H_{2,j}(u)ell_T=(alpha_0,alpha_1)`, this also gives

```text
H_{1,j+1}(u)ell_W=alpha_1-xi_T alpha_0=0.
```

Thus every residual locator with an addable in-domain anchor is a residual
face of a lifted common core.

In the remaining cases the locator is isolated in the residual one-exchange
graph.  If `beta_0=0`, the common-companion formula gives no finite addable
root.  If `xi_T in T`, the only possible companion root is already deleted by
the locator.  If `xi_T notin D`, no domain one-exchange can add it.  In all
three cases any residual neighbor would contradict the common companion-anchor
lemma.

Therefore the residual locator family has the exact disjoint ledger

```text
R_res = R_lifted disjoint union R_escape,
```

where `R_lifted` is the set of residual faces lying in lifted common cores and
`R_escape` is the set of isolated anchor escapes.  The escape side splits into
the three explicit local causes

```text
beta_0=0,        xi_T in T,        xi_T notin D.
```

So the M1 residual slope problem has two separate pieces: lifted common-core
face counting for `R_lifted`, and isolated anchor-escape slope counting for
`R_escape`.

## Projective Residual Lift Ledger

The escape cases are still boundary cases of the same lifted Hankel geometry.
For a residual locator `T`, write

```text
H_{2,j}(v)ell_T=(beta_0,beta_1),        H_{2,j}(u)ell_T=(alpha_0,alpha_1).
```

If `beta_0 != 0`, set `xi_T=beta_1/beta_0`.  Then the formal one-root lift

```text
L_T(X)(X-xi_T)
```

satisfies both one-row gates

```text
H_{1,j+1}(v)ell_{T,xi_T}=0,        H_{1,j+1}(u)ell_{T,xi_T}=0.        (PL1)
```

Indeed the denominator identity is `beta_1-xi_T beta_0=0`, and the numerator
identity follows from the residual bad-slope relation
`(alpha_0,alpha_1)=-z_T(beta_0,beta_1)`.

Thus finite anchors split into three lifted types:

1. `xi_T in D\T`: a squarefree in-domain lifted common core;
2. `xi_T in T`: a repeated-root degenerate lift, hence an isolated escape;
3. `xi_T notin D`: an off-domain finite lift, hence an isolated escape.

If `beta_0=0`, then residual noncontainment gives `beta_1 != 0`, and the
bad-slope equation gives `alpha_0=0`.  No finite `xi` can make
`beta_1-xi beta_0` vanish, so this is the projective infinity-anchor boundary
of the same lift ledger.  Consequently the isolated escape side is not an
unstructured remainder: it consists of repeated-root, off-domain, and
infinity-anchor boundary lifts.

## Residual Slope-Image Ledger

The anchor ledger also splits the residual slope image itself.  Define

```text
Z_res  = {z_T : T in R_res},
Z_lift = {z_T : T in R_lifted},
Z_esc  = {z_T : T in R_escape}.
```

Then exactly

```text
Z_res = Z_lift union Z_esc.          (SL1)
```

There is no third slope source after quotient-periodic locators,
contained/tangent locators, and fixed-slope root slices have been charged.

The lifted side has a local injectivity property.  If `W` is a lifted common
core and `T_x,T_y subset W` are two distinct residual faces, then `T_x` and
`T_y` are one-exchange neighbors.  If they had the same residual slope, the
same-slope root-slice lemma would put both in a fixed-slope root-slice packet,
so they would have been peeled before `R_res` was formed.  Hence the residual
faces of each lifted common core have pairwise distinct slopes.

Thus a future slope-image proof can work with two explicit objects:

1. injective residual-coordinate slopes inside lifted common cores; and
2. isolated anchor-escape slopes.

This is sharper than a locator count.  The lifted core may have many
noncontained or aperiodic faces before peeling, but after the root-slice charge
it contributes at most one residual face to any fixed slope.

## Top-Packet Lift Gate

The common anchor also lifts every nontrivial top packet to a single
denominator equation one degree higher.  Let `W` be a residual top packet, and
for `x in W` write

```text
T_x = W\{x}.
```

Let

```text
h_v(W) = H_{1,j+1}(v)ell_W
```

be the one-row Hankel pairing of the `(j+1)`-point locator `L_W` with the
denominator syndrome `v`.  Since

```text
L_W(X)=(X-x)L_{T_x}(X),
```

if

```text
H_{2,j}(v)ell_{T_x}=(beta_0(x),beta_1(x)),
```

then the shift identity gives

```text
h_v(W)=beta_1(x)-x beta_0(x).        (TP1)
```

This quantity is independent of the omitted root `x`.  If `T_x` is a vertex of
a nontrivial residual top packet, then it has a residual neighbor inside the
same `W`, and the common companion anchor says `beta_0(x) != 0` and
`beta_1(x)/beta_0(x)=x`.  Hence (TP1) vanishes.

Therefore every residual top packet satisfies the lifted denominator gate

```text
H_{1,j+1}(v)ell_W=0.                 (TP2)
```

Moreover, for each residual member `T_x subset W`, equation (TP2) is exactly the
statement that the companion anchor of `T_x` is the omitted root `x`, provided
`beta_0(x) != 0`.  Thus the residual top-packet search is no longer over
arbitrary `(j+1)`-sets: possible packets first lie in the one-row denominator
kernel (TP2), and then their `j`-subsets must pass the residual determinant and
aperiodicity gates.

The same lift holds for the numerator.  Write

```text
H_{2,j}(u)ell_{T_x}=(alpha_0(x),alpha_1(x)).
```

Since `T_x` is a residual bad locator, the determinant gate gives

```text
alpha_0(x)beta_1(x)-alpha_1(x)beta_0(x)=0.
```

For a nontrivial residual top packet, the denominator anchor has
`beta_0(x) != 0` and `beta_1(x)=x beta_0(x)`.  Hence

```text
alpha_1(x)=x alpha_0(x),
```

and the same shift identity gives

```text
H_{1,j+1}(u)ell_W=alpha_1(x)-x alpha_0(x)=0.       (TP3)
```

Thus every nontrivial residual top packet lies in the common lifted Hankel
kernel

```text
H_{1,j+1}(u)ell_W = H_{1,j+1}(v)ell_W = 0.
```

Equivalently, in the one-degree-up `t=1`, `j+1` window, residual top packets
are contained/tangent-core locators for the same all-line pencil.  The
remaining M1 obstruction is therefore not arbitrary top-packet geometry: it is
the question of how many residual `j`-faces of such lifted common-kernel
locators can also pass the original `t=2` aperiodic determinant gates.

In fact, the original determinant gate is automatic on every `j`-face of such
a lifted core.  If `W` satisfies the common lifted gate and `T_x=W\{x}`, then
the two shift identities give

```text
H_{2,j}(u)ell_{T_x}=(alpha_0(x),x alpha_0(x)),
H_{2,j}(v)ell_{T_x}=(beta_0(x),x beta_0(x)).
```

These two vectors are always proportional.  Hence each `j`-face of `W` is
either contained, when `beta_0(x)=0`, or contributes the finite bad slope

```text
z_x=-alpha_0(x)/beta_0(x).
```

Thus a nontrivial residual top packet is not merely contained in a lifted
common core; it is the residual part of a full bad-face simplex over that
core.  The only remaining filters on the faces are the charged
quotient-periodic predicate and the fixed-slope root-slice peeling.

This gives an exact top-packet census.  Enumerate all `(j+1)`-sets `W` with

```text
H_{1,j+1}(u)ell_W=H_{1,j+1}(v)ell_W=0.
```

For each such lifted common core, remove contained faces, quotient-periodic
faces, and faces peeled by fixed-slope root slices.  If at least two residual
faces remain, then they form exactly one residual top packet, namely the clique
on those remaining faces inside `W`.  Conversely every residual top packet
arises this way.  Thus the residual packet problem is precisely the problem of
bounding lifted common cores with residual face count at least two.

## Common-Base Residual-Slope Form

The lifted common-core condition has a direct interpolation meaning.  For
`t=2`, if a `(j+1)`-set `W` satisfies

```text
H_{1,j+1}(u)ell_W=H_{1,j+1}(v)ell_W=0,
```

then

```text
S_0=D\W
```

has size `k+1`, and both restrictions `f|S_0` and `g|S_0` are explained by
degree `<k` polynomials.  Let these interpolants be `F_0` and `G_0`.

For a face `T_x=W\{x}`, its support is `S_x=S_0 union {x}`.  On the base
`S_0`, the line word `f+zg` already agrees with `F_0+zG_0` for every slope
`z`.  Thus the only remaining incidence condition on `S_x` is the single
coordinate equation at `x`:

```text
f(x)+z g(x)=F_0(x)+zG_0(x).
```

If `g(x)-G_0(x) != 0`, the finite bad slope on that face is exactly

```text
z_x=-(f(x)-F_0(x))/(g(x)-G_0(x)).
```

If `g(x)-G_0(x)=0`, then the denominator residual vanishes and the face is in
the contained/tangent-core denominator ledger rather than the noncontained
aperiodic slope ledger.  Consequently the lifted-core obstruction can be read
without the Hankel vectors: it is a filtered residual-coordinate slope-counting
problem over common `k+1` bases, after quotient-periodic faces and
fixed-slope root-slice faces have been charged.

## Residual Triangle Classification

The residual graph can still have triangles, but their type is forced.  In the
Johnson graph on `j`-subsets, every triangle is one of two kinds:

1. a star triangle, where the three vertices share a common `(j-1)`-core and
   vary over three different exchanged roots; or
2. a top triangle, where the three vertices are the `j`-subsets of one
   `(j+1)`-set obtained by omitting three different elements.

Star triangles cannot survive in the residual `t=2` graph.  For a fixed
`(j-1)`-core, a nonzero determinant slice has at most two roots, while a
zero-determinant slice is contained or constant-slope and has already been
charged to the root-slice ledger.  Hence three residual vertices with one
common `(j-1)`-core are impossible.

Therefore every residual triangle is a top triangle.  This does not yet prove
that large top packets are small in number, but combined with the common
companion anchor it does prove that the residual graph is a disjoint union of
top-packet cliques and isolated residual locators.  Thus any future packing
argument can focus on controlling these top packets rather than arbitrary star
fibers or branching two-edge corners.

## Residual Top-Packet Ledger

The top-packet accounting is exact.  Let `R_res` be the residual aperiodic
locator family after root-slice peeling.  For every `(j+1)`-set `W subset D`,
put

```text
m_W = #{T in R_res : T subset W}.
```

Every residual one-exchange edge `{T,T'}` has the unique top packet
`W=T union T'`, so

```text
# residual edges = sum_W binom(m_W,2).
```

Inside one top packet, all `j`-subsets of `W` are mutually adjacent in the
Johnson graph.  The no-same-slope residual property therefore makes every
top packet slope-injective.  Since star triangles have been ruled out, the
residual triangle count is also exactly

```text
# residual triangles = sum_W binom(m_W,3).
```

The same packet ledger is local at each residual locator:

```text
deg_res(T) = sum_{W superset T} (m_W-1).
```

This is just the edge identity refined by endpoint.  It is useful because a
large residual degree cannot be spread invisibly through unrelated cores; it
must be witnessed by top packets incident to that locator.

The packet family is also linear as a hypergraph on residual locators: two
distinct top packets share at most one residual locator.  Indeed, if two
different `(j+1)`-sets `W,W'` contained two distinct `j`-subsets `T,T'`, then
`W=T union T'=W'`.  Consequently the residual graph is the two-section of a
linear hypergraph whose hyperedges are slope-injective top packets.

The common companion anchor strengthens this from linearity to
vertex-disjointness on the residual locator side.  If a residual locator `T`
has a neighbor, every neighbor adds the same root `xi_T`; hence every residual
edge through `T` lies in the single top packet `T union {xi_T}`.  No residual
locator can therefore sit in two distinct top packets.  The residual graph is
exactly a disjoint union of slope-injective top cliques, together with isolated
residual locators.

Each nontrivial top packet also satisfies the common lifted gate
`H_{1,j+1}(u)ell_W=H_{1,j+1}(v)ell_W=0`.  Thus large residual cliques must be
visible one degree up in the common Hankel kernel before the original
`t=2` residual determinant gates are even considered.  Once this lifted gate
holds, the determinant gates on all `j`-faces of `W` are automatic; the
residual packet is the subfamily of noncontained, aperiodic, unpeeled faces.

Thus the residual high-overlap obstruction has been localized further: pair
packets with `m_W=2` are isolated at triangle level, while every surviving
triangle and every large local clique is carried by a slope-injective
`(j+1)`-top packet.

## Verifier

The companion verifier

```bash
python3 experimental/scripts/verify_m1_all_line_hankel_aperiodic.py
```

enumerates small cyclic-domain cases.  For each case it:

- computes syndromes and Hankel windows for a deterministic family of all-line
  words;
- enumerates all split complements `T`;
- applies the projective slope gate for `t=2`;
- cross-checks every bad slope by direct RS interpolation on `D\T`;
- labels whole-fiber quotient-periodic complements at the selected scales;
- reports the aperiodic slope image after charged locators are removed;
- in the `t=2` rows, verifies the determinant gate and reports the strict
  one-exchange profile of the aperiodic locator family;
- checks that every same-slope strict one-exchange edge extends to the full
  fixed-slope root slice predicted by the lemma above;
- verifies that different-slope strict edges obey the quadratic root-slice
  dichotomy above;
- verifies that every zero-determinant slice is constant-slope or contained
  via the direction-pencil rank and Hankel overlap, and that constant zero
  slices account for all same-slope strict edges;
- peels root-slice members and checks that the residual aperiodic family has
  no same-slope one-exchange edges;
- reports the residual strict one-exchange count and verifies the residual
  maximum degree bound `<= j`;
- checks the quadratic companion map for every nonzero quadratic edge slice;
- verifies the common companion anchor `xi_T=beta_1/beta_0` for every oriented
  residual edge endpoint;
- verifies the full residual anchor ledger: addable in-domain anchors lift to
  common cores, while beta0-zero, in-support, and outside-domain anchor escapes
  are isolated residual locators;
- verifies the projective residual lift ledger: every finite anchor satisfies
  both one-row lifted Hankel gates, repeated-root and off-domain anchors are
  separated as finite boundary lifts, and beta0-zero escapes are checked as
  infinity anchors;
- verifies the residual slope-image ledger `Z_res=Z_lift union Z_esc` and
  checks that residual faces inside each lifted common core have pairwise
  distinct slopes;
- verifies that every nontrivial residual top packet satisfies the lifted
  denominator gate `H_{1,j+1}(v)ell_W=0`, with omitted-root anchors on its
  residual members;
- verifies the common lifted gate `H_{1,j+1}(u)ell_W=0` and the matching
  numerator omitted-root anchors;
- checks every `j`-face of each lifted top packet, verifying the omitted-root
  numerator/denominator anchor identities and the automatic determinant gate,
  and counts how many such faces are noncontained, aperiodic, residual, or
  removed by root-slice peeling;
- enumerates all lifted common cores and asserts that residual top packets are
  exactly the lifted common cores with at least two residual faces;
- verifies that each lifted common core is a common `k+1` base for `f` and
  `g`, and that every noncontained lifted face has the residual-coordinate
  cancellation slope `-(f(x)-F_0(x))/(g(x)-G_0(x))`;
- classifies every residual triangle and asserts that no star triangle remains
  after root-slice peeling;
- forms the residual top-packet ledger and checks that it accounts exactly for
  all residual edges and top triangles;
- checks the residual degree formula from the incident top packets;
- verifies that the top-packet hypergraph is linear and vertex-disjoint on
  residual locators;
- runs one deterministic arbitrary-line probe which hits the rank-one
  zero-determinant branch and verifies that it is classified by the same
  constant/contained zero-slice ledger.

The default audit currently checks three cyclic-domain parameter rows, twelve
deterministic polynomial-family line samples, and one deterministic arbitrary
line probe.  The largest observed residual aperiodic slope image in this smoke
packet has size `17`, after direct interpolation checks on every reported
support-wise bad slope.

In the polynomial-family full-domain `F_17`, `j=4`, `t=2` row, the residual
aperiodic locus has maximum slope fiber `16`, strict one-exchange degree `15`,
and `190` strict one-exchange pairs.  Of these strict edges, `78` are
same-slope edges, and the verifier certifies that they are exactly the
repeated pairs inside one constant-slope rank-two zero-determinant slice with
`13` aperiodic members.  The remaining `112` different-slope strict edges lie
on `112` nonzero quadratic slices; there are no zero-determinant
different-slope edge slices in this audit row, and the companion-map check
certifies both directions of all `112` nonzero quadratic edges.  After peeling
the root-slice members, the residual family has `86` aperiodic locators, all
`16` residual slopes still occur, the maximum residual slope fiber drops to
`9`, the residual strict edge count drops to `88`, the residual maximum strict
degree is `4=j`, and the residual same-slope one-exchange edge count is `0`.
The residual graph has `68` triangles in this row; all `68` are top triangles
and none are star triangles.  Its top-packet ledger has `14` packets, all
large, with maximum packet size `5`; these packets account for all `88`
residual edges, all `68` residual triangles, and the local residual degree
formula.  The maximum top-packet incidence of a residual locator is `1` in
this row, so the audited top packets are disjoint; the common-anchor check
certifies all `176=2*88` oriented residual edge endpoints.  The residual anchor
ledger partitions the `86` residual locators into `56` addable lifted-core
faces and `30` isolated anchor escapes: `5` with `beta_0=0`, `21` with
`xi_T in T`, and `4` with `xi_T notin D`.  The projective lift ledger checks
`81` finite residual-anchor lifts: `56` squarefree in-domain lifts, `21`
repeated-root boundary lifts, and `4` off-domain boundary lifts; the remaining
`5` escapes are infinity anchors.  On slope images, the `16` residual slopes
split as `16` lifted-core slopes and `13` escape slopes, with all `13` escape
slopes already overlapping the lifted side in this row.  The verifier also
checks `88` residual face-pairs inside lifted common cores and finds local
residual slope fiber max `1`.  The lifted
denominator gate is checked on all `14` residual top packets, with `56`
omitted-root anchor checks across their residual members; the common lifted
numerator gate has the same `14` packet checks and `56` numerator anchor
checks.  Across all `70=14*5` lifted `j`-faces, the verifier checks the
automatic determinant gate; `67` faces are noncontained, `64` are aperiodic,
`56` remain residual, and `8` are aperiodic faces removed by root-slice
peeling.  In this row the lifted-common-core census has exactly `14` cores,
all `14` of which have at least two residual faces and hence are precisely the
`14` residual top packets.  The common-base check certifies all `14` lifted
cores as common `k+1` bases for `f` and `g`, and the residual-slope check
certifies the cancellation formula on all `67` noncontained lifted faces.

The arbitrary `F_17`, `j=4`, `t=2` rank-one probe has `176` aperiodic locators,
all `17` slopes, and `16` zero-determinant slices.  Four of those zero slices
have rank-one direction pencil; the verifier classifies all zero slices in the
probe as constant-slope, and the residual maximum strict degree is again
`4=j`.  The probe also performs `360` companion-map checks on its nonzero
quadratic edge slices and has `24` residual triangles, all top-type.  Its
top-packet ledger has `17` packets: `3` large packets and `14` pair packets,
with maximum packet size `5`, accounting for `40` residual edges and `24`
triangles, with maximum top-packet incidence again `1`, so the audited top
packets are disjoint.  The common-anchor check certifies all `80=2*40`
oriented residual edge endpoints in the probe.  The residual anchor ledger
splits the `69` residual locators into `44` lifted-core residual faces and
`25` isolated anchor escapes: `4` with `beta_0=0`, `19` with `xi_T in T`, and
`2` with `xi_T notin D`.  The `65` finite residual-anchor lifts split as `44`
squarefree in-domain, `19` repeated-root, and `2` off-domain boundary lifts;
the remaining `4` escapes are infinity anchors.  The `16` residual slopes
split as `16` lifted-core slopes and `16` escape slopes, with complete overlap
between the two sources in this probe; the lifted-core residual slope fiber
max is again `1`, checked across `40` residual face-pairs.  The lifted
denominator gate is
checked on all `17` residual top packets, with `42` omitted-root anchor checks.
The common lifted numerator gate has the same `17` packet checks and `42`
numerator anchor checks.  Across all `85=17*5` lifted `j`-faces in the probe,
`84` are noncontained, `81` are aperiodic, `42` remain residual, and `39` are
aperiodic faces removed by root-slice peeling.  These are exactly the profile
quantities a packing proof must shrink or explain structurally.  The full
lifted-common-core census in the probe has `31` cores: `17` are residual
packets, `2` have exactly one residual face, and the others have no residual
faces after the quotient and root-slice charges.  These `31` lifted cores are
all common `k+1` bases for `f` and `g`, and the verifier checks the
residual-coordinate slope formula on all `140` noncontained lifted faces.

This is an audit/verifier for the M1 target, not a proof of the desired
polynomial all-line bound.  Its purpose is to make future counterexample-first
work precise: a claimed obstruction should now say whether its split locators
are contained/tangent, quotient-periodic, or genuinely aperiodic in this
Hankel-pencil ledger.
