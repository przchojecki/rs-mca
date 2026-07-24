import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 complete-T32 selector atlas

This stdlib-only module kernel-checks the finite meet-in-the-middle atlas used by
`m31_t32_skeleton_flatness_keystone.md`.

`native_decide` is used for the two 234,375-entry half-sum tables, their exact
intersection, the nine frozen relation rows, the 68,896 compressed collision
edges, endpoint uniqueness, the collision maximum, and exact integer arithmetic.
The polynomial reduction from a fixed canonical remainder to a selector-sum
fiber is proved in the note and mapped in `CORRESPONDENCE.md`.
-/

namespace M31FlatnessKeystone.SelectorAtlas

def fieldPrime : Nat := 2147483647

def pairWeights : List Int :=
  [1038945916, 1885292596, 838195206, 14530030,
   1742797653, 212443077, 1941424532, 7144319,
   228509164, 373229752, 1739004854, 2013328190,
   2079025011, 1796741361]

def singletonWeights : List Int := [9803698, 1263730590]

def fullWeights : List Int := pairWeights ++ singletonWeights

def pairCoefficientValues : List Int := [-2, -1, 0, 1, 2]

def singletonCoefficientValues : List Int := [-1, 0, 1]

def pairPatternStates : List Int := [-1, 0, 1]

def singletonPatternStates : List Int := [0, 1]

def coefficientVectors : Nat → List (List Int)
  | 0 => [[]]
  | n + 1 =>
      (coefficientVectors n).flatMap fun tail =>
        pairCoefficientValues.map fun value => value :: tail

def halfVectors : List (List Int) :=
  (coefficientVectors 7).flatMap fun pairs =>
    singletonCoefficientValues.map fun singleton => pairs ++ [singleton]

def dotInt : List Int → List Int → Int
  | coefficient :: coefficients, weight :: weights =>
      coefficient * weight + dotInt coefficients weights
  | _, _ => 0

def modP (value : Int) : Nat :=
  Int.toNat (value % (fieldPrime : Int))

def dotResidue (coefficients weights : List Int) : Nat :=
  modP (dotInt coefficients weights)

def leftWeights : List Int := pairWeights.take 7 ++ [singletonWeights.getD 0 0]

def rightWeights : List Int := pairWeights.drop 7 ++ [singletonWeights.getD 1 0]

def leftHalfResidues : List Nat :=
  halfVectors.map fun coefficients => dotResidue coefficients leftWeights

def rightNegativeHalfResidues : List Nat :=
  halfVectors.map fun coefficients => modP (-dotInt coefficients rightWeights)

def natLE (left right : Nat) : Bool := decide (left ≤ right)

def sortNats (values : List Nat) : List Nat :=
  List.mergeSort values natLE

def strictlyIncreasing : List Nat → Bool
  | [] => true
  | [_] => true
  | first :: second :: rest =>
      decide (first < second) && strictlyIncreasing (second :: rest)

def sortedIntersectionAux : Nat → List Nat → List Nat → List Nat
  | 0, _, _ => []
  | Nat.succ fuel, [], _ => []
  | Nat.succ fuel, _, [] => []
  | Nat.succ fuel, left :: lefts, right :: rights =>
      if left < right then
        sortedIntersectionAux fuel lefts (right :: rights)
      else if right < left then
        sortedIntersectionAux fuel (left :: lefts) rights
      else
        left :: sortedIntersectionAux fuel lefts rights

def sortedIntersection (left right : List Nat) : List Nat :=
  sortedIntersectionAux (left.length + right.length + 1) left right

def canonicalRelations : List (List Int) :=
  [ [-2, 1, 0, 2, -1, 0, 0, 2, 0, -1, -2, 0, 2, -2, 0, -1]
  , [-2, 2, -2, 0, 0, 0, 2, 1, 0, 2, -1, 0, -2, -1, 1, -1]
  , [-1, -2, -1, 2, 1, -2, 0, -2, -1, -1, 0, -1, -2, -1, 0, 0]
  , [-1, -1, -1, 0, -1, -1, 2, 1, -2, 1, 1, 0, 0, 2, -1, -1]
  , [-1, -1, -1, 1, -2, 2, 1, -1, 1, 1, -1, -2, 2, -2, 0, -1]
  , [-1, 0, 0, 0, 1, 0, 0, 1, -2, 0, 1, -2, -1, -2, 0, 1]
  , [-1, 1, 1, 2, -2, 0, -2, 2, 1, -2, 2, 0, 0, 1, 0, -1]
  , [-1, 2, -2, 1, 0, -2, -2, 2, 2, 2, -1, -1, 2, -1, 0, 1]
  , [0, -1, 2, 0, 2, 0, -2, -2, 0, 2, 2, 1, 1, 0, 1, -1]
  ]

def negateRelation (relation : List Int) : List Int :=
  relation.map fun value => -value

def zeroRelation : List Int := List.replicate 16 0

def leftPart (relation : List Int) : List Int :=
  relation.take 7 ++ [relation.getD 14 0]

def signedRelations : List (List Int) :=
  canonicalRelations ++ canonicalRelations.map negateRelation

def expectedIntersectionResidues : List Nat :=
  sortNats ((zeroRelation :: signedRelations).map fun relation =>
    dotResidue (leftPart relation) leftWeights)

def validRightStates (index : Nat) (delta : Int) : List Int :=
  let states := if index < 14 then pairPatternStates else singletonPatternStates
  states.filter fun right => states.contains (right + delta)

def patternPairsAux : Nat → List Int → List (List Int × List Int)
  | _, [] => [([], [])]
  | index, delta :: deltas =>
      (validRightStates index delta).flatMap fun right =>
        (patternPairsAux (index + 1) deltas).map fun pair =>
          ((right + delta) :: pair.1, right :: pair.2)

def patternPairs (relation : List Int) : List (List Int × List Int) :=
  patternPairsAux 0 relation

def allPatternPairs : List (List Int × List Int) :=
  canonicalRelations.flatMap patternPairs

def encodePattern (pattern : List Int) : Nat :=
  pattern.foldl (fun accumulator state =>
    accumulator * 3 + Int.toNat (state + 1)) 0

def endpointCodes : List Nat :=
  allPatternPairs.flatMap fun pair =>
    [encodePattern pair.1, encodePattern pair.2]

def fastBinomial (n k : Nat) : Nat :=
  (List.range k).foldl
    (fun value index => value * (n - index) / (index + 1))
    1

def patternWeight (pattern : List Int) (selectorSize : Nat) : Nat :=
  let pairPart := pattern.take 14
  let zeroCount := (pairPart.filter fun state => state == 0).length
  let nonzeroCount := 14 - zeroCount
  let singletonCount :=
    Int.toNat (pattern.getD 14 0) + Int.toNat (pattern.getD 15 0)
  let baseSize := nonzeroCount + singletonCount
  if selectorSize < baseSize then
    0
  else
    let remainder := selectorSize - baseSize
    if remainder % 2 = 1 then
      0
    else
      let doubledPairs := remainder / 2
      if doubledPairs ≤ zeroCount then fastBinomial zeroCount doubledPairs else 0

def collisionFiberMaximum : Nat :=
  allPatternPairs.foldl (fun current pair =>
    (List.range 31).foldl (fun accumulator selectorSize =>
      max accumulator
        (patternWeight pair.1 selectorSize + patternWeight pair.2 selectorSize))
      current) 0

def binomialMaximumThroughFourteen : Nat :=
  (List.range 15).foldl (fun current n =>
    (List.range (n + 1)).foldl (fun accumulator k =>
      max accumulator (fastBinomial n k)) current) 0

def relationRealizationCounts : List Nat :=
  canonicalRelations.map fun relation => (patternPairs relation).length

structure AtlasSummary where
  leftHalfCount : Nat
  rightHalfCount : Nat
  leftHalfInjective : Bool
  rightHalfInjective : Bool
  intersectionResidues : List Nat
  signedNonzeroRelationCount : Nat
  canonicalRelationCount : Nat
  canonicalRelationsZero : Bool
  relationRealizationCounts : List Nat
  compressedEdgeCount : Nat
  compressedEndpointCount : Nat
  endpointsUnique : Bool
  collisionFiberMaximum : Nat
  binomialMaximumThroughFourteen : Nat
  selectorFiberMaximum : Nat
  deriving Repr, DecidableEq

def atlasSummary : AtlasSummary :=
  let leftSorted := sortNats leftHalfResidues
  let rightSorted := sortNats rightNegativeHalfResidues
  let intersections := sortedIntersection leftSorted rightSorted
  let edges := allPatternPairs
  let endpoints := endpointCodes
  { leftHalfCount := leftHalfResidues.length
  , rightHalfCount := rightNegativeHalfResidues.length
  , leftHalfInjective := strictlyIncreasing leftSorted
  , rightHalfInjective := strictlyIncreasing rightSorted
  , intersectionResidues := intersections
  , signedNonzeroRelationCount := intersections.length - 1
  , canonicalRelationCount := canonicalRelations.length
  , canonicalRelationsZero :=
      canonicalRelations.all fun relation => dotResidue relation fullWeights == 0
  , relationRealizationCounts := relationRealizationCounts
  , compressedEdgeCount := edges.length
  , compressedEndpointCount := endpoints.length
  , endpointsUnique := strictlyIncreasing (sortNats endpoints)
  , collisionFiberMaximum := collisionFiberMaximum
  , binomialMaximumThroughFourteen := binomialMaximumThroughFourteen
  , selectorFiberMaximum :=
      max collisionFiberMaximum binomialMaximumThroughFourteen
  }

def expectedAtlasSummary : AtlasSummary :=
  { leftHalfCount := 234375
  , rightHalfCount := 234375
  , leftHalfInjective := true
  , rightHalfInjective := true
  , intersectionResidues := expectedIntersectionResidues
  , signedNonzeroRelationCount := 18
  , canonicalRelationCount := 9
  , canonicalRelationsZero := true
  , relationRealizationCounts :=
      [3888, 1944, 4608, 6912, 1024, 46656, 1728, 192, 1944]
  , compressedEdgeCount := 68896
  , compressedEndpointCount := 137792
  , endpointsUnique := true
  , collisionFiberMaximum := 482
  , binomialMaximumThroughFourteen := 3432
  , selectorFiberMaximum := 3432
  }

theorem selector_relation_atlas_exact :
    atlasSummary = expectedAtlasSummary := by
  native_decide

#print axioms selector_relation_atlas_exact

end M31FlatnessKeystone.SelectorAtlas
