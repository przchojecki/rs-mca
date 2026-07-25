import M31FlatnessKeystone
import M31QuotientBandMixing
import M31QuotientT16MixingFloor

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 flatness conjecture, round C1

The conjecture is the sharp scalar pointwise cap `1233` on every rooted
same-prefix shell in the sub-crossover band `33 <= e <= 213` of the pinned
punctured quotient domain.  It is stated as a finitary universal property of
all duplicate-free lists of certified neighbors, so a minimal falsifier is an
explicit list of `1234` full supports.

No theorem in this module proves the conjecture.  The proved declarations are:

* the logical implication from a minimal certificate to refutation;
* exact consistency of the integrated `T_64`, off-lattice `T_16`, and mixed
  `e=192` packets with the cap, including a certified packet of length `1233`;
* the exact scope guard supplied by the complete-`T_32` selector atlas; and
* the coefficient-four compiler arithmetic at the champion cap.

`native_decide` is used only for the closed finite zoo-consistency theorem.
Every theorem has a `#print axioms` census below.
-/

namespace M31FlatnessConjectureC1

abbrev Support := List Nat
abbrev PrefixTarget := List Nat

def fieldPrime : Nat := 2 ^ 31 - 1
def prefixDepth : Nat := 32
def supportSize : Nat := 479
def complementSize : Nat := 543
def bandLower : Nat := 33
def bandUpper : Nat := 213
def championCap : Nat := 1233
def budget : Nat := 16777215
def admissibleShellCount : Nat := supportSize - prefixDepth
def ambientFourContribution : Nat := 14456476
def coefficientFourTotal : Nat :=
  1 + championCap * admissibleShellCount + ambientFourContribution
def coefficientFourReserve : Nat := budget - coefficientFourTotal

/-- Boolean checker for a literal depth-32 target over the pinned base field. -/
def prefixTargetValid (target : PrefixTarget) : Bool :=
  (target.length == prefixDepth) &&
  target.all fun coefficient => decide (coefficient < fieldPrime)

/-- Canonical-list checker for a 479-subset of the punctured domain. -/
def canonicalSupportValid (support : Support) : Bool :=
  M31QuotientT16MixingFloor.Witness.supportValid support &&
  (M31QuotientT16MixingFloor.Witness.canonicalSupport support == support)

/-- Boolean checker for one exact rooted shell neighbor. -/
def bandNeighborValid
    (target : PrefixTarget) (anchor : Support) (e : Nat)
    (support : Support) : Bool :=
  canonicalSupportValid support &&
  (M31QuotientT16MixingFloor.Witness.locatorPrefix prefixDepth support == target) &&
  (M31QuotientT16MixingFloor.Witness.deficiency anchor support == e) &&
  !(support == anchor)

/--
A duplicate-free certificate checker for any finite subset of one rooted shell.
Universality over all such packets is equivalent to the pointwise shell-degree
cap, without requiring a separate executable powerset cardinality operator.
-/
def bandPacketValid
    (target : PrefixTarget) (anchor : Support) (e : Nat)
    (neighbors : List Support) : Bool :=
  prefixTargetValid target &&
  decide (bandLower ≤ e) && decide (e ≤ bandUpper) &&
  canonicalSupportValid anchor &&
  (M31QuotientT16MixingFloor.Witness.locatorPrefix prefixDepth anchor == target) &&
  M31QuotientT16MixingFloor.Witness.noDuplicates neighbors &&
  neighbors.all fun support => bandNeighborValid target anchor e support

/-- Prop wrapper used by the conjecture and falsifier interface. -/
def IsBandPacket
    (target : PrefixTarget) (anchor : Support) (e : Nat)
    (neighbors : List Support) : Prop :=
  bandPacketValid target anchor e neighbors = true

/--
The C1 champion.  It is a definition of a proposition, not a theorem.
-/
def m31Depth32BandFlatnessConjecture : Prop :=
  ∀ (target : PrefixTarget) (anchor : Support) (e : Nat)
      (neighbors : List Support),
    IsBandPacket target anchor e neighbors →
      neighbors.length ≤ championCap

/-- The minimal certificate shape that changes the scalar intercept floor. -/
def IsMinimalChampionFalsifier
    (target : PrefixTarget) (anchor : Support) (e : Nat)
    (neighbors : List Support) : Prop :=
  IsBandPacket target anchor e neighbors ∧
  neighbors.length = championCap + 1

/-- Any valid 1,234-neighbor packet formally refutes the champion. -/
theorem minimal_falsifier_refutes_champion
    (target : PrefixTarget) (anchor : Support) (e : Nat)
    (neighbors : List Support)
    (hFalsifier : IsMinimalChampionFalsifier target anchor e neighbors) :
    ¬ m31Depth32BandFlatnessConjecture := by
  intro hChampion
  have hBound := hChampion target anchor e neighbors hFalsifier.1
  rw [hFalsifier.2] at hBound
  exact Nat.not_succ_le_self championCap hBound

/-! ## Closed integrated-zoo instances -/

def t64SwapSpecs (t : Nat) : List (List Nat × List Nat) :=
  (M31QuotientT16MixingFloor.Witness.choose t
      M31QuotientT16MixingFloor.Witness.insideT64).flatMap fun removed =>
    (M31QuotientT16MixingFloor.Witness.choose t
      M31QuotientT16MixingFloor.Witness.outsideT64).map fun added =>
        (removed, added)

def t64SwapNeighbors (t : Nat) : List Support :=
  (t64SwapSpecs t).map
    M31QuotientT16MixingFloor.Witness.classSwapSupport

def e96Anchor : Support :=
  M31QuotientT16MixingFloor.Witness.canonicalSupport
    M31QuotientBandMixing.Witnesses.mixingAnchor

def e96Neighbor : Support :=
  M31QuotientT16MixingFloor.Witness.canonicalSupport
    M31QuotientBandMixing.Witnesses.mixingNeighbor

def e96Target : PrefixTarget :=
  M31QuotientT16MixingFloor.Witness.locatorPrefix prefixDepth e96Anchor

/--
Kernel-checked mandatory consistency pre-check.  It verifies the exact
`49/441/1225` `T_64` shell packets, the off-lattice `e=96` packet with its
`47/48` coefficient boundary, and the mixed `e=192` packet of exactly `1233`
distinct neighbors.  The last displayed list has length equal to the champion
cap; completeness of that rooted shell is not claimed.
-/
theorem integrated_zoo_consistency_shard :
    (t64SwapNeighbors 1).length = 49 ∧
    (t64SwapNeighbors 2).length = 441 ∧
    (t64SwapNeighbors 3).length = 1225 ∧
    IsBandPacket
      M31QuotientT16MixingFloor.Witness.eta
      M31QuotientT16MixingFloor.Witness.anchor
      64 (t64SwapNeighbors 1) ∧
    IsBandPacket
      M31QuotientT16MixingFloor.Witness.eta
      M31QuotientT16MixingFloor.Witness.anchor
      128 (t64SwapNeighbors 2) ∧
    IsBandPacket
      M31QuotientT16MixingFloor.Witness.eta
      M31QuotientT16MixingFloor.Witness.anchor
      192 (t64SwapNeighbors 3) ∧
    IsBandPacket e96Target e96Anchor 96 [e96Neighbor] ∧
    M31QuotientT16MixingFloor.Witness.locatorPrefix 47 e96Anchor =
      M31QuotientT16MixingFloor.Witness.locatorPrefix 47 e96Neighbor ∧
    M31QuotientT16MixingFloor.Witness.locatorPrefix 48 e96Anchor ≠
      M31QuotientT16MixingFloor.Witness.locatorPrefix 48 e96Neighbor ∧
    96 % 64 = 32 ∧
    IsBandPacket
      M31QuotientT16MixingFloor.Witness.eta
      M31QuotientT16MixingFloor.Witness.anchor
      192 M31QuotientT16MixingFloor.Witness.allNeighbors ∧
    M31QuotientT16MixingFloor.Witness.allNeighbors.length = championCap := by
  unfold IsBandPacket
  native_decide

/--
The complete-T32 atlas controls a fixed-remainder fiber, not one rooted shell.
Its exact `3432` total and `482` nontrivial-collision submaximum therefore do not
contradict the shell cap `1233`.
-/
theorem t32_skeleton_scope_shard :
    M31FlatnessKeystone.SelectorAtlas.atlasSummary.selectorFiberMaximum = 3432 ∧
    M31FlatnessKeystone.SelectorAtlas.atlasSummary.collisionFiberMaximum = 482 ∧
    482 < championCap ∧ 1225 < championCap ∧ championCap < 3432 := by
  have hAtlas := M31FlatnessKeystone.packet_selector_atlas
  constructor
  · have h := congrArg
      (fun summary : M31FlatnessKeystone.SelectorAtlas.AtlasSummary =>
        summary.selectorFiberMaximum) hAtlas
    simpa [M31FlatnessKeystone.SelectorAtlas.expectedAtlasSummary] using h
  constructor
  · have h := congrArg
      (fun summary : M31FlatnessKeystone.SelectorAtlas.AtlasSummary =>
        summary.collisionFiberMaximum) hAtlas
    simpa [M31FlatnessKeystone.SelectorAtlas.expectedAtlasSummary] using h
  · decide

/-- Exact average and coefficient-four ambient contribution on the pinned row. -/
theorem ambient_average_shard :
    M31QuotientBandMixing.Witnesses.M1022_479 /
        M31QuotientBandMixing.Witnesses.Q32 = 3614119 ∧
    (M31QuotientBandMixing.Witnesses.M1022_479 +
        M31QuotientBandMixing.Witnesses.Q32 - 1) /
        M31QuotientBandMixing.Witnesses.Q32 = 3614120 ∧
    (4 * M31QuotientBandMixing.Witnesses.M1022_479) /
        M31QuotientBandMixing.Witnesses.Q32 = ambientFourContribution := by
  simpa [ambientFourContribution] using
    M31QuotientBandMixing.Witnesses.quotient_average_arithmetic

/--
The load-bearing arithmetic shard: the sharp cap is inside the live window and
the coefficient-four compiler total is below budget by exactly `1,769,587`.
The adjacent scalar `5192` is already too expensive.
-/
theorem coefficient_four_compiler_shard :
    admissibleShellCount = 447 ∧
    championCap = 1233 ∧
    championCap ≤ 5191 ∧
    coefficientFourTotal = 15007628 ∧
    coefficientFourTotal ≤ budget ∧
    coefficientFourReserve = 1769587 ∧
    1 + 5191 * admissibleShellCount + ambientFourContribution = 16776854 ∧
    16776854 ≤ budget ∧
    1 + 5192 * admissibleShellCount + ambientFourContribution = 16777301 ∧
    budget < 16777301 := by
  decide

#print axioms minimal_falsifier_refutes_champion
#print axioms integrated_zoo_consistency_shard
#print axioms t32_skeleton_scope_shard
#print axioms ambient_average_shard
#print axioms coefficient_four_compiler_shard

end M31FlatnessConjectureC1
