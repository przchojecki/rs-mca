import M31SignedT8CensusR2.Collision
import M31SignedT8CensusR2.Reduction

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Census predicates and direct/reduced evidence

`directMomentCollisionBool` uses the deployed T8 roots.  The reduced census is
the intersection of the ternary cube with the explicit two-equation lattice
predicate `Lattice.latticeRowInt`.  The coordinatewise direct-to-reduced
certificate is `Data.moment_difference_table_exact`; summing that identity
against any selector is ordinary distributivity in `Z/pZ`.
-/

namespace M31SignedT8CensusR2.Census

open M31SignedT8CensusR2.Data
open M31SignedT8CensusR2.Lattice

def directMomentSum (row : List Int) (k : Nat) : Nat :=
  (List.zip row intactT16Classes).foldl (fun total entry =>
    (total + intResidue entry.1 * t8DifferenceMoment entry.2 k) % fieldPrime) 0

def directMomentCollisionBool (row : List Int) : Bool :=
  row.length == coordinateCount &&
  (List.range 32).all (fun j => directMomentSum row (j + 1) == 0)

def ternaryCubeBool (row : List Int) : Bool :=
  row.length == coordinateCount && ternaryBool row

def reducedSignedT8CensusBool (row : List Int) : Bool :=
  ternaryCubeBool row && latticeRowInt row

def latticeCubeIntersectionBool (row : List Int) : Bool :=
  ternaryCubeBool row && latticeRowInt row

theorem reduced_census_is_lattice_cube_intersection
    (row : List Int) :
    reducedSignedT8CensusBool row = latticeCubeIntersectionBool row := by
  rfl

theorem known_selector_direct_and_reduced :
    directMomentCollisionBool knownSelector = true ∧
    reducedSignedT8CensusBool knownSelector = true ∧
    directMomentSum knownSelector 8 = 0 ∧
    directMomentSum knownSelector 24 = 0 := by
  native_decide

/--
The two raw rows used in the reverse implication have invertible dyadic
coefficients.  These are explicit inverse certificates modulo `p`.
-/
theorem dyadic_row_inverse_certificates :
    (2048 * 1048576) % fieldPrime = 1 ∧
    (1024 * 2097152) % fieldPrime = 1 := by
  native_decide

#print axioms reduced_census_is_lattice_cube_intersection
#print axioms known_selector_direct_and_reduced
#print axioms dyadic_row_inverse_certificates

end M31SignedT8CensusR2.Census
