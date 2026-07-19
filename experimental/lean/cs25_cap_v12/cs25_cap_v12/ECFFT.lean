import cs25_cap_v12.QuotientRemainder

/-!
# Blueprint: rational-map fiber floors and the genus-one / ECFFT rows (`sec:ecfft`, `sec:answers-isogeny`)

Skeletons (proofs `sorry`) for the rational-map generalization of the fiber lemma and
its ECFFT/genus-one consequences in

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

A *rationally smooth* domain uses a rational map `ψ = f/g` (`f, g ∈ B[X]` coprime,
`a = deg f > e = deg g ≥ 0`, `g` nonvanishing on `D`); it is `(ψ, a)`-smooth if every
nonempty fiber has exactly `a` elements.  The FFTree domains of ECFFT are `(ψ, 2)`-smooth
of degree type `(a, e) = (2, 1)` for each `2`-isogeny's `x`-coordinate map.

**Update (skeleton falsity-and-repair packet, 2026-07-18):**
`prop_graded_rational_floor` was **false as stated** (vacuous `hδ`, list radius `δ`
unconstrained; machine-checked negation `prop_graded_rational_floor_false` over
`ZMod 2`); it is now statement-repaired to the paper's deep-band form and **proved**
as a wrapper over `thm_quotient_remainder_deep_floor`.  `cor_ecfft_macroscopic`
received two PLAUSIBLE-graded statement-hygiene repairs (`Δ` band bound, `hfB`/`hgB`
subfield ties) and stays sorried.

**Update (constructive discharge packet, 2026-07-19):** `prop_rational_floor` and
`cor_ecfft_onestep` are now **proved**, statements byte-identical to the audited
skeletons.  The floor is discharged constructively via the paper's locator expansion
`Λ_A = ∑_j (−1)^j e_j(A) f^{ℓ−j} g^j` (tex `:4852`–`:4856`), formalized as
`rational_locator_expansion` (remainder degree `≤ a(ℓ−2) + 2e`), a pigeonhole over
the `|B|` slopes `z = −e₁(A)`, and the distinct-interpolant fact
`eq_of_eval_eq_of_natDegree_lt`; the one-step corollary feeds the resulting list at
deep agreement `A = 2ℓ = k + 2` to the proved bridge
`cor_quotient_remainder_trigger` (`thm:quotient-remainder-deep-floor` +
`ecaFloor_trigger`), exactly as `cor_first_grid_cap_one` did at `A = k + 1`.
`cor_ecfft_macroscopic` is untouched (documented `hyp`-form residual).

Formalized here:

* `prop_rational_floor` — `prop:rational-floor`: the unified `(a, e)` fiber floor,
  producing a list of `≥ C(N, ℓ)/|B|` codewords of `RS[F, D, k'+1]` with
  `k' = aℓ − 2(a−e)` at radius `1 − aℓ/n`, from the word
  `u_z = (f^ℓ + z·f^{ℓ−1}g)|_D`.
* `cor_ecfft_onestep` — `cor:ecfft-onestep`: every ECFFT row `(a,e) = (2,1)` has an
  unsafe first staircase step: `ε_ca(C, 1 − ρ − 2/n) > (1/2k)(1 − n/q)`.
* `prop_graded_rational_floor` — `prop:graded-rational-floor`: graded prefix floors on
  every rational scale, giving a macroscopic unsafe band (statement-repaired; proved).
* `cor_ecfft_macroscopic` — `cor:ecfft-macroscopic`: the resulting macroscopic universal
  cap for genus-one rows (statement-repaired, PLAUSIBLE grade; sorried).
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- `(ψ, a)`-smoothness of a domain for a rational map `ψ = f/g` (`def:rational-smooth`):
`g` is nonvanishing on `D` and every fiber of `x ↦ f(x)/g(x)` has exactly `a` elements. -/
def RationalSmooth (dom : ι → F) (f g : Polynomial F) (a : ℕ) : Prop :=
  (∀ i, g.eval (dom i) ≠ 0) ∧ DomSmooth dom (fun x => f.eval x / g.eval x) a

omit [Fintype F] in
/-- Evaluation of a polynomial with all coefficients in a subfield `B` at a point of
`B` lands in `B`.  This is the coefficient-level form of the subfield tie
`f, g ∈ B[X]` of `def:rational-smooth` (tex `:4834`): it places the fiber values
`ψ(x) = f(x)/g(x)` and the slopes `z = −e₁(A)` of `prop:rational-floor` in `B`.
(The package elsewhere avoids this by taking value-level hypotheses, cf. the
`hQB` comment at `lem_phi_fiber_ii`; here the coefficient-level statement is what
the audited skeleton carries, so the implication is proved.) -/
theorem eval_mem_of_coeff_mem (B : Subfield F) {p : Polynomial F}
    (hp : ∀ n, p.coeff n ∈ B) {x : F} (hx : x ∈ B) : p.eval x ∈ B := by
  rw [Polynomial.eval_eq_sum_range]
  exact B.toSubring.sum_mem fun i _ => B.mul_mem (hp i) (B.pow_mem hx i)

omit [Fintype F] in
/-- **Locator expansion for `prop:rational-floor` (tex `:4852`–`:4856`).**
For any finite slope set `S`, the rational locator `Λ_S = ∏_{c∈S}(f − c·g)` differs
from its two leading expansion terms `f^{|S|} − e₁(S)·f^{|S|−1}·g` by the `j ≥ 2`
tail of `Λ_S = ∑_j (−1)^j e_j(S) f^{|S|−j} g^j`, whose degree is at most
`a(|S|−2) + 2e` (each `j ≥ 2` term has degree `a|S| − j(a−e) ≤ a(|S|−2) + 2e`);
for `|S| ≤ 1` the tail vanishes identically.  Proved by induction on `S`; the
`|S| ≤ 1` clause is load-bearing for the induction step (the `|S| = 2` remainder
`e₂·g²` must not pick up a spurious `deg ≤ a + 2e` contribution). -/
theorem rational_locator_expansion (f g : Polynomial F) {a e : ℕ}
    (hae : e < a) (hfdeg : f.natDegree = a) (hgdeg : g.natDegree = e) (S : Finset F) :
    ((∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ S.card
        + Polynomial.C (∑ c ∈ S, c) * f ^ (S.card - 1) * g).natDegree
      ≤ a * (S.card - 2) + 2 * e
    ∧ (S.card ≤ 1 →
        (∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ S.card
          + Polynomial.C (∑ c ∈ S, c) * f ^ (S.card - 1) * g = 0) := by
  classical
  induction S using Finset.induction_on with
  | empty => simp
  | @insert c₀ S hc₀ ih =>
    rcases Nat.eq_zero_or_pos S.card with hS0 | hSpos
    · -- the singleton case: the remainder vanishes identically
      have hSempty : S = ∅ := Finset.card_eq_zero.mp hS0
      subst hSempty
      have hzero : (∏ c ∈ ({c₀} : Finset F), (f - Polynomial.C c * g))
          - f ^ ({c₀} : Finset F).card
          + Polynomial.C (∑ c ∈ ({c₀} : Finset F), c) * f ^ (({c₀} : Finset F).card - 1) * g
          = 0 := by
        simp only [Finset.prod_singleton, Finset.sum_singleton, Finset.card_singleton]
        ring_nf
      rw [show insert c₀ (∅ : Finset F) = {c₀} from rfl] at *
      constructor
      · rw [hzero]; simp
      · intro _; exact hzero
    · -- the insert step at `|S| = m + 1`
      obtain ⟨m, hm⟩ : ∃ m, S.card = m + 1 := ⟨S.card - 1, by omega⟩
      obtain ⟨ihdeg, ihzero⟩ := ih
      rw [hm] at ihdeg ihzero
      simp only [Nat.add_sub_cancel] at ihdeg ihzero
      rw [Finset.prod_insert hc₀, Finset.sum_insert hc₀,
        Finset.card_insert_of_notMem hc₀, hm]
      simp only [Nat.add_sub_cancel]
      -- the remainder recursion r' = e₂-term + (f − c₀·g)·r
      have hE : (f - Polynomial.C c₀ * g) * (∏ c ∈ S, (f - Polynomial.C c * g))
          - f ^ (m + 1 + 1) + Polynomial.C (c₀ + ∑ c ∈ S, c) * f ^ (m + 1) * g
          = Polynomial.C c₀ * Polynomial.C (∑ c ∈ S, c) * f ^ m * g ^ 2
            + (f - Polynomial.C c₀ * g)
              * ((∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ (m + 1)
                + Polynomial.C (∑ c ∈ S, c) * f ^ m * g) := by
        simp only [map_add]
        ring
      rw [hE]
      refine ⟨?_, fun h => absurd h (by omega)⟩
      have hidx : m + 1 + 1 - 2 = m := by omega
      rw [hidx]
      refine le_trans (Polynomial.natDegree_add_le _ _) (max_le ?_ ?_)
      · -- the `e₂` term `C c₀ · C σ · f^m · g²`
        have hCC : (Polynomial.C c₀ * Polynomial.C (∑ c ∈ S, c) : Polynomial F).natDegree
            = 0 := by
          rw [← map_mul]; exact Polynomial.natDegree_C _
        have hfm : (f ^ m).natDegree ≤ a * m := by
          calc (f ^ m).natDegree ≤ m * f.natDegree := Polynomial.natDegree_pow_le
            _ = a * m := by rw [hfdeg, Nat.mul_comm]
        have hg2 : (g ^ 2).natDegree ≤ 2 * e := by
          calc (g ^ 2).natDegree ≤ 2 * g.natDegree := Polynomial.natDegree_pow_le
            _ = 2 * e := by rw [hgdeg]
        calc (Polynomial.C c₀ * Polynomial.C (∑ c ∈ S, c) * f ^ m * g ^ 2).natDegree
            ≤ (Polynomial.C c₀ * Polynomial.C (∑ c ∈ S, c) * f ^ m).natDegree
              + (g ^ 2).natDegree := Polynomial.natDegree_mul_le
          _ ≤ ((Polynomial.C c₀ * Polynomial.C (∑ c ∈ S, c)).natDegree
              + (f ^ m).natDegree) + (g ^ 2).natDegree :=
                Nat.add_le_add_right Polynomial.natDegree_mul_le _
          _ ≤ (0 + a * m) + 2 * e :=
                Nat.add_le_add (Nat.add_le_add (le_of_eq hCC) hfm) hg2
          _ = a * m + 2 * e := by omega
      · -- the `(f − c₀·g) · r` term; for `m = 0` the strengthened clause kills `r`
        have hfg : (f - Polynomial.C c₀ * g).natDegree ≤ a := by
          refine le_trans (Polynomial.natDegree_sub_le _ _) (max_le (le_of_eq hfdeg) ?_)
          refine le_trans Polynomial.natDegree_mul_le ?_
          rw [Polynomial.natDegree_C, hgdeg]
          omega
        rcases Nat.eq_zero_or_pos m with hm0 | hmpos
        · subst hm0
          rw [ihzero (by omega), mul_zero]
          simp
        · obtain ⟨t, rfl⟩ : ∃ t, m = t + 1 := ⟨m - 1, by omega⟩
          calc ((f - Polynomial.C c₀ * g)
              * ((∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ (t + 1 + 1)
                + Polynomial.C (∑ c ∈ S, c) * f ^ (t + 1) * g)).natDegree
              ≤ (f - Polynomial.C c₀ * g).natDegree
                + ((∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ (t + 1 + 1)
                  + Polynomial.C (∑ c ∈ S, c) * f ^ (t + 1) * g).natDegree :=
                Polynomial.natDegree_mul_le
            _ ≤ a + (a * (t + 1 + 1 - 2) + 2 * e) := Nat.add_le_add hfg ihdeg
            _ = a * (t + 1) + 2 * e := by
                have h1 : t + 1 + 1 - 2 = t := by omega
                rw [h1]
                have h2 : a * (t + 1) = a * t + a := by ring
                omega

omit [Fintype F] in
/-- Two polynomials of degree `< n` agreeing on an injective `n`-point evaluation
domain are equal.  This is the distinct-interpolant fact used inline by
`hasList_first_grid` (root-counting on the difference), extracted as a standalone
lemma for the fixed-slope injectivity step of `prop:rational-floor`
(tex `:4860`: "if `c_A = c_{A'}` as words then as polynomials"). -/
theorem eq_of_eval_eq_of_natDegree_lt (dom : ι → F) (hdom : Function.Injective dom)
    {p q : Polynomial F} (hp : p.natDegree < Fintype.card ι)
    (hq : q.natDegree < Fintype.card ι)
    (h : ∀ i, p.eval (dom i) = q.eval (dom i)) : p = q := by
  classical
  by_contra hne
  have hsub : p - q ≠ 0 := sub_ne_zero.mpr hne
  have hnd : (p - q).natDegree < Fintype.card ι :=
    lt_of_le_of_lt (Polynomial.natDegree_sub_le p q) (max_lt hp hq)
  have hsubroots : Finset.univ.image dom ⊆ (p - q).roots.toFinset := by
    intro x hx
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hx
    rw [Multiset.mem_toFinset, Polynomial.mem_roots hsub]
    simp [Polynomial.IsRoot, h i]
  have hn_le : Fintype.card ι ≤ (p - q).natDegree := by
    calc Fintype.card ι = (Finset.univ.image dom).card := by
          rw [Finset.card_image_of_injective _ hdom, Finset.card_univ]
      _ ≤ (p - q).roots.toFinset.card := Finset.card_le_card hsubroots
      _ ≤ Multiset.card (p - q).roots := Multiset.toFinset_card_le _
      _ ≤ (p - q).natDegree := Polynomial.card_roots' _
  omega

/-- **`prop:rational-floor` — rational-map fiber floor, unified `(a, e)` form.**

Let `dom` be `(ψ, a)`-smooth over `B` with `ψ = f/g` of degree type `(a, e)`,
`a > e ≥ 0`, `N = n/a`, and `2 ≤ ℓ ≤ N − 1`.  With `k' = aℓ − 2(a − e)`, some slope
`z ∈ B` makes the word `u_z(x) = f(x)^ℓ + z·f(x)^{ℓ−1}·g(x)` carry a list of at least
`C(N, ℓ)/|B|` distinct codewords of `RS[F, D, k'+1]` at radius `1 − aℓ/n` (i.e. at
agreement `aℓ = k' + 2(a − e)`).

**Update (constructive discharge, 2026-07-19; statement byte-identical):** proved,
following the paper's proof (tex `:4851`–`:4861`) verbatim: for each `ℓ`-subset `A`
of the `N` fiber values (which lie in `B` by `eval_mem_of_coeff_mem` and
`Subfield.div_mem`), the locator `Λ_A = ∏_{b∈A}(f − b·g)` vanishes on the `aℓ`
fiber points (`DomSmooth` double count) and expands as
`f^ℓ − e₁(A) f^{ℓ−1} g + r_A` with `deg r_A ≤ a(ℓ−2) + 2e = k'`
(`rational_locator_expansion`), so `u_{z_A} − Λ_A|_D = (−r_A)|_D ∈ RS[F, D, k'+1]`
for the slope `z_A = −e₁(A) ∈ B`; at a fixed slope the map `A ↦ (−r_A)|_D` is
injective (`eq_of_eval_eq_of_natDegree_lt` on `Λ_A`, degree `≤ aℓ < n`, plus fiber
recovery of `A` from the root set); pigeonholing the `C(N, ℓ)` subsets over the at
most `|B|` slopes yields a slope `z` whose fiber has size `≥ C(N, ℓ)/|B|`.  Note
the proof does not need the paper's coprimality of `f, g` (tex `:4834`): all
evaluations happen at domain points where `g ≠ 0`, and injectivity routes through
root recovery rather than the transcendence argument of tex `:4860`. -/
theorem prop_rational_floor (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {a e N k' ℓ : ℕ}
    (hfB : ∀ n, f.coeff n ∈ B) (hgB : ∀ n, g.coeff n ∈ B)
    (hae : e < a) (hfdeg : f.natDegree = a) (hgdeg : g.natDegree = e)
    (haN : a * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g a)
    (hℓlo : 2 ≤ ℓ) (hℓhi : ℓ ≤ N - 1) (hk' : k' = a * ℓ - 2 * (a - e)) :
    ∃ (z : F) (_ : z ∈ B) (L : ℕ),
      (Nat.choose N ℓ : ℝ) / (Fintype.card B : ℝ) ≤ (L : ℝ) ∧
      HasList (RSpoly dom (k' + 1))
        (1 - (a * ℓ : ℝ) / Fintype.card ι)
        (fun i => (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)) L := by
  classical
  set φ : F → F := fun x => f.eval x / g.eval x with hφ
  obtain ⟨hgne, hsm⟩ := hsmooth
  -- numerology
  have ha0 : 0 < a := by omega
  have hN3 : 3 ≤ N := by omega
  have hn : Fintype.card ι = a * N := haN.symm
  have hn0 : 0 < Fintype.card ι := by rw [hn]; exact Nat.mul_pos ha0 (by omega)
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have haℓn : a * ℓ ≤ Fintype.card ι := by
    rw [hn]; exact Nat.mul_le_mul_left a (by omega)
  obtain ⟨s, hNs⟩ : ∃ s, N = s + 3 := ⟨N - 3, by omega⟩
  have hk'eq : k' = a * (ℓ - 2) + 2 * e := by
    obtain ⟨t, rfl⟩ : ∃ t, ℓ = t + 2 := ⟨ℓ - 2, by omega⟩
    have h1 : a * (t + 2) = a * t + 2 * a := by ring
    have h2 : a * (t + 2 - 2) = a * t := by congr 1
    omega
  -- fiber values lie in B
  have hφB : ∀ i, φ (dom i) ∈ B := fun i =>
    B.div_mem (eval_mem_of_coeff_mem B hfB (hdomB i))
      (eval_mem_of_coeff_mem B hgB (hdomB i))
  -- the fiber image `ψ(D)` and its size N
  set T : Finset F := Finset.univ.image (fun i => φ (dom i)) with hT
  have hfiber : ∀ c ∈ T, (Finset.univ.filter (fun i => φ (dom i) = c)).card = a := by
    intro c hc
    obtain ⟨i₀, -, rfl⟩ := Finset.mem_image.mp hc
    exact hsm i₀
  have hTcard : T.card = N := by
    have hcount : Fintype.card ι
        = ∑ c ∈ T, (Finset.univ.filter (fun i => φ (dom i) = c)).card := by
      rw [← Finset.card_univ]
      exact Finset.card_eq_sum_card_image (fun i => φ (dom i)) Finset.univ
    rw [Finset.sum_congr rfl hfiber, Finset.sum_const, smul_eq_mul] at hcount
    have h1 : a * T.card = a * N := by rw [Nat.mul_comm a T.card]; omega
    exact Nat.eq_of_mul_eq_mul_left ha0 h1
  -- locator evaluation: vanishing on fibers, and fiber recovery
  have hvanish : ∀ (S : Finset F) (i : ι), φ (dom i) ∈ S →
      (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i) = 0 := by
    intro S i hi
    rw [Polynomial.eval_prod]
    refine Finset.prod_eq_zero hi ?_
    simp only [Polynomial.eval_sub, Polynomial.eval_mul, Polynomial.eval_C]
    show f.eval (dom i) - f.eval (dom i) / g.eval (dom i) * g.eval (dom i) = 0
    rw [div_mul_cancel₀ _ (hgne i)]
    ring
  have hrecover : ∀ (S : Finset F) (i : ι),
      (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i) = 0 → φ (dom i) ∈ S := by
    intro S i h0
    rw [Polynomial.eval_prod, Finset.prod_eq_zero_iff] at h0
    obtain ⟨c', hc'S, hc'⟩ := h0
    simp only [Polynomial.eval_sub, Polynomial.eval_mul, Polynomial.eval_C] at hc'
    have hval : φ (dom i) = c' := by
      show f.eval (dom i) / g.eval (dom i) = c'
      rw [sub_eq_zero] at hc'
      rw [hc', mul_div_cancel_right₀ _ (hgne i)]
    rwa [hval]
  -- membership: the codeword attached to a slope set S, via the expansion lemma
  have hkey : ∀ S : Finset F, S.card = ℓ →
      (fun i => (f.eval (dom i)) ^ ℓ
          + (-∑ c ∈ S, c) * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)
          - (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i))
        ∈ RSpoly dom (k' + 1) := by
    intro S hScard
    obtain ⟨hdeg, -⟩ := rational_locator_expansion f g hae hfdeg hgdeg S
    rw [hScard] at hdeg
    refine ⟨-((∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ ℓ
        + Polynomial.C (∑ c ∈ S, c) * f ^ (ℓ - 1) * g), ?_, ?_⟩
    · have hb : ((∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ ℓ
          + Polynomial.C (∑ c ∈ S, c) * f ^ (ℓ - 1) * g).natDegree ≤ k' := by
        refine le_trans hdeg ?_
        omega
      have hb' : (-((∏ c ∈ S, (f - Polynomial.C c * g)) - f ^ ℓ
          + Polynomial.C (∑ c ∈ S, c) * f ^ (ℓ - 1) * g)).natDegree ≤ k' := by
        rw [Polynomial.natDegree_neg]; exact hb
      exact lt_of_le_of_lt
        (Polynomial.degree_le_natDegree.trans (WithBot.coe_le_coe.mpr hb'))
        (WithBot.coe_lt_coe.mpr (Nat.lt_succ_self k'))
    · intro i
      simp only [Polynomial.eval_neg, Polynomial.eval_add, Polynomial.eval_sub,
        Polynomial.eval_mul, Polynomial.eval_pow, Polynomial.eval_C]
      ring
  -- closeness: agreement on the a·ℓ fiber points of S
  have hclose : ∀ S : Finset F, S ⊆ T → S.card = ℓ → ∀ z : F,
      relDist
        (fun i => (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i))
        (fun i => (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)
          - (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i))
        ≤ 1 - (a * ℓ : ℝ) / Fintype.card ι := by
    intro S hST hScard z
    have hfibcard : (Finset.univ.filter (fun i => φ (dom i) ∈ S)).card = a * ℓ := by
      have hinner : ∀ c ∈ S,
          ((Finset.univ.filter (fun i => φ (dom i) ∈ S)).filter
            (fun i => φ (dom i) = c)).card = a := by
        intro c hc
        have heqf : (Finset.univ.filter (fun i => φ (dom i) ∈ S)).filter
            (fun i => φ (dom i) = c) = Finset.univ.filter (fun i => φ (dom i) = c) := by
          ext i
          simp only [Finset.mem_filter, Finset.mem_univ, true_and]
          exact ⟨fun h => h.2, fun h => ⟨h ▸ hc, h⟩⟩
        rw [heqf]
        exact hfiber c (hST hc)
      calc (Finset.univ.filter (fun i => φ (dom i) ∈ S)).card
          = ∑ c ∈ S, ((Finset.univ.filter (fun i => φ (dom i) ∈ S)).filter
              (fun i => φ (dom i) = c)).card :=
            Finset.card_eq_sum_card_fiberwise (fun i hi => by
              simp only [Finset.coe_filter, Set.mem_setOf_eq] at hi
              exact hi.2)
        _ = ∑ _c ∈ S, a := Finset.sum_congr rfl hinner
        _ = S.card * a := by rw [Finset.sum_const, smul_eq_mul]
        _ = a * ℓ := by rw [hScard, Nat.mul_comm]
    have hsubd : Finset.univ.filter (fun i =>
          (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)
          ≠ (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)
            - (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i))
        ⊆ (Finset.univ.filter (fun i => φ (dom i) ∈ S))ᶜ := by
      intro i hi
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi
      simp only [Finset.mem_compl, Finset.mem_filter, Finset.mem_univ, true_and]
      intro hiS
      exact hi (by rw [hvanish S i hiS]; ring)
    have hnum : numDiff
        (fun i => (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i))
        (fun i => (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)
          - (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i))
        ≤ Fintype.card ι - a * ℓ := by
      calc numDiff _ _ ≤ ((Finset.univ.filter (fun i => φ (dom i) ∈ S))ᶜ).card :=
            Finset.card_le_card hsubd
        _ = Fintype.card ι - a * ℓ := by rw [Finset.card_compl, hfibcard]
    rw [relDist, div_le_iff₀ hnR]
    calc (numDiff _ _ : ℝ) ≤ ((Fintype.card ι - a * ℓ : ℕ) : ℝ) := by exact_mod_cast hnum
      _ = (Fintype.card ι : ℝ) - ((a * ℓ : ℕ) : ℝ) := by rw [Nat.cast_sub haℓn]
      _ = (1 - (a * ℓ : ℝ) / Fintype.card ι) * Fintype.card ι := by
          push_cast
          field_simp
  -- injectivity at a fixed slope: locator degrees stay below n
  have hΛdeg : ∀ S₀ : Finset F, S₀.card = ℓ →
      (∏ c ∈ S₀, (f - Polynomial.C c * g)).natDegree < Fintype.card ι := by
    intro S₀ hc
    have hterm : ∀ c ∈ S₀, (f - Polynomial.C c * g).natDegree ≤ a := by
      intro c _
      refine le_trans (Polynomial.natDegree_sub_le _ _) (max_le (le_of_eq hfdeg) ?_)
      refine le_trans Polynomial.natDegree_mul_le ?_
      rw [Polynomial.natDegree_C, hgdeg]
      omega
    calc (∏ c ∈ S₀, (f - Polynomial.C c * g)).natDegree
        ≤ ∑ c ∈ S₀, (f - Polynomial.C c * g).natDegree := Polynomial.natDegree_prod_le _ _
      _ ≤ S₀.card * a := by
          calc ∑ c ∈ S₀, (f - Polynomial.C c * g).natDegree
              ≤ S₀.card • a := Finset.sum_le_card_nsmul _ _ _ hterm
            _ = S₀.card * a := by rw [smul_eq_mul]
      _ = ℓ * a := by rw [hc]
      _ < Fintype.card ι := by
          rw [hn, hNs]
          have h1 : ℓ * a ≤ (s + 2) * a := Nat.mul_le_mul_right a (by omega)
          have h2 : (s + 2) * a = s * a + 2 * a := by ring
          have h3 : a * (s + 3) = s * a + 3 * a := by ring
          omega
  have hinj : ∀ S S' : Finset F, S ⊆ T → S' ⊆ T → S.card = ℓ → S'.card = ℓ →
      (∀ i, (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i)
          = (∏ c ∈ S', (f - Polynomial.C c * g)).eval (dom i)) → S = S' := by
    intro S S' hST hS'T hSc hS'c heq
    have hΛeq := eq_of_eval_eq_of_natDegree_lt dom hdom (hΛdeg S hSc) (hΛdeg S' hS'c) heq
    refine Finset.eq_of_subset_of_card_le ?_ (by omega)
    intro c hcS
    obtain ⟨i₀, -, hi₀⟩ := Finset.mem_image.mp (hST hcS)
    have h0 : (∏ c ∈ S, (f - Polynomial.C c * g)).eval (dom i₀) = 0 :=
      hvanish S i₀ (by rwa [hi₀])
    rw [hΛeq] at h0
    have := hrecover S' i₀ h0
    rwa [hi₀] at this
  -- pigeonhole the C(N, ℓ) slope sets over the ≤ |B| slopes z = −e₁
  set 𝒮 : Finset (Finset F) := T.powersetCard ℓ with h𝒮
  have h𝒮card : 𝒮.card = Nat.choose N ℓ := by
    rw [h𝒮, Finset.card_powersetCard, hTcard]
  have h𝒮ne : 𝒮.Nonempty := by
    rw [h𝒮]
    exact Finset.powersetCard_nonempty.mpr (by rw [hTcard]; omega)
  have hζB : ∀ S₀ ∈ 𝒮, -∑ c ∈ S₀, c ∈ B := by
    intro S₀ hS₀
    have hS₀T : S₀ ⊆ T := (Finset.mem_powersetCard.mp hS₀).1
    refine B.neg_mem (B.toSubring.sum_mem fun c hc => ?_)
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp (hS₀T hc)
    exact hφB i
  obtain ⟨z₀, hz₀img, hmax⟩ := Finset.exists_max_image
    (𝒮.image (fun S => -∑ c ∈ S, c))
    (fun z => (𝒮.filter (fun S => -∑ c ∈ S, c = z)).card) (h𝒮ne.image _)
  have hz₀B : z₀ ∈ B := by
    obtain ⟨S₀, hS₀, rfl⟩ := Finset.mem_image.mp hz₀img
    exact hζB S₀ hS₀
  set fib : Finset (Finset F) := 𝒮.filter (fun S => -∑ c ∈ S, c = z₀) with hfibdef
  refine ⟨z₀, hz₀B, fib.card, ?_, ?_⟩
  · -- the count: C(N, ℓ) ≤ |B| · fib.card, hence C(N, ℓ)/|B| ≤ fib.card
    have hcount : Nat.choose N ℓ ≤ Fintype.card B * fib.card := by
      have h1 : 𝒮.card = ∑ z ∈ 𝒮.image (fun S => -∑ c ∈ S, c),
          (𝒮.filter (fun S => -∑ c ∈ S, c = z)).card :=
        Finset.card_eq_sum_card_image _ _
      have h2 : ∑ z ∈ 𝒮.image (fun S => -∑ c ∈ S, c),
          (𝒮.filter (fun S => -∑ c ∈ S, c = z)).card
          ≤ (𝒮.image (fun S => -∑ c ∈ S, c)).card * fib.card := by
        calc ∑ z ∈ 𝒮.image (fun S => -∑ c ∈ S, c),
            (𝒮.filter (fun S => -∑ c ∈ S, c = z)).card
            ≤ (𝒮.image (fun S => -∑ c ∈ S, c)).card • fib.card :=
              Finset.sum_le_card_nsmul _ _ _ hmax
          _ = (𝒮.image (fun S => -∑ c ∈ S, c)).card * fib.card := by rw [smul_eq_mul]
      have h3 : (𝒮.image (fun S => -∑ c ∈ S, c)).card ≤ Fintype.card B := by
        have hsubB : 𝒮.image (fun S => -∑ c ∈ S, c)
            ⊆ Finset.univ.image (fun b : B => (b : F)) := by
          intro z hz
          obtain ⟨S₀, hS₀, rfl⟩ := Finset.mem_image.mp hz
          exact Finset.mem_image.mpr
            ⟨⟨-∑ c ∈ S₀, c, hζB S₀ hS₀⟩, Finset.mem_univ _, rfl⟩
        calc (𝒮.image (fun S => -∑ c ∈ S, c)).card
            ≤ (Finset.univ.image (fun b : B => (b : F))).card :=
              Finset.card_le_card hsubB
          _ = Fintype.card B := by
              rw [Finset.card_image_of_injective _ Subtype.val_injective,
                Finset.card_univ]
      calc Nat.choose N ℓ = 𝒮.card := h𝒮card.symm
        _ ≤ (𝒮.image (fun S => -∑ c ∈ S, c)).card * fib.card := h1 ▸ h2
        _ ≤ Fintype.card B * fib.card := Nat.mul_le_mul_right _ h3
    have hBpos : 0 < Fintype.card B := Fintype.card_pos_iff.mpr ⟨⟨0, B.zero_mem⟩⟩
    have hBposR : (0 : ℝ) < Fintype.card B := by exact_mod_cast hBpos
    rw [div_le_iff₀ hBposR]
    calc (Nat.choose N ℓ : ℝ) ≤ ((Fintype.card B * fib.card : ℕ) : ℝ) := by
          exact_mod_cast hcount
      _ = (fib.card : ℝ) * (Fintype.card B : ℝ) := by push_cast; ring
  · -- the list: enumerate the fixed-slope fiber
    have hfibmem : ∀ S₀ : Finset F, S₀ ∈ fib →
        S₀ ⊆ T ∧ S₀.card = ℓ ∧ -∑ c ∈ S₀, c = z₀ := by
      intro S₀ hS₀
      rw [hfibdef, Finset.mem_filter, h𝒮] at hS₀
      obtain ⟨hS₀𝒮, hS₀z⟩ := hS₀
      obtain ⟨hS₀T, hS₀c⟩ := Finset.mem_powersetCard.mp hS₀𝒮
      exact ⟨hS₀T, hS₀c, hS₀z⟩
    refine ⟨fun j => (fun i =>
        (f.eval (dom i)) ^ ℓ + z₀ * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)
        - (∏ c ∈ ((fib.equivFin.symm j : Finset F)), (f - Polynomial.C c * g)).eval
            (dom i)), ?_, ?_, ?_⟩
    · intro j
      obtain ⟨hST, hScard, hSz⟩ := hfibmem _ (fib.equivFin.symm j).2
      rw [← hSz]
      exact hkey _ hScard
    · intro j j' hjj'
      obtain ⟨hST, hScard, hSz⟩ := hfibmem _ (fib.equivFin.symm j).2
      obtain ⟨hS'T, hS'card, hS'z⟩ := hfibmem _ (fib.equivFin.symm j').2
      have heq : ∀ i,
          (∏ c ∈ ((fib.equivFin.symm j : Finset F)), (f - Polynomial.C c * g)).eval (dom i)
          = (∏ c ∈ ((fib.equivFin.symm j' : Finset F)), (f - Polynomial.C c * g)).eval
              (dom i) := by
        intro i
        have hpt := congrFun hjj' i
        dsimp only at hpt
        exact sub_right_inj.mp hpt
      have hSS : (fib.equivFin.symm j : Finset F) = (fib.equivFin.symm j' : Finset F) :=
        hinj _ _ hST hS'T hScard hS'card heq
      exact fib.equivFin.symm.injective (Subtype.ext hSS)
    · intro j
      obtain ⟨hST, hScard, hSz⟩ := hfibmem _ (fib.equivFin.symm j).2
      exact hclose _ hST hScard z₀

/-- **`cor:ecfft-onestep` — every ECFFT row has an unsafe first staircase step.**

For an ECFFT domain that is `(ψ, 2)`-smooth over `B` (degree type `(2, 1)`), with
`C = RS[F, D, k]`, `2 ∣ k`, `ρ = k/n ∈ [1/16, 1/2]`, `n < q < 2^256`, `n ≥ 2^12`, and
`ℓ = (k+2)/2 ≤ N − 1`, the field-size count `C(n/2, (k+2)/2) ≥ |B|·(q/k + 1)` holds,
and consequently the correlated-agreement error exceeds the threshold at the first
staircase step: `ε_ca(C, 1 − ρ − 2/n) > (1/2k)(1 − n/q)`.

**Update (constructive discharge, 2026-07-19; statement byte-identical):** proved.
As in the audited skeleton, the binomial count (a *conclusion* of the paper's
envelope argument, tex `:4866`/`:4878`–`:4882`) is carried as the hypothesis `hyp`;
the envelope entropy bound itself (`ρ ∈ [1/16, 1/2]`, `n ≥ 2^12`, `q < 2^256` ⇒
`C(n/2, (k+2)/2) ≥ |B|(q/k+1)`) remains unformalized, and the `ε_mca` band,
list-challenge, and odd-`k` clauses of tex `:4872`–`:4874` are likewise not stated
here (deviation flags 2–3 of the discharge audit note).  Route (tex `:4877`–
`:4883`): `prop_rational_floor` at `(a, e) = (2, 1)`, `ℓ = (k+2)/2`, `k' = 2ℓ − 2 =
k` gives a `C^+ = RS[F, D, k+1]` list of size `L ≥ C(N, ℓ)/|B| ≥ q/k + 1 >
(q − n)/k` at deep agreement `A = 2ℓ = k + 2`; the proved bridge
`cor_quotient_remainder_trigger` (Theorem A at `η = 1/2` + `ecaFloor_trigger`)
converts it into the printed `ε_ca` bound at `δ = 1 − ρ − 2/n`, exactly as
`cor_first_grid_cap_one` bridged the `c = 1` first-grid list at `A = k + 1`. -/
theorem cor_ecfft_onestep (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {N k ℓ : ℕ}
    (hfB : ∀ n, f.coeff n ∈ B) (hgB : ∀ n, g.coeff n ∈ B)
    (hfdeg : f.natDegree = 2) (hgdeg : g.natDegree = 1)
    (h2N : 2 * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g 2)
    (hk : 0 < k) (hkeven : Even k) (hℓ : ℓ = (k + 2) / 2) (hℓN : ℓ ≤ N - 1)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose (Fintype.card ι / 2) ((k + 2) / 2) : ℝ)) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < ecaErr (RSpoly dom k)
          (1 - (k : ℝ) / Fintype.card ι - 2 / Fintype.card ι)
          (1 - (k : ℝ) / Fintype.card ι - 2 / Fintype.card ι) := by
  classical
  -- numerology: k even and positive gives 2ℓ = k + 2, ℓ ≥ 2, N ≥ 3
  obtain ⟨m, hme⟩ := hkeven
  have hℓ2 : 2 * ℓ = k + 2 := by omega
  have hℓlo : 2 ≤ ℓ := by omega
  have hN3 : 3 ≤ N := by omega
  have hn0 : 0 < Fintype.card ι := by omega
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hkR : (0 : ℝ) < k := by exact_mod_cast hk
  -- instantiate the rational floor at (a, e) = (2, 1), where k' = 2ℓ − 2 = k
  have hk' : k = 2 * ℓ - 2 * (2 - 1) := by omega
  obtain ⟨z, hzB, L, hLbound, hlist⟩ :=
    prop_rational_floor dom hdom B hdomB f g hfB hgB (by omega : 1 < 2)
      hfdeg hgdeg h2N hsmooth hℓlo hℓN hk'
  -- align the binomial in `hyp` with the floor produced: n/2 = N, (k+2)/2 = ℓ
  have hNdiv : Fintype.card ι / 2 = N := by omega
  have hℓdiv : (k + 2) / 2 = ℓ := by omega
  rw [hNdiv, hℓdiv] at hyp
  -- the trigger: L ≥ q/k + 1 > (q − n)/k
  have hBpos : 0 < Fintype.card B := Fintype.card_pos_iff.mpr ⟨⟨0, B.zero_mem⟩⟩
  have hBposR : (0 : ℝ) < Fintype.card B := by exact_mod_cast hBpos
  have hL1 : (Fintype.card F : ℝ) / k + 1 ≤ L := by
    have h1 : (Fintype.card F : ℝ) / k + 1
        ≤ (Nat.choose N ℓ : ℝ) / (Fintype.card B : ℝ) := by
      rw [le_div_iff₀ hBposR]
      calc ((Fintype.card F : ℝ) / k + 1) * Fintype.card B
          = (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1) := by ring
        _ ≤ (Nat.choose N ℓ : ℝ) := hyp
    exact h1.trans hLbound
  have htrig : ((Fintype.card F : ℝ) - Fintype.card ι) / k < L := by
    have h2 : 0 < (Fintype.card ι : ℝ) / k := div_pos hnR hkR
    have h3 : ((Fintype.card F : ℝ) - Fintype.card ι) / k
        = (Fintype.card F : ℝ) / k - (Fintype.card ι : ℝ) / k := by rw [sub_div]
    linarith
  -- the bridge, at deep agreement A = 2ℓ = k + 2
  have hAlo : k < 2 * ℓ := by omega
  have hAn : 2 * ℓ ≤ Fintype.card ι := by omega
  have hlist' : HasList (RSpoly dom (k + 1))
      (1 - ((2 * ℓ : ℕ) : ℝ) / Fintype.card ι)
      (fun i => (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i))
      L := by
    have hcast : ((2 * ℓ : ℕ) : ℝ) = (2 * ℓ : ℝ) := by push_cast; ring
    rw [hcast]
    exact hlist
  have hδlo : 1 - ((2 * ℓ : ℕ) : ℝ) / Fintype.card ι
      ≤ 1 - (k : ℝ) / Fintype.card ι - 2 / Fintype.card ι := by
    have hcast2 : ((2 * ℓ : ℕ) : ℝ) = (k : ℝ) + 2 := by
      rw [hℓ2]; push_cast; ring
    rw [hcast2, add_div, sub_sub]
  have hδhi : 1 - (k : ℝ) / Fintype.card ι - 2 / Fintype.card ι
      < 1 - (k : ℝ) / Fintype.card ι := by
    have : 0 < 2 / (Fintype.card ι : ℝ) := by positivity
    linarith
  exact cor_quotient_remainder_trigger dom hdom hk hAlo hAn hq _ hlist' htrig _ hδlo hδhi

/-- **`prop:graded-rational-floor` — graded prefix floors on rational scales**
(tex `:5209`–`:5222`; statement-repaired and **proved**).

At every admissible scale, the graded prefix construction (heaviest-prefix locator
combined with the rational fiber map) produces a received word whose list at the
corresponding deep radius `1 − A/n` (paper: `A = am ≥ K > k`) has size at least the
graded prefix count `H`, giving a lower bound `ε_ca(C, δ) ≥ 𝓔_{q,k}(H)` across the
deep band `δ ∈ [1 − A/n, 1 − k/n)`.  Stated abstractly via `HasList` and the
deep-list floor `ecaFloor`, exactly as the skeleton chose to; the list input is the
content of the paper's pigeonhole (the `U_z` construction), which is *not* re-proved
here.

Statement repair (this packet; falsity class, machine-checked negation
`prop_graded_rational_floor_false`): the previous skeleton's only constraint on the
radius was `hδ : 1 − k/n ≤ 1` — vacuously true — while `hlist` was taken at the
*conclusion* radius `δ` itself; at `δ = 1` every pair is `intClose`, so `ecaErr = 0`
while `ecaFloor > 0`.  The paper's floor holds on the deep band below the list
agreement (`prop:graded-rational-floor` conclusion at radius `1 − am/n`, assembled
into bands by `lem:mca-monotone`); the defect was a formalization omission of the
deep-band constraint, not a paper defect.  Repaired by anchoring the list at a deep
agreement `A > k` and bounding `δ` inside `[1 − A/n, 1 − k/n)`; the repaired
statement is a direct wrapper over the proved `thm_quotient_remainder_deep_floor`.
The rational-smoothness binders are retained for paper-setting faithfulness
(the paper's instance produces `hlist` from them) although the wrapper consumes only
the list; the unused-variable warnings are deliberate. -/
theorem prop_graded_rational_floor
    (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {a e N k A : ℕ}
    (hae : e < a) (hfdeg : f.natDegree = a) (hgdeg : g.natDegree = e)
    (haN : a * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g a)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F) (hk : 0 < k)
    (H : ℕ) (hH : 1 ≤ H) (hAlo : k < A) (hAn : A ≤ Fintype.card ι)
    (hlist : ∃ U : ι → F, HasList (RSpoly dom (k + 1)) (1 - (A : ℝ) / Fintype.card ι) U H)
    (δ : ℝ) (hδlo : 1 - (A : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    ecaFloor (Fintype.card F) (Fintype.card ι) k H ≤ ecaErr (RSpoly dom k) δ δ := by
  obtain ⟨U, hU⟩ := hlist
  exact thm_quotient_remainder_deep_floor dom hdom hk hH hAlo hAn hq U hU δ hδlo hδhi

/-- **The previous `prop_graded_rational_floor` skeleton statement was false.**
Its radius hypothesis was `hδ : 1 − k/n ≤ 1` — always true — and `hlist` was taken
at the conclusion radius `δ` itself, so nothing prevented `δ = 1`.  Counterexample:
`F = ZMod 2`, `ι = Fin 1`, `dom ≡ 0`, `B = ⊤`, `f = X`, `g = 1`, `(a, e) = (1, 0)`,
`N = k = 1`, `H = 1`, `δ = 1`: the zero word carries the trivial one-element list at
radius `1`, and all hypotheses hold; but at `δ = 1` every pair `(f₁, f₂)` is
`intClose` (the interleaved distance never exceeds `1`), so no slope is CA-bad and
`ε_ca(C, 1, 1) = 0`, while `𝓔_{2,1}(1) = 1·(2−1)/(2·(2−1+1·1)) = 1/4 > 0`.  The
paper is not affected: `prop:graded-rational-floor` (tex `:5209`) states the floor
at the deep radius `1 − am/n` with `am ≥ K`, and the band assembly uses
`lem:mca-monotone` strictly below capacity; the missing deep-band constraint was a
formalization omission.  Stated over `Type` (universe 0), which suffices to refute
the universe-polymorphic skeleton. -/
theorem prop_graded_rational_floor_false :
    ¬ ∀ (ι F : Type) [Fintype ι] [Field F] [Fintype F]
        (dom : ι → F), Function.Injective dom →
        ∀ (B : Subfield F) [Fintype B], (∀ i, dom i ∈ B) →
        ∀ (f g : Polynomial F) (a e N k : ℕ),
          e < a → f.natDegree = a → g.natDegree = e →
          a * N = Fintype.card ι → RationalSmooth dom f g a →
          (Fintype.card ι : ℝ) < Fintype.card F → 0 < k →
          ∀ (δ : ℝ) (H : ℕ), 1 ≤ H →
            (∃ U : ι → F, HasList (RSpoly dom (k + 1)) δ U H) →
            1 - (k : ℝ) / Fintype.card ι ≤ 1 →
            ecaFloor (Fintype.card F) (Fintype.card ι) k H ≤ ecaErr (RSpoly dom k) δ δ := by
  intro h
  have hsmooth : RationalSmooth (fun _ : Fin 1 => (0 : ZMod 2)) Polynomial.X 1 1 := by
    refine ⟨fun i => by simp, ?_⟩
    intro i
    refine le_antisymm ?_ ?_
    · exact le_trans (Finset.card_le_univ _) (by simp)
    · exact Finset.card_pos.mpr ⟨0, by simp⟩
  have hlist : ∃ U : Fin 1 → ZMod 2,
      HasList (RSpoly (fun _ : Fin 1 => (0 : ZMod 2)) (1 + 1)) 1 U 1 := by
    refine ⟨fun _ => 0, fun _ _ => 0, fun _ => ⟨0, ?_, fun i => by simp⟩,
      fun a b _ => Subsingleton.elim a b, fun i => ?_⟩
    · rw [Polynomial.degree_zero]
      exact WithBot.bot_lt_coe _
    · have h0 : relDist (fun _ : Fin 1 => (0 : ZMod 2)) (fun _ => 0) = 0 := by
        simp [relDist, numDiff]
      rw [h0]
      norm_num
  have key := h (Fin 1) (ZMod 2) (fun _ => 0) (fun a b _ => Subsingleton.elim a b)
    ⊤ (fun _ => Subfield.mem_top _) Polynomial.X 1 1 0 1 1
    (by norm_num) Polynomial.natDegree_X Polynomial.natDegree_one
    (by simp) hsmooth (by simp [ZMod.card]) (by norm_num)
    1 1 le_rfl hlist (by norm_num [Fintype.card_fin])
  have herr : ecaErr (RSpoly (fun _ : Fin 1 => (0 : ZMod 2)) 1) 1 1 ≤ 0 := by
    refine Finset.sup'_le _ _ fun p _ => ?_
    have hnone : ∀ γ : ZMod 2,
        ¬ caBad (RSpoly (fun _ : Fin 1 => (0 : ZMod 2)) 1) 1 1 p.1 p.2 γ := by
      rintro γ ⟨-, hnc⟩
      refine hnc ⟨fun _ => p.1 0,
        ⟨Polynomial.C (p.1 0), lt_of_le_of_lt Polynomial.degree_C_le (by decide),
          fun i => (Polynomial.eval_C).symm⟩,
        fun _ => p.2 0,
        ⟨Polynomial.C (p.2 0), lt_of_le_of_lt Polynomial.degree_C_le (by decide),
          fun i => (Polynomial.eval_C).symm⟩, ?_⟩
      unfold relDist2
      rw [div_le_one (by simp : (0 : ℝ) < (Fintype.card (Fin 1) : ℝ))]
      exact_mod_cast Finset.card_le_univ _
    unfold prob
    rw [Finset.filter_eq_empty_iff.mpr fun γ _ => hnone γ]
    simp
  have hfloor : ecaFloor (Fintype.card (ZMod 2)) (Fintype.card (Fin 1))
      ((1 : ℕ) : ℝ) ((1 : ℕ) : ℝ) = 1 / 4 := by
    norm_num [ecaFloor, ZMod.card, Fintype.card_fin]
  rw [hfloor] at key
  linarith

/-- **`cor:ecfft-macroscopic` — macroscopic universal cap for genus-one rows**
(tex `:5241`–`:5262`; statement-repaired, PLAUSIBLE grade, still sorried).

Assembling `prop_graded_rational_floor` over the graded band gives that the
correlated-agreement error of a genus-one (ECFFT) row exceeds the half-inverse
dimension threshold not just at one step but throughout a macroscopic sub-capacity
band `δ ∈ [1 − ρ − Δ, 1 − ρ)` of width `Δ` bounded by the paper's certified gap.

Statement-hygiene repairs (this packet; untied-binder defect class, graded
**PLAUSIBLE** — no counterexample constructed, so no falsity claim):

1. **`Δ` was unbounded** (`hΔ : 0 < Δ` only), so the band `[1 − ρ − Δ, 1 − ρ)`
   admitted radii `δ < 0`, where no support of size `≥ (1−δ)n` exists, `mcaBad`
   never holds, and `emcaErr = 0` — below the threshold whenever `q > n`, `k ≥ 1`.
   A machine-checked negation would additionally need a satisfiable ECFFT-shaped
   instance of `hyp` (a genuine `(2,1)`-smooth domain with a large binomial), which
   is constructible but disproportionate for this packet — hence PLAUSIBLE, not a
   falsity claim.  Repaired with `hΔhi : Δ ≤ 1/512`, the paper's certified band
   width `2⁻⁹` (`cor:ecfft-macroscopic`(i), tex `:5247`: the `ε_mca` clause holds on
   `[1 − ρ − 2⁻⁹, 1 − ρ)`).
2. **`hfB`/`hgB` missing**: `prop_rational_floor` and `cor_ecfft_onestep` carry the
   subfield ties `f, g ∈ B[X]` (paper `def:rational-smooth`: `ψ = f/g` with
   `f, g ∈ B[X]`), which are what make the prefix pigeonhole run over `|B|`; this
   corollary omitted them — the same untied-binder class as the repaired
   `lem_phi_fiber_ii` (`hQB`, Fiber.lean).  Restored.

Residual (documented, not repaired): `hyp` here is the *one-step* binomial count of
`cor_ecfft_onestep`, while the paper's macroscopic corollary derives the graded count
`C(N, m) > |B|^{2m−k−1}(q/k+1)` at `m = ⌈(k+1+2⁻⁹n)/2⌉` from envelope hypotheses
(`ρ ∈ [1/16, 1/2]`, `n ≥ 2^14`, `q < 2^256`, `log₂|B| ≤ 64`, tex `:5241`–`:5245`)
that the skeleton never carried.  A discharge will likely need to swap `hyp` for the
graded form or add the envelope; this is flagged in the correspondence note and left
to the dischargeer. -/
theorem cor_ecfft_macroscopic (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {N k : ℕ}
    (hfB : ∀ n, f.coeff n ∈ B) (hgB : ∀ n, g.coeff n ∈ B)
    (hfdeg : f.natDegree = 2) (hgdeg : g.natDegree = 1)
    (h2N : 2 * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g 2)
    (hk : 0 < k) (hkeven : Even k)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose (Fintype.card ι / 2) ((k + 2) / 2) : ℝ))
    (Δ : ℝ) (hΔ : 0 < Δ) (hΔhi : Δ ≤ 1 / 512)
    (δ : ℝ) (hδlo : 1 - (k : ℝ) / Fintype.card ι - Δ ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < emcaErr (RSpoly dom k) δ := by
  sorry

end RSCap
