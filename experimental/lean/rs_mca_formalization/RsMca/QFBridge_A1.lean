import RsMca.QuotientOverlap
import RsMca.A6QuotientFloorClosed

/-!
# QFBridge_A1: closing `quotientFloor n1 (n1+1) = (3^n1 - 1)/2`

Stdlib-only (no mathlib) bridge that connects the published `List.range` foldr
`RsMca.quotientFloor n1 (n1+1)` to the already-proved parity-split core
`A6.PE`/`A6.PO`/`A6.minorityFloor`, yielding `RsMca.qf_half_closed`.

Route:
* `R n c := Σ_{t≤n} choose n t * c t` with the Pascal recurrence
  `R (n+1) c = R n c + R n (c∘succ)`.
* `wpar p n := R n (cpar p)` are the even/odd 2-weighted binomial sums; they satisfy
  the swap recurrence `wpar p (n+1) = wpar p n + 2 * wpar (1-p) n`, hence (cast to `Int`)
  equal `A6.PE`/`A6.PO`.
* the reindex `quotientFloor n1 (n1+1) = wpar ((n1+1)%2) n1` (the minority parity class),
  done by splitting the `u`-range, reversing the `range'` and `filter`-enumerating the
  parity class.
* combine with `A6.minorityFloor_closed`: `2 * qf + 1 = 3^n1`, then divide.
-/

namespace QFBridgeA1

open RsMca List

/-! ## Foundational finite-sum helpers -/

/-- Sum of a pointwise sum splits. -/
theorem sum_map_add (l : List Nat) (A B : Nat → Nat) :
    (l.map (fun k => A k + B k)).sum = (l.map A).sum + (l.map B).sum := by
  induction l with
  | nil => rfl
  | cons a t ih =>
    simp only [List.map_cons, List.sum_cons, ih]; omega

/-- Pulling a constant factor out of a sum. -/
theorem sum_map_mul_left (l : List Nat) (a : Nat) (h : Nat → Nat) :
    (l.map (fun k => a * h k)).sum = a * (l.map h).sum := by
  induction l with
  | nil => simp
  | cons x t ih =>
    simp only [List.map_cons, List.sum_cons, ih, Nat.mul_add]

/-- Sum of an all-zero mapped list is zero. -/
theorem sum_map_zero (l : List Nat) : (l.map (fun _ => (0 : Nat))).sum = 0 := by
  induction l with
  | nil => rfl
  | cons a t ih => simp only [List.map_cons, List.sum_cons, ih]

/-! ## Row sums and the Pascal recurrence -/

/-- `R n c = Σ_{t=0}^{n} choose n t * c t`. -/
def R (n : Nat) (c : Nat → Nat) : Nat :=
  ((List.range (n + 1)).map (fun t => choose n t * c t)).sum

/-- Helper: `c 0 + Σ_{k=0}^{n} choose n (k+1) * c (k+1) = R n c` (the top term `k=n`
    vanishes since `choose n (n+1) = 0`). -/
theorem aux_secondSum (n : Nat) (c : Nat → Nat) :
    c 0 + ((List.range (n + 1)).map (fun k => choose n (k + 1) * c (k + 1))).sum = R n c := by
  -- Expand `R n c` by peeling the `t = 0` term.
  have hR : R n c
      = c 0 + ((List.range n).map (fun k => choose n (k + 1) * c (k + 1))).sum := by
    unfold R
    rw [List.range_succ_eq_map]
    simp only [List.map_cons, List.sum_cons, List.map_map, choose_zero_right, Nat.one_mul]
    rfl
  -- The `range (n+1)` sum drops its top term (it is `0`).
  have htop : ((List.range (n + 1)).map (fun k => choose n (k + 1) * c (k + 1))).sum
      = ((List.range n).map (fun k => choose n (k + 1) * c (k + 1))).sum := by
    rw [List.range_succ, List.map_append, List.sum_append]
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
      choose_eq_zero_of_lt (Nat.lt_succ_self n), Nat.zero_mul, Nat.add_zero]
  rw [htop, hR]

/-- The Pascal row recurrence: `R (n+1) c = R n c + R n (c ∘ succ)`. -/
theorem R_succ (n : Nat) (c : Nat → Nat) :
    R (n + 1) c = R n c + R n (fun k => c (k + 1)) := by
  unfold R
  rw [List.range_succ_eq_map]
  simp only [List.map_cons, List.sum_cons, List.map_map, choose_zero_right, Nat.one_mul]
  -- The mapped tail: choose (n+1) (k+1) = choose n k + choose n (k+1).
  have hmap : ((List.range (n + 1)).map
        ((fun t => choose (n + 1) t * c t) ∘ Nat.succ))
      = (List.range (n + 1)).map
          (fun k => choose n k * c (k + 1) + choose n (k + 1) * c (k + 1)) := by
    apply List.map_congr_left
    intro k _
    show choose (n + 1) (k + 1) * c (k + 1) = _
    rw [show choose (n + 1) (k + 1) = choose n k + choose n (k + 1) from rfl, Nat.add_mul]
  rw [hmap]
  have hs : ((List.range (n + 1)).map
        (fun k => choose n k * c (k + 1) + choose n (k + 1) * c (k + 1))).sum
      = ((List.range (n + 1)).map (fun k => choose n k * c (k + 1))).sum
        + ((List.range (n + 1)).map (fun k => choose n (k + 1) * c (k + 1))).sum :=
    sum_map_add (List.range (n + 1)) (fun k => choose n k * c (k + 1))
      (fun k => choose n (k + 1) * c (k + 1))
  rw [hs]
  -- First piece is `R n (c∘succ)`; second piece closes via `aux_secondSum`.
  have h2 : c 0 + ((List.range (n + 1)).map (fun k => choose n (k + 1) * c (k + 1))).sum
      = ((List.range (n + 1)).map (fun t => choose n t * c t)).sum := aux_secondSum n c
  omega

/-! ## Parity-weighted binomial sums and their tie to `A6.PE` / `A6.PO` -/

/-- `cpar p t = 2^t` on the parity class `t ≡ p (mod 2)`, else `0`. -/
def cpar (p t : Nat) : Nat := if t % 2 = p then 2 ^ t else 0

/-- `wpar p n = Σ_{t ≤ n, t ≡ p} choose n t * 2^t`. -/
def wpar (p n : Nat) : Nat := R n (cpar p)

/-- The `succ`-shift swaps parity and pulls out a factor of two. -/
theorem cpar_succ_apply (p : Nat) (hp : p < 2) (k : Nat) :
    cpar p (k + 1) = 2 * cpar (1 - p) k := by
  have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
  unfold cpar
  by_cases hc : (k + 1) % 2 = p
  · have hk : k % 2 = 1 - p := by omega
    rw [if_pos hc, if_pos hk, hpow]
  · have hk : ¬ (k % 2 = 1 - p) := by omega
    rw [if_neg hc, if_neg hk, Nat.mul_zero]

/-- Pascal swap recurrence for the parity sums. -/
theorem wpar_succ (p : Nat) (hp : p < 2) (n : Nat) :
    wpar p (n + 1) = wpar p n + 2 * wpar (1 - p) n := by
  unfold wpar
  rw [R_succ]
  congr 1
  have hfun : (fun k => cpar p (k + 1)) = (fun k => 2 * cpar (1 - p) k) := by
    funext k; exact cpar_succ_apply p hp k
  rw [hfun]
  unfold R
  rw [show (fun t => choose n t * (2 * cpar (1 - p) t))
        = (fun t => 2 * (choose n t * cpar (1 - p) t)) from by
      funext t; rw [Nat.mul_left_comm]]
  exact sum_map_mul_left (List.range (n + 1)) 2 (fun t => choose n t * cpar (1 - p) t)

/-- The parity sums are exactly the `A6` recurrence sequences (cast to `Int`). -/
theorem wpar_cast (n : Nat) :
    ((wpar 0 n : Nat) : Int) = A6.PE n ∧ ((wpar 1 n : Nat) : Int) = A6.PO n := by
  induction n with
  | zero => refine ⟨?_, ?_⟩ <;> decide
  | succ m ih =>
    obtain ⟨ihe, iho⟩ := ih
    refine ⟨?_, ?_⟩
    · have hrec : wpar 0 (m + 1) = wpar 0 m + 2 * wpar 1 m := by
        rw [wpar_succ 0 (by decide) m]
      have hpe := A6.PE_succ m
      omega
    · have hrec : wpar 1 (m + 1) = wpar 1 m + 2 * wpar 0 m := by
        rw [wpar_succ 1 (by decide) m]
      have hpo := A6.PO_succ m
      omega

/-! ## The reindex: `quotientFloor n1 (n1+1) = wpar ((n1+1)%2) n1` -/

/-- Reversing the decreasing `u`-progression `[b-2, b-4, …]` yields the increasing
    step-`2` progression `range' (b - 2K) K 2`. -/
theorem reindex_reverse : ∀ (K b : Nat), 2 * K ≤ b →
    ((List.range' 1 K 1).map (fun u => b - 2 * u)).reverse = List.range' (b - 2 * K) K 2 := by
  intro K
  induction K with
  | zero => intro b _; simp
  | succ K ih =>
    intro b hb
    have h1 : b - 2 * (1 + 1 * K) = b - 2 * (K + 1) := by omega
    have h2 : b - 2 * K = b - 2 * (K + 1) + 2 := by omega
    rw [List.range'_concat, List.map_append, List.reverse_append, ih b (by omega),
      List.range'_succ]
    simp only [List.map_cons, List.map_nil, List.reverse_singleton, List.singleton_append,
      h1, h2]

/-- `quotientFloorTerm` with the `let` unfolded into an explicit guard. -/
theorem qft_eq (n1 ellp u : Nat) :
    quotientFloorTerm n1 ellp u
      = if 2 * u ≤ ellp ∧ u + (ellp - 2 * u) ≤ n1
        then choose n1 (ellp - 2 * u) * 2 ^ (ellp - 2 * u) else 0 := rfl

/-- Assembly, general `K`: with `2K ≤ n1+1 ≤ 2K+1`, the published floor is the
    increasing step-`2` binomial sum from `n1+1-2K` of length `K`. -/
theorem assembly_gen (n1 K : Nat) (hlo : 2 * K ≤ n1 + 1) (hhi : n1 + 1 ≤ 2 * K + 1) :
    quotientFloor n1 (n1 + 1)
      = ((List.range' (n1 + 1 - 2 * K) K 2).map (fun t => choose n1 t * 2 ^ t)).sum := by
  -- `quotientFloor` as a `.sum`.
  have hqf : quotientFloor n1 (n1 + 1)
      = ((List.range (n1 + 2)).map (quotientFloorTerm n1 (n1 + 1))).sum := by
    unfold quotientFloor; rw [List.sum_eq_foldr]
  -- The index list splits into `0`, the middle `range' 1 K 1`, and a zero suffix.
  have hlist : List.range (n1 + 2)
      = (0 :: List.range' 1 K 1) ++ List.range' (1 + K) (n1 + 1 - K) 1 := by
    rw [List.range_eq_range', show n1 + 2 = (n1 + 1) + 1 from rfl, List.range'_succ,
      Nat.zero_add]
    have h := @List.range'_append 1 K (n1 + 1 - K) 1
    simp only [Nat.one_mul] at h
    rw [show K + (n1 + 1 - K) = n1 + 1 from by omega] at h
    rw [← h, List.cons_append]
  -- The `u = 0` term vanishes.
  have hzero : quotientFloorTerm n1 (n1 + 1) 0 = 0 := by
    rw [qft_eq]; split <;> omega
  -- The middle terms are the clean binomial weights.
  have hmid : (List.range' 1 K 1).map (quotientFloorTerm n1 (n1 + 1))
      = (List.range' 1 K 1).map (fun u => choose n1 (n1 + 1 - 2 * u) * 2 ^ (n1 + 1 - 2 * u)) := by
    apply List.map_congr_left
    intro u hu
    rw [List.mem_range'] at hu
    obtain ⟨i, hi, hui⟩ := hu
    rw [qft_eq]; split
    · rfl
    · omega
  -- The middle sum is the reversed step-`2` sum, hence the target sum.
  have hmidsum : ((List.range' 1 K 1).map
        (fun u => choose n1 (n1 + 1 - 2 * u) * 2 ^ (n1 + 1 - 2 * u))).sum
      = ((List.range' (n1 + 1 - 2 * K) K 2).map (fun t => choose n1 t * 2 ^ t)).sum := by
    have hh : (List.range' 1 K 1).map (fun u => n1 + 1 - 2 * u)
        = (List.range' (n1 + 1 - 2 * K) K 2).reverse := by
      rw [← reindex_reverse K (n1 + 1) hlo, List.reverse_reverse]
    have hcomp : (fun u => choose n1 (n1 + 1 - 2 * u) * 2 ^ (n1 + 1 - 2 * u))
        = (fun t => choose n1 t * 2 ^ t) ∘ (fun u => n1 + 1 - 2 * u) := rfl
    rw [hcomp, ← List.map_map, hh, List.map_reverse, List.sum_reverse]
  -- The zero suffix.
  have hsufsum : ((List.range' (1 + K) (n1 + 1 - K) 1).map
        (quotientFloorTerm n1 (n1 + 1))).sum = 0 := by
    have hz : (List.range' (1 + K) (n1 + 1 - K) 1).map (quotientFloorTerm n1 (n1 + 1))
        = (List.range' (1 + K) (n1 + 1 - K) 1).map (fun _ => (0 : Nat)) := by
      apply List.map_congr_left
      intro u hu
      rw [List.mem_range'] at hu
      obtain ⟨i, hi, hui⟩ := hu
      rw [qft_eq]; split <;> omega
    rw [hz, sum_map_zero]
  rw [hqf, hlist, List.map_append, List.sum_append, List.map_cons, List.sum_cons,
    hzero, hmid, hmidsum, hsufsum]
  omega

/-- Assembly at the prize index: the published floor is the minority-parity sum. -/
theorem assembly (n1 : Nat) :
    quotientFloor n1 (n1 + 1)
      = ((List.range' ((n1 + 1) % 2) ((n1 + 1) / 2) 2).map (fun t => choose n1 t * 2 ^ t)).sum := by
  have h := assembly_gen n1 ((n1 + 1) / 2) (by omega) (by omega)
  rw [show n1 + 1 - 2 * ((n1 + 1) / 2) = (n1 + 1) % 2 from by omega] at h
  exact h

/-! ## Connecting the step-`2` sum to `wpar` -/

/-- The parity-filtered row sum equals the step-`2` `range'` sum (no `filter`/`decide`). -/
theorem parity_step (p : Nat) (hp : p < 2) (h : Nat → Nat) : ∀ N,
    ((List.range N).map (fun t => if t % 2 = p then h t else 0)).sum
      = ((List.range' p ((N + 1 - p) / 2) 2).map h).sum := by
  intro N
  induction N with
  | zero => simp [show (0 + 1 - p) / 2 = 0 from by omega]
  | succ N ih =>
    rw [List.range_succ, List.map_append, List.sum_append, ih]
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Nat.add_zero]
    by_cases hN : N % 2 = p
    · have hM : (N + 1 + 1 - p) / 2 = (N + 1 - p) / 2 + 1 := by omega
      have hN2 : p + 2 * ((N + 1 - p) / 2) = N := by omega
      rw [if_pos hN, hM, List.range'_concat, List.map_append, List.sum_append]
      simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Nat.add_zero, hN2]
    · have hM : (N + 1 + 1 - p) / 2 = (N + 1 - p) / 2 := by omega
      rw [if_neg hN, Nat.add_zero, hM]

/-- `wpar p n` as a step-`2` binomial sum. -/
theorem wpar_step (p : Nat) (hp : p < 2) (n : Nat) :
    wpar p n = ((List.range' p ((n + 2 - p) / 2) 2).map (fun t => choose n t * 2 ^ t)).sum := by
  have hfun : (fun t => choose n t * cpar p t)
      = (fun t => if t % 2 = p then choose n t * 2 ^ t else 0) := by
    funext t; unfold cpar
    by_cases hc : t % 2 = p
    · rw [if_pos hc, if_pos hc]
    · rw [if_neg hc, if_neg hc, Nat.mul_zero]
  unfold wpar R
  rw [hfun, parity_step p hp (fun t => choose n t * 2 ^ t) (n + 1),
    show (n + 1 + 1 - p) / 2 = (n + 2 - p) / 2 from by omega]

/-- The published floor at the prize index is the minority parity sum `wpar`. -/
theorem qf_eq_wpar (n1 : Nat) :
    quotientFloor n1 (n1 + 1) = wpar ((n1 + 1) % 2) n1 := by
  rw [assembly n1, wpar_step ((n1 + 1) % 2) (by omega) n1,
    show (n1 + 1) / 2 = (n1 + 2 - (n1 + 1) % 2) / 2 from by omega]

/-- The prize-rate identity in `Nat`: `2 · quotientFloor + 1 = 3^n1`. -/
theorem qf_two_mul (n1 : Nat) : 2 * quotientFloor n1 (n1 + 1) + 1 = 3 ^ n1 := by
  have hcast : ((quotientFloor n1 (n1 + 1) : Nat) : Int) = A6.minorityFloor n1 := by
    rw [qf_eq_wpar n1]
    unfold A6.minorityFloor
    obtain ⟨he, ho⟩ := wpar_cast n1
    by_cases hpar : n1 % 2 = 0
    · rw [if_pos hpar, show (n1 + 1) % 2 = 1 from by omega, ho]
    · rw [if_neg hpar, show (n1 + 1) % 2 = 0 from by omega, he]
  have hclosed := A6.minorityFloor_closed n1
  rw [A6.T_eq] at hclosed
  omega

end QFBridgeA1

/-- TARGET. The prize-rate quotient-floor closed form, fully proved (stdlib only). -/
theorem qf_half_closed (n1 : Nat) :
    RsMca.quotientFloor n1 (n1 + 1) = (3 ^ n1 - 1) / 2 := by
  have h := QFBridgeA1.qf_two_mul n1
  omega

example : RsMca.QuotientFloorHalfClosed := qf_half_closed

#print axioms qf_half_closed

#print axioms QFBridgeA1.assembly_gen
#print axioms QFBridgeA1.reindex_reverse
#print axioms QFBridgeA1.qft_eq
#print axioms QFBridgeA1.sum_map_zero
#print axioms QFBridgeA1.aux_secondSum
