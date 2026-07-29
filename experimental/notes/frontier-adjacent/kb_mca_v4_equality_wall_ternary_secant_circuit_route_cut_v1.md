---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: There is an exact abstract 69-record F_p-valued carrier family at the KoalaBear-scale numerical profile with constant support 981105, affine and secant rank eight, pair exchange at least 121284, pair secant distance at least 1053746, all 3280 projective ternary secants of distance at least 1052958, sixty canonical bounded circuits, no singleton circuit atoms, and every printed circuit restriction-rank bound. These explicitly listed weakened consequences do not imply cap 68 or constitute source-bound owner evidence; the arbitrary-coefficient secant-span distance is not certified.
architecture: null
partition_digest: null
atom_or_cell: K3_ABSTRACT_COARSE_INVARIANT_ROUTE_CUT
quantifier: one explicit abstract 69-record q-ary carrier family; not an actual GRS subcode, locator family, received line, or selector
projection_and_unit: abstract F_p-valued carrier records; not deployed slopes, a received line, or rational source-map classes
claimed_bound: no charge and no endpoint movement
status: PROVED_ROUTE_CUT_ROW_OPEN
impact: PAIRWISE_TERNARY_SECANT_SUPPORT_RANK_CIRCUIT_CAP68_ROUTE_REFUTED
falsifier: failure of any exact carrier, support, affine-rank, secant-rank, pair-distance, projective-ternary-distance, pair-exchange, circuit-minimality, no-singleton, or restriction-rank check in the committed certificate
replay: python3 experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.py --check
---

# KoalaBear equality-wall ternary-secant/circuit route cut

## 0. Verdict

The current consolidated K3 status leaves \(405\) labelled conic cases and
has no active \(U_{\rm paid}\) or witness-exhaustive partition.  A tempting
compression of that residual would try to force a cap of \(68\) records from
the following coarse numerical package:

\[
|V|=1{,}894{,}736,\qquad |Y_i|=981{,}105,
\tag{0.1}
\]

\[
\dim K_0=8,\qquad
d(K_V)=1{,}048{,}577,\qquad
|Y_i\setminus Y_j|\ge67{,}472,
\tag{0.2}
\]

and at least \(60\) bounded fundamental circuits with no singleton support
atom and

\[
\operatorname{rank}(K_0|_{Z_C})\le10-|C|.
\tag{0.3}
\]

This note gives an exact \(69\)-record abstract carrier family satisfying
the numerical support, affine/secant-rank, selected-pair distance,
projective ternary-secant distance, exchange, bounded-circuit,
no-singleton, and restriction-rank consequences.  It does **not** verify
the minimum distance of every arbitrary linear combination in the
eight-dimensional secant span.  Thus it does not satisfy the full
\(K_0\subseteq K_V\) consequence in (0.2).

The explicitly verified weakened consequences alone cannot prove cap
\(68\) and do not constitute source-bound owner evidence.  A valid closing
theorem must use the
full arbitrary-coefficient GRS-span statement or other structure omitted
here: split locator factorization, the source quotient and its
degree/cocycle, the primitive Hilbert--Burch module, or a same-record
active-owner predicate.

This is a route cut for a weakened implication.  It is not a counterexample
to the full primitive \(69\)-point theorem, is not a Reed--Solomon or MCA
counterexample, and books no charge.

## 1. Exact deployed constants

Put

\[
p=2{,}130{,}706{,}433,\qquad
n=2{,}097{,}152,\qquad k=1{,}048{,}576,
\tag{1.1}
\]

\[
N=|V|=1{,}894{,}736,\qquad
J=981{,}105,\qquad
Z=N-J=913{,}631,
\tag{1.2}
\]

\[
d_{\mathrm{GRS}}=1{,}048{,}577,\qquad
c=d_{\mathrm{GRS}}-J=67{,}472.
\tag{1.3}
\]

The full equality-wall route would require an actual inclusion
\(K_0\subseteq K_V\), where the intended shortened carrier code has
parameters

\[
K_V=[1{,}894{,}736,846{,}160,1{,}048{,}577]_F.
\tag{1.4}
\]

The construction below reproduces the distance threshold for every
selected pair and every projective ternary coefficient direction.  It does
not reproduce that threshold for every coefficient in
\(\mathbf F_p^8\), and it does not construct an embedding into the GRS
code (1.4).  Both distinctions are load-bearing.

The active row authority currently has
\[
U_{\rm paid}=\texttt{null},\qquad
\text{partition digest}=\texttt{null}.
\tag{1.5}
\]
This packet does not instantiate either field.

## 2. The exact affine carrier family

For \(r\in\{0,\ldots,255\}\), let

\[
b_r=(b_{r,0},\ldots,b_{r,7})\in\{\pm1\}^8,\qquad
b_{r,j}=(-1)^{\operatorname{bit}_j(r)}.
\tag{2.1}
\]

Use the \(69\) record indices

\[
\mathcal R=\{0,1,\ldots,67,128\}.
\tag{2.2}
\]

The certificate contains \(225\) exact coordinate types

\[
(u_\alpha,h_\alpha,m_\alpha),
\qquad
u_\alpha\in\{-1,0,1\}^8,\quad
h_\alpha\in\mathbf Z,\quad
m_\alpha\in\mathbf Z_{>0},
\tag{2.3}
\]

with

\[
\sum_{\alpha=1}^{225}m_\alpha=N.
\tag{2.4}
\]

Repeat coordinate type \(\alpha\) exactly \(m_\alpha\) times and set

\[
F_r(\alpha)=\langle b_r,u_\alpha\rangle-h_\alpha
\in\mathbf F_p.
\tag{2.5}
\]

We view these values inside \(\mathbf F_{p^6}\) through the canonical
base-field embedding.  Scalar extension preserves the Hamming weights
computed below and the displayed \(\mathbf F_p\)-ranks; it does not create a
GRS evaluation-code embedding.

Define its support and zero set by

\[
Y_r=\{\alpha:F_r(\alpha)\ne0\},
\qquad
Z_r=V\setminus Y_r,
\tag{2.6}
\]

counting every type with multiplicity \(m_\alpha\).

The exact certificate verifies, for every \(r\in\mathcal R\),

\[
|Z_r|=913{,}631,\qquad
|Y_r|=981{,}105.
\tag{2.7}
\]

Because (2.5) is affine-linear in \(b_r\), define the abstract secant space

\[
K_0^{\mathrm{abs}}
=\operatorname{span}\{F_r-F_0:r\in\mathcal R\}.
\tag{2.8}
\]

It has dimension eight.  The first independent star edges in the fixed
record order are

\[
1,2,4,8,16,32,64,128,
\tag{2.9}
\]

and their evaluation matrix has rank exactly eight over \(\mathbf F_p\).
The full vertex-function span has rank nine: the affine offset is a ninth
direction.  Thus

\[
\dim K_0^{\mathrm{abs}}=8,
\qquad
\dim\operatorname{span}\{F_r:r\in\mathcal R\}=9.
\tag{2.10}
\]

## 3. Exact selected-pair and ternary-secant thresholds

For \(r\ne s\), the certificate computes the complete q-ary Hamming
distance

\[
d_{rs}
=
\#\{x\in V:F_r(x)\ne F_s(x)\}.
\tag{3.1}
\]

Across all

\[
\binom{69}{2}=2{,}346
\tag{3.2}
\]

pairs, the maximum number of equal coordinates is \(840{,}990\).
Consequently

\[
\boxed{
\min_{r\ne s}d_{rs}
=1{,}894{,}736-840{,}990
=1{,}053{,}746
}
\tag{3.3}
\]

and hence

\[
\min_{r\ne s}d_{rs}-d_{\mathrm{GRS}}
=5{,}169.
\tag{3.4}
\]

The directed support exchange is also computed without sampling:

\[
\Delta_{rs}=|Y_r\setminus Y_s|
=|Y_s\setminus Y_r|.
\tag{3.5}
\]

Its exact extrema are

\[
\boxed{
121{,}284
\le\Delta_{rs}\le
616{,}161.
}
\tag{3.6}
\]

Thus every pair clears the deployed exchange floor with margin

\[
121{,}284-67{,}472=53{,}812.
\tag{3.7}
\]

The model also has the correct exchange-support implication: on every
coordinate in \(Y_r\triangle Y_s\), exactly one value is zero, so
\(F_r-F_s\ne0\).  It does not assert that the secant support equals the
symmetric difference.  Common-support coordinates may also contribute to
(3.1), exactly as they do in the actual equality-wall equations.

There are exactly

\[
\frac{3^8-1}{2}=3{,}280
\tag{3.8}
\]

projective directions \(a\in\{-1,0,1\}^8/\{\pm1\}\).  The verifier
enumerates every one and evaluates the secant word

\[
x\longmapsto \langle a,u_x\rangle .
\tag{3.9}
\]

The largest zero count is \(841{,}778\), attained first at

\[
a=(1,0,0,0,0,0,0,1).
\tag{3.10}
\]

Therefore

\[
\boxed{
\min_{a\in\{-1,0,1\}^8/\{\pm1\}}
\operatorname{wt}\langle a,u_\bullet\rangle
=1{,}052{,}958
=d_{\mathrm{GRS}}+4{,}381.
}
\tag{3.11}
\]

Equation (3.11) is an exhaustive finite statement about the declared
ternary directions.  It is **not** a minimum-distance theorem for all
nonzero \(a\in\mathbf F_p^8\).

## 4. Sixty canonical bounded circuits

Root the star at \(r=0\).  For every nonbasis selected index \(r\), let
\(S(r)\) be its set of one-bits and \(h=|S(r)|\).  Then

\[
F_r-\sum_{j\in S(r)}F_{2^j}+(h-1)F_0=0.
\tag{4.1}
\]

The coefficients in (4.1) are nonzero and sum to zero.  The participating
star secants are independent, so (4.1) is a minimal affine circuit of size
\(h+2\).  The \(60\) canonical circuits have exact histogram

\[
\begin{array}{c|rrrrr}
|C|&4&5&6&7&8\\ \hline
\#C&17&21&15&6&1.
\end{array}
\tag{4.2}
\]

There are no affine three-circuits among the \(69\) vertices.

At any carrier coordinate, if exactly one record in a circuit were
nonzero, evaluating (4.1) would leave one nonzero term.  Therefore every
canonical circuit has no singleton support atom.

For a circuit \(C\), let

\[
Z_C=\bigcap_{r\in C}Z_r.
\tag{4.3}
\]

All \(m-2\) independent circuit secants vanish on \(Z_C\).  Direct
finite-field matrix replay gives

\[
\boxed{
\operatorname{rank}(K_0^{\mathrm{abs}}|_{Z_C})\le10-|C|
}
\tag{4.4}
\]

for every canonical circuit.  The exact restriction-rank histogram is

\[
\begin{array}{c|rrrrrr}
\text{rank}&1&2&3&4&5&6\\ \hline
\#C&0&13&15&7&10&15.
\end{array}
\tag{4.5}
\]

The common-zero cardinalities range from \(198{,}347\) to \(427{,}173\).
All relations, deletions, carrier atoms, common-zero sets, and ranks are
recomputed in both the primary Python verifier and the independent Sage
replay.

## 5. Exact route cut

The construction proves:

> **Pairwise/ternary-secant circuit route cut.**  The listed
> KoalaBear-scale values of
> \(N,J,c\), affine and secant rank eight, selected-pair q-ary distance at
> least \(1{,}048{,}577\), the same threshold for all \(3{,}280\)
> projective ternary directions, pairwise exchange at least \(c\), sixty
> canonical minimal circuits of size at most ten, no singleton carrier
> atoms, and all inequalities
> \[
> \operatorname{rank}(K_0|_{Z_C})\le10-|C|
> \]
> do not imply cap \(68\) and do not constitute source-bound owner
> evidence.

This cuts off proposed proofs based only on the stated constant support,
selected-pair/ternary Hamming checks, pair exchange, affine rank, bounded
circuits, or their restriction-rank numerology.  It does not cut an
argument that genuinely uses the minimum distance of every nonzero word in
\(K_0\).  A further standalone binary Plotkin calculation is also
inapplicable: the q-ary secant may be nonzero on
\(Y_i\cap Y_j\), so its Hamming weight is not
\(|Y_i\triangle Y_j|\).

The next valid theorem must use at least one load-bearing input omitted by
the countermodel:

1. the full arbitrary-coefficient minimum-distance statement for the
   secant space, as supplied by actual membership in the deployed GRS
   evaluation code;
2. monic split locators and
   \(F_i=\Lambda_{Z_i}A_i^{\mathrm{src}}\);
3. the full-domain source-unit reciprocal parameter;
4. the polynomial quotients \(T_{ij}\), their degree bounds, exchange-root
   avoidance, and exact cocycle;
5. the primitive Hilbert--Burch presentation of the residue-line module;
   or
6. a same-line, same-slope, same-graph-record active owner.

This is the precise reason another standalone bounded-circuit incidence
computation cannot close the row.  A positive K3 theorem must instead
classify the full \(405\)-case residual using one of these load-bearing
inputs and then supply chronology-correct ownership and aggregation.

## 6. Construction status and nonclaims

The coordinate multiplicities were found by a continuous incidence
optimization followed by a direct singleton/empty-fibre integer
correction.  That optimization is not part of the proof.  The committed
witness is a sealed finite list, and the proof is the exact reconstruction
and exhaustive verification of all records, selected pairs, projective
ternary directions, and circuits.

A \(300{,}000\)-sample rank-seven search found no arbitrary-coefficient
word below (3.11), while CP-SAT and SCIP did not certify the first bounded
cofactor chart within their time limits.  These are empirical diagnostics,
not proof.  They are preserved as a failed full-span closure attempt under
`experimental/dead_ends/kb_mca_v4_full_span_hyperplane_closure_v1/`.

The construction does **not** provide:

- an embedding into the actual shortened GRS carrier code;
- a minimum-distance certificate for every arbitrary coefficient in
  \(K_0^{\mathrm{abs}}\);
- evaluation points or low-degree carrier polynomials;
- split locators or source cofactors;
- a source quotient, degree bound, or Hilbert--Burch module;
- a received line, selector, affine bad slope, or rational source-map
  class;
- source-bound owner evidence, a first-match payment, cap \(68\), or row
  closure.

Index \(128\) is an affine coloop relative to the other \(68\) selected
cube vertices and belongs to none of the canonical circuits.  The histogram
(4.2) counts the fixed \(60\) star fundamental circuits, not every minimal
circuit in the vertex configuration.

The rejected predecessor that omitted even the selected-pair distance
threshold is
preserved under
`experimental/dead_ends/kb_mca_v4_circuit_only_route_cut_v0/`.

## 7. Ledger

The live authority has \(U_{\mathrm{paid}}=\texttt{null}\), no active
partition digest, and therefore no defined post-\(U_{\mathrm{paid}}\)
remaining budget.  This packet preserves those nulls and adds exactly zero
charge.  It proves no \(U_Q\), no \(U_{BC}\), no \(U_{\mathrm{new}}\), and
no KoalaBear endpoint.

The certificate binds the current `agents.md`, the manually consolidated
K3 status in `experimental/experiments.tex`, and the live four-row
exact-completion certificate.  It checks semantically that the KoalaBear
row is open, \(U_{\mathrm{paid}}\) and the exhaustive partition are null,
the residual has \(405\) labelled conic cases, and the exact row parameters
and budget match.

## 8. Replay

```bash
python3 experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.py --check
python3 -O experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.py --tamper-selftest
sage experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.sage
```

The Python verifier performs \(960{,}747\) explicit checks, including every
one of the \(2{,}346\) pairs, all \(3{,}280\) projective ternary
directions, and every coordinate of every canonical circuit.  Its tamper
suite rejects \(42/42\) mutations, including duplicate keys, noncanonical
bytes, nonfinite constants, and trailing data.  Sage independently performs
\(44{,}493\) checks and reconstructs the finite-field ranks and all
pair/ternary/circuit inequalities.

# PROVED ROUTE CUT / KOALABEAR ROW OPEN
