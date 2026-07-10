/-!
# Deployed-row unsafe/quiet bracket anchors (W37 M1)

Kernel-checked Nat facts for the four deployed-row brackets
`U(a0) > B_*` and `U(a1) ≤ B_*` with `a1 = a0 + 1`, from hard inputs (d)/(e)
packets #520 (profile-envelope) and #521 (lower-reserve).

Source certs:
- `experimental/data/certificates/lower-reserve-unsafe/lower_reserve_unsafe.json`
- `experimental/data/certificates/profile-envelope-vs-target/profile_envelope_vs_target.json`

Hard inputs: (d) complete profile-envelope vs target; (e) lower reserve / unsafe-side.

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Disjoint from holmbuar asymptotic_spine packages.
-/

namespace DeployedBrackets

/-! ## KoalaBear rows (B_* = 274980728111395087) -/

/-- KoalaBear challenge budget B_*. -/
def BStarKB : Nat := 274980728111395087

/-- kb_mca: U(a0=1116047), U(a1=1116048) -/
def U0_kb_mca : Nat := 138634741058327852652
def U1_kb_mca : Nat := 57198030366
def a0_kb_mca : Nat := 1116047
def a1_kb_mca : Nat := 1116048

/-- kb_list: U(a0=1116046), U(a1=1116047) -/
def U0_kb_list : Nat := 157702518233425975347
def U1_kb_list : Nat := 65065153468
def a0_kb_list : Nat := 1116046
def a1_kb_list : Nat := 1116047

/-! ## Mersenne-31 rows (B_* = 16777215) -/

def BStarM31 : Nat := 16777215

/-- m31_mca -/
def U0_m31_mca : Nat := 4281388998575706
def U1_m31_mca : Nat := 1752700
def a0_m31_mca : Nat := 1116023
def a1_m31_mca : Nat := 1116024

/-- m31_list -/
def U0_m31_list : Nat := 4870025984688527
def U1_m31_list : Nat := 1993678
def a0_m31_list : Nat := 1116022
def a1_m31_list : Nat := 1116023

/-! ## Unsafe side: U(a0) > B_*  (hard input e / d) -/

theorem kb_mca_U0_gt_Bstar : U0_kb_mca > BStarKB := by native_decide
theorem kb_list_U0_gt_Bstar : U0_kb_list > BStarKB := by native_decide
theorem m31_mca_U0_gt_Bstar : U0_m31_mca > BStarM31 := by native_decide
theorem m31_list_U0_gt_Bstar : U0_m31_list > BStarM31 := by native_decide

/-! ## Quiet/safe side: U(a1) ≤ B_* -/

theorem kb_mca_U1_le_Bstar : U1_kb_mca ≤ BStarKB := by native_decide
theorem kb_list_U1_le_Bstar : U1_kb_list ≤ BStarKB := by native_decide
theorem m31_mca_U1_le_Bstar : U1_m31_mca ≤ BStarM31 := by native_decide
theorem m31_list_U1_le_Bstar : U1_m31_list ≤ BStarM31 := by native_decide

/-! ## Adjacent agreements: a1 = a0 + 1 -/

theorem kb_mca_adjacent : a1_kb_mca = a0_kb_mca + 1 := by native_decide
theorem kb_list_adjacent : a1_kb_list = a0_kb_list + 1 := by native_decide
theorem m31_mca_adjacent : a1_m31_mca = a0_m31_mca + 1 := by native_decide
theorem m31_list_adjacent : a1_m31_list = a0_m31_list + 1 := by native_decide

/-! ## Strict exceedance gaps at quiet edge: B_* + 1 - U(a1) -/

def gap_kb_mca : Nat := BStarKB + 1 - U1_kb_mca
def gap_kb_list : Nat := BStarKB + 1 - U1_kb_list
def gap_m31_mca : Nat := BStarM31 + 1 - U1_m31_mca
def gap_m31_list : Nat := BStarM31 + 1 - U1_m31_list

theorem gap_kb_mca_value : gap_kb_mca = 274980670913364722 := by native_decide
theorem gap_kb_list_value : gap_kb_list = 274980663046241620 := by native_decide
theorem gap_m31_mca_value : gap_m31_mca = 15024516 := by native_decide
theorem gap_m31_list_value : gap_m31_list = 14783538 := by native_decide

/-- Gaps are positive (U1 < B_*+1 which follows U1 ≤ B_*). -/
theorem gap_kb_mca_pos : gap_kb_mca > 0 := by native_decide
theorem gap_m31_mca_pos : gap_m31_mca > 0 := by native_decide

/-! ## Dual presentation via `decide` -/

theorem kb_mca_U0_gt_Bstar' : U0_kb_mca > BStarKB := by decide
theorem kb_mca_U1_le_Bstar' : U1_kb_mca ≤ BStarKB := by decide
theorem kb_mca_adjacent' : a1_kb_mca = a0_kb_mca + 1 := by decide
theorem gap_kb_mca_value' : gap_kb_mca = 274980670913364722 := by decide

end DeployedBrackets
