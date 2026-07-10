/-!
# General ∑N² ≤ max·∑N (W46 M2)

Maps to **hard input (b)** image-scale MI+MA / moment-to-max.

General ∀-lemma behind #557/#551:
  sumSq l ≤ maxList l * sumList l
Proved by induction on the list. NOT closed by native_decide.

Kernel-complete: no unfinished goals, no extra axioms, no mathlib.
-/

namespace SumSqGeneral

def sumList : List Nat → Nat
  | [] => 0
  | x :: xs => x + sumList xs

def sumSq : List Nat → Nat
  | [] => 0
  | x :: xs => x * x + sumSq xs

def maxList : List Nat → Nat
  | [] => 0
  | x :: xs => Nat.max x (maxList xs)

/-- x² ≤ M·x when x ≤ M. -/
theorem sq_le_mul_of_le {x M : Nat} (h : x ≤ M) : x * x ≤ M * x :=
  Nat.mul_le_mul_right x h

/-- HEADLINE: ∀ l, ∑ Nᵢ² ≤ (max Nᵢ)·(∑ Nᵢ). -/
theorem sumSq_le_max_mul_sum (l : List Nat) :
    sumSq l ≤ maxList l * sumList l := by
  induction l with
  | nil =>
    simp only [sumSq, maxList, sumList, Nat.mul_zero]
    exact Nat.le_refl 0
  | cons x xs ih =>
    simp only [sumSq, maxList, sumList]
    -- Goal: x*x + sumSq xs ≤ Nat.max x (maxList xs) * (x + sumList xs)
    have hx : x ≤ Nat.max x (maxList xs) := Nat.le_max_left x (maxList xs)
    have hm : maxList xs ≤ Nat.max x (maxList xs) := Nat.le_max_right x (maxList xs)
    have hsq : x * x ≤ Nat.max x (maxList xs) * x := sq_le_mul_of_le hx
    have htail : maxList xs * sumList xs ≤ Nat.max x (maxList xs) * sumList xs :=
      Nat.mul_le_mul_right (sumList xs) hm
    have h1 : sumSq xs ≤ Nat.max x (maxList xs) * sumList xs :=
      Nat.le_trans ih htail
    have h2 :
        x * x + sumSq xs ≤
          Nat.max x (maxList xs) * x + Nat.max x (maxList xs) * sumList xs :=
      Nat.add_le_add hsq h1
    have hdist :
        Nat.max x (maxList xs) * x + Nat.max x (maxList xs) * sumList xs =
          Nat.max x (maxList xs) * (x + sumList xs) := by
      rw [← Nat.mul_add]
    exact hdist ▸ h2

/-- Sanity: N=[6,3,3] from #557. -/
theorem toy_557 :
    sumSq [6, 3, 3] ≤ maxList [6, 3, 3] * sumList [6, 3, 3] :=
  sumSq_le_max_mul_sum _

theorem toy_557_num : 54 ≤ 6 * 12 := by native_decide

theorem toy_557_values :
    sumSq [6, 3, 3] = 54 := by native_decide

theorem toy_tight :
    sumSq [8] = maxList [8] * sumList [8] := by native_decide

end SumSqGeneral
