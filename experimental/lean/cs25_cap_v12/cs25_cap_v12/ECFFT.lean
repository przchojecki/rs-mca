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

/-- **`prop:rational-floor` — rational-map fiber floor, unified `(a, e)` form.**

Let `dom` be `(ψ, a)`-smooth over `B` with `ψ = f/g` of degree type `(a, e)`,
`a > e ≥ 0`, `N = n/a`, and `2 ≤ ℓ ≤ N − 1`.  With `k' = aℓ − 2(a − e)`, some slope
`z ∈ B` makes the word `u_z(x) = f(x)^ℓ + z·f(x)^{ℓ−1}·g(x)` carry a list of at least
`C(N, ℓ)/|B|` distinct codewords of `RS[F, D, k'+1]` at radius `1 − aℓ/n` (i.e. at
agreement `aℓ = k' + 2(a − e)`). -/
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
  sorry

/-- **`cor:ecfft-onestep` — every ECFFT row has an unsafe first staircase step.**

For an ECFFT domain that is `(ψ, 2)`-smooth over `B` (degree type `(2, 1)`), with
`C = RS[F, D, k]`, `2 ∣ k`, `ρ = k/n ∈ [1/16, 1/2]`, `n < q < 2^256`, `n ≥ 2^12`, and
`ℓ = (k+2)/2 ≤ N − 1`, the field-size count `C(n/2, (k+2)/2) ≥ |B|·(q/k + 1)` holds,
and consequently the correlated-agreement error exceeds the threshold at the first
staircase step: `ε_ca(C, 1 − ρ − 2/n) > (1/2k)(1 − n/q)`. -/
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
  sorry

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
