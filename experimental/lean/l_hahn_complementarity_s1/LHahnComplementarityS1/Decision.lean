import LHahnComplementarityS1.Complementarity

set_option maxRecDepth 1000000

/-!
# The selected-support hypothesis is target-equivalent

This module carries the packet's logical result, paper Theorem 4.1 and Claim B.

The mathematical input is the paper's Theorem 3.1: for every valid exact-size
selected-support realization, `H - E_Hahn = L + S_shell` with `S_shell >= 0`,
hence the dual objective is at least the list size.  That floor enters here as
the `dualFloor` field of `DualModel`, exactly as the round's own suggestion
proposed; it is not re-derived in Lean, because the Johnson scheme, the Hahn
functions and the cubic factorization are not formalized here.

Given that floor, the predecessor's named hypothesis
`RS_HAHN123_SELECTION_GAP` is proved equivalent to the desired adjacent-row cap,
and any oversized list is proved to supply the universal-selection falsifier on
its own.  Both facts are kernel-checked below, with no `decide` or
`native_decide` used in this module.
-/

namespace LHahnComplementarityS1

universe u

/--
The interface supplied by the adjacent Hahn dual.  `objective s` is
`H - (c1 G_1 + c2 G_2 + c3 G_3)` evaluated at the selection `s`, and `dualFloor`
is the consequence of the complementarity identity together with
`S_shell >= 0`.
-/
structure DualModel where
  ListObj : Type u
  card : ListObj → Nat
  Selection : ListObj → Type u
  objective : {x : ListObj} → Selection x → Rat
  dualFloor : ∀ (x : ListObj) (s : Selection x), (card x : Rat) ≤ objective s

/-- The desired adjacent-row safety statement, `L <= 16777214`. -/
def Safe (M : DualModel) : Prop :=
  ∀ x : M.ListObj, M.card x ≤ ell

/-- The predecessor's named hypothesis, with exactly its original meaning. -/
def SelectionGap (M : DualModel) : Prop :=
  ∀ x : M.ListObj, Bstar ≤ M.card x →
    ∃ s : M.Selection x, M.objective s < (M.card x : Rat)

/-- An adjacent list at or above the first forbidden cardinality. -/
def Unsafe (M : DualModel) : Prop :=
  ∃ x : M.ListObj, Bstar ≤ M.card x

/-- The predecessor's originally printed universal-selection falsifier. -/
def SelectionGapFalsifier (M : DualModel) : Prop :=
  ∃ x : M.ListObj,
    Bstar ≤ M.card x ∧ ∀ s : M.Selection x, (M.card x : Rat) ≤ M.objective s

/--
Paper Theorem 4.1 and Claim B.  Under the dual floor the named
selected-support hypothesis is logically equivalent to the adjacent-row cap, so
it is not a weaker bridge that could be discharged independently.
-/
theorem selection_gap_iff_safe (M : DualModel) :
    SelectionGap M ↔ Safe M := by
  constructor
  · intro hGap x
    rcases Nat.lt_or_ge ell (M.card x) with hgt | hle
    · exfalso
      have hgt' : 16777214 < M.card x := hgt
      have hLarge : Bstar ≤ M.card x := by
        show 16777215 ≤ M.card x
        omega
      obtain ⟨s, hs⟩ := hGap x hLarge
      exact absurd (M.dualFloor x s) (Rat.not_le.mpr hs)
    · exact hle
  · intro hSafe x hLarge
    exfalso
    have hcap : M.card x ≤ 16777214 := hSafe x
    have hL : 16777215 ≤ M.card x := hLarge
    omega

#print axioms LHahnComplementarityS1.selection_gap_iff_safe

/--
One oversized list is already a complete falsifier: the dual floor holds for
every selection from it, so no separate certification over all of its support
selections is needed.
-/
theorem unsafe_iff_falsifier (M : DualModel) :
    Unsafe M ↔ SelectionGapFalsifier M := by
  constructor
  · intro h
    obtain ⟨x, hx⟩ := h
    exact ⟨x, hx, M.dualFloor x⟩
  · intro h
    obtain ⟨x, hx, _⟩ := h
    exact ⟨x, hx⟩

#print axioms LHahnComplementarityS1.unsafe_iff_falsifier

/--
The negation form actually used in the paper's route kill: under the dual floor
no oversized list can exhibit the requested strict inequality, for any selection.
-/
theorem no_selection_beats_the_floor (M : DualModel)
    (x : M.ListObj) (s : M.Selection x) :
    ¬ (M.objective s < (M.card x : Rat)) := by
  intro hs
  exact absurd (M.dualFloor x s) (Rat.not_le.mpr hs)

#print axioms LHahnComplementarityS1.no_selection_beats_the_floor

end LHahnComplementarityS1
