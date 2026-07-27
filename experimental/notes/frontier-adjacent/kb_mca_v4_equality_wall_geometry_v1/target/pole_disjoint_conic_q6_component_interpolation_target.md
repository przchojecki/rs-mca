# Low-Degree Component Interpolation on the \(Q=6,s=6\) Source-Facet Deck

## 1. Status and role

This is the next algebraic target inside the pole-disjoint
irreducible-conic endpoint. It is not a booked owner payment and it
does not assume the endpoint classification.

The proved input is the exact \(Q=6,s=6\) rectangular-grid packet,
the fixed-source split-pencil star, the canonical source-facet deck,
and the component edge-coloring ledger in Corollaries 9.21 and
9.24--9.28 of

```text
proof/pole_disjoint_conic_facet_collinearity_reduction.md
```

The new point is that the remaining component/pole-cycle
compatibility question has a low-degree interpolation core. Every
nontrivial outgoing component partition

\[
4+2,\qquad 3+3,\qquad 2+2+2
\]

contains a component of first degree \(u=2\) or \(u=3\). The
single-component partition \(6\) is already monochromatic. It is
therefore enough to control degree-\(2\) and degree-\(3\) component
sections.

## 2. Exact endpoint data

Let

\[
\mathcal I,\mathcal L\subseteq\{1,\ldots,12\},
\qquad
|\mathcal I|=|\mathcal L|=6,
\]

and let

\[
\mathcal K\subseteq\mathcal I\cap\mathcal L,
\qquad |\mathcal K|=5.
\]

Write

\[
\eta\in\mathcal L\setminus\mathcal K
\]

for the remaining source label. The proved deck supplies:

1. a canonical bijection
   \[
   \tau:\mathcal I\longrightarrow\mathcal L^c;
   \]
2. a diagonal-free two-regular bipartite pole graph between
   \(\mathcal I^c\) and \(\mathcal L^c\);
3. an outgoing divisor \(O_j\) of degree \(12\) on every coordinate
   line \(T=\alpha_j\);
4. the exact noninvariant formula
   \[
   O_j=\psi^*\mathcal K+bZ_j
   \qquad(j\in\mathcal I^c);
   \]
5. the invariant formula
   \[
   O_x=\psi^*
   \left(
   \{\alpha_1,\ldots,\alpha_{12}\}
   \setminus
   \bigl(\mathcal K\cup\{\alpha_{\tau(x)}\}\bigr)
   \right)
   \qquad(x\in\mathcal I).
   \]

The pullback divisors over \(\mathcal K\) and \(\eta\) have degrees
\(10\) and \(2\), respectively, and may contain ramified deck-fixed
points. Over every \(\ell\in\mathcal L^c\), however, the two pole
points are distinct and free. If their pole-graph neighbors are
\(j,j'\in\mathcal I^c\), and
\(x_\ell=\tau^{-1}(\ell)\), the two horizontal fibers have source
root sets

\[
\mathcal I\setminus\{x_\ell\}\cup\{j'\},
\qquad
\mathcal I\setminus\{x_\ell\}\cup\{j\}.
\tag{2.1}
\]

Thus the free part of the deck is six exact one-exchange pairs of
six-element facets with a canonical common five-set.

## 3. Component split-locator sections

Factor the graph-free outgoing union over an algebraic closure:

\[
F_{\rm out}=\prod_{\rho=1}^m H_\rho,
\qquad
\operatorname{bideg}H_\rho=(u_\rho,2u_\rho),
\qquad
\sum_\rho u_\rho=6.
\tag{3.1}
\]

Fix one component \(H=H_\rho\) of first degree \(u\). For each
coordinate label \(j\), define the homogeneous binary form

\[
q_j(\lambda_0,\lambda_1)
=
H(\alpha_j,\lambda_0,\lambda_1).
\tag{3.2}
\]

The no-vertical-component theorem and the bidegree law imply

\[
\deg q_j=2u.
\tag{3.3}
\]

Let \(D_j=\operatorname{div}(q_j)\). Then

\[
D_j\le O_j,\qquad \deg D_j=2u,
\tag{3.4}
\]

and for the full component family the \(D_j\)'s partition \(O_j\)
with local multiplicity.

Write

\[
H(T,\lambda_0,\lambda_1)
=
\sum_{h=0}^{2u} c_h(T)
\lambda_0^{2u-h}\lambda_1^h.
\tag{3.5}
\]

Every coefficient polynomial satisfies

\[
\deg c_h\le u.
\tag{3.6}
\]

Consequently, for each \(h\), the twelve-vector

\[
\bigl(c_h(\alpha_1),\ldots,c_h(\alpha_{12})\bigr)
\tag{3.7}
\]

lies in the length-twelve Reed--Solomon evaluation space of
dimension \(u+1\). Equivalently, every \(u+2\) coordinate labels
satisfy the exact divided-difference relation

\[
\sum_{r=0}^{u+1}
\frac{c_h(\alpha_{j_r})}
{\prod_{v\ne r}(\alpha_{j_r}-\alpha_{j_v})}
=0.
\tag{3.8}
\]

Equations (3.3)--(3.8) are the interpolation constraint absent from
the purely combinatorial edge-color fixture.

## 4. Edge ownership and the correction

For a pole-graph edge \(e=(j,\ell)\), let \(z_e\) be the root of
\(Z_j\) above \(\alpha_\ell\). The edge belongs to \(H_\rho\) when

\[
H_\rho(\alpha_j,bz_e)=0.
\tag{4.1}
\]

A component of first degree \(u\) owns exactly \(2u\) pole-graph
edges. At each right vertex \(\ell\), the two component partitions
of the common five-set in (2.1) give the transport matrix

\[
n_{\rho\sigma}(\ell).
\]

Its row and column margins are

\[
\sum_\sigma n_{\rho\sigma}
=u_\rho-\mathbf 1_{\rho=c_-},
\qquad
\sum_\rho n_{\rho\sigma}
=u_\sigma-\mathbf 1_{\sigma=c_+}.
\tag{4.2}
\]

Define

\[
\mu_\ell=\sum_{\rho\ne\sigma}n_{\rho\sigma}(\ell),
\tag{4.3}
\]

and let \(\delta_j\) be one when the two pole-graph edges incident
to \(j\in\mathcal I^c\) have different component colors. A color
change at a right vertex forces \(\mu_\ell\ge1\).

The focused verifier contains a valid \(4+2\) transport fixture with

\[
\sum_\ell\mu_\ell=4,
\qquad
\sum_j\delta_j=4.
\tag{4.4}
\]

It satisfies all cardinalities and margins, but it is not claimed
to come from forms satisfying (3.5)--(3.8). Therefore the
interpolation equations are load-bearing.

### 4.1 The proved \(u=2\) star-configuration reduction

For \(u=2\), the actual component has two coefficient maps described
in

```text
proof/q6_u2_plane_map_reduction.md
```

The pole-parameter map

\[
\varphi_H:\mathbf P^1_\lambda\longrightarrow\mathbf P^2
\]

has total degree four. The six noninvariant source evaluations define
six lines \(\mathscr L_j\) in \(\mathbf P^2\), with no three
concurrent, and their fifteen pairwise intersections are exactly the
split quadratics with two roots among the six source labels. If
\(E_H\) is the reduced divisor of the four pole edges owned by the
component, then the exact effective-divisor identity is

\[
\boxed{
\varphi_H^*
\left(\sum_{j\in\mathcal I^c}\mathscr L_j\right)
=2\psi^*\mathcal K+E_H.}
\tag{4.5}
\]

This includes ramification multiplicity over \(\mathcal K\). The
image map has exactly one of the degree types

\[
(r,d)=(1,4),\qquad(2,2),\qquad(4,1).
\tag{4.6}
\]

The source-coordinate coefficient map has total degree two. If two
distinct source rows carry proportional component quartics, its image
must be a line, and all six row quartics span a space of dimension at
most two. More generally, the line-image branch has the exact
fiber-product form

\[
H(T,\lambda)=a(T)P(\lambda)+b(T)Q(\lambda),
\]

with a degree-two source map and a degree-four pole map. Thus repeated
zero-edge fibers form a canonical quotient-precursor branch, rather
than an omitted exception to rank-three interpolation. Same-record
owner payment for that quotient remains a separate interface.

The conic-image case is also reduced: the coefficient map factors
through a canonical degree-two pole quotient
\(\chi:\mathbf P^1_\lambda\to\mathbf P^1\), and \(H\) is the pullback
of a bidegree-\((2,2)\) correspondence. Consequently only the
birational rational-quartic image remains as a genuinely
non-quotient \(u=2\) interpolation case.

The actual divisor ledger sharpens both quotient branches in:

```text
proof/q6_u2_line_conic_quotient_reduction.md
```

The line image is impossible. In the reduced conic branch, the ten
common points form five equal-signature involution orbits, the four
free points are the complete free-root pairs of two rows, and the
common-signature graph is initially one of

\[
P_6,\qquad P_3\sqcup C_3,\qquad P_2\sqcup C_4.
\]

Exact star-conic geometry excludes \(P_3\sqcup C_3\): its two
endpoint source lines have the same second conic intersection, which
would identify the two disjoint degree-two free fibers. Thus only
\(P_6\) and \(P_2\sqcup C_4\) survive, with \(405\) labeled cases.
After cycle-union routing, quotienting by the
bipartition-preserving automorphism group of the actual pole graph
leaves respectively \(46,30,10,10\) conic cases for pole-cycle types
\(6,4+2,3+3,2+2+2\). Each representative has an
exact \(7\times3\) pair-matrix test for its candidate involution.
The conic involution differs from the deployed deck involution, and
the conic branch is impossible if both deck branch points lie over
\(\mathcal K\).

The two free-root pairs alone determine the candidate involution.
Testing its nondegeneracy and invariance of the common binary decic
reduces the preliminary endpoint-row quotient to only
\(3,3,2,1\) open orbits for the same four pole types. The larger
signature-graph quotient is consumed only by candidates surviving
that decic gate. This stronger reduction is proved in
`proof/q6_u2_conic_free_pair_involution_reduction.md`.

The same note excludes the case with exactly one deck branch point
over \(\mathcal K\), so all ramified common-pole conic cases are
closed. In the reduced branch, a surviving second involution is
either a reciprocal normalizer or generates a tame cyclic quotient
of exact order \(4\) or \(5\). The reciprocal branch has only
\(2,2,1,1\) open endpoint-row orbits after its right-neighbor
compatibility gate.

Every surviving case emits a canonical component-rooted source-label
quotient of degree \(2,4,\) or \(5\), maps \(\mathcal K\) to at
most three values, and collapses both actual endpoint-row neighbor
pairs. This is not the active pair-global domain-to-slope owner. The
remaining conic wall is the exact elimination-or-owner adapter in
`q6_u2_conic_source_quotient_adapter_target.md`.

In the unramified distinct-vertex quartic branch, the complement of
the ten selected star edges has five edges. There are exactly
\(1{,}455\) admissible complement graphs and \(11{,}130\)
graph/free-edge cases: \(8{,}730\) connected trees and \(2{,}400\)
disconnected cyclic cases. Tree restrictions determine one quartic
up to scale after five explicit node equations; disconnected cases
carry explicit cycle-product gates. If repeated normalization
preimages occur over star vertices, their total excess is at most
three by the \(\delta\)-invariant budget of a rational plane
quartic. The exact pole-graph symmetry quotient reduces the four
cycle types to \(985,490,188,79\) simple-vertex representatives, of
which \(985,488,188,77\) remain after the cycle-union cases are
removed. Ramification in \(\psi^*\mathcal K\) remains a separate
local-intersection case.

## 5. Target lemma

### Low-degree component cycle-union lemma

Let \(H\) be an actual outgoing component satisfying Sections 2--4
with

\[
u\in\{2,3\}.
\]

Then its \(2u\) owned pole-graph edges form a union of complete
pole-graph cycles.

Equivalently, the component has no boundary in the pole graph:

\[
\delta_j(H)=0
\quad(j\in\mathcal I^c),
\qquad
\mu_\ell(H,\cdot)=\mu_\ell(\cdot,H)=0
\quad(\ell\in\mathcal L^c),
\tag{5.1}
\]

unless the same equations emit one of the already sufficient
endpoint contradictions:

1. three actual reciprocal block rows have rank at most two;
2. three actual block locators lie in one twelve-set;
3. three actual block locators lie in one thirteen-set with
   dependent complementary quadratics;
4. a printed minor contradicts the exact rank-three source matrix.

The conclusion must use the actual component form \(H\), its split
divisors \(D_j\), and the selected endpoint rows. An abstract
edge-color contradiction is insufficient.

## 6. Immediate consequence

The target lemma proves the exact component/pole compatibility:

\[
\sum_{\ell\in\mathcal L^c}\mu_\ell
+
\sum_{j\in\mathcal I^c}\delta_j
=0,
\tag{6.1}
\]

or directly closes the endpoint by one of the alternatives in
Section 5.

Indeed:

* for partition \(4+2\), apply the lemma to the degree-two
  component;
* for partition \(3+3\), apply it to either degree-three component;
* for partition \(2+2+2\), apply it to every degree-two component;
* for partition \(6\), the edge coloring has one color already.

When (6.1) holds, every pole cycle is monochromatic and the outgoing
component partition coarsens the pole-cycle half-length partition.
The possible compatible pairs are:

\[
\begin{array}{c|c}
\text{component partition}&\text{pole-cycle partition}\\ \hline
6&6,\ 4+2,\ 3+3,\ 2+2+2\\
4+2&4+2,\ 2+2+2\\
3+3&3+3\\
2+2+2&2+2+2.
\end{array}
\tag{6.2}
\]

This does not by itself exclude the single-component case. It turns
the current correction problem into four finite compatible
normal-form families for the next endpoint argument.

## 7. Promising proof strategies

### 7.1 GRS parity checks

For \(u=2\), each coefficient vector in (3.7) lies in
\(\operatorname{RS}_3(\alpha_1,\ldots,\alpha_{12})\); for \(u=3\),
it lies in \(\operatorname{RS}_4\). Apply the dual parity checks to
the coefficient vectors after substituting the prescribed split
divisors from (2.1). A non-cycle edge set should force too many
independent zero/equality conditions on a space of dimension three
or four.

The calculation must retain all \(2u+1\) binary-form coefficients
simultaneously. Treating them independently loses the common split
divisor.

### 7.2 Resultants of neighboring coordinate fibers

At a left or right color transition, compare the two binary forms
whose divisors differ on one prescribed pole while sharing selected
source-facet roots. Their resultant or first subresultant should
acquire a source-labelled factor. For \(u=2,3\), its degree is small
enough to enumerate the possible factor allocations exactly.

A useful output is a three-row minor of the reciprocal block matrix,
not merely a repeated factor in an unselected component.

### 7.3 Small-\(u\) symbolic normal forms

Normalize three coordinate labels projectively and write the
degree-\(u\) coefficient polynomials \(c_h(T)\) explicitly. Impose:

* the split divisors \(D_j\le O_j\);
* the six one-exchange facet pairs;
* the proposed non-cycle edge-color pattern;
* squarefreeness at the twelve free pole points.

Eliminate component coefficients before source coordinates. The
finite output should be a list of source-labelled factors or minors,
with exact finite-field verification over the deployed field.

### 7.4 Discriminant and branch divisor

The map from the component normalization to the \(T\)-line has
degree \(2u\), while its projection to the pole parameter has degree
\(u\). A color transition prescribes incompatible monodromy on one
exchange pair. For \(u=2,3\), Riemann--Hurwitz and the deck
involution may force an additional branch point on the forbidden
source grid.

Any such argument must allow ramification above \(\mathcal K\) and
\(\eta\); only the twelve exchange points are known to be free.

### 7.5 Reciprocal-row interpolation

Insert the exact component divisors into the reciprocal-coordinate
identity before eliminating the component. Since the twelve block
rows span exactly three dimensions, a nonzero correction may force
three selected rows to share a two-dimensional coefficient space.
This route has the advantage that its output is already the
sufficient rank-two triple.

### 7.6 Star-configuration image-degree split

Use (4.5)--(4.6) before performing a full coefficient elimination.
There are only three cases.

* If the image is a line, apply the proved free-incidence
  contradiction; this branch is empty.
* If the image is a conic, the exact degree-two pole quotient is
  already proved and is distinct from the deck quotient. Solve the
  unique-candidate/common-decic problem on at most three open
  endpoint-row orbits for any pole graph. Apply the larger
  source-signature pair-matrix quotient only to surviving candidates.
  The ramified cases are excluded; classify only the reciprocal
  normalizer and cyclic orders \(4,5\).
* If the image is a rational quartic, combine the Hilbert function of
  the six-line star configuration with the singularity budget of a
  rational plane quartic. In the simple-vertex branch, enumerate the
  exact pole-graph orbit representatives, at most \(985\) open cases
  for any pole graph, apply the cycle gates, and reject reducible or
  positive-genus interpolants. Handle the at-most-three
  duplicate-preimage units and ramified common-pole fibers by local
  intersection type.

The line and conic cases are lower-dimensional and should be
classified before attempting the quartic eliminant. The exact
pullback divisor, rather than only the ten vertex incidences, must be
preserved.

## 8. Guardrails

The following do not prove the target:

* the component degree partition alone;
* the pole-cycle partition alone;
* the edge-color multiplicities \(2u\);
* the transport margins (4.2);
* treating the degree-ten and degree-two exceptional pullbacks as
  ten and two distinct points;
* testing only one convenient numerical normalization of the twelve
  source and pole labels;
* a rank defect on component coefficients not connected to three
  actual reciprocal block rows;
* a repeated split sextic without a same-record or direct endpoint
  contradiction.

The verifier's nonmonochromatic \(4+2\) fixture is a mandatory
regression for the first four guardrails.

## 9. Valid proof certificate

A compiler-grade proof should print:

1. the component degree \(u\in\{2,3\}\);
2. all coefficient forms \(c_h(T)\) or their exact normalized
   eliminant;
3. the twelve divisors \(D_j\) and their containment in \(O_j\);
4. the six exchange pairs and the component-owned pole edges;
5. the exact GRS parity checks, resultants, or minors used;
6. either the cycle-union conclusion or one selected endpoint
   contradiction from Section 5;
7. a tamper test changing one exchange root while preserving the
   combinatorial margins, which the algebraic validator rejects.

## 10. Valid falsifier

A falsifier must be an actual bidegree-\((u,2u)\) form over the
deployed KoalaBear field, for \(u=2\) or \(3\), satisfying
(2.1)--(4.2), with a non-cycle edge set and with:

* all twelve component fibers split inside the prescribed \(O_j\);
* the twelve coefficient columns satisfying (3.5)--(3.8);
* no rank-two triple of actual reciprocal block rows;
* no twelve-set or thirteen-set endpoint contradiction.

A colored pole graph or transportation matrix without the
interpolating component form is not a falsifier.
