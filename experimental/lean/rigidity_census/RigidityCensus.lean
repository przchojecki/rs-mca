/-!
# Prefix-rigidity instance + largest-fiber first-moment (W41-FIX M1)

Serves **K2* enlarged rigidity kernel**.

Source labels (frontiers draft):
- prop:prefix-rigidity-full (L2045): two distinct m-sets in one depth-w
  prefix fiber have Johnson distance d_J ≥ w+1
- lem:largest-fiber-log-detail: ∑ N(z)² ≤ (max N) · ∑ N(z)  (q=2 upper side)

Real instance of prop:prefix-rigidity-full:
- m=3, w=1, domain indices in F (combinatorial)
- Explicit m-sets M={0,1,4}, M'={0,2,3} (sorted Lists)
- Shared depth-w=1 prefix witness: equal elementary sum e1 (locator
  coefficient after leading) — e1(M)=0+1+4=5=e1(M')
- Johnson distance d_J = |M \ M'| = |{1,4}| = 2 ≥ w+1 = 2

Kept: largest-fiber first-moment on N=[5,3,2] and tight [4,4,4].

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Disjoint from anticode_packing (#540 packing-cap form of the same prop).
-/

namespace RigidityCensus

-- Serves K2* enlarged rigidity kernel.

/-! ## prop:prefix-rigidity-full instance -/

def m : Nat := 3
def w : Nat := 1
def jBound : Nat := w + 1

/-- Explicit distinct m-sets (sorted index Lists). -/
def Mset : List Nat := [0, 1, 4]
def Mset' : List Nat := [0, 2, 3]

def mem (x : Nat) : List Nat → Bool
  | [] => false
  | y :: ys => (x == y) || mem x ys

/-- |A \ B| = number of elements of A not in B. -/
def setDiffSize (A B : List Nat) : Nat :=
  A.foldl (fun acc x => if mem x B then acc else acc + 1) 0

/-- Johnson distance d_J(M,M') = |M \ M'|. -/
def dJ : Nat := setDiffSize Mset Mset'
def dJ_sym : Nat := setDiffSize Mset' Mset

/-- Elementary sum e1 (depth-1 prefix coefficient witness). -/
def e1 (xs : List Nat) : Nat := xs.foldl (fun acc x => acc + x) 0

theorem Mset_length : Mset.length = m := by native_decide
theorem Mset'_length : Mset'.length = m := by native_decide
theorem sets_distinct : Mset ≠ Mset' := by native_decide

/-- Shared depth-w=1 prefix: equal e1 sums. -/
theorem shared_depth1_prefix : e1 Mset = e1 Mset' := by native_decide
theorem e1_value : e1 Mset = 5 := by native_decide

/-- Symmetric Johnson distance. -/
theorem dJ_value : dJ = 2 := by native_decide
theorem dJ_sym_value : dJ_sym = 2 := by native_decide
theorem dJ_symmetric : dJ = dJ_sym := by native_decide

/-- Main rigidity instance: d_J ≥ w+1. -/
theorem prefix_rigidity_instance : dJ ≥ jBound := by native_decide
theorem prefix_rigidity_expanded : 2 ≥ 2 := by native_decide
theorem jBound_value : jBound = 2 := by native_decide

/-! ## lem:largest-fiber-log-detail (q=2 upper bound) — KEEP -/

def N : List Nat := [5, 3, 2]

def sumList (xs : List Nat) : Nat :=
  xs.foldl (fun acc x => acc + x) 0

def sumSq (xs : List Nat) : Nat :=
  xs.foldl (fun acc x => acc + x * x) 0

def maxList : List Nat → Nat
  | [] => 0
  | x :: xs => Nat.max x (maxList xs)

def totalM : Nat := sumList N
def maxN : Nat := maxList N
def sumN2 : Nat := sumSq N

theorem totalM_value : totalM = 10 := by native_decide
theorem maxN_value : maxN = 5 := by native_decide
theorem sumN2_value : sumN2 = 38 := by native_decide

/-- ∑ N(z)² ≤ (max N) · ∑ N(z). -/
theorem largest_fiber_first_moment : sumN2 ≤ maxN * totalM := by native_decide
theorem largest_fiber_first_moment_expanded : 38 ≤ 5 * 10 := by native_decide
theorem largest_fiber_in_sum : maxN * maxN ≤ sumN2 := by native_decide

/-- Tight equal-fiber case N=[4,4,4]. -/
def N2 : List Nat := [4, 4, 4]
def totalM2 : Nat := sumList N2
def maxN2 : Nat := maxList N2
def sumN2_2 : Nat := sumSq N2

theorem equal_fibers_tight : sumN2_2 = maxN2 * totalM2 := by native_decide
theorem equal_fibers_values : sumN2_2 = 48 := by native_decide

/-! ## Dual via `decide` -/

theorem shared_depth1_prefix' : e1 Mset = e1 Mset' := by decide
theorem dJ_value' : dJ = 2 := by decide
theorem prefix_rigidity_instance' : dJ ≥ jBound := by decide
theorem largest_fiber_first_moment' : sumN2 ≤ maxN * totalM := by decide
theorem equal_fibers_tight' : sumN2_2 = maxN2 * totalM2 := by decide
theorem sets_distinct' : Mset ≠ Mset' := by decide

end RigidityCensus
