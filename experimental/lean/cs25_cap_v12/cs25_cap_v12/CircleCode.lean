import cs25_cap_v12.BlueprintCommon
import cs25_cap_v12.Fiber

/-!
# Blueprint: circle codes, Chebyshev fibers, and torus uniformization (`sec:circle-geometry`, `sec:answers-stereo`)

Circle-code section of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

Throughout, `F ⊇ F_{p²}` is a finite field containing an element `i` with `i² = −1`.
The `x`-coordinate map on the norm-one torus is `χ(u) = (u + u⁻¹)/2`, and the
Chebyshev polynomials `T_a` (Mathlib's `Polynomial.Chebyshev.T`) satisfy the
semiconjugacy `T_a(χ(u)) = χ(uᵃ)`.  Twin cosets `𝒟 = gH ∪ g⁻¹H` give `x`-coordinate
domains `D = χ(𝒟)` on which `T_a` is `(T_a, a)`-smooth.

Proved here (no `sorry`):

* `chebyshev_semiconjugacy` — the Chebyshev semiconjugacy `T_a(χ(u)) = χ(uᵃ)`,
  under the explicit odd-characteristic hypothesis `(2 : F) ≠ 0` (the paper has
  `p` odd throughout; over characteristic two the identity is false, e.g. at `a = 0`).
* `twinCoset` and its structure lemmas — `lem:torus-fibers` (cyclic core):
  `card_pow_eq_one_of_dvd_card` (the `a`-power kernel has exactly `a` elements),
  `coset_pow_fiber_card` (the `a`-power map is exactly `a`-to-one on each coset),
  `coset_pow_fiber_cross_empty` / `twin_coset_image_coincident` (the
  disjoint/coincident image dichotomy governed by `g^{2a} ∉/∈ H^{(a)}`),
  `twin_coset_all_scales_iff` (the all-scales criterion
  `(∀ a ∣ M, g^{2a} ∉ H^{(a)}) ↔ ord(g) ∤ 2M`), and
  `lem_torus_fibers` (a twin-coset enumeration is `(Xᵃ, a)`-smooth, phrased with
  `DomSmooth` — exactly the `hsmooth` input of `cor_circle_grand`).
* `twinCoset_no_self_inverse`, `chi_eq_chi_iff`, `chi_pair_image_card`,
  `twin_coset_chi_card` — a twin coset has no self-inverse element, `χ` identifies
  exactly inverse pairs, and `|χ(𝒟)| = |H|` (this also discharges the cardinality
  claim baked into `def:circle-twin-domain` of the thresholds draft).
* `htwin_of_twin_coset` — the exact `2a`-point fiber-pair count `|E_w| = 2a` on an
  enumerated twin coset (the counting formerly *assumed* by this file's
  `lem_cheb_fibers` skeleton as `htwin`).
* `lem_cheb_fibers` — `lem:cheb-fibers`: an `x`-coordinate twin-coset domain is
  `(T_a, a)`-smooth (`DomSmooth`), now *proved* from explicit twin-coset hypotheses.
* `chebyshev_antisymm` — the antisymmetric companion
  `u^a − u^{−a} = (u − u⁻¹)·U_{a−1}(χ(u))` of the semiconjugacy.
* `lem_circle_rs` — `lem:circle-rs`, **statement repaired and proved**: the previous
  skeleton omitted `(2 : F) ≠ 0` and was false as stated (`lem_circle_rs_false`,
  `ZMod 2` counterexample); with the hypothesis restored, the torus uniformization
  `𝒞_w = t ∘ RS[F, E', 2w+1]` is proved in both directions.
* `lem_stereographic` — `lem:stereographic`, **statement repaired and proved**: the
  previous skeleton left `sdom`/`twist` untied to `pt` and was false as stated
  (`lem_stereographic_false`, `ZMod 5` counterexample); the repaired statement ties
  `sdom` to the stereographic coordinate with pole exclusion and fixes the twist to
  `(1 + s²)^{−w}`, and is proved in both directions.
* `lem_circle_rs_false`, `lem_stereographic_false` — machine-checked negations of
  the two pre-repair skeleton statements (formalization omissions, not paper
  defects: both papers carry `p ≡ 3 (mod 4)` / the stereographic parametrization).

  NOTE (statement repair): the previous skeleton took an index-level hypothesis
  `htwin` asserting the `2a`-count on the *same* index type that `hdom` forces to
  enumerate the `x`-domain injectively.  Those hypotheses are jointly
  unsatisfiable on a nonempty index type (a χ-section meets each inversion pair
  of the solution set at most once, capping the index-level count at
  `a + 1 < 2a` for `a ≥ 2` and at `1 < 2` for `a = 1`), so the skeleton
  statement was vacuous.  The statement below replaces `htwin` by the paper's actual
  hypotheses (`𝒟 = gH ∪ g⁻¹H` a twin coset, `a ∣ |H|`, `g^{2a} ∉ H^{(a)}`, and the
  domain enumerates `χ(𝒟)`), with the `2a`-count `E_w` proved in
  `htwin_of_twin_coset` and consumed on the torus side, per the printed proof of
  `lem:cheb-fibers` (tex/cs25_cap_v12.tex, `lem:torus-fibers`/`lem:cheb-fibers`).

Also proved (Fiber.lean discharge packet — this file now has **zero `sorry`**):

* `cor_circle_grand` — `cor:circle-grand`: the universal cap for circle-FRI
  line-round rows, **statement-repaired and proved**.  Two statement repairs: the
  lane-17 `htorusB` tie (untied `B`, graded PLAUSIBLE), and a `hδlo` cast repair
  (the previous skeleton's `(a * (k / a + 2) : ℝ)` elaborated `k / a` as *real*
  division while `hyp` uses the *floor* `ℓ₂ = ⌊k/a⌋ + 2`, silently widening the
  claimed band below the paper's certified endpoint `1 − A₂/n`; graded PLAUSIBLE
  claim-widening, no falsity claim — see the docstring).  The proof consumes the
  repaired-and-proved `lem_phi_fiber_ii` (Fiber.lean) at `φ = Xᵃ` — the
  divisibility-free route is forced since `k = 2w+1` is odd while every deployed
  folding scale is even (tex `:4010`) — plus `hasList_fiber_input` and the proved
  `universal_cap_emca_of_fiber_list` (MainCap.lean).
-/

namespace RSCap

open Classical Polynomial Pointwise

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- The `x`-coordinate (Chebyshev/torus projection) map `χ(u) = (u + u⁻¹)/2`. -/
noncomputable def chi (u : F) : F := (u + u⁻¹) / 2

/-- `χ` is inversion-invariant: `χ(u⁻¹) = χ(u)`. -/
theorem chi_inv (u : F) : chi u⁻¹ = chi u := by
  simp [chi, add_comm]

/-- **Chebyshev semiconjugacy** `T_a(χ(u)) = χ(uᵃ)` for `u ≠ 0`, in odd
characteristic (`(2 : F) ≠ 0`; the paper has `p` odd throughout).  This is the
identity underlying the tower structure of circle-FRI line rounds. -/
theorem chebyshev_semiconjugacy (h2 : (2 : F) ≠ 0) (u : F) (hu : u ≠ 0) (a : ℕ) :
    (Polynomial.Chebyshev.T F (a : ℤ)).eval (chi u) = chi (u ^ a) := by
  induction a using Nat.twoStepInduction with
  | zero =>
    simp only [Nat.cast_zero, Polynomial.Chebyshev.T_zero, Polynomial.eval_one, pow_zero, chi,
      inv_one]
    rw [eq_div_iff h2]
    ring
  | one =>
    simp [Polynomial.Chebyshev.T_one, chi]
  | more n ih1 ih2 =>
    have hcast : ((n + 2 : ℕ) : ℤ) = (n : ℤ) + 2 := by push_cast; ring
    have hcast1 : ((n + 1 : ℕ) : ℤ) = (n : ℤ) + 1 := by push_cast; ring
    rw [hcast, Polynomial.Chebyshev.T_add_two]
    simp only [Polynomial.eval_sub, Polynomial.eval_mul, Polynomial.eval_ofNat,
      Polynomial.eval_X]
    rw [← hcast1, ih2, ih1]
    have hun : u ^ n ≠ 0 := pow_ne_zero _ hu
    have hun1 : u ^ (n + 1) ≠ 0 := pow_ne_zero _ hu
    have hun2 : u ^ (n + 2) ≠ 0 := pow_ne_zero _ hu
    simp only [chi]
    field_simp
    ring

/-- **Antisymmetric Chebyshev semiconjugacy** `u^a − u^{−a} = (u − u⁻¹)·U_{a−1}(χ(u))`
for `u ≠ 0`, in odd characteristic — the antisymmetric companion of
`chebyshev_semiconjugacy`, proved by the same `Nat.twoStepInduction` pattern.
Mathlib's `Polynomial.Chebyshev.U` is `ℤ`-indexed, so at `a = 0` the right side is
`(u − u⁻¹)·U_{−1}(χ(u)) = 0`, matching the vanishing left side.  This is the one
new helper needed for the reverse (Laurent-symmetrization) direction of
`lem_circle_rs`: the symmetric part of `u^{−w}Q(u)` lands on
`chebyshev_semiconjugacy`, the antisymmetric part on this lemma. -/
theorem chebyshev_antisymm (h2 : (2 : F) ≠ 0) (u : F) (hu : u ≠ 0) (a : ℕ) :
    u ^ a - u⁻¹ ^ a = (u - u⁻¹) * (Polynomial.Chebyshev.U F ((a : ℤ) - 1)).eval (chi u) := by
  induction a using Nat.twoStepInduction with
  | zero =>
    simp [Polynomial.Chebyshev.U_neg_one]
  | one =>
    simp [Polynomial.Chebyshev.U_zero]
  | more n ih1 ih2 =>
    have hcast : ((n + 2 : ℕ) : ℤ) - 1 = ((n : ℤ) - 1) + 2 := by push_cast; ring
    have hcast1 : ((n + 1 : ℕ) : ℤ) - 1 = (n : ℤ) - 1 + 1 := by push_cast; ring
    rw [hcast, Polynomial.Chebyshev.U_add_two]
    simp only [Polynomial.eval_sub, Polynomial.eval_mul, Polynomial.eval_ofNat,
      Polynomial.eval_X]
    rw [show (n : ℤ) - 1 + 1 = ((n + 1 : ℕ) : ℤ) - 1 from hcast1.symm]
    have hun : u ^ n ≠ 0 := pow_ne_zero _ hu
    have hun1 : u ^ (n + 1) ≠ 0 := pow_ne_zero _ hu
    have hun2 : u ^ (n + 2) ≠ 0 := pow_ne_zero _ hu
    calc u ^ (n + 2) - u⁻¹ ^ (n + 2)
        = 2 * chi u * (u ^ (n + 1) - u⁻¹ ^ (n + 1)) - (u ^ n - u⁻¹ ^ n) := by
          simp only [chi, inv_pow]
          field_simp
          ring
      _ = 2 * chi u * ((u - u⁻¹) *
              (Polynomial.Chebyshev.U F (((n + 1 : ℕ) : ℤ) - 1)).eval (chi u))
            - ((u - u⁻¹) * (Polynomial.Chebyshev.U F (((n : ℕ) : ℤ) - 1)).eval (chi u)) := by
          rw [ih1, ih2]
      _ = (u - u⁻¹) * (2 * chi u *
              (Polynomial.Chebyshev.U F (((n + 1 : ℕ) : ℤ) - 1)).eval (chi u)
            - (Polynomial.Chebyshev.U F (((n : ℕ) : ℤ) - 1)).eval (chi u)) := by
          ring

/-- **`χ` identifies exactly inverse pairs**: for nonzero `u, v` in odd
characteristic, `χ(u) = χ(v)` iff `v ∈ {u, u⁻¹}`.  This is the two-to-one
statement of the twin-coset preamble (tex/cs25_cap_v12.tex) and of
`def:circle-twin-domain` in the thresholds draft. -/
theorem chi_eq_chi_iff (h2 : (2 : F) ≠ 0) {u v : F} (hu : u ≠ 0) (hv : v ≠ 0) :
    chi u = chi v ↔ v = u ∨ v = u⁻¹ := by
  constructor
  · intro h
    have h' : u + u⁻¹ = v + v⁻¹ := by
      have hmul := congrArg (· * 2) h
      simpa [chi, div_mul_cancel₀, h2] using hmul
    have e1 : u * u⁻¹ = 1 := mul_inv_cancel₀ hu
    have e2 : v * v⁻¹ = 1 := mul_inv_cancel₀ hv
    have key : (u - v) * (u * v - 1) = 0 := by
      linear_combination (u * v) * h' - v * e1 + u * e2
    rcases mul_eq_zero.mp key with h0 | h0
    · exact Or.inl (sub_eq_zero.mp h0).symm
    · exact Or.inr (eq_inv_of_mul_eq_one_right (sub_eq_zero.mp h0))
  · rintro (rfl | rfl)
    · rfl
    · exact (chi_inv u).symm

/-- Units version of `chi_eq_chi_iff`. -/
theorem chi_val_eq_chi_val_iff (h2 : (2 : F) ≠ 0) {u v : Fˣ} :
    chi (u : F) = chi (v : F) ↔ v = u ∨ v = u⁻¹ := by
  rw [chi_eq_chi_iff h2 u.ne_zero v.ne_zero]
  constructor
  · rintro (h | h)
    · exact Or.inl (Units.ext h)
    · exact Or.inr (Units.ext (by rw [h, Units.val_inv_eq_inv_val]))
  · rintro (rfl | rfl)
    · exact Or.inl rfl
    · exact Or.inr (Units.val_inv_eq_inv_val u)

/-! ## Twin cosets and torus fibers (`lem:torus-fibers`, cyclic core)

The abstract cyclic-group core of `lem:torus-fibers` (tex/cs25_cap_v12.tex): the
kernel of the `a`-power map has exactly `a` elements, the `a`-power map is exactly
`a`-to-one on each coset of `H`, the two image cosets are disjoint or coincident
according to `g^{2a} ∉/∈ H^{(a)}`, and the all-scales criterion
`(∀ a ∣ M, g^{2a} ∉ H^{(a)}) ↔ ord(g) ∤ 2M`.  The same statements serve
`lem:cheb-smooth` of `experimental/rs_mca_thresholds.tex`, whose hypotheses are
identical. -/

section TorusFibers

variable {G : Type*} [CommGroup G] [Fintype G]

/-- The twin coset `𝒟(g, H) = gH ∪ g⁻¹H` of circle FFT (`def:circle-twin-domain`
in the thresholds draft; twin-coset preamble in tex/cs25_cap_v12.tex). -/
def twinCoset (g : G) (H : Subgroup G) : Set G :=
  (g • (H : Set G)) ∪ (g⁻¹ • (H : Set G))

theorem mem_twinCoset {g u : G} {H : Subgroup G} :
    u ∈ twinCoset g H ↔ (∃ h ∈ H, g * h = u) ∨ (∃ h ∈ H, g⁻¹ * h = u) := by
  simp [twinCoset, Set.mem_smul_set, smul_eq_mul]

/-- A twin coset is closed under inversion. -/
theorem inv_mem_twinCoset {g u : G} {H : Subgroup G} (hu : u ∈ twinCoset g H) :
    u⁻¹ ∈ twinCoset g H := by
  rcases mem_twinCoset.mp hu with ⟨h, hh, rfl⟩ | ⟨h, hh, rfl⟩
  · exact mem_twinCoset.mpr (Or.inr ⟨h⁻¹, H.inv_mem hh, by rw [mul_inv_rev, mul_comm]⟩)
  · exact mem_twinCoset.mpr (Or.inl ⟨h⁻¹, H.inv_mem hh, by rw [mul_inv_rev, inv_inv, mul_comm]⟩)

/-- The twin coset is symmetric in `g ↔ g⁻¹`. -/
theorem twinCoset_inv (g : G) (H : Subgroup G) : twinCoset g⁻¹ H = twinCoset g H := by
  simp [twinCoset, inv_inv, Set.union_comm]

/-- If `g² ∉ H`, the two constituent cosets of a twin coset are disjoint. -/
theorem twin_coset_sides_disjoint {g : G} {H : Subgroup G} (hg2 : g ^ 2 ∉ H) {u : G}
    (h1 : ∃ h ∈ H, g * h = u) (h2 : ∃ h ∈ H, g⁻¹ * h = u) : False := by
  obtain ⟨h₁, hh₁, rfl⟩ := h1
  obtain ⟨h₂, hh₂, heq⟩ := h2
  apply hg2
  have h4 : g * (g⁻¹ * h₂) = g * (g * h₁) := congrArg (g * ·) heq
  rw [mul_inv_cancel_left] at h4
  have h3 : g ^ 2 = h₂ * h₁⁻¹ := by rw [h4, pow_two]; group
  exact h3 ▸ H.mul_mem hh₂ (H.inv_mem hh₁)

/-- **A twin coset contains no self-inverse element** (twin-coset preamble,
tex/cs25_cap_v12.tex; asserted inside `def:circle-twin-domain` /
`lem:cheb-smooth` of the thresholds draft). -/
theorem twinCoset_no_self_inverse {g : G} {H : Subgroup G} (hg2 : g ^ 2 ∉ H) :
    ∀ u ∈ twinCoset g H, u⁻¹ ≠ u := by
  intro u hu heq
  rcases mem_twinCoset.mp hu with ⟨h, hh, rfl⟩ | ⟨h, hh, rfl⟩
  · refine twin_coset_sides_disjoint hg2 ⟨h, hh, rfl⟩ ⟨h⁻¹, H.inv_mem hh, ?_⟩
    rw [show g⁻¹ * h⁻¹ = (g * h)⁻¹ by rw [mul_inv_rev, mul_comm]]
    exact heq
  · refine twin_coset_sides_disjoint hg2 ⟨h⁻¹, H.inv_mem hh, ?_⟩ ⟨h, hh, rfl⟩
    rw [show g * h⁻¹ = (g⁻¹ * h)⁻¹ by rw [mul_inv_rev, inv_inv, mul_comm]]
    exact heq

/-- Elements of a subgroup are killed by its order. -/
theorem pow_card_subgroup_eq_one {H : Subgroup G} {x : G} (hx : x ∈ H) :
    x ^ Fintype.card H = 1 := by
  have h := pow_card_eq_one (G := H) (x := ⟨x, hx⟩)
  have h' := congrArg (fun y : H => (y : G)) h
  simpa only [SubmonoidClass.coe_pow, OneMemClass.coe_one] using h'

/-- **The `a`-power kernel has exactly `a` elements** in a finite cyclic group whose
order is divisible by `a` (`lem:torus-fibers`, kernel step: `a ∣ M ∣ |𝕌|`). -/
theorem card_pow_eq_one_of_dvd_card [IsCyclic G] {a : ℕ} (ha : 0 < a)
    (haG : a ∣ Fintype.card G) :
    (Finset.univ.filter fun u : G => u ^ a = 1).card = a := by
  classical
  refine le_antisymm (by simpa using IsCyclic.card_pow_eq_one_le (α := G) ha) ?_
  obtain ⟨ζ, hζ⟩ := IsCyclic.exists_generator (α := G)
  have hord : orderOf ζ = Fintype.card G := by
    rw [orderOf_eq_card_of_forall_mem_zpowers hζ, Nat.card_eq_fintype_card]
  have hcard0 : Fintype.card G ≠ 0 := Fintype.card_ne_zero
  set w : G := ζ ^ (Fintype.card G / a) with hw
  have hdvd : Fintype.card G / a ∣ Fintype.card G :=
    ⟨a, (Nat.div_mul_cancel haG).symm⟩
  have hordw : orderOf w = a := by
    rw [hw, orderOf_pow, hord, Nat.gcd_comm, Nat.gcd_eq_left hdvd,
      Nat.div_div_self haG hcard0]
  calc a = (Finset.range a).card := (Finset.card_range a).symm
    _ ≤ (Finset.univ.filter fun u : G => u ^ a = 1).card := by
        refine Finset.card_le_card_of_injOn (fun m => w ^ m) ?_ ?_
        · intro m _
          refine Finset.mem_filter.mpr ⟨Finset.mem_univ _, ?_⟩
          rw [← pow_mul, mul_comm, pow_mul, ← hordw, pow_orderOf_eq_one, one_pow]
        · intro m hm m' hm' hmm
          have : (Set.Iio (orderOf w)).InjOn (w ^ ·) := pow_injOn_Iio_orderOf
          rw [Finset.coe_range] at hm hm'
          rw [hordw] at this
          exact this hm hm' hmm

/-- In a finite cyclic group, `H` is exactly the `|H|`-torsion: any `u` with
`u^{|H|} = 1` lies in `H` (unique subgroup of each order). -/
theorem mem_of_pow_card_eq_one [IsCyclic G] {H : Subgroup G} {u : G}
    (hu : u ^ Fintype.card H = 1) : u ∈ H := by
  classical
  have hpos : 0 < Fintype.card H := Fintype.card_pos_iff.mpr ⟨1⟩
  have hSle : (Finset.univ.filter fun x : G => x ∈ H)
      ⊆ Finset.univ.filter fun x : G => x ^ Fintype.card H = 1 := by
    intro x hx
    have hxH : x ∈ H := (Finset.mem_filter.mp hx).2
    exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, pow_card_subgroup_eq_one hxH⟩
  have hScard : (Finset.univ.filter fun x : G => x ∈ H).card = Fintype.card H :=
    (Fintype.card_subtype _).symm
  have hTle : (Finset.univ.filter fun x : G => x ^ Fintype.card H = 1).card
      ≤ Fintype.card H := by
    simpa using IsCyclic.card_pow_eq_one_le (α := G) hpos
  have heq := Finset.eq_of_subset_of_card_le hSle (hTle.trans (le_of_eq hScard.symm))
  have humem : u ∈ Finset.univ.filter fun x : G => x ^ Fintype.card H = 1 :=
    Finset.mem_filter.mpr ⟨Finset.mem_univ _, hu⟩
  rw [← heq] at humem
  exact (Finset.mem_filter.mp humem).2

/-- Torsion transfer: if `a ∣ |H|` and `k^a = 1`, then `k ∈ H` (cyclic ambient). -/
theorem mem_of_pow_eq_one_of_dvd [IsCyclic G] {H : Subgroup G} {a : ℕ}
    (haH : a ∣ Fintype.card H) {k : G} (hk : k ^ a = 1) : k ∈ H := by
  obtain ⟨c, hc⟩ := haH
  exact mem_of_pow_card_eq_one (by rw [hc, pow_mul, hk, one_pow])

/-- **The `a`-power map is exactly `a`-to-one on each coset** (`lem:torus-fibers`,
fiber step): for `u₀ ∈ gH` and `a ∣ |H|`, the fiber `{u ∈ gH : uᵃ = u₀ᵃ}` has
exactly `a` elements (a translate of the `a`-power kernel `K_a ≤ H`). -/
theorem coset_pow_fiber_card [IsCyclic G] {H : Subgroup G} {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H) (g u₀ : G) (hu₀ : ∃ h ∈ H, g * h = u₀) :
    (Finset.univ.filter fun u : G => (∃ h ∈ H, g * h = u) ∧ u ^ a = u₀ ^ a).card = a := by
  classical
  have haG : a ∣ Fintype.card G := by
    have hdvd := Subgroup.card_subgroup_dvd_card H
    simp only [Nat.card_eq_fintype_card] at hdvd
    exact haH.trans hdvd
  obtain ⟨h₀, hh₀, hgh₀⟩ := hu₀
  calc (Finset.univ.filter fun u : G => (∃ h ∈ H, g * h = u) ∧ u ^ a = u₀ ^ a).card
      = (Finset.univ.filter fun u : G => u ^ a = 1).card := by
        refine Finset.card_bij (fun u _ => u₀⁻¹ * u) ?_ ?_ ?_
        · rintro u hu
          obtain ⟨⟨h, hh, rfl⟩, hpow⟩ := Finset.mem_filter.mp hu |>.2
          refine Finset.mem_filter.mpr ⟨Finset.mem_univ _, ?_⟩
          show (u₀⁻¹ * (g * h)) ^ a = 1
          rw [mul_pow, inv_pow, hpow, inv_mul_cancel]
        · intro u₁ hu₁ u₂ hu₂ h12
          exact mul_left_cancel h12
        · intro k hk
          have hk1 : k ^ a = 1 := (Finset.mem_filter.mp hk).2
          have hkH : k ∈ H := mem_of_pow_eq_one_of_dvd haH hk1
          have hmemfib : u₀ * k ∈ Finset.univ.filter
              fun u : G => (∃ h ∈ H, g * h = u) ∧ u ^ a = u₀ ^ a := by
            refine Finset.mem_filter.mpr
              ⟨Finset.mem_univ _, ⟨h₀ * k, H.mul_mem hh₀ hkH, ?_⟩, ?_⟩
            · rw [← mul_assoc, hgh₀]
            · rw [mul_pow, hk1, mul_one]
          exact ⟨u₀ * k, hmemfib, by show u₀⁻¹ * (u₀ * k) = k; rw [inv_mul_cancel_left]⟩
    _ = a := card_pow_eq_one_of_dvd_card (G := G) ha haG

/-- **Cross-coset fibers are empty under the disjointness hypothesis**
(`lem:torus-fibers`, disjoint branch of the dichotomy): if `g^{2a} ∉ H^{(a)}`,
no `u ∈ g⁻¹H` has `uᵃ = u₀ᵃ` for `u₀ ∈ gH`. -/
theorem coset_pow_fiber_cross_empty {H : Subgroup G} {a : ℕ} (g : G)
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    {u u₀ : G} (hu₀ : ∃ h ∈ H, g * h = u₀) (hu : ∃ h ∈ H, g⁻¹ * h = u) :
    u ^ a ≠ u₀ ^ a := by
  intro heq
  obtain ⟨h₀, hh₀, rfl⟩ := hu₀
  obtain ⟨h₁, hh₁, rfl⟩ := hu
  apply hg2a
  refine Subgroup.mem_map.mpr ⟨h₁ * h₀⁻¹, H.mul_mem hh₁ (H.inv_mem hh₀), ?_⟩
  simp only [powMonoidHom_apply]
  rw [mul_pow, mul_pow, inv_pow] at heq
  rw [inv_mul_eq_iff_eq_mul] at heq
  calc (h₁ * h₀⁻¹) ^ a = h₁ ^ a * (h₀ ^ a)⁻¹ := by rw [mul_pow, inv_pow]
    _ = (g ^ a * (g ^ a * h₀ ^ a)) * (h₀ ^ a)⁻¹ := by rw [heq]
    _ = g ^ (2 * a) := by rw [two_mul, pow_add]; group

/-- **Coincident branch of the dichotomy** (`lem:torus-fibers`(b), coset level):
if `g^{2a} ∈ H^{(a)}`, the two image cosets coincide. -/
theorem twin_coset_image_coincident {H : Subgroup G} {a : ℕ} {g : G}
    (hin : g ^ (2 * a) ∈ Subgroup.map (powMonoidHom a) H) :
    (g ^ a) • ((Subgroup.map (powMonoidHom a) H : Subgroup G) : Set G)
      = (g⁻¹ ^ a) • ((Subgroup.map (powMonoidHom a) H : Subgroup G) : Set G) := by
  set K := Subgroup.map (powMonoidHom a) H
  ext x
  rw [mem_leftCoset_iff, mem_leftCoset_iff]
  constructor
  · intro hx
    have : (g⁻¹ ^ a)⁻¹ * x = g ^ (2 * a) * ((g ^ a)⁻¹ * x) := by
      rw [two_mul, pow_add]; group
    rw [this]
    exact K.mul_mem hin hx
  · intro hx
    have : (g ^ a)⁻¹ * x = (g ^ (2 * a))⁻¹ * ((g⁻¹ ^ a)⁻¹ * x) := by
      rw [two_mul, pow_add]; group
    rw [this]
    exact K.mul_mem (K.inv_mem hin) hx

/-- **All-scales criterion** (`lem:torus-fibers`, final claim): `g^{2a} ∉ H^{(a)}`
holds for every positive `a ∣ |H|` simultaneously iff `ord(g) ∤ 2|H|`. -/
theorem twin_coset_all_scales_iff {g : G} (H : Subgroup G) :
    (∀ a : ℕ, 0 < a → a ∣ Fintype.card H →
        g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
      ↔ ¬ orderOf g ∣ 2 * Fintype.card H := by
  constructor
  · intro hall hdvd
    refine hall (Fintype.card H) (Fintype.card_pos_iff.mpr ⟨1⟩) dvd_rfl ?_
    refine Subgroup.mem_map.mpr ⟨1, H.one_mem, ?_⟩
    simp only [powMonoidHom_apply, one_pow]
    exact (orderOf_dvd_iff_pow_eq_one.mp hdvd).symm
  · intro hnd a ha haH hmem
    apply hnd
    obtain ⟨h, hh, hpow⟩ := Subgroup.mem_map.mp hmem
    simp only [powMonoidHom_apply] at hpow
    obtain ⟨c, hc⟩ := haH
    rw [orderOf_dvd_iff_pow_eq_one, hc, show 2 * (a * c) = 2 * a * c by ring, pow_mul,
      ← hpow, ← pow_mul, ← hc]
    exact pow_card_subgroup_eq_one hh

/-- Auxiliary single-value fiber count on a full twin coset, left-based value:
for `w ∈ gH` and `g^{2a} ∉ H^{(a)}`, `#{u ∈ 𝒟 : uᵃ = wᵃ} = a`. -/
theorem twin_coset_pow_eq_card_left [IsCyclic G] {H : Subgroup G} {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H) (g : G)
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    {w : G} (hw : ∃ h ∈ H, g * h = w) :
    (Finset.univ.filter fun u : G =>
        ((∃ h ∈ H, g * h = u) ∨ (∃ h ∈ H, g⁻¹ * h = u)) ∧ u ^ a = w ^ a).card = a := by
  classical
  have hsplit : (Finset.univ.filter fun u : G =>
      ((∃ h ∈ H, g * h = u) ∨ (∃ h ∈ H, g⁻¹ * h = u)) ∧ u ^ a = w ^ a)
      = (Finset.univ.filter fun u : G => (∃ h ∈ H, g * h = u) ∧ u ^ a = w ^ a)
        ∪ (Finset.univ.filter fun u : G => (∃ h ∈ H, g⁻¹ * h = u) ∧ u ^ a = w ^ a) := by
    rw [← Finset.filter_or]
    exact Finset.filter_congr fun u _ => or_and_right
  have hempty : (Finset.univ.filter fun u : G =>
      (∃ h ∈ H, g⁻¹ * h = u) ∧ u ^ a = w ^ a) = ∅ := by
    rw [Finset.filter_eq_empty_iff]
    rintro u - ⟨hu, hpow⟩
    exact coset_pow_fiber_cross_empty g hg2a hw hu hpow
  rw [hsplit, hempty, Finset.union_empty]
  exact coset_pow_fiber_card ha haH g w hw

/-- Auxiliary single-value fiber count, right-based value: for `w ∈ g⁻¹H`,
`#{u ∈ 𝒟 : uᵃ = wᵃ} = a`. -/
theorem twin_coset_pow_eq_card_right [IsCyclic G] {H : Subgroup G} {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H) (g : G)
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    {w : G} (hw : ∃ h ∈ H, g⁻¹ * h = w) :
    (Finset.univ.filter fun u : G =>
        ((∃ h ∈ H, g * h = u) ∨ (∃ h ∈ H, g⁻¹ * h = u)) ∧ u ^ a = w ^ a).card = a := by
  classical
  have hg2a' : g⁻¹ ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H := by
    rw [inv_pow, (Subgroup.map (powMonoidHom a) H).inv_mem_iff]
    exact hg2a
  calc (Finset.univ.filter fun u : G =>
        ((∃ h ∈ H, g * h = u) ∨ (∃ h ∈ H, g⁻¹ * h = u)) ∧ u ^ a = w ^ a).card
      = (Finset.univ.filter fun u : G =>
          ((∃ h ∈ H, g⁻¹ * h = u) ∨ (∃ h ∈ H, g⁻¹⁻¹ * h = u)) ∧ u ^ a = w ^ a).card := by
        refine congrArg Finset.card (Finset.filter_congr fun u _ => ?_)
        rw [inv_inv]
        exact and_congr_left fun _ => or_comm
    _ = a := twin_coset_pow_eq_card_left ha haH g⁻¹ hg2a' hw

/-- **The twin coset is `(Xᵃ, a)`-smooth at the set level** (`lem:torus-fibers`(a)):
for `u₀ ∈ 𝒟` and `g^{2a} ∉ H^{(a)}`, `#{u ∈ 𝒟 : uᵃ = u₀ᵃ} = a`. -/
theorem twin_coset_pow_fiber_card [IsCyclic G] {H : Subgroup G} {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H) {g : G}
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    {u₀ : G} (hu₀ : u₀ ∈ twinCoset g H) :
    (Finset.univ.filter fun u : G =>
        u ∈ twinCoset g H ∧ u ^ a = u₀ ^ a).card = a := by
  classical
  have hrw : (Finset.univ.filter fun u : G => u ∈ twinCoset g H ∧ u ^ a = u₀ ^ a)
      = Finset.univ.filter fun u : G =>
        ((∃ h ∈ H, g * h = u) ∨ (∃ h ∈ H, g⁻¹ * h = u)) ∧ u ^ a = u₀ ^ a :=
    Finset.filter_congr fun u _ => by rw [mem_twinCoset]
  rw [hrw]
  rcases mem_twinCoset.mp hu₀ with hside | hside
  · exact twin_coset_pow_eq_card_left ha haH g hg2a hside
  · exact twin_coset_pow_eq_card_right ha haH g hg2a hside

/-- **The `E_w` pair count** (`lem:cheb-fibers`, printed proof): for `u₀ ∈ 𝒟`, the
solution set `E_w = {u ∈ 𝒟 : uᵃ ∈ {u₀ᵃ, u₀⁻ᵃ}}` has exactly `2a` elements.  This
is the counting hypothesis that the previous `lem_cheb_fibers` skeleton assumed
(as `htwin`); here it is proved. -/
theorem twin_coset_pow_pair_card [IsCyclic G] {H : Subgroup G} {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H) {g : G} (_hg2 : g ^ 2 ∉ H)
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    {u₀ : G} (hu₀ : u₀ ∈ twinCoset g H) :
    (Finset.univ.filter fun u : G =>
        u ∈ twinCoset g H ∧ (u ^ a = u₀ ^ a ∨ u ^ a = (u₀ ^ a)⁻¹)).card = 2 * a := by
  classical
  -- the two branch values are distinct: otherwise `u₀^{2a} = 1` puts `g^{2a}` in `H^{(a)}`
  have hne : u₀ ^ a ≠ (u₀ ^ a)⁻¹ := by
    intro hself
    apply hg2a
    have h2a1 : u₀ ^ (2 * a) = 1 := by
      have hmul : u₀ ^ a * u₀ ^ a = 1 := by
        nth_rewrite 1 [hself]
        exact inv_mul_cancel _
      rw [two_mul, pow_add]
      exact hmul
    rcases mem_twinCoset.mp hu₀ with ⟨h₀, hh₀, rfl⟩ | ⟨h₀, hh₀, rfl⟩
    · refine Subgroup.mem_map.mpr ⟨(h₀ ^ 2)⁻¹, H.inv_mem (H.pow_mem hh₀ 2), ?_⟩
      simp only [powMonoidHom_apply]
      rw [mul_pow] at h2a1
      have hinv : g ^ (2 * a) = (h₀ ^ (2 * a))⁻¹ := by
        rw [eq_inv_iff_mul_eq_one]; exact h2a1
      rw [inv_pow, ← pow_mul, hinv]
    · refine Subgroup.mem_map.mpr ⟨h₀ ^ 2, H.pow_mem hh₀ 2, ?_⟩
      simp only [powMonoidHom_apply]
      rw [mul_pow, inv_pow] at h2a1
      have heq2 : g ^ (2 * a) = h₀ ^ (2 * a) := inv_mul_eq_one.mp h2a1
      rw [← pow_mul, ← heq2]
  -- split the pair filter into the two single-value filters
  have hsplit : (Finset.univ.filter fun u : G =>
      u ∈ twinCoset g H ∧ (u ^ a = u₀ ^ a ∨ u ^ a = (u₀ ^ a)⁻¹))
      = (Finset.univ.filter fun u : G => u ∈ twinCoset g H ∧ u ^ a = u₀ ^ a)
        ∪ (Finset.univ.filter fun u : G => u ∈ twinCoset g H ∧ u ^ a = (u₀ ^ a)⁻¹) := by
    rw [← Finset.filter_or]
    exact Finset.filter_congr fun u _ => and_or_left
  have hdisj : Disjoint
      (Finset.univ.filter fun u : G => u ∈ twinCoset g H ∧ u ^ a = u₀ ^ a)
      (Finset.univ.filter fun u : G => u ∈ twinCoset g H ∧ u ^ a = (u₀ ^ a)⁻¹) := by
    rw [Finset.disjoint_left]
    rintro u hu1 hu2
    have h1 := (Finset.mem_filter.mp hu1).2.2
    have h2 := (Finset.mem_filter.mp hu2).2.2
    exact hne (h1 ▸ h2)
  have hcount1 : (Finset.univ.filter fun u : G =>
      u ∈ twinCoset g H ∧ u ^ a = u₀ ^ a).card = a :=
    twin_coset_pow_fiber_card ha haH hg2a hu₀
  have hcount2 : (Finset.univ.filter fun u : G =>
      u ∈ twinCoset g H ∧ u ^ a = (u₀ ^ a)⁻¹).card = a := by
    calc (Finset.univ.filter fun u : G =>
          u ∈ twinCoset g H ∧ u ^ a = (u₀ ^ a)⁻¹).card
        = (Finset.univ.filter fun u : G =>
            u ∈ twinCoset g H ∧ u ^ a = u₀⁻¹ ^ a).card := by
          refine congrArg Finset.card (Finset.filter_congr fun u _ => ?_)
          rw [inv_pow]
      _ = a := twin_coset_pow_fiber_card ha haH hg2a (inv_mem_twinCoset hu₀)
  rw [hsplit, Finset.card_union_of_disjoint hdisj, hcount1, hcount2, two_mul]

/-- **Standard-position cosets are twin cosets with `ord(g) ∤ 2M`**
(`rem:standard-position`, tex/cs25_cap_v12.tex; this is also the instantiation
`H = ⟨g⁴⟩`, `ord(g) = 4n` used by `thm:fixed-length-prime-density`(c) in the
thresholds draft): with `ord(g) = 4M` and `H₀ = ⟨g²⟩`, the coset `gH₀` is the
twin coset of `K = ⟨g⁴⟩`, with `g² ∉ K`, `ord(g) ∤ 2M`, and `|K| = M`. -/
theorem standard_position_twin_coset {g : G} {M : ℕ} (hM : 0 < M)
    (horder : orderOf g = 4 * M) :
    g • ((Subgroup.zpowers (g ^ 2) : Subgroup G) : Set G)
        = twinCoset g (Subgroup.zpowers (g ^ 4))
      ∧ g ^ 2 ∉ Subgroup.zpowers (g ^ 4)
      ∧ ¬ orderOf g ∣ 2 * M
      ∧ Fintype.card (Subgroup.zpowers (g ^ 4)) = M := by
  classical
  have hg2notK : g ^ 2 ∉ Subgroup.zpowers (g ^ 4) := by
    intro hmem
    obtain ⟨t, ht⟩ := Subgroup.mem_zpowers_iff.mp hmem
    have h1 : g ^ ((4 : ℤ) * t - 2) = 1 := by
      have h4t : (g ^ (4 : ℕ)) ^ t = g ^ ((4 : ℤ) * t) := by
        rw [← zpow_natCast g 4, ← zpow_mul]
        norm_cast
      rw [zpow_sub, ← h4t, ht, zpow_two]
      group
    have h2 : ((4 * M : ℕ) : ℤ) ∣ (4 : ℤ) * t - 2 := by
      rw [← horder]
      exact orderOf_dvd_iff_zpow_eq_one.mpr h1
    obtain ⟨c, hc⟩ := h2
    have hcast : ((4 * M : ℕ) : ℤ) = 4 * (M : ℤ) := by push_cast; ring
    rw [hcast] at hc
    have h4 : (4 : ℤ) ∣ (4 : ℤ) * t - 2 := ⟨(M : ℤ) * c, by rw [hc]; ring⟩
    obtain ⟨d, hd⟩ := h4
    omega
  have key4 : ∀ n : ℤ, (g ^ (4 : ℕ)) ^ n = g ^ (4 * n) := fun n => by
    rw [← zpow_natCast g 4, ← zpow_mul]
    norm_cast
  have key2 : ∀ n : ℤ, (g ^ (2 : ℕ)) ^ n = g ^ (2 * n) := fun n => by
    rw [← zpow_natCast g 2, ← zpow_mul]
    norm_cast
  have hgz : ∀ m : ℤ, g * g ^ m = g ^ (1 + m) := fun m => by
    rw [zpow_add, zpow_one]
  have hgzinv : ∀ m : ℤ, g⁻¹ * g ^ m = g ^ (-1 + m) := fun m => by
    rw [zpow_add, zpow_neg_one]
  refine ⟨?_, hg2notK, ?_, ?_⟩
  · ext u
    constructor
    · intro hu
      rw [mem_leftCoset_iff] at hu
      obtain ⟨t, ht⟩ := Subgroup.mem_zpowers_iff.mp hu
      have hu' : u = g ^ (1 + 2 * t) := by
        have hmul : g * ((g ^ (2 : ℕ)) ^ t) = g * (g⁻¹ * u) := congrArg (g * ·) ht
        rw [mul_inv_cancel_left] at hmul
        rw [← hmul, key2, hgz]
      rcases Int.even_or_odd t with ⟨s, hs⟩ | ⟨s, hs⟩
      · refine mem_twinCoset.mpr
          (Or.inl ⟨(g ^ 4) ^ s, Subgroup.mem_zpowers_iff.mpr ⟨s, rfl⟩, ?_⟩)
        rw [key4, hgz, hu']
        congr 1
        omega
      · refine mem_twinCoset.mpr (Or.inr ⟨(g ^ 4) ^ (s + 1),
          Subgroup.mem_zpowers_iff.mpr ⟨s + 1, rfl⟩, ?_⟩)
        rw [key4, hgzinv, hu']
        congr 1
        omega
    · intro hu
      rw [mem_leftCoset_iff]
      rcases mem_twinCoset.mp hu with ⟨x, hx, hxu⟩ | ⟨x, hx, hxu⟩ <;>
        obtain ⟨s, hs⟩ := Subgroup.mem_zpowers_iff.mp hx
      · refine Subgroup.mem_zpowers_iff.mpr ⟨2 * s, ?_⟩
        rw [← hxu, ← hs, key4, inv_mul_cancel_left, key2]
        congr 1
        ring
      · refine Subgroup.mem_zpowers_iff.mpr ⟨2 * s - 1, ?_⟩
        rw [← hxu, ← hs, key4, hgzinv, hgzinv, key2]
        congr 1
        ring
  · intro hdvd
    rw [horder] at hdvd
    have := Nat.le_of_dvd (by omega) hdvd
    omega
  · have hord4 : orderOf (g ^ (4 : ℕ)) = M := by
      rw [orderOf_pow, horder, Nat.gcd_comm, Nat.gcd_eq_left ⟨M, rfl⟩,
        Nat.mul_div_cancel_left M (by norm_num)]
    rw [← Nat.card_eq_fintype_card, Nat.card_zpowers, hord4]

end TorusFibers

/-! ## The `χ`-projection counts and the Chebyshev fiber theorem -/

/-- **`χ` halves inversion-closed self-inverse-free sets**: if `S ⊆ Fˣ` is closed
under inversion and has no self-inverse element, then `2·|χ(S)| = |S|`. -/
theorem chi_pair_image_card (h2 : (2 : F) ≠ 0) (S : Finset Fˣ)
    (hinv : ∀ u ∈ S, u⁻¹ ∈ S) (hself : ∀ u ∈ S, u⁻¹ ≠ u) :
    2 * (S.image fun u : Fˣ => chi (u : F)).card = S.card := by
  classical
  rw [Finset.card_eq_sum_card_image (fun u : Fˣ => chi (u : F)) S]
  have hfib : ∀ b ∈ S.image fun u : Fˣ => chi (u : F),
      (S.filter fun u : Fˣ => chi (u : F) = b).card = 2 := by
    intro b hb
    obtain ⟨u₀, hu₀S, rfl⟩ := Finset.mem_image.mp hb
    have hfset : (S.filter fun u : Fˣ => chi (u : F) = chi (u₀ : F)) = {u₀, u₀⁻¹} := by
      ext u
      simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton]
      constructor
      · rintro ⟨huS, hchi⟩
        rcases (chi_val_eq_chi_val_iff h2).mp hchi with h | h
        · exact Or.inl (by rw [← h])
        · exact Or.inr (by rw [h, inv_inv])
      · rintro (rfl | rfl)
        · exact ⟨hu₀S, rfl⟩
        · exact ⟨hinv u₀ hu₀S, by rw [Units.val_inv_eq_inv_val, chi_inv]⟩
    rw [hfset, Finset.card_pair (Ne.symm (hself u₀ hu₀S))]
  rw [Finset.sum_congr rfl hfib, Finset.sum_const, smul_eq_mul, mul_comm]

/-- **`|χ(𝒟)| = |H|`** for a twin coset `𝒟 = gH ∪ g⁻¹H` with `g² ∉ H`
(twin-coset preamble, tex/cs25_cap_v12.tex; this is the cardinality claim stated
without proof inside `def:circle-twin-domain` of the thresholds draft). -/
theorem twin_coset_chi_card (H : Subgroup Fˣ) (g : Fˣ) (hg2 : g ^ 2 ∉ H)
    (h2 : (2 : F) ≠ 0) :
    ((Finset.univ.filter fun u : Fˣ => u ∈ twinCoset g H).image
        fun u : Fˣ => chi (u : F)).card = Fintype.card H := by
  classical
  set S : Finset Fˣ := Finset.univ.filter fun u : Fˣ => u ∈ twinCoset g H with hS
  have hinv : ∀ u ∈ S, u⁻¹ ∈ S := by
    intro u hu
    refine Finset.mem_filter.mpr ⟨Finset.mem_univ _, inv_mem_twinCoset ?_⟩
    exact (Finset.mem_filter.mp hu).2
  have hself : ∀ u ∈ S, u⁻¹ ≠ u := fun u hu =>
    twinCoset_no_self_inverse hg2 u (Finset.mem_filter.mp hu).2
  have hpair := chi_pair_image_card h2 S hinv hself
  -- `|𝒟| = 2 |H|`: the two constituent cosets are disjoint of size `|H|` each
  have hcosetcard : ∀ g' : Fˣ, (Finset.univ.filter fun u : Fˣ =>
      ∃ h ∈ H, g' * h = u).card = Fintype.card H := by
    intro g'
    have h1 : (Finset.univ.filter fun u : Fˣ => ∃ h ∈ H, g' * h = u).card
        = (Finset.univ.filter fun u : Fˣ => u ∈ H).card := by
      refine Finset.card_bij (fun u _ => g'⁻¹ * u) ?_ ?_ ?_
      · rintro u hu
        obtain ⟨h, hh, rfl⟩ := (Finset.mem_filter.mp hu).2
        refine Finset.mem_filter.mpr ⟨Finset.mem_univ _, ?_⟩
        show g'⁻¹ * (g' * h) ∈ H
        rw [inv_mul_cancel_left]
        exact hh
      · intro u₁ _ u₂ _ h12
        exact mul_left_cancel h12
      · intro h hh
        refine ⟨g' * h, Finset.mem_filter.mpr ⟨Finset.mem_univ _,
          ⟨h, (Finset.mem_filter.mp hh).2, rfl⟩⟩,
          by show g'⁻¹ * (g' * h) = h; rw [inv_mul_cancel_left]⟩
    exact h1.trans (Fintype.card_subtype _).symm
  have hDcard : S.card = 2 * Fintype.card H := by
    have hsplit : S = (Finset.univ.filter fun u : Fˣ => ∃ h ∈ H, g * h = u)
        ∪ (Finset.univ.filter fun u : Fˣ => ∃ h ∈ H, g⁻¹ * h = u) := by
      rw [hS, ← Finset.filter_or]
      exact Finset.filter_congr fun u _ => by rw [mem_twinCoset]
    have hdisj : Disjoint (Finset.univ.filter fun u : Fˣ => ∃ h ∈ H, g * h = u)
        (Finset.univ.filter fun u : Fˣ => ∃ h ∈ H, g⁻¹ * h = u) := by
      rw [Finset.disjoint_left]
      rintro u hu1 hu2
      exact twin_coset_sides_disjoint hg2 (Finset.mem_filter.mp hu1).2
        (Finset.mem_filter.mp hu2).2
    rw [hsplit, Finset.card_union_of_disjoint hdisj, hcosetcard g, hcosetcard g⁻¹, two_mul]
  have := hpair.trans hDcard
  exact Nat.eq_of_mul_eq_mul_left (by norm_num) this

/-- **Discharge of the former `htwin` hypothesis**: on an injective enumeration
`tor : κ → Fˣ` of a full twin coset `𝒟 = gH ∪ g⁻¹H` (with `a ∣ |H|`, `g² ∉ H`,
`g^{2a} ∉ H^{(a)}`), the indexed fiber-pair count is exactly `2a`:
`#{j : tor jᵃ ∈ {tor iᵃ, tor i⁻ᵃ}} = 2a` for every `i`.  This is the Finset
filter-card statement the previous `lem_cheb_fibers` skeleton assumed. -/
theorem htwin_of_twin_coset (H : Subgroup Fˣ) (g : Fˣ) {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H) (hg2 : g ^ 2 ∉ H)
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    {κ : Type*} [Fintype κ] (tor : κ → Fˣ) (hinj : Function.Injective tor)
    (hmem : ∀ i, tor i ∈ twinCoset g H)
    (hsurj : ∀ u ∈ twinCoset g H, ∃ i, tor i = u) :
    ∀ i, (Finset.univ.filter fun j => tor j ^ a = tor i ^ a ∨
        tor j ^ a = (tor i ^ a)⁻¹).card = 2 * a := by
  classical
  intro i
  calc (Finset.univ.filter fun j => tor j ^ a = tor i ^ a ∨
        tor j ^ a = (tor i ^ a)⁻¹).card
      = (Finset.univ.filter fun u : Fˣ =>
          u ∈ twinCoset g H ∧ (u ^ a = tor i ^ a ∨ u ^ a = (tor i ^ a)⁻¹)).card := by
        refine Finset.card_bij (fun j _ => tor j) ?_ ?_ ?_
        · intro j hj
          exact Finset.mem_filter.mpr
            ⟨Finset.mem_univ _, hmem j, (Finset.mem_filter.mp hj).2⟩
        · intro j₁ _ j₂ _ h12
          exact hinj h12
        · intro u hu
          obtain ⟨huD, hupair⟩ := (Finset.mem_filter.mp hu).2
          obtain ⟨j, rfl⟩ := hsurj u huD
          exact ⟨j, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hupair⟩, rfl⟩
    _ = 2 * a := by
        convert twin_coset_pow_pair_card ha haH hg2 hg2a (hmem i) using 2
        exact (Finset.filter_congr_decidable _ _ _).trans
          (Finset.filter_congr_decidable _ _ _).symm

/-- **`lem:torus-fibers` — power fibers on torus twin cosets** (part (a),
`DomSmooth` form): an injective enumeration of a full twin coset
`𝒟 = gH ∪ g⁻¹H` with `a ∣ |H|` and `g^{2a} ∉ H^{(a)}` is `(Xᵃ, a)`-smooth.  The
conclusion is exactly the `hsmooth` hypothesis of `cor_circle_grand`. -/
theorem lem_torus_fibers (H : Subgroup Fˣ) (g : Fˣ) {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H)
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    (torus : ι → F) (tor : ι → Fˣ) (htorus : ∀ i, torus i = tor i)
    (hinj : Function.Injective tor)
    (hmem : ∀ i, tor i ∈ twinCoset g H)
    (hsurj : ∀ u ∈ twinCoset g H, ∃ i, tor i = u) :
    DomSmooth torus (fun x => x ^ a) a := by
  classical
  intro i
  show (Finset.univ.filter fun j => torus j ^ a = torus i ^ a).card = a
  have hval : ∀ j, torus j ^ a = ((tor j ^ a : Fˣ) : F) := fun j => by
    rw [htorus j, Units.val_pow_eq_pow_val]
  have hpred : ∀ j, (torus j ^ a = torus i ^ a) ↔ tor j ^ a = tor i ^ a := fun j => by
    rw [hval j, hval i]
    exact ⟨fun h => Units.ext h, fun h => congrArg Units.val h⟩
  calc (Finset.univ.filter fun j => torus j ^ a = torus i ^ a).card
      = (Finset.univ.filter fun j => tor j ^ a = tor i ^ a).card :=
        congrArg Finset.card (Finset.filter_congr fun j _ => hpred j)
    _ = (Finset.univ.filter fun u : Fˣ =>
          u ∈ twinCoset g H ∧ u ^ a = tor i ^ a).card := by
        refine Finset.card_bij (fun j _ => tor j) ?_ ?_ ?_
        · intro j hj
          exact Finset.mem_filter.mpr
            ⟨Finset.mem_univ _, hmem j, (Finset.mem_filter.mp hj).2⟩
        · intro j₁ _ j₂ _ h12
          exact hinj h12
        · intro u hu
          obtain ⟨huD, hupow⟩ := (Finset.mem_filter.mp hu).2
          obtain ⟨j, rfl⟩ := hsurj u huD
          exact ⟨j, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hupow⟩, rfl⟩
    _ = a := by
        convert twin_coset_pow_fiber_card ha haH hg2a (hmem i) using 2
        exact (Finset.filter_congr_decidable _ _ _).trans
          (Finset.filter_congr_decidable _ _ _).symm

/-- **`lem:cheb-fibers` — exact Chebyshev fibers on `x`-coordinate twin-coset
domains.**

If `dom` injectively enumerates the `x`-coordinate image `D = χ(𝒟)` of a twin
coset `𝒟 = gH ∪ g⁻¹H` (each `dom i = χ(torus i)` for a section `torus` of `χ`
with values in `𝒟`, and every `χ`-value of `𝒟` is attained), `a ∣ |H|`, and
`g^{2a} ∉ H^{(a)}`, then `dom` is `(T_a, a)`-smooth: every fiber of `x ↦ T_a(x)`
over the domain has exactly `a` elements.  Phrased via `DomSmooth` with the
Chebyshev evaluation map.

Statement repair (see module docstring): the previous skeleton assumed an
index-level `2a`-count `htwin` that is unsatisfiable together with `hdom`; the
twin-coset hypotheses below are the paper's, and the `2a`-count is now the
*proved* `twin_coset_pow_pair_card`/`htwin_of_twin_coset`. -/
theorem lem_cheb_fibers (H : Subgroup Fˣ) (g : Fˣ) {a : ℕ} (ha : 0 < a)
    (haH : a ∣ Fintype.card H) (hg2 : g ^ 2 ∉ H)
    (hg2a : g ^ (2 * a) ∉ Subgroup.map (powMonoidHom a) H)
    (h2 : (2 : F) ≠ 0)
    (dom : ι → F) (hdom : Function.Injective dom)
    (torus : ι → Fˣ) (hdomχ : ∀ i, dom i = chi (torus i : F))
    (hmem : ∀ i, torus i ∈ twinCoset g H)
    (hcover : ∀ u ∈ twinCoset g H, ∃ i, dom i = chi (u : F)) :
    DomSmooth dom (fun x => (Polynomial.Chebyshev.T F (a : ℤ)).eval x) a := by
  classical
  intro i
  show (Finset.univ.filter fun j => (Polynomial.Chebyshev.T F (a : ℤ)).eval (dom j)
      = (Polynomial.Chebyshev.T F (a : ℤ)).eval (dom i)).card = a
  -- the `T_a` fiber condition is the `χ`-pair condition on `a`-th powers
  have hTa : ∀ j, (Polynomial.Chebyshev.T F (a : ℤ)).eval (dom j)
      = chi ((torus j ^ a : Fˣ) : F) := fun j => by
    rw [hdomχ j, chebyshev_semiconjugacy h2 _ (Units.ne_zero _) a,
      Units.val_pow_eq_pow_val]
  have hpred : ∀ j, ((Polynomial.Chebyshev.T F (a : ℤ)).eval (dom j)
        = (Polynomial.Chebyshev.T F (a : ℤ)).eval (dom i))
      ↔ (torus j ^ a = torus i ^ a ∨ torus j ^ a = (torus i ^ a)⁻¹) := fun j => by
    rw [hTa j, hTa i, chi_val_eq_chi_val_iff h2]
    constructor
    · rintro (h | h)
      · exact Or.inl h.symm
      · exact Or.inr (by rw [h, inv_inv])
    · rintro (h | h)
      · exact Or.inl h.symm
      · exact Or.inr (by rw [h, inv_inv])
  -- the `E_w` Finset on the torus side
  set Ew : Finset Fˣ := Finset.univ.filter fun u : Fˣ =>
    u ∈ twinCoset g H ∧ (u ^ a = torus i ^ a ∨ u ^ a = (torus i ^ a)⁻¹) with hEw
  have hEwcard : Ew.card = 2 * a := by
    rw [hEw]
    convert twin_coset_pow_pair_card ha haH hg2 hg2a (hmem i) using 2
    exact (Finset.filter_congr_decidable _ _ _).trans
      (Finset.filter_congr_decidable _ _ _).symm
  have hEwinv : ∀ u ∈ Ew, u⁻¹ ∈ Ew := by
    intro u hu
    obtain ⟨huD, hupair⟩ := (Finset.mem_filter.mp hu).2
    refine Finset.mem_filter.mpr ⟨Finset.mem_univ _, inv_mem_twinCoset huD, ?_⟩
    rcases hupair with h | h
    · exact Or.inr (by rw [inv_pow, h])
    · exact Or.inl (by rw [inv_pow, h, inv_inv])
  have hEwself : ∀ u ∈ Ew, u⁻¹ ≠ u := fun u hu =>
    twinCoset_no_self_inverse hg2 u (Finset.mem_filter.mp hu).2.1
  -- the `T_a` fiber in the `x`-domain is in bijection with `χ(E_w)`
  have hbij : (Finset.univ.filter fun j =>
      (Polynomial.Chebyshev.T F (a : ℤ)).eval (dom j)
        = (Polynomial.Chebyshev.T F (a : ℤ)).eval (dom i)).card
      = (Ew.image fun u : Fˣ => chi (u : F)).card := by
    refine Finset.card_bij (fun j _ => dom j) ?_ ?_ ?_
    · intro j hj
      have hcond := (hpred j).mp (Finset.mem_filter.mp hj).2
      exact Finset.mem_image.mpr ⟨torus j,
        Finset.mem_filter.mpr ⟨Finset.mem_univ _, hmem j, hcond⟩, (hdomχ j).symm⟩
    · intro j₁ _ j₂ _ h12
      exact hdom h12
    · intro b hb
      obtain ⟨u, huEw, rfl⟩ := Finset.mem_image.mp hb
      obtain ⟨huD, hupair⟩ := (Finset.mem_filter.mp huEw).2
      obtain ⟨j, hj⟩ := hcover u huD
      have hju : chi ((torus j : Fˣ) : F) = chi (u : F) := by rw [← hdomχ j, hj]
      have hcase := (chi_val_eq_chi_val_iff h2).mp hju
      refine ⟨j, Finset.mem_filter.mpr ⟨Finset.mem_univ _, (hpred j).mpr ?_⟩, hj⟩
      rcases hcase with rfl | rfl
      · exact hupair
      · rcases hupair with h | h
        · rw [inv_pow] at h
          exact Or.inr (by rw [← h, inv_inv])
        · rw [inv_pow] at h
          exact Or.inl (inv_injective h)
  have hhalf := chi_pair_image_card h2 Ew hEwinv hEwself
  have himg : (Ew.image fun u : Fˣ => chi (u : F)).card = a :=
    Nat.eq_of_mul_eq_mul_left (by norm_num) (hhalf.trans hEwcard)
  rw [hbij]
  exact himg

/-! ## Sum reindexing helpers for the torus/stereographic uniformizations

Two pieces of pure index bookkeeping on `∑_{m < 2w+1}`: the center split used by the
Laurent symmetrization of `lem_circle_rs` (`m = w ± (d+1)` around the middle term
`m = w`), and the parity split used by the even/odd decomposition of
`lem_stereographic`. -/

/-- Center split: `∑_{m<2w+1} g(m) = g(w) + ∑_{d<w} (g(w+d+1) + g(w−d−1))`. -/
theorem sum_range_center {M : Type*} [AddCommMonoid M] (g : ℕ → M) (w : ℕ) :
    ∑ m ∈ Finset.range (2 * w + 1), g m
      = g w + ∑ d ∈ Finset.range w, (g (w + d + 1) + g (w - d - 1)) := by
  induction w with
  | zero => simp
  | succ n ih =>
    have h1 : 2 * (n + 1) + 1 = 2 * n + 1 + 1 + 1 := by ring
    have t1 : (∑ d ∈ Finset.range n, g (n + d + 1)) + g (2 * n + 1)
        = g (n + 1) + ∑ d ∈ Finset.range n, g (n + d + 2) := by
      have e1 := Finset.sum_range_succ (fun d => g (n + d + 1)) n
      have e2 := Finset.sum_range_succ' (fun d => g (n + d + 1)) n
      simp only at e1 e2
      rw [show n + n + 1 = 2 * n + 1 from by omega] at e1
      calc (∑ d ∈ Finset.range n, g (n + d + 1)) + g (2 * n + 1)
          = ∑ d ∈ Finset.range (n + 1), g (n + d + 1) := e1.symm
        _ = (∑ d ∈ Finset.range n, g (n + (d + 1) + 1)) + g (n + 0 + 1) := e2
        _ = g (n + 1) + ∑ d ∈ Finset.range n, g (n + d + 2) := by
            rw [add_comm]
            exact congrArg _ (Finset.sum_congr rfl fun d _ => by
              rw [show n + (d + 1) + 1 = n + d + 2 from by omega])
    have t2 : g n + ∑ d ∈ Finset.range n, g (n - d - 1)
        = (∑ d ∈ Finset.range n, g (n - d)) + g 0 := by
      have e1 := Finset.sum_range_succ (fun d => g (n - d)) n
      have e2 := Finset.sum_range_succ' (fun d => g (n - d)) n
      simp only at e1 e2
      rw [show n - n = 0 from by omega] at e1
      calc g n + ∑ d ∈ Finset.range n, g (n - d - 1)
          = (∑ d ∈ Finset.range n, g (n - (d + 1))) + g (n - 0) := by
            rw [show n - 0 = n from rfl, add_comm]
            exact congrArg (· + g n) (Finset.sum_congr rfl fun d _ => by
              rw [show n - d - 1 = n - (d + 1) from by omega])
        _ = ∑ d ∈ Finset.range (n + 1), g (n - d) := e2.symm
        _ = (∑ d ∈ Finset.range n, g (n - d)) + g 0 := e1
    rw [h1, Finset.sum_range_succ g (2 * n + 1 + 1), Finset.sum_range_succ g (2 * n + 1), ih,
      Finset.sum_range_succ (fun d => g (n + 1 + d + 1) + g (n + 1 - d - 1)) n]
    rw [show n + 1 + n + 1 = 2 * n + 1 + 1 from by omega,
      show n + 1 - n - 1 = 0 from by omega,
      show (∑ d ∈ Finset.range n, (g (n + 1 + d + 1) + g (n + 1 - d - 1)))
          = ∑ d ∈ Finset.range n, (g (n + d + 2) + g (n - d)) from
        Finset.sum_congr rfl fun d _ => by
          rw [show n + 1 + d + 1 = n + d + 2 from by omega,
            show n + 1 - d - 1 = n - d from by omega],
      Finset.sum_add_distrib, Finset.sum_add_distrib]
    calc g n + ((∑ d ∈ Finset.range n, g (n + d + 1)) + ∑ d ∈ Finset.range n, g (n - d - 1))
          + g (2 * n + 1) + g (2 * n + 1 + 1)
        = ((∑ d ∈ Finset.range n, g (n + d + 1)) + g (2 * n + 1))
            + (g n + ∑ d ∈ Finset.range n, g (n - d - 1)) + g (2 * n + 1 + 1) := by abel
      _ = (g (n + 1) + ∑ d ∈ Finset.range n, g (n + d + 2))
            + ((∑ d ∈ Finset.range n, g (n - d)) + g 0) + g (2 * n + 1 + 1) := by rw [t1, t2]
      _ = g (n + 1) + ((∑ d ∈ Finset.range n, g (n + d + 2))
            + ∑ d ∈ Finset.range n, g (n - d) + (g (2 * n + 1 + 1) + g 0)) := by abel

/-- Parity split: `∑_{m<2w+1} g(m) = ∑_{k≤w} g(2k) + ∑_{k<w} g(2k+1)`. -/
theorem sum_range_parity {M : Type*} [AddCommMonoid M] (g : ℕ → M) (w : ℕ) :
    ∑ m ∈ Finset.range (2 * w + 1), g m
      = (∑ k ∈ Finset.range (w + 1), g (2 * k)) + ∑ k ∈ Finset.range w, g (2 * k + 1) := by
  induction w with
  | zero => simp
  | succ n ih =>
    have h1 : 2 * (n + 1) + 1 = 2 * n + 1 + 1 + 1 := by ring
    rw [h1, Finset.sum_range_succ g (2 * n + 1 + 1), Finset.sum_range_succ g (2 * n + 1), ih,
      Finset.sum_range_succ (fun k => g (2 * k)) (n + 1),
      Finset.sum_range_succ (fun k => g (2 * k + 1)) n]
    rw [show 2 * (n + 1) = 2 * n + 1 + 1 from by omega]
    abel

/-- The degree-`≤ w` circle code `𝒞_w(F, E)` on a set of circle points `pt`, using the
canonical free-module form `f₀(x) + y·f₁(x)` with `deg f₀ ≤ w`, `deg f₁ ≤ w − 1`. -/
def circleCode (pt : ι → F × F) (w : ℕ) : Set (ι → F) :=
  {c | ∃ f0 f1 : Polynomial F, f0.degree ≤ (w : WithBot ℕ) ∧
        f1.degree < (w : WithBot ℕ) ∧
        ∀ i, c i = f0.eval (pt i).1 + (pt i).2 * f1.eval (pt i).1}

/-- **`lem:circle-rs` — torus uniformization of circle codes.**

With `i ∈ F`, `i² = −1`, the coordinate `u = x + iy` sends the circle point `pt i` to
the torus point `torus i`; then the degree-`≤ w` circle code equals the diagonally
twisted Reed–Solomon code `RS[F, E', 2w+1]` on the torus domain, the twist being
`t i = (torus i)^(−w)`.  Consequently the two codes have identical list sizes and
identical `ε_ca`, `ε_mca` at every radius.

Statement repair (see `lem_circle_rs_false` below): the previous skeleton omitted
the odd-characteristic hypothesis `(2 : F) ≠ 0` and was **false as stated** — the
paper carries `p ≡ 3 (mod 4)` globally (tex/cs25_cap_v12.tex `sec:circle-geometry`
preamble and `lem:circle-rs` itself), so this was a formalization omission, not a
paper defect.  With `h2` added the lemma is proved in full: the forward inclusion
clears denominators into an explicit polynomial `Q` of degree `≤ 2w`, and the
reverse inclusion is the Laurent symmetrization `u^{−w}Q(u) = f₀(χ(u)) + y·f₁(χ(u))`,
whose symmetric part is `chebyshev_semiconjugacy` and whose antisymmetric part is
`chebyshev_antisymm`.  (`htne` is derivable from `hcircle`/`htorus`/`hi` via
`u·(x − iy) = x² + y² = 1`, but is retained to keep the interface unchanged.) -/
theorem lem_circle_rs (pt : ι → F × F) (torus : ι → F) (w : ℕ)
    (h2 : (2 : F) ≠ 0)
    (i_unit : F) (hi : i_unit ^ 2 = -1)
    (hcircle : ∀ j, (pt j).1 ^ 2 + (pt j).2 ^ 2 = 1)
    (htorus : ∀ j, torus j = (pt j).1 + i_unit * (pt j).2) (htne : ∀ j, torus j ≠ 0) :
    circleCode pt w
      = (fun c i => (torus i) ^ (-(w : ℤ)) * c i) '' RSpoly torus (2 * w + 1) := by
  classical
  haveI : NeZero (2 : F) := ⟨h2⟩
  -- `i ≠ 0`, hence `2i ≠ 0`
  have hi0 : i_unit ≠ 0 := by
    intro h0
    have h1 : (-1 : F) = 0 := by rw [← hi, h0]; norm_num
    exact one_ne_zero (neg_eq_zero.mp h1)
  have h2i : (2 * i_unit : F) ≠ 0 := mul_ne_zero h2 hi0
  -- pointwise coordinates: `u⁻¹ = x − iy`, `x = χ(u)`, `y = (u − u⁻¹)/(2i)`
  have hinv : ∀ j, (torus j)⁻¹ = (pt j).1 - i_unit * (pt j).2 := by
    intro j
    refine inv_eq_of_mul_eq_one_right ?_
    rw [htorus j]
    linear_combination hcircle j - (pt j).2 ^ 2 * hi
  have hchi : ∀ j, chi (torus j) = (pt j).1 := by
    intro j
    simp only [chi]
    rw [hinv j, htorus j, div_eq_iff h2]
    ring
  have hx : ∀ j, (pt j).1 = (torus j + (torus j)⁻¹) / 2 := by
    intro j
    rw [← hchi j]
    simp only [chi]
  have hy : ∀ j, (pt j).2 = (torus j - (torus j)⁻¹) / (2 * i_unit) := by
    intro j
    rw [eq_div_iff h2i, hinv j, htorus j]
    ring
  ext c
  constructor
  · -- forward: clear denominators into an explicit `Q` of degree `≤ 2w`
    rintro ⟨f0, f1, hf0, hf1, hc⟩
    have hf0nat : f0.natDegree < w + 1 :=
      Nat.lt_succ_of_le (Polynomial.natDegree_le_iff_degree_le.mpr hf0)
    have hf0eval : ∀ z : F, f0.eval z = ∑ k ∈ Finset.range (w + 1), f0.coeff k * z ^ k :=
      fun z => Polynomial.eval_eq_sum_range' hf0nat z
    have hf1eval : ∀ z : F, f1.eval z = ∑ k ∈ Finset.range w, f1.coeff k * z ^ k := by
      intro z
      rcases eq_or_ne f1 0 with rfl | hne
      · simp
      · exact Polynomial.eval_eq_sum_range'
          ((Polynomial.natDegree_lt_iff_degree_lt hne).mpr hf1) z
    set Q : Polynomial F :=
      (∑ k ∈ Finset.range (w + 1), Polynomial.C (f0.coeff k * (2 : F)⁻¹ ^ k) *
          (Polynomial.X ^ (w - k) * (Polynomial.X ^ 2 + 1) ^ k))
        + ∑ k ∈ Finset.range w,
            Polynomial.C (f1.coeff k * (2 : F)⁻¹ ^ k * (2 * i_unit)⁻¹) *
              ((Polynomial.X ^ 2 - 1) *
                (Polynomial.X ^ (w - 1 - k) * (Polynomial.X ^ 2 + 1) ^ k))
      with hQdef
    have hX21 : (Polynomial.X ^ 2 + 1 : Polynomial F).natDegree ≤ 2 := by
      refine le_trans (Polynomial.natDegree_add_le _ _) ?_
      simp [Polynomial.natDegree_X_pow]
    have hX21' : (Polynomial.X ^ 2 - 1 : Polynomial F).natDegree ≤ 2 := by
      refine le_trans (Polynomial.natDegree_sub_le _ _) ?_
      simp [Polynomial.natDegree_X_pow]
    have hbase : ∀ m k : ℕ, (Polynomial.X ^ m * (Polynomial.X ^ 2 + 1) ^ k
        : Polynomial F).natDegree ≤ m + 2 * k := by
      intro m k
      refine le_trans Polynomial.natDegree_mul_le ?_
      rw [Polynomial.natDegree_X_pow]
      have hk : ((Polynomial.X ^ 2 + 1 : Polynomial F) ^ k).natDegree ≤ k * 2 :=
        le_trans Polynomial.natDegree_pow_le (Nat.mul_le_mul_left k hX21)
      omega
    have hQdeg : Q.degree < ((2 * w + 1 : ℕ) : WithBot ℕ) := by
      have hQnat : Q.natDegree ≤ 2 * w := by
        rw [hQdef]
        refine le_trans (Polynomial.natDegree_add_le _ _) (max_le ?_ ?_)
        · refine Polynomial.natDegree_sum_le_of_forall_le _ _ fun k hk => ?_
          have hkw : k < w + 1 := Finset.mem_range.mp hk
          have h1 : (Polynomial.C (f0.coeff k * (2 : F)⁻¹ ^ k) *
              (Polynomial.X ^ (w - k) * (Polynomial.X ^ 2 + 1) ^ k)).natDegree
              ≤ 0 + ((w - k) + 2 * k) :=
            le_trans Polynomial.natDegree_mul_le
              (add_le_add (Polynomial.natDegree_C _).le (hbase (w - k) k))
          omega
        · refine Polynomial.natDegree_sum_le_of_forall_le _ _ fun k hk => ?_
          have hkw : k < w := Finset.mem_range.mp hk
          have h1 : (Polynomial.C (f1.coeff k * (2 : F)⁻¹ ^ k * (2 * i_unit)⁻¹) *
              ((Polynomial.X ^ 2 - 1) *
                (Polynomial.X ^ (w - 1 - k) * (Polynomial.X ^ 2 + 1) ^ k))).natDegree
              ≤ 0 + (2 + ((w - 1 - k) + 2 * k)) :=
            le_trans Polynomial.natDegree_mul_le
              (add_le_add (Polynomial.natDegree_C _).le
                (le_trans Polynomial.natDegree_mul_le
                  (add_le_add hX21' (hbase (w - 1 - k) k))))
          omega
      refine lt_of_le_of_lt Polynomial.degree_le_natDegree ?_
      exact_mod_cast Nat.lt_succ_of_le hQnat
    have hQeval : ∀ j, Q.eval (torus j)
        = torus j ^ w * (f0.eval ((pt j).1) + (pt j).2 * f1.eval ((pt j).1)) := by
      intro j
      have hu : torus j ≠ 0 := htne j
      have hquad : ∀ k : ℕ, (torus j ^ 2 + 1) ^ k
          = torus j ^ k * (torus j + (torus j)⁻¹) ^ k := by
        intro k
        rw [← mul_pow]
        congr 1
        rw [mul_add, mul_inv_cancel₀ hu]
        ring
      have hterm0 : ∀ k ∈ Finset.range (w + 1),
          (Polynomial.C (f0.coeff k * (2 : F)⁻¹ ^ k) *
            (Polynomial.X ^ (w - k) * (Polynomial.X ^ 2 + 1) ^ k)).eval (torus j)
          = torus j ^ w * (f0.coeff k * ((pt j).1) ^ k) := by
        intro k hk
        have hkw : k ≤ w := Nat.lt_succ_iff.mp (Finset.mem_range.mp hk)
        have hk0 : torus j ^ k ≠ 0 := pow_ne_zero _ hu
        have h2k : (2 : F) ^ k ≠ 0 := pow_ne_zero _ h2
        have hwk : torus j ^ (w - k) = torus j ^ w * (torus j ^ k)⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ hk0, ← pow_add]
          congr 1
          omega
        simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow,
          Polynomial.eval_add, Polynomial.eval_one, Polynomial.eval_X]
        rw [hquad k, hwk, hx j, div_pow, inv_pow]
        field_simp
      have hterm1 : ∀ k ∈ Finset.range w,
          (Polynomial.C (f1.coeff k * (2 : F)⁻¹ ^ k * (2 * i_unit)⁻¹) *
            ((Polynomial.X ^ 2 - 1) *
              (Polynomial.X ^ (w - 1 - k) * (Polynomial.X ^ 2 + 1) ^ k))).eval (torus j)
          = torus j ^ w * ((pt j).2 * (f1.coeff k * ((pt j).1) ^ k)) := by
        intro k hk
        have hkw : k < w := Finset.mem_range.mp hk
        have hk0 : torus j ^ k ≠ 0 := pow_ne_zero _ hu
        have hk10 : torus j ^ (k + 1) ≠ 0 := pow_ne_zero _ hu
        have h2k : (2 : F) ^ k ≠ 0 := pow_ne_zero _ h2
        have hwk : torus j ^ (w - 1 - k) = torus j ^ w * (torus j ^ (k + 1))⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ hk10, ← pow_add]
          congr 1
          omega
        have hquad2 : torus j ^ 2 - 1 = torus j * (torus j - (torus j)⁻¹) := by
          rw [mul_sub, mul_inv_cancel₀ hu]
          ring
        simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow,
          Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_one, Polynomial.eval_X]
        rw [hquad k, hquad2, hwk, hx j, hy j, div_pow, inv_pow]
        field_simp
        ring
      rw [hQdef]
      rw [Polynomial.eval_add, Polynomial.eval_finset_sum, Polynomial.eval_finset_sum,
        Finset.sum_congr rfl hterm0, Finset.sum_congr rfl hterm1,
        hf0eval, hf1eval, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum]
      ring
    refine ⟨fun i2 => torus i2 ^ w * c i2, ⟨Q, hQdeg, fun i2 => ?_⟩, funext fun i2 => ?_⟩
    · show torus i2 ^ w * c i2 = Q.eval (torus i2)
      rw [hc i2]
      exact (hQeval i2).symm
    · show torus i2 ^ (-(w : ℤ)) * (torus i2 ^ w * c i2) = c i2
      rw [zpow_neg, zpow_natCast, inv_mul_cancel_left₀ (pow_ne_zero w (htne i2))]
  · -- reverse: Laurent symmetrization of `u^{−w}Q(u)`
    rintro ⟨cc, ⟨Q, hQ, hcc⟩, rfl⟩
    have hQe : ∀ z : F, Q.eval z = ∑ m ∈ Finset.range (2 * w + 1), Q.coeff m * z ^ m := by
      intro z
      rcases eq_or_ne Q 0 with rfl | hne
      · simp
      · exact Polynomial.eval_eq_sum_range'
          ((Polynomial.natDegree_lt_iff_degree_lt hne).mpr hQ) z
    refine ⟨Polynomial.C (Q.coeff w) + ∑ d ∈ Finset.range w,
        Polynomial.C (Q.coeff (w + d + 1) + Q.coeff (w - d - 1)) *
          Polynomial.Chebyshev.T F ((d + 1 : ℕ) : ℤ),
      ∑ d ∈ Finset.range w,
        Polynomial.C ((Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) * i_unit) *
          Polynomial.Chebyshev.U F ((d : ℕ) : ℤ), ?_, ?_, fun j => ?_⟩
    · -- `deg f₀ ≤ w`
      refine le_trans (Polynomial.degree_add_le _ _) (max_le ?_ ?_)
      · exact le_trans Polynomial.degree_C_le (by exact_mod_cast Nat.zero_le w)
      · refine le_trans (Polynomial.degree_sum_le _ _) ?_
        refine Finset.sup_le fun d hd => ?_
        have hdw : d < w := Finset.mem_range.mp hd
        have hT : (Polynomial.Chebyshev.T F ((d + 1 : ℕ) : ℤ)).degree
            = ((d + 1 : ℕ) : WithBot ℕ) := by
          have h := Polynomial.Chebyshev.degree_T (R := F) ((d + 1 : ℕ) : ℤ)
          rwa [Int.natAbs_natCast] at h
        refine le_trans (Polynomial.degree_mul_le _ _) ?_
        refine le_trans (add_le_add Polynomial.degree_C_le (le_of_eq hT)) ?_
        rw [zero_add]
        exact_mod_cast Nat.succ_le_of_lt hdw
    · -- `deg f₁ < w`
      rcases Nat.eq_zero_or_pos w with rfl | hw
      · rw [Finset.range_zero, Finset.sum_empty, Polynomial.degree_zero]
        exact WithBot.bot_lt_coe _
      · refine lt_of_le_of_lt (Polynomial.degree_sum_le _ _)
          (lt_of_le_of_lt (b := ((w - 1 : ℕ) : WithBot ℕ))
            (Finset.sup_le fun d hd => ?_) ?_)
        · have hdw : d < w := Finset.mem_range.mp hd
          have hU : (Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).degree = ((d : ℕ) : WithBot ℕ) :=
            Polynomial.Chebyshev.degree_U_natCast F d
          refine le_trans (Polynomial.degree_mul_le _ _)
            (le_trans (add_le_add Polynomial.degree_C_le (le_of_eq hU)) ?_)
          rw [zero_add]
          exact_mod_cast (by omega : d ≤ w - 1)
        · exact_mod_cast (by omega : w - 1 < w)
    · -- pointwise identity via center split + Chebyshev semiconjugacies
      have hu : torus j ≠ 0 := htne j
      have hw0 : torus j ^ w ≠ 0 := pow_ne_zero _ hu
      show torus j ^ (-(w : ℤ)) * cc j = _
      rw [hcc j, hQe (torus j), sum_range_center (fun m => Q.coeff m * torus j ^ m) w]
      have hdterm : ∀ d ∈ Finset.range w,
          Q.coeff (w + d + 1) * torus j ^ (w + d + 1)
            + Q.coeff (w - d - 1) * torus j ^ (w - d - 1)
          = torus j ^ w *
              ((Q.coeff (w + d + 1) + Q.coeff (w - d - 1)) *
                  (Polynomial.Chebyshev.T F ((d + 1 : ℕ) : ℤ)).eval ((pt j).1)
                + (pt j).2 * ((Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) * i_unit *
                    (Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).eval ((pt j).1))) := by
        intro d hd
        have hdw : d < w := Finset.mem_range.mp hd
        have hd10 : torus j ^ (d + 1) ≠ 0 := pow_ne_zero _ hu
        have hT : (Polynomial.Chebyshev.T F ((d + 1 : ℕ) : ℤ)).eval ((pt j).1)
            = (torus j ^ (d + 1) + (torus j ^ (d + 1))⁻¹) / 2 := by
          rw [← hchi j, chebyshev_semiconjugacy h2 (torus j) hu (d + 1)]
          simp only [chi]
        have hU : (torus j - (torus j)⁻¹) *
              (Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).eval ((pt j).1)
            = torus j ^ (d + 1) - (torus j ^ (d + 1))⁻¹ := by
          have h := (chebyshev_antisymm h2 (torus j) hu (d + 1)).symm
          rw [show ((d + 1 : ℕ) : ℤ) - 1 = ((d : ℕ) : ℤ) from by push_cast; ring,
            hchi j] at h
          rw [h, inv_pow]
        have hsplit : torus j ^ (w + d + 1) = torus j ^ w * torus j ^ (d + 1) := by
          rw [← pow_add, Nat.add_assoc]
        have hsplit2 : torus j ^ (w - d - 1) = torus j ^ w * (torus j ^ (d + 1))⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ hd10, ← pow_add]
          congr 1
          omega
        have hyU : (pt j).2 * ((Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) * i_unit *
              (Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).eval ((pt j).1))
            = (Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) *
                (torus j ^ (d + 1) - (torus j ^ (d + 1))⁻¹) * (2 : F)⁻¹ := by
          rw [hy j, div_eq_mul_inv, mul_inv]
          rw [show (torus j - (torus j)⁻¹) * ((2 : F)⁻¹ * i_unit⁻¹) *
                ((Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) * i_unit *
                  (Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).eval ((pt j).1))
              = (Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) * (2 : F)⁻¹ *
                  (i_unit * i_unit⁻¹) *
                  ((torus j - (torus j)⁻¹) *
                    (Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).eval ((pt j).1)) from by ring]
          rw [hU, mul_inv_cancel₀ hi0, mul_one]
          ring
        rw [hT, hyU, hsplit, hsplit2]
        field_simp
        ring
      have hf0e : (Polynomial.C (Q.coeff w) + ∑ d ∈ Finset.range w,
          Polynomial.C (Q.coeff (w + d + 1) + Q.coeff (w - d - 1)) *
            Polynomial.Chebyshev.T F ((d + 1 : ℕ) : ℤ)).eval ((pt j).1)
          = Q.coeff w + ∑ d ∈ Finset.range w,
              (Q.coeff (w + d + 1) + Q.coeff (w - d - 1)) *
                (Polynomial.Chebyshev.T F ((d + 1 : ℕ) : ℤ)).eval ((pt j).1) := by
        rw [Polynomial.eval_add, Polynomial.eval_C, Polynomial.eval_finset_sum]
        exact congrArg _ (Finset.sum_congr rfl fun d _ => by
          rw [Polynomial.eval_mul, Polynomial.eval_C])
      have hf1e : (∑ d ∈ Finset.range w,
          Polynomial.C ((Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) * i_unit) *
            Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).eval ((pt j).1)
          = ∑ d ∈ Finset.range w,
              (Q.coeff (w + d + 1) - Q.coeff (w - d - 1)) * i_unit *
                (Polynomial.Chebyshev.U F ((d : ℕ) : ℤ)).eval ((pt j).1) := by
        rw [Polynomial.eval_finset_sum]
        exact Finset.sum_congr rfl fun d _ => by
          rw [Polynomial.eval_mul, Polynomial.eval_C]
      rw [Finset.sum_congr rfl hdterm, ← Finset.mul_sum, Finset.sum_add_distrib,
        ← Finset.mul_sum, hf0e, hf1e, zpow_neg, zpow_natCast,
        inv_mul_eq_iff_eq_mul₀ hw0]
      ring

/-- **The previous `lem_circle_rs` skeleton statement was false.**  Without the
odd-characteristic hypothesis `(2 : F) ≠ 0`, the statement of `lem_circle_rs` (as it
stood before the repair) admits the counterexample `F = ZMod 2`, `ι = Fin 2`,
`pt = ![(0,1), (1,0)]`, `i_unit = 1`, `torus ≡ 1`, `w = 1`: all hypotheses hold
(`1² = −1` in `ZMod 2`), the circle code contains the non-constant word `![0, 1]`
(via `f₀ = X`, `f₁ = 0`), but `torus ≡ 1` collapses the right-hand side to the
constant words.  The paper is not affected: it carries `p ≡ 3 (mod 4)` throughout
(tex/cs25_cap_v12.tex `sec:circle-geometry` preamble and `lem:circle-rs`), so the
missing hypothesis was a formalization omission.  Stated over `Type` (universe 0),
which suffices to refute the universe-polymorphic skeleton. -/
theorem lem_circle_rs_false :
    ¬ ∀ (κ K : Type) [Fintype κ] [Field K] [Fintype K]
        (pt : κ → K × K) (torus : κ → K) (w : ℕ)
        (i_unit : K), i_unit ^ 2 = -1 →
        (∀ j, (pt j).1 ^ 2 + (pt j).2 ^ 2 = 1) →
        (∀ j, torus j = (pt j).1 + i_unit * (pt j).2) →
        (∀ j, torus j ≠ 0) →
        circleCode pt w
          = (fun c i => (torus i) ^ (-(w : ℤ)) * c i) '' RSpoly torus (2 * w + 1) := by
  intro h
  have key := h (Fin 2) (ZMod 2)
    ![((0 : ZMod 2), (1 : ZMod 2)), ((1 : ZMod 2), (0 : ZMod 2))]
    (fun _ => 1) 1 1 (by decide)
    (by decide) (by decide) (by decide)
  have hmem : (![0, 1] : Fin 2 → ZMod 2) ∈ circleCode
      ![((0 : ZMod 2), (1 : ZMod 2)), ((1 : ZMod 2), (0 : ZMod 2))] 1 := by
    refine ⟨Polynomial.X, 0, ?_, ?_, fun i => ?_⟩
    · simpa using Polynomial.degree_X_le
    · rw [Polynomial.degree_zero]
      exact WithBot.bot_lt_coe _
    · fin_cases i <;> simp
  rw [key] at hmem
  obtain ⟨cc, ⟨Q, hQ, hcc⟩, hfun⟩ := hmem
  have h0 := congrFun hfun 0
  have h1 := congrFun hfun 1
  have hconst : cc 0 = cc 1 := by rw [hcc 0, hcc 1]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, one_zpow,
    one_mul] at h0 h1
  rw [hconst, h1] at h0
  exact one_ne_zero h0

/-- **`cor:circle-grand` — universal circle-row cap.**

Assembling `lem_circle_rs` (list-size equality) with the map-smooth universal cap on
the torus domain, every circle-FRI line-round row is unsafe at its first staircase
step: for `C = 𝒞_w(F, E)` of odd RS dimension `k = 2w+1` under the field-size
hypothesis, `ε_mca(C, δ)` exceeds the threshold across the deep band.  Stated here for
the uniformized RS code.  (The `hsmooth` input is constructible for twin cosets
via `lem_torus_fibers`.)

Statement-hygiene repair 1 (lane-17 packet; untied-binder defect class, graded
PLAUSIBLE — no counterexample constructed, so no falsity claim): the original
skeleton took `B : Subfield F` and used `Fintype.card B` in `hyp`, but had **no
hypothesis tying `torus` to `B`**.  Its model `thm_phi_cap` (Fiber.lean) requires
the domain to be `B`-valued, and the paper instantiates a `B`-valued domain;
shrinking `B` weakens `hyp` while the fiber pigeonhole needs `B`-valued slopes, so
the untied statement is likely unprovable.  `htorusB` restores the tie.

Statement-hygiene repair 2 (this packet; cast-semantics defect class, graded
PLAUSIBLE claim-widening — no falsity claim): the previous `hδlo` read
`1 - (a * (k / a + 2) : ℝ) / n ≤ δ`, whose `k / a` elaborates as **real** division
(endpoint `1 − (k+2a)/n`), while `hyp` uses `Nat.choose N (k / a + 2)` with
**floor** division (`ℓ₂ = ⌊k/a⌋ + 2`, `A₂ = a·ℓ₂`).  Two different `ℓ₂` semantics
in one statement: since `a ∤ k` always here (`k` odd, `a` even in every 2-power
instantiation), `A₂ ≤ k + 2a − 1 < k + 2a`, so the real-division band started a
sliver *below* the paper's certified endpoint `1 − A₂/n_c` (tex `cor:circle-grand`(b)
`:4015`, and the parity note `:4010`); the fiber list does not reach those radii and
`emcaErr` is increasing in `δ`, so the widened claim is not provable by the paper
route.  Repaired to the `ℕ`-cast `1 - ((a * (k / a + 2) : ℕ) : ℝ) / n ≤ δ`,
matching the correct pattern of `thm_phi_cap`'s `hδlo` (`A₂ : ℕ` bound by
`hA₂ : A₂ = a * ℓ₂`).

Proved (census 1 → 0 for this file): `lem_phi_fiber_ii` at `φ = Xᵃ` — the
divisibility-free route is forced, `a ∤ k` (paper cor:circle-grand(b)) — with
`hQB` discharged by `Subfield` power-closure on `htorusB`; `hℓ₂N` is derived from
`hyp` (a binomial `≥ 2` forces `ℓ₂ < N`); then `hasList_fiber_input` and
`universal_cap_emca_of_fiber_list` close at any `δ < 1 − ρ`. -/
theorem cor_circle_grand (torus : ι → F) (hdom : Function.Injective torus)
    (B : Subfield F) [Fintype B] (htorusB : ∀ i, torus i ∈ B) {w N a k : ℕ}
    (hk : k = 2 * w + 1) (ha : 0 < a) (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth torus (fun x => x ^ a) a)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose N (k / a + 2) : ℝ))
    (δ : ℝ) (hδlo : 1 - ((a * (k / a + 2) : ℕ) : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < emcaErr (RSpoly torus k) δ := by
  classical
  have hk0 : 0 < k := by omega
  have hF0 : (0 : ℝ) < Fintype.card F := lt_of_le_of_lt (Nat.cast_nonneg _) hq
  have hBR : (0 : ℝ) < Fintype.card B := by exact_mod_cast Fintype.card_pos
  have hB1 : (1 : ℝ) ≤ Fintype.card B := by exact_mod_cast Fintype.card_pos
  have hqk : (0 : ℝ) < (Fintype.card F : ℝ) / k := div_pos hF0 (by exact_mod_cast hk0)
  -- `hyp` forces a genuinely large binomial, hence `ℓ₂ ≤ N - 1`
  have hchoose2 : 2 ≤ Nat.choose N (k / a + 2) := by
    by_contra hcon
    push_neg at hcon
    have h1 : (Nat.choose N (k / a + 2) : ℝ) ≤ 1 := by
      exact_mod_cast Nat.lt_succ_iff.mp hcon
    have h2 : (1 : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1) :=
      mul_le_mul_of_nonneg_right hB1 (by positivity)
    rw [one_mul] at h2
    linarith
  have hℓ₂N : k / a + 2 ≤ N - 1 := by
    rcases lt_or_ge (k / a + 2) N with hlt | hge
    · omega
    · exfalso
      have hle1 : Nat.choose N (k / a + 2) ≤ 1 := by
        rcases eq_or_lt_of_le hge with heq | hlt2
        · rw [← heq]; simp [Nat.choose_self]
        · simp [Nat.choose_eq_zero_of_lt hlt2]
      omega
  have hN3 : 2 ≤ N - 1 := le_trans (Nat.le_add_left 2 (k / a)) hℓ₂N
  have hn0 : 0 < Fintype.card ι := by
    rw [← haN]
    exact Nat.mul_pos ha (by omega)
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hak : (k : ℝ) < (1 - δ) * Fintype.card ι := by
    have h1 : (k : ℝ) / Fintype.card ι < 1 - δ := by linarith
    calc (k : ℝ) = (k : ℝ) / Fintype.card ι * Fintype.card ι := by
          rw [div_mul_cancel₀ _ (ne_of_gt hnR)]
      _ < (1 - δ) * Fintype.card ι := mul_lt_mul_of_pos_right h1 hnR
  -- instantiate the (repaired, proved) fiber lemma at `φ = Xᵃ`
  have hφdeg : (Polynomial.X ^ a : Polynomial F).natDegree = a := Polynomial.natDegree_X_pow a
  have hsmooth' : DomSmooth torus (fun x => (Polynomial.X ^ a : Polynomial F).eval x) a := by
    simpa using hsmooth
  have hQB : ∀ i, (Polynomial.X ^ a : Polynomial F).eval (torus i) ∈ B := by
    intro i
    simpa using pow_mem (htorusB i) a
  obtain ⟨z, hzB, L, hLge, hlist⟩ :=
    lem_phi_fiber_ii torus hdom B htorusB (Polynomial.X ^ a) ha hφdeg hQB haN hsmooth'
      rfl hℓ₂N rfl
  have hL1 : 1 ≤ L := by
    have h1 : (1 : ℝ) ≤ (Nat.choose N (k / a + 2) : ℝ) / (Fintype.card B : ℝ) := by
      rw [le_div_iff₀ hBR, one_mul]
      have h2 : (Fintype.card B : ℝ) * 1
          ≤ (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1) :=
        mul_le_mul_of_nonneg_left (by linarith) (by positivity)
      rw [mul_one] at h2
      linarith
    exact_mod_cast le_trans h1 hLge
  obtain ⟨P, hPdeg, hPdist, hPclose⟩ := hasList_fiber_input torus hδlo hnR hlist
  exact universal_cap_emca_of_fiber_list torus hdom hk0 δ hak hq Fintype.card_pos hyp
    ⟨fun i => ((Polynomial.X ^ a : Polynomial F).eval (torus i)) ^ (k / a + 2)
        + z * ((Polynomial.X ^ a : Polynomial F).eval (torus i)) ^ (k / a + 2 - 1),
      L, P, hL1, hPdeg, hPdist, hPclose, hLge⟩

/-- **`lem:stereographic` — stereographic uniformization, no `i` required.**

Over every finite field of odd characteristic, the stereographic map identifies the
degree-`≤ w` circle code with a Reed–Solomon code on the stereographic-image domain
`s(E)`, without needing `i ∈ F`.  This yields circle codes (and their universal caps)
over every challenge field.

Statement repair (see `lem_stereographic_false` below): the previous skeleton took
`sdom` and `twist` as **untied binders** — `hchar`/`hcircle` constrained only `F`/`pt`,
and nothing related `sdom` or `twist` to the circle points, so the statement was
false as stated.  The repaired statement ties `sdom` to `pt` via the inverse
stereographic parametrization `x = (1 − s²)/(1 + s²)`, `y = 2s/(1 + s²)` with the
pole exclusion `1 + s² ≠ 0`, and fixes the twist to the explicit denominator power
`(1 + s²)^{−w}` — matching the paper's `d := ((1 + s(P)²)^{−w})_{P∈E}`
(tex/cs25_cap_v12.tex, `lem:stereographic`).  `hcircle` becomes derivable
(`1 + s² = 2/(1 + x)`), so it is dropped.  Proved in full: both directions clear
denominators through the invertible even/odd substitution of the paper's proof —
the monomial `xʲ` contributes `(1−s²)ʲ(1+s²)^{w−j}` and `y·xʲ` contributes
`2s(1−s²)ʲ(1+s²)^{w−1−j}`; no Chebyshev machinery is needed. -/
theorem lem_stereographic (pt : ι → F × F) (w : ℕ)
    (hchar : (2 : F) ≠ 0)
    (sdom : ι → F)
    (hden : ∀ j, 1 + sdom j ^ 2 ≠ 0)
    (hxs : ∀ j, (pt j).1 = (1 - sdom j ^ 2) / (1 + sdom j ^ 2))
    (hys : ∀ j, (pt j).2 = 2 * sdom j / (1 + sdom j ^ 2)) :
    circleCode pt w
      = (fun c i => (1 + sdom i ^ 2) ^ (-(w : ℤ)) * c i) '' RSpoly sdom (2 * w + 1) := by
  classical
  have h1X : ((1 : Polynomial F) - Polynomial.X ^ 2).natDegree ≤ 2 := by
    refine le_trans (Polynomial.natDegree_sub_le _ _) ?_
    simp [Polynomial.natDegree_X_pow]
  have h2X : ((1 : Polynomial F) + Polynomial.X ^ 2).natDegree ≤ 2 := by
    refine le_trans (Polynomial.natDegree_add_le _ _) ?_
    simp [Polynomial.natDegree_X_pow]
  have h1X1 : ((1 : Polynomial F) - Polynomial.X).natDegree ≤ 1 := by
    refine le_trans (Polynomial.natDegree_sub_le _ _) ?_
    simp
  have h2X1 : ((1 : Polynomial F) + Polynomial.X).natDegree ≤ 1 := by
    refine le_trans (Polynomial.natDegree_add_le _ _) ?_
    simp
  -- scalar coordinates of the inverse stereographic map
  have h1x : ∀ j, 1 - (pt j).1 = 2 * sdom j ^ 2 / (1 + sdom j ^ 2) := by
    intro j
    rw [hxs j, eq_div_iff (hden j), sub_mul, div_mul_cancel₀ _ (hden j)]
    ring
  have h2x : ∀ j, 1 + (pt j).1 = 2 / (1 + sdom j ^ 2) := by
    intro j
    rw [hxs j, eq_div_iff (hden j), add_mul, div_mul_cancel₀ _ (hden j)]
    ring
  ext c
  constructor
  · -- forward: clear denominators into an explicit `Q` of degree `≤ 2w`
    rintro ⟨f0, f1, hf0, hf1, hc⟩
    have hf0nat : f0.natDegree < w + 1 :=
      Nat.lt_succ_of_le (Polynomial.natDegree_le_iff_degree_le.mpr hf0)
    have hf0eval : ∀ z : F, f0.eval z = ∑ k ∈ Finset.range (w + 1), f0.coeff k * z ^ k :=
      fun z => Polynomial.eval_eq_sum_range' hf0nat z
    have hf1eval : ∀ z : F, f1.eval z = ∑ k ∈ Finset.range w, f1.coeff k * z ^ k := by
      intro z
      rcases eq_or_ne f1 0 with rfl | hne
      · simp
      · exact Polynomial.eval_eq_sum_range'
          ((Polynomial.natDegree_lt_iff_degree_lt hne).mpr hf1) z
    set Q : Polynomial F :=
      (∑ k ∈ Finset.range (w + 1), Polynomial.C (f0.coeff k) *
          ((1 - Polynomial.X ^ 2) ^ k * (1 + Polynomial.X ^ 2) ^ (w - k)))
        + ∑ k ∈ Finset.range w, Polynomial.C (2 * f1.coeff k) *
            (Polynomial.X * ((1 - Polynomial.X ^ 2) ^ k *
              (1 + Polynomial.X ^ 2) ^ (w - 1 - k)))
      with hQdef
    have hbase : ∀ m k : ℕ, (((1 : Polynomial F) - Polynomial.X ^ 2) ^ k *
        ((1 : Polynomial F) + Polynomial.X ^ 2) ^ m).natDegree ≤ 2 * k + 2 * m := by
      intro m k
      refine le_trans Polynomial.natDegree_mul_le ?_
      have ha : (((1 : Polynomial F) - Polynomial.X ^ 2) ^ k).natDegree ≤ k * 2 :=
        le_trans Polynomial.natDegree_pow_le (Nat.mul_le_mul_left k h1X)
      have hb : (((1 : Polynomial F) + Polynomial.X ^ 2) ^ m).natDegree ≤ m * 2 :=
        le_trans Polynomial.natDegree_pow_le (Nat.mul_le_mul_left m h2X)
      omega
    have hQdeg : Q.degree < ((2 * w + 1 : ℕ) : WithBot ℕ) := by
      have hQnat : Q.natDegree ≤ 2 * w := by
        rw [hQdef]
        refine le_trans (Polynomial.natDegree_add_le _ _) (max_le ?_ ?_)
        · refine Polynomial.natDegree_sum_le_of_forall_le _ _ fun k hk => ?_
          have hkw : k < w + 1 := Finset.mem_range.mp hk
          have h1 : (Polynomial.C (f0.coeff k) *
              ((1 - Polynomial.X ^ 2) ^ k *
                (1 + Polynomial.X ^ 2) ^ (w - k)) : Polynomial F).natDegree
              ≤ 0 + (2 * k + 2 * (w - k)) :=
            le_trans Polynomial.natDegree_mul_le
              (add_le_add (Polynomial.natDegree_C _).le (hbase (w - k) k))
          omega
        · refine Polynomial.natDegree_sum_le_of_forall_le _ _ fun k hk => ?_
          have hkw : k < w := Finset.mem_range.mp hk
          have h1 : (Polynomial.C (2 * f1.coeff k) *
              (Polynomial.X * ((1 - Polynomial.X ^ 2) ^ k *
                (1 + Polynomial.X ^ 2) ^ (w - 1 - k))) : Polynomial F).natDegree
              ≤ 0 + (1 + (2 * k + 2 * (w - 1 - k))) :=
            le_trans Polynomial.natDegree_mul_le
              (add_le_add (Polynomial.natDegree_C _).le
                (le_trans Polynomial.natDegree_mul_le
                  (add_le_add Polynomial.natDegree_X_le (hbase (w - 1 - k) k))))
          omega
      refine lt_of_le_of_lt Polynomial.degree_le_natDegree ?_
      exact_mod_cast Nat.lt_succ_of_le hQnat
    have hQeval : ∀ j, Q.eval (sdom j)
        = (1 + sdom j ^ 2) ^ w * (f0.eval ((pt j).1) + (pt j).2 * f1.eval ((pt j).1)) := by
      intro j
      have hD : 1 + sdom j ^ 2 ≠ 0 := hden j
      have hterm0 : ∀ k ∈ Finset.range (w + 1),
          (Polynomial.C (f0.coeff k) *
            ((1 - Polynomial.X ^ 2) ^ k * (1 + Polynomial.X ^ 2) ^ (w - k))).eval (sdom j)
          = (1 + sdom j ^ 2) ^ w * (f0.coeff k * ((pt j).1) ^ k) := by
        intro k hk
        have hkw : k ≤ w := Nat.lt_succ_iff.mp (Finset.mem_range.mp hk)
        have hDk : (1 + sdom j ^ 2) ^ k ≠ 0 := pow_ne_zero _ hD
        have hwk : (1 + sdom j ^ 2) ^ (w - k)
            = (1 + sdom j ^ 2) ^ w * ((1 + sdom j ^ 2) ^ k)⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ hDk, ← pow_add]
          congr 1
          omega
        simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow,
          Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_one, Polynomial.eval_X]
        rw [hwk, hxs j, div_pow]
        field_simp
      have hterm1 : ∀ k ∈ Finset.range w,
          (Polynomial.C (2 * f1.coeff k) *
            (Polynomial.X * ((1 - Polynomial.X ^ 2) ^ k *
              (1 + Polynomial.X ^ 2) ^ (w - 1 - k)))).eval (sdom j)
          = (1 + sdom j ^ 2) ^ w * ((pt j).2 * (f1.coeff k * ((pt j).1) ^ k)) := by
        intro k hk
        have hkw : k < w := Finset.mem_range.mp hk
        have hDk1 : (1 + sdom j ^ 2) ^ (k + 1) ≠ 0 := pow_ne_zero _ hD
        have hwk : (1 + sdom j ^ 2) ^ (w - 1 - k)
            = (1 + sdom j ^ 2) ^ w * ((1 + sdom j ^ 2) ^ (k + 1))⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ hDk1, ← pow_add]
          congr 1
          omega
        simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow,
          Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_one, Polynomial.eval_X]
        rw [hwk, hxs j, hys j, div_pow]
        field_simp
        ring
      rw [hQdef]
      rw [Polynomial.eval_add, Polynomial.eval_finset_sum, Polynomial.eval_finset_sum,
        Finset.sum_congr rfl hterm0, Finset.sum_congr rfl hterm1,
        hf0eval, hf1eval, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum]
      ring
    refine ⟨fun i2 => (1 + sdom i2 ^ 2) ^ w * c i2, ⟨Q, hQdeg, fun i2 => ?_⟩,
      funext fun i2 => ?_⟩
    · show (1 + sdom i2 ^ 2) ^ w * c i2 = Q.eval (sdom i2)
      rw [hc i2]
      exact (hQeval i2).symm
    · show (1 + sdom i2 ^ 2) ^ (-(w : ℤ)) * ((1 + sdom i2 ^ 2) ^ w * c i2) = c i2
      rw [zpow_neg, zpow_natCast, inv_mul_cancel_left₀ (pow_ne_zero w (hden i2))]
  · -- reverse: even/odd split of `Q` through the invertible substitution
    rintro ⟨cc, ⟨Q, hQ, hcc⟩, rfl⟩
    have hQe : ∀ z : F, Q.eval z = ∑ m ∈ Finset.range (2 * w + 1), Q.coeff m * z ^ m := by
      intro z
      rcases eq_or_ne Q 0 with rfl | hne
      · simp
      · exact Polynomial.eval_eq_sum_range'
          ((Polynomial.natDegree_lt_iff_degree_lt hne).mpr hQ) z
    have hbase1 : ∀ m k : ℕ, (((1 : Polynomial F) - Polynomial.X) ^ k *
        ((1 : Polynomial F) + Polynomial.X) ^ m).natDegree ≤ k + m := by
      intro m k
      refine le_trans Polynomial.natDegree_mul_le ?_
      have ha : (((1 : Polynomial F) - Polynomial.X) ^ k).natDegree ≤ k * 1 :=
        le_trans Polynomial.natDegree_pow_le (Nat.mul_le_mul_left k h1X1)
      have hb : (((1 : Polynomial F) + Polynomial.X) ^ m).natDegree ≤ m * 1 :=
        le_trans Polynomial.natDegree_pow_le (Nat.mul_le_mul_left m h2X1)
      omega
    refine ⟨∑ k ∈ Finset.range (w + 1), Polynomial.C (Q.coeff (2 * k) * (2 : F)⁻¹ ^ w) *
        ((1 - Polynomial.X) ^ k * (1 + Polynomial.X) ^ (w - k)),
      ∑ k ∈ Finset.range w, Polynomial.C (Q.coeff (2 * k + 1) * (2 : F)⁻¹ ^ w) *
        ((1 - Polynomial.X) ^ k * (1 + Polynomial.X) ^ (w - 1 - k)), ?_, ?_, fun j => ?_⟩
    · -- `deg f₀ ≤ w`
      rw [← Polynomial.natDegree_le_iff_degree_le]
      refine Polynomial.natDegree_sum_le_of_forall_le _ _ fun k hk => ?_
      have hkw : k < w + 1 := Finset.mem_range.mp hk
      have h1 : (Polynomial.C (Q.coeff (2 * k) * (2 : F)⁻¹ ^ w) *
          ((1 - Polynomial.X) ^ k * (1 + Polynomial.X) ^ (w - k)) : Polynomial F).natDegree
          ≤ 0 + (k + (w - k)) :=
        le_trans Polynomial.natDegree_mul_le
          (add_le_add (Polynomial.natDegree_C _).le (hbase1 (w - k) k))
      omega
    · -- `deg f₁ < w`
      rcases Nat.eq_zero_or_pos w with rfl | hw
      · rw [Finset.range_zero, Finset.sum_empty, Polynomial.degree_zero]
        exact WithBot.bot_lt_coe _
      · refine lt_of_le_of_lt (b := ((w - 1 : ℕ) : WithBot ℕ)) ?_ ?_
        · rw [← Polynomial.natDegree_le_iff_degree_le]
          refine Polynomial.natDegree_sum_le_of_forall_le _ _ fun k hk => ?_
          have hkw : k < w := Finset.mem_range.mp hk
          have h1 : (Polynomial.C (Q.coeff (2 * k + 1) * (2 : F)⁻¹ ^ w) *
              ((1 - Polynomial.X) ^ k *
                (1 + Polynomial.X) ^ (w - 1 - k)) : Polynomial F).natDegree
              ≤ 0 + (k + (w - 1 - k)) :=
            le_trans Polynomial.natDegree_mul_le
              (add_le_add (Polynomial.natDegree_C _).le (hbase1 (w - 1 - k) k))
          omega
        · exact_mod_cast (by omega : w - 1 < w)
    · -- pointwise identity via parity split
      have hD : 1 + sdom j ^ 2 ≠ 0 := hden j
      have hDw : (1 + sdom j ^ 2) ^ w ≠ 0 := pow_ne_zero _ hD
      have h2w : (2 : F) ^ w ≠ 0 := pow_ne_zero _ hchar
      show (1 + sdom j ^ 2) ^ (-(w : ℤ)) * cc j = _
      rw [hcc j, hQe (sdom j), sum_range_parity (fun m => Q.coeff m * sdom j ^ m) w,
        zpow_neg, zpow_natCast, inv_mul_eq_iff_eq_mul₀ hDw]
      have heval0 : (∑ k ∈ Finset.range (w + 1),
          Polynomial.C (Q.coeff (2 * k) * (2 : F)⁻¹ ^ w) *
            ((1 - Polynomial.X) ^ k * (1 + Polynomial.X) ^ (w - k))).eval ((pt j).1)
          = ∑ k ∈ Finset.range (w + 1), Q.coeff (2 * k) * (2 : F)⁻¹ ^ w *
              ((1 - (pt j).1) ^ k * (1 + (pt j).1) ^ (w - k)) := by
        rw [Polynomial.eval_finset_sum]
        exact Finset.sum_congr rfl fun k _ => by
          simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow,
            Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_one, Polynomial.eval_X]
      have heval1 : (∑ k ∈ Finset.range w,
          Polynomial.C (Q.coeff (2 * k + 1) * (2 : F)⁻¹ ^ w) *
            ((1 - Polynomial.X) ^ k * (1 + Polynomial.X) ^ (w - 1 - k))).eval ((pt j).1)
          = ∑ k ∈ Finset.range w, Q.coeff (2 * k + 1) * (2 : F)⁻¹ ^ w *
              ((1 - (pt j).1) ^ k * (1 + (pt j).1) ^ (w - 1 - k)) := by
        rw [Polynomial.eval_finset_sum]
        exact Finset.sum_congr rfl fun k _ => by
          simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow,
            Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_one, Polynomial.eval_X]
      rw [heval0, heval1, mul_add, Finset.mul_sum, Finset.mul_sum, Finset.mul_sum]
      refine congrArg₂ (· + ·) (Finset.sum_congr rfl fun k hk => ?_)
        (Finset.sum_congr rfl fun k hk => ?_)
      · -- even terms: `q_{2k} s^{2k} = D^w · (q_{2k} 2^{−w} (1−x)^k (1+x)^{w−k})`
        have hkw : k ≤ w := Nat.lt_succ_iff.mp (Finset.mem_range.mp hk)
        have hDk : (1 + sdom j ^ 2) ^ k ≠ 0 := pow_ne_zero _ hD
        have h2k : (2 : F) ^ k ≠ 0 := pow_ne_zero _ hchar
        have hwk : (1 + sdom j ^ 2) ^ (w - k)
            = (1 + sdom j ^ 2) ^ w * ((1 + sdom j ^ 2) ^ k)⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ hDk, ← pow_add]
          congr 1
          omega
        have h2wk : (2 : F) ^ (w - k) = (2 : F) ^ w * ((2 : F) ^ k)⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ h2k, ← pow_add]
          congr 1
          omega
        rw [h1x j, h2x j, div_pow, div_pow, hwk, h2wk, inv_pow]
        field_simp
        ring
      · -- odd terms: `q_{2k+1} s^{2k+1} = D^w · (y · q_{2k+1} 2^{−w} (1−x)^k (1+x)^{w−1−k})`
        have hkw : k < w := Finset.mem_range.mp hk
        have hDk1 : (1 + sdom j ^ 2) ^ (k + 1) ≠ 0 := pow_ne_zero _ hD
        have h2k1 : (2 : F) ^ (k + 1) ≠ 0 := pow_ne_zero _ hchar
        have hwk : (1 + sdom j ^ 2) ^ (w - 1 - k)
            = (1 + sdom j ^ 2) ^ w * ((1 + sdom j ^ 2) ^ (k + 1))⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ hDk1, ← pow_add]
          congr 1
          omega
        have h2wk : (2 : F) ^ (w - 1 - k) = (2 : F) ^ w * ((2 : F) ^ (k + 1))⁻¹ := by
          rw [eq_mul_inv_iff_mul_eq₀ h2k1, ← pow_add]
          congr 1
          omega
        rw [h1x j, h2x j, hys j, div_pow, div_pow, hwk, h2wk, inv_pow]
        field_simp
        ring

/-- `5` is prime — file-local instance so that `ZMod 5` is a field in the
counterexample below (Mathlib only registers `2` and `3` globally). -/
private instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩

/-- **The previous `lem_stereographic` skeleton statement was false.**  Its binders
`sdom` and `twist` were untied to `pt` (`hchar`/`hcircle` constrain only `F`/`pt`),
so the statement admits the counterexample `F = ZMod 5`, `ι = Fin 2`,
`pt = const (1,0)`, `w = 0`, `sdom = 0`, `twist = ![1, 2]`: the left side is the set
of constant words, while the right side `{i ↦ twist i · Q.eval 0}` contains
non-constant words and misses the constant word `1` (it would need
`κ = 1` and `2κ = 1` simultaneously in `ZMod 5`).  See the repaired
`lem_stereographic` above, which ties `sdom` to the stereographic coordinate of `pt`
with pole exclusion and fixes `twist` to the explicit denominator power, per
tex/cs25_cap_v12.tex `lem:stereographic`.  Stated over `Type` (universe 0), which
suffices to refute the universe-polymorphic skeleton. -/
theorem lem_stereographic_false :
    ¬ ∀ (κ K : Type) [Fintype κ] [Field K] [Fintype K]
        (pt : κ → K × K) (w : ℕ),
        (2 : K) ≠ 0 →
        (∀ j, (pt j).1 ^ 2 + (pt j).2 ^ 2 = 1) →
        ∀ (sdom twist : κ → K), (∀ i, twist i ≠ 0) →
        circleCode pt w = (fun c i => twist i * c i) '' RSpoly sdom (2 * w + 1) := by
  intro h
  have key := h (Fin 2) (ZMod 5) (fun _ => (1, 0)) 0 (by decide) (by decide)
    (fun _ => 0) ![1, 2] (by decide)
  have hmem : (fun _ => (1 : ZMod 5)) ∈ circleCode
      (fun _ : Fin 2 => ((1 : ZMod 5), (0 : ZMod 5))) 0 := by
    refine ⟨Polynomial.C 1, 0, Polynomial.degree_C_le, ?_, fun i => by simp⟩
    rw [Polynomial.degree_zero]
    exact WithBot.bot_lt_coe _
  rw [key] at hmem
  obtain ⟨cc, ⟨Q, hQ, hcc⟩, hfun⟩ := hmem
  have h0 := congrFun hfun 0
  have h1 := congrFun hfun 1
  have hconst : cc 0 = cc 1 := by rw [hcc 0, hcc 1]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, one_mul] at h0 h1
  rw [← hconst, h0] at h1
  exact absurd h1 (by decide)

end RSCap
