import RsMca.Basic

namespace RsMca

/-!
# High-agreement tangent staircase: the generalized ledger arithmetic

Stdlib-only (`Nat`) formalization of the *integer ledger* arithmetic in
`experimental/notes/high_agreement/tangent_staircase.tex` and
`experimental/data/generalized-ledgers/generalized_high_agreement_ledgers_summary.md`.

The finite-field theorems themselves -- the moving-root tangent floor
`LD_sw(C,a) >= n-a+1` and the very-high-agreement staircase
`LD_sw(C,a) = n-a+1` when `3a-2n >= k` -- are finite-field statements and are
not reproved here.  Everything proved in this file is the surrounding *integer*
ledger, which the notes currently carry as hand arithmetic:

* the range equivalence `3a - 2n >= k  <->  r <= floor((n-k)/3)`
  (`tangentExact_iff_radius`), where `r = n - a` is the radius and `R = n - k`;
* the line / curve / interleaved numerators and `line = degree-one curve`;
* monotonicity of every numerator in the radius `r`;
* the `2^-128` safety gate `N <= B_Q` and the first-unsafe-radius characterization;
* the exact `F_{17^32}`, rate-`1/2` row (`n=512, k=256`): `B_Q = 6` by kernel
  computation of `floor(17^32 / 2^128)`, the staircase pinned between agreement
  `506` (unsafe) and `507` (safe), and the largest safe integer radius `5`.

This replaces the hand calculation in `tangent_staircase.tex`
(Cor. `f17-32-exact-tangent-gate`) -- including the 39-digit bracket
`6 * 2^128 < 17^32 < 7 * 2^128` -- with a machine-checked certificate.  It is a
coding-ledger certificate, not a protocol theorem: it adds no challenge-field,
extension-lift, folding, query, or cryptographic term.
-/

/-- Code reserve `R = n - k`. -/
def reserveR (n k : Nat) : Nat := n - k

/-- Integer Hamming radius `r = n - a` at agreement `a`. -/
def radius (n a : Nat) : Nat := n - a

/-! ## Range equivalence `3a - 2n >= k  <->  r <= floor(R/3)` -/

/-- The very-high-agreement hypothesis `3a - 2n >= k`, written over `Nat` as
    `2n + k <= 3a` to avoid truncated subtraction. -/
def tangentExactHyp (n k a : Nat) : Prop := 2 * n + k ≤ 3 * a

/-- Equivalence of the two forms of the exact-range condition: the agreement
    form `3a - 2n >= k` is the same as the radius form `3 r <= R`. -/
theorem tangentExact_iff_radius (n k a : Nat) (hka : k ≤ a) (han : a ≤ n) :
    tangentExactHyp n k a ↔ 3 * radius n a ≤ reserveR n k := by
  unfold tangentExactHyp radius reserveR
  omega

/-! ## Generalized ledger numerators (exact high-agreement range) -/

/-- Line / no-loss CA / projective-slope MCA numerator: `n - a + 1 = r + 1`. -/
def lineNumerator (r : Nat) : Nat := r + 1

/-- Degree-`d` finite-parameter curve CA/MCA numerator `min(q, d (r+1))`. -/
def curveNumerator (q d r : Nat) : Nat := min q (d * (r + 1))

/-- Interleaved-list uniqueness numerator (any arity `mu >= 1`). -/
def interleavedNumerator : Nat := 1

theorem lineNumerator_eq (r : Nat) : lineNumerator r = r + 1 := rfl

/-- The line numerator is the degree-one curve numerator, as long as the curve
    cap `q` is not active (`r + 1 <= q`). -/
theorem line_is_degree_one (q r : Nat) (hq : r + 1 ≤ q) :
    curveNumerator q 1 r = lineNumerator r := by
  unfold curveNumerator lineNumerator
  rw [Nat.one_mul, Nat.min_eq_right hq]

theorem lineNumerator_mono {r r' : Nat} (h : r ≤ r') :
    lineNumerator r ≤ lineNumerator r' := by
  unfold lineNumerator; omega

theorem curveNumerator_mono_radius (q d : Nat) {r r' : Nat} (h : r ≤ r') :
    curveNumerator q d r ≤ curveNumerator q d r' := by
  unfold curveNumerator
  have h2 : d * (r + 1) ≤ d * (r' + 1) := Nat.mul_le_mul (Nat.le_refl d) (by omega)
  omega

/-- General common-denominator numerator `N_total(r) = ell + sum_i d_i (r+1)`,
    over line/curve degrees `ds` (line is `d = 1`) and `ell` interleaved-list
    terms.  Defined by direct recursion to avoid any `List.sum` import. -/
def sumMul (ds : List Nat) (r : Nat) : Nat :=
  match ds with
  | [] => 0
  | d :: t => d * (r + 1) + sumMul t r

def totalNumerator (ell : Nat) (ds : List Nat) (r : Nat) : Nat :=
  ell + sumMul ds r

theorem sumMul_mono (ds : List Nat) {r r' : Nat} (h : r ≤ r') :
    sumMul ds r ≤ sumMul ds r' := by
  induction ds with
  | nil => simp [sumMul]
  | cons d t ih =>
    simp only [sumMul]
    exact Nat.add_le_add (Nat.mul_le_mul (Nat.le_refl d) (by omega)) ih

theorem totalNumerator_mono_radius (ell : Nat) (ds : List Nat) {r r' : Nat}
    (h : r ≤ r') : totalNumerator ell ds r ≤ totalNumerator ell ds r' := by
  unfold totalNumerator
  exact Nat.add_le_add_left (sumMul_mono ds h) ell

/-- A line term plus one interleaved-list term has numerator `r + 2`. -/
theorem totalNumerator_line_plus_list (r : Nat) :
    totalNumerator 1 [1] r = r + 2 := by
  show 1 + (1 * (r + 1) + 0) = r + 2
  omega

/-! ## The `2^-128` safety gate -/

/-- `B_Q = floor(Q / 2^128)`, the integer budget for the soundness numerator. -/
def budgetBQ (Q : Nat) : Nat := Q / 2 ^ 128

/-- A numerator `N` over denominator `Q` clears target `2^-128` iff `N <= B_Q`. -/
def certified (N Q : Nat) : Prop := N ≤ budgetBQ Q

/-- Line term alone is safe at radius `r` iff `r + 1 <= B_Q`. -/
def lineSafe (r BQ : Nat) : Prop := lineNumerator r ≤ BQ

theorem lineSafe_iff (r BQ : Nat) : lineSafe r BQ ↔ r + 1 ≤ BQ := Iff.rfl

/-- The first unsafe line radius is exactly `r = B_Q`: radius `B_Q - 1` is safe,
    radius `B_Q` is not. -/
theorem line_first_unsafe (BQ : Nat) (h : 1 ≤ BQ) :
    lineSafe (BQ - 1) BQ ∧ ¬ lineSafe BQ BQ := by
  unfold lineSafe lineNumerator
  omega

/-- Line plus one interleaved-list term is safe iff `r + 2 <= B_Q`, i.e.
    `r <= B_Q - 2`. -/
def lineListSafe (r BQ : Nat) : Prop := lineNumerator r + interleavedNumerator ≤ BQ

theorem lineListSafe_iff (r BQ : Nat) : lineListSafe r BQ ↔ r + 2 ≤ BQ := by
  unfold lineListSafe lineNumerator interleavedNumerator; omega

/-! ## The exact `F_{17^32}`, rate-`1/2` row (`n = 512`, `k = 256`)

`tangent_staircase.tex`, Cor. `f17-32-exact-tangent-gate`. -/

def f17_n : Nat := 512
def f17_k : Nat := 256

/-- The line/challenge denominator for the row is `|F| = 17^32`. -/
def f17_Q : Nat := 17 ^ 32

def f17_BQ : Nat := budgetBQ f17_Q

/-! ### Tier-1 addition certificates

The roadmap requests addition certificates for the field-count gate, instead of
asking a reviewer to trust a raw large-numeral comparison.  The two kernel
equalities below are the positive slack witnesses for

`6 * 2^128 < 17^32 < 7 * 2^128`.
-/

/-- Positive slack in the lower field-count gate:
`6 * 2^128 + f17_lower_gate_slack = 17^32`. -/
def f17_lower_gate_slack : Nat := 326217393234836465063858652730341978625

/-- Positive slack in the upper field-count gate:
`17^32 + f17_upper_gate_slack = 7 * 2^128`. -/
def f17_upper_gate_slack : Nat := 14064973686101998399515954701426232831

/-- Addition certificate for the lower side of the `17^32 / 2^128` gate. -/
theorem f17_lower_add_certificate :
    6 * 2 ^ 128 + f17_lower_gate_slack = 17 ^ 32 := by decide

/-- Addition certificate for the upper side of the `17^32 / 2^128` gate. -/
theorem f17_upper_add_certificate :
    17 ^ 32 + f17_upper_gate_slack = 7 * 2 ^ 128 := by decide

theorem f17_lower_gate_slack_pos : 0 < f17_lower_gate_slack := by decide

theorem f17_upper_gate_slack_pos : 0 < f17_upper_gate_slack := by decide

/-- `floor(17^32 / 2^128) = 6` for this row. -/
theorem f17_BQ_eq : f17_BQ = 6 := by decide

/-- The 39-digit bracket proved from the explicit positive addition certificates:
`6*2^128 < 17^32 < 7*2^128`. -/
theorem f17_bracket : 6 * 2 ^ 128 < 17 ^ 32 ∧ 17 ^ 32 < 7 * 2 ^ 128 := by decide

/-- Same bracket as `f17_bracket`, but routed through the printed addition
certificates rather than direct comparison. -/
theorem f17_bracket_from_add_certificates :
    6 * 2 ^ 128 < 17 ^ 32 ∧ 17 ^ 32 < 7 * 2 ^ 128 := by
  constructor
  · rw [← f17_lower_add_certificate]
    have hpos := f17_lower_gate_slack_pos
    omega
  · rw [← f17_upper_add_certificate]
    have hpos := f17_upper_gate_slack_pos
    omega

/-- The budget `B_Q = 6` lies inside the exact tangent range cap
`(512 - 256) / 3 = 85`. -/
theorem f17_budget_inside_tangent_cap :
    f17_BQ = 6 ∧ reserveR f17_n f17_k / 3 = 85 ∧ f17_BQ ≤ reserveR f17_n f17_k / 3 := by
  rw [f17_BQ_eq]
  unfold reserveR f17_n f17_k
  decide

/-- Exact staircase value in the tangent range: `LD_sw(C,a) = n - a + 1`,
    specialized to this row.  (Valid for `a >= 427`, i.e. `3a - 2n >= k`.) -/
def f17_LDsw (a : Nat) : Nat := f17_n - a + 1

theorem f17_LDsw_506 : f17_LDsw 506 = 7 := rfl
theorem f17_LDsw_507 : f17_LDsw 507 = 6 := rfl

/-- Both endpoints lie in the exact tangent range `3a - 2n >= k`. -/
theorem f17_506_in_range : tangentExactHyp f17_n f17_k 506 := by
  unfold tangentExactHyp; decide
theorem f17_507_in_range : tangentExactHyp f17_n f17_k 507 := by
  unfold tangentExactHyp; decide

/-- The `2^-128` staircase is pinned between `506` and `507`: at agreement `507`
    the numerator clears the budget, at `506` it does not. -/
theorem f17_staircase :
    certified (f17_LDsw 507) f17_Q ∧ ¬ certified (f17_LDsw 506) f17_Q := by
  unfold certified f17_LDsw f17_Q budgetBQ f17_n
  decide

/-- The largest safe integer Hamming radius for this row is `5`; radius `6` is
    already unsafe.  (Radius `r = n - a`, so `r = 5 <-> a = 507`, `r = 6 <-> a = 506`.) -/
theorem f17_largest_safe_radius :
    lineSafe 5 f17_BQ ∧ ¬ lineSafe 6 f17_BQ := by
  rw [f17_BQ_eq]; unfold lineSafe lineNumerator; decide

/-- The radius bookkeeping matching the agreement endpoints. -/
theorem f17_radius_endpoints : radius f17_n 507 = 5 ∧ radius f17_n 506 = 6 := by
  decide

/-! ### Endpoint ratios

The partial-submission note records the endpoint conversion over rationals:
`5/512 < 6/512 = 3/256`.  We use normalized `Rat` constructors so the facts are
kernel `rfl`/Boolean computations, without importing Mathlib numeric tactics.
-/

def f17_safe_radius_ratio : Rat := Rat.normalize 5 512
def f17_unsafe_radius_ratio : Rat := Rat.normalize 6 512
def f17_three_over_256 : Rat := Rat.normalize 3 256

/-- Endpoint conversion over rationals: `5/512 < 6/512 = 3/256`. -/
theorem f17_endpoint_ratios :
    f17_safe_radius_ratio < f17_unsafe_radius_ratio ∧
      f17_unsafe_radius_ratio = f17_three_over_256 := by
  constructor <;> rfl

/-- Endpoint bookkeeping in both integer-radius and normalized-rational forms. -/
theorem f17_endpoint_conversions :
    radius f17_n 507 = 5 ∧ radius f17_n 506 = 6 ∧
      f17_safe_radius_ratio < f17_unsafe_radius_ratio ∧
      f17_unsafe_radius_ratio = f17_three_over_256 := by
  exact ⟨f17_radius_endpoints.1, f17_radius_endpoints.2,
    f17_endpoint_ratios.1, f17_endpoint_ratios.2⟩

end RsMca
