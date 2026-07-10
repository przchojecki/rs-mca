/-!
# Deep-regime upper bound (W45 M1)

Maps to **hard input (a)/(d)** deep exact regime / profile envelope.

Source labels (frontiers draft — grepped before writing):
- thm:deep-regime-upper L1790
- eq:deep-upper L1795 (tag 3.5): if 3r ≤ d−1 then B_MCA(a) ≤ r+1

For RS_F(D,k): d = n−k+1 (MDS). Hyp and bound are Nat comparisons;
B_MCA machinery not rebuilt (honest Nonclaim).

Instances:
1. Boundary 3r = d−1: n=8,k=2,d=7,a=6,r=2; 6≤6; bound=3
2. Strict hyp: n=8,k=2,d=7,a=7,r=1; 3≤6; bound=2
3. Different params: n=10,k=3,d=8,a=8,r=2; 6≤7; bound=3

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
-/

namespace DeepRegimeUpper

-- Hard input (a)/(d): deep-regime upper bound.

/-! ## Instance 1 — tight boundary 3r = d−1 -/

def n1 : Nat := 8
def k1 : Nat := 2
def a1 : Nat := 6
def d1 : Nat := n1 - k1 + 1
def r1 : Nat := n1 - a1
def bound1 : Nat := r1 + 1

theorem d1_value : d1 = 7 := by native_decide
theorem r1_value : r1 = 2 := by native_decide
theorem hyp1_tight : 3 * r1 = d1 - 1 := by native_decide
theorem hyp1 : 3 * r1 ≤ d1 - 1 := by native_decide
theorem bound1_value : bound1 = 3 := by native_decide
/-- AD conclusion value: B_MCA(a) ≤ r+1 = 3 on this instance. -/
theorem deep_upper_1 : bound1 = r1 + 1 := by native_decide

/-! ## Instance 2 — strict hypothesis, smaller r -/

def n2 : Nat := 8
def k2 : Nat := 2
def a2 : Nat := 7
def d2 : Nat := n2 - k2 + 1
def r2 : Nat := n2 - a2
def bound2 : Nat := r2 + 1

theorem d2_value : d2 = 7 := by native_decide
theorem r2_value : r2 = 1 := by native_decide
theorem hyp2 : 3 * r2 ≤ d2 - 1 := by native_decide
theorem hyp2_strict : 3 * r2 < d2 - 1 := by native_decide
theorem bound2_value : bound2 = 2 := by native_decide
theorem deep_upper_2 : bound2 = r2 + 1 := by native_decide

/-! ## Instance 3 — different (n,k) -/

def n3 : Nat := 10
def k3 : Nat := 3
def a3 : Nat := 8
def d3 : Nat := n3 - k3 + 1
def r3 : Nat := n3 - a3
def bound3 : Nat := r3 + 1

theorem d3_value : d3 = 8 := by native_decide
theorem r3_value : r3 = 2 := by native_decide
theorem hyp3 : 3 * r3 ≤ d3 - 1 := by native_decide
theorem bound3_value : bound3 = 3 := by native_decide
theorem deep_upper_3 : bound3 = r3 + 1 := by native_decide

/-! ## RS MDS distance formula shared shape -/

theorem mds_d_formula : n1 - k1 + 1 = d1 := by native_decide
theorem r_formula : n1 - a1 = r1 := by native_decide

/-! ## Dual via `decide` -/

theorem hyp1' : 3 * r1 ≤ d1 - 1 := by decide
theorem hyp1_tight' : 3 * r1 = d1 - 1 := by decide
theorem hyp2' : 3 * r2 ≤ d2 - 1 := by decide
theorem hyp3' : 3 * r3 ≤ d3 - 1 := by decide
theorem bound1_value' : bound1 = 3 := by decide
theorem bound2_value' : bound2 = 2 := by decide
theorem bound3_value' : bound3 = 3 := by decide

end DeepRegimeUpper
