/-!
# Exact syndrome–secant compiler instance (W43 M2)

Maps to **hard input (a)** first-match atlas / **(c)** ray compiler.

Source labels (frontiers draft — grepped before writing):
- thm:syndrome-secant-exact L1607
- eq:transverse-secant-count L1615 (tag 3.3)
- eq:exact-secant-numerator L1621 (tag 3.4)

Finite conclusions instantiated:
1. For each fixed E, at most one transverse intersection parameter γ
2. Exact Θ_t count for a concrete (y0,y1): number of γ that hit some
   V_E with |E|≤t and transverse non-containment

Explicit toy (same F_5² as M1):
- t=1, D-points {0,1,2,3,4}, columns h_x=(1,x)
- V_∅ = {0}; V_{{x}} = span{(1,x)} = {(a, a·x)}
- y0=(1,1), y1=(0,1)
- Per-E uniqueness: each E contributes ≤1 γ
- Global Θ: γ∈{0,1,2,3,4} each hits a distinct singleton E
  ⇒ Θ_1(y0,y1) = 5

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
-/

namespace SyndromeSecant

-- Hard inputs (a)/(c): transverse secant incidence count.

def q : Nat := 5

def add (x y : Nat) : Nat := (x + y) % q
def mul (x y : Nat) : Nat := (x * y) % q

def y0 : Nat × Nat := (1, 1)
def y1 : Nat × Nat := (0, 1)

def linePt (γ : Nat) : Nat × Nat :=
  (add y0.1 (mul γ y1.1), add y0.2 (mul γ y1.2))

/-- V_∅ = {0}. -/
def inVEmpty (v : Nat × Nat) : Bool := v.1 == 0 && v.2 == 0

/-- V_{{x}} = span{(1,x)}. -/
def inVPoint (x : Nat) (v : Nat × Nat) : Bool := v.2 == mul v.1 x

def transverse (inV : Nat × Nat → Bool) : Bool :=
  !(inV y0 && inV y1)

def hitsEmpty (γ : Nat) : Bool :=
  inVEmpty (linePt γ) && transverse inVEmpty

def hitsPoint (x γ : Nat) : Bool :=
  inVPoint x (linePt γ) && transverse (inVPoint x)

def gammas : List Nat := [0, 1, 2, 3, 4]
def points : List Nat := [0, 1, 2, 3, 4]

/-- Count γ with hitsEmpty. -/
def countEmpty : Nat :=
  gammas.foldl (fun acc γ => if hitsEmpty γ then acc + 1 else acc) 0

/-- Count γ with hitsPoint x. -/
def countPoint (x : Nat) : Nat :=
  gammas.foldl (fun acc γ => if hitsPoint x γ then acc + 1 else acc) 0

/-- γ is in Θ if it hits empty or some singleton. -/
def inTheta (γ : Nat) : Bool :=
  hitsEmpty γ ||
    points.foldl (fun acc x => acc || hitsPoint x γ) false

def Theta : Nat :=
  gammas.foldl (fun acc γ => if inTheta γ then acc + 1 else acc) 0

/-! ## Per-E uniqueness (thm:syndrome-secant-exact fixed-E clause) -/

theorem countEmpty_le_1 : countEmpty ≤ 1 := by native_decide
theorem countEmpty_value : countEmpty = 0 := by native_decide

theorem countPoint0_le_1 : countPoint 0 ≤ 1 := by native_decide
theorem countPoint1_le_1 : countPoint 1 ≤ 1 := by native_decide
theorem countPoint2_le_1 : countPoint 2 ≤ 1 := by native_decide
theorem countPoint3_le_1 : countPoint 3 ≤ 1 := by native_decide
theorem countPoint4_le_1 : countPoint 4 ≤ 1 := by native_decide

theorem countPoint0_value : countPoint 0 = 1 := by native_decide
theorem countPoint1_value : countPoint 1 = 1 := by native_decide
theorem countPoint2_value : countPoint 2 = 1 := by native_decide
theorem countPoint3_value : countPoint 3 = 1 := by native_decide
theorem countPoint4_value : countPoint 4 = 1 := by native_decide

/-! ## Exact Θ_t count for this (y0,y1) -/

theorem Theta_value : Theta = 5 := by native_decide
theorem Theta_full : Theta = q := by native_decide

/-- Explicit which γ hits which singleton E={x}: γ = x-1 mod 5 for our y. -/
theorem hits_0_at_4 : hitsPoint 0 4 = true := by native_decide
theorem hits_1_at_0 : hitsPoint 1 0 = true := by native_decide
theorem hits_2_at_1 : hitsPoint 2 1 = true := by native_decide
theorem hits_3_at_2 : hitsPoint 3 2 = true := by native_decide
theorem hits_4_at_3 : hitsPoint 4 3 = true := by native_decide

/-- Transverse non-containment for the generators vs V_{{0}}. -/
theorem transverse_pt0 : transverse (inVPoint 0) = true := by native_decide

/-! ## Dual via `decide` -/

theorem countEmpty_le_1' : countEmpty ≤ 1 := by decide
theorem countPoint0_le_1' : countPoint 0 ≤ 1 := by decide
theorem Theta_value' : Theta = 5 := by decide
theorem hits_0_at_4' : hitsPoint 0 4 = true := by decide
theorem hits_1_at_0' : hitsPoint 1 0 = true := by decide

end SyndromeSecant
