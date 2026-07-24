import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Deficiency-resolved complete-T32 selector spectrum

This module computes the rooted-shell spectrum of the thirty-block selector
atlas, with selector size restricted to at most fourteen as forced by
479-point supports.  It is a finite computation inside the complete-T32
selector mechanism.

The module is support-selector level only.  The deployed interpretation of this
spectrum is outside the scope of this package: no transport from deployed
supports to the selector atlas is asserted, and no off-remainder, received-word,
codeword, ray, slope, or list-row claim is made.
-/

namespace M31SelectorSpectrum.Atlas

/--
Multiplicative binomial coefficient on `Nat`.  Self-contained; no external
dependency.  Agrees with `Nat.choose` on all arguments used below.
-/
def fastBinomial (n k : Nat) : Nat :=
  (List.range k).foldl
    (fun value i => value * (n - i) / (i + 1))
    1

abbrev Pattern := List Int

private def pairPatternStates : List Int := [-1, 0, 1]
private def singletonPatternStates : List Int := [0, 1]

/-- The nine nonzero selector relations, one from each sign pair. -/
def canonicalRelations : List Pattern :=
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

private def validRightStates (index : Nat) (delta : Int) : List Int :=
  let states := if index < 14 then pairPatternStates else singletonPatternStates
  states.filter fun right => states.contains (right + delta)

private def patternPairsAux : Nat → Pattern → List (Pattern × Pattern)
  | _, [] => [([], [])]
  | index, delta :: deltas =>
      (validRightStates index delta).flatMap fun right =>
        (patternPairsAux (index + 1) deltas).map fun pair =>
          ((right + delta) :: pair.1, right :: pair.2)

private def patternPairs (relation : Pattern) : List (Pattern × Pattern) :=
  patternPairsAux 0 relation

/-- All 68,896 nontrivial compressed collision edges. -/
def allPatternPairs : List (Pattern × Pattern) :=
  canonicalRelations.flatMap patternPairs

private def choose (n k : Nat) : Nat := fastBinomial n k

private def pairPart (pattern : Pattern) : List Int := pattern.take 14
private def singletonPart (pattern : Pattern) : List Int := (pattern.drop 14).take 2

private def zeroPairCount (pattern : Pattern) : Nat :=
  ((pairPart pattern).filter fun state => state == 0).length

private def nonzeroPairCount (pattern : Pattern) : Nat :=
  ((pairPart pattern).filter fun state => !(state == 0)).length

private def singletonOneCount (pattern : Pattern) : Nat :=
  ((singletonPart pattern).filter fun state => state == 1).length

private def baseSelectorSize (pattern : Pattern) : Nat :=
  nonzeroPairCount pattern + singletonOneCount pattern

/-- Number of doubled zero-pairs at one fixed selector size, when feasible. -/
private def doubledPairCount? (pattern : Pattern) (selectorSize : Nat) : Option Nat :=
  let base := baseSelectorSize pattern
  if selectorSize < base then
    none
  else
    let remainder := selectorSize - base
    if remainder % 2 = 1 then
      none
    else
      let doubled := remainder / 2
      if doubled ≤ zeroPairCount pattern then some doubled else none

private def pairRows (left right : Pattern) : List (Int × Int) :=
  List.zip (pairPart left) (pairPart right)

private def countPairRows
    (left right : Pattern) (predicate : Int → Int → Bool) : Nat :=
  ((pairRows left right).filter fun row => predicate row.1 row.2).length

private def zeroZeroCount (left right : Pattern) : Nat :=
  countPairRows left right fun a b => (a == 0) && (b == 0)

private def zeroNonzeroCount (left right : Pattern) : Nat :=
  countPairRows left right fun a b => (a == 0) && !(b == 0)

private def nonzeroZeroCount (left right : Pattern) : Nat :=
  countPairRows left right fun a b => !(a == 0) && (b == 0)

private def oppositeNonzeroCount (left right : Pattern) : Nat :=
  countPairRows left right fun a b =>
    !(a == 0) && !(b == 0) && !(a == b)

private def singletonRemovedCount (left right : Pattern) : Nat :=
  ((List.zip (singletonPart left) (singletonPart right)).filter fun row =>
    (row.1 == 1) && (row.2 == 0)).length

/--
For one fixed anchor split, count partner-pattern selectors with the prescribed
block deficiency.  `a`, `b`, and `c` count partner-zero coordinates on which the
anchor selects respectively one, both, and neither block.
-/
private def crossCountForSplit
    (a b c fixedRemoved partnerDoubled blockDeficiency : Nat) : Nat :=
  (List.range (a + 1)).foldl (fun total x =>
    (List.range (b + 1)).foldl (fun subtotal y =>
      if x + y ≤ partnerDoubled then
        let z := partnerDoubled - x - y
        if z ≤ c then
          let removed := fixedRemoved + (a - x) + 2 * (b - y)
          if removed = blockDeficiency then
            subtotal + choose a x * choose b y * choose c z
          else
            subtotal
        else
          subtotal
      else
        subtotal) total) 0

/-- Maximum cross-pattern rooted count for one oriented compressed edge. -/
private def crossPatternRootedMaximum
    (anchorPattern partnerPattern : Pattern)
    (selectorSize blockDeficiency : Nat) : Nat :=
  match doubledPairCount? anchorPattern selectorSize,
      doubledPairCount? partnerPattern selectorSize with
  | some anchorDoubled, some partnerDoubled =>
      let n00 := zeroZeroCount anchorPattern partnerPattern
      let n0n := zeroNonzeroCount anchorPattern partnerPattern
      let nn0 := nonzeroZeroCount anchorPattern partnerPattern
      let opposite := oppositeNonzeroCount anchorPattern partnerPattern
      let singletonRemoved := singletonRemovedCount anchorPattern partnerPattern
      (List.range (n00 + 1)).foldl (fun best u =>
        if u ≤ anchorDoubled then
          let v := anchorDoubled - u
          if v ≤ n0n then
            max best (crossCountForSplit
              nn0 u (n00 - u) (opposite + v + singletonRemoved)
              partnerDoubled blockDeficiency)
          else
            best
        else
          best) 0
  | _, _ => 0

/-- Rooted count inside one compressed pattern. -/
private def samePatternRootedCount
    (pattern : Pattern) (selectorSize blockDeficiency : Nat) : Nat :=
  match doubledPairCount? pattern selectorSize with
  | none => 0
  | some doubled =>
      if blockDeficiency % 2 = 1 then
        0
      else
        let movedPairs := blockDeficiency / 2
        let zeroCount := zeroPairCount pattern
        if movedPairs ≤ doubled then
          if movedPairs ≤ zeroCount - doubled then
            choose doubled movedPairs * choose (zeroCount - doubled) movedPairs
          else
            0
        else
          0

private def orientedEdgeRootedCount
    (anchorPattern partnerPattern : Pattern)
    (selectorSize blockDeficiency : Nat) : Nat :=
  samePatternRootedCount anchorPattern selectorSize blockDeficiency +
    crossPatternRootedMaximum
      anchorPattern partnerPattern selectorSize blockDeficiency

/-- Maximum rooted count in a one-pattern selector fiber. -/
private def zeroRelationRootedMaximum (blockDeficiency : Nat) : Nat :=
  if blockDeficiency % 2 = 1 then
    0
  else
    let movedPairs := blockDeficiency / 2
    (List.range 15).foldl (fun best zeroCount =>
      (List.range (zeroCount + 1)).foldl (fun subtotal doubled =>
        let minimumSelectorSize := 14 - zeroCount + 2 * doubled
        if minimumSelectorSize ≤ 14 then
          if movedPairs ≤ doubled then
            if movedPairs ≤ zeroCount - doubled then
              max subtotal
                (choose doubled movedPairs *
                  choose (zeroCount - doubled) movedPairs)
            else
              subtotal
          else
            subtotal
        else
          subtotal) best) 0

/-- Maximum rooted count contributed by a nontrivial collision edge. -/
private def nontrivialEdgeRootedMaximum (blockDeficiency : Nat) : Nat :=
  allPatternPairs.foldl (fun best pair =>
    (List.range 15).foldl (fun subtotal selectorSize =>
      max subtotal (max
        (orientedEdgeRootedCount
          pair.1 pair.2 selectorSize blockDeficiency)
        (orientedEdgeRootedCount
          pair.2 pair.1 selectorSize blockDeficiency))) best) 0

/--
The complete selector-atlas rooted maximum at deficiency `32 * t`, with at most
fourteen complete T32 blocks in a 479-point support.
-/
def selectorRootedMaximum (blockDeficiency : Nat) : Nat :=
  max (zeroRelationRootedMaximum blockDeficiency)
    (nontrivialEdgeRootedMaximum blockDeficiency)

/-- Deficiency-resolved selector spectrum for `t=1,...,14`. -/
def computedBlockDeficiencySpectrum : List Nat :=
  (List.range 14).map fun index => selectorRootedMaximum (index + 1)

/-- The predicted spectrum, indexed by the number of exchanged T32 blocks. -/
def expectedBlockDeficiencySpectrum : List Nat :=
  [0, 49, 0, 441, 0, 1225, 60, 1225, 210, 441, 45, 49, 3, 1]

/--
Deficiency-resolved selector cap.  Nonmultiples of 32 have no same-remainder
selector exchange.  For multiples of 32, the finite spectrum is indexed by the
number of exchanged T32 blocks.
-/
def t32ResolvedShellCap (e : Nat) : Nat :=
  if e % 32 = 0 then
    expectedBlockDeficiencySpectrum.getD (e / 32 - 1) 0
  else
    0

/--
Closed finite computation.  In particular, the first nonzero off-64-lattice
same-remainder shell occurs at point deficiency `32 * 7 = 224`, with maximum 60.
-/
theorem selector_rooted_spectrum_exact :
    allPatternPairs.length = 68896 ∧
    computedBlockDeficiencySpectrum = expectedBlockDeficiencySpectrum := by
  native_decide

/-- The `e=224` prediction extracted from the full spectrum. -/
theorem selector_e224_prediction : selectorRootedMaximum 7 = 60 := by
  native_decide

#print axioms selector_rooted_spectrum_exact
#print axioms selector_e224_prediction

end M31SelectorSpectrum.Atlas
