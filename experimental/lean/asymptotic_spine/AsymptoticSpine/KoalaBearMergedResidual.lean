import AsymptoticSpine.C8ChartExhaustion

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# KoalaBear merged residual: rank-49-or-pencil conjecture

This stdlib-only module freezes a conjectural slope-level atlas for the
KoalaBear MCA residual after the tangent and boundary-prefix Q first-match
cells have been deleted.  The conjecture is a `Prop` definition, not a theorem.
No proof, axiom, or `sorry` is supplied for it.

The theorem `rank49OrPencil_implies_uniform` is only a compiler: it proves that
an atlas satisfying the stated slope-level charges implies the advertised
uniform residual bound.  The concrete arithmetic and a small finite evidence
instance are kernel-checked below.
-/

namespace AsymptoticSpine.KoalaBearMergedResidual

/-! ## Frozen row, architecture, and ledger constants -/

def architecture : String :=
  "GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1"

def partitionDigest : String :=
  "4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc"

def ownerOrder : List String :=
  ["SOURCE_COORDINATE_TANGENT_IMAGE",
   "ACTIVE_V4_BOUNDARY_PREFIX_Q",
   "ACTIVE_V4_BALANCED_CORE",
   "UNPAID_V4_COMPLEMENT"]

def fieldPrime : Nat := 2_130_706_433
def extensionDegree : Nat := 6
def fieldOrder : Nat := fieldPrime ^ extensionDegree

def codeLength : Nat := 2_097_152
def codeDimension : Nat := 1_048_576
def agreement : Nat := 1_116_048
def redundancy : Nat := codeLength - codeDimension
def errorRadius : Nat := codeLength - agreement
def supportExcess : Nat := agreement - codeDimension

def targetDenominator : Nat := 2 ^ 128
def budget : Nat := 274_980_728_111_395_087

def paidTangentAtom : Nat := 981_104
def tangentRootedQShellCap : Nat := 400_389_155_870
def congestionQCap : Nat := 442_607_801_512
def provedQFloor : Nat := 57_198_030_365

def closureThreshold : Nat := 137_490_163_860_629_056

def properDimensionCap : Nat := 49
def properRank49Cap : Nat := 77_251_422_090_159_989
def properRank50Cap : Nat := 148_068_539_552_473_273

def normalizedPencilChartCap : Nat := 30_119_370_885_234_533
def scalarExceptionCap : Nat := 1
def onePencilSlopeCap : Nat := 2

def mergedResidualCap : Nat :=
  properRank49Cap + scalarExceptionCap +
    onePencilSlopeCap * normalizedPencilChartCap

/-! ## The frozen set-theoretic residual -/

/-- List presentation of finite set difference.  All cardinality claims below
also carry `Nodup`, so the lists represent sets of distinct finite slopes. -/
def listDifference {α : Type} [DecidableEq α]
    (xs ys : List α) : List α :=
  xs.filter fun x => !(ys.contains x)

/-- The exact merged residual
`R₂(r) = (Z(r) \ T(r)) \ Z_Q(r)` in the frozen owner chronology. -/
def mergedResidual
    {Line Slope : Type} [DecidableEq Slope]
    (badSlopes tangentSlopes qSlopes : Line → List Slope)
    (line : Line) : List Slope :=
  listDifference
    (listDifference (badSlopes line) (tangentSlopes line))
    (qSlopes line)

/-! ## Exact source-formula arithmetic -/

/-- Falling factorial `n * (n - 1) * ... * (n - k + 1)`.  This form avoids
computing two enormous binomial coefficients whose factorial factors cancel. -/
def fallingFactorial : Nat → Nat → Nat
  | _, 0 => 1
  | n, k + 1 => (n - k) * fallingFactorial n k

/-- The exact proper-intersection compiler specialized to slope degree `31` and
correction-space dimension `s`:

`floor (31 * (s + 1) * choose n (s + 1) / choose agreement (s + 1))`.

The equivalent falling-factorial ratio is used for finite evaluation. -/
def properCorrectionBound (s : Nat) : Nat :=
  31 * (s + 1) * fallingFactorial codeLength (s + 1) /
    fallingFactorial agreement (s + 1)

/-! ## Slope-level atlas contract -/

/-- A normalized residual atlas in the unit of distinct finite slopes.

`exactFirstMatch` gives equality of the residual slope set with the union of the
three charged classes.  The four disjointness fields make this a first-match
partition rather than a cover with multiplicity.  `coalescedCharge` is the
explicit support-to-slope coalescing obligation after that partition: the
residual cardinality is charged once to the proper block, the exceptional
block, or one normalized pencil key.  It is deliberately not a support census.
-/
structure ResidualSlopeAtlas (Slope Chart : Type)
    [DecidableEq Slope] [DecidableEq Chart] where
  residualSlopes : List Slope
  residualSlopes_nodup : residualSlopes.Nodup
  properDimension : Nat
  properSlopes : List Slope
  properSlopes_nodup : properSlopes.Nodup
  exceptionalSlopes : List Slope
  exceptionalSlopes_nodup : exceptionalSlopes.Nodup
  pencilCharts : List Chart
  pencilCharts_nodup : pencilCharts.Nodup
  pencilSlopes : Chart → List Slope
  pencilSlopes_nodup :
    ∀ chart ∈ pencilCharts, (pencilSlopes chart).Nodup
  exactFirstMatch :
    ∀ gamma,
      gamma ∈ residualSlopes ↔
        gamma ∈ properSlopes ∨
        gamma ∈ exceptionalSlopes ∨
        ∃ chart, chart ∈ pencilCharts ∧ gamma ∈ pencilSlopes chart
  proper_exception_disjoint :
    ∀ gamma ∈ properSlopes, gamma ∉ exceptionalSlopes
  proper_pencil_disjoint :
    ∀ gamma ∈ properSlopes, ∀ chart ∈ pencilCharts,
      gamma ∉ pencilSlopes chart
  exception_pencil_disjoint :
    ∀ gamma ∈ exceptionalSlopes, ∀ chart ∈ pencilCharts,
      gamma ∉ pencilSlopes chart
  pencil_pairwise_disjoint :
    ∀ first ∈ pencilCharts, ∀ second ∈ pencilCharts,
      first ≠ second →
      ∀ gamma, gamma ∈ pencilSlopes first →
        gamma ∉ pencilSlopes second
  proper_dimension_le : properDimension ≤ properDimensionCap
  proper_count_le : properSlopes.length ≤ properRank49Cap
  exceptional_count_le : exceptionalSlopes.length ≤ scalarExceptionCap
  pencil_chart_count_le : pencilCharts.length ≤ normalizedPencilChartCap
  pencil_slope_count_le :
    ∀ chart ∈ pencilCharts,
      (pencilSlopes chart).length ≤ onePencilSlopeCap
  coalescedCharge :
    residualSlopes.length ≤
      properSlopes.length + exceptionalSlopes.length +
        onePencilSlopeCap * pencilCharts.length

namespace ResidualSlopeAtlas

/-- The numerical compiler from the structured atlas to the merged residual
cap.  This theorem proves no atlas exists; it only consumes one. -/
theorem residual_length_le
    {Slope Chart : Type} [DecidableEq Slope] [DecidableEq Chart]
    (atlas : ResidualSlopeAtlas Slope Chart) :
    atlas.residualSlopes.length ≤ mergedResidualCap := by
  unfold mergedResidualCap
  calc
    atlas.residualSlopes.length ≤
        atlas.properSlopes.length + atlas.exceptionalSlopes.length +
          onePencilSlopeCap * atlas.pencilCharts.length :=
      atlas.coalescedCharge
    _ ≤ properRank49Cap + scalarExceptionCap +
          onePencilSlopeCap * normalizedPencilChartCap :=
      Nat.add_le_add
        (Nat.add_le_add atlas.proper_count_le atlas.exceptional_count_le)
        (Nat.mul_le_mul_left onePencilSlopeCap atlas.pencil_chart_count_le)

end ResidualSlopeAtlas

/-- The precise rank-49-or-pencil conjecture.

For every admissible received line, the exact duplicate-free residual list
`(Z \ T) \ Z_Q` admits:

* one proper correction-space slope image of explicit dimension at most `49`;
* at most one scalar-degenerate exceptional slope; and
* normalized one-parameter pencil keys, each certified semantically.

The semantic predicates are parameters because this module freezes the exact
logical contract without pretending to construct the Reed--Solomon objects. -/
def rank49OrPencilLaw
    (Line Slope Chart : Type)
    [DecidableEq Slope] [DecidableEq Chart]
    (admissible : Line → Prop)
    (badSlopes tangentSlopes qSlopes : Line → List Slope)
    (isProperCorrectionBlock : Line → Nat → List Slope → Prop)
    (isScalarDegenerateException : Line → List Slope → Prop)
    (isPrimitiveOneParameterPencil :
      Line → Chart → List Slope → Prop) : Prop :=
  ∀ line, admissible line →
    ∃ atlas : ResidualSlopeAtlas Slope Chart,
      atlas.residualSlopes =
        mergedResidual badSlopes tangentSlopes qSlopes line ∧
      isProperCorrectionBlock line atlas.properDimension
        atlas.properSlopes ∧
      isScalarDegenerateException line atlas.exceptionalSlopes ∧
      (∀ chart ∈ atlas.pencilCharts,
        isPrimitiveOneParameterPencil line chart
          (atlas.pencilSlopes chart))

/-- Uniform merged residual law, written as the universal quantifier equivalent
to `max_r |R₂(r)| ≤ mergedResidualCap`.  `Nodup` fixes the unit as distinct
finite slopes rather than supports or explanation states. -/
def uniformMergedResidualLaw
    (Line Slope : Type) [DecidableEq Slope]
    (admissible : Line → Prop)
    (badSlopes tangentSlopes qSlopes : Line → List Slope) : Prop :=
  ∀ line, admissible line →
    (mergedResidual badSlopes tangentSlopes qSlopes line).Nodup ∧
      (mergedResidual badSlopes tangentSlopes qSlopes line).length ≤
        mergedResidualCap

/-- A proved logical compiler: the conjectural structured law implies the
uniform cardinal law.  No Reed--Solomon atlas is constructed here. -/
theorem rank49OrPencil_implies_uniform
    (Line Slope Chart : Type)
    [DecidableEq Slope] [DecidableEq Chart]
    (admissible : Line → Prop)
    (badSlopes tangentSlopes qSlopes : Line → List Slope)
    (isProperCorrectionBlock : Line → Nat → List Slope → Prop)
    (isScalarDegenerateException : Line → List Slope → Prop)
    (isPrimitiveOneParameterPencil :
      Line → Chart → List Slope → Prop)
    (hLaw : rank49OrPencilLaw Line Slope Chart admissible
      badSlopes tangentSlopes qSlopes
      isProperCorrectionBlock isScalarDegenerateException
      isPrimitiveOneParameterPencil) :
    uniformMergedResidualLaw Line Slope admissible
      badSlopes tangentSlopes qSlopes := by
  intro line hline
  rcases hLaw line hline with ⟨atlas, hresidual, _, _, _⟩
  constructor
  · rw [← hresidual]
    exact atlas.residualSlopes_nodup
  · rw [← hresidual]
    exact atlas.residual_length_le

/-! ## Kernel-checked row and reserve evidence -/

theorem frozen_identifiers_exact :
    architecture =
      "GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1" ∧
    partitionDigest =
      "4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc" ∧
    ownerOrder =
      ["SOURCE_COORDINATE_TANGENT_IMAGE",
       "ACTIVE_V4_BOUNDARY_PREFIX_Q",
       "ACTIVE_V4_BALANCED_CORE",
       "UNPAID_V4_COMPLEMENT"] := by
  decide

theorem row_constants_exact :
    fieldPrime = 2_130_706_433 ∧
    extensionDegree = 6 ∧
    codeLength = 2_097_152 ∧
    codeDimension = 1_048_576 ∧
    agreement = 1_116_048 ∧
    redundancy = 1_048_576 ∧
    errorRadius = 981_104 ∧
    supportExcess = 67_472 := by
  native_decide

theorem field_order_and_budget_exact :
    fieldOrder =
      93_571_093_019_388_561_295_270_373_781_649_880_353_786_165_192_103_559_169 ∧
    fieldOrder / targetDenominator = budget := by
  native_decide

theorem proper_rank49_formula_exact :
    properCorrectionBound 49 = properRank49Cap := by
  native_decide

theorem proper_rank50_nearest_threat_exact :
    properCorrectionBound 50 = properRank50Cap ∧
    closureThreshold < properRank50Cap ∧
    properRank50Cap - closureThreshold = 10_578_375_691_844_217 := by
  native_decide

theorem one_pencil_incidence_exact :
    2 * errorRadius ≤ codeLength ∧
    codeLength < 3 * errorRadius := by
  native_decide

theorem merged_residual_decomposition_exact :
    mergedResidualCap = closureThreshold ∧
    properRank49Cap +
      onePencilSlopeCap * normalizedPencilChartCap +
      scalarExceptionCap = closureThreshold ∧
    closureThreshold - properRank49Cap = 60_238_741_770_469_067 := by
  native_decide

theorem tangent_rooted_shell_closure_is_sharp :
    paidTangentAtom + tangentRootedQShellCap +
        2 * mergedResidualCap = budget - 1 ∧
    paidTangentAtom + tangentRootedQShellCap +
        2 * (mergedResidualCap + 1) = budget + 1 := by
  native_decide

theorem congestion_cap_does_not_close_this_bound :
    (budget - paidTangentAtom - congestionQCap) / 2 =
      137_490_142_751_306_235 ∧
    137_490_142_751_306_235 < mergedResidualCap ∧
    mergedResidualCap - 137_490_142_751_306_235 = 21_109_322_821 := by
  native_decide

theorem q_floor_consistency :
    provedQFloor ≤ tangentRootedQShellCap ∧
    provedQFloor ≤ congestionQCap := by
  native_decide

/-! ## Exact theorem-pool constants used only as evidence -/

def fixedUnionNuTwoCap : Nat := 2_847_909_263_951
def rankRegularNu4982Cap : Nat := 94_008
def completeCorrectionRayCap : Nat := 1_963_173
def pavingPaidNullity : Nat := 9
def cloneResidualSupportExcess : Nat := 8_564
def cloneResidualOutsideMismatch : Nat := 9_812

theorem theorem_pool_fits_rank49_scale :
    fixedUnionNuTwoCap < properRank49Cap ∧
    rankRegularNu4982Cap < properRank49Cap ∧
    completeCorrectionRayCap < properRank49Cap ∧
    pavingPaidNullity < properDimensionCap ∧
    cloneResidualSupportExcess < supportExcess ∧
    cloneResidualOutsideMismatch < errorRadius := by
  native_decide

/-! ## Small finite evidence instance -/

inductive ToyLine where
  | only
  deriving DecidableEq

inductive ToyChart where
  | pencil
  deriving DecidableEq

def toyBadSlopes : ToyLine → List Nat
  | .only => [3, 5, 7, 11, 13]

def toyTangentSlopes : ToyLine → List Nat
  | .only => [3]

def toyQSlopes : ToyLine → List Nat
  | .only => [5]

def toyProper (_ : ToyLine) (dimension : Nat) (slopes : List Nat) : Prop :=
  dimension = 1 ∧ slopes = [7]

def toyException (_ : ToyLine) (slopes : List Nat) : Prop :=
  slopes = []

def toyPencil (_ : ToyLine) (_ : ToyChart) (slopes : List Nat) : Prop :=
  slopes = [11, 13]

def toyAtlas : ResidualSlopeAtlas Nat ToyChart where
  residualSlopes := [7, 11, 13]
  residualSlopes_nodup := by decide
  properDimension := 1
  properSlopes := [7]
  properSlopes_nodup := by decide
  exceptionalSlopes := []
  exceptionalSlopes_nodup := by decide
  pencilCharts := [.pencil]
  pencilCharts_nodup := by decide
  pencilSlopes := fun _ => [11, 13]
  pencilSlopes_nodup := by
    intro chart _
    cases chart
    decide
  exactFirstMatch := by
    intro gamma
    constructor
    · intro h
      simp only [List.mem_cons, List.mem_singleton] at h
      rcases h with h7 | h11 | h13
      · exact Or.inl (by simpa using h7)
      · exact Or.inr (Or.inr ⟨.pencil, by simp, by
          simp only [List.mem_cons, List.mem_singleton]
          exact Or.inl h11⟩)
      · exact Or.inr (Or.inr ⟨.pencil, by simp, by
          simp only [List.mem_cons, List.mem_singleton]
          exact Or.inr h13⟩)
    · intro h
      rcases h with hproper | hexception | ⟨chart, _, hpencil⟩
      · simp only [List.mem_singleton] at hproper
        simp only [List.mem_cons, List.mem_singleton]
        exact Or.inl hproper
      · simp at hexception
      · cases chart
        simp only [List.mem_cons, List.mem_singleton] at hpencil ⊢
        exact Or.inr hpencil
  proper_exception_disjoint := by simp
  proper_pencil_disjoint := by simp
  exception_pencil_disjoint := by simp
  pencil_pairwise_disjoint := by simp
  proper_dimension_le := by decide
  proper_count_le := by decide
  exceptional_count_le := by decide
  pencil_chart_count_le := by decide
  pencil_slope_count_le := by
    intro chart _
    cases chart
    decide
  coalescedCharge := by decide

theorem toy_merged_residual_exact :
    mergedResidual toyBadSlopes toyTangentSlopes toyQSlopes .only =
      [7, 11, 13] := by
  decide

theorem toy_rank49_or_pencil_evidence :
    rank49OrPencilLaw ToyLine Nat ToyChart
      (fun _ => True) toyBadSlopes toyTangentSlopes toyQSlopes
      toyProper toyException toyPencil := by
  intro line _
  cases line
  refine ⟨toyAtlas, toy_merged_residual_exact, ?_, rfl, ?_⟩
  · exact ⟨rfl, rfl⟩
  · intro chart _
    cases chart
    rfl

theorem toy_uniform_evidence :
    uniformMergedResidualLaw ToyLine Nat (fun _ => True)
      toyBadSlopes toyTangentSlopes toyQSlopes :=
  rank49OrPencil_implies_uniform ToyLine Nat ToyChart
    (fun _ => True) toyBadSlopes toyTangentSlopes toyQSlopes
    toyProper toyException toyPencil toy_rank49_or_pencil_evidence

#print axioms ResidualSlopeAtlas.residual_length_le
#print axioms rank49OrPencil_implies_uniform
#print axioms frozen_identifiers_exact
#print axioms row_constants_exact
#print axioms field_order_and_budget_exact
#print axioms proper_rank49_formula_exact
#print axioms proper_rank50_nearest_threat_exact
#print axioms one_pencil_incidence_exact
#print axioms merged_residual_decomposition_exact
#print axioms tangent_rooted_shell_closure_is_sharp
#print axioms congestion_cap_does_not_close_this_bound
#print axioms q_floor_consistency
#print axioms theorem_pool_fits_rank49_scale
#print axioms toy_merged_residual_exact
#print axioms toy_rank49_or_pencil_evidence
#print axioms toy_uniform_evidence

end AsymptoticSpine.KoalaBearMergedResidual
