# Pole-Disjoint Conic \(Q=6,s=6\) Split-Pencil Target

## 1. Status

This is one of the three surviving invariant-coordinate branches of
the first open deck value.

```text
Q=6, s=2,3,4,5: EXCLUDED
Q=6, s=1 fixed pole: EXCLUDED
Q=6, s=6 NORMAL FORMS: PROVED
Q=6, s=6 EXCLUSION: OPEN
PDCEC: OPEN
OWNER PAYMENT: NONE
```

The proved input is in Corollaries 9.21 and 9.24--9.28 of:

```text
proof/pole_disjoint_conic_facet_collinearity_reduction.md
```

The broader live interface is:

```text
target/pole_disjoint_conic_q6_intersection_target.md
```

## 2. Source and block packet

There are:

* twelve distinct source values \(\alpha_1,\ldots,\alpha_{12}\);
* sixty active roots;
* 120 distinct eleven-root active block locators \(U_\lambda\);
* a fixed-point-free deck pairing
  \(\lambda\leftrightarrow b\lambda\);
* pairwise block intersection
  \[
  |I_\lambda\cap I_{b\lambda}|=5;
  \]
* the exact \(1\)-\((60,11,22)\) block incidence;
* reciprocal block rows
  \[
  \left(
  \frac{\kappa_j}{U_\lambda(\alpha_j)}
  \right)_{j=1}^{12}
  \]
  of rank exactly three.

No source is active, so every locator value at every source is
nonzero.

Let

\[
\mathcal I=\{j:bZ_j=Z_j\}.
\]

This target assumes

\[
|\mathcal I|=6.
\]

The branch is graph-free. Its possible outgoing component partitions
are

\[
\boxed{6,\qquad4+2,\qquad3+3,\qquad2+2+2.}
\tag{2.1}
\]

## 3. Exact quotient grid

Put

\[
\mathcal R=\{1,\ldots,12\}\setminus\mathcal I,
\qquad
P_{\mathcal I}(T)=\prod_{j\in\mathcal I}(T-\alpha_j),
\qquad
P_{\mathcal R}(T)=\prod_{j\in\mathcal R}(T-\alpha_j).
\]

In the deck quotient coordinate \(w\),

\[
H_6(T,w)=P_{\mathcal I}(T)h(w),
\qquad
\deg h=5.
\tag{3.1}
\]

The polynomial \(h\) is squarefree and source-supported:

\[
\operatorname{div}(h)
=
\sum_{k\in\mathcal K}[\alpha_k],
\qquad
|\mathcal K|=5.
\tag{3.2}
\]

The even form has the exact normal form

\[
\boxed{
E_6(T,w)
=
P_{\mathcal R}(T)A(w)
+
h(w)(a_1(T)w+a_0(T)),}
\tag{3.3}
\]

where

\[
\deg_wA<5,
\qquad
\deg_Ta_0,\deg_Ta_1\le6,
\qquad
\gcd(A,h)=1.
\tag{3.4}
\]

The complete quotient resultant is

\[
\boxed{
\operatorname{div}\operatorname{Res}_w(E_6,h)
=
5\sum_{j\in\mathcal R}[\alpha_j].}
\tag{3.5}
\]

There is no residual quotient point. All outgoing/deck-conjugate
intersections lie on the six vertical source lines and five
horizontal source-pole lines in this rectangular packet.

## 4. Sixty fixed-source split secants

For each deck pair, define

\[
G_\lambda=\gcd(U_\lambda,U_{b\lambda}),
\qquad
A_\lambda=U_\lambda/G_\lambda,
\qquad
B_\lambda=U_{b\lambda}/G_\lambda.
\tag{4.1}
\]

Then:

\[
\deg G_\lambda=5,
\qquad
\deg A_\lambda=\deg B_\lambda=6;
\tag{4.2}
\]

\[
\gcd(A_\lambda,B_\lambda)=1;
\tag{4.3}
\]

and all roots of \(G_\lambda,A_\lambda,B_\lambda\) are active.
There is a unique \(c_\lambda\ne0,1\) such that

\[
\boxed{
A_\lambda-c_\lambda B_\lambda
=(1-c_\lambda)P_{\mathcal I}.}
\tag{4.4}
\]

Thus all sixty secants

\[
\langle[A_\lambda],[B_\lambda]\rangle
\subseteq\mathbf P(F[T]_{\le6})
\]

pass through \([P_{\mathcal I}]\).

Equivalently, for every pair the three split sextics

\[
A_\lambda,\qquad B_\lambda,\qquad P_{\mathcal I}
\]

are three fibers of one degree-six rational map. The first two
fibers are disjoint subsets of the active domain; the third is the
actual six-source set.

## 5. Source-label near-coincidence

Each invariant coordinate divisor is a complete source fiber:

\[
Z_j=\psi^*[\alpha_{\sigma(j)}],
\qquad
\sigma(j)\ne j
\qquad(j\in\mathcal I).
\tag{5.1}
\]

The map \(\sigma\) is injective. Put

\[
\mathcal L=\sigma(\mathcal I).
\]

Then

\[
\boxed{
\mathcal K\subseteq\mathcal I\cap\mathcal L,
\qquad
|\mathcal I\cap\mathcal L|\ge5.}
\tag{5.2}
\]

There are only two label configurations:

1. \(\mathcal L=\mathcal I\), and \(\sigma\) is a derangement of the
   six labels;
2. \(\mathcal I\) and \(\mathcal L\) differ by one label.

For \(j\notin\mathcal I\), the two pole roots of \(Z_j\) map to a
two-element source set \(\mathcal C_j\subseteq\mathcal L^c\).
The incidence

\[
j\longmapsto\mathcal C_j
\]

is two-regular on both sides, has no diagonal edge, and is disjoint
from \(\mathcal K\). Its cycle half-length partition is one of

\[
\boxed{6,\qquad4+2,\qquad3+3,\qquad2+2+2,}
\tag{5.3}
\]

the same four partitions as the graph-free outgoing components.

There is also a canonical perfect matching

\[
\tau:\mathcal I\longrightarrow\mathcal L^c.
\tag{5.4}
\]

If \(\eta\) is the unique label in
\(\mathcal L\setminus\mathcal K\), the complete horizontal
source-fiber deck is:

* the degree-ten pullback divisor over \(\mathcal K\), counted with
  local multiplicity, has root set \(\mathcal I^c\);
* the degree-two pullback fiber over \(\eta\), counted with local
  multiplicity, has root set \(\mathcal I\);
* over \(\ell\in\mathcal L^c\), the two fibers are
  \[
  \mathcal I\setminus\{\tau^{-1}(\ell)\}\cup\{j'\},
  \qquad
  \mathcal I\setminus\{\tau^{-1}(\ell)\}\cup\{j\},
  \tag{5.5}
  \]
  where \(j,j'\) are the two pole-graph neighbors of \(\ell\).

Thus the last twelve fibers are six exact one-exchange facet pairs.
They are distinct free pole points. The pullbacks over
\(\mathcal K\) and \(\eta\) may instead contain ramified deck-fixed
points, so their counts above are divisor degrees rather than
distinct-point counts.

If the outgoing components have first degrees \(u_\rho\), color a
pole-graph edge by the component containing its opposite coordinate
root. Color \(\rho\) occurs exactly \(2u_\rho\) times. At each right
vertex \(\ell\), Corollary 9.28 prints a transportation matrix
\(n_{\rho\sigma}(\ell)\) for the five common invariant labels. A
color change forces positive off-diagonal migration

\[
\mu_\ell=\sum_{\rho\ne\sigma}n_{\rho\sigma}(\ell)\ge1.
\tag{5.6}
\]

At a left vertex \(j\), let \(\delta_j\) record whether its two edge
colors differ. If every \(\mu_\ell\) and \(\delta_j\) vanishes, each
pole cycle is carried by one component and the component partition
coarsens the pole-cycle partition.

## 6. Exact paired incidence

The sixty deck pairs partition the 120 blocks. Their common cores and
one-sided differences satisfy

\[
\sum_\lambda |I_\lambda\cap I_{b\lambda}|=60\cdot5=300,
\]

\[
\sum_\lambda
|I_\lambda\mathbin{\triangle}I_{b\lambda}|
=60\cdot12=720.
\]

For an active root \(t\), if \(g_t\) is the number of deck pairs in
whose common core it occurs and \(d_t\) the number of pairs in whose
one-sided difference it occurs, then

\[
\boxed{2g_t+d_t=22.}
\tag{6.1}
\]

Only the averages

\[
\frac1{60}\sum_tg_t=5,
\qquad
\frac1{60}\sum_td_t=12
\]

are automatic.

The cyclic design-only guardrail survives even the stronger uniform
specialization \(g_t=5,d_t=12\): an explicit matching in the
verifier realizes it while retaining no common-12-set triple. Hence
the incidence ledger alone cannot close the branch. The algebraic
conditions (3.1)--(5.2) are load-bearing.

## 7. Target theorem

### Fixed-source split-pencil-star exclusion

No actual pole-disjoint irreducible-conic endpoint packet can satisfy
Sections 2--6.

A sufficient conclusion is any one of:

1. three actual block locators lie in one 12-set;
2. three actual block locators lie in one 13-set with dependent
   complementary quadratics;
3. three actual reciprocal block rows have rank at most two;
4. one of the component partitions in (2.1) violates the exact grid
   (3.1)--(3.5);
5. the split-pencil star (4.4) contradicts the active/source
   separation or paired block incidence.

Any conclusion excludes \(Q=6,s=6\). It does not need to emit an
owner cell, because a direct contradiction is an allowed closure of
the pole-disjoint irreducible-conic endpoint.

## 8. Promising proof routes

### 8.1 Repeated pencil line

A fixed pencil through \(P_{\mathcal I}\) has at most ten
**distinct** full active sextic fibers on the 60-point active domain.
At ten, those fibers partition the active set. Classify repeated
fibers and repeated pencil lines together with their five-root cores
\(G_\lambda\).

Do not infer a five-pair cap: the same sextic may recur in several
deck pairs with different cores. The current unconditional
multiplicity bound is only 22, from block replication.

The repository's moving-root theorem proves exactly the
ten-distinct-fiber count for this one pencil. Its owner-payment
corollary cannot yet be invoked: the packet has no printed injective
map from the deck-pair occurrences to actual first-match owner
slopes, and the five-root cores vary. Any owner route must supply
that missing same-record adapter rather than relabel the pencil
capacity as a payment. A local two-slope pencil cap does not derive a
global chart count, and a payment proved for one fixed union does not
aggregate across unions without an additional census theorem.

### 8.2 Coefficient-space secant geometry

The split sextics form points in \(\mathbf P^6\). Study the
intersection of the split-form locus on the active domain with the
cone of secants through \([P_{\mathcal I}]\). The desired theorem is
not a bound for arbitrary split forms: it must use sixty prescribed
pairs, the 11-block cores, and the rank-three reciprocal evaluation
matrix.

Useful exact equations are obtained by comparing the first six
elementary symmetric functions in (4.4). They express each pair's
active-root moments as affine functions of \(c_\lambda\) and the
fixed source-root moments.

### 8.3 Grid/component compatibility

Factor the outgoing curve according to one partition in (2.1).
Every component/deck-conjugate intersection is supported on the
rectangular source grid. Use local multiplicities to show that one
component must own too many vertical or horizontal fibers. Aggregate
Bézout alone is insufficient; the proof should retain which five
horizontal source poles form \(\mathcal K\).

### 8.4 Near-coincident label classification

Handle separately:

```text
L = I
|L intersect I| = 5
```

In the first case, classify the derangement \(\sigma\) and the
diagonal-free two-regular graph on the complementary labels. In the
second, track the unique entering and leaving labels through (3.3)
and (4.4). The finite graph types are small; the hard part is lifting
their labels back to the reciprocal block rows.

The pole graph and the outgoing component packet have the same four
possible partitions. A particularly sharp subtarget is:

> Prove
> \[
> \sum_{\ell\in\mathcal L^c}\mu_\ell
> +
> \sum_{j\in\mathcal I^c}\delta_j
> =0,
> \]
> or use a positive correction term to emit a selected rank-two
> triple or another endpoint contradiction.

The correction is now exact: \(\mu_\ell\) counts off-diagonal
component migration of the five common roots in (5.5), while
\(\delta_j\) records splitting of the opposite coordinate quadratic
between two components. Vanishing turns the finite graph
classification into a coarsening theorem for the component
classification.

The finite guardrail in Corollary 9.28 allows a nonzero correction
for a `4+2` component partition on a single twelve-edge cycle.
Therefore cardinalities and transportation margins alone do not
prove vanishing; the bidegree interpolation or reciprocal rows must
enter.

The resulting degree-two/degree-three interpolation problem is
stated separately in

```text
target/pole_disjoint_conic_q6_component_interpolation_target.md
```

Every nontrivial component partition contains such a low-degree
component; the single degree-six component is already monochromatic.

### 8.5 Function-field \(abc\) or fiber-product route

Each relation (4.4) is a polynomial \(S\)-unit equation with three
squarefree degree-six fibers. A single equation is permitted by the
usual polynomial \(abc\) bound. A useful argument must exploit the
simultaneous family of sixty equations sharing the same source
fiber and the paired block design.

### 8.6 Exact finite algebra

Choose seven coefficient coordinates for monic sextics and encode
(4.4) as bilinear equations in the pair roots and \(c_\lambda\).
Eliminate \(c_\lambda\) first. A proof certificate could be:

* a symbolic rank identity;
* a source-labelled resultant factor;
* a finite list of graph/component normal forms, each contradicted
  by a printed minor.

A floating search or a generic-dimension count is not a proof.

## 9. Guardrails

The following are insufficient:

* the \(1\)-design axioms alone;
* the exact \(Q=6\) perfect pairing alone;
* one isolated split-pencil identity;
* an arbitrary secant-star classification without actual active and
  source roots;
* the source-facet cardinalities without the bidegree interpolation
  constraints;
* a rank defect on records other than the selected block pair;
* an owner certificate without same-record payment.

The cyclic guardrail proves the first two cuts. The canonical
block-line theorem shows why one isolated identity is a genuine
planted precursor, but it does not compare sixty different pencil
lines through the same source locator. The one-pencil moving-root
theorem gives the ten-distinct-fiber cap, but not the missing
deck-pair-to-owner projection.

## 10. Valid falsifier

A falsifier must realize, over the deployed KoalaBear field:

* the exact source and active domains;
* 120 distinct eleven-root blocks with replication 22;
* the fixed-point-free \(Q=6\) deck pairing;
* reciprocal evaluation rank exactly three;
* all sixty identities (4.4);
* the quotient grid (3.1)--(3.5);
* one graph-free component partition from (2.1);
* the label constraints (5.1)--(5.2);
* no rank-two selected triple and no contradiction to the endpoint
  identity.

An abstract split-pencil star or paired block design is not a valid
falsifier.
