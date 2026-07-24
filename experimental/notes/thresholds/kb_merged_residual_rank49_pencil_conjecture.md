---
workboard_item: K3
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: For every admissible received line, the post-tangent post-Q residual R2 has at most 137490163860629056 distinct bad finite slopes; more precisely, it has a slope-level first-match rank-49-or-pencil atlas with one proper correction block, at most one scalar-degenerate exception, and at most 30119370885234533 normalized primitive one-parameter pencils of at most two slopes each.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1
partition_digest: 4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc
atom_or_cell: ACTIVE_V4_BALANCED_CORE union UNPAID_V4_COMPLEMENT, merged as R2 without changing the frozen partition
quantifier: Every admissible KoalaBear received line r over F_(2130706433^6), after the frozen first-match tangent and ACTIVE_V4_BOUNDARY_PREFIX_Q deletions.
projection_and_unit: Distinct bad finite slopes per received line. Every support or explanation is projected to its finite slope before charging; duplicate slopes across supports and raw charts are deleted by a fixed first-match assignment.
claimed_bound: CONJECTURE max_r |R2(r)| <= 137490163860629056. Under KB_TANGENT_ROOTED_Q_SHELL(3,7), this pays U_BC and U_new at that same value and closes the row with one unit of ledger slack.
status: CONJECTURAL
impact: ROW_CLOSURE
falsifier: One admissible line with at least 137490163860629057 distinct post-tangent post-Q finite slopes; or a finite exact certificate that every legal rank-49 block plus one exceptional slope leaves a normalized primitive-pencil cover number above 30119370885234533.
replay: "From experimental/lean/asymptotic_spine, on Lean 4.31.0 stdlib only: lake build AsymptoticSpine.KoalaBearMergedResidual prints an axioms census for every theorem in KoalaBearMergedResidual.lean. Arithmetic using large falling-factorial products is checked with native_decide and therefore discloses the generated theorem-local native-decision axiom. This is a conjecture only: no theorem asserts the deployed Reed-Solomon line satisfies the law."
---

# KoalaBear merged residual: rank-49-or-pencil conjecture

**Date:** 2026-07-23  
**Verdict:** `CONJECTURE`, not a theorem.  
**Deliverable type:** precise slope-level law, mechanism, evidence, threats, proof plan, falsifier, and stdlib Lean `Prop`.

## 1. Frozen object and ledger role

The deployed row is

```text
p = 2,130,706,433
F = F_(p^6)
n = 2,097,152
k = 1,048,576
a = 1,116,048
t = n-a = 981,104
d = a-k = 67,472
B* = 274,980,728,111,395,087.
```

For an admissible received line `r`, let `Z(r)` be its set of distinct bad
finite slopes.  Let `T(r)` be the frozen first-match tangent image and let
`Z_Q(r)` be the frozen `ACTIVE_V4_BOUNDARY_PREFIX_Q` image after tangent
deletion.  The object of this note is

\[
 R_2(r)=(Z(r)\setminus T(r))\setminus Z_Q(r).
\]

The frozen owner order is

```text
SOURCE_COORDINATE_TANGENT_IMAGE
  > ACTIVE_V4_BOUNDARY_PREFIX_Q
  > ACTIVE_V4_BALANCED_CORE
  > UNPAID_V4_COMPLEMENT.
```

The final two cells partition `R2`.  Therefore a uniform theorem
`|R2(r)| <= N` pays both `U_BC <= N` and `U_new <= N` inside the existing
four-atom additive ledger.  This note introduces no new owner, no new digest,
and no max-type `S+A+E` endgame.

The banked inputs are kept separate by proof status:

* `U_paid = 981,104` is an unconditional theorem;
* `U_Q <= 400,389,155,870` is conditional on
  `KB_TANGENT_ROOTED_Q_SHELL(3,7)`;
* `U_Q <= 442,607,801,512` is the rival conditional congestion cap;
* `|Z_Q| >= 57,198,030,365` is an unconditional floor, not an upper payment.

The conjecture below is an unconditional statement about the set `R2`.  Only
the final row-closure inference uses the tangent-rooted Q-shell hypothesis.

## 2. Precise conjecture

### 2.1 Normalized slope charts

A **normalized primitive pencil key** on a received line consists of the
post-deletion projective one-parameter correction direction together with the
core/owner data needed to identify the corresponding balanced-core pencil.
The charged object attached to a key is its set of **distinct finite slopes**,
not its supports, locators, explanations, or parameter pairs.

Two rules are part of the statement.

1. Every residual slope is projected to its finite slope before it is charged.
2. If one slope has several supports or belongs to several raw charts, a fixed
   first-match normalization assigns it to exactly one charged block.

Thus the pencil census below is a census of normalized slope fibres.  It is not
a support census in disguise.

### 2.2 Rank-49-or-pencil atlas law

For every admissible received line `r`, there exist pairwise disjoint sets of
distinct finite slopes

\[
 R_{\mathrm{prop}}(r),\qquad
 R_{\mathrm{pen}}(r),\qquad
 R_{\mathrm{exc}}(r)
\]

and a finite set `C(r)` of normalized primitive pencil keys such that

\[
 R_2(r)=R_{\mathrm{prop}}(r)\sqcup
        R_{\mathrm{pen}}(r)\sqcup
        R_{\mathrm{exc}}(r),                                      \tag{KBR2-1}
\]

with all of the following properties.

**(P49) One proper correction block.** There is one first-match primitive core
(or its coherent owner normalization) and one correction space `W_r`, proper
for that core in the sense of the proper-intersection compiler, with

\[
 \dim W_r\le49,
\]

such that every slope in `R_prop(r)` is the slope image of a rich parameter
point in `F x W_r`.  Consequently the proved proper-intersection theorem gives

\[
 |R_{\mathrm{prop}}(r)|
 \le
 \left\lfloor
 31\cdot50\frac{\binom{2{,}097{,}152}{50}}
                   {\binom{1{,}116{,}048}{50}}
 \right\rfloor
 =77{,}251{,}422{,}090{,}159{,}989.                    \tag{KBR2-2}
\]

The theorem counts rich parameter points and therefore safely overcounts
distinct slopes.

**(PEN) Primitive pencil cover.** There is a first-match assignment

\[
 \pi_r:R_{\mathrm{pen}}(r)\longrightarrow \mathcal C(r)
\]

such that every fibre is the post-deletion distinct-slope image of a genuine
primitive one-parameter moving-root pencil.  The proved one-pencil theorem
then gives

\[
 |\pi_r^{-1}(c)|\le2\qquad(c\in\mathcal C(r)).          \tag{KBR2-3}
\]

The conjectural exact chart census is

\[
 |\mathcal C(r)|
 \le30{,}119{,}370{,}885{,}234{,}533.                  \tag{KBR2-4}
\]

**(EXC) Scalar degeneracy.** The zero-scalar/global-affine or denominator-root
transition left outside the normalized blocks contributes at most one finite
slope:

\[
 |R_{\mathrm{exc}}(r)|\le1.                            \tag{KBR2-5}
\]

The substantive conjecture is the exhaustive slope-level construction of
`(KBR2-1)` with `(P49)`, `(PEN)`, and `(EXC)`, especially the assertion that
all nonproper residual components coalesce into the normalized pencil census.
The numerical inequalities consumed after that construction are proved.

### 2.3 Uniform law and exact integer

Equations `(KBR2-1)`--`(KBR2-5)` imply

\[
\begin{aligned}
 |R_2(r)|
 &\le77{,}251{,}422{,}090{,}159{,}989\\
 &\quad+2\cdot30{,}119{,}370{,}885{,}234{,}533+1\\
 &=\boxed{137{,}490{,}163{,}860{,}629{,}056}.
\end{aligned}                                                   \tag{KBR2}
\]

Equivalently,

\[
 \boxed{\max_{r\ \mathrm{admissible}}|R_2(r)|
 \le137{,}490{,}163{,}860{,}629{,}056.}
\]

This is the current best law.

## 3. Why this law

The source results point to a geometric dichotomy rather than a direct support
count.

First, the order-32 kernel dictionary and coherence mechanism organize many
slopes around one interpolating core or one coherent owner.  Relative to that
core, a correction lies in a codeword space `W`.  When the coordinate
hypersurfaces intersect properly, the proper-intersection compiler counts all
rich parameter points in one stroke and has no field-size factor.

Second, failure of properness is already typed: it is an evaluation rank-flat
or an exact polynomial clone component.  After the tangent and boundary-prefix
Q owners have been deleted, the expected irreducible one-dimensional remnants
are projective correction directions.  A genuine one-dimensional direction is
exactly the setting in which the moving-root theorem pays at most two distinct
finite slopes.  The law therefore predicts that nonproper geometry does not
create a new large unstructured numerator; it creates a census of paid
one-parameter slope fibres.

Third, dimension `49` is not chosen aesthetically.  It is the last generic
proper-intersection dimension whose exact KoalaBear bound leaves ample room in
the merged residual reserve.  Dimension `50` is the nearest explicit numerical
threat and no longer fits the residual cap.  The single exceptional slope is
the scalar degeneracy already isolated in the rational-atom setup, not an
arbitrary fudge factor.

This mechanism is deliberately line-local.  It asks for one coherent block and
one first-match chart census on the same received line; it never interchanges
`sup_line sum_chart` with `sum_chart sup_line`.

## 4. Evidence for

### 4.1 Exact reserve arithmetic

The tangent-rooted shell leaves

\[
 B^*-U_{\mathrm{paid}}-U_Q
 =274{,}980{,}327{,}721{,}258{,}113.
\]

Hence

\[
 \left\lfloor\frac{B^*-U_{\mathrm{paid}}-U_Q}{2}\right\rfloor
 =137{,}490{,}163{,}860{,}629{,}056.
\]

At the proposed bound,

\[
 981{,}104+400{,}389{,}155{,}870
 +2\cdot137{,}490{,}163{,}860{,}629{,}056
 =B^*-1.
\]

Increasing the bound by one makes the same total `B*+1`.  Thus the threshold is
sharp for this ledger and the proposed law lands exactly on it, with one unit
of closure slack.

The rival congestion cap would require

\[
 N\le137{,}490{,}142{,}751{,}306{,}235,
\]

which is smaller by `21,109,322,821`.  Therefore this conjecture closes the row
under the tangent-rooted shell only; it does not silently claim closure from
the congestion hypothesis.

### 4.2 Exact proper-intersection transition

The proved proper correction-space formula is

\[
 P_s=\left\lfloor
 31(s+1)\frac{\binom n{s+1}}{\binom a{s+1}}
 \right\rfloor.
\]

For this row, exact integer evaluation gives

```text
P_49 =  77,251,422,090,159,989
P_50 = 148,068,539,552,473,273.
```

The first consumes about `56.19%` of the merged residual allowance.  The second
exceeds it by exactly

```text
10,578,375,691,844,217.
```

This makes rank `50`, not a vague asymptotic regime, the nearest explicit
threat.

### 4.3 Exact one-pencil payment

The moving-root certificate uses

```text
moving points          = 2,097,152
moving roots per slope =   981,104.
```

Since

\[
 2{,}097{,}152<3\cdot981{,}104=2{,}943{,}312,
\]

three counted finite slopes are impossible.  The integrated finite C8 spine
also demonstrates the required discipline: raw chart projections overlap,
actual first-match deletion removes the duplicates, and the resulting
one-pencil leaf has exactly two distinct slopes.  That calibration proves the
interface and the cap, not deployed exhaustive coverage.

### 4.4 Consistency with the existing KoalaBear theorem pool

The following exact proved payments are all far below the rank-49 block scale:

```text
fixed-union MCA, nullity <= 2:       2,847,909,263,951
rank-regular fixed union, nu<=4982:             94,008
one complete correction ray:                 1,963,173
paving separated direction defect: paid through nullity 9
clone-residual parameter cuts: e<=8,564 and b0<=9,812.
```

The first three are direct slope/rich-point counts or safe overcounts of slopes;
the latter two are exact parameter-range payments.  They support the proposed
geometry: low-nullity, regular, separated-direction, and one-ray pieces are
already much cheaper than the conjectured generic block.

They do **not** prove `(KBR2)`.  No integrated adapter currently shows that
these packages exhaust `R2`, and this note does not sum support counts as if
they were slopes.

### 4.5 Q-floor consistency

The unconditional Q floor

```text
57,198,030,365
```

is below both conditional Q caps.  The floor neither contradicts nor supports
a particular residual size, but it confirms that the proposed law is not based
on pretending the Q cell is negligible.  The tangent-rooted cap is roughly
seven times that floor, and its full value is charged in the closure arithmetic.

## 5. Evidence against and nearest threats

1. **A proper rank-50 block is numerically dangerous.** The proved generic
   bound at dimension `50` already exceeds the entire merged residual
   allowance.  A theorem merely saying “the correction span has bounded
   dimension” is insufficient; the boundary must be `49`, or rank `50` needs
   extra structure.

2. **Positive-dimensional rank-flat and clone components are real.** The
   current spread-residual theorem identifies them as the surviving
   nonproper mechanisms; it does not prove that they split into primitive
   pencils.  This is the main mathematical risk to `(PEN)`.

3. **One coherent correction space is unproved.** Different 32-slope seeds
   could a priori produce incompatible cores or owner normalizations.  The
   conjecture needs a line-global coherence theorem strong enough to prevent a
   sum of many proper blocks.

4. **The chart census could be exponential.** The cap in `(KBR2-4)` is very
   large but finite.  An exponentially large family of genuinely distinct
   projective correction directions could exceed it even though each direction
   contributes only one or two slopes.

5. **Large-owner rational atoms may not present as proper core corrections.**
   The normalization step must either embed them in the single proper block,
   coalesce them into pencil keys, or show that the lone scalar exception is
   the only leftover.  Existing owner localization alone does not do this.

6. **Support abundance is not evidence for slope abundance.** Conversely, a
   huge support family may collapse to one slope, so neither a large support
   census nor a support counterexample decides this law without the exact
   projection.

## 6. What would prove it

A proof can be organized into five named inputs.

### Input A: canonical post-Q core/owner normalization

For every line with nonempty `R2`, choose a canonical first 32-slope core or a
coherent large-owner normalization.  Use the kernel dictionary, slope-degree
barrier, atom extraction, and coherence theorem to prove that every residual
slope is represented relative to this same normalization.  Lines with fewer
than 32 residual slopes are harmless and may be absorbed into the pencil or
exception part.

### Input B: rank-49 proper-block extraction

Construct one correction space `W_r` and prove that all residual points whose
coordinate hypersurfaces meet properly lie in one proper subspace of dimension
at most `49`.  The exact payment is then the proved proper-intersection
compiler.  If the initial span has dimension at least `50`, use the
minimum-distance support excess, fixed-union, paving, and clone-tolerant inputs
to extract a paid direction or a nonproper component before charging the
proper block.

### Input C: nonproper component-to-pencil theorem

Starting from the existing dichotomy for a nonproper tuple, prove that every
surviving evaluation rank-flat or exact polynomial clone component, after the
frozen tangent and Q deletions, has projective correction dimension one.  Then
construct its genuine moving-root certificate and apply `thm:bc-moving-root` /
`cor:bc-one-pencil`.

This is the heart of the conjecture.  It must prove the slope parameter injects
into the pencil parameter; a statement about support locators alone is not
enough.

### Input D: normalized chart census

Quotient raw component descriptions by equal projective correction direction
and equal post-deletion slope fibre.  Prove the line-local bound

\[
 |\mathcal C(r)|\le30{,}119{,}370{,}885{,}234{,}533.
\]

Promising counting resources are independent evaluation bases, rank-flat
closures, owner-pair collision rigidity, and the fact that a nonzero affine
coordinate function vanishes at only one finite slope.  The census must be
performed after first-match coalescing.

### Input E: exact first-match projection

Prove `(KBR2-1)` as a disjoint equality of distinct finite slopes, not merely a
cover of supports.  This includes:

```text
support/explanation -> projective correction direction -> finite slope,
```

uniqueness after the frozen owner order, and deletion of duplicate slopes
between the proper, pencil, and exceptional blocks.

Once Inputs A--E are available, the Lean compiler in the accompanying module
proves the uniform law, and the existing four-atom arithmetic closes the row
under `KB_TANGENT_ROOTED_Q_SHELL(3,7)`.

## 7. What would kill it

### 7.1 Sharp cardinal falsifier

One admissible received line with

\[
 |R_2(r)|\ge137{,}490{,}163{,}860{,}629{,}057
\]

kills the uniform law immediately.  A certificate consists of the received
pair, that many distinct finite slopes, one exact agreement witness per slope,
and exact first-match checks showing that none belongs to `T(r)` or `Z_Q(r)`.
All checks are finite over the deployed field.

### 7.2 Rank-50 geometric falsifier

A sharper mechanism-level falsifier is an admissible line carrying one proper
50-dimensional correction space with at least

\[
 137{,}490{,}163{,}860{,}629{,}057
\]

distinct post-Q residual slopes, all outside the scalar exception and with no
legal primitive-pencil reassignment.  Properness, richness, slope distinctness,
and first-match survival are finite determinant/evaluation checks.  The current
proper-intersection theorem allows such a count numerically, so this is the
nearest honest threat rather than a fantasy obstruction.

### 7.3 Exact cover-number falsifier

For a fixed received line, enumerate all legal rank-49 proper blocks and all
normalized primitive pencil fibres.  Remove the best proper block and one
exceptional slope.  If every remaining exact slope cover needs more than

```text
30,119,370,885,234,533
```

pencil keys, `(PEN)` is false even when `|R2(r)|` itself is below the final cap.
This is a finite set-cover certificate and directly tests the conjectured
mechanism.

## 8. Routes killed in this round

* **Raw support/locator census:** rejected.  It does not count distinct MCA
  slopes without a proved projection multiplicity.
* **One-pencil payment without chart exhaustion:** rejected.  The per-chart cap
  is proved; the live wall is the normalized chart census.
* **Generic proper dimension 50:** rejected.  Its exact bound exceeds the
  closure threshold by `10,578,375,691,844,217`.
* **Summing the FU/PAV/CR theorem pool directly:** rejected.  The constants are
  genuine, but no first-match adapter binds their hypotheses to a partition of
  `R2`.
* **Reopening the archived balanced-core problem:** unnecessary.  The statement
  is about the merged set `R2` and never requires a BC-specific certificate.
* **Using the Q floor as an upper estimate:** invalid.  It is a lower bound.
* **Claiming closure from the congestion cap:** false for the displayed `N` by
  an exact gap of `21,109,322,821`.

## 9. Lean formalization and proof-status boundary

The stdlib module is

```text
experimental/lean/asymptotic_spine/AsymptoticSpine/KoalaBearMergedResidual.lean
```

It contains:

* `ResidualSlopeAtlas`, whose lists are duplicate-free and whose
  `coalescedCharge` is explicitly slope-level;
* `rank49OrPencilLaw`, the conjectural `Prop` with every quantifier exposed;
* `uniformMergedResidualLaw`, the universal form of `max_r |R2(r)| <= N`;
* `rank49OrPencil_implies_uniform`, a proved logical/numerical compiler that
  constructs no Reed--Solomon atlas;
* exact row, field-order, budget, rank-49, rank-50, closure, congestion, Q-floor,
  and theorem-pool arithmetic;
* one small finite atlas instance proving the definitions are jointly
  satisfiable; and
* a `#print axioms` census for every theorem.

The conjecture is a definition only.  There is no `sorry`, no axiom asserting
it, and no theorem claiming the deployed Reed--Solomon line satisfies it.

Small structural and simple literal arithmetic proofs use `decide`.  The large
field-order and falling-factorial evaluations use `native_decide`; their axioms
census therefore discloses the generated theorem-local native-decision axiom.
Green compilation proves the arithmetic only.  It does not upgrade `(KBR2)` from
conjecture to theorem.

## 10. Current best law, standalone

For every admissible KoalaBear received line `r`, the distinct finite-slope
residual

\[
 R_2(r)=(Z(r)\setminus T(r))\setminus Z_Q(r)
\]

has a fixed-first-match slope partition into: one proper correction-space image
of dimension at most `49`, containing at most
`77,251,422,090,159,989` slopes; at most one scalar-degenerate slope; and at
most `30,119,370,885,234,533` normalized primitive one-parameter pencil fibres,
each containing at most two distinct finite slopes.  Therefore

\[
 \boxed{\max_r |R_2(r)|\le137{,}490{,}163{,}860{,}629{,}056.}
\]

This statement is a conjecture.  Under the separate conditional hypothesis
`KB_TANGENT_ROOTED_Q_SHELL(3,7)`, it pays both remaining atoms in the frozen
four-atom ledger and closes the KoalaBear MCA row with one unit of arithmetic
slack.
