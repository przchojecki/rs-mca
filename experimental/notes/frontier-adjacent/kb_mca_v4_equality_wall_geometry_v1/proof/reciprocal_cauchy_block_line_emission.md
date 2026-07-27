# Reciprocal-Cauchy Block-Line Emission

## 1. Status

This note proves an exact planted branch of the corrected
semantic-or-interpolation target.

The universal postcritical interpolation statement is false. In every
explicit counterexample currently known, the postcritical relation is
supported on reciprocal-Cauchy vertices lying on an overloaded line. Those
lines arise canonically from selected parameter blocks, and equality of two
block lines is equivalent to an exact split-pencil identity over the source
locator.

Thus the known interpolation failures are not unstructured failures. They
emit a bounded source-algebraic planted precursor.

This note does not prove that every postcritical relation contains an
overloaded block line, and it does not by itself validate an owner payment.

## 2. Reciprocal-Cauchy vertices

Let

\[
\alpha_1,\ldots,\alpha_a
\]

be distinct source values and let

\[
t_1,\ldots,t_R
\]

be distinct selected parameters, disjoint from the source values. Put

\[
n=a-1.
\]

For each \(n\)-subset \(I\subseteq[R]\), use the reciprocal-Cauchy
normalization

\[
y_I
=
\left[
\frac1{\prod_{i\in I}(\alpha_1-t_i)}
:\cdots:
\frac1{\prod_{i\in I}(\alpha_a-t_i)}
\right]
\in\mathbf P^{a-1}.
\tag{2.1}
\]

Fixed nonzero diagonal scalings of the ambient coordinates do not affect
any assertion below.

Write

\[
A_\Sigma(T)=\prod_{j=1}^a(T-\alpha_j)
\tag{2.2}
\]

for the source locator.

## 3. Every selected \(a\)-block gives a line

Fix an \(a\)-subset \(B\subseteq\{t_1,\ldots,t_R\}\), and put

\[
P_B(T)=\prod_{b\in B}(T-b).
\tag{3.1}
\]

For \(b\in B\), the vertex indexed by \(B\setminus\{b\}\) has coordinates

\[
\frac1{\prod_{r\in B\setminus\{b\}}(\alpha_j-r)}
=
\frac{\alpha_j-b}{P_B(\alpha_j)}.
\tag{3.2}
\]

Define

\[
\mathbf 1=(1,\ldots,1),
\qquad
\boldsymbol\alpha=(\alpha_1,\ldots,\alpha_a),
\]

and

\[
D_B=
\operatorname{diag}\left(
P_B(\alpha_1)^{-1},\ldots,P_B(\alpha_a)^{-1}
\right).
\]

Then all \(a\) vertices

\[
\mathcal V_B=
\{y_{B\setminus\{b\}}:b\in B\}
\tag{3.3}
\]

lie on the explicit line

\[
\boxed{
L_B=
\mathbf P\left(
D_B\operatorname{span}\{\mathbf1,\boldsymbol\alpha\}
\right).
}
\tag{3.4}
\]

They are distinct because the map

\[
b\longmapsto
D_B(\boldsymbol\alpha-b\mathbf1)
\]

is a projective parametrization of \(L_B\).

## 4. Exact coincidence criterion

### Theorem 4.1: block-line equality

Assume \(a\ge3\). For two selected \(a\)-blocks \(B,C\),

\[
\boxed{
L_B=L_C
}
\tag{4.1}
\]

if and only if there is \(c\in F^\times\) such that

\[
\boxed{
P_B-cP_C=(1-c)A_\Sigma.
}
\tag{4.2}
\]

If \(B\ne C\), then \(c\ne1\).

### Proof

Suppose first that \(L_B=L_C\). Multiplying the two-dimensional vector
spaces in (3.4) by \(D_B^{-1}\) gives

\[
\operatorname{diag}(r_1,\ldots,r_a)
\operatorname{span}\{\mathbf1,\boldsymbol\alpha\}
=
\operatorname{span}\{\mathbf1,\boldsymbol\alpha\},
\tag{4.3}
\]

where

\[
r_j=\frac{P_B(\alpha_j)}{P_C(\alpha_j)}.
\]

The image of \(\mathbf1\) gives constants \(u,v\) with

\[
r_j=u+v\alpha_j.
\tag{4.4}
\]

The image of \(\boldsymbol\alpha\) gives constants \(w,z\) with

\[
\alpha_jr_j=w+z\alpha_j.
\tag{4.5}
\]

Substituting (4.4) into (4.5) shows that the quadratic polynomial

\[
vT^2+(u-z)T-w
\]

vanishes at the \(a\ge3\) distinct source values. It is zero. Hence

\[
v=0,\qquad w=0,\qquad z=u,
\]

so every \(r_j\) equals one constant \(c\ne0\). Therefore

\[
P_B(\alpha_j)-cP_C(\alpha_j)=0
\qquad(1\le j\le a).
\]

The degree-\(a\) polynomial \(P_B-cP_C\) is divisible by the monic
degree-\(a\) source locator. Its leading coefficient is \(1-c\), giving
(4.2).

Conversely, (4.2) gives

\[
P_B(\alpha_j)=cP_C(\alpha_j)
\]

at every source value. Thus \(D_B=c^{-1}D_C\), and (3.4) gives
\(L_B=L_C\).

If \(c=1\), then \(P_B=P_C\), so unique factorization and monicity give
\(B=C\). \(\square\)

### Corollary 4.2: disjoint fibers and exact canonical-line capacity

Distinct selected blocks carried by one block line are pairwise disjoint.
More generally, every selected vertex on \(L_B\), including a vertex not
belonging to \(\mathcal V_B\), comes from a full or near-full split fiber
of the same pencil

\[
\operatorname{span}\{P_B,A_\Sigma\}.
\tag{4.6}
\]

These fibers have disjoint selected roots. Consequently, the number of
selected reciprocal-Cauchy vertices on a canonical block line is at most

\[
\boxed{
m_{\rm can}(R,a)
=
a\left\lfloor\frac Ra\right\rfloor
+
\mathbf1_{\{R\bmod a=a-1\}}.
}
\tag{4.7}
\]

At interpolation degree \(k\), the relation space supported by \(m\)
distinct vertices on the line has exact dimension

\[
\boxed{
\max\{0,m-(k+1)\}.
}
\tag{4.8}
\]

To prove the fiber statement, let \(I\) be an \((a-1)\)-subset whose
vertex lies on \(L_B\). By (3.4), there are \(u,v\in F\) such that

\[
P_B(\alpha_j)
=
(u+v\alpha_j)P_I(\alpha_j)
\qquad(1\le j\le a).
\]

The degree-\(a\) polynomial

\[
P_B-(u+vT)P_I
\]

is therefore divisible by \(A_\Sigma\). Comparing leading coefficients
gives the exact identity

\[
\boxed{
P_B-(u+vT)P_I=(1-v)A_\Sigma.
}
\tag{4.9}
\]

If \(v\ne0\), put \(\beta=-u/v\). Then

\[
P_B-(1-v)A_\Sigma
=
v(T-\beta)P_I.
\tag{4.10}
\]

Thus \(I\cup\{\beta\}\) is one degree-\(a\) fiber of the pencil. It is a
full selected fiber when \(\beta\) is selected and a near-full fiber when
\(\beta\) is not selected. If \(v=0\), (4.9) is the corresponding
degree-drop fiber with the missing root at infinity, again a near-full
fiber.

Two different pencil parameters cannot share a finite root: a common root
would annihilate both \(P_B\) and \(A_\Sigma\), contrary to the
source/selected disjointness. Hence all full and near-full fibers have
disjoint selected roots. A full fiber consumes \(a\) selected roots and
contributes \(a\) vertices; a near-full fiber consumes \(a-1\) selected
roots and contributes one vertex. Maximizing

\[
qa+s(a-1)\le R,
\qquad
m=qa+s
\]

gives (4.7): full fibers are always more efficient, and after taking
\(\lfloor R/a\rfloor\) of them the remainder supports one near-full fiber
only when it equals \(a-1\).

Distinct full blocks are disjoint as a special case. Alternatively,
Theorem 4.1 and evaluation at a hypothetical common selected root give
\((1-c)A_\Sigma(x)=0\), again a contradiction. Finally, distinct points
on a projective line impose \(\min\{m,k+1\}\) independent conditions on
degree-\(k\) forms, proving (4.8).

At the postcritical degree

\[
k=R-a+2,
\]

the maximum relation dimension supported on one canonical block line is

\[
\boxed{
\max\left\{
0,\,
m_{\rm can}(R,a)-R+a-3
\right\}.
}
\tag{4.11}
\]

## 5. Semantic meaning

For distinct blocks, (4.2) is a nontrivial pencil of three monic split
locators:

\[
P_B,\qquad P_C,\qquad A_\Sigma.
\]

Equivalently,

\[
P_B
=
cP_C+(1-c)A_\Sigma.
\tag{5.1}
\]

The datum

\[
\boxed{
(B,C,c,P_B,P_C,A_\Sigma)
}
\tag{5.2}
\]

is canonical and verifier-checkable from the selected and source values.
It is a bounded split-pencil planted precursor. It is rooted in the actual
selected records indexed by

\[
B\setminus\{b\},
\qquad
C\setminus\{c'\}.
\]

To become an active owner payment, the repository atlas must recognize
(5.2), prove that one of those same selected records is contained in the
paid cell, and apply whole-slope deletion. The polynomial identity alone
does not book payment.

## 6. Overloaded block lines force interpolation failure

Let \(k\) be the interpolation degree. A line carrying \(m\) distinct
points has degree-\(k\) Hilbert function at most

\[
\min\{m,k+1\}.
\]

Therefore:

### Corollary 6.1

If a collection of coincident block lines contributes more than \(k+1\)
distinct reciprocal-Cauchy vertices, then degree-\(k\) evaluation on the
full configuration is not surjective.

For postcritical interpolation,

\[
k=R-a+2.
\tag{6.1}
\]

At \((a,R)=(4,8)\), two disjoint four-blocks \(B,C\) partition the eight
selected parameters. Their coincident lines carry the eight distinct
vertices

\[
\mathcal V_B\sqcup\mathcal V_C.
\]

Since \(k=6\), a line has degree-\(6\) Hilbert function at most seven.
Thus (4.2) forces at least one postcritical relation.

## 7. Exact finite classification at \(\mathbf F_{13}\)

Take \(a=4,R=8\) over \(\mathbf F_{13}\). The four source and eight
selected values leave one field value unused. Translation moves that value
to zero, leaving

\[
\binom{12}{4}=495
\]

normalized source/selected partitions.

The exact census gives:

\[
\begin{array}{c|c|c}
\text{postcritical defect}
&
\text{coincident complementary block pairs}
&
\text{number of normalized partitions}
\\ \hline
0&0&474\\
1&1&18\\
2&2&3.
\end{array}
\tag{7.1}
\]

There are no mismatches. Hence every one of the 21 exceptional normalized
partitions is accounted for exactly by the block-line planted identity.
Translation gives 273 exceptions among all 6,435 partitions:

\[
234\text{ of defect }1,
\qquad
39\text{ of defect }2.
\]

The stronger relation-space computation also has no mismatch. For every
normalized partition, the complete left kernel of the postcritical
evaluation matrix equals the span of the relation spaces supported on its
coincident block lines:

\[
\begin{array}{c|c|c}
\dim K_{\rm global}
&
\dim K_{\rm block}
&
\text{number of normalized partitions}
\\ \hline
0&0&474\\
1&1&18\\
2&2&3.
\end{array}
\tag{7.2}
\]

For example, with sources

\[
\{0,1,2,5\}
\]

and complementary selected blocks

\[
B=\{3,4,7,11\},
\qquad
C=\{6,8,9,12\},
\]

one has \(c=4\) and

\[
P_B-4P_C=-3A_\Sigma
\qquad\text{in }\mathbf F_{13}[T].
\tag{7.3}
\]

The postcritical relation is supported on the eight collinear vertices
from \(\mathcal V_B\cup\mathcal V_C\).

Exact examples in characteristics \(17,19,23\) have the same form: defect
one, support on eight collinear vertices, and the identity (4.2).

Two higher-dimensional planted regressions give the same exact
relation-space conclusion:

\[
\begin{array}{c|c|c|c|c}
F&a&R&\dim K_{\rm global}&\dim K_{\rm block}\\ \hline
\mathbf F_{17}&5&10&2&2\\
\mathbf F_{17}&4&12&1&1.
\end{array}
\tag{7.4}
\]

The first packet has two coincident five-blocks. The second has three
coincident four-blocks. In both cases the quotient

\[
K_{\rm global}/K_{\rm block}
\]

is zero.

These finite statements do not prove that all fields or all
\((a,R)\)-ranges have no other exception type.

## 8. Corrected next theorem

The useful target is now:

> **Selected-record postcritical semantic-or-interpolation, SPSI.**
> For every actual KoalaBear reciprocal-Cauchy configuration in the
> equality-wall packet, either:
>
> 1. degree-\((R-a+2)\) evaluation is surjective; or
> 2. a nonzero postcritical relation emits a canonical enabled cell at one
>    of the same selected records in its support.

The block-line theorem proves the source-algebraic emission part of SPSI
for every relation generated by an overloaded family of coincident block
lines. The exact remaining lemma is:

> **Non-block-line relation classification.**
> Every postcritical relation not generated by overloaded coincident block
> lines either emits another enabled same-record semantic cell, or cannot
> occur in the actual KoalaBear range.

This is narrower and more realistic than KPRCI. It permits the explicit
rank failures already found, while requiring them to be consumed through
their printed source structure.

## 9. KoalaBear scale

At \(a=12,R=69\),

\[
k=59,
\qquad
k+1=60.
\]

One block contributes 12 vertices. Corollary 4.2 permits at most five
pairwise disjoint blocks and hence at most 60 vertices on one block line.
An overloaded line would require at least 61. Therefore:

\[
\boxed{
\text{The block-line mechanism cannot cause postcritical failure at }
(a,R)=(12,69).
}
\tag{9.1}
\]

The same capacity calculation for every surviving low-excess pair is:

\[
\begin{array}{c|c|c|c}
a&R\text{ range}&
\text{maximum block-line relation dimension}&
\text{zero-capacity values}\\ \hline
12&65,\ldots,69&4,3,2,1,0&69\\
13&66,\ldots,69&9,8,7,6&\varnothing\\
14&67,\ldots,69&0,0,0&67,68,69\\
15&68,69&4,3&\varnothing\\
16&69&8&\varnothing.
\end{array}
\tag{9.2}
\]

Whenever the capacity is positive, realizing it requires several
pairwise disjoint degree-\(a\) split locators in the same pencil

\[
\operatorname{span}\{P_{B_0},A_\Sigma\}.
\]

That is strong bounded split-pencil structure, substantially closer to
the existing planted/source-rational atlas than an arbitrary rank defect.
At the zero-capacity parameters, every failure is necessarily
non-block-line.

The remaining difficulty is to prove that every postcritical relation
either concentrates on such a low-degree carrier or gives a different
same-record semantic certificate. The known finite counterexamples no
longer obstruct that formulation.
