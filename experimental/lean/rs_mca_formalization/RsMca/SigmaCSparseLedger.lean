import Std

set_option maxRecDepth 10000

/-!
# sigma_C sparse-census finite anchors

This module records a stdlib-only Lean anchor for the committed
`(q,n,k,r) = (7,6,3,2)` sigma_C sparse-census row.  It deliberately proves only
finite arithmetic facts that the Lean kernel can check by enumeration:

* the recorded extremal sparse pair over `F_7`;
* the seven finite-slope witness sets from the Python certificate;
* for each witness set, the close degree-<3 Reed-Solomon word agrees with
  `eps1 + gamma eps2` on the recorded maximal witness set and has distance at
  most `r = 2`;
* `eps2|_S` is not the restriction of any degree-<3 codeword, by enumerating
  all `7^3 = 343` coefficient triples.

The global census statement remains a typed bridge discharged by
`experimental/scripts/verify_sigma_c_sparse_census.py` in the contribution note:
Lean does not see the Python verifier's exhaustive iteration over all sparse
pairs.
-/

namespace RsMca.SigmaC

abbrev GF7 := Fin 7

/-- Degree-<3 polynomial coefficients over `F_7`. -/
structure Quad where
  a0 : GF7
  a1 : GF7
  a2 : GF7
deriving DecidableEq, Repr

def elems7 : List GF7 := [0, 1, 2, 3, 4, 5, 6]

/-- The full `7^3` coefficient table for degree-<3 words. -/
def quadCoeffs7 : List Quad :=
  elems7.flatMap fun a0 =>
    elems7.flatMap fun a1 =>
      elems7.map fun a2 => { a0 := a0, a1 := a1, a2 := a2 }

def evalQuad (p : Quad) (x : GF7) : GF7 :=
  p.a0 + p.a1 * x + p.a2 * x * x

/-! ## The committed `(7,6,3,r=2)` sparse pair -/

def domainAt : Nat → GF7
  | 0 => 1
  | 1 => 3
  | 2 => 2
  | 3 => 6
  | 4 => 4
  | 5 => 5
  | _ => 0

def eps1At : Nat → GF7
  | 1 => 1
  | _ => 0

def eps2At : Nat → GF7
  | 0 => 1
  | 1 => 4
  | _ => 0

def gammaAt : Nat → GF7
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | _ => 0

def wordAt (gamma : GF7) (i : Nat) : GF7 :=
  eps1At i + gamma * eps2At i

/-! ## Recorded close codewords and maximal witness sets

The polynomial coefficient triples are decoded from the certificate's
`codeword_index` values under the verifier order
`itertools.product(range(7), repeat=3)`.
-/

def closePoly : Nat → Quad
  | 0 => { a0 := 0, a1 := 0, a2 := 0 }
  | 1 => { a0 := 1, a1 := 4, a2 := 3 }
  | 2 => { a0 := 3, a1 := 1, a2 := 5 }
  | 3 => { a0 := 1, a1 := 1, a2 := 1 }
  | 4 => { a0 := 2, a1 := 4, a2 := 5 }
  | 5 => { a0 := 0, a1 := 0, a2 := 0 }
  | 6 => { a0 := 1, a1 := 0, a2 := 5 }
  | _ => { a0 := 0, a1 := 0, a2 := 0 }

def witnessSet : Nat → List Nat
  | 0 => [0, 2, 3, 4, 5]
  | 1 => [0, 1, 2, 3]
  | 2 => [0, 1, 3, 5]
  | 3 => [0, 1, 2, 4]
  | 4 => [0, 1, 4, 5]
  | 5 => [1, 2, 3, 4, 5]
  | 6 => [0, 1, 2, 5]
  | _ => []

def indices6 : List Nat := [0, 1, 2, 3, 4, 5]

def wordMatchesCloseCodeword (g : Nat) : Bool :=
  (witnessSet g).all fun i =>
    wordAt (gammaAt g) i == evalQuad (closePoly g) (domainAt i)

def mismatchCount (g : Nat) : Nat :=
  (indices6.filter fun i =>
    !(wordAt (gammaAt g) i == evalQuad (closePoly g) (domainAt i))).length

def maximalWitnessSetRecorded (g : Nat) : Bool :=
  witnessSet g
    == indices6.filter fun i =>
      wordAt (gammaAt g) i == evalQuad (closePoly g) (domainAt i)

def closeWithinRadius2 (g : Nat) : Bool :=
  decide (mismatchCount g <= 2)

def supportRestrictsToCode (support : List Nat) : Bool :=
  quadCoeffs7.any fun p =>
    support.all fun i => evalQuad p (domainAt i) == eps2At i

def slopeWitnessFails (g : Nat) : Bool :=
  maximalWitnessSetRecorded g
    && wordMatchesCloseCodeword g
    && closeWithinRadius2 g
    && !(supportRestrictsToCode (witnessSet g))

def finiteSlopes7 : List Nat := [0, 1, 2, 3, 4, 5, 6]

def saturatedSlopeCount : Nat :=
  (finiteSlopes7.filter slopeWitnessFails).length

def tangentLowerBoundSlopes : List Nat := [0, 5]

/-! ## Kernel-checked finite anchors -/

theorem q763_degreeLt3_candidate_count : quadCoeffs7.length = 343 := by decide

theorem q763_gamma0_witness : slopeWitnessFails 0 = true := by decide
theorem q763_gamma1_witness : slopeWitnessFails 1 = true := by decide
theorem q763_gamma2_witness : slopeWitnessFails 2 = true := by decide
theorem q763_gamma3_witness : slopeWitnessFails 3 = true := by decide
theorem q763_gamma4_witness : slopeWitnessFails 4 = true := by decide
theorem q763_gamma5_witness : slopeWitnessFails 5 = true := by decide
theorem q763_gamma6_witness : slopeWitnessFails 6 = true := by decide

theorem q763_all_finite_slopes_bad :
    finiteSlopes7.all slopeWitnessFails = true := by decide

/-- The row has two constructive tangent-ratio slopes, giving the expected
`sigma_C >= r` lower-bound witness at `r = 2`. -/
theorem q763_tangent_lower_bound :
    tangentLowerBoundSlopes.length = 2
      ∧ tangentLowerBoundSlopes.all slopeWitnessFails = true := by decide

/-- For this recorded sparse pair, all seven finite `F_7` slopes are bad. -/
theorem q763_pair_saturates_finite_slopes :
    saturatedSlopeCount = 7 := by decide

/-! ## Typed bridges for the Python census obligations -/

def q763Eps1 : Nat → GF7 := eps1At
def q763Eps2 : Nat → GF7 := eps2At

/-- Bridge predicate for the verifier-backed global census statement.

`SparsePair e1 e2` is the RS/MCA sparse-support condition, and
`BadSlopeCount e1 e2` is the finite-slope count under the maximal-witness
definition from `towards-prize.tex`.  The Python certificate supplies the
exhaustive check over all sparse pairs; Lean certifies only the displayed
extremal pair above. -/
def SigmaCSparseCensusBridge
    (SparsePair : (Nat → GF7) → (Nat → GF7) → Prop)
    (BadSlopeCount : (Nat → GF7) → (Nat → GF7) → Nat) : Prop :=
  SparsePair q763Eps1 q763Eps2
    ∧ BadSlopeCount q763Eps1 q763Eps2 = 7
    ∧ ∀ e1 e2, SparsePair e1 e2 → BadSlopeCount e1 e2 ≤ 7

/-- Bridge predicate for the trivial-regime equality used as a verifier guard.
The Python verifier checks this over finite RS rows; this package only records
the boundary as a typed obligation. -/
def SigmaCTrivialRegimeBridge
    (SigmaAtRadius : Nat → Nat) : Prop :=
  ∀ r : Nat, 2 * r ≤ 3 → SigmaAtRadius r = r

end RsMca.SigmaC
