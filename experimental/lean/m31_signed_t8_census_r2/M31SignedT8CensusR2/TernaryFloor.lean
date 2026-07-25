import M31SignedT8CensusR2.Lattice
import Std.Data.HashMap

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Exact meet-in-the-middle exclusion through ternary support seven

Every signed relation of support at most seven can be split into a signed
four-subset and a signed subset of size at most three, except that supports at
most three already occur in the small table.  The executable certificate below
enumerates every such signed partial vector.

The four-subset side is streamed as 557,845 subsets times 16 sign masks; the
8,925,520 records are never materialized at once.
-/

namespace M31SignedT8CensusR2.TernaryFloor

open M31SignedT8CensusR2.Data
open M31SignedT8CensusR2.Lattice

abbrev Key := Nat × Nat
abbrev SignedPartial := List Nat × Nat

def coordinateIndices : List Nat := List.range coordinateCount

def choose : Nat → List α → List (List α)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | k + 1, x :: xs =>
      (choose k xs).map (fun ys => x :: ys) ++ choose (k + 1) xs

def signIsPositive (bits position : Nat) : Bool :=
  (bits / (2 ^ position)) % 2 == 1

def signedAdd (total weight : Nat) (positive : Bool) : Nat :=
  if positive then
    (total + weight) % fieldPrime
  else
    (total + fieldPrime - weight) % fieldPrime

def partialKey (indices : List Nat) (bits : Nat) : Key :=
  (List.zip indices (List.range indices.length)).foldl (fun total entry =>
    let i := entry.1
    let position := entry.2
    let positive := signIsPositive bits position
    (signedAdd total.1 (weightAt i 0) positive,
     signedAdd total.2 (weightAt i 1) positive)) (0, 0)

def signedPartialsOfSize (k : Nat) : List SignedPartial :=
  (choose k coordinateIndices).flatMap fun indices =>
    (List.range (2 ^ k)).map fun bits => (indices, bits)

def smallPartials : List SignedPartial :=
  (List.range 4).flatMap signedPartialsOfSize

def smallKeyMap : Std.HashMap Key (List Nat) :=
  smallPartials.foldl (fun table candidate =>
    table.insert (partialKey candidate.1 candidate.2) candidate.1)
    (Std.HashMap.emptyWithCapacity 310249)

def negativeKey (key : Key) : Key :=
  ((fieldPrime - key.1) % fieldPrime,
   (fieldPrime - key.2) % fieldPrime)

def disjointBool (xs ys : List Nat) : Bool :=
  xs.all fun x => !(ys.contains x)

def fourSignedPartialSafe (indices : List Nat) (bits : Nat) : Bool :=
  let key := partialKey indices bits
  if key == (0, 0) then
    false
  else
    match smallKeyMap.get? (negativeKey key) with
    | none => true
    | some smallIndices => !(disjointBool indices smallIndices)

def fourSubsetSafe (indices : List Nat) : Bool :=
  (List.range 16).all fun bits => fourSignedPartialSafe indices bits

def allFourPartialsSafe : Bool :=
  (choose 4 coordinateIndices).all fourSubsetSafe

def expectedUnsignedSubsetCounts : List Nat :=
  [1, 62, 1891, 37820, 557845]

def computedUnsignedSubsetCounts : List Nat :=
  (List.range 5).map fun k => (choose k coordinateIndices).length

def expectedSignedPartialCounts : List Nat :=
  [1, 124, 7564, 302560, 8925520]

def computedSignedPartialCounts : List Nat :=
  (List.range 5).map fun k =>
    (choose k coordinateIndices).length * (2 ^ k)

theorem enumeration_domain_sizes_exact :
    computedUnsignedSubsetCounts = expectedUnsignedSubsetCounts ∧
    computedSignedPartialCounts = expectedSignedPartialCounts ∧
    smallPartials.length = 310249 ∧
    (choose 4 coordinateIndices).length * 16 = 8925520 ∧
    smallPartials.length + (choose 4 coordinateIndices).length * 16 = 9235769 := by
  native_decide

/--
`smallKeyMap.size = smallPartials.length` certifies that all 310,249 signed
partials of sizes zero through three have distinct two-equation keys.  In
particular, no nonempty such partial has key zero.
-/
theorem small_partial_keys_are_injective :
    smallKeyMap.size = smallPartials.length ∧
    smallKeyMap.size = 310249 ∧
    smallKeyMap.get? (0, 0) = some [] := by
  native_decide

/--
Exact MITM exhaustion.  For every one of the 8,925,520 signed four-subsets,
the key is nonzero and its negative is not represented by a disjoint signed
partial of size at most three.
-/
theorem no_ternary_relation_through_support_seven_certificate :
    allFourPartialsSafe = true := by
  native_decide

theorem split_sizes_cover_support_through_seven
    (m : Nat) (h : m ≤ 7) :
    m ≤ 3 ∨ (4 ≤ m ∧ m - 4 ≤ 3) := by
  omega

theorem certified_sector_deficiency_floor_arithmetic :
    8 * 8 = 64 ∧
    64 < 192 := by
  decide

#print axioms enumeration_domain_sizes_exact
#print axioms small_partial_keys_are_injective
#print axioms no_ternary_relation_through_support_seven_certificate
#print axioms split_sizes_cover_support_through_seven
#print axioms certified_sector_deficiency_floor_arithmetic

end M31SignedT8CensusR2.TernaryFloor
