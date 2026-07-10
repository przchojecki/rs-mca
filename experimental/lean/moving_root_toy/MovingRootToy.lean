/-!
# Moving-root bound on an explicit F_5 pencil (W38 M2)

Kernel-checked instance of prop:split-pencil-payment / eq:moving-root-bound
(thm:bc-moving-root incidence form):

```text
|Z| ≤ floor((n − g) / h)
```

Explicit toy:
- Field F_5 = {0,1,2,3,4}
- Domain D = F_5, n = 5
- A(X) = X², B(X) = X
- G = gcd = X (common zeros on D: {0}), g = 1
- Moving points: {1,2,3,4}
- Projective parameters: affine (1,t) for t∈F_5 and infinity (0,1)
- h = 1: Z = { params with ≥1 moving root }

Enumeration (machine-checked below):
- (1,0): 0 moving roots
- (1,1): 1  (x=4)
- (1,2): 1  (x=3)
- (1,3): 1  (x=2)
- (1,4): 1  (x=1)
- (0,1): 0  (pure B vanishes only at 0 ∉ moving)

So |Z| = 4 and floor((5−1)/1) = 4, hence |Z| ≤ bound.

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Disjoint from asymptotic_spine and from W37 Nat-only anchors.
-/

namespace MovingRootToy

/-- Field size / domain size. -/
def q : Nat := 5
def n : Nat := 5
def g : Nat := 1
def h : Nat := 1

/-- A(x) = x² mod 5. -/
def evalA (x : Nat) : Nat := (x * x) % 5

/-- B(x) = x mod 5. -/
def evalB (x : Nat) : Nat := x % 5

/-- Moving points D \ Z(G) = {1,2,3,4}. -/
def moving : List Nat := [1, 2, 3, 4]

/-- Does s·A(x) + t·B(x) vanish mod 5? -/
def vanishes (s t x : Nat) : Bool :=
  ((s * evalA x + t * evalB x) % 5) == 0

/-- Number of moving roots for parameter (s,t). -/
def countMoving (s t : Nat) : Nat :=
  moving.foldl (fun acc x => if vanishes s t x then acc + 1 else acc) 0

/-- Projective parameters: affine chart s=1 and infinity (0,1). -/
def params : List (Nat × Nat) :=
  [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (0, 1)]

/-- |Z|: number of parameters with at least h moving roots. -/
def nWithH : Nat :=
  params.foldl
    (fun acc p => if countMoving p.1 p.2 ≥ h then acc + 1 else acc) 0

/-- Bound floor((n-g)/h). -/
def bound : Nat := (n - g) / h

/-! ## Intermediate root counts (explicit table) -/

theorem count_1_0 : countMoving 1 0 = 0 := by native_decide
theorem count_1_1 : countMoving 1 1 = 1 := by native_decide
theorem count_1_2 : countMoving 1 2 = 1 := by native_decide
theorem count_1_3 : countMoving 1 3 = 1 := by native_decide
theorem count_1_4 : countMoving 1 4 = 1 := by native_decide
theorem count_0_1 : countMoving 0 1 = 0 := by native_decide

/-! ## Bound ingredients -/

theorem bound_value : bound = 4 := by native_decide
theorem nWithH_value : nWithH = 4 := by native_decide

/-- Main instance: moving-root bound holds on this pencil. -/
theorem moving_root_bound_instance : nWithH ≤ bound := by native_decide

/-- Equivalent expanded form. -/
theorem moving_root_bound_expanded : 4 ≤ 4 := by native_decide

/-- Domain / gcd sizes. -/
theorem n_value : n = 5 := by native_decide
theorem g_value : g = 1 := by native_decide
theorem moving_length : moving.length = 4 := by native_decide
theorem n_minus_g : n - g = 4 := by native_decide

/-! ## Dual presentation via `decide` -/

theorem count_1_1' : countMoving 1 1 = 1 := by decide
theorem nWithH_value' : nWithH = 4 := by decide
theorem bound_value' : bound = 4 := by decide
theorem moving_root_bound_instance' : nWithH ≤ bound := by decide
theorem moving_root_bound_expanded' : 4 ≤ 4 := by decide

/-- Sanity: each of the four nonzero affine slopes hits exactly one moving root. -/
theorem four_affine_hits :
    countMoving 1 1 + countMoving 1 2 + countMoving 1 3 + countMoving 1 4 = 4 := by
  native_decide

theorem four_affine_hits' :
    countMoving 1 1 + countMoving 1 2 + countMoving 1 3 + countMoving 1 4 = 4 := by
  decide

end MovingRootToy
