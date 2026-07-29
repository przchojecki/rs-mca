---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The twelve mandatory producer specializations saturate twice the complete degree-24 source divisor. This makes that divisor invariant under the conic involution, and the reciprocal, D4, and D5 reduced quotient profiles all have impossible fixed-point or orbit multiplicities.
architecture: null
partition_digest: null
atom_or_cell: K3_Q6_U2_COMPLETE_SOURCE_CONIC_EXCLUSION
quantifier: every actual Q=6,s=6,u=2 conic-image outgoing component after the retained source reduction, for every pole partition, source-label overlap chart, and surviving signature
projection_and_unit: component existence obstruction; not a distinct-slope count
claimed_bound: complete exclusion of the Q=6,s=6,u=2 conic-image branch, with zero ledger movement
status: PROVED_COMPLETE_SOURCE_REDUCED_CONIC_EXCLUSION_ROW_OPEN
impact: CLOSES_Q6_U2_CONIC_IMAGE_BRANCH
falsifier: a valid actual conic component for which a source row fails to divide B, the twelve row divisors do not sum to 2 div(B), div(B) is not invariant under iota, or one of the printed reciprocal/D4/D5 orbit tables has a compatible row
replay: python3 experimental/scripts/verify_kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.py --check --tamper-selftest
---

# KoalaBear \(Q=6,s=6,u=2\) complete-source conic exclusion

## 0. Verdict

The \(Q=6,s=6,u=2\) conic-image branch is empty.

The decisive condition is not signature-specific.  Every actual component
must divide all twelve specialized source fibers of the endpoint producer.
Those twelve quartic divisors have total degree \(48\), exactly twice the
degree of the complete source divisor.  The source degree of the component
is two, so the local divisibility inequalities saturate at every pole:

\[
\boxed{
\sum_{i=1}^{12}\operatorname{div}H(\alpha_i,-)
=2\operatorname{div}B.}
\tag{0.1}
\]

In the conic branch every row divisor is invariant under the second
involution \(\iota\).  Hence the complete divisor \(B\), not only the common
decic, is \(\iota\)-invariant.  The previously proved reciprocal,
\(D_4\), and \(D_5\) profiles are then impossible by fixed-point and orbit
multiplicity.

This closes the reduced conic branch uniformly and combines with the
already-proved ramified-common exclusions to close the complete conic-image
case.  It does not close the birational-quartic \(u=2\) image, the \(u=3\)
branch, cap \(68\), or the KoalaBear row.  It books no ledger charge.

## 1. Imported source-reduction facts

Work over the algebraic closure of the deployed field of odd characteristic

\[
p=2{,}130{,}706{,}433.
\]

The source reduction retained from commit
`44542e91e459364a521870ed2ebde7f6fe5055bf`, and manually integrated at
`0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d`, supplies:

1. twelve distinct source labels
   \(\alpha_1,\ldots,\alpha_{12}\);
2. pairwise pole-disjoint coordinate quadratics \(z_i\) and
   \[
   B=\prod_{i=1}^{12}z_i;
   \tag{1.1}
   \]
3. the endpoint producer
   \[
   M(T,X)=
   \sum_{i=1}^{12}\kappa_iL_i(T)\frac{B(X)}{z_i(X)},
   \qquad \kappa_i\ne0;
   \tag{1.2}
   \]
4. for every actual outgoing component \(H\),
   \[
   H\mid F_{\rm out}\mid M;
   \tag{1.3}
   \]
5. the complete-divisor identity
   \[
   \operatorname{div}B
   =
   \operatorname{div}\psi^*\Sigma,
   \qquad
   \Sigma=\sum_{i=1}^{12}[\alpha_i],
   \tag{1.4}
   \]
   where \(\psi\) is the degree-two quotient by the deployed deck
   involution \(b\).

The source-fiber specialization in PR #1127 gives, for

\[
q_i(X)=H(\alpha_i,X),
\]

\[
\boxed{
q_i\mid \frac{B}{z_i}\mid B
\qquad(1\le i\le12).}
\tag{1.5}
\]

All forms are treated as binary forms, so a pole at infinity is included.
The restriction \(q_i\) is a nonzero binary quartic.  If it vanished
identically, the source line \(T=\alpha_i\) would be a component of the
irreducible bidegree-\((2,4)\) form \(H\).

In the conic-image branch, the coefficient map factors as a separable
degree-two quotient

\[
\chi:\mathbf P^1_X\longrightarrow\mathbf P^1_X/\langle\iota\rangle
\]

followed by a conic embedding.  Equivalently,

\[
H=(\operatorname{id}\times\chi)^*\overline H.
\tag{1.6}
\]

Thus each row divisor has the form

\[
\operatorname{div}q_i=\chi^*\Delta_i
\tag{1.7}
\]

for a degree-two divisor \(\Delta_i\), and is invariant under \(\iota\).
The degree is separable because the characteristic is odd.

The conic reductions added in commit
`f42ad6ab64cda5f1d4061b73e739f8944ebb13eb` (PR #1117), and retained by the
same manual integration commit, also prove:

- \(\iota\ne b\);
- every common-decic branch containing one or two deck branch points is
  empty;
- every remaining reduced conic profile is reciprocal, \(D_4\), or
  \(D_5\).

These later inputs are proved in
`q6_u2_plane_map_reduction.md`,
`q6_u2_line_conic_quotient_reduction.md`, and
`q6_u2_conic_free_pair_involution_reduction.md` in commit `f42ad6ab6`.

## 2. Complete-source saturation

Fix a pole point \(x\in\operatorname{supp}B\).  The binary form

\[
H(T,x)
\]

is nonzero of degree at most two in \(T\).  Otherwise the pole line
\(X=x\) would be a component of \(H\).  Consequently at most two of the
twelve distinct source labels are zeros of \(H(T,x)\).

By (1.5),

\[
\operatorname{ord}_xq_i\le\operatorname{ord}_xB.
\]

At most two summands are positive, so

\[
\sum_{i=1}^{12}\operatorname{ord}_xq_i
\le
2\operatorname{ord}_xB.
\tag{2.1}
\]

The two effective divisors in (2.1), summed over all \(x\), have the same
degree:

\[
\sum_i\deg q_i=12\cdot4=48
=2\deg B.
\tag{2.2}
\]

Therefore every local inequality is equality.  This proves (0.1), or,
after choosing nonzero equation scales,

\[
\boxed{\prod_{i=1}^{12}q_i\sim B^2.}
\tag{2.3}
\]

Each divisor on the left of (0.1) is \(\iota\)-invariant by (1.7).
Hence

\[
\boxed{\iota^*\operatorname{div}B=\operatorname{div}B.}
\tag{2.4}
\]

There is a second local consequence.  If \(x\) is fixed by \(\iota\), then
\(\chi\) is ramified at \(x\), and every pullback \(\chi^*\Delta_i\) has
even order there.  If \(x\) were a simple root of \(B\), divisibility
would force

\[
\operatorname{ord}_xq_i=0
\quad\text{for every }i,
\]

contradicting (0.1).  Thus:

\[
\boxed{
x\in\operatorname{Fix}(\iota)\cap\operatorname{supp}B
\Longrightarrow
\operatorname{ord}_xB=2.}
\tag{2.5}
\]

Because \(B=\psi^*\Sigma\) and \(\Sigma\) is reduced, its only double roots
are selected branch points of the deck quotient \(\psi\), equivalently
fixed points of \(b\).

## 3. Reciprocal profile

Normalize the commuting involutions as

\[
b(x)=-x,
\qquad
\iota(x)=\frac{\mu}{x},
\qquad
\mu\ne0.
\tag{3.1}
\]

On the deck quotient \(w=x^2\), the second involution induces

\[
J(w)=\frac{\mu^2}{w}.
\tag{3.2}
\]

Its two fixed source values are \(+\mu\) and \(-\mu\).  The proved reduced
common-set profile is

\[
\mathcal K=
\{-\mu,\ r,\ \mu^2/r,\ s,\ \mu^2/s\}.
\tag{3.3}
\]

Thus \(\mathcal K\) is \(J\)-invariant and contains exactly one fixed
source value, \(-\mu\).

Equation (2.4), together with \(B=\psi^*\Sigma\), makes the complete
twelve-source set \(\Sigma\) invariant under \(J\): pullback of divisors by
the finite surjective map \(\psi\) is injective.  Its complement
\(\Sigma\setminus\mathcal K\) is a \(J\)-invariant seven-set.  An
involution-invariant odd set contains a fixed point, so the other fixed
value \(+\mu\) belongs to \(\Sigma\).

The deck fiber over \(+\mu\) is

\[
x^2=\mu.
\]

Its two points are precisely the fixed points of \(\iota\).  They are not
the deck branch points \(0,\infty\), so both occur simply in \(B\).  This
contradicts (2.5).  The reciprocal profile is empty.

## 4. \(D_4\) profile

Put

\[
g=b\iota.
\]

In the \(D_4\) profile, \(g\) has order four.  Its two fixed points lie in
the reduced common decic, so they are already simple roots of \(B\).
Every other geometric \(g\)-orbit has length four: a tame order-four
projectivity has the same fixed pair as its square and therefore has no
two-cycle.

Let

\[
r\in\{0,1,2\}
\]

be the number of deck branch points whose source values belong to
\(\Sigma\).  The multiplicity-one and multiplicity-two support strata of
\(B=\psi^*\Sigma\) have sizes

\[
24-2r
\qquad\text{and}\qquad
r.
\tag{4.1}
\]

Both strata are \(g\)-invariant by (2.4) and the original \(b\)-invariance.
The two \(g\)-fixed points already belong to the simple stratum.  Hence the
double stratum has size divisible by four, while the simple stratum has
size congruent to two modulo four:

\[
r\equiv0\pmod4,
\qquad
24-2r\equiv2\pmod4.
\tag{4.2}
\]

No \(r\in\{0,1,2\}\) satisfies both conditions.  Explicitly:

\[
\begin{array}{c|c|c|c|c}
r&|\operatorname{supp}_1B|&|\operatorname{supp}_2B|
&r\equiv0\ (4)&24-2r\equiv2\ (4)\\ \hline
0&24&0&\checkmark&\times\\
1&22&1&\times&\checkmark\\
2&20&2&\times&\times
\end{array}
\tag{4.3}
\]

The \(D_4\) profile is empty.

## 5. \(D_5\) profile

Now \(g=b\iota\) has order five.  The reduced common decic is one free
ten-point dihedral orbit and contains neither of the two fixed points of
\(g\).  Every other \(g\)-orbit is fixed or has length five.

Use the same \(r\) and multiplicity strata as in (4.1).

- If \(r=0\), the simple stratum has size \(24\equiv4\pmod5\).  It would
  require four \(g\)-fixed points, but a nonidentity projectivity has only
  two.
- If \(r=1\), the singleton double stratum must be \(g\)-fixed.  The
  simple stratum has size \(22\equiv2\pmod5\) and requires two fixed
  points disjoint from the double stratum.  This would require three
  distinct \(g\)-fixed points.
- If \(r=2\), the two double points must be the two \(g\)-fixed points.
  They are also exactly the two deck-fixed points of \(b\).  Thus
  \(g\), \(b\), and \(\iota=bg\) all fix the same pair.  In odd
  characteristic a nontrivial projective involution is uniquely determined
  by its two fixed points, so \(\iota=b\).  Then \(g=b\iota=1\),
  contradicting its order five.

Equivalently, the exact residue table is

\[
\begin{array}{c|c|c|c|c}
r&|\operatorname{supp}_1B|&|\operatorname{supp}_2B|
&\text{simple fixed points required}
&\text{double fixed points required}\\ \hline
0&24&0&4&0\\
1&22&1&2&1\\
2&20&2&0&2
\end{array}
\tag{5.1}
\]

The \(D_5\) profile is empty.

## 6. Consequence for the conic frontier

The proof used only the complete source divisor and the already-classified
quotient profile.  It is independent of:

- the pole-cycle partition \(6\), \(4+2\), \(3+3\), or \(2+2+2\);
- the common-signature graph;
- the identification \(\mathcal L=\mathcal I\) versus the one-label
  exchange chart;
- the ordering or orientation of the coordinate quadratics;
- the common-pair assignment and the weighted-GRS rank chart.

In particular, the exact \(2+2+2\) graph control has

\[
324=288+36
\]

post-star cases in ten representatives: eight \(P_6\) representatives
covering \(288\) cases and two \(P_2\sqcup C_4\) representatives covering
\(36\).  All ten receive the same terminal

```text
DELETED_BY_COMPLETE_SOURCE_DIVISOR_PROFILE_OBSTRUCTION
```

before signature-specific elimination.

The ten-representative ledger is only a graph-level regression.  A
source-semantic compiler would also have to enumerate right-label
identifications and the one-label exchange chart.  The uniform theorem
bypasses that larger census, so no unproved assignment-independence is used.

Combining Sections 3--5 with the imported exclusions of the one- and
two-common-branch-point cases proves:

\[
\boxed{\text{The complete \(Q=6,s=6,u=2\) conic-image branch is empty.}}
\tag{6.1}
\]

This is a structural K3 closure, not a numeric ledger payment.  The next
maximal branch is the \(u=2\) birational-quartic image, followed by \(u=3\).

## 7. Exact replays

Python regenerates the divisor-degree ledger, the three profile tables, the
\(324/10\) graph frontier, and the canonical JSON certificate:

```bash
python3 \
  experimental/scripts/verify_kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.py \
  --check --tamper-selftest
```

Sage independently checks the reciprocal normal form, the tame dihedral
orbit sizes, both ramification tables, and the graph totals:

```bash
sage \
  experimental/scripts/verify_kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.sage
```

The canonical payload SHA-256 is printed by either replay.  These programs
verify the exact finite enumeration and arithmetic consequences.  The
divisor argument in Sections 1--6 is the proof.

## 8. Scope and nonclaims

- **Proved:** complete-source saturation (0.1), complete-divisor
  \(\iota\)-invariance, exclusion of reciprocal/\(D_4\)/\(D_5\), and hence
  exclusion of every \(Q=6,s=6,u=2\) conic-image component.
- **Imported:** the endpoint producer, complete source divisor,
  degree-two conic quotient, ramified-common exclusions, and reduced-profile
  classification.
- **Not proved:** the birational-quartic \(u=2\) branch, \(u=3\), a
  same-record owner, cap \(68\), or the global KoalaBear row.
- **Ledger:** unchanged; movement is zero.
