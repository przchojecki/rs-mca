---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: After the active tangent, deep-MCA, source-rational, and joint C5/base owners, two selector-free pair-global source owners charge the common-twist subline and the degree-9208 source-Frobenius root set, raising the bankable subtotal to 19625940372935.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_ADAPTER_V1
atom_or_cell: U_paid=ACTIVE_C5_BASE_PREDECESSOR+ACTIVE_V4_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST+ACTIVE_V4_PAIR_GLOBAL_SOURCE_FROBENIUS_EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_9208
quantifier: Uniform over every admissible received line over F_(p^6)
projection_and_unit: Distinct bad finite slopes per received line
claimed_bound: U_paid=19625940372935
status: PROVED
impact: BANKABLE_ATOM
falsifier: Selector dependence of either owner set, a qualifying common-twist record with a selected slope off the canonical source subline, a qualifying effective-multiplier record of degree at most 9208 with a selected slope off the canonical endpoint determinant, or failure of the printed root caps.
replay: python3 experimental/scripts/verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1.py --check
---

# KoalaBear active common-twist and Frobenius-9208 adapter

**PROVED DIRECT ACTIVE-V4 OWNER EXTENSION / BANKABLE ATOM / ROW OPEN.**

This packet inserts two source-only, pair-global owners after the active
tangent/deep/source-rational/C5-base partition:

```text
ACTIVE_V4_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST
ACTIVE_V4_PAIR_GLOBAL_SOURCE_FROBENIUS_EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_9208
```

Neither owner imports a selector, carrier, graph line, support, witness,
rank minimizer, histogram, or the legacy one-cut gate.

## 1. Incoming active residual

Use

\[
p=2{,}130{,}706{,}433,\qquad
B=\mathbf F_p,\qquad
F=\mathbf F_{p^6},
\]

and the exact residual \(R_4\) after:

```text
SOURCE_COORDINATE_TANGENT_IMAGE
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5_OR_RESIDUAL_BASE.
```

The fixed translated source pair, its support \(\Sigma\), its source labels,
and the domain order precede every later selector. The joint C5/base owner
already implies that a nonempty \(R_4\) has

```text
F_proj(R) != B
and every gamma in R4 satisfies gamma notin B.
```

The two new owners below are nevertheless defined on the whole incoming
residual, not only on Q.

## 2. Pair-global common-twist subline

The source-subline theorem constructs from the fixed source pair either an
empty set or one canonical projective \(B\)-subline \(S_{\rm src}\).
Every qualifying one-slack common-linear-gcd record in every complete
selector rebuilt after arbitrary earlier deletion has every selected slope
on this same subline.

Define

\[
Z_{\rm twist}
=R_4\cap\{\eta\in F:[\eta:1]\in S_{\rm src}\}.
\]

The earlier tangent owner already removed every finite source label. The
projective subline has at most \(p+1\) points, and the source-label deletion
saves at least two finite points in the all-finite case and at least one in
the infinity case. Hence

\[
\boxed{|Z_{\rm twist}|\le p-1=2{,}130{,}706{,}432.}
\tag{2.1}
\]

The construction is pair-global and subset-stable. Intersecting it with the
smaller post-C5/base residual cannot increase the cap.

## 3. Endpoint source-Frobenius owner

Set

\[
m=9{,}208,\qquad 2(m+1)=18{,}418.
\]

For an ordered \(18{,}418\)-subset \(T_0\subseteq\Sigma\), the proved
source-Frobenius eliminant is

\[
E_{T_0,m}(Z)=
\det_{a\in T_0}
\left[
a^iS_a(Z)^p\ (0\le i\le m)
\ \middle|\
a^iS_a(Z)\ (0\le i\le m)
\right].
\tag{3.1}
\]

Choose the first nonzero determinant in the fixed domain order. If none is
nonzero, define the owner set to be empty. Otherwise put

\[
\mathcal Z_{9208}=\{\eta\in F:E_{T_\star,9208}(\eta)=0\}.
\tag{3.2}
\]

This choice depends only on the fixed source pair, translation, and domain
order. It does not choose a minor from a selector or record.

Every selected slope in every qualifying full-outside
coefficient-rank-two record with effective multiplier degree at most
\(9{,}208\) annihilates every determinant (3.1). The diagonal-Krylov
nonvanishing proof works whenever

\[
2m<18{,}418,\qquad p>m+1,\qquad e>2m.
\tag{3.3}
\]

At \(m=9{,}208\),

\[
18{,}418-2m=2,
\]

so this is the sharp proved endpoint of that argument. The determinant
degree gives

\[
\boxed{
|\mathcal Z_{9208}|
\le(m+1)(p+1)
=9{,}209(p+1)
=19{,}621{,}675{,}550{,}706.
}
\tag{3.4}
\]

Define the active cell as the exact incoming residual intersection with
\(\mathcal Z_{9208}\), after the twist cell has been deleted.

### Why the endpoint is bankable here

The legacy packet banked only \(m=195\), because its inherited rank-nine
one-cut/aggregate-excess accounting became unusable at \(m=196\). That is a
downstream architecture constraint, not a failure of the endpoint algebra
or root bound. This active packet does not import that legacy one-cut gate.
It charges the finite root set (3.2) directly against the MCA slope budget,
where the endpoint cap (3.4) is valid and far below \(B^*\).

The degree-\(9{,}208\) owner supersedes the earlier moving-cofactor
four-anchor owner. The two are not added.

## 4. Exact active partition

The owner order is:

```text
SOURCE_COORDINATE_TANGENT_IMAGE
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5_OR_RESIDUAL_BASE
ACTIVE_V4_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST
ACTIVE_V4_PAIR_GLOBAL_SOURCE_FROBENIUS_EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_9208
ACTIVE_V4_BOUNDARY_PREFIX_Q
ACTIVE_V4_BALANCED_CORE
UNPAID_V4_COMPLEMENT
```

Each cell is the current residual intersected with its fixed predicate, and
the next residual is exact set difference. The nine cells are therefore
pairwise disjoint and exhaustive. The first six are bankable.

When canonical C5 owns the whole incoming residual, both new cells and the
tail are empty. Otherwise the residual-base component has already removed
all base slopes; the twist and Frobenius cells then delete only nonbase
members of their pair-global source sets.

## 5. Exact ledger

\[
\begin{aligned}
U_{\rm paid}
={}&2{,}134{,}115{,}797\\
&+2{,}130{,}706{,}432\\
&+19{,}621{,}675{,}550{,}706\\
={}&\boxed{19{,}625{,}940{,}372{,}935}.
\end{aligned}
\]

With

\[
B^*=274{,}980{,}728{,}111{,}395{,}087,
\]

the remaining unconditional reserve is

\[
\boxed{274{,}961{,}102{,}171{,}022{,}152.}
\]

The row remains open:

\[
U_{\rm total}
=19{,}625{,}940{,}372{,}935+U_Q+U_{BC}+U_{\rm new}.
\]

## 6. Outgoing residual theorem

After exact deletion and selector restart, no qualifying common-twist record
can survive. Every surviving qualifying full-outside
coefficient-rank-two record has effective multiplier degree at least
\(9{,}209\). In the usual slack notation

\[
r=s-t-1,
\]

this gives

\[
r\ge9{,}209,\qquad
s\ge t+9{,}210=76{,}682.
\]

The source-rational restart then gives

\[
e\ge\left\lceil\frac{s}{2}\right\rceil\ge38{,}341.
\]

Independently of record qualification, every outgoing slope avoids the two
fixed pair-global source sets \(S_{\rm src}\) and
\(\mathcal Z_{9208}\).

## 7. Proof authority and nonclaims

The source-subline theorem is:

```text
experimental/notes/m1/
m1_kb_rank9_one_slack_twist_subline_owner_v1.md
```

The effective-multiplier theorem and its algebraic endpoint are:

```text
experimental/notes/m1/
m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.md
```

The active predecessor is:

```text
experimental/notes/frontier-adjacent/
kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.md
```

The verifier binds these sources, checks the endpoint arithmetic, exact
first-match partition, C5-empty-tail branch, and no-double-charge rule, and
rejects semantic mutations.

This packet does not import the legacy selector, rank-nine one-cut gate,
aggregate-excess allowance, carrier, or histogram. It does not prove that
every outgoing Q slope is a qualifying full-outside rank-two record. It does
not replay the conditional Q compiler, pay balanced core or complement, or
close the row.

# PROVED
