---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: "Under KB_TANGENT_ROOTED_Q_SHELL(3,7), the proposed rank-49-or-pencil split closes exactly when an independently derived normalized primitive-pencil chart count N satisfies N <= 30119370885234533 (closure_comparison_iff). The predecessor's printed N equals the closure threshold solved backwards (predecessor_chart_count_is_threshold_derived), not a census. Exact first-match ownership, duplicate-free chart keys, pairwise-disjoint fibres, and the two-slope moving-root cap admit arbitrarily many charts (local_conditions_do_not_bound_chart_count), so they cannot imply Input D. The KoalaBear law is therefore neither proved nor refuted; this is a certified route cut requiring new Reed-Solomon geometry."
architecture: LIST_B_K_LANE_FOUR_ATOM_LEDGER
partition_digest: actual-first-match-post-tangent-post-q-merged-residual
atom_or_cell: R2 rank-49 proper block or primitive one-parameter pencils or scalar exception
quantifier: "Under KB_TANGENT_ROOTED_Q_SHELL(3,7), every actual received line for the desired law; unconditionally, every natural bound in the abstract local-interface independence theorem."
projection_and_unit: "Distinct affine bad slopes per received line; normalized nonempty primitive-pencil chart keys after slope-level first-match deletion and coalescing."
claimed_bound: "properRank49Cap + 1 + 2*N <= 137490163860629056 iff N <= 30119370885234533 (proved). No independently derived deployed N is proved. The ambient field-size census is independent but nonclosing."
status: PROVED
impact: ROUTE_CUT
falsifier: "A source-bound theorem constructing the actual post-Q normalized primitive-pencil atlas and deriving its chart count independently of the closure threshold; an actual first-match residual configuration outside the three proposed cells; or an actual derived chart-census lower bound above 60238741770469066."
replay: "Lean 4.31.0, stdlib only, from experimental/lean/asymptotic_spine: lake build AsymptoticSpine.KoalaBearMergedResidual AsymptoticSpine.KoalaBearRankOrPencilS1 AsymptoticSpine. Integer audit: python3 experimental/scripts/verify_kb_rank_or_pencil_stop.py --check and --tamper-selftest."
consumers: "The KoalaBear merged-residual packet (experimental/notes/thresholds/kb_merged_residual_rank49_pencil_conjecture.md, AsymptoticSpine/KoalaBearMergedResidual.lean). A future Input C+D producer theorem constructing the actual post-Q primitive-pencil atlas and its target-independent chart count is the named successor; its output feeds closure_comparison_iff."
risk_limits: "Every row-closure line is conditional on KB_TANGENT_ROOTED_Q_SHELL(3,7). All of Inputs A-E remain OPEN; no deployed Reed-Solomon producer is supplied. The independence and obstruction results are proved over an abstract two-slope list model; that model is NOT a Reed-Solomon residual configuration and does NOT refute the KoalaBear law."
---

# KoalaBear merged residual: the rank-or-pencil census is an independent theorem

**State:** `CERTIFIED STOP / ROUTE CUT / OPEN GAP`

## Request worked from

Prove or refute the KoalaBear merged-residual rank-or-pencil law on the actual
first-match residual, with a normalized primitive-pencil chart census derived
independently of the closure threshold; otherwise provide a precise certified
obstruction.

## Abstract

Under the standing conditional `KB_TANGENT_ROOTED_Q_SHELL(3,7)`, the predecessor
proved an axiom-free compiler from a supplied rank-49-or-pencil atlas to the
desired residual bound.  It did not construct the actual post-Q Reed--Solomon
atlas or count its normalized primitive-pencil charts.  This note attempts to
supply that missing census.

The result is a certified stop rather than a proof or an actual-residual
counterexample.  First, the exact closure inequality is

```text
77,251,422,090,159,989 + 1 + 2N
  <= 137,490,163,860,629,056
iff
N <= 30,119,370,885,234,533.
```

The number on the right is exactly the threshold remainder divided by two.  It
is therefore a target-derived allowance, not a chart census.  Second, the local
facts already available from the one-pencil compiler---duplicate-free chart
keys, exact first-match ownership, pairwise-disjoint fibres, and at most two
slopes per fibre---do not imply any numerical chart bound.  A kernel-checked
family has `m` distinct chart keys and exactly two disjoint slope tokens over
every key for every natural `m`.  Hence a new theorem about the actual
Reed--Solomon correction geometry is logically indispensable.

The source-free ambient bound obtained by choosing one slope from every nonempty
disjoint chart is independently derived from the field size, but it is
astronomically too large.  None of Inputs A--E is fully discharged.  In
particular, Input D is now certified to be independent of the local
pencil-payment and first-match axioms.  The actual law remains a conjecture.

## 1. Frozen row contract

Every row-closure statement below carries the standing conditional

```text
KB_TANGENT_ROOTED_Q_SHELL(3,7).
```

The frozen values are:

| quantity | exact value | status and derivation |
| --- | ---: | --- |
| agreement | `1,116,048` | frozen row identifier |
| `B*` | `274,980,728,111,395,087` | frozen target budget |
| `U_paid` | `981,104` | frozen paid ledger |
| `U_Q` | `<= 400,389,155,870` | conditional on `KB_TANGENT_ROOTED_Q_SHELL(3,7)` |
| post-Q reserve | `274,980,327,721,258,113` | `B* - U_paid - 400,389,155,870` |
| residual closure threshold | `137,490,163,860,629,056` | `floor(post-Q reserve / 2)` |
| proper rank-49 cap | `77,251,422,090,159,989` | derived from `properCorrectionBound(49)` and kernel checked in the predecessor |
| scalar-degenerate cap | `1` | proposed atlas cell cap |
| one-pencil slope cap | `2` | moving-root incidence consequence |

The residual under study is the actual first-match family

```text
R2(r) = (Z(r) \ T(r)) \ Z_Q(r),
```

where tangent ownership precedes Q ownership, and the desired remaining
ownership order is:

```text
one proper rank-<=49 correction block
  > coalesced normalized primitive one-parameter pencil charts
  > at most one scalar-degenerate exception.
```

This note does not change the predecessor's 17 deployed arithmetic theorems or
its conditional compiler.

## 2. Current best statements

### Theorem 2.1 — exact closure comparison

**Claim under `KB_TANGENT_ROOTED_Q_SHELL(3,7)`.**  Suppose the actual first-match
residual satisfies the predecessor's three-cell law and suppose `N` is an
independently derived count of normalized, nonempty, primitive pencil charts
after coalescing.  Then this split closes exactly when

```text
properRank49Cap + 1 + 2N <= closureThreshold,
```

and numerically this is equivalent to

```text
N <= 30,119,370,885,234,533.
```

This is kernel checked as

```text
AsymptoticSpine.KoalaBearRankOrPencilS1.closure_comparison_iff.
```

At one chart beyond that allowance, the charged bound is exactly

```text
137,490,163,860,629,058 = closureThreshold + 2,
```

kernel checked by

```text
AsymptoticSpine.KoalaBearRankOrPencilS1.first_failing_chart_count_exact.
```

### Theorem 2.2 — the predecessor chart constant is threshold-derived

**Claim under `KB_TANGENT_ROOTED_Q_SHELL(3,7)`; the conditional is carried but
not used by the arithmetic.**  Define

```text
leftoverPencilSlopeBudget
  = closureThreshold - properRank49Cap - 1
  = 60,238,741,770,469,066.
```

Then

```text
30,119,370,885,234,533
  = leftoverPencilSlopeBudget / 2,
```

and twice that number is exactly the leftover budget.  This is kernel checked by

```text
AsymptoticSpine.KoalaBearRankOrPencilS1.
  predecessor_chart_count_is_threshold_derived.
```

Therefore the predecessor constant is not evidence for Input D.  Its derivation
direction is target-to-count, not geometry-to-count.

### Theorem 2.3 — local first-match pencil data imply no census

**Claim under `KB_TANGENT_ROOTED_Q_SHELL(3,7)`; the conditional is carried but
unused by this structural theorem.**  For every natural bound `b`, there is an
explicit finite list model with `b+1` normalized chart keys such that:

1. the chart-key list is duplicate-free;
2. every chart fibre is duplicate-free and has exactly two slope tokens;
3. different chart fibres are pairwise disjoint;
4. every token lies in the fibre selected by its exact owner; and
5. the flattened token list has length exactly `2(b+1)`.

The model is

```text
charts(m)       = [0, 1, ..., m-1],
slopes(c)       = [(c,false), (c,true)],
owner(c,branch) = c.
```

The universal unboundedness theorem is kernel checked as

```text
AsymptoticSpine.KoalaBearRankOrPencilS1.
  local_conditions_do_not_bound_chart_count.
```

It bundles conditions 1--3 and 5 through `LocalTwoSlopeConditions`; condition 4
(exact first-match owner membership) is the supporting theorem
`model_slope_mem_owner_pencil`.  The full supporting checked declarations are:

```text
model_chart_count_exact
model_charts_nodup
model_pencil_count_exact
model_pencil_nodup
mem_modelPencilSlopes_iff
model_pencil_pairwise_disjoint
model_slope_mem_owner_pencil
flatMap_modelPencilSlopes_length
model_slope_count_exact
model_local_conditions.
```

Consequently, the moving-root cap and exact slope-level first-match disjointness
cannot derive Input D.  Primitive Reed--Solomon geometry must do additional work.

### Corollary 2.4 — exact mechanism-level boundary model

**Claim under `KB_TANGENT_ROOTED_Q_SHELL(3,7)`; the conditional is carried but
unused by the model.**  Instantiating the abstract model at

```text
m = 60,238,741,770,469,067
  = censusRefutationBoundary + 1
```

gives exactly

```text
120,477,483,540,938,134
```

pairwise-disjoint slope tokens.  The proposed split charge becomes

```text
77,251,422,090,159,989 + 1
  + 2 * 60,238,741,770,469,067
= 197,728,905,631,098,124
> 137,490,163,860,629,056.
```

The chart count, slope-token count, local conditions, and failed split are
checked by

```text
obstruction_model_chart_count_exact
obstruction_model_slope_count_exact
obstruction_model_local_conditions
obstruction_model_split_fails.
```

Yet the model's direct slope-token count is still below the closure threshold by

```text
17,012,680,319,690,922,
```

checked by

```text
obstruction_model_direct_size_fits.
```

This distinction is load-bearing: the model refutes inference from the local API
to a chart census, not the direct KoalaBear residual bound.  It is a route cut,
not an actual Reed--Solomon counterexample.

## 3. Derivation-direction ledger

| number or bound | derived from | independent of the closure target? | evidentiary status |
| --- | --- | --- | --- |
| `77,251,422,090,159,989` | the predecessor's `properCorrectionBound(49)` formula | yes | valid proper-block cap, conditional on actual one-block coverage |
| `60,238,741,770,469,066` | `closureThreshold - properRank49Cap - 1` | no | target remainder, not a census |
| `30,119,370,885,234,533` | the preceding remainder divided by the two-slope cap | no | maximum allowable count, not a census |
| `fieldOrder` | KoalaBear field cardinality | yes | ambient ceiling only |
| `N <= fieldOrder` | choose one representative slope from each normalized nonempty pairwise-disjoint chart | yes | independently derived but nonclosing |
| `60,238,741,770,469,067` in the model | refutation boundary plus one | no | independence witness only, not an RS census |

The independently derived ambient ceiling is

```text
fieldOrder
= 93,571,093,019,388,561,295,270,373,781,649,880,353,786,165,192,103,559,169.
```

For normalized used charts with nonempty disjoint slope fibres, selecting one
slope per chart injects the chart set into the finite slope field.  This gives
`N <= fieldOrder` without using the closure target.  It is nevertheless useless
for closure, and even exceeds the contract's census-refutation boundary.  The
exact failed comparison is checked by

```text
ambient_field_chart_ceiling_is_nonclosing.
```

This was the only general census available without an actual
correction-component classification.

## 4. Audit of the actual first-match obligation

The predecessor formalization

```text
AsymptoticSpine/KoalaBearMergedResidual.lean
```

proves the conditional compiler

```text
rank49OrPencil_implies_uniform
```

without axioms.  However, its law quantifies over abstract `Line`, `Slope`, and
`Chart` types and receives the following objects as parameters:

```text
badSlopes
tangentSlopes
qSlopes
isProperCorrectionBlock
isScalarDegenerateException
isPrimitiveOneParameterPencil.
```

Thus it is a consumer of an actual Reed--Solomon producer; it is not that
producer.

The integrated C8 exhaustion module does not fill the gap.  It proves a
four-chart finite calibration with exact post-deletion cells

```text
[[5], [7,9], [11,13], [17]],
```

pays the finite one-pencil cell, and leaves the named deep residual `[17]`
unpaid.  Its own note explicitly excludes deployed KoalaBear C8 exhaustion and
treats genuine pencil membership and slope-to-parameter injection as external
inputs.  Relevant kernel declarations are

```text
C8MovingRootCertificate.koalaBearMca_slopes_length_le_two
C8ChartExhaustionPacket.postDeletionSlopeCells_nodup
C8ChartExhaustionPacket.mem_postDeletionSlopeCells_iff
c8Spine_movingPencil_paid
c8Spine_deepResidual_exact.
```

Therefore neither the predecessor law nor the finite C8 calibration supplies an
actual map

```text
R2(r) slope -> normalized primitive-pencil chart key,
```

nor a theorem that the normalized key family has a target-independent count.

## 5. Status of Inputs A--E

| input | required content | status |
| --- | --- | --- |
| **A** | canonical post-Q core and owner normalization on every actual line | `OPEN`; no concrete deployed producer was found |
| **B** | all proper survivors lie in one rank-`<=49` proper block | `OPEN`; the cap formula is proved, but actual one-block coverage is not |
| **C** | every nonproper rank-flat/clone component becomes a genuine primitive projective-dimension-one moving-root pencil with slope injection | `OPEN`; the moving-root theorem only pays a supplied genuine pencil |
| **D** | normalized chart census after coalescing, derived independently of the target | `OPEN / INDEPENDENT`; local first-match plus two-slope data provably have unbounded models |
| **E** | exact actual slope-level first-match equality, projection, and disjointness | `OPEN`; the predecessor stores this as atlas data, and the finite calibration is not deployed exhaustion |

No single Input A--E is completely discharged.  The full-value result is the
precise obstruction for Input D: it cannot be a corollary of the already-proved
local pencil payment or of abstract first-match disjointness.

## 6. Routes killed

### 6.1 Inheriting the predecessor count

Killed by `predecessor_chart_count_is_threshold_derived`.  The constant is
exactly the target remainder divided by two.

### 6.2 Inheriting the sibling all-pencil count

The sibling quantity `68,745,081,930,314,528 = closureThreshold / 2` has the
same target-to-count derivation direction.  It is not evidence.

### 6.3 Multiplying "two slopes per pencil" by an unstated number of pencils

Killed by `local_conditions_do_not_bound_chart_count`.  The local mechanism
permits arbitrary chart multiplicity.

### 6.4 Counting charts by the ambient slope field

This count is genuinely independent of the target, but
`ambient_field_chart_ceiling_is_nonclosing` proves that it is much too large.

### 6.5 Promoting the finite C8 calibration to deployed exhaustion

Killed by the calibration's explicit scope: it has four fixture charts and one
named unpaid deep residual, not the actual KoalaBear first-match residual on
every line.

### 6.6 Calling the abstract boundary model an RS refutation

Rejected.  The model intentionally erases primitive locator geometry.  It proves
logical independence of Input D and even has direct slope-token size below the
threshold.  It is not an admissible received-line residual configuration.

## 7. Evidence for and against the proposed law

### Evidence in favor

- The proper rank-49 block cap is independently derived and kernel checked in
  the predecessor as `proper_rank49_formula_exact`.
- A supplied genuine one-parameter moving-root pencil has at most two slopes; the
  finite specialization is checked by
  `C8MovingRootCertificate.koalaBearMca_slopes_length_le_two`.
- The predecessor compiler `rank49OrPencil_implies_uniform` is axiom-free once an
  actual atlas with the required count is supplied.
- The exact arithmetic has large room for one rank-49 block plus a sufficiently
  small chart family.

### Evidence against treating the law as proved

- No actual post-Q canonical component producer is present in the branch or
  active source interface.
- The current C8 calibration explicitly leaves a higher-dimensional deep residual
  unpaid.
- `prop:q-sp-no-ray` warns that support or pair information does not automatically
  compile to rays or slopes.
- `hyp:ray-compiler` and `prop:curve-degree-ray-compiler` mark the
  higher-dimensional projection as a separate theorem.
- The chart census is not a consequence of first-match disjointness or the
  two-slope bound.

No actual residual configuration outside the three cells was constructed, and no
actual RS chart-census lower bound above `60,238,741,770,469,066` was derived.
Hence the contract's full refutation criterion is not met.

## 8. Natural next step

The next useful theorem must join Inputs C and D rather than revisit arithmetic.
For every actual received line `r`, it should:

1. construct `R2(r)` from the frozen tangent-then-Q owner chronology;
2. assign every nonproper survivor a concrete correction component and canonical
   core;
3. prove that each surviving nonproper component is either an earlier owner,
   scalar-degenerate, or a genuine projective-dimension-one primitive pencil;
4. prove slope-to-pencil-parameter injection;
5. define a normalized key whose equality is exactly primitive-pencil
   coalescence;
6. prove the used key list is nonempty-fibred, duplicate-free, and exhaustive on
   actual slopes; and
7. derive its count from correction geometry, rank-flat incidence, or owner data
   without mentioning `closureThreshold`, `properRank49Cap`, `B*`, or any target
   remainder.

The final comparison is then immediate from `closure_comparison_iff`:

```text
N <= 30,119,370,885,234,533  -> this split closes;
actual lower bound N > 60,238,741,770,469,066
  -> the contract's strong refutation criterion is met.
```

An intermediate count that does not close should trigger a different
decomposition, for example a higher-dimensional curve-degree ray compiler or a
direct residual-cardinality payment, rather than another target-derived split.

## 9. Lean package and validation

### Package

```text
experimental/lean/asymptotic_spine/
```

New module:

```text
AsymptoticSpine/KoalaBearRankOrPencilS1.lean
```

Package root import:

```text
AsymptoticSpine.lean
```

Namespace:

```text
AsymptoticSpine.KoalaBearRankOrPencilS1
```

The module imports only Lean `Init`/stdlib material and the predecessor module.
It imports no Mathlib.  No `sorry`, `admit`, `sorryAx`, unsafe declaration, or
custom axiom occurs.

### `native_decide` disclosure

`native_decide` is used only for closed natural-number comparisons and equalities
in:

```text
predecessor_chart_count_is_threshold_derived
first_failing_chart_count_exact
ambient_field_chart_ceiling_is_nonclosing
obstruction_model_chart_count_exact
obstruction_model_slope_count_exact
obstruction_model_split_fails
obstruction_model_direct_size_fits.
```

Their `#print axioms` output contains the generated theorem-local
native-decision axiom.  The structural model theorems use only standard Lean
principles among `propext`, `Classical.choice`, and `Quot.sound`;
`model_pencil_count_exact` is axiom-free.  `closure_comparison_iff` is closed by
`omega` and depends only on `propext`, `Classical.choice`, and `Quot.sound`.
Every declared theorem has an explicit `#print axioms` census at module end.

### Replay

From `experimental/lean/asymptotic_spine`, on Lean `4.31.0`, stdlib only:

```text
lake build \
  AsymptoticSpine.KoalaBearMergedResidual \
  AsymptoticSpine.KoalaBearRankOrPencilS1 \
  AsymptoticSpine
```

builds the two modules and replays the package default target.  The independent
integer audit is

```text
python3 experimental/scripts/verify_kb_rank_or_pencil_stop.py --check
python3 experimental/scripts/verify_kb_rank_or_pencil_stop.py --tamper-selftest
```

which recomputes every displayed integer (the ambient field order
`fieldOrder = p^6`, the proper rank-49/50 caps from the exact falling-factorial
formula, the ledger chain, the iff boundary, the threshold-derived chart count,
and the obstruction-model charges) in Python bignums and confirms that every
pinned constant is sensitive to a one-unit mutation.

Green compilation verifies the Lean statements above.  It does not turn the
abstract model into Reed--Solomon geometry and does not discharge the standing
shell hypothesis.

## 10. References and exact source labels

1. Predecessor note: `experimental/notes/thresholds/kb_merged_residual_rank49_pencil_conjecture.md`.
2. Predecessor Lean: `experimental/lean/asymptotic_spine/AsymptoticSpine/KoalaBearMergedResidual.lean`; declarations `ResidualSlopeAtlas.residual_length_le`, `rank49OrPencil_implies_uniform`, `proper_rank49_formula_exact`, `merged_residual_decomposition_exact`, and `tangent_rooted_shell_closure_is_sharp`.
3. Active workboard: `agents.md`, Lane K, especially K3 "Pay MCA projection and residual geometry."
4. Active architecture: `experimental/grande_finale.tex`; exact labels `thm:bc-moving-root`, `cor:bc-one-pencil`, `prop:q-sp-no-ray`, `hyp:ray-compiler`, `prop:curve-degree-ray-compiler`, and `lem:profile-multiplicity`.
5. First-match lineage: `archived/asymptotic_rs_mca.tex`; exact labels `lem:first-match` and `def:cells`.
6. C8 route-cut note: `experimental/notes/thresholds/c8_chart_exhaustion_route_cut.md`.
7. C8 Lean calibration: `experimental/lean/asymptotic_spine/AsymptoticSpine/C8ChartExhaustion.lean`.
8. Semantic-producer audit: `experimental/notes/audits/c8_c9_semantic_producer_preflight.md`.

## Verdict

Under `KB_TANGENT_ROOTED_Q_SHELL(3,7)`, the exact closure comparison is proved,
but the actual rank-or-pencil law and its independently derived normalized chart
census are not.  The predecessor count is certified as threshold-derived, and the
local pencil/first-match axioms are certified insufficient to imply any census.

# OPEN GAP
