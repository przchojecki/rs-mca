# Pole-Disjoint Conic \(Q=5\) Resultant Target (Resolved)

## 0. Resolution

The source-coupled target formulated below is proved impossible by
Theorem 9.17 of
`proof/pole_disjoint_conic_facet_collinearity_reduction.md`.

At either deck-fixed double coordinate pole, the exact source
presentation gives

\[
\frac{\partial_\lambda M}{M}
=
\frac{\partial_\lambda h_\ell}{h_\ell},
\]

which is independent of \(T\). The graph and deck-invariant component
factors have zero odd derivative there, so the outgoing odd part
\(H(T,w_\pm)\) must be proportional to the fixed outgoing fiber
\(E(T,w_\pm)=c_\pm P_S(T)\). But \(H\) contains both double-pole
source factors, while \(P_S\) contains neither. The proportionality
constant is zero. Every root in \(S\) then has fixed-point
multiplicity at least two, contradicting the simplicity forced by
the exact degree-100 intersection equality.

Therefore

\[
\boxed{Q=5\text{ is impossible}.}
\]

The next open deck value is \(Q=6\).

## 1. Role and status

This was the smallest remaining subtarget in the
\((1,2)\)-component branch before Theorem 9.17. It is retained as a
resolved proof-development record, not as a live target.

At the stage when this target was formulated, the preceding reduction
had proved

\[
Q\in\{5,6,7,8,9,10\}.
\]

The active range is now

\[
Q\in\{6,7,8,9,10\},
\]

with \(Q=6\) formulated in
`target/pole_disjoint_conic_q6_intersection_target.md`.

At \(Q=5\), all intersection inequalities are equalities. The branch
has an exact invariant/anti-invariant normal form and only two
possible outgoing-component partitions:

\[
\boxed{5\qquad\text{or}\qquad3+2.}
\]

This historical target is retained because its normalization is a
useful audit trail. It is closed by direct contradiction; no active
owner payment is needed.

## 2. Inherited endpoint data

Work over the algebraic closure of the deployed KoalaBear field,
whose characteristic is odd. The packet prints:

1. twelve distinct source points
   \[
   \alpha_1,\ldots,\alpha_{12}\in\mathbf P^1_T;
   \]
2. twelve pairwise-disjoint effective quadratic coordinate divisors
   \[
   Z_j=\operatorname{div}(z_j),
   \]
   whose binary quadratics span a three-dimensional space;
3. the pole divisor
   \[
   \operatorname{div}B=\sum_{j=1}^{12}Z_j;
   \]
4. the degree-two source map
   \[
   \psi:\mathbf P^1_\lambda\longrightarrow\mathbf P^1_w
   \]
   with deck involution \(b\);
5. the endpoint factor \(M(T,\lambda)\) and complementary factor
   \(W_1(T,\lambda)\), with \(\gcd(M,W_1)=1\);
6. the exact source fibers
   \[
   \operatorname{div}M(\alpha_j,\cdot)
   =\operatorname{div}B-Z_j;
   \]
7. the outgoing component union
   \[
   \mathcal X_{\rm out}\subseteq V(M)
   \]
   of bidegree \((5,10)\), whose deck conjugate lies in \(V(W_1)\);
8. all 120 selected-record fibers, the 60 deck pairs, the block
   coordinates, and the exact grid derivative identities.

The union \(\mathcal X_{\rm out}\) is either irreducible with
component parameter \(u=5\), or it has two components with parameters
\(u=3\) and \(u=2\). An outgoing graph component is already excluded.

## 3. Exact equality packet

Let \(\beta_+,\beta_-\) be the two fixed points of \(b\). Equality in
the outgoing/deck-conjugate intersection bound proves that both are
coordinate poles. There are distinct labels
\(\ell_+,\ell_-\) with

\[
Z_{\ell_+}=2[\beta_+],
\qquad
Z_{\ell_-}=2[\beta_-].
\tag{3.1}
\]

No other coordinate divisor meets its deck conjugate:

\[
\gcd(Z_j,bZ_j)=0
\quad
(j\notin\{\ell_+,\ell_-\}).
\tag{3.2}
\]

The outgoing curve and its conjugate have intersection number \(100\).
Every intersection lies on a source line, with multiplicity ten at
\(\alpha_{\ell_+},\alpha_{\ell_-}\) and multiplicity eight at each
other source:

\[
\operatorname{div}
\operatorname{Res}_\lambda
(\mathcal X_{\rm out},b\mathcal X_{\rm out})
=
8\sum_{j=1}^{12}[\alpha_j]
+2[\alpha_{\ell_+}]
+2[\alpha_{\ell_-}].
\tag{3.3}
\]

## 4. Invariant/anti-invariant descent

Choose coordinates \([x:y]\) with

\[
b[x:y]=[x:-y],
\qquad
w=[x^2:y^2].
\]

A defining form of the outgoing curve decomposes uniquely as

\[
F_{\rm out}(T;x,y)
=E(T;x^2,y^2)+xy\,H(T;x^2,y^2),
\tag{4.1}
\]

where

\[
\operatorname{bideg}E=(5,5),
\qquad
\operatorname{bideg}H=(5,4).
\tag{4.2}
\]

There is a five-subset

\[
S\subseteq
\{1,\ldots,12\}\setminus\{\ell_+,\ell_-\}
\]

such that, for \(P_S(T)=\prod_{j\in S}(T-\alpha_j)\),

\[
E(T,w_+)=c_+P_S(T),
\qquad
E(T,w_-)=c_-P_S(T),
\quad c_\pm\ne0.
\tag{4.3}
\]

Put

\[
R=
\{1,\ldots,12\}
\setminus
\bigl(S\cup\{\ell_+,\ell_-\}\bigr);
\qquad |R|=5.
\]

The anti-invariant part has the exact source factor

\[
H(T,w)
=(T-\alpha_{\ell_+})(T-\alpha_{\ell_-})H_3(T,w),
\tag{4.4}
\]

where

\[
\operatorname{bideg}H_3=(3,4).
\]

The residual resultant is completely prescribed:

\[
\boxed{
\operatorname{div}\operatorname{Res}_w(E,H_3)
=
3\sum_{j\in S}[\alpha_j]
+4\sum_{j\in R}[\alpha_j].}
\tag{4.5}
\]

Equivalently:

* for \(j\in S\), the specialized forms
  \(E(\alpha_j,w)\) and \(H_3(\alpha_j,w)\) have gcd degree three;
* for \(j\in R\), their gcd degree is four;
* they are coprime at
  \(T=\alpha_{\ell_+},\alpha_{\ell_-}\);
* they have no common zero away from these ten source lines.

The total intersection degree is

\[
(5,5)\cdot(3,4)=35=5\cdot3+5\cdot4.
\]

## 5. Source coupling that must be retained

The bare forms \(E,H_3\) are not the whole theorem. A valid proof must
retain their derivation from the actual endpoint:

1. \(F_{\rm out}\) divides \(M\);
2. \(F_{\rm out}^b\) divides \(W_1\);
3. each outgoing source fiber is an actual sub-divisor of
   \(\operatorname{div}B-Z_j\);
4. the selected-record fibers are squarefree at all 120 actual
   parameters;
5. the component bidegrees are either \(5\), or \(3+2\);
6. every outgoing component maps birationally to an even-subdegree
   component of
   \[
   f(T)=f(w),
   \qquad
   f(T)=\frac{V_{\rm act}(T)}{A(T)^5};
   \]
7. the block coordinates satisfy the exact reciprocal rank-three
   realization;
8. at every actual incidence \((t,\lambda_s)\), the vertex identity
   \[
   \frac{c_t'(\lambda_s)V_{\rm act}'(t)}
        {A(t)^5U_s'(t)}
   \]
   is constant across \(t\in I_s\).

An argument using only (4.3)--(4.5) is a source-free resultant
classification and does not by itself emit the selected owner.

## 6. Target conclusion (achieved)

Prove one of the following:

1. the \(Q=5\) packet is impossible;
2. three actual reciprocal block rows have rank at most two;
3. one actual selected record emits a previously enabled quotient,
   planted, field, collective-rank, or saturation owner, together
   with its printed payment.

The first conclusion is proved by the source-derivative contradiction
in Section 0. The two component partitions do not need separate
classification.

## 7. Suggested proof routes

### 7.1 Sylvester-bundle rigidity

View the Sylvester matrix of \(E\) and \(H_3\) as the bundle map

\[
\mathcal O(-5)^4\oplus\mathcal O(-3)^5
\longrightarrow
\mathcal O^9
\]

on the \(T\)-line. Its determinant has maximal possible degree \(35\),
while its fiber corank is at least three on \(S\) and at least four
on \(R\). Classify the equality case while imposing both
fixed-section identities (4.3).

The required conclusion is not just the determinant formula: one
must recover a global kernel, a forbidden factor, or a source-ranked
minor.

### 7.2 Component-factor analysis

For partition \(3+2\), write

\[
F_{\rm out}=F_3F_2
\]

with bidegrees \((3,6)\) and \((2,4)\). Decompose each factor into
its even and odd parts under \(b\), then compare the induced
factorization of \(E,H_3\) with the exact \(3/4\) source gcd pattern.
The unequal component degrees should make any exchange of the two
five-element fixed fibers visible.

For partition \(5\), use irreducibility to exclude any global
subresultant kernel produced by the Sylvester equality case.

### 7.3 Source derivative residues

At the 45 quotient intersection points printed by (4.5), combine the
local Sylvester kernel with the exact grid vertex formula. Products
around alternating source/root cycles cancel the block scalars. The
desired output is a vanishing \(3\times3\) reciprocal minor, not
merely a relation among unlabeled quotient points.

### 7.4 Low-subdegree monodromy

The outgoing component images have subdegrees \(10\), or \(6\) and
\(4\), in the degree-60 self-correspondence of \(f\). Classify these
suborbits under the inertia element of cycle type \(5^{12}\), while
retaining the quadratic lift. An imprimitive conclusion must be
converted to an actual source quotient or to a contradiction with
the two double coordinate poles.

## 8. Guardrails

Do not:

* replace the exact source fibers by arbitrary split forms;
* infer a global gcd only from the resultant divisor;
* count a per-witness interpolation rank drop as collective rank;
* forget that an emitted cell must contain the same selected owner;
* use a finite-field experiment as a deployed-field proof;
* book a payment from the \(Q=5\) normal form alone.

## 9. Valid falsifier

A falsifier must realize the full endpoint data in Section 2,
including actual selected parameters, source fibers, component
partition, complementary factor, rank-three coordinates, and vertex
identities. Abstract forms satisfying only (4.3)--(4.5) do not
falsify the source-coupled target.
