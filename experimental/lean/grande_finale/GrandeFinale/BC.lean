import Mathlib
import GrandeFinale

/-!
# The BC program: base-field-normalized split-pencil census (`grande_finale.tex`, `\S`"Proved Prefix and Split-Pencil Reductions")

This file formalizes the *theorem-level*, self-contained parts of the BC program
of the manuscript — the proved reductions that surround the open conjecture BC
(`conj:BC`, "base-field-normalized split-pencil census").  BC itself is a
genuinely open research conjecture: it is an asymptotic `e^{o(n)}` census bound on
the number of primitive split locators in each affine pencil (plus finite
row-wise constants at the deployed rows), and it is *not* a self-contained
theorem.  What is proved here are the surrounding reductions that the manuscript
records as already theorem-level:

* the slope-elimination uniqueness kernel: a non-common support carries at most
  one finite slope (`prop:slope-elimination`);
* the near-rational lattice dichotomy kernels — the parameter-space dimension
  identity `(ω-d₁+1)+(ω-d₂+1) = ω-w+1` and the binomial census count
  `binom(n-d₁, m)` (`thm:near-rational`);
* the MDS decoding-uniqueness kernel behind the near-rational uniqueness
  argument (two degree-`<K` codewords agreeing on `≥ K` points coincide);
* the near-rational-line algebraic identity and the Hamming subadditivity bound
  used by the support-wise two-anchor theorem; these kernels alone do not
  identify a paid owner (`cor:near-rational-line`);
* the deficiency-one eliminant kernels: the remainder-vanishing split test and
  the eliminant degree bound `j + (n-j+1)·j` (`thm:deficiency-one-eliminant`);
* the split-chart tangent-slope cap `#slopes ≤ |T*|` (`prop:split-chart-tangent`);
* the base-field pigeonhole census count `N·binom(m_{d₁}, m)`
  (`prop:base-field-floor`);
* the extension-valued distinct-slope kernels: the root-count-per-collision bound,
  the distinct-value lower bound, and the pole-averaging selection
  (`prop:rank-one-distinct-slope-floor`, `prop:rank-one-floor`).

Each declaration references the `\label{...}` of the manuscript statement it
formalizes.
-/

open scoped BigOperators
open scoped Classical
open Polynomial

namespace GrandeFinale.BC

/-! ## Slope elimination (`prop:slope-elimination`)

For a support `T` that is not common for both `u` and `v`, the residue vector
`(S_r(v,T))_{r<w}` is nonzero, and the slope equation
`(S_r(u,T))_{r<w} + z(S_r(v,T))_{r<w} = 0` forces `z` from any nonzero coordinate.
Hence there is at most one finite slope. -/

/--
Slope-elimination uniqueness (`prop:slope-elimination`).  If the residue vector
`b` is nonzero, then the affine equation `a r + z·b r = 0` (for all coordinates
`r`) has at most one solution `z`: any nonzero coordinate `b r₀` forces
`z = -a r₀ / b r₀`.
-/
theorem slope_elimination_unique {ι F : Type*} [Field F] (a b : ι → F)
    (hb : b ≠ 0) {z1 z2 : F}
    (h1 : ∀ r, a r + z1 * b r = 0) (h2 : ∀ r, a r + z2 * b r = 0) :
    z1 = z2 := by
  refine Classical.not_not.1 fun h => ?_
  obtain ⟨r, hr⟩ := Function.ne_iff.1 hb
  have := h1 r; have := h2 r
  simp_all +decide [add_eq_zero_iff_eq_neg]

/-! ## Near-rational lattice dichotomy (`thm:near-rational`)

The shifted weak-Popov row degrees satisfy `d₁ + d₂ = n - K + 1` (the determinant
degree).  In the interior branch `d₁ ≥ w+1`, the two multipliers `A, B` have
`deg A ≤ ω - d₁` and `deg B ≤ ω - d₂`, so the parameter space has dimension
`(ω-d₁+1) + (ω-d₂+1) = ω - w + 1`.  In the near-rational branch `d₁ ≤ w`, the
valid supports are exactly the `m`-subsets of the `n - d₁` agreement positions. -/

/--
Near-rational parameter-space dimension (`thm:near-rational`, interior branch).
With the determinant-degree relation `d₁ + d₂ = n - K + 1`, `ω = n - m`, and
`w = m - K`, the total number of multiplier coefficients collapses to
`ω - w + 1` (stated over `ℤ` to avoid truncated subtraction).
-/
theorem nearRational_dim_count (n K m d1 d2 ω w : ℤ)
    (hd : d1 + d2 = n - K + 1) (hω : ω = n - m) (hw : w = m - K) :
    (ω - d1 + 1) + (ω - d2 + 1) = ω - w + 1 := by
  grind

/--
Near-rational census count (`thm:near-rational`, near-rational branch).  When the
census is nonempty, the valid size-`m` supports are exactly the `m`-subsets of the
`A = n - d₁` agreement positions, so their number is `binom(|A|, m)`.
-/
theorem nearRational_binomial_count {D : Type*} [DecidableEq D] (A : Finset D) (m : ℕ) :
    (Finset.powersetCard m A).card = A.card.choose m := by
  rw [Finset.card_powersetCard]

/--
MDS decoding uniqueness (`thm:near-rational`, uniqueness step).  Two polynomials
of degree `< K` (codewords of `RS[F,D,K]`) that agree on a support of size at
least `K` are equal.  This is the Reed–Solomon distance argument: two codewords
within distance `w` of `U` would agree on `≥ n - 2w ≥ K` points and hence
coincide.
-/
theorem codeword_agreement_unique {F : Type*} [Field F] {p q : F[X]} {K : ℕ}
    (hp : p.natDegree < K) (hq : q.natDegree < K) {S : Finset F}
    (hS : K ≤ S.card) (hagree : ∀ x ∈ S, p.eval x = q.eval x) : p = q := by
  by_contra h_neq
  have h_roots : S ⊆ (p - q).roots.toFinset := by
    intro x hx; simp_all +decide [sub_eq_iff_eq_add]
  exact absurd (Finset.card_le_card h_roots)
    (not_le.mpr (lt_of_le_of_lt (Multiset.toFinset_card_le _)
      (lt_of_le_of_lt (Polynomial.card_roots' _)
        (lt_of_le_of_lt (Polynomial.natDegree_sub_le _ _) (max_lt hp hq)
          |> lt_of_lt_of_le <| by linarith))))

/-! ## Near-rational structural kernels (`cor:near-rational-line`) -/

/--
Near-rational-line algebraic identity (`cor:near-rational-line`).  If an affine
line `u + z·v` decomposes as `c₁ + e₁` at slope `z₁` and as `c₂ + e₂` at slope
`z₂ ≠ z₁`, then `v` is recovered as
`v = (z₁ - z₂)⁻¹ ((c₁ - c₂) + (e₁ - e₂))`.  Since `c₁ - c₂` is a codeword and
`e₁ - e₂` is small, `v` is close to a codeword.  A chronology-correct payment
requires the separate support-wise two-anchor theorem and its hypotheses.
-/
theorem near_rational_line_algebra {D F : Type*} [Field F]
    (u v c1 c2 e1 e2 : D → F) {z1 z2 : F} (hz : z1 ≠ z2)
    (h1 : ∀ x, u x + z1 * v x = c1 x + e1 x)
    (h2 : ∀ x, u x + z2 * v x = c2 x + e2 x) :
    ∀ x, v x = (z1 - z2)⁻¹ * ((c1 x - c2 x) + (e1 x - e2 x)) := by
  grind

/--
Hamming subadditivity (`cor:near-rational-line`).  If `e₁` is supported on a set
of size `≤ A.card` and `e₂` on a set of size `≤ B.card`, then the difference
`e₁ - e₂` is supported on a set of size at most `A.card + B.card`.  With
`|A|, |B| ≤ w` this gives the distance-`2w` bound for `v`.
-/
theorem support_sub_card_le {D F : Type*} [Field F] [DecidableEq D]
    (e1 e2 : D → F) (s A B : Finset D)
    (hs : ∀ x ∈ s, e1 x - e2 x ≠ 0)
    (h1 : ∀ x, e1 x ≠ 0 → x ∈ A) (h2 : ∀ x, e2 x ≠ 0 → x ∈ B) :
    s.card ≤ A.card + B.card := by
  refine le_trans (Finset.card_le_card ?_) (Finset.card_union_le _ _)
  intro x hx
  by_cases h3 : e1 x = 0 <;> by_cases h4 : e2 x = 0 <;> aesop

/-! ## Deficiency-one split-test eliminant (`thm:deficiency-one-eliminant`) -/

/--
Split-test remainder vanishing (`thm:deficiency-one-eliminant`, split branch).
If the top-chart locator `L` divides the pseudo-division remainder `R` and
`deg R < deg L`, then `R = 0`.  This is the step that turns a top-chart parameter
passing the split test `L_z ∣ Λ_D` into a vanishing eliminant coefficient.
-/
theorem split_test_remainder_zero {F : Type*} [Field F] {L R : F[X]}
    (hdvd : L ∣ R) (hdeg : R.natDegree < L.natDegree) : R = 0 := by
  contrapose! hdeg
  exact Polynomial.natDegree_le_of_dvd hdvd hdeg

/--
Eliminant degree bound (`thm:deficiency-one-eliminant`).  The eliminant
`c_j · R_m` has degree at most `j + (n-j+1)·j`, since `deg c_j ≤ j` (a `j×j`
minor of an affine-linear pencil) and each pseudo-division remainder coefficient
has `Z`-degree at most `(n-j+1)·j`.
-/
theorem deficiency_one_degree_bound {F : Type*} [Field F] {cj Rm : F[X]} {j n : ℕ}
    (hcj : cj.natDegree ≤ j) (hRm : Rm.natDegree ≤ (n - j + 1) * j) :
    (cj * Rm).natDegree ≤ j + (n - j + 1) * j :=
  le_trans (Polynomial.natDegree_mul_le ..) (add_le_add hcj hRm)

/-! ## Split charts are tangent-borne (`prop:split-chart-tangent`) -/

/--
Split-chart tangent-slope cap (`prop:split-chart-tangent`).  On an identically
split chart with fixed root set `T*`, every MCA-bad finite slope equals a tangent
ratio `-e_f(x)/e_g(x)` for some `x ∈ T*`.  Hence the number of bad slopes is at
most `|T*| = j`.
-/
theorem split_chart_tangent_slope_bound {D F : Type*} [DecidableEq F]
    (Tstar : Finset D) (ratio : D → F) (Z : Finset F)
    (hZ : ∀ z ∈ Z, ∃ x ∈ Tstar, z = ratio x) :
    Z.card ≤ Tstar.card := by
  refine le_trans (Finset.card_le_card (show Z ⊆ Finset.image ratio Tstar from ?_))
    Finset.card_image_le
  intro z hz
  obtain ⟨x, hx, rfl⟩ := hZ z hz
  exact Finset.mem_image_of_mem _ hx

/-! ## Interior base-field split-pencil floor (`prop:base-field-floor`) -/

/--
Base-field census count (`prop:base-field-floor`).  For a family `𝒢` of prefix
supports, each of size `m_{d₁}`, the number of agreement-support pairs `(M', T)`
with `T ⊆ M'` and `|T| = m` is `|𝒢| · binom(m_{d₁}, m)`.  Combined with the
pigeonhole floor `|𝒢| ≥ ⌈binom(n, m_{d₁})·b^{-(d₁-1)}⌉`
(`GrandeFinale.prefix_witness_maxfiber`), this is the base-field-normalized census
lower bound.
-/
theorem base_field_floor_count {D : Type*} [DecidableEq D]
    (𝒢 : Finset (Finset D)) (m md1 : ℕ) (hcard : ∀ M' ∈ 𝒢, M'.card = md1) :
    ∑ M' ∈ 𝒢, (Finset.powersetCard m M').card = 𝒢.card * md1.choose m := by
  rw [Finset.sum_congr rfl fun x hx => by rw [Finset.card_powersetCard, hcard x hx]]
  simp +decide

/-! ## Extension-valued distinct-slope rank-one floor (`prop:rank-one-distinct-slope-floor`) -/

/--
Root-count-per-collision bound (`prop:rank-one-distinct-slope-floor`).  For a
nonzero polynomial `p` (here `p = ℓ_S - ℓ_{S'}`, of degree `≤ K-1`), the number
of poles `α ∈ s` with `p(α) = 0` — i.e. the number of poles where two supports
give the same slope — is at most `deg p`.
-/
theorem poly_root_count_bound {F : Type*} [Field F] {p : F[X]} (hp : p ≠ 0)
    (s : Finset F) : (s.filter (fun x => p.eval x = 0)).card ≤ p.natDegree :=
  le_trans (Finset.card_le_card (show _ ⊆ p.roots.toFinset from fun x hx => by aesop))
    (Multiset.toFinset_card_le _) |> le_trans <| Polynomial.card_roots' _

/--
Distinct-value lower bound (`prop:rank-one-distinct-slope-floor`).  For a map `g`
on a finite set `s`, the number of distinct values is at least `|s|` minus the
number of colliding unordered pairs: `|s| ≤ |image g| + ∑_y binom(k_y, 2)`, where
`k_y` is the fiber size of value `y`.  This turns the collision budget into a
distinct-slope count.
-/
theorem distinct_value_lower {ι β : Type*} [DecidableEq β] (s : Finset ι) (g : ι → β) :
    s.card ≤ (s.image g).card
      + ∑ y ∈ s.image g, ((s.filter (fun i => g i = y)).card).choose 2 := by
  have h_card_fibers : s.card = ∑ y ∈ s.image g, (s.filter (fun i => g i = y)).card :=
    Finset.card_eq_sum_card_fiberwise (fun x hx => Finset.mem_image_of_mem g hx)
  rw [h_card_fibers]
  have h_termwise : ∀ y ∈ s.image g,
      (s.filter (fun i => g i = y)).card ≤ 1 + (s.filter (fun i => g i = y)).card.choose 2 := by
    intro y hy
    rcases Finset.card (Finset.filter (fun i => g i = y) s) with (_ | _ | n) <;>
      simp +arith +decide [Nat.choose]
  simpa [Finset.sum_add_distrib] using Finset.sum_le_sum h_termwise

/--
Pole-averaging selection (`prop:rank-one-distinct-slope-floor`, `prop:rank-one-floor`).
If the total collision count over the allowed poles `P` is at most `total`, then
some pole `α ∈ P` has collision count at most `total / |P|`, i.e.
`|P| · col α ≤ total`.  This selects the extension pole with few colliding
support-pairs.
-/
theorem pole_averaging_select {A : Type*} (P : Finset A) (hP : P.Nonempty)
    (col : A → ℕ) (total : ℕ) (hcol : ∑ α ∈ P, col α ≤ total) :
    ∃ α ∈ P, P.card * col α ≤ total := by
  obtain ⟨α, hα, hmin⟩ := Finset.exists_min_image _ col hP
  exact ⟨α, hα, le_trans (by simpa using Finset.sum_le_sum hmin) hcol⟩

/-! ## New elements: proper theorems for the former BC cell

The manuscript upgrades the open conjecture BC ("base-field-normalized
split-pencil census") into a family of *proved* statements.  The enumerative
heart is a moving-root incidence bound on one-parameter projective locator
pencils; around it sit the split-pencil dimension bound, the exact saturation
identity that identifies the correct MCA numerator, and the line-ray
bookkeeping.  This section formalizes those new elements. -/

/-! ### The moving-root incidence bound (`thm:bc-moving-root`)

For a projective locator pencil `L_[s:t] = s·A + t·B` over a domain `D` with
fixed `D`-part `G = gcd(A,B,Λ_D)`, each *moving* domain point `x ∈ D ∖ Z(G)`
has `(A(x),B(x)) ≠ (0,0)`, so the homogeneous equation `s·A(x)+t·B(x)=0` has a
unique projective solution `[s:t]`.  Hence a moving point is a root of at most
one pencil member.  If each counted slope `λ` carries at least `h` moving roots,
the incidence count `I` satisfies `h·|Z| ≤ |I| ≤ |D ∖ Z(G)| = n - g`.

The self-contained combinatorial kernel is the following: a family of pairwise
*disjoint* index sets (`inc λ` = the moving roots assigned to slope `λ`), each of
size at least `h` and all contained in the moving-point set `Pts`, forces
`|Z|·h ≤ |Pts|`. -/

/-
Moving-root incidence bound (`thm:bc-moving-root`, counting kernel).  If the sets
`inc λ` (`λ ∈ Z`) are pairwise disjoint, each contained in `Pts`, and each has at
least `h` elements, then `|Z|·h ≤ |Pts|`.  Instantiated with `Pts = D ∖ Z(G)`
(size `n - g`) and `h` moving roots per counted slope, this is the incidence
bound `h·|𝒵| ≤ n - g` of the moving-root theorem.
-/
theorem bc_moving_root {α β : Type*} [DecidableEq β]
    (Z : Finset α) (Pts : Finset β) (h : ℕ) (inc : α → Finset β)
    (hsub : ∀ a ∈ Z, inc a ⊆ Pts)
    (hdisj : (Z : Set α).PairwiseDisjoint inc)
    (hh : ∀ a ∈ Z, h ≤ (inc a).card) :
    Z.card * h ≤ Pts.card := by
      have h_count : (Finset.biUnion Z inc).card ≤ Pts.card := by
        exact Finset.card_le_card ( Finset.biUnion_subset.mpr hsub );
      rw [ Finset.card_biUnion ] at h_count;
      · exact le_trans ( by simpa using Finset.sum_le_sum hh ) h_count;
      · exact hdisj

/-
Moving-root division form (`thm:bc-moving-root`, `cor:bc-one-pencil`).  Under the
same disjoint-incidence hypotheses with `1 ≤ h`, the number of counted slopes is
at most `⌊|Pts| / h⌋`.  With `|Pts| = n - g` and `h = ω - g` this is the
corollary bound `|𝒵| ≤ ⌊(n-g)/(ω-g)⌋`.
-/
theorem bc_moving_root_div {α β : Type*} [DecidableEq β]
    (Z : Finset α) (Pts : Finset β) (h : ℕ) (hh1 : 1 ≤ h) (inc : α → Finset β)
    (hsub : ∀ a ∈ Z, inc a ⊆ Pts)
    (hdisj : (Z : Set α).PairwiseDisjoint inc)
    (hh : ∀ a ∈ Z, h ≤ (inc a).card) :
    Z.card ≤ Pts.card / h := by
      rw [Nat.le_div_iff_mul_le hh1]
      exact bc_moving_root Z Pts h inc hsub hdisj hh

/-- Primitive one-parameter BC pencil floor at the KoalaBear MCA row
(`cor:bc-one-pencil`): with `n = 2^21` and `ω = n - m = 980104`, the floor
`⌊n/ω⌋ = 2`, so a primitive one-parameter pencil contributes at most two finite
bad slopes. -/
theorem bc_one_pencil_floor_KB : (2097152 : ℕ) / 980104 = 2 := by native_decide

/-- Primitive one-parameter BC pencil floor at the Mersenne-31 MCA row
(`cor:bc-one-pencil`): with `n = 2^21` and `ω = n - m = 980128`, the floor
`⌊n/ω⌋ = 2`. -/
theorem bc_one_pencil_floor_M31 : (2097152 : ℕ) / 980128 = 2 := by native_decide

/-! ### Projective locator pencil and its fixed `D`-part (`def:projective-locator-pencil`) -/

/--
The fixed `D`-part of a projective locator pencil (`def:projective-locator-pencil`):
`G_D(A,B) = gcd(gcd(A,B), Λ_D)`.  Its roots are the common roots of every pencil
member `s·A + t·B`. -/
noncomputable def commonDPart {F : Type*} [Field F] (A B lamD : F[X]) : F[X] :=
  gcd (gcd A B) lamD

/-
Every member of a projective locator pencil is divisible by the fixed `D`-part
(`def:projective-locator-pencil`).  Hence a root of `G_D(A,B)` is a common root of
every member `s·A + t·B`, i.e. a *fixed* (non-moving) root.
-/
theorem commonDPart_dvd_pencil {F : Type*} [Field F] (A B lamD : F[X]) (s t : F) :
    commonDPart A B lamD ∣ (Polynomial.C s * A + Polynomial.C t * B) := by
      exact dvd_add ( dvd_mul_of_dvd_right ( GCDMonoid.gcd_dvd_left _ _ |> dvd_trans <| GCDMonoid.gcd_dvd_left _ _ ) _ ) ( dvd_mul_of_dvd_right ( GCDMonoid.gcd_dvd_left _ _ |> dvd_trans <| GCDMonoid.gcd_dvd_right _ _ ) _ )

/-! ### Split-pencil dimension bound (`thm:bc-proper`) -/

/-
Split-pencil dimension bound (`thm:bc-proper`, coefficient-count kernel).  Each
size-`m` agreement support in the profile is represented by a coefficient pair
`(A, B)` with `deg A ≤ ω - d₁` (`r₁` coefficients) and `deg B ≤ ω - d₂` (`r₂`
coefficients).  If the representation map `φ` is injective on the census, then the
number of supports is at most `|F|^{r₁+r₂}`.
-/
theorem bc_dimension_bound {S F : Type*} [Fintype F] [DecidableEq F]
    (census : Finset S) (r1 r2 : ℕ) (φ : S → (Fin r1 → F) × (Fin r2 → F))
    (hφ : Set.InjOn φ census) :
    census.card ≤ (Fintype.card F) ^ (r1 + r2) := by
      have h_card_image : census.card ≤ (Finset.image φ census).card := by
        rw [ Finset.card_image_of_injOn hφ ];
      exact h_card_image.trans ( le_trans ( Finset.card_le_univ _ ) ( by simp +decide [ pow_add ] ) )

/-! ### Exact saturation identity (`thm:saturation`) -/

/-
Exact saturation identity (`thm:saturation`).  The support-locator census
`Cen(U;m)` is the disjoint union, over codewords `c`, of the `m`-subsets of the
agreement set `S c`.  Its cardinality is therefore `∑_c binom(s_c(U), m)`, where
`s_c(U) = |S c|`.  The fiber above a fixed codeword ray `c` has size
`binom(s_c(U), m)`.
-/
theorem saturation_identity {D C : Type*} [DecidableEq D]
    (Cf : Finset C) (S : C → Finset D) (m : ℕ) :
    (Cf.sigma (fun c => (S c).powersetCard m)).card = ∑ c ∈ Cf, (S c).card.choose m := by
  aesop

/-
Raw support BC is not the MCA object (`cor:raw-bc-fails`).  If `U` saturates a
single codeword ray `c₀` (with `s_{c₀} = n - d ≥ m`) and no other codeword on `m`
or more positions, then the raw support-locator census collapses to a single
binomial `binom(n-d, m)` — exponentially larger than the one MCA bad slope it
represents.
-/
theorem raw_bc_single_ray {D C : Type*} [DecidableEq D]
    (Cf : Finset C) (S : C → Finset D) (m : ℕ) (c0 : C) (hc0 : c0 ∈ Cf)
    (hother : ∀ c ∈ Cf, c ≠ c0 → (S c).card < m) :
    ∑ c ∈ Cf, (S c).card.choose m = (S c0).card.choose m := by
      rw [ Finset.sum_eq_single c0 ] <;> simp_all +decide [ Nat.choose_eq_zero_of_lt ]

/-! ### Line-ray saturation identity (`prop:line-ray-saturation`) -/

/-
Line-ray saturation identity (`prop:line-ray-saturation`).  Summing the
saturation identity over a set `E` of finite slopes, the total support census
`∑_{z∈E} Cen(U_z;m)` equals the sum of `binom(s_{z,c}, m)` over the line rays —
the pairs `(z,c)` with agreement `s_{z,c} ≥ m` — since terms with `s_{z,c} < m`
vanish.
-/
theorem line_ray_saturation {D E C : Type*} [DecidableEq D]
    (Ef : Finset E) (Cf : Finset C) (S : E → C → Finset D) (m : ℕ) :
    ∑ z ∈ Ef, ∑ c ∈ Cf, (S z c).card.choose m
      = ∑ p ∈ (Ef ×ˢ Cf).filter (fun p => m ≤ (S p.1 p.2).card),
          (S p.1 p.2).card.choose m := by
            rw [ Finset.sum_filter, Finset.sum_product ];
            exact Finset.sum_congr rfl fun x hx => Finset.sum_congr rfl fun y hy => by split_ifs <;> simp_all +decide [ Nat.choose_eq_zero_of_lt ] ;

/-! ### Johnson packing bound for Q (`thm:q-proper`) -/

/-
Johnson packing kernel (`thm:q-proper`).  Distinct members of a prefix fiber have
Johnson distance at least `w+1` (`prop:prefix-rigidity`), so the radius-`t` Johnson
balls (`t = ⌊w/2⌋`) around fiber members are pairwise disjoint; each ball has the
uniform size `V` and lies inside the ambient set of all `m`-subsets.  Hence
`|Fib_w(z)|·V ≤ binom(n, m)`.  This is the disjoint-uniform-family packing bound.
-/
theorem johnson_packing {D : Type*} [DecidableEq (Finset D)]
    (Fib : Finset (Finset D)) (V : ℕ) (Univ : Finset (Finset D))
    (ball : Finset D → Finset (Finset D))
    (hsub : ∀ M ∈ Fib, ball M ⊆ Univ)
    (hsize : ∀ M ∈ Fib, (ball M).card = V)
    (hdisj : (Fib : Set (Finset D)).PairwiseDisjoint ball) :
    Fib.card * V ≤ Univ.card := by
      have h_union : (Fib.biUnion ball).card ≤ Univ.card := by
        exact Finset.card_le_card ( Finset.biUnion_subset.mpr hsub );
      convert h_union using 1;
      rw [ Finset.card_biUnion hdisj, Finset.sum_congr rfl hsize, Finset.sum_const, smul_eq_mul, mul_comm ]

/-! ### Off-diagonal stratum bound for SP (`thm:sp-proper`) -/

/-
Off-diagonal stratum bound (`thm:sp-proper`, encoding kernel).  An off-diagonal
shift pair at distance `e` is encoded by a common part `R` of size `m-e`, an
`A`-root set of size `e` inside `D ∖ R`, and a `B`-root set of size `e` inside
`D ∖ (R ∪ A)`.  This encoding is injective, so the number of such pairs is at most
`binom(n, m-e) · binom(n-m+e, e) · binom(n-m, e)`.
-/
theorem sp_stratum_bound {D X : Type*} [DecidableEq D]
    (Dset : Finset D) (n m e : ℕ) (hn : Dset.card = n)
    (pairs : Finset X) (R A B : X → Finset D)
    (hR : ∀ p ∈ pairs, R p ⊆ Dset ∧ (R p).card = m - e)
    (hA : ∀ p ∈ pairs, A p ⊆ Dset \ R p ∧ (A p).card = e)
    (hB : ∀ p ∈ pairs, B p ⊆ Dset \ (R p ∪ A p) ∧ (B p).card = e)
    (hinj : ∀ p ∈ pairs, ∀ q ∈ pairs, R p = R q → A p = A q → B p = B q → p = q) :
    pairs.card ≤ n.choose (m - e) * ((n - m + e).choose e) * ((n - m).choose e) := by
  by_contra h;
  have h_inj : pairs.card ≤ Finset.card (Finset.image (fun p => ((R p, A p), B p)) pairs) := by
    rw [ Finset.card_image_of_injOn ];
    exact fun p hp q hq h => hinj p hp q hq ( by aesop ) ( by aesop ) ( by aesop );
  have h_card : Finset.card (Finset.image (fun p => ((R p, A p), B p)) pairs) ≤ Finset.sum (Finset.powersetCard (m - e) Dset) (fun r => Finset.sum (Finset.powersetCard e (Dset \ r)) (fun a => Finset.card (Finset.powersetCard e (Dset \ (r ∪ a))))) := by
    have h_card : Finset.image (fun p => ((R p, A p), B p)) pairs ⊆ Finset.biUnion (Finset.powersetCard (m - e) Dset) (fun r => Finset.biUnion (Finset.powersetCard e (Dset \ r)) (fun a => Finset.image (fun b => ((r, a), b)) (Finset.powersetCard e (Dset \ (r ∪ a)))) ) := by
      grind +splitIndPred;
    exact le_trans ( Finset.card_le_card h_card ) ( Finset.card_biUnion_le.trans <| Finset.sum_le_sum fun r hr => Finset.card_biUnion_le.trans <| Finset.sum_le_sum fun a ha => Finset.card_image_le );
  refine' h ( h_inj.trans ( h_card.trans _ ) );
  refine' le_trans ( Finset.sum_le_sum fun r hr => Finset.sum_le_sum fun a ha => show Finset.card ( Finset.powersetCard e ( Dset \ ( r ∪ a ) ) ) ≤ Nat.choose ( n - m ) e from _ ) _;
  · simp +zetaDelta at *;
    rw [ Finset.card_sdiff ] ; simp +decide [ * ];
    rw [ show ( r ∪ a ) ∩ Dset = r ∪ a from Finset.inter_eq_left.mpr ( Finset.union_subset hr.1 ( ha.1.trans ( Finset.sdiff_subset ) ) ) ] ; rw [ Finset.card_union_of_disjoint ( Finset.disjoint_left.mpr fun x hx₁ hx₂ => by have := ha.1 hx₂; aesop ) ] ; simp +decide [ * ] ;
    by_cases h : m ≤ e <;> simp_all +decide;
    · exact Nat.choose_le_choose _ ( Nat.sub_le_sub_left h _ );
    · rw [ Nat.sub_add_cancel h.le ];
  · simp +decide [ ← Finset.sum_mul _ _ _ ];
    gcongr;
    refine' le_trans ( Finset.sum_le_sum fun x hx => Nat.choose_le_choose _ <| show ( Dset \ x ).card ≤ n - m + e from _ ) _;
    · grind;
    · simp +decide [ ← hn, Finset.card_powersetCard ]

end GrandeFinale.BC
