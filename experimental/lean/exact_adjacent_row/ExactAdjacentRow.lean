/-!
# Exact first adjacent row (W44 M2)

Maps to **hard input (d)** profile-envelope / **(e)** adjacent-row comparison.

Source labels (frontiers draft — grepped before writing):
- thm:exact-first-adjacent-row L1870
- AD1: B_C^{MCA}(k+1) = M when |F| > Q_sep(M)
  with M = C(n,k+1), Q_sep(M) = max{M, C(M,2)}

Explicit toy RS parameters:
- n=4, k=1 ⇒ M = C(4,2) = 6
- Q_sep(M) = max{6, C(6,2)} = max{6, 15} = 15
- Concrete |F| = 16 > 15 (gate holds)
- Theorem conclusion on this instance: B_MCA(k+1) = B_MCA(2) = M = 6

Honest Nonclaim: anchors the gate arithmetic and the stated equality
value M; does not rebuild the full MCA maximizer over lines.

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Complements deployed-brackets #532.
-/

namespace ExactAdjacentRow

-- Hard inputs (d)/(e): exact first adjacent row AD1.

def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n (k + 1) + binom n k

def maxNat (x y : Nat) : Nat := if x ≥ y then x else y

def n : Nat := 4
def k : Nat := 1
def R : Nat := n - k

/-- M = C(n, k+1) = C(n, R-1). -/
def M : Nat := binom n (k + 1)

/-- Q_sep(M) = max{M, C(M,2)}. -/
def Qsep : Nat := maxNat M (binom M 2)

/-- Concrete separating field size. -/
def Fsize : Nat := 16

/-- Anchored AD1 value: B_MCA(k+1) = M under the gate. -/
def B_MCA_kp1 : Nat := M

/-! ## Parameter arithmetic -/

theorem R_value : R = 3 := by native_decide
theorem M_value : M = 6 := by native_decide
theorem binom_4_2 : binom 4 2 = 6 := by native_decide
theorem binom_6_2 : binom 6 2 = 15 := by native_decide
theorem Qsep_value : Qsep = 15 := by native_decide
theorem Qsep_is_binomM2 : Qsep = binom M 2 := by native_decide

/-- Field-size gate |F| > Q_sep(M). -/
theorem field_gate : Fsize > Qsep := by native_decide
theorem field_gate_expanded : 16 > 15 := by native_decide

/-- AD1 conclusion on this instance: B_MCA(k+1) = M. -/
theorem AD1_value : B_MCA_kp1 = M := by native_decide
theorem AD1_expanded : B_MCA_kp1 = 6 := by native_decide

/-! ## Second toy: n=3, k=1, M=3, Qsep=3, |F|=4 -/

def n2 : Nat := 3
def k2 : Nat := 1
def M2 : Nat := binom n2 (k2 + 1)
def Qsep2 : Nat := maxNat M2 (binom M2 2)
def Fsize2 : Nat := 4

theorem M2_value : M2 = 3 := by native_decide
theorem Qsep2_value : Qsep2 = 3 := by native_decide
theorem field_gate2 : Fsize2 > Qsep2 := by native_decide
theorem AD1_toy2 : M2 = 3 := by native_decide

/-! ## Adjacent-threshold shape (AD2 constants, not the a* decision) -/

/-- binom(n, R-2) for n=4, R=3: C(4,1)=4; band 4 ≤ b < 6 for a*=k+2. -/
def binom_n_Rminus2 : Nat := binom n (R - 2)
theorem binom_n_Rminus2_value : binom_n_Rminus2 = 4 := by native_decide
theorem AD2_band_nonempty : binom_n_Rminus2 < M := by native_decide

/-! ## Dual via `decide` -/

theorem M_value' : M = 6 := by decide
theorem Qsep_value' : Qsep = 15 := by decide
theorem field_gate' : Fsize > Qsep := by decide
theorem AD1_value' : B_MCA_kp1 = M := by decide
theorem field_gate2' : Fsize2 > Qsep2 := by decide
theorem AD2_band_nonempty' : binom_n_Rminus2 < M := by decide

end ExactAdjacentRow
