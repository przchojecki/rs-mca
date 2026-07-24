import Std.Tactic

/-!
# Lane L: fixed-G ordinary RS endpoint arithmetic

Stdlib-only arithmetic shadow of
`experimental/notes/thresholds/m31_fixed_g_boundary_endpoint_plotkin_v1.md`.

The source note proves the coding-theory and constant-weight combinatorics.
This module checks the frozen parameters, exact finite-field Johnson grid,
Plotkin division, pullback arithmetic, and the adjacent-shell route stop.

No Mathlib. No `sorry`.
-/

namespace LFixedGEndpointPlotkin

def p : Nat := 2147483647
def boundaryLength : Nat := 981129
def slack : Nat := 67447
def exchangeDistance : Nat := slack + 1
def BStar : Nat := 16777215
def targetListBound : Nat := BStar - 1

def lowDimension : Nat := 5412
def lowAgreement : Nat := 72859
def lowErrors : Nat := 908270

def highDimension : Nat := 840823
def highAgreement : Nat := 908270
def highErrors : Nat := 72859

def endpointWeight : Nat := 72859
def shortenedLength : Nat := boundaryLength - 1
def shortenedWeight : Nat := endpointWeight - 1
def plotkinNumerator : Nat := exchangeDistance * shortenedLength
def plotkinDenominator : Nat :=
  plotkinNumerator - shortenedWeight * (shortenedLength - shortenedWeight)
def shortenedCap : Nat := 171578
def ordinaryListCap : Nat := 2310492
def fixedGBallCap : Nat := ordinaryListCap + 1

def johnsonEll : Nat := targetListBound

def finiteJohnsonLhs (a : Nat) : Nat :=
  (johnsonEll - 1) * (p * a - boundaryLength) ^ 2

def finiteJohnsonRhs (d : Nat) : Nat :=
  boundaryLength ^ 2 * (p - 1) ^ 2 * (johnsonEll - 1)
    - boundaryLength * (p - 1) * p * johnsonEll *
      (boundaryLength - (d - 1))

def ceilDiv (a b : Nat) : Nat := (a + b - 1) / b

def adjacentWeight : Nat := 72860
def adjacentTwoLength : Nat := boundaryLength - 2
def adjacentTwoWeight : Nat := adjacentWeight - 2
def adjacentTwoNumerator : Nat := exchangeDistance * adjacentTwoLength
def adjacentTwoDenominator : Nat :=
  adjacentTwoNumerator -
    adjacentTwoWeight * (adjacentTwoLength - adjacentTwoWeight)
def adjacentTwoCap : Nat := 169204
def adjacentRouteCap : Nat := 30682446

/-! ## Frozen endpoint parameters -/

theorem field_value : p = 2 ^ 31 - 1 := by native_decide

theorem low_row_partition :
    lowAgreement + lowErrors = boundaryLength := by native_decide

theorem high_row_partition :
    highAgreement + highErrors = boundaryLength := by native_decide

theorem low_slack_identity :
    lowAgreement = lowDimension + slack := by native_decide

theorem high_slack_identity :
    highAgreement = highDimension + slack := by native_decide

theorem endpoint_complement_symmetry :
    boundaryLength - lowAgreement = highAgreement ∧
    boundaryLength - highAgreement = lowAgreement := by
  native_decide

theorem exchange_distance_value :
    exchangeDistance = 67448 := by native_decide

/-! ## Limiting quadratic Johnson comparison -/

theorem low_classical_johnson_deficit :
    boundaryLength * (lowDimension - 1) - lowAgreement ^ 2 = 455138 := by
  native_decide

theorem high_classical_johnson_deficit :
    boundaryLength * (highDimension - 1) - highAgreement ^ 2 = 455138 := by
  native_decide

theorem low_classical_johnson_previous_deficit :
    boundaryLength * (lowDimension - 1) - 72862 ^ 2 = 17975 := by
  native_decide

theorem low_classical_johnson_boundary_margin :
    72863 ^ 2 - boundaryLength * (lowDimension - 1) = 127750 := by
  native_decide

theorem high_classical_johnson_boundary_margin :
    908271 ^ 2 - boundaryLength * (highDimension - 1) = 1361403 := by
  native_decide

/-! ## Exact finite-p, target-list Johnson grid -/

theorem low_finite_johnson_previous_deficit :
    finiteJohnsonRhs lowDimension - finiteJohnsonLhs 72861 =
      8221003905619924567540362320760 := by
  native_decide

theorem low_finite_johnson_boundary_margin :
    finiteJohnsonLhs 72862 - finiteJohnsonRhs lowDimension =
      3053765018644647902938550527393 := by
  native_decide

theorem low_finite_johnson_row_deficit :
    finiteJohnsonRhs lowDimension - finiteJohnsonLhs lowAgreement =
      30770077526717780184713611320764 := by
  native_decide

theorem high_finite_johnson_row_deficit :
    finiteJohnsonRhs highDimension - finiteJohnsonLhs highAgreement =
      34579558183296310721328734410451 := by
  native_decide

theorem high_finite_johnson_boundary_margin :
    finiteJohnsonLhs 908271 - finiteJohnsonRhs highDimension =
      105968468789629159598961272090208 := by
  native_decide

theorem low_exact_johnson_errors :
    boundaryLength - 72862 = 908267 := by native_decide

theorem high_exact_johnson_errors :
    boundaryLength - 908271 = 72858 := by native_decide

theorem low_post_johnson_gap :
    lowErrors - 908267 = 3 := by native_decide

theorem high_post_johnson_gap :
    highErrors - 72858 = 1 := by native_decide

/-! ## One-coordinate Plotkin specialization -/

theorem shortened_values :
    shortenedLength = 981128 ∧ shortenedWeight = 72858 ∧
    shortenedLength - shortenedWeight = 908270 := by
  native_decide

theorem plotkin_numerator_value :
    plotkinNumerator = 66175121344 := by native_decide

theorem plotkin_incidence_product :
    shortenedWeight * (shortenedLength - shortenedWeight) =
      66174735660 := by
  native_decide

theorem plotkin_denominator_value :
    plotkinDenominator = 385684 := by native_decide

theorem shortened_cap_division :
    plotkinNumerator / plotkinDenominator = shortenedCap := by
  native_decide

theorem shortened_cap_remainder :
    plotkinNumerator % plotkinDenominator = 231992 := by
  native_decide

theorem shortened_cap_of_cross {M : Nat}
    (h : M * plotkinDenominator ≤ plotkinNumerator) :
    M ≤ shortenedCap := by
  simp [plotkinDenominator, plotkinNumerator, shortenedLength,
    shortenedWeight, endpointWeight, boundaryLength, exchangeDistance,
    slack, shortenedCap] at h ⊢
  omega

theorem pullback_division :
    boundaryLength * shortenedCap / endpointWeight = ordinaryListCap := by
  native_decide

theorem pullback_remainder :
    boundaryLength * shortenedCap % endpointWeight = 14934 := by
  native_decide

theorem ordinary_cap_of_incidence {L M : Nat}
    (hIncidence : L * endpointWeight ≤ boundaryLength * M)
    (hShort : M ≤ shortenedCap) :
    L ≤ ordinaryListCap := by
  simp [endpointWeight, boundaryLength, shortenedCap, ordinaryListCap] at *
  omega

theorem endpoint_cap_of_plotkin_cross {L M : Nat}
    (hIncidence : L * endpointWeight ≤ boundaryLength * M)
    (hPlotkin : M * plotkinDenominator ≤ plotkinNumerator) :
    L ≤ ordinaryListCap :=
  ordinary_cap_of_incidence hIncidence (shortened_cap_of_cross hPlotkin)

theorem ordinary_cap_below_target :
    ordinaryListCap ≤ targetListBound := by native_decide

theorem ordinary_safety_margin :
    targetListBound - ordinaryListCap = 14466722 := by
  native_decide

theorem fixed_g_anchor_addback :
    fixedGBallCap = 2310493 := by native_decide

theorem fixed_g_ball_below_budget :
    fixedGBallCap ≤ BStar := by native_decide

theorem fixed_g_safety_margin :
    BStar - fixedGBallCap = 14466722 := by native_decide

/-! ## Adjacent-shell route stop -/

theorem adjacent_one_shortening_deficit :
    (adjacentWeight - 1) * (boundaryLength - adjacentWeight) -
      exchangeDistance * (boundaryLength - 1) = 449727 := by
  native_decide

theorem adjacent_two_values :
    adjacentTwoLength = 981127 ∧ adjacentTwoWeight = 72858 ∧
    adjacentTwoLength - adjacentTwoWeight = 908269 := by
  native_decide

theorem adjacent_two_numerator_value :
    adjacentTwoNumerator = 66175053896 := by native_decide

theorem adjacent_two_denominator_value :
    adjacentTwoDenominator = 391094 := by native_decide

theorem adjacent_two_cap_division :
    adjacentTwoNumerator / adjacentTwoDenominator = adjacentTwoCap := by
  native_decide

theorem adjacent_two_cap_remainder :
    adjacentTwoNumerator % adjacentTwoDenominator = 384720 := by
  native_decide

theorem adjacent_route_first_ceiling :
    ceilDiv (adjacentRouteCap * adjacentWeight) boundaryLength =
      2278521 := by
  native_decide

theorem adjacent_route_second_ceiling :
    ceilDiv (2278521 * (adjacentWeight - 1)) (boundaryLength - 1) =
      adjacentTwoCap := by
  native_decide

theorem adjacent_route_successor_first_ceiling :
    ceilDiv ((adjacentRouteCap + 1) * adjacentWeight) boundaryLength =
      2278522 := by
  native_decide

theorem adjacent_route_successor_second_ceiling :
    ceilDiv (2278522 * (adjacentWeight - 1)) (boundaryLength - 1) =
      adjacentTwoCap + 1 := by
  native_decide

theorem adjacent_route_exceeds_target :
    adjacentRouteCap - targetListBound = 13905232 := by
  native_decide

/-! ## Axiom census -/

#print axioms field_value
#print axioms low_row_partition
#print axioms high_row_partition
#print axioms low_slack_identity
#print axioms high_slack_identity
#print axioms endpoint_complement_symmetry
#print axioms exchange_distance_value
#print axioms low_classical_johnson_deficit
#print axioms high_classical_johnson_deficit
#print axioms low_classical_johnson_previous_deficit
#print axioms low_classical_johnson_boundary_margin
#print axioms high_classical_johnson_boundary_margin
#print axioms low_finite_johnson_previous_deficit
#print axioms low_finite_johnson_boundary_margin
#print axioms low_finite_johnson_row_deficit
#print axioms high_finite_johnson_row_deficit
#print axioms high_finite_johnson_boundary_margin
#print axioms low_exact_johnson_errors
#print axioms high_exact_johnson_errors
#print axioms low_post_johnson_gap
#print axioms high_post_johnson_gap
#print axioms shortened_values
#print axioms plotkin_numerator_value
#print axioms plotkin_incidence_product
#print axioms plotkin_denominator_value
#print axioms shortened_cap_division
#print axioms shortened_cap_remainder
#print axioms shortened_cap_of_cross
#print axioms pullback_division
#print axioms pullback_remainder
#print axioms ordinary_cap_of_incidence
#print axioms endpoint_cap_of_plotkin_cross
#print axioms ordinary_cap_below_target
#print axioms ordinary_safety_margin
#print axioms fixed_g_anchor_addback
#print axioms fixed_g_ball_below_budget
#print axioms fixed_g_safety_margin
#print axioms adjacent_one_shortening_deficit
#print axioms adjacent_two_values
#print axioms adjacent_two_numerator_value
#print axioms adjacent_two_denominator_value
#print axioms adjacent_two_cap_division
#print axioms adjacent_two_cap_remainder
#print axioms adjacent_route_first_ceiling
#print axioms adjacent_route_second_ceiling
#print axioms adjacent_route_successor_first_ceiling
#print axioms adjacent_route_successor_second_ceiling
#print axioms adjacent_route_exceeds_target

end LFixedGEndpointPlotkin
