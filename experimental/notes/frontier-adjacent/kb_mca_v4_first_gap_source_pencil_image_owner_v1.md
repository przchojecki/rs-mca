---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The pair-global union of the finite images of all base-rational projective points of the first-gap source interpolation pencil owns every first-gap full-outside coefficient-rank-two slope and has cap 4180889210446272.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
atom_or_cell: U_paid=ACTIVE_SIX_OWNER_PREDECESSOR+ACTIVE_V4_FIRST_GAP_BASE_RATIONAL_SOURCE_PENCIL_IMAGE
quantifier: Uniform over every admissible received line over F_(p^6) and every complete selector rebuilt after the six active source owners
projection_and_unit: Distinct bad finite slopes per received line
claimed_bound: U_paid=4200515150819207
status: PROVED
impact: BANKABLE_ATOM
falsifier: A retained first-gap full-outside coefficient-rank-two record whose complement locator is not a base-rational point of the intrinsic source residue line, or a selected finite slope not in the corresponding reduced-map image on D minus Sigma.
replay: python3 experimental/scripts/verify_kb_mca_v4_first_gap_source_pencil_image_owner_v1.py --check
---

# KoalaBear first-gap source-pencil image owner

**PROVED PAIR-GLOBAL FIRST-GAP OWNER / BANKABLE ATOM / ROW OPEN.**

This packet pays the first open full-outside slack directly. It does not
bound graph lines, determinant bases, or split locators. Instead it charges
the finite slope image of the intrinsic two-dimensional source pencil.

The new owner is

```text
ACTIVE_V4_FIRST_GAP_BASE_RATIONAL_SOURCE_PENCIL_IMAGE.
```

It is fixed by the translated received pair before any selector is built.

## 1. Exact first-gap source data

Use

\[
p=2{,}130{,}706{,}433,\qquad
B=\mathbf F_p,\qquad
F=\mathbf F_{p^6},
\]

\[
n=2{,}097{,}152,\qquad
e=67{,}472,\qquad
s=|\Sigma|=2e=134{,}944.
\]

The off-source domain has cardinality

\[
\boxed{n-s=1{,}962{,}208.}
\tag{1.1}
\]

At this full-outside first-gap endpoint the carrier is forced:

\[
\boxed{V=D\setminus\Sigma.}
\tag{1.2}
\]

It is therefore fixed by the translated source pair and domain, rather than
chosen by a later selector. In particular, \(L_V\) is pair-global.

Let

\[
A_B=B[X]/(L_\Sigma),\qquad
A_F=F\otimes_B A_B,
\]

and let \(U_F\) be the image in \(A_F\) of the polynomials of degree at most
\(e\). For the fixed translated source pair put

\[
u_0=L_V^{-1}\epsilon _0,\qquad
u_1=L_V^{-1}\epsilon _1.
\]

The proved complement-locator linearization constructs the intrinsic source
residue line

\[
W_\Sigma
=\{q\in A_F:q u_0\in U_F,\ q u_1\in U_F\},
\qquad
\dim_F W_\Sigma=2.
\tag{1.3}
\]

No selector, carrier basis, graph line, support, or determinant occurs in
the definition of \(W_\Sigma\). The apparent carrier input is the forced
pair-global carrier (1.2).

## 2. Base-rational source-pencil points

Define

\[
\mathcal P_B(W_\Sigma)
=\mathbf P(W_\Sigma)\cap\mathbf P(A_B).
\tag{2.1}
\]

The proved projective rational-point dichotomy gives

\[
\#\mathcal P_B(W_\Sigma)\in\{0,1,p+1\}.
\]

In particular,

\[
\boxed{\#\mathcal P_B(W_\Sigma)\le p+1=2{,}130{,}706{,}434.}
\tag{2.2}
\]

Every actual complement locator \(Y\) is a polynomial over \(B\), is
disjoint from \(\Sigma\), and therefore gives a nonzero unit

\[
q_Y=[L_Y]\in A_B^\times.
\]

The exact source admission test is

\[
Y\text{ is admitted}\iff q_Y\in W_\Sigma.
\tag{2.3}
\]

Consequently every actual first-gap graph line uses one point of
\(\mathcal P_B(W_\Sigma)\).

## 3. One finite image per projective point

Fix \([q]\in\mathcal P_B(W_\Sigma)\). There are unique degree-at-most-\(e\)
representatives \(R_q,S_q\) of

\[
q(u_0,u_1).
\tag{3.1}
\]

Uniqueness follows because \(2e\) distinct source evaluations determine a
polynomial of degree at most \(e\). The pair is nonzero because the
multiplier map \(q\mapsto q(u_0,u_1)\) is injective.

Cancel the polynomial gcd of \(R_q,S_q\), and denote the resulting
projective map by

\[
\psi_q([X:Z])=[-\overline R_q^{\,\rm hom}(X,Z):
                   \overline S_q^{\,\rm hom}(X,Z)].
\tag{3.2}
\]

Scaling \(q\) scales both coordinates before gcd cancellation, so
\(\psi_q\) depends only on the projective point \([q]\).

Define its finite off-source image

\[
\mathcal I_q
=\{\eta\in F:
      [\eta:1]=\psi_q([x:1])
      \text{ for some }x\in D\setminus\Sigma\}.
\tag{3.3}
\]

Poles and common zeros contribute no finite image point. Since (3.3) is the
image of a set of size \(n-s\),

\[
\boxed{|\mathcal I_q|\le n-s.}
\tag{3.4}
\]

No injectivity of \(\psi_q\) is asserted or needed.

## 4. Exact selected-slope containment

Let a complete selector be rebuilt after the six active source owners, and
let \(L\) be any retained first-gap full-outside coefficient-rank-two graph
line. Its complement locator supplies \(q_Y\) as in (2.3). The
complement-locator identity says that the line's reduced source pair is
exactly the degree-at-most-\(e\) pair associated with \(q_Y\), up to a
common scalar and the gcd already cancelled in (3.2).

For every selected finite slope \(\eta\) on \(L\), moving-root
transversality supplies

\[
x\in D\setminus\Sigma
\]

such that

\[
R_{q_Y}(x)+\eta S_{q_Y}(x)=0
\tag{4.1}
\]

and the two values are not both zero. After gcd cancellation, (4.1) is
exactly

\[
[\eta:1]=\psi_{q_Y}([x:1]).
\]

Therefore

\[
\boxed{\eta\in\mathcal I_{q_Y}.}
\tag{4.2}
\]

This containment is selector-faithful and same-slope: it starts from the
actual locator and actual moving-root equation of the selected record. The
owner set itself is nevertheless selector-independent.

## 5. Pair-global owner and cap

Define

\[
\mathcal I_{\rm FG}
=\bigcup_{[q]\in\mathcal P_B(W_\Sigma)}\mathcal I_q.
\tag{5.1}
\]

Equations (2.2) and (3.4) give

\[
\begin{aligned}
|\mathcal I_{\rm FG}|
&\le(p+1)(n-s)\\
&=2{,}130{,}706{,}434\cdot1{,}962{,}208\\
&=\boxed{4{,}180{,}889{,}210{,}446{,}272}.
\end{aligned}
\tag{5.2}
\]

Let \(R_6\) be the exact residual after the active tangent, deep-MCA,
source-rational, C5/base, common-twist, and Frobenius-9208 owners. Define

\[
Z_{\rm FG}=R_6\cap\mathcal I_{\rm FG},\qquad
R_7=R_6\setminus Z_{\rm FG}.
\tag{5.3}
\]

Then

\[
\boxed{|Z_{\rm FG}|\le4{,}180{,}889{,}210{,}446{,}272.}
\tag{5.4}
\]

By (4.2), no first-gap full-outside coefficient-rank-two selected slope can
remain in \(R_7\), regardless of which complete selector is rebuilt there.

This payment does not need:

* the determinant-weighted selected-basis packing bound;
* reciprocal rank-two versus rank-excess classification;
* a low-root-swap owner;
* a bound on the number of graph lines or locators; or
* injectivity of any source rational map.

Those reductions remain useful for sharper payments and for possible
higher-slack analogues, but they are no longer required to close the first
open slack.

## 6. Exact successor partition

The owner order is

```text
SOURCE_COORDINATE_TANGENT_IMAGE
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER
ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5_OR_RESIDUAL_BASE
ACTIVE_V4_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST
ACTIVE_V4_PAIR_GLOBAL_SOURCE_FROBENIUS_EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_9208
ACTIVE_V4_FIRST_GAP_BASE_RATIONAL_SOURCE_PENCIL_IMAGE
ACTIVE_V4_BOUNDARY_PREFIX_Q
ACTIVE_V4_BALANCED_CORE
UNPAID_V4_COMPLEMENT
```

Every cell is the current residual intersected with its fixed predicate, and
the next residual is exact set difference. The ten cells are pairwise
disjoint and exhaustive. The first seven are bankable.

The first-gap owner is subset-stable because both \(W_\Sigma\) and
\(\mathcal I_{\rm FG}\) are fixed before the incoming residual or any
selector is chosen.

## 7. Exact ledger

The six-owner predecessor paid

\[
19{,}625{,}940{,}372{,}935.
\]

After (5.2),

\[
\begin{aligned}
U_{\rm paid}
&=19{,}625{,}940{,}372{,}935
 +4{,}180{,}889{,}210{,}446{,}272\\
&=\boxed{4{,}200{,}515{,}150{,}819{,}207}.
\end{aligned}
\tag{7.1}
\]

With

\[
B^*=274{,}980{,}728{,}111{,}395{,}087,
\]

the remaining unconditional reserve is

\[
\boxed{270{,}780{,}212{,}960{,}575{,}880.}
\tag{7.2}
\]

The first-gap charge uses about \(1.52054\%\) of the previous reserve. The
KoalaBear row remains open because the other full-outside slacks

```text
67,472..209,568
```

and the separate Q/balanced-core obligations are not paid by this theorem.

## 8. Proof authority

The load-bearing inputs are:

```text
experimental/notes/frontier-adjacent/
kb_mca_v4_first_gap_source_interpolation_pencil_v1.md

experimental/notes/frontier-adjacent/
kb_mca_v4_first_gap_complement_locator_linearization_v1.md

experimental/notes/frontier-adjacent/
kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.md

experimental/notes/frontier-adjacent/
kb_mca_v4_c5_twist_frobenius9208_adapter_v1.md
```

The reciprocal normal form is not needed for the cap, but its projective
rational-point theorem supplies (2.2).

## 9. Guardrails

Do not use this packet to claim:

* that there are at most \(p+1\) graph lines or complement locators;
* that one reduced map is injective;
* that the same two-dimensional source pencil persists above the first gap;
* that the determinant-packing theorem is proved at other slacks;
* that Q or balanced core is paid; or
* that the KoalaBear row is closed.

The proved statement is exactly:

\[
\boxed{
\text{active six-owner residual}
\cap
\text{first-gap full-outside rank-two slopes}
\subseteq
\mathcal I_{\rm FG},
\qquad
|\mathcal I_{\rm FG}|
\le4{,}180{,}889{,}210{,}446{,}272.}
\]

# PROVED
