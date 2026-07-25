import M31SignedT8CensusR2.Data

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Explicit lattice basis, symmetries, witnesses, and the SVP route cut
-/

namespace M31SignedT8CensusR2.Lattice

open M31SignedT8CensusR2.Data

def coordinateCount : Nat := 62

def basisCoefficients : List (Nat × Nat) :=
  [
    (993648993, 1172681669), (714335106, 1286204341), (2060060871, 1662804007), (367103032, 400894168),
    (940340973, 1712435118), (1764686455, 1697843305), (1462637694, 1485855141), (986055872, 1962940771),
    (699733207, 2119757327), (885713178, 1210032709), (1159913708, 951962814), (564727414, 1780683700),
    (1242893547, 1764452922), (1097298958, 647526508), (1906415089, 552655339), (2059806525, 754917309),
    (24385513, 970479421), (291924331, 1345812055), (626288185, 501133813), (749289002, 1381430926),
    (761833632, 669163700), (646381753, 190127166), (2003184910, 1702598777), (1436489092, 1500087824),
    (514100634, 587848127), (95575661, 375374600), (1121579486, 1960567246), (756714550, 824889980),
    (658396687, 1650354968), (449910597, 86885222), (1763751832, 1323234518), (1403520954, 1847791674),
    (1824503966, 163912673), (318964257, 1503411421), (588630469, 1084588092), (815488261, 1008713880),
    (1428631468, 458627230), (1374013276, 1748393261), (2013199753, 1810278174), (1014312210, 1394755382),
    (1854991570, 1744274420), (1636136337, 1850387157), (833691921, 730882952), (734511773, 1800525138),
    (986187849, 1454612679), (1225695496, 1815621389), (924431050, 1995875195), (1912576056, 1146371327),
    (1175709920, 448564251), (1459100300, 352396648), (1208407568, 1336204018), (340548168, 930250467),
    (644964896, 1279560573), (684232847, 1745227478), (1842090302, 1825428015), (816097782, 826404246),
    (959624050, 1463168287), (1112983662, 394484187), (409716325, 1709303351), (367655146, 1299764435)
  ]

def basisRowZero : List Nat :=
  (List.range coordinateCount).map fun i => if i == 0 then fieldPrime else 0

def basisRowOne : List Nat :=
  (List.range coordinateCount).map fun i => if i == 1 then fieldPrime else 0

def tailBasisRow (j : Nat) : List Nat :=
  let coeff := basisCoefficients.getD j (0, 0)
  (List.range coordinateCount).map fun i =>
    if i == 0 then coeff.1
    else if i == 1 then coeff.2
    else if i == j + 2 then 1
    else 0

def basisRowsNat : List (List Nat) :=
  basisRowZero :: basisRowOne ::
    (List.range 60).map tailBasisRow

def weightAt (i coordinate : Nat) : Nat :=
  let pair := expectedWeightPairs.getD i (0, 0)
  if coordinate == 0 then pair.1 else pair.2

def dotModNat (row : List Nat) (coordinate : Nat) : Nat :=
  (List.zip row (List.range coordinateCount)).foldl
    (fun total entry =>
      (total + (entry.1 % fieldPrime) * weightAt entry.2 coordinate) % fieldPrime) 0

def latticeRowNat (row : List Nat) : Bool :=
  row.length == coordinateCount &&
  dotModNat row 0 == 0 &&
  dotModNat row 1 == 0

def eraseAt (i : Nat) (xs : List α) : List α :=
  xs.take i ++ xs.drop (i + 1)

def detAux : Nat → List (List Int) → Int
  | 0, _ => 1
  | _ + 1, [] => 0
  | n + 1, row :: rows =>
      (List.zip (List.range row.length) row).foldl (fun total entry =>
        let i := entry.1
        let coefficient := entry.2
        if coefficient == 0 then
          total
        else
          let minor := rows.map (eraseAt i)
          let term := coefficient * detAux n minor
          if i % 2 == 0 then total + term else total - term) 0

def determinant (matrix : List (List Int)) : Int :=
  detAux matrix.length matrix

def basisRowsInt : List (List Int) :=
  basisRowsNat.map fun row => row.map Int.ofNat

def lowerTriangularBool (matrix : List (List Int)) : Bool :=
  (List.zip (List.range matrix.length) matrix).all fun indexedRow =>
    let i := indexedRow.1
    let row := indexedRow.2
    (List.zip (List.range row.length) row).all fun indexedEntry =>
      let j := indexedEntry.1
      let value := indexedEntry.2
      if i < j then value == 0 else true

def diagonal (matrix : List (List Int)) : List Int :=
  (List.zip (List.range matrix.length) matrix).map fun indexedRow =>
    indexedRow.2.getD indexedRow.1 0

def intResidue : Int → Nat
  | .ofNat n => n % fieldPrime
  | .negSucc n => (fieldPrime - ((n + 1) % fieldPrime)) % fieldPrime

def dotModInt (row : List Int) (coordinate : Nat) : Nat :=
  (List.zip row (List.range coordinateCount)).foldl
    (fun total entry =>
      (total + intResidue entry.1 * weightAt entry.2 coordinate) % fieldPrime) 0

def latticeRowInt (row : List Int) : Bool :=
  row.length == coordinateCount &&
  dotModInt row 0 == 0 &&
  dotModInt row 1 == 0

def supportCount (row : List Int) : Nat :=
  (row.filter fun x => !(x == 0)).length

def squaredNorm (row : List Int) : Nat :=
  row.foldl (fun total x => total + x.natAbs * x.natAbs) 0

def ternaryBool (row : List Int) : Bool :=
  row.all fun x => (x == -1) || (x == 0) || (x == 1)

def knownSelector : List Int :=
  [
    1, 0, -1, -1, -1, 0, 1, 0, -1, 0, 0, -1,
    0, 1, -1, 0, -1, 0, -1, 0, -1, 0, 0, 1,
    0, 1, -1, 0, 1, -1, 1, 0, 0, 0, 0, 0,
    1, -1, -1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0
  ]

def normTwentyTwoRouteCut : List Int :=
  [
    0, -1, -1, 1, 1, 1, 0, 0, 1, 0, 1, -1,
    0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 1, 1,
    -1, 0, 1, 0, -1, 0, -2, 0, 0, 1, -1, 0,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0
  ]

def canonicalRep4096 (x : Nat) : Nat :=
  let r := x % 4096
  if r ≤ 2048 then r else 4096 - r

def puncturePreservingMultiplier (u : Nat) : Bool :=
  u % 2 == 1 &&
  sameSet [canonicalRep4096 u, canonicalRep4096 (3 * u)] [1, 3]

def puncturePreservingMultipliers : List Nat :=
  (List.range 4096).filter puncturePreservingMultiplier

def canonicalT16Class (x : Nat) : Nat :=
  let r := x % 256
  if r ≤ 128 then r else 256 - r

theorem explicit_basis_rows_are_lattice_rows :
    basisCoefficients.length = 60 ∧
    basisRowsNat.length = coordinateCount ∧
    basisRowsNat.all (fun row => row.length == coordinateCount) = true ∧
    basisRowsNat.all latticeRowNat = true := by
  native_decide

/--
The determinant is evaluated by a standard Laplace recursion.  Zero entries are
skipped, so the explicit lower-triangular basis follows one nonzero branch per
row.
-/
theorem explicit_basis_determinant :
    lowerTriangularBool basisRowsInt = true ∧
    diagonal basisRowsInt =
      (fieldPrime : Int) :: (fieldPrime : Int) :: List.replicate 60 1 ∧
    determinant basisRowsInt = 4611686014132420609 ∧
    determinant basisRowsInt = (fieldPrime : Int) * (fieldPrime : Int) := by
  native_decide

theorem known_selector_relation_exact :
    knownSelector.length = coordinateCount ∧
    ternaryBool knownSelector = true ∧
    supportCount knownSelector = 24 ∧
    (knownSelector.filter fun x => x == 1).length = 11 ∧
    (knownSelector.filter fun x => x == -1).length = 13 ∧
    latticeRowInt knownSelector = true ∧
    squaredNorm knownSelector = 24 := by
  native_decide

/--
An ordinary Euclidean SVP search sees this valid lattice vector of squared norm
22 before it can decide the ternary minimum.  The coefficient `-2` makes the
vector inadmissible for the ternary census.
-/
theorem norm_twenty_two_nonternary_route_cut :
    normTwentyTwoRouteCut.length = coordinateCount ∧
    supportCount normTwentyTwoRouteCut = 19 ∧
    squaredNorm normTwentyTwoRouteCut = 22 ∧
    latticeRowInt normTwentyTwoRouteCut = true ∧
    ternaryBool normTwentyTwoRouteCut = false ∧
    normTwentyTwoRouteCut.getD 30 0 = -2 := by
  native_decide

theorem puncture_preserving_multiplier_action_is_trivial :
    puncturePreservingMultipliers = [1, 4095] ∧
    puncturePreservingMultipliers.all (fun u =>
      expectedIntactT16Classes.all (fun a =>
        canonicalT16Class (u * a) == a)) = true := by
  native_decide

theorem ternary_coordinate_fixed_by_sign_only_at_zero :
    ([-1, 0, 1] : List Int).filter (fun x => -x == x) = [0] := by
  native_decide

#print axioms explicit_basis_rows_are_lattice_rows
#print axioms explicit_basis_determinant
#print axioms known_selector_relation_exact
#print axioms norm_twenty_two_nonternary_route_cut
#print axioms puncture_preserving_multiplier_action_is_trivial
#print axioms ternary_coordinate_fixed_by_sign_only_at_zero

end M31SignedT8CensusR2.Lattice
