import LRatehalfBracketS1.Arithmetic

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Arithmetic shadow of the exact 256-class subset-product spectrum

The source note proves the character-orthogonality formula.  This module checks
all binomial coefficients, character coefficients, residue-fiber values, total
mass, and the strict improvement at the printed integers.
-/

namespace LRatehalfBracketS1

abbrev baseSubsetCount : Nat :=
  2839611126271508546268984656777172227686073202135060380392524976909278609885

abbrev orderTwoBinomial : Nat :=
  11975573020964041433067793888190275875

abbrev oddProductFiber : Nat :=
  11092230961998080258863221315535829014445503027953220397756221760927612835

abbrev oddProductImprovement : Nat :=
  46779582113140786847921069875743265

abbrev oddRatioNumerator : Nat :=
  2218446192399616051772644263107165802889100605590644079551244352185522567

abbrev oddRatioDenominator : Nat :=
  2218446192399616051772644263107165802879744689168015922181660138210373914

/-- Character coefficients for orders `2,4,...,256`. -/
def nontrivialCharacterCoefficients : List Int :=
  [ -11975573020964041433067793888190275875
  , -916312070471295267
  , -300540195
  , -6435
  , -35
  , -3
  , 1
  , -1
  ]

abbrev v1ProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824067538309226683299
abbrev v2ProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824053220933130265251
abbrev v3ProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824053220933120873571
abbrev v4ProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824053220933120873171
abbrev v5ProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824053220933120873167
abbrev v6ProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824053220933120873166
abbrev v7ProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824053220933120873167
abbrev zeroProductFiber : Nat :=
  11092230961998080258863221315535829014351943863726938824053220933120873166

/-- Exact binomial and old ceiling arithmetic. -/
theorem integrated_floor_formula_exact :
    fastBinomial 255 129 = baseSubsetCount ∧
    baseSubsetCount % 256 = 221 ∧
    (baseSubsetCount + 255) / 256 = integratedFloor := by
  native_decide

#print axioms LRatehalfBracketS1.integrated_floor_formula_exact

/--
For an odd product exponent, character orthogonality leaves only the trivial and
order-two characters.  This theorem checks the resulting exact integer.
-/
theorem odd_product_fiber_arithmetic :
    fastBinomial 127 64 = orderTwoBinomial ∧
    (baseSubsetCount + orderTwoBinomial) % 256 = 0 ∧
    (baseSubsetCount + orderTwoBinomial) / 256 = oddProductFiber ∧
    oddProductFiber = integratedFloor + oddProductImprovement ∧
    oddProductFiber > integratedFloor := by
  native_decide

#print axioms LRatehalfBracketS1.odd_product_fiber_arithmetic

/-- The eight nontrivial character coefficients printed in the source proof. -/
theorem character_coefficients_exact :
    nontrivialCharacterCoefficients =
      [ -11975573020964041433067793888190275875
      , -916312070471295267
      , -300540195
      , -6435
      , -35
      , -3
      , 1
      , -1
      ] ∧
    fastBinomial 63 32 = 916312070471295267 ∧
    fastBinomial 31 16 = 300540195 ∧
    fastBinomial 15 8 = 6435 ∧
    fastBinomial 7 4 = 35 ∧
    fastBinomial 3 2 = 3 ∧
    fastBinomial 1 1 = 1 ∧
    fastBinomial 0 0 = 1 := by
  native_decide

#print axioms LRatehalfBracketS1.character_coefficients_exact

/-- The full printed residue spectrum has the correct total subset mass. -/
theorem product_spectrum_mass_exact :
    128 * oddProductFiber +
      64 * v1ProductFiber +
      32 * v2ProductFiber +
      16 * v3ProductFiber +
      8 * v4ProductFiber +
      4 * v5ProductFiber +
      2 * v6ProductFiber +
      v7ProductFiber +
      zeroProductFiber = baseSubsetCount := by
  native_decide

#print axioms LRatehalfBracketS1.product_spectrum_mass_exact

/-- The odd residue classes attain the maximum of the printed spectrum. -/
theorem odd_product_is_spectrum_max :
    v1ProductFiber ≤ oddProductFiber ∧
    v2ProductFiber ≤ oddProductFiber ∧
    v3ProductFiber ≤ oddProductFiber ∧
    v4ProductFiber ≤ oddProductFiber ∧
    v5ProductFiber ≤ oddProductFiber ∧
    v6ProductFiber ≤ oddProductFiber ∧
    v7ProductFiber ≤ oddProductFiber ∧
    zeroProductFiber ≤ oddProductFiber := by
  native_decide

#print axioms LRatehalfBracketS1.odd_product_is_spectrum_max

/-- Exact reduced ratio between the odd-fiber floor and the integrated floor. -/
theorem odd_product_ratio_exact :
    Nat.gcd oddRatioNumerator oddRatioDenominator = 1 ∧
    oddProductFiber * oddRatioDenominator =
      integratedFloor * oddRatioNumerator := by
  native_decide

#print axioms LRatehalfBracketS1.odd_product_ratio_exact

end LRatehalfBracketS1
