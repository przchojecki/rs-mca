import LInteriorPayS1.AllDepthStop

/-!
# Best scalar terminal cap after every shortening depth

For `t ≤ 5,412` this route uses the ordinary constant-weight Plotkin cap. Once
`t ≥ 5,413`, the residual support weight is below the required exchange
distance, so any genuine terminal section is a singleton and the sharp scalar
terminal cap is one. Even this piecewise best terminal input pulls back above
the target at every possible depth.
-/

namespace LInteriorPayS1

/-- Any residual candidate type whose exchange metric is bounded by its common
weight becomes subsingleton once that weight is smaller than the required
minimum exchange distance. This is the abstract combinatorial justification
for the terminal cap one. -/
theorem residual_below_distance_subsingleton
    {α : Type}
    (weight : α → Nat)
    (exchange : α → α → Nat)
    (residualWeight minimumDistance : Nat)
    (hweight : ∀ x, weight x = residualWeight)
    (hexchangeUpper : ∀ x y, exchange x y ≤ weight x)
    (hminimum : ∀ x y, x ≠ y → minimumDistance ≤ exchange x y)
    (hsmall : residualWeight < minimumDistance) :
    Subsingleton α := by
  refine ⟨?_⟩
  intro x y
  by_cases hxy : x = y
  · exact hxy
  · have hlo := hminimum x y hxy
    have hhi := hexchangeUpper x y
    rw [hweight x] at hhi
    have hfalse : False := by omega
    exact False.elim hfalse

/-- Best terminal scalar cap available from the named route: Plotkin while the
residual weight is at least the exchange distance, singleton afterward. -/
def bestTerminalCap (t : Nat) : Nat :=
  if t ≤ maximumIntersection then plotkinCap t else 1

def bestShorteningRouteCap (t : Nat) : Nat :=
  pullback t (bestTerminalCap t)

theorem best_route_two_exact :
    bestShorteningRouteCap 2 = shorteningPlotkinRouteCap 2 := by
  native_decide

/-- In the automatically-singleton range, exact reverse incidence pullback of
terminal cap one is already worse than the two-shortening cap. -/
theorem late_singleton_pullback_above_two
    (t : Nat) (hlate : 5413 ≤ t) (ht : t ≤ supportWeight) :
    shorteningPlotkinRouteCap 2 ≤ pullback t 1 := by
  have hpull := pullback_ge_pow_thirteen_all_depth t 1 ht
  have hpow : 13 ^ 7 ≤ 13 ^ t :=
    Nat.pow_le_pow_right (by decide) (by omega)
  calc
    shorteningPlotkinRouteCap 2 ≤ 62748517 := by native_decide
    _ = 13 ^ 7 := by native_decide
    _ ≤ 13 ^ t := hpow
    _ = 13 ^ t * 1 := by simp
    _ ≤ pullback t 1 := hpull

/-- The literal best-cap scalar route is minimized at two shortenings over all
possible depths `2 ≤ t ≤ supportWeight`. -/
theorem two_shortening_is_best_terminal_route_minimum
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ supportWeight) :
    bestShorteningRouteCap 2 ≤ bestShorteningRouteCap t := by
  unfold bestShorteningRouteCap bestTerminalCap
  have htwo : 2 ≤ maximumIntersection := by native_decide
  rw [if_pos htwo]
  by_cases hearly : t ≤ maximumIntersection
  · rw [if_pos hearly]
    have ht5412 : t ≤ 5412 := by
      simpa [maximumIntersection, supportWeight, exchangeDistance, slack]
        using hearly
    have hbase := two_shortening_is_route_minimum t h2 ht5412
    simpa [shorteningPlotkinRouteCap] using hbase
  · rw [if_neg hearly]
    have hnot : ¬ t ≤ 5412 := by
      simpa [maximumIntersection, supportWeight, exchangeDistance, slack]
        using hearly
    have hlate : 5413 ≤ t := by omega
    have hbase := late_singleton_pullback_above_two t hlate ht
    simpa [shorteningPlotkinRouteCap] using hbase

theorem best_terminal_incidence_route_cannot_pay
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ supportWeight) :
    targetListBound < bestShorteningRouteCap t := by
  have hmin := two_shortening_is_best_terminal_route_minimum t h2 ht
  have hstop : targetListBound < bestShorteningRouteCap 2 := by native_decide
  omega

#print axioms residual_below_distance_subsingleton
#print axioms best_route_two_exact
#print axioms late_singleton_pullback_above_two
#print axioms two_shortening_is_best_terminal_route_minimum
#print axioms best_terminal_incidence_route_cannot_pay

end LInteriorPayS1
