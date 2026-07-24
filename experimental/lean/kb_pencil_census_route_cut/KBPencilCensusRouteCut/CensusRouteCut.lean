import Init.Data.List.Nat.Range

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# KoalaBear pencil-census route cut

Self-contained, stdlib-only audit kernel for the K3 pencil-census derivation
question.  It does not assert or refute any deployed Reed-Solomon law, produces
no chart census, and pays nothing.  It kernel-checks the facts that delimit any
future rank-49-or-pencil payment of the K3 residual-geometry obligation:

1. the two pencil-chart constants in circulation are exactly the closure
   threshold solved backwards, so neither is census evidence;
2. exact first-match ownership together with exactly two slopes per pencil has
   models with arbitrarily many pairwise-disjoint pencil charts, so the local
   pencil API cannot imply any chart census;
3. the one source-free ambient census (one chart per field slope) is
   independently derived but astronomically nonclosing.

Every constant is either frozen row data or *derived here* with its conditional
provenance explicit in its name.  `uQConditional` is a conditional bound that is
NOT banked in the live synthesis; every value downstream of it carries the
`Conditional` suffix.  Nothing in this module treats those values as payments.

`native_decide` is used only for closed natural-number arithmetic and is
disclosed by the axiom census at module end.  No `sorry`, custom axiom, or
Mathlib import occurs.
-/

namespace KBPencilCensusRouteCut.CensusRouteCut

/-! ## Frozen row constants (unconditional) -/

def fieldPrime : Nat := 2_130_706_433
def extensionDegree : Nat := 6
def fieldOrder : Nat := fieldPrime ^ extensionDegree
def codeLength : Nat := 2_097_152
def agreement : Nat := 1_116_048
def targetDenominator : Nat := 2 ^ 128

/-- The frozen KoalaBear budget `B*`. -/
def bStar : Nat := 274_980_728_111_395_087

/-- The banked tangent payment `U_paid` (live synthesis, KoalaBear tangent
theorem). -/
def uPaidBanked : Nat := 981_104

/-! ## Conditional threshold chain

`uQConditional` is the conditional `U_Q` bound of the withdrawn merged-residual
proposal.  It is conditional on `KB_TANGENT_ROOTED_Q_SHELL(3,7)` and is NOT a
banked ledger value: the live synthesis does not carry it.  It is reproduced
here only so that the derivation direction of the proposal's own constants can
be certified.  Every downstream value keeps the `Conditional` marker.
-/

def uQConditional : Nat := 400_389_155_870

def postQReserveConditional : Nat := bStar - uPaidBanked - uQConditional

def closureThresholdConditional : Nat := postQReserveConditional / 2

/-- The proposal's remaining cell caps: one scalar-degenerate exception and two
slopes per genuine one-parameter pencil. -/
def scalarExceptionCap : Nat := 1
def onePencilSlopeCap : Nat := 2

/-! ## The proper rank-49 cap, derived from its formula -/

def fallingFactorial : Nat → Nat → Nat
  | _, 0 => 1
  | n, k + 1 => n * fallingFactorial (n - 1) k

/-- The exact proper-intersection compiler specialized to slope degree `31` and
correction-space dimension `s`:
`floor (31 * (s + 1) * choose codeLength (s + 1) / choose agreement (s + 1))`,
evaluated as the equivalent falling-factorial ratio. -/
def properCorrectionBound (s : Nat) : Nat :=
  31 * (s + 1) * fallingFactorial codeLength (s + 1) /
    fallingFactorial agreement (s + 1)

def properRank49Cap : Nat := 77_251_422_090_159_989

/-- The rank-49 cap is the formula value, not a free pin. -/
theorem rank49_cap_formula_exact :
    properCorrectionBound 49 = properRank49Cap := by
  native_decide

/-! ## Exact derivation-direction certifications -/

/-- The frozen field data reproduce the exact ambient order and budget. -/
theorem field_order_and_budget_exact :
    fieldOrder =
      93_571_093_019_388_561_295_270_373_781_649_880_353_786_165_192_103_559_169 ∧
    fieldOrder / targetDenominator = bStar := by
  native_decide

/-- The conditional threshold chain, with every step printed. -/
theorem threshold_chain_exact :
    postQReserveConditional = 274_980_327_721_258_113 ∧
    closureThresholdConditional = 137_490_163_860_629_056 := by
  native_decide

/-- Slope capacity left after charging the rank-49 block and the exception. -/
def leftoverPencilSlopeBudgetConditional : Nat :=
  closureThresholdConditional - properRank49Cap - scalarExceptionCap

/-- The proposal's pencil-chart constant reconstructed from the closure
threshold, rather than counted from Reed-Solomon chart data. -/
def thresholdDerivedChartCount : Nat :=
  leftoverPencilSlopeBudgetConditional / onePencilSlopeCap

/-- The chart-census refutation boundary of the proposal's contract. -/
def censusRefutationBoundary : Nat :=
  closureThresholdConditional - properRank49Cap - scalarExceptionCap

/-- Exact derivation-direction audit: the proposal's chart constant
`30119370885234533` is the target remainder divided by the two-slope charge,
and its sibling constant `68745081930314528` is the bare threshold divided by
two.  Both are target-to-count, not geometry-to-count. -/
theorem chart_constants_are_threshold_derived :
    leftoverPencilSlopeBudgetConditional = 60_238_741_770_469_066 ∧
    thresholdDerivedChartCount = 30_119_370_885_234_533 ∧
    onePencilSlopeCap * thresholdDerivedChartCount =
      leftoverPencilSlopeBudgetConditional ∧
    closureThresholdConditional / 2 = 68_745_081_930_314_528 := by
  native_decide

/-- The exact closure comparison for an independently derived chart count `N`.
No chart census is produced by this theorem. -/
theorem closure_comparison_iff (N : Nat) :
    properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * N ≤ closureThresholdConditional ↔
      N ≤ 30_119_370_885_234_533 := by
  change
    77_251_422_090_159_989 + 1 + 2 * N ≤
        137_490_163_860_629_056 ↔
      N ≤ 30_119_370_885_234_533
  omega

/-- One chart beyond the threshold-derived count misses the residual threshold
by exactly two slope-charge units. -/
theorem first_failing_chart_count_exact :
    properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * (thresholdDerivedChartCount + 1) =
      closureThresholdConditional + 2 ∧
    closureThresholdConditional <
      properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * (thresholdDerivedChartCount + 1) := by
  native_decide

/-- The only source-free ambient census, one nonempty disjoint chart per finite
field slope, is arithmetically far too large to close this split.  The theorem
checks only the comparison; obtaining the injection is the elementary
nonempty/disjoint-fibre step. -/
theorem ambient_field_chart_ceiling_is_nonclosing :
    censusRefutationBoundary < fieldOrder ∧
    closureThresholdConditional <
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
model, not offered as a Reed-Solomon census. -/
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
    closureThresholdConditional <
      properRank49Cap + scalarExceptionCap +
        onePencilSlopeCap * obstructionModelChartCount := by
  native_decide

/-- The same abstract model does not refute the direct residual-cardinality law:
its pairwise-disjoint slope tokens still fit below the closure threshold.  This
separates a route cut from a deployed Reed-Solomon counterexample. -/
theorem obstruction_model_direct_size_fits :
    (modelSlopeList obstructionModelChartCount).length <
      closureThresholdConditional := by
  rw [obstruction_model_slope_count_exact]
  native_decide

#print axioms rank49_cap_formula_exact
#print axioms field_order_and_budget_exact
#print axioms threshold_chain_exact
#print axioms chart_constants_are_threshold_derived
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

end KBPencilCensusRouteCut.CensusRouteCut
