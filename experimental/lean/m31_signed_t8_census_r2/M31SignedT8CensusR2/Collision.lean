import M31SignedT8CensusR2.Lattice

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Direct 479-factor verification of the known signed T8 collision

Discovery equations are not used as the final collision check.  The locator
prefix recurrence below multiplies all 479 factors on each side.
-/

namespace M31SignedT8CensusR2.Collision

open M31SignedT8CensusR2.Data
open M31SignedT8CensusR2.Lattice

abbrev Support := List Nat
abbrev PrefixTarget := List Nat

def canonicalSupport (seed : List Nat) : Support :=
  puncturedReps.filter fun r => seed.contains r

def isSubset (xs ys : List Nat) : Bool :=
  xs.all fun x => ys.contains x

def intersectionCard (xs ys : List Nat) : Nat :=
  (xs.filter fun x => ys.contains x).length

def deficiency (xs ys : List Nat) : Nat :=
  xs.length - intersectionCard xs ys

def supportDifference (xs ys : Support) : Support :=
  xs.filter fun r => !(ys.contains r)

def supportValid (support : Support) : Bool :=
  support.length == 479 &&
  noDuplicates support &&
  isSubset support puncturedReps

def prefixTail (root previous : Nat) : List Nat → List Nat
  | [] => []
  | coefficient :: coefficients =>
      ((coefficient + fieldPrime -
          ((root % fieldPrime) * (previous % fieldPrime)) % fieldPrime) % fieldPrime) ::
        prefixTail root coefficient coefficients

def prefixStep (root : Nat) : List Nat → List Nat
  | [] => []
  | leading :: coefficients =>
      leading :: prefixTail root leading coefficients

/-- Direct multiplication of `prod (Y-labelOfRep r)`, retaining the top depth. -/
def locatorPrefix (depth : Nat) (reps : List Nat) : PrefixTarget :=
  ((reps.foldl
      (fun coefficients r => prefixStep (labelOfRep r) coefficients)
      (1 :: List.replicate depth 0)).drop 1)

def xT8Classes : List Nat :=
  [5, 247, 245, 243, 17, 235, 229, 31, 223, 219, 215, 211,
   51, 55, 199, 61, 193, 65, 77, 177, 175, 95, 97, 107]

def yT8Classes : List Nat :=
  [251, 9, 11, 13, 239, 21, 27, 225, 33, 37, 41, 45,
   205, 201, 57, 195, 63, 191, 179, 79, 81, 161, 159, 149]

def exchangeReps (classes : List Nat) : List Nat :=
  canonicalSupport (classes.flatMap t8BlockReps)

def xExchangeReps : List Nat := exchangeReps xT8Classes
def yExchangeReps : List Nat := exchangeReps yT8Classes

def availableCoreReps : List Nat :=
  puncturedReps.filter fun r =>
    !(xExchangeReps.contains r) && !(yExchangeReps.contains r)

def commonCore : List Nat := availableCoreReps.take 287

def anchor : Support :=
  canonicalSupport (commonCore ++ xExchangeReps)

def neighbor : Support :=
  canonicalSupport (commonCore ++ yExchangeReps)

def canonicalT16OfHalf (a : Nat) : Nat :=
  let r := a % 256
  if r ≤ 128 then r else 256 - r

def signOfHalf (a : Nat) : Int :=
  let r := a % 256
  if r ≤ 128 then 1 else -1

def selectorFromX : List Int :=
  expectedIntactT16Classes.map fun c =>
    match xT8Classes.find? (fun a => canonicalT16OfHalf a == c) with
    | none => 0
    | some a => signOfHalf a

theorem opposite_half_selector_packet_exact :
    xT8Classes.length = 24 ∧
    yT8Classes.length = 24 ∧
    noDuplicates (xT8Classes.map canonicalT16OfHalf) = true ∧
    (List.zip xT8Classes yT8Classes).all (fun pair =>
      canonicalT16OfHalf pair.1 == canonicalT16OfHalf pair.2 &&
      (t8Rho pair.1 + t8Rho pair.2) % fieldPrime == 0) = true ∧
    selectorFromX = knownSelector := by
  native_decide

theorem exact_core_and_complement_construction :
    xExchangeReps.length = 192 ∧
    yExchangeReps.length = 192 ∧
    noDuplicates xExchangeReps = true ∧
    noDuplicates yExchangeReps = true ∧
    intersectionCard xExchangeReps yExchangeReps = 0 ∧
    availableCoreReps.length = 638 ∧
    commonCore.length = 287 ∧
    noDuplicates commonCore = true ∧
    intersectionCard commonCore xExchangeReps = 0 ∧
    intersectionCard commonCore yExchangeReps = 0 ∧
    anchor.length = 479 ∧
    neighbor.length = 479 := by
  native_decide

/--
Final verification layer: both locators are multiplied from all 479 deployed
roots.  The first 39 nonleading coefficients agree and coefficient 40 differs.
-/
theorem known_collision_direct_479_factor_check :
    supportValid anchor = true ∧
    supportValid neighbor = true ∧
    canonicalSupport anchor = anchor ∧
    canonicalSupport neighbor = neighbor ∧
    supportDifference anchor neighbor = xExchangeReps ∧
    supportDifference neighbor anchor = yExchangeReps ∧
    deficiency anchor neighbor = 192 ∧
    locatorPrefix 32 anchor = locatorPrefix 32 neighbor ∧
    locatorPrefix 39 anchor = locatorPrefix 39 neighbor ∧
    locatorPrefix 40 anchor ≠ locatorPrefix 40 neighbor ∧
    (locatorPrefix 40 anchor).getD 39 0 = 381197232 ∧
    (locatorPrefix 40 neighbor).getD 39 0 = 1671112725 := by
  native_decide

#print axioms opposite_half_selector_packet_exact
#print axioms exact_core_and_complement_construction
#print axioms known_collision_direct_479_factor_check

end M31SignedT8CensusR2.Collision
