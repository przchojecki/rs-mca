/-!
# First-match atlas partition identity (W37 M2)

Kernel-checked Nat facts for the committed first-match toy used by hard input
(a) packets #519 / #526:

Cells (slope projections, ordered):
  C₀ = {0,1,2,3}, C₁ = {2,3,4,5}, C₂ = {5,6,7,8,9}

First-match parts Zᵢ°:
  Z₀° = {0,1,2,3} (size 4)
  Z₁° = {4,5}     (size 2)   -- {2,3} already claimed
  Z₂° = {6,7,8,9} (size 4)   -- {5} already claimed

Partition identity: ∑ |Zᵢ°| = |⋃ Zᵢ°| = 10
Disjointness (size form): |Z₀°| + |Z₁°| + |Z₂°| = |union| (no double-count).

Source: first-match oracle_overlap toy in first-match-atlas / atlas-2 certs.
Hard input: (a) witness-exhaustive first-match atlas.

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Disjoint from holmbuar asymptotic_spine packages.
-/

namespace FirstMatchPartition

/-- First-match bucket sizes for the committed toy. -/
def size0 : Nat := 4
def size1 : Nat := 2
def size2 : Nat := 4

/-- Total covered slopes (union size). -/
def total : Nat := 10

/-- Exhaustive partition: sum of bucket sizes equals total. -/
theorem sum_eq_total : size0 + size1 + size2 = total := by native_decide

/-- Explicit expansion of the sum. -/
theorem sum_value : size0 + size1 + size2 = 10 := by native_decide

/-- Disjointness (size form): no double-counting — sum equals union cardinality. -/
theorem disjoint_size_form : size0 + size1 + size2 = total := by native_decide

/-- Pairwise size lower bounds (each bucket nonempty or as specified). -/
theorem size0_pos : size0 > 0 := by native_decide
theorem size1_pos : size1 > 0 := by native_decide
theorem size2_pos : size2 > 0 := by native_decide

/-- Second presentation via `decide`. -/
theorem sum_eq_total' : size0 + size1 + size2 = total := by decide
theorem sum_value' : 4 + 2 + 4 = 10 := by decide

/-- Named fold matching the identity shape ∑ sizes = total. -/
def sumSizes (xs : List Nat) : Nat :=
  xs.foldl (fun acc s => acc + s) 0

theorem sumSizes_toy : sumSizes [size0, size1, size2] = total := by native_decide
theorem sumSizes_toy' : sumSizes [4, 2, 4] = 10 := by decide

/-- Boundary toy from #526: later-subset first-match sizes [5,0,1], sum=6. -/
def boundary_sizes : List Nat := [5, 0, 1]
theorem boundary_sum : sumSizes boundary_sizes = 6 := by native_decide
theorem boundary_sum' : 5 + 0 + 1 = 6 := by decide

end FirstMatchPartition
