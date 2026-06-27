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

## Root Slices As A Higher-Slack Core Pencil

The root-slice slope set is itself a standard Hankel-pencil slope image one
degree lower.  For a `(j-1)`-core `R`, let `ell_R` be the locator vector of
`L_R`, and define

```text
Z_3 =
  {z : exists R subset D, |R|=j-1,
       (H_{3,j-1}(u)+zH_{3,j-1}(v))ell_R=0,
       H_{3,j-1}(v)ell_R != 0}.
```

Then

```text
Z_root subset Z_3.                                      (RS3)
```

Indeed, a root-slice packet for `(R,z)` satisfies

```text
(H_{2,j}(u)+zH_{2,j}(v))p_R=0,
(H_{2,j}(u)+zH_{2,j}(v))s_R=0,
```

where `p_R` is `L_R` padded to degree `j` and `s_R` is the coefficient vector
of `X L_R`.  The first equation gives the shift-`0` and shift-`1` Hankel
relations for `L_R`; the second gives the shift-`1` and shift-`2` relations.
Together they are exactly

```text
(H_{3,j-1}(u)+zH_{3,j-1}(v))ell_R=0.
```

The denominator three-row vector cannot vanish for a genuine peeled
root-slice packet: if `H_{3,j-1}(v)ell_R=0`, then every member
`R union {x}` of the slice has `H_{2,j}(v)ell_{R union {x}}=0`, so the whole
slice is contained and contributes no noncontained aperiodic slope.

Thus the `Z_root` term in the slack-two reduction can be replaced by the
higher-slack core-locator image `Z_3`.  This turns the same-slope part of the
`t=2` problem into a recursive or inductive input rather than an independent
packet count.

## Arbitrary-Slack Same-Slope One-Exchange Lift

The root-slice lift is not special to `t=2`; only the later quadratic
different-slope analysis is.  Fix any slack `t>=1`, a slope `z`, and put

```text
A_z = H_{t,j}(u)+zH_{t,j}(v).
```

Let `R subset D` have size `j-1`, and suppose two distinct one-root extensions
`R union {x}` and `R union {y}` have the same noncontained slope `z`.  With

```text
ell_{R union {w}} = s_R-wp_R,
```

the two equations

```text
A_z(s_R-xp_R)=0,        A_z(s_R-yp_R)=0
```

again imply

```text
A_z p_R=0,        A_z s_R=0.
```

The padded equation gives the shift-`0` through shift-`t-1` Hankel relations
for `L_R`; the shifted equation gives shift-`1` through shift-`t`.  Together
they are exactly

```text
(H_{t+1,j-1}(u)+zH_{t+1,j-1}(v))ell_R=0.        (RS(t))
```

The denominator vector in this `(t+1,j-1)` pencil cannot vanish for a genuine
same-slope one-exchange edge, because if `H_{t+1,j-1}(v)ell_R=0` then every
member `R union {w}` of the root slice has
`H_{t,j}(v)ell_{R union {w}}=0`, contradicting noncontainment at the two
endpoints.  Therefore every same-slope one-exchange collision at slack `t`
is charged to the next-slack core-locator slope image.

This does not handle all strict overlaps when `t>2`; pairs differing in two
or more roots are new higher-slack objects.  It does prove that the
one-exchange same-slope part is recursively exact at every slack, so repeated
one-root collision structure never needs a separate nonrecursive budget.  The
verifier audits this general lift on every row.  In the nontrivial
`F_13`, `n=12`, `j=7`, `t=3` row, the same-slope strict pairs are precisely
the `30` one-exchange pairs, and they are covered by `2` root slices with one
slope value in the `t=4`, `j=6` core-locator image.

## Two-Exchange Quadratic Determinantal Slices

The first strict-overlap structure not covered by one-exchange root slices
appears at `t=3`: two complements may differ by two roots.  Fix a common
core `R subset D` of size `j-2`, and write

```text
L_R(X)=c_0+c_1X+...+c_{j-2}X^{j-2}.
```

For a two-root extension `{x,y}`, put

```text
s=x+y,        p=xy.
```

Then

```text
L_{R union {x,y}}(X)=L_R(X)(X^2-sX+p).
```

If `e_0,e_1,e_2` are the coefficient vectors of
`L_R, X L_R, X^2 L_R`, padded to length `j+1`, then

```text
ell_{R union {x,y}} = e_2 - s e_1 + p e_0.          (TE1)
```

Consequently, for each syndrome direction `w`,

```text
H_{3,j}(w)ell_{R union {x,y}}
 = W_2 - s W_1 + p W_0,
W_i = H_{3,j}(w)e_i.                                (TE2)
```

Thus the `t=3` projective slope gate on a fixed two-exchange core is a
determinantal locus in the two elementary coordinates `(s,p)`.  Writing

```text
A_i=H_{3,j}(u)e_i,        B_i=H_{3,j}(v)e_i,
```

a finite noncontained slope exists exactly when `B_2-sB_1+pB_0` is nonzero
and all three `2x2` minors of the two vectors

```text
A_2-sA_1+pA_0,        B_2-sB_1+pB_0
```

vanish.  Each minor is a quadratic polynomial in `(s,p)`.  For any pair of
coordinates `(r,c)`, its coefficients are

```text
det(A_2,B_2)
 - s[det(A_1,B_2)+det(A_2,B_1)]
 + p[det(A_0,B_2)+det(A_2,B_0)]
 + s^2 det(A_1,B_1)
 - sp[det(A_1,B_0)+det(A_0,B_1)]
 + p^2 det(A_0,B_0).                                (TE3)
```

This is the two-exchange analogue of the one-root quadratic slice, but it is
not yet a packing bound: the common zero set of three quadrics in the
pair-symmetric plane can still have structured components.  Its value is that
the next higher-slack obstruction is now a concrete low-degree determinantal
slice, rather than an arbitrary set of two-root exchanges.

The verifier checks (TE1), (TE2), and the quadratic-minor certificate (TE3) on
every `t=3` row.  In the `F_13`, `n=12`, `j=7`, `t=3` audit row, the largest
seed has `42` strict pairs: `30` same-slope one-exchange pairs handled by the
root-slice lift above, and `12` two-exchange pairs.  All `12` two-exchange
pairs are different-slope and lie in the audited quadratic determinantal
slices.

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

## Residual Slope-Fiber Packing Bound

The residual one-exchange independence gives a global multiplicity bound
inside every residual slope fiber.  Fix a residual slope `z` and let

```text
F_z={T in R_res : z_T=z}.
```

If two distinct complements `T,T' in F_z` shared a `(j-1)`-core, then they
would be same-slope strict one-exchange neighbors in the residual family,
contradicting the root-slice peeling corollary.  Hence each `(j-1)`-subset of
the domain occurs in at most one member of `F_z`.  Counting incidences
`(R,T)` with `R subset T`, `|R|=j-1`, gives

```text
|F_z| j <= binom(n,j-1).
```

This is a fiber-multiplicity theorem, not a slope-image theorem: it bounds how
many residual locators can carry one fixed slope, but it does not yet bound
the number of nonempty residual slope fibers.

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

## Homogeneous Projective Residual Lift Ledger

Every residual locator has a projective lift into the same common one-row
Hankel kernel.  For a residual locator `T`, write

```text
H_{2,j}(v)ell_T=(beta_0,beta_1),        H_{2,j}(u)ell_T=(alpha_0,alpha_1).
```

Let `s_T` be the coefficient vector of `X L_T`, and let `p_T` be the
coefficient vector of `L_T` padded to degree `j+1`.  Since `T` is residual
and noncontained, `(beta_0,beta_1) != 0`.  Put

```text
[xi:eta]=[beta_1:beta_0] in P^1(F).
```

Then the homogeneous projective lift

```text
ell_T^proj = eta s_T - xi p_T
```

satisfies both one-row gates

```text
H_{1,j+1}(v)ell_T^proj=0,        H_{1,j+1}(u)ell_T^proj=0.        (PL1)
```

Indeed the denominator identity is `eta beta_1-xi beta_0=0`, and the numerator
identity is `eta alpha_1-xi alpha_0=0`, which follows from the residual
determinant gate.

Moreover this projective lift is unique.  The full projective one-root pencil
over `T` is

```text
{ eta s_T - xi p_T : [xi:eta] in P^1(F) }.
```

Its denominator one-row condition is the single homogeneous equation

```text
eta beta_1 - xi beta_0 = 0.
```

Because `T` is residual and noncontained, `(beta_0,beta_1) != 0`, so this
equation cuts out exactly one point of `P^1(F)`, namely
`[xi:eta]=[beta_1:beta_0]`.  The residual determinant gate then makes the same
point satisfy the numerator one-row condition.  Thus a residual locator has
exactly one projective lifted-kernel anchor.

When `eta != 0`, this is a nonzero scalar multiple of
`L_T(X)(X-xi_T)`, where `xi_T=xi/eta=beta_1/beta_0`.  Thus finite anchors
split into three lifted types:

1. `xi_T in D\T`: a squarefree in-domain lifted common core;
2. `xi_T in T`: a repeated-root degenerate lift, hence an isolated escape;
3. `xi_T notin D`: an off-domain finite lift, hence an isolated escape.

If `beta_0=0`, then residual noncontainment gives `beta_1 != 0`, and the
lift is the padded vector `L_T` itself, up to a nonzero scalar.  Thus
beta0-zero escapes are exactly the infinity-anchor boundary of the same
projective lift ledger.  Consequently the isolated escape side is not an
unstructured remainder: it consists of repeated-root, off-domain, and
infinity-anchor boundary lifts inside the common projective one-row kernel.

## Repeated And Infinity Anchor One-Row Forms

The other two boundary escape types also have pinned one-row descriptions.
First consider a repeated-root escape, so the finite anchor `xi_T=xi` lies in
`T`.  Put

```text
P_T(X)=(X-xi)L_T(X),
```

which has a double root at `xi`.  As above,

```text
H_{1,j+1}(u)P_T=H_{1,j+1}(v)P_T=0.
```

Although the twist by `(X-xi)^{-1}` has a pole at `xi in D`, the polynomial
`P_T` vanishes at `xi`, so its value there is irrelevant in the one-row
pairing.  Define the domain-pole twist by assigning any value at `xi` and
using

```text
u^xi(x)=u(x)/(x-xi),        v^xi(x)=v(x)/(x-xi)        (x != xi).
```

Then

```text
H_{1,j+1}(u^xi)P_T=(H_{2,j}(u)L_T)_0,
H_{1,j+1}(v^xi)P_T=(H_{2,j}(v)L_T)_0.
```

The repeated-root escape has `(H_{2,j}(v)L_T)_0 != 0`, and its slope is again
the pinned one-row twisted slope

```text
z_T=-H_{1,j+1}(u^xi)P_T/H_{1,j+1}(v^xi)P_T.        (RA1)
```

For an infinity escape, `beta_0=0`, so the padded locator `L_T` itself lies in
the common one-row kernel:

```text
H_{1,j}(u)L_T=H_{1,j}(v)L_T=0.
```

Residual noncontainment gives `beta_1 != 0`, and the determinant gate forces
`alpha_0=0`.  Hence the slope is determined by the shifted one-row quotient

```text
z_T=- (H_{2,j}(u)L_T)_1 / (H_{2,j}(v)L_T)_1.        (IA1)
```

Equivalently, `H_{1,j}(u^+ + z_T v^+)L_T=0`, where `u^+_m=u_{m+1}` and
`v^+_m=v_{m+1}`.  Thus every isolated escape type is now a pinned one-row
object:

```text
off-domain anchor     -> external-pole twisted one-row fiber;
repeated anchor       -> domain-pole twisted one-row fiber with double root;
infinity anchor       -> shifted one-row fiber at infinity.
```

The verifier asserts (RA1) for every repeated-root escape and (IA1) for every
infinity escape, in addition to the off-domain twisted identity (EA1).

## Projective Lift-Fiber Ledger

The projective lift map has no hidden multiplicity beyond the squarefree
in-domain common cores.  Let

```text
Phi(T) = [eta s_T - xi p_T],
```

where `[xi:eta]=[beta_1:beta_0]` is the unique projective anchor of the
residual locator `T`.  Then the fibers of `Phi` are exactly as follows.

First, every boundary lift is a singleton fiber.  If the anchor is already in
`T`, then the lifted polynomial has one repeated root and its distinct
`D`-roots recover `T`.  If the finite anchor is outside `D`, then the `D`-root
set of the lift is again exactly `T`.  If the anchor is infinity, then the
lift is the padded locator `L_T`, so `T` is recovered from its finite roots.

Second, a nontrivial fiber can only be a squarefree in-domain lifted core
`W subset D` of size `j+1`.  In that case the possible residual preimages are
the `j`-faces `W\{x}` which survive the quotient and root-slice charges.
Consequently the residual strict one-exchange graph is exactly the disjoint
union of cliques on the non-singleton squarefree projective lift fibers:

```text
E_res = disjoint union over Phi-fibers F of binom(F,2).
```

This reformulates the remaining M1 packing problem one level higher.  Boundary
projective lifts can only contribute isolated slopes, while every residual
edge and every residual top packet comes from a squarefree in-domain fiber of
the unique projective lifted-kernel map.

## Boundary-Only Counterexample To Squarefree Absorption

The boundary side cannot simply be absorbed into the squarefree lifted-core
side.  The verifier includes a deterministic `F_13`, `n=12`, `j=4`, `t=2`
cyclic-domain row where, after quotient and root-slice charges, the residual
family has no squarefree projective lift fibers and no lifted common cores, but
still has a nonempty residual slope image.

In each seed of this row, all `24` residual locators are off-domain
projective boundary singleton fibers, the squarefree lifted slope image is
empty, and the `6` residual slopes are all new boundary slopes:

```text
Z_lift = empty,        |Z_esc|=|Z_res|=6.
```

Thus the projective lift-fiber reduction has two genuinely necessary terms:
squarefree in-domain fibers and boundary singleton fibers.  A proof of M1 may
bound the two terms by different arguments, but it cannot close the residual
slope image by discarding or absorbing the boundary term into the squarefree
one.

## External-Anchor Counterexample To Anchor Counting

The boundary singleton term cannot simply be bounded by the number of
off-domain anchors either.  For a finite off-domain boundary locator, write
`xi_T=beta_1/beta_0 in F\D` for its external projective anchor.  In the same
`F_13`, `n=12`, `j=4`, `t=2` row, every residual locator has the same external
anchor `xi_T=0`.

Thus all `24` residual boundary singleton locators are concentrated over one
external anchor, there are still no squarefree lifted cores or lifted slopes,
and the residual slope image has size `6`:

```text
#{xi_T : T residual boundary} = 1,        |Z_esc|=|Z_res|=6.
```

Consequently the boundary part in Przemek's all-line aperiodic residue-packing
target needs a slope-image bound per external anchor, not only a count of the
external anchors themselves.  The verifier asserts this concentration in the
boundary-only row: one external anchor, `24` locators on that anchor, and `6`
distinct residual slopes on that same anchor.

## External-Anchor Twisted One-Row Reduction

There is still useful structure inside a fixed external anchor.  Fix
`xi in F\D`, and let `T` be a residual off-domain boundary locator with
anchor `xi_T=xi`.  Put

```text
P_T(X) = (X-xi)L_T(X).
```

Then the projective lift ledger gives the two one-row common-kernel equations

```text
H_{1,j+1}(u)P_T = 0,        H_{1,j+1}(v)P_T = 0.
```

Now twist the line values on the domain by the external pole:

```text
u^{xi}(x)=u(x)/(x-xi),        v^{xi}(x)=v(x)/(x-xi),        x in D.
```

Since `xi notin D`, this is well-defined.  If

```text
H_{2,j}(u)L_T=(alpha_0,alpha_1),
H_{2,j}(v)L_T=(beta_0,beta_1),
```

then the identities `P_T=(X-xi)L_T` give

```text
H_{1,j+1}(u^{xi})P_T = alpha_0,
H_{1,j+1}(v^{xi})P_T = beta_0.
```

The residual off-domain case has `beta_0 != 0`, so its original bad slope is
exactly the one-row twisted slope

```text
z_T = -alpha_0/beta_0
    = -H_{1,j+1}(u^{xi})P_T / H_{1,j+1}(v^{xi})P_T.        (EA1)
```

Conversely, for a `j`-subset `T subset D` and fixed `xi notin D`, the two
untwisted one-row equations for `P_T=(X-xi)L_T`, together with
`H_{1,j+1}(v^{xi})P_T != 0`, imply the original `t=2` determinant gate and
the slope formula above.  Thus the per-external-anchor boundary term reduces
to a one-row twisted slope-image problem over external-root lifted locators.

This is the first structural replacement for anchor counting: after the
quotient, tangent, and root-slice charges, one must bound the image of (EA1)
for each fixed external pole `xi`, not merely count how many such poles occur.

## Fixed-Anchor Slope-Fiber Reduction

The fixed external-anchor term can be made one step more explicit.  Fix
`xi in F\D` and a finite slope `z`.  For an off-domain residual locator
`T`, put `P_T=(X-xi)L_T` as above.  Then `T` lies over the fixed
anchor-slope pair `(xi,z)` if and only if `P_T` is a degree `j+1` polynomial
with pinned root `xi`, all other roots in `D`, and

```text
H_{1,j+1}(u)P_T = 0,
H_{1,j+1}(v)P_T = 0,
H_{1,j+1}(u^xi+zv^xi)P_T = 0,
H_{1,j+1}(v^xi)P_T != 0,              (EA1F)
```

with the usual residual filters: noncontained, not quotient-periodic, and not
removed by a fixed-slope root slice.  The first two equations say that the
projective lift is in the common one-row Hankel kernel; the third equation is
the pinned twisted `t=1` incidence for the slope `z`; and the last inequality
keeps the slope finite and noncontained in the twisted one-row reduction.

Thus the isolated off-domain boundary image is exactly the set of slopes for
which one of these pinned split-locator fibers is nonempty:

```text
Z_ext(xi) = { z : F_{xi,z} != empty }.
```

This does not yet bound `|Z_ext(xi)|`; the `F_13` boundary model shows that a
single external anchor can have several nonempty slope fibers, and each slope
fiber can contain several locators.  In that row, all off-domain locators have
`xi=0`, and the verifier splits the `24` locators into exactly six
anchor-slope fibers of size four.  Its value is that the remaining boundary
problem is now a concrete pinned one-row split-locator fiber problem, rather
than an unstructured collection of isolated residual locators.

There is also a clean packing bound inside each fixed anchor-slope fiber.
Since off-domain projective boundary fibers are isolated components of the
residual one-exchange graph, two distinct locators in the same `F_{xi,z}`
cannot differ by one exchange.  Equivalently, no `(j-1)`-subset of `D` is
contained in two different complements `T` in that fiber.  Counting
`(T,R)` with `R subset T`, `|R|=j-1`, gives

```text
|F_{xi,z}| * j <= binom(n,j-1).        (EA1P)
```

In support language, the corresponding `(k+2)`-point supports form a packing:
no `(k+1)`-point support is contained in two members of the same fixed
anchor-slope fiber.  This is a multiplicity bound for one fiber, not a bound
on the number of nonempty slope fibers.  The remaining task is still to bound
how many slopes `z` have `F_{xi,z} != empty`.

## Fixed-Anchor Rich-Point Arrangement

The fixed-anchor problem has an exact projective-incidence form.  Fix
`xi in F\D` and let `V_xi` be the vector space of degree `<=j+1`
coefficient vectors `P` satisfying

```text
P(xi)=0,        H_{1,j+1}(u)P=0,        H_{1,j+1}(v)P=0.
```

For each domain point `x in D`, let

```text
R_x={ [P] in P(V_xi) : P(x)=0 }
```

be the corresponding root hyperplane in the projective common kernel.  Since a
nonzero `P in V_xi` already has the root `xi`, it can vanish on at most `j`
points of `D` unless it is zero.  Thus the fixed-anchor split locators are
exactly the `j`-rich points of this arrangement:

```text
T subset D, |T|=j, P=(X-xi)L_T
        <->  [P] in P(V_xi) lying on the j hyperplanes {R_x : x in T}.
```

On these rich points the slope map is the projective linear ratio

```text
[P] -> - H_{1,j+1}(u^xi)P / H_{1,j+1}(v^xi)P,
```

with the finite-slope condition `H_{1,j+1}(v^xi)P != 0`.  The residual
off-domain boundary term is therefore not an arbitrary collection of isolated
locators: it is the image, after quotient/root-slice residual filters, of the
`j`-rich points in a root-hyperplane arrangement inside `P(V_xi)`.

This is the incidence form of the remaining fixed-anchor M1 task.  In the
`F_13`, `n=12`, `j=4` boundary row, the single anchor `xi=0` has
`dim V_xi=4`, hence `|P(V_xi)|=2380`; among these projective points there are
`39` four-rich points and `9` finite rich slopes.  Quotient charging removes
the antipodal family, leaving the `24` residual rich points and `6` residual
slopes recorded in the product model.

## Low-Dimensional Fixed-Anchor Pencils

The fixed-anchor arrangement is already controlled when `dim V_xi <= 2`.
If `dim V_xi=1`, then `P(V_xi)` is a single point, so there is at most one
rich point and at most one finite slope.

Now suppose `dim V_xi=2`, so `P(V_xi)` is a projective line.  Let

```text
r_xi = #{x in D : P(x)=0 for every P in V_xi}
```

be the number of fixed domain roots of the pencil.  Necessarily `r_xi<j`;
otherwise every polynomial in the pencil would be divisible by
`(X-xi)prod_{x in R}(X-x)` with `|R|=j`, a degree `j+1` polynomial, forcing
`dim V_xi=1`.

For every non-fixed `x in D`, the condition `P(x)=0` is a nonzero linear
condition on the two-dimensional space `V_xi`, hence it selects exactly one
projective point of the pencil.  Therefore two distinct rich points cannot
use the same non-fixed domain root.  Since each `j`-rich point already has the
`r_xi` fixed roots and must use at least `j-r_xi` non-fixed roots, the rich
points are bounded by

```text
#{j-rich points in P(V_xi)} <= floor((n-r_xi)/(j-r_xi)).        (EA1L)
```

The finite fixed-anchor slope image is no larger than the set of rich points,
so it satisfies the same bound.  Thus low-dimensional external-anchor
kernels do not contribute an uncontrolled boundary term; the remaining
fixed-anchor difficulty starts at projective dimension at least two, i.e.
`dim V_xi >= 3`.

## Fixed-Anchor Projective-Plane Bound

The first higher-dimensional case, `dim V_xi=3`, is still polynomially
controlled.  Then `P(V_xi)` is a projective plane.  Let `r_xi` be the number
of fixed domain roots, and put

```text
s = j-r_xi.
```

As before `s>0`.  For each non-fixed `x in D`, the condition `P(x)=0` is a
projective line in `P(V_xi)`.  Several domain roots may define the same root
line; let `w(L)` be the number of non-fixed roots producing a root line `L`,
and let `M` be the number of distinct non-fixed root lines.

No root line can have weight greater than `s`, since every point of that line
would then vanish at `xi`, the `r_xi` fixed roots, and more than `s`
additional domain roots, exceeding degree `j+1`.  Call a root line heavy if
`w(L)=s`, and let `h` be the number of heavy lines.  Points on a heavy line
are already `j`-rich, and the slope map restricted to that projective line is
a ratio of two linear forms, so it has at most `|F|+1` values.

Every remaining rich point is not on a heavy line.  It must therefore collect
its `s` non-fixed roots from at least two distinct root lines, hence is the
intersection point of a pair of distinct root lines.  Thus

```text
#{j-rich points}, |finite slope image|
    <= h(|F|+1) + binom(M,2)
    <= floor((n-r_xi)/s)(|F|+1) + binom(n-r_xi,2).        (EA1P2)
```

This closes the fixed-anchor projective-plane case in the polynomial-field
window.  The first fixed-anchor arrangement case not handled by the line and
plane incidence reductions is therefore `dim V_xi>=4`, exactly where the
`F_13` boundary row sits.

## Fixed-Anchor Three-Space Bound

The next case, `dim V_xi=4`, is also controlled by an incidence decomposition.
Now `P(V_xi)` is a projective three-space, and each non-fixed domain root
defines a projective plane.  Keep `s=j-r_xi>0`, let `M` be the number of
distinct non-fixed root planes, and write `w(H)` for the total root weight of
a root plane `H`.

No root plane has `w(H)>s`, by the same degree argument.  Let `h_2` be the
number of heavy planes with `w(H)=s`; each heavy plane consists entirely of
rich points and has `|F|^2+|F|+1` projective points.

For root planes which do not already account for the point through one heavy
plane, consider projective lines obtained as pairwise intersections of root
planes.  Let a line be heavy if the total weight of all root planes containing
it is at least `s`, and let `h_1` be the number of such lines.  Every point on
a heavy line is rich, and each line has `|F|+1` projective points.

It remains to consider a rich point not on a heavy plane or a heavy line.  The
root planes through it have total weight at least `s`, but no one-dimensional
or two-dimensional span of their defining linear forms already has weight
`>=s`.  Therefore those forms span dimension at least three, so some triple
of root planes cuts out that point.  Hence the residual rich points are
covered by triple intersections of distinct root planes.  This gives

```text
#{j-rich points}, |finite slope image|
    <= h_2(|F|^2+|F|+1) + h_1(|F|+1) + binom(M,3).        (EA1P3)
```

Thus fixed-anchor kernels of dimension four are still polynomially bounded in
the field-size window.  The next issue is either higher-dimensional
fixed-anchor kernels or sharpening these polynomial bounds to the exact
reserve scale needed by a final M1 theorem.

## Rank-Stratified Fixed-Anchor Cover

The same incidence argument has a dimension-free form.  Let
`d=dim V_xi`, let `s=j-r_xi>0`, and let the distinct non-fixed root
hyperplanes in `P(V_xi)` have weights `w(H)`.  For a rank-`q` rowspace `U`
spanned by root hyperplanes, define its weight by

```text
W(U)=sum_{H subset U} w(H),
```

where `H subset U` means that the linear form defining `H` lies in `U`.  Call
`U` heavy if `W(U)>=s`, and let `h_q` be the number of heavy rank-`q`
rowspaces.

Every `j`-rich point is covered by this heavy-flat ledger.  Indeed, the root
hyperplanes through a projective point have total weight at least `s`; their
linear forms lie in the annihilator of that point, hence span rank at most
`d-1`.  Their span is a heavy rowspace `U`, and the point lies in the
projective flat cut out by `U`, which has

```text
(|F|^(d-q)-1)/(|F|-1)
```

points.  Therefore

```text
#{j-rich points}, |finite slope image|
  <= sum_{q=1}^{d-1} h_q (|F|^(d-q)-1)/(|F|-1)
  <= sum_{q=1}^{d-1} binom(M,q) (|F|^(d-q)-1)/(|F|-1).        (EA1R)
```

This is intentionally cruder than the low-dimensional bounds above, because
it counts whole heavy flats.  Its use is structural: fixed-anchor escapes are
always controlled by a concrete hyperplane-arrangement rank ledger.  The sharp
M1 work is therefore to prove that the relevant fixed-anchor dimensions and
quotient-aware heavy-flat counts fit the final reserve, not to find a new
kind of boundary escape outside the Hankel-pencil arrangement.

## All Boundary Anchor Arrangement Reduction

The repeated-root and infinity one-row forms put the whole isolated escape
term in the same incidence language as the off-domain fixed-anchor term.  The
three boundary arrangement spaces are:

```text
V_ext(xi) = {P deg <= j+1 : P(xi)=0,
             H_{1,j+1}(u)P=H_{1,j+1}(v)P=0},        xi in F\D;

V_rep(xi) = {P deg <= j+1 : P(xi)=P'(xi)=0,
             H_{1,j+1}(u)P=H_{1,j+1}(v)P=0},        xi in D;

V_inf     = {L deg <= j : H_{1,j}(u)L=H_{1,j}(v)L=0}.
```

For `V_ext(xi)` the split points are the `j`-rich points among the root
hyperplanes `P(x)=0`, `x in D`, and the slope map is the external-pole
twisted ratio from (EA1).  For `V_rep(xi)`, the double root at `xi` is already
built into the space, so a repeated-root escape with anchor `xi` is a
`(j-1)`-rich point for the root hyperplanes indexed by `D\{xi}`; its slope is
the domain-pole twisted ratio (RA1).  For `V_inf`, the split points are the
`j`-rich points for `L(x)=0`, `x in D`, and the slope map is the shifted
ratio (IA1).

Thus the isolated boundary slope image is covered by the three arrangement
slope images

```text
Z_esc subset
    (union_{xi in F\D} Z_ext(xi))
    union (union_{xi in D} Z_rep(xi))
    union Z_inf,                                      (BA1)
```

If `Z_ext`, `Z_rep`, and `Z_inf` are defined with the residual filters
included, namely noncontained, not quotient-periodic, and not removed by a
fixed-slope root slice, then (BA1) is an equality.  The value of (BA1) is that
every isolated escape is now a rich-point slope image inside a linear
projective kernel.  There is no fourth unstructured boundary class.

The rank-stratified cover (EA1R) applies verbatim to each of these three
arrangements.  If `m` is the required richness (`j` for `V_ext`, `j-1` for
`V_rep`, and `j` for `V_inf`), `r` is the number of fixed domain roots in the
relevant root domain, and `s=m-r`, then every rich point is covered by a
heavy rowspace generated by root hyperplanes.  Hence its rich-point count and
finite slope image are bounded by

```text
sum_{q=1}^{d-1} h_q (|F|^(d-q)-1)/(|F|-1),
```

with `d` the dimension of the corresponding boundary kernel.  The verifier
now asserts this arrangement containment and rank-stratified cover for
repeated-root and infinity escapes, in addition to the earlier external-anchor
checks.

Define `B_arr(V,m)` to be this rank-stratified bound for a boundary
arrangement with kernel `V` and required richness `m`.  For the active
residual boundary anchors put

```text
B_boundary =
    sum_{xi in F\D active} B_arr(V_ext(xi),j)
  + sum_{xi in D active}   B_arr(V_rep(xi),j-1)
  +                         B_arr(V_inf,j)        if infinity is active.
```

Then (BA1) gives the explicit escape bound

```text
|Z_esc| <= B_boundary.                         (BA2)
```

Combining (BA2) with the lifted-side recursion and the higher-slack
root-slice reduction gives the audited all-line slack-two bound

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_common + B_boundary.       (M1R4)
```

This is not yet the final M1 reserve-scale theorem: `B_boundary` may still be
too crude if it counts large heavy flats.  Its role is to replace the
unstructured escape term by a single explicit arrangement budget.  The
remaining boundary work is now to prove quotient-aware or dimension-sensitive
savings for `B_boundary`.

There is one immediate sharpening: for slope counts, a heavy flat need not be
charged by all of its projective points.  The slope map on every boundary
arrangement is the ratio of two linear forms, hence its image on a projective
flat has size at most `|F|+1`, and at most one value if the flat is a single
point.  Replacing each heavy rank-`q` flat contribution

```text
(|F|^(d-q)-1)/(|F|-1)
```

by

```text
min((|F|^(d-q)-1)/(|F|-1), |F|+1)
```

gives a slope-image budget `B_boundary^slope` with

```text
|Z_esc| <= B_boundary^slope <= B_boundary,          (BA3)
```

and therefore

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_common
                         + B_boundary^slope.       (M1R5)
```

This refinement is invisible in rows where all heavy flats are points or
projective lines, but it prevents higher-dimensional heavy planes and larger
flats from being charged by their full point count.

## Polynomial-Field Boundary Closure

There is also a coarser but more global boundary consequence.  Let
`A_boundary` be the number of active projective boundary anchors after the
quotient, tangent/contained, and root-slice charges:

```text
A_boundary =
    #{xi in F\D : Z_ext(xi) nonempty}
  + #{xi in D   : Z_rep(xi) nonempty}
  + 1_{Z_inf nonempty}.
```

For each fixed boundary anchor, the corresponding escape slopes are the image
of a projective linear ratio on a subset of one projective kernel.  Hence one
anchor contributes at most `|F|+1` projective slope values, and therefore at
most `|F|+1` finite values.  Since the possible finite off-domain anchors,
repeated anchors, and the infinity anchor together number at most `|F|+1`,

```text
|Z_esc| <= (|F|+1)A_boundary <= (|F|+1)^2.        (BA4)
```

Combining (BA4) with the recursive slack-two reduction gives

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_common
                         + (|F|+1)A_boundary
                       <= |Z_3| + (j+1)N_common
                         + (|F|+1)^2.             (M1R6)
```

Thus in the polynomial-field window `|F| <= n^C`, the isolated boundary term
is automatically polynomial in `n`.  The remaining nontrivial M1 inputs for a
polynomial all-line packing theorem are then the higher-slack slope image
`Z_3` and the one-row/common-base term `N_common`; sharper boundary-arrangement
work is only needed for reserve-scale constants or for field-size regimes not
controlled by `|F|=poly(n)`.

The field-size factor in (BA4) is real.  The full-domain monomial boundary
families below have one active external anchor carrying all nonzero slopes for
infinite prime families, so no q-independent `O(A_boundary)` escape theorem
can hold after quotient charging.

## External-Anchor Top-Coefficient Form

The twisted one-row reduction has an equivalent interpolation form.  Let
`B=D\T`, so `|B|=k+2`, and write `R_{y,B}` for the unique polynomial of
degree `< k+2` agreeing with a word `y` on `B`.  Put

```text
R_{y,B}(X) = c_{k+1}(y,B)X^{k+1}+c_k(y,B)X^k+...
```

For the external lift `P_T=(X-xi)L_T`, the first row of the original
two-row Hankel product is the top coefficient

```text
(H_{2,j}(y)L_T)_0 = c_{k+1}(y,B).
```

Indeed, for `x in B`,
`lambda_D(x)L_T(x)=1/Q_B'(x)`, where `Q_B(X)=prod_{b in B}(X-b)`;
this is the usual Lagrange formula for the leading coefficient of
`R_{y,B}`.  The anchor equation
`(H_{2,j}(y)L_T)_1=xi(H_{2,j}(y)L_T)_0` is therefore exactly

```text
c_k(y,B) = (xi - sum_{b in B} b)c_{k+1}(y,B).        (EA2)
```

Thus an off-domain anchor forces the top two interpolation coefficients of
both line directions to be locked with the same scalar.  The bad slope

```text
z_T = -c_{k+1}(u,B)/c_{k+1}(v,B)
```

cancels `c_{k+1}` and then cancels `c_k` automatically by (EA2).  Hence
`u+z_T v` has degree `< k` on `B`.  The verifier checks this coefficient
identity and the resulting degree drop for every off-domain residual locator.

## Full-Domain Monomial Boundary Family

The product model is an instance of a general full-domain boundary family.
Let `D=F_p^*`, take `t=2`, and let `T subset D` have size `j`.  For the
monomial directions

```text
u(X)=A X^{p-2-j},        v(X)=B X^{p-2},        A,B != 0,
```

the full-domain Lagrange weights give the syndrome rule

```text
sum_{x in F_p^*} lambda_D(x)x^m x^d =
  1  if m+d+1 == 0 mod p-1,
  0  otherwise.
```

Writing `L_T(X)=prod_{x in T}(X-x)`, the two Hankel products are therefore

```text
H_{2,j}(u)L_T = A(1, -sum_{x in T}x),
H_{2,j}(v)L_T = B((-1)^j prod_{x in T}x, 0).
```

Thus the determinant gate holds exactly on the zero-sum locus

```text
sum_{x in T} x = 0,
```

and every such locator has external anchor `xi=0` and product slope

```text
z_T = -A / (B(-1)^j prod_{x in T}x).        (EA3)
```

This family is a reusable floor model for any proposed fixed-external-anchor
bound: after quotient-periodic zero-sum locators are charged, the residual
boundary slope image is the product image of the remaining zero-sum
`j`-subsets.  The verifier audits this identity for the full-domain toy cases
`(p,j)=(13,4),(13,3),(17,4),(17,3)`.  The corresponding residual
product-image sizes after quotient charging are `6`, `4`, `16`, and `16`.

The product image has a built-in coset symmetry.  Multiplying all roots in
`T` by `lambda in F_p^*` preserves the zero-sum condition and sends

```text
prod(T) -> lambda^j prod(T).
```

It also preserves quotient-periodicity, since multiplication by `lambda`
translates exponent classes in the cyclic full-domain model.  Consequently
both the charged and residual product images are unions of cosets of the
`j`th-power subgroup `(F_p^*)^j`.  The verifier asserts this coset closure.
In the audited rows, the residual product images decompose as follows:

```text
(p,j)=(13,4):  |(F_p^*)^j|=3,   2 residual cosets;
(p,j)=(13,3):  |(F_p^*)^j|=4,   1 residual coset;
(p,j)=(17,4):  |(F_p^*)^j|=4,   4 residual cosets;
(p,j)=(17,3):  |(F_p^*)^j|=16,  1 residual coset.
```

More generally, the full zero-sum product image has a normalized
`(j-2)`-variable form.  Every zero-sum `j`-subset can be scaled and ordered as

```text
T = lambda {1,r_1,...,r_{j-2},-1-r_1-...-r_{j-2}},
```

where the displayed `j` elements are nonzero and pairwise distinct.  On this
allowed parameter set,

```text
prod(T) = lambda^j(-r_1...r_{j-2}(1+r_1+...+r_{j-2})).       (EA4)
```

Therefore the full zero-sum product image is exactly the `j`th-power closure
of this normalized product map.  The verifier asserts this uniform normal form
in every audited full-domain monomial row, and then checks the low-dimensional
specializations below.

The quotient-periodic part has its own exact product ledger.  Let `K_m` be
the multiplicative subgroup of `F_p^*` of size `m>1`, and suppose a locator is
a union of `c=j/m` whole `K_m`-cosets,

```text
T = union_{i=1}^c a_i K_m.
```

Each coset has sum zero, so every such quotient-periodic locator is
automatically on the zero-sum boundary locus.  Also

```text
prod_{x in aK_m} x = a^m prod_{x in K_m}x = (-1)^{m+1}a^m,
```

hence

```text
prod(T) = (-1)^{c(m+1)} prod_{i=1}^c a_i^m.        (EA5)
```

Thus a charged scale `m` contributes the `c`-subset product image inside the
`m`th-power subgroup `(F_p^*)^m`, with the displayed sign.  The verifier checks
this scale-by-scale product formula and the scale count

```text
binom((p-1)/m, j/m)
```

for every charged scale present in the audited rows.  These are scale-specific
ledgers: a locator can be periodic at more than one charged scale, so
scale-counts may overlap, while the charged locator ledger itself remains the
union of the charged scales.

For `j=3`, the normalized product-coset problem is one-dimensional.  Every
zero-sum triple can be scaled to

```text
T = lambda {1,r,-1-r}.
```

For `r in F_p^*`, the nonzero and distinctness conditions exclude

```text
r in {-1,1,-2,-1/2}.
```

For the remaining parameters,

```text
prod(T) = lambda^3(-r(1+r)).        (EA6)
```

Thus the full zero-sum product image is exactly the cube-closure of the
quadratic image `q(r)=-r(1+r)` on those allowed parameters.  The verifier
asserts this identity at the locator level and in aggregate product images.

This also identifies the size-`3` quotient charge in the triple case.  When
`3 | p-1` and the size-`3` quotient fibers are charged, the quotient-periodic
zero-sum triples are precisely the cosets `lambda mu_3` of the cube-root
subgroup, and their product image is the cube subgroup `(F_p^*)^3`.  This is a
locator charge, not a formal subtraction of product values: residual triples
may share a product value with a charged quotient triple in larger fields.  In
the audited `(p,j)=(13,3)` row there is no such overlap, so the active
size-`3` quotient charge leaves one residual cube coset.  In the audited
`(17,3)` row there is no size-`3` quotient charge and the cube map is
bijective, so the single external anchor already sees all `16` nonzero
products.

This gives an infinite field-size floor.  Suppose `p >= 11` and
`p == 2 mod 3`.  Then the cube map on `F_p^*` is bijective, and no size-`3`
quotient subgroup exists.  Since `{1,2,-3}` is a distinct nonzero zero-sum
triple, the zero-sum product image is nonempty.  Multiplying that triple by
`lambda` preserves zero-sum and multiplies the product by `lambda^3`; because
the cube map is onto, every nonzero product occurs.  There is no quotient
charge in size `3`, so the residual product image is all of `F_p^*`.

Consequently, for the monomial boundary line with `j=3`, one fixed external
anchor `xi=0` carries all `p-1` nonzero slopes for every prime
`p >= 11`, `p == 2 mod 3`.  The verifier audits this infinite-family theorem
at `p=11,17,23,29`.

When `p == 1 mod 3`, the size-`3` quotient family is present, but the residual
image is still field-sized for all `p >= 31`.  Let `H=(F_p^*)^3`, and fix a
cubic character `psi` with kernel `H`.  For a target cube coset `gamma H`,
the number of `r in F_p` with

```text
-r(1+r) in gamma H
```

is at least

```text
(p-2-2sqrt(p))/3.
```

Indeed, the two roots `r=0,-1` give the `p-2` main term, and the two
nontrivial cubic-character sums

```text
sum_r psi(-r(1+r)/gamma),     sum_r psi^2(-r(1+r)/gamma)
```

are each bounded by `sqrt(p)` by the degree-two multiplicative-character Weil
bound.  The forbidden normalized parameters are only

```text
r in {1,-2,-1/2,omega,omega^2},
```

where the first three give repeated roots and `omega,omega^2` give the charged
quotient triple.  Since `(p-2-2sqrt(p))/3 > 5` for `p>=31`, every cube coset
has a residual representative, hence the residual product image is all of
`F_p^*`.  The verifier audits the first saturated cases `p=31,37,43` and
records `p=19` as an additional small exception beyond the existing `(13,3)`
audit row; at `p=19`, the residual image has only `12` products.

For `j=4`, the normalized product image is a binary cubic modulo fourth
powers.  Every zero-sum four-subset can be scaled and ordered as

```text
T = lambda {1,r,s,-1-r-s}.
```

For `r,s in F_p^*`, the allowed parameter set is cut out by

```text
-1-r-s != 0,        |{1,r,s,-1-r-s}| = 4,
```

and on this set

```text
prod(T) = lambda^4(-rs(1+r+s)).       (EA7)
```

The ordered parameter count is

```text
p^2 - 9p + 26.
```

Equivalently, each scaling orbit of zero-sum four-subsets contributes `4!`
normalized ordered parameter pairs, which matches the closed count below.
Thus the full zero-sum product image is exactly the fourth-power closure of
the binary cubic image `c(r,s)=-rs(1+r+s)` on the allowed parameter set.  The
verifier asserts this identity in the `(13,4)` and `(17,4)` full-domain rows.

This cubic normal form is also the right way to interpret the antipodal
quotient charge.  The charged antipodal product image is the square subgroup,
but residual non-antipodal locators may still share product values with that
charged image.  Hence quotient charging is a locator-level ledger operation;
the residual boundary theorem must bound the product image of the locators
that remain, not subtract charged product values from the cubic image.

For `j=4`, the residual product image is in fact field-sized for every
prime `p >= 17` once the antipodal quotient family is charged.  We prove this
by a pair-product construction for large `p`, and audit the remaining finite
range.

Let

```text
A={x(1-x): x notin {0,1,1/2}}.
```

If `y=ab` with `a=x(1-x)` and `b=u(1-u)` in `A`, then

```text
T={x,1-x,-u,u-1}
```

has sum zero and product `y`.  It is residual unless the two pairs collide or
form the antipodal quotient family.  For fixed `y`, the number of ordered
parameter pairs `(x,u)` with

```text
x(1-x)u(1-u)=y,        x,u notin {0,1,1/2},
```

is at least `p-11-2sqrt(p)`.  To see this, let
`n(a)=1+chi(1-4a)-1_{a=1/4}` be the number of allowed `x` with
`x(1-x)=a`.  Expanding

```text
sum_{a in F_p^*} n(a)n(y/a)
```

leaves the main term `p-3`, the quadratic character convolution, and a
deliberately loose eight-point allowance for the two excluded repeated-root
fibers.  The convolution is bounded by the Hasse-Weil estimate for the
associated quadratic double cover:

```text
|sum_{a in F_p^*} chi((1-4a)(1-4y/a))| <= 2sqrt(p).
```

The collision or antipodal exclusions are bounded by `24` ordered pairs: they
force `u` to be one of the six affine functions
`-x,x+1,x-1,2-x,x,1-x`, and each resulting product equation has degree at most
`4` in `x`.  Since `p-11-2sqrt(p)>24` for `p>=53`, every nonzero `y` has a
non-antipodal zero-sum four-subset of product `y`.  The verifier checks the
finite remaining primes

```text
p=17,19,23,29,31,37,41,43,47.
```

The verifier also audits the pair-product argument at `p=53,59,61`: in these
rows every nonzero `y` has more than `24` ordered pair representations, at
most `24` exclusions, and at least one residual witness.

Thus, for every prime `p>=17`, the `j=4` full-domain monomial boundary model
has residual product image all of `F_p^*` after quotient charging.  One fixed
external anchor again carries `p-1` nonzero residual slopes.

The same full-domain model has a closed zero-sum count for every `j`.  For
`0 <= j <= p-1`,

```text
#{T subset F_p^*: |T|=j, sum(T)=0}
  = (binom(p-1,j) + (p-1)(-1)^j)/p.       (EA8)
```

Indeed, averaging over additive characters gives the trivial-character term
`binom(p-1,j)`.  For every nontrivial additive character `psi`, the coefficient
of `Y^j` in

```text
prod_{x in F_p^*}(1+Y psi(x))
```

is `(-1)^j`, because after adjoining the missing `x=0` factor one has
`prod_{x in F_p}(1+Y psi(x))=1+Y^p`.  This proves (EA8).  The verifier asserts
this general formula in every audited full-domain monomial row.

Specializing (EA8) to triples gives

```text
#{T subset F_p^*: |T|=3, sum(T)=0} = (p-1)(p-5)/6.
```

Indeed the number of zero-sum three-subsets of `F_p` is
`(p-1)(p-2)/6`, and the triples containing `0` are exactly
`{0,a,-a}`, giving `(p-1)/2` exclusions.

Specializing (EA8) to four-subsets gives

```text
#{T subset F_p^*: |T|=4, sum(T)=0}
  = (p-1)(p^2-9p+26)/24.
```

Here the zero-sum four-subsets of `F_p` are counted by choosing three
nonzero differences, giving `(p-1)(p-2)(p-3)/24`, and subtracting the
zero-containing triples above.  When the antipodal quotient family is charged,
the residual zero-sum count becomes

```text
(p-1)(p-5)(p-7)/24,
```

because the charged antipodal families are the `binom((p-1)/2,2)` choices of
two pairs `{a,-a}` and `{b,-b}`.  The verifier asserts these formulas in the
full-domain monomial audits.

For `j=4`, the quotient-periodic zero-sum part has an exact form.  Since the
charged fiber size `2` is present in the full-domain audits, quotient-charged
four-subsets are precisely unions of two antipodal pairs

```text
T={a,-a,b,-b}.
```

These are zero-sum and have product `(ab)^2`, so their product image is exactly
the square subgroup of `F_p^*`.  Conversely, the verifier checks that every
quotient-charged zero-sum four-subset in the audited full-domain cases is such
an antipodal-pair union.  Thus the residual product image is not the obvious
square-family contribution; that square contribution is already removed by the
quotient charge.

## Fixed-Anchor Field-Size Floor

The monomial boundary family also gives a sharp scale warning.  In the audited
`F_17` full-domain toy cases `j=3` and `j=4`, the residual product image after
quotient charging is all of `F_17^*`.  Since the slope map is a nonzero scalar
multiple of `prod(T)^{-1}`, the single external anchor `xi=0` already carries
all `16` nonzero slopes.

Thus a fixed-external-anchor boundary theorem cannot aim for a constant or
anchor-count bound.  Even after quotient-periodic locators are charged, one
external anchor may contribute a slope image of size comparable to the domain
size.  The plausible target has to be a polynomial or linear-in-`q_line`
product-image bound compatible with the M1 reserve, not a collapse of the
boundary term to `O(1)` per anchor.

## Exact F13 Boundary Product Model

The `F_13`, `n=12`, `j=4`, `t=2` boundary-only row is not only a numerical
counterexample.  It has a closed finite model.  Write `D=F_13^*`, and let
`T subset D` have size `4`.  For seed `s in {0,1,2,3}`, the words used by the
verifier restrict on `D` to polynomials whose relevant top terms are

```text
u_s(X) = (2s+3)X^7 + lower terms,
v_s(X) = (3s+1)X^11 + lower terms.
```

The verifier checks the following exact assertions for every seed.  A locator
`T` is bad if and only if

```text
sum_{x in T} x = 0.
```

For such a zero-sum `T`, the common external anchor is `xi=0`, and

```text
H_{2,4}(u_s)L_T = (2s+3, 0),
H_{2,4}(v_s)L_T = ((3s+1)prod_{x in T}x, 0).
```

Thus the bad slope is the product slope

```text
z_T = -(2s+3) / ((3s+1)prod_{x in T}x).
```

There are `39` zero-sum four-subsets of `F_13^*`.  The quotient-periodic
charge removes `15` of them.  The `24` residual boundary locators split into
six product fibers

```text
prod(T) in {1,3,7,8,9,11},
```

with exactly four residual locators in each product fiber; each product fiber
has one slope by the product formula.  This explains the boundary-only row's
six slopes as a product image inside one external anchor.  It is a concrete
model for the next task: a fixed-anchor proof must control
product/top-coefficient images, not just the number of external anchors.

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
Consequently the boundary term can be made overlap-aware.  Put

```text
Z_esc^new = Z_esc \ Z_lift.
```

Then

```text
|Z_res| = |Z_lift| + |Z_esc^new|.     (SL2)
```

Thus an isolated escape slope already realized by an active lifted common
core need not be charged a second time.  Only the new escape image
`Z_esc^new` is a genuinely separate residual boundary cost.

The lifted side has a local injectivity property.  If `W` is a lifted common
core and `T_x,T_y subset W` are two distinct residual faces, then `T_x` and
`T_y` are one-exchange neighbors.  If they had the same residual slope, the
same-slope root-slice lemma would put both in a fixed-slope root-slice packet,
so they would have been peeled before `R_res` was formed.  Hence the residual
faces of each lifted common core have pairwise distinct slopes.

Thus a future slope-image proof can work with two explicit objects:

1. injective residual-coordinate slopes inside lifted common cores; and
2. isolated anchor-escape slopes not already in the lifted image.

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

## Active Residual-Ratio Ledger

The residual-coordinate form gives an exact active-core ledger.  For a lifted
common core `W`, write

```text
rho_W(x)=-(f(x)-F_0(x))/(g(x)-G_0(x))
```

whenever the denominator is nonzero, and put `T_x=W\{x}`.  Let

```text
A_W={x in W : T_x remains residual after contained/tangent,
              quotient-periodic, and root-slice charges}.
```

Then the residual faces carried by `W` are exactly `{T_x : x in A_W}`, and the
slope of `T_x` is `rho_W(x)`.  These active faces are also unique across
lifted common cores.  If a residual lifted face `T` is carried by
`W=T union {x}`, then the denominator anchor identity gives
`H_{2,j}(v)ell_T=(beta_0,x beta_0)` with `beta_0 != 0`, so the projective
companion anchor of `T` is `xi_T=beta_1/beta_0=x`.  Thus any lifted common
core carrying `T` must be `T union {xi_T}`.

Moreover `rho_W` is injective on `A_W` after the root-slice peeling.  Indeed,
if two distinct residual coordinates `x,y in A_W` had the same ratio
`rho_W(x)=rho_W(y)=z`, then the two faces `T_x` and `T_y` would form a
same-slope one-exchange edge inside `W`.  The root-slice theorem above
promotes every such same-slope edge to its full fixed-slope root slice, and
the peeling step removes that slice.  Hence no repeated residual ratio can
survive.

Thus the lifted residual locators are partitioned by active residual
coordinates, and their slope image is exactly the active ratio image:

```text
R_lifted = disjoint_union_W {W\{x} : x in A_W},
Z_lift = union_W rho_W(A_W),
|rho_W(A_W)|=|A_W|=|R_W|,
|Z_lift| <= sum_W |A_W| <= (j+1)N_active.          (LR3)
```

It is useful to name the middle quantity:

```text
N_face = sum_W |A_W|.
```

This is the exact number of active residual coordinates on lifted common
cores.  It can be much smaller than the coarse worst-case face budget
`(j+1)N_active`, while still depending only on the active common-core
partition.

This is the local no-loss statement for the lifted side of the all-line
packing reduction.  Inactive common bases have `A_W=empty`; active bases with
one surviving coordinate contribute one isolated residual ratio; active bases
with at least two surviving coordinates are exactly the residual top-packet
cores below.

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

## Residual Component Theorem

The preceding local statements combine into an exact component theorem for the
`t=2` residual one-exchange graph.  Let `G_res` have vertices the residual
aperiodic locators left after quotient-periodic charging and root-slice
peeling, and join two vertices when their supports have strict overlap
`>k`, equivalently when their `j`-point complements differ by one exchange.
Then every connected component of `G_res` is one of the following:

1. an isolated residual locator; or
2. the full clique on the residual `j`-faces of a unique squarefree
   `(j+1)`-set `W subset D` satisfying
   `H_{1,j+1}(u)ell_W=H_{1,j+1}(v)ell_W=0`.

In case (2), the component is exactly one projective lifted-kernel fiber and
one top packet, and its vertices have pairwise distinct slopes.  Every
projective boundary lift, including off-domain external-anchor lifts, repeated
root lifts, and infinity lifts, is in case (1).

The proof is the ledger assembled above.  The common companion anchor puts all
neighbors of a residual locator in the single packet obtained by adjoining its
anchor.  The no-star-triangle and top-packet identities make each nontrivial
component a clique inside one `(j+1)`-packet.  The projective lift-fiber ledger
identifies that packet with one squarefree lifted-kernel fiber, while boundary
projective fibers are singleton fibers and hence isolated.  Finally,
root-slice peeling removes all same-slope residual edges, so every nontrivial
component is slope-injective.

Consequently the residual `t=2` slope image has no hidden high-overlap graph
structure left to control.  It splits into slope-injective lifted-core clique
components and isolated escape vertices:

```text
Z_res =
  union_{squarefree lifted cores W} Z_W
  union Z_iso,
```

where `|Z_W|` is exactly the number of residual faces of `W`.  The remaining
M1 work is therefore a counting/slope-image problem for these lifted cores and
isolated boundary escapes, not a general Johnson-graph packing problem.

## Lifted-Side Recursion Bound

The component theorem gives an explicit additive recursion for the lifted side
of the `t=2` residual slope image.  Let

```text
N_common =
  #{W subset D : |W|=j+1,
       H_{1,j+1}(u)ell_W = H_{1,j+1}(v)ell_W = 0}.
```

Equivalently, `N_common` is the number of `(k+1)`-point bases `S_0=D\W` on
which both line directions are individually explained by degree `<k`
polynomials.  Then

```text
|Z_lift| <= sum_W #{residual faces of W} <= (j+1)N_common,
```

and therefore

```text
|Z_res| <= (j+1)N_common + |Z_esc|.        (LR1)
```

Here `Z_esc` is the isolated escape slope image from the projective boundary
fibers.  The point of (LR1) is that the lifted-core contribution is no longer
a new `t=2` packing problem: it is charged additively to the one-degree-up
`t=1` common-base incidence count, with no multiplication by the number of
residual locators.  Thus the non-recursive term still needing a separate M1
bound is precisely the isolated boundary/escape slope image.

There is a sharper active version which is useful in degenerate endpoint
cases.  For a lifted common core `W`, let `R_W` be the set of its `j`-faces
which remain residual after the contained/tangent, quotient-periodic, and
root-slice charges.  Define

```text
N_active = #{W : H_{1,j+1}(u)ell_W=H_{1,j+1}(v)ell_W=0
                  and R_W != empty }.
```

The component theorem gives disjoint lifted-core components, and the
residual-coordinate slope formula makes each `R_W` slope-injective.  Hence

```text
|Z_lift| <= sum_W |R_W| <= (j+1)N_active,       (LR2)
```

where `N_active <= N_common`.  This distinction matters when one endpoint has
many one-row bases, for example because it is already close to a codeword:
inactive common bases do not contribute lifted residual slopes and should not
be treated as an obstruction.  The verifier counts `N_active` as the sum of
common cores with either one residual face or a residual top-packet.

## `t=2` M1 Slope-Image Reduction

Combining the root-slice peeling and the lifted-side recursion gives a single
conditional reduction for the full `t=2` aperiodic slope image.  Let `Z_root`
be the slope set of the constant root-slice packets removed by the peeling
step, let `N_common` be the lifted common-core count above, and let `Z_esc`
be the isolated escape slope image.  Then

```text
|AperSlope(f,g;2,j)| <= |Z_root| + (j+1)N_common + |Z_esc|.        (M1R2)
```

Indeed, every aperiodic locator either lies in a peeled constant root-slice
packet or survives in `R_res`.  The peeled part contributes only slopes in
`Z_root`.  The residual part splits by the anchor ledger into lifted faces
and isolated escapes, and (LR1) bounds the lifted-face slope image by
`(j+1)N_common` while leaving exactly `Z_esc` as the boundary term.

Thus, in slack two, the all-line aperiodic M1 target has been reduced to three
separate estimates:

```text
root-slice slope count        |Z_root|,
one-degree-up common bases    N_common,
isolated escape slopes        |Z_esc|.
```

Bounding these three quantities by `n^B` uniformly, after quotient-periodic
classes are charged, would prove the desired polynomial aperiodic slope-image
bound for `t=2`.  The verifier now asserts this reduction directly by
checking the root/residual slope split and the inequality (M1R2) in every
audited row.

Using (RS3), the same bound has a recursive form

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_common + |Z_esc|.       (M1R2')
```

The active-core version is stronger:

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_active + |Z_esc|.       (M1R2'')
```

Using the overlap-aware boundary image from (SL2), the sharper active version
is

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_active + |Z_esc^new|,
Z_esc^new = Z_esc \ Z_lift.                         (M1R2''')
```

The face-exact version is sharper still:

```text
|AperSlope(f,g;2,j)| <= |Z_3| + N_face + |Z_esc^new|,           (M1R2'''')
N_face = sum_W |A_W|.
```

Indeed, the root-slice contribution is charged to `Z_3`, the lifted residual
contribution has slope image contained in the active coordinate set counted
by `N_face`, and the only boundary contribution not already counted is
`Z_esc^new`.  Since `N_face <= (j+1)N_active`, (M1R2'''') implies
(M1R2''') and is the sharpest reduction before accounting for overlap between
the root-slice and residual slope images.

There is a final overlap saving at the root/residual boundary.  The root
slice and residual slope images cover the aperiodic image by union, so only
root-slice slopes absent from the residual image must be charged separately.
Put

```text
Z_root^new = Z_root \ Z_res,
Z_3^new    = Z_3 \ Z_res.
```

Then the exact root/residual slope ledger is

```text
|AperSlope(f,g;2,j)| = |Z_res| + |Z_root^new|,
```

and, using `Z_root subset Z_3`,

```text
|AperSlope(f,g;2,j)| <= |Z_3^new| + N_face + |Z_esc^new|.       (M1R2''''')
```

Equivalently, this is (M1R2'''') with already-residual higher-slack
root-slice slopes removed before charging the recursive term.  The verifier
asserts the exact disjoint count and the recursive `Z_3\Z_res` version in
every audited row.  In the current `F_17` full-domain rows the face-exact
recursive bound drops from `57` to `56`; in the rank-one zero-slice probe it
drops from `47` to `45`.

This does not assert that boundary escapes are harmless.  It says that the
only boundary slopes still needing a separate estimate are those not already
seen by active lifted common cores.  In rows where boundary escapes and lifted
cores have the same slope image, the residual boundary term disappears from
the slope-image bound.

The price is that `Z_3` is a larger raw higher-slack slope image than the
actually peeled root-slice slope set.  The gain is conceptual: root slices are
not a new obstruction type, but a `t=3`, degree-`j-1` core-locator problem.

Using the boundary arrangement budget (BA2), this becomes the fully explicit
audited reduction

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_common + B_boundary.      (M1R4)
```

Using the projective-linear slope-image refinement (BA3), the sharper audited
version is

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_common
                         + B_boundary^slope.       (M1R5)
```

Thus the remaining proof inputs are a higher-slack slope-image bound for
`Z_3`, a one-row common-base bound for `N_common`, and a quotient-aware
boundary-arrangement bound for `B_boundary^slope`.

The middle term is not a new slack-two object.  Define the one-degree-up
one-row locator fiber of a word `y` by

```text
Fib_1(y) =
  {W subset D : |W|=j+1, H_{1,j+1}(Syn(y))ell_W=0}.
```

Then

```text
N_common = |Fib_1(f) cap Fib_1(g)|
         <= min(|Fib_1(f)|, |Fib_1(g)|).             (M1R3)
```

This is exactly the common-base interpretation of the Hankel equation: a
core `W` is counted by `N_common` precisely when both endpoints are explained
on the same `(k+1)`-point base `D\W`.  Consequently any uniform `t=1`
one-row locator-fiber theorem immediately bounds the lifted-common term in
(M1R2), with the only slack-two-specific work left in `Z_root` and `Z_esc`.
The verifier reports `|Fib_1(f)|`, `|Fib_1(g)|`, and their common-core count
for the audited rows.

Putting (M1R3) together with the polynomial-field boundary closure (M1R6)
removes the two slack-two-specific terms which are not higher-slack root
images.  For every finite field instance,

```text
|AperSlope(f,g;2,j)|
  <= |Z_3|
     + (j+1) min(|Fib_1(f)|, |Fib_1(g)|)
     + (|F|+1)^2.                                  (M1R7)
```

Consequently, in the polynomial-field window `|F| <= n^C`, the `t=2`
all-line aperiodic packing target follows from two inputs:

1. a polynomial bound for the higher-slack core slope image `Z_3`; and
2. a polynomial one-row locator-fiber bound for every endpoint word.

More explicitly, if `|Z_3| <= n^B3` and
`|Fib_1(y)| <= n^B1` uniformly for endpoint words `y`, then

```text
|AperSlope(f,g;2,j)| <= n^B3 + n^(B1+1) + O(n^(2C)).
```

This is the current clean route to the slack-two part of Przemek's all-line
target.  The boundary and lifted-core geometry established above proves that
there is no multiplicative recursion loss at this rung: the lifted term is
additive through `Fib_1`, root slices are charged upward to `Z_3`, and boundary
escapes cost only the polynomial field-size term.

The sharper active-field version keeps the same boundary closure while
discarding inactive common bases:

```text
|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_active + (|F|+1)^2.      (M1R8)
```

It is still implied by the two-input bound because `N_active <= N_common <=
min(|Fib_1(f)|,|Fib_1(g)|)`, but it is the more faithful local obstruction:
to improve the slack-two estimate one can bound active residual common cores,
not all one-row common bases.  The overlap-aware version keeps the same
polynomial-field fallback but replaces the exact boundary term by
`|Z_esc^new|`, the escape slopes not already realized by active common-core
ratios.

## Verifier

The companion verifier

```bash
python3 experimental/scripts/verify_m1_all_line_hankel_aperiodic.py
```

enumerates small cyclic-domain cases.  For each case it:

- computes syndromes and Hankel windows for a deterministic family of all-line
  words;
- enumerates all split complements `T`;
- applies the projective slope gate, with the determinant-gate cross-check in
  the `t=2` rows;
- cross-checks every bad slope by direct RS interpolation on `D\T`;
- labels whole-fiber quotient-periodic complements at the selected scales;
- reports the aperiodic slope image after charged locators are removed;
- for every row, counts one-exchange pairs and verifies the arbitrary-slack
  same-slope lift into the `(t+1,j-1)` Hankel core image;
- in the `t=3` rows, counts two-exchange pairs and verifies the quadratic
  determinantal slice certificate in the pair-symmetric coordinates
  `(x+y,xy)`;
- in the `t=2` rows, verifies the determinant gate and reports the strict
  one-exchange profile of the aperiodic locator family;
- in the `t=2` rows, checks that every same-slope strict one-exchange edge
  extends to the full fixed-slope root slice predicted by the lemma above;
- verifies that different-slope strict edges obey the quadratic root-slice
  dichotomy above;
- verifies that every zero-determinant slice is constant-slope or contained
  via the direction-pencil rank and Hankel overlap, and that constant zero
  slices account for all same-slope strict edges;
- peels root-slice members and checks that the residual aperiodic family has
  no same-slope one-exchange edges;
- checks residual slope-fiber core disjointness, hence the global packing
  bound `|F_z| j <= binom(n,j-1)` for every residual slope `z`;
- reports the residual strict one-exchange count and verifies the residual
  maximum degree bound `<= j`;
- checks the quadratic companion map for every nonzero quadratic edge slice;
- verifies the common companion anchor `xi_T=beta_1/beta_0` for every oriented
  residual edge endpoint;
- verifies the full residual anchor ledger: addable in-domain anchors lift to
  common cores, while beta0-zero, in-support, and outside-domain anchor escapes
  are isolated residual locators;
- for every off-domain external anchor, groups escape locators by
  `(anchor,slope)` and verifies the pinned twisted `t=1` equation
  `H_{1,j+1}(u^xi+zv^xi)P_T=0`;
- verifies that every fixed `(anchor,slope)` fiber is one-exchange-free by
  checking disjointness of its `(j-1)`-cores, hence satisfies the packing
  bound `|F_{xi,z}| * j <= binom(n,j-1)`;
- rewrites each fixed external-anchor term as a projective root-hyperplane
  arrangement, checking the pinned common-kernel dimension, the `j`-rich
  points, and their finite twisted slope image;
- checks the low-dimensional fixed-anchor pencil theorem: when
  `dim V_xi <= 2`, fixed roots partition the remaining rich roots and give
  the bound `floor((n-r_xi)/(j-r_xi))`;
- checks the fixed-anchor projective-plane bound: when `dim V_xi=3`, rich
  points are covered by heavy root lines and pairwise intersections of
  non-heavy root lines;
- checks the fixed-anchor three-space bound: when `dim V_xi=4`, rich points
  are covered by heavy planes, heavy pair-intersection lines, and triple
  intersections of root planes;
- checks the general fixed-anchor rank-stratified cover: rich points are
  covered by heavy flats generated by root hyperplanes in `P(V_xi)`;
- verifies the homogeneous projective residual lift ledger: every residual
  locator maps to the common one-row lifted Hankel kernel through
  `beta_0 X L_T-beta_1 L_T`, with finite anchors, repeated-root lifts,
  off-domain lifts, and infinity anchors separated afterward;
- enumerates all `p+1` projective one-root anchors for each residual locator
  and verifies that the common lifted-kernel anchor is unique and equal to
  `[beta_1:beta_0]`;
- groups residual locators by their normalized projective lift and verifies
  the lift-fiber ledger: boundary fibers are singleton, nontrivial fibers are
  squarefree in-domain top packets, and the fiber pair count equals the
  residual strict edge count;
- computes the connected components of the residual one-exchange graph and
  verifies the component theorem: every nontrivial component is one
  slope-injective squarefree lifted-core clique, and every projective boundary
  lift is isolated;
- asserts the lifted-side recursion bound
  `|Z_res| <= (j+1)N_common + |Z_esc|`, with `N_common` the audited count of
  one-degree-up common bases;
- computes the new escape slope image `Z_esc \ Z_lift` and asserts the
  overlap-aware lifted-side bounds
  `|Z_res| <= (j+1)N_common + |Z_esc \ Z_lift|` and
  `|Z_res| <= (j+1)N_active + |Z_esc \ Z_lift|`;
- asserts the face-exact active-coordinate bound
  `|Z_res| <= N_face + |Z_esc \ Z_lift|`, where
  `N_face=sum_W |A_W|` is the surviving lifted residual face count;
- asserts the total `t=2` slope-image reduction
  `|AperSlope| <= |Z_root| + (j+1)N_common + |Z_esc|`;
- checks the higher-slack root-slice reduction `Z_root subset Z_3` and the
  recursive bound `|AperSlope| <= |Z_3| + (j+1)N_common + |Z_esc|`;
- asserts the recursive overlap-aware active bound
  `|AperSlope| <= |Z_3| + (j+1)N_active + |Z_esc \ Z_lift|`;
- asserts the sharper face-exact recursive bound
  `|AperSlope| <= |Z_3| + N_face + |Z_esc \ Z_lift|`;
- asserts the root/residual overlap refinement
  `|AperSlope| <= |Z_3 \ Z_res| + N_face + |Z_esc \ Z_lift|`;
- computes the boundary arrangement budget `B_boundary` and asserts
  `|Z_esc| <= B_boundary` and
  `|AperSlope| <= |Z_3| + (j+1)N_common + B_boundary`;
- computes the slope-image boundary budget `B_boundary^slope` by charging each
  heavy flat by at most `|F|+1` slope values, and asserts the sharper
  `|AperSlope| <= |Z_3| + (j+1)N_common + B_boundary^slope`;
- computes the active-anchor boundary budget
  `(|F|+1)A_boundary <= (|F|+1)^2` and asserts the polynomial-field reduction
  `|AperSlope| <= |Z_3| + (j+1)N_common + (|F|+1)A_boundary`;
- asserts the two-input polynomial-field reduction
  `|AperSlope| <= |Z_3| + (j+1)min(|Fib_1(f)|,|Fib_1(g)|) + (|F|+1)^2`;
- counts active lifted common cores and asserts the sharper active-field
  reduction `|AperSlope| <= |Z_3| + (j+1)N_active + (|F|+1)^2`;
- reports the endpoint `t=1` locator-fiber counts `|Fib_1(f)|` and
  `|Fib_1(g)|`, and checks `N_common <= min(|Fib_1(f)|,|Fib_1(g)|)`;
- checks the `F_13`, `n=12`, `j=4`, `t=2` boundary-only row as a counterexample
  to absorbing all residual slopes into squarefree lifted-core fibers;
- checks the same boundary-only row as a counterexample to bounding boundary
  slopes merely by the number of external anchors: all `24` residual boundary
  locators share one external anchor but produce `6` residual slopes;
- verifies the external-anchor twisted one-row reduction: every off-domain
  residual locator with anchor `xi` has the same slope as the one-row
  Hankel-pencil gate for the twisted line `u/(X-xi),v/(X-xi)` on
  `(X-xi)L_T`;
- verifies the repeated-root and infinity-anchor one-row reductions: repeated
  escapes use the domain-pole twisted gate on `(X-xi)L_T`, while infinity
  escapes use the shifted one-row quotient for `L_T`;
- verifies the all-boundary arrangement reduction: residual repeated-root and
  infinity escapes are contained in their rich-point slope images and satisfy
  the same rank-stratified cover as fixed external anchors;
- checks the external-anchor top-coefficient form: on `B=D\T`, the first
  Hankel row equals the top interpolation coefficient, the anchor equation
  locks the top two coefficients by `xi-sum(B)`, and the residual slope
  cancels both top coefficients;
- verifies the exact `F_13` boundary product model: bad locators are exactly
  the zero-sum four-subsets, quotient charging removes `15` of the `39`, and
  the `24` residual locators split into six four-element product fibers;
- audits the full-domain monomial boundary family, where `X^{p-2-j}` versus
  `X^{p-2}` has bad locators exactly on the zero-sum locus and slopes given by
  the product image of the deleted roots;
- verifies the `j`th-power coset symmetry of the charged and residual product
  images in that family;
- checks the general full-domain zero-sum product normal form: after scaling
  one root to `1`, the product image is the `j`th-power closure of the
  normalized `(j-2)`-variable map;
- checks the quotient-fiber product ledger scale by scale: a union of
  `j/m` whole size-`m` cosets is automatically zero-sum and has product
  `(-1)^{(j/m)(m+1)}` times a `j/m`-subset product in `(F_p^*)^m`;
- checks the `j=3` product-coset reduction: every zero-sum triple normalizes to
  `{1,r,-1-r}`, the product image is the cube-closure of `-r(1+r)`, and an
  active size-`3` quotient charge has cube-subgroup product image;
- asserts the `j=3` cube-bijective field-size floor: for audited primes
  `p=11,17,23,29` with `p == 2 mod 3`, there is no size-`3` quotient charge
  and the residual product image is all of `F_p^*`;
- asserts the `j=3` cubic-character field-size floor: for `p == 1 mod 3`,
  the note proves residual product saturation for `p>=31`, and the verifier
  audits `p=31,37,43`, with small exceptions recorded by the existing `(13,3)`
  row and by the added `p=19` row;
- checks the `j=4` product-coset reduction: every zero-sum quadruple
  normalizes to `{1,r,s,-1-r-s}`, with product image the fourth-power closure
  of the binary cubic `-rs(1+r+s)`;
- asserts the `j=4` residual field-size floor after antipodal quotient
  charging: the residual product image is all of `F_p^*` for every audited
  prime `17 <= p < 53`, while the note proves the large-prime range by a
  pair-product character-sum bound;
- audits the large-prime pair-product proof at `p=53,59,61`, checking that
  ordered pair-product representations beat the collision and antipodal
  exclusions for every nonzero target product;
- asserts the general additive-character count for zero-sum `j`-subsets of
  `F_p^*`, including the `j=3` and `j=4` specializations and the residual
  count after antipodal quotient charging;
- checks the `j=4` antipodal quotient charge in that family: quotient-charged
  zero-sum four-subsets are exactly unions `{a,-a,b,-b}`, whose products form
  the square subgroup;
- asserts the `F_17` fixed-anchor field-size floor: in the full-domain
  monomial cases `j=3,4`, one external anchor carries all `16` nonzero slopes
  after quotient charging;
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
- counts inactive common cores and checks that the active residual-ratio
  ledger partitions the residual lifted faces, with exact active-ratio slope
  image `Z_lift` and no repeated ratios inside an active common core after
  root-slice peeling;
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

The default audit currently checks four cyclic-domain parameter rows,
seventeen deterministic polynomial-family line samples, and one deterministic
arbitrary line probe.  Three rows exercise the full `t=2` residual reducer,
while the `F_13`, `n=12`, `j=7`, `t=3` row exercises the arbitrary-slack
same-slope one-exchange lift and the two-exchange quadratic determinantal
slice certificate.  The largest observed residual aperiodic slope image in
this smoke packet has size `17`, after direct interpolation checks on every
reported support-wise bad slope.

The `F_13`, `n=12`, `j=4`, `t=2` row is kept as a boundary-only counterexample
to the tempting squarefree-absorption shortcut.  In all four deterministic
seeds it has `24` residual locators, all of them off-domain projective
boundary singleton fibers; it has no lifted common cores, no squarefree
projective lift fibers, and no lifted slopes.  Nevertheless it has `6`
residual slopes, all coming from `6` new escape slopes.  The verifier also
asserts that all `24` residual locators share one external anchor, so these
`6` escape slopes cannot be bounded by external-anchor count alone.

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
`xi_T in T`, and `4` with `xi_T notin D`.  The homogeneous projective lift
ledger checks all `86` residual locators in the common one-row lifted kernel.
It also checks uniqueness of the projective lifted-kernel anchor for all `86`
residual locators by enumerating the `18` anchors of `P^1(F_17)`.
The normalized projective lift map has `44` fibers: `14` squarefree in-domain
fibers and `30` boundary singleton fibers.  Its maximum fiber size is `5`, and
the `88` unordered pairs inside projective lift fibers account exactly for the
`88` residual strict edges.
Among these, `81` finite residual-anchor lifts split as `56` squarefree
in-domain lifts, `21` repeated-root boundary lifts, and `4` off-domain
boundary lifts; the remaining `5` escapes are infinity anchors.  On slope
images, the `16` residual slopes
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
`2` with `xi_T notin D`.  The homogeneous projective lift ledger checks all
`69` residual locators in the common one-row lifted kernel and verifies
uniqueness of all `69` projective anchors.  These locators form `44`
projective lift fibers: `19` squarefree in-domain fibers and `25` boundary
singletons.  The `40` unordered pairs inside projective lift fibers account
exactly for the `40` residual strict edges.  The `65` finite residual-anchor
lifts split as `44` squarefree in-domain, `19` repeated-root, and `2`
off-domain boundary lifts; the remaining `4` escapes are infinity
anchors.  The `16` residual slopes
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
