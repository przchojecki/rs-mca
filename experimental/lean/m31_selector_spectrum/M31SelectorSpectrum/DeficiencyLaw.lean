import M31SelectorSpectrum.SpectrumGenerator

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Deficiency-level form of the structural selector-spectrum law

This module lifts the block-deficiency generator to point deficiencies.  It
checks the complete frozen range `34,...,479`, including every off-lattice zero
and the explicit zero values at 96 and 160.

This is equality with the atlas-printed selector cap, not a proof that every
deployed same-remainder rooted shell satisfies that cap.  The deployed
interpretation of this spectrum is outside the scope of this package.
-/

namespace M31SelectorSpectrum.DeficiencyLaw

open M31SelectorSpectrum.SpectrumGenerator

/--
Structural selector-spectrum generator at point deficiency `e`.  Outside the
fourteen relevant T32 block deficiencies, and away from the 32-lattice, it is
zero.
-/
def deficiencySpectrumGenerator (e : Nat) : Nat :=
  let t := e / 32
  if e % 32 = 0 ∧ 1 ≤ t ∧ t ≤ 14 then
    selectorSpectrumGenerator t
  else
    0

/-- The frozen point-deficiency range `34,...,479`. -/
def contractDeficiencies : List Nat :=
  (List.range 446).map fun index => index + 34

/--
On every deficiency in the frozen contract, the structural generator is exactly
the atlas-printed `t32ResolvedShellCap`.
-/
theorem deficiency_generator_matches_atlas_cap_on_contract :
    contractDeficiencies.map deficiencySpectrumGenerator =
      contractDeficiencies.map M31SelectorSpectrum.Atlas.t32ResolvedShellCap := by
  native_decide

/-- Every off-32-lattice deficiency in the frozen range is generated as zero. -/
theorem off_lattice_contract_is_zero :
    (contractDeficiencies.filter fun e => !(e % 32 == 0)).all
      (fun e => deficiencySpectrumGenerator e == 0) = true := by
  native_decide

/-- Explicit zero predictions retained by the generator. -/
theorem explicit_zero_predictions :
    deficiencySpectrumGenerator 96 = 0 ∧
    deficiencySpectrumGenerator 160 = 0 := by
  native_decide

/-- The four exceptional positive off-64-lattice selector values. -/
theorem exceptional_point_deficiency_values :
    deficiencySpectrumGenerator 224 = 60 ∧
    deficiencySpectrumGenerator 288 = 210 ∧
    deficiencySpectrumGenerator 352 = 45 ∧
    deficiencySpectrumGenerator 416 = 3 := by
  native_decide

#print axioms deficiency_generator_matches_atlas_cap_on_contract
#print axioms off_lattice_contract_is_zero
#print axioms explicit_zero_predictions
#print axioms exceptional_point_deficiency_values

end M31SelectorSpectrum.DeficiencyLaw
