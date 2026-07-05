namespace StaircaseLogic

/-!
# Abstract staircase / one-step layer (stdlib-only, no mathlib)

Stdlib-only (no mathlib) formalization of the **abstract monotone integer
staircase** and its **one-step localization**, the certificate grammar of

* `experimental/thresholds.tex`
    (`def:integer numerator staircase`, `thm:staircase`, `cor:endpoint`,
    `thm:corridor`);
* `experimental/cap25_v13_experimental.tex`
    (`thm:v13-staircase`, `cor:v13-endpoint`, `thm:v13-corridor`,
    `rem:v13-staircase-v12`);
* `experimental/experiments.tex`
    (`thm:one-step-staircase`, i.e. `prop:onestep`);
* `agents.md` (the finite MCA node `B_C(a_safe-1) > B*`, `B_C(a_safe) <= B*`).

This file proves ONLY the abstract order-theoretic layer, on an opaque
nonincreasing numerator `N : Nat -> Nat` with an integer budget `B`.  It carries
no field theory and no huge integers: `N a`, `B`, `n` are opaque `Nat`s, and the
theorems are pure `Nat`/order facts closed by `omega`.  The finite-slope
semantics of `N` (that it *is* `LD_sw`) and the arithmetic value of
`B_* = floor(eps* Q)` are supplied by the row packet / Python verifier and enter
here only as the instance data of a `Staircase` (see `ToyCert.lean`).

`Unsafe` is spelled with a capital `U` because `unsafe` is a reserved Lean
keyword; it denotes the note's "unsafe" agreement.

No `sorry`, no `native_decide`, no mathlib; `#print axioms` at the foot.
-/

/-- **Integer numerator staircase** (`def:integer numerator staircase`,
`thresholds.tex` / `cap25_v13_experimental.tex`).

* `N a` is the bad-sampled-parameter numerator at agreement threshold `a`
  (`= LD_sw(C,a)` for MCA / line-MCA rows), **nonincreasing** in `a` on the
  agreement interval `I = [amin, amax]` — raising the agreement threshold only
  removes valid supports.
* `B` is the integer challenge budget `B_* = floor(eps* Q)`.
* `n` is the block length; the closed integer Hamming radius at agreement `a` is
  `r = n - a`.

Antitonicity is stated exactly as the note's "nonincreasing on `I`". -/
structure Staircase where
  /-- Bad-parameter numerator at agreement threshold `a`. -/
  N : Nat → Nat
  /-- Integer budget `B_* = floor(eps* Q)`. -/
  B : Nat
  /-- Block length; closed integer radius at agreement `a` is `n - a`. -/
  n : Nat
  /-- Left endpoint of the agreement interval `I`. -/
  amin : Nat
  /-- Right endpoint of the agreement interval `I`. -/
  amax : Nat
  /-- `I = [amin, amax]` is a nonempty interval. -/
  hI : amin ≤ amax
  /-- The interval sits inside the block: `amax ≤ n` (so radii `n - a ≥ 0`). -/
  hn : amax ≤ n
  /-- `N` is nonincreasing (antitone) on `I`: larger agreement ⇒ smaller count. -/
  antitone : ∀ a a', amin ≤ a → a ≤ a' → a' ≤ amax → N a' ≤ N a

namespace Staircase

variable (S : Staircase)

/-- Agreement `a` is **safe** when the numerator is within budget: `N a ≤ B_*`. -/
def safe (a : Nat) : Prop := S.N a ≤ S.B

/-- Agreement `a` is **unsafe** when the numerator exceeds budget: `N a > B_*`.
(Capital `U`: `unsafe` is a reserved keyword.) -/
def Unsafe (a : Nat) : Prop := S.B < S.N a

instance (a : Nat) : Decidable (S.safe a) := inferInstanceAs (Decidable (S.N a ≤ S.B))
instance (a : Nat) : Decidable (S.Unsafe a) := inferInstanceAs (Decidable (S.B < S.N a))

theorem unsafe_iff_not_safe (a : Nat) : S.Unsafe a ↔ ¬ S.safe a := by
  unfold safe Unsafe; exact Nat.not_le.symm

/-! ## Monotonicity of safety (safety is upward-closed) -/

/-- **Safety is upward-closed.**  Because `N` is *antitone* in the agreement, a
*larger* agreement carries a *smaller* numerator (`N a' ≤ N a`), so once a row is
safe every higher in-interval agreement is safe:
`a ≤ a'` and `safe a` ⟹ `safe a'`.

This is the direction fix flagged in the note: antitone-in-`a` means the safe
set is the **up-set** `{a : a ≥ a_*}`, not the down-set. -/
theorem safe_up {a a' : Nat}
    (ha : S.amin ≤ a) (haa : a ≤ a') (ha' : a' ≤ S.amax) (hs : S.safe a) :
    S.safe a' := by
  have hmono : S.N a' ≤ S.N a := S.antitone a a' ha haa ha'
  unfold safe at hs ⊢
  omega

/-! ## First safe agreement, uniqueness, and the one-step certificate -/

/-- `a` is the (interior) **first safe agreement** `a_*` of `thm:staircase` case
(iii): it is in `I`, safe, and every strictly smaller in-interval agreement is
unsafe.  Equivalently `N(a_*-1) > B_* ≥ N(a_*)`. -/
def IsFirstSafe (a : Nat) : Prop :=
  S.amin ≤ a ∧ a ≤ S.amax ∧ S.safe a ∧ ∀ b, S.amin ≤ b → b < a → S.Unsafe b

/-- **Uniqueness of the first safe point** (`thm:staircase`, the "unique" in case
(iii)).  A monotone Boolean predicate on a finite linear order has at most one
first-true point; here that is the first safe agreement. -/
theorem firstSafe_unique {a a' : Nat}
    (h : S.IsFirstSafe a) (h' : S.IsFirstSafe a') : a = a' := by
  obtain ⟨ha0, _, hsa, hmin⟩ := h
  obtain ⟨ha0', _, hsa', hmin'⟩ := h'
  rcases Nat.lt_or_ge a a' with hlt | hge
  · exact absurd hsa ((S.unsafe_iff_not_safe a).mp (hmin' a ha0 hlt))
  · rcases Nat.lt_or_ge a' a with hlt' | hge'
    · exact absurd hsa' ((S.unsafe_iff_not_safe a').mp (hmin a' ha0' hlt'))
    · omega

/-- **One-step certificate** (`prop:onestep` = `thm:one-step-staircase`, the v13
one-step case of `thm:v13-staircase`/`thm:v13-corridor`, `rem:v13-staircase-v12`;
`agents.md` finite MCA node).

A matched adjacent pair — `N a0 > B_*` (unsafe lower certificate `L(a0)`) and
`N (a0+1) ≤ B_*` (safe upper certificate `U(a0+1)`) — pins the first safe
agreement exactly to `a_* = a0 + 1`.  Antitonicity turns the single unsafe point
`a0` into "all `b ≤ a0` unsafe", which is the minimality half of `IsFirstSafe`. -/
theorem oneStep_isFirstSafe (a0 : Nat)
    (h0 : S.amin ≤ a0) (h1 : a0 + 1 ≤ S.amax)
    (hunsafe : S.Unsafe a0) (hsafe : S.safe (a0 + 1)) :
    S.IsFirstSafe (a0 + 1) := by
  refine ⟨by omega, h1, hsafe, ?_⟩
  intro b hb hlt
  have hble : b ≤ a0 := by omega
  have ha0max : a0 ≤ S.amax := by omega
  have hmono : S.N a0 ≤ S.N b := S.antitone b a0 hb hble ha0max
  unfold Unsafe at hunsafe ⊢
  omega

/-- **Staircase set characterization** (`thm:staircase` case (iii)): given the
first safe agreement `a_*`, the safe in-interval agreements are exactly the
up-set `{a : a ≥ a_*}`.  The forward direction is minimality; the backward
direction is `safe_up` (antitonicity). -/
theorem safe_iff_ge_firstSafe {aStar a : Nat}
    (hfs : S.IsFirstSafe aStar) (ha : S.amin ≤ a) (ha' : a ≤ S.amax) :
    S.safe a ↔ aStar ≤ a := by
  obtain ⟨h0, _, hsa, hmin⟩ := hfs
  constructor
  · intro hs
    rcases Nat.lt_or_ge a aStar with hlt | hge
    · exact absurd hs ((S.unsafe_iff_not_safe a).mp (hmin a ha hlt))
    · exact hge
  · intro hge
    exact S.safe_up h0 hge ha' hsa

/-! ## Endpoint / supremum characterization (`cor:v13-endpoint`) -/

/-- Largest safe **closed integer radius** `r_safe = n - a_*` (`cor:v13-endpoint`,
`cor:endpoint`). -/
def rSafe (aStar : Nat) : Nat := S.n - aStar

/-- Numerator of the **real closed-ball supremum** `(n - a_* + 1)/n` of safe radii
(`cor:v13-endpoint`); the denominator is `n`.  This endpoint is *not attained*. -/
def supNum (aStar : Nat) : Nat := S.n - aStar + 1

/-- **Closed-radius endpoint convention** (`cor:v13-endpoint`, `cor:endpoint`), in
`Nat`/rational form.  In the interior case with first safe agreement `a_*`:

* (i) the largest safe closed integer radius `r_safe = n - a_*` is **attained**
  (its agreement `a_*` is safe);
* (ii) the supremum numerator is `r_safe + 1 = n - a_* + 1`;
* (iii) the real supremum `(n - a_* + 1)/n` is **not attained**: the agreement
  `a_* - 1` at radius `supNum` is unsafe (`N(a_*-1) > B_*`);
* (iv) every safe agreement has radius numerator `< supNum`, so `(n-a_*+1)/n` is a
  strict upper bound for the safe radii — the rational-supremum statement.

Part (iv) is the "rational form": for grid radii `j/n` (`j = n - a`), safe
`⟺ j ≤ n - a_* ⟺ j < n - a_* + 1`, so the safe radii sit strictly below the
fraction `supNum/n`. -/
theorem endpoint_supremum {aStar : Nat}
    (hfs : S.IsFirstSafe aStar) (hint : S.amin < aStar) :
    S.safe (S.n - S.rSafe aStar)
      ∧ S.supNum aStar = S.rSafe aStar + 1
      ∧ S.Unsafe (S.n - S.supNum aStar)
      ∧ (∀ a, S.amin ≤ a → a ≤ S.amax → S.safe a → S.n - a < S.supNum aStar) := by
  have hfs' := hfs
  obtain ⟨h0, h1, hsa, hmin⟩ := hfs'
  have haStar_le_n : aStar ≤ S.n := Nat.le_trans h1 S.hn
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- (i) n - r_safe = a_*, which is safe
    have hEq : S.n - S.rSafe aStar = aStar := by unfold rSafe; omega
    rw [hEq]; exact hsa
  · -- (ii) supNum = r_safe + 1
    unfold rSafe supNum; omega
  · -- (iii) n - supNum = a_* - 1, which is unsafe
    have hEq : S.n - S.supNum aStar = aStar - 1 := by unfold supNum; omega
    rw [hEq]; exact hmin (aStar - 1) (by omega) (by omega)
  · -- (iv) every safe agreement's radius numerator is < supNum
    intro a ha ha' hs
    have hge : aStar ≤ a := (S.safe_iff_ge_firstSafe hfs ha ha').mp hs
    unfold supNum; omega

/-! ## Computable first-safe search (ties the abstract `a_*` to a fold) -/

/-- Linear first-match scan for the first safe agreement, `fuel`-bounded. -/
def firstSafeFrom (S : Staircase) : Nat → Nat → Nat
  | 0, cur => cur
  | Nat.succ fuel, cur => if S.N cur ≤ S.B then cur else S.firstSafeFrom fuel (cur + 1)

/-- The computable first-safe agreement: scan `I` from `amin` upward, returning
the first `a` with `N a ≤ B_*`. -/
def firstSafe (S : Staircase) : Nat := S.firstSafeFrom (S.amax - S.amin + 1) S.amin

/-- One-step unfolding of the scan (definitional). -/
theorem firstSafeFrom_succ (S : Staircase) (f cur : Nat) :
    S.firstSafeFrom (f + 1) cur =
      if S.N cur ≤ S.B then cur else S.firstSafeFrom f (cur + 1) := rfl

/-- **Search correctness.**  If every agreement in `[cur, aStar)` is unsafe and
`aStar` is safe and reachable within `fuel`, the scan from `cur` returns `aStar`. -/
theorem firstSafeFrom_eq (S : Staircase) (aStar : Nat) :
    ∀ fuel cur, cur ≤ aStar → aStar < cur + fuel →
      (∀ b, cur ≤ b → b < aStar → ¬ S.safe b) → S.safe aStar →
      S.firstSafeFrom fuel cur = aStar := by
  intro fuel
  induction fuel with
  | zero => intro cur hcur hlt _ _; omega
  | succ f ih =>
    intro cur hcur hlt hbelow hsafe
    rw [firstSafeFrom_succ]
    rcases Nat.lt_or_ge cur aStar with hlt2 | hge2
    · -- cur < aStar : unsafe here, recurse from cur+1
      have hnsc : ¬ (S.N cur ≤ S.B) := hbelow cur (Nat.le_refl cur) hlt2
      rw [if_neg hnsc]
      exact ih (cur + 1) (by omega) (by omega)
        (fun b hb hb2 => hbelow b (by omega) hb2) hsafe
    · -- cur = aStar : safe here, return cur
      have heq : cur = aStar := Nat.le_antisymm hcur hge2
      have hsc : S.N cur ≤ S.B := by rw [heq]; exact hsafe
      rw [if_pos hsc]; exact heq

/-- The computable `firstSafe` returns the abstract first safe agreement `a_*`. -/
theorem firstSafe_eq_of_isFirstSafe (S : Staircase) {aStar : Nat}
    (h : S.IsFirstSafe aStar) : S.firstSafe = aStar := by
  obtain ⟨h0, h1, hsa, hmin⟩ := h
  unfold firstSafe
  refine S.firstSafeFrom_eq aStar (S.amax - S.amin + 1) S.amin h0 ?_ ?_ hsa
  · have hI := S.hI; omega
  · exact fun b hb hb2 => (S.unsafe_iff_not_safe b).mp (hmin b hb hb2)

/-- **One-step certificate, computable form** (`prop:onestep`): the matched
adjacent pair `N a0 > B_*`, `N (a0+1) ≤ B_*` makes the scan return `a_* = a0+1`,
so `firstSafe = a0 + 1` literally. -/
theorem oneStep_firstSafe (S : Staircase) (a0 : Nat)
    (h0 : S.amin ≤ a0) (h1 : a0 + 1 ≤ S.amax)
    (hunsafe : S.Unsafe a0) (hsafe : S.safe (a0 + 1)) :
    S.firstSafe = a0 + 1 :=
  S.firstSafe_eq_of_isFirstSafe (S.oneStep_isFirstSafe a0 h0 h1 hunsafe hsafe)

/-! ## Axiom audit -/

#print axioms safe_up
#print axioms firstSafe_unique
#print axioms oneStep_isFirstSafe
#print axioms safe_iff_ge_firstSafe
#print axioms endpoint_supremum
#print axioms firstSafeFrom_eq
#print axioms firstSafe_eq_of_isFirstSafe
#print axioms oneStep_firstSafe

end Staircase

end StaircaseLogic
