import cs25_cap_v12.BlueprintCommon

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

Still skeletons (proofs `sorry`):

* `circleCode` and `lem_circle_rs` — `lem:circle-rs`: the degree-`≤ w` circle code
  equals a diagonally twisted Reed–Solomon code `RS[F, E', 2w+1]` on the torus domain,
  hence has identical list sizes and CA/MCA errors.
* `cor_circle_grand` — `cor:circle-grand`: the universal cap for circle-FRI line-round
  rows.
* `lem_stereographic` — `lem:stereographic`: the stereographic uniformization,
  requiring no `i`, giving circle codes over every challenge field.
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
identical `ε_ca`, `ε_mca` at every radius. -/
theorem lem_circle_rs (pt : ι → F × F) (torus : ι → F) (w : ℕ)
    (i_unit : F) (hi : i_unit ^ 2 = -1)
    (hcircle : ∀ j, (pt j).1 ^ 2 + (pt j).2 ^ 2 = 1)
    (htorus : ∀ j, torus j = (pt j).1 + i_unit * (pt j).2) (htne : ∀ j, torus j ≠ 0) :
    circleCode pt w
      = (fun c i => (torus i) ^ (-(w : ℤ)) * c i) '' RSpoly torus (2 * w + 1) := by
  sorry

/-- **`cor:circle-grand` — universal circle-row cap.**

Assembling `lem_circle_rs` (list-size equality) with the map-smooth universal cap on
the torus domain, every circle-FRI line-round row is unsafe at its first staircase
step: for `C = 𝒞_w(F, E)` of odd RS dimension `k = 2w+1` under the field-size
hypothesis, `ε_mca(C, δ)` exceeds the threshold across the deep band.  Stated here for
the uniformized RS code.  (The `hsmooth` input is now constructible for twin cosets
via `lem_torus_fibers`.) -/
theorem cor_circle_grand (torus : ι → F) (hdom : Function.Injective torus)
    (B : Subfield F) [Fintype B] {w N a k : ℕ}
    (hk : k = 2 * w + 1) (ha : 0 < a) (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth torus (fun x => x ^ a) a)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose N (k / a + 2) : ℝ))
    (δ : ℝ) (hδlo : 1 - (a * (k / a + 2) : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < emcaErr (RSpoly torus k) δ := by
  sorry

/-- **`lem:stereographic` — stereographic uniformization, no `i` required.**

Over every finite field of odd characteristic, the stereographic map identifies the
degree-`≤ w` circle code with a Reed–Solomon code on the stereographic-image domain
`s(E)`, without needing `i ∈ F`.  This yields circle codes (and their universal caps)
over every challenge field.  Stated as an equality of the circle code with a twisted
RS code under an explicit stereographic domain `sdom`. -/
theorem lem_stereographic (pt : ι → F × F) (w : ℕ)
    (hchar : (2 : F) ≠ 0)
    (hcircle : ∀ j, (pt j).1 ^ 2 + (pt j).2 ^ 2 = 1)
    (sdom : ι → F) (twist : ι → F) (htw : ∀ i, twist i ≠ 0) :
    circleCode pt w = (fun c i => twist i * c i) '' RSpoly sdom (2 * w + 1) := by
  sorry

end RSCap
