import M31FlatnessKeystone
import M31QuotientBandMixing
import M31QuotientT16MixingFloor
import M31SelectorSpectrum

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 flatness conjecture A1, session two: tension certificates

This module is a stdlib-only adversarial ledger audit of the pinned Mersenne-31
quotient-prefix conjecture.  The new computational statement closes the eight
integrated `T_16`-mixed neighbors under every same-canonical-`T_32` selector
continuation, with direct locator-prefix multiplication as the verification
layer.  It also constructs the reflected deficiency-256 packet and separates
the band conjecture from the out-of-band compiler premise.
-/

namespace M31FlatnessConjectureA1S2

open M31QuotientT16MixingFloor
open M31QuotientBandMixing

abbrev Support := List Nat

def fieldPrime : Nat := 2 ^ 31 - 1
def supportSize : Nat := 479
def prefixDepth : Nat := 32
def bandLower : Nat := 33
def bandUpper : Nat := 213
def championCap : Nat := 1233
def budget : Nat := 16777215
def admissibleShellCount : Nat := 447
def ambientContribution : Nat := 14456476

def sameSet [BEq α] (xs ys : List α) : Bool :=
  xs.all ys.contains && ys.all xs.contains

def certifiedAt (e : Nat) (support : Support) : Bool :=
  Witness.supportValid support &&
  (Witness.locatorPrefix prefixDepth support == Witness.eta) &&
  (Witness.deficiency Witness.anchor support == e) &&
  !(support == Witness.anchor)

def fullBlockClasses
    (classes : List Nat) (blockReps : Nat → List Nat)
    (support : Support) : List Nat :=
  classes.filter fun a => (blockReps a).all support.contains

def blockRemainder
    (classes : List Nat) (blockReps : Nat → List Nat)
    (support : Support) : Support :=
  let fullReps := (fullBlockClasses classes blockReps support).flatMap blockReps
  support.filter fun r => !(fullReps.contains r)

def availableBlockClasses
    (classes : List Nat) (blockReps : Nat → List Nat)
    (support : Support) : List Nat :=
  let remainder := blockRemainder classes blockReps support
  classes.filter fun a =>
    (blockReps a).all (fun r => !(remainder.contains r))

def completionSelectorSize
    (classes : List Nat) (blockReps : Nat → List Nat) (blockSize : Nat)
    (support : Support) : Nat :=
  (supportSize - (blockRemainder classes blockReps support).length) / blockSize

def completionCandidates
    (classes : List Nat) (blockReps : Nat → List Nat) (blockSize : Nat)
    (support : Support) : List Support :=
  let remainder := blockRemainder classes blockReps support
  let available := availableBlockClasses classes blockReps support
  let selectorSize := completionSelectorSize classes blockReps blockSize support
  (Witness.choose selectorSize available).map fun selected =>
    Witness.canonicalSupport (remainder ++ selected.flatMap blockReps)

def certifiedCompletionClosure
    (classes : List Nat) (blockReps : Nat → List Nat) (blockSize e : Nat)
    (support : Support) : List Support :=
  (completionCandidates classes blockReps blockSize support).filter
    (certifiedAt e)

def intactT64Classes : List Nat :=
  Witness.oddT64Classes.filter fun a => !(a == 1) && !(a == 3)

def intactT32Classes : List Nat :=
  Witness.oddT32Classes.filter fun a => !(a == 1) && !(a == 3)

def t64Remainder (support : Support) : Support :=
  blockRemainder intactT64Classes Witness.t64BlockReps support

def t32Remainder (support : Support) : Support :=
  blockRemainder intactT32Classes Witness.t32BlockReps support

def t64AvailableClasses (support : Support) : List Nat :=
  availableBlockClasses intactT64Classes Witness.t64BlockReps support

def t32AvailableClasses (support : Support) : List Nat :=
  availableBlockClasses intactT32Classes Witness.t32BlockReps support

def t64SelectorSize (support : Support) : Nat :=
  completionSelectorSize intactT64Classes Witness.t64BlockReps 64 support

def t32SelectorSize (support : Support) : Nat :=
  completionSelectorSize intactT32Classes Witness.t32BlockReps 32 support

def t64ClosureAt (e : Nat) (support : Support) : List Support :=
  certifiedCompletionClosure
    intactT64Classes Witness.t64BlockReps 64 e support

def t32ClosureAt (e : Nat) (support : Support) : List Support :=
  certifiedCompletionClosure
    intactT32Classes Witness.t32BlockReps 32 e support

def mixedAt (index : Nat) : Support :=
  Witness.mixedNeighbors.getD index []

def mixedRemainderRepresentatives : List Support :=
  [mixedAt 0, mixedAt 3, mixedAt 4, mixedAt 5]

def appendUniqueSupport (supports : List Support) (support : Support) : List Support :=
  if supports.contains support then supports else supports ++ [support]

def uniqueSupports (supports : List Support) : List Support :=
  supports.foldl appendUniqueSupport []

def closedMixedE192 : List Support :=
  uniqueSupports
    (mixedRemainderRepresentatives.flatMap (t32ClosureAt 192))

def reflectedMixedE256 : List Support :=
  uniqueSupports
    (mixedRemainderRepresentatives.flatMap (t32ClosureAt 256))

def t64SwapSpecs4 : List (List Nat × List Nat) :=
  (Witness.choose 4 Witness.insideT64).flatMap fun removed =>
    (Witness.choose 4 Witness.outsideT64).map fun added => (removed, added)

def t64SwapNeighbors4 : List Support :=
  t64SwapSpecs4.map Witness.classSwapSupport

def reflectedE256Neighbors : List Support :=
  t64SwapNeighbors4 ++ reflectedMixedE256

theorem integrated_floor_matches_cap :
    Witness.classSwapNeighbors.length = 1225 ∧
    Witness.mixedNeighbors.length = 8 ∧
    Witness.allNeighbors.length = championCap ∧
    Witness.noDuplicates Witness.allNeighbors = true ∧
    Witness.allNeighbors.all (certifiedAt 192) = true := by
  native_decide

theorem mixed_remainder_geometry_exact :
    (mixedRemainderRepresentatives.map fun support =>
      (t64Remainder support).length) = [351, 415, 415, 351] ∧
    (mixedRemainderRepresentatives.map fun support =>
      (t64AvailableClasses support).length) = [4, 2, 2, 4] ∧
    (mixedRemainderRepresentatives.map t64SelectorSize) = [2, 1, 1, 2] ∧
    (mixedRemainderRepresentatives.map fun support =>
      (t32Remainder support).length) = [351, 415, 415, 351] ∧
    (mixedRemainderRepresentatives.map fun support =>
      (t32AvailableClasses support).length) = [9, 5, 5, 9] ∧
    (mixedRemainderRepresentatives.map t32SelectorSize) = [4, 2, 2, 4] := by
  native_decide

theorem mixed_t64_t32_closure_exact :
    (mixedRemainderRepresentatives.map fun support =>
      (t64ClosureAt 192 support).length) = [3, 1, 1, 3] ∧
    (mixedRemainderRepresentatives.map fun support =>
      (t32ClosureAt 192 support).length) = [3, 1, 1, 3] ∧
    mixedRemainderRepresentatives.all (fun support =>
      sameSet (t64ClosureAt 192 support) (t32ClosureAt 192 support)) = true ∧
    closedMixedE192.length = 8 ∧
    Witness.noDuplicates closedMixedE192 = true ∧
    sameSet closedMixedE192 Witness.mixedNeighbors = true ∧
    closedMixedE192.all (certifiedAt 192) = true := by
  native_decide

theorem reflected_e256_mixed_packet_exact :
    (mixedRemainderRepresentatives.map fun support =>
      (t64ClosureAt 256 support).length) = [3, 1, 1, 3] ∧
    (mixedRemainderRepresentatives.map fun support =>
      (t32ClosureAt 256 support).length) = [3, 1, 1, 3] ∧
    mixedRemainderRepresentatives.all (fun support =>
      sameSet (t64ClosureAt 256 support) (t32ClosureAt 256 support)) = true ∧
    reflectedMixedE256.length = 8 ∧
    Witness.noDuplicates reflectedMixedE256 = true ∧
    reflectedMixedE256.all (certifiedAt 256) = true ∧
    reflectedMixedE256.all (fun support =>
      !(t64SwapNeighbors4.contains support)) = true := by
  native_decide

theorem reflected_e256_full_packet_exact :
    t64SwapSpecs4.length = 1225 ∧
    t64SwapNeighbors4.length = 1225 ∧
    Witness.noDuplicates t64SwapNeighbors4 = true ∧
    t64SwapNeighbors4.all (certifiedAt 256) = true ∧
    reflectedE256Neighbors.length = 1233 ∧
    Witness.noDuplicates reflectedE256Neighbors = true ∧
    reflectedE256Neighbors.all (certifiedAt 256) = true := by
  native_decide

theorem selector_zero_and_deployed_e96_coexist :
    M31SelectorSpectrum.DeficiencyLaw.deficiencySpectrumGenerator 96 = 0 ∧
    Witnesses.deficiency Witnesses.mixingAnchor Witnesses.mixingNeighbor = 96 ∧
    Witnesses.locatorPrefix 47 Witnesses.mixingAnchor =
      Witnesses.locatorPrefix 47 Witnesses.mixingNeighbor ∧
    Witnesses.locatorPrefix 48 Witnesses.mixingAnchor ≠
      Witnesses.locatorPrefix 48 Witnesses.mixingNeighbor := by
  rcases M31SelectorSpectrum.DeficiencyLaw.explicit_zero_predictions with
    ⟨h96, _⟩
  rcases Witnesses.mixing_supports_exact with
    ⟨_, _, _, _, hDeficiency⟩
  rcases Witnesses.mixing_prefix_exact with ⟨h47, h48⟩
  exact ⟨h96, hDeficiency, h47, h48⟩

theorem selector_atlas_scope_arithmetic :
    M31FlatnessKeystone.SelectorAtlas.atlasSummary.selectorFiberMaximum = 3432 ∧
    M31FlatnessKeystone.SelectorAtlas.atlasSummary.collisionFiberMaximum = 482 ∧
    482 < championCap ∧
    1225 < championCap ∧
    championCap < 3432 ∧
    max 1225 10 = 1225 := by
  have hAtlas := M31FlatnessKeystone.packet_selector_atlas
  constructor
  · have h := congrArg
      (fun summary : M31FlatnessKeystone.SelectorAtlas.AtlasSummary =>
        summary.selectorFiberMaximum) hAtlas
    simpa [M31FlatnessKeystone.SelectorAtlas.expectedAtlasSummary] using h
  · constructor
    · have h := congrArg
        (fun summary : M31FlatnessKeystone.SelectorAtlas.AtlasSummary =>
          summary.collisionFiberMaximum) hAtlas
      simpa [M31FlatnessKeystone.SelectorAtlas.expectedAtlasSummary] using h
    · decide

structure TypedExternalLedger where
  pinnedBandShell : Nat
  comparisonDomainFiber : Nat
  abstractMomentMaximum : Nat
  momentOrder : Nat
  deriving Repr, DecidableEq

def typedExternalLedger : TypedExternalLedger :=
  { pinnedBandShell := championCap
  , comparisonDomainFiber := 145422675
  , abstractMomentMaximum := 16794161
  , momentOrder := 990 }

theorem typed_external_obstructions_coexist :
    typedExternalLedger.pinnedBandShell ≤ championCap ∧
    budget < typedExternalLedger.comparisonDomainFiber ∧
    typedExternalLedger.comparisonDomainFiber - 8 * budget = 11204955 ∧
    budget < typedExternalLedger.abstractMomentMaximum ∧
    typedExternalLedger.abstractMomentMaximum - budget = 16946 ∧
    typedExternalLedger.momentOrder = 990 := by
  decide

def BandCap (shell : Nat → Nat) : Prop :=
  ∀ e, bandLower ≤ e → e ≤ bandUpper → shell e ≤ championCap

def outOfBandCountermodel (e : Nat) : Nat :=
  if e = 214 then 5192 else 0

theorem band_only_countermodel :
    BandCap outOfBandCountermodel ∧
    outOfBandCountermodel 214 = 5192 ∧
    championCap < outOfBandCountermodel 214 := by
  constructor
  · intro e _hLower hUpper
    have hUpper' : e ≤ 213 := by
      simpa [bandUpper] using hUpper
    have hne : e ≠ 214 := by
      omega
    simp [outOfBandCountermodel, hne, championCap]
  · decide

theorem compiler_arithmetic_requires_out_of_band_input :
    bandUpper - bandLower + 1 = 181 ∧
    admissibleShellCount - 181 = 266 ∧
    181 + 266 = admissibleShellCount ∧
    1 + championCap * admissibleShellCount + ambientContribution = 15007628 ∧
    budget - 15007628 = 1769587 ∧
    1 + 5191 * admissibleShellCount + ambientContribution = 16776854 ∧
    1 + 5192 * admissibleShellCount + ambientContribution = 16777301 ∧
    budget < 16777301 := by
  decide

#print axioms integrated_floor_matches_cap
#print axioms mixed_remainder_geometry_exact
#print axioms mixed_t64_t32_closure_exact
#print axioms reflected_e256_mixed_packet_exact
#print axioms reflected_e256_full_packet_exact
#print axioms selector_zero_and_deployed_e96_coexist
#print axioms selector_atlas_scope_arithmetic
#print axioms typed_external_obstructions_coexist
#print axioms band_only_countermodel
#print axioms compiler_arithmetic_requires_out_of_band_input

end M31FlatnessConjectureA1S2
