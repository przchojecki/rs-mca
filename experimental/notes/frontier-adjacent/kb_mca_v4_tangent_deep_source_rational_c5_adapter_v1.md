---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: After active tangent, intrinsic deep-MCA, and pair-global source-rational deletion, one joint projective-base C5/residual-base owner takes the entire incoming residual on the intrinsic-base stratum and all remaining base slopes otherwise, with maximum cap p+1=2130706434.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_ADAPTER_V1
atom_or_cell: U_paid=SOURCE_COORDINATE_TANGENT_IMAGE+ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER+ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL+ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5_OR_RESIDUAL_BASE
quantifier: Uniform over every admissible received line over F_(p^6)
projection_and_unit: Distinct bad finite slopes per received line
claimed_bound: U_paid=2134115797
status: PROVED
impact: BANKABLE_ATOM
falsifier: A positive-rank pair with intrinsic projective syndrome field F_p whose post-earlier-owner bad finite slopes are not exhausted by canonical C5, a surviving base slope in the nonbase branch, or failure of the p+1 maximum-not-sum cap.
replay: python3 experimental/scripts/verify_kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.py --check
---

# KoalaBear v4 tangent-deep-source-rational-C5/base adapter

**PROVED DIRECT ACTIVE-V4 OWNER EXTENSION / BANKABLE ATOM / ROW OPEN.**

This packet adds one joint pair-global projective-base C5/residual-base owner
to the proved tangent/deep/source-rational successor partition. It banks

\[
\begin{aligned}
U_{\rm paid}
&=981{,}104+349{,}526+2{,}078{,}733+2{,}130{,}706{,}434\\
&=2{,}134{,}115{,}797.
\end{aligned}
\]

No legacy selector, carrier, graph line, basis, or residual state is
imported. The active proof consumes only the intrinsic projective syndrome
field and canonical C5 witness-exhaustion theorem for the fixed received
pair.

## 1. Fixed pair and intrinsic field

Use the deployed row

\[
n=2{,}097{,}152,\qquad
p=2{,}130{,}706{,}433,\qquad
\mathbb F=\mathbf F_{p^6},\qquad
B=\mathbf F_p.
\]

Let \(Z(R)\) be the complete set of bad finite slopes for the fixed received
line after the public SP3 translation, and let \(R_3\) be the exact residual
after:

```text
SOURCE_COORDINATE_TANGENT_IMAGE
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL.
```

The intrinsic projective syndrome field \(F_{\rm proj}(R)\) is a property of
the received pair, not of a selector or one witness. Earlier whole-slope
deletion does not change it.

## 2. Pair-global C5/base dichotomy

Define the active predicate:

\[
\mathcal C_{5/B}(R)=
\begin{cases}
R_3,&\operatorname{rank}Y_R>0
       \text{ and }F_{\rm proj}(R)=B,\\
R_3\cap B,&\text{otherwise}.
\end{cases}
\tag{2.1}
\]

This is a pair-global first-match cell. The second line is the residual
base-slope owner.

If \(\operatorname{rank}Y_R=0\), the source theorem says that the
noncontained exact-witness residual is empty. If the rank is positive and
\(F_{\rm proj}(R)=B\), projective subline confinement gives

\[
\widehat Z(R)\subseteq A\mathbf P^1(B)
\]

for one projective coordinate change \(A\). Canonical C5 is
witness-exhaustive on this minimal-field stratum after whatever earlier
realized cells were removed. It therefore owns the entire incoming residual
\(R_3\), not only the base-valued slopes or one displayed local subline.

The projective line \(\mathbf P^1(B)\) has \(p+1\) points. Restricting to the
finite slope chart can only decrease the count, so

\[
\boxed{|\mathcal C_{5/B}(R)|\le p+1=2{,}130{,}706{,}434.}
\tag{2.2}
\]

If \(F_{\rm proj}(R)\ne B\), the C5 part is empty by definition. No local
base-defined pencil is promoted to C5 in that branch. The joint cell is then
exactly \(R_3\cap B\), whose cap is \(p\).

The two cases are exclusive. Their uniform joint charge is the maximum

\[
\boxed{\max\{p+1,p\}=p+1=2{,}130{,}706{,}434,}
\tag{2.3}
\]

not the sum \(2p+1\). This exact joint maximum is why adding the residual-base
owner has zero additional ledger cost beyond the C5 cap.

## 3. Stability under the earlier active owners

The C5 theorem and residual-base predicate are already formulated after
arbitrary realized earlier first-match cells. In the enabled branch C5 owns
all of \(R_3\); in the disabled branch the joint cell owns exactly the
remaining base slopes. Thus it is automatically stable under the active
tangent, deep, and source-rational deletions:

```text
intrinsic-base:    joint cell=R3 and R4=empty
intrinsic-nonbase: joint cell=R3 intersect F_p and R4=R3\F_p.
```

No selector restart is needed to define this owner. Any later Q,
balanced-core, or complement selector is built only on \(R_4\).

This distinction is load-bearing. A support-dependent \(B\)-subline inside a
pair with \(F_{\rm proj}(R)=\mathbb F\) is not C5-owned. Such a local
extension or lower-gcd rational component remains in the outgoing residual.

## 4. Successor partition

The owner order is

```text
SOURCE_COORDINATE_TANGENT_IMAGE
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5_OR_RESIDUAL_BASE
ACTIVE_V4_BOUNDARY_PREFIX_Q
ACTIVE_V4_BALANCED_CORE
UNPAID_V4_COMPLEMENT
```

Every cell is the current residual intersected with its predicate; the next
residual is exact set difference. Hence the seven cells are pairwise
disjoint and exhaustive. The first four are bankable.

When C5 is enabled it owns the entire incoming residual, so Q, balanced core,
and complement are all empty. When it is disabled, every base-field slope is
removed before those cells.

## 5. Exact ledger

\[
B^*=274{,}980{,}728{,}111{,}395{,}087,
\]

\[
B^*-2{,}134{,}115{,}797
=274{,}980{,}725{,}977{,}279{,}290.
\]

Thus

\[
U_{\rm total}
=2{,}134{,}115{,}797+U_Q+U_{BC}+U_{\rm new}.
\]

This uses the safe sum of tangent, deep, source-rational, and the joint
C5/base cap. Inside the last block, C5 and residual base combine by the exact
maximum (2.3), not by addition. It does not import the broader legacy
C5/source-rational/base maximum because source rational is deliberately an
earlier independent active cell here.

## 6. Relevance to the boundary-Q common carrier

This owner removes the globally projective-base pair stratum and every
remaining base-field slope before Q.
Consequently, a four-row proper-domain common-carrier packet surviving into
the active Q cell must satisfy

```text
F_proj(R) != B
and gamma_i notin B for every surviving row.
```

A carrier pencil that merely becomes base-defined after a
support-dependent change of coordinates is not enough: the intrinsic field
test belongs to the whole received pair. The remaining proper-domain
split-locator theorem may therefore assume the pair is field-full (or in
another nonbase intrinsic-field stratum) and should route genuine descent
separately from local coefficient accidents.

## 7. Proof authority and nonclaims

The pair-global C5/base owner and its maximum \(p+1\) cap are proved in:

```text
experimental/notes/m1/m1_kb_projective_base_pair_c5_owner_v1.md
```

The active predecessor is:

```text
experimental/notes/frontier-adjacent/
kb_mca_v4_tangent_deep_source_rational_adapter_v1.md
```

The verifier binds those sources, recomputes the partition digest and exact
ledger, checks both intrinsic-base and intrinsic-nonbase branches, and
rejects semantic mutations.

This packet does not import the legacy Frobenius, carrier-incidence,
histogram, or selector-dependent owners. It does not
claim that every base-defined local common carrier has
\(F_{\rm proj}(R)=B\). It does not replay Q on the new partition, pay
balanced core or complement, or close the row.

# PROVED
