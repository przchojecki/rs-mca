import Std

/-!
# A6: stdlib-only parity-split core for the prize-rate quotient floor

Goal (Paper B `slackMCA_v4` thm:exactcount, prize rate `rho = 1/2`):

    quotientFloor n1 (n1+1) = (3^n1 - 1)/2.

`quotientFloor n1 (n1+1)` is (re-indexing `u -> t = ell'-2u`) the sum of
`choose n1 t * 2^t` over the residue class `t ≡ n1+1 (mod 2)`, `0 ≤ t ≤ n1-1`,
i.e. over the FULL parity class opposite to `n1` in `[0,n1]` (the `t = n1` term has
`t ≡ n1`, so it is excluded; nothing past `n1-1` survives the `u ≤ n1-t` gate).

So the floor is the "minority" 2-weighted binomial sum, and the whole identity is
the binomial parity split of `(1±2)^n1`:

    Σ_{t even} C(n,t)2^t = (3^n + (-1)^n)/2,   Σ_{t odd} C(n,t)2^t = (3^n - (-1)^n)/2.

This file PROVES that split, stdlib-only (no mathlib), via the Pascal recurrence
the two sums satisfy:

    Se(n+1) = Se(n) + 2·So(n),   So(n+1) = 2·Se(n) + So(n),   (Se,So)(0) = (1,0).

(That recurrence is Pascal `C(n+1,t)=C(n,t)+C(n,t-1)` reindexed; it is verified
numerically against the literal `choose`-sums and against `quotientFloor` for
n ≤ 39 in the A6 Python verifier.) Everything is over `Int` so the alternating
`(-1)^n` term is exact, and every proof is `rfl`/`omega`/short induction — no
`ring`, no `pow_succ`, no mathlib; the inductive theorems use no `decide`.

The ONE remaining obligation (left as a typed target, exactly like the existing
`QuotientFloorHalfClosed`) is the *combinatorial bridge*: that the `List.range`
foldr defining `quotientFloor n1 (n1+1)` equals this minority sum `PO`/`PE`. That
bridge is pure bookkeeping (reindex the foldr, discharge the `if`-guard, apply
Pascal) but needs a stdlib finite-sum/foldr development; it is NOT done here.
-/

namespace A6

/-- Paired even/odd 2-weighted binomial sums, carried by their Pascal recurrence,
    over `Int`. Numerically `(pep n).1 = Σ_{t even} C(n,t) 2^t` and
    `(pep n).2 = Σ_{t odd} C(n,t) 2^t`. -/
def pep : Nat → Int × Int
  | 0     => (1, 0)
  | n + 1 => ((pep n).1 + 2 * (pep n).2, 2 * (pep n).1 + (pep n).2)

/-- Even-index 2-weighted binomial sum `Σ_{t even} C(n,t) 2^t`. -/
def PE (n : Nat) : Int := (pep n).1
/-- Odd-index 2-weighted binomial sum `Σ_{t odd} C(n,t) 2^t` (the rho=1/2 minority
    floor when `n` is even). -/
def PO (n : Nat) : Int := (pep n).2

@[simp] theorem PE_zero : PE 0 = 1 := rfl
@[simp] theorem PO_zero : PO 0 = 0 := rfl
theorem PE_succ (n : Nat) : PE (n + 1) = PE n + 2 * PO n := rfl
theorem PO_succ (n : Nat) : PO (n + 1) = 2 * PE n + PO n := rfl

/-- `3^n` carried as a recurrence (so no `Int` `^`-lemma dependency is needed). -/
def T : Nat → Int
  | 0     => 1
  | n + 1 => 3 * T n

/-- The alternating sign `(-1)^n`, as a recurrence. -/
def D : Nat → Int
  | 0     => 1
  | n + 1 => - D n

theorem T_succ (n : Nat) : T (n + 1) = 3 * T n := rfl
theorem D_succ (n : Nat) : D (n + 1) = - D n := rfl

/-- `T` really is `3^n` (stated via the `Nat` power, cast to `Int`). -/
theorem T_eq (n : Nat) : T n = ((3 ^ n : Nat) : Int) := by
  induction n with
  | zero => rfl
  | succ k ih => rw [T_succ, ih, Nat.pow_succ]; omega

/-- TOTAL: `Σ_t C(n,t) 2^t = 3^n`  (the `(1+2)^n` row). -/
theorem pe_add_po (n : Nat) : PE n + PO n = T n := by
  induction n with
  | zero => rfl
  | succ k ih => rw [PE_succ, PO_succ, T_succ]; omega

/-- SIGNED SPLIT: `Σ_{even} - Σ_{odd} = (-1)^n`  (the `(1-2)^n` row). -/
theorem pe_sub_po (n : Nat) : PE n - PO n = D n := by
  induction n with
  | zero => rfl
  | succ k ih => rw [PE_succ, PO_succ, D_succ]; omega

/-- Even-index closed form: `2·Σ_{t even} C(n,t)2^t = 3^n + (-1)^n`. -/
theorem two_pe (n : Nat) : 2 * PE n = T n + D n := by
  have h1 := pe_add_po n; have h2 := pe_sub_po n; omega

/-- Odd-index closed form: `2·Σ_{t odd} C(n,t)2^t = 3^n - (-1)^n`. -/
theorem two_po (n : Nat) : 2 * PO n = T n - D n := by
  have h1 := pe_add_po n; have h2 := pe_sub_po n; omega

/-! ### Parity evaluation of the alternating sign -/

/-- `D` has period two. -/
theorem D_two (n : Nat) : D (n + 2) = D n := by rw [D_succ, D_succ]; omega

/-- `D` is `1` on even indices. -/
theorem D_even (m : Nat) : D (2 * m) = 1 := by
  induction m with
  | zero => rfl
  | succ k ih => rw [show 2 * (k + 1) = 2 * k + 2 from by omega, D_two, ih]

/-- `D` is `-1` on odd indices. -/
theorem D_odd (m : Nat) : D (2 * m + 1) = -1 := by rw [D_succ, D_even]

/-! ### The prize-rate minority floor closed form `2·minority + 1 = 3^n`

At `rho = 1/2` the floor is the parity class OPPOSITE to `n`:
the odd-`t` sum `PO` when `n` is even, the even-`t` sum `PE` when `n` is odd.
In BOTH cases `2·floor + 1 = 3^n`. -/

/-- `n = 2m` even: the floor is the odd sum and `2·PO(2m) + 1 = 3^{2m}`. -/
theorem minorityFloor_even (m : Nat) : 2 * PO (2 * m) + 1 = T (2 * m) := by
  have h := two_po (2 * m); rw [D_even] at h; omega

/-- `n = 2m+1` odd: the floor is the even sum and `2·PE(2m+1) + 1 = 3^{2m+1}`. -/
theorem minorityFloor_odd (m : Nat) : 2 * PE (2 * m + 1) + 1 = T (2 * m + 1) := by
  have h := two_pe (2 * m + 1); rw [D_odd] at h; omega

/-- Unified prize-rate floor (over `Int`): the opposite-parity 2-weighted binomial
    sum `minorityFloor n` satisfies `2·floor + 1 = 3^n`, hence `= (3^n - 1)/2`. -/
def minorityFloor (n : Nat) : Int := if n % 2 = 0 then PO n else PE n

theorem minorityFloor_closed (n : Nat) : 2 * minorityFloor n + 1 = T n := by
  unfold minorityFloor
  rcases Nat.mod_two_eq_zero_or_one n with h | h
  · rw [if_pos h, show n = 2 * (n / 2) from by omega]
    exact minorityFloor_even (n / 2)
  · rw [if_neg (by omega), show n = 2 * (n / 2) + 1 from by omega]
    exact minorityFloor_odd (n / 2)

/-! ### Concrete checks tying the recurrence to Paper B's published floor counts -/

-- `n = 8`: odd sum `PO 8 = 3280 = (3^8-1)/2 = A(16,9)`; even sum `PE 8 = 3281`.
example : PO 8 = 3280 := by decide
example : PE 8 = 3281 := by decide
example : 2 * PO 8 + 1 = (3 : Int) ^ 8 := by decide
-- `n = 16`: `PO 16 = 21523360 = (3^16-1)/2 = A(32,17)`.
example : PO 16 = 21523360 := by decide
-- `n = 7` (odd): even sum `PE 7 = 1093 = (3^7-1)/2`, the prize-rate floor there.
example : PE 7 = 1093 := by decide
example : 2 * PE 7 + 1 = (3 : Int) ^ 7 := by decide

/-! ### The remaining obligation: the foldr/`choose` bridge (typed target)

`quotientFloor n1 (n1+1)` (Paper B's `List.range` foldr of guarded
`choose n1 t * 2^t` terms) equals the prize-rate minority floor proved above.
This is the only gap between this PROVED parity split and the published closed
form; it is pure foldr/Pascal bookkeeping and is left unproved here. -/

/-- Typed target: the published floor foldr equals the proved minority sum.
    `quotientFloorNat` is whatever Paper B's `quotientFloor n1 (n1+1)` evaluates to
    as a `Nat`; the claim is its `Int` cast is `minorityFloor n1`. Proving this plus
    `minorityFloor_closed` gives `quotientFloor n1 (n1+1) = (3^n1 - 1)/2`. -/
def QuotientFloorBridge (quotientFloorNat : Nat → Nat) : Prop :=
  ∀ n1 : Nat, (quotientFloorNat n1 : Int) = minorityFloor n1

end A6
