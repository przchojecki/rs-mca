import cs25_cap_v12.BlueprintCommon
import cs25_cap_v12.MainCap

/-!
# Locator fibers and the map-smooth fiber lemma (`sec:fiber`, `sec:map-smooth`)

Fiber-construction results of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

These are the constructions that supply the list-mass input (`hfiber`) consumed by
`RSCap.universal_cap_of_fiber_list` / `RSCap.universal_cap_emca_of_fiber_list` in
`MainCap.lean`.

Proved here (no `sorry`):

* `lem_phi_fiber_ii` — `lem:phi-fiber`(ii): the divisibility-free map-smooth fiber
  lemma, with `ℓ₂ = ⌊k/a⌋ + 2`, `A₂ = a·ℓ₂`.  **Statement repaired and proved**:
  the previous skeleton left the folding polynomial `φ` untied to the base field
  `B` and was **false as stated** (see the repair note in the docstring; the paper
  requires `φ ∈ B[X]`, `def:map-smooth`).  With the value-level tie `hQB` restored,
  the lemma is proved in full, following the printed proof verbatim (locator
  `P_A = ∏_{b∈A}(Y−b)`, Vieta for the top two coefficients, composition
  injectivity, pigeonhole over `B`).
* `thm_phi_cap` — `thm:phi-cap`: the universal cap for map-smooth domains,
  assembling the repaired `lem_phi_fiber_ii` with the (already proved) reduction
  `RSCap.universal_cap_of_fiber_list`.  Inherits the `hQB` repair.
* `hasList_fiber_input` — the reusable translation from the word-level list
  certificate `HasList` (`BlueprintCommon.lean`) to the polynomial-level fiber
  input `hfiber` consumed by `MainCap.lean`.
* Auxiliary locator algebra: `locTail`, `locator_split`, `locTail_natDegree_le`,
  `locTail_eval_of_mem`, `locator_subset_eq` (private).

Still a skeleton (proof `sorry`):

* `lem_fiber_ii` — `lem:fiber`(ii): the multiplicative-coset power-map special
  case with `a ∣ k`.  **Out of scope for the circle-code route**: `cor_circle_grand`
  (`CircleCode.lean`) has odd `k = 2w+1` while every deployed folding scale `a` is
  even, so `a ∤ k` always (tex `:4010`) and only the divisibility-free
  `lem_phi_fiber_ii` is consumed.  `lem_fiber_ii` is not a literal instance of the
  proved lemma: its radius endpoint `ℓ₂ ≤ N` admits the edge case `ℓ₂ = N` that
  `lem_phi_fiber_ii` (with `ℓ₂ ≤ N − 1`) excludes, so it is left honestly sorried
  rather than silently weakened.

The pure fiber constructions are `B`-valued; the slope `z = −e₁(A)` is an elementary
symmetric function of a subset `A` of the quotient domain `Q = φ(D)`, hence lies in
`B` *provided `φ` maps the domain into `B`* — that is exactly the repaired
hypothesis — and the pigeonhole is over `B` rather than `F`.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- **`lem:fiber`(ii) — locator fibers are lists (multiplicative coset).**

Let `B ⊆ F`, let `dom : ι → F` be an injective, `B`-valued evaluation domain of
size `n = |ι|` that is `(x ↦ xᵃ, a)`-smooth with quotient order `N = n/a` (so
`a·N = n`), and suppose `a ∣ k` with `ℓ₂ = ρN + 2 ≤ N` (here `ρ = k/n`, so
`ρN = k/a`).  Then there is a slope value `z ∈ B` such that the received word
`u_z(x) = xᵏ⁺²ᵃ + z·xᵏ⁺ᵃ` carries a decoding list of at least `C(N, ℓ₂)/|B|`
pairwise-distinct codewords of `RS[F, D, k+1]` at radius `1 − ρ − 2/N`; equivalently
at radius `1 − (k+2a)/n`.

This is exactly the list-mass hypothesis consumed by
`RSCap.universal_cap_of_fiber_list`.

**Left honestly sorried (out of scope for the circle-code route).**  With `a ∣ k`
this is the `φ = Xᵃ` instance of the proved `lem_phi_fiber_ii` *except* at the edge
`ℓ₂ = N` (this statement allows `ℓ₂ ≤ N`, the divisibility-free lemma demands
`ℓ₂ ≤ N − 1`; the edge case has `C(N,N) = 1` and a single locator).  The census
target `cor_circle_grand` never consumes it: circle rows have odd `k = 2w+1` and
even `a`, so `a ∤ k` always (tex `:4010`; cf. `rem:no-divisibility` `:3801`). -/
theorem lem_fiber_ii (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {a N k ℓ₂ : ℕ} (ha : 0 < a) (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => x ^ a) a)
    (hak : a ∣ k) (hℓ₂ : ℓ₂ = k / a + 2) (hℓ₂N : ℓ₂ ≤ N) :
    ∃ (z : F) (_ : z ∈ B) (L : ℕ),
      (Nat.choose N ℓ₂ : ℝ) / (Fintype.card B : ℝ) ≤ (L : ℝ) ∧
      HasList (RSpoly dom (k + 1))
        (1 - (k : ℝ) / Fintype.card ι - 2 / N)
        (fun i => (dom i) ^ (k + 2 * a) + z * (dom i) ^ (k + a)) L := by
  sorry

/-! ### Locator algebra

For an `ℓ₂`-subset `A` of the quotient domain, the locator is
`P_A(Y) = ∏_{b∈A}(Y − b) = Y^{ℓ₂} + z_A·Y^{ℓ₂−1} + R_A(Y)` with `z_A = −e₁(A)`
and `deg R_A ≤ ℓ₂ − 2` (Vieta).  `locTail A ℓ₂` is the tail `R_A`. -/

/-- The tail `R_A` of the locator: `∏_{b∈A}(Y−b) − Y^{ℓ₂} − (−∑_{b∈A} b)·Y^{ℓ₂−1}`. -/
private noncomputable def locTail (A : Finset F) (ℓ₂ : ℕ) : Polynomial F :=
  (∏ b ∈ A, (X - C b)) - X ^ ℓ₂ - C (-∑ b ∈ A, b) * X ^ (ℓ₂ - 1)

omit [Fintype F] in
/-- The locator splits as `P_A = Y^{ℓ₂} + z_A·Y^{ℓ₂−1} + R_A` (definitional). -/
private theorem locator_split (A : Finset F) (ℓ₂ : ℕ) :
    (∏ b ∈ A, (X - C b) : Polynomial F)
      = X ^ ℓ₂ + C (-∑ b ∈ A, b) * X ^ (ℓ₂ - 1) + locTail A ℓ₂ := by
  unfold locTail; ring

omit [Fintype F] in
/-- The locator `∏_{b∈A}(Y−b)` is monic of degree `|A|`. -/
private theorem locator_monic (A : Finset F) :
    (∏ b ∈ A, (X - C b) : Polynomial F).Monic :=
  monic_prod_of_monic _ _ fun b _ => monic_X_sub_C b

omit [Fintype F] in
private theorem locator_natDegree (A : Finset F) {ℓ₂ : ℕ} (hAcard : A.card = ℓ₂) :
    (∏ b ∈ A, (X - C b) : Polynomial F).natDegree = ℓ₂ := by
  rw [natDegree_prod_of_monic _ _ fun b _ => monic_X_sub_C b,
    Finset.sum_const_nat fun b _ => natDegree_X_sub_C b, mul_one, hAcard]

omit [Fintype F] in
/-- **Vieta (top two coefficients).**  `deg R_A ≤ ℓ₂ − 2`: the `Y^{ℓ₂}` and
`Y^{ℓ₂−1}` coefficients of the locator are `1` and `−e₁(A)`, so the tail drops two
degrees. -/
private theorem locTail_natDegree_le {A : Finset F} {ℓ₂ : ℕ} (hAcard : A.card = ℓ₂)
    (h2 : 2 ≤ ℓ₂) : (locTail A ℓ₂).natDegree ≤ ℓ₂ - 2 := by
  have hdeg := locator_natDegree A hAcard
  have hnext : (∏ b ∈ A, (X - C b) : Polynomial F).coeff (ℓ₂ - 1) = -∑ b ∈ A, b := by
    have h1 := Polynomial.prod_X_sub_C_nextCoeff (s := A) (f := (id : F → F))
    simp only [id] at h1
    rwa [Polynomial.nextCoeff_of_natDegree_pos (by rw [hdeg]; omega), hdeg] at h1
  refine Polynomial.natDegree_le_iff_coeff_eq_zero.mpr fun m hm => ?_
  unfold locTail
  simp only [Polynomial.coeff_sub, Polynomial.coeff_C_mul, Polynomial.coeff_X_pow]
  rcases (by omega : m = ℓ₂ - 1 ∨ m = ℓ₂ ∨ ℓ₂ < m) with hm1 | hm1 | hm1
  · subst hm1
    rw [hnext, if_neg (by omega), if_pos rfl]
    ring
  · rw [hm1]
    have hc : (∏ b ∈ A, (X - C b) : Polynomial F).coeff ℓ₂ = 1 := by
      rw [← hdeg]; exact (locator_monic A).coeff_natDegree
    rw [hc, if_pos rfl, if_neg (by omega)]
    ring
  · have hc : (∏ b ∈ A, (X - C b) : Polynomial F).coeff m = 0 :=
      Polynomial.coeff_eq_zero_of_natDegree_lt (by rw [hdeg]; exact hm1)
    rw [hc, if_neg (by omega), if_neg (by omega)]
    ring

omit [Fintype F] in
/-- Evaluating the split locator at a root `y ∈ A`:
`y^{ℓ₂} + z_A·y^{ℓ₂−1} + R_A(y) = 0`. -/
private theorem locTail_eval_of_mem {A : Finset F} {ℓ₂ : ℕ} {y : F} (hy : y ∈ A) :
    y ^ ℓ₂ + (-∑ b ∈ A, b) * y ^ (ℓ₂ - 1) + (locTail A ℓ₂).eval y = 0 := by
  have h0 : (∏ b ∈ A, (X - C b) : Polynomial F).eval y = 0 := by
    rw [Polynomial.eval_prod]
    exact Finset.prod_eq_zero hy (by simp)
  have h1 := congrArg (Polynomial.eval y) (locator_split A ℓ₂)
  simp only [Polynomial.eval_add, Polynomial.eval_pow, Polynomial.eval_mul,
    Polynomial.eval_C, Polynomial.eval_X] at h1
  rw [h0] at h1
  exact h1.symm

omit [Fintype F] in
/-- **Injectivity of `A ↦ c_A` at a fixed slope** (the printed argument): if two
`ℓ₂`-subsets share the slope `z_A = z_{A'}` and their tail words agree on the whole
(injective, size `> k`) domain, then the tails agree as polynomials (a degree-`≤ k`
polynomial has `< n` roots), composition with the nonconstant `φ` is injective
(leading-coefficient argument), and equal locators force `A = A'` (root multisets). -/
private theorem locator_subset_eq (dom : ι → F) (hdom : Function.Injective dom)
    (φ : Polynomial F) {a k ℓ₂ : ℕ} (ha : 0 < a) (hφdeg : φ.natDegree = a)
    (h2 : 2 ≤ ℓ₂) (hak : a * (ℓ₂ - 2) ≤ k) (hkn : k < Fintype.card ι)
    {A A' : Finset F} (hA : A.card = ℓ₂) (hA' : A'.card = ℓ₂)
    (hz : (-∑ b ∈ A, b) = (-∑ b ∈ A', b))
    (heq : ∀ i, ((locTail A ℓ₂).comp φ).eval (dom i)
      = ((locTail A' ℓ₂).comp φ).eval (dom i)) :
    A = A' := by
  have hdegc : ∀ S : Finset F, S.card = ℓ₂ → ((locTail S ℓ₂).comp φ).natDegree ≤ k := by
    intro S hS
    rw [Polynomial.natDegree_comp, hφdeg]
    calc (locTail S ℓ₂).natDegree * a ≤ (ℓ₂ - 2) * a :=
          mul_le_mul_left (locTail_natDegree_le hS h2) a
      _ = a * (ℓ₂ - 2) := mul_comm _ _
      _ ≤ k := hak
  -- the two compositions agree on `n > k` points, hence are equal
  have hcompeq : (locTail A ℓ₂).comp φ = (locTail A' ℓ₂).comp φ := by
    by_contra hne
    set d : Polynomial F := (locTail A ℓ₂).comp φ - (locTail A' ℓ₂).comp φ with hd
    have hd0 : d ≠ 0 := sub_ne_zero.mpr hne
    have hdeg : d.natDegree ≤ k :=
      le_trans (Polynomial.natDegree_sub_le _ _) (max_le (hdegc A hA) (hdegc A' hA'))
    have himg : Finset.univ.image dom ⊆ d.roots.toFinset := by
      intro x hx
      obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hx
      rw [Multiset.mem_toFinset, Polynomial.mem_roots']
      refine ⟨hd0, ?_⟩
      show d.eval (dom i) = 0
      rw [hd, Polynomial.eval_sub, heq i, sub_self]
    have hcard : Fintype.card ι ≤ d.roots.toFinset.card := by
      rw [← Finset.card_univ, ← Finset.card_image_of_injective Finset.univ hdom]
      exact Finset.card_le_card himg
    have hroots : d.roots.toFinset.card ≤ k :=
      le_trans (le_trans (Multiset.toFinset_card_le _) (Polynomial.card_roots' d)) hdeg
    omega
  -- strip the composition (leading-coefficient argument)
  have htail : locTail A ℓ₂ = locTail A' ℓ₂ := by
    by_contra hne
    have hr0 : locTail A ℓ₂ - locTail A' ℓ₂ ≠ 0 := sub_ne_zero.mpr hne
    have hφ0 : φ ≠ 0 := by
      intro h
      rw [h, Polynomial.natDegree_zero] at hφdeg
      omega
    have hc0 : (locTail A ℓ₂ - locTail A' ℓ₂).comp φ = 0 := by
      rw [Polynomial.sub_comp]
      exact sub_eq_zero.mpr hcompeq
    have hlc : ((locTail A ℓ₂ - locTail A' ℓ₂).comp φ).leadingCoeff ≠ 0 := by
      rw [Polynomial.leadingCoeff_comp (by rw [hφdeg]; omega)]
      exact mul_ne_zero (Polynomial.leadingCoeff_ne_zero.mpr hr0)
        (pow_ne_zero _ (Polynomial.leadingCoeff_ne_zero.mpr hφ0))
    rw [hc0, Polynomial.leadingCoeff_zero] at hlc
    exact hlc rfl
  -- equal locators have equal root multisets
  have hloc : (∏ b ∈ A, (X - C b) : Polynomial F) = ∏ b ∈ A', (X - C b) := by
    rw [locator_split A ℓ₂, locator_split A' ℓ₂, htail, hz]
  have hval : A.val = A'.val := by
    have hr1 := Polynomial.roots_prod_X_sub_C A
    have hr2 := Polynomial.roots_prod_X_sub_C A'
    rw [← hr1, ← hr2, hloc]
  exact Finset.val_inj.mp hval

omit [Fintype F] in
/-- **`HasList` → fiber-input translation (reusable glue).**  A word-level list
certificate `HasList (RSpoly dom (k+1)) δ₀ U L` yields the polynomial-level data
consumed by `RSCap.universal_cap_of_fiber_list` / `universal_cap_emca_of_fiber_list`
at any radius `δ ≥ δ₀`: representative polynomials of degree `≤ k`, pairwise
distinct, each disagreeing with `U` on at most `δ·n` points. -/
theorem hasList_fiber_input (dom : ι → F) {k L : ℕ} {δ₀ δ : ℝ} (hδ : δ₀ ≤ δ)
    (hn : (0 : ℝ) < Fintype.card ι) {U : ι → F}
    (h : HasList (RSpoly dom (k + 1)) δ₀ U L) :
    ∃ P : Fin L → Polynomial F,
      (∀ i, (P i).degree ≤ (k : WithBot ℕ)) ∧
      (∀ i j, i ≠ j → P i ≠ P j) ∧
      (∀ i, ((Finset.univ.filter (fun x => (P i).eval (dom x) ≠ U x)).card : ℝ)
        ≤ δ * Fintype.card ι) := by
  classical
  obtain ⟨W, hWmem, hWinj, hWclose⟩ := h
  choose Q hQdeg hQeval using hWmem
  refine ⟨Q, fun i => ?_, fun i j hij hQeq => ?_, fun i => ?_⟩
  · rcases eq_or_ne (Q i) 0 with h0 | h0
    · rw [h0, Polynomial.degree_zero]; exact bot_le
    · have h1 : (Q i).natDegree < k + 1 :=
        (Polynomial.natDegree_lt_iff_degree_lt h0).mpr (hQdeg i)
      exact Polynomial.natDegree_le_iff_degree_le.mp (by omega)
  · exact hij (hWinj (funext fun x => by rw [hQeval i x, hQeval j x, hQeq]))
  · have hc := hWclose i
    simp only [relDist, numDiff] at hc
    rw [div_le_iff₀ hn] at hc
    have hset : Finset.univ.filter (fun x => (Q i).eval (dom x) ≠ U x)
        = Finset.univ.filter (fun x => U x ≠ W i x) := by
      ext x
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, hQeval i x]
      exact ne_comm
    rw [hset]
    calc ((Finset.univ.filter (fun x => U x ≠ W i x)).card : ℝ)
        ≤ δ₀ * Fintype.card ι := hc
      _ ≤ δ * Fintype.card ι := mul_le_mul_of_nonneg_right hδ (le_of_lt hn)

omit [Fintype F] in
/-- **`lem:phi-fiber`(ii) — divisibility-free map-smooth fiber lemma.**

Generalizes `lem_fiber_ii` from the power map to an arbitrary `(φ, a)`-smooth,
`B`-valued domain, and removes the hypothesis `a ∣ k`.  With `ℓ₂ = ⌊k/a⌋ + 2` and
`A₂ = a·ℓ₂ ∈ [k+a+1, k+2a]`, some slope `z ∈ B` makes
`u_z(x) = φ(x)^{ℓ₂} + z·φ(x)^{ℓ₂−1}` carry `≥ C(N, ℓ₂)/|B|` distinct codewords of
`RS[F, D, k+1]` at radius `1 − A₂/n`.  Here `φ` is (the evaluation of) a polynomial
of degree `a`.

**Statement repair (untied-binder defect class, graded FALSE AS STATED —
hand-verified counterexample, not machine-checked).**  The previous skeleton bound
`φ : Polynomial F` with nothing tying `φ` (or its values on the domain) to `B`,
while the paper requires `φ ∈ B[X]` (`def:map-smooth`, tex `:3744`: "let
`φ ∈ B[X]` have degree `a`") — this is what makes `Q = φ(D) ⊆ B` and hence
`z_A = −e₁(A) ∈ B`.  Counterexample to the untied statement: `F = F₁₆`,
`B = F₄`, `t ∈ F₁₆ ∖ F₄`, `φ = X + t`, `a = 1`, `ι = Fin 4`, `dom` an enumeration
of `F₄`, `k = 1`, `N = 4`, `ℓ₂ = 3`, `A₂ = 3`.  The conclusion demands `z ∈ F₄`
and one degree-`≤ 1` codeword agreeing with `u_z` on `≥ 3` of the `4` points; but
`u_z − c` is (as a polynomial in the domain coordinate) a monic cubic with
`X²`-coefficient `t + z ∉ F₄`, while a monic cubic vanishing on `3` distinct
points of `F₄` has `X²`-coefficient in `F₄` — contradiction for every `z ∈ B`,
and `4` agreements are impossible (degree `3`).  A Lean negation lemma would need
a concrete `GF(16)/GF(4)` instance (the `F₄/F₂` shrink is impossible since
`a = 1` forces `n ≤ |B|`), which is `decide`-infeasible at reasonable cost; the
counterexample is therefore documented here and the statement repaired, with no
formalized falsity claim.  **Repair:** the value-level tie
`hQB : ∀ i, φ.eval (dom i) ∈ B` (the minimal hypothesis making the printed proof
sound; the paper-faithful coefficient-level `φ ∈ B[X]` implies it given `hdomB`).

Proved in full, following the printed proof (tex `:3771`–`:3799`): Vieta for the
locator's top coefficients (`locTail_natDegree_le`), complete disjoint fibers for
the `A₂`-point agreement, composition injectivity (`locator_subset_eq`), and the
pigeonhole over `B`.  (`hdomB` is retained from the paper's setting `D ⊆ B`; the
proof of this list conclusion consumes only `hQB`, whence the unused-variable
warning — deliberately kept rather than strengthening the statement.) -/
theorem lem_phi_fiber_ii (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (φ : Polynomial F) {a N k ℓ₂ A₂ : ℕ}
    (ha : 0 < a) (hφdeg : φ.natDegree = a)
    (hQB : ∀ i, φ.eval (dom i) ∈ B)
    (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) a)
    (hℓ₂ : ℓ₂ = k / a + 2) (hℓ₂N : ℓ₂ ≤ N - 1) (hA₂ : A₂ = a * ℓ₂) :
    ∃ (z : F) (_ : z ∈ B) (L : ℕ),
      (Nat.choose N ℓ₂ : ℝ) / (Fintype.card B : ℝ) ≤ (L : ℝ) ∧
      HasList (RSpoly dom (k + 1))
        (1 - (A₂ : ℝ) / Fintype.card ι)
        (fun i => (φ.eval (dom i)) ^ ℓ₂ + z * (φ.eval (dom i)) ^ (ℓ₂ - 1)) L := by
  classical
  -- ℕ bookkeeping
  have hℓ₂2 : 2 ≤ ℓ₂ := by rw [hℓ₂]; exact Nat.le_add_left 2 (k / a)
  have hN3 : ℓ₂ + 1 ≤ N := by omega
  have hn0 : 0 < Fintype.card ι := by
    rw [← haN]; exact Nat.mul_pos ha (by omega)
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hℓ₂sub : ℓ₂ - 2 = k / a := by rw [hℓ₂]; exact Nat.add_sub_cancel _ _
  have hak : a * (ℓ₂ - 2) ≤ k := by
    rw [hℓ₂sub, mul_comm]
    exact Nat.div_mul_le_self k a
  have hA₂ge : k + a + 1 ≤ A₂ := by
    have h3 : A₂ = a * (k / a) + a * 2 := by rw [hA₂, hℓ₂, Nat.mul_add]
    have h1 : a * (k / a) + k % a = k := Nat.div_add_mod k a
    have h4 : k % a < a := Nat.mod_lt _ ha
    generalize a * (k / a) = m at h1 h3
    generalize k % a = s at h1 h4
    omega
  have hA₂n : A₂ + a ≤ Fintype.card ι := by
    have h1 : a * (ℓ₂ + 1) ≤ a * N := mul_le_mul_right hN3 a
    rw [haN] at h1
    calc A₂ + a = a * (ℓ₂ + 1) := by rw [hA₂, Nat.mul_add, Nat.mul_one]
      _ ≤ Fintype.card ι := h1
  have hkn : k < Fintype.card ι := by omega
  have hA₂le : A₂ ≤ Fintype.card ι := by omega
  -- the quotient domain `Q = φ(D)` has exactly `N` elements
  have hfib : ∀ b ∈ Finset.univ.image (fun i => φ.eval (dom i)),
      (Finset.univ.filter (fun j => φ.eval (dom j) = b)).card = a := by
    intro b hb
    obtain ⟨i₀, -, rfl⟩ := Finset.mem_image.mp hb
    exact hsmooth i₀
  have hQcard : (Finset.univ.image (fun i => φ.eval (dom i))).card = N := by
    have hsum : Fintype.card ι
        = (Finset.univ.image (fun i => φ.eval (dom i))).card * a := by
      rw [← Finset.card_univ,
        Finset.card_eq_sum_card_image (fun i => φ.eval (dom i)) Finset.univ]
      exact Finset.sum_const_nat hfib
    have h2 : a * N = a * (Finset.univ.image (fun i => φ.eval (dom i))).card := by
      rw [haN, hsum]; exact Nat.mul_comm _ _
    exact (Nat.eq_of_mul_eq_mul_left ha h2).symm
  -- each `ℓ₂`-subset of `Q` covers exactly `A₂` domain points
  have hSAcard : ∀ A ∈ (Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂,
      (Finset.univ.filter (fun i => φ.eval (dom i) ∈ A)).card = A₂ := by
    intro A hA
    obtain ⟨hAQ, hAcard⟩ := Finset.mem_powersetCard.mp hA
    have h1 : (Finset.univ.filter (fun i => φ.eval (dom i) ∈ A)).card
        = ∑ b ∈ A, ((Finset.univ.filter (fun i => φ.eval (dom i) ∈ A)).filter
            (fun i => φ.eval (dom i) = b)).card :=
      Finset.card_eq_sum_card_fiberwise fun i hi => (Finset.mem_filter.mp hi).2
    have h2 : ∀ b ∈ A, ((Finset.univ.filter (fun i => φ.eval (dom i) ∈ A)).filter
        (fun i => φ.eval (dom i) = b)).card = a := by
      intro b hb
      have hEq : (Finset.univ.filter (fun i => φ.eval (dom i) ∈ A)).filter
          (fun i => φ.eval (dom i) = b)
          = Finset.univ.filter (fun i => φ.eval (dom i) = b) := by
        ext i
        simp only [Finset.mem_filter, Finset.mem_univ, true_and]
        exact ⟨fun h => h.2, fun h => ⟨by rw [h]; exact hb, h⟩⟩
      rw [hEq]
      exact hfib b (hAQ hb)
    rw [h1, Finset.sum_const_nat h2, hAcard, hA₂]
    exact Nat.mul_comm ℓ₂ a
  -- slopes lie in `B` (uses the repaired hypothesis `hQB`)
  have hzB : ∀ A ∈ (Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂,
      (-∑ b ∈ A, b) ∈ B := by
    intro A hA
    obtain ⟨hAQ, -⟩ := Finset.mem_powersetCard.mp hA
    refine neg_mem (sum_mem fun b hb => ?_)
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp (hAQ hb)
    exact hQB i
  -- pigeonhole over `B`: an argmax slope `z`
  have h𝒜card : ((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).card
      = Nat.choose N ℓ₂ := by
    rw [Finset.card_powersetCard, hQcard]
  have h𝒜ne : ((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).Nonempty :=
    Finset.powersetCard_nonempty.mpr (by rw [hQcard]; omega)
  obtain ⟨z, hzimg, hzmax⟩ := Finset.exists_max_image
    (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
      (fun A => -∑ b ∈ A, b))
    (fun z' => (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).filter
      (fun A => (-∑ b ∈ A, b) = z')).card)
    (h𝒜ne.image _)
  have hzB' : z ∈ B := by
    obtain ⟨A, hA, rfl⟩ := Finset.mem_image.mp hzimg
    exact hzB A hA
  -- the argmax fiber
  set 𝒮 := ((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).filter
    (fun A => (-∑ b ∈ A, b) = z) with h𝒮
  have himgB : (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
      (fun A => -∑ b ∈ A, b)).card ≤ Fintype.card B := by
    have hsub : (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
        (fun A => -∑ b ∈ A, b)) ⊆ Finset.univ.image (fun b : B => (b : F)) := by
      intro x hx
      obtain ⟨A, hA, rfl⟩ := Finset.mem_image.mp hx
      exact Finset.mem_image.mpr ⟨⟨_, hzB A hA⟩, Finset.mem_univ _, rfl⟩
    calc (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
          (fun A => -∑ b ∈ A, b)).card
        ≤ (Finset.univ.image (fun b : B => (b : F))).card := Finset.card_le_card hsub
      _ = Fintype.card B := by
          rw [Finset.card_image_of_injective _ Subtype.coe_injective, Finset.card_univ]
  have hchoose_le : Nat.choose N ℓ₂ ≤ Fintype.card B * 𝒮.card := by
    have h1 : ((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).card
        = ∑ z' ∈ (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
            (fun A => -∑ b ∈ A, b)),
          (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).filter
            (fun A => (-∑ b ∈ A, b) = z')).card :=
      Finset.card_eq_sum_card_image _ _
    have h2 : ∑ z' ∈ (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
          (fun A => -∑ b ∈ A, b)),
        (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).filter
          (fun A => (-∑ b ∈ A, b) = z')).card
        ≤ (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
            (fun A => -∑ b ∈ A, b)).card * 𝒮.card := by
      calc ∑ z' ∈ (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
            (fun A => -∑ b ∈ A, b)),
          (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).filter
            (fun A => (-∑ b ∈ A, b) = z')).card
          ≤ ∑ _z' ∈ (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
              (fun A => -∑ b ∈ A, b)), 𝒮.card := Finset.sum_le_sum hzmax
        _ = (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
              (fun A => -∑ b ∈ A, b)).card * 𝒮.card :=
            Finset.sum_const_nat fun _ _ => rfl
    calc Nat.choose N ℓ₂
        = ((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).card :=
          h𝒜card.symm
      _ ≤ (((Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂).image
            (fun A => -∑ b ∈ A, b)).card * 𝒮.card := le_trans (le_of_eq h1) h2
      _ ≤ Fintype.card B * 𝒮.card := mul_le_mul_left himgB _
  have hBR : (0 : ℝ) < Fintype.card B := by exact_mod_cast Fintype.card_pos
  have hLreal : (Nat.choose N ℓ₂ : ℝ) / (Fintype.card B : ℝ) ≤ (𝒮.card : ℝ) := by
    rw [div_le_iff₀ hBR, mul_comm]
    exact_mod_cast hchoose_le
  -- membership data for elements of the argmax fiber
  have hmem𝒮 : ∀ A ∈ 𝒮,
      A ∈ (Finset.univ.image (fun i => φ.eval (dom i))).powersetCard ℓ₂
        ∧ (-∑ b ∈ A, b) = z := by
    intro A hA
    rw [h𝒮, Finset.mem_filter] at hA
    exact hA
  -- agreement of the received word with the tail codeword on the covered points
  have hagree : ∀ A ∈ 𝒮, ∀ i, φ.eval (dom i) ∈ A →
      φ.eval (dom i) ^ ℓ₂ + z * φ.eval (dom i) ^ (ℓ₂ - 1)
        = (-((locTail A ℓ₂).comp φ)).eval (dom i) := by
    intro A hA i hi
    obtain ⟨-, hAz⟩ := hmem𝒮 A hA
    have h0 := locTail_eval_of_mem (ℓ₂ := ℓ₂) hi
    simp only [Polynomial.eval_neg, Polynomial.eval_comp]
    rw [← hAz]
    linear_combination h0
  -- assemble the decoding list
  refine ⟨z, hzB', 𝒮.card, hLreal, ?_⟩
  refine ⟨fun j => fun i =>
    (-((locTail ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F) ℓ₂).comp φ)).eval (dom i),
    fun j => ?_, fun j j' hjj => ?_, fun j => ?_⟩
  · -- membership in `RS[F, D, k+1]`
    obtain ⟨hApc, -⟩ := hmem𝒮 _ (𝒮.equivFin.symm j).2
    obtain ⟨-, hAcard⟩ := Finset.mem_powersetCard.mp hApc
    refine ⟨-((locTail ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F) ℓ₂).comp φ),
      ?_, fun i => rfl⟩
    have hnd : (-((locTail ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F) ℓ₂).comp φ)).natDegree
        ≤ k := by
      rw [Polynomial.natDegree_neg, Polynomial.natDegree_comp, hφdeg]
      calc (locTail ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F) ℓ₂).natDegree * a
          ≤ (ℓ₂ - 2) * a := mul_le_mul_left (locTail_natDegree_le hAcard hℓ₂2) a
        _ = a * (ℓ₂ - 2) := mul_comm _ _
        _ ≤ k := hak
    exact lt_of_le_of_lt (Polynomial.natDegree_le_iff_degree_le.mp hnd)
      (by exact_mod_cast Nat.lt_succ_self k)
  · -- pairwise distinctness via `locator_subset_eq`
    obtain ⟨hApc, hAz⟩ := hmem𝒮 _ (𝒮.equivFin.symm j).2
    obtain ⟨hApc', hAz'⟩ := hmem𝒮 _ (𝒮.equivFin.symm j').2
    obtain ⟨-, hAcard⟩ := Finset.mem_powersetCard.mp hApc
    obtain ⟨-, hAcard'⟩ := Finset.mem_powersetCard.mp hApc'
    have hAA : ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F)
        = ((𝒮.equivFin.symm j' : {x // x ∈ 𝒮}) : Finset F) := by
      refine locator_subset_eq dom hdom φ ha hφdeg hℓ₂2 hak hkn hAcard hAcard'
        (by rw [hAz, hAz']) fun i => ?_
      have h1 := congrFun hjj i
      simpa using h1
    exact 𝒮.equivFin.symm.injective (Subtype.ext hAA)
  · -- closeness at radius `1 − A₂/n`
    obtain ⟨hApc, -⟩ := hmem𝒮 _ (𝒮.equivFin.symm j).2
    have hSA := hSAcard _ hApc
    have hsub : Finset.univ.filter (fun i =>
        φ.eval (dom i) ^ ℓ₂ + z * φ.eval (dom i) ^ (ℓ₂ - 1)
          ≠ (-((locTail ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F) ℓ₂).comp φ)).eval (dom i))
        ⊆ (Finset.univ.filter (fun i =>
            φ.eval (dom i) ∈ ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F)))ᶜ := by
      intro i hi
      rw [Finset.mem_compl]
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi ⊢
      exact fun hmem => hi (hagree _ (𝒮.equivFin.symm j).2 i hmem)
    have hcard2 : (Finset.univ.filter (fun i =>
        φ.eval (dom i) ^ ℓ₂ + z * φ.eval (dom i) ^ (ℓ₂ - 1)
          ≠ (-((locTail ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F) ℓ₂).comp φ)).eval (dom i))).card
        ≤ Fintype.card ι - A₂ := by
      calc _ ≤ ((Finset.univ.filter (fun i =>
            φ.eval (dom i) ∈ ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F)))ᶜ).card :=
          Finset.card_le_card hsub
        _ = Fintype.card ι - A₂ := by rw [Finset.card_compl, hSA]
    simp only [relDist, numDiff]
    rw [div_le_iff₀ hnR]
    calc ((Finset.univ.filter (fun i =>
          φ.eval (dom i) ^ ℓ₂ + z * φ.eval (dom i) ^ (ℓ₂ - 1)
            ≠ (-((locTail ((𝒮.equivFin.symm j : {x // x ∈ 𝒮}) : Finset F) ℓ₂).comp φ)).eval (dom i))).card : ℝ)
        ≤ ((Fintype.card ι - A₂ : ℕ) : ℝ) := by exact_mod_cast hcard2
      _ = (Fintype.card ι : ℝ) - A₂ := by rw [Nat.cast_sub hA₂le]
      _ = (1 - (A₂ : ℝ) / Fintype.card ι) * Fintype.card ι := by
          rw [sub_mul, one_mul, div_mul_cancel₀ _ (ne_of_gt hnR)]

/-- **`thm:phi-cap` — universal cap for map-smooth domains.**

Under the field-size hypothesis `(eq:hyp-phi)` `C(N, ℓ₂) ≥ |B|·(q/k + 1)` and the
map-smoothness of `lem_phi_fiber_ii`, the correlated-agreement error of
`C = RS[F, D, k]` exceeds the half-inverse-dimension threshold at every deep radius
`δ ∈ [1 − A₂/n, 1 − ρ − 1/n]`.  This is the `(φ, a)`-smooth analogue of the main
theorem `thm:main` and specializes to it when `φ = Xᵃ`, `D` a multiplicative coset,
and `a ∣ k`.

**Statement repair (inherited from `lem_phi_fiber_ii`, graded PLAUSIBLE here — no
counterexample constructed for this statement, so no falsity claim):** the previous
skeleton left `φ` untied to `B`.  The conclusion does not mention `z ∈ B`, but the
only known proof route needs the fiber list of size `≥ C(N,ℓ₂)/|B|`, whose
pigeonhole requires `B`-valued slopes; under `(eq:hyp-phi)` a pigeonhole over `F`
cannot deliver the required list size.  Same repair: `hQB`.

Proved: the repaired `lem_phi_fiber_ii` supplies the list at the left endpoint
`1 − A₂/n ≤ δ`, `hasList_fiber_input` translates it to the polynomial-level fiber
input, and the (already proved) `RSCap.universal_cap_of_fiber_list` closes.  The
paper's `ε_mca` band and `δ*_C` clause are not modeled here (the `emca` variant is
available downstream via `universal_cap_emca_of_fiber_list`, and is consumed
directly by `cor_circle_grand`). -/
theorem thm_phi_cap (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (φ : Polynomial F) {a N k ℓ₂ A₂ : ℕ}
    (hk : 0 < k) (ha : 0 < a) (hφdeg : φ.natDegree = a)
    (hQB : ∀ i, φ.eval (dom i) ∈ B)
    (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) a)
    (hℓ₂ : ℓ₂ = k / a + 2) (hℓ₂N : ℓ₂ ≤ N - 1) (hA₂ : A₂ = a * ℓ₂)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose N ℓ₂ : ℝ))
    (δ : ℝ) (hδlo : 1 - (A₂ : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ ≤ 1 - (k : ℝ) / Fintype.card ι - 1 / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < ecaErr (RSpoly dom k) δ δ := by
  classical
  have hℓ₂2 : 2 ≤ ℓ₂ := by rw [hℓ₂]; exact Nat.le_add_left 2 (k / a)
  have hn0 : 0 < Fintype.card ι := by
    rw [← haN]; exact Nat.mul_pos ha (by omega)
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hak : (k : ℝ) < (1 - δ) * Fintype.card ι := by
    have h1 : (k : ℝ) / Fintype.card ι + 1 / Fintype.card ι ≤ 1 - δ := by linarith
    have h2 := mul_le_mul_of_nonneg_right h1 (le_of_lt hnR)
    rw [add_mul, div_mul_cancel₀ _ (ne_of_gt hnR), div_mul_cancel₀ _ (ne_of_gt hnR)] at h2
    linarith
  obtain ⟨z, hzB, L, hLge, hlist⟩ :=
    lem_phi_fiber_ii dom hdom B hdomB φ ha hφdeg hQB haN hsmooth hℓ₂ hℓ₂N hA₂
  have hBR : (0 : ℝ) < Fintype.card B := by exact_mod_cast Fintype.card_pos
  have hqk : (0 : ℝ) < (Fintype.card F : ℝ) / k :=
    div_pos (lt_of_le_of_lt (Nat.cast_nonneg _) hq) (by exact_mod_cast hk)
  have hL1 : 1 ≤ L := by
    have hexp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        = (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k) + Fintype.card B := by ring
    have h1 : (1 : ℝ) ≤ (Nat.choose N ℓ₂ : ℝ) / (Fintype.card B : ℝ) := by
      rw [le_div_iff₀ hBR]
      have h2 : (0 : ℝ) ≤ (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k) :=
        le_of_lt (mul_pos hBR hqk)
      linarith [hyp]
    exact_mod_cast le_trans h1 hLge
  obtain ⟨P, hPdeg, hPdist, hPclose⟩ := hasList_fiber_input dom hδlo hnR hlist
  exact universal_cap_of_fiber_list dom hdom hk δ hak hq Fintype.card_pos hyp
    ⟨fun i => (φ.eval (dom i)) ^ ℓ₂ + z * (φ.eval (dom i)) ^ (ℓ₂ - 1), L, P,
      hL1, hPdeg, hPdist, hPclose, hLge⟩

end RSCap
