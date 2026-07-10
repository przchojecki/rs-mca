/-!
# Syndrome-line normal form uniqueness (W43 M1)

Maps to **hard input (a)** first-match atlas / **(c)** ray compiler incidence.

Source labels (frontiers draft — grepped before writing):
- prop:syndrome-line-normal-form L1570
- eq:syndrome-line L1578 (tag 3.2)

Exact conclusion instantiated: for fixed E, at most one finite slope γ with
  s(u0)+γ s(u1) ∈ V_E  and  {s(u0),s(u1)} ⊄ V_E.

Explicit toy (F_5, R=2):
- Syndrome space F_5² with coords mod 5
- V_E = span{(1,0)} = {(a,0) : a ∈ F_5}  (rational-normal column at x=0)
- s0 = (1,1), s1 = (0,1)
- Non-containment: neither s0 nor s1 lies in V_E
- Enumerate γ∈{0,1,2,3,4}: unique bad slope γ=4
  (s0+4·s1 = (1,0) ∈ V_E)

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
-/

namespace SyndromeLine

-- Hard inputs (a)/(c): syndrome-line incidence uniqueness.

def q : Nat := 5

def add (x y : Nat) : Nat := (x + y) % q
def mul (x y : Nat) : Nat := (x * y) % q

/-- Syndrome vectors as (coord0, coord1). -/
def s0 : Nat × Nat := (1, 1)
def s1 : Nat × Nat := (0, 1)

/-- V_E = span{(1,0)}: second coordinate zero. -/
def inVE (v : Nat × Nat) : Bool := v.2 == 0

/-- Line point s0 + γ·s1. -/
def linePt (γ : Nat) : Nat × Nat :=
  (add s0.1 (mul γ s1.1), add s0.2 (mul γ s1.2))

/-- {s0,s1} ⊆ V_E iff both generators in V_E. -/
def bothInVE : Bool := inVE s0 && inVE s1

/-- MCA-bad on S=D\E per eq:syndrome-line. -/
def isBad (γ : Nat) : Bool :=
  inVE (linePt γ) && !bothInVE

def gammas : List Nat := [0, 1, 2, 3, 4]

def countBad : Nat :=
  gammas.foldl (fun acc γ => if isBad γ then acc + 1 else acc) 0

/-! ## Non-containment hypothesis -/

theorem s0_not_in_VE : inVE s0 = false := by native_decide
theorem s1_not_in_VE : inVE s1 = false := by native_decide
theorem nonContainment : bothInVE = false := by native_decide

/-! ## Unique bad slope γ = 4 -/

theorem linePt_4 : linePt 4 = (1, 0) := by native_decide
theorem isBad_4 : isBad 4 = true := by native_decide
theorem isBad_0 : isBad 0 = false := by native_decide
theorem isBad_1 : isBad 1 = false := by native_decide
theorem isBad_2 : isBad 2 = false := by native_decide
theorem isBad_3 : isBad 3 = false := by native_decide

theorem countBad_value : countBad = 1 := by native_decide

/-- Main instance of prop:syndrome-line-normal-form uniqueness. -/
theorem uniqueness : countBad ≤ 1 := by native_decide
theorem uniqueness_exact : countBad = 1 := by native_decide

/-! ## Dual via `decide` -/

theorem nonContainment' : bothInVE = false := by decide
theorem countBad_value' : countBad = 1 := by decide
theorem uniqueness' : countBad ≤ 1 := by decide
theorem isBad_4' : isBad 4 = true := by decide
theorem linePt_4' : linePt 4 = (1, 0) := by decide

end SyndromeLine
