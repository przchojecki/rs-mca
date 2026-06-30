import RsMca.Basic

namespace RsMca

/-!
# Finite-row MCA threshold gates (work plan `towards-prize.md` Lane V; Paper 1)

Stdlib-only (no mathlib) formalization of the finite field-count gates that pin the
`eps* = 2^-128` safe/unsafe transition for the solved smooth row

  `C = RS[F_{17^32}, H, 256]`,   `n = |H| = 512`,   `k = 256`,   `rho = 1/2`

(`experimental/notes/thresholds/f17_32_finite_mca_threshold.tex`). The high-agreement
tangent staircase gives the bad-slope numerator `B_fin(C,a) = 513 - a` for `a >= 427`,
and the threshold is decided by where `B_fin(a) * 2^128` crosses `17^32`:
`6 * 2^128 < 17^32 < 7 * 2^128`, i.e. `floor(17^32 / 2^128) = 6`. Hence agreement
`a = 507` is safe and `a = 506` is unsafe (radius `r = 5` safe, `r = 6` unsafe).

These are the Lane V gates V2 (agreement/radius staircase) and V3 (the field-count
inequality). All proofs are kernel `decide` / core `Nat` `div` lemmas — axiom-free
(`#print axioms`: no `sorryAx`, no `native_decide`).
-/

/-! ## V3: the field-count gate -/

/-- V3: `6 * 2^128 < 17^32 < 7 * 2^128` — the gate pinning the 506/507 transition.
    Equivalently `floor(17^32 / 2^128) = 6`. -/
theorem field_count_gate : 6 * 2 ^ 128 < 17 ^ 32 ∧ 17 ^ 32 < 7 * 2 ^ 128 := by decide

/-- Projective-slope variant: the `|F| + 1` denominator gives the same integer
    threshold, since `17^32 + 1 < 7 * 2^128` still holds. -/
theorem field_count_gate_proj : 17 ^ 32 + 1 < 7 * 2 ^ 128 := by decide

/-- `floor(17^32 / 2^128) = 6`, the budget the staircase must clear. -/
theorem field_floor : 17 ^ 32 / 2 ^ 128 = 6 := by decide

/-! ## V2: the agreement/radius staircase -/

/-- The high-agreement bad-slope numerator of the solved row: `B_fin(a) = 513 - a`. -/
def Bfin (a : Nat) : Nat := 513 - a

/-- Scanner table rows (`a >= 427`): `B_fin(506)=7, 507=6, 508=5, 512=1`. -/
theorem Bfin_samples :
    Bfin 506 = 7 ∧ Bfin 507 = 6 ∧ Bfin 508 = 5 ∧ Bfin 512 = 1 := by decide

/-- Core safe/unsafe equivalence: a multiplicity `m` clears the `2^-128` budget
    (`m * 2^128 <= 17^32`) exactly when `m <= 6`. -/
theorem clears_budget_iff (m : Nat) : m * 2 ^ 128 ≤ 17 ^ 32 ↔ m ≤ 6 := by
  rw [← field_floor]
  exact (Nat.le_div_iff_mul_le (by decide)).symm

/-- V2 threshold: in the staircase range, the row is safe at agreement `a`
    (`B_fin(a) * 2^128 <= 17^32`) iff `a >= 507`. So `a = 507` is the exact
    safe threshold and `a = 506` is unsafe. -/
theorem safe_iff_agreement_ge_507 (a : Nat) (h : a ≤ 513) :
    Bfin a * 2 ^ 128 ≤ 17 ^ 32 ↔ 507 ≤ a := by
  rw [Bfin, clears_budget_iff]
  omega

end RsMca
