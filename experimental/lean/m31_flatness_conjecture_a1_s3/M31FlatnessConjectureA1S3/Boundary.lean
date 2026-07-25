import M31FlatnessKeystone
import M31QuotientBandMixing
import M31QuotientT16MixingFloor

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 flatness conjecture A1, session 3: necessity and boundary certificates

This module does not prove or refute the pinned depth-32 champion.  It checks
three exact failure surfaces of weakened statements:

* restoring one deleted quotient label gives a 1,234-neighbor depth-32 packet;
* observing only 31 locator coefficients gives a 1,234-neighbor packet on the
  exact pinned domain;
* aggregating several exact deficiencies before applying the scalar cap gives a
  1,723-neighbor packet on the exact pinned domain.

It also records the duplicate-list interface failure.  Every support packet is
constructed canonically from the quotient labels and every claimed prefix is
checked by the direct truncated multiplication of all 479 linear factors.
`native_decide` is used only for the closed finite certificates below.
-/

namespace M31FlatnessConjectureA1S3

abbrev Support := List Nat
abbrev PrefixTarget := List Nat

abbrev fieldPrime : Nat :=
  M31QuotientT16MixingFloor.Witness.fieldPrime
abbrev pinnedDomain : List Nat :=
  M31QuotientT16MixingFloor.Witness.puncturedReps
abbrev fullDomain : List Nat :=
  M31QuotientT16MixingFloor.Witness.oddReps
abbrev pinnedAnchor : Support :=
  M31QuotientT16MixingFloor.Witness.anchor
abbrev pinnedTarget : PrefixTarget :=
  M31QuotientT16MixingFloor.Witness.eta
abbrev insideT64 : List Nat :=
  M31QuotientT16MixingFloor.Witness.insideT64
abbrev outsideT64 : List Nat :=
  M31QuotientT16MixingFloor.Witness.outsideT64

abbrev noDuplicates {α : Type} [BEq α] (xs : List α) : Bool :=
  M31QuotientT16MixingFloor.Witness.noDuplicates xs
abbrev chooseW {α : Type} (k : Nat) (xs : List α) : List (List α) :=
  M31QuotientT16MixingFloor.Witness.choose k xs
abbrev locatorPrefix (depth : Nat) (support : Support) : PrefixTarget :=
  M31QuotientT16MixingFloor.Witness.locatorPrefix depth support
abbrev deficiency (anchor support : Support) : Nat :=
  M31QuotientT16MixingFloor.Witness.deficiency anchor support
abbrev t64BlockReps (a : Nat) : List Nat :=
  M31QuotientT16MixingFloor.Witness.t64BlockReps a
abbrev t32BlockReps (a : Nat) : List Nat :=
  M31QuotientT16MixingFloor.Witness.t32BlockReps a
abbrev fastBinomial (n k : Nat) : Nat :=
  M31QuotientT16MixingFloor.Witness.fastBinomial n k


def supportSize : Nat := 479
def championCap : Nat := 1233
def bandLower : Nat := 33
def bandUpper : Nat := 213

/-- Canonicalize a support against an explicitly supplied ordered domain. -/
def canonicalOn (domain support : Support) : Support :=
  domain.filter fun r => support.contains r

/-- The support validity guard used by every boundary packet. -/
def canonicalSupportValidOn (domain support : Support) : Bool :=
  (support.length == supportSize) &&
  noDuplicates support &&
  (support.all fun r => domain.contains r) &&
  (canonicalOn domain support == support)

/-- A literal target of the requested depth over the pinned base field. -/
def targetValidAt (depth : Nat) (target : PrefixTarget) : Bool :=
  (target.length == depth) &&
  (target.all fun coefficient => decide (coefficient < fieldPrime))

/-- Direct exact-shell packet checker at a chosen domain and prefix depth. -/
def exactShellPacketValidAt
    (domain : Support) (depth : Nat) (target : PrefixTarget)
    (anchor : Support) (e : Nat) (neighbors : List Support) : Bool :=
  targetValidAt depth target &&
  canonicalSupportValidOn domain anchor &&
  (locatorPrefix depth anchor == target) &&
  noDuplicates neighbors &&
  (neighbors.all fun support =>
    canonicalSupportValidOn domain support &&
    (locatorPrefix depth support == target) &&
    (deficiency anchor support == e) &&
    !(support == anchor))

/-- The scalar statement with domain, depth, and band made explicit. -/
def UniformShellCap
    (domain : Support) (depth lower upper cap : Nat) : Prop :=
  ∀ (target : PrefixTarget) (anchor : Support) (e : Nat)
      (neighbors : List Support),
    exactShellPacketValidAt domain depth target anchor e neighbors = true →
    lower ≤ e → e ≤ upper → neighbors.length ≤ cap

/-- Same-target packet checker after forgetting the exact-shell equality. -/
def aggregateBandPacketValidAt
    (domain : Support) (depth lower upper : Nat) (target : PrefixTarget)
    (anchor : Support) (neighbors : List Support) : Bool :=
  targetValidAt depth target &&
  canonicalSupportValidOn domain anchor &&
  (locatorPrefix depth anchor == target) &&
  noDuplicates neighbors &&
  (neighbors.all fun support =>
    canonicalSupportValidOn domain support &&
    (locatorPrefix depth support == target) &&
    decide (lower ≤ deficiency anchor support) &&
    decide (deficiency anchor support ≤ upper) &&
    !(support == anchor))

/-- The invalid aggregate replacement for the pointwise shell cap. -/
def UniformAggregateBandCap
    (domain : Support) (depth lower upper cap : Nat) : Prop :=
  ∀ (target : PrefixTarget) (anchor : Support)
      (neighbors : List Support),
    aggregateBandPacketValidAt domain depth lower upper target anchor neighbors = true →
    neighbors.length ≤ cap

/-- Support replacement inside an explicitly supplied domain. -/
def exchangedOnDomain
    (domain anchor removed added : Support) : Support :=
  domain.filter fun r =>
    (anchor.contains r && !(removed.contains r)) || added.contains r

/-! ## Boundary 1: one restored puncture -/

/-- Restore representative `3` while keeping representative `1` deleted. -/
def restoreThreeDomain : Support :=
  fullDomain.filter fun r => !(r == 1)

def restoreThreeOutsideT64 : List Nat :=
  [3, 5, 11, 15, 17, 25, 29, 31]

def restoreThreeSpecs : List (List Nat × List Nat) :=
  (chooseW 3 insideT64).flatMap fun removed =>
    (chooseW 3 restoreThreeOutsideT64).map fun added => (removed, added)

def restoreThreeSupport (spec : List Nat × List Nat) : Support :=
  exchangedOnDomain restoreThreeDomain pinnedAnchor
    (spec.1.flatMap t64BlockReps)
    (spec.2.flatMap t64BlockReps)

/-- The first 1,234 members of the 1,960-member one-puncture family. -/
def restoreThreeNeighbors : List Support :=
  (restoreThreeSpecs.take (championCap + 1)).map restoreThreeSupport

/--
Restoring only the deleted representative `3` already falsifies the scalar
cap.  Every locator comparison below is recomputed from all 479 roots.
-/
theorem single_puncture_boundary_packet_exact :
    restoreThreeDomain.length = 1023 ∧
    noDuplicates restoreThreeDomain = true ∧
    restoreThreeSpecs.length = 1960 ∧
    restoreThreeNeighbors.length = championCap + 1 ∧
    exactShellPacketValidAt restoreThreeDomain 32 pinnedTarget pinnedAnchor 192
      restoreThreeNeighbors = true := by
  native_decide

/-- The cap cannot be made domain-agnostic even by restoring one point. -/
theorem single_puncture_uniform_cap_refuted :
    ¬ UniformShellCap restoreThreeDomain 32 bandLower bandUpper championCap := by
  intro hCap
  rcases single_puncture_boundary_packet_exact with
    ⟨_, _, _, hLength, hPacket⟩
  have hBound := hCap pinnedTarget pinnedAnchor 192 restoreThreeNeighbors
    hPacket (by decide) (by decide)
  rw [hLength] at hBound
  exact Nat.not_succ_le_self championCap hBound

/-! ## Boundary 2: one fewer locator coefficient -/

/-- Split each intact `T_64` class into its two `T_32` classes. -/
def splitT64ToT32 (a : Nat) : List Nat := [a, 64 - a]

def insideT32 : List Nat := insideT64.flatMap splitT64ToT32
def outsideT32 : List Nat := outsideT64.flatMap splitT64ToT32

/-- Three complete inside `T_64` classes, represented as six `T_32` classes. -/
def depth31Removed : List Nat := [7, 57, 9, 55, 13, 51]

def depth31AddedChoices : List (List Nat) :=
  (chooseW 6 outsideT32).take (championCap + 1)

def depth31Support (added : List Nat) : Support :=
  exchangedOnDomain pinnedDomain pinnedAnchor
    (depth31Removed.flatMap t32BlockReps)
    (added.flatMap t32BlockReps)

def depth31Neighbors : List Support :=
  depth31AddedChoices.map depth31Support

def depth31Target : PrefixTarget := locatorPrefix 31 pinnedAnchor

def depth31BreakNeighbor : Support := depth31Neighbors.getD 1 []

def coefficient32 (support : Support) : Nat :=
  (locatorPrefix 32 support).getD 31 0

/--
The exact pinned domain has a direct 1,234-neighbor falsifier at depth 31.
The selected break neighbor has a different coefficient 32, locating the
failure surface exactly between depths 31 and 32.
-/
theorem depth31_boundary_packet_exact :
    insideT32.length = 14 ∧
    outsideT32.length = 14 ∧
    (chooseW 6 outsideT32).length = 3003 ∧
    depth31AddedChoices.length = championCap + 1 ∧
    depth31Neighbors.length = championCap + 1 ∧
    exactShellPacketValidAt pinnedDomain 31 depth31Target pinnedAnchor 192
      depth31Neighbors = true ∧
    coefficient32 pinnedAnchor = 141998040 ∧
    coefficient32 depth31BreakNeighbor = 138806059 ∧
    locatorPrefix 32 depth31BreakNeighbor ≠ locatorPrefix 32 pinnedAnchor := by
  native_decide

/-- Observing only 31 coefficients is insufficient on the exact pinned domain. -/
theorem depth31_uniform_cap_refuted :
    ¬ UniformShellCap pinnedDomain 31 bandLower bandUpper championCap := by
  intro hCap
  rcases depth31_boundary_packet_exact with
    ⟨_, _, _, _, hLength, hPacket, _, _, _⟩
  have hBound := hCap depth31Target pinnedAnchor 192 depth31Neighbors
    hPacket (by decide) (by decide)
  rw [hLength] at hBound
  exact Nat.not_succ_le_self championCap hBound

/-! ## Boundary 3: forgetting the exact deficiency -/


def t64SwapSpecs (t : Nat) : List (List Nat × List Nat) :=
  (chooseW t insideT64).flatMap fun removed =>
    (chooseW t outsideT64).map fun added => (removed, added)

def t64SwapSupport (spec : List Nat × List Nat) : Support :=
  exchangedOnDomain pinnedDomain pinnedAnchor
    (spec.1.flatMap t64BlockReps)
    (spec.2.flatMap t64BlockReps)

def t64SwapNeighbors (t : Nat) : List Support :=
  (t64SwapSpecs t).map t64SwapSupport

/-- Exact-shell packets at 64 and 128, followed by the certified 1,233 packet. -/
def aggregateBandNeighbors : List Support :=
  t64SwapNeighbors 1 ++
  t64SwapNeighbors 2 ++
  M31QuotientT16MixingFloor.Witness.allNeighbors

/--
The pointwise shell quantifier is essential: pooling three band shells produces
1,723 distinct same-target neighbors, although no displayed shell exceeds the
champion scalar.
-/
theorem aggregate_shell_packet_exact :
    (t64SwapNeighbors 1).length = 49 ∧
    (t64SwapNeighbors 2).length = 441 ∧
    M31QuotientT16MixingFloor.Witness.allNeighbors.length = 1233 ∧
    aggregateBandNeighbors.length = 1723 ∧
    (aggregateBandNeighbors.filter fun support =>
      deficiency pinnedAnchor support == 64).length = 49 ∧
    (aggregateBandNeighbors.filter fun support =>
      deficiency pinnedAnchor support == 128).length = 441 ∧
    (aggregateBandNeighbors.filter fun support =>
      deficiency pinnedAnchor support == 192).length = 1233 ∧
    aggregateBandPacketValidAt pinnedDomain 32 bandLower bandUpper
      pinnedTarget pinnedAnchor aggregateBandNeighbors = true := by
  native_decide

/-- A single aggregate cap of 1,233 over the whole band is false. -/
theorem aggregate_uniform_cap_refuted :
    ¬ UniformAggregateBandCap pinnedDomain 32 bandLower bandUpper championCap := by
  intro hCap
  rcases aggregate_shell_packet_exact with
    ⟨_, _, _, hLength, _, _, _, hPacket⟩
  have hBound := hCap pinnedTarget pinnedAnchor aggregateBandNeighbors hPacket
  rw [hLength] at hBound
  have hNot : ¬ 1723 ≤ championCap := by decide
  exact hNot hBound

/-! ## Representation boundary: duplicate-free lists -/

/-- One exact deficiency-64 neighbor. -/
def firstE64Neighbor : Support := (t64SwapNeighbors 1).headD []

def repeatedNeighborPacket : List Support :=
  List.replicate (championCap + 1) firstE64Neighbor

/-- Exact-shell checker with the duplicate guard deliberately removed. -/
def exactShellPacketWithoutDuplicateGuard
    (domain : Support) (depth : Nat) (target : PrefixTarget)
    (anchor : Support) (e : Nat) (neighbors : List Support) : Bool :=
  targetValidAt depth target &&
  canonicalSupportValidOn domain anchor &&
  (locatorPrefix depth anchor == target) &&
  (neighbors.all fun support =>
    canonicalSupportValidOn domain support &&
    (locatorPrefix depth support == target) &&
    (deficiency anchor support == e) &&
    !(support == anchor))

/--
Without duplicate-freeness, one valid neighbor can be repeated 1,234 times.
This is an encoding counterexample, not a counterexample to set cardinality.
-/
theorem duplicate_guard_boundary_exact :
    repeatedNeighborPacket.length = championCap + 1 ∧
    noDuplicates repeatedNeighborPacket = false ∧
    exactShellPacketWithoutDuplicateGuard pinnedDomain 32 pinnedTarget
      pinnedAnchor 64 repeatedNeighborPacket = true := by
  native_decide

/-! ## Closed arithmetic used by the derivation-direction ledger -/

theorem boundary_family_arithmetic :
    fastBinomial 14 6 = 3003 ∧
    3003 * 3003 = 9018009 ∧
    fastBinomial 7 3 = 35 ∧
    fastBinomial 8 3 = 56 ∧
    35 * 56 = 1960 ∧
    49 + 441 + 1233 = 1723 ∧
    championCap + 1 = 1234 ∧
    1234 < 1723 ∧
    1233 < 1960 ∧
    1233 < 9018009 := by
  native_decide

#print axioms single_puncture_boundary_packet_exact
#print axioms single_puncture_uniform_cap_refuted
#print axioms depth31_boundary_packet_exact
#print axioms depth31_uniform_cap_refuted
#print axioms aggregate_shell_packet_exact
#print axioms aggregate_uniform_cap_refuted
#print axioms duplicate_guard_boundary_exact
#print axioms boundary_family_arithmetic

end M31FlatnessConjectureA1S3
