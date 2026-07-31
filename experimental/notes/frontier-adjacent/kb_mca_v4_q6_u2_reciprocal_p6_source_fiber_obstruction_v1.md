---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every actual outgoing component must divide all twelve specialized source fibers of the endpoint producer. The exact reciprocal-P6 local component from PR #1126 is coprime to the complete source polynomial at five common invariant sources and the extra invariant source eta=0, so that committed witness cannot lift to an actual endpoint component.
architecture: null
partition_digest: null
atom_or_cell: K3_Q6_U2_RECIPROCAL_P6_PARENT_WITNESS_SOURCE_FIBER_GATE
quantifier: the one exact local component committed in PR #1126, tested against all twelve mandatory source fibers of the active endpoint producer
projection_and_unit: polynomial-component compatibility; not distinct bad slopes per received line
claimed_bound: witness-specific active-producer deletion, with no charge and no endpoint movement
status: PROVED_WITNESS_SPECIFIC_ACTIVE_SOURCE_FIBER_DELETION_ROW_OPEN
impact: ACTIVE_SOURCE_SEMANTIC_DELETION_OF_PR_1126_WITNESS
falsifier: failure of the producer specialization lemma, failure to bind the exact parent H and twelve labels, or a nonzero common factor at any of the six printed fatal source fibers in either committed replay
replay: python3 experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_source_fiber_obstruction_v1.py --check
---

# KoalaBear reciprocal-\(P_6\) source-fiber obstruction

## 0. Verdict

The exact local component committed in PR
[#1126](https://github.com/przchojecki/rs-mca/pull/1126), with its declared
twelve labels and normalized deck coordinate, does not extend to an actual
\(Q=6,u=2\) endpoint component.

The missing condition is elementary but source-global.  If
\(H(T,X)\) is an actual outgoing component, then for every one of the
twelve source labels \(\alpha_i\),

\[
 H(\alpha_i,X)\mid B(X),
\tag{0.1}
\]

where \(B\) is the product of the twelve coordinate quadratics.  The parent
packet reconstructed \(H\) on only six noninvariant row labels.  On the other
six mandatory source labels, its exact gcd with \(B\) has degree zero.

This is a source-semantic deletion of one committed witness.  It does not
contradict the parent's local joint-consistency theorem, eliminate every
reciprocal-\(P_6\) component, produce a same-record owner, or move a ledger
quantity.

## 1. The source-fiber divisibility lemma

The source reduction retained from PR #1116 starts with twelve distinct
source labels \(\alpha_1,\ldots,\alpha_{12}\), their Lagrange basis
\(L_i(T)\), twelve pairwise pole-disjoint binary quadratics \(z_i(X)\), and

\[
 B(X)=\prod_{i=1}^{12}z_i(X),
 \qquad
 h_i(X)=\frac{B(X)}{z_i(X)}.
\tag{1.1}
\]

Repeated roots inside one \(z_i\) are allowed.  The endpoint producer is

\[
 M(T,X)
 =
 \sum_{i=1}^{12}\kappa_iL_i(T)h_i(X),
 \qquad
 \kappa_i\ne0.
\tag{1.2}
\]

Let \(H(T,X)\) be an actual irreducible outgoing component of bidegree
\((2,4)\).  By definition of the outgoing component union,

\[
 H\mid F_{\rm out}\mid M.
\tag{1.3}
\]

Specialize a polynomial factorization \(M=HG\) at \(T=\alpha_i\).  Since
\(L_j(\alpha_i)=\delta_{ij}\),

\[
 H(\alpha_i,X)G(\alpha_i,X)
 =
 M(\alpha_i,X)
 =
 \kappa_i h_i(X)
 =
 \kappa_i\frac{B(X)}{z_i(X)}.
\tag{1.4}
\]

The right side is nonzero and the component used below is monic of
\(X\)-degree four, so its specialization cannot vanish identically.  Thus

\[
\boxed{
 H(\alpha_i,X)\mid \frac{B(X)}{z_i(X)}
 \quad\Longrightarrow\quad
 H(\alpha_i,X)\mid B(X)
 \qquad(1\le i\le12).}
\tag{1.5}
\]

The final condition is deliberately weaker than the assigned-coordinate
condition.  It depends only on the complete source divisor.  It is therefore
independent of the nonzero \(\kappa_i\), the ordering of the invariant
coordinates, pole orientations, and nonzero equation scales.

Homogenizing \(H(\alpha_i,X)\) and \(B(X)\) shows that the common-factor
degree is invariant under a projective change of the pole coordinate.  In
the committed affine chart both forms are monic, so neither has a root at
infinity and the affine gcd is the complete binary-form test.

The source-producer formula, outgoing-component factorization, and complete
source-divisor identity are proved in Corollaries 9.25--9.28 of
source-reduction commit
`44542e91e459364a521870ed2ebde7f6fe5055bf`, whose theorem-level conclusions
were manually integrated in commit
`0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d`.  Equations (1.1)--(1.5) are
included here so that the new implication does not rely on a prose summary.

## 2. The exact parent component and complete source divisor

Retain the parent field

\[
 E=\mathbf F_p[\omega]/(\omega^2-1923159404),
 \qquad
 p=2{,}130{,}706{,}433,
\tag{2.1}
\]

and its bidegree-\((2,4)\) polynomial

\[
 H(T,X)
 =
 X^4-S(T)X^3+\bigl(2+P(T)\bigr)X^2-S(T)X+1.
\tag{2.2}
\]

The exact coefficients of \(S\) and \(P\) and all six noninvariant labels
are read from the payload with SHA-256

```text
a3231f7903e255b254b202a269aca1740aec666cd04c13940711e83d29e8ce1b
```

at parent commit
`0f6c23f5c4f02ee9f9e8f340f833abc0096cf254`.

The parent deck coordinate is \(X\mapsto-X\), with quotient
\(\psi(X)=X^2\).  The proved source-facet coverage says that the product of
the twelve actual coordinate quadratics is, up to a nonzero scalar, the
pullback of the complete twelve-source divisor.  Thus its monic
representative is

\[
 B(X)=\prod_{\beta\ {\rm in\ the\ complete\ source\ set}}
       (X^2-\beta).
\tag{2.3}
\]

Concretely, the source reduction defines
\(\widehat A=\prod_j(\psi_n-\alpha_j\psi_d)\) and proves
\(\operatorname{div}\widehat A=\operatorname{div}B\), hence
\(\widehat A\sim B\).

Indeed, the six invariant coordinate divisors are six complete deck fibers
over a six-label set \(\mathcal L\).  The other six coordinate quadratics
give a two-regular bipartite incidence on the complementary six labels:
their twelve roots comprise both points of every deck fiber over
\(\mathcal L^c\).  The two collections therefore multiply to the pullback
of all twelve source labels, with the same multiplicities.

An individual noninvariant coordinate quadratic need not be one complete
deck fiber; only the product identity is used.  The complete source set
consists of:

1. the five roots of the committed reciprocal source quintic
   \(A_{\mathcal K}\);
2. the extra invariant label \(\eta=0\); and
3. the six committed noninvariant row labels.

These twelve values are distinct in \(E\).  The polynomial (2.3) has degree
\(24\).  Because the full deck fiber over \(\eta=0\) is \(X^2\), \(B\) has exactly the
expected repeated root at \(X=0\); repeated roots inside one coordinate
quadratic are allowed by the producer.  The other coordinate quadratics are
reduced and their root sets are disjoint.

## 3. Exact obstruction

The Python verifier and independent Sage replay reconstruct \(E\), the five
quintic roots, all twelve source labels, \(B\), and every specialized row
\(H(\beta,X)\).  Their complete gcd-degree table is:

\[
\begin{array}{c|c|c|c}
\text{source role}&\text{count}
&\deg\gcd(H(\beta,X),B(X))&\text{necessary gate}\\ \hline
\text{common invariant source}&5&0&\text{fails}\\
\eta=0&1&0&\text{fails}\\
\text{noninvariant row source}&6&4&\text{passes}
\end{array}
\tag{3.1}
\]

Thus the histogram is exactly

\[
\boxed{\{0:6,\ 4:6\}.}
\tag{3.2}
\]

At each of the first six sources, Bézout gives

\[
\gcd(H(\beta,X),B(X))=1.
\tag{3.3}
\]

Coprimality over \(E\) remains coprimality after scalar extension.  It
therefore contradicts the necessary divisibility (1.5), not merely a
chosen factorization or coordinate assignment.

As a positive control, the Sage replay also verifies that each of the six
noninvariant rows is exactly the product of the two committed pole
quadratics.  Each has gcd degree four with the complete \(B\), as required
by the weaker assignment-independent gate (1.5).

The terminal is consequently

```text
DELETED_BY_ACTIVE_SOURCE_FIBER_DIVISIBILITY
```

for this witness.

## 4. Implication and boundary

The result changes the operational conclusion of the parent witness without
making its theorem false:

- **Still proved:** the local source-facet, weighted-GRS, split-pole,
  exact-\(P_6\), endpoint-deck, and reciprocal equations checked in #1126
  are jointly consistent.
- **Now excluded:** that exact \(H\) cannot be an actual factor of the
  endpoint producer because it fails six mandatory source fibers.
- **Still open:** other reciprocal endpoint orbits, every other
  reciprocal-\(P_6\) component, \(D_4/D_5\), \(P_2\sqcup C_4\), simple and
  repeated quartics, the hereditary \(69\)-class deletion theorem, and the
  KoalaBear row.

No received line, affine bad slope, first-match owner, or payment is
constructed.  The active values \(U_{\rm paid},U_Q,U_{\rm BC},U_{\rm new}\)
remain null and ledger movement is zero.

The next component compiler must impose (1.5) at all twelve sources before
running a reciprocal, \(D_4\), \(D_5\), or signature eliminant.  In
particular, a future \(2+2+2\) compiler should treat the six omitted source
fibers as a load-bearing first gate rather than accept a six-row
interpolation packet as an actual component.

## 5. Replays

```bash
python3 \
  experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_source_fiber_obstruction_v1.py \
  --check
python3 \
  experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_source_fiber_obstruction_v1.py \
  --tamper-selftest
sage \
  experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_source_fiber_obstruction_v1.sage
```

The Python verifier first revalidates and hash-binds the parent certificate,
then performs exact \(\mathbf F_{p^2}\) polynomial arithmetic and runs a
36-case mutation suite.  The Sage replay independently reconstructs the
field, complete source divisor, twelve fibers, gcds, and the six stronger
exact positive controls.
