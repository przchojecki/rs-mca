---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: At the first open equality wall sigma_wall=134943, rank three forces both the occupied locator-residue space and the complete reciprocal space to have base dimension three. On every projective residue line, the complete reciprocal products define a canonical rank-two polynomial congruence module. The source-unit product identity forces its cofactor gcd to be one, so the complete reciprocal columns generate the full line module and no proper cofactor source partition survives. A resultant-avoidance argument chooses one base reciprocal direction whose two line products are coprime and reach degree 134944. Relative to this direction, every exact root-swap edge exchanges exactly 134944 roots and every exact-swap component has at most 7 locators; every other pair exchanges at least 67472 roots. Equality h=0 makes every occupied source-product pair already coprime of exact degree e, so the line collision divisor cannot be charged as per-direction gcd mass. Its zero branch is nevertheless paid by global source-map-class deduplication: a residue line either contains one map class or has pairwise distinct maps. Every nontrivial exact-swap component forces the actual selector K0 rows on a common zero set of at least 103967 carrier coordinates to have rank at most 7; equivalently it emits a nonzero K0 generalized-Reed-Solomon word with quotient degree at most (m-1)e-c, at most c for a two-point component, and source-scale moving-block weight at least e+c=s. This precursor is not an instance of any current active owner. More strongly, every candidate 69-point transversal packet admits one canonical full-domain source-unit reciprocal parameter for which all 2346 pair relations are nonzero and every vertex cofactor is nonzero at every carrier point. For that parameter the source quotient and the actual selector secant quotient are exactly the same polynomial, of degree at most exchange-c, and the secant is nonzero on all 2*exchange coordinates. Rooting the resulting secants at one vertex and using dim(K0)=8 canonically places each of at least 60 remaining directions in a fundamental circuit of at most 9 secants, equivalently an affine circuit of at most 10 actual graph records. The induced carrier-membership partition has no singleton atom. A minimal m-record circuit contributes m-2 independent K0 secants vanishing on its common locator-zero set, so the selector restriction there has rank at most 10-m; a three-record circuit has at least 423079 common zeros and rank at most 7. Thus the source/selector coupling problem is closed; the remaining local theorem is bounded-circuit partition payment or a packing contradiction for this canonical secant graph on a line with nonzero collision divisor. Locator multiplicity and repeated source maps are immaterial to the slope ledger: each map class feeds one image of size at most 1894736. Consequently a cap of 68 distinct source-map classes on every projective line would pay the complete rank-three packet, while 69 does not suffice by this incidence summation. A bare weighted residue-line cap 130 is impossible: the source-free locator cylinder contains a one-root-swap line with 913632 locators.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
atom_or_cell: ACTIVE_FULL_OUTSIDE_EQUALITY_WALL_RESIDUE_LINE_PARTITION_REDUCTION
quantifier: Per received line, fixed translated source, rebuilt complete selector, scalar-unpaid rank-three equality packet, and projective residue line
projection_and_unit: Distinct selected finite slopes per received line; monic complement locators and complete base reciprocal space
claimed_bound: Exact cofactor-primitivity and exchange reduction only; no additional charge and no payment of the primitive large-exchange line branch
status: PROVED_REDUCTION_ROW_OPEN
impact: BARE_LINE_CAP_CUT_AND_ACTIVE_COFACTOR_PRIMITIVITY_PROVED_FIRST_OPEN_134943_UNCHANGED
falsifier: A rank-three equality packet whose complete reciprocal dimension is not three; a projective residue line whose product-pair congruence module has determinant ideal other than Lambda_Sigma; a source-valid line with nonconstant cofactor gcd; failure of the nonzero degree-at-most-2e resultant to admit a base reciprocal direction; two active coprime-row locators exchanging fewer than c roots; an exact-swap component larger than 1+floor((carrier_size-locator_degree)/e) relative to the generic direction; or a claim that split-locator residue geometry alone implies line occupancy at most 130.
replay: python3 experimental/scripts/verify_kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.py --check
---

# KoalaBear equality-wall residue-line partition reduction

## 0. Result and theorem boundary

The equality-wall locator-cylinder reduction leaves one rank-three packet at

\[
r=134{,}943,\qquad
s=202{,}416,\qquad
e=134{,}944,\qquad
c=67{,}472,
\tag{0.1}
\]

with

\[
e=2c,\qquad s=3c,\qquad e+c=s.
\tag{0.2}
\]

Its carrier and actual complement-locator degree are

\[
|V|=1{,}894{,}736,\qquad J=981{,}105.
\tag{0.3}
\]

The upstream constant-adjugate theorem now gives the simultaneous collapse

\[
\dim_B W_B=\dim_B\mathcal R_B=3,
\tag{0.4}
\]

where \(W_B\) is the occupied locator-residue space and \(\mathcal R_B\) is
the complete reciprocal space.

This note proves the following further facts.

1. A source-free line cap is false.  The split-locator cylinder contains a
   projective residue line with
   \[
   |V|-J+1=913{,}632
   \]
   actual locators.
2. Every projective residue line \(U\subset W_B\) carries a canonical
   polynomial congruence module of determinant \(\Lambda_\Sigma\).
3. The complete reciprocal columns on \(U\) have cofactor ideal
   \[
   \Lambda_\Sigma g_U,\qquad g_U\mid\Lambda_\Sigma,\qquad
   \deg g_U\le c.
   \]
   The source-unit product identity forces \(g_U=1\), so the columns
   generate the complete line module.
4. A base reciprocal direction can be chosen whose two products on the line
   are coprime and have maximum degree exactly \(e\).  Relative to this
   direction, every pair of distinct admitted locators exchanges at least
   \(c\) roots, every exact root-swap edge has exchange exactly \(e\), and
   every exact-swap component has at most
   \[
   1+\left\lfloor\frac{|V|-J}{e}\right\rfloor=7
   \]
   locators.
5. All locators above one projective residue direction feed the same
   source-map image.  Directions defining the same projective source map
   can also be deduplicated globally.  On each projective residue line,
   either all directions have the same map or their maps are pairwise
   distinct.  A local cap \(68\) on distinct map classes would pay the full
   rank-three packet with exact reserve margin
   \(292{,}758{,}501{,}275{,}736\); cap \(69\) is insufficient for this
   summation.
6. Since the equality stratum has \(h=0\), every occupied source-product
   pair is already coprime and has exact projective degree \(e\).  The
   fixed line collision divisor therefore forbids exceptional kernel
   directions; it supplies no positive gcd mass that can be summed over
   occupied directions.
7. A nontrivial exact-swap component of size \(m\le7\) forces the actual
   selector rows on its common zero set to have rank at most seven.  The
   common zero set has size
   \[
   |V|-J-(m-1)e\ge103{,}967.
   \]
   Equivalently, the component emits a nonzero \(K_0\)-word with a
   generalized-Reed--Solomon quotient of degree at most
   \((m-1)e-c\).  This is a same-selector collective-rank precursor, not
   yet an active paid owner.
8. Every packet of at most \(69\) occupied directions admits one canonical
   full-domain source-unit reciprocal parameter avoiding all \(s\) source
   zeros, all \(69|V|\) vertex/cofactor zeros, and all
   \(\binom{69}{2}\) pair kernels.  For every pair, the source quotient is
   exactly the shortened quotient of the actual selector secant.
9. Hence all \(2{,}346\) edges of a candidate \(69\)-point packet are
   simultaneously nonzero actual \(K_0\) secants with
   \[
   \deg T_{ij}\le\Delta_{ij}-c,\qquad
   \operatorname{wt}_{\rm exch}(w_{ij})=2\Delta_{ij}.
   \]
   No source/selector coupling theorem remains.
10. Rooting this complete graph at one vertex and taking a canonical basis
    of its star in the eight-dimensional \(K_0\) space gives at least
    \(60\) canonical fundamental circuits.  Every circuit uses at most
    \(9\) star edges, equivalently at most \(10\) actual graph-line records,
    and its carrier membership partition has no singleton atom.
11. A minimal \(m\)-record circuit has \(m-2\) independent rooted secants,
    all vanishing on the common locator-zero set.  Hence
    \[
    \operatorname{rank}(K_0|_{Z_C})\le10-m.
    \]
    For \(m=3\), the no-singleton partition gives
    \[
    |Z_C|\ge423{,}079,\qquad
    \operatorname{rank}(K_0|_{Z_C})\le7.
    \]

These are exact reductions, not a payment.  Every actual line is now in the
primitive cofactor branch.  The remaining problem is to bound the number of
directions in the resulting canonical secant graph by a packing theorem or
to emit one already-paid owner from that graph.  No charge is booked and the
first open slack remains \(134{,}943\).

## 1. The unrestricted residue-line cap is false

Let \(C\subset V\) have size \(J-1\).  For each \(a\in V\setminus C\), put

\[
q_a(X)=\Lambda_C(X)(X-a).
\tag{1.1}
\]

These are distinct monic degree-\(J\) split locators.  Their polynomial span
has dimension two, so their residues modulo \(\Lambda_\Sigma\) lie on one
projective residue line.  Since \(V\cap\Sigma=\varnothing\), every residue is
a unit.  The line contains

\[
\boxed{|V|-J+1=913{,}632}
\tag{1.2}
\]

actual locators.

In particular,

\[
913{,}632>130.
\tag{1.3}
\]

Thus the sufficient weighted line cap \(130\) from the parent reduction
cannot follow from any combination of:

* splitness and monicity;
* the locator degree and carrier size;
* residue-line membership;
* source-unit status.

Any valid cap must use the active source pair, the coprime exact-degree row,
the selector, or earlier first-match routing.  The family (1.1) is a
source-free route cut, not a post-atlas falsifier: no received line or
first-match survival is asserted for it.

The same formula gives exact finite controls:

\[
\begin{array}{c|c|c|c}
(p,|V|,J)&(17,10,7)&(19,12,8)&(23,14,10)\\ \hline
|V|-J+1&4&5&5.
\end{array}
\tag{1.4}
\]

Exhaustive small-field censuses find these one-root pencils as maximum
unrestricted lines in the respective equality models.

## 2. The canonical residue-line congruence module

Fix a projective line \(U\subset W_B\) and choose two distinct actual
locator residues \(q_0,q_1\) spanning it.  Work over the PID \(B[X]\) and
write

\[
A_B=B[X]/(\Lambda_\Sigma).
\]

Define

\[
\mathcal M_U
=
\left\{
(R,S)\in B[X]^2:
q_1R-q_0S\equiv0\pmod{\Lambda_\Sigma}
\right\}.
\tag{2.1}
\]

Both \(q_0\) and \(q_1\) are units in \(A_B\).  Hence

\[
(R,S)\longmapsto q_1R-q_0S\pmod{\Lambda_\Sigma}
\tag{2.2}
\]

is a surjection from \(B[X]^2\) onto \(A_B\).  Its kernel
\(\mathcal M_U\) is free of rank two, and the exact sequence gives

\[
\boxed{\operatorname{Fitt}_0(B[X]^2/\mathcal M_U)
=(\Lambda_\Sigma).}
\tag{2.3}
\]

Equivalently, the determinant of any polynomial basis of \(\mathcal M_U\)
is a unit multiple of \(\Lambda_\Sigma\).

Let \(\delta_0\le\delta_1\) be the row degrees of a row-reduced minimal
basis.  The predictable-degree property gives

\[
\boxed{\delta_0+\delta_1=s.}
\tag{2.4}
\]

The degree-\(e\) section has exact dimension

\[
\boxed{
\dim_B\left(\mathcal M_U\cap B[X]_{\le e}^2\right)
=
\max(e-\delta_0+1,0)+\max(e-\delta_1+1,0).
}
\tag{2.5}
\]

Through the unique degree-at-most-\(e\) representatives, this section is
exactly the complete reciprocal product space on \(q_0,q_1\).  Thus the
line packet has an intrinsic two-generator normal form; it is not an
arbitrary set of points in a growing polynomial cylinder.

## 3. Cofactor gcd and the source-partition precursor

Choose bases of \(W_B\) and \(\mathcal R_B\) whose first two locator rows
span \(U\).  By (0.4), the complete product matrix is a \(3\times3\)
polynomial matrix \(P\) satisfying

\[
\det P=\kappa\Lambda_\Sigma^2,
\qquad \kappa\in B^\times.
\tag{3.1}
\]

Let \(R_U\) be its first two rows.  Each \(2\times2\) minor of \(R_U\)
vanishes on \(\Sigma\), so after dividing by \(\Lambda_\Sigma\) the three
cofactors form a polynomial vector

\[
h_U=(h_0,h_1,h_2),
\qquad \deg h_i\le2e-s=c.
\tag{3.2}
\]

Define the monic invariant

\[
g_U=\gcd(h_0,h_1,h_2).
\tag{3.3}
\]

The third row of \(P\) dotted with \(h_U\) equals
\(\kappa\Lambda_\Sigma\).  Therefore

\[
\boxed{g_U\mid\Lambda_\Sigma,\qquad \deg g_U\le c.}
\tag{3.4}
\]

This statement is independent, up to units, of the chosen bases: the ideal
generated by the \(2\times2\) minors is the second determinantal ideal of
the complete two-row product module.

At this stage a nonconstant \(g_U\) would define the proper source subset

\[
T_U=\{\sigma\in\Sigma:g_U(\sigma)=0\}
\tag{3.5}
\]

is a nonempty proper source subset with

\[
1\le |T_U|=\deg g_U\le c=67{,}472.
\tag{3.6}
\]

and would be a canonical source-partition precursor.  It also has an exact
first-jet meaning.  Write the two complete product rows
as polynomial vectors \(r_0(X),r_1(X)\in B[X]^3\).  At every source point,

\[
r_1(\sigma)=\lambda_\sigma r_0(\sigma)
\tag{3.7}
\]

for a unique scalar \(\lambda_\sigma\), because a reciprocal basis contains
a source unit and \(q_0,q_1\) are source units.  The cross product
\(r_0\wedge r_1\) equals \(\Lambda_\Sigma h_U\), up to the fixed cofactor
signs.  If \(\sigma\in T_U\), this cross product has a double zero at
\(\sigma\).  Differentiating and using (3.7) gives

\[
r_0(\sigma)\wedge
\left(r_1'(\sigma)-\lambda_\sigma r_0'(\sigma)\right)=0.
\tag{3.8}
\]

Hence there is a scalar \(\mu_\sigma\) such that

\[
\boxed{
r_1'(\sigma)
=
\lambda_\sigma r_0'(\sigma)+\mu_\sigma r_0(\sigma).
}
\tag{3.9}
\]

Thus \(T_U\) would be an extra projective first-jet coincidence locus for
the two line rows.

In an actual source packet this locus is empty.  The cofactor vector is one
column of

\[
Q=\operatorname{adj}(P)/\Lambda_\Sigma,
\]

so, after choosing signs consistently,

\[
P h_U=\kappa\Lambda_\Sigma e_3.
\tag{3.10}
\]

Suppose \(g_U\ne1\), write

\[
h_U=g_U\widetilde h,\qquad
\Lambda_\Sigma=g_U\widetilde\Lambda,
\tag{3.11}
\]

and divide (3.10) in the integral domain \(B[X]\):

\[
P\widetilde h=\kappa\widetilde\Lambda e_3.
\tag{3.12}
\]

Choose \(\sigma\in T_U\).  Since \(\Lambda_\Sigma\) is squarefree and
\(g_U\mid\Lambda_\Sigma\),

\[
\widetilde\Lambda(\sigma)\ne0.
\tag{3.13}
\]

Let \(v_0,v_1,v_2\) be the complete reciprocal basis indexing the columns of
\(P\), and put

\[
w(\sigma)=\sum_{j=0}^2\widetilde h_j(\sigma)v_j(\sigma).
\tag{3.14}
\]

Every matrix entry satisfies

\[
P_{ij}(\sigma)=q_i(\sigma)v_j(\sigma).
\tag{3.15}
\]

The first coordinate of (3.12) therefore says

\[
q_0(\sigma)w(\sigma)=0.
\]

The actual locator \(q_0\) has all its roots in \(V\), disjoint from
\(\Sigma\), so \(q_0(\sigma)\ne0\) and \(w(\sigma)=0\).  The third coordinate
of (3.12) then says simultaneously

\[
0=q_2(\sigma)w(\sigma)
=\kappa\widetilde\Lambda(\sigma)\ne0,
\]

a contradiction.  Hence

\[
\boxed{g_U=1.}
\tag{3.16}
\]

This is the exact source-bound owner/partition conclusion: the apparent
proper source-partition branch is empty in every actual rank-three packet.
The source-unit row identity is load-bearing; a general polynomial matrix
with determinant \(\Lambda_\Sigma^2\) need not have primitive cofactors.

Let \(L_U\subset\mathcal M_U\) be the submodule generated by the three
complete reciprocal-product columns.  Its determinantal ideal is

\[
\operatorname{Fitt}_0(B[X]^2/L_U)
=(\Lambda_\Sigma g_U).
\tag{3.17}
\]

Equations (2.3), (3.16), and (3.17) give

\[
\boxed{L_U=\mathcal M_U.}
\tag{3.18}
\]

Moreover the primitive cofactor vector is the complete first syzygy of the
three columns.  The line module has the exact Hilbert--Burch presentation

\[
0\longrightarrow B[X]
\xrightarrow{\ h_U\ }
B[X]^3
\xrightarrow{\ R_U\ }
\mathcal M_U
\longrightarrow0.
\tag{3.19}
\]

Thus the remaining incidence problem may assume a primitive degree-at-most
\(c\) syzygy and a complete two-generator line module.  No source-partition
owner is needed.

### 3.1 A coprime exact-degree reciprocal direction

Write the two-row product matrix as

\[
R_U(X)=
\begin{pmatrix}
R_0(X)&R_1(X)&R_2(X)\\
S_0(X)&S_1(X)&S_2(X)
\end{pmatrix}.
\tag{3.20}
\]

For \(\lambda=(\lambda_0,\lambda_1,\lambda_2)\), put

\[
R_\lambda=\sum_j\lambda_jR_j,
\qquad
S_\lambda=\sum_j\lambda_jS_j,
\tag{3.21}
\]

and homogenize both polynomials to binary forms of degree \(e\).

The primitive minor identity determines the pointwise ranks of \(R_U\).
For \(x\notin\Sigma\), at least one maximal minor is nonzero, so

\[
\operatorname{rank}R_U(x)=2.
\tag{3.22}
\]

For \(\sigma\in\Sigma\), the product rows are proportional.  They are not
both zero because the locator residues are source units and the complete
reciprocal space contains a source unit.  Hence

\[
\operatorname{rank}R_U(\sigma)=1.
\tag{3.23}
\]

At the point at infinity the rank is also at least one: otherwise every
complete product would have degree below \(e\), contradicting the actual
coprime source row with one coordinate of exact degree \(e\).

Over \(\overline B\), the projective parameters \([\lambda]\) for which
\((R_\lambda,S_\lambda)\) have a common projective root form the image of
the kernel incidence

\[
\left\{(x,[\lambda]):
R_U(x)\lambda=0\right\}
\subset\mathbf P^1\times\mathbf P^2.
\tag{3.24}
\]

The fiber is one point where the rank is two and one projective line at
each of the finitely many rank-one points.  Its image is therefore a proper
closed subset of \(\mathbf P^2\).  Equivalently, the homogeneous resultant

\[
\mathfrak R(\lambda)
=\operatorname{Res}(R_\lambda,S_\lambda)
\tag{3.25}
\]

is a nonzero polynomial.  Its total degree is at most

\[
2e=269{,}888<p=2{,}130{,}706{,}433.
\tag{3.26}
\]

The finite-field polynomial zero bound now gives a nonzero
\(\lambda\in B^3\) with

\[
\mathfrak R(\lambda)\ne0.
\tag{3.27}
\]

For the corresponding complete reciprocal direction \(v_*\), the two
line products satisfy

\[
\boxed{
\gcd(R_*,S_*)=1,
\qquad
\max(\deg R_*,\deg S_*)=e.
}
\tag{3.28}
\]

The resultant also excludes a common zero at every source point, so \(v_*\)
is a source unit.  This is a base-field direction and is fixed once for the
whole residue line.

## 4. Pair exchange dichotomy on one residue line

Choose the complete reciprocal source unit \(v_*\) from (3.28).  For two
distinct actual line locators \(q_0,q_1\), let

\[
R_i=\operatorname{rep}_{\le e}(q_iv_*),
\qquad i=0,1,
\tag{4.1}
\]

and name \(A=R_0\), \(B=R_1\).  Then

\[
\gcd(A,B)=1,\qquad d=\max(\deg A,\deg B)=e.
\tag{4.2}
\]

Every further projective point on the line has the form

\[
q_z\equiv a q_0+b q_1\pmod{\Lambda_\Sigma},
\tag{4.3}
\]

and its \(v_*\)-product representative is

\[
aA+bB.
\tag{4.4}
\]

Let \(Y_0,Y_z\subset V\) be the locator root sets.  Remove their common
part and put

\[
C_0=Y_0\cap Y_z,\qquad
P_0=\Lambda_{Y_0\setminus C_0},\qquad
P_z=\Lambda_{Y_z\setminus C_0},
\tag{4.5}
\]

\[
\Delta=|Y_0\setminus Y_z|
=\deg P_0=\deg P_z.
\tag{4.6}
\]

On \(\Sigma\), the two descriptions of \(q_z/q_0\) give

\[
\Lambda_\Sigma
\mid
A P_z-(aA+bB)P_0.
\tag{4.7}
\]

The polynomial in (4.7) has degree at most \(d+\Delta\).  Hence exactly one
of the following holds.

### Nonzero branch

If the polynomial is nonzero, then

\[
\boxed{\Delta\ge s-d.}
\tag{4.8}
\]

### Exact root-swap branch

If the polynomial is zero, then \(b\ne0\) and

\[
\gcd(A,aA+bB)=1.
\]

Unique factorization in (4.7) gives, up to nonzero constants,

\[
\boxed{A=P_0,\qquad aA+bB=P_z,\qquad \Delta=d.}
\tag{4.9}
\]

Thus the zero branch is not cancellation.  It is an exact split-polynomial
root-swap pencil with a fixed common locator core.

## 5. The generic direction fixes the exact-swap degree

For any two distinct projective parameters on \(U\), their product
polynomials are two independent linear combinations of \(A,B\).  Their gcd
is therefore \(\gcd(A,B)=1\).  The degree-\(e\) leading coefficient is one
nonzero linear form on the projective parameter line, so it vanishes at at
most one parameter.  Consequently, for every distinct pair,

\[
d=\max(\deg A_\alpha,\deg A_\beta)=e.
\tag{5.1}
\]

In the exact branch, (4.9) now gives

\[
\boxed{\Delta=e=134{,}944.}
\tag{5.2}
\]

In the nonzero branch, (4.8) gives

\[
\Delta\ge s-e=c=67{,}472.
\tag{5.3}
\]

Combining the two branches proves the exact line-distance guard

\[
\boxed{
q_0\ne q_z
\quad\Longrightarrow\quad
|Y_0\setminus Y_z|\ge c=67{,}472.
}
\tag{5.4}
\]

This is the first deployed source restriction that rules out the unrestricted
one-root pencil (1.1).

## 6. Exact-swap components have size at most seven

Consider the graph on admitted locators in one fixed residue line, joining
two locators when their relation is the zero branch of (4.7).  In a connected
component, (4.9) and unique factorization force a common monic core \(Q\) and
a coprime polynomial pencil:

\[
q_\alpha=Q\,C_\alpha,\qquad
C_\alpha=\alpha A+\beta B,\qquad
\deg C_\alpha=d.
\tag{6.1}
\]

Distinct pencil members \(C_\alpha,C_\beta\) are coprime.  Their degree-\(d\)
root sets in \(V\) are therefore pairwise disjoint.  Since
\(\deg Q=J-d\), the available roots outside the common core number
\(|V|-J+d\).  Hence

\[
|\mathcal C|
\le
\left\lfloor\frac{|V|-J+d}{d}\right\rfloor
=
1+\left\lfloor\frac{|V|-J}{d}\right\rfloor.
\tag{6.2}
\]

By (5.2), \(d=e\).  At the deployed row,

\[
|V|-J=913{,}631
\tag{6.3}
\]

and therefore

\[
\boxed{
|\mathcal C|
\le
1+\left\lfloor\frac{913{,}631}{134{,}944}\right\rfloor
=7.
}
\tag{6.4}
\]

This pays the exact-swap multiplicity inside one component relative to the
fixed generic reciprocal direction.  It does not
bound how many large-exchange components one primitive residue line may
contain.

## 7. Projective-direction source-map deduplication

Let \(u_0,u_1\in F\otimes_B\mathcal R_B\) be the two actual translated
source coordinates.  For an occupied projective residue direction

\[
P=[q]\in\mathbf P(W_B),
\tag{7.1}
\]

let

\[
R_q=\operatorname{rep}_{\le e}(qu_0),
\qquad
S_q=\operatorname{rep}_{\le e}(qu_1).
\tag{7.2}
\]

These representatives are unique because

\[
e=134{,}944<s=202{,}416.
\tag{7.3}
\]

Changing \(q\) by a nonzero base scalar changes both representatives by
the same scalar.  Hence the finite source-map image

\[
\mathcal I_P=
\left\{
\eta\in F:
[\eta:1]=[-R_q(x):S_q(x)]
\text{ for some }x\in D\setminus\Sigma
\right\}
\tag{7.4}
\]

depends only on \(P\), not on the chosen representative and not on which
monic split locator lifts \(P\).

The already-proved moving-root equation sends every selected slope whose
actual locator has projective residue \(P\) into \(\mathcal I_P\).  No
injectivity is needed, so

\[
\boxed{|\mathcal I_P|\le |D\setminus\Sigma|
=|V|=1{,}894{,}736.}
\tag{7.5}
\]

Let \(\mathscr P\subset\mathbf P(W_B)\) be the set of occupied projective
residue directions and put \(N_{\rm pt}=|\mathscr P|\).  The complete
rank-three slope set therefore satisfies

\[
\boxed{
\#\Gamma_{\operatorname{rank}=3}
\le |V|N_{\rm pt}.
}
\tag{7.6}
\]

In particular, arbitrary multiplicity of monic locator lifts above one
projective point costs nothing further in this ledger.

The active reserve permits

\[
N_{\rm pt}\le
\left\lfloor
\frac{270{,}780{,}212{,}960{,}575{,}880}{1{,}894{,}736}
\right\rfloor
=142{,}911{,}842{,}578.
\tag{7.7}
\]

There is now a sharper sufficient local theorem.  Suppose every projective
line in \(\mathbf P(W_B)\simeq\mathbf P^2(B)\) contains at most \(68\)
points of \(\mathscr P\).  Choose one occupied point \(P_0\).  Summing the
unweighted point counts on the \(p+1\) lines through \(P_0\) gives

\[
N_{\rm pt}+p\le68(p+1),
\]

and hence

\[
\boxed{
N_{\rm pt}\le67p+68=142{,}757{,}331{,}079.
}
\tag{7.8}
\]

The resulting slope charge is

\[
142{,}757{,}331{,}079\cdot1{,}894{,}736
=270{,}487{,}454{,}459{,}300{,}144,
\tag{7.9}
\]

leaving exact reserve margin

\[
\boxed{292{,}758{,}501{,}275{,}736.}
\tag{7.10}
\]

The adjacent cap \(69\) does not close by this argument:

\[
(68p+69)|V|
=274{,}524{,}580{,}645{,}231{,}568
>B_{\rm rem}
\tag{7.11}
\]

by \(3{,}744{,}367{,}684{,}655{,}688\).

Thus the exact local target is no longer weighted locator occupancy
\(130\).  It is the unweighted statement

\[
\boxed{
|\ell\cap\mathscr P|\le68
\quad\text{for every projective residue line }\ell.
}
\tag{7.12}
\]

### 7.1 The fixed source-coordinate collision divisor

The source-map family on one residue line has an additional exact
linearization.  Let \(u_0,u_1\) be the translated source coordinates and
choose projective generators \(q_0,q_1\) of \(U\).  Put

\[
R_i=\operatorname{rep}_{\le e}(q_i u_0),
\qquad
S_i=\operatorname{rep}_{\le e}(q_i u_1),
\qquad i=0,1.
\tag{7.13}
\]

For \(q_\lambda=a q_0+b q_1\), uniqueness of degree-at-most-\(e\)
representatives gives

\[
R_\lambda=aR_0+bR_1,
\qquad
S_\lambda=aS_0+bS_1.
\tag{7.14}
\]

At every \(\sigma\in\Sigma\), the two rows are products of the same source
coordinate pair by \(q_0(\sigma)\) and \(q_1(\sigma)\).  Therefore

\[
\Lambda_\Sigma
\mid
R_0S_1-R_1S_0.
\]

Since the determinant has degree at most \(2e\), there is one fixed
polynomial \(H_U\) such that

\[
\boxed{
R_0S_1-R_1S_0=\Lambda_\Sigma H_U,
\qquad
\deg H_U\le2e-s=c=67{,}472.
}
\tag{7.15}
\]

For any two projective parameters
\(\lambda=[a:b]\), \(\mu=[c:d]\), bilinearity gives

\[
R_\lambda S_\mu-R_\mu S_\lambda
=(ad-bc)\Lambda_\Sigma H_U.
\tag{7.16}
\]

Thus \(H_U\) is basis-independent up to a nonzero scalar and controls every
same-root collision between source maps on the line.  If \(H_U=0\), all
line directions define the same projective source map wherever that map is
defined.  Suppose now that \(H_U\ne0\).  If
\(x\in V=D\setminus\Sigma\) and \(H_U(x)\ne0\), the matrix

\[
\begin{pmatrix}
R_0(x)&R_1(x)\\
S_0(x)&S_1(x)
\end{pmatrix}
\]

is nonsingular.  Consequently the map

\[
[a:b]\longmapsto[-R_\lambda(x):S_\lambda(x)]
\tag{7.17}
\]

is injective on \(\mathbf P^1(B)\).  Failure of injectivity at a fixed
carrier point can occur only at a root of \(H_U\), and hence at no more than
\(c\) carrier points:

\[
\boxed{
\#\{x\in V:\text{two line directions have the same source-map value at }x\}
\le c.
}
\tag{7.18}
\]

The zero branch and the nonzero branch are therefore both explicit.  Define
two occupied projective directions to be equivalent when their projective
source maps are the same rational map.  This is a global equivalence
relation.  For any two distinct occupied points \(P,Q\), their joining
residue line has \(H_U=0\) exactly when \(P\) and \(Q\) are equivalent.
Consequently:

* if \(H_U=0\), all occupied points of \(U\) belong to one map class;
* if \(H_U\ne0\), no two occupied points of \(U\) belong to the same map
  class.

Choose the first occupied point in every map class.  The representative set
meets an \(H_U=0\) line in at most one point, and it meets an \(H_U\ne0\)
line in exactly the number of distinct occupied maps on that line.  Hence a
cap \(68\) on distinct maps on every transversal line gives
\[
N_{\rm map}\le67p+68.
\tag{7.18a}
\]
Every map class contributes selected slopes from one image of size at most
\(|V|\), so
\[
\#\Gamma_{\operatorname{rank}=3}\le |V|N_{\rm map}.
\tag{7.18b}
\]
Thus the local theorem need only exclude \(69\) occupied points on a line
with \(H_U\ne0\).  Lines with \(H_U=0\) are already deduplicated to one
map class.  In the nonzero branch all but at most \(c\) carrier points are
transversal in the projective direction.

This does not by itself upper-bound the union of source-map images, because
collisions may use different carrier points.  It does remove arbitrary
same-root overlap from the remaining problem.  A proof of the \(68\)-point
cap may now split into the at-most-\(c\) exceptional roots of \(H_U\) and
the transversal incidence relation (7.17).  Identifying low-degree
\(H_U\) with the already-paid effective-multiplier owner requires a
same-object adapter and is not assumed here.

### 7.2 Equality has no per-direction gcd budget

The reciprocal-kernel normalization writes

\[
h=r+x-e
\tag{7.19}
\]

and divides the actual multiplier by an extra outside-source common factor
of degree \(h\).  In the present equality stratum \(h=0\).  Hence this
factor is a nonzero constant, and for every occupied projective direction
\(P=[q]\) the actual products

\[
\left(
\operatorname{rep}_{\le e}(qu_0),
\operatorname{rep}_{\le e}(qu_1)
\right)
\tag{7.20}
\]

are already coprime and have exact projective degree \(e\).

This is a useful route cut.  The polynomial \(H_U\) in (7.15) is a
collision divisor for the whole projective line; it is not a common factor
of an occupied pair in (7.20).  At a carrier root of \(H_U\), the
two-by-two evaluation matrix has a projective kernel direction.  Any such
kernel direction has a common zero in its two source products and therefore
is not occupied.  Thus roots of \(H_U\) can exclude exceptional directions,
but they assign no positive gcd degree to the occupied directions:

\[
\boxed{
\sum_{P\in\mathscr P\cap U}
\deg\gcd(R_P,S_P)=0.
}
\tag{7.21}
\]

In particular, the cap \(68\) cannot be proved by distributing
\(\deg H_U\le c\) as a per-direction gcd budget.

### 7.3 Exact-swap components force a selector rank defect

Retain one exact-swap component \(\mathcal C\) of size \(m\ge2\).  By
(6.1), its actual complement locators have the form

\[
q_i=Q\,C_i,\qquad 1\le i\le m,
\tag{7.22}
\]

where

\[
\deg Q=J-e,\qquad \deg C_i=e,
\tag{7.23}
\]

and the root sets of the \(C_i\) are pairwise disjoint subsets of \(V\).
Let

\[
Y_i=Z(Q)\sqcup Z(C_i),\qquad Z_i=V\setminus Y_i
\tag{7.24}
\]

be the complement locator and common-zero set of the corresponding graph
line.  Their common zero set is

\[
Z_{\mathcal C}
=
\bigcap_{i=1}^m Z_i
=
V\setminus
\left(Z(Q)\sqcup\bigsqcup_{i=1}^m Z(C_i)\right),
\tag{7.25}
\]

so exactly

\[
\boxed{
|Z_{\mathcal C}|
=
|V|-J-(m-1)e.
}
\tag{7.26}
\]

Let \(G_{Z_{\mathcal C}}\) be the matrix of the actual \(K_0\)-generator
rows indexed by this set.  If it had rank eight, it would contain an
independent eight-row subset \(B\).  Then \(B\subseteq Z_i\) for every
\(i\).  The same-selector basis-reconstruction theorem would make every
one of the \(m\) graph lines equal to the unique line \(L_B\).  Its
common-zero set and monic complement locator are unique, so all \(q_i\)
would coincide, contrary to \(m\ge2\).  Therefore

\[
\boxed{
\operatorname{rank}G_{Z_{\mathcal C}}\le7.
}
\tag{7.27}
\]

The component cap \(m\le7\) makes this a large-set rank defect:

\[
|Z_{\mathcal C}|
\ge
|V|-J-6e
=
103{,}967.
\tag{7.28}
\]

For a two-point component, the common zero set is even larger:

\[
|Z_{\mathcal C}|=|V|-J-e=778{,}687.
\tag{7.29}
\]

There is an equivalent polynomial form.  The actual selector space
\(K_0\) lies in the weighted Reed--Solomon carrier code

\[
K_V=[\,|V|,\nu,R+1\,]_F,\qquad
R=n-k=1{,}048{,}576,\qquad
\nu=|V|-R=846{,}160.
\tag{7.30}
\]

By (7.27), some nonzero \(w_{\mathcal C}\in K_0\) vanishes on
\(Z_{\mathcal C}\).  Writing the generalized-Reed--Solomon word as

\[
w_{\mathcal C}(x)
=
\rho_x P_{\mathcal C}(x),
\qquad \rho_x\ne0,\qquad
\deg P_{\mathcal C}\le\nu-1,
\tag{7.31}
\]

gives

\[
P_{\mathcal C}
=
\Lambda_{Z_{\mathcal C}}H_{\mathcal C}
\tag{7.32}
\]

with

\[
\boxed{
\deg H_{\mathcal C}
\le
\nu-1-|Z_{\mathcal C}|
=
(m-1)e-c.
}
\tag{7.33}
\]

In particular, a two-point exact-swap component emits a nonzero
same-selector \(K_0\)-word with quotient degree at most

\[
e-c=c=67{,}472.
\tag{7.34}
\]

The factorization also forces source-scale mass on the moving blocks.  Let
\[
\mathcal M_{\mathcal C}
=\bigsqcup_{i=1}^m Z(C_i),
\qquad |\mathcal M_{\mathcal C}|=me.
\]
For any nonzero word in the kernel of \(G_{Z_{\mathcal C}}\), the same
argument as (7.31)--(7.33) gives
\[
w(x)=\rho_x\Lambda_{Z_{\mathcal C}}(x)H(x),
\qquad
\deg H\le(m-1)e-c.
\]
The factor \(\Lambda_{Z_{\mathcal C}}\) is nonzero on every moving-block
coordinate.  A nonzero \(H\) has at most \((m-1)e-c\) roots there, so
\[
\boxed{
\operatorname{wt}\!\left(w|_{\mathcal M_{\mathcal C}}\right)
\ge
me-\bigl((m-1)e-c\bigr)
=e+c=s=202{,}416.
}
\tag{7.35}
\]
In particular every such word meets at least two moving blocks.  When
\(m=2\), the same degree-\(c\) polynomial can vanish at at most \(c\)
points of either degree-\(e\) block, and hence
\[
\boxed{
\operatorname{wt}\!\left(w|_{Z(C_i)}\right)
\ge e-c=c=67{,}472
\quad(i=1,2).
}
\tag{7.36}
\]

This is a baseline-free collective-rank precursor rooted in the actual
selector.  It is not the active intrinsic deep-MCA predicate, which bounds
the actual error support of one selected slope, and it is not by itself the
active source-rational predicate, which requires one qualifying source-map
pair attached to the same slopes.  The existing rank-nine incidence packets
also leave selector-dependent low-rank aggregation open.  No current owner
therefore pays (7.27) or (7.33) without a new same-object adapter.

There is a tempting but invalid numerical shortcut here.  The two-point
quotient bound satisfies

\[
\deg H_{\mathcal C}\le c=67{,}472
<
E(s)=\left\lfloor\frac{s-1}{2}\right\rfloor
=101{,}207.
\tag{7.37}
\]

The source-rational owner nevertheless does not apply.  It requires a
coprime pair of polynomial lifts whose quotient map agrees with the fixed
source labels on all of \(\Sigma\), together with moving-root
transversality for the same selected slopes.  In contrast,
\(H_{\mathcal C}\) is the residual factor of one zero-syndrome
\(K_0\)-word.  It supplies neither a second coordinate nor the source-anchor
identities.  Moreover equality has \(h=0\), so every actual occupied
source-product pair is already coprime of exact reduced degree

\[
e=134{,}944=E(s)+33{,}737.
\tag{7.38}
\]

Thus (7.35) cannot be substituted for a qualifying low-degree source map.
The other active owners also do not accept the precursor:

* the tangent owner is fixed by the source labels before the selector;
* the deep-MCA owner requires one selected slope's actual error support to
  be at most \(349{,}525\), whereas \(w_{\mathcal C}\) is a codeword
  difference and every nonzero carrier-code word has weight at least
  \(R+1=1{,}048{,}577\);
* the C5/base and twist owners are pair-global source predicates already
  deleted before this selector;
* the Frobenius owner requires an attached effective multiplier of degree
  at most \(9{,}208\), while (7.33) neither gives that degree nor identifies
  \(H_{\mathcal C}\) with the effective multiplier; and
* the field-native branch-2 rank owner tests the Hankel rank of an actual
  selected error, not the restriction rank of \(K_0\) on
  \(Z_{\mathcal C}\).

Consequently the component branch is not an unrecognized instance of a
current scalar owner.  A completion must either construct a new
same-selector collective-rank owner with a global distinct-slope cap, or
derive one of the existing owner predicates at one of the component's
actual selected slopes using additional selector equations.

### 7.4 A 69-point packet can be made simultaneously nonexact

The component split is useful structure for one fixed reciprocal direction,
but it is not necessary in the final \(69\)-point reduction.  Let
\[
\mathscr Q=\{q_1,\ldots,q_M\}\subset U,
\qquad M\le69,
\tag{7.39}
\]
be distinct occupied directions.  For \(i\ne j\), remove the common roots
of their actual locators and write
\[
P_{ij}=\Lambda_{Y_i\setminus Y_j},
\qquad
P_{ji}=\Lambda_{Y_j\setminus Y_i},
\qquad
\deg P_{ij}=\deg P_{ji}=\Delta_{ij}.
\tag{7.40}
\]

Parameterize the complete reciprocal space by
\(\lambda\in B^3\), and let \(A_i(\lambda)\) be the unique
degree-at-most-\(e\) representative of the product of \(q_i\) with that
reciprocal direction.  The pair numerator
\[
\mathcal E_{ij}(\lambda)
=
A_i(\lambda)P_{ji}-A_j(\lambda)P_{ij}
\tag{7.41}
\]
is divisible by \(\Lambda_\Sigma\).  Its quotient
\[
T_{ij}(\lambda)
=\mathcal E_{ij}(\lambda)/\Lambda_\Sigma
\tag{7.42}
\]
depends \(B\)-linearly on \(\lambda\).

This linear map is not identically zero.  Otherwise every complete
reciprocal column would satisfy
\[
A_iP_{ji}=A_jP_{ij}.
\]
The two complete product rows for \(q_i,q_j\) would then be proportional
over \(B(X)\).  Since two distinct projective points span \(U\), this would
give rank one for a row basis of the complete line module, contradicting
\(L_U=\mathcal M_U\) and \(\operatorname{rank}\mathcal M_U=2\).

Choose one nonzero coefficient functional
\(\ell_{ij}(\lambda)\) of \(T_{ij}(\lambda)\), canonically by the fixed
coefficient order.  The product
\[
\mathcal L_{\mathscr Q}(\lambda)
=
\prod_{1\le i<j\le M}\ell_{ij}(\lambda)
\tag{7.43}
\]
is a nonzero polynomial of degree
\[
\binom M2\le\binom{69}{2}=2{,}346
<p=2{,}130{,}706{,}433.
\tag{7.44}
\]
A nonzero polynomial over \(B=\mathbf F_p\) whose degree in every variable
is below \(p\) cannot vanish on all of \(B^3\).  Hence there is a nonzero
reciprocal parameter \(\lambda_{\mathscr Q}\) such that
\[
\boxed{
T_{ij}(\lambda_{\mathscr Q})\ne0
\quad\text{for every }i<j.
}
\tag{7.45}
\]
The first such parameter in the fixed projective order is canonical.

Every pair is now in the nonzero branch simultaneously.  Since
\(\deg A_i(\lambda_{\mathscr Q})\le e\), degree comparison in (7.41) gives
\[
\boxed{
\Delta_{ij}\ge s-e=c
}
\tag{7.46}
\]
and the sharper quotient bound
\[
\boxed{
\deg T_{ij}(\lambda_{\mathscr Q})
\le e+\Delta_{ij}-s
=\Delta_{ij}-c.
}
\tag{7.47}
\]
In particular, every minimum-exchange edge \(\Delta_{ij}=c\) has a nonzero
constant quotient.

Thus nontrivial exact-swap components and their unpaid rank precursors can
be bypassed when proving the cap \(68\): any proposed \(69\)-point packet
admits one canonical reciprocal direction for which all \(2{,}346\) pair
relations are nonzero.  The component rank theorem remains useful optional
structure for fixed directions, but a component-to-owner adapter is no
longer on the shortest proof path.

### 7.5 Every pair also has an actual-selector secant word

The selector gives a parallel degree budget on every pair, not only on
exact-swap components.  Let the graph-line coefficient pairs be
\[
(a_i,b_i),\qquad (a_j,b_j),
\]
so that \(a_i-a_j,b_i-b_j\in K_0\).  Put
\[
Z_{ij}=Z_i\cap Z_j.
\tag{7.48}
\]
If \(G_{Z_{ij}}\) had rank eight, an independent eight-subset of \(Z_{ij}\)
would reconstruct both graph lines as the same canonical line.  Therefore
\[
\boxed{\operatorname{rank}G_{Z_{ij}}\le7.}
\tag{7.49}
\]

The two difference words vanish on \(Z_{ij}\), and they are not both zero
because the graph lines are distinct.  If
\[
\Delta_{ij}=|Y_i\setminus Y_j|=|Y_j\setminus Y_i|,
\]
then
\[
|Z_{ij}|=|V|-J-\Delta_{ij}.
\tag{7.50}
\]
Every nonzero word \(w\) in
\[
\operatorname{span}\{a_i-a_j,b_i-b_j\}
\tag{7.51}
\]
therefore has the GRS factorization
\[
w(x)=\rho_x\Lambda_{Z_{ij}}(x)H_{ij,w}(x),
\qquad
\boxed{\deg H_{ij,w}\le\Delta_{ij}-c.}
\tag{7.52}
\]

On the disjoint exchange union
\[
(Y_i\setminus Y_j)\sqcup(Y_j\setminus Y_i)
\]
the factor \(\Lambda_{Z_{ij}}\) is nonzero.  Its size is
\(2\Delta_{ij}\), while \(H_{ij,w}\) has at most
\(\Delta_{ij}-c\) roots.  Hence
\[
\boxed{
\operatorname{wt}\!\left(
w|_{(Y_i\setminus Y_j)\sqcup(Y_j\setminus Y_i)}
\right)
\ge\Delta_{ij}+c.
}
\tag{7.53}
\]
For a minimum-exchange edge \(\Delta_{ij}=c\), the quotient is a nonzero
constant and the secant word is nonzero at all \(2c\) exchange
coordinates.

At this stage the remaining \(69\)-point theorem appears to have two edge
records on every pair:

1. the simultaneous source/reciprocal quotient
   \(0\ne T_{ij}\), \(\deg T_{ij}\le\Delta_{ij}-c\);
2. a nonzero actual-selector \(K_0\) secant word with a quotient of the same
   degree and exchange-block weight at least \(\Delta_{ij}+c\).

The next subsection proves that these records are exactly the same object.
Thus no coupling hypothesis is imported from this provisional formulation.

### 7.6 The source quotient is exactly the selector secant quotient

At the equality endpoint the coupling can be written explicitly.  Let
\((P_i,Q_i)\) be the degree-\(<k\) graph-line polynomial lifts, so
\[
a_i=\epsilon_0-\operatorname{ev}(P_i),
\qquad
b_i=\epsilon_1-\operatorname{ev}(Q_i).
\tag{7.54}
\]
Full-outside equality gives \(D=V\sqcup\Sigma\).  The complete
outside-source common gcd is \(\Lambda_{Z_i}\), because \(h=0\).  If
\[
R_i=\operatorname{rep}_{\le e}(q_i u_0),
\qquad
S_i=\operatorname{rep}_{\le e}(q_i u_1),
\tag{7.55}
\]
then uniqueness of degree-at-most-\(e\) source representatives gives
\[
\boxed{
P_i=\Lambda_{Z_i}R_i,
\qquad
Q_i=\Lambda_{Z_i}S_i.
}
\tag{7.56}
\]
Indeed, the source-multiplier construction gives, in
\(F[X]/(\Lambda_\Sigma)\),
\[
u_\ell=\Lambda_V^{-1}\epsilon_\ell,\qquad
q_i=\Lambda_{Y_i}=\Lambda_V/\Lambda_{Z_i}
\quad(\ell=0,1).
\]
Therefore
\[
q_i u_\ell=\epsilon_\ell/\Lambda_{Z_i}
\quad\text{on }\Sigma.
\]
After division by \(\Lambda_{Z_i}\), both sides of (7.56) have degree at
most \(e\) and agree at all \(s>e\) source points.  This also binds (7.56)
to the actual graph-line lifts rather than to an auxiliary representative.

For \((\alpha,\beta)\in F^2\), put
\[
v_{\alpha,\beta}=\alpha u_0+\beta u_1,
\qquad
A_i^{\alpha,\beta}=\alpha R_i+\beta S_i.
\tag{7.57}
\]
Let \(T_{ij}^{\alpha,\beta}\) be the quotient in (7.42) formed from these
products.  Since
\[
\Lambda_{Z_i}
=\Lambda_{Z_{ij}}P_{ji},
\qquad
\Lambda_{Z_j}
=\Lambda_{Z_{ij}}P_{ij},
\tag{7.58}
\]
equations (7.41), (7.54), and (7.56) give the exact polynomial identity
\[
\boxed{
\alpha(a_i-a_j)+\beta(b_i-b_j)
=
-\operatorname{ev}_D\!\left(
\Lambda_\Sigma\Lambda_{Z_{ij}}
T_{ij}^{\alpha,\beta}
\right).
}
\tag{7.59}
\]
The polynomial on the right has degree at most
\[
s+(|V|-J-\Delta_{ij})+(\Delta_{ij}-c)
=s+|V|-J-c
=k-1.
\tag{7.60}
\]
After shortening from \(D\) to \(V\), its GRS quotient is exactly
\(-T_{ij}^{\alpha,\beta}\), up to the fixed nonzero coordinate
multipliers.  Thus the two edge records in Section 7.5 are the same object,
not merely objects with matching degree bounds.

For each pair, the restriction
\[
(\alpha,\beta)\longmapsto T_{ij}^{\alpha,\beta}
\tag{7.61}
\]
is nonzero.  If both \(T_{ij}^{1,0}\) and \(T_{ij}^{0,1}\) vanished, (7.59)
would give \(a_i=a_j\) and \(b_i=b_j\), so the two graph lines would
coincide.  Hence each pair excludes at most one point of
\(\mathbf P^1(F)\).

At each source point \(\sigma\), the nonzero pair
\((u_0(\sigma),u_1(\sigma))\) excludes at most one projective parameter for
which \(v_{\alpha,\beta}(\sigma)=0\).  Equality \(h=0\) also says that
\((R_i,S_i)\) is coprime for every occupied direction.  Hence at each
\((i,x)\in\mathscr Q\times V\), the pair
\((R_i(x),S_i(x))\) is nonzero and excludes at most one parameter for which
\(A_i^{\alpha,\beta}(x)=0\).  Therefore a packet of at most \(69\)
directions has at most
\[
s+69|V|+\binom{69}{2}
=202{,}416+130{,}736{,}784+2{,}346
=130{,}941{,}546
<p<|F|+1
\tag{7.62}
\]
forbidden parameters.  The first remaining parameter in the fixed
projective order gives one canonical full-domain source-unit reciprocal
direction
\(v_{\mathscr Q}^{\rm src}\) satisfying
\[
\boxed{
v_{\mathscr Q}^{\rm src}(\sigma)\ne0
\quad(\sigma\in\Sigma),
\qquad
A_i^{\rm src}(x)\ne0
\quad(i\le|\mathscr Q|,\ x\in V),
\qquad
T_{ij}^{\rm src}\ne0
\quad(i<j).
}
\tag{7.63}
\]

Consequently every edge of a candidate \(69\)-point packet now carries one
nonzero actual \(K_0\) secant whose exact shortened quotient is the
simultaneous source quotient:
\[
\deg T_{ij}^{\rm src}\le\Delta_{ij}-c,
\qquad
\boxed{
\operatorname{wt}_{\rm exch}(w_{ij}^{\rm src})
=2\Delta_{ij}.
}
\tag{7.64}
\]
Indeed, on \(Z_i\setminus Z_j\) the \(i\)-th graph polynomial vanishes and
the \(j\)-th equals a nonzero locator factor times
\(A_j^{\rm src}(x)\ne0\); the symmetric statement holds on
\(Z_j\setminus Z_i\).  Thus the edge difference is nonzero at every
exchange coordinate.  Equivalently, \(T_{ij}^{\rm src}\) has no root on
either exchange block.

The remaining theorem is no longer a source/selector coupling problem.  It
is a packing or owner-emission theorem for this single canonical complete
graph of actual selector secants.

### 7.7 Canonical bounded circuits and the no-singleton partition

For the parameter selected in Section 7.6, define the vertex word
\[
c_i^{\rm src}
=
\alpha a_i+\beta b_i
=
\epsilon_{\rm src}
-\operatorname{ev}_D(F_i),
\qquad
F_i=\Lambda_{Z_i}A_i^{\rm src}.
\tag{7.65}
\]
Here \(\epsilon_{\rm src}=\alpha\epsilon_0+\beta\epsilon_1\), and
\[
F_i(x)\ne0\quad\Longleftrightarrow\quad x\in Y_i
\qquad(x\in V)
\tag{7.66}
\]
by the full-domain choice in (7.63).

Orient the edge words by
\[
w_{ij}=c_i^{\rm src}-c_j^{\rm src}.
\tag{7.67}
\]
Then
\[
w_{ij}+w_{jk}+w_{ki}=0
\tag{7.68}
\]
and (7.59) becomes
\[
w_{ij}
=-\operatorname{ev}_D\!\left(
\Lambda_\Sigma\Lambda_{Z_{ij}}T_{ij}^{\rm src}
\right).
\tag{7.69}
\]
Evaluation is injective on degree-\(<k\) polynomials.  Dividing the
polynomial form of (7.68) by \(\Lambda_\Sigma\) therefore gives the exact
quotient cocycle
\[
\boxed{
\Lambda_{Z_{ij}}T_{ij}^{\rm src}
+\Lambda_{Z_{jk}}T_{jk}^{\rm src}
+\Lambda_{Z_{ki}}T_{ki}^{\rm src}=0.
}
\tag{7.70}
\]

Now fix the first vertex and put
\[
\mathcal W_*=
\operatorname{span}_F\{w_{1i}:2\le i\le M\}\subseteq K_0.
\tag{7.71}
\]
Since \(\dim_FK_0=8\), let
\[
d_*=\dim_F\mathcal W_*\le8.
\tag{7.72}
\]
Choose the first \(d_*\) independent star edges in the fixed packet order.
For every nonbasis vertex \(j\), its star edge has a unique expansion
\[
w_{1j}=\sum_{b\in B_j}\gamma_{j,b}w_{1b},
\qquad
\gamma_{j,b}\ne0,
\qquad
|B_j|\le d_*\le8,
\tag{7.73}
\]
after deleting zero coefficients.  Thus
\[
\boxed{
\Lambda_{Z_{1j}}T_{1j}^{\rm src}
-\sum_{b\in B_j}
\gamma_{j,b}\Lambda_{Z_{1b}}T_{1b}^{\rm src}=0
}
\tag{7.74}
\]
is a canonical source/selector circuit with at most \(9\) nonzero edge
terms.  If \(M=69\), there are at least
\[
M-1-d_*\ge69-1-8=60
\tag{7.75}
\]
such circuits, one for every nonbasis vertex.

Expanding (7.73) through (7.67) gives an affine relation
\[
\sum_{i\in C_j}\lambda_{j,i}c_i^{\rm src}=0,
\qquad
\sum_{i\in C_j}\lambda_{j,i}=0,
\qquad
|C_j|\le10.
\tag{7.76}
\]
Delete zero coefficients and then take the unique minimal dependent subset
in the fixed order.  Distinct graph records cannot form a two-element
circuit: proportional \(F_i,F_j\) would have the same exact carrier zero
set \(Z_i=Z_j\), hence the same monic locator.  Therefore the resulting
actual-record circuit satisfies
\[
3\le|C_j|\le10
\tag{7.77}
\]
and every coefficient in (7.76) is nonzero.

For \(A\subseteq C_j\), form the exact carrier atom
\[
V_A=
\{x\in V:x\in Y_i\ \Longleftrightarrow\ i\in A\}.
\tag{7.78}
\]
If \(A=\{i\}\) were a singleton and \(x\in V_A\), then (7.66) would leave
exactly one nonzero term in the corresponding polynomial form of (7.76),
a contradiction.  Hence
\[
\boxed{V_{\{i\}}=\varnothing\quad(i\in C_j).}
\tag{7.79}
\]
Equivalently, every carrier root used by one locator in a circuit is used
by at least one other locator in that circuit:
\[
\boxed{
Y_i\subseteq\bigcup_{\substack{h\in C_j\\h\ne i}}Y_h
\quad(i\in C_j).
}
\tag{7.80}
\]

This is a bounded-size, same-object partition precursor: it is built from
the actual graph records, actual \(K_0\) secants, exact source quotients, and
the fixed first-match packet.  It is not yet a paid active partition.  The
remaining local theorem can now be stated on circuits of at most ten records
rather than on an unstructured \(69\)-point line:

> **Bounded-circuit owner/partition emission.**  Every actual circuit
> satisfying (7.69), (7.74), (7.77), and (7.79) either emits an already-paid
> owner at one of its graph records or belongs to a family whose total line
> occupancy is at most \(68\).

### 7.8 Every minimal circuit forces a collective selector-rank defect

Let \(C\) be a minimal actual-record circuit obtained above and put
\[
m=|C|,\qquad
Z_C=\bigcap_{i\in C}Z_i
=V\setminus\bigcup_{i\in C}Y_i.
\tag{7.81}
\]
Minimal affine dependence means that the affine span of the \(m\) distinct
vertex words has dimension exactly \(m-2\).  After fixing any root
\(i_0\in C\), the secants
\[
\{w_{i_0i}:i\in C\setminus\{i_0\}\}
\tag{7.82}
\]
therefore span an \((m-2)\)-dimensional subspace of \(K_0\).

Every graph polynomial \(F_i=\Lambda_{Z_i}A_i^{\rm src}\) vanishes on
\(Z_C\).  Hence all vertex words restrict there to the same source unit
\(\epsilon_{\rm src}\), and every secant in (7.82) vanishes on \(Z_C\).
The restriction map
\[
K_0\longrightarrow F^{Z_C}
\tag{7.83}
\]
therefore has kernel dimension at least \(m-2\).  Since
\(\dim_FK_0=8\),
\[
\boxed{
\operatorname{rank}(K_0|_{Z_C})\le8-(m-2)=10-m.
}
\tag{7.84}
\]

The no-singleton conclusion (7.79) also gives an exact support count.
Every point of \(\bigcup_iY_i\) occurs in at least two of the \(m\) sets,
while every \(Y_i\) has size \(J\).  Thus
\[
\left|\bigcup_{i\in C}Y_i\right|
\le
\left\lfloor\frac{mJ}{2}\right\rfloor,
\qquad
\boxed{
|Z_C|\ge
\max\left\{0,\ |V|-\left\lfloor\frac{mJ}{2}\right\rfloor\right\}.
}
\tag{7.85}
\]
For a three-record circuit this is nontrivial:
\[
\boxed{
|Z_C|
\ge
1{,}894{,}736
-
\left\lfloor\frac{3\cdot981{,}105}{2}\right\rfloor
=423{,}079,
\qquad
\operatorname{rank}(K_0|_{Z_C})\le7.
}
\tag{7.86}
\]

This rank loss is collective and baseline-free in the limited sense that
it is generated by a minimal relation among distinct actual graph records,
not by the interpolation equation of one witness.  It remains a precursor:
the active partition has no owner whose predicate is merely (7.84), and a
rank defect without the same-record projection and charge is not payment.

## 8. Exact finite controls

The parent \(\mathbf F_{19}\) rank-three fixture has

\[
s=6,\qquad e=4,\qquad c=2,\qquad |V|=12,\qquad J=8.
\]

Its complete reciprocal dimension is three.  On a selected residue line,
the cofactor quotient polynomials have gcd one, so it realizes the primitive
cofactor branch.  Three admitted locators share a six-root core and have
three pairwise-disjoint two-root moving blocks.  Thus

\[
\Delta=c=2,\qquad
|\mathcal C|=3
=1+\left\lfloor\frac{12-8}{2}\right\rfloor.
\tag{8.1}
\]

This shows that the \(c\)-scale exchange threshold can be sharp in an exact
rank-three equality packet.  The verifier also finds a resultant-nonzero
reciprocal direction with coprime degree-\(e\) products; relative to that
direction the two-root relations belong to the nonzero branch, as required
by (5.2).  In fact \(260\) of the \(19^2+19+1\) projective reciprocal
directions pass the coprime exact-degree gate in this fixture; the selected
control has zero generic exact edges and three nonzero exchange edges.

There is also a source-interpolation route cut over \(\mathbf F_{23}\), with

\[
s=6,\qquad e=4,\qquad c=2,\qquad |V|=14,\qquad J=10.
\tag{8.2}
\]

Four split locators occupy one projective residue line, have minimum
Johnson distance \(2=c\), and extend with a fifth locator to an occupied
residue plane of dimension three.  The complete reciprocal space has
dimension three, the product matrix has rank three, and the line cofactor
gcd is one.  Among the \(23^2+23+1\) reciprocal directions, \(403\) give a
coprime exact-degree product pair on the line.  For the canonical first such
direction, all six locator pairs lie in the nonzero exchange branch:

\[
\boxed{
\text{four occupied line points}
=
\text{four distinct exact-swap components}.
}
\tag{8.3}
\]

Its source-coordinate collision divisor has degree \(2=c\) and no root on
the fourteen-point carrier.  Thus the four-component control lies entirely
in the transversal branch of (7.17).

The exhaustive extension check considered all \(839\) residue planes through
this four-point line.  Of these, \(746\) have rank-three product determinant
and \(177\) satisfy the complete coprime source-pair admission; every one of
the \(177\) retains all four line points.

This fixture does not construct the deployed complete selector or replay the
first-match atlas, so it is not a falsifier to the \(68\)-point target.  It is
an exact route cut: rank three, cofactor primitivity, pair distance, and the
generic reciprocal choice do not force all points on one line into one
exact-swap component.  The remaining theorem must genuinely control many
large-exchange components; it cannot obtain the cap by proving one component
per line.

A separate exact diagonal \(3\times3\) polynomial fixture over
\(\mathbf F_{19}\) has determinant \(\Lambda_\Sigma^2\) and cofactor gcd
equal to a prescribed degree-two divisor of \(\Lambda_\Sigma\).  It verifies
that the source-unit identity (3.15) is load-bearing.  The matrix is not a
complete source-valid locator/reciprocal packet and therefore does not
contradict (3.16).

The source-valid searches independently corroborate (3.16):

* the exhaustive \(\mathbf F_{13}\), \(s=6,e=4,c=2\) partition-ratio model
  checked all \(6{,}545\) seed triples, retained \(5{,}336\) post-C5 packets,
  and produced \(14\) rank-three packet types;
* all \(42\) row-pair residue lines in those rank-three types had
  \(\deg g_U=0\);
* the stored \(\mathbf F_{17}\) and \(\mathbf F_{19}\) source-valid
  rank-three samples contributed another \(18\) and \(42\) checked row-pair
  lines, again all with \(g_U=1\).

These finite controls verify the algebra and normalizations but are not used
in the proof of (3.16).  They do not assert an asymptotic line cap.

## 9. Why the rank-16 cap-130 theorem does not transfer

The repository's rank-16 fixed-pair theorem also ends with a numerical cap
\(130\), but that equality of numbers is incidental.  Its frozen source
interface starts with:

* two saturated endpoint candidates;
* common neighbors forming a simple row--column grid;
* row and column degrees at most \(14\);
* complete actual tails of size at least \(62{,}356+c_0\);
* one tail universe of size at most \(913{,}633\);
* disjoint tails on a common row or column;
* transverse intersections at most \(5{,}116-c_0\);
* affine tail-coordinate lines whose copies in one primitive direction
  have total multiplicity at most \(5{,}116-c_0\).

None of these objects is produced by the equality-wall Hilbert--Burch
module.  A projective residue line is the endpoint line itself, not a grid
of common neighbors in an active affine plane.  Its split locators do not
come with the rank-16 complete-tail decomposition, row/column skeleton, or
primitive-direction coloring.  Conversely, cofactor primitivity and the
exchange floor \(67{,}472\) do not imply those hypotheses.

Therefore the rank-16 weighted-arrangement/DPW/extactic theorem cannot be
imported.  A valid reuse would first need a new source theorem constructing
the entire endpoint-grid and complete-tail interface from the actual
equality packet.  That construction is at least as strong as the remaining
incidence problem and is not assumed here.

## 10. The corrected next theorem

The previous weighted local target

\[
M_\ell\le130
\tag{10.1}
\]

remains a sufficient numerical payment only after the actual source and
selector contracts are used.  Section 1 proves that it is false as a bare
locator-cylinder theorem.  Section 7 supersedes it with a smaller,
unweighted target that automatically deduplicates locator lifts.

The source-bound bridge now has one bounded-circuit theorem.

> **KoalaBear equality-wall primitive 69-point exclusion.**  For every
> actual rank-three equality packet and every projective residue line
> \(U\subset W_B\), use the primitive Hilbert--Burch presentation (3.19).
> The occupied projective residue directions on \(U\) number at most \(68\).
> Equivalently, for the canonical reciprocal parameter
> \(\lambda_{\mathscr Q}\) supplied by (7.43)--(7.45), no \(69\) distinct
> occupied directions can support the complete family of nonzero pair
> quotients
> \[
> T_{ij}\ne0,\qquad
> \deg T_{ij}\le\Delta_{ij}-c.
> \]
> Equivalently, the at least \(60\) canonical circuits supplied by
> (7.73)--(7.77), each with the no-singleton partition (7.79) and
> collective rank bound (7.84), cannot all remain primitive: one must emit
> an already-paid owner at one of its same graph records, or a canonical
> packing theorem must bound the total line occupancy by \(68\).

This is strictly narrower than the former weighted line-cap problem:
locator multiplicities have been removed from the ledger, every line is
primitive in the congruence-module sense, and one canonical reciprocal
direction makes every pair relation nonexact at once.  There is no longer a
need to pay exact-swap components before attacking the \(69\)-point packet.
The \(\mathbf F_{23}\) four-point control shows that rank three, cofactor
primitivity, source-map transversality, and pairwise nonzero exchange alone
do not settle the required \(69\)-point scale.

Promising proof routes are:

1. **Bounded-circuit owner emission.**  Classify the actual minimal circuits
   of size \(3\) through \(10\) using their exact quotient cocycle,
   no-singleton carrier partition, and rank bound \(10-m\).  The emitted
   owner must contain one of the same graph records and carry its active
   projection.
2. **Triangle-first rank route.**  A three-record circuit has selector rank
   at most seven on at least \(423{,}079\) common coordinates.  Either match
   this exact collective object to an active rank/saturation predicate or
   prove that a \(69\)-point line necessarily produces enough triangles for
   a separate packing charge.
3. **Primitive module normal form.**  Use \(L_U=\mathcal M_U\) to put all
   line products in one row-reduced two-generator basis with row degrees
   summing to \(s\), then classify the degree-\(e\) split solutions.
4. **Low-excess edge compression.**  Organize the \(2{,}346\) edges by
   \(\Delta_{ij}-c\).  A dense class of bounded excess gives a bounded-degree
   polynomial packet; the complementary class must consume enough distinct
   locator roots to violate the carrier budget or selector incidence.
5. **Fitting-to-rank emission.**  Show that excessive primitive occupancy
   forces a common divisor in the cofactor minors, contradicting (3.16), or
   lowers the complete reciprocal rank to the already-paid rank-two branch.
6. **Optional component rank route.**  The selector-rank and moving-block
   mass theorem (7.27)--(7.36) remains available if a same-object collective
   rank owner is later proved, but it is not required by the shortest
   reduction.

## 11. Scope

This packet proves:

* complete reciprocal dimension exactly three in the rank-three equality
  branch;
* the source-free one-root-pencil obstruction to a bare line cap;
* the canonical rank-two congruence module and its determinant
  \(\Lambda_\Sigma\);
* source-bound cofactor primitivity \(g_U=1\);
* emptiness of the apparent projective first-jet source-partition branch;
* the primitive Hilbert--Burch presentation of the complete line module;
* the pair exchange dichotomy;
* the active minimum exchange distance \(c=67{,}472\);
* the generic reciprocal resultant theorem and exact-swap component cap
  \(7\);
* the four-component primitive rank-three route cut over \(\mathbf F_{23}\);
* the fixed source-coordinate collision divisor
  \(\deg H_U\le c\) and off-divisor direction injectivity;
* the equality-\(h=0\) no-gcd-budget guard for occupied directions;
* the exact-swap component common-zero formula and selector restriction
  rank at most seven on at least \(103{,}967\) coordinates;
* the associated nonzero \(K_0\) generalized-Reed--Solomon word with
  quotient degree at most \((m-1)e-c\), and at most \(c\) for a two-point
  component;
* source-scale moving-block weight at least \(e+c=s\) for every nonzero
  component kernel word, and at least \(c\) on each block when \(m=2\);
* exact separation of that precursor from every current active owner
  predicate;
* simultaneous reciprocal genericization of every packet of at most
  \(69\) directions, producing nonzero pair quotients
  \(\deg T_{ij}\le\Delta_{ij}-c\) on all pairs;
* the exact identity between every source quotient and its actual shortened
  selector-secant quotient;
* a full-domain source-unit parameter making every vertex cofactor nonzero
  on the carrier and every pair secant nonzero on all exchange coordinates;
* the oriented secant cocycle and at least \(60\) canonical fundamental
  circuits in every candidate \(69\)-point packet;
* actual-record circuit size between \(3\) and \(10\), with no singleton
  carrier-membership atom;
* the circuit selector-rank bound
  \(\operatorname{rank}(K_0|_{Z_C})\le10-|C|\);
* the three-record specialization with at least \(423{,}079\) common zeros
  and selector rank at most seven;
* projective-direction and global source-map-class deduplication;
* the sufficient unweighted residue-line cap \(68\), its exact reserve
  margin, and the adjacent cap-\(69\) negative control;
* the exact non-importability ledger for the unrelated rank-16 cap-\(130\)
  theorem.

It does not:

* prove unweighted occupied-point line cap \(68\) in the primitive branch;
* emit a paid same-record owner from the canonical bounded circuits, or
  prove a packing theorem limiting their parent line to \(68\) map classes;
* pay the optional selector rank precursor (7.27)--(7.36) through an active
  same-slope owner;
* pay \(r=134{,}943\);
* move the first open interval;
* add or reorder an owner;
* change the partition digest or reserve.

# PROVED REDUCTION / ROW OPEN
