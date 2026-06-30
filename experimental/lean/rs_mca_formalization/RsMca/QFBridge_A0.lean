import RsMca.QuotientOverlap
import RsMca.A6QuotientFloorClosed

/-!
# QFBridge_A0: closing `quotientFloor n1 (n1+1) = (3^n1 - 1)/2`

Stdlib-only bridge from Paper B's `List.range`-foldr quotient floor to A6's proved
parity split.  Strategy (orchestrator "A0"): build a finite-sum combinator `S`,
prove the Pascal swap recurrence for the parity-weighted binomial sums `wp n p`
(`= Σ_{t ≡ p (2)} C(n,t) 2^t`), identify `wp n 0 = PE n`, `wp n 1 = PO n`, then
reindex the quotient-floor foldr onto the opposite-parity sum and feed
`A6.minorityFloor_closed`.
-/

namespace QFBridge_A0

open RsMca

/-! ## A finite-sum combinator over `[0, k)` and its basic algebra -/

/-- Sum of `f` over `0, 1, …, k-1`. -/
def S (f : Nat → Nat) (k : Nat) : Nat := ((List.range k).map f).foldr (· + ·) 0

@[simp] theorem S_zero (f : Nat → Nat) : S f 0 = 0 := rfl

/-- Folding `(·+·)` with a nonzero base just adds that base. -/
theorem foldr_add_base (L : List Nat) (c : Nat) :
    L.foldr (· + ·) c = L.foldr (· + ·) 0 + c := by
  induction L with
  | nil => simp
  | cons a t ih => simp only [List.foldr_cons, ih]; omega

/-- Peel the top index: `S f (k+1) = S f k + f k`. -/
theorem S_succ (f : Nat → Nat) (k : Nat) : S f (k + 1) = S f k + f k := by
  unfold S
  rw [List.range_succ, List.map_append, List.foldr_append]
  simp only [List.map_cons, List.map_nil, List.foldr_cons, List.foldr_nil]
  rw [foldr_add_base]; omega

/-- Peel the bottom index: `S f (k+1) = f 0 + S (fun t => f (t+1)) k`. -/
theorem S_cons (f : Nat → Nat) (k : Nat) :
    S f (k + 1) = f 0 + S (fun t => f (t + 1)) k := by
  unfold S
  rw [List.range_succ_eq_map]
  simp only [List.map_cons, List.foldr_cons, List.map_map]
  rfl

/-- Sums add pointwise. -/
theorem S_add (f g : Nat → Nat) (k : Nat) :
    S (fun t => f t + g t) k = S f k + S g k := by
  induction k with
  | zero => rfl
  | succ k ih => rw [S_succ, S_succ, S_succ, ih]; omega

/-- A constant factor pulls out of the sum. -/
theorem S_mul (c : Nat) (f : Nat → Nat) (k : Nat) :
    S (fun t => c * f t) k = c * S f k := by
  induction k with
  | zero => simp [S]
  | succ k ih => rw [S_succ, S_succ, ih, Nat.mul_add]

/-- Distribute a guard over a sum. -/
theorem ite_add' (P : Prop) [Decidable P] (a b : Nat) :
    (if P then a + b else 0) = (if P then a else 0) + (if P then b else 0) := by
  by_cases h : P <;> simp [h]

/-- Pull a constant out of a guard. -/
theorem ite_mul' (P : Prop) [Decidable P] (c a : Nat) :
    (if P then c * a else 0) = c * (if P then a else 0) := by
  by_cases h : P <;> simp [h]

end QFBridge_A0
