import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Exact arithmetic for adjacent fixed-`G` Hahn complementarity

The accompanying paper proves the complementarity identity `H = L + E_Hahn +
S_shell`, the target-sized conservation law, the integer variance minimization
behind the first-moment floor, and the random-transversal moment formulas.  This
module certifies the frozen rows, the exact correspondence between the three
dual root shells in exchange-distance and intersection coordinates, the cubic
substitution identity, the sign and zero set of the shell cubic over the whole
allowed range, the exact rational ledger (`H`, `Delta_open`, `theta_open`,
`theta_closed`, the first-moment floor, the integral third-moment ceiling and its
improvement, `Q_star`), the two integer incidence maxima, and the enumerated
radius-`100` shell minimum with the two band fractions printed from it.

It does not formalize the Johnson scheme, the Hahn functions, Reed--Solomon
codes, the dual factorization, or the transversal sample space; those are proved
in the accompanying paper and in the cited source packets.
-/

namespace LHahnComplementarityS1

/-! ## Frozen rows -/

abbrev p : Nat := 2147483647
abbrev N : Nat := 981129
abbrev w : Nat := 67447
abbrev D : Nat := 67448
abbrev s0 : Nat := 72860
abbrev Bstar : Nat := 16777215
abbrev ell : Nat := 16777214

/-- Low row degree bound and agreement. -/
abbrev dLow : Nat := 5413
abbrev mLow : Nat := 72860
/-- High row degree bound and agreement. -/
abbrev dHigh : Nat := 840822
abbrev mHigh : Nat := 908269

theorem declared_rows_exact :
    p = 2 ^ 31 - 1 ∧
    D = w + 1 ∧
    ell = Bstar - 1 ∧
    s0 = mLow ∧
    mLow + mHigh = N ∧
    (N : Int) - 2 * (mHigh : Int) = -835409 ∧
    dLow - 1 = 5412 ∧
    dHigh - 1 = 840821 := by
  native_decide

#print axioms LHahnComplementarityS1.declared_rows_exact

/-! ## The three dual root shells -/

/-- Exchange-distance form of the frozen cubic factor. -/
def shellPoly (e : Int) : Int := (e - 67448) * (e - 70799) * (e - 70800)

/-- Intersection form of the same factor. -/
def intersectionPoly (t : Int) : Int := (5412 - t) * (2061 - t) * (2060 - t)

/--
The two printed forms of the shell cubic are the same polynomial under
`e = s0 - t`.  This is equations (B) and (C) of the paper.
-/
theorem distance_intersection_identity (t : Int) :
    shellPoly (72860 - t) = intersectionPoly t := by
  unfold shellPoly intersectionPoly
  have h1 : (72860 : Int) - t - 67448 = 5412 - t := by omega
  have h2 : (72860 : Int) - t - 70799 = 2061 - t := by omega
  have h3 : (72860 : Int) - t - 70800 = 2060 - t := by omega
  rw [h1, h2, h3]

#print axioms LHahnComplementarityS1.distance_intersection_identity

/-- The root correspondence and its preserved spacing. -/
theorem root_shells_exact :
    (s0 : Int) - 67448 = 5412 ∧
    (s0 : Int) - 70799 = 2061 ∧
    (s0 : Int) - 70800 = 2060 ∧
    (70799 : Int) - 67448 = 3351 ∧
    (5412 : Int) - 2061 = 3351 ∧
    (70800 : Int) - 70799 = 1 ∧
    shellPoly 67448 = 0 ∧ shellPoly 70799 = 0 ∧ shellPoly 70800 = 0 := by
  native_decide

#print axioms LHahnComplementarityS1.root_shells_exact

/-! ## Sign and zero set over the whole allowed range -/

/-- Every allowed selected-support intersection, `0 ≤ t ≤ 5412`. -/
def allowedIntersections : List Int := (List.range 5413).map (fun i => Int.ofNat i)

/-- Every allowed exchange distance, `D ≤ e ≤ s0`. -/
def allowedDistances : List Int := (List.range 5413).map (fun i => Int.ofNat (67448 + i))

theorem allowed_ranges_exact :
    allowedIntersections.length = 5413 ∧
    allowedDistances.length = 5413 ∧
    allowedDistances.head? = some 67448 ∧
    allowedDistances.getLast? = some 72860 := by
  native_decide

#print axioms LHahnComplementarityS1.allowed_ranges_exact

/--
Over the whole allowed exchange-distance range the shell cubic is nonnegative,
and its zero set is exactly the three printed root shells.  This is the finite
instance of (2.2) that the packet actually uses.
-/
theorem shell_sign_and_zeros_on_allowed :
    allowedDistances.all (fun e => decide (0 ≤ shellPoly e)) = true ∧
    allowedDistances.filter (fun e => decide (shellPoly e = 0)) =
      [67448, 70799, 70800] := by
  native_decide

#print axioms LHahnComplementarityS1.shell_sign_and_zeros_on_allowed

/-- The same statement in intersection coordinates. -/
theorem intersection_sign_and_zeros_on_allowed :
    allowedIntersections.all (fun t => decide (0 ≤ intersectionPoly t)) = true ∧
    allowedIntersections.filter (fun t => decide (intersectionPoly t = 0)) =
      [2060, 2061, 5412] := by
  native_decide

#print axioms LHahnComplementarityS1.intersection_sign_and_zeros_on_allowed

/-! ## The exact rational ledger -/

abbrev H : Rat := (24044092640301071703360149280 : Rat) / 1159431963847722545269
abbrev c1 : Rat := (979061542845605776592576657442 : Rat) / 21065719351149270924992461
abbrev c2 : Rat := (2127197006408557278777618631055673 : Rat) / 1137547685530096782227047625
abbrev c3 : Rat :=
  (389001796223311531724035804630343856388 : Rat) / 20668103898396328436283228298625
abbrev alpha : Rat := (118055716980403503 : Rat) / 1924657059987219425146540

abbrev DeltaOpen : Rat := H - (Bstar : Rat)
abbrev thetaOpen : Rat :=
  (81858218311343544899896663534139630625 : Rat) /
    389001796223311531724035804630343856388
abbrev thetaClosed : Rat :=
  (40929119489723721648112549908683964625 : Rat) /
    194500898111655765862017902315171928194
abbrev g1Floor : Rat := (200351922 : Rat) / 1233618913144709
abbrev integralG3Ceiling : Rat :=
  (7745382636890381786544822902247859893375 : Rat) /
    36807150535206474929475326013497088586156
abbrev Qstar : Rat :=
  (181495440148245273326617612350 : Rat) / 47158238754849128004301

/-- Positivity of every inherited dual constant. -/
theorem dual_constants_positive :
    0 < c1 ∧ 0 < c2 ∧ 0 < c3 ∧ 0 < alpha ∧ 0 < H := by
  native_decide

#print axioms LHahnComplementarityS1.dual_constants_positive

/-- `Delta_open = H - B*`, as the printed exact rational, and its integer floor. -/
theorem delta_open_exact :
    DeltaOpen =
      (4592053304955603301034903445 : Rat) / 1159431963847722545269 ∧
    (20737821 : Rat) < H ∧ H < 20737822 ∧
    (20737821 : Nat) - ell = 3960607 ∧
    (3960606 : Rat) < DeltaOpen ∧ DeltaOpen < 3960607 := by
  native_decide

#print axioms LHahnComplementarityS1.delta_open_exact

/-- Both printed one-mode thresholds are the stated quotients, and the closed
proxy is the larger of the two. -/
theorem thresholds_exact :
    thetaOpen = DeltaOpen / c3 ∧
    thetaClosed = (H - (ell : Rat)) / c3 ∧
    thetaOpen < thetaClosed := by
  native_decide

#print axioms LHahnComplementarityS1.thresholds_exact

/--
The first-moment floor is exactly the minimal integer coordinate-degree variance
`rho (N - rho) / (B* s0 (N - s0))` at the printed incidence remainder.
-/
theorem first_moment_floor_exact :
    (Bstar * s0) % N = 244929 ∧
    g1Floor =
      ((244929 * (N - 244929) : Nat) : Rat) /
        ((Bstar * s0 * (N - s0) : Nat) : Rat) := by
  native_decide

#print axioms LHahnComplementarityS1.first_moment_floor_exact

/--
The integral third-moment ceiling is exactly what the conservation law gives
after subtracting the first-moment floor, it is strictly below `theta_open`, and
the printed improvement bound holds.
-/
theorem integral_ceiling_exact :
    integralG3Ceiling = (DeltaOpen - c1 * g1Floor) / c3 ∧
    integralG3Ceiling < thetaOpen ∧
    thetaOpen - integralG3Ceiling < (41 : Rat) / 100000000000 ∧
    (40 : Rat) / 100000000000 < thetaOpen - integralG3Ceiling := by
  native_decide

#print axioms LHahnComplementarityS1.integral_ceiling_exact

/-- The first-moment contribution is negligible against the conserved reserve. -/
theorem first_moment_contribution_small :
    c1 * g1Floor < (76 : Rat) / 10000 ∧
    (75 : Rat) / 10000 < c1 * g1Floor ∧
    c1 * g1Floor < DeltaOpen := by
  native_decide

#print axioms LHahnComplementarityS1.first_moment_contribution_small

/-! ## Integer incidence maxima -/

abbrev lowC : Nat := Bstar * (Bstar - 1) * 5412
abbrev highC : Nat := Bstar * (Bstar - 1) * 840821
abbrev lowTmax : Nat := 1222536914966
abbrev highTmax : Nat := 15238236246526

/--
Each printed total-incidence maximum is the exact integer boundary of the
quadratic (6.4): the maximum itself satisfies it and the next integer does not.
The surplus and the exact-size codeword count follow by integer subtraction.
-/
theorem incidence_maxima_exact :
    lowTmax ^ 2 ≤ N * (lowTmax + lowC) ∧
    ¬ ((lowTmax + 1) ^ 2 ≤ N * ((lowTmax + 1) + lowC)) ∧
    lowTmax - Bstar * mLow = 149030066 ∧
    highTmax ^ 2 ≤ N * (highTmax + highC) ∧
    ¬ ((highTmax + 1) ^ 2 ≤ N * ((highTmax + 1) + highC)) ∧
    highTmax - Bstar * mHigh = 11955691 ∧
    Bstar - 11955691 = 4821524 := by
  native_decide

#print axioms LHahnComplementarityS1.incidence_maxima_exact

/-! ## Radius-100 concentration -/

/-- `Q_star` is the printed quotient of the conserved reserve. -/
theorem qstar_exact :
    Qstar = DeltaOpen / (alpha * ((Bstar : Rat) - 1)) ∧
    (3848647 : Rat) < Qstar ∧ Qstar < 3848648 := by
  native_decide

#print axioms LHahnComplementarityS1.qstar_exact

/-- Allowed intersections at distance at least `100` from all three root shells. -/
def outsideBand (t : Int) : Bool :=
  decide (100 ≤ Int.natAbs (t - 2060)) &&
  decide (100 ≤ Int.natAbs (t - 2061)) &&
  decide (100 ≤ Int.natAbs (t - 5412))

/--
Enumerated over all `5413` allowed intersections: outside the three radius-`99`
bands the shell cubic is at least `32835100`, and that value is attained, so the
printed minimum is exact rather than merely a bound.
-/
theorem radius100_shell_minimum :
    (allowedIntersections.filter outsideBand).all
        (fun t => decide (32835100 ≤ intersectionPoly t)) = true ∧
    (allowedIntersections.filter outsideBand).any
        (fun t => decide (intersectionPoly t = 32835100)) = true ∧
    allowedIntersections.filter (fun t => decide (intersectionPoly t = 32835100)) =
      [2161] := by
  native_decide

#print axioms LHahnComplementarityS1.radius100_shell_minimum

/--
The two printed band fractions hold as the bounds the paper states them to be:
at most `0.1172113851386057` of ordered distinct pairs outside the bands, hence
at least `0.8827886148613943` inside.  The outside value is a strict upper bound
on the exact quotient, not its truncated expansion.
-/
theorem band_fractions_bound :
    Qstar / 32835100 < (1172113851386057 : Rat) / 10000000000000000 ∧
    (8827886148613943 : Rat) / 10000000000000000 < 1 - Qstar / 32835100 ∧
    (1172113851386056 : Rat) / 10000000000000000 < Qstar / 32835100 := by
  native_decide

#print axioms LHahnComplementarityS1.band_fractions_bound

/-! ## Inherited route stops -/

theorem inherited_route_stops_exact :
    (20737821 : Nat) - ell = 3960607 ∧
    (30682446 : Nat) - ell = 13905232 ∧
    ell < 20737821 ∧
    ell < 30682446 := by
  native_decide

#print axioms LHahnComplementarityS1.inherited_route_stops_exact

end LHahnComplementarityS1
