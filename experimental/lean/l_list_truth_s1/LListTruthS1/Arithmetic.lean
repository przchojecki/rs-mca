import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Exact arithmetic for the declared rate-half ordinary-list bracket

The accompanying paper proves the Reed--Solomon interpolation packing theorem
and the binomial coefficient estimates.  This module certifies the frozen row,
the legal quotient-rotation scale census, the `c = 2` specialization, and every
printed exponent used in the symbolic bit-length bounds.  It does not formalize
finite fields, Reed--Solomon codes, or the source locator theorem.
-/

namespace LListTruthS1

abbrev q0 : Nat := 6597069766657
abbrev codeLength : Nat := 2199023255552
abbrev codeDimension : Nat := 1099511627776
abbrev agreement : Nat := 1116691496959
abbrev radiusNumerator : Nat := 1082331758593
abbrev radiusDenominator : Nat := 2199023255552

abbrev t33 : Nat := 8589934592
abbrev t34 : Nat := 17179869184

abbrev cTwo : Nat := 2
abbrev quotientSize : Nat := 1099511627776
abbrev rotationD : Nat := 8589934591
abbrev rotationM : Nat := 558345748479
abbrev rotationS : Nat := 1
abbrev rotationComplement : Nat := 541165879296
abbrev rotationCenter : Nat := 549755813887

abbrev rotationNumeratorLowerExponent : Nat := 1090921693144
abbrev rotationDenominatorUpperExponent : Nat := 369367187410
abbrev rotationLowerExponent : Nat := 721554505734
abbrev rotationNumeratorUpperExponent : Nat := 1099511627775
abbrev rotationDenominatorLowerExponent : Nat := 360777252820
abbrev rotationUpperExponent : Nat := 738734374955
abbrev rotationBitMin : Nat := 721554505735
abbrev rotationBitMax : Nat := 738734374956

abbrev packingComplement : Nat := 17179869183
abbrev packingExponent : Nat := 2095944040454

/-- The declared field, rate-half row, agreement, and radius integers are exact. -/
theorem declared_row_exact :
    q0 = 3 * (2 ^ 41) + 1 ∧
    codeLength = 2 ^ 41 ∧
    codeDimension = 2 ^ 40 ∧
    2 * codeDimension = codeLength ∧
    agreement = codeDimension + 2 ^ 34 - 1 ∧
    radiusNumerator = codeLength - agreement ∧
    radiusDenominator = codeLength ∧
    Nat.gcd radiusNumerator radiusDenominator = 1 := by
  native_decide

#print axioms LListTruthS1.declared_row_exact

/-- The row is strictly beyond the exact finite-field Johnson agreement. -/
theorem radius_and_johnson_exact :
    agreement ^ 2 < codeLength * (codeDimension - 1) ∧
    codeLength * (codeDimension - 1) - agreement ^ 2 =
      1170851739846527019909119 := by
  native_decide

#print axioms LListTruthS1.radius_and_johnson_exact

/-- Elementary legality predicate for a dyadic quotient scale `c = 2^j`. -/
def legalScaleAtAgreement (j : Nat) : Bool :=
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

/-- Legal exponents among all divisors `2^j` of `2^40`. -/
def legalScaleIndices : List Nat :=
  (List.range 41).filter legalScaleAtAgreement

/-- The expected interval `1,2,...,33`. -/
def expectedLegalScaleIndices : List Nat :=
  (List.range 33).map (fun j => j + 1)

/-- Exactly thirty-three quotient scales are legal at the frozen agreement. -/
theorem legal_scale_census_exact :
    legalScaleIndices = expectedLegalScaleIndices ∧
    legalScaleIndices.length = 33 := by
  native_decide

#print axioms LListTruthS1.legal_scale_census_exact

/--
The smallest legal quotient block, `c = 2`, satisfies every elementary
hypothesis of the integrated cyclic quotient-rotation theorem and preserves the
frozen exact agreement.
-/
theorem c_two_specialization_exact :
    t33 = 2 ^ 33 ∧
    cTwo = 2 ∧
    cTwo ∣ codeDimension ∧
    quotientSize = codeLength / cTwo ∧
    rotationD = t33 - 1 ∧
    1 ≤ rotationD ∧
    rotationD ≤ quotientSize / 2 - 1 ∧
    rotationM = quotientSize / 2 + rotationD ∧
    rotationS = cTwo - 1 ∧
    0 < rotationS ∧
    rotationS < cTwo ∧
    codeDimension + rotationD * cTwo + rotationS = agreement ∧
    rotationM + rotationComplement = quotientSize - 1 ∧
    rotationComplement = 63 * t33 ∧
    rotationCenter = 64 * t33 - 1 := by
  native_decide

#print axioms LListTruthS1.c_two_specialization_exact

/-- Exact power-of-two bracket used for the declared prime field. -/
theorem field_power_bracket_exact :
    2 ^ 42 < q0 ∧ q0 < 2 ^ 43 := by
  native_decide

#print axioms LListTruthS1.field_power_bracket_exact

/--
Exact exponents in the certified bit interval for the `c = 2` symbolic lower
bound.  The source proof supplies the binomial inequalities; this theorem checks
all exponent arithmetic and printed decimals.
-/
theorem rotation_bit_interval_exact :
    rotationNumeratorLowerExponent = 127 * t33 - 40 ∧
    rotationDenominatorUpperExponent = 43 * t33 - 46 ∧
    rotationLowerExponent =
      rotationNumeratorLowerExponent - rotationDenominatorUpperExponent ∧
    rotationLowerExponent = 84 * t33 + 6 ∧
    rotationLowerExponent = 721554505734 ∧
    rotationNumeratorUpperExponent = 128 * t33 - 1 ∧
    rotationDenominatorLowerExponent = 42 * t33 - 44 ∧
    rotationUpperExponent =
      rotationNumeratorUpperExponent - rotationDenominatorLowerExponent ∧
    rotationUpperExponent = 86 * t33 + 43 ∧
    rotationUpperExponent = 738734374955 ∧
    rotationBitMin = rotationLowerExponent + 1 ∧
    rotationBitMin = 721554505735 ∧
    rotationBitMax = rotationUpperExponent + 1 ∧
    rotationBitMax = 738734374956 := by
  native_decide

#print axioms LListTruthS1.rotation_bit_interval_exact

/--
The `c = 2` lower exponent exceeds the total-subset exponent available to every
other legal quotient scale by the printed positive margin.
-/
theorem quotient_scale_dominance_exact :
    rotationLowerExponent > 2 ^ 39 ∧
    rotationLowerExponent - 2 ^ 39 = 171798691846 ∧
    rotationLowerExponent - (2 ^ 39 - 1) = 171798691847 := by
  native_decide

#print axioms LListTruthS1.quotient_scale_dominance_exact

/--
Exact exponent in the bit-length certificate for the deterministic interpolation
packing cap.
-/
theorem packing_bit_cap_exact :
    t34 = 2 ^ 34 ∧
    codeLength = 128 * t34 ∧
    codeDimension = 64 * t34 ∧
    agreement = 65 * t34 - 1 ∧
    packingComplement = t34 - 1 ∧
    agreement = 65 * packingComplement + 64 ∧
    packingComplement > 0 ∧
    packingExponent = codeLength - 6 * packingComplement ∧
    packingExponent = 122 * t34 + 6 ∧
    packingExponent = 2095944040454 ∧
    rotationBitMin ≤ packingExponent := by
  native_decide

#print axioms LListTruthS1.packing_bit_cap_exact

end LListTruthS1
