---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: After the active tangent and intrinsic deep-MCA owners, one pair-global bounded-degree source-rational image owns at most 2078733 further bad finite slopes; Q, balanced core, and final residual remain exact set differences.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_ADAPTER_V1
partition_digest: 5f5ff58ad53c76fd522b4ee45dd9966c1f982fab788fa5de95b917945679760f
atom_or_cell: U_paid=SOURCE_COORDINATE_TANGENT_IMAGE+ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER+ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
quantifier: Uniform over every admissible received line over F_(p^6)
projection_and_unit: Distinct bad finite slopes per received line
claimed_bound: U_paid=3409363
status: PROVED
impact: BANKABLE_ATOM
falsifier: Failure of source-map uniqueness, pair-globality, image cap, fixed-translation compatibility, or exact first-match exhaustion.
replay: python3 experimental/scripts/verify_kb_mca_v4_tangent_deep_source_rational_adapter_v1.py --check
---

# KoalaBear v4 tangent-deep-source-rational adapter

**PROVED DIRECT ACTIVE-V4 OWNER EXTENSION / BANKABLE ATOM / ROW OPEN.**

This packet adds one selector-free source-rational owner to the proved
tangent-plus-deep successor partition. It banks

\[
U_{\rm paid}
=981{,}104+349{,}526+2{,}078{,}733
=3{,}409{,}363.
\]

No legacy selector, carrier, graph line, basis, or residual state is imported.
The exact successor partition digest is
`5f5ff58ad53c76fd522b4ee45dd9966c1f982fab788fa5de95b917945679760f`.

## 1. Fixed source state

Use exactly the deployed row and the same one public SP3 translation already
fixed by the active tangent owner:

\[
n=2{,}097{,}152,\quad k=1{,}048{,}576,\quad
A=1{,}116{,}048,
\]
\[
p=2{,}130{,}706{,}433,\quad
\mathbb F=\mathbf F_{p^6},\quad D\subset\mathbf F_p.
\]

Let \((\epsilon_0,\epsilon_1)\) be the translated source pair,

\[
\Sigma=\operatorname{supp}(\epsilon_0)\cup
\operatorname{supp}(\epsilon_1),\qquad s=|\Sigma|,
\]

and for \(h\in\Sigma\) define the projective source label

\[
\lambda(h)=[-\epsilon_0(h):\epsilon_1(h)].
\]

No alternative translation is unioned.

## 2. Intrinsic rational image

Set

\[
s_0=18{,}419,\qquad E(s)=\left\lfloor\frac{s-1}{2}\right\rfloor.
\]

Call the fixed source data compatible when \(s\ge s_0\) and there is a
nonconstant rational map \(\psi:\mathbf P^1\to\mathbf P^1\) with

\[
1\le\deg\psi\le E(s),\qquad
\psi([h:1])=\lambda(h)\quad(h\in\Sigma).
\]

Two such maps have cross determinant of degree at most
\(2E(s)\le s-1\), yet that determinant vanishes at all \(s\) distinct source
points. Hence it vanishes identically, so the compatible map is unique.

Define the finite source-rational image

\[
\mathcal R(\epsilon_0,\epsilon_1)=
\{\eta\in\mathbb F:[\eta:1]=\psi([x:1])
\text{ for some }x\in D\setminus\Sigma\}
\]

when compatible, omitting poles, and define it to be empty otherwise.

This set is pair-global. It contains no selector-derived data. Its cap is the
cardinality of its finite domain:

\[
|\mathcal R|
\le |D\setminus\Sigma|
=n-s
\le n-s_0
=2{,}078{,}733.
\tag{2.1}
\]

No injectivity of \(\psi\) is used.

## 3. Active owner insertion

Let \(R_2\) be the exact residual after the active tangent and intrinsic
deep-MCA cells. Define

\[
Z_{\rm SRat}=R_2\cap\mathcal R,\qquad
R_3=R_2\setminus Z_{\rm SRat}.
\]

Then

\[
|Z_{\rm SRat}|\le2{,}078{,}733.
\tag{3.1}
\]

Earlier overlap is removed by the intersection with \(R_2\); later overlap is
removed by exact set difference. Because \(\mathcal R\) is fixed by the pair
before any selector is chosen, (3.1) is hereditary under the two earlier
deletions.

The source theorem proves more: every qualifying full-outside rank-two
low-degree record selected from any subset of the old incoming residual has
all its selected finite slopes in this same image. That subset-stability is
useful downstream, but it is not needed to justify deleting the bounded
image itself. The source theorem explicitly states that deleting an incoming
bad slope in the image without a qualifying record is harmless.

## 4. Successor partition

The owner order is

```text
SOURCE_COORDINATE_TANGENT_IMAGE
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
ACTIVE_V4_BOUNDARY_PREFIX_Q
ACTIVE_V4_BALANCED_CORE
UNPAID_V4_COMPLEMENT
```

All cells are formed by iterated exact set difference and therefore are
pairwise disjoint and exhaustive over the complete bad finite-slope set.
Only the first three are bankable.

## 5. Exact ledger

\[
B^*=274{,}980{,}728{,}111{,}395{,}087,
\]
\[
B^*-3{,}409{,}363
=274{,}980{,}728{,}107{,}985{,}724.
\]

Thus

\[
U_{\rm total}
=3{,}409{,}363+U_Q+U_{BC}+U_{\rm new}.
\]

The source-rational active charge is `2,078,733`. It is not the historical
ledger movement `2,078,732`, which arose inside a legacy maximum-not-sum
C5/source-rational/base block. This packet does not import that block.

## 6. Proof authority and nonclaims

The source-rational uniqueness, image, cap, and subset-stability theorem is:

```text
experimental/notes/m1/m1_kb_rank9_source_rational_owner_splice_v1.md
```

The active predecessor is:

```text
experimental/notes/frontier-adjacent/kb_mca_v4_tangent_deep_owner_adapter_v1.md
```

The verifier checks exact arithmetic, source hashes, intrinsic-image
first-match insertion, disjoint exhaustion, null downstream atoms, and
semantic tamper rejection.

This packet does not import canonical C5, residual-base, Frobenius, carrier,
histogram, or any other legacy owner. It does not replay conditional Q on the
new residual, pay balanced core or complement, close the row, or move an
endpoint.

# PROVED
