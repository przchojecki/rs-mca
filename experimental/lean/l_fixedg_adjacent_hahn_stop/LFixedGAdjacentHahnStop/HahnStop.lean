import Std.Tactic

/-!
# Lane L: fixed-G adjacent-interior Hahn stop

Stdlib-only arithmetic and finite-kernel replay for
`experimental/notes/thresholds/l_fixedg_adjacent_hahn_stop_v1.md`.

The source note proves the constant-weight Johnson-scheme/Delsarte argument.
This module checks the frozen adjacent rows, exact finite-p Johnson grid, the
degree-three dual and primal certificates, the complete finite prefix of the
all-degree feasibility check, the elementary tail gates, and the exact
conditional quarter-gap conversion.

No Mathlib. No `sorry`.
-/

namespace LFixedGAdjacentHahnStop

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
def maxIntersection : Nat := supportWeight - exchangeDistance

def johnsonEll : Nat := targetListBound

def finiteJohnsonLhs (a : Nat) : Nat :=
  (johnsonEll - 1) * (p * a - boundaryLength) ^ 2

def finiteJohnsonRhs (d : Nat) : Nat :=
  boundaryLength ^ 2 * (p - 1) ^ 2 * (johnsonEll - 1)
    - boundaryLength * (p - 1) * p * johnsonEll *
      (boundaryLength - (d - 1))

def qNat (n : Nat) : Rat := Rat.normalize (Int.ofNat n) 1
def qInt (z : Int) : Rat := Rat.normalize z 1

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

def aa (degree : Nat) : Rat :=
  mkRat
    (Int.ofNat
      ((boundaryLength + 1 - degree) *
        (supportWeight - degree) *
        (boundaryLength - supportWeight - degree)))
    ((boundaryLength + 1 - 2 * degree) *
      (boundaryLength - 2 * degree))

def cc (degree : Nat) : Rat :=
  mkRat
    (Int.ofNat
      (degree *
        (supportWeight + 1 - degree) *
        (boundaryLength - supportWeight + 1 - degree)))
    ((boundaryLength + 2 - 2 * degree) *
      (boundaryLength + 1 - 2 * degree))

def hahnNext (degree distance : Nat) (previous current : Rat) : Rat :=
  (((aa degree + cc degree - qNat distance) * current) -
      cc degree * previous) / aa degree

def hahnTail (distance : Nat) : Nat → Nat → Rat → Rat → List Rat
  | 0, _, _, _ => []
  | steps + 1, degree, previous, current =>
      let next := hahnNext degree distance previous current
      next :: hahnTail distance steps (degree + 1) current next

def hahnSequence (distance maximumDegree : Nat) : List Rat :=
  if maximumDegree = 0 then
    [qNat 1]
  else
    qNat 1 :: hahnDirect 1 distance ::
      hahnTail distance (maximumDegree - 1) 1 (qNat 1) (hahnDirect 1 distance)

def activeDistance0 : Nat := 67448
def activeDistance1 : Nat := 70799
def activeDistance2 : Nat := 70800

def activeIntersection0 : Nat := supportWeight - activeDistance0
def activeIntersection1 : Nat := supportWeight - activeDistance1
def activeIntersection2 : Nat := supportWeight - activeDistance2

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

def primalMoment (degree : Nat) : Rat :=
  qNat 1 +
    y0 * hahnDirect degree activeDistance0 +
    y1 * hahnDirect degree activeDistance1 +
    y2 * hahnDirect degree activeDistance2

def dualPolynomial (intersection : Nat) : Rat :=
  qNat 1 +
    c1 * hahnDirect 1 (supportWeight - intersection) +
    c2 * hahnDirect 2 (supportWeight - intersection) +
    c3 * hahnDirect 3 (supportWeight - intersection)

def factorScale : Rat :=
  Rat.normalize
    118055716980403503
    1924657059987219425146540

def factorPolynomial (intersection : Nat) : Rat :=
  factorScale *
    qInt (Int.ofNat intersection - 5412) *
    qInt (Int.ofNat intersection - 2061) *
    qInt (Int.ofNat intersection - 2060)

def dualFactorizationVerified : Bool :=
  (List.range (maxIntersection + 1)).all
    (fun intersection =>
      decide (dualPolynomial intersection = factorPolynomial intersection))

def dualFeasibleVerified : Bool :=
  (List.range (maxIntersection + 1)).all
    (fun intersection => decide (dualPolynomial intersection ≤ qNat 0))

def sequence0 : List Rat := hahnSequence activeDistance0 490
def sequence1 : List Rat := hahnSequence activeDistance1 490
def sequence2 : List Rat := hahnSequence activeDistance2 490

def prefixTriples : List ((Rat × Rat) × Rat) :=
  List.zip
    (List.zip (sequence0.drop 4) (sequence1.drop 4))
    (sequence2.drop 4)

def prefixSlacksPositive : Bool :=
  prefixTriples.all
    (fun values =>
      decide
        (qNat 0 <
          qNat 1 +
            y0 * values.1.1 +
            y1 * values.1.2 +
            y2 * values.2))

def minimumPrefixSlack : Rat :=
  Rat.normalize
    550052954011442897244763831709362374052806653649987382880740
    551410447208318265674262258763948662468585127118502801971127

def lpNumerator : Nat := 24044092640301071703360149280
def lpDenominator : Nat := 1159431963847722545269
def lpObjective : Rat := Rat.normalize (Int.ofNat lpNumerator) lpDenominator
def lpFloor : Nat := 20737821

def conditionalNumerator : Nat :=
  331360992001249019355025234436669495903
def conditionalDenominator : Nat :=
  20668103898396328436283228298625
def conditionalObjective : Rat :=
  Rat.normalize (Int.ofNat conditionalNumerator) conditionalDenominator
def conditionalFloor : Nat := 16032481

def yCeiling : Nat := 20738000
def modeIntersection : Nat := 5410
def activeModeDistance : Nat := modeIntersection - activeIntersection2
def coarseTailMass : Nat :=
  3 * yCeiling ^ 2 * (supportWeight + 1) * 3 ^ activeModeDistance
def tailStart : Nat := 491

/-! ## Frozen adjacent rows and Johnson comparison -/

theorem field_value : p = 2 ^ 31 - 1 := by native_decide

theorem low_row_partition :
    lowAgreement + lowErrors = boundaryLength := by native_decide

theorem high_row_partition :
    highAgreement + highErrors = boundaryLength := by native_decide

theorem low_slack_identity :
    lowAgreement = lowDimension + slack := by native_decide

theorem high_slack_identity :
    highAgreement = highDimension + slack := by native_decide

theorem adjacent_complement_symmetry :
    boundaryLength - lowAgreement = highAgreement ∧
    boundaryLength - highAgreement = lowAgreement := by
  native_decide

theorem exchange_distance_value :
    exchangeDistance = 67448 ∧ maxIntersection = 5412 := by
  native_decide

theorem low_classical_johnson_deficit :
    boundaryLength * (lowDimension - 1) - lowAgreement ^ 2 = 1290548 := by
  native_decide

theorem high_classical_johnson_deficit :
    boundaryLength * (highDimension - 1) - highAgreement ^ 2 = 1290548 := by
  native_decide

theorem low_finite_johnson_row_deficit :
    finiteJohnsonRhs lowDimension - finiteJohnsonLhs lowAgreement =
      95406788482294553836102174030451 := by
  native_decide

theorem low_finite_johnson_previous_deficit :
    finiteJohnsonRhs lowDimension - finiteJohnsonLhs 72868 =
      5205542238636045247040359936547 := by
  native_decide

theorem low_finite_johnson_boundary_margin :
    finiteJohnsonLhs 72869 - finiteJohnsonRhs lowDimension =
      6070309882968202312269231869644 := by
  native_decide

theorem high_finite_johnson_row_deficit :
    finiteJohnsonRhs highDimension - finiteJohnsonLhs highAgreement =
      99216260018857531361012790918704 := by
  native_decide

theorem high_finite_johnson_boundary_margin :
    finiteJohnsonLhs 908270 - finiteJohnsonRhs highDimension =
      41331612211590842518015690016521 := by
  native_decide

theorem exact_johnson_errors_and_gaps :
    boundaryLength - 72869 = 908260 ∧
    lowErrors - 908260 = 9 ∧
    boundaryLength - 908270 = 72859 ∧
    highErrors - 72859 = 1 := by
  native_decide

/-! ## Exact degree-three primal and dual certificates -/

theorem active_intersections :
    activeIntersection0 = 5412 ∧
    activeIntersection1 = 2061 ∧
    activeIntersection2 = 2060 := by
  native_decide

theorem primal_weights_positive_and_bounded :
    qNat 0 < y0 ∧ y0 < qNat yCeiling ∧
    qNat 0 < y1 ∧ y1 < qNat yCeiling ∧
    qNat 0 < y2 ∧ y2 < qNat yCeiling := by
  native_decide

theorem dual_coefficients_positive :
    qNat 0 < c1 ∧ qNat 0 < c2 ∧ qNat 0 < c3 := by
  native_decide

theorem primal_tight_first_three :
    primalMoment 1 = qNat 0 ∧
    primalMoment 2 = qNat 0 ∧
    primalMoment 3 = qNat 0 := by
  native_decide

theorem dual_active_roots :
    dualPolynomial activeIntersection0 = qNat 0 ∧
    dualPolynomial activeIntersection1 = qNat 0 ∧
    dualPolynomial activeIntersection2 = qNat 0 := by
  native_decide

theorem dual_factorization_on_allowed_intersections :
    dualFactorizationVerified = true := by
  native_decide

theorem dual_nonpositive_on_allowed_intersections :
    dualFeasibleVerified = true := by
  native_decide

theorem recurrence_matches_direct_through_three :
    hahnSequence activeDistance0 3 =
      [hahnDirect 0 activeDistance0, hahnDirect 1 activeDistance0,
        hahnDirect 2 activeDistance0, hahnDirect 3 activeDistance0] ∧
    hahnSequence activeDistance1 3 =
      [hahnDirect 0 activeDistance1, hahnDirect 1 activeDistance1,
        hahnDirect 2 activeDistance1, hahnDirect 3 activeDistance1] ∧
    hahnSequence activeDistance2 3 =
      [hahnDirect 0 activeDistance2, hahnDirect 1 activeDistance2,
        hahnDirect 2 activeDistance2, hahnDirect 3 activeDistance2] := by
  native_decide

theorem prefix_slacks_positive_through_490 :
    prefixSlacksPositive = true := by
  native_decide

theorem degree_five_slack_value :
    primalMoment 5 = minimumPrefixSlack := by
  native_decide

/-! ## Objective, floor, and conditional quarter-gap arithmetic -/

theorem primal_objective_value :
    qNat 1 + y0 + y1 + y2 = lpObjective := by
  native_decide

theorem dual_objective_value :
    qNat 1 + c1 + c2 + c3 = lpObjective := by
  native_decide

theorem lp_division :
    lpNumerator / lpDenominator = lpFloor ∧
    lpNumerator % lpDenominator = 112348530301907230431 := by
  native_decide

theorem lp_floor_bracket :
    qNat lpFloor < lpObjective ∧
    lpObjective < qNat (lpFloor + 1) := by
  native_decide

theorem lp_route_excess :
    lpFloor - targetListBound = 3960607 := by
  native_decide

theorem two_shortening_improvement :
    30682446 - lpFloor = 9944625 := by
  native_decide

theorem lp_cap_of_cross {L : Nat}
    (h : L * lpDenominator ≤ lpNumerator) :
    L ≤ lpFloor := by
  simp [lpDenominator, lpNumerator, lpFloor] at h ⊢
  omega

theorem quarter_gap_objective :
    lpObjective - c3 * Rat.normalize 1 4 = conditionalObjective := by
  native_decide

theorem conditional_division :
    conditionalNumerator / conditionalDenominator = conditionalFloor ∧
    conditionalNumerator % conditionalDenominator =
      8944183953230554666120301857278 := by
  native_decide

theorem conditional_floor_bracket :
    qNat conditionalFloor < conditionalObjective ∧
    conditionalObjective < qNat (conditionalFloor + 1) := by
  native_decide

theorem conditional_safety_margin :
    targetListBound - conditionalFloor = 744733 ∧
    BStar - (conditionalFloor + 1) = 744733 := by
  native_decide

theorem conditional_cap_of_cross {L : Nat}
    (h : L * conditionalDenominator ≤ conditionalNumerator) :
    L ≤ conditionalFloor := by
  simp [conditionalDenominator, conditionalNumerator, conditionalFloor] at h ⊢
  omega

/-! ## All-degree tail arithmetic gates -/

theorem mode_left_ratio_margin :
    (supportWeight - 5409) ^ 2 =
      5410 * (boundaryLength - 2 * supportWeight + 5410) + 806611 := by
  native_decide

theorem mode_right_ratio_margin :
    5411 * (boundaryLength - 2 * supportWeight + 5411) =
      (supportWeight - 5410) ^ 2 + 174520 := by
  native_decide

theorem lower_step_factor_three_margin :
    3 * 2061 * (boundaryLength - 2 * supportWeight + 2061) =
      (supportWeight - 2060) ^ 2 + 165437010 := by
  native_decide

theorem upper_step_factor_three_margin :
    3 * (supportWeight - 5411) ^ 2 =
      5412 * (boundaryLength - 2 * supportWeight + 5412) + 9097579551 := by
  native_decide

theorem active_mode_distance_value :
    activeModeDistance = 3350 := by
  native_decide

theorem multiplicity_half_margin :
    boundaryLength - 3 * supportWeight + 1 = 762550 := by
  native_decide

def growthLhs (degree : Nat) : Nat :=
  (boundaryLength - 2 * degree - 1) *
    (boundaryLength - degree + 1)

def growthRhs (degree : Nat) : Nat :=
  (degree + 1) *
    (boundaryLength - 2 * degree + 1)

theorem multiplicity_growth_endpoint_margin :
    growthLhs (supportWeight - 1) =
      growthRhs (supportWeight - 1) + 697910557790 := by
  native_decide

theorem tail_start_integer_gate :
    2 * tailStart ^ tailStart * coarseTailMass <
      (boundaryLength - tailStart + 1) ^ tailStart := by
  native_decide

/-! ## Axiom census -/

#print axioms field_value
#print axioms low_row_partition
#print axioms high_row_partition
#print axioms low_slack_identity
#print axioms high_slack_identity
#print axioms adjacent_complement_symmetry
#print axioms exchange_distance_value
#print axioms low_classical_johnson_deficit
#print axioms high_classical_johnson_deficit
#print axioms low_finite_johnson_row_deficit
#print axioms low_finite_johnson_previous_deficit
#print axioms low_finite_johnson_boundary_margin
#print axioms high_finite_johnson_row_deficit
#print axioms high_finite_johnson_boundary_margin
#print axioms exact_johnson_errors_and_gaps
#print axioms active_intersections
#print axioms primal_weights_positive_and_bounded
#print axioms dual_coefficients_positive
#print axioms primal_tight_first_three
#print axioms dual_active_roots
#print axioms dual_factorization_on_allowed_intersections
#print axioms dual_nonpositive_on_allowed_intersections
#print axioms recurrence_matches_direct_through_three
#print axioms prefix_slacks_positive_through_490
#print axioms degree_five_slack_value
#print axioms primal_objective_value
#print axioms dual_objective_value
#print axioms lp_division
#print axioms lp_floor_bracket
#print axioms lp_route_excess
#print axioms two_shortening_improvement
#print axioms lp_cap_of_cross
#print axioms quarter_gap_objective
#print axioms conditional_division
#print axioms conditional_floor_bracket
#print axioms conditional_safety_margin
#print axioms conditional_cap_of_cross
#print axioms mode_left_ratio_margin
#print axioms mode_right_ratio_margin
#print axioms lower_step_factor_three_margin
#print axioms upper_step_factor_three_margin
#print axioms active_mode_distance_value
#print axioms multiplicity_half_margin
#print axioms multiplicity_growth_endpoint_margin
#print axioms tail_start_integer_gate

end LFixedGAdjacentHahnStop
