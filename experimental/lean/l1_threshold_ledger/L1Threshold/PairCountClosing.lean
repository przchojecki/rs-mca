namespace L1Threshold

/-!
# Theorem R closing: discrete Cauchy–Schwarz kills the `t = 3` mixed kernel set

Stdlib-only (no mathlib) formalization of the **closing arithmetic** of the
prime-`ell` onset theorem for background-free coset sunflowers over `F_p`:

* note  : `experimental/notes/l1/l1_prime_ell_onset.md`      (PR #223, Theorem R / Lemma R)
* note  : `experimental/notes/l1/l1_coset_mixed_vacancy_threshold.md` (PR #222, Theorem A)
* thresholds writeup: `experimental/thresholds.tex`.

## The gate this file certifies

In the graded `m = t+1` regime every mixed full-petal codeword produces a fixed
sector polynomial `Gamma` and a per-coset **retained count** `rho_j = #{x in b_j H : P(x)=0}`.
The field-theoretic pair-count (Lemma R, note §Lemma R — the `(*)` twisted-root
bound, which needs `F_p` polynomial root counting and is recorded as a typed
target `LemmaR_pairCount` / `TwistedRootBound` below) supplies

    sum_j rho_j (rho_j - 1)  <=  (ell-1)(ell-2)     with each   rho_j <= ell-1.

The theorem is **listed iff** the total retained `R = sum_j rho_j` reaches
`(m-t+1) ell = 2 ell`; so "no mixed minimal kernel set" is exactly `R <= 2 ell - 1`.
The note closes this by Cauchy–Schwarz over the `m = t+1` cosets. This file
machine-checks that **closing step as an exact integer inequality**, for the two
proved cells of the `ell = 5` frontier:

* `closing_four` : `t = 3`, `m = t+1 = 4` cosets  (note "Theorem R");
* `closing_three`: `t = 2`, `m = t+1 = 3` cosets  (note "`(2,3)` by the same proof").

Both conclude `R <= 2 ell - 1` from the pair-count budget and `ell >= 3`
(the strict `(ell-1)(ell-2) < ell(ell-2)` step is exactly where `ell > 2` enters).

The bound is **razor-tight** and the method boundary is **sharp in `t`**; both are
recorded as kernel-checked (`decide`) certificates:

* `tightness_four` : the profile `[3,2,2,2]` at `ell = 5` attains the pair-count
  budget with equality AND hits `R = 2 ell - 1 = 9` (note §Tightness, `p in {41,61}`);
* `noclose_five`   : at `t = 4` (`m = 5`, `ell = 7`) the profile `[3,3,3,3,3]`
  meets the pair-count budget yet has `R = 15 >= 2 ell = 14`, so the closing FAILS
  — the pair-count argument closes *exactly* `t = 3` (note §Scope).

Everything here is `Nat` arithmetic proved by `omega` over atomic products and by
kernel `decide`: no `sorry`, no `native_decide`, no mathlib. `#print axioms` at the
foot reports the standard `[propext, Quot.sound]` only.

## Method note (no `ring` in core)

Lean's core stdlib has no `ring`/`nlinarith`, so every quadratic identity is
distributed by hand with `Nat.add_mul` / `Nat.mul_add` / `Nat.mul_comm` and then
closed by `omega`, which treats each product `x*y` as an opaque non-negative atom.
Discrete Cauchy–Schwarz is assembled from the six (resp. three) pairwise AM–GM
facts `2 x y <= x^2 + y^2`.
-/

/-! ## Discrete algebra core -/

/-- Binomial-free square of a sum: `(x+y)^2 = x^2 + 2xy + y^2`. -/
theorem sq_add (x y : Nat) : (x + y) * (x + y) = x * x + 2 * (x * y) + y * y := by
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add, Nat.mul_comm y x]; omega

/-- Cross-product expansion `(a+b)(c+d) = ac + ad + bc + bd`. -/
theorem mul_expand2 (a b c d : Nat) : (a + b) * (c + d) = a * c + a * d + b * c + b * d := by
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add]; omega

/-- Discrete AM–GM: `2 x y <= x^2 + y^2` over `Nat` (proved by the `(x-y)^2 >= 0`
    identity, made subtraction-free by splitting on `x <= y`). -/
theorem amgm (x y : Nat) : 2 * (x * y) ≤ x * x + y * y := by
  rcases Nat.le_total x y with h | h
  · obtain ⟨k, rfl⟩ := Nat.le.dest h
    rw [sq_add x k, Nat.mul_add]; omega
  · obtain ⟨k, rfl⟩ := Nat.le.dest h
    rw [sq_add y k, Nat.add_mul, Nat.mul_comm k y]; omega

/-- Four-term square expansion. -/
theorem sq4 (a b c d : Nat) : (a + b + c + d) * (a + b + c + d) =
    a*a + b*b + c*c + d*d + 2*(a*b) + 2*(a*c) + 2*(a*d) + 2*(b*c) + 2*(b*d) + 2*(c*d) := by
  rw [show a + b + c + d = (a + b) + (c + d) from by omega,
      sq_add (a + b) (c + d), sq_add a b, sq_add c d, mul_expand2 a b c d]; omega

/-- Three-term square expansion. -/
theorem sq3 (a b c : Nat) : (a + b + c) * (a + b + c) =
    a*a + b*b + c*c + 2*(a*b) + 2*(a*c) + 2*(b*c) := by
  rw [show a + b + c = (a + b) + c from by omega, sq_add (a + b) c, sq_add a b, Nat.add_mul]
  omega

/-! ## Discrete Cauchy–Schwarz (`(sum x_i)^2 <= m * sum x_i^2`) -/

/-- Cauchy–Schwarz over four naturals: `(a+b+c+d)^2 <= 4 (a^2+b^2+c^2+d^2)`. -/
theorem cs4 (a b c d : Nat) :
    (a + b + c + d) * (a + b + c + d) ≤ 4 * (a*a + b*b + c*c + d*d) := by
  rw [sq4]
  have h1 := amgm a b; have h2 := amgm a c; have h3 := amgm a d
  have h4 := amgm b c; have h5 := amgm b d; have h6 := amgm c d
  omega

/-- Cauchy–Schwarz over three naturals: `(a+b+c)^2 <= 3 (a^2+b^2+c^2)`. -/
theorem cs3 (a b c : Nat) :
    (a + b + c) * (a + b + c) ≤ 3 * (a*a + b*b + c*c) := by
  rw [sq3]
  have h1 := amgm a b; have h2 := amgm a c; have h3 := amgm b c
  omega

/-! ## The quadratic closing step -/

/-- Auxiliary product expansions used to feed `omega` after substituting
    `L = e + 3`, `R = 2e + 6 + f` (so all `Nat` subtraction disappears). -/
private theorem h4e (e : Nat) : (2 * e) * (2 * e) = 4 * (e * e) := by
  rw [Nat.mul_assoc 2 e (2 * e), Nat.mul_comm e (2 * e), Nat.mul_assoc 2 e e]; omega

private theorem h5e (e f : Nat) : (2 * e) * f = 2 * (e * f) := Nat.mul_assoc 2 e f

private theorem hP (e : Nat) : (e + 2) * (e + 1) = e * e + 3 * e + 2 := by
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add]; omega

private theorem hRR (e f : Nat) :
    (2*e + 6 + f) * (2*e + 6 + f) = 4*(e*e) + 4*(e*f) + f*f + 24*e + 12*f + 36 := by
  rw [sq_add (2*e + 6) f, sq_add (2*e) 6, h4e e, Nat.add_mul (2*e) 6 f, h5e e f]; omega

/-- **Discrete quadratic closing.** If `R^2 <= 4 R + 4 (L-1)(L-2)` and `L >= 3`
    then `R <= 2 L - 1`. This is the integer form of "the positive root of
    `R^2 - 4R - 4(L-1)(L-2)` is `< 2L`, hence the integer `R` is `<= 2L-1`",
    valid precisely because `L > 2`. -/
theorem quad_closing {R L : Nat} (hL : 3 ≤ L)
    (h : R * R ≤ 4 * R + 4 * ((L - 1) * (L - 2))) : R ≤ 2 * L - 1 := by
  obtain ⟨e, rfl⟩ : ∃ e, L = e + 3 := ⟨L - 3, by omega⟩
  have hL1 : (e + 3) - 1 = e + 2 := by omega
  have hL2 : (e + 3) - 2 = e + 1 := by omega
  rw [hL1, hL2, hP e] at h
  rcases Nat.lt_or_ge R (2 * e + 6) with hlt | hge
  · omega
  · exfalso
    obtain ⟨f, rfl⟩ : ∃ f, R = 2 * e + 6 + f := ⟨R - (2 * e + 6), by omega⟩
    rw [hRR e f] at h; omega

/-- Pair-to-square bookkeeping: `rho (rho - 1) + rho = rho^2` (subtraction-free). -/
theorem pair_sq (x : Nat) : x * (x - 1) + x = x * x := by
  cases x with
  | zero => rfl
  | succ n => rw [Nat.succ_sub_one, Nat.mul_succ]

/-! ## Theorem R closing (the shipped gate) -/

/-- **Theorem R, `t = 3` (`m = 4` cosets).** From the Lemma-R pair-count budget
    `sum_j rho_j(rho_j-1) <= (ell-1)(ell-2)` over the four cosets and `ell >= 3`,
    the total retained count satisfies `R = sum_j rho_j <= 2 ell - 1`. Hence
    `R < 2 ell = (m-t+1) ell`, the mixed codeword is unlisted, and (by the PR #219
    reconstruction bijection, cited) there is no mixed minimal kernel set.

    Note: only the pair-count budget and `ell >= 3` are needed; the per-coset
    caps `rho_j <= ell-1` (used upstream to prove Lemma R) are not required by the
    closing, so this is the sharper statement. -/
theorem closing_four (r0 r1 r2 r3 ell : Nat) (hell : 3 ≤ ell)
    (hpair : r0*(r0-1) + r1*(r1-1) + r2*(r2-1) + r3*(r3-1) ≤ (ell-1)*(ell-2)) :
    r0 + r1 + r2 + r3 ≤ 2 * ell - 1 := by
  have hcs := cs4 r0 r1 r2 r3
  have e0 := pair_sq r0; have e1 := pair_sq r1
  have e2 := pair_sq r2; have e3 := pair_sq r3
  apply quad_closing hell
  omega

/-- The note's/task's **full-hypothesis** form of Theorem R (`t = 3`): the
    per-coset caps `rho_j <= ell - 1` are stated explicitly alongside the
    pair-count budget, exactly as written. The caps are what the upstream field
    argument uses to establish Lemma R (the budget); the closing itself needs only
    the budget, so here they are recorded (underscore binders) and discharged by
    `closing_four`. `3 <= ell` is `ell > 2`. -/
theorem closing_four_capped (r0 r1 r2 r3 ell : Nat) (hell : 3 ≤ ell)
    (_hc0 : r0 ≤ ell - 1) (_hc1 : r1 ≤ ell - 1) (_hc2 : r2 ≤ ell - 1) (_hc3 : r3 ≤ ell - 1)
    (hpair : r0*(r0-1) + r1*(r1-1) + r2*(r2-1) + r3*(r3-1) ≤ (ell-1)*(ell-2)) :
    r0 + r1 + r2 + r3 ≤ 2 * ell - 1 :=
  closing_four r0 r1 r2 r3 ell hell hpair

/-- **Theorem R, `t = 2` (`m = 3` cosets).** Same conclusion `R <= 2 ell - 1`
    over three cosets (note: `(2,3)` cell, closed "by the same proof run over its
    `m = 3` cosets"). -/
theorem closing_three (r0 r1 r2 ell : Nat) (hell : 3 ≤ ell)
    (hpair : r0*(r0-1) + r1*(r1-1) + r2*(r2-1) ≤ (ell-1)*(ell-2)) :
    r0 + r1 + r2 ≤ 2 * ell - 1 := by
  have hcs := cs3 r0 r1 r2
  have e0 := pair_sq r0; have e1 := pair_sq r1; have e2 := pair_sq r2
  apply quad_closing hell
  omega

/-! ## `List`-indexed restatement (the `sum_j` form of the note) -/

/-- `sum_j rho_j`. -/
def retained (rhos : List Nat) : Nat := rhos.foldr (· + ·) 0

/-- `sum_j rho_j (rho_j - 1)` — the Lemma-R pair-count functional. -/
def pairCount (rhos : List Nat) : Nat :=
  (rhos.map (fun r => r * (r - 1))).foldr (· + ·) 0

/-- Theorem R closing over a length-4 coset list, phrased with the note's `sum_j`. -/
theorem closing_four_list (rhos : List Nat) (hlen : rhos.length = 4)
    {ell : Nat} (hell : 3 ≤ ell) (hpair : pairCount rhos ≤ (ell - 1) * (ell - 2)) :
    retained rhos ≤ 2 * ell - 1 := by
  match rhos, hlen with
  | [r0, r1, r2, r3], _ =>
    have hp : r0*(r0-1) + r1*(r1-1) + r2*(r2-1) + r3*(r3-1) ≤ (ell-1)*(ell-2) := by
      simp only [pairCount, List.map_cons, List.map_nil, List.foldr_cons, List.foldr_nil] at hpair
      omega
    have hgoal := closing_four r0 r1 r2 r3 ell hell hp
    simp only [retained, List.foldr_cons, List.foldr_nil]
    omega

/-- Theorem R closing over a length-3 coset list. -/
theorem closing_three_list (rhos : List Nat) (hlen : rhos.length = 3)
    {ell : Nat} (hell : 3 ≤ ell) (hpair : pairCount rhos ≤ (ell - 1) * (ell - 2)) :
    retained rhos ≤ 2 * ell - 1 := by
  match rhos, hlen with
  | [r0, r1, r2], _ =>
    have hp : r0*(r0-1) + r1*(r1-1) + r2*(r2-1) ≤ (ell-1)*(ell-2) := by
      simp only [pairCount, List.map_cons, List.map_nil, List.foldr_cons, List.foldr_nil] at hpair
      omega
    have hgoal := closing_three r0 r1 r2 ell hell hp
    simp only [retained, List.foldr_cons, List.foldr_nil]
    omega

/-! ## Sharpness certificates (kernel `decide`, axiom-free) -/

/-- **Razor-tightness** (note §Tightness, `p in {41,61}`). At `ell = 5`, `m = 4`
    the retained profile `[3,2,2,2]` attains the Lemma-R budget with EQUALITY
    (`sum rho(rho-1) = 12 = (ell-1)(ell-2)`) and simultaneously reaches the bound
    `R = 2 ell - 1 = 9`. So `closing_four` is sharp — no argument with slack in the
    pair-count could exclude `R = 2 ell - 1`. -/
theorem tightness_four :
    (3*(3-1) + 2*(2-1) + 2*(2-1) + 2*(2-1) = (5-1)*(5-2)) ∧ (3 + 2 + 2 + 2 = 2*5 - 1) := by
  decide

/-- The tight profile really satisfies the `closing_four` hypotheses, and the
    conclusion holds at the boundary. -/
theorem tightness_four_inrange :
    (3*(3-1) + 2*(2-1) + 2*(2-1) + 2*(2-1) ≤ (5-1)*(5-2)) ∧ (3 + 2 + 2 + 2 ≤ 2*5 - 1) := by
  decide

/-- **Method boundary is sharp in `t`** (note §Scope). At `t = 4` (`m = 5` cosets,
    `ell = 7`) the profile `[3,3,3,3,3]` still meets the Lemma-R pair-count budget
    (`sum rho(rho-1) = 30 = (ell-1)(ell-2)`) yet has `R = 15 >= 2 ell = 14`. Thus the
    naive `m = 5` analogue of `closing_four` is FALSE: the pair-count budget alone
    cannot force `R <= 2 ell - 1` beyond `t = 3`. Pair-counting closes exactly `t = 3`. -/
theorem noclose_five :
    (3*(3-1) + 3*(3-1) + 3*(3-1) + 3*(3-1) + 3*(3-1) ≤ (7-1)*(7-2))
      ∧ ¬ (3 + 3 + 3 + 3 + 3 ≤ 2*7 - 1) := by
  decide

/-- A second `t = 4` non-closure witness, `ell = 11`, profile `[5,5,5,5,3]`
    (note §Scope: "`t=4, ell=11`: 23"). Budget `86 <= 90`, but `R = 23 >= 2 ell = 22`. -/
theorem noclose_five_11 :
    (5*(5-1) + 5*(5-1) + 5*(5-1) + 5*(5-1) + 3*(3-1) ≤ (11-1)*(11-2))
      ∧ ¬ (5 + 5 + 5 + 5 + 3 ≤ 2*11 - 1) := by
  decide

/-! ## Typed targets — the field-theoretic inputs NOT proved here

Mirroring `RsMca`'s `CERTIFICATION_MAP` convention: these record the exact
statements this stdlib layer *consumes as hypotheses*. Their proofs live over
`F_p` (polynomial root counting / the PR #219 reconstruction bijection) and are
outside the stdlib-only scope; they are supplied by
`experimental/scripts/verify_l1_prime_ell_onset.py` (exhaustive at `ell = 5`) and
the note's finite-field argument. -/

/-- Lemma R (note §Lemma R), the pair-count budget over the `m = t+1` cosets, as
    the interface `Prop` that `closing_four` / `closing_three` take as hypothesis.
    Upstream it is itself a double-count: the ordered pairs of same-level retained
    points inject, via `(x, omega = x'/x)`, into the union over `omega in mu_ell`,
    `omega != 1` (there are `ell - 1` of them) of the level-coincidence sets
    `{x : Gamma(x) = Gamma(omega x)}`, each of size `<= ell - 2` by the `(*)`
    twisted-root bound (which needs PRIME `ell` and `F_p` root counting — the
    finite-field content, supplied by the note and
    `verify_l1_prime_ell_onset.py`, not stdlib-certifiable). The same injective
    packing shape is formalized in `FiberDoubleCount.double_count`. -/
def LemmaR_pairCount (rhos : List Nat) (ell : Nat) : Prop :=
  pairCount rhos ≤ (ell - 1) * (ell - 2)

/-! ## Axiom audit -/

#print axioms closing_four
#print axioms closing_three
#print axioms closing_four_list
#print axioms tightness_four
#print axioms noclose_five

end L1Threshold
