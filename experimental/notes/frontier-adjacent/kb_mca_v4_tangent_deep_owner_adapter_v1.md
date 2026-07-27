---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every received line has a source-coordinate tangent first-match cell of at most 981104 distinct bad finite slopes followed by an intrinsic deep-MCA cell whose union with tangent has size at most 1330630; Q, balanced core, and final residual are exact set differences.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_OWNER_ADAPTER_V1
partition_digest: 04bcf1873b693f6f4b07d3c2116b2af42872db9d9edb19e76a81034191d80041
atom_or_cell: U_paid=SOURCE_COORDINATE_TANGENT_IMAGE+ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
quantifier: Uniform over every admissible received line over F_(p^6)
projection_and_unit: Distinct bad finite slopes per received line
claimed_bound: U_paid=1330630
status: PROVED
impact: BANKABLE_ATOM
falsifier: Failure of tangent translation invariance, deep-witness lifting, either global source cap, or exact first-match exhaustion.
replay: python3 experimental/scripts/verify_kb_mca_v4_tangent_deep_owner_adapter_v1.py --check; lake build in experimental/lean/kb_mca_v4_tangent_deep_owner_adapter
---

# KoalaBear v4 tangent-plus-deep owner adapter

**PROVED DIRECT ACTIVE-V4 RE-PROOF / BANKABLE OWNER EXTENSION / ROW OPEN.**

This packet strengthens the active source-bound KoalaBear partition without
importing the legacy M1 ledger. It places the intrinsic deep-MCA owner directly
after the active tangent owner and proves

\[
U_{\rm paid}=981{,}104+349{,}526=1{,}330{,}630.
\]

The remaining active Q, balanced-core, and complement values stay null.

## 1. Frozen row contract

\[
p=2{,}130{,}706{,}433,\qquad \mathbb F=\mathbf F_{p^6},
\]
\[
n=2{,}097{,}152,\qquad k=1{,}048{,}576,\qquad
A=1{,}116{,}048.
\]

Put

\[
R=n-k=1{,}048{,}576,\qquad j=n-A=981{,}104.
\]

The row budget is

\[
B^*=274{,}980{,}728{,}111{,}395{,}087.
\]

The projection and accounting unit is one distinct bad finite slope on one
fixed received line. Supports, witnesses, coordinates, selectors, and
certificates are never charged.

All cells use architecture
`GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_OWNER_ADAPTER_V1` and exact partition
digest
`04bcf1873b693f6f4b07d3c2116b2af42872db9d9edb19e76a81034191d80041`.

## 2. Active tangent owner

The predecessor packet
`kb_mca_v4_tangent_source_adapter_v1.md` fixes one public first common SP3
translation for the whole received line. With translated errors \(e_0,e_1\)
and

\[
\Sigma=\operatorname{supp}(e_0)\cup\operatorname{supp}(e_1),
\]

the source-coordinate tangent image is

\[
\mathcal T=
\{-e_0(x)/e_1(x):x\in\Sigma,\ e_1(x)\ne0\}.
\]

The exact sparsification theorem preserves the complete bad-slope set under
that single translation, and

\[
|\mathcal T|\le|\Sigma|\le n-A=981{,}104.
\tag{2.1}
\]

No union over alternative translations is allowed.

## 3. Intrinsic deep-MCA owner

For a bad slope \(z\), let \(y_z\) be the corresponding point on the received
line. Define the intrinsic predicate \(\mathsf{Deep}(z)\) to mean:

* there is an exact noncontained agreement witness for \(y_z\);
* its explaining codeword is \(c_z\);
* the actual error support
  \(E_z=\operatorname{supp}(y_z-c_z)\) satisfies
  \(|E_z|\le r_*\), where

\[
r_*=\left\lfloor\frac{n-k}{3}\right\rfloor=349{,}525.
\tag{3.1}
\]

This is an existential predicate on the slope, not a witness multiplicity.
Set

\[
A_*=n-r_*=1{,}747{,}627.
\tag{3.2}
\]

The exact numerical gate is

\[
3r_*=1{,}048{,}575\le n-k=1{,}048{,}576.
\tag{3.3}
\]

### Witness lifting

For a witness satisfying \(|E_z|\le r_*\), the same codeword agrees with
\(y_z\) on the full set \(D\setminus E_z\), whose size is at least \(A_*\).
Noncontainment persists: a simultaneous explanation on a larger agreement set
would restrict to one on the original witness support. If exact size is
required, choose an \(A_*\)-subset containing the original support.

Thus every slope satisfying \(\mathsf{Deep}\) is bad at agreement \(A_*\).
The exact deep-MCA numerator therefore gives the global envelope

\[
|\{z:\mathsf{Deep}(z)\}|\le r_*+1=349{,}526.
\tag{3.4}
\]

This envelope is uniform over the received line and monotone under every
earlier first-match deletion. Restricting the deep cell to non-tangent slopes
cannot increase it.

### Relation to the legacy deep owner

The legacy M1 accounting first charged \(67{,}472\) branch-2 slopes and then
extended the shared deep envelope by \(282{,}054\). Exactly,

\[
67{,}472+282{,}054=349{,}526.
\tag{3.5}
\]

Equation (3.5) is provenance, not the active proof. The active packet uses the
single intrinsic predicate and global cap (3.4) directly.

## 4. Frontloading identity

Let \(Z\) be the complete bad-slope set, \(T\) the tangent predicate, and \(D\)
the intrinsic deep predicate. The old local order `deep then tangent` pays

\[
(Z\cap D)\cup((Z\setminus D)\cap T),
\]

whereas the active order `tangent then deep` pays

\[
(Z\cap T)\cup((Z\setminus T)\cap D).
\]

Both sets equal

\[
Z\cap(T\cup D).
\tag{4.1}
\]

This pointwise identity is formalized by
`frontload_tangent_paid_union`. It avoids any transport of selectors,
witnesses, or residual states.

Using the two global envelopes,

\[
|Z\cap(T\cup D)|
\le |T|+|D|
\le981{,}104+349{,}526
=1{,}330{,}630.
\tag{4.2}
\]

Overlap only improves the bound.

## 5. Active first-match partition

Let \(Q\) and \(BC\) denote the active-v4 boundary-prefix and balanced-core
predicates. Define

\[
Z_T=Z\cap T,\qquad R_1=Z\setminus T,
\]
\[
Z_D=R_1\cap D,\qquad R_2=R_1\setminus D,
\]
\[
Z_Q=R_2\cap Q,\qquad R_3=R_2\setminus Q,
\]
\[
Z_{BC}=R_3\cap BC,\qquad Z_{\rm new}=R_3\setminus BC.
\]

The owner order is

```text
SOURCE_COORDINATE_TANGENT_IMAGE
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
ACTIVE_V4_BOUNDARY_PREFIX_Q
ACTIVE_V4_BALANCED_CORE
UNPAID_V4_COMPLEMENT
```

These five cells are pairwise disjoint and exhaust \(Z\) by iterated exact set
difference. The first two are bankable through (2.1) and (3.4). The last
three remain unpaid.

## 6. Exact ledger

\[
U_{\rm paid}=1{,}330{,}630,
\]
\[
B^*-U_{\rm paid}
=274{,}980{,}728{,}110{,}064{,}457.
\tag{6.1}
\]

The reserve in (6.1) is not an allocation. The open ledger is

\[
U_{\rm total}
=1{,}330{,}630+U_Q+U_{BC}+U_{\rm new}.
\]

## 7. Proof authority

The tangent theorem is consumed from:

```text
experimental/rs_mca_thresholds.tex
experimental/lean/rs_mca_thresholds/RsMcaThresholds/ExactSparsification.lean
experimental/notes/frontier-adjacent/kb_mca_v4_tangent_source_adapter_v1.md
```

The intrinsic deep theorem is consumed from:

```text
tex/cs25_cap_v12.tex
experimental/rs_mca_thresholds.tex
experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md
experimental/notes/m1/m1_kb_branch3_deep_ccl_tdd_v1.md
```

`KbMcaV4TangentDeepOwnerAdapter.lean` proves the Boolean frontloading,
first-owner, and integer kernels. It does not replace either source
cardinality theorem. The Python verifier checks structure, bindings, exact
arithmetic, finite first-match regressions, and tamper rejection.

## 8. Nonclaims

This packet does not:

* import the full legacy M1 owner stack or its \(422{,}354{,}730{,}332\)
  recorded total;
* transport any legacy first-match selector or residual state;
* prove or bank active \(U_Q\), \(U_{BC}\), or \(U_{\rm new}\);
* reuse the predecessor conditional-Q number automatically;
* prove a source-bound partition bridge for the remaining legacy owners;
* close the KoalaBear row or move the official endpoint.

The conditional Q packet is architecture- and incoming-residual-sensitive.
It must be replayed against this successor partition before it can be used.

# PROVED
