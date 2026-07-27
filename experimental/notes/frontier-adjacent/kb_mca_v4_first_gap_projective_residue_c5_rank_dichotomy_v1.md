---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: At the first open full-outside slack, the source residue line either has one base-rational projective point, so all admitted complement locators share the same projective residue and exchange at least 134944 roots, or it is base-defined and the post-C5 residual has a canonical reciprocal multiplier matrix with kernel dimension at least three.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_ADAPTER_V1
partition_digest: aede55b9409dd7c1407e626da09179ef48a00c52dc4a5cf272757cea1a804d4c
atom_or_cell: UNPAID_FIRST_GAP_SELECTED_BASIS_SOURCE_RESIDUE_PACKING
quantifier: Uniform for every received line and every selector rebuilt after the six active owner deletions at the first open full-outside slack
projection_and_unit: Distinct bad finite slopes per received line; complement-locator projective residues and one canonical base-field reciprocal rank matrix
claimed_bound: Exact one-point-or-rank-excess dichotomy; no slope charge
status: PROVED
impact: ROUTE_CUT
falsifier: A surviving first-gap source residue line with at least two base-rational projective points and reciprocal kernel dimension two, or two locators in its one-point branch with Johnson exchange below 134944
replay: python3 experimental/scripts/verify_kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.py --check
---

# KoalaBear first-gap projective residue C5/rank dichotomy

## Status

**PROVED SOURCE-BOUND DICHOTOMY / ZERO LEDGER MOVEMENT / RECIPROCAL
RANK PAYMENT OPEN.**

The first-gap complement-locator theorem places every admitted split locator
in one two-dimensional residue space \(W_\Sigma\). This note proves that the
base-field nature of the split locators has a sharp consequence:

\[
\boxed{
\begin{array}{c}
\text{all admitted locators lie at one projective residue point}\\
\text{and distinct locators exchange at least }2e
\end{array}}
\quad\text{or}\quad
\boxed{
\dim_B\mathcal R(q_0,q_1)\ge3.}
\tag{0.1}
\]

Here \(\mathcal R(q_0,q_1)\) is one canonical, base-field reciprocal
multiplier kernel. Its generic dimension is two. If it has dimension two,
the translated source pair descends projectively to \(B=\mathbf F_p\), and
the already-paid active C5 owner deletes the entire incoming residual. Thus
only genuine reciprocal rank excess can support a post-C5 residue line with
more than one base-rational projective direction.

This is not a payment for that rank excess and does not close the
determinant-weighted packing theorem. It replaces the unsupported shortcut

```text
local base-defined residue line => C5
```

by the exact implication

```text
local base-defined residue line
+ generic reciprocal rank
=> pair-global projective descent
=> active C5.
```

## 1. Frozen first-gap data

Use

\[
B=\mathbf F_p,\qquad F=\mathbf F_{p^6},
\qquad p=2{,}130{,}706{,}433,
\]

\[
e=67{,}472,\qquad
s=|\Sigma|=2e=134{,}944.
\tag{1.1}
\]

The source points lie in \(B\). Put

\[
\Lambda_\Sigma(X)=\prod_{h\in\Sigma}(X-h),
\]

\[
A_B=B[X]/(\Lambda_\Sigma),\qquad
A_F=F[X]/(\Lambda_\Sigma)
     \simeq F\otimes_B A_B.
\tag{1.2}
\]

Let \(U_B\subset A_B\) be the evaluation image of
\(B[X]_{\le e}\), and put \(U_F=F\otimes_B U_B\). Then

\[
\dim_B A_B=2e,\qquad
\dim_B U_B=e+1,\qquad
\operatorname{codim}_{A_B}U_B=e-1.
\tag{1.3}
\]

For the fixed carrier \(V\) and translated source pair
\((\epsilon _0,\epsilon _1)\), define

\[
u_i=\Lambda_V^{-1}\epsilon_i\in A_F,\qquad i=0,1.
\tag{1.4}
\]

The proved complement-locator linearization gives

\[
W_\Sigma
=\{q\in A_F:q u_0\in U_F,\ q u_1\in U_F\},
\qquad
\dim_F W_\Sigma=2.
\tag{1.5}
\]

Every actual complement locator \(Y\subset V\) is supported on base-field
points, so

\[
q_Y=[\Lambda_Y]\in A_B^\times.
\tag{1.6}
\]

It is source-admissible exactly when \(q_Y\in W_\Sigma\).

The qualifying first-gap record is coefficient-rank two. Equivalently,
\(u_0,u_1\) are \(F\)-linearly independent: multiplication by the unit
\(q_Y\) carries them to the actual coprime, rank-two reduced source pair.

## 2. Projective rational-point dichotomy

Write

\[
\mathbf P_B(W_\Sigma)
=\{[q]\in\mathbf P(W_\Sigma):[q]\text{ has a representative in }A_B\}.
\tag{2.1}
\]

### Theorem 2.1

For any two-dimensional \(F\)-subspace \(W\subset F\otimes_B A_B\),

\[
\boxed{
\#\mathbf P_B(W)\in\{0,1,p+1\}.}
\tag{2.2}
\]

If it contains two distinct points represented by \(q_0,q_1\in A_B\), then

\[
\boxed{
W=Fq_0\oplus Fq_1
=F\otimes_B(Bq_0\oplus Bq_1)}
\tag{2.3}
\]

and

\[
\boxed{
\mathbf P_B(W)=\mathbf P(Bq_0\oplus Bq_1)
\simeq\mathbf P^1(B).}
\tag{2.4}
\]

#### Proof

Distinct projective points give \(F\)-linearly independent representatives,
so they form an \(F\)-basis of \(W\), proving the first equality in (2.3).
They are also \(B\)-linearly independent.

Extend \(q_0,q_1\) to a \(B\)-basis of \(A_B\). If

\[
q=a q_0+b q_1\in A_B,\qquad a,b\in F,
\]

then the two coordinates of the base-field vector \(q\) in that extended
basis are \(a,b\). Hence \(a,b\in B\). Thus every base-rational point of
\(\mathbf P(W)\) is represented by a nonzero \(B\)-linear combination of
\(q_0,q_1\), and every such combination is in \(W\). This proves (2.4).
The projective line over \(B\) has \(p+1\) points. If there are not two
distinct base-rational points, the intersection has size zero or one.
\(\square\)

Because an actual first-gap line supplies at least one \(q_Y\), only the
one-point and \(p+1\)-point alternatives occur on a nonempty active record.

## 3. Reciprocal multiplier kernel

Assume now that \(W_\Sigma\) has two base-rational points and choose a
base-field basis \(q_0,q_1\in A_B\). Define

\[
\boxed{
\mathcal R(q_0,q_1)
=\{v\in A_B:q_0v\in U_B,\ q_1v\in U_B\}.}
\tag{3.1}
\]

This is the **reciprocal multiplier kernel**. Its scalar extension is

\[
\mathcal R_F(q_0,q_1)
=\{v\in A_F:q_0v\in U_F,\ q_1v\in U_F\}.
\tag{3.2}
\]

Since \(q_0,q_1\in W_\Sigma\), equations (1.5) give

\[
u_0,u_1\in\mathcal R_F(q_0,q_1).
\tag{3.3}
\]

Their independence therefore proves

\[
\boxed{\dim_B\mathcal R(q_0,q_1)\ge2.}
\tag{3.4}
\]

### Exact matrix

Let \(H_e\) be any \((e-1)\)-row base-field parity matrix for \(U_B\):

\[
U_B=\ker H_e.
\]

In source-value coordinates,

\[
\boxed{
\mathsf M(q_0,q_1)=
\begin{pmatrix}
H_e\operatorname{diag}(q_0)\\
H_e\operatorname{diag}(q_1)
\end{pmatrix}
\in B^{(2e-2)\times2e}.}
\tag{3.5}
\]

Then

\[
\ker_B\mathsf M(q_0,q_1)=\mathcal R(q_0,q_1).
\tag{3.6}
\]

The matrix has \(2e-2\) rows and \(2e\) columns. Thus the generic rank
contract is

\[
\operatorname{rank}_B\mathsf M(q_0,q_1)=2e-2,
\qquad
\dim_B\mathcal R(q_0,q_1)=2.
\tag{3.7}
\]

The alternative

\[
\boxed{
\dim_B\mathcal R(q_0,q_1)\ge3
\iff
\operatorname{rank}_B\mathsf M(q_0,q_1)\le2e-3}
\tag{3.8}
\]

is therefore an exact, baseline-free collective rank precursor. It is
constructed from the actual source chart and the actual residue line, not
from one witness's automatic interpolation equation.

## 4. Generic reciprocal rank forces C5

### Theorem 4.1

Suppose

\[
\dim_B\mathcal R(q_0,q_1)=2.
\tag{4.1}
\]

Then the fixed translated source pair is projectively defined over \(B\).
Consequently the active C5 owner removes the complete incoming residual.

#### Proof

Choose a \(B\)-basis \(v_0,v_1\) of \(\mathcal R(q_0,q_1)\). By (3.3),
\(u_0,u_1\) belong to its scalar extension. Their independence makes them
another basis, so there is \(C\in\operatorname{GL}_2(F)\) with

\[
[u_0\ u_1]=[v_0\ v_1]C.
\tag{4.2}
\]

Multiply pointwise on \(\Sigma\) by the base-valued unit \(\Lambda_V\), and
extend the two resulting vectors by zero off \(\Sigma\). Put

\[
R_i=\mathbf1_\Sigma\Lambda_Vv_i\in B^D,\qquad i=0,1.
\tag{4.3}
\]

Equations (1.4) and (4.2) give

\[
[\epsilon _0\ \epsilon _1]=[R_0\ R_1]C.
\tag{4.4}
\]

The original received pair differs from the translated source pair by two
explaining codewords. This is a syndrome gauge, so (4.4) gives a
base-field definition of the global syndrome plane. If its syndrome rank is
zero, the source theorem leaves no noncontained exact-witness residual. If
the rank is positive, its intrinsic projective syndrome field is \(B\).
The already-paid pair-global active C5 owner is witness-exhaustive on that
stratum and deletes the complete incoming residual.

Either case contradicts a later surviving first-gap record. \(\square\)

The proof uses the pair-global source vectors (4.3). Merely observing a
support-local \(B\)-subline would not be enough and is expressly excluded by
the active C5 contract.

## 5. Post-C5 one-point-or-rank-excess theorem

Combine Theorems 2.1 and 4.1.

### Corollary 5.1

Every nonempty first-gap residue line surviving the active C5/base owner
satisfies exactly one of the following useful alternatives:

1. \(\mathbf P_B(W_\Sigma)\) has one point; or
2. \(W_\Sigma\) is base-defined and, for a canonical base-field basis,
   \[
   \boxed{\dim_B\mathcal R(q_0,q_1)\ge3.}
   \tag{5.1}
   \]

This is the **one-point-or-rank-excess** dichotomy.

A canonical basis in the second branch can be obtained by row-reducing
\(W_\Sigma\cap A_B\) in the fixed monomial coordinate order. Therefore the
rank matrix (3.5) is verifier-checkable and does not depend on an arbitrary
choice of two selected slopes or locators.

## 6. Consequence for split-locator packing

Every complement-locator residue \(q_Y\) is base-rational. In the one-point
branch, all admitted locators therefore satisfy

\[
[\Lambda_Y]=[\Lambda_{Y'}]\quad\text{in }A_\Sigma
\tag{6.1}
\]

for one common projective residue point.

The proved projective residue collision theorem now applies to every pair:
if \(Y\ne Y'\), then

\[
\boxed{
|Y\setminus Y'|
=|Y'\setminus Y|
\ge2e=134{,}944.}
\tag{6.2}
\]

This is stronger than the previously available global statement, which gave
the \(2e\) floor only after two locators were already known to occupy the
same projective residue bucket.

In the rank-excess branch, (6.2) need not hold across different projective
points. Instead the exact matrix (3.5) is the emitted structural datum. A
valid downstream owner must:

1. contain one of the same surviving slopes reconstructed from this source
   line;
2. use rank relative to the generic reciprocal contract (3.7), not the
   automatic per-witness interpolation rank;
3. print a distinct-slope projection bound; and
4. perform whole-slope deletion before rebuilding the next selector.

The rank-excess branch is not paid in this packet.

## 7. Reciprocal rational normal form

The reciprocal rank defect is not an arbitrary matrix defect. It has an
exact low-degree rational normal form.

Take two distinct **occupied** residue points

\[
q_i=[\Lambda_{Y_i}]\in W_\Sigma\cap A_B^\times,
\qquad i=0,1,
\tag{7.1}
\]

and put

\[
r=\dim_B\mathcal R(q_0,q_1).
\]

Assume \(r\ge3\). For \(v\in\mathcal R(q_0,q_1)\), let
\((R_v,S_v)\in B[X]_{\le e}^2\) be the unique polynomial representatives of

\[
(q_0v,q_1v)\in U_B^2.
\tag{7.2}
\]

These pairs form an \(r\)-dimensional graph space \(\mathcal G\).

### Theorem 7.1

There is a coprime pair \(A,B\in B[X]\), unique up to a common nonzero
scalar, such that

\[
\boxed{
\mathcal G
=\{(AT,BT):T\in B[X]_{\le e-d}\},}
\tag{7.3}
\]

where

\[
\boxed{
d=\max(\deg A,\deg B)=e-r+1\le e-2.}
\tag{7.4}
\]

In particular,

\[
\boxed{
\frac{q_1}{q_0}=\frac BA
\quad\text{on }\Sigma.}
\tag{7.5}
\]

#### Proof

The degree-\(e\) leading-coefficient map

\[
\mathcal G\longrightarrow B^2
\]

has a nonzero kernel because \(\dim\mathcal G=r\ge3\). Choose a nonzero
\((R_*,S_*)\) in that kernel, so both polynomials have degree at most
\(e-1\).

For any \((R,S)\in\mathcal G\), the determinant

\[
R_*S-S_*R
\]

vanishes at all \(2e\) points of \(\Sigma\). Its degree is at most
\((e-1)+e=2e-1\), so it is the zero polynomial.

Write

\[
R_*=GA,\qquad S_*=GB,\qquad\gcd(A,B)=1.
\]

Then \(AS=BR\). Coprimality gives

\[
R=AT,\qquad S=BT
\]

for a polynomial \(T\), and the degree bound gives
\(\deg T\le e-d\). Conversely, every such pair has the same pointwise ratio
as \((R_*,S_*)\), hence as \(q_1/q_0\), on \(\Sigma\), so it belongs to
\(\mathcal G\). Thus

\[
r=\dim\mathcal G=e-d+1,
\]

so, equivalently, `d=e-r+1`. This proves (7.3)--(7.5). \(\square\)

### Corollary 7.2: large exchange or low-degree root swap

Let

\[
C=Y_0\cap Y_1,\qquad
P_i=\Lambda_{Y_i\setminus C},\qquad
\Delta=|Y_0\setminus Y_1|.
\]

Equation (7.5) gives

\[
\Lambda_\Sigma
\mid AP_1-BP_0.
\tag{7.6}
\]

Therefore exactly one of the following holds:

1. the polynomial in (7.6) is nonzero, and
   \[
   \boxed{
   \Delta\ge2e-d=e+r-1;}
   \tag{7.7}
   \]
2. it is zero, and
   \[
   \boxed{
   AP_1=BP_0,\qquad
   P_0\mid A,\quad P_1\mid B,\quad
   \Delta\le d.}
   \tag{7.8}
   \]

Indeed, the degree in the nonzero case is at most \(d+\Delta\), which must
be at least \(\deg\Lambda_\Sigma=2e\). In the zero case, \(P_0,P_1\) are
coprime because their root sets are disjoint. Equation (7.8) follows by
Euclid's lemma.

Thus reciprocal rank excess has no diffuse middle-distance branch. It is
either a stronger constant-weight separation, or an exact root exchange
supported on one low-degree rational pencil. At the deployed first gap,
\(r\ge3\) makes the large-exchange floor at least

\[
e+2=67{,}474.
\tag{7.9}
\]

The low-degree root swap is a canonical planted/rational precursor, but this
packet does not claim that the current active source-rational owner already
pays it. That owner is defined from the received source-coordinate map,
whereas (7.5) is a ratio of complement-locator residue directions. A
same-slope adapter is still required.

## 8. Finite exact controls

The verifier contains three independent controls.

### 8.1 Rational projective points

It exhausts every projective line in

\[
\mathbf P^2(\mathbf F_9)
\]

relative to the embedded Baer subplane
\(\mathbf P^2(\mathbf F_3)\). Among the \(91\) lines, exactly \(13\) are
base-defined and contain \(4=p+1\) base points; the other \(78\) contain one
base point. Thus the checked histogram is

```text
base-rational points  line count
1                     78
4                     13
```

This is finite verification of the two nonempty alternatives in (2.2).

### 8.2 Reciprocal rank

Over \(\mathbf F_{17}\), with \(e=3\) and six source points, the verifier
builds the exact matrix (3.5). A quadratic unit multiplier gives the generic
kernel dimension two. A linear unit multiplier gives kernel dimension three,
demonstrating the exact rank-excess gate.

### 8.3 Exhaustive split-locator rank-excess controls

Two rows exhaust every pair of complement locators and verify Theorem 7.1
and Corollary 7.2.

For

```text
F_23, e=3, j=4:
  complement locators                         56
  reciprocal dimension 2 pairs             1,120
  reciprocal dimension 3 pairs               420
  rank-excess rational degree 1 pairs         420
  exact one-root swaps                        420
```

For

```text
F_31, e=4, j=5:
  complement locators                        210
  reciprocal dimension 2 pairs             9,975
  reciprocal dimension 3 pairs             9,450
  reciprocal dimension 4 pairs             2,520
  rational degree 2 / 1 pairs        9,450 / 2,520
  exact low-degree swaps                   11,970
```

Every rank-excess pair in these rows is in the exact low-degree swap branch;
the maximum exchanges are respectively one and two. This is useful evidence
that the close-pair obstruction is algebraic rather than a failure of the
large-exchange estimate. It is not a deployed owner census.

### 8.4 Existing source controls

The verifier rebuilds the exhaustive \(F_{17},e=2,j=6\) complement-locator
domain and the same structured plus deterministic-random source cases used
by the residue packet. For every case it:

1. reconstructs the two-dimensional source residue line;
2. chooses its base-field kernel basis;
3. builds the reciprocal matrix;
4. verifies that both actual source coordinates lie in its kernel; and
5. records the exact reciprocal-kernel dimension.

These are finite controls, not a deployed rank-payment theorem.

## 9. Exact remaining target

The determinant-weighted source-bound bridge is now split into two sharply
different obligations.

### Branch A: one residue point

Use the global exchange floor (6.2), together with the actual eight-row
outlier basis, richness \(J_B\), and source splitting, to prove

\[
\sum_B(J_B-20)_+
\le E_{\max}^{\rm active}.
\tag{8.1}
\]

Ordinary constant-weight packing alone is unlikely to reach (8.1); the
bordered-minor and split-locator coupling must remain attached.

### Branch B: reciprocal rank excess

Convert

\[
\operatorname{rank}_B\mathsf M(q_0,q_1)\le2e-3
\tag{8.2}
\]

into a canonical active owner with a same-slope projection and payment. The
normal form in Section 7 splits this further:

* a low-degree exact root swap (7.8), which should emit a canonical planted
  or rational owner after proving the same-slope adapter;
* the large-exchange branch (7.7), which should be combined with the
  bordered-minor outlier basis rather than paid as an abstract rank defect;
* a common divisor or degree defect, already routed by the residue admission
  dichotomy;
* a proper-field or Frobenius-stable reciprocal kernel, routed through the
  active C5/Frobenius owners; or
* a genuinely baseline-free collective rank cell whose minors admit an
  exact slope count.

The note proves neither (8.1) nor the payment in (8.2). The active ledger and
partition digest are unchanged.

## 10. Guardrails

Do not use this result to claim:

* that every local base-defined pencil is C5-owned;
* that reciprocal rank excess is automatically a paid rank cell;
* that \(p+1\) is an upper bound for all rich graph lines;
* that the \(2e\) exchange floor alone is budget-fitting;
* that arbitrary residue-line incidence controls determinant weights; or
* that the KoalaBear row is closed.

The exact new boundary is:

\[
\boxed{
\text{post-C5 first-gap residue line}
\Longrightarrow
\begin{cases}
\text{one rational residue point and global }2e\text{ exchange},\\
\text{or one canonical reciprocal rank defect.}
\end{cases}}
\]

# PROVED
