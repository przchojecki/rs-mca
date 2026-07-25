import LInteriorPayS1.CriticalGap

/-!
# Literal all-depth extension of the incidence--Plotkin stop

`CriticalGap.lean` proves the nontrivial residual-weight range. This module
extends the same scalar obstruction through every possible common-coordinate
shortening depth `t ≤ 72,860`. For `t > 5,412` the remaining support weight is
smaller than the required exchange distance, but even a singleton terminal
section pulls back far above the target.
-/

namespace LInteriorPayS1

/-- Every reverse incidence ratio is at least thirteen until all selected
support coordinates have been deleted. -/
theorem coordinate_ratio_at_least_thirteen_all_depth
    (j : Nat) (hj : j ≤ 72859) :
    13 * (supportWeight - j) ≤ boundaryLength - j := by
  simp [supportWeight, boundaryLength]
  omega

theorem pullStep_ge_thirteen_all_depth
    (j x : Nat) (hj : j ≤ 72859) :
    13 * x ≤ pullStep j x := by
  have hden : 0 < supportWeight - j := by
    simp [supportWeight]
    omega
  apply (Nat.le_div_iff_mul_le hden).2
  calc
    13 * x * (supportWeight - j) =
        x * (13 * (supportWeight - j)) := by ac_rfl
    _ ≤ x * (boundaryLength - j) :=
      Nat.mul_le_mul_left x
        (coordinate_ratio_at_least_thirteen_all_depth j hj)

theorem pullback_ge_pow_thirteen_all_depth
    (t x : Nat) (ht : t ≤ supportWeight) :
    13 ^ t * x ≤ pullback t x := by
  induction t generalizing x with
  | zero => simp [pullback]
  | succ t ih =>
      have htj : t ≤ 72859 := by
        simp [supportWeight] at ht
        omega
      have hstep : 13 * x ≤ pullStep t x :=
        pullStep_ge_thirteen_all_depth t x htj
      have hrec : 13 ^ t * pullStep t x ≤ pullback t (pullStep t x) :=
        ih (pullStep t x) (by omega)
      calc
        13 ^ (t + 1) * x = 13 ^ t * (13 * x) := by
          simp [Nat.pow_succ, Nat.mul_assoc]
        _ ≤ 13 ^ t * pullStep t x := Nat.mul_le_mul_left (13 ^ t) hstep
        _ ≤ pullback t (pullStep t x) := hrec
        _ = pullback (t + 1) x := by rfl

/-- Positivity and numerator domination of the terminal Plotkin denominator at
all possible shortening depths after the first positive case. -/
theorem positive_plotkin_denominator_bounds_all_depth
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ supportWeight) :
    0 < plotkinPositiveDenominator t ∧
    plotkinPositiveDenominator t ≤ plotkinNumerator t := by
  simp [plotkinPositiveDenominator, plotkinNumerator,
    exchangeDistance, slack, boundaryLength, supportWeight] at *
  omega

theorem plotkinCap_positive_all_depth
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ supportWeight) :
    1 ≤ plotkinCap t := by
  have hbounds := positive_plotkin_denominator_bounds_all_depth t h2 ht
  unfold plotkinCap
  apply (Nat.le_div_iff_mul_le hbounds.1).2
  simpa using hbounds.2

theorem large_shortening_route_cap_all_depth
    (t : Nat) (h7 : 7 ≤ t) (ht : t ≤ supportWeight) :
    62748517 ≤ shorteningPlotkinRouteCap t := by
  have hpull := pullback_ge_pow_thirteen_all_depth t (plotkinCap t) ht
  have hcap := plotkinCap_positive_all_depth t (by omega) ht
  have hpow : 13 ^ 7 ≤ 13 ^ t := Nat.pow_le_pow_right (by decide) h7
  calc
    62748517 = 13 ^ 7 := by native_decide
    _ ≤ 13 ^ t := hpow
    _ = 13 ^ t * 1 := by simp
    _ ≤ 13 ^ t * plotkinCap t := Nat.mul_le_mul_left (13 ^ t) hcap
    _ ≤ pullback t (plotkinCap t) := hpull
    _ = shorteningPlotkinRouteCap t := by rfl

/-- Literal all-depth route minimum, including the automatically-singleton
residual range `t > supportWeight - exchangeDistance`. -/
theorem two_shortening_is_route_minimum_all_depth
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ supportWeight) :
    shorteningPlotkinRouteCap 2 ≤ shorteningPlotkinRouteCap t := by
  by_cases hsmall : t ≤ 6
  · have hcases : t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 := by omega
    rcases hcases with h | h | h | h | h
    · subst t; native_decide
    · subst t; native_decide
    · subst t; native_decide
    · subst t; native_decide
    · subst t; native_decide
  · have h7 : 7 ≤ t := by omega
    have hlarge := large_shortening_route_cap_all_depth t h7 ht
    have hclosed : shorteningPlotkinRouteCap 2 < 62748517 := by native_decide
    omega

theorem incidence_shortening_plotkin_cannot_pay_all_depth
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ supportWeight) :
    targetListBound < shorteningPlotkinRouteCap t := by
  have hmin := two_shortening_is_route_minimum_all_depth t h2 ht
  have hstop : targetListBound < shorteningPlotkinRouteCap 2 := by native_decide
  omega

#print axioms coordinate_ratio_at_least_thirteen_all_depth
#print axioms pullStep_ge_thirteen_all_depth
#print axioms pullback_ge_pow_thirteen_all_depth
#print axioms positive_plotkin_denominator_bounds_all_depth
#print axioms plotkinCap_positive_all_depth
#print axioms large_shortening_route_cap_all_depth
#print axioms two_shortening_is_route_minimum_all_depth
#print axioms incidence_shortening_plotkin_cannot_pay_all_depth

end LInteriorPayS1
