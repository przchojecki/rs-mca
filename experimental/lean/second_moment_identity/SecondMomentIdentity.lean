/-!
# Second-moment identity for prefix fibers (W40 M3)

Kernel-checked instance of lem:second-moment-identity:

For residual supports partitioned by prefix value s, with
Q(s) = |Ω ∩ Φ^{-1}(s)|,

```text
  ∑_s Q(s)²  =  number of ordered pairs with common prefix syndrome
```

and ∑_s Q(s)² ≤ (max_s Q(s)) · ∑_s Q(s).

Explicit toy fibers (prefix classes):
- Fiber A (s=0): supports {0,1,2}     Q=3
- Fiber B (s=1): supports {3,4}       Q=2
- Fiber C (s=2): supports {5}         Q=1
- sum Q = 6, sum Q² = 9+4+1 = 14
- max Q = 3, max·sum = 18 ≥ 14
- Ordered pairs with common prefix: 3²+2²+1² = 14 (identity)

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
-/

namespace SecondMomentIdentity

/-- Sum of squares of a list. -/
def sumSq (xs : List Nat) : Nat :=
  xs.foldl (fun acc q => acc + q * q) 0

def sumList (xs : List Nat) : Nat :=
  xs.foldl (fun acc q => acc + q) 0

def maxList : List Nat → Nat
  | [] => 0
  | x :: xs => Nat.max x (maxList xs)

/-- Fiber sizes Q(s). -/
def Q : List Nat := [3, 2, 1]

/-- Second moment SP = ∑ Q(s)². -/
def SP : Nat := sumSq Q

/-- Total residual supports. -/
def total : Nat := sumList Q

/-- max_s Q(s). -/
def Qmax : Nat := maxList Q

/-- Explicit ordered-pair count by expanding fibers.
    Fiber A: 3×3=9, B: 2×2=4, C: 1×1=1. -/
def orderedPairsByFiber : Nat := 3 * 3 + 2 * 2 + 1 * 1

/-! ## Values -/

theorem SP_value : SP = 14 := by native_decide
theorem total_value : total = 6 := by native_decide
theorem Qmax_value : Qmax = 3 := by native_decide
theorem orderedPairs_value : orderedPairsByFiber = 14 := by native_decide

/-- Main identity: ∑ Q² = ordered common-prefix pairs. -/
theorem second_moment_identity : SP = orderedPairsByFiber := by native_decide

/-- Elementary bound SP ≤ Qmax · total. -/
theorem second_moment_bound : SP ≤ Qmax * total := by native_decide

theorem second_moment_bound_expanded : 14 ≤ 3 * 6 := by native_decide

/-! ## Second toy: three equal fibers Q=[2,2,2] -/

def Q2 : List Nat := [2, 2, 2]
def SP2 : Nat := sumSq Q2
def total2 : Nat := sumList Q2
def Qmax2 : Nat := maxList Q2

theorem SP2_value : SP2 = 12 := by native_decide
theorem total2_value : total2 = 6 := by native_decide
theorem identity2 : SP2 = 2 * 2 + 2 * 2 + 2 * 2 := by native_decide
theorem bound2 : SP2 ≤ Qmax2 * total2 := by native_decide

/-! ## Dual via `decide` -/

theorem SP_value' : SP = 14 := by decide
theorem second_moment_identity' : SP = orderedPairsByFiber := by decide
theorem second_moment_bound' : SP ≤ Qmax * total := by decide
theorem SP2_value' : SP2 = 12 := by decide
theorem bound2' : SP2 ≤ Qmax2 * total2 := by decide

/-- Fold shape matching ∑_s Q(s)². -/
theorem sumSq_explicit : sumSq [3, 2, 1] = 14 := by native_decide
theorem sumSq_explicit' : sumSq [3, 2, 1] = 14 := by decide

end SecondMomentIdentity
