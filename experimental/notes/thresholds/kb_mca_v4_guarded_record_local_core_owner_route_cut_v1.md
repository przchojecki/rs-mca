---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: "Record-local cores do not define disjoint slope owners; a global-core-first compiler is disjoint, coherent degree-31 empty-core forests are impossible, first source changes are correction rays, and the complete selected forest fits the KoalaBear budget whenever its affine error rank is at most three."
architecture: GRANDE_FINALE_V4_SAE
partition_digest: "ACTIVE_V4_SOURCE_SHA256=03b8806c5e71ebd41a97012fbdcc6442dabd4c8bf9383b7d832a48b0c55ce5ab; exact banking chronology remains unfrozen"
atom_or_cell: "S/E common-core forest; LOCAL_EMPTY_ORDER_32_CORE and HIGH_ALL_RAY_AFFINE_DIMENSION_AT_LEAST_4 remain"
quantifier: "every already-declared active-v4 first-match residual slope set on one actual received line, subject to the theorem's printed guards"
projection_and_unit: "distinct finite affine bad slopes per actual received line; one selected complete actual pair per slope"
claimed_bound: "157397034144292985 through affine error rank three, with disjoint 2w+31 add-back and signed slack 117583693966967127; deployed ledger movement zero"
status: PROVED
impact: ROUTE_CUT
falsifier: "an actual guarded record-local core invariant, a coherent degree-31 empty-core forest, a non-ray 31-overlap source change, or an affine-rank-at-most-three selected family exceeding the printed exact cap"
replay: "python3 experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.py --check && python3 -O experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.py --check && python3 experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.py --tamper-selftest && /usr/local/bin/sage experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.sage && /Users/scott/math_code/.venv/bin/python experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1_flint.py"
---

# Guarded actual-record route cut for the common-core forest

**Status:** independently reviewed finite route cut; no deployed-row payment.
The abstract theorems and certificate are GREEN, while active-v4 chronology
and any deployed banking remain YELLOW and open.

## 1. Scope and conclusion

This packet is stacked on PR #1163 at exact head
`e26c15b2d2c2f98ae12dda17b97c40981f76e1ff`.  It audits the first ownership
rule proposed for the direct Grande Finale v4 S/A/E common-core forest:

> assign an actual bad slope to the fixed-core family determined by the
> common intersection of the maximal supports in a local critical record.

That rule is false.  Over

\[
 \operatorname{RS}[\mathbb F_{11},\mathbb F_{11}^{\times},5]
 \quad\text{at agreement }m=7,
\]

one actual received line has seven support-wise MCA-bad slopes with unique
degree-`<5` explanations.  Its seven realizable critical order-six records
have three different record-local cores:

```text
{8,10} : 1 record
{10}   : 5 records
{5,10} : 1 record.
```

Every displayed slope occurs in records with at least two different cores;
five slopes occur with all three.  Hence record-local core identity is not a
slope invariant and direct record-to-core assignment double-charges slopes.

The route cut is deliberately narrow.  The complete seven-slope family has
global core `{10}`, so this fixture does not refute a line-global priority or
same-owner maximum theorem.  It proves that such a theorem is additional
mathematics: it cannot be replaced by local canonicalization.

## 2. Exact guarded record

Order the domain as `1,...,10`.  The received line is

```text
u = (0,1,4,10,9,6,9,4,3,0)
v = (7,2,10,7,9,5,2,2,9,3).
```

For slopes `0,2,3,5,6,8,9`, the certificate prints one coefficient vector
of length five and its exact seven-point maximal agreement support.  Exhausting
all `C(10,5)=252` interpolation seeds at each slope proves that this is the
unique degree-`<5` explanation with at least seven agreements.  Interpolating
`u` and `v` separately on the identical support shows that at least one has
degree at least five, so every record is support-wise noncontained.

The shifted-lattice minimum is recomputed from the literal matrix

\[
 (W,N)\longmapsto
 \bigl(W(x)(u(x)+\gamma v(x))-N(x)\bigr)_{x\in D}
\]

with

\[
 s_5(W,N)=\max(\deg W,\deg N-4).
\]

For all seven slopes the exact minimum is

\[
 d_1=3=w+1,
 \qquad w=m-k=2.
\]

Thus none is in the near-rational stratum `d1<=w`.  The actual locator pair
`W=Lambda_(D\S)`, `N=Wh` also satisfies the exact degree guard
`s_5(W,N)<=omega`, with `omega=n-m=3`; no silent `K=k+1` transport is used.

The explanations are not one affine polynomial line.  All seven
`6`-subsets are enumerated, rather than selecting only the two records first
reported by public-DAG commit `83eefd94f`.  That public-DAG fixture and its
whole-line global-core continuation `be4efd23a` are prior provenance, not
novel claims of this packet.  The new branch begins at the empty-global-core
coherence fence below.

## 3. Deployed guard layer

The packet keeps the KoalaBear units frozen as distinct finite affine bad
slopes per actual received line.  It imports, but does not reprice, the proved
near-rational owner

\[
 2w=134944.
\]

This charge is separate from the 31-slope exception reserve:

\[
 2w+31=134975,
 \qquad
 B_*-(2w+31)=274980728111260112.
\]

The #1160 line is a mandatory negative BC regression.  Its displayed slope
words have a locator witness of shifted degree at most `67471`, strictly below
the balanced guard `w=67472`; they therefore terminate at
`NEAR_RATIONAL_2W`, never in the common-core forest or the 31-slope reserve.

## 4. Global-core-first compiler

The collision does not prevent a stronger canonical compiler.  Fix any
already-declared first-match residual slope set `Z` of at least 32 slopes on
one received line and,
for every slope, choose the first complete realizable tuple in the pinned
field/domain/coefficient order.  Let `S_gamma` be its maximal agreement
support and put

\[
 G_Z=\bigcap_{\gamma\in Z}S_\gamma,
 \qquad c_Z=|G_Z|.
\]

### Theorem 4.1 (global-core-first ownership)

The following is a total, disjoint line-level compiler.

1. Earlier owners are retained before `Z` is formed.
2. If the selected explanations are globally affine, all of `Z` goes to the
   existing global-affine owner.
3. If they are non-affine and `G_Z` is nonempty, then `c_Z<k` and the entire
   set `Z` is one fixed-core family.  Apply the #1163 cancellation adapter
   once with `C=G_Z`.  Every slope, maximal support, and explanation has the
   stated image and inverse.  For each slope #1163 supplies at least one
   compatible noncontained size-`m` witness containing `G_Z`; the inverse is
   typed on such core-containing witnesses.  No arbitrary witness omitting a
   core point is claimed preserved, and no local critical-record core is used
   as an owner.
4. Writing `s=k-c_Z`, the resulting family terminates exactly as in #1163:
   `FIXED_CORE_GENERIC_PAID_s_LE_2`; under shortened direction separation,
   `DIRECTION_SEPARATED_PAID_3_LE_s_LE_13`; otherwise
   `DIRECTION_LIST_SHORTENED_s` for `3<=s<=13`; or
   `COMMON_CORE_SHORTENED_s_GE_14` for `s>=14`.
5. If `G_Z` is empty, all of `Z` goes to the single explicit residual
   `EMPTY_GLOBAL_CORE_WITH_LOCAL_CRITICAL_CORES`.

The proof is set-theoretic except for the imported #1163 adapter.  The
complete-tuple order selects one actual record per slope.  Intersection over
the whole selected line is unique.  When it is nonempty, it lies in every
selected maximal support, so #1163 applies to the whole family simultaneously
and proves `c_Z<k` in the non-affine case.  The five terminals are mutually
exclusive by `s` and the direction-separation predicate.  When the
intersection is empty, the declared residual is exhaustive by definition.
Thus every slope of `Z` is compiled once, and there is no sum over core
choices.

The GF(11) order-six atlas is the exact small-row control for this mechanism:
`G_Z={10}`, `c_Z=1`, and `s=4`.  Without a
proved shortened direction-separation certificate, the exact output is
`DIRECTION_LIST_SHORTENED_4`.  The three record-local cores are regression
data only; they do not affect ownership.

This theorem closes the ownership/add-back ambiguity on the nonempty-global-
core branch.  It does not pay every such branch: the #1163 staircase residuals
remain literal.  Its new maximal residual is

```text
EMPTY_GLOBAL_CORE_WITH_LOCAL_CRITICAL_CORES.
```

That is the next source-bound S/A/E target.

Subsequent public-DAG composition `fc74e16cd` sharpens the separate nonempty-
global-core KoalaBear branch to the first residual cell
`s=r=14, 31769<=e<=1044245`.  This packet neither imports nor duplicates that
arithmetic chain.  Its remaining claims concern the empty/noncoherent forest.

### Theorem 4.2 (degree-31 coherent forests have a global core)

There is a sharper exact fence on that residual.  Let `Z` contain at least
32 slopes with maximal supports `S_gamma`.  Suppose:

1. every 32 of the supports have nonempty intersection; and
2. all selected explanations are evaluations of one polynomial

   \[
   H(X,Z)=\sum_{j=0}^{31}H_j(X)Z^j,
   \qquad \deg H_j<k.
   \]

Then the whole family has nonempty global core.

Indeed, assume the complements `D\S_gamma` cover `D`, and choose an
inclusion-minimal covering subfamily indexed by `I`.  Because every
32-subfamily of supports intersects, no 32 complements cover `D`, so
`|I|>=33`.  Minimality supplies, for every `i in I`, a private point `x_i`
which lies in `S_j` for all `j!=i` but not in `S_i`.  At that point the
coordinate error polynomial

\[
 E_{x_i}(Z)=H(x_i,Z)-r_0(x_i)-Zr_1(x_i)
\]

vanishes at the `|I|-1>=32` distinct slopes indexed by `I\setminus\{i\}`.
Its degree is at most 31, hence it is identically zero.  But maximality of
`S_i` and `x_i notin S_i` give `E_{x_i}(gamma_i) != 0`, a contradiction.

The constants are sharp at the set-system/root-count level.  Four supports
`S_i={0,1,2,3}\setminus\{i\}` are 3-wise intersecting with empty total
intersection, and over `GF(5)` the degree-three polynomials

\[
 E_i(Z)=\prod_{j\ne i}(Z-j)
\]

vanish on every off-diagonal label and not on label `i`.  Degree two cannot
do so.

Consequently an empty-global-core line must terminate in at least one of

```text
LOCAL_EMPTY_ORDER_32_CORE
NONCOHERENT_DEGREE_31_SOURCE_FOREST.
```

This is a genuine strengthening of the route cut, but not yet a deployed
owner.  The active source constructs the coefficientwise degree-31
interpolant `H` for one fixed order-32 core.  It does not state that the
interpolants attached to all overlapping common-core records are identical.
Thus the remaining bridge is exactly source coherence/transport across
31-overlaps, not the existence of another local core or another generic
sunflower estimate.

### Theorem 4.3 (every first source change is one correction ray)

The transport across one 31-overlap is nevertheless exact.  Let two
order-32 records share the slopes `J`, with `|J|=31`, and let `H,H'` be their
coefficientwise interpolants of `Z`-degree at most 31.  On every shared slope
they give the identical selected explanation.  Hence, coefficientwise in
`X`, their difference has the 31 distinct roots in `J`.  Therefore

\[
 H'(X,Z)-H(X,Z)=P(X)L_J(Z),
 \qquad L_J(Z)=\prod_{\gamma\in J}(Z-\gamma),
 \qquad \deg P<k. \tag{4.1}
\]

The quotient is independent of `Z` because both sides before division have
`Z`-degree at most 31.  If `P=0`, the two source passports are identical.  If
`P!=0` and `eta` is the new slope of the second record, then

\[
 h'_{\eta}(X)=H(X,\eta)+cP(X),
 \qquad c=L_J(\eta)\ne0. \tag{4.2}
\]

This equality preserves the actual received line, slope, explanation, and
maximal support: it is an identity for the already-selected complete record,
not a reconstruction from numerical profile data.  Thus every first
passport change is an actual point on one correction ray.

The source's printed `1,963,173` complete-ray bound assumes that the base
order-32 source is primitive and has empty common support.  That hypothesis
cannot be silently imported here: an overlap edge in this forest may start
from a locally common-core record.  The correct guarded extension is as
follows.  Put

\[
 A=\{x\in D:P(x)=0\ \hbox{and}\ E_x(Z)\equiv0\},
 \qquad E_x(Z)=H(x,Z)-r_0(x)-Zr_1(x).
\]

Every rich point on the ray agrees automatically on `A`.  If the family is
not globally affine, first retain the canonical complete rich point at every
realized slope.  This loses no distinct slope and makes the slope indices
distinct.

The set `A` need not equal the exact intersection of the selected maximal
supports: an additional coordinate with `P(x)!=0` can agree along a nonlinear
graph `c=-E_x(gamma)/P(x)`.  We therefore use the following explicit common-
subset extension of #1163, rather than silently invoking its exact-core
statement.  Since `P` is nonzero of degree `<k`,

\[
 |A|\le\deg P<k.
\]

Let `G_A` be the locator of `A`, and let `a_0,a_1` interpolate `r_0,r_1`
there.  The identity `E_x(Z)=0` for every `x in A` says coefficientwise that
`H-a_0-Za_1` is divisible by `G_A`; `P` is divisible by `G_A` as well.  Hence

\[
 H'=\frac{H-a_0-Za_1}{G_A},\qquad P'=\frac P{G_A}
\]

are polynomial, and division of the received line gives a typed shortened
ray `H'(X,gamma)+cP'(X)`.  Exactly as in #1163's exchange argument, every
selected rich slope has a noncontained exact size-`m` witness containing
`A`: otherwise all such supports containing `A` would be pair-contained,
their connected exchange graph and RS injectivity would give one pair on the
maximal support.  Division and the displayed inverse preserve the identical
slope, scalar `c`, selected explanation, maximal support off `A`, and one
compatible noncontained witness.  This proves the needed distinct-slope,
common-subset cancellation without asserting that `A` is the maximal common
core.

Writing `q=k-|A|`, the shortened row is

\[
 (n',k',m')=(R+q,q,d+q).
\]

If `q<=2`, the fixed-family branch is already paid.  Suppose `q>=3`.  On the
shortened domain, a vertical coordinate `P'(x)=0` has a nonzero degree-at-
most-31 error polynomial; otherwise `x` belonged to `A`.  The source's clone
argument therefore applies with at most `floor((R+q)/q)` large affine clone
classes, rather than the original constant two.  Each contributes at most
`t+1` slopes.

For every remaining rich support, all vertical and graph-clone parts have
size at most `q-1`.  Put

\[
 m'=u(q-1)+r,\qquad0\le r<q-1,
\]

and let

\[
 \Xi(m',q-1)=\binom{m'}2-u\binom{q-1}2-\binom r2.
\]

This is the exact minimum number of heterogeneous unordered pairs in a
partition of `m'` points into parts of size at most `q-1`.  The guarded
one-ray count is consequently

\[
 U_{\rm ray}(q)\le
 \left\lfloor\frac{R+q}{q}\right\rfloor(t+1)
 +\left\lfloor
 \frac{31\binom{R+q}{2}}{\Xi(d+q,q-1)}
 \right\rfloor. \tag{4.3}
\]

There is also a short exact proof of the maximum, so the claim does not rest
on a million-point enumeration.  At `q=3`, the two summands are

\[
 342{,}921{,}706{,}230+7{,}486.
\]

For `q>=4`,

\[
 \Xi(d+q,q-1)\ge(q-1)(d+1).
\]

The first summand decreases with `q`.  The relaxed second summand also
decreases on `4<=q<=k`, since

\[
 \frac{(R+q)(R+q-1)}{q-1}
 =(q-1)+(2R+1)+\frac{R(R+1)}{q-1}.
\]

Their joint `q>=4` upper bound is therefore the relaxed `q=4` value
`257,275,964,613`, strictly below the exact `q=3` value.  Exact big-integer
enumeration over every deployed `3<=q<=1048576` independently confirms

\[
 \max_q U_{\rm ray}(q)
 =U_{\rm ray}(3)
 =342{,}921{,}713{,}716
 <B_*.
\]

At `q=k`, (4.3) recovers the printed primitive/no-common value
`1,963,173`.  Thus one guarded correction-ray direction is genuinely paid,
including the locally common-core case, without importing the wrong
hypotheses.

This still is not an aggregate forest payment.  Different overlap edges may
produce different directions `P`; summing `U_ray` over edges or directions
would change the maximum-type chronology into an unproved additive census.
The remaining theorem is now precise: canonically assign every noncoherent
actual slope to its first overlap edge and prove that all realized `P`
directions share one already-paid owner, admit one maximum-type ray compiler,
or have a budget-fitting exact direction multiplicity.  A failure must emit
the first two directions and their complete actual records.

### Theorem 4.4 (selector-free low-rank forest payment)

The integrated all-LineRay affine-core set-pair theorem gives one existing
aggregate gate that must be applied before declaring the multiple-direction
residual primitive.  Take the set `P` of all selected actual
`(slope,explanation)` pairs after the common-support branch.  The error word
is

\[
 e_{\gamma,h}=r_0+\gamma r_1-h.
\]

Its weight is at most `t=n-m=981104`; the RS kernel distance is greater than
`t`; and actual same-support noncontainment is exactly the required
transversality.  Because this packet selects one complete record per slope,
the pair count equals the distinct-slope count.  If `a` is the affine
dimension of all these error vectors, the imported theorem gives

\[
 |Z|=|P|\le {t+a\choose a}.
\]

Exact KoalaBear arithmetic is

| `a` | all-LineRay cap | `B_*-(2w+31)-cap` |
|---:|---:|---:|
| 0 | 1 | 274980728111260111 |
| 1 | 981105 | 274980728110279007 |
| 2 | 481284001065 | 274980246827259047 |
| 3 | 157397034144292985 | 117583693966967127 |
| 4 | 38605872343809750481845 | negative |

Thus every noncoherent forest with `a<=3` has a budget-fitting exact
selector-free payment even after the already-paid, disjoint `2w+31=134975`
add-back.  The first residual is

```text
HIGH_ALL_RAY_AFFINE_DIMENSION_AT_LEAST_4.
```

The imported theorem has a complete handwritten proof and exact finite
verifier, while its Lean file is explicitly only an unproved statement
target.  This packet replays the normal, optimized, and tamper checks; it does
not misreport the Lean target as a formal proof.  Since the theorem has not
yet been inserted into the active v4 S/A/E chronology at this exact joint,
the present packet records the payment gate but keeps deployed ledger movement
zero pending independent source and mathematics review.

## 5. Exact record-local route cut

A deterministic order on complete realizable records can assign each slope
once.  On this fixture the lexicographic selector is total.  That observation
does **not** prove a payment: tie-breaking supplies neither a bound on the
number of realized fixed-core families nor an aggregate projection-fiber or
add-back inequality.

The weakest surviving theorem is consequently:

> On one actual received line, construct a line-global priority on complete
> realizable explanation records and prove an aggregate distinct-slope bound
> for all selected fixed-core families, or prove a same-owner maximum-type
> S/A/E theorem that bypasses this sum.  The theorem must preserve owner and
> chronology and route `LOCAL_EMPTY_ORDER_32_CORE` and
> `NONCOHERENT_DEGREE_31_SOURCE_FOREST` explicitly.  Equivalently, prove
> degree-31 source coherence across the 31-overlap forest; Theorem 4.2 then
> forces one global core.  If coherence fails, use Theorem 4.3 to assign the
> first change to one genuine correction ray and prove the aggregate
> direction bound without summing per-edge charges.  Apply Theorem 4.4 first:
> only affine error rank at least four may remain.

The present terminal is

```text
SEMANTIC_ROUTE_CUT_RECORD_LOCAL_CORE_OWNER_NONINVARIANCE
```

with

```text
U_S movement = U_A movement = U_E movement = 0.
```

## 6. Search and literature record

An exact follow-up search prescribed empty global core, two distinct local
cores, unique actual explanations, same-support noncontainment, and
`d1=w+1`.  It found no fixture in 2,000 deterministic support systems or in
the one-/two-swap neighborhood of the certified record.  This is bounded
negative evidence, not a theorem, and the search program is retained in the
campaign scratch directory.

Sunflower/spread decompositions provide a natural recursive link/core forest,
but their published general losses are exponential in the support size.  No
reviewed theorem located in that literature yields the row-sharp aggregate
bound required here; importing a generic sunflower lemma would not move the
KoalaBear ledger.

## 7. Replays and nonclaims

Python exhausts the actual explanation atlas and hostile mutations.  Sage
independently reconstructs explanations, supports, ranks, and cores.  FLINT
replays every shifted-lattice rank.  Wolfram independently returned the core
histogram, all seven values `d1=3`, non-affinity, and the exact reserve
arithmetic.

No layer cake, moment, Markov, Chebyshev, asymptotic estimate, K3 elimination,
or witness-to-slope multiplicity is used.  This packet does not refute a
line-global compiler, prove S/A/E, move the v4 ledger, close KoalaBear, or
settle the universal four-rate problem.

The fixture is not claimed to survive every active v4 earlier-owner strip.
It survives exactly the actual-degree, same-support, global-affine, and
near-rational guards checked above.  Therefore it refutes the proposed local
core ownership rule, not the full first-match residual.

PR #1156 treats the independent denominator-root/coordinate-clone `(E)`
branch.  No clone payment or source contract from that branch is imported or
re-priced here.
