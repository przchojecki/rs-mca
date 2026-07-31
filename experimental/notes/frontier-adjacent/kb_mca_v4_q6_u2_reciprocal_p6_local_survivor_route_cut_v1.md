---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Over the deployed KoalaBear field, the normalized Q=6,u=2 source-facet, weighted-GRS, split-pole, exact-P6, endpoint-deck, and reciprocal-involution equations have an exact local solution in F_(p^2) contained in F_(p^6). Therefore these local equations alone cannot eliminate the reciprocal P6 branch; an additional active source-semantic deletion or a chronology-valid same-record owner is necessary.
architecture: null
partition_digest: null
atom_or_cell: K3_Q6_U2_RECIPROCAL_P6_LOCAL_COMPONENT
quantifier: one exact local source-facet component over the deployed field; not an active first-match received-line record
projection_and_unit: normalized row locators and twelve source labels; not distinct bad slopes per received line
claimed_bound: no charge and no endpoint movement
status: PROVED_LOCAL_SOURCE_FACET_SURVIVOR_ROW_OPEN
impact: DIRECT_RECIPROCAL_P6_LOCAL_ELIMINATION_ROUTE_CUT
falsifier: failure of any exact field, interpolation, weighted-GRS, split-pole, gcd-graph, deck-fibre, source-locator, or reciprocal-involution check in either committed replay
replay: python3 experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.py --check
---

# KoalaBear reciprocal-\(P_6\) local survivor route cut

## 0. Verdict

The normalized \(Q=6,u=2\) conic reduction does not become empty after
imposing the exact degree-two reconstruction equations, the split source
labels, the endpoint deck fibres, and the reciprocal involution.  This note
gives one exact solution over
\[
 \mathbf F_{p^2}\subset \mathbf F_{p^6},
 \qquad p=2{,}130{,}706{,}433.
\]
Its six reconstructed quartic rows have exact common-signature graph \(P_6\).

Consequently, a proof that tries to eliminate every reciprocal-\(P_6\)
component from only the equations checked here is false.  The next closing
step must use an omitted active source-semantic condition or route the same
record to a chronology-valid owner.

This is a local route cut.  It is not a received-line or bad-slope witness,
does not prove survival of the active first-match partition, does not exclude
all earlier owners, is not a KoalaBear MCA counterexample, and moves no ledger
quantity.

## 1. Exact field and witness

Put
\[
 c=1{,}923{,}159{,}404,\qquad
 E=\mathbf F_p[\omega]/(\omega^2-c).
\]
The certificate verifies \(c^{(p-1)/2}=-1\), so \(E\cong\mathbf F_{p^2}\).
Because \(2\mid6\), \(E\) is the unique quadratic subfield of the deployed
scalar field.

Use the six distinct row labels
\[
\begin{split}
(\alpha_0,\ldots,\alpha_5)=(&1{,}706{,}416{,}115,\,
294{,}572{,}568,\,
2{,}122{,}972{,}579,\\
&1{,}628{,}586{,}834,\,
1{,}566{,}096{,}308,\,
2{,}054{,}706{,}456).
\end{split}
\]
They lie in \(\mathbf F_p\), with
\[
 \alpha_3=\alpha_1^{-1},\qquad
 \alpha_5=\alpha_4^{-1}.
\]

For \(q\in E\), set
\[
 g_q(X)=X^2-qX+1.
\]
Along the labelled path
\[
 0-1-3-4-5-2
\]
take the seven consecutive factor parameters
\[
 (q_0,\ldots,q_6)
 =\omega(1,0,1168433532,962272901,
          914561315,1216145118,1646993078).
\]
All seven parameters are distinct, every \(q_j^2-4\) is nonzero, and every
\(g_{q_j}\) splits into two distinct roots in \(E\).

If row \(i\) occurs at path position \(j\), define
\[
 R_i(X)=g_{q_j}(X)g_{q_{j+1}}(X).
\]
The exact gcd degrees are
\[
 \deg\gcd(R_i,R_k)=
 \begin{cases}
 2,&\{i,k\}\text{ is a path edge},\\
 0,&\text{otherwise}.
 \end{cases}
\]
Thus the signature is exactly \(P_6\), rather than a degeneration with an
extra shared factor.

## 2. Exact degree-two and weighted-GRS reconstruction

Write
\[
 R_i(X)
 =X^4-S(\alpha_i)X^3+
   \bigl(2+P(\alpha_i)\bigr)X^2
   -S(\alpha_i)X+1,
\]
where
\[
\begin{split}
S(T)&=\omega\bigl(
190235001+50728375T+237946587T^2\bigr),\\
P(T)&=
1619401242+901515189T+1468071313T^2.
\end{split}
\]
Direct substitution verifies all twelve displayed \(S\)- and \(P\)-values.
The coefficient-map minor is
\[
 S_1P_2-S_2P_1=1259334169\,\omega\ne0,
\]
so the three coefficient vectors are independent and the image is the
nondegenerate conic chart required by the local reduction.

This also satisfies the exact weighted-GRS reconstruction, not merely an
unweighted six-label interpolation.  Let
\[
 d_i=\prod_{h\ne i}(\alpha_i-\alpha_h)
\]
and take scale polynomial \(A(T)=1\).  For every nonleading coefficient
\(r_{i,j}=[X^j]R_i\), \(0\le j\le3\), and every \(0\le m\le2\), the certificate
checks
\[
 \sum_{i=0}^5
 \frac{\alpha_i^m A(\alpha_i)r_{i,j}}{d_i}=0.
\]
Indeed \(r_{i,j}\) is the evaluation of a polynomial of degree at most two,
so the numerator has degree at most four; the identity follows from the
six-point Lagrange coefficient formula.  Equivalently,
\[
 H(T,X)=X^4-S(T)X^3+(2+P(T))X^2-S(T)X+1
\]
has bidegree at most \((2,4)\) and satisfies
\[
 H(\alpha_i,X)=R_i(X)
\]
for all six rows.

## 3. Source and reciprocal gates

Put
\[
 a=q_2,\qquad b=q_5,\qquad
 \mathcal K=\{0,a,-a,-b,b\}.
\]
The common decic
\[
 C_{\mathcal K}(X)=\prod_{q\in\mathcal K}g_q(X)
\]
is squarefree, even, palindromic, and coprime to \(X^2-1\).  Hence it is
invariant under both the deck map \(X\mapsto-X\) and the reciprocal
involution \(X\mapsto X^{-1}\), with no reciprocal fixed root.

The five common source labels are the roots of
\[
\begin{split}
A_{\mathcal K}(T)
 &=(T+1)
   \bigl(T^2+(2-a^2)T+1\bigr)
   \bigl(T^2+(2-b^2)T+1\bigr)\\
 &=T^5+735731088T^4+2104711620T^3\\
 &\qquad+2104711620T^2+735731088T+1.
\end{split}
\]
This polynomial is squarefree and splits in \(E\).  Its roots are disjoint
from the six \(\alpha_i\) and from the extra invariant label \(0\), giving
twelve distinct source labels in the deployed field.

The two free quadratics are \(g_{q_0}\) and \(g_{q_6}\).  Their coefficient
rows have cross product proportional to
\[
 (1,0,1),
\]
which is the nondegenerate involution \(X\mapsto X^{-1}\).  With right-label
permutation
\[
 (3,4,5,0,2,1),
\]
neither endpoint uses a diagonal pole incidence.  At endpoint \(i=0,2\), the
two selected source values \(u,v\) satisfy exactly
\[
 u+v=q_i^2-2,\qquad uv=1.
\]
Thus they are the squared deck fibre of the corresponding free pole
quadratic.

## 4. Exact implication and boundary

The construction proves consistency of the following local package:

1. deployed characteristic and scalar field;
2. twelve distinct deployed source labels;
3. split, reduced pole quadratics;
4. exact \(P_6\) common-signature graph;
5. bidegree-\((2,4)\) row reconstruction;
6. all twelve weighted-GRS parity equations;
7. nondegenerate conic coefficient image;
8. endpoint deck-fibre and no-diagonal conditions;
9. reciprocal common-decic and source-quintic gates.

It does **not** construct the active received line, its selected bad slope,
the final explaining polynomial, or a first-match record.  It therefore does
not prove that the component survives the complete K3 source semantics.
Likewise, the absence of an owner in this packet means only that no owner is
supplied; it is not a proof that every reviewed earlier owner is false.

The direct reciprocal-\(P_6\) emptiness route is nevertheless closed: any
valid elimination must use a condition outside items 1--9.  The maximal next
attack is to bind this exact local component to the active source producer
and then prove one of two outcomes:

- the producer or an earlier first-match gate forbids it; or
- the same line, slope, and graph record enters a chronology-valid paid
  owner.

The other reciprocal endpoint orbits, the \(D_4/D_5\) components,
\(P_2\sqcup C_4\), and the simple and repeated quartic branches remain open.
No active \(U_{\rm paid}\), \(U_Q\), \(U_{\rm BC}\), or \(U_{\rm new}\) is
changed.

## 5. Replays

```bash
python3 \
  experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.py \
  --check
python3 \
  experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.py \
  --tamper-selftest
sage \
  experimental/scripts/verify_kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.sage
```

The Python verifier implements \(\mathbf F_{p^2}\) arithmetic independently
and binds the canonical JSON payload.  The Sage replay reconstructs the
finite field, all polynomial identities, the twelve weighted-GRS checks, and
the complete source-label set.
