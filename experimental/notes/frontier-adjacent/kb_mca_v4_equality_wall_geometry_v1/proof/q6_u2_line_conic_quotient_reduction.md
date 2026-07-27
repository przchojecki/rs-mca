# The \(u=2\) Line Exclusion and Conic-Involution Reduction

## 1. Status

This note continues:

```text
proof/q6_u2_plane_map_reduction.md
```

for an actual irreducible component \(H\) of bidegree \((2,4)\).
It proves:

1. the line-image branch is impossible;
2. in the reduced common-pole conic branch, the ten common points
   form five equal-signature orbits of the conic involution;
3. the four free points are the two complete free-root pairs of
   exactly two source rows;
4. the resulting common-signature graph first has three combinatorial
   types, and exact star-conic geometry excludes
   \(P_3\sqcup C_3\);
5. the conic quotient differs from the deployed deck quotient;
6. if both deck branch points lie over \(\mathcal K\), the conic
   branch is impossible.

The remaining conic branch is an exact second-involution
interpolation problem. No owner payment is booked.

## 2. Exact row-divisor ledger

For the six noninvariant source labels, write

\[
q_j(\lambda)=H(\alpha_j,\lambda),
\qquad
D_j=\operatorname{div}(q_j).
\]

Every \(D_j\) has degree four and is a subdivisor of the actual
outgoing row divisor

\[
O_j=\psi^*\mathcal K+bZ_j.
\tag{2.1}
\]

The second summand consists of exactly two distinct simple free
points. The proved component identity is

\[
\boxed{\sum_{j=1}^6D_j=2D_{\mathcal K}+E_H,}
\tag{2.2}
\]

where \(D_{\mathcal K}=\psi^*\mathcal K\) has degree ten and
\(E_H\) is the reduced divisor of the four owned free edges.

At a point of \(D_{\mathcal K}\), the horizontal degree-two
polynomial \(H(T,\lambda)\) has exactly two distinct roots among the
six noninvariant source labels. At a point of \(E_H\), it has
exactly one such root.

## 3. The line-image branch is impossible

Suppose the pole-coefficient image is a line. The proved
factorization is

\[
H(T,\lambda)=a(T)P(\lambda)+b(T)Q(\lambda),
\qquad
\gcd(P,Q)=1.
\tag{3.1}
\]

Hence the six \(q_j\)'s belong to the projective pencil
\(\langle P,Q\rangle\).

### Lemma 3.1

If two nonzero members of \(\langle P,Q\rangle\) share one
projective root, they are proportional.

#### Proof

At a root \(\lambda\), the pair \((P(\lambda),Q(\lambda))\) is
nonzero by coprimality. It imposes one homogeneous linear equation
on the pencil parameter, with one projective solution. \(\square\)

Every row \(j\) must meet \(D_{\mathcal K}\). Otherwise all four
roots of \(q_j\) would have to lie in the two-point free divisor
\(bZ_j\), whose roots are simple. This is impossible.

Choose a common-pole root of \(q_j\). A second row \(k\ne j\)
vanishes there by the exact horizontal-fiber statement. Lemma 3.1
gives

\[
q_j\sim q_k.
\tag{3.2}
\]

Their complete divisors are equal. They cannot contain a free point:
such a point would then occur in two row divisors, while \(E_H\) is
reduced with coefficient one in (2.2). Thus both divisors are
supported on \(D_{\mathcal K}\).

The same argument applies to every row. Therefore no row divisor
contains a free point, contradicting

\[
\deg E_H=4.
\]

Hence:

\[
\boxed{\text{The actual \(u=2\) line-image branch is empty.}}
\tag{3.3}
\]

This is a direct endpoint contradiction. It needs no semantic owner
adapter.

## 4. Conic pullback and its involution

Suppose the coefficient image is a smooth conic. Then

\[
\varphi_H=\nu\circ\chi,
\qquad
\chi:\mathbf P^1_\lambda\to\mathbf P^1_y,
\qquad
\deg\chi=2.
\tag{4.1}
\]

Let \(\iota\) be the nontrivial deck involution of \(\chi\). The
field has odd characteristic, so the degree-two map is separable.

For every source line \(\mathscr L_j\), let
\(\Delta_j=\nu^*\mathscr L_j\), an effective divisor of degree two
on the \(y\)-line. Then

\[
\boxed{D_j=\chi^*\Delta_j.}
\tag{4.2}
\]

Consequently every \(D_j\) is \(\iota\)-invariant.

For a pole point \(\lambda\), define its row signature

\[
\operatorname{sig}(\lambda)
=\{j:\lambda\in D_j\},
\tag{4.3}
\]

with local multiplicity retained when necessary. Equation (4.2)
implies

\[
\operatorname{sig}(\iota\lambda)
=\operatorname{sig}(\lambda).
\tag{4.4}
\]

Equation (2.2) then shows that \(\iota\) preserves
\(D_{\mathcal K}\) and \(E_H\) separately: common points have
signature size two, while free points have signature size one.

## 5. Reduced common-pole classification

Assume first that \(D_{\mathcal K}\) is reduced. At a common point,
the two source lines through its star vertex meet the smooth conic
transversely. Otherwise their total pullback multiplicity would
exceed the coefficient two in (2.2). In particular, \(\chi\) is
unramified there.

Thus the ten common points form five two-element \(\iota\)-orbits.
The two points in one orbit have the same two-label signature and
map to the same star vertex.

The five signatures are distinct. If two different
\(\iota\)-orbits had the same signature \(\{j,k\}\), both would map
to the unique vertex
\(\mathscr L_j\cap\mathscr L_k\), contradicting that a fiber of
\(\chi\) has degree two.

At a free point, (2.2) also has coefficient one. Therefore \(\chi\)
is unramified and the conic meets the corresponding source line
transversely. Its \(\iota\)-mate is another free point with the same
one-label signature.

Each row has only its two actual free roots. Hence:

\[
\boxed{
e_j:=|D_j\cap E_H|\in\{0,2\},\qquad
\#\{j:e_j=2\}=2.}
\tag{5.1}
\]

Let \(G_\chi\) be the simple graph on the six source rows whose
edges are the five distinct common signatures. Each edge occurs
twice upstairs. Since \(\deg D_j=4\),

\[
2\deg_{G_\chi}(j)+e_j=4.
\tag{5.2}
\]

Thus two vertices have degree one and four have degree two. The two
degree-one vertices are exactly the rows owning both free edges.
The graph is a disjoint union of one path and zero or more cycles.
There are only three unlabeled possibilities:

\[
\boxed{
P_6,\qquad P_3\sqcup C_3,\qquad P_2\sqcup C_4.}
\tag{5.3}
\]

Their labeled counts in the reduced common-signature universe are
respectively

\[
\boxed{360,\qquad60,\qquad45,}
\tag{5.4}
\]

for \(465\) labeled common-signature graphs in total. These are
labeled configurations before quotienting by a pole-graph symmetry.

The exact coefficient-plane calculation in

```text
proof/q6_u2_star_conic_geometry_reduction.md
```

excludes all \(60\) labeled \(P_3\sqcup C_3\) graphs in this reduced
universe. Its two
endpoint source lines have the same second conic intersection, so
their two disjoint degree-two free divisors would be the same fiber
of \(\chi\). Hence the geometric survivor list is

\[
\boxed{P_6,\qquad P_2\sqcup C_4,}
\tag{5.5}
\]

with \(405\) labeled graphs before pole-cycle routing.

## 6. The conic quotient is not the deck quotient

Let \(j\) be one of the two degree-one vertices in (5.2). Its two
free roots are precisely the two points of \(bZ_j\), lying over two
different values of the deck quotient \(\psi\).

The deck involution \(b\) sends each point of \(bZ_j\) to the
corresponding point of \(Z_j\), not to the other point of \(bZ_j\).
But \(\iota\) swaps the two free roots of row \(j\). Therefore

\[
\boxed{\iota\ne b.}
\tag{6.1}
\]

Equivalently, \(\chi\) is not a
\(\operatorname{PGL}_2\)-reparameterization of \(\psi\).
The direct quotient-identification adapter is therefore cut; the
surviving structure is genuinely a second degree-two quotient.

## 7. Ramified deck fibers over \(\mathcal K\)

Suppose \(\lambda_*\) is a deck branch point lying over
\(\mathcal K\). Its coefficient in \(D_{\mathcal K}\) is two, so
the right side of (2.2) has local multiplicity four.

The point \(\varphi_H(\lambda_*)\) is a star vertex on two distinct
source lines. A smooth conic has one tangent line at that point, so
the sum of its local intersection multiplicities with those two
lines is at most three. Therefore an unramified \(\chi\) cannot
produce multiplicity four. It follows that \(\chi\) is ramified at
\(\lambda_*\); exact equality then forces both source lines to be
transverse to the conic.

Hence every deck branch point over \(\mathcal K\) is also a branch
point of \(\chi\). If both deck branch points lie over
\(\mathcal K\), then \(b\) and \(\iota\) have the same two fixed
points. In odd characteristic a nontrivial projective involution is
uniquely determined by its two fixed points. Thus
\(\iota=b\), contradicting (6.1).

Therefore:

\[
\boxed{
\text{The conic branch is empty when both deck branch points lie
over \(\mathcal K\).}}
\tag{7.1}
\]

The companion free-pair reduction subsequently excludes the case
with exactly one deck branch point over \(\mathcal K\). Thus only
the reduced zero-branch-point case remains.

## 8. Exact second-involution target

The two free-root pairs at the path endpoints already determine at
most one projective involution \(\iota\). In the pair-matrix
formulation below, their two distinct rows have rank two, so their
kernel is one-dimensional. The stronger construction and the common
binary-decic invariance gate are proved in:

```text
proof/q6_u2_conic_free_pair_involution_reduction.md
```

The five common pairs are therefore tests on one fixed candidate,
not additional seed choices.

That companion note also proves that the one-deck-branch-point case
is impossible: the two distinct involutions would share one fixed
point and their product would be a nontrivial translation of order
the KoalaBear characteristic, which cannot preserve the other eight
common points. In the reduced case, any surviving second involution
is either a reciprocal normalizer or generates with the deck
involution a tame cyclic quotient of order \(4\) or \(5\).

There is an equivalent determinant formulation that is better
suited to the endpoint compiler. In an affine pole coordinate, write
a trace-zero representative of a projective involution as

\[
M=
\begin{pmatrix}
a&b\\
c&-a
\end{pmatrix},
\qquad
a^2+bc\ne0.
\tag{8.1}
\]

It exchanges finite points \(x,y\) exactly when

\[
\boxed{cxy-a(x+y)-b=0.}
\tag{8.2}
\]

For the five common pairs and two free pairs, form the seven rows

\[
\boxed{
\bigl(x_iy_i,\;-(x_i+y_i),\;-1\bigr).}
\tag{8.3}
\]

All seven pairs are fibers of one separable degree-two quotient if
and only if this \(7\times3\) matrix has rank at most two and its
kernel contains a vector \((c,a,b)\) with
\(a^2+bc\ne0\). The homogeneous version uses the same trace-zero
matrix and works when one point is infinite.

The seven-row rank criterion remains an exact final check. The
stronger preliminary target is to test common-decic invariance for
the candidate determined by the first two free rows.

Thus the conic branch is reduced to:

> **Second-involution matching lemma.** For each of the \(405\)
> geometrically surviving labeled graphs in (5.5), form the candidate projective
> involution swapping the two actual free-root pairs. The five
> common pairs cannot all be exchanged by that involution, unless
> the same source-labelled equations emit an
> existing endpoint minor or a valid same-record quotient cell.

This is a symbolic finite matching problem on the actual pole
points. A convenient numerical normalization is evidence only.
Every failure is witnessed by one printed \(3\times3\) minor.

After cycle-union routing and the star-conic exclusion, the
incidence-preserving automorphism group of each declared pole graph
gives the separate orbit census:

\[
\boxed{
\begin{array}{c|r|r|r}
\text{pole cycles}&\text{pre-geometry open orbits}&
\text{open labeled cases}&\text{open orbits}\\ \hline
6&52&405&46\\
4+2&37&378&30\\
3+3&13&405&10\\
2+2+2&12&324&10
\end{array}}
\tag{8.4}
\]

The \(405\) in (5.5) is the total labeled survivor count before a
pole-cycle type is fixed. The values \(46,30,10,10\) in the last
column of (8.4) are orbit counts in four different pole-cycle
universes under their respective incidence-preserving automorphism
groups. They neither sum to \(405\) nor partition one common labeled
set.

The exact classifier is:

```text
experiments/classify_q6_u2_conic_graph_orbits.py
```

Thus the largest reduced conic elimination has \(46\), not \(465\),
second-involution graph representatives. The classifier regenerates
the actual free pole edges, common-signature edges, and orbit size of
every open canonical representative. The committed compact
certificate binds those full lists by ordered representative
digests, digest chains, scalar ledgers, and complete-row hashes.

Before that graph test, the free-pair quotient leaves only
\(3,3,2,1\) open endpoint-row orbits for pole-cycle types
\(6,4+2,3+3,2+2+2\), respectively. Each endpoint orbit has one
canonical candidate involution and one common-decic invariance gate.

No ramified common-pole conic case remains: the one-branch-point case
is excluded by the translation argument, and the two-branch-point
case by equality of the involutions.

## 9. Updated branch boundary

\[
\boxed{
\begin{array}{c|c}
\text{image type}&\text{status}\\ \hline
\text{line}&\text{excluded}\\
\text{conic, two deck branch points in }\mathcal K&\text{excluded}\\
\text{conic, one deck branch point in }\mathcal K&\text{excluded}\\
\text{conic, reduced }D_{\mathcal K}&
\text{reciprocal or cyclic order }4,5\\
\text{birational quartic}&
\text{separate star-quartic elimination}
\end{array}}
\]

No conclusion here proves the \(u=3\) component theorem.
