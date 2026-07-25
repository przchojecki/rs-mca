import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Exact arithmetic for the rate-half ordinary-list lower packet

This module certifies only the frozen integers and the specialization gates used
with the already integrated cyclic quotient-rotation theorem.  It does not
formalize finite fields, Reed--Solomon codes, or the theorem's locator proof.
-/

namespace LRatehalfBracketS1

/-- Multiplicative binomial coefficient, self-contained and stdlib-only. -/
def fastBinomial (n k : Nat) : Nat :=
  (List.range k).foldl
    (fun value i => value * (n - i) / (i + 1))
    1

abbrev q0 : Nat := 6597069766657
abbrev codeLength : Nat := 2199023255552
abbrev codeDimension : Nat := 1099511627776
abbrev agreement : Nat := 1116691496959
abbrev radiusNumerator : Nat := 1082331758593
abbrev radiusDenominator : Nat := 2199023255552

abbrev integratedFloor : Nat :=
  11092230961998080258863221315535829014398723445840079610908300691051869570

abbrev c32 : Nat := 4294967296
abbrev quotientSize512 : Nat := 512
abbrev d3 : Nat := 3
abbrev m259 : Nat := 259
abbrev s32 : Nat := 4294967295

abbrev alternateBinomialPrinted : Nat :=
  225456433407227622163483597843439619508493793232120672594634608050001706637890080324384766467272782434839065859827588447117318678944033170766566666570205

abbrev alternateDenominator : Nat :=
  22282920707143600347625292288

abbrev alternateLower : Nat :=
  10117903140720209347161374303886548269936958556723901042315597656335386755181744190072527742895613796941873719315303119609998

abbrev alternateImprovement : Nat :=
  10117903140720209347161374303886548269936958556723889950084635658255127891960428654243513344172167956862262811014612067740428

abbrev alternateRatioNumerator : Nat :=
  722707367194300667654383878849039162138354182623135788736828404023956196798696013576609124492543842638705265665378794257857

abbrev alternateRatioDenominator : Nat :=
  792302211571291447061658665395416358171337388988577115064878620789419255

/-- The printed row, field, rate, and agreement integers are exact. -/
theorem declared_row_exact :
    q0 = 3 * (2 ^ 41) + 1 ∧
    codeLength = 2 ^ 41 ∧
    codeDimension = 2 ^ 40 ∧
    2 * codeDimension = codeLength ∧
    agreement = codeDimension + 2 ^ 34 - 1 := by
  native_decide

#print axioms LRatehalfBracketS1.declared_row_exact

/-- The radius fraction is reduced and the row is strictly post-Johnson. -/
theorem radius_and_johnson_exact :
    radiusNumerator = codeLength - agreement ∧
    radiusDenominator = codeLength ∧
    Nat.gcd radiusNumerator radiusDenominator = 1 ∧
    agreement ^ 2 < codeLength * (codeDimension - 1) ∧
    codeLength * (codeDimension - 1) - agreement ^ 2 =
      1170851739846527019909119 := by
  native_decide

#print axioms LRatehalfBracketS1.radius_and_johnson_exact

/--
The alternate quotient-rotation parameters satisfy every elementary hypothesis
of the integrated theorem and preserve the declared exact agreement.
-/
theorem alternate_parameters_exact :
    c32 = 2 ^ 32 ∧
    c32 ∣ codeDimension ∧
    quotientSize512 = codeLength / c32 ∧
    d3 = 3 ∧
    1 ≤ d3 ∧
    d3 ≤ quotientSize512 / 2 - 1 ∧
    m259 = quotientSize512 / 2 + d3 ∧
    s32 = c32 - 1 ∧
    0 < s32 ∧
    s32 < c32 ∧
    codeDimension + d3 * c32 + s32 = agreement := by
  native_decide

#print axioms LRatehalfBracketS1.alternate_parameters_exact

/-- Exact numerator `C(511,259)` for the alternate specialization. -/
theorem alternate_binomial_exact :
    fastBinomial 511 259 = alternateBinomialPrinted := by
  native_decide

#print axioms LRatehalfBracketS1.alternate_binomial_exact

/-- Exact denominator and ceiling for `ceil(C(511,259)/(512*q0^2))`. -/
theorem alternate_lower_exact :
    alternateDenominator = quotientSize512 * q0 ^ 2 ∧
    (alternateBinomialPrinted + alternateDenominator - 1) /
        alternateDenominator = alternateLower ∧
    alternateLower * alternateDenominator - alternateBinomialPrinted =
      13270828466727777212650525219 := by
  native_decide

#print axioms LRatehalfBracketS1.alternate_lower_exact

/-- The alternate list floor is strictly larger than the integrated floor. -/
theorem alternate_strict_improvement :
    alternateLower > integratedFloor ∧
    alternateLower = integratedFloor + alternateImprovement ∧
    alternateLower / integratedFloor > 2 ^ 169 := by
  native_decide

#print axioms LRatehalfBracketS1.alternate_strict_improvement

/-- Exact reduced ratio between the alternate and integrated list floors. -/
theorem alternate_ratio_exact :
    Nat.gcd alternateRatioNumerator alternateRatioDenominator = 1 ∧
    alternateLower * alternateRatioDenominator =
      integratedFloor * alternateRatioNumerator := by
  native_decide

#print axioms LRatehalfBracketS1.alternate_ratio_exact

end LRatehalfBracketS1
