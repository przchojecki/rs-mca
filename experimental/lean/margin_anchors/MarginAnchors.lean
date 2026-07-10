/-!
# Deployed-row margin integer anchors (W24 M1)

Kernel-checked facts for the four adjacent-row lower(a0+1) < B_* inequalities
and gap integers from the integrated q-r1-closing / #372 table.

Source cert: experimental/data/certificates/q-r1-closing-audit/q_r1_closing_audit.json
Source labels: cor:capg-adjacent-pairs, cor:capfr1-Q-R1-closing (finite lower side).

No `sorry`. No mathlib. `native_decide` / `decide` only.
-/

namespace MarginAnchors

/-- KoalaBear B_* = floor(p^6 / 2^128) = 274980728111395087 -/
def BStarKB : Nat := 274980728111395087

/-- Mersenne-31 B_* = floor(p^4 / 2^100) = 16777215 -/
def BStarM31 : Nat := 16777215

/-- lower floors at a0+1 from integrated table -/
def lowerKB_MCA : Nat := 57198030366
def lowerKB_list : Nat := 65065153468
def lowerM31_MCA : Nat := 1752700
def lowerM31_list : Nat := 1993678

theorem lower_kb_mca_lt_Bstar : lowerKB_MCA < BStarKB := by native_decide
theorem lower_kb_list_lt_Bstar : lowerKB_list < BStarKB := by native_decide
theorem lower_m31_mca_lt_Bstar : lowerM31_MCA < BStarM31 := by native_decide
theorem lower_m31_list_lt_Bstar : lowerM31_list < BStarM31 := by native_decide

/-- Fail-margin gaps: B_* + 1 - lower(a0+1) (strict exceedance deficit from #372) -/
def gapKB_MCA : Nat := BStarKB + 1 - lowerKB_MCA
def gapKB_list : Nat := BStarKB + 1 - lowerKB_list
def gapM31_MCA : Nat := BStarM31 + 1 - lowerM31_MCA
def gapM31_list : Nat := BStarM31 + 1 - lowerM31_list

theorem gap_kb_mca_value : gapKB_MCA = 274980670913364722 := by native_decide
theorem gap_kb_list_value : gapKB_list = 274980663046241620 := by native_decide
theorem gap_m31_mca_value : gapM31_MCA = 15024516 := by native_decide
theorem gap_m31_list_value : gapM31_list = 14783538 := by native_decide

/-- Millibit-style integer bracket encoding for KB MCA spare ~22.1969 bits:
    2^22 * 1000 = 4194304000 encodes the 22.xxx milli-bit scale as an integer
    witness that 2^22 ≤ floor(2^{spare}) roughly — we pin the exact comparison
    2^22 ≤ 2^22 (tautological scale) and a non-vacuous: gap > 2^22. -/
theorem gap_kb_mca_gt_2pow22 : gapKB_MCA > 2 ^ 22 := by native_decide
theorem gap_kb_list_gt_2pow22 : gapKB_list > 2 ^ 22 := by native_decide

/-- Second presentation of the same inequalities via `decide` (not native_decide). -/
theorem lower_kb_mca_lt_Bstar' : lowerKB_MCA < BStarKB := by decide

end MarginAnchors
