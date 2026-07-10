/-!
# General first-occurrence length bound (W46 M1)

Maps to **hard input (a)** first-match atlas / PO6 mechanism.

General ∀-lemma behind #563 structural atlas:
  (firstOccurrences l).length ≤ l.length
proved by induction on the list. NOT closed by native_decide.

Kernel-complete: no unfinished goals, no extra axioms, no mathlib.
-/

namespace FirstOccGeneral

/-- Membership as Bool. -/
def mem (x : Nat) : List Nat → Bool
  | [] => false
  | y :: ys => (x == y) || mem x ys

/-- Fold step: append s only if not already present. -/
def step (acc : List Nat) (s : Nat) : List Nat :=
  if mem s acc then acc else acc ++ [s]

/-- First-occurrence dedup fold. -/
def firstOccurrences (l : List Nat) : List Nat :=
  l.foldl step []

theorem step_length_le (acc : List Nat) (s : Nat) :
    (step acc s).length ≤ acc.length + 1 := by
  unfold step
  split
  · exact Nat.le_succ acc.length
  · simp only [List.length_append, List.length_singleton]
    exact Nat.le_refl _

/-- Invariant: foldl step acc l has length ≤ acc.length + l.length. -/
theorem foldl_step_length_le (l acc : List Nat) :
    (l.foldl step acc).length ≤ acc.length + l.length := by
  induction l generalizing acc with
  | nil =>
    simp only [List.foldl_nil, List.length_nil, Nat.add_zero]
    exact Nat.le_refl _
  | cons x xs ih =>
    -- (foldl step (step acc x) xs).length ≤ (step acc x).length + xs.length
    have h := ih (step acc x)
    have hs : (step acc x).length ≤ acc.length + 1 := step_length_le acc x
    have h1 : (step acc x).length + xs.length ≤ (acc.length + 1) + xs.length :=
      Nat.add_le_add_right hs xs.length
    have h2 : (xs.foldl step (step acc x)).length ≤ (acc.length + 1) + xs.length :=
      Nat.le_trans h h1
    -- goal after simp: … ≤ acc.length + xs.length.succ
    simp only [List.foldl_cons, List.length_cons]
    -- xs.length.succ = xs.length + 1
    have rearrange :
        acc.length + 1 + xs.length = acc.length + xs.length.succ := by
      simp only [Nat.succ_eq_add_one, Nat.add_assoc, Nat.add_comm 1 xs.length]
    exact rearrange ▸ h2

/-- HEADLINE: ∀ l, |firstOccurrences l| ≤ |l|. -/
theorem firstOccurrences_length_le (l : List Nat) :
    (firstOccurrences l).length ≤ l.length := by
  have h := foldl_step_length_le l []
  simp only [firstOccurrences, List.length_nil, Nat.zero_add] at h ⊢
  exact h

/-- Sanity: collision list from atlas-style slopes. -/
theorem toy_collision_le :
    (firstOccurrences [0, 0, 1, 1, 2]).length ≤ [0, 0, 1, 1, 2].length :=
  firstOccurrences_length_le _

theorem toy_collision_value :
    (firstOccurrences [0, 0, 1, 1, 2]).length = 3 := by native_decide

theorem toy_strict :
    (firstOccurrences [0, 0]).length < [0, 0].length := by native_decide

end FirstOccGeneral
