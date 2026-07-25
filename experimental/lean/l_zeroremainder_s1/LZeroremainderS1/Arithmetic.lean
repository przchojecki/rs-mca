import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Exact arithmetic for the zero-remainder rate-half list scale

The accompanying paper proves the cyclic quotient-rotation theorem at the
zero-remainder boundary `s = 0`, the full-quotient product-flatness law, and the
binomial coefficient estimates behind the certified bit interval.  This module
certifies the frozen row, the legality of the boundary specialization
`c = 1, s = 0`, the exact reason the predecessor's strict contract excluded that
scale, and every printed exponent and small-block certificate used in the
bit-length proofs.  It does not formalize finite fields, Reed--Solomon codes, or
the source locator construction.
-/

namespace LZeroremainderS1

abbrev q0 : Nat := 6597069766657
abbrev codeLength : Nat := 2199023255552
abbrev codeDimension : Nat := 1099511627776
abbrev agreement : Nat := 1116691496959
abbrev radiusNumerator : Nat := 1082331758593
abbrev radiusDenominator : Nat := 2199023255552

abbrev t34 : Nat := 17179869184

/-- The boundary specialization of the source theorem: `c = 1`, `s = 0`. -/
abbrev boundaryC : Nat := 1
abbrev boundaryN : Nat := 2199023255552
abbrev boundaryD : Nat := 17179869183
abbrev boundaryM : Nat := 1116691496959
abbrev boundaryS : Nat := 0

abbrev lowerBitExponent : Nat := 1466604010421
abbrev lowerBitEndpoint : Nat := 1466604010422
abbrev upperBitExponent : Nat := 1467447159515
abbrev upperBitEndpoint : Nat := 1467447159516

/-- Predecessor certified bit interval for the `c = 2` champion. -/
abbrev predecessorLowerEndpoint : Nat := 721554505735
abbrev predecessorUpperEndpoint : Nat := 738734374956

/-- Predecessor deterministic packing cap, carried unchanged. -/
abbrev packingCapBitEndpoint : Nat := 2095944040454

/-- The frozen row, its abbreviations, and the exact radius numerator. -/
theorem declared_row_exact :
    q0 = 3 * 2 ^ 41 + 1 ∧
    q0 = 768 * 2 ^ 33 + 1 ∧
    codeLength = 2 ^ 41 ∧
    codeDimension = 2 ^ 40 ∧
    t34 = 2 ^ 34 ∧
    agreement = codeDimension + t34 - 1 ∧
    codeLength = 128 * t34 ∧
    agreement = 65 * t34 - 1 ∧
    radiusNumerator = codeLength - agreement ∧
    radiusDenominator = codeLength := by
  native_decide

#print axioms LZeroremainderS1.declared_row_exact

/-- The row is strictly beyond the exact finite-field Johnson agreement. -/
theorem radius_and_johnson_exact :
    agreement ^ 2 < codeLength * (codeDimension - 1) ∧
    codeLength * (codeDimension - 1) - agreement ^ 2 =
      1170851739846527019909119 := by
  native_decide

#print axioms LZeroremainderS1.radius_and_johnson_exact

/--
Every elementary hypothesis of the zero-remainder quotient-rotation theorem
holds at the boundary specialization, and the frozen exact agreement is
reproduced.
-/
theorem zero_remainder_specialization_legal :
    boundaryC ∣ codeDimension ∧
    boundaryN = codeLength / boundaryC ∧
    1 ≤ boundaryD ∧
    boundaryD ≤ boundaryN / 2 - 1 ∧
    boundaryM = boundaryN / 2 + boundaryD ∧
    boundaryM = agreement ∧
    boundaryS = 0 ∧
    codeLength / 2 + boundaryD * boundaryC = agreement ∧
    boundaryD = t34 - 1 := by
  native_decide

#print axioms LZeroremainderS1.zero_remainder_specialization_legal

/--
The predecessor's strict legality predicate, reproduced verbatim from the
integrated positive-remainder contract `0 < s < c`.
-/
def strictLegalScaleAtAgreement (j : Nat) : Bool :=
  let c := 2 ^ j
  let N := codeLength / c
  let d := 2 ^ (34 - j) - 1
  let s := c - 1
  decide
    (c ∣ codeDimension ∧
      1 ≤ d ∧
      d ≤ N / 2 - 1 ∧
      0 < s ∧
      s < c ∧
      codeDimension + d * c + s = agreement)

/--
The exact reason the boundary scale was missing: at `j = 0` the strict predicate
is false, yet every one of its conjuncts other than `0 < s` holds there.  The
positive-remainder contract, not an arithmetic obstruction, excluded `c = 1`.
-/
theorem strict_contract_excludes_c_one_only_on_positivity :
    strictLegalScaleAtAgreement 0 = false ∧
    (2 ^ 0 ∣ codeDimension) ∧
    1 ≤ 2 ^ (34 - 0) - 1 ∧
    2 ^ (34 - 0) - 1 ≤ codeLength / 2 ^ 0 / 2 - 1 ∧
    (2 ^ 0 - 1 : Nat) < 2 ^ 0 ∧
    codeDimension + (2 ^ (34 - 0) - 1) * 2 ^ 0 + (2 ^ 0 - 1) = agreement ∧
    ¬ (0 < (2 ^ 0 - 1 : Nat)) := by
  native_decide

#print axioms LZeroremainderS1.strict_contract_excludes_c_one_only_on_positivity

/--
The predecessor census of thirty-three strictly legal dyadic scales is
unchanged: the boundary scale is added outside that contract, not inside it.
-/
theorem predecessor_census_unchanged :
    ((List.range 41).filter strictLegalScaleAtAgreement).length = 33 ∧
    ((List.range 41).filter strictLegalScaleAtAgreement) =
      (List.range 33).map (fun j => j + 1) ∧
    strictLegalScaleAtAgreement 0 = false := by
  native_decide

#print axioms LZeroremainderS1.predecessor_census_unchanged

/--
The full-quotient product coordinate is exactly flat at the boundary scale: the
subset size is coprime to the quotient order, which is the hypothesis of the
product-flatness law.
-/
theorem product_coordinate_coprime :
    Nat.gcd boundaryM boundaryN = 1 ∧
    boundaryM % 2 = 1 ∧
    boundaryN = 2 ^ 41 := by
  native_decide

#print axioms LZeroremainderS1.product_coordinate_coprime

/-- The ratio-block certificate behind the twenty-two step numerator estimate. -/
theorem ratio_block_certificate :
    2 * 63 ^ 22 > 65 ^ 22 := by
  native_decide

#print axioms LZeroremainderS1.ratio_block_certificate

/-- The exact certificates bounding `q0 ^ (T - 2)` from above. -/
theorem field_power_upper_certificate :
    q0 < 769 * 2 ^ 33 ∧
    2 ^ 19 * 769 ^ 46 < 1024 ^ 46 ∧
    t34 - 2 = 46 * 373475417 := by
  native_decide

#print axioms LZeroremainderS1.field_power_upper_certificate

/-- The exact certificates bounding `q0 ^ (T - 2)` from below. -/
theorem field_power_lower_certificate :
    q0 > 3 * 2 ^ 41 ∧
    2 ^ 5 * 3 ^ 12 > 4 ^ 12 := by
  native_decide

#print axioms LZeroremainderS1.field_power_lower_certificate

/-- The two exact ceiling divisions that fix the block counts. -/
theorem block_count_exact :
    (t34 - 1 + 21) / 22 = 780903145 ∧
    (t34 - 2 + 11) / 12 = 1431655766 := by
  native_decide

#print axioms LZeroremainderS1.block_count_exact

/-- The lower bit exponent, assembled from the printed block arithmetic. -/
theorem lower_bit_exponent_exact :
    85 * t34 + 3 + 19 * 373475417 - 780903145 = lowerBitExponent ∧
    lowerBitExponent + 1 = lowerBitEndpoint ∧
    128 * t34 - 42 - 780903145 - 41 - (43 * (t34 - 2) - 19 * 373475417) =
      lowerBitExponent := by
  native_decide

#print axioms LZeroremainderS1.lower_bit_exponent_exact

/-- The upper bit exponent, assembled from the printed block arithmetic. -/
theorem upper_bit_exponent_exact :
    85 * t34 + 45 + 5 * 1431655766 = upperBitExponent ∧
    upperBitExponent + 1 = upperBitEndpoint ∧
    128 * t34 - 41 - (43 * (t34 - 2) - 5 * 1431655766) = upperBitExponent := by
  native_decide

#print axioms LZeroremainderS1.upper_bit_exponent_exact

/-- The certified bit interval for the boundary lower bound is nonempty. -/
theorem certified_bit_interval_exact :
    lowerBitEndpoint = 1466604010422 ∧
    upperBitEndpoint = 1467447159516 ∧
    lowerBitEndpoint < upperBitEndpoint := by
  native_decide

#print axioms LZeroremainderS1.certified_bit_interval_exact

/--
The boundary lower bound is not a refinement inside the predecessor interval:
its certified minimum bit length strictly exceeds the predecessor maximum.
-/
theorem new_lower_exceeds_predecessor_interval :
    predecessorLowerEndpoint < predecessorUpperEndpoint ∧
    predecessorUpperEndpoint < lowerBitEndpoint := by
  native_decide

#print axioms LZeroremainderS1.new_lower_exceeds_predecessor_interval

end LZeroremainderS1
