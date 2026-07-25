---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: In the unique Q=147595, k=4981 residual, every positive common-direction-zero branch has cap at most 444522, and every projective evaluation line of size at least five supplies enough exact recurrence deficit to close. The only scalar survivor histograms are the all-singleton case and (2), (2,2), (3), (3,2), (4). For any seven actual source members forming a basis, exact lcm normalization then forces either a paid common zero, a paid line of size at least five, or a pair of master locators with gcd degree at least 16903.
architecture: M31_RANK7_SOURCE_BASIS_PRIVATE_ROOT_OVERLAP_DICHOTOMY_V1
atom_or_cell: Source-bound rank-seven branch payment and high-overlap route cut; no v4 atom value and no signed Xi_46 payment.
quantifier: Every counted normalized-label class in the unique k=4981 residual of the proved Q=147595 compiler, together with any seven actual source members forming a basis of its rank-seven master span.
projection_and_unit: Distinct LIST codewords per received word. The recurrence numerator counts agreement incidences and divides once by 72428.
claimed_bound: Positive common-zero branches have cap at most 444522; a projective line of size at least five gives cap at most 9806393. Every remaining source class has at most 28 private master-locator roots and some basis pair with master-locator gcd degree at least 16903.
status: PROVED LOCAL TWO-BRANCH PAYMENT / HIGH-OVERLAP ROUTE CUT / Q=147595 OPEN / ROW OPEN
impact: SOURCE-SPECIFIC RECURRENCE STABILITY / EXACT PRIMITIVE TERMINAL / NO LEDGER MOVEMENT
falsifier: A positive-z cap above 444522; a size-at-least-five projective line with deficit below 3214704; another scalar survivor histogram; an actual source basis not covering Z(P); a private root that is neither a common direction zero nor on its coordinate-axis projective line; or a z=0 source basis with at most 28 private roots and every pairwise locator gcd below 16903.
replay: Standard-library Python normal and optimized checks, hostile mutations, an independent heap replay, Sage exact-integer and finite-field source controls, strict JSON/schema/source hashes, and a sealed parent payload pin.
---

# M31 rank-seven source-basis private-root/overlap dichotomy

## 1. Result and scope

The fixed-mismatch predecessor leaves one residual at

\[
Q=147\,595,\qquad k=4\,981,
\]

with exact-rank-six direction, combined-domain length

\[
N_k=K+k=1\,053\,557,
\]

agreement

\[
m=k+w=72\,428,
\]

and current recurrence cap \(9\,806\,438\).  The refined outer compiler
closes exactly when this cap is at most \(9\,806\,393\).

This packet proves the source-bound trichotomy

\[
\boxed{
z>0
\quad\text{or}\quad
\text{one projective evaluation line has size at least }5
\quad\text{or}\quad
\deg\gcd(G_i,G_j)\ge16\,903
}
\tag{1.1}
\]

for some pair in every seven-member actual source basis.  The first two
branches close the local residual.  The third branch is the explicit
unpaid terminal

```text
HIGH_PAIRWISE_MASTER_LOCATOR_OVERLAP
```

and is a specialization of the existing
`CROSS_COFACTOR_INTERLACED_H_AND_DEEP_FIBER_INCIDENCE` obstruction.
Therefore (1.1) is a strict route reduction, not payment of \(Q=147\,595\),
a v4 atom, or the M31 LIST row.

## 2. Positive common-direction-zero branch

Let \(z\) be the number of common direction zeros of the full affine
hyperplane after division by \(L_S\).  The predecessor proves that every
such zero is a fixed mismatch.  Delete all \(z\) coordinates and divide
the direction by their squarefree locator.  The transformed parameters are

\[
j=4\,981-z,\qquad v=67\,447+z,
\tag{2.1}
\]

while

\[
N_j-j=1\,048\,576,\qquad j+v=72\,428.
\tag{2.2}
\]

Exact direction rank six requires \(j\ge6\), hence \(z\le4\,975\);
larger \(z\) would force the divided direction to have rank below six and
therefore cannot occur in this full-hyperplane residual.

For \(1\le z\le4\,975\), the ordinary Johnson denominator and numerator
inside the rank-six recurrence are

\[
\begin{aligned}
D_z
&=72\,428^2-(1\,053\,557-z)(4\,980-z)\\
&=-898\,676+1\,058\,537z-z^2,
\\
P_z
&=(1\,053\,557-z)(67\,448+z)\\
&=71\,060\,312\,536+986\,109z-z^2.
\end{aligned}
\tag{2.3}
\]

The concave quadratic \(D_z\) is positive at both endpoints of
\(1\le z\le4\,975\), hence positive throughout that interval.

At \(z=1\),

\[
D_1=159\,860,\qquad
P_1=71\,061\,298\,644
=444\,522D_1+11\,724.
\tag{2.4}
\]

Moreover

\[
444\,523D_z-P_z
=-470\,542\,464\,084
+470\,543\,056\,742z
-444\,522z^2.
\tag{2.5}
\]

The right side is concave in \(z\), so its minimum on the integer interval
occurs at an endpoint.  Its endpoint values are

\[
148\,136,\qquad
2\,329\,478\,967\,501\,116,
\tag{2.6}
\]

both positive.  Thus

\[
\boxed{C_{6,z}\le444\,522\quad(z\ge1),}
\tag{2.7}
\]

far below the closing cap \(9\,806\,393\).  The exact recurrence replay
agrees at \(z=1\).  Consequently every local counterexample has

\[
z=0.
\tag{2.8}
\]

No padding is used in this sharper branch; padding would erase the gain in
\(v\).

## 3. Exact projective-line deficit

At \(z=0\), the binding child value is

\[
C_5(4\,980)=674\,155.
\tag{3.1}
\]

The all-singleton recurrence numerator is

\[
1\,053\,557\cdot674\,155
=710\,260\,719\,335
=9\,806\,438\cdot72\,428+27\,871.
\tag{3.2}
\]

The largest numerator producing cap at most \(9\,806\,393\) is

\[
9\,806\,394\cdot72\,428-1
=710\,257\,504\,631.
\tag{3.3}
\]

Hence the exact required deficit is

\[
\Delta_{\rm close}=3\,214\,704.
\tag{3.4}
\]

If a projective evaluation line has size \(s\), the recurrence charges it
by the rank-five child at dimension \(4\,981-s\).  Relative to \(s\)
singleton lines, its exact numerator deficit is

\[
\Delta(s)
=s\bigl(674\,155-C_5(4\,981-s)\bigr).
\tag{3.5}
\]

The first binding values are

\[
\begin{array}{c|r|r}
s&C_5(4\,981-s)&\Delta(s)\\ \hline
1&674\,155&0\\
2&76\,516&1\,195\,278\\
3&38\,570&1\,906\,755\\
4&25\,783&2\,593\,488\\
5&19\,363&3\,273\,960.
\end{array}
\tag{3.6}
\]

An exact scan over every admissible \(5\le s\le4\,976\) has unique minimum
\(\Delta(5)=3\,273\,960>\Delta_{\rm close}\).  Thus

\[
\boxed{\text{one projective line of size at least five closes}.}
\tag{3.7}
\]

Exhausting the nonnegative histograms below (3.4) leaves only

\[
\varnothing,\qquad
(2),\qquad
(2,2),\qquad
(3),\qquad
(3,2),\qquad
(4).
\tag{3.8}
\]

Their deficits are, respectively,

\[
0,\ 1\,195\,278,\ 2\,390\,556,\ 1\,906\,755,\
3\,102\,033,\ 2\,593\,488.
\tag{3.9}
\]

This is an exact scalar envelope.  It does not assert that any listed
histogram is realizable by the source.

## 4. Actual source-basis coverage

Use the master normalization

\[
P=\operatorname{lcm}_{f\in\mathcal I}G_f,\qquad
Q_f=P/G_f,\qquad f=Q_fb_f,
\tag{4.1}
\]

where \(P\) and every \(G_f\) are split and squarefree and
\(\gcd(b_f,G_f)=1\).  Choose seven **actual source members**

\[
f_i=Q_ib_i,\qquad i=1,\ldots,7,
\tag{4.2}
\]

forming a basis of the exact rank-seven space \(\mathcal W\).  Arbitrary
linear-combination bases have no canonical locators and are not admissible
in what follows.

For \(\alpha\in Z(P)\), squarefreeness and individual coprimality give

\[
f_i(\alpha)\ne0
\quad\Longleftrightarrow\quad
\alpha\in Z(G_i).
\tag{4.3}
\]

If no basis locator contained \(\alpha\), all seven basis polynomials would
vanish there, so every element of \(\mathcal W\) would vanish there.  This
contradicts the predecessor exact-lcm no-common-zero theorem.  Therefore

\[
\operatorname{lcm}(G_1,\ldots,G_7)=P.
\tag{4.4}
\]

## 5. Private roots: common zero or axis line

Call \(\alpha\in Z(P)\) private to \(G_i\) when it lies in \(G_i\) and no
other basis locator.  Relative to (4.2),

\[
\operatorname{ev}_{\alpha}|_{\mathcal W}
=f_i(\alpha)e_i^*.
\tag{5.1}
\]

For the normalized-label functional \(\lambda\), the divided direction is
\(\ker\lambda/L_S\).  Since \(S\subset E_0\) and
\(E_0\cap Z(P)=\varnothing\),

\[
L_S(\alpha)\ne0.
\tag{5.2}
\]

The restriction of (5.1) to the divided direction is therefore

\[
\frac{f_i(\alpha)}{L_S(\alpha)}
e_i^*|_{\ker\lambda}.
\tag{5.3}
\]

There are exactly two cases:

1. \(e_i^*|_{\ker\lambda}=0\), equivalently
   \(e_i^*\) is proportional to \(\lambda\); then \(\alpha\) is a common
   direction zero and Section 2 pays the branch.
2. The restriction is nonzero; then every private root of type \(i\) lies
   on the same projective direction line.

The nonvanishing qualification is load-bearing.  The unqualified assertion
“every private root gives a projective line point” is false when
\(\lambda\) is a coordinate functional.

In the remaining \(z=0\) branch, all private roots are in the second case.
If there are at least 29 total private roots, the pigeonhole principle
gives one type with at least

\[
\left\lceil\frac{29}{7}\right\rceil=5
\tag{5.4}
\]

roots, and Section 3 closes.  Hence every survivor has at most 28 private
roots.

## 6. Forced high pairwise locator overlap

For \(\alpha\in Z(P)\), let

\[
r_\alpha
=|\{i:\alpha\in Z(G_i)\}|.
\tag{6.1}
\]

By (4.4), \(1\le r_\alpha\le7\).  Let \(n_1\) count roots with
\(r_\alpha=1\).  Then

\[
\sum_{i=1}^7\deg G_i
=\sum_{\alpha\in Z(P)}r_\alpha
\ge n_1+2(g-n_1)
=2g-n_1.
\tag{6.2}
\]

For a survivor \(n_1\le28\), so

\[
\sum_i\deg G_i
\ge2(354\,972)-28
=709\,916.
\tag{6.3}
\]

Because the locators are split and squarefree,

\[
\begin{aligned}
\sum_{i<j}\deg\gcd(G_i,G_j)
&=\sum_{\alpha\in Z(P)}\binom{r_\alpha}{2}\\
&\ge\sum_{\alpha\in Z(P)}(r_\alpha-1)\\
&=\sum_i\deg G_i-g\\
&\ge354\,944.
\end{aligned}
\tag{6.4}
\]

There are \(\binom72=21\) pairs.  Therefore

\[
\boxed{
\max_{i<j}\deg\gcd(G_i,G_j)
\ge
\left\lceil\frac{354\,944}{21}\right\rceil
=16\,903.
}
\tag{6.5}
\]

This proves (1.1).

## 7. Exact status of the high-overlap component

Write

\[
J=\gcd(G_i,G_j),\qquad
G_i=JA_i,\qquad G_j=JA_j.
\tag{7.1}
\]

The pairwise source determinant factors as

\[
G_ib_j-G_jb_i
=J(A_ib_j-A_jb_i).
\tag{7.2}
\]

The reduced determinant \(A_ib_j-A_jb_i\) is nonzero.  Indeed, equality
would give \(A_i\mid b_i\) and \(A_j\mid b_j\) because
\(\gcd(A_i,A_j)=1\).  Since \(A_i\mid G_i\), \(A_j\mid G_j\), and the
canonical pairs satisfy
\(\gcd(b_i,G_i)=\gcd(b_j,G_j)=1\), this forces
\(A_i=A_j=1\).  Then \(G_i=G_j=J\) and (7.2) forces \(b_i=b_j\), contrary
to the linear independence of the two basis members.

If \(K_{ij}=\gcd(H_i,H_j)\), then \(K_{ij}\) is split on \(E_0\), disjoint
from \(J\), and the pairwise CRT identity gives

\[
K_{ij}\mid A_ib_j-A_jb_i.
\tag{7.3}
\]

Consequently

\[
\deg K_{ij}
\le
\deg\operatorname{lcm}(G_i,G_j)-w-1.
\tag{7.4}
\]

Equation (7.4) is exact but does not yet pay the row: its induced scalar
bound is weaker than the already imposed shallow gates.  No integrated
owner pays a common factor of two master error-side locators merely from
its degree.  In particular:

- fixed-\(G\) payment requires an entire common locator slice;
- common-zero payment requires a zero of the whole direction span;
- pairwise CRT owners concern \(H_i,H_j\), not \(G_i,G_j\);
- periodic or quotient payment requires a declared invariant folding.

The high-overlap branch must therefore remain explicitly unpaid.

## 8. Relation to current upstream work

The open T8/T16/T32 flatness packets are support-alignment results.  They do
not supply the arbitrary-source projection needed here.  The open
rate-half and adjacent fixed-\(G\) Hahn packets show that pairwise support
relaxations are too weak and do not transfer to this combined-domain
residual.  The canonical-remainder packet does not prove its load-bearing
cross-remainder clauses and has no source adapter to (4.1).

Thus this packet is nonduplicate.  It uses source information absent from
those PRs and identifies a different surviving component.

## 9. Ledger effect and nonclaims

The active v4 ledger remains

```text
U_paid    = 3730
U_Q       = null
U_list_int= null
U_ext     = null
U_new     = null
Xi_46     remains open
row       remains open
```

No official endpoint, v4 atom, signed charge, rank-at-least-eight branch, or
stable paper is changed.

## 10. Proof audit

### Statement audited

The implication from the unique \(k=4\,981\) recurrence state to the
positive-common-zero payment, the complete projective-deficit histogram,
and the actual-source-basis private-root/high-overlap trichotomy.

### Files and sections read

- `m31_rank7_combined_domain_fixed_mismatch_recurrence_v1.md`, Sections
  2--5.
- `m31_rank7_shallow_master_denominator_cut_v1.md`, Sections 1--2.
- `m31_rank7_weighted_head_interlaced_source_route_cut_v1.md`, the
  recurrence and deployed source-family sections.
- `m31_varying_g_affine_span_shortening_route_cut_v1.md`, source
  normalization and common-zero definitions.
- Current upstream PR bodies and theorem notes through PR #1104.

### Dependencies

- **PROVEN by sealed predecessors:** exact rank seven; actual source
  normalization \(f_i=(P/G_i)b_i\); split squarefree \(P,G_i\);
  \(\gcd(b_i,G_i)=1\); no common zero of \(\mathcal W\) on \(Z(P)\);
  complete projective-line slicing; every full-hyperplane common direction
  zero is a fixed mismatch; and the exact \(Q=147\,595\) residual.
- **PROVED here:** the all-positive-\(z\) payment, full line-deficit scan,
  exhaustive six scalar survivor histograms, actual-basis lcm coverage,
  private-root restriction dichotomy, and \(16\,903\) overlap theorem.
- **EXACT CERTIFIED COMPUTATION:** recurrence arrays, Johnson endpoint
  arithmetic, line deficits, histogram exhaustion, pair-overlap arithmetic,
  and finite-field source controls.
- **UNPROVEN:** payment or impossibility of the high-overlap component,
  \(Q=147\,595\), later heads, ranks at least eight, v4 ownership, and the
  global row.

### Parameter dependence

All numerical statements are finite and exact at the fixed M31 parameters.
There are no asymptotic constants or hidden dependence on
\(T,Y,\mathcal L,\mathcal L_{\bar I},\lambda,I\).  The proof retains
\(\lambda\) explicitly in (5.3).

### Layer-cake / dyadic summability

Not applicable.

### Moment / Markov / Chebyshev

Not applicable.

### Edge cases and notation

- The seven basis elements must be actual source members with canonical
  \(G_i\), not arbitrary combinations.
- A private root may be a common direction zero; \(z=0\) is required before
  treating it as a projective line point.
- Exact rank six requires \(4\,981-z\ge6\).  Larger \(z\) is a rank-drop
  branch, not an omitted recurrence state.
- The five nonzero histograms are scalar envelopes, not constructed source
  lists.
- A large pairwise master-locator gcd is not a common zero of the entire
  direction and is not automatically a fixed-\(G\) owner.

### Numerical evidence

All deployed numbers are exact integers.  The Sage finite-field examples
test the source algebra and the load-bearing private-root qualifier; they do
not prove the M31 theorem in place of Sections 2--6.

### Verdict

**GREEN locally / YELLOW globally.**  The corrected trichotomy is proved
and independently replayed.  It is a bankable route cut.  It does not
authorize \(Q=147\,595\) or global closure.

### Remaining risks

The exact source equations have not yet been used to classify the
\(16\,903\)-overlap pair.  A primitive high-overlap component may exist.
The recurrence caps are upper bounds and need not be attained.

### Maximal next theorem

For a forced pair (7.1), combine the reduced determinant (7.2) with

\[
H_\nu=\gcd(L_0,G_\nu-b_\nu V)
\]

for the complete source layer.  Prove that every compatible component
either:

1. creates another projective-line deficit of at least \(112\,671\) in the
   closest \((3,2)\) histogram;
2. enters a named fixed-\(G\), quotient, or complete-fiber owner with exact
   add-back; or
3. is an explicit source-compatible primitive component.

The theorem must work on the complete mixed-\(G\) layer; another standalone
pairwise support bound cannot close it.

**OPEN GAP**
