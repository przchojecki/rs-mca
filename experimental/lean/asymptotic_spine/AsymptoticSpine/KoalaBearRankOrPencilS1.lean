import Init.Data.List.Nat.Range
import AsymptoticSpine.KoalaBearMergedResidual

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# KoalaBear rank-or-pencil S1: census-independence stop

This stdlib-only module audits the proposed rank-49-or-pencil closure route for
the actual KoalaBear merged residual.  It does not assert or refute the deployed
Reed--Solomon law.  Instead it kernel-checks two facts that delimit any proof.

1. The predecessor's printed chart count is exactly the closure threshold
   solved backwards after charging the rank-49 block and one exceptional slope.
2. Exact first-match ownership together with exactly two slopes per pencil has
   models with arbitrarily many pairwise-disjoint pencil charts.  Hence the
   moving-root cap and slope-level disjointness alone imply no normalized chart
   census; a deployed Reed--Solomon geometry theorem is indispensable.

The standing row-closure conditional remains
`KB_TANGENT_ROOTED_Q_SHELL(3,7)`.  None of the structural independence results
uses or proves that hypothesis.

`native_decide` is used only for closed natural-number arithmetic.  Its printed
axiom census therefore discloses the generated native-decision axiom.  No
`sorry`, custom axiom, or Mathlib import occurs.
-/

namespace AsymptoticSpine.KoalaBearRankOrPencilS1

open KoalaBearMergedResidual

/-- Exact standing conditional label carried by every row-closure claim. -/
def standingConditionalLabel : String :=
  "KB_TANGENT_ROOTED_Q_SHELL(3,7)"

/-- Slope capacity left after the predecessor charges the proper rank-49 block
and the single scalar-degenerate exception. -/
def leftoverPencilSlopeBudget : Nat :=
  closureThreshold - properRank49Cap - scalarExceptionCap

/-- The predecessor's pencil-chart constant reconstructed from the closure
threshold, rather than counted from Reed--Solomon chart data. -/
def thresholdDerivedChartCount : Nat :=
  leftoverPencilSlopeBudget / onePencilSlopeCap

/-- The contract's chart-census refutation boundary. -/
def censusRefutationBoundary : Nat :=
  closureThreshold - properRank49Cap - scalarExceptionCap

/-- Exact derivation-direction audit: the predecessor chart count is the target
remainder divided by the two-slope charge. -/
theorem predecessor_chart_count_is_threshold_derived :
    leftoverPencilSlopeBudget = 60_238_741_770_469_066 ∧
    thresholdDerivedChartCount = normalizedPencilChartCap ∧
    onePencilSlopeCap * normalizedPencilChartCap =
      leftoverPencilSlopeBudget := by
  native_decide

/-- The exact closure comparison for an independently derived chart count `N`.
No chart census is produced by this theorem. -/
theorem closure_comparison_iff (N : Nat) :
    properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * N ≤ closureThreshold ↔
      N ≤ normalizedPencilChartCap := by
  change
    77_251_422_090_159_989 + 1 + 2 * N ≤
        137_490_163_860_629_056 ↔
      N ≤ 30_119_370_885_234_533
  omega

/-- One chart beyond the threshold-derived count misses the residual threshold
by exactly two slope-charge units. -/
theorem first_failing_chart_count_exact :
    properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * (normalizedPencilChartCap + 1) =
      closureThreshold + 2 ∧
    closureThreshold <
      properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * (normalizedPencilChartCap + 1) := by
  native_decide

/-- The only source-free ambient census, one nonempty disjoint chart per finite
field slope, is arithmetically far too large to close this split.  The theorem
checks only the comparison; obtaining the injection is the elementary
nonempty/disjoint-fibre step. -/
theorem ambient_field_chart_ceiling_is_nonclosing :
    censusRefutationBoundary < fieldOrder ∧
    closureThreshold <
      properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * fieldOrder := by
  native_decide

/-! ## Arbitrarily large exact two-slope first-match models -/

/-- Model chart keys and slope tokens.  The Boolean coordinate is the two-slope
branch inside one chart. -/
abbrev ModelChart := Nat
abbrev ModelSlope := Nat × Bool

/-- Exactly `m` normalized chart keys, represented without duplicates. -/
def modelCharts (m : Nat) : List ModelChart :=
  List.range m

/-- Exactly two distinct slope tokens over one normalized chart key. -/
def modelPencilSlopes (chart : ModelChart) : List ModelSlope :=
  [(chart, false), (chart, true)]

/-- The disjoint-union presentation of all model slope tokens. -/
def modelSlopeList (m : Nat) : List ModelSlope :=
  (modelCharts m).flatMap modelPencilSlopes

/-- Exact first-match owner of one model slope token. -/
def modelOwner (slope : ModelSlope) : ModelChart :=
  slope.1

/-- Exact chart census of the model, derived from `List.range`. -/
theorem model_chart_count_exact (m : Nat) :
    (modelCharts m).length = m := by
  simp [modelCharts]

/-- The normalized model chart list is duplicate-free. -/
theorem model_charts_nodup (m : Nat) :
    (modelCharts m).Nodup := by
  simpa [modelCharts] using (List.nodup_range (n := m))

/-- Every model pencil has exactly two slope tokens. -/
theorem model_pencil_count_exact (chart : ModelChart) :
    (modelPencilSlopes chart).length = 2 := by
  rfl

/-- The two slope tokens in one model pencil are distinct. -/
theorem model_pencil_nodup (chart : ModelChart) :
    (modelPencilSlopes chart).Nodup := by
  simp [modelPencilSlopes]

/-- Membership in a model pencil is exactly equality with its first-match owner. -/
theorem mem_modelPencilSlopes_iff
    (chart : ModelChart) (slope : ModelSlope) :
    slope ∈ modelPencilSlopes chart ↔ modelOwner slope = chart := by
  rcases slope with ⟨owner, branch⟩
  cases branch <;> simp [modelPencilSlopes, modelOwner]

/-- Distinct normalized charts have disjoint slope fibres. -/
theorem model_pencil_pairwise_disjoint
    {first second : ModelChart} (hne : first ≠ second) :
    ∀ slope, slope ∈ modelPencilSlopes first →
      slope ∉ modelPencilSlopes second := by
  intro slope hfirst hsecond
  have hf : modelOwner slope = first :=
    (mem_modelPencilSlopes_iff first slope).1 hfirst
  have hs : modelOwner slope = second :=
    (mem_modelPencilSlopes_iff second slope).1 hsecond
  exact hne (hf.symm.trans hs)

/-- Every slope token lies in the pencil selected by its exact owner. -/
theorem model_slope_mem_owner_pencil (slope : ModelSlope) :
    slope ∈ modelPencilSlopes (modelOwner slope) := by
  exact (mem_modelPencilSlopes_iff (modelOwner slope) slope).2 rfl

/-- Flattening any chart list contributes exactly two entries per chart. -/
theorem flatMap_modelPencilSlopes_length (charts : List ModelChart) :
    (charts.flatMap modelPencilSlopes).length = 2 * charts.length := by
  induction charts with
  | nil => rfl
  | cons chart rest ih =>
      simp [modelPencilSlopes, ih] <;> omega

/-- Exact slope-token census of the model, derived from the chart list and the
two-slope fibre definition. -/
theorem model_slope_count_exact (m : Nat) :
    (modelSlopeList m).length = 2 * m := by
  calc
    (modelSlopeList m).length = 2 * (modelCharts m).length :=
      flatMap_modelPencilSlopes_length (modelCharts m)
    _ = 2 * m := by rw [model_chart_count_exact]

/-- The local semantic content retained after chart construction: duplicate-free
chart keys, duplicate-free two-slope fibres, pairwise first-match disjointness,
and the exact flattened charge. -/
def LocalTwoSlopeConditions (m : Nat) : Prop :=
  (modelCharts m).Nodup ∧
  (∀ chart, chart ∈ modelCharts m →
    (modelPencilSlopes chart).Nodup ∧
    (modelPencilSlopes chart).length = 2) ∧
  (∀ first, first ∈ modelCharts m →
    ∀ second, second ∈ modelCharts m →
      first ≠ second →
      ∀ slope, slope ∈ modelPencilSlopes first →
        slope ∉ modelPencilSlopes second) ∧
  (modelSlopeList m).length = 2 * m

/-- The model satisfies all local first-match and two-slope conditions for every
chart count `m`. -/
theorem model_local_conditions (m : Nat) : LocalTwoSlopeConditions m := by
  refine ⟨model_charts_nodup m, ?_, ?_, model_slope_count_exact m⟩
  · intro chart _
    exact ⟨model_pencil_nodup chart, model_pencil_count_exact chart⟩
  · intro first _ second _ hne
    exact model_pencil_pairwise_disjoint hne

/-- No constant chart census follows from duplicate-free chart keys, exact
pairwise first-match ownership, and the per-pencil two-slope theorem alone. -/
theorem local_conditions_do_not_bound_chart_count (bound : Nat) :
    bound < (modelCharts (bound + 1)).length ∧
    LocalTwoSlopeConditions (bound + 1) := by
  constructor
  · rw [model_chart_count_exact]
    omega
  · exact model_local_conditions (bound + 1)

/-- First abstract chart count beyond the contract's mechanism-level refutation
boundary.  It is derived from that boundary only to instantiate the independence
model, not offered as a Reed--Solomon census. -/
def obstructionModelChartCount : Nat :=
  censusRefutationBoundary + 1

/-- Exact chart count in the boundary independence model. -/
theorem obstruction_model_chart_count_exact :
    (modelCharts obstructionModelChartCount).length =
      60_238_741_770_469_067 := by
  rw [model_chart_count_exact]
  native_decide

/-- Exact flattened slope-token count in the boundary independence model. -/
theorem obstruction_model_slope_count_exact :
    (modelSlopeList obstructionModelChartCount).length =
      120_477_483_540_938_134 := by
  rw [model_slope_count_exact]
  native_decide

/-- The boundary independence model still has duplicate-free normalized keys,
exact pairwise first-match ownership, and exactly two slopes in every chart. -/
theorem obstruction_model_local_conditions :
    LocalTwoSlopeConditions obstructionModelChartCount :=
  model_local_conditions obstructionModelChartCount

/-- Charging the proper cap, exception, and the boundary-model chart census
collapses the proposed split. -/
theorem obstruction_model_split_fails :
    closureThreshold <
      properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * obstructionModelChartCount := by
  native_decide

/-- The same abstract model does not refute the direct residual-cardinality law:
its pairwise-disjoint 120 quadrillion slope tokens still fit below the closure
threshold.  This separates a route cut from a deployed Reed--Solomon
counterexample. -/
theorem obstruction_model_direct_size_fits :
    (modelSlopeList obstructionModelChartCount).length <
      closureThreshold := by
  rw [obstruction_model_slope_count_exact]
  native_decide

#print axioms predecessor_chart_count_is_threshold_derived
#print axioms closure_comparison_iff
#print axioms first_failing_chart_count_exact
#print axioms ambient_field_chart_ceiling_is_nonclosing
#print axioms model_chart_count_exact
#print axioms model_charts_nodup
#print axioms model_pencil_count_exact
#print axioms model_pencil_nodup
#print axioms mem_modelPencilSlopes_iff
#print axioms model_pencil_pairwise_disjoint
#print axioms model_slope_mem_owner_pencil
#print axioms flatMap_modelPencilSlopes_length
#print axioms model_slope_count_exact
#print axioms model_local_conditions
#print axioms local_conditions_do_not_bound_chart_count
#print axioms obstruction_model_chart_count_exact
#print axioms obstruction_model_slope_count_exact
#print axioms obstruction_model_local_conditions
#print axioms obstruction_model_split_fails
#print axioms obstruction_model_direct_size_fits

end AsymptoticSpine.KoalaBearRankOrPencilS1
