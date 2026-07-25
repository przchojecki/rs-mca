import Std.Tactic

/-!
# Lane L, session one: fixed-G interior payment

This stdlib-only module kernel-checks two exact statements used by the
accompanying research note.

* The inherited adjacent-row degree-three Hahn dual reaches the target
  `L ≤ 16,777,214` as soon as its weighted first-three Hahn energy pays one
  exact rational gap. The one-mode sufficient threshold on `G₃` is strictly
  smaller than `1/4`.
* Every scalar route consisting only of repeated common-coordinate incidence
  shortening followed by the ordinary constant-weight Plotkin inequality stops
  above the target. Two shortenings are optimal inside this named route.

The Reed--Solomon-specific moment gap is deliberately defined as a `Prop`; it is
not asserted as a theorem. No Mathlib, `sorry`, or custom axiom is used.
-/

namespace LInteriorPayS1

/-! ## Frozen row and Hahn-dual constants -/

def p : Nat := 2147483647
def boundaryLength : Nat := 981129
def slack : Nat := 67447
def exchangeDistance : Nat := slack + 1
def BStar : Nat := 16777215
def targetListBound : Nat := BStar - 1

def lowDimension : Nat := 5413
def lowAgreement : Nat := 72860
def lowErrors : Nat := boundaryLength - lowAgreement

def highDimension : Nat := 840822
def highAgreement : Nat := 908269
def highErrors : Nat := boundaryLength - highAgreement

def supportWeight : Nat := 72860
def maximumIntersection : Nat := supportWeight - exchangeDistance

def qNat (n : Nat) : Rat := Rat.normalize (Int.ofNat n) 1

def lpObjective : Rat :=
  Rat.normalize
    24044092640301071703360149280
    1159431963847722545269

def c1 : Rat :=
  Rat.normalize
    979061542845605776592576657442
    21065719351149270924992461

def c2 : Rat :=
  Rat.normalize
    2127197006408557278777618631055673
    1137547685530096782227047625

def c3 : Rat :=
  Rat.normalize
    389001796223311531724035804630343856388
    20668103898396328436283228298625

def criticalGap : Rat := lpObjective - qNat targetListBound

def h3CriticalThreshold : Rat :=
  Rat.normalize
    40929119489723721648112549908683964625
    194500898111655765862017902315171928194

inductive AdjacentRow where
  | low
  | high
  deriving DecidableEq, Repr

/-- Only the data consumed by the exact low-Hahn compiler. The predicate
`arises` in the conjecture below carries the separate RS-realizability content. -/
structure SelectedSupportHahnData where
  row : AdjacentRow
  listSize : Nat
  g1 : Rat
  g2 : Rat
  g3 : Rat
  deriving Repr

def weightedLowHahnEnergy (data : SelectedSupportHahnData) : Rat :=
  c1 * data.g1 + c2 * data.g2 + c3 * data.g3

/-- The sharp one-hypothesis conjecture for the inherited degree-three dual.
The argument `arises` is intended to mean “is the normalized Hahn data of a
selected-support family arising from one of the two adjacent ordinary-RS rows.”
It is written directly in the objective form consumed by Delsarte duality. -/
def RSHahn123CriticalGap
    (arises : SelectedSupportHahnData → Prop) : Prop :=
  ∀ data, arises data →
    lpObjective - weightedLowHahnEnergy data ≤ qNat targetListBound

/-- Simpler but stronger one-mode version. Standard Johnson-scheme positivity
of `G₁,G₂` turns this into `RSHahn123CriticalGap`; that analytic bridge is
proved in the source note rather than re-encoding ordered-rational algebra. -/
def RSH3CriticalGap
    (arises : SelectedSupportHahnData → Prop) : Prop :=
  ∀ data, arises data → h3CriticalThreshold ≤ data.g3

/-! ## Exact critical-gap arithmetic and compiler -/

theorem field_value : p = 2 ^ 31 - 1 := by native_decide

theorem row_partitions_and_slack :
    lowAgreement + lowErrors = boundaryLength ∧
    highAgreement + highErrors = boundaryLength ∧
    lowAgreement = lowDimension + slack ∧
    highAgreement = highDimension + slack := by
  native_decide

theorem adjacent_complement_symmetry :
    lowErrors = highAgreement ∧ highErrors = lowAgreement := by
  native_decide

theorem target_and_anchor_addback :
    targetListBound = 16777214 ∧ targetListBound + 1 = BStar := by
  native_decide

theorem dual_coefficients_positive :
    qNat 0 < c1 ∧ qNat 0 < c2 ∧ qNat 0 < c3 := by
  native_decide

theorem critical_gap_exact :
    criticalGap =
      Rat.normalize
        4592054464387567148757448714
        1159431963847722545269 := by
  native_decide

theorem critical_gap_is_c3_times_threshold :
    criticalGap = c3 * h3CriticalThreshold := by
  native_decide

theorem exact_h3_threshold_objective :
    lpObjective - c3 * h3CriticalThreshold = qNat targetListBound := by
  native_decide

theorem h3_threshold_strictly_below_quarter :
    h3CriticalThreshold < Rat.normalize 1 4 := by
  native_decide

theorem quarter_objective_and_floor :
    lpObjective - c3 * Rat.normalize 1 4 =
      Rat.normalize
        331360992001249019355025234436669495903
        20668103898396328436283228298625 ∧
    16032481 < 16032482 ∧
    targetListBound - 16032481 = 744733 := by
  native_decide

/-- The conjecture is already in the exact objective form required by the
conditional list compiler. This theorem is a scope-preserving elimination of
the named hypothesis, not a proof of that hypothesis. -/
theorem critical_gap_hypothesis_compiles
    (arises : SelectedSupportHahnData → Prop)
    (hgap : RSHahn123CriticalGap arises)
    (data : SelectedSupportHahnData)
    (harises : arises data) :
    lpObjective - weightedLowHahnEnergy data ≤ qNat targetListBound :=
  hgap data harises

/-! ## Kernel-checked evidence for and against the conjecture -/

def singletonData : SelectedSupportHahnData where
  row := .low
  listSize := 1
  g1 := qNat 1
  g2 := qNat 1
  g3 := qNat 1

def criticalBoundaryData : SelectedSupportHahnData where
  row := .low
  listSize := targetListBound
  g1 := qNat 0
  g2 := qNat 0
  g3 := h3CriticalThreshold

def zeroMomentTemplate : SelectedSupportHahnData where
  row := .low
  listSize := targetListBound + 1
  g1 := qNat 0
  g2 := qNat 0
  g3 := qNat 0

theorem singleton_satisfies_weighted_gap :
    lpObjective - weightedLowHahnEnergy singletonData < qNat targetListBound := by
  native_decide

theorem critical_boundary_is_exact :
    lpObjective - weightedLowHahnEnergy criticalBoundaryData =
      qNat targetListBound := by
  native_decide

theorem zero_moment_template_is_direct_falsifier :
    qNat targetListBound <
      lpObjective - weightedLowHahnEnergy zeroMomentTemplate := by
  native_decide

/-! A direct normalized Hahn evaluation for a two-support stress instance. -/

def choose : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => choose n k + choose n (k + 1)

def falling : Nat → Nat → Nat
  | _, 0 => 1
  | n, k + 1 => falling n k * (n - k)

def hahnNumerator (degree distance : Nat) : Int :=
  (List.range (degree + 1)).foldl
    (fun total s =>
      let term :=
        choose degree s *
          falling distance s ^ 2 *
          falling (supportWeight - distance) (degree - s) *
          falling (boundaryLength - supportWeight - distance) (degree - s)
      if s % 2 = 0 then total + Int.ofNat term else total - Int.ofNat term)
    0

def hahnDenominator (degree : Nat) : Nat :=
  falling supportWeight degree *
    falling (boundaryLength - supportWeight) degree

def hahnDirect (degree distance : Nat) : Rat :=
  mkRat (hahnNumerator degree distance) (hahnDenominator degree)

def endpointPairG3 : Rat := qNat 1 + hahnDirect 3 supportWeight

theorem endpoint_pair_g3_exact :
    endpointPairG3 =
      Rat.normalize 62407467461571137 62439698060243047 := by
  native_decide

theorem endpoint_pair_clears_h3_threshold :
    h3CriticalThreshold < endpointPairG3 := by
  native_decide

/-! The matching fractional LP optimum has zero first-three Hahn moments. It
is not an RS family, but it is the exact obstruction to deriving the conjecture
from ordinary Johnson-scheme positivity alone. -/

def activeDistance0 : Nat := 67448
def activeDistance1 : Nat := 70799
def activeDistance2 : Nat := 70800

def y0 : Rat :=
  Rat.normalize
    11248760258723433202306504856279750
    542640826015902648804433187

def y1 : Rat :=
  Rat.normalize
    5964107581872309468780632000
    1295085503617906083065473

def y2 : Rat :=
  Rat.normalize
    1726595658518143191722829859
    485801992852195746467711

def fractionalPrimalMoment (degree : Nat) : Rat :=
  qNat 1 +
    y0 * hahnDirect degree activeDistance0 +
    y1 * hahnDirect degree activeDistance1 +
    y2 * hahnDirect degree activeDistance2

theorem fractional_primal_zero_first_three :
    fractionalPrimalMoment 1 = qNat 0 ∧
    fractionalPrimalMoment 2 = qNat 0 ∧
    fractionalPrimalMoment 3 = qNat 0 := by
  native_decide

/-! ## All-depth incidence-shortening plus Plotkin route cut -/

/-- The signed Plotkin denominator before truncating to `Nat`. -/
def plotkinSignedDenominator (t : Nat) : Int :=
  Int.ofNat exchangeDistance *
      (Int.ofNat boundaryLength - Int.ofNat t) -
    (Int.ofNat supportWeight - Int.ofNat t) *
      Int.ofNat (boundaryLength - supportWeight)

/-- On the valid positive-denominator range this is the same quantity in Nat. -/
def plotkinPositiveDenominator (t : Nat) : Nat :=
  840821 * t - 1290548

def plotkinNumerator (t : Nat) : Nat :=
  exchangeDistance * (boundaryLength - t)

def plotkinCap (t : Nat) : Nat :=
  plotkinNumerator t / plotkinPositiveDenominator t

def pullStep (j x : Nat) : Nat :=
  x * (boundaryLength - j) / (supportWeight - j)

/-- Exact reverse of the nested incidence ceilings. -/
def pullback : Nat → Nat → Nat
  | 0, x => x
  | t + 1, x => pullback t (pullStep t x)

def shorteningPlotkinRouteCap (t : Nat) : Nat :=
  pullback t (plotkinCap t)

theorem signed_plotkin_denominator_boundary :
    plotkinSignedDenominator 0 = -1290548 ∧
    plotkinSignedDenominator 1 = -449727 ∧
    plotkinSignedDenominator 2 = 391094 := by
  native_decide

theorem exact_shortening_route_caps_two_through_six :
    (plotkinCap 2 = 169204 ∧ shorteningPlotkinRouteCap 2 = 30682446) ∧
    (plotkinCap 3 = 53717 ∧ shorteningPlotkinRouteCap 3 = 131171251) ∧
    (plotkinCap 4 = 31926 ∧ shorteningPlotkinRouteCap 4 = 1049844832) ∧
    (plotkinCap 5 = 22712 ∧ shorteningPlotkinRouteCap 5 = 10057615672) ∧
    (plotkinCap 6 = 17626 ∧ shorteningPlotkinRouteCap 6 = 105113028810) := by
  native_decide

theorem two_shortening_route_excess :
    shorteningPlotkinRouteCap 2 - targetListBound = 13905232 := by
  native_decide

theorem coordinate_ratio_at_least_thirteen
    (j : Nat) (hj : j ≤ 5411) :
    13 * (supportWeight - j) ≤ boundaryLength - j := by
  simp [supportWeight, boundaryLength]
  omega

theorem pullStep_ge_thirteen
    (j x : Nat) (hj : j ≤ 5411) :
    13 * x ≤ pullStep j x := by
  have hden : 0 < supportWeight - j := by
    simp [supportWeight]
    omega
  apply (Nat.le_div_iff_mul_le hden).2
  calc
    13 * x * (supportWeight - j) =
        x * (13 * (supportWeight - j)) := by ac_rfl
    _ ≤ x * (boundaryLength - j) :=
      Nat.mul_le_mul_left x (coordinate_ratio_at_least_thirteen j hj)

theorem pullback_ge_pow_thirteen
    (t x : Nat) (ht : t ≤ 5412) :
    13 ^ t * x ≤ pullback t x := by
  induction t generalizing x with
  | zero => simp [pullback]
  | succ t ih =>
      have htj : t ≤ 5411 := by omega
      have hstep : 13 * x ≤ pullStep t x :=
        pullStep_ge_thirteen t x htj
      have hrec : 13 ^ t * pullStep t x ≤ pullback t (pullStep t x) :=
        ih (pullStep t x) (by omega)
      calc
        13 ^ (t + 1) * x = 13 ^ t * (13 * x) := by
          simp [Nat.pow_succ, Nat.mul_assoc]
        _ ≤ 13 ^ t * pullStep t x := Nat.mul_le_mul_left (13 ^ t) hstep
        _ ≤ pullback t (pullStep t x) := hrec
        _ = pullback (t + 1) x := by rfl

theorem positive_plotkin_denominator_bounds
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ 5412) :
    0 < plotkinPositiveDenominator t ∧
    plotkinPositiveDenominator t ≤ plotkinNumerator t := by
  simp [plotkinPositiveDenominator, plotkinNumerator,
    exchangeDistance, slack, boundaryLength]
  omega

theorem plotkinCap_positive
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ 5412) :
    1 ≤ plotkinCap t := by
  have hbounds := positive_plotkin_denominator_bounds t h2 ht
  unfold plotkinCap
  apply (Nat.le_div_iff_mul_le hbounds.1).2
  simpa using hbounds.2

theorem large_shortening_route_cap
    (t : Nat) (h7 : 7 ≤ t) (ht : t ≤ 5412) :
    62748517 ≤ shorteningPlotkinRouteCap t := by
  have hpull := pullback_ge_pow_thirteen t (plotkinCap t) ht
  have hcap := plotkinCap_positive t (by omega) ht
  have hpow : 13 ^ 7 ≤ 13 ^ t := Nat.pow_le_pow_right (by decide) h7
  calc
    62748517 = 13 ^ 7 := by native_decide
    _ ≤ 13 ^ t := hpow
    _ = 13 ^ t * 1 := by simp
    _ ≤ 13 ^ t * plotkinCap t := Nat.mul_le_mul_left (13 ^ t) hcap
    _ ≤ pullback t (plotkinCap t) := hpull
    _ = shorteningPlotkinRouteCap t := by rfl

/-- Exact all-depth route cut: among every valid number of common-coordinate
shortenings, the scalar incidence-plus-Plotkin method is minimized at `t=2` and
still exceeds the target. -/
theorem two_shortening_is_route_minimum
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ 5412) :
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
    have hlarge := large_shortening_route_cap t h7 ht
    have hclosed : shorteningPlotkinRouteCap 2 < 62748517 := by native_decide
    omega

theorem incidence_shortening_plotkin_cannot_pay
    (t : Nat) (h2 : 2 ≤ t) (ht : t ≤ 5412) :
    targetListBound < shorteningPlotkinRouteCap t := by
  have hmin := two_shortening_is_route_minimum t h2 ht
  have hstop : targetListBound < shorteningPlotkinRouteCap 2 := by native_decide
  omega

/-! ## Exact row print-block arithmetic -/

theorem low_row_print_arithmetic :
    lowDimension = 5413 ∧
    lowAgreement = 72860 ∧
    lowErrors = 908269 ∧
    boundaryLength - 72869 = 908260 ∧
    lowErrors - 908260 = 9 := by
  native_decide

theorem high_row_print_arithmetic :
    highDimension = 840822 ∧
    highAgreement = 908269 ∧
    highErrors = 72860 ∧
    boundaryLength - 908270 = 72859 ∧
    highErrors - 72859 = 1 := by
  native_decide

/-! ## Axiom census -/

#print axioms field_value
#print axioms row_partitions_and_slack
#print axioms adjacent_complement_symmetry
#print axioms target_and_anchor_addback
#print axioms dual_coefficients_positive
#print axioms critical_gap_exact
#print axioms critical_gap_is_c3_times_threshold
#print axioms exact_h3_threshold_objective
#print axioms h3_threshold_strictly_below_quarter
#print axioms quarter_objective_and_floor
#print axioms critical_gap_hypothesis_compiles
#print axioms singleton_satisfies_weighted_gap
#print axioms critical_boundary_is_exact
#print axioms zero_moment_template_is_direct_falsifier
#print axioms endpoint_pair_g3_exact
#print axioms endpoint_pair_clears_h3_threshold
#print axioms fractional_primal_zero_first_three
#print axioms signed_plotkin_denominator_boundary
#print axioms exact_shortening_route_caps_two_through_six
#print axioms two_shortening_route_excess
#print axioms coordinate_ratio_at_least_thirteen
#print axioms pullStep_ge_thirteen
#print axioms pullback_ge_pow_thirteen
#print axioms positive_plotkin_denominator_bounds
#print axioms plotkinCap_positive
#print axioms large_shortening_route_cap
#print axioms two_shortening_is_route_minimum
#print axioms incidence_shortening_plotkin_cannot_pay
#print axioms low_row_print_arithmetic
#print axioms high_row_print_arithmetic

end LInteriorPayS1
