import LZeroremainderS1.Arithmetic

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Exact arithmetic for the pairwise-intersection obstruction

The accompanying paper proves the greedy packing existence theorem, the
factorial bound `r ! ≥ (r / 3) ^ r`, and the monotonicity of the conflict terms.
This module certifies the exact rewritings of `a / (T - 1)` and
`(n - a) / (T - 1)`, the power-of-two domination of the resulting constants,
every printed exponent of the conflict volume and of the packing floor, and the
position of the obstruction inside the new bracket.
-/

namespace LZeroremainderS1

/-- The greedy block excess `r = T - 1 = a - k`. -/
abbrev packingR : Nat := 17179869183

abbrev conflictVolumeExponent : Nat := 274877906962
abbrev obstructionExponent : Nat := 1923364445403
abbrev obstructionBitEndpoint : Nat := 1923364445404

/--
The exact rewritings behind the two binomial estimates, and the power-of-two
domination of the constants `3 * 66` and `3 * 64` they produce.
-/
theorem packing_constants_exact :
    packingR = t34 - 1 ∧
    packingR = agreement - codeDimension ∧
    agreement = 65 * packingR + 64 ∧
    codeLength - agreement = 63 * packingR + 64 ∧
    agreement < 66 * packingR ∧
    codeLength - agreement < 64 * packingR ∧
    3 * 66 = 198 ∧
    198 < 256 ∧
    3 * 64 = 192 ∧
    192 < 256 ∧
    256 = 2 ^ 8 := by
  native_decide

#print axioms LZeroremainderS1.packing_constants_exact

/--
The conflict-volume exponent, both as printed and as assembled from the factor
`T` and the two `2 ^ (8 * r)` binomial bounds.
-/
theorem conflict_volume_exponent_exact :
    16 * t34 + 18 = conflictVolumeExponent ∧
    34 + 8 * packingR + 8 * packingR = conflictVolumeExponent ∧
    t34 = 2 ^ 34 := by
  native_decide

#print axioms LZeroremainderS1.conflict_volume_exponent_exact

/--
The obstruction exponent, both as printed and as the numerator lower exponent
minus the conflict-volume upper exponent.
-/
theorem obstruction_exponent_exact :
    112 * t34 - 60 - 780903145 = obstructionExponent ∧
    128 * t34 - 42 - 780903145 - conflictVolumeExponent = obstructionExponent ∧
    obstructionExponent + 1 = obstructionBitEndpoint := by
  native_decide

#print axioms LZeroremainderS1.obstruction_exponent_exact

/--
The route cut in exact position: the packing obstruction lies strictly above the
new certified lower endpoint and strictly below the deterministic packing cap.
No upper argument restricted to agreement-set sizes and pairwise intersections
can therefore close the bracket.
-/
theorem route_cut_position_exact :
    lowerBitEndpoint < obstructionBitEndpoint ∧
    obstructionBitEndpoint < packingCapBitEndpoint ∧
    upperBitEndpoint < obstructionBitEndpoint := by
  native_decide

#print axioms LZeroremainderS1.route_cut_position_exact

/-- The new bracket is nonvacuous, and its endpoint ratio is below `143 / 100`. -/
theorem bracket_ratio_certificate :
    lowerBitEndpoint < packingCapBitEndpoint ∧
    100 * packingCapBitEndpoint < 143 * lowerBitEndpoint := by
  native_decide

#print axioms LZeroremainderS1.bracket_ratio_certificate

/--
The predecessor bracket ratio exceeded `143 / 100` at both predecessor
endpoints, so the narrowing is a property of the added boundary scale and not of
the cap.
-/
theorem predecessor_ratio_exceeded_the_new_one :
    143 * predecessorLowerEndpoint < 100 * packingCapBitEndpoint ∧
    143 * predecessorUpperEndpoint < 100 * packingCapBitEndpoint := by
  native_decide

#print axioms LZeroremainderS1.predecessor_ratio_exceeded_the_new_one

end LZeroremainderS1
