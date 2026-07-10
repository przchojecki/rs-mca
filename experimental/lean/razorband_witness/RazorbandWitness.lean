/-!
# Universal tangent floor instance (W41 M3)

Serves **K5 razor-band witness kernel** (proved sub-fact; band closure
open). K5 prices deficit-side witnesses through the rate-1/2 band; an
upper-bound kernel cannot serve that node. The proved finite floor used
here is the elementary MCA lower bound:

Source label: prop:universal-tangent-floor / eq:tangent-floor (frontiers):
  B_{C,Γ}^{MCA}(a) ≥ min{|Γ|, n−a+1}

for every RS code, every a ≥ k+1, every nonempty Γ ⊆ F.

Explicit toys:
1. n=7, a=4, |Γ|=5 → min(5, 7−4+1)=min(5,4)=4
2. n=6, a=5, |Γ|=2 → min(2, 6−5+1)=min(2,2)=2
3. n=8, a=6, |Γ|=10 → min(10, 3)=3

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Nonclaim: does NOT close the rate-1/2 razor band; only anchors the
proved tangent-floor lower bound used on the deficit side.
-/

namespace RazorbandWitness

/-- Serves K5 razor-band witness kernel (proved sub-fact; band closure open). -/

def minNat (x y : Nat) : Nat := if x ≤ y then x else y

/-- Toy 1. -/
def n1 : Nat := 7
def a1 : Nat := 4
def Gamma1 : Nat := 5
def floor1 : Nat := minNat Gamma1 (n1 - a1 + 1)

theorem floor1_value : floor1 = 4 := by native_decide
theorem floor1_expanded : minNat 5 (7 - 4 + 1) = 4 := by native_decide
theorem floor1_le_Gamma : floor1 ≤ Gamma1 := by native_decide
theorem floor1_le_redundancy : floor1 ≤ n1 - a1 + 1 := by native_decide

/-- Toy 2. -/
def n2 : Nat := 6
def a2 : Nat := 5
def Gamma2 : Nat := 2
def floor2 : Nat := minNat Gamma2 (n2 - a2 + 1)

theorem floor2_value : floor2 = 2 := by native_decide
theorem floor2_tight : floor2 = Gamma2 := by native_decide

/-- Toy 3. -/
def n3 : Nat := 8
def a3 : Nat := 6
def Gamma3 : Nat := 10
def floor3 : Nat := minNat Gamma3 (n3 - a3 + 1)

theorem floor3_value : floor3 = 3 := by native_decide
theorem floor3_is_redundancy : floor3 = n3 - a3 + 1 := by native_decide

/-- a ≥ k+1 shape: for k=2, a=4 is admissible on toy 1. -/
def k1 : Nat := 2
theorem a_ge_k_plus_1 : a1 ≥ k1 + 1 := by native_decide

/-- Positivity: floors are positive (nonempty witness lower bounds). -/
theorem floor1_pos : floor1 > 0 := by native_decide
theorem floor2_pos : floor2 > 0 := by native_decide
theorem floor3_pos : floor3 > 0 := by native_decide

/-! ## Dual via `decide` -/

theorem floor1_value' : floor1 = 4 := by decide
theorem floor2_value' : floor2 = 2 := by decide
theorem floor3_value' : floor3 = 3 := by decide
theorem a_ge_k_plus_1' : a1 ≥ k1 + 1 := by decide
theorem floor1_pos' : floor1 > 0 := by decide

end RazorbandWitness
