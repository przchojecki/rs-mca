import LInteriorPayS1.CriticalGap

/-!
# Existential selected-support formulation of the critical low-Hahn gap

A Reed--Solomon list may admit more than one choice of one exact-size agreement
support per codeword. The sharp fixed-dual interface only constrains hypothetical
lists larger than the integer target and asks for one paying selection per such
list. This module states that interface and its direct falsifier as stdlib Lean
`Prop`s. It does not assert the conjecture.
-/

namespace LInteriorPayS1

universe u

/-- The objective mass needed to force the rational dual objective strictly
below `BStar = targetListBound + 1`. -/
def integerCriticalGap : Rat := lpObjective - qNat BStar

/-- Sharp open `G₃` boundary for the integer target: `G₃` strictly above this
value makes the degree-three-only objective strictly smaller than `BStar`. -/
def h3IntegerOpenThreshold : Rat :=
  Rat.normalize
    81858218311343544899896663534139630625
    389001796223311531724035804630343856388

/-- Every hypothetical oversized adjacent list admits at least one valid
selected-support realization whose inherited degree-three Hahn objective is
strictly smaller than that list's own cardinality. Combined with the frozen
dual inequality, this is a direct contradiction. -/
def RSHahn123SelectionGap
    (ListObject : Type u)
    (isAdjacentList : ListObject → Prop)
    (listSize : ListObject → Nat)
    (selects : ListObject → SelectedSupportHahnData → Prop) : Prop :=
  ∀ list, isAdjacentList list → targetListBound < listSize list →
    ∃ data, selects list data ∧ data.listSize = listSize list ∧
      lpObjective - weightedLowHahnEnergy data < qNat (listSize list)

/-- Direct falsifier: one genuine oversized adjacent list with at least one
valid selected-support realization, but every size-correct valid realization
leaves the inherited objective at or above the list's own cardinality. -/
def RSHahn123SelectionGapFalsifier
    (ListObject : Type u)
    (isAdjacentList : ListObject → Prop)
    (listSize : ListObject → Nat)
    (selects : ListObject → SelectedSupportHahnData → Prop)
    (list : ListObject) : Prop :=
  isAdjacentList list ∧ targetListBound < listSize list ∧
    (∃ data, selects list data ∧ data.listSize = listSize list) ∧
    ∀ data, selects list data → data.listSize = listSize list →
      qNat (listSize list) ≤ lpObjective - weightedLowHahnEnergy data

/-- Stronger one-mode proxy on selected-support data. Standard nonnegativity of
`G₁,G₂` turns a strict `G₃` gap into the strict integer objective gap. -/
def RSH3IntegerOpenGap
    (arises : SelectedSupportHahnData → Prop) : Prop :=
  ∀ data, arises data → h3IntegerOpenThreshold < data.g3

/-! ## Exact open-threshold arithmetic -/

theorem integer_critical_gap_exact :
    integerCriticalGap =
      Rat.normalize
        4592053304955603301034903445
        1159431963847722545269 := by
  native_decide

theorem exact_h3_integer_boundary_objective :
    lpObjective - c3 * h3IntegerOpenThreshold = qNat BStar := by
  native_decide

theorem integer_open_threshold_below_closed :
    h3IntegerOpenThreshold < h3CriticalThreshold := by
  native_decide

theorem integer_open_threshold_below_quarter :
    h3IntegerOpenThreshold < Rat.normalize 1 4 := by
  native_decide

/-- Scope-preserving extraction of the paying selected-support data. -/
theorem selection_gap_supplies_paying_data
    (ListObject : Type u)
    (isAdjacentList : ListObject → Prop)
    (listSize : ListObject → Nat)
    (selects : ListObject → SelectedSupportHahnData → Prop)
    (hgap : RSHahn123SelectionGap ListObject isAdjacentList listSize selects)
    (list : ListObject)
    (hlist : isAdjacentList list)
    (hlarge : targetListBound < listSize list) :
    ∃ data, selects list data ∧ data.listSize = listSize list ∧
      lpObjective - weightedLowHahnEnergy data < qNat (listSize list) :=
  hgap list hlist hlarge

/-- The exact logical compiler: if every valid selected realization obeys the
frozen dual inequality, the selection-gap conjecture excludes every oversized
list and yields the integer target. -/
theorem selection_gap_compiles_integer_cap
    (ListObject : Type u)
    (isAdjacentList : ListObject → Prop)
    (listSize : ListObject → Nat)
    (selects : ListObject → SelectedSupportHahnData → Prop)
    (dualBound : ∀ list data, isAdjacentList list → selects list data →
      data.listSize = listSize list →
      qNat (listSize list) ≤
        lpObjective - weightedLowHahnEnergy data)
    (hgap : RSHahn123SelectionGap ListObject isAdjacentList listSize selects) :
    ∀ list, isAdjacentList list → listSize list ≤ targetListBound := by
  intro list hlist
  by_cases hle : listSize list ≤ targetListBound
  · exact hle
  · have hlarge : targetListBound < listSize list := by omega
    obtain ⟨data, hselects, hsize, hpay⟩ := hgap list hlist hlarge
    have hdual := dualBound list data hlist hselects hsize
    change
      (lpObjective - weightedLowHahnEnergy data).blt (qNat (listSize list)) = false
      at hdual
    have htf : true = false := hpay.symm.trans hdual
    cases htf

/-- The printed falsifier is logically incompatible with the selection-gap
conjecture. -/
theorem selection_gap_falsifier_refutes
    (ListObject : Type u)
    (isAdjacentList : ListObject → Prop)
    (listSize : ListObject → Nat)
    (selects : ListObject → SelectedSupportHahnData → Prop)
    (list : ListObject)
    (hfals : RSHahn123SelectionGapFalsifier
      ListObject isAdjacentList listSize selects list) :
    ¬ RSHahn123SelectionGap ListObject isAdjacentList listSize selects := by
  intro hgap
  rcases hfals with ⟨hlist, hlarge, _hexists, hall⟩
  obtain ⟨data, hselects, hsize, hpay⟩ := hgap list hlist hlarge
  have hdual := hall data hselects hsize
  change
    (lpObjective - weightedLowHahnEnergy data).blt (qNat (listSize list)) = false
    at hdual
  have htf : true = false := hpay.symm.trans hdual
  cases htf

/-! A nonvacuous kernel-checked model of the abstract interface. It certifies
the Prop wiring and exact boundary arithmetic; it is not claimed to arise from
an adjacent Reed--Solomon list. -/

def openPayingData : SelectedSupportHahnData where
  row := .low
  listSize := BStar
  g1 := qNat 0
  g2 := qNat 0
  g3 := h3CriticalThreshold

inductive ToyAdjacentList where
  | oversized
  deriving DecidableEq, Repr

def toyIsAdjacent (_ : ToyAdjacentList) : Prop := True

def toyListSize (_ : ToyAdjacentList) : Nat := BStar

def toySelects
    (_ : ToyAdjacentList)
    (data : SelectedSupportHahnData) : Prop :=
  data = openPayingData

theorem open_paying_data_is_strictly_below_forbidden_integer :
    lpObjective - weightedLowHahnEnergy openPayingData < qNat BStar := by
  native_decide

theorem oversized_selection_gap_evidence :
    RSHahn123SelectionGap
      ToyAdjacentList toyIsAdjacent toyListSize toySelects := by
  intro list _ _
  cases list
  refine ⟨openPayingData, rfl, rfl, ?_⟩
  exact open_paying_data_is_strictly_below_forbidden_integer

#print axioms integer_critical_gap_exact
#print axioms exact_h3_integer_boundary_objective
#print axioms integer_open_threshold_below_closed
#print axioms integer_open_threshold_below_quarter
#print axioms selection_gap_supplies_paying_data
#print axioms selection_gap_compiles_integer_cap
#print axioms selection_gap_falsifier_refutes
#print axioms open_paying_data_is_strictly_below_forbidden_integer
#print axioms oversized_selection_gap_evidence

end LInteriorPayS1
