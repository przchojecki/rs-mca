import Std

namespace LRootliftBridge

/-! ## Deployed exact arithmetic -/

def p : Nat := 2 ^ 31 - 1
def q : Nat := p ^ 4
def n : Nat := 2 ^ 21
def k : Nat := 2 ^ 20
def agreement : Nat := 1116023
def errors : Nat := n - agreement
def w : Nat := agreement - k
def bStar : Nat := 16777215
def rootCount : Nat := 32
def fibreSize : Nat := 65536
def agreementRemainder : Nat := 1911
def multiplier : Nat := 8
def baseline : Nat := multiplier * (agreementRemainder + 1)
def offset : Nat := rootCount * baseline - 1
def reportedCount (L : Nat) : Nat := rootCount * L - offset

theorem field_size :
    q = 21267647892944572736998860269687930881 := by
  native_decide

theorem row_parameters :
    n = 2097152 ∧ k = 1048576 ∧ errors = 981129 ∧ w = 67447 := by
  native_decide

theorem order32_decomposition :
    n = rootCount * fibreSize ∧
    agreement = 17 * fibreSize + agreementRemainder ∧
    w = fibreSize + agreementRemainder := by
  native_decide

theorem budget_decomposition :
    bStar + 1 = multiplier * n ∧
    baseline = 15296 ∧
    offset = 489471 := by
  native_decide

theorem reported_low :
    reportedCount 539583 = 16777185 ∧
    bStar - reportedCount 539583 = 30 := by
  native_decide

theorem reported_high :
    reportedCount 539584 = 16777217 ∧
    reportedCount 539584 - bStar = 2 := by
  native_decide

theorem reported_boundary :
    (bStar + offset) / rootCount = 539583 ∧
    (bStar + offset) % rootCount = 30 := by
  native_decide

theorem crude_rooted_boundary :
    bStar / rootCount = 524287 ∧
    bStar % rootCount = 31 ∧
    rootCount * 524287 = bStar - 31 ∧
    rootCount * 524288 = bStar + 1 := by
  native_decide

/-! ## Exact F_37 finite counterexample

The target code is the affine Reed--Solomon code on all 37 field elements.
The selected roots are 0,...,31.  The two words are zero on those roots and
have the displayed five values at 32,...,36.

All field elements are represented by canonical naturals in [0,37).
-/

def modulus : Nat := 37
def domain : List Nat := List.range modulus
def roots : List Nat := List.range 32

def wordA (x : Nat) : Nat :=
  if x = 35 then 1 else if x = 36 then 2 else 0

def wordB (x : Nat) : Nat :=
  if x = 35 then 1 else if x = 36 then 1 else 0

def evalAffine (poly : Nat × Nat) (x : Nat) : Nat :=
  (poly.1 + poly.2 * x) % modulus

def affinePolys : List (Nat × Nat) :=
  (List.range modulus).flatMap fun intercept =>
    (List.range modulus).map fun slope => (intercept, slope)

def targetAgreement (u : Nat → Nat) (poly : Nat × Nat) : Nat :=
  (domain.filter fun x => evalAffine poly x == u x).length

def targetList (u : Nat → Nat) : List (Nat × Nat) :=
  affinePolys.filter fun poly => decide (targetAgreement u poly ≥ 2)

def inv37 (a : Nat) : Nat :=
  ((List.range modulus).find? fun z => (a * z) % modulus == 1).getD 0

def partnerReceived (u : Nat → Nat) (alpha x : Nat) : Nat :=
  (u x * inv37 ((x + modulus - alpha) % modulus)) % modulus

def partnerAgreement (u : Nat → Nat) (alpha constant : Nat) : Nat :=
  (domain.filter fun x =>
    (x != alpha) && (constant == partnerReceived u alpha x)).length

def partnerList (u : Nat → Nat) (alpha : Nat) : List Nat :=
  (List.range modulus).filter fun constant =>
    decide (partnerAgreement u alpha constant ≥ 1)

def allPartnerSizeThree (u : Nat → Nat) : Bool :=
  roots.all fun alpha => (partnerList u alpha).length == 3

def liftConstant (alpha constant : Nat) : Nat × Nat :=
  ((modulus - (alpha * constant) % modulus) % modulus, constant % modulus)

def rootSlice (u : Nat → Nat) (alpha : Nat) : List (Nat × Nat) :=
  (partnerList u alpha).map fun constant => liftConstant alpha constant

def rootMultiplicity (u : Nat → Nat) (poly : Nat × Nat) : Nat :=
  (roots.filter fun alpha => (rootSlice u alpha).contains poly).length

def isRooted (u : Nat → Nat) (poly : Nat × Nat) : Bool :=
  decide (rootMultiplicity u poly > 0)

def rootedTarget (u : Nat → Nat) : List (Nat × Nat) :=
  (targetList u).filter fun poly => isRooted u poly

def freeCount (u : Nat → Nat) : Nat :=
  (targetList u).length - (rootedTarget u).length

def overlapExcess (u : Nat → Nat) : Nat :=
  (rootedTarget u).foldl
    (fun total poly => total + (rootMultiplicity u poly - 1)) 0

theorem partner_sizes_A : allPartnerSizeThree wordA = true := by
  native_decide

theorem partner_sizes_B : allPartnerSizeThree wordB = true := by
  native_decide

theorem target_count_A :
    (targetList wordA).length = 70 ∧
    (rootedTarget wordA).length = 65 ∧
    freeCount wordA = 5 ∧
    overlapExcess wordA = 31 := by
  native_decide

theorem target_count_B :
    (targetList wordB).length = 72 ∧
    (rootedTarget wordB).length = 65 ∧
    freeCount wordB = 7 ∧
    overlapExcess wordB = 31 := by
  native_decide

theorem partner_size_does_not_determine_target :
    allPartnerSizeThree wordA = allPartnerSizeThree wordB ∧
    (targetList wordA).length ≠ (targetList wordB).length := by
  native_decide

/-! The smallest cross-root multiplication collision:
    X*(X-1) = (X-1)*X. -/

def mulRoot (alpha : Nat) (poly : Nat × Nat) : Nat × Nat × Nat :=
  (
    (modulus - (alpha * poly.1) % modulus) % modulus,
    (poly.1 + modulus - (alpha * poly.2) % modulus) % modulus,
    poly.2 % modulus
  )

theorem cross_root_collision :
    mulRoot 0 (36, 1) = mulRoot 1 (0, 1) ∧
    mulRoot 0 (36, 1) = (0, 36, 1) := by
  native_decide

#print axioms field_size
#print axioms row_parameters
#print axioms order32_decomposition
#print axioms budget_decomposition
#print axioms reported_low
#print axioms reported_high
#print axioms reported_boundary
#print axioms crude_rooted_boundary
#print axioms partner_sizes_A
#print axioms partner_sizes_B
#print axioms target_count_A
#print axioms target_count_B
#print axioms partner_size_does_not_determine_target
#print axioms cross_root_collision

end LRootliftBridge
