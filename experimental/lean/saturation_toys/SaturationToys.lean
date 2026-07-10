/-!
# Saturation identity toy anchors (W24 M2)

`thm:saturation` (grande_finale): Cen(U;m) = ∑_c C(s_c(U), m).

Tiny combinatorial instances with closed Nat arithmetic (no field model).

Weave: #383; grande_finale thm:saturation / cor:raw-bc-fails.
No sorry. Core Lean only. Dual presentation: `native_decide` and `decide`.
-/

namespace SaturationToys

/-- Toy 1: one ray size 4, m=2 → C(4,2)=6 -/
theorem toy1_C4_2 : (4 * 3) / 2 = 6 := by native_decide

/-- Toy 2: sizes 3 and 2, m=2 → C(3,2)+C(2,2)=3+1=4 -/
theorem toy2_sum : (3 * 2) / 2 + (2 * 1) / 2 = 4 := by native_decide

/-- Toy 3: sizes 5,3,0 m=2 → 10+3+0=13 -/
theorem toy3_sum : (5 * 4) / 2 + (3 * 2) / 2 + 0 = 13 := by native_decide

/-- Second presentation via `decide` -/
theorem toy1' : (4 * 3) / 2 = 6 := by decide
theorem toy2' : 3 + 1 = 4 := by decide
theorem toy3' : 10 + 3 + 0 = 13 := by decide

/-- Named census fold for the identity shape Cen = sum of binoms -/
def binom2 (n : Nat) : Nat := (n * (n - 1)) / 2

def census2 (sizes : List Nat) : Nat :=
  sizes.foldl (fun acc s => acc + binom2 s) 0

theorem census2_toy2 : census2 [3, 2] = 4 := by native_decide
theorem census2_toy3 : census2 [5, 3, 0] = 13 := by native_decide

end SaturationToys
