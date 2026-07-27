# Pole-Disjoint Conic Endpoint Classification

## 1. Status and role

This is the closest live target in the KoalaBear source-bound
owner/partition bridge.

### v18 facet-collinearity update

The external facet-collinearity reduction proves that three actual
blocks contained in one 12-set would give three distinct collinear
points on the irreducible conic, which is impossible. It also proves
the corresponding 13-set quadratic-pencil refinement, reciprocal
block coordinates, block distinctness, rank three, the component law
\((u,2u)\), and the exact grid vertex formula. The subsequent
deck analysis proves that every conjugate block pair has one common
intersection parameter \(Q\), and excludes \(Q=1\) by a dihedral
coordinate-pencil contradiction. The outgoing curve/deck-conjugate
intersection bound also excludes \(Q=2,3,4\), and gives an exact
degree-100 resultant packet at \(Q=5\), followed by a
\((5,5)\)-by-\((3,4)\) quotient resultant of degree 35. The exact
fixed-pole source derivative then excludes that equality packet. Thus any remaining
\((1,2)\)-component branch has
\[
6\le Q\le10.
\]

Consequently the two-template family in Section 6 is not a possible
irreducible endpoint. It remains the expected model for the separate
reducible two-line branch. The focused sufficient target for the
irreducible branch is now:

```text
target/pole_disjoint_conic_one_triangle_target.md
```

The preceding packet proves every line branch impossible. It also
reduces the principal irreducible-conic branch to the exact endpoint
specified below. The endpoint itself is not proved impossible and has
not been routed to a same-record owner.

```text
TARGET STATUS: OPEN
ACTIVE OWNER PAYMENT: NONE
EQUALITY-WALL PAYMENT: NOT BOOKED
```

The target is deliberately stated with all source-coupled data. The
bare incidence design is too weak, as Section 7 demonstrates at the
actual parameters.

## 2. Inherited KoalaBear data

Work over the deployed KoalaBear field, or after a scalar extension
when taking projective roots. The principal row has

\[
a=12,\qquad R=69,\qquad k=59,\qquad m=2k+2=120.
\tag{2.1}
\]

Let

\[
\mathcal T=\{t_1,\ldots,t_{69}\}
\]

be the selected carrier roots and

\[
\Lambda=\{\lambda_1,\ldots,\lambda_{120}\}
\]

the distinct selected conic parameters.

The normalization of the assumed irreducible plane conic has twelve
nonzero quadratic coordinate forms

\[
z_i(\lambda)\in H^0(\mathbf P^1_\lambda,\mathcal O(2)),
\qquad 1\le i\le12.
\]

They span \(H^0(\mathcal O(2))\), and their projective root divisors
are pairwise disjoint:

\[
\gcd(z_i,z_j)=1\qquad(i\ne j).
\tag{2.2}
\]

Repeated roots within one \(z_i\) are allowed. Put

\[
B(\lambda)=\prod_{i=1}^{12}z_i(\lambda),
\qquad
h_i(\lambda)=\frac{B(\lambda)}{z_i(\lambda)}.
\tag{2.3}
\]

Thus \(\deg B=24\) and \(\deg h_i=22\). The \(h_i\) are linearly
independent: at a root belonging only to \(z_i\), the rational
functions \(h_j/B=1/z_j\) have distinct pole support, and the same
argument with the highest local pole order handles a double root.

Let \(L_i(T)\) be the degree-eleven Lagrange source basis and
\(\kappa_i\ne0\). The endpoint curve is

\[
M(T,\lambda)
=
\sum_{i=1}^{12}\kappa_iL_i(T)h_i(\lambda).
\tag{2.4}
\]

It has bidegree \((11,22)\), has no vertical or horizontal component,
and

\[
\mathcal D=V(M)\subset\mathbf P^1_T\times\mathbf P^1_\lambda.
\tag{2.5}
\]

For every actual \(\lambda_s\), the horizontal fiber

\[
M(T,\lambda_s)
\]

is a nonzero scalar multiple of a squarefree degree-eleven locator
whose roots lie in \(\mathcal T\).

## 3. Exact endpoint identity

Define

\[
V(T)=\prod_{t\in\mathcal T}(T-t),
\qquad
L(\lambda)=\prod_{s=1}^{120}(\lambda-\lambda_s),
\tag{3.1}
\]

and let

\[
A(T)=\prod_{i=1}^{12}(T-\alpha_i)
\]

be the source locator. The effective conic source-pole theorem proves

\[
\mathcal O_{\mathcal D}(12,-24)\simeq\mathcal O_{\mathcal D}.
\tag{3.2}
\]

After five periods, the grid section is the restriction of a unique
polynomial \(Q_9(T)\) of degree at most nine:

\[
\frac{V(T)B(\lambda)^5}
     {L(\lambda)A(T)^5}
=Q_9(T)
\qquad\text{on }\mathcal D.
\tag{3.3}
\]

Equivalently, there is a bihomogeneous \(W\) of bidegree \((58,98)\)
such that

\[
\boxed{
V(T)B(\lambda)^5
-
Q_9(T)L(\lambda)A(T)^5
=M(T,\lambda)W(T,\lambda).
}
\tag{3.4}
\]

Every factor and every selected record in (3.4) is inherited from the
actual source packet. A proof may not replace them by arbitrary
polynomials having only the same degrees.

## 4. Exact design consequence

Exactly sixty selected roots are active and nine are inactive:

\[
\mathcal T
=
\mathcal T_{\rm act}\sqcup\mathcal T_{\rm inact},
\qquad
|\mathcal T_{\rm act}|=60,
\qquad
|\mathcal T_{\rm inact}|=9.
\tag{4.1}
\]

The degree-nine remainder is exactly

\[
Q_9(T)
=
c\prod_{t\in\mathcal T_{\rm inact}}(T-t),
\qquad c\ne0.
\tag{4.2}
\]

Index the locator support at \(\lambda_s\) by \(I_s\). Then

\[
I_s\subseteq\mathcal T_{\rm act},
\qquad
|I_s|=11,
\tag{4.3}
\]

and every active root belongs to exactly 22 indexed supports:

\[
\#\{s:t\in I_s\}=22.
\tag{4.4}
\]

Thus the indexed block family is an exact

\[
1\text{-}(60,11,22)
\tag{4.5}
\]

design, with 120 blocks and total incidence \(1320\).

## 5. Equivalent reciprocal-code formulation

Evaluate the independent functions \(h_i\) at the 120 actual
parameters:

\[
\mathcal C
=
\left\{
\left(
\sum_{i=1}^{12}c_ih_i(\lambda_s)
\right)_{s=1}^{120}
:
c_i\in\overline{\mathbf F}
\right\}.
\tag{5.1}
\]

This is a 12-dimensional reciprocal-quadratic evaluation code. The
coefficient vector

\[
[\kappa_1L_1(t):\cdots:\kappa_{12}L_{12}(t)]
\tag{5.2}
\]

traces a degree-eleven rational normal curve in
\(\mathbf P^{11}\). At each active selected root \(t\), the associated
codeword has exactly the 22 zero coordinates indexed by

\[
\{s:t\in I_s\}.
\tag{5.3}
\]

At each inactive root it has no zero coordinate. Therefore the target
may equivalently be viewed as a classification of a degree-eleven
rational normal curve containing sixty weight-98 words of this
source-derived reciprocal-quadratic code, with the exact global
identity (3.4).

This is not an ordinary GRS minimum-weight classification: the
functions have common numerator \(B\) and twelve disjoint quadratic
pole divisors. Any code argument must retain that pole structure.

## 6. Reducible two-template model and irreducible guardrail

A canonical line template on sixty roots consists of a partition

\[
\mathcal T_{\rm act}
=P_1\sqcup\cdots\sqcup P_5,
\qquad |P_j|=12,
\tag{6.1}
\]

and its sixty facets

\[
\{P_j\setminus\{t\}:1\le j\le5,\ t\in P_j\}.
\tag{6.2}
\]

Each root occurs in eleven of those facets. Two such indexed template
families therefore give 120 blocks and replication 22.

This is exactly the incidence profile expected from a reducible conic
whose two line components are each saturated at the proved
60-vertex canonical-line capacity.

The facet-collinearity theorem now proves that this family cannot be
the block family of the irreducible endpoint: any three facets of one
part give a forbidden collinear triple. Therefore deriving this model
inside the irreducible branch is already a contradiction. Canonical
component labels and same-record payment remain necessary only when
handling the separate reducible two-line branch.

## 7. Design-only guardrail

The \(1\)-design condition does not imply the two-template conclusion.
There is an explicit counterexample at the actual parameters.

Identify the active points with \(\mathbf Z/60\mathbf Z\). Take the
sixty translates of

\[
\{0,1,\ldots,10\}
\]

and the sixty translates of

\[
\{0,2,4,\ldots,20\}.
\]

All 120 blocks are distinct, every block has size eleven, and every
point occurs in 22 blocks. Hence this is a
\(1\)-\((60,11,22)\) design.

In a canonical facet family, the twelve facets of one 12-set are
pairwise 10-intersecting. In the displayed cyclic design, the graph
joining two blocks when they intersect in ten points has maximum clique
size two. It therefore contains no canonical 12-facet family at all.

The endpoint proof must use (3.4), the rational-normal coefficient
curve, the disjoint quadratic poles, or another equivalent
source-coupled property. Pure incidence regularity cannot work.

## 8. Target theorem

> **Pole-disjoint conic endpoint classification (PDCEC).**
> No actual principal KoalaBear packet satisfying Sections 2--4 exists
> on an irreducible conic.
>
> A sufficient sharpened form is to force one triple of blocks whose
> reciprocal coordinate rows have rank at most two. In particular it
> suffices to force three blocks contained in one 12-set, or a
> quadratic-pencil triple inside one 13-set.

A successful proof may establish either route:

1. **Exclusion form:** prove directly that (2.2)--(4.4) are
   incompatible with an irreducible conic.
2. **One-triangle form:** prove the focused sufficient target in
   `pole_disjoint_conic_one_triangle_target.md`.

## 9. Useful intermediate lemmas

### 9.1 Reciprocal-quadratic rational-normal splitting

Prove that a degree-eleven rational normal curve in the code (5.1)
cannot contain sixty distinct weight-98 words unless the twelve
quadratic poles separate into two canonical source templates.

This is the cleanest code-geometric formulation, but the conclusion
must be made canonical enough for the owner interface.

### 9.2 Endpoint factorization from the quotient identity

Use (3.4) at active roots and actual parameters to show that its local
first derivatives force groups of twelve locators sharing one
degree-twelve completion. Ten such groups would give the two
five-block partitions.

The promising data are:

* every active vertical fiber has all 22 intersections on the actual
  horizontal grid;
* \(Q_9(t)\ne0\) on every active root;
* all actual horizontal locators are squarefree;
* the source-pole period is exact, with no effective remainder.

### 9.3 Chow or toric curve classification

Regard the sixty active coefficient points as lying in the
fixed-root split-form locus inside \(\mathbf P^{22}\). Classify
degree-eleven rational curves in that locus under the additional
reciprocal-quadratic pole constraints.

A general classification of curves in the Chow variety is more than
is needed. The useful theorem must exploit the fixed 120-coordinate
evaluation grid and the twelve disjoint quadratic pole divisors.

### 9.4 Pair-codegree amplification

The design has average pair intersection close to two, but first- and
second-moment incidence alone do not force a template. A viable
amplification would derive large 10-intersection cliques from the
polynomial identity, then complete each clique to the unique
degree-twelve block.

### 9.5 Reducibility criterion

It would suffice to prove that the sixty active vertical fibers split
into two nonempty families whose coefficient points lie on two lines
in the ambient postcritical space. An irreducible plane conic meets a
line in at most two points unless the line is a component, so either
family would force reducibility once it contains three distinct
selected vertices.

## 10. Routes that do not suffice

The following conclusions are already excluded as complete proofs:

* the \(1\)-design axioms alone;
* ordinary Johnson or pair-incidence counting;
* treating (5.1) as an arbitrary MDS/GRS code;
* producing an unrooted block partition;
* reusing the completed line theorem without deriving an actual line
  component;
* replacing the hard band or source packet by a generic quadratic
  parametrization;
* attaching a cell to another record having the same carrier support.

## 11. Finite experiments

The smallest numerical analogue with the same endpoint bookkeeping is

\[
a=4,\quad q=2,\quad R=9,\quad m=16,
\tag{11.1}
\]

giving eight active roots, one inactive root, sixteen 3-blocks, and
replication six. It is suitable for exact searches over small fields:

1. enumerate four pairwise pole-disjoint coordinate quadratics
   spanning \(H^0(\mathcal O(2))\);
2. construct the reciprocal curve \(M\);
3. search for sixteen squarefree split fibers on nine selected roots;
4. test the endpoint polynomial identity;
5. classify every surviving design up to projective and carrier
   relabeling.

The packet already verifies that all 715 characteristic-13
\((a,R)=(4,9)\) configurations with zero canonical-line capacity have
full postcritical rank. A direct conic-oriented search would provide a
more targeted regression but would remain finite evidence.

## 12. Valid proof and falsifier

A valid proof must consume the actual identity (3.4) or an equivalent
source-derived invariant and must preserve the selected-record labels
through the owner conclusion.

A valid falsifier must exhibit all of:

* twelve quadratic coordinate forms spanning \(H^0(\mathcal O(2))\);
* pairwise disjoint projective root divisors;
* 69 selected roots and 120 distinct actual parameters;
* squarefree degree-eleven fibers on the selected root set;
* the exact \(1\)-\((60,11,22)\) active design;
* the exact degree-nine inactive-root polynomial;
* the global identity (3.4);
* an irreducible conic;
* failure of every enabled same-record owner.

An arbitrary \(1\)-design, an abstract reciprocal code, or a freely
decorated owner family is not a falsifier.

## 13. Downstream consequence

PDCEC closes the principal irreducible-conic endpoint. Combined with
the proved grouped-Cauchy line theorem, it removes every principal
postcritical circuit through support \(2k+2\), except for the separately
specified reducible-conic payment interface.

The remaining circuit hierarchy would then begin with:

```text
reducible two-line conic template/payment
a=14, R=67 and R=69 conic boundaries
selected-record cubic emission
support at least 3k+1
```

PDCEC is therefore a major but not final step toward the complete
KoalaBear equality-wall payment.
