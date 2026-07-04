import Std

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-!
# Exact eca/emca staircase finite anchors

This module records a stdlib-only Lean anchor for the committed
`(q,n,k) = (7,6,3)` exact worst-case `eca_C`/`emca_C` staircase certificate.
It deliberately proves only finite arithmetic facts that the Lean kernel can
check by enumeration:

* the recorded EMCA argmax pairs for radii `r = 0, 1, 2`;
* the finite-slope MCA-bad counts `1, 2, 7` for those recorded pairs;
* the `r = 1` ECA argmax pair is column-far by a finite search over all
  degree-`<3` Reed-Solomon words on every agreement-`5` support;
* the recorded `r = 1` ECA pair has exactly two finite CA-bad slopes;
* the printed sparsification numerators satisfy
  `max(eca_C,sigma_C) = emca_C` for the three radii.

The global worst-case statements remain typed bridges discharged by
`experimental/scripts/verify_exact_worstcase_eca_emca_staircase.py`; Lean does
not see the Python verifier's exhaustive iteration over all syndrome-class pair
representatives.
-/

namespace RsMca.EmcaStaircase

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

/-! ## Canonical affine `(7,6,3)` row -/

def domainAt : Nat → GF7
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | _ => 0

def indices6 : List Nat := [0, 1, 2, 3, 4, 5]
def finiteSlopes7 : List Nat := [0, 1, 2, 3, 4, 5, 6]

def gammaAt : Nat → GF7
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | _ => 0

def supportSize6 : List (List Nat) :=
  [[0, 1, 2, 3, 4, 5]]

def supportSize5 : List (List Nat) :=
  [[1, 2, 3, 4, 5],
   [0, 2, 3, 4, 5],
   [0, 1, 3, 4, 5],
   [0, 1, 2, 4, 5],
   [0, 1, 2, 3, 5],
   [0, 1, 2, 3, 4]]

def supportSize4 : List (List Nat) :=
  [[2, 3, 4, 5],
   [1, 3, 4, 5],
   [1, 2, 4, 5],
   [1, 2, 3, 5],
   [1, 2, 3, 4],
   [0, 3, 4, 5],
   [0, 2, 4, 5],
   [0, 2, 3, 5],
   [0, 2, 3, 4],
   [0, 1, 4, 5],
   [0, 1, 3, 5],
   [0, 1, 3, 4],
   [0, 1, 2, 5],
   [0, 1, 2, 4],
   [0, 1, 2, 3]]

def supportsForRadius : Nat → List (List Nat)
  | 0 => supportSize6
  | 1 => supportSize5
  | 2 => supportSize4
  | _ => []

def wordAt (eps1 eps2 : Nat → GF7) (gamma : GF7) (i : Nat) : GF7 :=
  eps1 i + gamma * eps2 i

def restrictsToCode (word : Nat → GF7) (support : List Nat) : Bool :=
  quadCoeffs7.any fun p =>
    support.all fun i => evalQuad p (domainAt i) == word i

def mcaBadSlope (eps1 eps2 : Nat → GF7) (r g : Nat) : Bool :=
  (supportsForRadius r).any fun support =>
    restrictsToCode (wordAt eps1 eps2 (gammaAt g)) support
      && !(restrictsToCode eps2 support)

def mcaBadSlopes (eps1 eps2 : Nat → GF7) (r : Nat) : List Nat :=
  finiteSlopes7.filter fun g => mcaBadSlope eps1 eps2 r g

/-! ## EMCA argmax pairs from the committed JSON certificate -/

def emcaR0Eps1 : Nat → GF7
  | _ => 0

def emcaR0Eps2 : Nat → GF7
  | 5 => 1
  | _ => 0

def emcaR1Eps1 : Nat → GF7
  | 5 => 1
  | _ => 0

def emcaR1Eps2 : Nat → GF7
  | 4 => 1
  | 5 => 1
  | _ => 0

def emcaR2Eps1 : Nat → GF7
  | 5 => 1
  | _ => 0

def emcaR2Eps2 : Nat → GF7
  | 4 => 1
  | _ => 0

/-! ## ECA argmax pair at `r = 1` -/

def ecaR1Eps1 : Nat → GF7
  | 5 => 1
  | _ => 0

def ecaR1Eps2 : Nat → GF7
  | 4 => 1
  | 5 => 1
  | _ => 0

def pairExplainedOn (eps1 eps2 : Nat → GF7) (support : List Nat) : Bool :=
  restrictsToCode eps1 support && restrictsToCode eps2 support

def pairFarAtRadius (eps1 eps2 : Nat → GF7) (r : Nat) : Bool :=
  !((supportsForRadius r).any fun support => pairExplainedOn eps1 eps2 support)

def caBadSlope (eps1 eps2 : Nat → GF7) (r g : Nat) : Bool :=
  pairFarAtRadius eps1 eps2 r
    && ((supportsForRadius r).any fun support =>
      restrictsToCode (wordAt eps1 eps2 (gammaAt g)) support)

def caBadSlopes (eps1 eps2 : Nat → GF7) (r : Nat) : List Nat :=
  finiteSlopes7.filter fun g => caBadSlope eps1 eps2 r g

def caBadSlopeGivenColumnFar (eps1 eps2 : Nat → GF7) (r g : Nat) : Bool :=
  (supportsForRadius r).any fun support =>
    restrictsToCode (wordAt eps1 eps2 (gammaAt g)) support

def caBadSlopesGivenColumnFar (eps1 eps2 : Nat → GF7) (r : Nat) : List Nat :=
  finiteSlopes7.filter fun g => caBadSlopeGivenColumnFar eps1 eps2 r g

/-! ## Kernel-checked finite anchors -/

theorem q763_degreeLt3_candidate_count : quadCoeffs7.length = 343 := by decide

theorem q763_emca_r0_bad_slopes :
    mcaBadSlopes emcaR0Eps1 emcaR0Eps2 0 = [0] := by decide

theorem q763_emca_r1_bad_slopes :
    mcaBadSlopes emcaR1Eps1 emcaR1Eps2 1 = [0, 6] := by decide

theorem q763_emca_r2_bad_slopes :
    mcaBadSlopes emcaR2Eps1 emcaR2Eps2 2 = [0, 1, 2, 3, 4, 5, 6] := by decide

theorem q763_emca_r0_numerator :
    (mcaBadSlopes emcaR0Eps1 emcaR0Eps2 0).length = 1 := by decide

theorem q763_emca_r1_numerator :
    (mcaBadSlopes emcaR1Eps1 emcaR1Eps2 1).length = 2 := by decide

theorem q763_emca_r2_numerator :
    (mcaBadSlopes emcaR2Eps1 emcaR2Eps2 2).length = 7 := by decide

theorem q763_eca_r1_column_far :
    pairFarAtRadius ecaR1Eps1 ecaR1Eps2 1 = true := by decide

theorem q763_eca_r1_bad_slopes_when_column_far :
    caBadSlopesGivenColumnFar ecaR1Eps1 ecaR1Eps2 1 = [0, 6] := by decide

theorem q763_eca_r1_numerator :
    (caBadSlopesGivenColumnFar ecaR1Eps1 ecaR1Eps2 1).length = 2 := by decide

theorem q763_sparsify_r0 :
    max 1 0 = 1 := by decide

theorem q763_sparsify_r1 :
    max 2 1 = 2 := by decide

theorem q763_sparsify_r2 :
    max 7 7 = 7 := by decide

/-! ## Typed bridges for the Python staircase obligations -/

def q763EmcaR0Eps1 : Nat → GF7 := emcaR0Eps1
def q763EmcaR0Eps2 : Nat → GF7 := emcaR0Eps2
def q763EmcaR1Eps1 : Nat → GF7 := emcaR1Eps1
def q763EmcaR1Eps2 : Nat → GF7 := emcaR1Eps2
def q763EmcaR2Eps1 : Nat → GF7 := emcaR2Eps1
def q763EmcaR2Eps2 : Nat → GF7 := emcaR2Eps2

/-- Bridge predicate for the verifier-backed worst-case EMCA staircase.

`PairClass e1 e2` is the syndrome-class representative predicate used by the
Python verifier, and `McaBadSlopeCount r e1 e2` is the finite-slope count under
the exact support-wise MCA definition.  The Python certificate supplies the
exhaustive check over all pair classes; Lean certifies only the displayed
argmax pairs above. -/
def EmcaStaircaseBridge
    (PairClass : (Nat → GF7) → (Nat → GF7) → Prop)
    (McaBadSlopeCount : Nat → (Nat → GF7) → (Nat → GF7) → Nat) : Prop :=
  PairClass q763EmcaR0Eps1 q763EmcaR0Eps2
    ∧ PairClass q763EmcaR1Eps1 q763EmcaR1Eps2
    ∧ PairClass q763EmcaR2Eps1 q763EmcaR2Eps2
    ∧ McaBadSlopeCount 0 q763EmcaR0Eps1 q763EmcaR0Eps2 = 1
    ∧ McaBadSlopeCount 1 q763EmcaR1Eps1 q763EmcaR1Eps2 = 2
    ∧ McaBadSlopeCount 2 q763EmcaR2Eps1 q763EmcaR2Eps2 = 7
    ∧ ∀ r e1 e2, r ≤ 2 → PairClass e1 e2 → McaBadSlopeCount r e1 e2 ≤
        match r with
        | 0 => 1
        | 1 => 2
        | 2 => 7
        | _ => 0

/-- Bridge predicate for the verifier-backed `eca_C` column-far side of the
staircase.  Lean checks the displayed `r=1` column-far argmax pair; the Python
verifier supplies the global maximization over pair classes and all radii. -/
def EcaStaircaseBridge
    (PairClass : (Nat → GF7) → (Nat → GF7) → Prop)
    (CaBadSlopeCount : Nat → (Nat → GF7) → (Nat → GF7) → Nat) : Prop :=
  PairClass ecaR1Eps1 ecaR1Eps2
    ∧ CaBadSlopeCount 1 ecaR1Eps1 ecaR1Eps2 = 2
    ∧ ∀ e1 e2, PairClass e1 e2 → CaBadSlopeCount 1 e1 e2 ≤ 2

end RsMca.EmcaStaircase
