/-!
# Exact arithmetic of the M31 canonical-remainder barrier

Kernel-checked arithmetic for `experimental/notes/thresholds/m31_remainder_barrier.md`.

Scope, stated because this packet is deliberately not uniform in verification standing. The
stratified inequality of the note's §2 and the abstract map of its §3 are *carried* with their
hypotheses and falsifiers; they are not finite computations and nothing here re-derives them. What
follows checks the arithmetic that those statements imply, which is the whole of the note's §2
corollary and §4 conditional.

Disclosure. Proofs are `rfl` and `decide` on closed numerals; `native_decide` is not used anywhere
in this package, and the `#print axioms` censuses appear at the end. stdlib only, no Mathlib.
-/

namespace M31RemainderBarrier

def Bstar : Nat := 16777215

/-- Binomial coefficients, defined here because the package is stdlib-only. -/
def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

/-! ## The strata coefficients are binomial in one family -/

theorem coeff_495  : binom 12 4 = 495  := by decide
theorem coeff_1287 : binom 13 5 = 1287 := by decide
theorem coeff_1716 : binom 13 6 = 1716 := by decide
theorem coeff_3003 : binom 14 6 = 3003 := by decide
theorem coeff_3432 : binom 14 7 = 3432 := by decide

/-! ## The corollary constant, by both routes -/

/-- Charging the exceptional contributions above `1716` separately. -/
theorem constant_by_exceptions : (3432 - 1716) + 3 * (3003 - 1716) = 5577 := by rfl

/-- The stratified constant with one `1716` absorbed into `r(eta)`. -/
theorem constant_by_absorption : 7293 - 1716 = 5577 := by rfl

theorem constants_agree :
    (3432 - 1716) + 3 * (3003 - 1716) = 7293 - 1716 := by rfl

/-- Every stratum coefficient is at most the absorbing coefficient `1716`. -/
theorem strata_bounded_by_1716 :
    482 ≤ 1716 ∧ 495 ≤ 1716 ∧ 1287 ≤ 1716 ∧ 1716 ≤ 1716 := by decide

/-! ## The barrier -/

/-- The stratified upper bound as a function of the represented-remainder count. -/
def bound (r : Nat) : Nat := 1716 * r + 5577

theorem bound_at_9773 : bound 9773 = 16776045 := by rfl

theorem bound_at_9774 : bound 9774 = 16777761 := by rfl

theorem safe_at_9773 : bound 9773 ≤ Bstar := by decide

theorem slack_at_9773 : Bstar - bound 9773 = 1170 := by rfl

theorem over_at_9774 : ¬ (bound 9774 ≤ Bstar) := by decide

theorem excess_at_9774 : bound 9774 - Bstar = 546 := by rfl

/-- `9773` is exactly the largest represented-remainder count the bound keeps safe. -/
theorem barrier_is_sharp_for_the_bound :
    bound 9773 ≤ Bstar ∧ ¬ (bound 9774 ≤ Bstar) := by decide

/-! ## The conditional out-of-band signature, given the open hypothesis `H_1237` -/

/-- In-band capacity under a uniform `1237` cap on the `181` shells of `33..213`. -/
theorem in_band_capacity : 181 * 1237 = 223897 := by rfl

/-- Out-of-band mass forced in an unsafe fiber. -/
theorem out_of_band_mass : Bstar - 223897 = 16553318 := by rfl

/-- Pigeonhole over the `266` out-of-band shells. -/
theorem out_of_band_pigeonhole : 16553318 = 266 * 62230 + 138 := by rfl

/-- Hence some out-of-band shell has degree at least `62231`. -/
theorem out_of_band_shell_floor : 266 * 62230 < 16553318 ∧ 62230 + 1 = 62231 := by decide

/-- The shell counts partition the admissible range. -/
theorem shell_split : 181 + 266 = 447 := by rfl

/-! ## Axiom censuses -/

#print axioms coeff_495
#print axioms coeff_1287
#print axioms coeff_1716
#print axioms coeff_3003
#print axioms coeff_3432
#print axioms constant_by_exceptions
#print axioms constant_by_absorption
#print axioms constants_agree
#print axioms strata_bounded_by_1716
#print axioms bound_at_9773
#print axioms bound_at_9774
#print axioms safe_at_9773
#print axioms slack_at_9773
#print axioms over_at_9774
#print axioms excess_at_9774
#print axioms barrier_is_sharp_for_the_bound
#print axioms in_band_capacity
#print axioms out_of_band_mass
#print axioms out_of_band_pigeonhole
#print axioms out_of_band_shell_floor
#print axioms shell_split

end M31RemainderBarrier
