# Pole-Disjoint Conic One-Triangle Target

## 1. Status

This is the focused sufficient target produced by the
facet-collinearity reduction.

```text
PDCEC: OPEN
ONE-TRIANGLE TARGET: OPEN
NEW OWNER PAYMENT: NONE
```

All notation and hypotheses are inherited from:

```text
target/pole_disjoint_conic_endpoint_classification_target.md
proof/postcritical_conic_pole_support_reduction.md
proof/pole_disjoint_conic_facet_collinearity_reduction.md
```

## 2. Exact inherited packet

The packet contains:

* 60 active carrier roots;
* 120 pairwise distinct 11-subsets \(I_s\);
* every active root in exactly 22 blocks;
* twelve source roots \(\alpha_j\), disjoint from the active roots;
* nonzero weights \(\kappa_j\);
* reciprocal block rows
  \[
  x_s
  =
  \left(
  \frac{\kappa_j}{U_s(\alpha_j)}
  \right)_{j=1}^{12},
  \qquad
  U_s(T)=\prod_{t\in I_s}(T-t);
  \]
* the exact rank condition
  \[
  \operatorname{rank}(x_s)_{s=1}^{120}=3;
  \]
* the cleaned endpoint identity
  \[
  V_{\rm act}(T)B(\lambda)^5
  -
  cL(\lambda)A(T)^5
  =
  M(T,\lambda)W_1(T,\lambda);
  \]
* the complementary fiber laws and vertex derivative identity;
* component bidegrees \((u,2u)\).

The projective rows \([x_s]\) are 120 distinct points on one
irreducible conic.

## 3. Sufficient closure

Prove that at least one triple \(s_1,s_2,s_3\) satisfies any of the
following equivalent-or-stronger degeneracies.

### 3.1 Common 12-set

\[
\left|I_{s_1}\cup I_{s_2}\cup I_{s_3}\right|\le12.
\tag{3.1}
\]

The blocks are then three facets of one 12-set, and their reciprocal
rows are collinear.

### 3.2 Quadratic-pencil 13-set

Let

\[
Q=I_{s_1}\cup I_{s_2}\cup I_{s_3},
\qquad |Q|\le13,
\]

and

\[
D_r(T)=\prod_{t\in Q\setminus I_{s_r}}(T-t).
\]

Prove that the three degree-at-most-two polynomials \(D_r\) are
linearly dependent. At \(|Q|=13\), this says the three complementary
pairs are fibers of one degree-two rational map.

### 3.3 Direct reciprocal-rank degeneracy

\[
\operatorname{rank}
\left(
\frac{1}{U_{s_r}(\alpha_j)}
\right)_{\substack{1\le r\le3\\1\le j\le12}}
\le2.
\tag{3.2}
\]

Equivalently, for some nonzero \((A_1,A_2,A_3)\),

\[
A_1U_{s_2}U_{s_3}
+A_2U_{s_1}U_{s_3}
+A_3U_{s_1}U_{s_2}
\]

is divisible by the source locator \(A(T)\).

Any of (3.1)--(3.2) gives three distinct collinear points on the
irreducible conic, a contradiction. Therefore it proves PDCEC.

## 4. Additional exact structure

The forcing argument may consume:

1. the complementary \(1\)-\((60,49,98)\) design carried by \(W_1\);
2. the exact grid partition: 1320 incidences on \(M\), 5880 on
   \(W_1\);
3. the nonzero vertex values
   \[
   W_1(t,\lambda_s)
   =
   \frac{V_{\rm act}'(t)B(\lambda_s)^5}
        {\gamma_sU_s'(t)};
   \]
4. the per-block derivative invariant
   \[
   \frac{c_t'(\lambda_s)V_{\rm act}'(t)}
        {A(t)^5U_s'(t)}
   \quad\text{is independent of }t\in I_s;
   \]
5. the component law \((u,2u)\), with no \((1,1)\) component;
6. for a \((1,2)\) component, the descent
   \[
   g=f\circ\psi
   \]
   and the deck-asymmetry inclusion
   \[
   \operatorname{fib}_{H_0}(\lambda_s)
   \subseteq I_s\setminus I_{\iota(s)}.
   \]
7. in its live deck-asymmetric branch, a non-diagonal component of
   the self-correspondence \(f(T)=f(w)\) of even bidegree
   \[
   (d,d),\qquad d\in\{2,4,\ldots,20\},
   \]
   whose \(w\)-projection has the same quadratic lift.
8. a single integer \(Q\in\{6,\ldots,10\}\), independent of the
   deck pair, such that
   \[
   |I_s\cap I_{\iota(s)}|=11-Q,
   \qquad
   |I_s\setminus I_{\iota(s)}|
   =
   |I_{\iota(s)}\setminus I_s|
   =Q.
   \]
9. exclusion of \(Q=1\): its two quadratic graphs force a
   factorization
   \[
   f=F\circ r_n,
   \qquad
   n\in\{2,3,4,6,12\},
   \]
   through a degree-\(n\) Dickson/Chebyshev quotient. The coordinate
   divisors then become fibers of one degree-two map and span at
   most a pencil, contradicting the required rank-three conic
   coordinates.
10. exclusion of \(Q=2,3,4\): the outgoing component union has
    bidegree \((Q,2Q)\), its deck conjugate is coprime to it, and the
    twelve source fibers force more than their Bézout intersection
    number \(4Q^2\). At \(Q=5\), equality forces both deck
     ramification points to be double coordinate poles and fixes the
     complete degree-100 source resultant.
11. exclusion of \(Q=5\): the equality packet descends to a
    \((5,5)\)-by-\((3,4)\) resultant. The exact source derivative at
    either deck-fixed double pole makes the outgoing odd part
    proportional to its fixed fiber. Its two forced source factors
    make that proportionality zero, producing double fixed roots
    where the equality packet requires simple roots.

## 5. Promising strategies

### 5.1 Rank-three matroid forcing

The 120 reciprocal rows form a rank-three realization with highly
restricted denominators. Use its nine-dimensional relation space to
show that one \(3\times3\) minor forced by the design must vanish.
An arbitrary rank-three realization is insufficient; the proof must
use the locator-product form.

### 5.2 Derivative-cycle forcing

Multiply the vertex identities around short alternating cycles of the
incidence bipartite graph. The block and root scalars cancel, leaving
cross-ratio constraints on active roots and parameters. Show that one
cycle forces a quadratic-pencil triple.

### 5.3 Component partition forcing

Each irreducible component of \(M\) owns exactly \(u\) roots in every
block and \(2u\) blocks through every active root. Because
\(\sum u=11\), an odd-\(u\) component exists. Classify the smallest
odd component and use its induced subdesign to force a degenerate
triple.

### 5.4 Degree-two descent closure

In the \((1,2)\) branch, exploit the involution pairing of all 120
parameters and the strict block distinctness to amplify
\[
\operatorname{fib}_{H_0}(\lambda_s)
\subseteq I_s\setminus I_{\iota(s)}.
\]
The target is a short orbit or component intersection forcing three
reciprocal rows into rank two.

Equivalently, classify low-subdegree factors of
\[
\frac{V_{\rm act}(T)A(w)^5-V_{\rm act}(w)A(T)^5}{T-w}
\]
that have even bidegree at most 20 and whose second projection admits
the prescribed quadratic lift. Excluding all such factors closes the
entire \((1,2)\) component branch.

The uniform deck-pair ledger and coordinate-pencil argument close
the first subcase completely:
\[
\boxed{Q=1\text{ is impossible}.}
\]
Thus every remaining degree-two descent has
\[
6\le Q\le10,
\qquad
1\le |I_s\cap I_{\iota(s)}|\le5.
\]
The next useful refinement is to classify the outgoing component
partition
\[
Q=u_1+\cdots+u_r.
\]
If some \(u_i=1\), the same two-graph argument supplies the Dickson
factorization and shows that neither deck-fixed point is a pole. If
every \(u_i\ge2\), there are at most five outgoing components, each
inducing an even self-correspondence subdegree at most 20.

The sharp first remaining case is \(Q=6\). Its outgoing curve and
deck conjugate have intersection number \(144\). If \(s\) coordinate
quadratics are deck-invariant, the source fibers, fixed sections, and
fixed-pole derivative force at least
\[
132+2s
\]
intersections, leaving residual slack at most \(12-2s\). On the
involution quotient, every invariant coordinate label factors the odd
form, and the off-source resultant has degree at most \(6-s\). In a
graph branch one such residual quotient point is already consumed, so
\(s\le5\). In a graph-free branch the component partition is one of
\[
\boxed{6,\qquad4+2,\qquad3+3,\qquad2+2+2.}
\]
The quotient-pole incidence theorem eliminates
\(s=2,3,4,5\), and the \(s=1\) coordinate divisor cannot be fixed.
Thus only

\[
\boxed{s=0,\qquad s=1\text{ nonfixed},\qquad s=6}
\]

remain. A graph component is possible only for \(s=0\) or \(s=1\)
and has no fixed coordinate pole. At \(s=6\), the horizontal
degree-five factor is squarefree and supported on five of the twelve
source poles. Moreover, the two disjoint degree-six difference
locators of every deck-conjugate block pair span a line through the
same fixed six-source locator \(P_{\mathcal I}\). The five horizontal
source poles lie in the intersection of the invariant coordinate
labels and the six source fibers consumed by those coordinates, so
those two six-sets differ in at most one label.

Classifying these three source-labelled packets, or showing they are
incompatible with source-coordinate rank three, is now the smallest
remaining subtarget. Its complete interface is printed in

```text
target/pole_disjoint_conic_q6_intersection_target.md
```

### 5.5 Fixed-root Chow geometry

Classify degree-eleven rational curves in the fixed-root split-form
locus after imposing rank three and the exact complementary identity.
Only a theorem retaining the source evaluations and selected-record
labels is useful.

## 6. Guardrails

The cyclic \(1\)-\((60,11,22)\) design from the parent target has no
common-12-set triple and survives every design-only condition above.
Therefore pure incidence counting cannot prove this target.

The following are also insufficient:

* finding an unrooted planted template;
* treating the reciprocal rows as an arbitrary rank-three matrix;
* assuming pair codegrees or a 2-design property not proved upstream;
* assuming \(M\) irreducible;
* using the \((1,2)\) descent without closing its deck-asymmetric
  component branch.

## 7. Valid completion

A valid proof must derive a concrete triple from the actual endpoint
identity or prove a different direct contradiction. It must not infer
PDCEC from finite experiments.

A valid falsifier must realize the complete endpoint identity,
pairwise-disjoint quadratic poles, squarefree actual fibers,
rank-three reciprocal rows, component law, and every derivative
identity while keeping all \(\binom{120}{3}\) reciprocal-row triples
of rank three.

## 8. Downstream effect

Proving this target eliminates the principal irreducible-conic
endpoint. The remaining geometric ledger begins with the reducible
two-line owner/payment branch, the two \(a=14\) conic boundaries,
cubic selected-record emission, and circuits of support at least
\(3k+1\).
