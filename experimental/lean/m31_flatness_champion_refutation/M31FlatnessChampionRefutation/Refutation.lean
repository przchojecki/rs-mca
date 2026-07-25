/-!
# Exact arithmetic of the M31 depth-32 shell counterexample

Kernel-checked exact arithmetic for every claim line of
`experimental/notes/thresholds/m31_flatness_champion_refutation.md`.

Scope. This module checks *arithmetic*, not enumeration. The two enumerated inputs — the
`12` complete-`T_16` mixed supports at deficiency `192`, and the incidence distribution of that
sector over all `3432` whole-`T_64` anchors — enter here as recorded values, exactly as printed in
the note. Nothing below asserts that those enumerations were performed by this file.

Disclosure. Proofs are by `rfl` and by `decide` on closed numerals and on a closed list of
numerals; no `native_decide` is used anywhere in this module, and no axioms beyond the ones the
`#print axioms` censuses at the end display. stdlib only, no Mathlib.
-/

namespace M31FlatnessChampionRefutation

/-! ## Frozen row constants -/

/-- The deployed budget for the Mersenne-31 list stress row at `2^-100`. -/
def Bstar : Nat := 16777215

/-- Admissible deficiencies: `479 - 32`, the Newton wall removing `1..32`. -/
def admissibleShells : Nat := 447

/-- The integrated coefficient-four ambient term `floor(4M/Q)`. -/
def ambient : Nat := 14456476

/-- The compiler total for a uniform per-shell intercept `b`. -/
def compilerTotal (b : Nat) : Nat := 1 + b * admissibleShells + ambient

/-! ## Support arithmetic -/

theorem support_from_T16_classes : 29 * 16 + 15 = 479 := by rfl

theorem support_from_T64_classes : 7 * 64 + 31 = 479 := by rfl

theorem admissible_shells_eq : 479 - 32 = admissibleShells := by rfl

/-! ## The refuting packet -/

/-- Binomial coefficients, defined here because the package is stdlib-only. -/
def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

/-- The whole-`T_64` triple-exchange family at deficiency `192` has `C(7,3)^2` members. -/
theorem whole_family_at_192 : binom 7 3 * binom 7 3 = 1225 := by decide

/-- The whole-block family over all deficiencies has `C(14,7)` members. -/
theorem whole_family_total : binom 14 7 = 3432 := by decide

/-- The packet: `1225` whole-`T_64` exchanges together with `12` mixed supports. -/
theorem packet_identity : 1225 + 12 = 1237 := by rfl

/-- Deficiency `192` lies inside the declared band `33..213`. -/
theorem band_membership : 33 ≤ 192 ∧ 192 ≤ 213 := by decide

/-- The packet strictly exceeds the refuted cap, with excess exactly `4`. -/
theorem strict_excess : 1233 < 1237 ∧ 1237 - 1233 = 4 := by decide

/-- The corresponding out-of-band floor at deficiency `256`. -/
theorem out_of_band_floor : 1225 + 18 = 1243 := by rfl

/-! ## Compiler recalibration -/

theorem total_at_1233 : compilerTotal 1233 = 15007628 := by rfl

theorem total_at_1237 : compilerTotal 1237 = 15009416 := by rfl

theorem total_at_5191 : compilerTotal 5191 = 16776854 := by rfl

theorem total_at_5192 : compilerTotal 5192 = 16777301 := by rfl

/-- The forced intercept still fits the budget. -/
theorem forced_intercept_safe : compilerTotal 1237 ≤ Bstar := by decide

/-- Its exact reserve. -/
theorem forced_intercept_reserve : Bstar - compilerTotal 1237 = 1767799 := by rfl

/-- The refutation costs exactly this much reserve. -/
theorem reserve_cost : compilerTotal 1237 - compilerTotal 1233 = 1788 := by rfl

/-- The previously certified edge is unchanged: `5191` fits and `5192` does not. -/
theorem edge_unchanged : compilerTotal 5191 ≤ Bstar ∧ ¬ (compilerTotal 5192 ≤ Bstar) := by decide

/-! ## The recorded incidence census

`incidenceCensus` records, as `(incidence, anchors)` pairs, the distribution of mixed
deficiency-`192` incidence over the whole-`T_64` anchor family, exactly as printed in the note.
-/

def incidenceCensus : List (Nat × Nat) :=
  [(0, 406), (2, 492), (3, 312), (4, 82), (5, 332), (6, 522),
   (8, 460), (9, 304), (10, 86), (11, 312), (12, 124)]

/-- The census is complete: its counts exhaust the whole-`T_64` anchor family. -/
theorem census_total : (incidenceCensus.map Prod.snd).foldl (· + ·) 0 = 3432 := by decide

/-- The census covers exactly the same family the binomial identity counts. -/
theorem census_total_eq_family :
    (incidenceCensus.map Prod.snd).foldl (· + ·) 0 = binom 14 7 := by decide

/-- Every recorded incidence is at most `12`. -/
theorem census_max_le : ∀ p ∈ incidenceCensus, p.fst ≤ 12 := by decide

/-- The value `12` is attained, by `124` anchors. -/
theorem census_max_attained : (12, 124) ∈ incidenceCensus := by decide

/-- The superseded summary value `8` is not the maximum of this census. -/
theorem stale_summary_refuted : ∃ p ∈ incidenceCensus, 8 < p.fst := by decide

/-! ## Axiom censuses -/

#print axioms support_from_T16_classes
#print axioms support_from_T64_classes
#print axioms admissible_shells_eq
#print axioms whole_family_at_192
#print axioms whole_family_total
#print axioms packet_identity
#print axioms band_membership
#print axioms strict_excess
#print axioms out_of_band_floor
#print axioms total_at_1233
#print axioms total_at_1237
#print axioms total_at_5191
#print axioms total_at_5192
#print axioms forced_intercept_safe
#print axioms forced_intercept_reserve
#print axioms reserve_cost
#print axioms edge_unchanged
#print axioms census_total
#print axioms census_total_eq_family
#print axioms census_max_le
#print axioms census_max_attained
#print axioms stale_summary_refuted

end M31FlatnessChampionRefutation
