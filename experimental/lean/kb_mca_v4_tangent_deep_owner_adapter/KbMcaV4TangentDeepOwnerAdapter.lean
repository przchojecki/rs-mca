import Std

/-!
# KoalaBear v4 tangent-plus-deep owner adapter

This stdlib-only module formalizes the finite first-match, frontloading, and
integer kernels of the active KoalaBear tangent-plus-deep owner packet.

The source theorems that produce the tangent and deep envelopes are recorded
in `CORRESPONDENCE.md`. This module does not axiomatize or re-prove them.
-/

set_option autoImplicit false

namespace KbMcaV4TangentDeepOwnerAdapter

def basePrime : Nat := 2130706433
def extensionDegree : Nat := 6
def domainSize : Nat := 2097152
def codeDimension : Nat := 1048576
def redundancy : Nat := domainSize - codeDimension
def agreement : Nat := 1116048
def tangentCharge : Nat := domainSize - agreement
def deepRadius : Nat := redundancy / 3
def deepAgreement : Nat := domainSize - deepRadius
def deepCharge : Nat := deepRadius + 1
def paidCharge : Nat := tangentCharge + deepCharge
def budget : Nat := 274980728111395087
def remainingBudget : Nat := 274980728110064457
def legacyBranch2Charge : Nat := 67472
def legacyBranch3Increment : Nat := 282054

/-- Active first-match owner order. -/
inductive Owner where
  | tangent
  | deep
  | q
  | bc
  | new
  | outside
  deriving DecidableEq, Repr

/-- The active successor partition inserts the intrinsic deep owner after the
source-coordinate tangent owner and before Q. -/
def firstOwner {F : Type}
    (bad tangent deep qCertified bcCertified : F -> Bool) (z : F) : Owner :=
  if bad z then
    if tangent z then .tangent
    else if deep z then .deep
    else if qCertified z then .q
    else if bcCertified z then .bc
    else .new
  else .outside

/-- Every bad slope has exactly one active owner constructor. -/
theorem activeOwner_cases_of_bad {F : Type}
    (bad tangent deep qCertified bcCertified : F -> Bool) (z : F)
    (hbad : bad z = true) :
    firstOwner bad tangent deep qCertified bcCertified z = .tangent ∨
    firstOwner bad tangent deep qCertified bcCertified z = .deep ∨
    firstOwner bad tangent deep qCertified bcCertified z = .q ∨
    firstOwner bad tangent deep qCertified bcCertified z = .bc ∨
    firstOwner bad tangent deep qCertified bcCertified z = .new := by
  cases htan : tangent z <;>
  cases hdeep : deep z <;>
  cases hq : qCertified z <;>
  cases hbc : bcCertified z <;>
  simp [firstOwner, hbad, htan, hdeep, hq, hbc]

/-- Constructor-valued first ownership is unique. -/
theorem firstOwner_unique {F : Type}
    (bad tangent deep qCertified bcCertified : F -> Bool) (z : F)
    (o1 o2 : Owner)
    (h1 : firstOwner bad tangent deep qCertified bcCertified z = o1)
    (h2 : firstOwner bad tangent deep qCertified bcCertified z = o2) :
    o1 = o2 := by
  exact h1.symm.trans h2

/-- The legacy local order places the intrinsic deep owner before tangent. -/
def legacyDeepThenTangentPaid {F : Type}
    (bad tangent deep : F -> Bool) (z : F) : Bool :=
  (bad z && deep z) || (bad z && !deep z && tangent z)

/-- The active order places tangent before the restricted deep owner. -/
def activeTangentThenDeepPaid {F : Type}
    (bad tangent deep : F -> Bool) (z : F) : Bool :=
  (bad z && tangent z) || (bad z && !tangent z && deep z)

/-- Frontloading tangent preserves the union of the two source-bound cells
pointwise. -/
theorem frontload_tangent_paid_union {F : Type}
    (bad tangent deep : F -> Bool) (z : F) :
    legacyDeepThenTangentPaid bad tangent deep z =
      activeTangentThenDeepPaid bad tangent deep z := by
  cases hbad : bad z <;>
  cases htan : tangent z <;>
  cases hdeep : deep z <;>
  simp [legacyDeepThenTangentPaid, activeTangentThenDeepPaid,
    hbad, htan, hdeep]

/-- A slope in the active deep cell is bad, is outside tangent, and satisfies
the intrinsic deep predicate. -/
theorem activeDeep_characterization {F : Type}
    (bad tangent deep qCertified bcCertified : F -> Bool) (z : F) :
    firstOwner bad tangent deep qCertified bcCertified z = .deep ↔
      bad z = true ∧ tangent z = false ∧ deep z = true := by
  cases hbad : bad z <;>
  cases htan : tangent z <;>
  cases hdeep : deep z <;>
  cases hq : qCertified z <;>
  cases hbc : bcCertified z <;>
  simp [firstOwner, hbad, htan, hdeep, hq, hbc]

/-- Exact deployed deep-radius, charge, and row-ledger arithmetic. -/
theorem deployedConstantsExact :
    redundancy = 1048576 ∧
    tangentCharge = 981104 ∧
    deepRadius = 349525 ∧
    3 * deepRadius ≤ redundancy ∧
    deepAgreement = 1747627 ∧
    deepCharge = 349526 ∧
    legacyBranch2Charge + legacyBranch3Increment = deepCharge ∧
    paidCharge = 1330630 ∧
    paidCharge < budget ∧
    budget - paidCharge = remainingBudget := by
  decide

#print axioms activeOwner_cases_of_bad
#print axioms firstOwner_unique
#print axioms frontload_tangent_paid_union
#print axioms activeDeep_characterization
#print axioms deployedConstantsExact

end KbMcaV4TangentDeepOwnerAdapter
