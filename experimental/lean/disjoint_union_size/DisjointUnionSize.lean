/-!
# listUnion length laws (W47 M2)
Hard input (a). Real induction. No mathlib.
-/

namespace DisjointUnionSize

def mem (x : Nat) : List Nat → Bool
  | [] => false
  | y :: ys => (x == y) || mem x ys

def nodup : List Nat → Bool
  | [] => true
  | x :: xs => (!mem x xs) && nodup xs

def step (acc : List Nat) (x : Nat) : List Nat :=
  match mem x acc with
  | true => acc
  | false => acc ++ [x]

def listUnion (a b : List Nat) : List Nat :=
  a.foldl step b

def disjoint : List Nat → List Nat → Bool
  | [], _ => true
  | x :: xs, b => (!mem x b) && disjoint xs b

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

theorem step_length_le (acc : List Nat) (x : Nat) :
    (step acc x).length ≤ acc.length + 1 := by
  unfold step
  cases h : mem x acc with
  | true => exact Nat.le_succ _
  | false =>
    simp only [List.length_append, List.length_singleton]
    exact Nat.le_refl _

theorem foldl_step_length_le (a acc : List Nat) :
    (a.foldl step acc).length ≤ acc.length + a.length := by
  induction a generalizing acc with
  | nil =>
    simp only [List.length_nil, Nat.add_zero]
    exact Nat.le_refl _
  | cons x xs ih =>
    have h := ih (step acc x)
    have hs := step_length_le acc x
    have h1 := Nat.add_le_add_right hs xs.length
    have h2 := Nat.le_trans h h1
    have rearrange :
        acc.length + 1 + xs.length = acc.length + xs.length.succ := by
      simp only [Nat.succ_eq_add_one, Nat.add_assoc, Nat.add_comm 1 xs.length]
    exact rearrange ▸ h2

theorem listUnion_length_le (a b : List Nat) :
    (listUnion a b).length ≤ a.length + b.length := by
  have h := foldl_step_length_le a b
  simpa [listUnion, Nat.add_comm] using h

theorem step_length_eq_not_mem (acc : List Nat) (x : Nat)
    (hni : mem x acc = false) :
    (step acc x).length = acc.length + 1 := by
  unfold step
  rw [hni]
  simp only [List.length_append, List.length_singleton]

theorem disjoint_cons_left {x : Nat} {xs b : List Nat}
    (h : disjoint (x :: xs) b = true) :
    mem x b = false ∧ disjoint xs b = true := by
  have ⟨h1, h2⟩ := and_eq_true h
  exact ⟨not_eq_true h1, h2⟩

theorem nodup_cons {x : Nat} {xs : List Nat} (h : nodup (x :: xs) = true) :
    mem x xs = false ∧ nodup xs = true := by
  have ⟨h1, h2⟩ := and_eq_true h
  exact ⟨not_eq_true h1, h2⟩

theorem mem_step_eq (acc : List Nat) (x y : Nat) (hni : mem x acc = false) :
    mem y (step acc x) = (mem y acc || (y == x)) := by
  unfold step
  rw [hni]
  exact mem_append_singleton acc x y

theorem disjoint_step (xs acc : List Nat) (x : Nat)
    (hdis : disjoint xs acc = true)
    (hx_ni_xs : mem x xs = false)
    (hni : mem x acc = false) :
    disjoint xs (step acc x) = true := by
  induction xs with
  | nil => rfl
  | cons y ys ih =>
    have ⟨hy_ni_acc, hdis_ys⟩ := disjoint_cons_left hdis
    have hx_ni_ys : mem x ys = false := by
      -- (x==y || mem x ys) = false
      have hx : ((x == y) || mem x ys) = false := hx_ni_xs
      cases hm : mem x ys with
      | false => rfl
      | true =>
        rw [hm, or_true] at hx
        cases hx
    have hy_ne_x : y ≠ x := by
      intro heq
      have hx : ((x == y) || mem x ys) = false := hx_ni_xs
      rw [heq, beq_self_eq_true, true_or] at hx
      cases hx
    have hy_ni_step : mem y (step acc x) = false := by
      have h := mem_step_eq acc x y hni
      have hyx : (y == x) = false := beq_eq_false_iff_ne.mpr hy_ne_x
      rw [h, hy_ni_acc, hyx, or_false]
    change ((!mem y (step acc x)) && disjoint ys (step acc x)) = true
    rw [hy_ni_step]
    change (true && disjoint ys (step acc x)) = true
    rw [Bool.true_and]
    exact ih hdis_ys hx_ni_ys

theorem foldl_length_eq_disjoint (a acc : List Nat)
    (hdis : disjoint a acc = true) (hnd : nodup a = true) :
    (a.foldl step acc).length = acc.length + a.length := by
  induction a generalizing acc with
  | nil =>
    simp only [List.foldl_nil, List.length_nil, Nat.add_zero]
  | cons x xs ih =>
    have ⟨hni, hdis_xs⟩ := disjoint_cons_left hdis
    have ⟨hx_ni_xs, hnd_xs⟩ := nodup_cons hnd
    have hs := step_length_eq_not_mem acc x hni
    have hdis_step := disjoint_step xs acc x hdis_xs hx_ni_xs hni
    have ih' := ih (step acc x) hdis_step hnd_xs
    simp only [List.foldl_cons, List.length_cons]
    rw [ih', hs]
    simp only [Nat.succ_eq_add_one, Nat.add_assoc, Nat.add_comm 1 xs.length]

theorem listUnion_length_eq_of_disjoint (a b : List Nat)
    (hnd : nodup a = true) (hdis : disjoint a b = true) :
    (listUnion a b).length = a.length + b.length := by
  have h := foldl_length_eq_disjoint a b hdis hnd
  simpa [listUnion, Nat.add_comm] using h

theorem toy_le :
    (listUnion [0, 1] [1, 2, 3]).length ≤ [0, 1].length + [1, 2, 3].length :=
  listUnion_length_le _ _

theorem toy_eq :
    (listUnion [1, 2] [3, 4]).length = [1, 2].length + [3, 4].length :=
  listUnion_length_eq_of_disjoint _ _ (by native_decide) (by native_decide)

theorem toy_eq_value :
    (listUnion [1, 2] [3, 4]).length = 4 := by native_decide

theorem toy_le_value :
    (listUnion [0, 0, 1] [1, 2]).length ≤ 5 := by native_decide

end DisjointUnionSize
