/-
  Stdlib-only (no mathlib) formalization of the M1 width-one ledger's exact
  combinatorial core: the (W1-first-root) partition identity from
  experimental/notes/m1/m1_width_one_fixedroot_closure.md.

      R1Flag(A) = sum_{x in Z} sum_{f=0}^{a-1} C(|Z_{>x}|, f).      (W1-first-root)

  With n = |Z| = q-1 and the ordered shadow, |Z_{>x}| runs over n-1,...,0, so the
  RHS is  outer (n-1) a = sum_{j=0}^{n-1} (sum_{f=0}^{a-1} C(j,f)),
  and  R1Flag = sum_{e=1}^{a} C(n,e).

  Engine: the hockey-stick / column-sum identity  sum_{m=0}^{N} C(m,f) = C(N+1,f+1).

  Uses the SAME local Pascal `choose` as RsMca/QuotientOverlap.lean, so it drops
  straight into the existing stdlib ledger. This file is prelude-only (no imports):
  `#print axioms W1.W1_first_root` and `W1.hockey` both report only
  `[propext, Quot.sound]` (no `sorry`/`native_decide`/`Classical.choice`).

  SCOPE: this is the EXACT (closed-count) side of `FixedRootOneRoot_r1`. The
  residual *bound* `WO_1(A_0) <= FixedRootOneRoot_r1(A_0) + O_sigma(Q^{sigma+1})`
  remains an open typed target (the width-one critical-tail reduction is
  CONDITIONAL); this file does not close it.
-/

namespace W1

/-- Local Pascal binomial (identical to RsMca/QuotientOverlap.lean `choose`). -/
def choose : Nat → Nat → Nat
  | _,    0    => 1
  | 0,    _+1  => 0
  | n+1, k+1 => choose n k + choose n (k+1)

/-- Column sum `sum_{m=0}^{N} C(m,f)` (the f-th column, rows 0..N). -/
def colSum : Nat → Nat → Nat
  | 0,    f => choose 0 f
  | N+1, f => colSum N f + choose (N+1) f

/-- Row prefix `sum_{f=0}^{k-1} C(M,f)` (first `k` entries of row `M`). -/
def rowPrefix (M : Nat) : Nat → Nat
  | 0    => 0
  | k+1 => rowPrefix M k + choose M k

/-- Outer sum `sum_{j=0}^{N} rowPrefix j a` = the (W1-first-root) RHS for n=N+1. -/
def outer : Nat → Nat → Nat
  | 0,    a => rowPrefix 0 a
  | N+1, a => outer N a + rowPrefix (N+1) a

/-- `R1Flag` shape: `sum_{e=1}^{a} C(n,e)`. -/
def R1Flag (n : Nat) : Nat → Nat
  | 0    => 0
  | a+1 => R1Flag n a + choose n (a+1)

/-- Hockey-stick / column-sum identity: `sum_{m=0}^{N} C(m,f) = C(N+1,f+1)`. -/
theorem hockey (N f : Nat) : colSum N f = choose (N+1) (f+1) := by
  induction N with
  | zero =>
      -- colSum 0 f = choose 0 f ; choose 1 (f+1) = choose 0 f + choose 0 (f+1) = choose 0 f
      simp only [colSum, choose]; omega
  | succ N ih =>
      -- colSum (N+1) f = colSum N f + choose (N+1) f = C(N+1,f+1)+C(N+1,f) = C(N+2,f+1)
      simp only [colSum, ih, choose]
      omega

/-- Distribution step: adding one level to the inner prefix adds a whole column. -/
theorem outer_succ_level (N a : Nat) :
    outer N (a+1) = outer N a + colSum N a := by
  induction N with
  | zero => simp only [outer, rowPrefix, colSum]
  | succ N ih =>
      simp only [outer, colSum, rowPrefix, ih]
      omega

theorem outer_zero_level (N : Nat) : outer N 0 = 0 := by
  induction N with
  | zero => simp only [outer, rowPrefix]
  | succ N ih => simp only [outer, rowPrefix, ih]

/-- **The (W1-first-root) identity**:  outer (n-1) a = R1Flag n a, stated as
    `outer N a = R1Flag (N+1) a` (so `n = N+1 = q-1`). -/
theorem W1_first_root (N a : Nat) : outer N a = R1Flag (N+1) a := by
  induction a with
  | zero => simp only [outer_zero_level, R1Flag]
  | succ a ih =>
      rw [outer_succ_level, ih, hockey]
      simp only [R1Flag]

/-! ## Cross-link to the brute-force numbers from the Python verifier.
    For `q`, set `n = q-1`, `a = (q-2)/2`.  These `decide`-check against the
    enumerated `R1Flag(brute)` column (q=6 -> 15, q=10 -> 255, q=14 -> 4095). -/

def aLevel (q : Nat) : Nat := (q - 2) / 2

theorem R1Flag_q6  : R1Flag 5  (aLevel 6)  = 15   := by decide
theorem R1Flag_q10 : R1Flag 9  (aLevel 10) = 255  := by decide
theorem R1Flag_q14 : R1Flag 13 (aLevel 14) = 4095 := by decide

/-- And the identity instance at q=14 (n=13): the RHS prefix-sum equals 4095 too. -/
theorem firstroot_q14 : outer 12 (aLevel 14) = 4095 := by
  rw [W1_first_root]; decide

end W1
