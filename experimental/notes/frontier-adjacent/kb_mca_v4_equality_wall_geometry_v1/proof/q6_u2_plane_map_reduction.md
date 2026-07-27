# The \(u=2\) Coefficient-Map and Star-Configuration Reduction

## 1. Status

This note proves a further reduction inside the open
\(Q=6,s=6\) low-degree component interpolation target. It does not
prove the component cycle-union lemma and books no owner payment.

The input is Corollaries 9.27--9.28 of

```text
proof/pole_disjoint_conic_facet_collinearity_reduction.md
```

and an actual irreducible outgoing component

\[
H(T,\lambda_0,\lambda_1)
\]

of bidegree \((2,4)\).

The reduction has two complementary parts:

1. the \(\lambda\)-coefficient map realizes the ten common-pole
   incidences as vertices of a six-line star configuration in
   \(\mathbf P^2\);
2. the \(T\)-coefficient map proves that the only case omitted by a
   two-distinct-zero-edge-fiber rank-three search is automatically a
   rank-two case.

Both statements use the actual component form. They are not
consequences of the pole-edge coloring alone.

## 2. The coefficient map in the pole parameter

Write

\[
H(T,\lambda)
=
A(\lambda)T^2+B(\lambda)T+C(\lambda),
\tag{2.1}
\]

in one affine \(T\)-chart. Homogeneously, \(A,B,C\) are binary
quartics in \(\lambda\).

They have no common projective zero. Indeed, a common zero
\(\lambda_*\) would make

\[
H(T,\lambda_*)\equiv0
\]

as a polynomial in \(T\), so the horizontal line
\(\lambda=\lambda_*\) would divide \(H\). This contradicts the
irreducibility and bidegree \((2,4)\) of \(H\).

Consequently the coefficient triple defines a morphism

\[
\varphi_H:\mathbf P^1_\lambda\longrightarrow\mathbf P^2,
\qquad
\lambda\longmapsto[A(\lambda):B(\lambda):C(\lambda)],
\tag{2.2}
\]

with

\[
\varphi_H^*\mathcal O_{\mathbf P^2}(1)
\simeq\mathcal O_{\mathbf P^1}(4).
\tag{2.3}
\]

For the six noninvariant source labels
\(j\in\mathcal I^c\), let

\[
\mathscr L_j
=
\{[A:B:C]:A\alpha_j^2+B\alpha_j+C=0\}
\subset\mathbf P^2.
\tag{2.4}
\]

These are six distinct lines. No three are concurrent: a nonzero
quadratic cannot vanish at three distinct \(\alpha_j\)'s. Moreover,

\[
\mathscr L_j\cap\mathscr L_k
=
\bigl[(T-\alpha_j)(T-\alpha_k)\bigr].
\tag{2.5}
\]

Thus the fifteen pairwise intersections of the
\(\mathscr L_j\)'s are exactly the projective split quadratics with
two roots among the six noninvariant source labels.

For

\[
q_j(\lambda)=H(\alpha_j,\lambda),
\]

one has the exact equivalence

\[
q_j(\lambda)=0
\quad\Longleftrightarrow\quad
\varphi_H(\lambda)\in\mathscr L_j.
\tag{2.6}
\]

## 3. Exact pullback divisor

Let

\[
D_{\mathcal K}=\psi^*\mathcal K.
\]

It is an effective divisor of degree ten. Its support need not have
ten distinct points: ramified deck-fixed fibers are allowed.

Let \(E_H\) be the reduced divisor of the four pole-graph edges
owned by \(H\). Corollary 9.28 gives

\[
\deg E_H=4.
\tag{3.1}
\]

Then

\[
\boxed{
\varphi_H^*
\left(\sum_{j\in\mathcal I^c}\mathscr L_j\right)
=
2D_{\mathcal K}+E_H.}
\tag{3.2}
\]

To prove (3.2), sum the six divisors
\(\operatorname{div}(q_j)\). At every point of
\(D_{\mathcal K}\), counted with its local pullback multiplicity,
the horizontal fiber of the degree-two component \(H\) contains
exactly two of the six noninvariant source labels. This contributes
\(2D_{\mathcal K}\). At a free pole point over
\(\mathcal L^c\), the source-facet formula (9.105) contains exactly
one noninvariant source label. Such a point contributes precisely
when its pole edge is owned by \(H\), and all four such roots are
simple. Corollary 9.28 shows that there are four of them. There are
no other roots because each of the six \(q_j\)'s has degree four:

\[
6\cdot4=2\cdot10+4.
\]

This proves the equality of effective divisors.

In the unramified finite regression, (3.2) says more concretely:

* each of the ten common pole points occurs in exactly two of the
  six split quartics;
* exactly four of the twelve free edge poles occur;
* each row contains four roots in total.

The first bullet is compulsory. Merely requiring that no common
pole occur in all six rows is too weak.

## 4. Degree trichotomy

Let \(C_H\) be the image curve of \(\varphi_H\), let
\(d=\deg C_H\), and let \(r\) be the generic degree of
\(\mathbf P^1_\lambda\to C_H\).

The image is not a point. Otherwise
\(H(T,\lambda)\) would be a product of a quadratic in \(T\) and a
quartic in \(\lambda\), contradicting irreducibility.

Equation (2.3) gives

\[
rd=4.
\]

Hence exactly one of the following occurs:

\[
\boxed{
(r,d)=(1,4),\qquad(2,2),\qquad(4,1).}
\tag{4.1}
\]

The remaining \(u=2\) theorem can therefore be split into three
geometric cases:

1. a birational rational quartic through the required
   star-configuration vertices;
2. a double cover of a conic;
3. a fourfold cover of a line.

In every case, (3.2) is the full pullback of the six-line
arrangement. The four free edge points are the only intersections
not lying above \(\mathcal K\).

## 5. The coefficient map in the source coordinate

Write instead

\[
H(T,\lambda)
=
\sum_{h=0}^4 c_h(T)
\lambda_0^{4-h}\lambda_1^h,
\qquad
\deg c_h\le2.
\tag{5.1}
\]

No projective \(T\)-value is a common zero of all five \(c_h\)'s,
because that would give a vertical component of \(H\). Thus

\[
\theta_H:\mathbf P^1_T\longrightarrow\mathbf P^4,
\qquad
T\longmapsto[c_0(T):\cdots:c_4(T)]
\tag{5.2}
\]

is a basepoint-free morphism with

\[
\theta_H^*\mathcal O_{\mathbf P^4}(1)
\simeq\mathcal O_{\mathbf P^1}(2).
\tag{5.3}
\]

Its nonconstant image is therefore either:

1. a conic, reached birationally; or
2. a line, reached with degree two.

Suppose two distinct source rows \(j\ne k\) have proportional
quartics:

\[
H(\alpha_j,\lambda)
\sim
H(\alpha_k,\lambda).
\tag{5.4}
\]

Then

\[
\theta_H(\alpha_j)=\theta_H(\alpha_k).
\]

The conic alternative is an embedding and cannot identify two
distinct source points. Therefore the image of \(\theta_H\) is a
line. In particular,

\[
\boxed{
\dim\operatorname{span}
\{H(\alpha_j,\lambda):j\in\mathcal I^c\}
\le2.}
\tag{5.5}
\]

This proves the rank-two reduction for the repeated-fiber case; it
is not a heuristic fiber-cap rule.

## 6. The line image is an exact quotient precursor

The line-image alternative in either coefficient map has a canonical
fiber-product form. If the image of \(\varphi_H\) is a line, the
three quartics \(A,B,C\) in (2.1) span a two-dimensional space.
Equivalently, there are coprime pairs

\[
a(T),b(T)\in F[T]_{\le2},
\qquad
P(\lambda),Q(\lambda)\in F[\lambda]_{\le4}
\]

such that

\[
\boxed{
H(T,\lambda)=a(T)P(\lambda)+b(T)Q(\lambda).}
\tag{6.1}
\]

The same factorization follows from the line-image alternative for
\(\theta_H\). The pairs are coprime: a common factor of \(a,b\)
would give a vertical component, while a common factor of \(P,Q\)
would give a horizontal component.

Define

\[
g=[a:b]:\mathbf P^1_T\longrightarrow\mathbf P^1,
\qquad
f=[-Q:P]:\mathbf P^1_\lambda\longrightarrow\mathbf P^1.
\tag{6.2}
\]

The basepoint-free degrees in (2.3) and (5.3) give

\[
\deg g=2,\qquad \deg f=4.
\tag{6.3}
\]

Equation (6.1) is exactly

\[
\boxed{
H(T,\lambda)=0
\quad\Longleftrightarrow\quad
g(T)=f(\lambda).}
\tag{6.4}
\]

Thus every horizontal component fiber is a complete fiber of one
actual degree-two rational source map. The two maps are canonical
up to the simultaneous \(\operatorname{PGL}_2\) change of their
common target coordinate.

This proves a genuine quotient precursor in the line-image branch.
Excluding that branch, or adapting its quotient to a same-record owner,
is a downstream obligation and is not claimed in this packet.

## 7. The conic image is an exact pole-quotient precursor

Suppose the image of \(\varphi_H\) is a conic. Its normalization is
a Veronese embedding

\[
\nu:\mathbf P^1\hookrightarrow\mathbf P^2.
\]

The degree type in (4.1) is \((r,d)=(2,2)\), so

\[
\varphi_H=\nu\circ\chi
\]

for a basepoint-free degree-two map

\[
\chi=[p:q]:\mathbf P^1_\lambda\longrightarrow\mathbf P^1,
\qquad
\deg p=\deg q=2.
\tag{7.1}
\]

After one invertible linear change of the coefficient coordinates
in \(\mathbf P^2\), there are quadratic polynomials
\(a(T),b(T),c(T)\) such that

\[
\boxed{
H(T,\lambda)
=
a(T)p(\lambda)^2
+b(T)p(\lambda)q(\lambda)
+c(T)q(\lambda)^2.}
\tag{7.2}
\]

Equivalently, if

\[
\overline H(T,X,Y)
=a(T)X^2+b(T)XY+c(T)Y^2,
\]

then

\[
\boxed{
H=(\operatorname{id}_{\mathbf P^1_T}\times\chi)^*
\overline H.}
\tag{7.3}
\]

Thus the conic-image branch is the pullback of a bidegree-\((2,2)\)
correspondence through one actual degree-two quotient of the pole
parameter. The quotient is canonical up to
\(\operatorname{PGL}_2\), as it is the normalization factor of the
coefficient image conic.

This is a genuine pole-quotient precursor. As in Section 6, the
same-record owner/payment adapter is not supplied by the geometric
factorization alone.

Classifying and eliminating the finite conic-image signatures is a
downstream obligation and is not claimed in this packet.

## 8. Birational-quartic gluing in the simple-vertex branch

Assume now that the image type is \((r,d)=(1,4)\), that
\(D_{\mathcal K}\) is reduced, and that its ten points map to ten
distinct vertices of the six-line star configuration.

Let \(G\) be the simple graph on the six lines in which
\(\{j,k\}\) is an edge precisely when the quartic image contains
\(\mathscr L_j\cap\mathscr L_k\). Then

\[
|E(G)|=10.
\tag{8.1}
\]

Let \(e_j\in\{0,1,2\}\) be the number of the four free owned edge
points lying on \(\mathscr L_j\). Restriction of the plane quartic
to \(\mathscr L_j\) has degree four, and (3.2) accounts for all of
its zeros. Therefore

\[
\boxed{\deg_G(j)+e_j=4.}
\tag{8.2}
\]

For the complement graph \(\overline G\subset K_6\),

\[
|E(\overline G)|=5,
\qquad
\boxed{\deg_{\overline G}(j)=1+e_j.}
\tag{8.3}
\]

In particular every vertex of \(\overline G\) has positive degree.
If \(\overline G\) is connected, it is a tree. If it is
disconnected, it necessarily contains a cycle because

\[
|E|-|V|+\#\text{components}
=\#\text{components}-1>0.
\tag{8.4}
\]

### 8.1 Exact line-restriction gluing

Let \(R_j\) be the degree-four section on \(\mathscr L_j\) whose
zero divisor consists of:

1. the selected star vertices incident to \(j\); and
2. the \(e_j\) owned free edge points on \(\mathscr L_j\).

The restriction of an actual quartic equation \(F_C\) to
\(\mathscr L_j\) has the form

\[
F_C|_{\mathscr L_j}=c_jR_j
\tag{8.5}
\]

for a nonzero scalar \(c_j\).

At a selected star vertex, both adjacent restrictions vanish and
compatibility is automatic. At an unselected vertex
\(v_{jk}=\mathscr L_j\cap\mathscr L_k\), both values are nonzero
and gluing is exactly

\[
\boxed{
c_jR_j(v_{jk})=c_kR_k(v_{jk}).}
\tag{8.6}
\]

These are the edges of \(\overline G\).

If \(\overline G\) is a tree, equations (8.6) determine all six
\(c_j\)'s uniquely up to common scale. If it contains a cycle, the
product of the corresponding nonzero edge ratios around every
cycle must equal one. These are explicit multiplicative equations
in the actual source labels and free pole points.

Compatibility at the fifteen pairwise intersections is sufficient
to glue the six restrictions to a unique plane quartic. Indeed, for
the union \(\mathscr A=\bigcup_j\mathscr L_j\), the restriction
sequence is

\[
0\longrightarrow\mathcal O_{\mathbf P^2}(-2)
\longrightarrow\mathcal O_{\mathbf P^2}(4)
\longrightarrow\mathcal O_{\mathscr A}(4)
\longrightarrow0.
\tag{8.7}
\]

Since
\(H^0(\mathcal O_{\mathbf P^2}(-2))=
H^1(\mathcal O_{\mathbf P^2}(-2))=0\), restriction is an
isomorphism onto the compatible line sections. Hence:

\[
\boxed{
\begin{array}{l}
\text{tree complement: one explicit quartic up to scale};\\
\text{cyclic complement: explicit cycle-product gates; if they}\\
\text{hold, each projective solution of the component-scale}\\
\text{system glues to one unique quartic.}
\end{array}}
\tag{8.8}
\]

### 8.2 Finite tree census

In the tree branch, (8.3) says that the Prüfer word of
\(\overline G\) has length four and contains label \(j\) exactly
\(e_j\) times. Therefore the number of compatible labeled trees for
one owned-edge distribution is

\[
\boxed{
\frac{4!}{\prod_{j=1}^6e_j!}.}
\tag{8.9}
\]

This is at most \(24\). There are only
\(\binom{12}{4}=495\) choices of four free pole edges before the
pole-cycle condition is imposed. The exact labeled census is

\[
\begin{array}{c|c}
\text{owned-edge count pattern}&\text{tree cases}\\ \hline
1+1+1+1&5{,}760\\
2+1+1&2{,}880\\
2+2&90
\end{array}
\tag{8.10}
\]

and hence

\[
\boxed{5{,}760+2{,}880+90=8{,}730}
\tag{8.11}
\]

raw labeled gluing cases. This is smaller than the coarse cap
\(495\cdot24=11{,}880\).

The disconnected complements are finite as well. Enumerating the
\(\binom{15}{5}=3{,}003\) five-edge subgraphs of \(K_6\), retaining
exactly those with degrees in \(\{1,2,3\}\), gives:

\[
\begin{array}{c|c|c}
\text{complement type}&\text{graphs}&
\text{graph/free-edge cases}\\ \hline
\text{connected tree}&1{,}170&8{,}730\\
\text{disconnected cyclic}&285&2{,}400
\end{array}
\tag{8.12}
\]

Here a degree \(d_j\) at vertex \(j\) forces
\(e_j=d_j-1\), and contributes
\(\binom2{e_j}\) choices of the actual free pole edges. Therefore
the entire simple-vertex branch has exactly

\[
\boxed{1{,}455\text{ complement graphs and }11{,}130
\text{ graph/free-edge cases}.}
\tag{8.13}
\]

For each case, the remaining checks are exact:

1. construct the six \(R_j\)'s;
2. solve (8.6);
3. interpolate the unique quartic;
4. test irreducibility and geometric genus zero;
5. recover its normalization parameter and compare it with the
   actual component;
6. emit the cycle-union conclusion or an actual endpoint minor.

This is a finite elimination target over the deployed labels. The
disconnected cases first test their cycle-product gates; the
connected cases have a unique scalar solution. A
generic quartic through the fourteen prescribed points has genus
three, so the rationality requirement is load-bearing.

Repeated star vertices and ramification in \(D_{\mathcal K}\) are
not covered by this simple branch. They must be handled with local
intersection multiplicities and the total \(\delta\)-invariant
budget three of a rational plane quartic.

### 8.3 Duplicate normalization preimages

There is nevertheless an exact bound on the repeated-vertex
remainder when \(D_{\mathcal K}\) is reduced. Let \(n_v\) be the
number of points in the normalization lying over a star vertex
\(v\). Distinct normalization preimages are distinct local branches,
and therefore

\[
\delta_v\ge n_v-1.
\tag{8.14}
\]

An irreducible plane quartic has arithmetic genus three. Since the
component is rational,

\[
\sum_v\delta_v=3.
\tag{8.15}
\]

Consequently

\[
\boxed{\sum_v(n_v-1)\le3.}
\tag{8.16}
\]

Thus at least seven of the ten unramified common-pole points map to
distinct star vertices. Only three duplicate-preimage units remain
outside the simple-vertex branch. This does not cover a ramified
point of \(D_{\mathcal K}\), where one normalization point can carry
higher pullback multiplicity without creating a second branch.

## 9. Exhaustive split of normalized finite searches

For a \(u=2\) component, the four edge incidences imply that at
least two of the six noninvariant rows contain no edge pole.

There are two exhaustive cases.

### 9.1 Two distinct zero-edge quartics

Choose their two distinct monic split locators \(P,Q\). All six
row quartics lie in a vector space of dimension at most three by
(5.1). Modulo \(\operatorname{span}\{P,Q\}\), every remaining
quartic therefore lies in one common projective residual direction
or has zero residual.

This is the correct rank-three finite-search parameterization.
The residual direction must be drawn from the union of all six
rows; choosing it only from one preselected row is not exhaustive.

### 9.2 The zero-edge quartics coincide

The exact two-occurrence rule from Section 3 implies that there are
exactly two zero-edge rows and that the other four rows each own
one edge pole. Equation (5.5) then puts all six quartics on one
projective line. A finite search need only test
\(\operatorname{span}\{P,Q_1\}\), where \(Q_1\) is any one of the
four edge-containing quartics.

These two cases cover every normalized finite \(u=2\) tuple. In the
second case, Section 6 already supplies the exact quotient precursor,
so a finite search is only a regression for the stronger
no-configuration claim.

## 10. Sharpened remaining lemma

The \(u=2\) part of the component cycle-union target is reduced to:

> **Star-configuration pullback lemma.**
> Let \(\varphi:\mathbf P^1\to\mathbf P^2\) be one of the three
> maps in (4.1), arising from the actual bidegree-\((2,4)\)
> component, and let \(\mathscr L_1,\ldots,\mathscr L_6\) be the
> six source-evaluation lines. If
> \[
> \varphi^*\left(\sum_j\mathscr L_j\right)
> =2D_{\mathcal K}+E
> \]
> with \(D_{\mathcal K}=\psi^*\mathcal K\) and \(E\) the four
> selected free pole edges, then \(E\) is a union of complete
> pole-graph cycles, or the same component equations emit one of
> the selected endpoint contradictions listed in the low-degree
> component interpolation target.

The three image-degree cases suggest different proof mechanisms:

* **line image:** prove the exact free-incidence divisor contradiction,
  or emit a paid same-record quotient owner;
* **conic image:** classify the induced degree-two quotient and its
  finite pole-graph signatures, then eliminate them or emit a paid
  same-record owner;
* **quartic image:** use the finite gluing reduction in Section 8;
  the full simple-vertex branch has exactly 11,130 raw
  graph/free-edge cases, including 8,730 trees and 2,400 cyclic
  complements, while
  an unramified rational quartic has at most three duplicate
  normalization-preimage units over the star vertices. Ramified
  common-pole fibers remain a separate local-intersection branch.

The line and conic cases should be attempted before a general
quartic elimination.

## 11. Guardrails

This reduction does not justify any of the following:

* replacing the actual source labels by one convenient twelve-point
  numerical normalization;
* replacing \(D_{\mathcal K}\) by ten distinct points when the deck
  can ramify over \(\mathcal K\);
* inferring the exact weighted-GRS interpolation law from
  coefficient rank at most three;
* treating a normalized finite-field no-solution result as a proof
  for the deployed endpoint;
* booking a rank-two owner without identifying the corresponding
  actual reciprocal block rows.

Any finite regression accompanying this note is evidence about its
printed normalization only.
