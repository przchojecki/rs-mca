/-!
# firstOccurrences membership + nodup (W47 M1)
Hard input (a). Completes #568. Real induction. No mathlib.
-/

namespace FirstOccNodupMem

def mem (x : Nat) : List Nat → Bool
  | [] => false
  | y :: ys => (x == y) || mem x ys

def step (acc : List Nat) (s : Nat) : List Nat :=
  match mem s acc with
  | true => acc
  | false => acc ++ [s]

def firstOccurrences (l : List Nat) : List Nat :=
  l.foldl step []

def nodup : List Nat → Bool
  | [] => true
  | x :: xs => (!mem x xs) && nodup xs

theorem or_false (b : Bool) : (b || false) = b := by cases b <;> rfl
theorem false_or (b : Bool) : (false || b) = b := by cases b <;> rfl
theorem true_or (b : Bool) : (true || b) = true := by cases b <;> rfl
theorem or_true (b : Bool) : (b || true) = true := by cases b <;> rfl
theorem or_assoc (a b c : Bool) : ((a || b) || c) = (a || (b || c)) := by
  cases a <;> cases b <;> cases c <;> rfl
theorem not_eq_true {b : Bool} (h : (!b) = true) : b = false := by
  cases b <;> simp_all
theorem and_eq_true {a b : Bool} (h : (a && b) = true) : a = true ∧ b = true := by
  cases a <;> cases b <;> simp_all

theorem mem_append_singleton (acc : List Nat) (y x : Nat) :
    mem x (acc ++ [y]) = (mem x acc || (x == y)) := by
  induction acc with
  | nil =>
    change (x == y || false) = (false || (x == y))
    rw [or_false, false_or]
  | cons z zs ih =>
    change ((x == z) || mem x (zs ++ [y])) = (((x == z) || mem x zs) || (x == y))
    rw [ih, or_assoc]

theorem mem_step (acc : List Nat) (s x : Nat) :
    mem x (step acc s) = (mem x acc || (x == s)) := by
  unfold step
  cases hmem : mem s acc with
  | true =>
    cases heq : (x == s) with
    | false => simp only [hmem, heq, or_false]
    | true =>
      have hx : x = s := eq_of_beq heq
      subst hx
      simp only [hmem, true_or]
  | false =>
    exact mem_append_singleton acc s x

theorem mem_foldl_step (l acc : List Nat) (x : Nat) :
    mem x (l.foldl step acc) = (mem x acc || mem x l) := by
  induction l generalizing acc with
  | nil =>
    change mem x acc = (mem x acc || false)
    rw [or_false]
  | cons y ys ih =>
    change mem x (ys.foldl step (step acc y)) =
      (mem x acc || ((x == y) || mem x ys))
    rw [ih, mem_step, or_assoc]

theorem firstOccurrences_mem (l : List Nat) (x : Nat) :
    mem x (firstOccurrences l) = mem x l := by
  unfold firstOccurrences
  have h := mem_foldl_step l [] x
  change mem x (l.foldl step []) = (false || mem x l) at h
  rw [false_or] at h
  exact h

/-! ## nodup -/

theorem nodup_nil : nodup [] = true := rfl

theorem nodup_cons_iff {x : Nat} {xs : List Nat} (h : nodup (x :: xs) = true) :
    mem x xs = false ∧ nodup xs = true := by
  have ⟨h1, h2⟩ := and_eq_true h
  exact ⟨not_eq_true h1, h2⟩

theorem nodup_append_singleton (acc : List Nat) (s : Nat)
    (hnd : nodup acc = true) (hni : mem s acc = false) :
    nodup (acc ++ [s]) = true := by
  induction acc with
  | nil =>
    -- nodup [s] = (!false) && true
    change ((!mem s []) && nodup []) = true
    simp only [mem, Bool.not_false, nodup_nil, Bool.true_and]
  | cons z zs ih =>
    have ⟨hz_ni, hzs⟩ := nodup_cons_iff hnd
    -- mem s (z::zs) = false
    have hs_ne_z : z ≠ s := by
      intro heq
      have : mem s (z :: zs) = true := by
        rw [heq]
        change (s == s || mem s zs) = true
        rw [beq_self_eq_true, true_or]
      rw [this] at hni
      cases hni
    have hs_ni_zs : mem s zs = false := by
      have hcons : ((s == z) || mem s zs) = false := hni
      cases hm : mem s zs with
      | false => rfl
      | true =>
        rw [hm, or_true] at hcons
        cases hcons
    have ih' := ih hzs hs_ni_zs
    have hmem : mem z (zs ++ [s]) = false := by
      have h := mem_append_singleton zs s z
      have zne : (z == s) = false := beq_eq_false_iff_ne.mpr hs_ne_z
      rw [h, hz_ni, zne, or_false]
    -- nodup (z :: (zs ++ [s]))
    change ((!mem z (zs ++ [s])) && nodup (zs ++ [s])) = true
    rw [hmem]
    change (true && nodup (zs ++ [s])) = true
    rw [Bool.true_and]
    exact ih'

theorem nodup_step (acc : List Nat) (s : Nat) (hnd : nodup acc = true) :
    nodup (step acc s) = true := by
  unfold step
  cases hmem : mem s acc with
  | true => exact hnd
  | false => exact nodup_append_singleton acc s hnd hmem

theorem nodup_foldl_step (l acc : List Nat) (hnd : nodup acc = true) :
    nodup (l.foldl step acc) = true := by
  induction l generalizing acc with
  | nil => exact hnd
  | cons y ys ih => exact ih (step acc y) (nodup_step acc y hnd)

theorem firstOccurrences_nodup (l : List Nat) :
    nodup (firstOccurrences l) = true := by
  unfold firstOccurrences
  exact nodup_foldl_step l [] nodup_nil

theorem toy_mem :
    mem 1 (firstOccurrences [0, 1, 1, 2]) = mem 1 [0, 1, 1, 2] :=
  firstOccurrences_mem _ _

theorem toy_nodup :
    nodup (firstOccurrences [0, 0, 1, 1, 2]) = true :=
  firstOccurrences_nodup _

theorem toy_nodup_value :
    nodup (firstOccurrences [0, 0, 1, 1, 2]) = true := by native_decide

theorem toy_mem_value :
    mem 2 (firstOccurrences [0, 1, 2, 2]) = true := by native_decide

end FirstOccNodupMem
