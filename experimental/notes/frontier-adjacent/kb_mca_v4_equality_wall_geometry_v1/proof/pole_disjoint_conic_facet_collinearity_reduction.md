# Pole-Disjoint Conic Facet-Collinearity Reduction

## Reader map

### Proof spine

1. The inherited endpoint identity is divided by the nine inactive roots
   (Theorem 3.1).
2. Source and active roots separate, the reciprocal block-coordinate map is
   an embedded conic, and all 120 blocks are distinct (Lemmas 4.1--4.3 and
   Theorem 4.4).
3. Three blocks in one 12-set would give three collinear points on that conic
   (Theorem 5.1), replacing the older two-template target by a one-triangle
   exclusion.
4. Every correspondence component has bidegree \((u,2u)\), and the exact
   grid-vertex formula is available (Theorems 7.1 and 8.1).
5. The quadratic-section descent eliminates \(Q=1\) and \(Q=5\)
   (Corollary 9.12 and Theorem 9.17).
6. The first open case compresses to \(Q=6\), then to \(s=6\), and finally
   to the fixed split-pencil star with the source-facet and component-color
   ledgers (Corollaries 9.20--9.28).
7. Guardrails 9.29--9.31 state exactly why the remaining normalized
   `P3+C3` common-signature family is not paid in this note.

### Assumption ledger

| Input | Exact inherited hypothesis | First use |
| --- | --- | --- |
| Row | \(a=12\), \(R=69\), \(k=59\), \(m=120\) | Section 1 |
| Coordinates | twelve pairwise pole-disjoint quadratics spanning \(H^0(\mathcal O(2))\) | Lemma 4.3 |
| Endpoint | \(M\) has bidegree \((11,22)\) and no vertical or horizontal component | Theorem 3.1 |
| Fibers | 120 distinct non-pole parameters with squarefree split 11-root fibers | Sections 2--5 |
| Design | exact \(1\)-\((60,11,22)\) active-root design | Theorems 5.1 and 8.1 |
| Divisor identity | equation (1.1), with the printed inactive-root locator | Theorem 3.1 |
| Parent normalization | fixed-domain rank-16 and source-fiber reductions | Section 1 status |

No global slope census, owner payment, or KoalaBear endpoint is an input or a
conclusion.

### Dependency DAG

```text
parent fixed-domain/source-fiber normalization
  -> Theorem 3.1
  -> Lemmas 4.1--4.3 -> Theorem 4.4
  -> Theorems 5.1--5.2
  -> Theorem 7.1 -> Theorem 8.1
  -> Theorem 9.2 -> Theorem 9.3
  -> Corollaries 9.7--9.12       [Q=1 closed]
  -> Theorems 9.13--9.19         [Q=5 closed]
  -> Corollaries 9.20--9.28      [Q=6,u=2 normalized residue]
  -> Guardrails 9.29--9.31       [P3+C3 child target]
```

### Theorem index

| Range | Content |
| --- | --- |
| 3.1 | inactive-root division and exact specialized quotients |
| 4.1--4.4 | separation, reciprocal coordinates, embedded conic, block distinctness |
| 5.1--6.3 | facet-triple exclusion and sharpened emission target |
| 7.1--8.1 | component bidegrees and grid-vertex formula |
| 9.2--9.12 | quadratic descent and complete \(Q=1\) exclusion |
| 9.13--9.19 | outgoing-conjugate ledger and complete \(Q=5\) exclusion |
| 9.20--9.28 | exact \(Q=6,u=2\) split-pencil, source-facet, and edge-color reduction |
| 9.29--9.31 | nonclaims and the precise remaining signature wall |

## 1. Status and role

This note advances the open PDCEC target

```text
target/pole_disjoint_conic_endpoint_classification_target.md
```

originally formulated in the v17 review packet and integrated here
into `koalabear_owner_partition_bridge_external_review_2026-07-26_v18`.
All data of Sections 2--4 of that target are assumed: the principal
row

\[
a=12,\qquad R=69,\qquad k=59,\qquad m=2k+2=120,
\]

the twelve pairwise pole-disjoint coordinate quadratics
\(z_i\in H^0(\mathbf P^1_\lambda,\mathcal O(2))\) spanning
\(H^0(\mathcal O(2))\), the products \(B=\prod_iz_i\) and
\(h_i=B/z_i\), the twelve distinct sources \(\alpha_j\) with
\(A(T)=\prod_j(T-\alpha_j)\) and Lagrange basis \(L_i\), the weights
\(\kappa_i\ne0\), the endpoint curve

\[
M(T,\lambda)=\sum_{i=1}^{12}\kappa_iL_i(T)h_i(\lambda)
\]

of bidegree \((11,22)\) with no vertical or horizontal component, the
69 selected roots \(\mathcal T\), the 120 distinct parameters
\(\lambda_s\) avoiding every coordinate pole, the squarefree split
fibers \(M(T,\lambda_s)=\gamma_sU_s(T)\) with
\(U_s=\prod_{t\in I_s}(T-t)\), the identity

\[
V(T)B(\lambda)^5-Q_9(T)L(\lambda)A(T)^5=M(T,\lambda)W(T,\lambda),
\tag{1.1}
\]

the exact \(1\)-\((60,11,22)\) design on
\(\mathcal T_{\rm act}\), and the inactive-root locator
\(Q_9=c\prod_{t\in\mathcal T_{\rm inact}}(T-t)\).

This note proves, unconditionally for every such packet:

1. the inactive roots divide out of (1.1) exactly, leaving a
   two-term spectral identity with constant remainder;
2. no source is an active root, and the 120 blocks \(I_s\) are
   pairwise distinct;
3. the actual conic point at \(\lambda_s\) has explicit reciprocal
   block coordinates
   \(\bigl[\kappa_j/U_s(\alpha_j)\bigr]_{j=1,\dots,12}\);
4. **facet collinearity**: any three blocks contained in one 12-set
   force three collinear points on the conic, hence are impossible on
   an irreducible conic;
5. consequently the expected two-template decomposition of the
   target's Section 6 is itself irreducible-infeasible, so a proof
   deriving that decomposition already proves the exclusion form:
   a single derived 12-set triple (or any collinear parameter triple)
   is a sufficient closure of PDCEC;
6. every irreducible component of the endpoint correspondence has
   bidegree \((u,2u)\);
7. the exact grid vertex formula requested by Section 9.2 of the
   target;
8. a descent dichotomy for bidegree-\((1,2)\) components: such a
   component forces \(g=f\circ\psi\) for a degree-two rational map
   \(\psi\) and either contradicts block distinctness or forces a
   deck-asymmetric component of \(\mathcal D\) whose conjugate lies
   in the complementary factor \(V(W_1)\).

Item 4 is the engine that Section 9.5 of the target postulated but
did not construct. Items 2--5 together replace the two-template
expectation by a strictly sharper one-triangle target.

```text
PDCEC STATUS AFTER THIS NOTE: OPEN, SHARPENED
ACTIVE OWNER PAYMENT: NONE
NEW PAYMENT BOOKED: NONE
```

## 2. Notation

Write

\[
V_{\rm act}(T)=\prod_{t\in\mathcal T_{\rm act}}(T-t),
\qquad
V_{\rm inact}(T)=\prod_{t\in\mathcal T_{\rm inact}}(T-t),
\qquad
V=V_{\rm act}V_{\rm inact},
\]

so \(Q_9=c\,V_{\rm inact}\) with \(c\ne0\). For an active root \(t\)
let

\[
c_t(\lambda)=M(t,\lambda)
=\gamma_t\prod_{s\,:\,t\in I_s}(\lambda-\lambda_s),
\qquad
\bar c_t(\lambda)=\prod_{s\,:\,t\notin I_s}(\lambda-\lambda_s).
\tag{2.1}
\]

The first equality in (2.1) holds because \(c_t\) has degree at most
22 and vanishes at the 22 distinct parameters of the blocks
containing \(t\); if its leading coefficient vanished, \(c_t\) would
have 22 roots in degree at most 21 and be identically zero, giving a
vertical component. Hence \(\deg c_t=22\), \(\gamma_t\ne0\), and
\(c_t\) is squarefree. For a block \(s\) let

\[
C_s(T)=\frac{V_{\rm act}(T)}{U_s(T)}
=\prod_{t\in\mathcal T_{\rm act}\setminus I_s}(T-t),
\qquad \deg C_s=49.
\]

Define the two spectral maps

\[
f(T)=\frac{V_{\rm act}(T)}{A(T)^5},
\qquad
g(\lambda)=c\,\frac{L(\lambda)}{B(\lambda)^5},
\tag{2.2}
\]

of degrees 60 and 120, and

\[
G(T,\lambda)
=V_{\rm act}(T)B(\lambda)^5-c\,L(\lambda)A(T)^5,
\tag{2.3}
\]

of bidegree \((60,120)\), so that \(V(G)\) is the closure of
\(\{f(T)=g(\lambda)\}\).

## 3. Exact inactive-root division

### Theorem 3.1

There is a bihomogeneous \(W_1\) of bidegree \((49,98)\) with

\[
\boxed{
V_{\rm act}(T)B(\lambda)^5-c\,L(\lambda)A(T)^5
=M(T,\lambda)\,W_1(T,\lambda),
}
\tag{3.1}
\]

and \(W=(Q_9/c)\,W_1\). Moreover:

\[
W_1(T,\lambda_s)=\frac{B(\lambda_s)^5}{\gamma_s}\,C_s(T)
\qquad(1\le s\le120),
\tag{3.2}
\]

\[
W_1(t,\lambda)=-\frac{c\,A(t)^5}{\gamma_t}\,\bar c_t(\lambda)
\qquad(t\in\mathcal T_{\rm act}),
\tag{3.3}
\]

\[
W_1(\alpha_j,\lambda)
=\frac{V_{\rm act}(\alpha_j)}{\kappa_j}\,B(\lambda)^4z_j(\lambda)
\qquad(1\le j\le12).
\tag{3.4}
\]

### Proof

Fix an inactive root \(t_0\). Then \(V(t_0)=0\) and \(Q_9(t_0)=0\),
so (1.1) gives \(M(t_0,\lambda)W(t_0,\lambda)\equiv0\). Since \(M\)
has no vertical component, \(M(t_0,\lambda)\not\equiv0\), hence
\(W(t_0,\lambda)\equiv0\) and \((T-t_0)\mid W\). The nine inactive
roots are distinct, so \(V_{\rm inact}\mid W\); write
\(W=V_{\rm inact}W_1\). Substituting \(V=V_{\rm act}V_{\rm inact}\)
and \(Q_9=cV_{\rm inact}\) into (1.1) and cancelling the nonzero
polynomial \(V_{\rm inact}\) gives (3.1). Bidegrees:
\((69,120)-(9,0)-(11,22)=(49,98)\).

At \(\lambda=\lambda_s\): \(L(\lambda_s)=0\) and
\(M(T,\lambda_s)=\gamma_sU_s\), so (3.1) reads
\(V_{\rm act}B(\lambda_s)^5=\gamma_sU_sW_1(T,\lambda_s)\), which is
(3.2); note \(B(\lambda_s)\ne0\) because the actual parameters avoid
every coordinate pole.

At \(T=t\in\mathcal T_{\rm act}\): \(V_{\rm act}(t)=0\), so
\(-cL(\lambda)A(t)^5=c_t(\lambda)W_1(t,\lambda)\); by (2.1),
\(L=\gamma_t^{-1}c_t\bar c_t\), giving (3.3).

At \(T=\alpha_j\): \(A(\alpha_j)=0\) and
\(M(\alpha_j,\lambda)=\kappa_jh_j(\lambda)\) since
\(L_i(\alpha_j)=\delta_{ij}\), so
\(V_{\rm act}(\alpha_j)B^5=\kappa_jh_jW_1(\alpha_j,\lambda)\); with
\(h_j=B/z_j\) this is (3.4). \(\square\)

### Remark 3.2

Equation (3.1) says the endpoint correspondence
\(\mathcal D=V(M)\) and the complementary correspondence
\(V(W_1)\) are complementary unions of components of the fiber
product \(\{f=g\}\). Equation (3.2) says the vertical fibers of
\(W_1\) at the actual parameters are exactly the complementary
locators; (3.3) says its horizontal fibers at active roots are
exactly the complementary parameter products; so \(V(W_1)\) carries
the complementary \(1\)-\((60,49,98)\) design. Equation (3.4) shows
each coordinate quadratic \(z_j\) reappears, once, as the deviation
of the source fiber of \(W_1\) from \(B^4\).

## 4. Separation and block distinctness

### Lemma 4.1

No source \(\alpha_j\) is an active root. Consequently
\(U_s(\alpha_j)\ne0\) and \(C_s(\alpha_j)\ne0\) for all \(s,j\), and
\(A(t)\ne0\) for every \(t\in\mathcal T_{\rm act}\).

### Proof

If \(\alpha_j\in\mathcal T_{\rm act}\), its codeword is
\(c_{\alpha_j}=M(\alpha_j,\cdot)=\kappa_jh_j\), whose root divisor is
\(\sum_{i\ne j}\operatorname{div}(z_i)\), supported on coordinate
poles. But the codeword of an active root vanishes at 22 actual
parameters, and the parameters avoid every coordinate pole.
Contradiction. (An inactive root may coincide with a source; this is
not excluded and is not needed.) \(\square\)

### Lemma 4.2 (reciprocal block coordinates)

For every \(s\) and every \(j\),

\[
\kappa_j\,h_j(\lambda_s)=\gamma_s\,U_s(\alpha_j),
\tag{4.1}
\]

and therefore the actual conic point
\(p_s=[z_1(\lambda_s):\cdots:z_{12}(\lambda_s)]\in\mathbf P^{11}\)
satisfies

\[
\boxed{
p_s=\Bigl[\frac{\kappa_1}{U_s(\alpha_1)}:\cdots:
\frac{\kappa_{12}}{U_s(\alpha_{12})}\Bigr].
}
\tag{4.2}
\]

### Proof

Evaluate \(M\) at \((\alpha_j,\lambda_s)\) in both presentations:
\(M(\alpha_j,\lambda)=\kappa_jh_j(\lambda)\) and
\(M(T,\lambda_s)=\gamma_sU_s(T)\). This is (4.1). Then

\[
z_j(\lambda_s)=\frac{B(\lambda_s)}{h_j(\lambda_s)}
=\frac{B(\lambda_s)\,\kappa_j}{\gamma_s\,U_s(\alpha_j)},
\]

and \(B(\lambda_s)/\gamma_s\ne0\) is a common factor. All
denominators are nonzero by Lemma 4.1 and pole avoidance. \(\square\)

### Lemma 4.3 (embedded conic)

The morphism \(p:\mathbf P^1_\lambda\to\mathbf P^{11}\),
\(\lambda\mapsto[z_1(\lambda):\cdots:z_{12}(\lambda)]\), is a closed
embedding onto an irreducible conic \(C\) spanning a plane
\(\Pi\subset\mathbf P^{11}\). In particular \(p\) is injective, so
the 120 points \(p_s\) are pairwise distinct.

### Proof

Choose a basis \(q_0,q_1,q_2\) of \(H^0(\mathcal O(2))\) and write
\(z_i=\sum_m c_{im}q_m\). Then \(p=\ell\circ v\), where
\(v:\lambda\mapsto[q_0:q_1:q_2]\) is the degree-two Veronese
embedding of \(\mathbf P^1\) as a smooth conic in \(\mathbf P^2\),
and \(\ell:\mathbf P^2\to\mathbf P^{11}\) is the linear map with
matrix \((c_{im})\). Since the \(z_i\) span \(H^0(\mathcal O(2))\),
the matrix has rank 3, so \(\ell\) is an everywhere-defined linear
embedding. \(\square\)

### Theorem 4.4 (block distinctness)

The 120 blocks \(I_s\) are pairwise distinct.

### Proof

If \(I_s=I_{s'}\) then \(U_s=U_{s'}\), so \(p_s=p_{s'}\) by (4.2),
so \(\lambda_s=\lambda_{s'}\) by Lemma 4.3, so \(s=s'\). \(\square\)

### Remark 4.5

The target's Section 4 asserts only the \(1\)-design (4.3)--(4.5);
distinctness of the blocks was previously a feature of the
design-only guardrail, not a proved property of the endpoint.
Theorem 4.4 shows every actual endpoint design has 120 distinct
blocks, as the guardrail anticipated.

### Remark 4.6 (rank three)

The \(120\times12\) matrix
\(X=\bigl(\kappa_j/U_s(\alpha_j)\bigr)_{s,j}\) has rank exactly 3:
its rows are the coordinate vectors of the \(p_s\), the evaluation
matrix \((z_j(\lambda_s))\) is column-equivalent to the evaluation of
the 3-dimensional space \(H^0(\mathcal O(2))\) at 120 distinct
points, and evaluation of a nonzero quadratic at three or more
distinct points cannot vanish identically. Equivalently: there is a
9-dimensional space of vectors \(\nu\in F^{12}\) with
\(\sum_j\nu_j/U_s(\alpha_j)=0\) for all \(s\), namely the pullback of
the linear relation space of the twelve quadratics \(z_j\). This
reformulates the plane condition entirely in terms of blocks,
sources, and weights; it is recorded here because any future forcing
argument may consume it without reconstructing the conic.

## 5. Facet collinearity

### Theorem 5.1 (facet-triple exclusion)

Let \(s_1,s_2,s_3\) be three distinct block indices with

\[
\bigl|I_{s_1}\cup I_{s_2}\cup I_{s_3}\bigr|\le12 .
\]

Then the three conic points \(p_{s_1},p_{s_2},p_{s_3}\) are distinct
and collinear in \(\mathbf P^{11}\). Since three distinct points of
an irreducible conic are never collinear, no actual pole-disjoint
irreducible-conic endpoint packet contains three blocks lying in a
common 12-set.

### Proof

Distinct 11-sets have union at least 12, so
\(P=I_{s_1}\cup I_{s_2}\cup I_{s_3}\) has exactly 12 elements, all
of them active roots. Each \(I_{s_r}\) is an 11-subset of \(P\), so
\(I_{s_r}=P\setminus\{t_r\}\), and the \(t_r\) are pairwise distinct
because the blocks are distinct (Theorem 4.4). In particular the
three blocks are pairwise 10-intersecting. Set

\[
(A_1,A_2,A_3)=(t_2-t_3,\;t_3-t_1,\;t_1-t_2)\ne(0,0,0),
\]

so \(A_1+A_2+A_3=0\) and \(A_1t_1+A_2t_2+A_3t_3=0\). Write
\(U_P=\prod_{t\in P}(T-t)\); then
\(U_{s_r}=U_P/(T-t_r)\), and \(U_P(\alpha_j)\ne0\) for every source
\(\alpha_j\) because every element of \(P\) is an active root, hence
not a source (Lemma 4.1). For every \(j\):

\[
\sum_{r=1}^3\frac{A_r}{U_{s_r}(\alpha_j)}
=\frac{\sum_{r=1}^3A_r(\alpha_j-t_r)}{U_P(\alpha_j)}
=\frac{\alpha_j\sum_rA_r-\sum_rA_rt_r}{U_P(\alpha_j)}
=0 .
\]

Multiplying coordinatewise by the fixed nonzero scalars \(\kappa_j\)
preserves the relation, so by (4.2) the \(3\times12\) coordinate
matrix of \(p_{s_1},p_{s_2},p_{s_3}\) has the left kernel vector
\((A_1,A_2,A_3)\) and rank at most 2. The three points are distinct
(Lemma 4.3), so they span a line \(\Lambda\subset\mathbf P^{11}\).
All three lie on \(C\). A line meets an irreducible conic in at most
two points, for otherwise the line would be a component of the
degree-two curve \(C\), contradicting irreducibility. \(\square\)

### Theorem 5.2 (13-set pencil refinement)

Let \(s_1,s_2,s_3\) be distinct blocks with
\(|Q|\le13\) for \(Q=I_{s_1}\cup I_{s_2}\cup I_{s_3}\), and let
\(D_r(T)=\prod_{t\in Q\setminus I_{s_r}}(T-t)\) be the complementary
factors (each of degree \(|Q|-11\le2\)). If the three polynomials
\(D_1,D_2,D_3\) are linearly dependent, the same conclusion holds:
the packet cannot exist on an irreducible conic. For \(|Q|=13\) the
dependence condition says exactly that the three complementary pairs
\(Q\setminus I_{s_r}\) are three fibers of a single degree-two
rational map (equivalently, are cut by a pencil of quadratics;
writing \(Q\setminus I_{s_r}=\{a_r,b_r\}\), equivalently the three
points \((a_r+b_r,\,a_rb_r)\) are collinear in the affine plane;
the equal-sum family \(a_1+b_1=a_2+b_2=a_3+b_3\) is the parabolic
instance).

### Proof

Take \(\sum_rA_rD_r\equiv0\) with \((A_r)\ne0\). If some \(A_r=0\),
the remaining two \(D\)'s are proportional, hence equal as monic
polynomials of equal degree, hence \(I_{s_r}\) coincide for two
indices, contradicting distinctness; so all \(A_r\ne0\). Then for
every \(j\),

\[
\sum_r\frac{A_r}{U_{s_r}(\alpha_j)}
=\frac{\sum_rA_rD_r(\alpha_j)}{U_Q(\alpha_j)}=0,
\]

with \(U_Q=\prod_{t\in Q}(T-t)\), whose values at sources are
nonzero because every element of \(Q\) is active; the proof
concludes as in Theorem 5.1. Theorem 5.1 is the case \(|Q|=12\), where the \(D_r\)
are three linear polynomials, hence automatically dependent.
\(\square\)

### Remark 5.3 (general collinearity ledger)

By (4.2), for any three distinct blocks the following are
equivalent:

1. \(p_{s_1},p_{s_2},p_{s_3}\) are collinear;
2. the \(3\times12\) matrix \((1/U_{s_r}(\alpha_j))\) has rank
   \(\le2\);
3. some nontrivial combination
   \(A_1U_{s_2}U_{s_3}+A_2U_{s_1}U_{s_3}+A_3U_{s_1}U_{s_2}\)
   (degree \(\le33\)) is divisible by \(A(T)\).

Every one of the \(\binom{120}{3}=280{,}840\) triples of an actual
irreducible packet must therefore have rank exactly 3 in form 2.
Theorems 5.1 and 5.2 isolate the triples whose degeneracy is forced
combinatorially (5.1) or by one printed determinant (5.2); all
remaining triples impose value conditions on
\((\mathcal T_{\rm act},\alpha,\kappa)\) through form 3.

## 6. Collapse of the emission form

### Corollary 6.1 (two-template infeasibility)

A canonical two-template family (target Section 6) contains the
twelve facets of each part \(P_j\); any three of them lie in the
common 12-set \(P_j\). By Theorem 5.1 the actual block family of an
irreducible-conic packet is never a two-template family. More
generally its 10-intersection graph contains no triangle of blocks
with union inside a 12-set; in particular no part of any partition
of \(\mathcal T_{\rm act}\) into 12-sets carries three actual
facets.

### Corollary 6.2 (template emission implies exclusion)

Suppose some argument derives, from the actual packet data
(2.4)--(3.4) of the target, a canonical two-template decomposition
of its own block family. Then the packet does not exist. Hence the
template-emission route inside the irreducible branch collapses to
exclusion: such a derivation is already a contradiction, without
constructing or validating an owner payment. The same-record
owner/payment interface remains relevant in the separate reducible
two-line branch, where Theorem 5.1 does not apply because the conic
contains lines.

### Corollary 6.3 (sharpened target)

PDCEC is implied by the following statement.

> **One-triangle target.** Every configuration satisfying Sections
> 2--4 of the PDCEC target contains three blocks
> \(I_{s_1},I_{s_2},I_{s_3}\) with
> \(|I_{s_1}\cup I_{s_2}\cup I_{s_3}|\le12\), or three blocks
> satisfying the hypothesis of Theorem 5.2, or any triple that is
> degenerate in the sense of Remark 5.3.

This replaces the previous goal of deriving ten complete facet
groups (target Section 9.2) by the derivation of a single degenerate
triple. It also corrects the expectation of target Section 6: for
the irreducible packet the two-template structure is not the
conclusion to be reached; it is one of infinitely many structures
already known to be unreachable. The actual endpoint design, if it
exists, is guardrail-like: 120 distinct blocks and maximum
10-intersection clique at most two, exactly as in the Section 7
cyclic counterexample.

### Remark 6.4 (guardrail sharpening)

The Section 7 cyclic design satisfies every combinatorial condition
proved here (distinct blocks; no three blocks in a 12-set, since a
12-set triple is pairwise 10-intersecting and the design's maximum
10-clique is two). The design-only route cut therefore survives all
results of this note, as it must: Theorems 5.1--5.2 consume the
source-coupled data (4.2), not the design axioms. What the note adds
against the cyclic model is value-level: its many 13-set triples
(consecutive interval translates) each impose, through Theorem 5.2,
one explicit nonvanishing determinant condition on the actual root
values, and every remaining triple imposes the rank-3 condition of
Remark 5.3.

## 7. Component bidegree law

### Theorem 7.1

Every irreducible component \(\mathcal D'\) of
\(\mathcal D=V(M)\) has bidegree \((u',2u')\) for some
\(u'\ge1\). The same holds for every irreducible component of
\(V(W_1)\).

### Proof

Let \((u',v')\) be the bidegree. Over each actual parameter
\(\lambda_s\), the fiber of \(\mathcal D\) is the reduced scheme of
the 11 grid points \((t,\lambda_s)\), \(t\in I_s\), because the
fiber \(\gamma_sU_s\) is squarefree; the fiber of \(\mathcal D'\) is
a degree-\(u'\) subscheme, hence exactly \(u'\) distinct grid
points, and the fibers of distinct components are disjoint there.
Over each active root \(t\), the vertical fiber of \(\mathcal D\) is
the reduced scheme of the 22 points \((t,\lambda_s)\),
\(t\in I_s\), because \(c_t\) is squarefree (Section 2); the
vertical fiber of \(\mathcal D'\) consists of exactly \(v'\) of
them. Counting the marked incidences of \(\mathcal D'\) by rows and
by columns,

\[
120\,u'=\sum_{s}\#\{t\in I_s:(t,\lambda_s)\in\mathcal D'\}
=\sum_{t\in\mathcal T_{\rm act}}
\#\{s:(t,\lambda_s)\in\mathcal D'\}
=60\,v',
\]

so \(v'=2u'\). For \(W_1\), replace (11, 22, blocks) by
(49, 98, complements): the horizontal fibers \(C_s\) are squarefree
of degree 49 with all roots active, and the vertical fibers
\(\bar c_t\) are squarefree of degree 98 with all roots actual, by
(3.2) and (3.3). These exact fibers also exclude vertical and
horizontal components of \(V(W_1)\). A vertical component would
contribute its \(T\)-root to every actual horizontal fiber, although
each such fiber is exactly the 49-root complement \(C_s\). A
horizontal component would contribute its \(\lambda\)-root to every
active vertical fiber, although each such fiber is exactly the
98-root complement \(\bar c_t\). Hence every component of
\(V(W_1)\) has positive bidegrees and owns marked grid incidences;
the same double count gives \(120u'=60v'\).
\(\square\)

### Corollary 7.2

\(\mathcal D\) has no component of bidegree \((1,1)\): no Mobius
graph \(T=\mu(\lambda)\) lies on the endpoint curve. Every component
has even \(T\)-projection degree \(2u'\), and since
\(\sum u'=11\) is odd, at least one component has odd \(u'\).

## 8. Grid vertex formula

### Theorem 8.1

At every actual incidence \((t,\lambda_s)\), \(t\in I_s\):

\[
M_T(t,\lambda_s)=\gamma_s\,U_s'(t)\ne0,
\qquad
M_\lambda(t,\lambda_s)=c_t'(\lambda_s)\ne0,
\]

\[
\boxed{
c_t'(\lambda_s)\,V_{\rm act}'(t)\,B(\lambda_s)^5
=-\,c\,L'(\lambda_s)\,A(t)^5\,\gamma_s\,U_s'(t),
}
\tag{8.1}
\]

and

\[
W_1(t,\lambda_s)
=\frac{V_{\rm act}'(t)\,B(\lambda_s)^5}{\gamma_s\,U_s'(t)}\ne0 .
\tag{8.2}
\]

In particular \(V(W_1)\) passes through no actual incidence of
\(\mathcal D\): the \(60\times120\) grid incidences split exactly,
1320 to \(\mathcal D\) and 5880 to \(V(W_1)\). Consequently
\(\gcd(M,W_1)=1\): a common component would lie on \(\mathcal D\),
own at least one actual incidence by Theorem 7.1, and place a zero
of \(W_1\) there, contradicting (8.2).

### Proof

Differentiate (3.1) in \(T\) and evaluate at \((t,\lambda_s)\).
Since \(V_{\rm act}(t)=0\), \(L(\lambda_s)=0\), \(M(t,\lambda_s)=0\):

\[
V_{\rm act}'(t)B(\lambda_s)^5=M_T(t,\lambda_s)\,W_1(t,\lambda_s).
\]

Differentiate (3.1) in \(\lambda\) and evaluate at the same point:

\[
-\,c\,L'(\lambda_s)A(t)^5=M_\lambda(t,\lambda_s)\,W_1(t,\lambda_s).
\]

All named scalars on the left sides are nonzero: the active roots
are distinct and disjoint from sources, the parameters are distinct
and avoid poles. Hence \(M_T,M_\lambda,W_1\) are all nonzero at the
point, giving (8.2); the two displays give (8.1) after eliminating
\(W_1\). The fiber values are
\(M_T(t,\lambda_s)=\gamma_sU_s'(t)\) and
\(M_\lambda(t,\lambda_s)=c_t'(\lambda_s)\) by (2.1). \(\square\)

### Remark 8.2 (per-block and per-root rigidity)

Equation (8.1) separates:

\[
\frac{c_t'(\lambda_s)\,V_{\rm act}'(t)}{A(t)^5\,U_s'(t)}
=-\,\frac{c\,\gamma_s\,L'(\lambda_s)}{B(\lambda_s)^5}
\quad\text{is independent of }t\in I_s,
\]

\[
\frac{c_t'(\lambda_s)\,B(\lambda_s)^5}
{\gamma_s\,L'(\lambda_s)\,U_s'(t)}
=-\,\frac{c\,A(t)^5}{V_{\rm act}'(t)}
\quad\text{is independent of }s\ni t .
\]

This is the exact first-derivative system that Section 9.2 of the
target requested. It expresses, for each block, the eleven
logarithmic derivatives of the codewords at the block parameter
through the single block polynomial \(U_s\), and dually. Any future
forcing argument for the one-triangle target can consume (8.1)
directly; the identity (3.1) need not be revisited.

## 9. Quadratic-section descent for \((1,2)\)-components

Throughout this section assume \(\mathcal D\) has an irreducible
component of bidegree \((1,2)\), i.e. the graph
\(\{T=\psi(\lambda)\}\) of a degree-two rational map
\(\psi=\psi_n/\psi_d\).

### Lemma 9.1

\(\psi\) maps the parameter set two-to-one onto the active roots,
and the coordinate-pole set into the source set, with

\[
\operatorname{div}\prod_{j=1}^{12}
\bigl(\psi_n-\alpha_j\psi_d\bigr)
=\operatorname{div}B .
\tag{9.1}
\]

Moreover a coordinate pole is a critical point of \(\psi\) exactly
when it is a double root of its coordinate quadratic.

### Proof

For every \(s\), \((\psi(\lambda_s),\lambda_s)\in\mathcal D\), and
the fiber of \(\mathcal D\) over \(\lambda_s\) is \(I_s\times
\{\lambda_s\}\); so \(\psi(\lambda_s)\in I_s\subset\mathcal T_{\rm
act}\). Conversely the graph's vertical fiber over an active root
\(t\) consists of \(\psi^{-1}(t)\) with multiplicity, is contained
in the reduced 22-point vertical fiber of \(\mathcal D\), hence
consists of 2 distinct parameters; ranging over the 60 active roots
this exhausts all 120 parameters. In particular no parameter is a
critical point of \(\psi\).

Over a pole \(\pi\) of multiplicity \(e\in\{1,2\}\) in \(B\), say
\(z_{j_0}(\pi)=0\), the fiber of \(\mathcal D\) is the reduced
divisor of \(M(T,\pi)=\kappa_{j_0}h_{j_0}(\pi)L_{j_0}(T)\), i.e. the
eleven sources other than \(\alpha_{j_0}\); so
\(\psi(\pi)=\alpha_{m}\) for some \(m\ne j_0\). Conversely if
\(\psi(\xi)=\alpha_j\) then \((\alpha_j,\xi)\in\mathcal D\), and the
horizontal fiber of \(\mathcal D\) over \(\alpha_j\) is
\(\operatorname{div}h_j\), supported on poles; so
\(\psi^{-1}(\{\alpha_j\}_j)\) is exactly the pole set, giving the
support statement in (9.1).

For the multiplicities, expand \(0=M(\psi(\lambda),\lambda)\) at
\(\pi\): with \(\psi(\pi)=\alpha_m\),

\[
0=\kappa_mL_m(\psi(\lambda))h_m(\lambda)
+\kappa_{j_0}L_{j_0}(\psi(\lambda))h_{j_0}(\lambda)
+\sum_{i\ne m,j_0}\kappa_iL_i(\psi(\lambda))h_i(\lambda).
\]

Orders of vanishing at \(\pi\): the first term has order exactly
\(e\) (since \(L_m(\alpha_m)\ne0\), \(\operatorname{ord}_\pi
h_m=e\)); the terms \(i\ne m,j_0\) have order at least \(e+1\)
(\(\operatorname{ord}h_i=e\) and \(L_i(\alpha_m)=0\)); the
\(j_0\)-term has order \(\operatorname{ord}_\pi
L_{j_0}(\psi(\lambda))=\operatorname{ord}_\pi(\psi-\alpha_m)\),
which is the local ramification index \(e_\psi(\pi)\)
(\(h_{j_0}(\pi)\ne0\) by pole disjointness). Vanishing of the sum
forces the two lowest orders to agree: \(e_\psi(\pi)=e\). Summing
local multiplicities gives (9.1) exactly. \(\square\)

### Theorem 9.2 (descent)

If \(\mathcal D\) contains a \((1,2)\)-component with map \(\psi\),
then

\[
\boxed{f\circ\psi=g,}
\tag{9.2}
\]

and with
\(\mathfrak F(x,w)=V_{\rm act}(x)A(w)^5-V_{\rm act}(w)A(x)^5\),

\[
G(T,\lambda)=\zeta\cdot\psi_d(\lambda)^{60}\,
\mathfrak F\bigl(T,\psi(\lambda)\bigr),
\qquad \zeta\ne0 .
\tag{9.3}
\]

Hence every component of \(V(G)\) — in particular every component
of \(\mathcal D\) and of \(V(W_1)\) — maps onto a component of the
self-correspondence \(V(\mathfrak F)\) of \(f\) under
\((T,\lambda)\mapsto(T,\psi(\lambda))\).

### Proof

The graph lies on \(V(G)=\{f(T)=g(\lambda)\}\), so
\(f(\psi(\lambda))=g(\lambda)\) identically, which is (9.2). For
(9.3), define the binary forms

\[
\widehat A(\lambda)=\prod_{j=1}^{12}
\bigl(\psi_n-\alpha_j\psi_d\bigr),
\qquad
\widehat V(\lambda)=\prod_{t\in\mathcal T_{\rm act}}
\bigl(\psi_n-t\,\psi_d\bigr),
\]

of degrees 24 and 120, so that

\[
\psi_d^{60}\,\mathfrak F\bigl(T,\psi(\lambda)\bigr)
=V_{\rm act}(T)\,\widehat A(\lambda)^5
-\widehat V(\lambda)\,A(T)^5 .
\]

By (9.1), \(\operatorname{div}\widehat A=\operatorname{div}B\), so
\(\widehat A=\zeta_1B\) with \(\zeta_1\ne0\). By Lemma 9.1 the zero
divisor of \(\widehat V\) is
\(\psi^*\mathcal T_{\rm act}=\sum_s[\lambda_s]\), each parameter
simple because no parameter is critical for \(\psi\); comparing
degrees, \(\widehat V=\zeta_2L\) with \(\zeta_2\ne0\). Composing
(9.2) with these,

\[
g=f\circ\psi=\frac{\widehat V}{\widehat A^5}
=\frac{\zeta_2}{\zeta_1^5}\cdot\frac{L}{B^5},
\qquad\text{so}\qquad
\zeta_2=c\,\zeta_1^5 .
\]

Hence \(\psi_d^{60}\mathfrak F(T,\psi(\lambda))
=\zeta_1^5\bigl(V_{\rm act}B^5-cLA^5\bigr)=\zeta_1^5\,G\), which is
(9.3) with \(\zeta=\zeta_1^{-5}\). The final statement holds because
\(\mathrm{id}\times\psi\) is a finite surjective morphism and, by
(9.3), \(V(G)\) is the set-theoretic preimage of
\(V(\mathfrak F)\), so every component of \(V(G)\) maps onto a
component of \(V(\mathfrak F)\). \(\square\)

### Theorem 9.3 (dichotomy)

Assume a \((1,2)\)-component exists, let \(\iota\) be the deck
involution of \(\psi\), and let
\(\sigma=\mathrm{id}\times\iota\) act on
\(\mathbf P^1_T\times\mathbf P^1_\lambda\). Write
\(\mathcal D=\{T=\psi(\lambda)\}\cup\mathcal D^\circ\). Then:

1. \(V(G)\) is \(\sigma\)-invariant, so \(\sigma\) permutes its
   irreducible components;
2. at least one component \(H_0\) of \(\mathcal D^\circ\) satisfies
   \(\sigma(H_0)\not\subseteq\mathcal D\); for every such component,
   \(\sigma(H_0)\) is a component of \(V(W_1)\), and for every
   conjugate parameter pair
   \((\lambda_s,\lambda_{s'}=\iota(\lambda_s))\):

\[
\operatorname{fib}_{H_0}(\lambda_s)\subseteq I_s\setminus I_{s'} .
\tag{9.4}
\]

### Proof

Since \(\psi\circ\iota=\psi\), equation (9.3) gives
\(G\circ\sigma=(\psi_d\circ\iota)^{60}\psi_d^{-60}\,G\) as rational
functions, so \(\sigma(V(G))=V(G)\), proving 1. Note that \(\iota\)
maps the parameter set to itself: \(\psi(\iota\lambda_s)
=\psi(\lambda_s)\in\mathcal T_{\rm act}\), and by Lemma 9.1 the
\(\psi\)-preimage of the active set is exactly the parameter set.
No parameter is fixed by \(\iota\): a fixed point is a critical
point of \(\psi\), and no parameter is critical.

The graph is \(\sigma\)-invariant. If every component of
\(\mathcal D^\circ\) had \(\sigma\)-image inside \(\mathcal D\),
then \(\sigma\) would permute the components of
\(\mathcal D^\circ\) (the graph is accounted for separately, and
\(\sigma\) is an involution on components), making all of
\(\mathcal D\) \(\sigma\)-invariant. Then for every conjugate pair,
applying \(\sigma\) to the fiber gives
\(I_s=\{x:(x,\lambda_s)\in\mathcal D\}
=\{x:(x,\lambda_{s'})\in\mathcal D\}=I_{s'}\), contradicting
Theorem 4.4 because \(\lambda_s\ne\lambda_{s'}\). This proves the
existence claim in 2.

Let \(H_0\subseteq\mathcal D^\circ\) with
\(\sigma(H_0)\not\subseteq\mathcal D\). Since \(\sigma(H_0)\) is a
component of \(V(G)\) and \(G=MW_1\) with \(\gcd(M,W_1)=1\)
(Theorem 8.1), \(\sigma(H_0)\) is a component of \(V(W_1)\). If
\((x,\lambda_s)\in H_0\) with \(x\in I_s\), then
\((x,\lambda_{s'})\in\sigma(H_0)\subseteq V(W_1)\); by (3.3) the
vertical fiber of \(V(W_1)\) over the active root \(x\) consists
exactly of the parameters whose blocks avoid \(x\), so
\(x\notin I_{s'}\), which is (9.4). \(\square\)

### Remark 9.4

The dichotomy leaves exactly one live sub-branch for
\((1,2)\)-components: \(g=f\circ\psi\), all of \(V(G)\) pulled back
from the self-correspondence of the degree-60 map \(f\), and at
least one conjugate component pair split between \(M\) and \(W_1\)
with the marked-fiber avoidance (9.4). Every other configuration
with a \((1,2)\)-component contradicts block distinctness. This is
recorded as a narrowed open sub-branch, not a closure.

### Corollary 9.5 (bounded self-correspondence lift)

In the live deck-asymmetric branch, the degree-60 map

\[
f(T)=\frac{V_{\rm act}(T)}{A(T)^5}
\]

has a non-diagonal irreducible self-correspondence component
\(H\subset V(\mathfrak F)\) of bidegree

\[
\boxed{(d,d)=(2u,2u)}
\tag{9.5}
\]

for some

\[
\boxed{1\le u\le10,\qquad
d\in\{2,4,\ldots,20\}.}
\tag{9.6}
\]

Moreover the second projection \(H\to\mathbf P^1_w\) factors through
the same degree-two map \(\psi:\mathbf P^1_\lambda\to\mathbf P^1_w\):
on the normalization of \(H\) there is a rational function
\(\lambda\) such that

\[
w=\psi(\lambda),
\qquad
\deg(H\to\mathbf P^1_\lambda)=u.
\tag{9.7}
\]

#### Proof

Choose the component \(H_0\subset\mathcal D^\circ\) supplied by
Theorem 9.3, so \(\sigma(H_0)\ne H_0\) and
\(\sigma(H_0)\subset V(W_1)\). Let \(H\) be its image in
\(V(\mathfrak F)\) under

\[
(T,\lambda)\longmapsto(T,w=\psi(\lambda)).
\]

The component \(H\) is non-diagonal: the pullback of the diagonal
\(T=w\) is exactly the graph \(T=\psi(\lambda)\), already removed
from \(\mathcal D^\circ\).

The base change of \(H\to\mathbf P^1_w\) by the quadratic cover
\(\psi\) contains \(H_0\) and \(\sigma(H_0)\) as distinct conjugate
components. Hence each maps birationally to \(H\); otherwise one
component would already have generic degree two over \(H\), leaving
no degree for its distinct conjugate in the quadratic base change.

Write the bidegree of \(H_0\) as \((u,2u)\), as supplied by
Theorem 7.1. Its projection to the \(T\)-line has degree \(2u\).
Birationality therefore gives degree \(2u\) for the projection
\(H\to\mathbf P^1_T\). Every component of
\(f(T)=f(w)\) has equal two projection degrees: composing either
projection with the degree-60 map \(f\) gives the same map
\(H\to\mathbf P^1\). Thus \(H\) has bidegree \((2u,2u)\).

The components of \(\mathcal D^\circ\) have total first bidegree ten,
so \(1\le u\le10\). Finally, because \(H_0\to H\) is birational, its
\(\lambda\)-coordinate descends to the normalization of \(H\);
there \(w=\psi(\lambda)\). The projection
\(H_0\to\mathbf P^1_\lambda\) has degree \(u\), proving (9.7).
\(\square\)

### Remark 9.6

Corollary 9.5 replaces an unrestricted component problem by a finite
low-subdegree target:

> exclude a non-diagonal self-correspondence of \(f\) having even
> subdegree at most 20 and a quadratic lift of one projection.

This can be attacked through the monodromy subdegrees of \(f\), a
factorization of the residual divided difference
\(\mathfrak F/(T-w)\), or a direct source-pole analysis. No such
classification is claimed here.

### Corollary 9.7 (uniform deck-pair intersection)

Remain in the live deck-asymmetric branch. Partition the irreducible
components of \(\mathcal D^\circ\) into

\[
\mathscr C_{\rm in}
=
\{H:\sigma(H)\subseteq\mathcal D\},
\qquad
\mathscr C_{\rm out}
=
\{H:\sigma(H)\subseteq V(W_1)\}.
\]

If \(H\) has bidegree \((u_H,2u_H)\), put

\[
P=\sum_{H\in\mathscr C_{\rm in}}u_H,
\qquad
Q=\sum_{H\in\mathscr C_{\rm out}}u_H.
\]

Then

\[
\boxed{P+Q=10,\qquad 1\le Q\le10}
\tag{9.8}
\]

and every conjugate parameter pair
\(\lambda_{s'}=\iota(\lambda_s)\) satisfies the exact identities

\[
\boxed{
|I_s\cap I_{s'}|=1+P=11-Q,
\qquad
|I_s\setminus I_{s'}|
=
|I_{s'}\setminus I_s|
=Q.}
\tag{9.9}
\]

#### Proof

The non-graph components of \(\mathcal D\) have total first
bidegree ten, so \(P+Q=10\). Theorem 9.3 supplies at least one
component in \(\mathscr C_{\rm out}\), hence \(Q\ge1\).

The graph contributes the common root
\(T=\psi(\lambda_s)=\psi(\lambda_{s'})\). The union of the
components in \(\mathscr C_{\rm in}\) is \(\sigma\)-stable:
\(\sigma\) is an involution and permutes those components. Its two
fibers over \(\lambda_s,\lambda_{s'}\) therefore give the same
\(P\) active roots.

If \(H\in\mathscr C_{\rm out}\), applying \(\sigma\) sends every
root of its \(\lambda_s\)-fiber to a root of \(W_1\) over
\(\lambda_{s'}\). By (3.3), that root is outside \(I_{s'}\).
The same argument with \(s,s'\) reversed gives \(Q\) roots in each
one-sided difference. Finally, the selected fibers of
\(\mathcal D\) are the reduced degree-eleven locators \(U_s\).
Thus the graph and the component fibers partition each \(I_s\)
without multiplicity, and the displayed counts are exact.
\(\square\)

### Corollary 9.8 (paired facets at \(Q=1\))

If \(Q=1\), then every deck pair consists of two distinct
eleven-subsets with ten common roots. Equivalently,

\[
|I_s\cup I_{\iota(s)}|=12,
\]

so the pair forms two distinct facets of its common twelve-set.

This does not force a third facet by incidence counting alone. It
does reduce the one-triangle target in this branch to showing that
one of these 60 canonical twelve-sets contains a third block, or
that the source-coupled derivative identities already force a
rank-two reciprocal-row triple.

### Theorem 9.9 (the \(Q=1\) dihedral factor)

Assume \(Q=1\). Then, after extending scalars to an algebraic
closure, there are:

* a degree
  \[
  n\in\boxed{\{2,3,4,6,12\}},
  \tag{9.10}
  \]
* a degree-\(n\) Dickson/Chebyshev quotient
  \(r:\mathbf P^1\to\mathbf P^1\), and
* a rational map \(F\) of degree \(60/n\),

such that

\[
\boxed{f=F\circ r.}
\tag{9.11}
\]

Every pole of \(F\) has order five and avoids the branch values of
\(r\). There are exactly \(12/n\) such poles. Consequently the
twelve source points of \(f\) are a disjoint union of \(12/n\)
generic \(r\)-fibers of size \(n\). Likewise the sixty active zeros
are a disjoint union of \(60/n\) generic \(r\)-fibers.

#### Proof

By (9.8), the only component of
\(\mathscr C_{\rm out}\) has first degree one. It is therefore a
second graph

\[
T=\phi(\lambda)
\]

for a separable degree-two rational map \(\phi\), distinct from the
graph \(T=\psi(\lambda)\). Both graphs lie on \(V(G)\), so

\[
f\circ\phi=g=f\circ\psi.
\tag{9.12}
\]

Let \(a\) and \(b\) be the deck involutions of \(\phi\) and
\(\psi\), respectively. They are distinct. Indeed, if \(a=b\),
then \(\phi=\mu\circ\psi\) for a Mobius transformation \(\mu\).
The graph of \(\phi\) would then be invariant under the deck
involution \(b\), contrary to its membership in
\(\mathscr C_{\rm out}\).

The rational function in (9.12), of degree \(120\), is invariant
under \(a\) and \(b\). Its deck group is finite, so
\(\langle a,b\rangle\) is a finite dihedral group \(D_n\) of order
\(2n\), where \(n\ge2\). Let

\[
q:\mathbf P^1_\lambda\longrightarrow\mathbf P^1_\lambda/D_n
\]

be the quotient. Since \(\phi\) is the quotient by the reflection
\(\langle a\rangle\), \(q=r\circ\phi\) for a degree-\(n\) map
\(r\). Equation (9.12) descends to \(f=F\circ r\). Also
\(2n\mid120\), so \(n\mid60\).

This quotient is explicitly Dickson/Chebyshev. In a coordinate in
which the rotation \(ab\) is \(z\mapsto\zeta z\) and \(a\) is
\(z\mapsto z^{-1}\), the reflection quotient is
\(x=z+z^{-1}\), the full dihedral quotient is
\(y=z^n+z^{-n}\), and \(y=D_n(x)\) for the degree-\(n\)
Dickson polynomial. Thus \(r\) has two finite branch fibers with
ramification index two and one point over infinity with index \(n\).

The pole divisor of \(f\) consists of the twelve source points, all
with multiplicity five. If a pole of \(F\) were a finite branch
value of \(r\), its pullback would contain a point of even pole
order, impossible. A pole at infinity would require
\(n\,\operatorname{ord}_\infty(F)=5\), hence \(n=5\) and pole
order one. But then the remaining pole degree of
\(\deg F=12\) would be eleven, not divisible by five, whereas all
remaining poles are generic and have order five. Thus every pole of
\(F\) is generic of order five. Their number is

\[
\frac{\deg F}{5}=\frac{12}{n},
\]

so \(n\mid12\). Together with \(n\mid60\) and \(n\ge2\), this gives
(9.10). The same pullback argument applied to the sixty simple
zeros shows that the zeros of \(F\) are simple generic values and
gives the final assertion. \(\square\)

### Corollary 9.10 (source-cycle and residue normal form)

Under \(Q=1\), let

\[
P_j=\psi^*[\alpha_j],\qquad
Q_j=\phi^*[\alpha_j],\qquad
Z_j=\operatorname{div}(z_j).
\]

These are reduced degree-two divisors, and both
\((P_j)_{j=1}^{12}\) and \((Q_j)_{j=1}^{12}\) partition
\(\operatorname{div}B\).

There is a labeled two-regular multigraph \(\Gamma\) on the twelve
source indices with the following exact properties:

1. \(\Gamma\) is a disjoint union of \(12/n\) cycles of the common
   length \(n\) from (9.10), with a two-cycle represented by two
   parallel edges;
2. the edge carrying label \(j\) has two distinct endpoints
   \(r(j),s(j)\), neither equal to \(j\);
3. one has the divisor identity
   \[
   \boxed{Z_j+Q_j=P_{r(j)}+P_{s(j)}.}
   \tag{9.13}
   \]

Moreover there are nonzero scalars \(\epsilon_j\) such that, with

\[
C_j(w)
=
(w-\alpha_j)(w-\alpha_{r(j)})(w-\alpha_{s(j)}),
\]

the following two rational identities hold:

\[
\boxed{
\sum_{j=1}^{12}\frac{\epsilon_j}{C_j(w)}=0,
\qquad
\sum_{j=1}^{12}\frac{\alpha_j\epsilon_j}{C_j(w)}=0.}
\tag{9.14}
\]

Equivalently,

\[
\boxed{
\sum_{j=1}^{12}
\frac{\epsilon_j}
{(w-\alpha_{r(j)})(w-\alpha_{s(j)})}=0.}
\tag{9.15}
\]

Orient each cycle of \(\Gamma\). For an edge \(j\) directed from
\(r(j)\) to \(s(j)\), (9.15) is equivalent to

\[
\boxed{
\epsilon_j=c_{\Gamma(j)}
(\alpha_{r(j)}-\alpha_{s(j)})}
\tag{9.16}
\]

for one nonzero scalar \(c_{\Gamma(j)}\) per cycle. After this
substitution, the first identity in (9.14) is equivalent to twelve
explicit residue equations. If \(j_+(k)\) and \(j_-(k)\) are the
outgoing and incoming edge labels at vertex \(k\), and edge \(k\)
is oriented \(r(k)\to s(k)\), then

\[
\boxed{
c_{\Gamma_v(k)}
\left(
\frac1{\alpha_k-\alpha_{j_+(k)}}
-
\frac1{\alpha_k-\alpha_{j_-(k)}}
\right)
+
c_{\Gamma_e(k)}
\left(
\frac1{\alpha_k-\alpha_{r(k)}}
-
\frac1{\alpha_k-\alpha_{s(k)}}
\right)
=0.}
\tag{9.17}
\]

Here \(\Gamma_v(k)\) is the cycle containing vertex \(k\), while
\(\Gamma_e(k)\) is the cycle containing the edge labelled \(k\).

#### Proof

Theorem 9.9 shows that every pole of the full dihedral quotient is
generic. Hence \(\operatorname{div}B\) is reduced, and its
\(D_n\)-orbits have size \(2n\). The \(b\)-orbits are the divisors
\(P_j\), while the \(a\)-orbits are the divisors \(Q_j\). On each
generic \(D_n\)-orbit, the incidence between reflection orbits is
an \(n\)-cycle. This gives item 1.

At \(Q=1\), factor

\[
M=\Gamma_\psi\Gamma_\phi R,
\]

where \(R\) has bidegree \((9,18)\) and is \(b\)-invariant. At the
source \(T=\alpha_j\), the exact source fiber gives

\[
\operatorname{div}h_j
=P_j+Q_j+\operatorname{div}R(\alpha_j,\lambda).
\tag{9.18}
\]

But \(\operatorname{div}h_j=\operatorname{div}B-Z_j\). The final
term in (9.18) is \(b\)-invariant, as are
\(\operatorname{div}B\) and \(P_j\). Therefore \(Z_j+Q_j\) is a
reduced, \(b\)-invariant degree-four subdivisor of
\(\operatorname{div}B\), hence is the union of two distinct
\(b\)-orbits \(P_{r(j)},P_{s(j)}\). Equation (9.18) also shows that
neither orbit is \(P_j\). The \(Q_j\)'s partition
\(\operatorname{div}B\), so their incidence with the \(P\)-orbits
is exactly the cycle incidence described above. This proves
(9.13) and items 2--3.

Because \(R\) has no horizontal component, its \(b\)-invariant
divisor descends through \(w=\psi(\lambda)\) to a divisor
\(\overline R\) of bidegree \((9,9)\). From (9.18) and (9.13),

\[
\overline R(\alpha_j,w)
=
\mu_j\,
\frac{A(w)}
{(w-\alpha_j)(w-\alpha_{r(j)})(w-\alpha_{s(j)})}
\tag{9.19}
\]

for some \(\mu_j\ne0\). A polynomial of \(T\)-degree at most nine,
evaluated at the twelve distinct \(\alpha_j\)'s, has its two leading
Lagrange coefficients zero. Applying those two identities to
\(\overline R(T,w)\), dividing (9.19) by \(A(w)\), and putting
\(\epsilon_j=\mu_j/A'(\alpha_j)\), gives (9.14). Taking \(w\) times
the first identity minus the second gives (9.15).

Finally,

\[
\frac1{(w-\alpha_r)(w-\alpha_s)}
=
\frac1{\alpha_r-\alpha_s}
\left(
\frac1{w-\alpha_r}-\frac1{w-\alpha_s}
\right).
\]

The vanishing in (9.15) is exactly the zero-divergence condition for
the edge flows
\(\epsilon_j/(\alpha_{r(j)}-\alpha_{s(j)})\). On each connected
cycle those flows are constant, proving (9.16). Substitution into
the first identity of (9.14) and taking the residue at
\(w=\alpha_k\) gives (9.17). \(\square\)

### Remark 9.11

Before using the coordinate divisors, the \(Q=1\) branch admits the
finite five-case normal form

\[
n\in\{2,3,4,6,12\},
\]

with the equal-cycle source system (9.13)--(9.17).
The two-vertex expansion of the labeled graph alone is insufficient:
such graphs exist. The load-bearing constraints are the common
Dickson cycle length and the residue equations with all
\(\epsilon_j\ne0\). Even those equations are not by themselves a
complete exclusion: the verifier prints an abstract \(n=3\)
arithmetic-progression fixture satisfying (9.14)--(9.17). The next
corollary closes the branch by retaining the coordinate divisors,
which that abstract fixture does not supply.

### Corollary 9.12 (the \(Q=1\) branch is impossible)

Every actual pole-disjoint irreducible-conic endpoint with a
\((1,2)\)-component satisfies

\[
\boxed{Q\ge2.}
\tag{9.20}
\]

#### Proof

Assume \(Q=1\), and retain the notation of Theorem 9.9 and
Corollary 9.10. Factor

\[
M=\Gamma_\psi\Gamma_\phi R,
\]

where \(R\) is \(b\)-invariant. At \(T=\alpha_j\), equation (9.18)
and \(\operatorname{div}h_j=\operatorname{div}B-Z_j\) show that

\[
Z_j+Q_j
\quad\text{is \(b\)-invariant.}
\tag{9.21}
\]

Theorem 9.9 also shows that the support of
\(\operatorname{div}B\) is a union of generic, hence free,
\(D_n\)-orbits. Therefore \(Q_j\) and \(bQ_j\) are disjoint. Indeed,
if \(y\in Q_j\) and \(by\in Q_j=\{y,ay\}\), then either \(b\) fixes
\(y\), or \(a^{-1}b\) fixes \(y\). Both group elements are nontrivial
because \(a\ne b\), contradicting freeness. The divisors \(Z_j\) and
\(Q_j\) are also disjoint by (9.18), because
\(\operatorname{div}B\) is reduced.

Applying \(b\) to (9.21), the degree-two divisor \(bQ_j\) is a
subdivisor of \(Z_j+Q_j\). It is disjoint from \(Q_j\), so it is a
subdivisor of \(Z_j\). Equal degrees give

\[
\boxed{Z_j=bQ_j\qquad(1\le j\le12).}
\tag{9.22}
\]

Put \(\chi=\phi\circ b\), a degree-two rational map. Since
\(Q_j=\phi^*[\alpha_j]\), equation (9.22) says

\[
Z_j=\chi^*[\alpha_j].
\]

Writing \(\chi=[\chi_n:\chi_d]\), the binary quadratic
\(\chi_n-\alpha_j\chi_d\) has divisor \(Z_j\), and hence is a
nonzero scalar multiple of \(z_j\). Thus all twelve coordinate
quadratics \(z_j\) lie in

\[
\operatorname{span}\{\chi_n,\chi_d\},
\]

a space of dimension at most two. This contradicts the rank-three
coordinate hypothesis of Lemma 4.3. Hence \(Q=1\) is impossible.
\(\square\)

### Theorem 9.13 (outgoing-conjugate intersection bound)

Every actual pole-disjoint irreducible-conic endpoint with a
\((1,2)\)-component satisfies

\[
\boxed{Q\ge5.}
\tag{9.23}
\]

More precisely, let \(\mathcal X_{\rm out}\) be the union of the
components in \(\mathscr C_{\rm out}\). It has bidegree
\((Q,2Q)\), while its deck conjugate
\(\sigma\mathcal X_{\rm out}\) is contained in \(V(W_1)\). The two
curves have no common component and

\[
\mathcal X_{\rm out}\cdot\sigma\mathcal X_{\rm out}=4Q^2.
\tag{9.24}
\]

If \(r\in\{0,1,2\}\) is the number of fixed points of the deck
involution \(b\) that belong to \(\operatorname{div}B\), then

\[
\boxed{
4Q^2
\ge
12(2Q-2)+2r+(2-r)Q.}
\tag{9.25}
\]

#### Proof

For a source \(\alpha_j\), let \(O_j\) be the degree-\(2Q\) fiber
divisor of \(\mathcal X_{\rm out}\), let \(P_j=\psi^*[\alpha_j]\),
and let \(J_j\) be the fiber divisor of the union of the components
in \(\mathscr C_{\rm in}\). The exact source fiber of \(M\) gives

\[
\operatorname{div}B-Z_j=P_j+J_j+O_j.
\tag{9.26}
\]

The divisors \(\operatorname{div}B\), \(P_j\), and \(J_j\) are
\(b\)-invariant. Consequently

\[
E_j:=Z_j+O_j
\tag{9.27}
\]

is a \(b\)-invariant effective divisor of degree \(2Q+2\). Since
\(O_j=E_j-Z_j\) and \(bO_j=E_j-bZ_j\), coefficientwise minima and
maxima give the exact identity

\[
\boxed{
\deg\gcd(O_j,bO_j)
=
2Q-2+\deg\gcd(Z_j,bZ_j).}
\tag{9.28}
\]

Indeed, the right-hand side is

\[
\deg E_j-\deg\operatorname{lcm}(Z_j,bZ_j)
=(2Q+2)-(4-\deg\gcd(Z_j,bZ_j)).
\]

The curve \(\sigma\mathcal X_{\rm out}\) is a union of components of
\(V(W_1)\), whereas \(\mathcal X_{\rm out}\subseteq V(M)\).
Theorem 8.1 gives \(\gcd(M,W_1)=1\), so these curves have no common
component. Their bidegrees give (9.24).

At every point of the vertical line \(T=\alpha_j\), the local
intersection multiplicity is at least the minimum of the two fiber
multiplicities. One way to see this is to quotient the local
intersection algebra by the parameter \(T-\alpha_j\): its length is
the minimum of the two orders in the resulting one-variable DVR,
and quotienting cannot increase length. Summing over the fiber and
using (9.28) therefore gives at least

\[
12(2Q-2)+
\sum_{j=1}^{12}\deg\gcd(Z_j,bZ_j)
\tag{9.29}
\]

intersections on the twelve source lines.

The involution \(b\) has two fixed points. If a fixed point
\(\beta\) belongs to \(\operatorname{div}B\), pole disjointness puts
it in a unique \(Z_j\), and Lemma 9.1 says that \(Z_j=2[\beta]\).
Thus it contributes two to the sum in (9.29). If instead
\(\beta\notin\operatorname{div}B\), the horizontal fixed line
\(\lambda=\beta\) meets \(\mathcal X_{\rm out}\) in degree \(Q\).
Every such point also lies on
\(\sigma\mathcal X_{\rm out}\). None lies on a source line, because

\[
M(\alpha_j,\beta)=\kappa_jh_j(\beta)\ne0
\]

for every \(j\). The fixed lines therefore add \((2-r)Q\)
intersections disjoint from those counted in (9.29), while the
pole fixed points contribute at least \(2r\) inside (9.29). This
proves (9.25).

For \(Q\ge2\), the right side of (9.25) is minimized at \(r=2\), so

\[
4Q^2\ge24Q-20.
\tag{9.30}
\]

This fails for \(Q=2,3,4\). Corollary 9.12 already excludes \(Q=1\),
proving (9.23). \(\square\)

### Corollary 9.14 (the exact \(Q=5\) equality packet)

If \(Q=5\), both fixed points \(\beta_+,\beta_-\) of \(b\) are
coordinate poles. There are distinct labels
\(\ell_+,\ell_-\) such that

\[
Z_{\ell_+}=2[\beta_+],
\qquad
Z_{\ell_-}=2[\beta_-],
\tag{9.31}
\]

and

\[
\deg\gcd(Z_j,bZ_j)
=
\begin{cases}
2,&j\in\{\ell_+,\ell_-\},\\
0,&j\notin\{\ell_+,\ell_-\}.
\end{cases}
\tag{9.32}
\]

All \(100\) intersections of
\(\mathcal X_{\rm out}\) and
\(\sigma\mathcal X_{\rm out}\) occur on the twelve source lines.
Their intersection degrees there are ten at
\(\alpha_{\ell_+},\alpha_{\ell_-}\) and eight at each other source.
Equivalently, the homogeneous fiber resultant has divisor

\[
\boxed{
\operatorname{div}
\operatorname{Res}_{\lambda}
(\mathcal X_{\rm out},\sigma\mathcal X_{\rm out})
=
8\sum_{j=1}^{12}[\alpha_j]
+2[\alpha_{\ell_+}]
+2[\alpha_{\ell_-}].}
\tag{9.33}
\]

#### Proof

At \(Q=5\), (9.25) reads

\[
100\ge106-3r.
\]

Hence \(r=2\). The lower bound then equals the full intersection
number \(100\). Equality must hold in every preceding estimate.
The two fixed pole points give the two double divisors in (9.31) and
already contribute four to the gcd sum in (9.29), so no other
\(Z_j\) can meet its conjugate. Equation (9.28) gives the stated
source intersection degrees. Since they sum to \(100\), there are
no other intersections, and pushing the intersection cycle to the
\(T\)-line gives (9.33). \(\square\)

### Theorem 9.15 (the \(Q=5\) invariant/anti-invariant normal form)

Assume \(Q=5\), and retain the labels
\(\ell_+,\ell_-\) from Corollary 9.14. After choosing homogeneous
coordinates \([x:y]\) on the parameter line such that

\[
b[x:y]=[x:-y],
\]

put \(w=[x^2:y^2]\). A defining form \(F_{\rm out}\) of
\(\mathcal X_{\rm out}\) has the unique decomposition

\[
\boxed{
F_{\rm out}(T;x,y)
=
E(T;x^2,y^2)+xy\,H(T;x^2,y^2),}
\tag{9.34}
\]

where \(E\) has bidegree \((5,5)\) in \((T,w)\), while \(H\) has
bidegree \((5,4)\).

There is a five-subset

\[
S\subseteq
\{1,\ldots,12\}\setminus\{\ell_+,\ell_-\}
\tag{9.35}
\]

such that, with

\[
P_S(T)=\prod_{j\in S}(T-\alpha_j),
\]

the two fixed-section fibers satisfy

\[
\boxed{
E(T,w_+)=c_+P_S(T),
\qquad
E(T,w_-)=c_-P_S(T)}
\tag{9.36}
\]

for nonzero scalars \(c_+,c_-\). Moreover

\[
\boxed{
H(T,w)
=
(T-\alpha_{\ell_+})(T-\alpha_{\ell_-})H_3(T,w),}
\tag{9.37}
\]

where \(H_3\) has bidegree \((3,4)\).

If

\[
R=
\{1,\ldots,12\}
\setminus
\bigl(S\cup\{\ell_+,\ell_-\}\bigr),
\]

then \(|R|=5\), and the quotient resultants have the exact divisors

\[
\boxed{
\operatorname{div}\operatorname{Res}_w(E,H)
=
3\sum_{j\in S}[\alpha_j]
+4\sum_{j\in R}[\alpha_j]
+5[\alpha_{\ell_+}]
+5[\alpha_{\ell_-}],}
\tag{9.38}
\]

\[
\boxed{
\operatorname{div}\operatorname{Res}_w(E,H_3)
=
3\sum_{j\in S}[\alpha_j]
+4\sum_{j\in R}[\alpha_j].}
\tag{9.39}
\]

Thus the unresolved \(Q=5\) branch is reduced to a
\((5,5)\)-by-\((3,4)\) fixed-source resultant problem of total
intersection degree \(35\).

#### Proof

The decomposition (9.34) is the even/odd decomposition of a binary
form of degree ten under \(y\mapsto-y\). The even monomials are
binary forms of degree five in \((x^2,y^2)\); every odd monomial is
\(xy\) times a binary form of degree four in those variables.

We first record the local consequence of equality in Corollary 9.14.
Let \(\beta\) be a fixed point of \(b\), let \(T=\alpha_j\), and
suppose that \(\beta\) is a root of the fiber
\(F_{\rm out}(\alpha_j,\cdot)\). Its multiplicity is at most two,
because \(\operatorname{div}B\) has multiplicity two there. Equality
in the source-fiber intersection lower bound forces this root to be
simple. Indeed, in local coordinates with \(b(y)=-y\), a double
fiber root has

\[
F_{\rm out}(0,y)=a y^2+O(y^3),
\qquad a\ne0.
\]

Writing

\[
F_{\rm out}-F_{\rm out}^b=2yD,
\]

one has \(D(0,y)=O(y^2)\). Additivity of local intersection
multiplicity against the product \(yD\), followed by specialization
to the source line, gives

\[
I(F_{\rm out},F_{\rm out}^b)
=I(F_{\rm out},y)+I(F_{\rm out},D)
\ge1+2=3,
\]

strictly larger than the fiber-gcd contribution two. This contradicts
the equality of all local bounds in Corollary 9.14.

At \(\beta_+\), the degree-five polynomial
\(F_{\rm out}(T,\beta_+)\) divides

\[
M(T,\beta_+)
=
\text{constant}\cdot L_{\ell_+}(T),
\]

whose eleven source roots are simple. It therefore owns a
five-subset \(S_+\) of the source labels. Similarly \(\beta_-\)
defines a five-subset \(S_-\). The preceding paragraph shows that
all these fixed-section incidences are simple.

At a source \(\alpha_j\), the common fiber divisor of
\(F_{\rm out}\) and \(F_{\rm out}^b\) has even degree, namely eight
or ten by (9.28) and (9.32). Its nonfixed points occur in
\(b\)-pairs. Therefore

\[
\mathbf1_{j\in S_+}+\mathbf1_{j\in S_-}
\]

is even for every \(j\), and hence \(S_+=S_-=:S\). Also
\(\ell_+\notin S_+\), because the source fiber
\(O_{\ell_+}\) is disjoint from
\(Z_{\ell_+}=2[\beta_+]\); equality of the two sets then excludes
\(\ell_+\) from both. The same argument excludes \(\ell_-\).
This proves (9.35)--(9.36).

At \(T=\alpha_{\ell_+}\), no fixed point occurs in the common fiber,
whose degree is ten. Its five nonfixed \(b\)-orbits are common roots
of

\[
E(\alpha_{\ell_+},w)
\quad\text{and}\quad
H(\alpha_{\ell_+},w).
\]

Since the second polynomial has \(w\)-degree at most four, it must
vanish identically. The same holds at \(\alpha_{\ell_-}\), proving
(9.37).

For \(j\in S\), two of the eight common fiber points are the fixed
points, leaving three nonfixed \(b\)-orbits. For \(j\in R\), all
eight points are nonfixed, giving four common quotient roots. For
\(j=\ell_+,\ell_-\), all ten points are nonfixed, giving five.
The curves \(E=0\) and \(H=0\) have no common component, since such
a component would pull back to a common component of
\(\mathcal X_{\rm out}\) and its deck conjugate. Their intersection
number is

\[
(5,5)\cdot(5,4)=45.
\]

The displayed source multiplicities sum to

\[
5\cdot3+5\cdot4+2\cdot5=45,
\]

so they exhaust the resultant and prove (9.38). Factoring the two
\(T\)-linear terms from \(H\) removes five resultant orders at each
of \(\alpha_{\ell_+},\alpha_{\ell_-}\). The residual intersection
number is

\[
(5,5)\cdot(3,4)=35,
\]

and (9.39) follows. \(\square\)

### Corollary 9.16 (no graph component at \(Q=5\))

At \(Q=5\), the outgoing component partition is one of

\[
\boxed{5,\qquad 3+2.}
\tag{9.40}
\]

In particular, no component of \(\mathscr C_{\rm out}\) has
\(u_H=1\).

#### Proof

Suppose an outgoing component has \(u_H=1\). It is a second graph

\[
T=\phi(\lambda)
\]

for a separable degree-two map \(\phi\), distinct from the graph of
\(\psi\). The proof of Theorem 9.9 uses the hypothesis \(Q=1\) only
to guarantee the presence of this graph; once it is present, the two
deck involutions again generate a finite dihedral group and give

\[
f=F\circ r_n,
\qquad
n\in\{2,3,4,6,12\}.
\]

The pole argument in that proof is unchanged: every source pole is
generic for the dihedral quotient. In particular, neither fixed point
of the deck involution \(b\) belongs to \(\operatorname{div}B\), so
the integer \(r\) in Theorem 9.13 is zero.

At \(Q=5\), inequality (9.25) would then give

\[
100\ge12\cdot8+2\cdot5=106,
\]

a contradiction. Hence every outgoing part has size at least two.
The partitions of five with this property are exactly \(5\) and
\(3+2\). \(\square\)

### Theorem 9.17 (the \(Q=5\) branch is impossible)

Every actual pole-disjoint irreducible-conic endpoint with a
\((1,2)\)-component satisfies

\[
\boxed{Q\ge6.}
\tag{9.41}
\]

#### Proof

Assume \(Q=5\). Let \(\Gamma_\psi\) define the graph component, let
\(F_{\rm in}\) define the union of the components in
\(\mathscr C_{\rm in}\), and let \(F_{\rm out}\) define
\(\mathcal X_{\rm out}\). Up to a nonzero scalar,

\[
M=\Gamma_\psi F_{\rm in}F_{\rm out}.
\tag{9.42}
\]

Both the graph divisor and the \(F_{\rm in}\)-divisor are
\(b\)-invariant. Their defining forms may be normalized to be
\(b\)-invariant as well. Indeed, an anti-invariant defining form
would vanish identically on either fixed parameter line of \(b\),
giving a forbidden horizontal component.

Fix one of the two deck-fixed points, say \(\beta_+\), and use a
local parameter \(y\) with

\[
b(y)=-y,\qquad y(\beta_+)=0.
\]

By Corollary 9.14,

\[
Z_{\ell_+}=2[\beta_+].
\]

In the source presentation

\[
M(T,\lambda)
=
\sum_{i=1}^{12}\kappa_iL_i(T)h_i(\lambda),
\]

the term \(h_{\ell_+}\) is nonzero at \(\beta_+\), whereas every
\(h_i\) with \(i\ne\ell_+\) contains the double factor
\(z_{\ell_+}\). Therefore

\[
M(T,\beta_+)
=
\kappa_{\ell_+}L_{\ell_+}(T)h_{\ell_+}(\beta_+),
\tag{9.43}
\]

\[
\partial_yM(T,\beta_+)
=
\kappa_{\ell_+}L_{\ell_+}(T)
\partial_yh_{\ell_+}(\beta_+).
\tag{9.44}
\]

On the complement of the roots of (9.43), division gives a scalar
independent of \(T\):

\[
\frac{\partial_yM(T,\beta_+)}{M(T,\beta_+)}
=
\frac{\partial_yh_{\ell_+}(\beta_+)}
       {h_{\ell_+}(\beta_+)}.
\tag{9.45}
\]

The first two factors on the right side of (9.42) are even in \(y\),
so their first derivatives vanish at \(y=0\). Hence (9.45) implies

\[
\partial_yF_{\rm out}(T,\beta_+)
=d_+F_{\rm out}(T,\beta_+)
\tag{9.46}
\]

for one scalar \(d_+\).

Use the invariant/anti-invariant decomposition (9.34). The quotient
coordinate \(w=[x^2:y^2]\) has zero first derivative at a branch
point, while the local anti-invariant factor \(xy\) has nonzero first
derivative there. Consequently (9.46) is equivalent, up to a
nonzero scalar, to

\[
H(T,w_+)=d'_+E(T,w_+).
\tag{9.47}
\]

Theorem 9.15 gives

\[
E(T,w_+)=c_+P_S(T)
\]

and

\[
H(T,w_+)
=(T-\alpha_{\ell_+})(T-\alpha_{\ell_-})H_3(T,w_+).
\]

The set \(S\) excludes both \(\ell_+\) and \(\ell_-\). Evaluating
(9.47) at either of those two source points therefore forces
\(d'_+=0\), and hence

\[
H(T,w_+)\equiv0.
\tag{9.48}
\]

For every \(j\in S\), the fixed point \(\beta_+\) is a root of the
fiber \(F_{\rm out}(\alpha_j,\cdot)\). Equation (9.48), together
with the fact that the invariant quotient coordinate has no linear
term at \(\beta_+\), makes this root have multiplicity at least two.
But the local equality argument in Theorem 9.15 proves that every
fixed-point root in the \(Q=5\) equality packet is simple. This is a
contradiction. Therefore \(Q=5\) is impossible. \(\square\)

### Corollary 9.18 (fixed-pole odd/even proportionality)

Let \(Q\ge2\), and let \(\beta\) be a fixed point of the deck
involution \(b\) that belongs to the coordinate divisor \(Z_\ell\).
Then

\[
Z_\ell=2[\beta].
\]

After linearizing \(b\) and writing a defining form of the outgoing
component union as

\[
F_{\rm out}(T;x,y)
=E_Q(T;x^2,y^2)+xy\,H_Q(T;x^2,y^2),
\tag{9.49}
\]

with bidegrees

\[
\operatorname{bideg}E_Q=(Q,Q),
\qquad
\operatorname{bideg}H_Q=(Q,Q-1),
\]

one has

\[
\boxed{
H_Q(T,w_\beta)=d_\beta E_Q(T,w_\beta)}
\tag{9.50}
\]

for a scalar \(d_\beta\). Moreover
\(E_Q(T,w_\beta)\) is, up to a nonzero scalar, a squarefree
degree-\(Q\) divisor of

\[
L_\ell(T)=\prod_{j\ne\ell}(T-\alpha_j).
\tag{9.51}
\]

#### Proof

Lemma 9.1 gives \(Z_\ell=2[\beta]\). The fixed fiber of
\(\mathcal X_{\rm out}\) is a degree-\(Q\) factor of

\[
M(T,\beta)
=
\kappa_\ell h_\ell(\beta)L_\ell(T),
\]

so it is squarefree and source-supported, proving (9.51).

Equations (9.43)--(9.46) did not use \(Q=5\): the direct source
expansion makes the logarithmic derivative of \(M\) at \(\beta\)
constant in \(T\), while the graph and the union of the
\(\mathscr C_{\rm in}\)-components are deck invariant and have zero
odd derivative. Thus the outgoing logarithmic derivative is constant.
The local invariant/anti-invariant decomposition (9.49) converts that
identity exactly into (9.50). \(\square\)

### Theorem 9.19 (invariant-coordinate source factors and sharpened intersection bound)

Let

\[
\mathcal I
=
\{j: bZ_j=Z_j\},
\qquad
s=|\mathcal I|.
\tag{9.52}
\]

Then

\[
\deg\gcd(Z_j,bZ_j)
=
\begin{cases}
2,&j\in\mathcal I,\\
0,&j\notin\mathcal I.
\end{cases}
\tag{9.53}
\]

For every \(Q\ge2\), the anti-invariant quotient form in (9.49)
has the source factorization

\[
\boxed{
H_Q(T,w)
=
P_{\mathcal I}(T)\,
\overline H_Q(T,w),}
\qquad
P_{\mathcal I}(T)
=
\prod_{j\in\mathcal I}(T-\alpha_j),
\tag{9.54}
\]

where

\[
\operatorname{bideg}\overline H_Q
=(Q-s,Q-1).
\tag{9.55}
\]

The quotient resultant has degree

\[
\deg_T\operatorname{Res}_w(E_Q,\overline H_Q)
=
2Q^2-Q-Qs,
\tag{9.56}
\]

and its source divisor contains

\[
(Q-1)\sum_{j\notin\mathcal I}[\alpha_j].
\tag{9.57}
\]

Consequently its residual divisor away from the twelve source
points has degree at most

\[
\boxed{
2Q^2-13Q+12-s.}
\tag{9.58}
\]

There is also a sharper form of Theorem 9.13:

\[
\boxed{
4Q^2
\ge
26Q-24+2s.}
\tag{9.59}
\]

#### Proof

Suppose \(Z_j\) and \(bZ_j\) meet. If a common point is not fixed by
\(b\), then both points of its \(b\)-orbit belong to the degree-two
divisor \(Z_j\), so \(bZ_j=Z_j\). If the common point is fixed,
Lemma 9.1 gives \(Z_j=2[\beta]\), which is again \(b\)-invariant.
This proves (9.53).

Fix a source \(\alpha_j\). Equation (9.28) and (9.53) give

\[
\deg\gcd(O_j,bO_j)
=
2Q-2+2\mathbf1_{j\in\mathcal I}.
\tag{9.60}
\]

Let \(m_j\) count the deck-fixed coordinate poles occurring in this
common fiber. Corollary 9.18 shows that at each such pole the
invariant and anti-invariant quotient forms both vanish. Its lift
has multiplicity exactly two in the source fiber: it has
multiplicity at least two by (9.50), and the complete source fiber
contains the corresponding coordinate pole with multiplicity two.
All other common points occur in free \(b\)-pairs. Therefore

\[
\begin{aligned}
\deg\gcd\bigl(
E_Q(\alpha_j,\cdot),
H_Q(\alpha_j,\cdot)
\bigr)
&\ge
\frac{
2Q-2+2\mathbf1_{j\in\mathcal I}-2m_j
}{2}
+m_j\\
&=
Q-1+\mathbf1_{j\in\mathcal I}.
\end{aligned}
\tag{9.61}
\]

The \(w\)-degree of \(H_Q\) is only \(Q-1\). For
\(j\in\mathcal I\), (9.61) therefore forces

\[
H_Q(\alpha_j,w)\equiv0.
\]

The source points are distinct, proving (9.54)--(9.55).

The curves \(E_Q=0\) and \(\overline H_Q=0\) have no common
component: a common component would lift to a common component of
\(\mathcal X_{\rm out}\) and \(b\mathcal X_{\rm out}\).
Their bidegrees give (9.56). At every source not in
\(\mathcal I\), (9.61) gives at least \(Q-1\) common quotient
roots. Subtracting their total degree

\[
(12-s)(Q-1)
\]

from (9.56) proves (9.57)--(9.58).

It remains to prove (9.59). Let \(\beta\) be a deck-fixed
coordinate pole, and let

\[
E_Q(T,w_\beta)
\]

have its \(Q\) simple source roots, as in Corollary 9.18. At each
such source root use local coordinates

\[
x=T-\alpha_j,\qquad b(y)=-y,\qquad w-w_\beta=y^2.
\]

The invariant form \(E_Q\) has a nonzero linear \(x\)-term, while
(9.50) implies that \(H_Q-d_\beta E_Q\) is divisible by \(y^2\).
Since

\[
(F_{\rm out},F_{\rm out}^b)
=(E_Q,yH_Q),
\]

additivity of local intersection multiplicity gives

\[
I(F_{\rm out},F_{\rm out}^b)
=
I(E_Q,y)+I(E_Q,H_Q)
\ge1+2=3.
\tag{9.62}
\]

The fiber-gcd count (9.60) accounts for only two at this fixed
root. Thus every fixed coordinate pole adds \(Q\) further
intersections beyond (9.29). If \(r\) is their number, the source
fibers, these local excesses, and the non-pole fixed lines force

\[
\begin{aligned}
4Q^2
&\ge
12(2Q-2)+2s+rQ+(2-r)Q\\
&=
26Q-24+2s,
\end{aligned}
\]

which proves (9.59). \(\square\)

### Corollary 9.20 (the exact first-open \(Q=6\) compression)

At \(Q=6\),

\[
\boxed{0\le s\le6,}
\tag{9.63}
\]

\[
\boxed{
H_6(T,w)
=
P_{\mathcal I}(T)\,
\overline H_6(T,w),
\qquad
\operatorname{bideg}\overline H_6=(6-s,5),}
\tag{9.64}
\]

and

\[
\boxed{
\operatorname{div}
\operatorname{Res}_w(E_6,\overline H_6)
=
5\sum_{j\notin\mathcal I}[\alpha_j]
+D_s,
\qquad
\deg D_s=6-s,}
\tag{9.65a}
\]

for an effective divisor \(D_s\) on the source line. In particular,

\[
\boxed{
\deg
\left(
\operatorname{Res}_w(E_6,\overline H_6)
\bigm|_{\mathbf P^1_T\setminus\{\alpha_1,\ldots,\alpha_{12}\}}
\right)
\le6-s.}
\tag{9.65}
\]

Equivalently, after the compulsory source and fixed-section
intersections are removed,

\[
\boxed{
\mathcal X_{\rm out}\cdot b\mathcal X_{\rm out}
\text{ has residual degree at most }12-2s.}
\tag{9.66}
\]

If a deck fixed point \(\beta\) is a coordinate pole, with label
\(\ell\in\mathcal I\), then

\[
\boxed{
\overline H_6(T,w_\beta)\equiv0.}
\tag{9.67}
\]

Thus each such pole supplies a horizontal quotient factor of
\(\overline H_6\).

If the outgoing union contains a graph component, then

\[
\boxed{s\le5.}
\tag{9.68}
\]

#### Proof

Equations (9.63)--(9.66) are (9.54), (9.58), and (9.59) at
\(Q=6\). The source containment (9.57) has degree \(60-5s\),
whereas the full resultant degree (9.56) is \(66-6s\). Their
difference is \(6-s\), proving the exact decomposition (9.65a).

For (9.67), Corollary 9.18 gives

\[
H_6(T,w_\beta)=d_\beta E_6(T,w_\beta).
\]

The label \(\ell\) belongs to \(\mathcal I\), so (9.64) makes the
left side vanish at \(T=\alpha_\ell\). The fixed-section divisor is
a factor of \(L_\ell\), hence

\[
E_6(\alpha_\ell,w_\beta)\ne0.
\]

Therefore \(d_\beta=0\). Since \(P_{\mathcal I}\) is nonzero as a
polynomial, (9.64) gives (9.67).

Finally, suppose an outgoing graph \(T=\phi(\lambda)\) is present.
Its deck conjugate is the graph \(T=\phi(b\lambda)\). Their four
intersections consist of the two fixed points of \(b\) and the two
fixed points of the nontrivial dihedral rotation \(ab\), where
\(a\) is the deck involution of \(\phi\). The latter two points form
one free \(b\)-orbit. The generic-pole conclusion of Theorem 9.9
shows that this orbit lies on no source line. It therefore supplies
one off-source common quotient root of \(E_6\) and
\(\overline H_6\). The residual bound (9.65) is consequently at
least one, proving \(s\le5\). \(\square\)

### Corollary 9.21 (the \(s=6\) rectangular-grid normal form)

Assume \(Q=6\) and \(s=6\). Put

\[
\mathcal R=\{1,\ldots,12\}\setminus\mathcal I,
\qquad
P_{\mathcal R}(T)
=
\prod_{j\in\mathcal R}(T-\alpha_j).
\tag{9.69}
\]

Choose an affine quotient coordinate \(w\) whose point at infinity
does not belong to the degree-five divisor occurring below.

Then

\[
\boxed{
H_6(T,w)=P_{\mathcal I}(T)h(w),}
\tag{9.70}
\]

where \(h\) has exact degree five. It is squarefree and all five
roots belong to the reduced source-pole set:

\[
\boxed{
\operatorname{div}(h)
=
\sum_{k\in\mathcal K}[\alpha_k]
\quad\text{for some }
\mathcal K\subseteq\{1,\ldots,12\},
\quad |\mathcal K|=5.}
\tag{9.70a}
\]

Moreover

\[
\boxed{
\operatorname{div}
\operatorname{Res}_w(E_6,h)
=
5\sum_{j\in\mathcal R}[\alpha_j],}
\tag{9.71}
\]

and there are polynomials

\[
A(w),\qquad a_0(T),\qquad a_1(T)
\]

with

\[
\deg_wA<5,
\qquad
\deg_Ta_0,\deg_Ta_1\le6,
\]

such that

\[
\boxed{
E_6(T,w)
=
P_{\mathcal R}(T)A(w)
+
h(w)\bigl(a_1(T)w+a_0(T)\bigr),}
\tag{9.72}
\]

and

\[
\boxed{\gcd(A,h)=1.}
\tag{9.73}
\]

Equivalently,

\[
F_{\rm out}-F_{\rm out}^b
=
2xy\,P_{\mathcal I}(T)h(w)
\tag{9.74}
\]

is a product of the six invariant source lines and a horizontal
divisor of total parameter degree twelve. All intersections with
the conjugate curve occur on this rectangular vertical/horizontal
packet; there is no residual quotient intersection.

If a deck-fixed point is a coordinate pole, its quotient value is a
root of \(h\), and its degree-six fixed-section source divisor is
exactly \(P_{\mathcal R}\).

#### Proof

At \(s=6\), (9.64) makes \(\overline H_6\) independent of \(T\);
write it as \(h(w)\). For every \(j\in\mathcal R\), (9.61) gives
five common quotient roots. Hence \(h\) has degree at least five.
Its degree is at most five, so it has exact degree five and

\[
h(w)\mid E_6(\alpha_j,w)
\qquad(j\in\mathcal R).
\tag{9.75}
\]

The common lifted divisor at a source label is a subdivisor of the
pole divisor. Lemma 9.1 identifies its quotient with the reduced
twelve-point source divisor. Thus the five roots of \(h\) are
distinct source poles, proving (9.70a).

The total degree in (9.56) is now thirty, while the six source
fibers in (9.57) already contribute thirty. This proves (9.71).

In the affine coordinate fixed above, scale \(h\) to be monic and
divide \(E_6\) by \(h\) as a polynomial
in \(w\):

\[
E_6(T,w)
=
h(w)\bigl(a_1(T)w+a_0(T)\bigr)+R(T,w),
\qquad
\deg_wR<5.
\tag{9.76}
\]

Every coefficient of \(R\) has \(T\)-degree at most six. Equation
(9.75) says that all six source points in \(\mathcal R\) are roots
of every coefficient. Therefore

\[
R(T,w)=P_{\mathcal R}(T)A(w),
\]

proving (9.72).

If \(A\) and \(h\) shared a root \(w_0\), then (9.72) would give

\[
E_6(T,w_0)\equiv0
\qquad\text{and}\qquad
h(w_0)=0.
\]

The horizontal quotient component \(w=w_0\) would lift to a common
component of \(\mathcal X_{\rm out}\) and
\(b\mathcal X_{\rm out}\), contrary to Theorem 9.13. This proves
(9.73). Equations (9.74) and the absence of residual intersections
follow from (9.70) and (9.65).

Finally, (9.67) puts every fixed coordinate pole among the roots of
\(h\). Evaluating (9.72) at such a root gives a nonzero scalar
multiple of \(P_{\mathcal R}\), by (9.73). Corollary 9.18 identifies
that polynomial with the fixed-section divisor. \(\square\)

### Corollary 9.22 (graph-branch cross-intersection capacity)

Assume \(Q=6\) and that the outgoing union contains a graph
\(\Gamma_\phi\). Write

\[
\mathcal X_{\rm out}=\Gamma_\phi+\mathcal R_{\rm out},
\qquad
\operatorname{bideg}\mathcal R_{\rm out}=(5,10).
\tag{9.77}
\]

At the source \(\alpha_j\), let \(Q_j\) and \(R_j\) be the
degree-two and degree-ten fiber divisors of these two factors, and
put

\[
t_j=\deg\gcd(Q_j,bZ_j),
\qquad
T_0=\sum_{j=1}^{12}t_j.
\tag{9.78}
\]

Then

\[
\boxed{4\le T_0\le9-s.}
\tag{9.79}
\]

More precisely, the exact source common-divisor degrees are

\[
\deg\gcd(Q_j,bR_j)=2-t_j,
\tag{9.80}
\]

\[
\deg\gcd(R_j,bQ_j)=2-t_j,
\tag{9.81}
\]

\[
\deg\gcd(R_j,bR_j)
=
6+2\mathbf1_{j\in\mathcal I}+2t_j.
\tag{9.82}
\]

If \(s=5\), then \(T_0=4\), all twenty intersections of
\(\Gamma_\phi\) with \(b\mathcal R_{\rm out}\) occur on source
lines, and all one hundred intersections of
\(\mathcal R_{\rm out}\) with \(b\mathcal R_{\rm out}\) occur on
the source lines or the two deck-fixed horizontal lines. The unique
off-source quotient-resultant point is the free \(b\)-orbit where
\(\Gamma_\phi\) meets its deck conjugate.

#### Proof

The graph argument in Corollary 9.16 shows that all poles are generic
for the dihedral action. In particular,

\[
Q_j\cap bQ_j=\varnothing,
\tag{9.83}
\]

and the complete source fiber is reduced. Since

\[
E_j=Z_j+Q_j+R_j
\]

is \(b\)-invariant, the points of \(Q_j\) outside \(bZ_j\) must lie
in \(bR_j\). This proves (9.80); applying \(b\) gives (9.81).
Subtracting these two contributions from (9.60) gives (9.82).

The bidegrees give

\[
\Gamma_\phi\cdot b\mathcal R_{\rm out}=20.
\]

The source lines already contribute at least

\[
\sum_j(2-t_j)=24-T_0,
\]

so \(T_0\ge4\).

Similarly,

\[
\mathcal R_{\rm out}\cdot b\mathcal R_{\rm out}=100.
\]

Equation (9.82) contributes at least

\[
72+2s+2T_0
\]

on the source lines. Neither deck fixed point is a pole in the graph
branch. Each of the two fixed horizontal lines contributes five more
intersections of the residual curve with its conjugate. Therefore

\[
100\ge82+2s+2T_0,
\]

which is \(T_0\le9-s\) and proves (9.79).

At \(s=5\), the two bounds force \(T_0=4\). Both preceding Bézout
bounds are then equalities. Thus the cross and residual component
intersections have no unlisted support. Corollary 9.20 identifies the
single remaining quotient point with the free dihedral-rotation
orbit of the graph pair. \(\square\)

### Theorem 9.23 (quotient-pole capacity excludes \(2\le s\le5\))

At \(Q=6\),

\[
\boxed{s\notin\{2,3,4,5\}.}
\tag{9.84}
\]

If \(s=1\), the unique invariant coordinate divisor is not supported
at a deck fixed point. Consequently:

\[
\boxed{
\text{every graph-containing \(Q=6\) packet has }
s\in\{0,1\}\text{ and no fixed coordinate pole}.}
\tag{9.85}
\]

The complete remaining invariant-coordinate alternatives are

\[
\boxed{s=0,\qquad s=1\text{ nonfixed},\qquad s=6.}
\tag{9.86}
\]

#### Proof

The quotient by the deck involution is the map

\[
w=\psi(\lambda).
\]

Lemma 9.1 identifies the quotient of the pole divisor with the
reduced twelve-point source divisor

\[
\sum_{k=1}^{12}[\alpha_k].
\tag{9.87}
\]

Let

\[
\mathcal R=\{1,\ldots,12\}\setminus\mathcal I,
\qquad
n=|\mathcal R|=12-s,
\qquad
d=6-s.
\]

For every \(j\in\mathcal R\), equation (9.61) says that

\[
\overline H_6(\alpha_j,w)
\mid
E_6(\alpha_j,w).
\tag{9.88}
\]

The divisor on the left has exact degree five: it has at least five
common roots, while its \(w\)-degree is at most five. Those five
roots are distinct and belong to the source set (9.87), because the
common lifted divisor is a subdivisor of the pole divisor and the
quotient pole divisor is reduced.

For each quotient pole \(\alpha_k\), consider

\[
\overline H_6(T,\alpha_k)
\]

as a polynomial in \(T\), of degree at most \(d\). If none of these
twelve polynomials is identically zero, each vanishes at at most
\(d\) of the \(n\) source points indexed by \(\mathcal R\). Counting
the incidences supplied by (9.88) in the two directions gives

\[
5n\le12d.
\tag{9.89}
\]

For \(2\le s\le5\), however,

\[
5(12-s)-12(6-s)=7s-12>0,
\]

contradicting (9.89). Hence some
\(\overline H_6(T,\alpha_k)\) is identically zero.

Equation (9.88) then makes

\[
E_6(\alpha_j,\alpha_k)=0
\qquad(j\in\mathcal R).
\]

Here \(n=12-s\ge7\), while \(E_6(T,\alpha_k)\) has \(T\)-degree at
most six. Therefore it too vanishes identically. The horizontal
quotient line \(w=\alpha_k\) is a common component of
\(E_6\) and \(\overline H_6\), hence lifts to a common component of
\(\mathcal X_{\rm out}\) and \(b\mathcal X_{\rm out}\). This
contradicts Theorem 9.13 and proves (9.84).

Now suppose \(s=1\) and the invariant coordinate divisor is a fixed
double pole. Corollary 9.20 gives

\[
\overline H_6(T,w_\beta)\equiv0.
\]

The same divisibility (9.88) forces
\(E_6(\alpha_j,w_\beta)=0\) at all eleven labels in
\(\mathcal R\), again making \(E_6(T,w_\beta)\) identically zero and
giving a forbidden common component. Thus the \(s=1\) divisor is
nonfixed.

Finally, a graph branch has \(s\le5\) by Corollary 9.20. Combining
this with (9.84) proves (9.85), and Corollary 9.20 already gives
\(s\le6\), proving (9.86). \(\square\)

### Corollary 9.24 (the \(s=6\) fixed split-pencil star)

Assume \(Q=6\) and \(s=6\). For each of the sixty deck-conjugate
parameter pairs \((\lambda,\lambda'=b\lambda)\), let

\[
G_\lambda(T)
=
\gcd(U_\lambda,U_{\lambda'}),
\qquad
A_\lambda(T)=\frac{U_\lambda(T)}{G_\lambda(T)},
\qquad
B_\lambda(T)=\frac{U_{\lambda'}(T)}{G_\lambda(T)}.
\tag{9.90}
\]

Then \(G_\lambda\) is monic of degree five, while
\(A_\lambda,B_\lambda\) are monic degree-six polynomials with
disjoint active-root sets. There is a unique scalar
\(c_\lambda\ne0,1\) such that

\[
\boxed{
A_\lambda-c_\lambda B_\lambda
=
(1-c_\lambda)P_{\mathcal I}.}
\tag{9.91}
\]

Thus all sixty projective secant lines

\[
\left\langle[A_\lambda],[B_\lambda]\right\rangle
\subseteq\mathbf P(F[T]_{\le6})
\]

pass through the same six-source point
\([P_{\mathcal I}]\).

#### Proof

In coordinates with \(b[x:y]=[x:-y]\), an invariant quadratic is
an eigenvector of the induced action on binary quadratics. The
negative eigenspace is spanned by \(xy\), whose divisor consists of
the two deck fixed points, each with multiplicity one. This cannot
be a coordinate divisor: Lemma 9.1 says that a coordinate pole fixed
by \(b\) is a critical point of the degree-two map, and hence is a
double root of its coordinate quadratic. Therefore every
\(z_j\), \(j\in\mathcal I\), belongs to the positive eigenspace:

\[
z_j(b\lambda)=z_j(\lambda)
\qquad(j\in\mathcal I)
\tag{9.92}
\]

after choosing the standard lift of \(b\).

The reciprocal coordinate law (4.2), applied at \(\lambda\) and
\(\lambda'\), now gives one scalar \(c_\lambda\ne0\), independent
of \(j\in\mathcal I\), such that

\[
U_\lambda(\alpha_j)
=
c_\lambda U_{\lambda'}(\alpha_j)
\qquad(j\in\mathcal I).
\tag{9.93}
\]

The two blocks have intersection size \(11-Q=5\), so (9.90) has
the asserted degrees. Active/source separation makes
\(G_\lambda(\alpha_j)\ne0\); dividing (9.93) by it gives

\[
A_\lambda(\alpha_j)
=
c_\lambda B_\lambda(\alpha_j)
\qquad(j\in\mathcal I).
\]

Hence the degree-at-most-six polynomial
\(A_\lambda-c_\lambda B_\lambda\) is divisible by the monic
degree-six polynomial \(P_{\mathcal I}\). Since \(A_\lambda\) and
\(B_\lambda\) are monic, comparison of leading coefficients gives
(9.91). If \(c_\lambda=1\), their difference would have degree at
most five and six distinct roots, forcing
\(A_\lambda=B_\lambda\), contrary to their disjoint root sets.
Thus \(c_\lambda\ne1\). \(\square\)

### Corollary 9.25 (the \(s=6\) source-label near-coincidence)

Assume \(Q=6\) and \(s=6\). For each
\(j\in\mathcal I\), there is a unique source label
\(\sigma(j)\ne j\) such that

\[
\boxed{Z_j=\psi^*[\alpha_{\sigma(j)}].}
\tag{9.94}
\]

The map \(\sigma:\mathcal I\to\{1,\ldots,12\}\) is injective. Put

\[
\mathcal L=\sigma(\mathcal I).
\]

If \(\mathcal K\) is the five-element source-pole set from (9.70a),
then

\[
\boxed{
\mathcal K\subseteq\mathcal I\cap\mathcal L,
\qquad
|\mathcal I\cap\mathcal L|\ge5.}
\tag{9.95}
\]

Consequently either \(\mathcal L=\mathcal I\), in which case
\(\sigma\) is a fixed-point-free permutation of the six labels, or
\(\mathcal I\) and \(\mathcal L\) differ by exactly one label.

For \(j\notin\mathcal I\), let \(\mathcal C_j\) be the two-element
set of quotient source poles supporting \(Z_j+bZ_j\). Then the
bipartite incidence

\[
j\longmapsto\mathcal C_j
\]

between the six noninvariant coordinate labels and the six source
labels outside \(\mathcal L\) is two-regular on both sides, has no
diagonal incidence, and is disjoint from \(\mathcal K\).

#### Proof

Lemma 9.1 says that every coordinate pole maps under \(\psi\) to a
source label different from its coordinate label. If \(Z_j\) is
\(b\)-invariant, it is one complete degree-two fiber of \(\psi\),
which proves (9.94) and \(\sigma(j)\ne j\). Pole disjointness makes
these six fibers disjoint, so \(\sigma\) is injective.

Now fix \(j\notin\mathcal I\). The quotient of the invariant divisor
\(E_j\) has degree seven. Its degree-two coordinate part is
\(\mathcal C_j\). Equations (9.61), (9.70), and (9.75) identify the
remaining degree-five common part with \(\mathcal K\). Hence

\[
\overline E_j=\mathcal C_j+\mathcal K
\tag{9.96}
\]

as a reduced source-pole divisor. Equation (9.26) partitions the
reduced quotient pole divisor into
\([\alpha_j]\), the quotient of \(J_j\), and \(\overline E_j\).
Therefore

\[
\mathcal K\cap\mathcal C_j=\varnothing,
\qquad
j\notin\mathcal K.
\tag{9.97}
\]

As \(j\) ranges outside \(\mathcal I\), the coordinate roots in the
\(Z_j\)'s are exactly the pole roots not already consumed by the six
full fibers (9.94). Each source fiber outside \(\mathcal L\) has two
roots, while each noninvariant \(Z_j\) contributes one root to each
of two distinct source fibers. Thus the incidences
\(\mathcal C_j\) form the asserted two-regular bipartite graph on
\(\mathcal I^c\) and \(\mathcal L^c\). In particular their union is
\(\mathcal L^c\). Equation (9.97) gives
\(\mathcal K\subseteq\mathcal L\); its second clause for all
\(j\notin\mathcal I\) gives
\(\mathcal K\subseteq\mathcal I\). This proves (9.95), and the
six-set alternative follows. \(\square\)

### Corollary 9.26 (split-pencil fiber capacity and pole-cycle types)

Assume \(Q=6\) and \(s=6\).

1. Any one projective pencil line through
   \([P_{\mathcal I}]\) contains at most ten **distinct** monic
   degree-six locators split on the active domain. If it contains
   ten, their root sets partition all sixty active roots.
2. The two-regular bipartite pole graph of Corollary 9.25 has cycle
   half-length partition

\[
\boxed{
6,\qquad4+2,\qquad3+3,\qquad2+2+2.}
\tag{9.98}
\]

These are exactly the four graph-free outgoing component partitions.

#### Proof

Let \(A_1,A_2\) be two distinct monic split sextics on one line
through \(P_{\mathcal I}\). There are nonzero scalars \(u,v\) with

\[
A_1-uA_2=vP_{\mathcal I}.
\tag{9.99}
\]

If an active root \(t\) belonged to both \(A_1\) and \(A_2\), then
(9.99) would give \(P_{\mathcal I}(t)=0\), contradicting
active/source separation. Thus distinct split fibers on the pencil
have disjoint six-element active root sets. There can be at most
\(60/6=10\), and equality partitions the active domain.

For the second statement, every vertex of the bipartite pole graph
has degree two. Its connected components are therefore even cycles.
Pole disjointness makes the two neighbors of a left vertex distinct,
so there is no two-cycle; every cycle has half-length at least two.
The half-lengths sum to six. The partitions of six with all parts at
least two are exactly (9.98). \(\square\)

### Corollary 9.27 (the \(s=6\) source-facet deck)

Assume \(Q=6\) and \(s=6\). There is a canonical bijection

\[
\boxed{\tau:\mathcal I\longrightarrow\mathcal L^c}
\tag{9.100}
\]

with the following properties. For \(j\notin\mathcal I\),

\[
\boxed{
O_j=\psi^*\mathcal K+bZ_j.}
\tag{9.101}
\]

For \(x\in\mathcal I\), the invariant effective divisor \(O_x\) is
the pullback of the reduced six-point source divisor

\[
\boxed{
\overline O_x
=
\{\alpha_1,\ldots,\alpha_{12}\}
\setminus
\bigl(\mathcal K\cup\{\alpha_{\tau(x)}\}\bigr).}
\tag{9.102}
\]

Let \(\eta\) be the unique label in
\(\mathcal L\setminus\mathcal K\). The horizontal source fibers of
the outgoing union are then completely determined:

1. if \(k\in\mathcal K\) and
   \(\pi\in\psi^{-1}(\alpha_k)\), then
   \[
   \operatorname{Root}_T F_{\rm out}(T,\pi)
   =\{\alpha_j:j\notin\mathcal I\};
   \tag{9.103}
   \]
2. if \(\pi\in\psi^{-1}(\alpha_\eta)\), then
   \[
   \operatorname{Root}_T F_{\rm out}(T,\pi)
   =\{\alpha_x:x\in\mathcal I\};
   \tag{9.104}
   \]
3. let \(\ell\in\mathcal L^c\), and write
   \[
   \psi^{-1}(\alpha_\ell)=\{\pi,b\pi\},
   \qquad
   \pi\in Z_j,\quad b\pi\in Z_{j'}
   \]
   for the two neighbors \(j,j'\in\mathcal I^c\) of \(\ell\) in
   the pole graph. If \(x_\ell=\tau^{-1}(\ell)\), then
   \[
   \boxed{
   \begin{aligned}
   \operatorname{Root}_T F_{\rm out}(T,\pi)
   &=
   \{\alpha_x:x\in\mathcal I\setminus\{x_\ell\}\}
   \cup\{\alpha_{j'}\},\\
   \operatorname{Root}_T F_{\rm out}(T,b\pi)
   &=
   \{\alpha_x:x\in\mathcal I\setminus\{x_\ell\}\}
   \cup\{\alpha_j\}.
   \end{aligned}}
   \tag{9.105}
   \]

Thus the twelve distinct pole points over \(\mathcal L^c\) are six
one-exchange pairs of facets: each pair has a canonical common
five-set of invariant source labels. The pullbacks over
\(\mathcal K\) and \(\eta\) have degrees ten and two, respectively;
they are divisor degrees and allow ramified deck-fixed fibers.

#### Proof

For \(j\notin\mathcal I\), Corollary 9.25 gives

\[
\overline E_j=\mathcal C_j+\mathcal K.
\]

Pulling this divisor back by \(\psi\), and using
\(\psi^*\mathcal C_j=Z_j+bZ_j\), gives

\[
Z_j+O_j=Z_j+bZ_j+\psi^*\mathcal K.
\]

Cancellation proves (9.101).

Now let \(x\in\mathcal I\). Both \(Z_x\) and \(E_x=Z_x+O_x\) are
deck invariant. More precisely, the exact source-fiber
decomposition writes them as unions of complete invariant component
fibers; their defining invariant forms descend through \(\psi\).
Thus \(O_x=\psi^*\overline O_x\) for an effective degree-six source
divisor. Pole disjointness makes its six source labels distinct,
although the pullback may have multiplicity two at a ramified
deck-fixed point. If \(k\in\mathcal K\), evaluate (9.72) at
\((T,w)=(\alpha_x,\alpha_k)\). Since
\(P_{\mathcal R}(\alpha_x)\ne0\) and \(A(\alpha_k)\ne0\) by
\(\gcd(A,h)=1\), the value is nonzero. Thus

\[
\mathcal K\cap\overline O_x=\varnothing.
\]

The complement of \(\mathcal K\) has seven labels, so there is a
unique label \(\tau(x)\) for which (9.102) holds.

Fix \(\ell\in\mathcal L^c\). Its two pole points belong to two
distinct noninvariant coordinate divisors \(Z_j,Z_{j'}\).
At \(\pi\in Z_j\), the complete horizontal fiber of \(M\) is the
eleven-source divisor omitting \(\alpha_j\); at \(b\pi\in Z_{j'}\)
it omits \(\alpha_{j'}\). The graph contributes the common root
\(\alpha_\ell\), and the deck-invariant union of the
\(\mathscr C_{\rm in}\)-components has the same four source roots
at \(\pi\) and \(b\pi\). Those four roots avoid
\(\alpha_j,\alpha_{j'}\). Consequently the two degree-six outgoing
fibers have five common roots and differ by the exchange
\(\alpha_j\leftrightarrow\alpha_{j'}\).

No noninvariant source label can be one of the five common roots:
by (9.101), the common part of \(O_r\) and \(bO_r\) is
\(\psi^*\mathcal K\), while \(\ell\notin\mathcal K\).
Therefore exactly five invariant labels contain the full fiber over
\(\ell\). Exactly one \(x\in\mathcal I\) omits it, so
\(\tau(x)=\ell\). This holds for every \(\ell\in\mathcal L^c\);
since both sets have size six, \(\tau\) is a bijection. The same
argument identifies the exchanged roots and proves (9.105).

Finally, (9.101) and (9.102) show directly that every pole over
\(\mathcal K\) has outgoing root set \(\mathcal I^c\), while the
unique label \(\eta\in\mathcal L\setminus\mathcal K\) belongs to
every \(\overline O_x\), \(x\in\mathcal I\), and to no
\(\overline O_j\), \(j\notin\mathcal I\). This proves
(9.103)--(9.104). \(\square\)

### Corollary 9.28 (component edge coloring and the exact correction)

Factor the graph-free outgoing union over an algebraic closure as

\[
F_{\rm out}=\prod_{\rho=1}^m H_\rho,
\qquad
\operatorname{bideg}H_\rho=(u_\rho,2u_\rho),
\qquad
\sum_\rho u_\rho=6.
\tag{9.106}
\]

Color an edge \(e=(j,\ell)\) of the pole graph by \(\rho\) when,
for its unique pole \(z_e\in Z_j\cap\psi^{-1}(\alpha_\ell)\),

\[
H_\rho(\alpha_j,bz_e)=0.
\tag{9.107}
\]

Then:

1. the coloring is well defined, and color \(\rho\) occurs exactly
   \[
   \boxed{2u_\rho}
   \tag{9.108}
   \]
   times;
2. at a right vertex \(\ell\in\mathcal L^c\), retain the notation
   of (9.105), and let
   \(S_\rho^-(\ell)\), \(S_\rho^+(\ell)\) be the source-root sets of
   \(H_\rho(T,\pi)\), \(H_\rho(T,b\pi)\), respectively. Put
   \[
   n_{\rho\sigma}(\ell)
   =
   \left|
   S_\rho^-(\ell)\cap S_\sigma^+(\ell)
   \cap(\mathcal I\setminus\{x_\ell\})
   \right|.
   \tag{9.109}
   \]
   If \(c_-\) is the color of \((j',\ell)\) and \(c_+\) the color
   of \((j,\ell)\), then
   \[
   \boxed{
   \begin{aligned}
   \sum_\sigma n_{\rho\sigma}(\ell)
   &=u_\rho-\mathbf1_{\rho=c_-},\\
   \sum_\rho n_{\rho\sigma}(\ell)
   &=u_\sigma-\mathbf1_{\sigma=c_+}.
   \end{aligned}}
   \tag{9.110}
   \]

Define the right-vertex migration

\[
\mu_\ell=\sum_{\rho\ne\sigma}n_{\rho\sigma}(\ell).
\tag{9.111}
\]

If the two pole-graph edges at \(\ell\) have different colors, then
\(\mu_\ell\ge1\). At a left vertex \(j\), let
\(\delta_j=1\) when its two incident edges have different colors
and \(0\) otherwise. Hence

\[
\boxed{
\sum_{\ell\in\mathcal L^c}\mu_\ell=0
\quad\text{and}\quad
\sum_{j\in\mathcal I^c}\delta_j=0}
\tag{9.112}
\]

is a sufficient exact condition for every pole-graph cycle to be
carried by one outgoing component. Under (9.112), the component
partition \((u_\rho)\) is a coarsening of the pole-cycle
half-length partition.

#### Proof

Every edge root in (9.107) is simple: it lies in a noninvariant
coordinate divisor over \(\mathcal L^c\), hence in a free deck
fiber. The corresponding source-fiber root therefore belongs to
exactly one component. Fix \(H_\rho\).
Its intersections with the six noninvariant source lines total
\(6(2u_\rho)=12u_\rho\). Along the degree-ten pullback divisor
\(\psi^*\mathcal K\), equation (9.103) makes the horizontal fiber
consist of \(u_\rho\) noninvariant source roots. Summing with local
pullback multiplicity therefore accounts for \(10u_\rho\)
incidences; this includes ramified deck-fixed fibers. Equation
(9.101) says that all remaining
noninvariant-source incidences are precisely the edge roots
\(bZ_j\). Their number is therefore \(2u_\rho\), proving (9.108).

Equation (9.105) says that the two component root partitions at
\(\pi,b\pi\) have the common five-set
\(\mathcal I\setminus\{x_\ell\}\), with the extra root
\(\alpha_{j'}\) at \(\pi\) and \(\alpha_j\) at \(b\pi\).
Deleting those extra roots from the component containing them gives
exactly the row and column sums (9.110).

If \(c_-\ne c_+\) and all off-diagonal entries in (9.109) vanished,
the diagonal entry in row \(\rho\) would have to equal both
\(u_\rho-\mathbf1_{\rho=c_-}\) and
\(u_\rho-\mathbf1_{\rho=c_+}\) for every \(\rho\), which is
impossible. Thus \(\mu_\ell\ge1\). If (9.112) holds, the two edge
colors agree at every right vertex and at every left vertex. Color
is consequently constant around each cycle. Summing the edge count
\(2u_\rho\) over the cycles of one color proves the coarsening
statement. \(\square\)

### Guardrail 9.29 (the correction is not numerically forced to vanish)

The source-facet cardinalities, color counts, and transportation
margins in Corollary 9.28 do not alone imply (9.112). On a single
twelve-edge pole cycle take component degrees \(4+2\). Color four
edges by the degree-two component and the other eight by the
degree-four component. At a right vertex with different incoming
and outgoing colors, the common-five transportation matrix can be

\[
\begin{pmatrix}3&1\\0&1\end{pmatrix}
\quad\text{or}\quad
\begin{pmatrix}3&0\\1&1\end{pmatrix},
\]

according to the orientation; at equal-color vertices use the
corresponding diagonal matrix. These matrices satisfy (9.110), the
global color counts are \(8\) and \(4\), and the cycle is not
monochromatic. The focused verifier prints such a fixture.

This is a combinatorial route cut, not an algebraic falsifier.
Eliminating the correction requires the actual bidegree-\((u,2u)\)
factor interpolation, the reciprocal block rows, or another
source-coupled identity.

### Guardrail 9.30 (fiber multiplicity is not controlled)

Corollary 9.26 counts distinct split sextics, not deck-pair
occurrences. The same sextic can a priori occur in several pairs
with different five-root cores \(G_\lambda\). Block replication gives
only the coarse multiplicity cap twenty-two. Therefore neither
Corollary 9.26 nor the equality of the two partition lists in (9.98)
identifies pole-graph cycles with outgoing irreducible components.
That compatibility is a genuine remaining lemma.

### Guardrail 9.31 (the current split-pencil theorem does not yet pay this packet)

The identity of Corollary 9.24 is exactly a one-parameter projective
locator pencil on the sixty-point active domain. Its fixed active
part is trivial, and the moving-root incidence theorem therefore
recovers the bound

\[
\left\lfloor\frac{60}{6}\right\rfloor=10
\]

for the number of distinct split sextics on one pencil. This is the
same enumerative content as the first part of Corollary 9.26.

The corresponding first-match C8 payment theorem has additional
hypotheses which are not supplied here. It requires one actual MCA
split-pencil chart after the earlier semantic branches have been
removed, together with an injective map from bad owner slopes to the
pencil parameter. The present deck-pair packet prints neither that
owner-slope map nor a proof that repeated occurrences with different
five-root cores \(G_\lambda\) belong to one such chart. Indeed,
Guardrail 9.30 is precisely the surviving multiplicity obstruction.

Thus Corollary 9.24 is a canonical planted/split-pencil precursor and
Corollary 9.26 pays its distinct-fiber census. They do not by
themselves book a same-record owner payment. The relevant repository
interfaces are the moving-root theorem and its one-pencil corollary
in `experimental/grande_finale.tex`, together with the explicit
nonclaim in `proof/reciprocal_cauchy_block_line_emission.md`.

This interface check was repeated against repository main commit
`b13de8113a03f06b6fc22bbd2f289a8abcdf7e95` on 2026-07-27. Neither
the local pencil-cap interface nor a payment for one fixed union
supplies the missing global census, cross-union aggregation, or
same-record adapter for this packet.

## 10. What remains open

The one-triangle target of Corollary 6.3 is the sharpest presently
identified sufficient closure of PDCEC. It is not claimed equivalent:
PDCEC could also be proved by another exclusion argument that does not
produce a degenerate triple. The proved inventory it may consume:

```text
inherited: (1.1), the 1-(60,11,22) design, Q9 = inactive locator
this note: cleaned identity (3.1) with fiber laws (3.2)-(3.4)
this note: separation, block distinctness, conic coordinates (4.2)
this note: rank-3 block/source reformulation (Remark 4.6)
this note: collinearity ledger (Remark 5.3)
this note: component law (u,2u), no (1,1) components
this note: vertex formula (8.1)-(8.2) and grid splitting
this note: (1,2) descent dichotomy (Section 9)
this note: even self-correspondence subdegree 2,...,20 (Corollary 9.5)
this note: uniform deck-pair intersection 11-Q (Corollary 9.7)
this note: Q=1 dihedral degrees 2,3,4,6,12 (Theorem 9.9)
this note: Q=1 source-cycle residue system (Corollary 9.10)
this note: Q=1 coordinate-pencil contradiction (Corollary 9.12)
this note: Q=2,3,4 outgoing-conjugate exclusion (Theorem 9.13)
this note: exact Q=5 resultant packet (Corollary 9.14)
this note: Q=5 (5,5)-by-(3,4) normal form (Theorem 9.15)
this note: Q=5 outgoing partitions reduced to 5 or 3+2 (Corollary 9.16)
this note: Q=5 source-derivative contradiction (Theorem 9.17)
this note: fixed-pole odd/even proportionality (Corollary 9.18)
this note: invariant-coordinate source factors and sharpened intersection bound
           (Theorem 9.19)
this note: Q=6 quotient-resultant residual degree at most 6-s
           (Corollary 9.20)
this note: Q=6, s=6 rectangular-grid normal form
           (Corollary 9.21)
this note: Q=6 graph-branch capacity 4 <= T0 <= 9-s
           (Corollary 9.22)
this note: Q=6 quotient-pole capacity excludes s=2,3,4,5
           (Theorem 9.23)
this note: Q=6, s=6 gives sixty split secants through one source
           locator (Corollary 9.24)
this note: Q=6, s=6 source-label sets agree in at least five labels
           (Corollary 9.25)
this note: Q=6, s=6 pencil fiber cap 10 and pole-cycle types
           (Corollary 9.26)
this note: Q=6, s=6 canonical source-facet deck and matching
           (Corollary 9.27)
this note: Q=6, s=6 component edge coloring and exact correction
           (Corollary 9.28)
this note: component cardinalities do not force correction zero
           (Guardrail 9.29)
```

Routes already insufficient (target Section 10) remain insufficient;
this note adds none of the forbidden shortcuts: all statements
consume the source-coupled identity through (4.1)--(4.2), (3.1), or
first derivatives of (3.1), never the design axioms alone. The
design-only cyclic guardrail survives every combinatorial statement
proved here, as required.

No owner payment is booked. The reducible two-line template branch
is untouched, except that Corollary 6.2 shows its payment interface
cannot be reached from inside the irreducible branch.
