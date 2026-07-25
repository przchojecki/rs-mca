import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 signed T8 census round 2: lift arithmetic

No received word, codeword, ray, slope, or row payment is asserted.
-/

namespace M31SignedT8CensusR2.Reduction

def fieldPrime : Nat := 2 ^ 31 - 1
def domainSize : Nat := 1022
def supportSize : Nat := 479
def intactClassCount : Nat := 62
def halfClassSize : Nat := 8

def selectorDeficiency (m : Nat) : Nat := halfClassSize * m

def requiredCoreSize (m : Nat) : Int :=
  (supportSize : Int) - (selectorDeficiency m : Int)

def availableCoreLabels (m : Nat) : Int :=
  (domainSize : Int) - (2 * selectorDeficiency m : Int)

def liftableBool (m : Nat) : Bool :=
  decide (0 ≤ requiredCoreSize m ∧ requiredCoreSize m ≤ availableCoreLabels m)

def expectedLiftableTable : List Bool :=
  List.replicate 60 true ++ List.replicate 3 false

/-- Exact symbolic lift criterion throughout the 62-coordinate census range. -/
theorem lift_criterion_iff_support_le_59
    (m : Nat) (hm : m ≤ intactClassCount) :
    (0 ≤ requiredCoreSize m ∧
      requiredCoreSize m ≤ availableCoreLabels m) ↔
      m ≤ 59 := by
  unfold requiredCoreSize availableCoreLabels selectorDeficiency
    supportSize domainSize halfClassSize intactClassCount at *
  omega

/-- Exact census-range table: precisely `m = 0,...,59` lifts. -/
theorem liftable_table_exact :
    (List.range (intactClassCount + 1)).map liftableBool =
      expectedLiftableTable := by
  native_decide

def positiveRowsBelowKnownWitness : List Nat :=
  (List.range 23).map (fun j => j + 1)

def autoLiftImprovementBool (m : Nat) : Bool :=
  liftableBool m && decide (selectorDeficiency m < 192)

/-- Every positive ternary row with `m < 24` lifts and has deficiency `< 192`. -/
theorem auto_lift_rows_below_known_witness_exact :
    positiveRowsBelowKnownWitness.all autoLiftImprovementBool = true := by
  native_decide

theorem auto_lift_below_known_witness
    (m : Nat) (hPositive : 0 < m) (hBelow : m < 24) :
    (0 ≤ requiredCoreSize m ∧
      requiredCoreSize m ≤ availableCoreLabels m) ∧
    selectorDeficiency m < 192 := by
  have hm : m ≤ intactClassCount := by
    unfold intactClassCount
    omega
  constructor
  · exact (lift_criterion_iff_support_le_59 m hm).2 (by omega)
  · unfold selectorDeficiency halfClassSize
    omega

/-- Endpoint arithmetic separating the liftable and unliftable rows. -/
theorem lift_endpoint_arithmetic :
    selectorDeficiency 24 = 192 ∧
    requiredCoreSize 24 = 287 ∧
    availableCoreLabels 24 = 638 ∧
    liftableBool 24 = true ∧
    requiredCoreSize 59 = 7 ∧
    availableCoreLabels 59 = 78 ∧
    liftableBool 59 = true ∧
    requiredCoreSize 60 = -1 ∧
    availableCoreLabels 60 = 62 ∧
    liftableBool 60 = false ∧
    requiredCoreSize 61 = -9 ∧
    availableCoreLabels 61 = 46 ∧
    liftableBool 61 = false ∧
    requiredCoreSize 62 = -17 ∧
    availableCoreLabels 62 = 30 ∧
    liftableBool 62 = false := by
  native_decide

#print axioms lift_criterion_iff_support_le_59
#print axioms liftable_table_exact
#print axioms auto_lift_rows_below_known_witness_exact
#print axioms auto_lift_below_known_witness
#print axioms lift_endpoint_arithmetic

end M31SignedT8CensusR2.Reduction
