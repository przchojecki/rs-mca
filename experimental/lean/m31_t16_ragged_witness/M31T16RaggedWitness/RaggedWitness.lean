import M31T16RaggedWitness.CountingRefutation

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Explicit ragged depth-32 collision

This module constructs two deployed 479-supports from twenty-four opposite
T8 half-classes and a 287-point common core.  It verifies the support
conditions, deficiency 192, exact locator-prefix agreement through coefficient
39, failure at coefficient 40, and a partial T16 class on both sides.

No received word, codeword, ray, slope, or list-row projection is asserted.

The finite domain machinery (`oddReps`, `labelOfRep`, `fieldPrime`,
`chebyshevPowTwo`, `canonicalSupport`, `puncturedReps`, `supportValid`,
`deficiency`, `locatorPrefix`, `noDuplicates`, `sumMod`, `isSubset`,
`t16BlockReps`) is the upstream package
`experimental/lean/m31_quotient_t16_mixing_floor/` (`Witness.lean`).
-/

namespace M31T16RaggedWitness.RaggedWitness

open M31QuotientT16MixingFloor.Witness

def t8BlockReps (a : Nat) : List Nat :=
  oddReps.filter fun r =>
    (r % 512 == a) || (r % 512 == 512 - a)

def t8Rho (a : Nat) : Nat :=
  chebyshevPowTwo 3 ((2 * labelOfRep a) % fieldPrime)

/--
The selected T8 half in each of twenty-four intact T16 classes.  The lists are
paired positionwise; paired entries are opposite halves of one T16 class.
-/
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

def supportDifference (xs ys : Support) : Support :=
  xs.filter fun r => !(ys.contains r)

def cubeMod (x : Nat) : Nat :=
  let y := x % fieldPrime
  (((y * y) % fieldPrime) * y) % fieldPrime

def sumCubesMod (xs : List Nat) : Nat :=
  xs.foldl (fun total x => (total + cubeMod x) % fieldPrime) 0

def commonPrefix32 : PrefixTarget :=
  [1855844193, 1473516259, 1180855483, 1278472540,
   19420661, 1326549671, 185963244, 549194916,
   1782472388, 540362367, 1873064133, 1262538111,
   1676789978, 1180247279, 705606729, 896635126,
   1579828831, 624675746, 1809833968, 679266634,
   777394799, 1302213418, 902807383, 658621866,
   543253585, 517492700, 226469049, 919947861,
   1715697364, 1176419888, 1774114675, 433908075]

theorem signed_t8_relation_exact :
    xT8Classes.length = 24 ∧
    yT8Classes.length = 24 ∧
    noDuplicates (xT8Classes ++ yT8Classes) = true ∧
    (xT8Classes ++ yT8Classes).all
      (fun a => (t8BlockReps a).length == 8) = true ∧
    (List.zip xT8Classes yT8Classes).all
      (fun pair => (t8Rho pair.1 + t8Rho pair.2) % fieldPrime == 0) = true ∧
    sumMod (xT8Classes.map t8Rho) = 0 ∧
    sumMod (yT8Classes.map t8Rho) = 0 ∧
    sumCubesMod (xT8Classes.map t8Rho) = 0 ∧
    sumCubesMod (yT8Classes.map t8Rho) = 0 := by
  native_decide

theorem explicit_ragged_collision :
    xExchangeReps.length = 192 ∧
    yExchangeReps.length = 192 ∧
    noDuplicates xExchangeReps = true ∧
    noDuplicates yExchangeReps = true ∧
    commonCore.length = 287 ∧
    noDuplicates commonCore = true ∧
    supportValid anchor = true ∧
    supportValid neighbor = true ∧
    canonicalSupport anchor = anchor ∧
    canonicalSupport neighbor = neighbor ∧
    supportDifference anchor neighbor = xExchangeReps ∧
    supportDifference neighbor anchor = yExchangeReps ∧
    deficiency anchor neighbor = 192 ∧
    locatorPrefix 32 anchor = commonPrefix32 ∧
    locatorPrefix 32 neighbor = commonPrefix32 ∧
    locatorPrefix 39 anchor = locatorPrefix 39 neighbor ∧
    locatorPrefix 40 anchor ≠ locatorPrefix 40 neighbor ∧
    (locatorPrefix 40 anchor).getD 39 0 = 381197232 ∧
    (locatorPrefix 40 neighbor).getD 39 0 = 1671112725 := by
  native_decide

theorem t16_class_five_is_partial_on_both_sides :
    (t16BlockReps 5).length = 16 ∧
    (t8BlockReps 5).length = 8 ∧
    (t8BlockReps 251).length = 8 ∧
    ((supportDifference anchor neighbor).filter fun r =>
      (t16BlockReps 5).contains r) = t8BlockReps 5 ∧
    ((supportDifference neighbor anchor).filter fun r =>
      (t16BlockReps 5).contains r) = t8BlockReps 251 ∧
    isSubset (t8BlockReps 5) (t16BlockReps 5) = true ∧
    isSubset (t8BlockReps 251) (t16BlockReps 5) = true ∧
    t8BlockReps 5 ≠ t16BlockReps 5 ∧
    t8BlockReps 251 ≠ t16BlockReps 5 := by
  native_decide

#print axioms signed_t8_relation_exact
#print axioms explicit_ragged_collision
#print axioms t16_class_five_is_partial_on_both_sides

end M31T16RaggedWitness.RaggedWitness
